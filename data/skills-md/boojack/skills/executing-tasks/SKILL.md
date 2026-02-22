---
name: executing-tasks
description: Executes an approved task plan exactly as written, producing code changes, running validations, and recording completion status for each task. Use when a task plan exists with readiness status "Ready for execution" and implementation work should begin.
---

# Executing Tasks

Takes `plan.md` from `docs/issues/YYYY-MM-DD-<slug>/` as input. Executes each task exactly as specified, validates results, and records outcomes.

Does NOT modify the plan, merge/split/reorder tasks, introduce new tasks, make design decisions, or perform opportunistic refactors.

```
THE PLAN IS IMMUTABLE — STOP ON ANY DEVIATION
```

## Workflow

Execute in **batches of 3 tasks**, pausing for review between batches.

```
- [ ] Load plan
- [ ] For each batch of 3:
  - [ ] Confirm → Execute → Validate → Record (per task)
  - [ ] Report batch → Wait for feedback
- [ ] Declare completion
```

### Step 1: Load Plan

Read `plan.md`. Verify Readiness Declaration is "Ready for execution". If blocked or requires update, STOP.

### Step 2: Execute Batch

For each task in the current batch:

**Confirm** — Restate task ID, objective, files, boundaries. Dependencies satisfied? If no, STOP.

**Execute** — Perform only actions in Implementation. Touch only declared files. Do NOT "improve" beyond scope.

**Validate** — Run exact validation commands. Pass → record. Fail → STOP, record failure.

**Record** under **## Execution Log**:

```
### T<N>: <title>

**Status**: Completed | Failed | Skipped
**Files Changed**: list
**Validation**: `command` — PASS/FAIL
**Deviations**: None | (describe — then STOP)
```

Any deviation = failure. STOP and record.

### Step 3: Report Batch

After each batch (or on failure):
- Tasks completed with validation results
- Remaining tasks count
- **"Batch complete. Ready for feedback before continuing."**

Wait for user feedback before next batch.

### Step 4: Declare Completion

Exactly one:
- **All tasks completed successfully**
- **Execution halted at T\<N\> due to failure** — what failed
- **Execution blocked pending clarification** — what's needed

On failure, include **Blocker for planner**: what change would allow the plan to succeed. Do NOT fix by modifying the plan, skip tasks, or rationalize deviations.

## Output

Save to `docs/issues/YYYY-MM-DD-<slug>/execution.md`.

```markdown
## Execution Log

## Completion Declaration
```

## Red Flags - STOP

If you catch yourself thinking:
- "I'll just fix this small thing while I'm here"
- "This validation is obviously correct, I'll skip it"
- "The plan says X but Y is clearly better"
- "I'll combine these two tasks for efficiency"
- "Completed with minor deviation"
- "This file isn't in scope but it needs updating too"
- "I'll reorder these tasks, it makes more sense"
- "One more attempt should fix it"

**All of these mean: STOP. Record failure. Do not continue.**

## Anti-patterns

- ❌ "Completed (with deviation)" → ✓ "Failed" + blocker
- ❌ Fixing plan during execution → ✓ stop, record blocker
- ❌ "Obviously correct" → ✓ run exact command, record result
- ❌ Continuing after failure → ✓ STOP at first failure
- ❌ Touching undeclared files → ✓ only declared files
