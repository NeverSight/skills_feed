---
name: code-review-and-commit
description: Review uncommitted Git changes for correctness, quality, and project convention alignment, then apply fixes and prepare a safe, atomic commit plan. Use when users ask to review code before committing, improve local changes, split work into logical conventional commits, or execute `git add`/`git commit` with clear staging boundaries.
---

# Code Review and Commit

Perform a high-signal review of working-tree changes, fix meaningful issues, and produce an understandable commit history.

Source basis: adapted from a local Claude Code agent prompt (`code-review-and-commit.md`).

## Workflow

1. Inspect current change scope.
1. Review for correctness and maintainability issues.
1. Apply necessary fixes.
1. Validate updated changes.
1. Build a commit plan.
1. Ask for approval before creating commits.
1. Execute commits in order and report results.

## 1) Inspect Current Change Scope

Run:

- `git status --short`
- `git diff` (unstaged)
- `git diff --staged` (if relevant)

Map changes by concern (feature, fix, refactor, tests, docs) before suggesting commit boundaries.

## 2) Review Priorities

Prioritize in this order:

1. Correctness and regressions.
1. Security and secret leakage risks.
1. Broken architecture or project-pattern violations.
1. Missing tests for behavior changes.
1. Readability and maintainability improvements.

Review for:

- Logic bugs and unhandled edge cases.
- Missing error handling or validation.
- Performance pitfalls in changed code paths.
- Type accuracy and docstring quality; favor concise, useful docs.
- Low-value comments that restate obvious code behavior.
- Resource-lifecycle problems (cleanup, context management).
- Violations of repository conventions from project docs.

## 3) Apply Fixes

When findings are actionable and safe, implement fixes directly.

- Keep scope tight to the requested work.
- Avoid unrelated refactors unless necessary for correctness.
- Re-check diffs after each meaningful fix.

## 4) Validate

Run relevant quality checks when available (for example lint, tests, type checks).

If checks cannot run, explicitly state what was skipped and why.

## 5) Build Commit Plan

Group changes into atomic commits that can be reverted independently.

For each proposed commit include:

- Commit type and summary (`feat`, `fix`, `refactor`, `test`, `docs`, `chore`).
- Exact files to stage.
- Why this grouping is coherent.
- Final commit message draft.

Commit message rules:

- Use imperative mood.
- Keep subject concise (target <= 50 chars).
- Add body only when needed, explaining why.
- Wrap body lines near 72 chars.

## 6) Approval Gate

Before running `git add` or `git commit`, present the full commit plan and request approval.

If the user asks for changes, revise the plan and re-present before executing.

## 7) Execute and Report

After approval:

1. Stage only planned files for the current commit.
1. Create the commit.
1. Confirm success with commit hash and summary.
1. Repeat for remaining commits.

End with a concise recap:

- Commits created (hash + subject).
- Files included per commit.
- Any remaining unstaged/uncommitted changes.

## Output Format

Use this structure:

1. `Review Findings` grouped by severity (`Critical`, `Important`, `Suggestion`).
1. `Applied Fixes` with file-level summary.
1. `Validation Results` (commands run and outcomes).
1. `Proposed Commit Plan` (numbered commits with file list + message).
1. `Execution Results` after approval.

## Decision Rules

- Prefer correctness over style.
- Favor project conventions over personal preference.
- Surface trade-offs when multiple valid approaches exist.
- Escalate explicitly when changes are risky or architecture-affecting.
