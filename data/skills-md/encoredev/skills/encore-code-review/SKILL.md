---
name: encore-code-review
description: Review Encore.ts code for best practices and anti-patterns.
---

# Encore Code Review

## Instructions

When reviewing Encore.ts code, check for these common issues:

## Critical Issues

### 1. Infrastructure Inside Functions

```typescript
// WRONG: Infrastructure declared inside function
async function setup() {
  const db = new SQLDatabase("mydb", { migrations: "./migrations" });
  const topic = new Topic<Event>("events", { deliveryGuarantee: "at-least-once" });
}

// CORRECT: Package level declaration
const db = new SQLDatabase("mydb", { migrations: "./migrations" });
const topic = new Topic<Event>("events", { deliveryGuarantee: "at-least-once" });
```

### 2. Using require() Instead of import

```typescript
// WRONG
const { api } = require("encore.dev/api");

// CORRECT
import { api } from "encore.dev/api";
```

### 3. Wrong Service Import Pattern

```typescript
// WRONG: Direct import from another service
import { getUser } from "../user/api";

// CORRECT: Use ~encore/clients
import { user } from "~encore/clients";
const result = await user.getUser({ id });
```

### 4. Missing Error Handling

```typescript
// WRONG: Returning null for not found
const user = await db.queryRow`SELECT * FROM users WHERE id = ${id}`;
if (!user) return null;

// CORRECT: Throw APIError
import { APIError } from "encore.dev/api";

const user = await db.queryRow`SELECT * FROM users WHERE id = ${id}`;
if (!user) {
  throw APIError.notFound("user not found");
}
```

### 5. SQL Injection Risk

```typescript
// WRONG: String concatenation
await db.query(`SELECT * FROM users WHERE email = '${email}'`);

// CORRECT: Template literal with automatic escaping
await db.queryRow`SELECT * FROM users WHERE email = ${email}`;
```

## Warning Issues

### 6. Missing Type Annotations

```typescript
// WEAK: No explicit types
export const getUser = api(
  { method: "GET", path: "/users/:id", expose: true },
  async ({ id }) => {
    return await findUser(id);
  }
);

// BETTER: Explicit request/response types
interface GetUserRequest { id: string; }
interface User { id: string; email: string; name: string; }

export const getUser = api(
  { method: "GET", path: "/users/:id", expose: true },
  async ({ id }: GetUserRequest): Promise<User> => {
    return await findUser(id);
  }
);
```

### 7. Exposed Internal Endpoints

```typescript
// CHECK: Should this cron endpoint be exposed?
export const cleanupJob = api(
  { expose: true },  // Probably should be false
  async () => { /* ... */ }
);
```

### 8. Non-Idempotent Subscription Handlers

```typescript
// RISKY: Not idempotent (pubsub has at-least-once delivery)
const _ = new Subscription(orderCreated, "process-order", {
  handler: async (event) => {
    await chargeCustomer(event.orderId);  // Could charge twice!
  },
});

// SAFER: Check before processing
const _ = new Subscription(orderCreated, "process-order", {
  handler: async (event) => {
    const order = await getOrder(event.orderId);
    if (order.status !== "pending") return;  // Already processed
    await chargeCustomer(event.orderId);
  },
});
```

### 9. Secrets Called at Module Level

```typescript
// WRONG: Secret accessed at startup
const stripeKey = secret("StripeKey");
const client = new Stripe(stripeKey());  // Called during import

// CORRECT: Access inside functions
const stripeKey = secret("StripeKey");

async function charge() {
  const client = new Stripe(stripeKey());  // Called at runtime
}
```

## Review Checklist

- [ ] All infrastructure at package level
- [ ] Using ES6 imports, not require()
- [ ] Cross-service calls use `~encore/clients`
- [ ] Proper error handling with APIError
- [ ] SQL uses template literals
- [ ] Request/response types defined
- [ ] Internal endpoints have `expose: false`
- [ ] Subscription handlers are idempotent
- [ ] Secrets accessed inside functions, not at import time
- [ ] Migrations follow naming convention (001_name.up.sql)

## Output Format

When reviewing, report issues as:

```
[CRITICAL] [file:line] Description of issue
[WARNING] [file:line] Description of concern  
[GOOD] Notable good practice observed
```
