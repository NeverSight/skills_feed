---
name: feature-tasks
description: Break a feature request into dependency-aware implementation tasks and generate a machine-readable task graph. Use when planning or executing feature work that needs task IDs, blockers, critical paths, or parallel work windows.
---

# Feature Tasks

Create planning artifacts in `planning/<dd-mm-yyyy-title-slug>/` and generate `task.graph.json`.

## Workflow

1. Clarify feature scope, constraints, and acceptance criteria.
2. Pick a title slug (for example `add-new-payment-method`). The generator resolves it to `planning/<dd-mm-yyyy-title-slug>/` for new folders, while existing non-prefixed folders are reused.
3. Author `planning/<dd-mm-yyyy-title-slug>/SPEC.md` with: feature overview, requirements,
   constraints, and design decisions. Required by the companion orchestration skill.
4. Author `planning/<dd-mm-yyyy-title-slug>/tasks.yaml` using the strict schema below.
5. Keep related planning artifacts in the same folder (`SPEC.md`, `task.graph.json`, `task.status.json`).
6. Run the bundled script to validate and generate `task.graph.json`.
7. Fix all schema and parity errors until generation succeeds.
8. Use `task.graph.json` to drive execution order.

## tasks.yaml schema (strict)

`version` must be `3`. Version `3` supports the optional `context` field per task.

```yaml
version: 3
project: <project-name>
tasks:
  - id: TASK-001
    phase: planning
    priority: high # low | medium | high | critical
    title: Define acceptance criteria and scope
    blocked_by: []
    acceptance:
      - Acceptance criteria reviewed by stakeholders
    deliverables:
      - docs/spec.md updated with final scope
    owner_type: docs # frontend | backend | infra | docs | qa | fullstack
    estimate: M
    notes: Optional context
    context:
      - src/api/orders.ts
      - SPEC.md#payment-flow
      - Uses Repository pattern from src/lib/repo.ts
critical_paths:
  - id: cp-main
    tasks: [TASK-001]
parallel_windows:
  - id: pw-initial
    tasks: [TASK-001]
```

## Required task fields

Every task must include:

- `id` (unique string)
- `phase` (string)
- `priority` (`low|medium|high|critical`)
- `title` (string)
- `blocked_by` (array of task IDs; empty allowed)
- `acceptance` (non-empty array of strings)
- `deliverables` (non-empty array of strings)
- `owner_type` (`frontend|backend|infra|docs|qa|fullstack`)
- `estimate` (string)

Optional:

- `notes` (string)
- `context` (array of strings): File paths, spec section refs, or hints pointing
  worker agents to relevant code. Example:
  `["src/api/orders.ts", "SPEC.md#payment-flow", "Uses Repository pattern from src/lib/repo.ts"]`

## Task granularity

- Each task should be completable in a single agent session (typically 1-3 files changed).
- If acceptance criteria span multiple subsystems, split into separate tasks with dependencies.
- Prefer more small tasks over fewer large ones — parallelism improves throughput.
- A task that changes more than 5 files is usually too broad.

## Execution

Run from the target repository:

```bash
<path-to-skill>/scripts/generate-task-graph [title-slug] [output-graph-json]
```

Default behavior:

- Input: `<git-root>/planning/<dd-mm-yyyy-title-slug>/tasks.yaml`
- Output: `<git-root>/planning/<dd-mm-yyyy-title-slug>/task.graph.json`
- If `title-slug` is omitted, the script derives it from the current branch name, strips common conventional prefixes (`feat-`, `fix-`, etc.), and resolves new folders to a `dd-mm-yyyy-<slug>` prefix (existing non-prefixed folders are reused).

## Validation and parity checks

The script fails with actionable errors when:

- Required fields are missing
- `version` is not `3`
- `priority` or `owner_type` enum values are invalid
- Task IDs are duplicated
- `blocked_by` references unknown IDs
- `critical_paths[*].tasks` or `parallel_windows[*].tasks` reference unknown IDs
- A task depends on itself
- Dependency cycles exist

## Companion Skill

Use `feature-tasks-work` for orchestration mode after planning is complete.
