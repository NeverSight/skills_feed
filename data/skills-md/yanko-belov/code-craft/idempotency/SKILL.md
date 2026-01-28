---
name: idempotency
description: Use when creating mutation endpoints. Use when trusting frontend to prevent duplicates. Use when payments or critical operations can be repeated.
---

# Idempotency

## Overview

**Critical operations must be safe to retry. Use idempotency keys.**

Networks fail. Clients retry. Users double-click. Without idempotency, retries cause duplicate charges, orders, or data corruption.

## When to Use

- Payment processing endpoints
- Order creation
- Any operation that shouldn't happen twice
- Asked to "trust the frontend" to prevent duplicates

## The Iron Rule

```
NEVER rely on frontend to prevent duplicate requests.
```

**No exceptions:**
- Not for "frontend disables the button"
- Not for "we show a loading state"
- Not for "it rarely happens"
- Not for "users won't double-click"

## Detection: Duplicate Risk Smell

If mutations have no duplicate protection, STOP:

```typescript
// ❌ VIOLATION: No idempotency protection
app.post('/payments', async (req, res) => {
  const { userId, amount, cardToken } = req.body;
  
  // If this request retries, user gets charged twice!
  const payment = await stripeCharge(amount, cardToken);
  await db.payments.create({ userId, amount, stripeId: payment.id });
  
  res.json({ success: true });
});
```

What can go wrong:
- Network timeout → client retries → double charge
- User double-clicks → two requests → double charge
- Mobile app retry logic → multiple requests

## The Correct Pattern: Idempotency Keys

```typescript
// ✅ CORRECT: Idempotency key protection

app.post('/payments', async (req, res) => {
  // Require idempotency key
  const idempotencyKey = req.headers['idempotency-key'];
  if (!idempotencyKey) {
    return res.status(400).json({ 
      error: 'Idempotency-Key header is required' 
    });
  }
  
  const { userId, amount, cardToken } = validated(req.body);
  
  // Check for existing request with this key
  const existing = await db.idempotencyKeys.findOne({
    where: { key: idempotencyKey, userId }
  });
  
  if (existing) {
    // Return cached response
    return res.status(existing.statusCode).json(existing.response);
  }
  
  try {
    // Process the payment
    const payment = await stripeCharge(amount, cardToken);
    await db.payments.create({ userId, amount, stripeId: payment.id });
    
    const response = { success: true, paymentId: payment.id };
    
    // Cache the response
    await db.idempotencyKeys.create({
      key: idempotencyKey,
      userId,
      statusCode: 200,
      response,
      expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000) // 24 hours
    });
    
    res.json(response);
  } catch (error) {
    // Cache error responses too (optional, depends on error type)
    throw error;
  }
});

// Client usage:
// POST /payments
// Headers: { "Idempotency-Key": "user-123-order-456-attempt-1" }
```

## Idempotency Key Design

### Key Generation (Client Side)
```typescript
// Option 1: UUID per request
const key = crypto.randomUUID();

// Option 2: Deterministic (better for retries)
const key = `${userId}-${orderId}-${timestamp}`;

// Option 3: Hash of request content
const key = hash(JSON.stringify({ userId, items, amount }));
```

### Key Storage (Server Side)
```typescript
interface IdempotencyRecord {
  key: string;
  userId: string;
  statusCode: number;
  response: any;
  createdAt: Date;
  expiresAt: Date;  // Clean up old keys
}
```

## What Needs Idempotency

| Operation | Risk | Solution |
|-----------|------|----------|
| Payments | Double charge | Idempotency key |
| Order creation | Duplicate orders | Idempotency key |
| Inventory decrement | Over-decrement | Idempotency key |
| Email sending | Duplicate emails | Idempotency key |
| Account creation | Duplicate accounts | Unique constraint + idempotency |

## Pressure Resistance Protocol

### 1. "Frontend Prevents Duplicates"
**Pressure:** "We disable the button, show loading state"

**Response:** Networks retry automatically. JavaScript crashes. Users have fast fingers.

**Action:** Backend idempotency. Frontend UX is not protection.

### 2. "It Rarely Happens"
**Pressure:** "Duplicates are rare edge cases"

**Response:** Rare × many users = many angry users. One duplicate charge = support nightmare.

**Action:** Protect all critical mutations.

### 3. "Users Won't Double-Click"
**Pressure:** "Our users are careful"

**Response:** Users have slow connections. Buttons are small. Frustration leads to clicking.

**Action:** Never rely on user behavior.

### 4. "Database Has Unique Constraint"
**Pressure:** "Duplicate insert will fail"

**Response:** Unique constraint throws error. User sees error. UX is terrible.

**Action:** Idempotency returns same success response.

## Red Flags - STOP and Reconsider

- Payment endpoints without idempotency
- "Frontend handles duplicate prevention"
- Network retries causing side effects
- Users reporting double charges
- No Idempotency-Key header support

**All of these mean: Add idempotency protection.**

## Quick Reference

| Unsafe | Safe |
|--------|------|
| Trust frontend | Require idempotency key |
| Error on duplicate | Return cached response |
| Assume single request | Design for retries |
| POST = new resource always | POST + key = at-most-once |

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "Frontend prevents it" | Networks retry. Users double-click. |
| "Rarely happens" | Rare × scale = many incidents. |
| "Users are careful" | Users are human. |
| "Unique constraint" | Constraints throw errors, not success. |
| "Too complex" | Simpler than handling support tickets. |

## The Bottom Line

**Require idempotency keys for all critical mutations.**

Never trust frontend protection. Cache responses by idempotency key. Return the same response for duplicate requests. Clean up old keys periodically.
