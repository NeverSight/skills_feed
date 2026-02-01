---
name: accelint-ts-testing
description: Use when writing, reviewing, or refactoring vitest tests. Load when you see *.test.ts or *.spec.ts files, nested describe blocks, loose assertions (toBeTruthy), over-mocking, slow tests, or async testing needs. Covers AAA pattern, parameterized tests, test doubles hierarchy, mock cleanup, test isolation, and performance optimization. Keywords include vitest, testing, TDD, assertions, mocks, stubs, fakes, spies, beforeEach, describe, it, expect, vi.mock, it.each.
compatibility: Requires vitest testing framework
license: Apache-2.0
metadata:
  author: accelint
  version: "1.0"
---

# Vitest Best Practices

Comprehensive patterns for writing maintainable, effective vitest tests. Focused on expert-level guidance for test organization, clarity, and performance.

## NEVER Do When Writing Vitest Tests

- **NEVER skip global mock cleanup configuration** - Manual cleanup appears safe but creates "action at a distance" failures: a mock in test file A leaks into test file B running 3 files later, causing non-deterministic failures that only appear when tests run in specific orders. These Heisenbugs waste hours in CI debugging. Configure `clearMocks: true`, `resetMocks: true`, `restoreMocks: true` in `vitest.config.ts` once to eliminate this entire class of order-dependent failure.
- **NEVER nest describe blocks more than 2 levels deep** - Deep nesting creates cognitive overhead and excessive indentation. Put context in test names instead: `it('should add item to empty cart')` vs `describe('when cart is empty', () => describe('addItem', ...))`.
- **NEVER mock your own pure functions** - Mocking internal code makes tests brittle and less valuable. Mock only external dependencies (APIs, databases, third-party libraries). Prefer fakes > stubs > spies > mocks.
- **NEVER use loose assertions like `toBeTruthy()` or `toBeDefined()`** - These assertions pass for multiple distinct values you never intended: `toBeTruthy()` passes for `1`, `"false"`, `[]`, and `{}` - all semantically different. When refactoring changes `getUser()` from returning `{id: 1}` to returning `1`, your test still passes but your production code breaks. Loose assertions create false confidence that evaporates in production. `toBeTypeOf()` is NOT a loose assertion.
- **NEVER test implementation details instead of behavior** - Tests that verify "function X was called 3 times" create false failures: you optimize code to call X once via memoization, all tests fail, yet the user experience is identical (and faster). These tests actively punish performance improvements and refactoring. Test what users observe (outputs given inputs), not how your code achieves it internally.
- **NEVER share mutable state between tests** - Tests that depend on execution order or previous test state create flaky, unreliable suites. Each test must be fully independent with fresh setup.
- **NEVER use `any` or skip type checking in test files** - When implementation signatures change, tests with `as any` silently pass while calling functions with wrong arguments. You ship broken code that TypeScript could have caught. Tests are executable documentation: `user as any` communicates nothing, but `createTestUser(Partial<User>)` shows exactly what properties matter for this test case.

## Before Writing Tests, Ask

Apply these expert thinking patterns before implementing tests:

### Test Isolation and Setup
- **Where should cleanup logic live?** Think in layers: configuration eliminates entire error classes (mock cleanup in vitest.config.ts), setup files handle project-wide concerns (custom matchers, global mocks), beforeEach handles test-specific state. Each test doing its own mock cleanup is like each function doing its own null checks - it works but misses the point. Push concerns to the highest appropriate layer.
- **Does this test depend on previous tests or shared state?** Test suites are parallel universes - each test should work identically whether it runs first, last, or alone. State dependency creates "quantum tests" that pass or fail based on execution order. If a test needs data from another test, they're actually one test split artificially.

### What to Test
- **Am I testing behavior or implementation?** Test what users experience (inputs → outputs), not how code achieves it (which functions were called). Implementation tests break during safe refactoring.
- **What's the simplest dependency I can use?** Real implementation > fake > stub > spy > mock. Each step down this hierarchy adds brittleness. Mock only when using real code is impractical (external APIs, slow operations).

