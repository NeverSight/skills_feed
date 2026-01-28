---
name: test-driven-development
description: Use when implementing any feature or bugfix, before writing implementation code. Enforces RED-GREEN-REFACTOR cycle with strict discipline against rationalization.
---

# Test-Driven Development

## The Iron Law of TDD

**Write code before test? Delete it. Start over.**

This is not negotiable. This is not optional. You cannot rationalize your way out of this.

## The RED-GREEN-REFACTOR Cycle

### 1. RED - Write a Failing Test First
- Write the smallest test that fails for the right reason
- The test should fail because the feature doesn't exist yet
- Run the test and verify it fails

### 2. GREEN - Make It Pass (Minimum Code)
- Write the minimum code to make the test pass
- Don't write more than necessary
- Don't optimize yet
- Don't refactor yet

### 3. REFACTOR - Improve the Code
- Now you can clean up
- Remove duplication
- Improve naming
- Extract methods/functions
- All tests must still pass after refactoring

## Forbidden Rationalizations

If you catch yourself thinking ANY of these, STOP:

- "This is just a simple function" → WRONG. Simple functions need tests.
- "I'll write tests after" → WRONG. That's not TDD.
- "Let me just get it working first" → WRONG. Tests first.
- "This doesn't need a test" → WRONG. Everything needs tests.
- "I'll test it manually" → WRONG. Write automated tests.
- "The test is obvious" → WRONG. Write it anyway.
- "I'm just exploring" → WRONG. Explore with tests.

## Test Quality Guidelines

### Good Tests Are:
- **Fast** - Tests should run in milliseconds
- **Isolated** - No dependencies between tests
- **Repeatable** - Same result every time
- **Self-validating** - Pass or fail, no interpretation
- **Timely** - Written before the code

### Test Structure (Arrange-Act-Assert):
```
// Arrange - Set up the test conditions
const input = createTestInput();

// Act - Execute the code under test
const result = functionUnderTest(input);

// Assert - Verify the expected outcome
expect(result).toBe(expectedValue);
```

## When to Use This Skill

- Starting any new feature
- Fixing any bug (write a test that reproduces the bug first)
- Refactoring existing code (ensure tests exist first)
- Any code change that could break existing functionality

## YAGNI (You Aren't Gonna Need It)

Don't write code you don't need yet:
- No speculative features
- No "just in case" abstractions
- No premature optimization
- Build what's needed now, nothing more

## DRY (Don't Repeat Yourself)

But only during REFACTOR phase:
- First make it work (GREEN)
- Then make it right (REFACTOR)
- Duplication is okay temporarily
- Remove it during refactor

## Commit Strategy

- Commit after each GREEN
- Commit after each REFACTOR
- Small, frequent commits
- Each commit should pass all tests
