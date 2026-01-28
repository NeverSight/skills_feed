---
name: convex-actions-scheduling
description: "Guide for Convex actions, scheduling, cron jobs, and orchestration patterns. Use when implementing external API calls, background jobs, scheduled tasks, cron jobs, or multi-step workflows. Activates for action implementation, ctx.scheduler usage, crons.ts creation, or long-running workflow tasks."
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Convex Actions & Scheduling Guide

## Overview

Convex provides powerful tools for handling asynchronous work, external API calls, and scheduled tasks. This skill covers actions (non-deterministic operations), the scheduler for background jobs, cron jobs for recurring tasks, and orchestration patterns for complex workflows.

## TypeScript: NEVER Use `any` Type

**CRITICAL RULE:** This codebase has `@typescript-eslint/no-explicit-any` enabled. Using `any` will cause build failures.

## When to Use This Skill

Use this skill when:

- Calling external APIs (fetch, third-party SDKs)
- Implementing background job processing
- Scheduling delayed or recurring tasks
- Creating cron jobs for periodic work
- Building multi-step workflows
- Orchestrating complex operations across functions

## Actions: Non-Deterministic Operations

### What Actions Can Do

Actions are for work that:

- Calls external APIs (`fetch`, third-party SDKs)
- Uses Node.js modules (crypto, fs, etc.)
- Performs non-deterministic operations
- Needs to orchestrate multiple queries/mutations

### What Actions Cannot Do

**CRITICAL:** Actions have NO direct database access!

```typescript
// ❌ WRONG: Actions cannot access ctx.db
export const processData = action({
  args: { id: v.id("items") },
  returns: v.null(),
  handler: async (ctx, args) => {
    const item = await ctx.db.get(args.id); // ❌ ERROR! No ctx.db in actions
    return null;
  },
});

// ✅ CORRECT: Use ctx.runQuery and ctx.runMutation
export const processData = action({
  args: { id: v.id("items") },
  returns: v.null(),
  handler: async (ctx, args) => {
    // Read via query
    const item = await ctx.runQuery(internal.items.getById, { id: args.id });

    // Call external API
    const result = await fetch("https://api.example.com/process", {
      method: "POST",
      body: JSON.stringify(item),
    });

    // Write via mutation
    await ctx.runMutation(internal.items.updateResult, {
      id: args.id,
      result: await result.json(),
    });

    return null;
  },
});
```

### Node.js Runtime for Actions

Add `"use node";` at the top of files using Node.js modules:

```typescript
// convex/pdf.ts
"use node";

import { internalAction } from "./_generated/server";
import { v } from "convex/values";
import pdf from "pdf-parse";

export const extractText = internalAction({
  args: { pdfData: v.bytes() },
  returns: v.string(),
  handler: async (ctx, args) => {
    const buffer = Buffer.from(args.pdfData);
    const data = await pdf(buffer);
    return data.text;
  },
});
```

### Action Patterns

**Pattern 1: External API Call**

```typescript
export const sendEmail = internalAction({
  args: {
    to: v.string(),
    subject: v.string(),
    body: v.string(),
  },
  returns: v.object({
    success: v.boolean(),
    messageId: v.optional(v.string()),
  }),
  handler: async (ctx, args) => {
    const response = await fetch("https://api.sendgrid.com/v3/mail/send", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.SENDGRID_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        personalizations: [{ to: [{ email: args.to }] }],
        from: { email: "noreply@example.com" },
        subject: args.subject,
        content: [{ type: "text/plain", value: args.body }],
      }),
    });

    if (response.ok) {
      const data = await response.json();
      return { success: true, messageId: data.id };
    }

    return { success: false };
  },
});
```

**Pattern 2: Multi-Step Workflow**