### Test Clarity
- **Can someone understand this test in 5 seconds?** Follow AAA pattern (Arrange, Act, Assert) with clear boundaries. If setup is complex, extract to helper functions with descriptive names.
- **Are there multiple variations of the same behavior?** Use `it.each()` for parameterized tests instead of copying test structure. One assertion per concept keeps tests focused.

### Performance and Maintenance
- **Will this test still be valuable in 6 months?** Avoid testing framework internals or trivial operations. Focus on business logic, edge cases, and error handling that actually prevent bugs.
- **Is this test fast enough to run on every save?** Avoid expensive operations in tests. Use fakes for databases, mock timers for delays, stub external calls. Tests should complete in milliseconds.

## What This Skill Covers

Expert guidance on vitest testing patterns:

1. **Organization** - File placement, naming, describe block structure
2. **AAA Pattern** - Arrange, Act, Assert for instant clarity
3. **Parameterized Tests** - Using `it.each()` to reduce duplication
4. **Error Handling** - Testing exceptions, edge cases, fault injection
5. **Assertions** - Strict assertions to catch unintended values
6. **Test Doubles** - Fakes, stubs, mocks, spies hierarchy and when to use each
7. **Async Testing** - Promises, async/await, timers, concurrent tests
8. **Performance** - Fast tests through efficient setup and global config
9. **Vitest Features** - Coverage, watch mode, setup files, config discovery
10. **Snapshot Testing** - When snapshots help vs hurt maintainability

## How to Use

This skill uses a **progressive disclosure** structure to minimize context usage:

### 1. Start with the Overview (AGENTS.md)
Read [AGENTS.md](AGENTS.md) for a concise overview of all rules with one-line summaries and the workflow for discovering existing test configuration.

### 2. Check for Existing Test Configuration
Before writing tests:
- First check `vitest.config.ts` for global mock cleanup settings (`clearMocks`, `resetMocks`, `restoreMocks`)
- Then search for setup files (`test/setup.ts`, `vitest.setup.ts`, etc.) and analyze their configuration
- See the workflow in [AGENTS.md](AGENTS.md#workflow-before-writing-tests)

### 3. Load Specific Rules as Needed
Use these explicit triggers to know when to load each reference file:

**MANDATORY Loading (load entire file):**
- **Writing async tests with promises/timers** → [async-testing.md](references/async-testing.md)
- **Working with mocks, stubs, spies, or fakes** → [test-doubles.md](references/test-doubles.md)

**Load When You See These Patterns:**
- **Nested describe blocks >2 levels deep** → [organization.md](references/organization.md)
- **Test files not co-located with implementation** → [organization.md](references/organization.md)
- **Tests without clear Arrange/Act/Assert structure** → [aaa-pattern.md](references/aaa-pattern.md)
- **Duplicate test code with slight variations** → [parameterized-tests.md](references/parameterized-tests.md)
- **Missing error case tests or inadequate edge case coverage** → [error-handling.md](references/error-handling.md)
- **Loose assertions like `toBeTruthy()` or `toBeDefined()`** → [assertions.md](references/assertions.md)
- **Tests running slow (>100ms per test)** → [performance.md](references/performance.md)
- **Need coverage, watch mode, or vitest-specific features** → [vitest-features.md](references/vitest-features.md)
- **Considering or reviewing snapshot tests** → [snapshot-testing.md](references/snapshot-testing.md)

**Do NOT Load Unless Specifically Needed:**
- Do NOT load [performance.md](references/performance.md) if tests are fast (<50ms)
- Do NOT load [snapshot-testing.md](references/snapshot-testing.md) unless snapshots are mentioned
- Do NOT load [vitest-features.md](references/vitest-features.md) for basic test writing

### 4. Apply the Pattern
Each reference file contains:
- ❌ Incorrect examples showing the anti-pattern
- ✅ Correct examples showing the optimal implementation
- Explanations of why the pattern matters

## Quick Example

See [quick-start.md](references/quick-start.md) for a complete before/after example showing how this skill transforms unclear tests into clear, maintainable ones.
