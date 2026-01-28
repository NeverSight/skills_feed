---
name: aaa-pattern
description: Use when writing tests. Use when test structure is unclear. Use when arrange/act/assert phases are mixed.
---

# AAA Pattern (Arrange-Act-Assert)

## Overview

**Every test has three phases: Arrange, Act, Assert. Keep them separate.**

Clear structure makes tests readable, maintainable, and debuggable. When phases blur together, tests become confusing.

## When to Use

- Writing any test
- Test logic is hard to follow
- Unclear what's being tested
- Multiple actions or assertions mixed together

## The Iron Rule

```
EVERY test must have clearly separated Arrange, Act, and Assert phases.
```

**No exceptions:**
- Not for "it's a simple test"
- Not for "it's more concise this way"
- Not for "the phases are obvious"

## Detection: Mixed Phases Smell

If arrange/act/assert blend together, STOP:

```typescript
// ❌ VIOLATION: Phases mixed together
it('adds items to cart', () => {
  const cart = new Cart();
  cart.add({ id: '1', price: 10 });
  expect(cart.items.length).toBe(1);  // Assert in the middle
  cart.add({ id: '2', price: 20 });   // More acting
  expect(cart.total).toBe(30);        // Another assert
  expect(cart.items.length).toBe(2);  // And another
});
```

Problems:
- What exactly is being tested?
- Which action caused which result?
- Hard to name the test accurately

## The Correct Pattern: Clear Separation

```typescript
// ✅ CORRECT: Clear AAA structure
it('calculates total price of all items in cart', () => {
  // Arrange
  const cart = new Cart();
  cart.add({ id: '1', name: 'Apple', price: 10 });
  cart.add({ id: '2', name: 'Banana', price: 20 });
  
  // Act
  const total = cart.getTotal();
  
  // Assert
  expect(total).toBe(30);
});

it('tracks number of items in cart', () => {
  // Arrange
  const cart = new Cart();
  
  // Act
  cart.add({ id: '1', name: 'Apple', price: 10 });
  cart.add({ id: '2', name: 'Banana', price: 20 });
  
  // Assert
  expect(cart.itemCount).toBe(2);
});
```

## The Three Phases

### Arrange
Set up the test scenario:
- Create objects
- Configure mocks
- Prepare input data
- Set initial state

### Act
Execute the behavior being tested:
- **Single action** (usually)
- Call the method
- Trigger the event
- Make the request

### Assert
Verify the outcome:
- Check return values
- Verify state changes
- Confirm mock interactions
- Validate side effects

## Advanced: Given-When-Then

For BDD-style tests, same concept:

```typescript
describe('Cart', () => {
  describe('when adding items', () => {
    it('should update the total', () => {
      // Given (Arrange)
      const cart = new Cart();
      const item = { id: '1', price: 25 };
      
      // When (Act)
      cart.add(item);
      
      // Then (Assert)
      expect(cart.total).toBe(25);
    });
  });
});
```

## One Assert Per Test?

**Guideline, not rule.** Multiple asserts are fine if they verify ONE behavior:

```typescript
// ✅ OK: Multiple asserts for one logical behavior
it('creates user with correct properties', () => {
  // Arrange
  const input = { email: 'a@b.com', name: 'Alice' };
  
  // Act
  const user = createUser(input);
  
  // Assert - all verify the creation behavior
  expect(user.id).toBeDefined();
  expect(user.email).toBe('a@b.com');
  expect(user.name).toBe('Alice');
  expect(user.createdAt).toBeInstanceOf(Date);
});
```

```typescript
// ❌ BAD: Multiple behaviors in one test
it('user operations', () => {
  const user = createUser({ name: 'Alice' });
  expect(user.name).toBe('Alice');
  
  updateUser(user.id, { name: 'Bob' });
  expect(user.name).toBe('Bob');  // Different behavior!
  
  deleteUser(user.id);
  expect(getUser(user.id)).toBeNull();  // Yet another behavior!
});
```

## Pressure Resistance Protocol

### 1. "It's More Concise"
**Pressure:** "Combining phases makes the test shorter"

**Response:** Short but confusing is worse than longer but clear.

**Action:** Separate the phases. Add comments if needed.

### 2. "It's a Simple Test"
**Pressure:** "For trivial tests, AAA is overkill"

**Response:** Consistency matters. All tests should follow the same pattern.

**Action:** Use AAA even for simple tests. It costs nothing.

### 3. "I Need Multiple Actions"
**Pressure:** "The behavior requires multiple steps"

**Response:** Multiple setup steps go in Arrange. Only the behavior being tested goes in Act.

**Action:** If you need multiple Acts, you probably need multiple tests.

## Red Flags - STOP and Reconsider

- `expect()` calls between actions
- No clear single "act" 
- Assertions scattered throughout
- Hard to describe what test verifies
- Test name doesn't match structure

**All of these mean: Restructure with clear AAA.**

## Quick Reference

| Phase | Contains | Example |
|-------|----------|---------|
| **Arrange** | Setup, mocks, data | `const cart = new Cart()` |
| **Act** | Single behavior | `const total = cart.checkout()` |
| **Assert** | Verifications | `expect(total).toBe(100)` |

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It's more concise" | Clarity beats brevity. |
| "The phases are obvious" | Make them explicit anyway. |
| "Simple test, no need" | Consistency matters. |
| "Multiple actions needed" | Split into multiple tests. |
| "Comments are enough" | Structure is better than comments. |

## The Bottom Line

**Arrange. Act. Assert. In that order. Clearly separated.**

Every test sets up (Arrange), does one thing (Act), and verifies (Assert). When phases are clear, tests are readable, debuggable, and maintainable.
