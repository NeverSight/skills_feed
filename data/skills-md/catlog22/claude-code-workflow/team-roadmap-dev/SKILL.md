---
name: team-roadmap-dev
description: Unified team skill for roadmap-driven development workflow. Coordinator discusses roadmap with user, then dispatches phased execution pipeline (plan -> execute -> verify). All roles invoke this skill with --role arg. Triggers on "team roadmap-dev".
allowed-tools: TeamCreate(*), TeamDelete(*), SendMessage(*), TaskCreate(*), TaskUpdate(*), TaskList(*), TaskGet(*), Agent(*), AskUserQuestion(*), Read(*), Write(*), Edit(*), Bash(*), Glob(*), Grep(*)
---

# Team Roadmap Dev

Unified team skill: roadmap-driven development with phased execution pipeline. Coordinator discusses roadmap with the user and manages phase transitions. All team members invoke with `--role=xxx` to route to role-specific execution.

## Architecture Overview

```
+---------------------------------------------------+
|  Skill(skill="team-roadmap-dev")                   |
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
plann-  execu-  verif-
er      tor     ier

(tw) = team-worker agent
```

## Command Architecture

```
roles/
├── coordinator/
│   ├── role.md                # Orchestrator: roadmap discussion + phase management
│   └── commands/
│       ├── roadmap-discuss.md # Discuss roadmap with user, generate phase plan
│       ├── dispatch.md        # Create task chain per phase
│       ├── monitor.md         # Stop-Wait phase execution loop
│       ├── pause.md           # Save state and exit cleanly
│       └── resume.md          # Resume from paused session
├── planner/
│   ├── role.md                # Research + task JSON generation per phase
│   └── commands/
│       ├── research.md        # Context gathering + codebase exploration
│       └── create-plans.md    # action-planning-agent delegation → IMPL-*.json
├── executor/
│   ├── role.md                # Task execution with wave parallelism
│   └── commands/
│       └── implement.md       # Code implementation via code-developer
└── verifier/
    ├── role.md                # Goal-backward verification
    └── commands/
        └── verify.md          # Convergence criteria checking + gap detection
```

## Role Router

### Input Parsing

Parse `$ARGUMENTS` to extract `--role`. If absent → Orchestration Mode (auto route to coordinator). If `--resume` present → coordinator handles resume via commands/resume.md.

### Role Registry

| Role | Spec | Task Prefix | Inner Loop |
|------|------|-------------|------------|
| coordinator | [roles/coordinator/role.md](roles/coordinator/role.md) | (none) | - |
| planner | [role-specs/planner.md](role-specs/planner.md) | PLAN-* | true |
| executor | [role-specs/executor.md](role-specs/executor.md) | EXEC-* | true |
| verifier | [role-specs/verifier.md](role-specs/verifier.md) | VERIFY-* | true |

> **⚠️ COMPACT PROTECTION**: 角色文件是执行文档，不是参考资料。当 context compression 发生后，角色指令仅剩摘要时，**必须立即 `Read` 对应 role.md 重新加载后再继续执行**。不得基于摘要执行任何 Phase。

### Dispatch

1. Extract `--role` from arguments
2. If no `--role` → route to coordinator (Orchestration Mode)
3. Look up role in registry → Read the role file → Execute its phases

### Orchestration Mode

When invoked without `--role`, coordinator auto-starts. User just provides task description.

**Invocation**: `Skill(skill="team-roadmap-dev", args="<task-description>")`

**Lifecycle**:
```
User provides task description
  → coordinator: Roadmap discussion → TeamCreate → Create phase task chain
  → coordinator Phase 4: spawn first batch workers (background) → STOP
  → Worker executes → SendMessage callback → coordinator advances next step
  → Loop until phase pipeline complete → transition to next phase or complete
```

**User Commands** (wake paused coordinator):

| Command | Action |
|---------|--------|
| `check` / `status` | Output execution status graph, no advancement |
| `resume` / `continue` | Check worker states, advance next step |

---

## Shared Infrastructure

### Artifact System

**Fixed Artifacts** (session-level, persist throughout session):

