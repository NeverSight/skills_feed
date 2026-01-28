---
name: fail-fast
description: Use when handling errors. Use when tempted to catch and swallow exceptions. Use when returning default values to hide failures.
---

# Fail Fast

## Overview

**When something goes wrong, fail immediately and visibly.**

Don't hide errors with try/catch that returns defaults. Don't let invalid state propagate. Fail at the point of failure, not three layers later with corrupted data.

## When to Use

- Writing error handling code
- Tempted to catch and return default
- Adding "defensive" null checks everywhere
- Wrapping everything in try/catch
- Returning error objects instead of throwing

## The Iron Rule

```
NEVER hide failures. Fail loud, fail early.
```

**No exceptions:**
- Not for "the app shouldn't crash"
- Not for "return something rather than throw"
- Not for "handle errors gracefully"
- Not for "defensive programming"

## Detection: The "Swallow" Smell

If errors disappear silently, you're failing slow:

```typescript
// ❌ VIOLATION: Hiding failures
async function processPayment(userId: string, amount: number): Promise<PaymentResult> {
  try {
    const user = await getUser(userId);
    if (!user) return { success: false, error: 'User not found' };
    
    const card = await validateCard(user.cardToken);
    if (!card.valid) return { success: false, error: 'Invalid card' };
    
    const result = await chargeCard(card, amount);
    if (!result.success) return { success: false, error: 'Payment failed' };
    
    return { success: true, transactionId: result.id };
  } catch (error) {
    return { success: false, error: 'Internal error' };  // ← SWALLOWED!
  }
}
```

Problems:
- Caller doesn't know WHAT failed
- Stack trace is lost
- Bugs hide as "internal error"
- No visibility into actual failures

## The Correct Pattern: Fail Fast

Throw at the point of failure. Let errors propagate:

```typescript
// ✅ CORRECT: Fail fast
async function processPayment(userId: string, amount: number): Promise<Transaction> {
  // Validate early - fail fast on bad input
  if (!userId) throw new ValidationError('userId is required');
  if (amount <= 0) throw new ValidationError('amount must be positive');
  
  // Let failures propagate - don't swallow
  const user = await getUser(userId);
  if (!user) throw new NotFoundError(`User ${userId} not found`);
  
  const card = await validateCard(user.cardToken);
  if (!card.valid) throw new PaymentError('Card validation failed', card.errors);
  
  // This might throw - that's okay! Let it.
  const transaction = await chargeCard(card, amount);
  
  return transaction;
}

// Caller handles errors appropriately
try {
  const tx = await processPayment(userId, amount);
  res.json({ success: true, transactionId: tx.id });
} catch (error) {
  if (error instanceof ValidationError) {
    res.status(400).json({ error: error.message });
  } else if (error instanceof NotFoundError) {
    res.status(404).json({ error: error.message });
  } else if (error instanceof PaymentError) {
    res.status(402).json({ error: error.message });
  } else {
    // Unknown error - log it, return 500
    logger.error('Payment failed', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}
```

## Why Fail-Slow Is Dangerous

| Problem | Impact |
|---------|--------|
| **Hidden bugs** | Errors become "it didn't work" |
| **Lost context** | Stack trace shows catch, not cause |
| **Corrupted state** | Invalid data propagates |
| **Debugging nightmare** | Where did it actually fail? |
| **Silent data loss** | Operations fail but app continues |

## Fail Fast Techniques

### 1. Validate Early

```typescript
function createUser(data: unknown): User {
  // Fail IMMEDIATELY on bad input
  if (!data || typeof data !== 'object') {
    throw new ValidationError('Invalid user data');
  }
  
  const { email, name } = data as Record<string, unknown>;
  
  if (!email || typeof email !== 'string') {
    throw new ValidationError('Email is required');
  }
  
  if (!name || typeof name !== 'string') {
    throw new ValidationError('Name is required');
  }
  
  // Only proceed with valid data
  return new User(email, name);
}
```

### 2. Assert Invariants

```typescript
function withdraw(account: Account, amount: number): void {
  // Assert what must be true
  assert(amount > 0, 'Withdrawal amount must be positive');
  assert(account.balance >= amount, 'Insufficient funds');
  
  account.balance -= amount;
  
  // Post-condition check
  assert(account.balance >= 0, 'Balance went negative - invariant violated');
}
```

### 3. Use Type System

```typescript
// ❌ Fail slow: null checks everywhere
function processOrder(order: Order | null): void {
  if (!order) return;  // Silent failure
  // ...
}

// ✅ Fail fast: require valid input
function processOrder(order: Order): void {
  // If order is null, TypeScript catches it
  // If it gets here with null, it will throw - good!
}
```

## Pressure Resistance Protocol

### 1. "The App Shouldn't Crash"
**Pressure:** "Users will see errors if we throw"

**Response:** Users seeing a clear error is better than corrupted data or silent failure.

**Action:** Throw errors, catch at boundaries (API layer), return appropriate HTTP codes.

### 2. "Return Something Rather Than Throw"
**Pressure:** "Returning error objects is more functional"

**Response:** Error objects are fine IF callers check them. They usually don't.

**Action:** Throw for unexpected failures. Use Result types only if callers actually handle both cases.

### 3. "Handle Errors Gracefully"
**Pressure:** "Graceful = don't throw"

**Response:** Graceful = appropriate response. Swallowing is not graceful.

**Action:** Throw, catch at boundary, return meaningful error response.

### 4. "Defensive Programming"
**Pressure:** "Defensive code handles all cases"

**Response:** Defensive = validate early and fail. Not = hide failures.

**Action:** Validate inputs, assert invariants, throw on violations.

## Red Flags - STOP and Reconsider

If you notice ANY of these, refactor:

- `catch (e) { return null; }`
- `catch (e) { return { success: false }; }`
- `if (!x) return;` (silent early return)
- `try { } catch { }` (empty catch)
- Returning default values on error
- "Error: Internal error" (generic catch-all)
- Logs error but continues execution

**All of these mean: Let the error propagate or throw explicitly.**

## Quick Reference

| Fail Slow (Bad) | Fail Fast (Good) |
|-----------------|------------------|
| `catch (e) { return null }` | `catch (e) { throw e }` |
| `if (!user) return` | `if (!user) throw new NotFoundError()` |
| `return { success: false }` | `throw new OperationError()` |
| Generic "internal error" | Specific error types |
| Swallow and continue | Propagate and handle at boundary |

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "App shouldn't crash" | Clear errors are better than hidden bugs. |
| "Return instead of throw" | Callers ignore return values. Throws can't be ignored. |
| "Graceful error handling" | Swallowing isn't graceful. |
| "Defensive programming" | Defensive = validate and fail, not hide. |
| "Never let functions crash" | Crashing on errors finds bugs. |
| "User experience" | Users prefer "payment failed" over silent failures. |

## The Bottom Line

**Fail fast. Fail loud. Fail at the source.**

When errors occur: throw immediately with context. Let errors propagate to boundaries where they can be logged and translated to user-appropriate responses. Never swallow. Never return defaults to hide failure.
