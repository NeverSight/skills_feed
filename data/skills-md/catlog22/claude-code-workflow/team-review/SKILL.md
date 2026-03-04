---
name: team-review
description: "Unified team skill for code review. Uses team-worker agent architecture with role-spec files. 3-role pipeline: scanner, reviewer, fixer. Triggers on team-review."
allowed-tools: TeamCreate(*), TeamDelete(*), SendMessage(*), TaskCreate(*), TaskUpdate(*), TaskList(*), TaskGet(*), Agent(*), AskUserQuestion(*), Read(*), Write(*), Edit(*), Bash(*), Glob(*), Grep(*), mcp__ace-tool__search_context(*)
---

# Team Review

Unified team skill: code scanning, vulnerability review, optimization suggestions, and automated fix. All team members invoke with `--role=xxx` to route to role-specific execution.

## Architecture

```
+---------------------------------------------------+
|  Skill(skill="team-review")                        |
|  args="<task-description>"                         |
+-------------------+-------------------------------+
                    |
         Orchestration Mode (auto -> coordinator)
                    |
              Coordinator (inline)
              Phase 0-5 orchestration
                    |
    +-------+-------+-------+
    v       v       v
 [tw]    [tw]    [tw]
scann-  review- fixer
er      er

(tw) = team-worker agent
```

## Role Router

### Input Parsing

Parse `$ARGUMENTS` to extract `--role`. If absent → Orchestration Mode (auto route to coordinator).

### Role Registry

| Role | Spec | Task Prefix | Inner Loop |
|------|------|-------------|------------|
| coordinator | [roles/coordinator/role.md](roles/coordinator/role.md) | (none) | - |
| scanner | [role-specs/scanner.md](role-specs/scanner.md) | SCAN-* | false |
| reviewer | [role-specs/reviewer.md](role-specs/reviewer.md) | REV-* | false |
| fixer | [role-specs/fixer.md](role-specs/fixer.md) | FIX-* | true |

> **⚠️ COMPACT PROTECTION**: 角色文件是执行文档，不是参考资料。当 context compression 发生后，角色指令仅剩摘要时，**必须立即 `Read` 对应 role.md 重新加载后再继续执行**。不得基于摘要执行任何 Phase。

### Dispatch

1. Extract `--role` from arguments
2. If no `--role` → route to coordinator (Orchestration Mode)
3. Look up role in registry → Read the role file → Execute its phases

### Orchestration Mode

When invoked without `--role`, coordinator auto-starts. User just provides target description.

**Invocation**: `Skill(skill="team-review", args="<target-path>")`

**Lifecycle**:
```
User provides scan target
  → coordinator Phase 1-3: Parse flags → TeamCreate → Create task chain
  → coordinator Phase 4: spawn first batch workers (background) → STOP
  → Worker executes → SendMessage callback → coordinator advances next step
  → Loop until pipeline complete → Phase 5 report
```

**User Commands** (wake paused coordinator):

| Command | Action |
|---------|--------|
| `check` / `status` | Output execution status graph, no advancement |
| `resume` / `continue` | Check worker states, advance next step |

---

## Pipeline (CP-1 Linear)

```
coordinator dispatch
  → SCAN-* (scanner: toolchain + LLM scan)
  → REV-*  (reviewer: deep analysis + report)
  → [user confirm]
  → FIX-*  (fixer: plan + execute + verify)
```

### Cadence Control

**Beat model**: Event-driven, each beat = coordinator wake → process → spawn → STOP.

```
Beat Cycle (single beat)
═══════════════════════════════════════════════════════════
  Event                   Coordinator              Workers
───────────────────────────────────────────────────────────
  callback/resume ──→ ┌─ handleCallback ─┐
                      │  mark completed   │
                      │  check pipeline   │
                      ├─ handleSpawnNext ─┤
                      │  find ready tasks │
                      │  spawn workers ───┼──→ [Worker A] Phase 1-5
                      └─ STOP (idle) ─────┘         │
                                                     │
  callback ←─────────────────────────────────────────┘
  (next beat)              SendMessage + TaskUpdate(completed)
═══════════════════════════════════════════════════════════
```

