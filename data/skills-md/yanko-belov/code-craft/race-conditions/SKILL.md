---
name: race-conditions
description: Use when multiple operations access shared state. Use when order of operations matters. Use when "it works most of the time" but occasionally fails mysteriously.
---

# Race Conditions

## Overview

**When outcome depends on timing, you have a race. Races are bugs waiting to happen.**

Race conditions occur when correctness depends on the relative timing of events. They're insidious because they work most of the time, fail randomly, and are nearly impossible to reproduce.

## When to Use

- Multiple async operations access shared state
- Database read-then-write patterns
- Concurrent API requests modify same resource
- "Works in development, fails in production"
- Intermittent bugs that can't be reproduced

## The Iron Rule

```
NEVER read-then-write without atomicity guarantees.
```

**No exceptions:**
- Not for "it's fast, timing won't matter"
- Not for "only one user at a time"
- Not for "we'll fix it if it breaks"
- Not for "it works in testing"

**If timing can affect outcome, you have a race condition.**

## Detection: The TOCTOU Pattern

Time-Of-Check to Time-Of-Use: checking something, then acting on it.

```typescript
// ❌ VIOLATION: Classic race condition
async function withdrawMoney(accountId: string, amount: number): Promise<void> {
  // Time-of-check
  const account = await db.accounts.findById(accountId);
  if (account.balance >= amount) {
    // Time-of-use (gap where another transaction can happen!)
    await db.accounts.update(accountId, {
      balance: account.balance - amount  // Uses stale value!
    });
  }
}

// Two simultaneous $80 withdrawals from $100 account:
// T1: Reads balance = $100 ✓
// T2: Reads balance = $100 ✓  (race!)
// T1: balance >= 80? Yes. Update to $20
// T2: balance >= 80? Yes. Update to $20  (should have been denied!)
// Result: Two $80 withdrawals, final balance $20 (should be overdraft error)
```

## Correct Patterns

### 1. Atomic Operations

```typescript
// ✅ CORRECT: Atomic update with condition
async function withdrawMoney(accountId: string, amount: number): Promise<boolean> {
  const result = await db.accounts.updateOne(
    { 
      _id: accountId,
      balance: { $gte: amount }  // Check AND update atomically
    },
    { 
      $inc: { balance: -amount } 
    }
  );
  
  if (result.modifiedCount === 0) {
    throw new InsufficientFundsError(accountId, amount);
  }
  
  return true;
}
```

### 2. Database Transactions

```typescript
// ✅ CORRECT: Transaction with proper isolation
async function transferMoney(
  fromId: string, 
  toId: string, 
  amount: number
): Promise<void> {
  await db.transaction(async (tx) => {
    // Lock rows with FOR UPDATE
    const from = await tx.accounts
      .findById(fromId)
      .forUpdate();  // Locks row until commit
    
    const to = await tx.accounts
      .findById(toId)
      .forUpdate();
    
    if (from.balance < amount) {
      throw new InsufficientFundsError(fromId, amount);
    }
    
    await tx.accounts.update(fromId, { balance: from.balance - amount });
    await tx.accounts.update(toId, { balance: to.balance + amount });
    
    // Commit releases locks
  });
}
```

### 3. Optimistic Locking

```typescript
// ✅ CORRECT: Optimistic locking with version
async function updateDocument(
  id: string, 
  updates: Partial<Document>
): Promise<Document> {
  const maxRetries = 3;
  
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    const doc = await db.documents.findById(id);
    
    const result = await db.documents.updateOne(
      { 
        _id: id,
        version: doc.version  // Only update if version matches
      },
      { 
        $set: updates,
        $inc: { version: 1 }  // Increment version
      }
    );
    
    if (result.modifiedCount > 0) {
      return { ...doc, ...updates, version: doc.version + 1 };
    }
    
    // Version mismatch - someone else updated, retry
    await sleep(Math.random() * 100);  // Jitter
  }
  
  throw new ConcurrentModificationError(id);
}
```

### 4. Distributed Locks

```typescript
// ✅ CORRECT: Distributed lock for complex operations
async function processOrder(orderId: string): Promise<void> {
  const lockKey = `order:${orderId}:lock`;
  const lockTTL = 30000; // 30 seconds
  
  const lock = await redis.acquireLock(lockKey, lockTTL);
  if (!lock) {
    throw new OrderAlreadyProcessingError(orderId);
  }
  
  try {
    // Safe - only one process can be here for this order
    await doExpensiveOrderProcessing(orderId);
  } finally {
    await redis.releaseLock(lockKey, lock);
  }
}
```

### 5. Idempotency Keys

```typescript
// ✅ CORRECT: Idempotency prevents duplicate processing
async function createPayment(
  idempotencyKey: string,
  data: PaymentData
): Promise<Payment> {
  // Check if already processed
  const existing = await db.payments.findByIdempotencyKey(idempotencyKey);
  if (existing) {
    return existing;  // Return previous result
  }
  
  // Try to claim the idempotency key atomically
  try {
    await db.idempotencyKeys.insert({
      key: idempotencyKey,
      status: 'processing',
      createdAt: new Date(),
    });
  } catch (error) {
    if (isDuplicateKeyError(error)) {
      // Another request claimed it - fetch and return
      const existing = await db.payments.findByIdempotencyKey(idempotencyKey);
      if (existing) return existing;
      throw new PaymentProcessingError('Payment in progress');
    }
    throw error;
  }
  
  // Safe to process - we own the idempotency key
  const payment = await processPayment(data);
  
  await db.idempotencyKeys.update(idempotencyKey, {
    status: 'completed',
    result: payment.id,
  });
  
  return payment;
}
```

