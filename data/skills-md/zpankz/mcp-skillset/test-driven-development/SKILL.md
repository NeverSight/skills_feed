---
name: test-driven-development
description: Use when implementing any feature or bugfix, before writing implementation code - write the test first, watch it fail, write minimal code to pass; ensures tests actually verify behavior by requiring failure first
---

# Test-Driven Development (TDD)

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

**Violating the letter of the rules is violating the spirit of the rules.**

## When to Use

**Always:**

- New features
- Bug fixes
- Refactoring
- Behavior changes

**Exceptions (ask your human partner):**

- Throwaway prototypes
- Generated code
- Configuration files

Thinking "skip TDD just this once"? Stop. That's rationalization.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over.

**No exceptions:**

- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete

Implement fresh from tests. Period.

## Progressive Loading

**L2 Content** (loaded when methodology details needed):
- See: [references/methodology.md](./references/methodology.md)
  - Red-Green-Refactor Cycle
  - Good Tests Principles
  - Why Order Matters
  - Common Rationalizations
  - Verification Checklist

**L3 Content** (loaded when advanced patterns needed):
- See: [references/anti-patterns.md](./references/anti-patterns.md)
  - Testing Mock Behavior
  - Test-Only Methods
  - Mocking Without Understanding
  - Incomplete Mocks
  - Integration Tests as Afterthought
  - Quick Reference Guide
