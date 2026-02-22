---
name: convex-actions
description: Best practices for Convex actions, transactions, and scheduling. Use when writing actions that call external APIs, using ctx.runQuery/ctx.runMutation, scheduling functions with ctx.scheduler, or working with the Convex runtime vs Node.js runtime ("use node").
---

# Convex Actions

## Function Types Overview

| Type | Database Access | External APIs | Caching | Use Case |
|------|----------------|---------------|---------|----------|
| Query | Read-only | No | Yes, reactive | Fetching data |
| Mutation | Read/Write | No | No | Modifying data |
| Action | Via runQuery/runMutation | Yes | No | External integrations |

## Actions with Node.js Runtime

Add `"use node";` at the top of files using Node.js APIs:

```typescript
// convex/email.ts
"use node";

import { action, internalAction } from "./_generated/server";
import { v } from "convex/values";
import { internal } from "./_generated/api";

export const sendEmail = action({
  args: { to: v.string(), subject: v.string(), body: v.string() },
  returns: v.object({ success: v.boolean() }),
  handler: async (ctx, args) => {
    const apiKey = process.env.RESEND_API_KEY;
    if (!apiKey) throw new Error("RESEND_API_KEY not configured");

    const response = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ from: "noreply@example.com", ...args }),
    });

    return { success: response.ok };
  },
});
```

## Scheduling Functions

Use `ctx.scheduler.runAfter` to schedule functions:

```typescript
export const createTask = mutation({
  args: { title: v.string(), userId: v.id("users") },
  returns: v.id("tasks"),
  handler: async (ctx, args) => {
    const taskId = await ctx.db.insert("tasks", {
      title: args.title,
      userId: args.userId,
      status: "pending",
    });

    // Schedule processing (always use internal functions!)
    await ctx.scheduler.runAfter(0, internal.tasks.processTask, { taskId });

    return taskId;
  },
});

// Internal function for scheduled work
export const processTask = internalMutation({
  args: { taskId: v.id("tasks") },
  returns: v.null(),
  handler: async (ctx, args) => {
    await ctx.db.patch("tasks", args.taskId, { status: "processing" });
    // ... processing logic
    return null;
  },
});
```

## Use `runAction` Only When Changing Runtime

Replace `runAction` with plain TypeScript functions unless switching runtimes:

```typescript
// Bad - unnecessary runAction overhead
await ctx.runAction(internal.scrape.scrapePage, { url });

// Good - plain TypeScript function
import * as Scrape from './model/scrape';
await Scrape.scrapePage(ctx, { url });
```

## Avoid Sequential `ctx.runMutation` / `ctx.runQuery`

Each call runs in its own transaction. Combine for consistency:

```typescript
// Bad - inconsistent reads
const team = await ctx.runQuery(internal.teams.getTeam, { teamId });
const owner = await ctx.runQuery(internal.teams.getOwner, { teamId });

// Good - single consistent query
const { team, owner } = await ctx.runQuery(internal.teams.getTeamAndOwner, { teamId });

// Bad - non-atomic loop
for (const user of users) {
  await ctx.runMutation(internal.users.insert, user);
}

// Good - atomic batch
await ctx.runMutation(internal.users.insertMany, { users });
```

**Exceptions:** Migrations, aggregations, or when side effects occur between calls.

## Prefer Helper Functions in Queries/Mutations

Use plain TypeScript instead of `ctx.runQuery`/`ctx.runMutation`:

```typescript
// Good - plain helper
import * as Users from './model/users';
const user = await Users.getCurrentUser(ctx);

// Bad - unnecessary overhead
const user = await ctx.runQuery(api.users.getCurrentUser);
```

**Exception:** Partial rollback needs `ctx.runMutation`:
```typescript
try {
  await ctx.runMutation(internal.orders.process, { orderId });
} catch (e) {
  // Rollback process, record failure
  await ctx.db.insert("failures", { orderId, error: `${e}` });
}
```

## Await All Promises

Always await async operations:

```typescript
// Bad - missing await
ctx.scheduler.runAfter(0, internal.tasks.process, { id });
ctx.db.patch("tasks", docId, { status: "done" });

// Good - awaited
await ctx.scheduler.runAfter(0, internal.tasks.process, { id });
await ctx.db.patch("tasks", docId, { status: "done" });
```

**ESLint:** Use `no-floating-promises` rule.

## Complete Action Example

```typescript
// convex/payments.ts
"use node";

import { action, internalMutation } from "./_generated/server";
import { v } from "convex/values";
import { internal } from "./_generated/api";

export const processPayment = action({
  args: { orderId: v.id("orders"), amount: v.number() },
  returns: v.object({ success: v.boolean(), transactionId: v.optional(v.string()) }),
  handler: async (ctx, args) => {
    // 1. Read data via query
    const order = await ctx.runQuery(internal.orders.get, { orderId: args.orderId });
    if (!order) throw new Error("Order not found");

    // 2. Call external API
    const result = await fetch("https://api.stripe.com/v1/charges", {
      method: "POST",
      headers: { Authorization: `Bearer ${process.env.STRIPE_KEY}` },
      body: new URLSearchParams({ amount: String(args.amount * 100), currency: "usd" }),
    });
    const data = await result.json();

    // 3. Update database via mutation
    await ctx.runMutation(internal.orders.updateStatus, {
      orderId: args.orderId,
      status: data.status === "succeeded" ? "paid" : "failed",
      transactionId: data.id,
    });

    return { success: data.status === "succeeded", transactionId: data.id };
  },
});
```

## References

- Actions: https://docs.convex.dev/functions/actions
- Scheduling: https://docs.convex.dev/scheduling/scheduled-functions
