---
name: team-frontend
description: Unified team skill for frontend development. Uses team-worker agent architecture with role-spec files for domain logic. Coordinator orchestrates pipeline, workers are team-worker agents. Built-in ui-ux-pro-max design intelligence. Triggers on "team frontend".
allowed-tools: Agent, TaskCreate, TaskList, TaskGet, TaskUpdate, TeamCreate, TeamDelete, SendMessage, AskUserQuestion, Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch, mcp__ace-tool__search_context
---

# Team Frontend Development

Unified team skill: frontend development with built-in ui-ux-pro-max design intelligence. Covers requirement analysis, design system generation, frontend implementation, and quality assurance. Built on **team-worker agent architecture** -- all worker roles share a single agent definition with role-specific Phase 2-4 loaded from markdown specs.

## Architecture

```
+---------------------------------------------------+
|  Skill(skill="team-frontend")                      |
|  args="<task-description>"                         |
+-------------------+-------------------------------+
                    |
         Orchestration Mode (auto -> coordinator)
                    |
              Coordinator (inline)
              Phase 0-5 orchestration
                    |
    +-------+-------+-------+-------+
    v       v       v       v
 [tw]    [tw]    [tw]    [tw]
analyst  archi-  devel-  qa
         tect    oper

(tw) = team-worker agent
```

## Role Router

This skill is **coordinator-only**. Workers do NOT invoke this skill -- they are spawned as `team-worker` agents directly.

### Input Parsing

Parse `$ARGUMENTS`. No `--role` needed -- always routes to coordinator.

### Role Registry

| Role | Spec | Task Prefix | Type | Inner Loop |
|------|------|-------------|------|------------|
| coordinator | [roles/coordinator/role.md](roles/coordinator/role.md) | (none) | orchestrator | - |
| analyst | [role-specs/analyst.md](role-specs/analyst.md) | ANALYZE-* | read_only_analysis | false |
| architect | [role-specs/architect.md](role-specs/architect.md) | ARCH-* | code_generation | false |
| developer | [role-specs/developer.md](role-specs/developer.md) | DEV-* | code_generation | true |
| qa | [role-specs/qa.md](role-specs/qa.md) | QA-* | read_only_analysis | false |

### Dispatch

Always route to coordinator. Coordinator reads `roles/coordinator/role.md` and executes its phases.

### Orchestration Mode

User just provides task description.

**Invocation**:
```bash
Skill(skill="team-frontend", args="<task-description>")
```

**Lifecycle**:
```
User provides task description
  -> coordinator Phase 1-3: Parse requirements -> TeamCreate -> Create task chain
  -> coordinator Phase 4: spawn first batch workers (background) -> STOP
  -> Worker (team-worker agent) executes -> SendMessage callback -> coordinator advances
  -> GC loop (developer <-> qa) if fix_required (max 2 rounds)
  -> All tasks complete -> Phase 5 report + completion action
```

**User Commands** (wake paused coordinator):

| Command | Action |
|---------|--------|
| `check` / `status` | Output execution status graph, no advancement |
| `resume` / `continue` | Check worker states, advance next step |

---

## Command Execution Protocol

When coordinator needs to execute a command (dispatch, monitor):

1. **Read the command file**: `roles/coordinator/commands/<command-name>.md`
2. **Follow the workflow** defined in the command file (Phase 2-4 structure)
3. **Commands are inline execution guides** -- NOT separate agents or subprocesses
4. **Execute synchronously** -- complete the command workflow before proceeding

Example:
```
Phase 3 needs task dispatch
  -> Read roles/coordinator/commands/dispatch.md
  -> Execute Phase 2 (Context Loading)
  -> Execute Phase 3 (Task Chain Creation)
  -> Execute Phase 4 (Validation)
  -> Continue to Phase 4
```

---

## Coordinator Spawn Template

### v5 Worker Spawn (all roles)

When coordinator spawns workers, use `team-worker` agent with role-spec path:

```
Agent({
  subagent_type: "team-worker",
  description: "Spawn <role> worker",
  team_name: "frontend",
  name: "<role>",
  run_in_background: true,
  prompt: `## Role Assignment
role: <role>
role_spec: .claude/skills/team-frontend/role-specs/<role>.md
session: <session-folder>
session_id: <session-id>
team_name: frontend
requirement: <task-description>
inner_loop: <true|false>

Read role_spec file to load Phase 2-4 domain instructions.
Execute built-in Phase 1 (task discovery) -> role-spec Phase 2-4 -> built-in Phase 5 (report).`
})
```

**Inner Loop roles** (developer): Set `inner_loop: true`. The team-worker agent handles the loop internally.

**Single-task roles** (analyst, architect, qa): Set `inner_loop: false`.

---

## Pipeline Definitions

### Pipeline Diagrams

**Page Mode** (4 beats, linear):
```
Pipeline: Page (Linear)
=====================================================
Stage 1           Stage 2           Stage 3           Stage 4
ANALYZE-001  -->  ARCH-001     -->  DEV-001      -->  QA-001
[analyst]         [architect]       [developer]       [qa]
```

**Feature Mode** (5 beats, with architecture review gate):
```
Pipeline: Feature (Architecture Review Gate)
=====================================================
Stage 1           Stage 2           Stage 3           Stage 4           Stage 5
ANALYZE-001  -->  ARCH-001     -->  QA-001       -->  DEV-001      -->  QA-002
[analyst]         [architect]       [qa:arch-rev]     [developer]       [qa:code-rev]
```

