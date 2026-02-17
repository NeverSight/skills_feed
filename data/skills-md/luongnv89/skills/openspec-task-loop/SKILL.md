---
name: openspec-task-loop
version: 1.0.0
description: Apply OpenSpec OPSX in a strict one-task-at-a-time loop. Use when the user asks to execute work as single-task changes, wants spec-first implementation per task, or says to use OpenSpec method for each task from a task list. Supports both native /opsx command environments and manual fallback by creating OpenSpec artifact files directly.
---

# OpenSpec Task Loop

## Overview

Run OpenSpec as **one task = one change**. Keep scope tight, generate artifacts, implement, verify, and archive before moving to the next task.

## Workflow Decision

1. **If `/opsx:*` commands are supported in the current coding tool**: use native OPSX flow.
2. **If not supported**: use manual fallback by creating files under `openspec/changes/<change-id>/`.

## Core Loop (Single Task)

For each selected task from `tasks.md`:

1. **Select exactly one task**
   - Keep one atomic unit of value (usually 1–3 dev days).
   - If too large, split before proceeding.

2. **Create a task-scoped change**
   - Use change id format: `task-<task-id>-<short-slug>` (example: `task-2-3-pin-crud`).

3. **Plan with OpenSpec artifacts**
   - `proposal.md`: intent, scope, acceptance criteria, out-of-scope.
   - `specs/.../spec.md`: requirements and GIVEN/WHEN/THEN scenarios.
   - `design.md`: implementation approach and tradeoffs.
   - `tasks.md`: implementation checklist for this single task.

4. **Implement only this task scope**
   - Do not include unrelated refactors.
   - Update checkboxes as work completes.

5. **Verify before archive**
   - Validate completeness, correctness, coherence.
   - Fix critical mismatches before archive.

6. **Archive and sync**
   - Merge delta specs if needed.
   - Archive change folder.
   - Mark the parent project task complete.

## Native OPSX Command Path

Use this sequence per task:

```text
/opsx:new task-<task-id>-<slug>
/opsx:ff <change-id>          # or /opsx:continue for stepwise control
/opsx:apply <change-id>
/opsx:verify <change-id>
/opsx:archive <change-id>
```

Rules:
- Prefer `/opsx:continue` when requirements are still unclear.
- Prefer `/opsx:ff` when scope is clear and small.
- If implementation reveals drift, update artifacts before continuing.

## Manual Fallback Path (No /opsx Support)

If slash commands are unavailable:

1. Ensure OpenSpec tree exists (`openspec/changes`, `openspec/specs`).
2. Scaffold one change folder with:
   - `proposal.md`
   - `design.md`
   - `tasks.md`
   - `specs/<capability>/spec.md`
3. Use templates from `references/openspec-task-templates.md`.
4. Implement task and update checkboxes.
5. Run local validation/tests.
6. Merge spec deltas into `openspec/specs/` and move change to `openspec/changes/archive/<date>-<change-id>/`.

## Quality Gate (must pass before archive)

- [ ] Scope remained single-task and atomic
- [ ] Acceptance criteria satisfied
- [ ] Spec scenarios reflected in tests or executable checks
- [ ] No unrelated files changed
- [ ] Parent `tasks.md` updated with completion state
- [ ] Archive note includes what changed and why

## Output Format for Updates

When reporting progress, use:

```markdown
Task: <id + title>
Change: <openspec change id>
Status: planning | implementing | verifying | archived
Done:
- ...
Next:
- ...
Risks/Notes:
- ...
```

## Resources

- `references/openspec-task-templates.md` — proposal/spec/design/tasks templates for manual mode.
- `scripts/new_task_change.sh` — optional scaffold script for manual mode.
