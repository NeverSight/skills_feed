---
name: test-auto
description: Create test suites with unit, integration, and e2e tests. Use when setting up tests, improving coverage, or when user asks about testing.
---

# Test Automation

Create comprehensive test suites following the testing pyramid.

## When to Use

- Setting up tests for new code
- User asks to "add tests" or "improve coverage"
- Before refactoring (add tests first)
- Implementing CI/CD test pipelines

## Testing Pyramid

```
    /\        E2E (few, critical paths)
   /  \       Integration (moderate)
  /____\      Unit (many, fast)
```

## Test Structure

### Unit Tests

- Test individual functions/methods
- Mock external dependencies
- Fast execution (<100ms per test)
- High coverage (>80%)

### Integration Tests

- Test component interactions
- Use test databases/containers
- Moderate execution time
- Cover critical integrations

### E2E Tests

- Test complete user flows
- Use Playwright/Cypress
- Slowest execution
- Cover happy paths only

## Test Patterns

```javascript
// Arrange-Act-Assert
describe("UserService", () => {
  it("should create user with valid data", async () => {
    // Arrange
    const userData = { name: "Test", email: "test@example.com" };

    // Act
    const result = await userService.create(userData);

    // Assert
    expect(result.id).toBeDefined();
    expect(result.name).toBe("Test");
  });
});
```

## Output

- Test files with clear naming
- Mock/stub implementations
- Test data factories
- Coverage configuration
- CI pipeline integration

## Examples

**Input:** "Add tests for the auth module"
**Action:** Analyze auth module, create unit tests for functions, integration tests for flows

**Input:** "Set up testing for this project"
**Action:** Detect framework, configure test runner, create example tests, add CI config
