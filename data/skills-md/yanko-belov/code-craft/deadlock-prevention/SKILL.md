---
name: deadlock-prevention
description: Use when acquiring multiple locks. Use when operations wait for each other. Use when system hangs without crashing.
---

# Deadlock Prevention

## Overview

**When two processes wait for each other forever, you have a deadlock.**

Deadlocks are permanent freezes—no crash, no error, just silence. They occur when processes hold resources while waiting for resources held by others, creating circular wait.

## When to Use

- Acquiring multiple locks or resources
- Nested transactions across tables/services
- Distributed systems with cross-service calls
- "System freezes under load"
- No errors but operations never complete

## The Iron Rule

```
NEVER acquire locks in inconsistent order across the codebase.
```

**No exceptions:**
- Not for "this path is rare"
- Not for "we'll add timeout"
- Not for "different services, won't conflict"
- Not for "only happens under heavy load"

**Inconsistent lock ordering guarantees eventual deadlock.**

## The Four Deadlock Conditions

Deadlock requires ALL four. Break ANY one to prevent:

```
┌────────────────────────────────────────────────────────────┐
│ 1. MUTUAL EXCLUSION    │ Resource can only be held by one │
│ 2. HOLD AND WAIT       │ Hold one, wait for another       │
│ 3. NO PREEMPTION       │ Can't force release of resource  │
│ 4. CIRCULAR WAIT       │ A waits for B, B waits for A     │
└────────────────────────────────────────────────────────────┘
```

**Most practical: Break Circular Wait with consistent ordering.**

## Detection: The Circular Wait Pattern

```typescript
// ❌ VIOLATION: Inconsistent lock order = guaranteed deadlock

// Service A: Transfer from X to Y
async function transferAtoB(fromId: string, toId: string, amount: number) {
  await lockAccount(fromId);  // Lock A first
  await lockAccount(toId);    // Then lock B
  // transfer...
  await unlockAccount(toId);
  await unlockAccount(fromId);
}

// Service B: Transfer from Y to X  
async function transferBtoA(fromId: string, toId: string, amount: number) {
  await lockAccount(fromId);  // Lock B first (OPPOSITE ORDER!)
  await lockAccount(toId);    // Then lock A
  // transfer...
}

// Deadlock scenario:
// T1: Locks account A, waits for B
// T2: Locks account B, waits for A
// Result: Both wait forever
```

## Prevention Strategies

### 1. Consistent Lock Ordering (Primary Strategy)

```typescript
// ✅ CORRECT: Always acquire locks in the same order
async function transfer(
  accountId1: string, 
  accountId2: string, 
  amount: number
): Promise<void> {
  // ALWAYS lock lower ID first - creates total ordering
  const [first, second] = accountId1 < accountId2 
    ? [accountId1, accountId2] 
    : [accountId2, accountId1];
  
  const lock1 = await acquireLock(`account:${first}`);
  const lock2 = await acquireLock(`account:${second}`);
  
  try {
    await doTransfer(accountId1, accountId2, amount);
  } finally {
    await releaseLock(lock2);
    await releaseLock(lock1);  // Release in reverse order
  }
}
```

### 2. Lock Timeout (Break No Preemption)

```typescript
// ✅ CORRECT: Timeout prevents permanent deadlock
async function acquireWithTimeout(
  resource: string, 
  timeoutMs: number
): Promise<Lock | null> {
  const deadline = Date.now() + timeoutMs;
  
  while (Date.now() < deadline) {
    const lock = await tryAcquireLock(resource);
    if (lock) return lock;
    
    // Backoff with jitter
    await sleep(50 + Math.random() * 50);
  }
  
  return null;  // Timeout - caller must handle
}

async function transfer(from: string, to: string, amount: number) {
  const lock1 = await acquireWithTimeout(`account:${from}`, 5000);
  if (!lock1) throw new LockTimeoutError(from);
  
  try {
    const lock2 = await acquireWithTimeout(`account:${to}`, 5000);
    if (!lock2) {
      throw new LockTimeoutError(to);  // Release lock1 in finally
    }
    
    try {
      await doTransfer(from, to, amount);
    } finally {
      await releaseLock(lock2);
    }
  } finally {
    await releaseLock(lock1);
  }
}
```