| Artifact | Path | Created By | Purpose |
|----------|------|------------|---------|
| roadmap.md | `<session>/roadmap.md` | coordinator (roadmap-discuss) | Phase plan with requirements and success criteria |
| state.md | `<session>/state.md` | coordinator | Living memory (<100 lines), updated every significant action |
| config.json | `<session>/config.json` | coordinator | Session settings: mode, depth, gates |

**Dynamic Artifacts** (per-phase, form execution history):

| Artifact | Path | Created By | Purpose |
|----------|------|------------|---------|
| context.md | `<session>/phase-N/context.md` | planner (research) | Phase context and requirements |
| IMPL_PLAN.md | `<session>/phase-N/IMPL_PLAN.md` | planner (create-plans) | Implementation overview with task dependency graph |
| IMPL-*.json | `<session>/phase-N/.task/IMPL-*.json` | planner (create-plans) | Task JSON files (unified flat schema with convergence criteria) |
| TODO_LIST.md | `<session>/phase-N/TODO_LIST.md` | planner (create-plans) | Checklist tracking for all tasks |
| summary-{ID}.md | `<session>/phase-N/summary-{IMPL-ID}.md` | executor (implement) | Execution record with requires/provides/convergence-met |
| verification.md | `<session>/phase-N/verification.md` | verifier (verify) | Convergence criteria check results + gap list |

### Init Prerequisite

Coordinator **must** ensure `.workflow/project-tech.json` exists before starting. If not found, invoke `/workflow:init`.

### Team Configuration

| Setting | Value |
|---------|-------|
| Team name | roadmap-dev |
| Session directory | `.workflow/.team/RD-<slug>-<date>/` |
| Message directory | `.workflow/.team-msg/roadmap-dev/` |

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

#### Output Tagging

All outputs must carry `[role_name]` prefix.

#### Coordinator Isolation

| Allowed | Forbidden |
|---------|-----------|
| Discuss roadmap with user (AskUserQuestion) | Direct code writing/modification |
| Create task chain (TaskCreate) | Calling CLI tools for implementation |
| Dispatch tasks to workers | Direct analysis/testing/verification |
| Monitor progress (message bus) | Bypassing workers |
| Report results to user | Modifying source code |

#### Worker Isolation