```typescript
export const processOrder = internalAction({
  args: { orderId: v.id("orders") },
  returns: v.null(),
  handler: async (ctx, args) => {
    // Step 1: Get order details
    const order = await ctx.runQuery(internal.orders.getById, {
      orderId: args.orderId,
    });
    if (!order) throw new Error("Order not found");

    try {
      // Step 2: Charge payment (external API)
      const paymentResult = await fetch("https://api.stripe.com/v1/charges", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${process.env.STRIPE_SECRET_KEY}`,
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          amount: String(order.total),
          currency: "usd",
          source: order.paymentMethodId,
        }),
      });

      if (!paymentResult.ok) {
        throw new Error("Payment failed");
      }

      const paymentData = await paymentResult.json();

      // Step 3: Update order status
      await ctx.runMutation(internal.orders.markPaid, {
        orderId: args.orderId,
        chargeId: paymentData.id,
      });

      // Step 4: Schedule fulfillment
      await ctx.scheduler.runAfter(0, internal.fulfillment.processOrder, {
        orderId: args.orderId,
      });
    } catch (error) {
      await ctx.runMutation(internal.orders.markFailed, {
        orderId: args.orderId,
        error: String(error),
      });
    }

    return null;
  },
});
```

## Scheduling

### Fire-and-Forget (Immediate)

Schedule work to run immediately but asynchronously:

```typescript
export const submitJob = mutation({
  args: { data: v.string() },
  returns: v.id("jobs"),
  handler: async (ctx, args) => {
    const jobId = await ctx.db.insert("jobs", {
      data: args.data,
      status: "pending",
    });

    // Schedule immediately (0ms delay)
    await ctx.scheduler.runAfter(0, internal.jobs.process, { jobId });

    return jobId;
  },
});
```

### Delayed Execution

Schedule work to run after a delay:

```typescript
// Self-destructing message
export const sendExpiringMessage = mutation({
  args: { body: v.string(), expiresInMs: v.number() },
  returns: v.id("messages"),
  handler: async (ctx, args) => {
    const id = await ctx.db.insert("messages", { body: args.body });

    // Delete after specified time
    await ctx.scheduler.runAfter(args.expiresInMs, internal.messages.delete, {
      id,
    });

    return id;
  },
});

export const delete_ = internalMutation({
  args: { id: v.id("messages") },
  returns: v.null(),
  handler: async (ctx, args) => {
    await ctx.db.delete(args.id);
    return null;
  },
});
```

### Scheduled at Specific Time

```typescript
export const scheduleReminder = mutation({
  args: {
    userId: v.id("users"),
    message: v.string(),
    sendAt: v.number(), // Unix timestamp
  },
  returns: v.id("scheduledFunctions"),
  handler: async (ctx, args) => {
    // Schedule at specific timestamp
    return await ctx.scheduler.runAt(
      args.sendAt,
      internal.notifications.sendReminder,
      {
        userId: args.userId,
        message: args.message,
      }
    );
  },
});
```

### Cancel Scheduled Functions

```typescript
export const cancelReminder = mutation({
  args: { scheduledId: v.id("_scheduled_functions") },
  returns: v.null(),
  handler: async (ctx, args) => {
    await ctx.scheduler.cancel(args.scheduledId);
    return null;
  },
});
```

### Scheduling from Actions

Actions can also schedule work:

```typescript
export const processWithRetry = internalAction({
  args: { jobId: v.id("jobs"), attempt: v.number() },
  returns: v.null(),
  handler: async (ctx, args) => {
    try {
      // Try to process
      const job = await ctx.runQuery(internal.jobs.getById, {
        jobId: args.jobId,
      });
      const result = await fetch("https://api.example.com/process", {
        method: "POST",
        body: JSON.stringify(job),
      });

      if (!result.ok) throw new Error("API error");

      await ctx.runMutation(internal.jobs.markComplete, {
        jobId: args.jobId,
        result: await result.json(),
      });
    } catch (error) {
      if (args.attempt < 3) {
        // Retry with exponential backoff
        const delay = Math.pow(2, args.attempt) * 1000;
        await ctx.scheduler.runAfter(delay, internal.jobs.processWithRetry, {
          jobId: args.jobId,
          attempt: args.attempt + 1,
        });
      } else {
        await ctx.runMutation(internal.jobs.markFailed, {
          jobId: args.jobId,
          error: String(error),
        });
      }
    }

    return null;
  },
});
```

## Cron Jobs

### Creating Cron Jobs

Cron jobs must be defined in `convex/crons.ts`:

```typescript
// convex/crons.ts
import { cronJobs } from "convex/server";
import { internal } from "./_generated/api";

const crons = cronJobs();

// Run every hour
crons.interval(
  "cleanup stale jobs",
  { hours: 1 },
  internal.jobs.cleanupStale,
  {}
);