**Pipeline beat view**:

```
Review Pipeline (3 beats, linear with user checkpoint)
──────────────────────────────────────────────────────────
Beat  1         2         ⏸         3
      │         │         │         │
      SCAN → REV ──→ [confirm] → FIX
      ▲                              ▲
   pipeline                       pipeline
    start                          done

SCAN=scanner  REV=reviewer  FIX=fixer
```

**Checkpoints**:

| Trigger | Location | Behavior |
|---------|----------|----------|
| Review→Fix transition | REV-* complete | Pause, present review report, wait for user `resume` to confirm fix |
| Quick mode (`-q`) | After SCAN-* | Pipeline ends after scan, no review/fix |
| Fix-only mode (`--fix`) | Entry | Skip scan/review, go directly to fixer |

**Stall Detection** (coordinator `handleCheck` executes):

| Check | Condition | Resolution |
|-------|-----------|------------|
| Worker no response | in_progress task no callback | Report waiting task list, suggest user `resume` |
| Pipeline deadlock | no ready + no running + has pending | Check blockedBy dependency chain, report blocking point |

### Task Metadata Registry

| Task ID | Role | Phase | Dependencies | Description |
|---------|------|-------|-------------|-------------|
| SCAN-001 | scanner | scan | (none) | Toolchain + LLM code scanning |
| REV-001 | reviewer | review | SCAN-001 | Deep analysis and review report |
| FIX-001 | fixer | fix | REV-001 + user confirm | Plan + execute + verify fixes |

---

## Shared Infrastructure

### Worker Phase 1: Task Discovery (shared by all workers)

Every worker executes the same task discovery flow on startup:

1. Call `TaskList()` to get all tasks
2. Filter: subject matches this role's prefix + owner is this role + status is pending + blockedBy is empty
3. No tasks → idle wait
4. Has tasks → `TaskGet` for details → `TaskUpdate` mark in_progress

**Resume Artifact Check** (prevent duplicate output after resume):
- Check whether this task's output artifact already exists
- Artifact complete → skip to Phase 5 report completion
- Artifact incomplete or missing → normal Phase 2-4 execution

### Worker Phase 5: Report (shared by all workers)

Standard reporting flow after task completion:

1. **Message Bus**: Call `mcp__ccw-tools__team_msg` to log message
   - Parameters: operation="log", session_id=<session-id>, from=<role>, type=<message-type>, data={ref: "<artifact-path>"}
   - `to` and `summary` auto-defaulted -- do NOT specify explicitly
   - **CLI fallback**: `ccw team log --session-id <session-id> --from <role> --type <type> --json`
2. **SendMessage**: Send result to coordinator
3. **TaskUpdate**: Mark task completed
4. **Loop**: Return to Phase 1 to check next task

### Wisdom Accumulation (all roles)

Cross-task knowledge accumulation. Coordinator creates `wisdom/` directory at session initialization.

**Directory**:
```
<session-folder>/wisdom/
├── learnings.md      # Patterns and insights
├── decisions.md      # Architecture and design decisions
├── conventions.md    # Codebase conventions
└── issues.md         # Known risks and issues
```

**Worker Load** (Phase 2): Extract `Session: <path>` from task description, read wisdom directory files.
**Worker Contribute** (Phase 4/5): Write this task's discoveries to corresponding wisdom files.

### Role Isolation Rules

| Allowed | Forbidden |
|---------|-----------|
| Process tasks with own prefix | Process tasks with other role prefixes |
| SendMessage to coordinator | Communicate directly with other workers |
| Use tools declared in Toolbox | Create tasks for other roles |
| Delegate to commands/ files | Modify resources outside own responsibility |

Coordinator additional restrictions: Do not write/modify code directly, do not call implementation CLI tools, do not execute analysis/test/review directly.

### Team Configuration

| Setting | Value |
|---------|-------|
| Team name | review |
| Session directory | `.workflow/.team/RV-<slug>-<date>/` |
| Shared memory | `.msg/meta.json` in session dir |
| Team config | `specs/team-config.json` |
| Finding schema | `specs/finding-schema.json` |
| Dimensions | `specs/dimensions.md` |

