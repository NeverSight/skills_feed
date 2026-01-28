---
name: analyzing-test-coverage
description: "Creates and analyzes tests using Vitest and MSW patterns. Generates test builders, mocks repositories, and configures integration tests. Triggers on: write tests, test coverage, Vitest, MSW mock, vi.fn, vi.mock, unit test, integration test, test builder, mock setup, test failure."
allowed-tools: "Read, Grep, Glob, Write, Edit, Bash(pnpm test:*)"
---

# Testing Strategy Analyst

## Purpose

Guide the creation of comprehensive tests following project patterns for unit tests, integration tests, and E2E tests using Vitest, MSW, and project-specific test helpers.

## When to Use

- Writing new tests
- Analyzing test coverage gaps
- Setting up mocks for testing
- Organizing test files
- Debugging test failures

## Table of Contents

- [Testing Stack](#testing-stack)
- [Test Organization](#test-organization)
- [Quick Pattern Reference](#quick-pattern-reference)
- [Running Tests](#running-tests)
- [Test Quality Checklist](#test-quality-checklist)
- [Common Pitfalls](#common-pitfalls)
- [References](#references)

## Testing Stack

| Tool | Purpose |
|------|---------|
| **Vitest** | Test runner and assertion library |
| **MSW** | Mock Service Worker for network mocking |
| **vi** | Vitest mock utilities |
| **test-helpers/** | Project-specific test utilities |

## Test Organization

```
src/
├── modules/
│   └── category/
│       ├── category-service.ts
│       ├── category-service.test.ts        # Unit tests
│       ├── repository.ts
│       ├── repository.test.ts              # Repository tests
│       └── category.integration.test.ts    # Integration tests
├── core/
│   └── diff/
│       └── comparators/
│           ├── category-comparator.ts
│           └── category-comparator.test.ts
├── test-helpers/
│   ├── config-file-builder.ts
│   ├── graphql-mocks.ts
│   ├── config-fixtures.ts
│   └── cli-runner.ts
└── lib/
    └── test-setup.ts                       # Global test setup

e2e/
└── ...                                     # End-to-end tests
```

## Quick Pattern Reference

### Service Tests
See `references/patterns.md` for full examples. Key structure:
- Declare dependencies at suite level
- Reset mocks in `beforeEach` with `vi.clearAllMocks()`
- Use describe blocks for method grouping
- Follow **Arrange-Act-Assert** pattern

### Repository Tests with MSW
See `references/patterns.md` for MSW setup. Key steps:
1. Define handlers with `graphql.query()` / `graphql.mutation()`
2. Setup server with `beforeAll` / `afterAll`
3. Override handlers for specific test cases with `server.use()`

### Test Data Builders
See `references/test-builders.md` for implementations. Pattern:
- Create builder class with fluent interface
- Validate with Zod schema in `build()`
- Provide factory functions for convenience

### Mock Functions
See `references/patterns.md` for examples. Common patterns:
- `vi.fn()` for simple mocks
- `vi.mocked()` for typed access
- `vi.mock()` for module mocking

## Running Tests

```bash
# Run all tests
pnpm test

# Run specific test file
pnpm test -- --filter=category-service

# Run tests matching pattern
pnpm test -- --grep="should create category"

# Watch mode
pnpm test -- --watch

# With coverage
pnpm test -- --coverage
```

See `references/commands-reference.md` for advanced options and coverage configuration.

## Test Quality Checklist

### For Every Test

- [ ] Follows Arrange-Act-Assert pattern
- [ ] Has descriptive test name
- [ ] Tests one thing per test
- [ ] Includes both positive and negative cases
- [ ] Uses typed mocks (not `any`)
- [ ] Cleans up after itself (beforeEach/afterEach)

### For Test Suites

- [ ] Covers all public methods
- [ ] Covers error scenarios
- [ ] Covers edge cases
- [ ] Uses schema-validated test data
- [ ] Has integration tests for complex flows

## Validation Checkpoints

| Phase | Validate | Command |
|-------|----------|---------|
| Test written | File exists | Check `*.test.ts` created |
| Tests pass | All green | `pnpm test <file>` |
| Coverage adequate | Key paths covered | `pnpm test --coverage` |
| Mocks typed | No `any` in mocks | `npx tsc --noEmit` |

## Common Pitfalls

**Not Resetting Mocks**:
```typescript
beforeEach(() => {
  vi.clearAllMocks(); // Always reset!
});
```

**Testing Implementation Details**:
```typescript
// BAD - tests internal structure
expect(service.internalMap.size).toBe(1);

// GOOD - tests behavior
expect(await service.findBySlug('test')).toBeDefined();
```

**Flaky Async Tests**:
```typescript
// BAD - race condition
const result = service.process();
expect(result).toBe(expected);

// GOOD - await properly
const result = await service.process();
expect(result).toBe(expected);
```

## References

### Skill Reference Files
- `references/patterns.md` - Detailed test patterns with full code examples
- `references/test-builders.md` - Builder pattern implementations
- `references/commands-reference.md` - Complete command reference

### Project Resources
- `{baseDir}/src/test-helpers/` - Test utilities
- `{baseDir}/vitest.config.ts` - Test configuration
- `{baseDir}/docs/TESTING_PROTOCOLS.md` - Testing protocols

### External Documentation
- Vitest docs: https://vitest.dev
- MSW docs: https://mswjs.io

## Related Skills

- **Complete entity workflow**: See `adding-entity-types` for E2E implementation including tests
- **Zod test patterns**: See `designing-zod-schemas` for schema validation tests
- **GraphQL mocking**: See `writing-graphql-operations` for MSW handlers

## Quick Reference Rule

For a condensed quick reference, see `.claude/rules/testing-standards.md` (automatically loaded when editing `*.test.ts` files).
