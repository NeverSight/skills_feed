---
name: unit-tests
description: Generates well-structured unit tests using Vitest with the "given/should" prose format. Use when writing tests for new code, adding coverage to existing code, or following TDD practices.
---

# Unit Tests

Act as a top-tier software engineer with serious testing skills.

Write unit tests for: $ARGUMENTS

Each test must answer these 5 questions:

1. What is the unit under test? (test should be in a named describe block)
2. What is the expected behavior? ($given and $should arguments are adequate)
3. What is the actual output? (the unit under test was exercised by the test)
4. What is the expected output? ($expected and/or $should are adequate)
5. How can we find the bug? (implicitly answered if the above questions are answered correctly)

## Rules

- Use Vitest with describe, expect, and test.
- Tests must use the "given: ..., should: ..." prose format.
- Colocate tests with functions. Test files should be in the same folder as the implementation file.
- Use cuid2 for IDs unless specified otherwise.
- If an argument is a database entity, use an existing factory function and override values as needed.
- Capture the `actual` and the `expected` value in variables.
- The top-level `describe` block should describe the component under test.
- The `test` block should describe the case via `"given: ..., should: ..."`.
- Avoid `expect.any(Constructor)` in assertions. Expect specific values instead.
- Always use the `toEqual` equality assertion.
- Empty line before `actual` variable assignment.
- NO empty line between `actual` and `expected` assignments.
- Empty line after `expected` variable assignment before the `toEqual` assertion.
- Tests must be readable, isolated, thorough, and explicit.
- Test expected edge cases.
- Create factory functions for reused data structures rather than sharing mutable fixtures.

## When NOT to use this skill

- For React component render tests (`.test.tsx`), use `/happy-dom-tests` instead.
- For database or server action tests (`.spec.ts`), use `/integration-tests` instead.
- For browser-level user flow tests (`.e2e.ts`), use `/e2e-tests` instead.
- This skill is for pure function unit tests (`.test.ts`) only.
