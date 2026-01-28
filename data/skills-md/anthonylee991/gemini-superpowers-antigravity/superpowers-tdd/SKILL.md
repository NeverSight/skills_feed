---
name: superpowers-tdd
description: Applies tests-first discipline (red/green/refactor) and adds regression tests for bugs. Use when implementing features, fixing bugs, or refactoring.
---

# TDD Skill

## When to use this skill
- new features that can be unit tested
- bug fixes (always add a regression test if practical)
- refactors (protect behavior with tests first)

## Rules
- Prefer **red -> green -> refactor**.
- If tests are hard, still add **verification**: minimal repro script, integration test, or clear manual steps.
- Keep tests focused: one behavior per test where possible.
- Name tests by behavior, not implementation details.

## Process
1. Define the behavior change (what should be true after).
2. Write/adjust a test to capture it (make it fail first if possible).
3. Implement the minimal change to pass.
4. Refactor if needed (keep passing).
5. Run the relevant test suite + any linters.

## Output requirements
When you change code, include:
- what tests you added/changed
- how to run them
- what they prove
