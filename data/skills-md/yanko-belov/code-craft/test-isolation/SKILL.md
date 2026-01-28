---
name: test-isolation
description: Use when writing tests that share state. Use when tests depend on other tests. Use when test order matters.
---

# Test Isolation

## Overview

**Each test must be independent. No shared state. No dependencies between tests.**

Tests that depend on each other are brittle, hard to debug, and can't run in parallel. Every test should set up its own state and clean up after itself.

## When to Use

- Writing any test that uses shared data
- Tests that must run in a specific order
- Tests that fail randomly or when run alone
- Test suites that can't run in parallel

## The Iron Rule

```
NEVER let one test depend on another test's state or execution.
```

**No exceptions:**
- Not for "it's more efficient"
- Not for "the first test creates the data"
- Not for "they always run in order"
- Not for "it works on my machine"

## Detection: Dependency Smell

If tests share mutable state or depend on order, STOP:

```typescript
// ❌ VIOLATION: Tests depend on each other
describe('UserService', () => {
  let userService: UserService;
  let createdUserId: string;  // Shared state!
  
  it('creates a user', async () => {
    const user = await userService.create({ name: 'Alice' });
    createdUserId = user.id;  // First test sets state
    expect(user).toBeDefined();
  });
  
  it('finds the created user', async () => {
    const user = await userService.findById(createdUserId);  // Second test uses it
    expect(user.name).toBe('Alice');
  });
});
```

Problems:
- Second test fails if first doesn't run
- Can't run tests in parallel
- Random failures when order changes

## The Correct Pattern: Isolated Tests

Each test manages its own state:

```typescript
// ✅ CORRECT: Each test is independent
describe('UserService', () => {
  let userService: UserService;
  
  beforeEach(() => {
    userService = new UserService(new InMemoryUserRepo());
  });
  
  afterEach(() => {
    // Clean up if needed
  });
  
  it('creates a user', async () => {
    const user = await userService.create({ name: 'Alice' });
    expect(user.id).toBeDefined();
    expect(user.name).toBe('Alice');
  });
  
  it('finds a user by id', async () => {
    // Arrange: Create own test data
    const created = await userService.create({ name: 'Bob' });
    
    // Act
    const found = await userService.findById(created.id);
    
    // Assert
    expect(found.name).toBe('Bob');
  });
  
  it('returns null for non-existent user', async () => {
    // No setup needed - tests the empty state
    const found = await userService.findById('non-existent');
    expect(found).toBeNull();
  });
});
```

## Isolation Techniques

### 1. Fresh Instance Per Test
```typescript
beforeEach(() => {
  service = new Service(new MockDependency());
});
```

### 2. Database Transactions
```typescript
beforeEach(async () => {
  await db.beginTransaction();
});

afterEach(async () => {
  await db.rollback();  // Undo all changes
});
```

### 3. In-Memory Stores
```typescript
beforeEach(() => {
  repository = new InMemoryRepository();  // Fresh empty store
});
```

### 4. Factory Functions
```typescript
function createTestUser(overrides = {}) {
  return { id: uuid(), name: 'Test', ...overrides };
}

it('test 1', () => {
  const user = createTestUser({ name: 'Alice' });
});

it('test 2', () => {
  const user = createTestUser({ name: 'Bob' });  // Own data
});
```

## Pressure Resistance Protocol

### 1. "It's More Efficient"
**Pressure:** "Creating data once and reusing is faster"

**Response:** Shared state causes random failures that waste hours debugging.

**Action:** Use `beforeEach` to create fresh state. The milliseconds saved aren't worth the debugging time.

### 2. "The First Test Creates Data"
**Pressure:** "Test 1 creates a user, Test 2 verifies it"

**Response:** This creates implicit coupling. Test 2 can't run alone.

**Action:** Each test creates its own data in Arrange phase.

### 3. "They Always Run In Order"
**Pressure:** "Our test runner executes sequentially"

**Response:** Test runners parallelize. CI environments differ. Order assumptions break.

**Action:** Write tests that pass regardless of order.

## Red Flags - STOP and Reconsider

- Variables declared outside tests and mutated inside
- Tests that fail when run individually
- Tests that fail when run in different order
- `beforeAll` that creates data used by multiple tests
- Comments like "run after test X"

**All of these mean: Refactor for isolation.**

## Quick Reference

| Shared State (Bad) | Isolated (Good) |
|-------------------|-----------------|
| `let userId` outside tests | Create user in each test |
| `beforeAll` creates data | `beforeEach` creates fresh data |
| Tests modify shared object | Each test has own instance |
| Order-dependent execution | Any order works |

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It's more efficient" | Debugging flaky tests is inefficient. |
| "They run in order" | Not in parallel mode or different environments. |
| "It works locally" | It'll fail in CI. |
| "Just this one time" | One coupling leads to more. |
| "The data is read-only" | Until someone adds a write. |

## The Bottom Line

**Every test stands alone. No shared state. No order dependencies.**

If a test can't run by itself and pass, it's not a valid test. Each test creates what it needs, verifies what it should, and cleans up after itself.