**System Mode** (7 beats, dual-track parallel):
```
Pipeline: System (Dual-Track Parallel)
=====================================================
Stage 1           Stage 2           Stage 3           Stage 4 (parallel)      Stage 5     Stage 6     Stage 7
ANALYZE-001  -->  ARCH-001     -->  QA-001       --> ARCH-002 ─┐         -->  QA-002 -->  DEV-002 --> QA-003
[analyst]         [architect]       [qa:arch-rev]    [architect] |             [qa]        [developer] [qa:final]
                                                     DEV-001  ──┘
                                                     [developer:tokens]
```

### Generator-Critic Loop (developer <-> qa)

```
developer (Generator) -> QA artifact -> qa (Critic)
                      <- QA feedback <-
                         (max 2 rounds)

Convergence: qa.score >= 8 && qa.critical_count === 0
```

---

## Task Metadata Registry

| Task ID | Role | Stage | Dependencies | Description |
|---------|------|-------|-------------|-------------|
| ANALYZE-001 | analyst | analysis | (none) | Requirement analysis + design intelligence |
| ARCH-001 | architect | design | ANALYZE-001 | Design token system + component architecture |
| ARCH-002 | architect | design | QA-001 (system) | Component specs refinement |
| DEV-001 | developer | impl | ARCH-001 or QA-001 | Frontend implementation |
| DEV-002 | developer | impl | QA-002 (system) | Component implementation |
| QA-001 | qa | review | ARCH-001 or DEV-001 | Architecture or code review |
| QA-002 | qa | review | DEV-001 | Code review |
| QA-003 | qa | review | DEV-002 (system) | Final quality check |

---

## ui-ux-pro-max Integration

### Design Intelligence Engine

Analyst role invokes ui-ux-pro-max via Skill to obtain industry design intelligence:

| Action | Invocation |
|--------|------------|
| Full design system | `Skill(skill="ui-ux-pro-max", args="<industry> <keywords> --design-system")` |
| Domain search | `Skill(skill="ui-ux-pro-max", args="<query> --domain <domain>")` |
| Tech stack guidance | `Skill(skill="ui-ux-pro-max", args="<query> --stack <stack>")` |

**Supported Domains**: product, style, typography, color, landing, chart, ux, web
**Supported Stacks**: html-tailwind, react, nextjs, vue, svelte, shadcn, swiftui, react-native, flutter

**Fallback**: If ui-ux-pro-max skill not installed, degrade to LLM general design knowledge. Suggest installation: `/plugin install ui-ux-pro-max@ui-ux-pro-max-skill`

---

## Completion Action

At Phase 5, coordinator offers interactive completion:

```
AskUserQuestion({
  questions: [{
    question: "Team pipeline complete. What would you like to do?",
    header: "Completion",
    options: [
      { label: "Archive & Clean (Recommended)" },
      { label: "Keep Active" },
      { label: "Export Results" }
    ]
  }]
})
```

| Choice | Steps |
|--------|-------|
| Archive & Clean | Verify completed -> update status -> TeamDelete() -> final summary |
| Keep Active | Status="paused" -> "Resume with: Skill(skill='team-frontend', args='resume')" |
| Export Results | Ask target dir -> copy artifacts -> Archive flow |

---

## Message Bus

Every SendMessage must be preceded by `mcp__ccw-tools__team_msg` log:

```
mcp__ccw-tools__team_msg({
  operation: "log",
  session_id: <session-id>,
  from: <role>,
  type: <message-type>,
  data: {ref: <artifact-path>}
})
```

`to` and `summary` auto-defaulted -- do NOT specify explicitly.

**CLI fallback**: `ccw team log --session-id <session-id> --from <role> --type <type> --json`

**Message types by role**:

| Role | Types |
|------|-------|
| coordinator | `task_unblocked`, `sync_checkpoint`, `fix_required`, `error`, `shutdown` |
| analyst | `analyze_ready`, `error` |
| architect | `arch_ready`, `arch_revision`, `error` |
| developer | `dev_complete`, `dev_progress`, `error` |
| qa | `qa_passed`, `qa_result`, `fix_required`, `error` |

---

## Session Directory

```
.workflow/.team/FE-<slug>-<YYYY-MM-DD>/
├── .msg/
│   ├── messages.jsonl          # Message bus log
│   └── meta.json               # Session state + cross-role state
├── wisdom/                     # Cross-task knowledge
├── analysis/                   # Analyst output
│   ├── design-intelligence.json
│   └── requirements.md
├── architecture/               # Architect output
│   ├── design-tokens.json
│   ├── component-specs/
│   └── project-structure.md
├── qa/                         # QA output
│   └── audit-<NNN>.md
└── build/                      # Developer output
```

## Error Handling

| Scenario | Resolution |
|----------|------------|
| Unknown command | Error with available command list |
| QA score < 6 over 2 GC rounds | Escalate to user |
| Dual-track sync failure (system mode) | Fallback to single-track sequential |
| ui-ux-pro-max unavailable | Degrade to LLM general design knowledge |
| Worker no response | Report waiting task, suggest user `resume` |
| Pipeline deadlock | Check blockedBy chain, report blocking point |
