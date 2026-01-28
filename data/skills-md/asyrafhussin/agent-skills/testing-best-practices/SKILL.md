---
name: testing-best-practices
description: Unit testing, integration testing, and test-driven development principles. Use when writing tests, reviewing test code, improving test coverage, or setting up testing strategy. Triggers on "write tests", "review tests", "testing best practices", or "TDD".
---

# Testing Best Practices

Unit testing, integration testing, and TDD principles for reliable, maintainable test suites. Guidelines for writing effective tests that provide confidence and documentation.

## When to Apply

Reference these guidelines when:
- Writing unit tests
- Writing integration tests
- Reviewing test code
- Improving test coverage
- Setting up testing strategy

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Test Structure | CRITICAL | `struct-` |
| 2 | Test Isolation | CRITICAL | `iso-` |
| 3 | Assertions | HIGH | `assert-` |
| 4 | Test Data | HIGH | `data-` |
| 5 | Mocking | MEDIUM | `mock-` |
| 6 | Coverage | MEDIUM | `cov-` |
| 7 | Performance | LOW | `perf-` |

## Quick Reference

### 1. Test Structure (CRITICAL)

- `struct-aaa` - Arrange, Act, Assert pattern
- `struct-naming` - Descriptive test names
- `struct-one-assert` - One logical assertion per test
- `struct-describe-it` - Organized test suites
- `struct-given-when-then` - BDD style when appropriate

### 2. Test Isolation (CRITICAL)

- `iso-independent` - Tests run independently
- `iso-no-shared-state` - No shared mutable state
- `iso-deterministic` - Same result every run
- `iso-no-order-dependency` - Run in any order
- `iso-cleanup` - Clean up after tests

### 3. Assertions (HIGH)

- `assert-specific` - Specific assertions
- `assert-meaningful-messages` - Helpful failure messages
- `assert-expected-first` - Expected value first
- `assert-no-magic-numbers` - Use named constants

### 4. Test Data (HIGH)

- `data-factories` - Use factories/builders
- `data-minimal` - Minimal test data
- `data-realistic` - Realistic edge cases
- `data-fixtures` - Manage test fixtures

### 5. Mocking (MEDIUM)

- `mock-only-boundaries` - Mock at boundaries
- `mock-verify-interactions` - Verify important calls
- `mock-minimal` - Don't over-mock
- `mock-realistic` - Realistic mock behavior

### 6. Coverage (MEDIUM)

- `cov-meaningful` - Focus on meaningful coverage
- `cov-edge-cases` - Cover edge cases
- `cov-unhappy-paths` - Test error scenarios
- `cov-not-100-percent` - 100% isn't the goal

### 7. Performance (LOW)

- `perf-fast-unit` - Unit tests run fast
- `perf-slow-integration` - Integration tests can be slower
- `perf-parallel` - Run tests in parallel

## Essential Guidelines

For detailed examples, see the rule files in the `rules/` directory.

### AAA Pattern (Arrange, Act, Assert)

```typescript
it('calculates total with discount', () => {
  // Arrange - set up test data
  const cart = new ShoppingCart();
  cart.addItem({ name: 'Book', price: 20 });
  cart.applyDiscount(0.1);

  // Act - execute the code under test
  const total = cart.getTotal();

  // Assert - verify the result
  expect(total).toBe(18);
});
```

### Descriptive Test Names

```typescript
// ✅ Describes behavior and scenario
describe('UserService.register', () => {
  it('creates user with hashed password', () => {});
  it('throws ValidationError when email is invalid', () => {});
  it('sends welcome email after successful registration', () => {});
});

// ❌ Vague names
it('test1', () => {});
it('should work', () => {});
```

### Test Isolation

```typescript
// ✅ Each test sets up its own data
beforeEach(() => {
  mockRepository = { save: jest.fn(), find: jest.fn() };
  service = new OrderService(mockRepository);
});

// ❌ Shared state between tests
let globalOrder: Order; // Tests depend on each other
```

## Test Pyramid

```
        /\
       /  \      E2E Tests (few)
      /----\     - Test critical user flows
     /      \    - Slow, expensive
    /--------\   Integration Tests (some)
   /          \  - Test component interactions
  /------------\ - Database, API calls
 /              \ Unit Tests (many)
/----------------\ - Fast, isolated
                   - Test single units
```

## Output Format

When reviewing tests, output findings:

```
file:line - [category] Description of issue
```

Example:
```
tests/user.test.ts:15 - [struct] Missing Arrange/Act/Assert separation
tests/order.test.ts:42 - [iso] Test depends on previous test's state
tests/cart.test.ts:28 - [assert] Multiple unrelated assertions in one test
```

## How to Use

Read individual rule files for detailed explanations:

```
rules/struct-aaa-pattern.md
rules/iso-independent-tests.md
rules/data-factories.md
```

## References

This skill is built on testing best practices from:
- **Jest**: https://jestjs.io
- **Vitest**: https://vitest.dev
- **Testing Library**: https://testing-library.com
- Kent C. Dodds' testing principles
- TDD by Kent Beck
- Working Effectively with Legacy Code by Michael Feathers

## Metadata

- **Version**: 1.0.0
- **Rule Count**: 23 rules across 7 categories
- **License**: MIT
- **Last Updated**: 2026-01-17

## Contributing

These rules are derived from industry best practices and testing community standards. For detailed examples and additional context, refer to the individual rule files in the `rules/` directory.
