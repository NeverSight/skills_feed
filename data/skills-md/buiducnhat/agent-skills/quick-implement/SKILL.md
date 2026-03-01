---
name: quick-implement
description: Rapid implementation for small, low-risk, well-defined changes. Use when the task is narrow in scope, has clear acceptance criteria, and can be completed safely without a formal multi-phase plan.
---

# Quick Implement

## Purpose

Implement small features or bug fixes directly, with strict scope control and verification.

Use this skill for speed **only when risk is low** and requirements are clear.

## Scope Gate (Required Before Coding)

Treat a task as **quick-implement eligible** only if all conditions below are true:

1. **Clear requirement**
   - Expected behavior is explicit
   - No major product/architecture ambiguity

2. **Small change surface**
   - Usually touches a small number of files (rough guideline: <= 5 files)
   - No broad cross-module refactor

3. **Low architectural risk**
   - No foundational redesign
   - No migration-heavy change
   - No multi-phase rollout dependency

4. **Straightforward verification**
   - Can validate with targeted tests/checks quickly
   - No long exploratory debugging loop required

If any condition fails, escalate to `write-plan`.

## Hard Stop Escalation Criteria

Immediately stop quick implementation and switch to planning when any of these appear:

- Requirement ambiguity that needs design decisions
- Unexpected coupling across multiple subsystems
- Significant data model or schema changes
- Security-sensitive or compliance-critical changes
- Performance work requiring benchmarks/design trade-offs
- Refactor growing beyond original small scope
- Repeated failed attempts without a clear root cause
- Need for phased delivery, feature flags, or migration strategy

Escalation message template:

- "This change exceeds rapid-implementation safety limits. Recommend `write-plan` first to define phased execution and risk controls."

## Workflow

### Step 1: Analyze and Contextualize

1. Understand the user request and define acceptance criteria.
2. Review relevant project documentation first:
   - `docs/project-pdr.md`
   - `docs/architecture.md`
   - `docs/codebase.md`
   - `docs/code-standard.md`
3. Inspect only the minimum necessary code paths.
4. Confirm the task still passes the Scope Gate.
5. If ambiguity remains, ask clarifying questions before coding.

### Step 2: Implement

1. Make the smallest correct change to satisfy requirements.
2. Reuse existing patterns and conventions.
3. Avoid opportunistic refactors unrelated to the request.
4. Keep changes idempotent and safe to rerun when applicable.

### Step 3: Verify

Run proportional validation for the change:

1. Targeted tests related to modified behavior
2. Relevant lint/type checks for touched areas
3. Build or runtime verification if applicable

If verification fails unexpectedly:

- Attempt focused fixes if clearly local
- If failures suggest broader impact, escalate to `write-plan`

### Step 4: Complete

1. Summarize what changed and why.
2. List modified files.
3. Report verification commands and outcomes.
4. Update documentation if behavior, architecture, or domain rules changed (typically `docs/project-pdr.md`, `docs/codebase.md`, `docs/architecture.md`).

## Execution Boundaries

- Do not expand scope without explicit user approval.
- Do not assume unspecified behavior; clarify instead.
- Do not force completion when risk increases—escalate early.

## Output Checklist

Before final response, confirm:

- Scope Gate was satisfied
- No hidden architectural changes were introduced
- Verification was run and reported
- Escalation was used if safety limits were exceeded

## Integration

- Escalate to `write-plan` when complexity or risk exceeds quick-implement limits.
- Use `fix` when the task is primarily debugging an issue.
