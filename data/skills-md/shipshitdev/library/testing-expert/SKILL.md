---
name: testing-expert
description: Expert in testing strategies for React, Next.js, and NestJS applications covering unit tests, integration tests, E2E tests, and testing best practices
---

# Testing Expert Skill

Expert in testing strategies for React, Next.js, and NestJS applications.

## When to Use This Skill

- Writing unit tests
- Creating integration tests
- Setting up E2E tests
- Testing React components
- Testing API endpoints
- Testing database operations
- Setting up test infrastructure
- Reviewing test coverage

## Project Context Discovery

1. **Scan Documentation:** Check `.agent/SYSTEM/ARCHITECTURE.md` for testing architecture
2. **Identify Tools:** Jest/Vitest, React Testing Library, Supertest, Playwright/Cypress
3. **Discover Patterns:** Review existing test files, utilities, mocking patterns
4. **Use Project-Specific Skills:** Check for `[project]-testing-expert` skill

## Core Testing Principles

### Testing Pyramid

- **Unit Tests** (70%): Fast, isolated, test individual functions/components
- **Integration Tests** (20%): Test component interactions
- **E2E Tests** (10%): Test full user flows

### Coverage Targets

- Line coverage: > 80%
- Branch coverage: > 75%
- Function coverage: > 85%
- Critical paths: 100%

### Test Organization

```
src/
  users/
    users.controller.ts
    users.controller.spec.ts  # Unit tests
    users.service.ts
    users.service.spec.ts
  __tests__/
    integration/
    e2e/
```

### Test Quality (AAA Pattern)

```typescript
it('should return users filtered by organization', async () => {
  // Arrange: Set up test data
  const organizationId = 'org1';
  const expectedUsers = [{ organization: organizationId }];

  // Act: Execute the code being tested
  const result = await service.findAll(organizationId);

  // Assert: Verify the result
  expect(result).toEqual(expectedUsers);
});
```

## Good Tests Are

- Independent (no test dependencies)
- Fast (< 100ms each)
- Repeatable (same result every time)
- Meaningful (test real behavior)
- Maintainable (easy to update)

## Testing Best Practices Summary

1. **Test Isolation:** Each test independent, clean up after
2. **Meaningful Tests:** Test behavior, not implementation
3. **Mocking Strategy:** Mock external dependencies, not what you're testing
4. **Test Data:** Use factories, keep data minimal, clean up
5. **Coverage:** High coverage, focus on critical paths

## Integration

| Test Type | Tools | Use Case |
|-----------|-------|----------|
| Unit | Jest/Vitest | Functions, components, services |
| Integration | Supertest + Jest | Controller + Service + DB |
| E2E | Playwright/Cypress | Full user flows |
| Component | React Testing Library | React component behavior |

---

**For complete React Testing Library examples, hook testing, Next.js page/API testing, NestJS service/controller testing, integration test setup, E2E test patterns, MongoDB testing, authentication helpers, test fixtures, and mocking patterns, see:** `references/full-guide.md`
