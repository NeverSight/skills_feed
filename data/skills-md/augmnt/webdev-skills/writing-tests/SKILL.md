---
name: writing-tests
description: Guides test creation with practical strategies for unit, integration, and e2e tests. Use when writing tests, deciding what to test, setting up test infrastructure, or discussing coverage. Triggers on "write tests", "should I test", "test coverage", or test file creation.
---

# Writing Tests

Test behavior, not implementation. Prioritize by risk.

## When to Use Each Type

| Type | What | When | Tools |
|------|------|------|-------|
| Unit | Single function/hook | Pure logic, calculations | Vitest, Jest |
| Integration | Component + deps | Forms, data display | Testing Library |
| E2E | Full user flow | Critical paths | Playwright |

## Always Test

- Auth flows
- Payment/checkout
- Data mutations (create, update, delete)
- Authorization rules
- Critical business logic

## Rarely Test

- Static content
- Third-party internals
- Pure styling

## File Organization

```
src/components/Button/
├── Button.tsx
└── Button.test.tsx      # Colocated

e2e/                     # E2E at root
├── auth.spec.ts
└── checkout.spec.ts
```

## Patterns

### Arrange-Act-Assert

```typescript
test('increments on click', () => {
  // Arrange
  render(<Counter initial={0} />)
  // Act
  fireEvent.click(screen.getByRole('button'))
  // Assert
  expect(screen.getByText('1')).toBeInTheDocument()
})
```

### Query Priority (best → worst)

1. `getByRole` - semantic, accessible
2. `getByLabelText` - form inputs
3. `getByText` - content
4. `getByTestId` - last resort

### Test Behavior, Not Implementation

```typescript
// ❌ Implementation
expect(component.state.isOpen).toBe(true)

// ✅ Behavior
expect(screen.getByRole('dialog')).toBeVisible()
```

## Minimum Viable Testing

If time-constrained:
1. E2E for happy paths (covers most ground)
2. Unit for complex logic (catches edge cases)
3. Integration for critical components (forms, data)

## Advanced Patterns

For API mocking, test fixtures, and coverage guidance, see [MOCKING.md](MOCKING.md).