| Allowed | Forbidden |
|---------|-----------|
| Process own-prefix tasks only | Process other roles' tasks |
| SendMessage to coordinator only | Direct worker-to-worker communication |
| Use Toolbox-declared tools | TaskCreate for other roles |
| Delegate to commands/*.md | Modify resources outside scope |

### Message Bus & Task Lifecycle

Each role's role.md contains self-contained Message Bus and Task Lifecycle. See `roles/<role>/role.md`.

---

## Pipeline

```
Phase N lifecycle:
  Coordinator (roadmap-discuss → dispatch phase N)
    → PLAN-N01: Planner (research → action-planning-agent → IMPL-*.json)
    → EXEC-N01: Executor (load IMPL-*.json → wave-based code-developer)
    → VERIFY-N01: Verifier (convergence criteria check)
    → Coordinator (transition: gap closure or next phase)

Cross-phase flow:
  Init → Roadmap Discussion → Phase 1 → Phase 2 → ... → Phase N → Complete
                                   ↑                          |
                                   └── gap closure loop ──────┘

Session lifecycle:
  Running → Pause (save coordinates) → Resume (re-enter monitor at coordinates)
```

### Cadence Control

**Beat model**: Event-driven, each beat = coordinator wake → process → spawn → STOP. Phase beat: PLAN → EXEC → VERIFY per phase.

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

**Phase beat view**:

```
Single Phase (3 beats, strictly serial)
──────────────────────────────────────────────────────────
Beat  1         2              3
      │         │              │
      PLAN → EXEC ──→ VERIFY
      ▲                        ▲
   phase                    phase
    start                    done

PLAN=planner  EXEC=executor  VERIFY=verifier

Multi-Phase (N x 3 beats, with gap closure loop)
──────────────────────────────────────────────────────────
Phase 1:  PLAN-101 → EXEC-101 → VERIFY-101
                                    │
                              ⏸ CHECKPOINT ── gap closure or next phase
                                    │
Phase 2:  PLAN-201 → EXEC-201 → VERIFY-201
                                    │
                              ⏸ CHECKPOINT
                                    │
Phase N:  PLAN-N01 → EXEC-N01 → VERIFY-N01 → Complete
```

**Checkpoints**:

| Trigger | Location | Behavior |
|---------|----------|----------|
| Phase transition | VERIFY-N01 complete | Evaluate gaps: if gaps found → gap closure loop; if clean → next phase |
| Gap closure limit | 3 iterations | Stop iteration, report current state to user |
| Pipeline stall | No ready + no running | Check missing tasks, report to user |

**Stall Detection** (coordinator `handleCheck` executes):

| Check | Condition | Resolution |
|-------|-----------|------------|
| Worker no response | in_progress task no callback | Report waiting task list, suggest user `resume` |
| Pipeline deadlock | no ready + no running + has pending | Check blockedBy dependency chain, report blocking point |
| Phase verification fails | Gaps detected in VERIFY | Coordinator triggers gap closure loop (max 3 iterations) |

### Task Metadata Registry

| Task ID | Role | Phase | Dependencies | Description |
|---------|------|-------|-------------|-------------|
| PLAN-N01 | planner | phase N | (none or previous VERIFY) | Research + context gathering + task JSON generation |
| EXEC-N01 | executor | phase N | PLAN-N01 | Wave-based code implementation following plans |
| VERIFY-N01 | verifier | phase N | EXEC-N01 | Convergence criteria verification + gap detection |

---

## Coordinator Spawn Template

### v5 Worker Spawn (all roles)

When coordinator spawns workers, use `team-worker` agent with role-spec path:

```
Agent({
  subagent_type: "team-worker",
  description: "Spawn <role> worker",
  team_name: "roadmap-dev",
  name: "<role>",
  run_in_background: true,
  prompt: `## Role Assignment
role: <role>
role_spec: .claude/skills/team-roadmap-dev/role-specs/<role>.md
session: <session-folder>
session_id: <session-id>
team_name: roadmap-dev
requirement: <task-description>
inner_loop: true

Read role_spec file to load Phase 2-4 domain instructions.
Execute built-in Phase 1 (task discovery) -> role-spec Phase 2-4 -> built-in Phase 5 (report).`
})
```

**All roles** (planner, executor, verifier): Set `inner_loop: true`.

---

## Completion Action

When the pipeline completes (all phases done, coordinator Phase 5):

```
AskUserQuestion({
  questions: [{
    question: "Roadmap Dev pipeline complete. What would you like to do?",
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
| Keep Active | Update session status="paused" -> output resume instructions: `Skill(skill="team-roadmap-dev", args="resume")` |
| Export Results | AskUserQuestion for target path -> copy deliverables -> Archive & Clean |

## Session Directory

```
.workflow/.team/RD-<slug>-<date>/
├── roadmap.md                 # Phase plan with requirements
├── state.md                   # Living memory (<100 lines)
├── config.json                # Session settings
├── wisdom/                    # Cross-task knowledge
│   ├── learnings.md
│   ├── decisions.md
│   ├── conventions.md
│   └── issues.md
├── phase-1/                   # Per-phase artifacts
│   ├── context.md
│   ├── IMPL_PLAN.md
│   ├── TODO_LIST.md
│   ├── .task/IMPL-*.json
│   ├── summary-*.md
│   └── verification.md
├── phase-2/
│   └── ...
├── .msg/
│   ├── messages.jsonl              # Team message bus log
│   └── meta.json                   # Session metadata + shared state
```

## Session Resume

Coordinator supports `--resume` / `--continue` for interrupted sessions:

1. Scan `.workflow/.team/RD-*/` for sessions with status "active" or "paused"
2. Multiple matches → AskUserQuestion for selection
3. Audit TaskList → reconcile session state <-> task status
4. Reset in_progress → pending (interrupted tasks)
5. Rebuild team and spawn needed workers only
6. Create missing tasks with correct blockedBy
7. Kick first executable task → Phase 4 coordination loop

## Error Handling

| Scenario | Resolution |
|----------|------------|
| Unknown --role value | Error with available role list |
| Missing --role arg | Orchestration Mode → auto route to coordinator |
| Role file not found | Error with expected path (roles/<name>/role.md) |
| project-tech.json missing | Coordinator invokes /workflow:init |
| Phase verification fails with gaps | Coordinator triggers gap closure loop |
| Max gap closure iterations (3) | Report to user, ask for guidance |