## Common Race Condition Patterns

| Pattern | Problem | Solution |
|---------|---------|----------|
| Check-then-act | State changes between check and act | Atomic check-and-act |
| Read-modify-write | Value changes after read | Atomic update or lock |
| Lazy initialization | Multiple threads initialize | Double-checked locking or atomic init |
| Counter increment | Lost updates | Atomic increment |
| First-one-wins | Multiple claim "first" | Atomic claim with unique constraint |

## Language-Specific Patterns

### JavaScript/Node.js

```typescript
// ❌ VIOLATION: Shared state in closure
let requestCount = 0;
async function handleRequest() {
  requestCount++;  // Race! Read-modify-write is NOT atomic
  // ...
}

// ✅ CORRECT: Atomic counter
import { createClient } from 'redis';
const redis = createClient();

async function handleRequest() {
  const count = await redis.incr('request_count');  // Atomic
  // ...
}
```

### Python

```python
# ❌ VIOLATION: Check-then-act
def get_or_create(key: str, factory: Callable) -> Any:
    if key not in cache:  # Check
        cache[key] = factory()  # Act - race!
    return cache[key]

# ✅ CORRECT: Atomic with lock
from threading import Lock
lock = Lock()

def get_or_create(key: str, factory: Callable) -> Any:
    with lock:
        if key not in cache:
            cache[key] = factory()
        return cache[key]
```

## Pressure Resistance Protocol

### 1. "It's Fast, Timing Won't Matter"
**Pressure:** "The operation takes microseconds"

**Response:** Production load creates overlap. Under load, "fast" operations overlap frequently. Race conditions scale with traffic.

**Action:** Use atomic operations. Speed doesn't prevent races.

### 2. "Only One User at a Time"
**Pressure:** "Low traffic, won't have concurrent requests"

**Response:** Users double-click. Tabs refresh. Bots hammer. Mobile retries on timeout. "Low traffic" has bursts.

**Action:** Design for concurrency even if you don't expect it.

### 3. "We'll Fix It If It Breaks"
**Pressure:** "Ship now, fix later"

**Response:** Race conditions are nearly impossible to reproduce. You'll spend weeks debugging "random" failures.

**Action:** Build it correctly now. Cheaper than debugging later.

### 4. "It Works in Testing"
**Pressure:** "All tests pass"

**Response:** Tests run sequentially. Production runs concurrently. Race conditions hide in serial execution.

**Action:** Write concurrent tests. Load test. Assume races exist.

## Red Flags - STOP and Reconsider

If you notice ANY of these patterns, you likely have a race:

- `if (condition) { update based on condition }`
- `read(); compute(); write(computed);`
- `check availability; book;`
- `get count; increment; save count;`
- Global or shared mutable state
- "Works most of the time"
- "Can't reproduce in development"
- Timeouts that "fix" intermittent bugs

**All of these mean: Add atomicity guarantees.**

## Testing for Race Conditions

```typescript
// Concurrent test to expose races
describe('withdraw', () => {
  it('handles concurrent withdrawals correctly', async () => {
    await db.accounts.create({ id: 'test', balance: 100 });
    
    // Simulate 10 concurrent $20 withdrawals
    const withdrawals = Array(10).fill(null).map(() => 
      withdrawMoney('test', 20).catch(() => 'failed')
    );
    
    const results = await Promise.all(withdrawals);
    const successful = results.filter(r => r !== 'failed').length;
    
    // Only 5 should succeed (5 × $20 = $100)
    expect(successful).toBe(5);
    
    const account = await db.accounts.findById('test');
    expect(account.balance).toBe(0);
  });
});
```

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It's fast enough" | Fast operations still overlap under load. |
| "Low traffic" | Retries, double-clicks, bots create concurrency. |
| "Works in dev" | Dev is serial. Prod is parallel. |
| "Fix when it breaks" | Race bugs are unfindable. Fix now. |
| "Just add a sleep" | Sleeps don't fix races, just hide them. |
| "Users won't do that" | Users do everything you don't expect. |

## Quick Reference

| Scenario | Solution |
|----------|----------|
| Balance check before update | Atomic conditional update |
| Increment counter | Atomic increment (Redis INCR, SQL += 1) |
| Complex multi-step operation | Database transaction with locks |
| Cross-service operation | Distributed lock |
| Duplicate request prevention | Idempotency key |
| Version conflicts | Optimistic locking |

## The Bottom Line

**If correctness depends on timing, you have a bug.**

Read-then-write is a race. Check-then-act is a race. Any gap between observing state and acting on it is a race. Use atomic operations, transactions, locks, or idempotency keys. Never assume "it's fast enough" or "traffic is low."
