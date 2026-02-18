---
name: task-planner
description: >-
  Guide for decomposing large tasks into executable steps, managing
  dependencies and priorities, and distributing work across agents. Includes
  TodoList integration patterns.
---

# Task Planner

This skill helps you turn ambiguous or large requests into a clear, sequenced plan with ownership and verification.

## Outputs To Produce

- A short problem statement
- Assumptions and open questions
- A step-by-step plan with measurable outcomes
- Risks and rollback/containment options
- Test and verification steps

## Decomposition Technique

Split work into thin vertical slices:

- One slice should be mergeable on its own
- Each slice should include tests or validation
- Prefer smallest unit that reduces uncertainty

Common slice types:

- Spec tests (lock requirements, CLI flags, edge cases)
- Implementation changes (small, isolated)
- Documentation updates
- Observability and traceability improvements

## Dependency And Priority Rules

- Identify blockers first (missing API, failing tests, permissions).
- Order by "unblocks others" and "reduces uncertainty".
- For multi-agent work, keep interfaces stable and define contracts (inputs/outputs) per slice.

## Multi-Agent Assignment

When delegating:

- Specify the exact deliverable (files, tests, output format)
- Specify constraints (no commits, branch constraints, time limits)
- Specify the acceptance test (what must pass)

Example delegation message:

```
Please write tests for <feature>.
Constraints:
- Do not change implementation yet
- Use pytest
Acceptance:
- Tests fail before implementation
- Tests cover edge cases: <...>
```

## TodoList Integration

Use a TodoList to track execution:

- Keep items small, phrased as outcomes
- Include "verify" tasks (tests, manual checks)
- Mark completed immediately to prevent drift

Example TodoList:

- Add failing tests for <behavior>
- Implement <behavior> behind tests
- Run targeted tests
- Update docs
- Run full test suite

## Progress Reporting

For status updates, report:

- What is done (with tests run)
- What is next
- What is blocked and by what