// Run at specific cron schedule
crons.cron(
  "daily report",
  "0 9 * * *", // 9 AM every day
  internal.reports.generateDaily,
  {}
);

// Run every 5 minutes
crons.interval(
  "sync external data",
  { minutes: 5 },
  internal.sync.pullExternalData,
  {}
);

// Run weekly on Sundays at midnight
crons.cron(
  "weekly cleanup",
  "0 0 * * 0",
  internal.maintenance.weeklyCleanup,
  {}
);

export default crons;
```

### Interval Options

```typescript
// Various interval configurations
crons.interval("every-minute", { minutes: 1 }, handler, {});
crons.interval("every-hour", { hours: 1 }, handler, {});
crons.interval("every-day", { hours: 24 }, handler, {});
crons.interval("every-30-seconds", { seconds: 30 }, handler, {});
```

### Cron Schedule Syntax

Standard cron format: `minute hour day month weekday`

```typescript
// Examples
"* * * * *"; // Every minute
"0 * * * *"; // Every hour
"0 0 * * *"; // Every day at midnight
"0 9 * * *"; // Every day at 9 AM
"0 0 * * 0"; // Every Sunday at midnight
"0 0 1 * *"; // First day of every month
"*/5 * * * *"; // Every 5 minutes
"0 */2 * * *"; // Every 2 hours
```

### Cron Job Implementation

```typescript
// convex/jobs.ts
export const cleanupStale = internalMutation({
  args: {},
  returns: v.number(),
  handler: async (ctx) => {
    const oneHourAgo = Date.now() - 60 * 60 * 1000;

    const staleJobs = await ctx.db
      .query("jobs")
      .withIndex("by_status_and_createdAt", (q) =>
        q.eq("status", "pending").lt("createdAt", oneHourAgo)
      )
      .collect();

    for (const job of staleJobs) {
      await ctx.db.patch(job._id, { status: "stale" });
    }

    return staleJobs.length;
  },
});
```

## Orchestration Patterns

### Pattern 1: Saga Pattern (Compensating Transactions)

For operations that span multiple services with rollback:

```typescript
export const createSubscription = internalAction({
  args: {
    userId: v.id("users"),
    planId: v.string(),
  },
  returns: v.union(v.id("subscriptions"), v.null()),
  handler: async (ctx, args) => {
    const user = await ctx.runQuery(internal.users.getById, {
      userId: args.userId,
    });
    if (!user) throw new Error("User not found");

    // Step 1: Create Stripe subscription
    let stripeSubscriptionId: string | null = null;
    try {
      const stripeResponse = await fetch(
        "https://api.stripe.com/v1/subscriptions",
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${process.env.STRIPE_SECRET_KEY}`,
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: new URLSearchParams({
            customer: user.stripeCustomerId,
            items: [{ price: args.planId }]
              .map((i, idx) => `items[${idx}][price]=${i.price}`)
              .join("&"),
          }),
        }
      );

      if (!stripeResponse.ok) {
        throw new Error("Stripe subscription failed");
      }

      const stripeData = await stripeResponse.json();
      stripeSubscriptionId = stripeData.id;
    } catch (error) {
      // No cleanup needed - nothing created yet
      return null;
    }

    // Step 2: Create local subscription record
    try {
      const subscriptionId = await ctx.runMutation(
        internal.subscriptions.create,
        {
          userId: args.userId,
          planId: args.planId,
          stripeSubscriptionId,
        }
      );

      return subscriptionId;
    } catch (error) {
      // Rollback: Cancel Stripe subscription
      await fetch(
        `https://api.stripe.com/v1/subscriptions/${stripeSubscriptionId}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${process.env.STRIPE_SECRET_KEY}`,
          },
        }
      );

      return null;
    }
  },
});
```

### Pattern 2: Fan-Out / Fan-In

Process multiple items in parallel, then aggregate:

```typescript
// Fan-out: Schedule processing for each item
export const processAll = mutation({
  args: { itemIds: v.array(v.id("items")) },
  returns: v.id("batchJobs"),
  handler: async (ctx, args) => {
    const batchId = await ctx.db.insert("batchJobs", {
      totalItems: args.itemIds.length,
      completedItems: 0,
      status: "processing",
    });

    // Fan-out: Schedule each item
    for (const itemId of args.itemIds) {
      await ctx.scheduler.runAfter(0, internal.items.processOne, {
        itemId,
        batchId,
      });
    }

    return batchId;
  },
});

