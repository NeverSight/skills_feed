---
name: code-style
description: Use when writing or modifying any code. Enforces naming conventions, function design, and code clarity principles.
---

# Code Style

## Core Philosophy

Code should be self-explanatory. Comments explain WHY, not WHAT.

## Function Design

### Small and Focused
Each function should do one thing well. Split larger functions into smaller, independent methods.

### Either Call Or Pass
A function should either:
- **Call** other methods (high-level orchestration), OR
- **Pass** data / perform low-level operations

Never mix abstraction levels in one function body. This is the Single Level of Abstraction (SLA) principle.

```typescript
// BAD - mixed abstraction levels
function processOrder(order: Order) {
  validateOrder(order);                    // high-level call
  const tax = order.total * 0.1;           // low-level calculation
  await sendConfirmation(order);           // high-level call
  db.insert('orders', { ...order, tax });  // low-level operation
}

// GOOD - consistent abstraction
function processOrder(order: Order) {
  validateOrder(order);
  const enrichedOrder = calculateTaxes(order);
  await persistOrder(enrichedOrder);
  await sendConfirmation(enrichedOrder);
}
```

### Never Use If With Else
Prefer guard clauses or polymorphism over if-else blocks.

```typescript
// BAD
function getDiscount(user: User) {
  if (user.isPremium) {
    return 0.2;
  } else {
    return 0;
  }
}

// GOOD - guard clause
function getDiscount(user: User) {
  if (!user.isPremium) return 0;
  return 0.2;
}
```

### Avoid Flag Arguments
Flag arguments indicate a function is doing more than one thing.

```typescript
// BAD
function createUser(data: UserData, sendEmail: boolean) { ... }

// GOOD
function createUser(data: UserData) { ... }
function createUserAndNotify(data: UserData) { ... }
```

## Naming

### Expressive Over Comments
```typescript
// BAD
const d = 7; // days in recovery period

// GOOD
const daysInRecoveryPeriod = 7;
```

### No Abbreviations
```typescript
// BAD
getUserCmt(), calcRecReq()

// GOOD
getUserComment(), calculateRecoveryRequirement()
```

### Booleans Read Like Questions
```typescript
// BAD
eligible, recovery

// GOOD
isEligible, isRecovering, hasPassedDeadline
```

### Collections Use Plurals
```typescript
// BAD
const post = getPosts();

// GOOD
const posts = getPosts();
```

### Use Intermediate Variables
```typescript
const hasRequiredPostCount = posts.length >= 2;
const isWithinRecoveryWindow = new Date() <= recoveryDeadline;
const canStartRecovery = hasRequiredPostCount && isWithinRecoveryWindow;
```

## Constants

### No Magic Numbers
```typescript
// BAD
if (streak >= 21) { ... }

// GOOD
const GOLD_BADGE_STREAK_THRESHOLD = 21;
if (streak >= GOLD_BADGE_STREAK_THRESHOLD) { ... }
```

## Comments

### Sparingly and Meaningful
- Code tells HOW, comments tell WHY
- If you need a comment, first try better naming
- Use `TODO:` for known limitations
- Delete obsolete comments
