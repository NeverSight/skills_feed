---
name: code-simplifier
description: >-
  Guide for simplifying recently-changed code. Use this skill to invoke the
  code-simplifier subagent for targeted refactors (deduplication, branching
  simplification, readability improvements) with safety checks.
---

# Code Simplifier

This skill helps you simplify code in a controlled, reviewable way, focusing on files that changed recently.

## When To Use

- You have working code but it is hard to read or maintain.
- A PR introduces duplication or unnecessary conditionals.
- You want to reduce complexity without changing behavior.

## Scope Rules

- Prefer small, safe changes: reduce duplication, simplify branching, clarify naming.
- Do not change external behavior unless explicitly requested.
- Do not "optimize" without evidence.

## Target Selection (Recently Changed Files)

Pick the smallest set of relevant files:

```bash
git diff --name-only
git diff --name-only origin/main...HEAD
```

If you must expand scope, do it intentionally and explain why.

## Subagent Invocation (Task Tool)

Use the Task tool to delegate the simplification pass to a specialized subagent:

- subagent_type: `code-simplifier`

Provide:

- The file list and why each file is included
- Any constraints (no behavior change, keep public APIs stable, etc.)
- What "done" looks like (tests passing, lint clean, etc.)

Example prompt to the subagent:

```
Simplify the following changed files: <files...>.
Goals:
- Reduce duplication
- Simplify conditionals and early returns
- Improve naming and structure for readability
Constraints:
- No behavior change
- Keep public interfaces stable
Deliverables:
- A concise change list
- Suggested tests to add/update
```

## Review Checklist

- Diff is mostly deletions or localized rewrites, not wide churn.
- Conditionals are simpler (fewer nested branches).
- Shared logic is extracted once (helpers, small functions).
- Names reflect intent.
- Tests still pass; add tests if behavior was ambiguous.