### 3. Try-Lock with Backoff (Break Hold and Wait)

```typescript
// ✅ CORRECT: Don't hold while waiting - release and retry
async function acquireMultipleLocks(
  resources: string[], 
  maxRetries = 10
): Promise<Lock[]> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    const locks: Lock[] = [];
    let success = true;
    
    // Sort for consistent ordering
    const sorted = [...resources].sort();
    
    for (const resource of sorted) {
      const lock = await tryAcquireLock(resource);
      if (lock) {
        locks.push(lock);
      } else {
        // Can't get this lock - release all and retry
        success = false;
        break;
      }
    }
    
    if (success) {
      return locks;
    }
    
    // Release all acquired locks
    await Promise.all(locks.map(releaseLock));
    
    // Exponential backoff with jitter
    await sleep(Math.pow(2, attempt) * 10 + Math.random() * 50);
  }
  
  throw new DeadlockPreventionError('Could not acquire all locks');
}
```

### 4. Single Lock for Related Resources

```typescript
// ✅ CORRECT: One lock covers all related resources
async function transfer(from: string, to: string, amount: number) {
  // Use a higher-level lock instead of per-account locks
  const transferLock = await acquireLock('transfer-system');
  
  try {
    // No deadlock possible - only one lock
    await doTransfer(from, to, amount);
  } finally {
    await releaseLock(transferLock);
  }
}

// Trade-off: Less parallelism, but no deadlock risk
// Use when: Operations are fast, correctness > throughput
```

### 5. Lock Hierarchy

```typescript
// ✅ CORRECT: Hierarchical locking - always acquire parent before child
enum LockLevel {
  SYSTEM = 0,
  REGION = 1,
  ACCOUNT = 2,
  TRANSACTION = 3,
}

class HierarchicalLock {
  private heldLocks: Map<LockLevel, Set<string>> = new Map();
  
  async acquire(level: LockLevel, resource: string): Promise<void> {
    // Validate hierarchy - can only acquire lower levels
    for (const [heldLevel] of this.heldLocks) {
      if (level <= heldLevel) {
        throw new LockHierarchyViolation(
          `Cannot acquire ${level} while holding ${heldLevel}`
        );
      }
    }
    
    await this.doAcquire(level, resource);
    
    if (!this.heldLocks.has(level)) {
      this.heldLocks.set(level, new Set());
    }
    this.heldLocks.get(level)!.add(resource);
  }
}
```

## Database-Specific Patterns

### SQL: Lock Ordering

```sql
-- ❌ VIOLATION: No consistent order
-- Transaction 1
SELECT * FROM accounts WHERE id = 'A' FOR UPDATE;
SELECT * FROM accounts WHERE id = 'B' FOR UPDATE;

-- Transaction 2 (opposite order)
SELECT * FROM accounts WHERE id = 'B' FOR UPDATE;
SELECT * FROM accounts WHERE id = 'A' FOR UPDATE;

-- ✅ CORRECT: Always order by ID
SELECT * FROM accounts 
WHERE id IN ('A', 'B') 
ORDER BY id 
FOR UPDATE;
```

### PostgreSQL: Lock Timeout

```sql
-- Set lock timeout to prevent permanent deadlock
SET lock_timeout = '5s';

BEGIN;
SELECT * FROM accounts WHERE id = 'A' FOR UPDATE;
-- If can't acquire within 5s, transaction fails with error
-- Better than hanging forever
COMMIT;
```

## Distributed System Patterns

```typescript
// ✅ CORRECT: Distributed lock with lease
class DistributedLock {
  async acquire(resource: string, leaseDuration: number): Promise<Lease> {
    const lease: Lease = {
      id: uuid(),
      resource,
      expiresAt: Date.now() + leaseDuration,
    };
    
    // Atomic set-if-not-exists with TTL
    const acquired = await redis.set(
      `lock:${resource}`,
      JSON.stringify(lease),
      'NX',  // Only if not exists
      'PX', leaseDuration  // Expire after duration
    );
    
    if (!acquired) {
      throw new LockNotAvailableError(resource);
    }
    
    return lease;
  }
  
  async release(lease: Lease): Promise<void> {
    // Only release if we still own it (compare lease ID)
    const script = `
      if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("del", KEYS[1])
      else
        return 0
      end
    `;
    await redis.eval(script, 1, `lock:${lease.resource}`, JSON.stringify(lease));
  }
}
```

