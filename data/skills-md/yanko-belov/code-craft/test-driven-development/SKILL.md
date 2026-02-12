---
name: test-driven-development
description: Use when implementing any new feature or function. Use when asked to "add tests later". Use when writing code before tests.
---

# Test-Driven Development (TDD)

## Overview

**Write the test first. Watch it fail. Then write the code.**

TDD is not about testing - it's about design. Writing tests first forces you to think about the interface before the implementation.

## When to Use

- Implementing any new function, method, or feature
- Asked to "write code now, add tests later"
- Fixing a bug (write test that reproduces it first)
- Refactoring existing code

## The Iron Rule

```
NEVER write production code without a failing test first.
```

**No exceptions:**
- Not for "it's a simple function"
- Not for "we'll add tests later"
- Not for "I already know how to implement it"
- Not for "tests slow me down"

## The TDD Cycle

```
RED → GREEN → REFACTOR → REPEAT
```

1. **RED**: Write a failing test
2. **GREEN**: Write minimal code to pass
3. **REFACTOR**: Clean up while tests pass
4. **REPEAT**: Next test case

## Detection: Code-First Smell

If you're about to write implementation without a test, STOP:

```typescript
// ❌ VIOLATION: Implementation first
function calculateDiscount(total: number): number {
  return total > 100 ? total * 0.1 : 0;
}
// "We'll add tests later if needed"

// ✅ CORRECT: Test first
describe('calculateDiscount', () => {
  it('returns 10% discount for orders over $100', () => {
    expect(calculateDiscount(150)).toBe(15);
  });
  
  it('returns 0 for orders $100 or less', () => {
    expect(calculateDiscount(100)).toBe(0);
    expect(calculateDiscount(50)).toBe(0);
  });
});

// NOW write the implementation
function calculateDiscount(total: number): number {
  return total > 100 ? total * 0.1 : 0;
}
```

## Why Test-First Matters

| Test-After | Test-First |
|------------|------------|
| Tests verify what code does | Tests define what code should do |
| Implementation drives design | Requirements drive design |
| Tests often skipped | Tests always exist |
| Hard to test = poor design | Hard to test = caught early |
| "Does it work?" | "Is it right?" |

## Pressure Resistance Protocol

### 1. "We'll Add Tests Later"
**Pressure:** "Just write the function, we can test it later"

**Response:** "Later" never comes. Tests written after are weaker and often skipped entirely.

**Action:** Write the test now. It takes 30 seconds.

### 2. "It's Too Simple to Test"
**Pressure:** "This function is trivial, testing is overkill"

**Response:** Simple functions grow complex. Simple bugs cause outages. Test everything.

**Action:** Write the test. Simple functions = simple tests.

### 3. "I Know How to Implement It"
**Pressure:** "I already have the solution in my head"

**Response:** TDD isn't about uncertainty - it's about capturing requirements as executable specs.

**Action:** Write the test first. Prove your mental model is correct.

### 4. "Tests Slow Me Down"
**Pressure:** "Writing tests takes extra time"

**Response:** Debugging takes 10x longer than testing. TDD is faster overall.

**Action:** The test you write now saves hours of debugging later.

## Red Flags - STOP and Reconsider

- Writing any function without a test
- "Let me just get it working first"
- Implementation file open without test file
- Committing code without corresponding tests
- Tests that pass immediately (never saw them fail)

**All of these mean: Stop. Write the test first.**

## Quick Reference

| Situation | TDD Response |
|-----------|--------------|
| New feature | Write failing test → implement |
| Bug fix | Write test that reproduces bug → fix |
| Refactor | Ensure tests exist → refactor → tests pass |
| "Tests later" | Tests now. Always now. |

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "Tests slow me down" | Debugging slows you down more. |
| "It's too simple" | Simple tests are fast to write. |
| "I'll test later" | You won't. Test now. |
| "I know it works" | Prove it with a test. |
| "Tests are for QA" | Tests are for developers. |
| "Just a prototype" | Prototypes become production. Test them. |

## The Bottom Line

**Test first. Code second. No exceptions.**

The test is the specification. The test is the documentation. The test is the safety net. Write it first, every time.
