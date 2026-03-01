---
name: execute-plan
description: Execute an approved implementation plan exactly and safely. Use when a plan already exists (for example in docs/plans/...) and work must be carried out phase-by-phase with verification checkpoints, status tracking, and final execution reporting.
---

# Execute Plan

## Overview

Execute a pre-approved plan with strict adherence to scope, sequence, and verification.

The input is typically:

- `execute-plan docs/plans/YYMMDD-HHmm-<plan-slug>/SUMMARY.md`
- or shorthand: `execute-plan docs/plans/YYMMDD-HHmm-<plan-slug>`

Do not redesign the plan during execution. If ambiguity or blockers appear, stop and ask.

## Workflow

### Step 1: Initialize

1. **Locate Plan**
   - Confirm the plan path exists and is readable.
   - If a directory is provided, locate `SUMMARY.md` inside it.

2. **Load Execution Context**
   - Read:
     - `docs/project-pdr.md`
     - `docs/architecture.md`
     - `docs/codebase.md`
     - `docs/code-standard.md`
   - Review the plan’s phase files and dependencies.

3. **Select Execution Mode (Explicit Rule)**
   - Default mode: **Batch**
   - Use **Interactive** when any of the following is true:
     - High-risk changes (auth, payments, migrations, security-critical logic)
     - Irreversible operations (data migrations, destructive scripts)
     - Unclear acceptance criteria
     - User explicitly requests checkpoints
   - If mode is unclear, ask once and proceed with user choice.

4. **Find Next Pending Phase**
   - First `[ ]` phase
   - If none, first `[-]` phase
   - If no pending/in-progress phases remain, go to final verification.

5. **Critical Plan Sanity Check**
   - Ensure each phase has:
     - clear objective
     - file targets
     - verification commands
   - If essential details are missing or contradictory, stop and request clarification.

### Step 2: Execute Per-Phase Loop

For each phase in order:

1. **Skip Completed**
   - If status is `[x]`, continue to next phase.

2. **Mark In Progress**
   - Update phase status to `[-]` before making changes.

3. **Execute Exactly**
   - Implement only the tasks defined in that phase.
   - Do not expand scope without approval.

4. **Verify Phase**
   - Run the phase-specific verification commands from the plan.
   - At minimum, run relevant tests/checks tied to touched files.

5. **Handle Failures**
   - If verification fails:
     - Attempt focused fixes within phase scope.
     - Re-run verification.
   - If still failing or root cause is outside scope, stop and report blocker.

6. **Mark Complete**
   - Update phase status to `[x]` only after verification passes.

7. **Progress Report**
   - **Interactive mode:** report and wait for confirmation before next phase.
   - **Batch mode:** report briefly and continue immediately.

### Step 3: Final Verification

After all phases are complete:

1. **Project-Wide Validation**
   - Run full lint/type-check suite
   - Run all relevant tests (or full test suite if required by the plan)
   - Run build verification if applicable

2. **Stabilize**
   - Fix regressions introduced during execution.
   - Re-run failed checks until green or blocked.

3. **Manual Validation Checkpoint**
   - If user/manual QA is required, ask explicitly and pause:
     - `Verified` to accept
     - or provide feedback for follow-up iteration

### Step 4: Completion Artifacts

1. **Documentation Sync**
   - If behavior/architecture/codebase expectations changed, update:
     - `docs/project-pdr.md`
     - `docs/codebase.md`
     - `docs/architecture.md`

2. **Create Execution Report**
   - File: `docs/plans/YYMMDD-HHmm-<plan-slug>/EXECUTION-REPORT.md`
   - Include all required sections below.

3. **Announce Completion**
   - Output: `Execution complete. Report created at <path>.`

## Execution Report Standard

`EXECUTION-REPORT.md` must use this structure:

# Execution Report: <Plan Title>

> Date: YYYY-MM-DD HH:mm:ss  
> Mode: Batch | Interactive  
> Plan Path: <relative-path>

## Summary

- Overall result (Completed | Completed with follow-ups | Blocked)
- High-level outcome in 2-4 bullets

## Phase Results

- Phase 1: <name> — ✅/⚠️
  - Implemented:
  - Verification:
  - Notes:
- Phase 2: ...

## Verification Matrix

- Lint: pass/fail (command)
- Type-check: pass/fail (command)
- Tests: pass/fail (command)
- Build: pass/fail (command)
- Manual QA: pass/fail/pending

## Deviations

- List any approved deviations from the original plan.
- If none: `None.`

## Blockers and Resolutions

- Blocker:
- Impact:
- Resolution:
- Status:

## Follow-ups

- Remaining tasks, if any
- Recommended owner/next action

## Changed Files

- Relative path list (grouped by area if large)

## Rules

- **Follow the plan strictly**: no silent scope changes.
- **Stop on blocker**: missing dependency, contradictory instructions, or unexplained failures.
- **No guessing**: ask for clarification when uncertain.
- **Verify before complete**: never mark phase done without passing checks.
- **Idempotency**: prefer safe/re-runnable operations.
- **Respect project standards**: follow `docs/code-standard.md` and related project docs.
- **Do not skip workflow steps**: initialization, per-phase verification, final verification, and reporting are all mandatory.

## Integration

- Use `scripts/get-time.sh` for:
  - `YYMMDD-HHmm` folder naming
  - `YYYY-MM-DD HH:mm:ss` report timestamps
