---
name: convex-cron
description: Scheduled functions and cron jobs in Convex. Use when setting up recurring tasks, cleanup jobs, data syncing, scheduled notifications, or any background automation that runs on a schedule.
---

# Convex Cron Jobs

## Basic Cron Setup

```typescript
// convex/crons.ts
import { cronJobs } from "convex/server";
import { internal } from "./_generated/api";

const crons = cronJobs();

// Run every hour
crons.interval(
  "cleanup expired sessions",
  { hours: 1 },
  internal.tasks.cleanupExpiredSessions,
  {}
);

// Run every day at midnight UTC
crons.cron(
  "daily report",
  "0 0 * * *",
  internal.reports.generateDailyReport,
  {}
);

export default crons;
```

## Interval-Based Scheduling

```typescript
// Every 5 minutes
crons.interval("sync data", { minutes: 5 }, internal.sync.fetchData, {});

// Every 2 hours
crons.interval("cleanup temp", { hours: 2 }, internal.files.cleanup, {});

// Every 30 seconds (minimum)
crons.interval("health check", { seconds: 30 }, internal.monitoring.check, {});
```

## Cron Expression Scheduling

```
┌───────────── minute (0-59)
│ ┌───────────── hour (0-23)
│ │ ┌───────────── day of month (1-31)
│ │ │ ┌───────────── month (1-12)
│ │ │ │ ┌───────────── day of week (0-6, Sunday=0)
* * * * *
```

```typescript
// Every day at 9 AM UTC
crons.cron("morning digest", "0 9 * * *", internal.notifications.morning, {});

// Every Monday at 8 AM UTC
crons.cron("weekly summary", "0 8 * * 1", internal.reports.weekly, {});

// First day of month at midnight
crons.cron("monthly billing", "0 0 1 * *", internal.billing.process, {});

// Every 15 minutes
crons.cron("frequent sync", "*/15 * * * *", internal.sync.run, {});
```

## Internal Functions for Crons

Always use internal functions:

```typescript
// convex/tasks.ts
import { internalMutation } from "./_generated/server";
import { v } from "convex/values";

export const cleanupExpiredSessions = internalMutation({
  args: {},
  returns: v.number(),
  handler: async (ctx) => {
    const oneHourAgo = Date.now() - 60 * 60 * 1000;

    const expired = await ctx.db
      .query("sessions")
      .withIndex("by_lastActive")
      .filter((q) => q.lt(q.field("lastActive"), oneHourAgo))
      .collect();

    for (const session of expired) {
      await ctx.db.delete(session._id);
    }

    return expired.length;
  },
});
```

## Crons with Arguments

```typescript
crons.interval(
  "cleanup temp files",
  { hours: 1 },
  internal.cleanup.byType,
  { fileType: "temp", maxAge: 3600000 }
);

crons.interval(
  "cleanup cache files",
  { hours: 24 },
  internal.cleanup.byType,
  { fileType: "cache", maxAge: 86400000 }
);
```

## Batching Large Datasets

Handle large datasets to avoid timeouts:

```typescript
const BATCH_SIZE = 100;

export const processBatch = internalMutation({
  args: { cursor: v.optional(v.string()) },
  returns: v.null(),
  handler: async (ctx, args) => {
    const result = await ctx.db
      .query("items")
      .withIndex("by_status", (q) => q.eq("status", "pending"))
      .paginate({ numItems: BATCH_SIZE, cursor: args.cursor ?? null });

    for (const item of result.page) {
      await ctx.db.patch(item._id, { status: "processed", processedAt: Date.now() });
    }

    // Schedule next batch if more items
    if (!result.isDone) {
      await ctx.scheduler.runAfter(0, internal.tasks.processBatch, {
        cursor: result.continueCursor,
      });
    }
    return null;
  },
});
```

## External API Calls

Use actions for external APIs:

```typescript
// convex/sync.ts
"use node";

import { internalAction, internalMutation } from "./_generated/server";
import { internal } from "./_generated/api";
import { v } from "convex/values";

export const syncExternalData = internalAction({
  args: {},
  returns: v.null(),
  handler: async (ctx) => {
    const response = await fetch("https://api.example.com/data", {
      headers: { Authorization: `Bearer ${process.env.API_KEY}` },
    });

    const data = await response.json();

    await ctx.runMutation(internal.sync.storeData, { data, syncedAt: Date.now() });
    return null;
  },
});

// In crons.ts
crons.interval("sync external", { minutes: 15 }, internal.sync.syncExternalData, {});
```

## Logging and Monitoring

```typescript
export const cleanupWithLogging = internalMutation({
  args: {},
  returns: v.null(),
  handler: async (ctx) => {
    const startTime = Date.now();
    let processedCount = 0;

    try {
      const items = await ctx.db.query("items")
        .filter((q) => q.lt(q.field("expiresAt"), Date.now()))
        .collect();

      for (const item of items) {
        await ctx.db.delete(item._id);
        processedCount++;
      }

      await ctx.db.insert("cronLogs", {
        jobName: "cleanup",
        duration: Date.now() - startTime,
        processedCount,
        status: "success",
      });
    } catch (error) {
      await ctx.db.insert("cronLogs", {
        jobName: "cleanup",
        duration: Date.now() - startTime,
        processedCount,
        status: "failed",
        error: String(error),
      });
      throw error;
    }
    return null;
  },
});
```

## Common Pitfalls

- **Using public functions** - Always use internal functions
- **Forgetting timezone** - All cron expressions use UTC
- **Long-running mutations** - Break into batches
- **Missing error handling** - Log failures for debugging

## References

- Cron Jobs: https://docs.convex.dev/scheduling/cron-jobs
- Scheduling: https://docs.convex.dev/scheduling
