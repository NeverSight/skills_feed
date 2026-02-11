---
name: code-quality
description: >-
  Code quality standards: warnings-as-errors, no underscore prefixes for unused vars,
  mandatory test coverage. Apply to any TypeScript, JavaScript, Rust, or Python project.
  Triggers: code review, linting, writing new functions, refactoring.
---

# Code Quality Standards

## Unused Variables

- NEVER prefix unused variables with underscore (_) to silence linters
- Either USE the variable or REMOVE it entirely
- If a function parameter is required by an interface but unused, restructure to avoid it
- Exception: destructuring where you need to skip positional elements (rare)

## Warnings Are Errors

- Treat ALL compiler/linter warnings as errors that must be fixed
- Do not leave warnings for "later" -- fix them now
- Common warnings to watch: unused imports, unreachable code, implicit any

## Test Coverage

- Every new function or module MUST have corresponding tests
- Test the happy path AND at least one error/edge case
- Run existing tests after changes to verify nothing breaks

## Type Safety

- Never use `as any`, `@ts-ignore`, or `@ts-expect-error` to suppress type errors
- Never use empty catch blocks `catch(e) {}`
- Never delete failing tests to make the suite "pass"

## Formatting

- Always run the project's formatter after editing any file
- Verify formatting before committing
