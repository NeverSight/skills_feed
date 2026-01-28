---
name: criteria-test-loop
description: Drive coding by success criteria and tests; use for bugfixes, features with tests, and algorithmic changes. Emphasize naive-correct first, then optimize.
---

# Criteria Test Loop

## Quick start

- Define success criteria or tests.
- Implement the naive correct version.
- Iterate until tests pass.
- Optimize only after correctness.

## Procedure

1) Convert the request into explicit success checks.
2) Write or select tests that prove success.
3) Implement the simplest correct solution.
4) Run or reason through tests; fix failures.
5) Optimize while preserving the tests.

## Output format

- Success criteria: bullets.
- Tests: new or existing.
- Result: pass/fail and notes.
- Optimization (optional): what changed and why.

## Guardrails

- Do not optimize before correctness.
- Keep the test loop tight and explicit.
- If tests are missing, add the smallest set that proves success.