## Pressure Resistance Protocol

### 1. "Just Add a Longer Timeout"
**Pressure:** "Increase timeout to avoid failures"

**Response:** Longer timeout = longer deadlock before failure. The deadlock still exists.

**Action:** Fix the ordering. Timeout is safety net, not solution.

### 2. "It Only Happens Under Heavy Load"
**Pressure:** "Rare edge case, not worth fixing"

**Response:** Production IS heavy load. "Rare" becomes "constant" at scale. Deadlocks are permanent failures.

**Action:** Fix now. Deadlocks scale with traffic.

### 3. "Different Services Won't Conflict"
**Pressure:** "Services are independent"

**Response:** If they share resources (DB rows, Redis keys, files), they conflict.

**Action:** Coordinate lock ordering across services.

### 4. "We Can Just Restart"
**Pressure:** "Restart clears deadlocks"

**Response:** Restart kills in-flight transactions. Data corruption risk. User impact. Root cause remains.

**Action:** Prevent deadlocks. Don't treat symptoms.

## Red Flags - STOP and Reconsider

If you notice ANY of these, deadlock risk is high:

- Acquiring locks in different orders across code paths
- Nested lock acquisition without clear hierarchy
- "This endpoint hangs sometimes"
- No lock timeouts
- Locks held across async operations
- Cross-service locking without coordination
- Locks acquired in loops

**All of these mean: Redesign lock strategy.**

## Deadlock Detection

```typescript
// Runtime deadlock detection
class DeadlockDetector {
  private waitGraph: Map<string, Set<string>> = new Map();  // who waits for whom
  
  recordWaiting(waiter: string, holder: string): void {
    if (!this.waitGraph.has(waiter)) {
      this.waitGraph.set(waiter, new Set());
    }
    this.waitGraph.get(waiter)!.add(holder);
    
    // Check for cycle
    if (this.hasCycle(waiter)) {
      throw new DeadlockDetectedError(
        `Deadlock: ${this.describeCycle(waiter)}`
      );
    }
  }
  
  private hasCycle(start: string, visited = new Set<string>()): boolean {
    if (visited.has(start)) return true;
    visited.add(start);
    
    for (const next of this.waitGraph.get(start) || []) {
      if (this.hasCycle(next, visited)) return true;
    }
    
    visited.delete(start);
    return false;
  }
}
```

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "Timeout handles it" | Timeout is symptom relief. Deadlock still happens. |
| "Rare under normal load" | Production load IS when it matters. |
| "Services are isolated" | Shared DB = shared resource = deadlock possible. |
| "Just restart when stuck" | Kills transactions, corrupts state. |
| "Lock ordering is too restrictive" | Ordered locks enable parallelism. Deadlocks kill it. |
| "It worked in testing" | Tests don't have production concurrency. |

## Quick Reference

| Strategy | When to Use |
|----------|-------------|
| Consistent ordering | Default choice - always order locks |
| Lock timeout | Safety net for all locking |
| Try-lock with backoff | High contention, can retry |
| Single coarse lock | Low throughput OK, simplicity needed |
| Lock hierarchy | Complex systems with nested resources |
| Distributed locks with lease | Cross-service coordination |

## Deadlock Prevention Checklist

| Requirement | Check |
|-------------|-------|
| All lock acquisitions follow consistent order | ☐ |
| Lock timeouts configured | ☐ |
| Locks released in finally blocks | ☐ |
| No locks held across await boundaries (if avoidable) | ☐ |
| Deadlock detection/monitoring in place | ☐ |
| Lock ordering documented for cross-team code | ☐ |

## The Bottom Line

**Order your locks. Always. Every path. Every service.**

Deadlocks come from inconsistent lock ordering. Pick an order (alphabetical, ID-based, hierarchical) and enforce it everywhere. Add timeouts as safety nets. Monitor for lock contention. When pressured to "just add timeout," fix the ordering instead.
