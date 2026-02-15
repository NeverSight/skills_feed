---
name: feature-tasks-work
description: Orchestrate execution from feature task plans. Use when work should start from SPEC.md and tasks.yaml, optionally using task.graph.json, by delegating implementation tasks to other agent/model worker instances.
---

# Feature Tasks Work

Execute planned work as an orchestrator with deterministic delegation and status tracking.

## Mandatory interface

Use the bundled CLI for orchestration state and prompt assembly.

- Do not hand-edit `planning/<dd-mm-yyyy-title-slug>/task.status.json` during normal execution.
- Use `taskctl` commands for queue reads, task lifecycle transitions, and delegation prompts.
- Hand edits are recovery-only when the status file is corrupted.

Set a command alias before orchestration:

```bash
TASKCTL="<path-to-skill>/scripts/taskctl"
```

Always execute the CLI via `"$TASKCTL" ...`.
Do not assume `taskctl` is available on `PATH`.

Terminology note:
- In this skill, `collaborator`, `subagent`, and `teammate` mean a worker identity (agent/model/session id), not a filesystem path.

Runtime behavior:

- `scripts/taskctl` runs `node taskctl.mjs` when Node.js is available.
- Otherwise it runs `bun taskctl.mjs` when Bun is available.
- If neither is available, it exits with an install message.

## Protocol

1. Start orchestration with minimal prior context. If your agent supports session reset, use it.
2. Resolve `title-slug` (for example `add-new-payment-method`) under `planning/`; new folders use `dd-mm-yyyy-<slug>` while existing non-prefixed folders are reused.
3. Run `"$TASKCTL" init <title-slug>`.
   - Loads or creates `task.status.json`.
   - Resets stale `in_progress` entries to `todo`.
   - Re-evaluates blocked tasks whose blockers are now done.
4. Discover dispatchable work with `"$TASKCTL" ready <title-slug> --json`.
5. For each task, prefer atomic dispatch:
   - `"$TASKCTL" dispatch <title-slug> [task-id] --owner <orchestrator-or-worker-id> --json`
6. If dispatch is not used, do split mode:
   - Build delegation payload/prompt with `"$TASKCTL" prompt <title-slug> <task-id> --json`.
   - Mark dispatched with `"$TASKCTL" start <title-slug> <task-id> --owner <orchestrator-or-worker-id>`.
7. Delegate using the generated prompt.
8. After each attempt, persist result with:
   - `"$TASKCTL" complete <title-slug> <task-id> --result <done|blocked|failed> --summary "..." --files ... --tests ... --blockers ... --next ...`
9. Retry policy:
   - Protocol failure (missing response fields): retry once with a format reminder.
   - Transient failure (timeout/rate limit): retry once after a pause.
   - Task failure (`result=failed`): mark blocked and continue.
   - Persistent failure (second attempt fails): mark blocked and continue.
10. Repeat `dispatch -> complete` until no `todo` tasks remain.
11. Emit final summary with done/blocked counts and unresolved blockers.

## CLI commands

The script supports these commands:

- `init [title-slug]`
- `ready [title-slug]`
- `prompt [title-slug] [task-id]`
- `dispatch [title-slug] [task-id] --owner <owner-name>`
- `start [title-slug] <task-id> --owner <owner-name>`
- `complete [title-slug] <task-id> --result <done|blocked|failed> --summary <text> [--files a,b] [--tests a,b] [--blockers a,b] [--next a,b]`
- `status [title-slug]`

Notes:

- If `title-slug` is omitted, it is derived from the current branch and resolved to `dd-mm-yyyy-<slug>` for new folders (existing non-prefixed folders are reused).
- `prompt` returns both structured payload and formatted prompt when `--json` is used.
- For `prompt` or `dispatch`, if `title-slug` is omitted and task ID is explicit, pass `--task <task-id>`.

## Delegation payload contract (outbound)

Use the payload from `taskctl prompt`. Required fields:

- `task_id`
- `title`
- `acceptance`
- `deliverables`
- `project`
- `dependency_results` (for each done blocker: `{ task_id, result_summary, files_changed }`)
- `response_format` list

Optional fields:

- `context`
- `spec_excerpt`

## spec_excerpt rules

`taskctl prompt` follows these rules:

- If `SPEC.md` exists and is under 200 lines, include all of it.
- If `SPEC.md` is over 200 lines, include only sections referenced by `context` entries containing `SPEC.md#<section>`.
- If `SPEC.md` is missing, omit `spec_excerpt`.

## Delegation response contract (required)

Every delegated task must return:

- `task_id`
- `result` (`done|blocked|failed`)
- `result_summary`
- `files_changed` (array)
- `tests_run` (array)
- `blockers` (array)
- `next_unblocked_tasks` (array of task IDs)

Treat missing required fields as protocol failure and apply retry policy.

## Context management

- Keep per completed task: task_id, one-line result_summary, files_changed.
- Discard after completion: full delegation prompt, full response body, acceptance, deliverables, context hints.
- Always retain: dispatch queue and `task.status.json` summary counts.
- When context pressure is high (>60% tasks done): summarize completed tasks into one block and discard individual details.
- Never discard blocked task details and blockers.

## task.status.json schema

Default path: `planning/<dd-mm-yyyy-title-slug>/task.status.json`.

```json
{
  "project": "my-project",
  "schema_version": 2,
  "updated_at": "2026-02-11T12:00:00.000Z",
  "summary": {
    "todo": 2,
    "in_progress": 1,
    "done": 3,
    "blocked": 1
  },
  "tasks": {
    "TASK-001": {
      "state": "done",
      "owner": "worker-backend-1",
      "attempts": 1,
      "started_at": "2026-02-11T11:40:00.000Z",
      "finished_at": "2026-02-11T11:55:00.000Z",
      "blockers": [],
      "files_changed": ["src/api/orders.ts"],
      "tests_run": ["bun test -- orders"],
      "result_summary": "Implemented order endpoint and tests.",
      "next_unblocked_tasks": ["TASK-002"]
    }
  }
}
```

## State semantics

- `todo`: not started.
- `in_progress`: delegated and awaiting result.
- `done`: completed and accepted.
- `blocked`: cannot proceed after retry policy or hard dependency blockage.

Only dispatch tasks in `todo` state that are currently unblocked.