// Process single item
export const processOne = internalAction({
  args: { itemId: v.id("items"), batchId: v.id("batchJobs") },
  returns: v.null(),
  handler: async (ctx, args) => {
    const item = await ctx.runQuery(internal.items.getById, {
      itemId: args.itemId,
    });

    // Process item (external API, etc.)
    const result = await fetch("https://api.example.com/process", {
      method: "POST",
      body: JSON.stringify(item),
    });

    // Update item with result
    await ctx.runMutation(internal.items.updateResult, {
      itemId: args.itemId,
      result: await result.json(),
    });

    // Fan-in: Update batch progress
    await ctx.runMutation(internal.batches.incrementCompleted, {
      batchId: args.batchId,
    });

    return null;
  },
});

// Fan-in: Track completion
export const incrementCompleted = internalMutation({
  args: { batchId: v.id("batchJobs") },
  returns: v.null(),
  handler: async (ctx, args) => {
    const batch = await ctx.db.get(args.batchId);
    if (!batch) return null;

    const newCompleted = batch.completedItems + 1;
    const isComplete = newCompleted >= batch.totalItems;

    await ctx.db.patch(args.batchId, {
      completedItems: newCompleted,
      status: isComplete ? "completed" : "processing",
    });

    if (isComplete) {
      // Trigger completion handler
      await ctx.scheduler.runAfter(0, internal.batches.onComplete, {
        batchId: args.batchId,
      });
    }

    return null;
  },
});
```

### Pattern 3: Retry with Exponential Backoff and Jitter

```typescript
export const processWithRetry = internalAction({
  args: {
    jobId: v.id("jobs"),
    attempt: v.number(),
    maxAttempts: v.optional(v.number()),
  },
  returns: v.null(),
  handler: async (ctx, args) => {
    const maxAttempts = args.maxAttempts ?? 5;

    try {
      const job = await ctx.runQuery(internal.jobs.getById, {
        jobId: args.jobId,
      });
      if (!job) return null;

      const response = await fetch("https://api.example.com/process", {
        method: "POST",
        body: JSON.stringify(job),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      await ctx.runMutation(internal.jobs.markComplete, {
        jobId: args.jobId,
        result: await response.json(),
      });
    } catch (error) {
      if (args.attempt < maxAttempts) {
        // Exponential backoff with jitter
        const baseDelay = Math.pow(2, args.attempt) * 1000;
        const jitter = Math.random() * 1000;
        const delay = baseDelay + jitter;

        await ctx.scheduler.runAfter(delay, internal.jobs.processWithRetry, {
          jobId: args.jobId,
          attempt: args.attempt + 1,
          maxAttempts,
        });

        await ctx.runMutation(internal.jobs.updateAttempt, {
          jobId: args.jobId,
          attempt: args.attempt + 1,
          nextRetryAt: Date.now() + delay,
        });
      } else {
        await ctx.runMutation(internal.jobs.markFailed, {
          jobId: args.jobId,
          error: String(error),
          finalAttempt: args.attempt,
        });
      }
    }

    return null;
  },
});
```

### Pattern 4: Idempotency Keys

Prevent duplicate processing:

```typescript
export const processPayment = mutation({
  args: {
    idempotencyKey: v.string(),
    amount: v.number(),
    customerId: v.string(),
  },
  returns: v.union(v.id("payments"), v.null()),
  handler: async (ctx, args) => {
    // Check if already processed
    const existing = await ctx.db
      .query("payments")
      .withIndex("by_idempotency_key", (q) =>
        q.eq("idempotencyKey", args.idempotencyKey)
      )
      .unique();

    if (existing) return existing._id; // Already done, return existing

    // Process and record
    const paymentId = await ctx.db.insert("payments", {
      idempotencyKey: args.idempotencyKey,
      amount: args.amount,
      customerId: args.customerId,
      status: "pending",
    });

    await ctx.scheduler.runAfter(0, internal.payments.charge, { paymentId });

    return paymentId;
  },
});
```

## Common Pitfalls

### Pitfall 1: Actions Without Error Handling

**❌ WRONG:**

```typescript
export const sendNotification = internalAction({
  args: { userId: v.id("users") },
  returns: v.null(),
  handler: async (ctx, args) => {
    const user = await ctx.runQuery(internal.users.getById, {
      userId: args.userId,
    });

    // If this fails, we lose track of the failure
    await fetch("https://api.pushover.net/send", {
      method: "POST",
      body: JSON.stringify({ user: user.pushToken, message: "Hello" }),
    });

    return null;
  },
});
```

**✅ CORRECT:**

```typescript
export const sendNotification = internalAction({
  args: { userId: v.id("users"), notificationId: v.id("notifications") },
  returns: v.null(),
  handler: async (ctx, args) => {
    const user = await ctx.runQuery(internal.users.getById, {
      userId: args.userId,
    });

    try {
      const response = await fetch("https://api.pushover.net/send", {
        method: "POST",
        body: JSON.stringify({ user: user.pushToken, message: "Hello" }),
      });

      if (!response.ok) {
        throw new Error(`Push API error: ${response.status}`);
      }

      await ctx.runMutation(internal.notifications.markSent, {
        notificationId: args.notificationId,
      });
    } catch (error) {
      await ctx.runMutation(internal.notifications.markFailed, {
        notificationId: args.notificationId,
        error: String(error),
      });
    }

    return null;
  },
});
```

### Pitfall 2: Not Using Internal Functions

**❌ WRONG:**

```typescript
// Public action callable by anyone!
export const deleteAllUserData = action({
  args: { userId: v.id("users") },
  returns: v.null(),
  handler: async (ctx, args) => {
    // Dangerous! No auth check, publicly accessible
    await ctx.runMutation(api.users.delete, { userId: args.userId });
    return null;
  },
});
```

**✅ CORRECT:**

```typescript
// Internal action - only callable from other functions
export const deleteAllUserData = internalAction({
  args: { userId: v.id("users") },
  returns: v.null(),
  handler: async (ctx, args) => {
    // Safe - only called from authenticated internal code
    await ctx.runMutation(internal.users.delete, { userId: args.userId });
    return null;
  },
});

// Public mutation with auth check schedules the internal action
export const requestAccountDeletion = mutation({
  args: {},
  returns: v.null(),
  handler: async (ctx) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    const user = await ctx.db
      .query("users")
      .withIndex("by_tokenIdentifier", (q) =>
        q.eq("tokenIdentifier", identity.tokenIdentifier)
      )
      .unique();

    if (!user) throw new Error("User not found");

    await ctx.scheduler.runAfter(0, internal.users.deleteAllUserData, {
      userId: user._id,
    });

    return null;
  },
});
```

### Pitfall 3: Thundering Herd

**❌ WRONG:**

```typescript
// All retries happen at the same time
const retryDelay = 5000;
await ctx.scheduler.runAfter(retryDelay, internal.jobs.retry, { jobId });
```

**✅ CORRECT:**

```typescript
// Add jitter to spread out retries
const baseDelay = 5000;
const jitter = Math.random() * 1000;
await ctx.scheduler.runAfter(baseDelay + jitter, internal.jobs.retry, {
  jobId,
});
```

## Quick Reference

### Scheduling Methods

```typescript
// Immediate (0ms delay)
await ctx.scheduler.runAfter(0, internal.jobs.process, { jobId });

// Delayed (milliseconds)
await ctx.scheduler.runAfter(5000, internal.messages.delete, { id });

// At specific timestamp
await ctx.scheduler.runAt(timestamp, internal.reports.send, {});

// Cancel scheduled function
await ctx.scheduler.cancel(scheduledFunctionId);
```

### Cron Syntax

| Expression     | Description           |
| -------------- | --------------------- |
| `* * * * *`    | Every minute          |
| `0 * * * *`    | Every hour            |
| `0 0 * * *`    | Every day at midnight |
| `0 9 * * 1-5`  | 9 AM weekdays         |
| `*/15 * * * *` | Every 15 minutes      |
| `0 0 1 * *`    | First of month        |

### Action Context Methods

```typescript
// Read data
await ctx.runQuery(internal.table.query, args);

// Write data
await ctx.runMutation(internal.table.mutation, args);

// Call another action
await ctx.runAction(internal.external.action, args);

// Schedule work
await ctx.scheduler.runAfter(delay, internal.jobs.process, args);
await ctx.scheduler.runAt(timestamp, internal.jobs.process, args);
```