---

## Coordinator Spawn Template

### v5 Worker Spawn (all roles)

When coordinator spawns workers, use `team-worker` agent with role-spec path:

```
Agent({
  agent_type: "team-worker",
  description: "Spawn <role> worker",
  team_name: "review",
  name: "<role>",
  run_in_background: true,
  prompt: `## Role Assignment
role: <role>
role_spec: .claude/skills/team-review/role-specs/<role>.md
session: <session-folder>
session_id: <session-id>
team_name: review
requirement: <task-description>
inner_loop: <true|false>

Read role_spec file to load Phase 2-4 domain instructions.
Execute built-in Phase 1 (task discovery) -> role-spec Phase 2-4 -> built-in Phase 5 (report).`
})
```

**Inner Loop roles** (fixer): Set `inner_loop: true`.

**Single-task roles** (scanner, reviewer): Set `inner_loop: false`.

## Usage

```bash
# Via coordinator (auto pipeline)
Skill(skill="team-review", args="src/auth/**")                    # scan + review
Skill(skill="team-review", args="--full src/auth/**")             # scan + review + fix
Skill(skill="team-review", args="--fix .review/review-*.json")    # fix only
Skill(skill="team-review", args="-q src/auth/**")                 # quick scan only

# Direct role invocation
Skill(skill="team-review", args="--role=scanner src/auth/**")
Skill(skill="team-review", args="--role=reviewer --input scan-result.json")
Skill(skill="team-review", args="--role=fixer --input fix-manifest.json")

# Flags (all modes)
--dimensions=sec,cor,perf,maint    # custom dimensions (default: all 4)
-y / --yes                         # skip confirmations
-q / --quick                       # quick scan mode
--full                             # full pipeline (scan → review → fix)
--fix                              # fix mode only
```

---

## Completion Action

When the pipeline completes (all tasks done, coordinator Phase 5):

```
AskUserQuestion({
  questions: [{
    question: "Review pipeline complete. What would you like to do?",
    header: "Completion",
    multiSelect: false,
    options: [
      { label: "Archive & Clean (Recommended)", description: "Archive session, clean up tasks and team resources" },
      { label: "Keep Active", description: "Keep session active for follow-up work or inspection" },
      { label: "Export Results", description: "Export deliverables to a specified location, then clean" }
    ]
  }]
})
```

| Choice | Action |
|--------|--------|
| Archive & Clean | Update session status="completed" -> TeamDelete() -> output final summary |
| Keep Active | Update session status="paused" -> output resume instructions: `Skill(skill="team-review", args="resume")` |
| Export Results | AskUserQuestion for target path -> copy deliverables -> Archive & Clean |

---

## Session Directory

```
.workflow/.team/RV-<slug>-<YYYY-MM-DD>/
├── .msg/
│   ├── messages.jsonl          # Message bus log
│   └── meta.json               # Session state + cross-role state
├── wisdom/                     # Cross-task knowledge
│   ├── learnings.md
│   ├── decisions.md
│   ├── conventions.md
│   └── issues.md
├── scan/                       # Scanner output
│   └── scan-results.json
├── review/                     # Reviewer output
│   └── review-report.json
└── fix/                        # Fixer output
    └── fix-manifest.json
```

## Error Handling

| Scenario | Resolution |
|----------|------------|
| Unknown --role value | Error with available role list |
| Missing --role arg | Orchestration Mode → auto route to coordinator |
| Role file not found | Error with expected file path (roles/<name>/role.md) |
| Invalid flags | Warn and continue with defaults |
| No target specified (no --role) | AskUserQuestion to clarify |

## Execution Rules

1. **Parse first**: Extract --role and flags from $ARGUMENTS before anything else
2. **Progressive loading**: Read ONLY the matched role.md, not all four
3. **Full delegation**: Role.md owns entire execution -- do not add logic here
4. **Self-contained**: Each role.md includes its own message bus, task lifecycle, toolbox
5. **DO NOT STOP**: Continuous execution until role completes all 5 phases
