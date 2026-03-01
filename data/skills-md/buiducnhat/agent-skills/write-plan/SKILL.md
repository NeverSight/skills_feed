---
name: write-plan
description: Create detailed, execution-ready implementation plans for complex or high-risk changes without coding. Use when scope is large, requirements are mostly known, and work should be broken into validated phases before execution.
---

# Write Plan

## Overview

Produce a complete, self-contained implementation plan that can be executed by `execute-plan` with minimal ambiguity.

This skill is for planning only:

- Do not implement code
- Do not modify production files (except plan artifacts)

## Artifact Conventions

Use one consistent artifact structure for every plan:

- Plan directory: `docs/plans/YYMMDD-HHmm-<plan-slug>/`
- Main summary: `docs/plans/YYMMDD-HHmm-<plan-slug>/SUMMARY.md`
- Phase files: `docs/plans/YYMMDD-HHmm-<plan-slug>/phase-01-<name>.md`, `phase-02-<name>.md`, etc.
- Optional research notes: `docs/plans/YYMMDD-HHmm-<plan-slug>/research/<topic>.md`

Use `scripts/get-time.sh` for:

- Folder timestamp: `YYMMDD-HHmm`
- Human-readable timestamp: `YYYY-MM-DD HH:mm:ss`

## Workflow

### Step 1: Contextualize

Read project documentation first:

- `docs/project-pdr.md`
- `docs/architecture.md`
- `docs/codebase.md`
- `docs/code-standard.md`

Then inspect only the code areas relevant to the requested change.

Capture:

- Existing patterns to follow
- Constraints and dependencies
- Risks, assumptions, and unknowns

### Step 2: Initialize Plan Artifacts

1. Create: `docs/plans/YYMMDD-HHmm-<plan-slug>/`
2. Create:
   - `SUMMARY.md`
   - one phase file per implementation phase
3. Add `research/` only if needed.

### Step 3: Define Strategy and Phases

Design a phased strategy that is safe and verifiable.

Each phase should have:

- A clear objective
- Ordered tasks
- Verification commands
- Exit criteria

Granularity rule:

- Tasks should be small, concrete, and typically 2-10 minutes each.

### Step 4: Research (Only if Needed)

Research is optional and should be proportional to uncertainty.

Preferred order:

1. Existing project docs and code
2. Existing skills and local references
3. External references (only if available in the current environment)

If external research capability is unavailable, proceed with local evidence and explicitly list assumptions and open questions.

Document findings in:

- `docs/plans/YYMMDD-HHmm-<plan-slug>/research/<topic>.md`

### Step 5: Write Plan Content

## `SUMMARY.md` format

```markdown
# Implementation Plan: <Title>

> Created: YYYY-MM-DD HH:mm:ss
> Status: Draft

## Objective

- What is being built/changed and why.

## Scope

- In scope
- Out of scope

## Architecture & Approach

- Design decisions and rationale.
- Constraints and compatibility notes.

## Phases

- [ ] **Phase 1: <name>** — Goal: <goal>
- [ ] **Phase 2: <name>** — Goal: <goal>

## Key Changes

- Files/modules likely to change
- Data/API/schema impacts

## Verification Strategy

- Lint/typecheck/tests/build commands
- Manual checks if needed

## Dependencies

- New packages/tools (if any) with reason

## Risks & Mitigations

- Risk → mitigation

## Open Questions

- Items requiring user confirmation
```

## `phase-XX-<name>.md` format

```markdown
# Phase XX: <Name>

## Objective

- Specific result for this phase.

## Preconditions

- What must already be true.

## Tasks

1. Context: files/components to inspect or modify
2. Implement: exact change steps
3. Verify: commands/checks to run
4. Confirm: expected outcome

## Verification

- Commands:
  - <command 1>
  - <command 2>
- Expected results:
  - <result>

## Exit Criteria

- Clear checklist that determines completion.
```

### Step 6: Review and Refine

Before presenting the plan, verify:

- Paths are exact and consistent
- Phase order is logical
- Tasks are actionable (no vague steps)
- Verification is defined for each phase
- Risks/assumptions are explicit
- Plan is executable without hidden context

Then present for user review.

If multiple viable approaches exist, present options and ask for one of:

- **Validate**: refine via additional clarifying questions
- **Confirm**: approve current plan for execution

Iterate until confirmed.

### Step 7: Handoff

When approved, end with:

Plan `<relative_path_to_plan>/SUMMARY.md` is ready.  
Use `/clear` and then `/execute-plan <relative_path_to_plan>/SUMMARY.md` to execute it.

## Rules

- Never automatically implement or execute the code change in the same session, or ask user for execution right now, always finished when completed planning and ready for user review.
- Prefer explicit file paths and concrete commands
- Align with project standards and existing architecture
- Ask clarifying questions when uncertainty affects execution safety
- Keep plans self-contained and deterministic
