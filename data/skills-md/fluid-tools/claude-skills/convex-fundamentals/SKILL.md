---
name: convex-fundamentals
description: "Guide for Convex backend development fundamentals including function types (queries, mutations, actions), layered architecture, HTTP actions, and the core mental model. Use when building Convex backends, creating queries/mutations/actions, implementing HTTP webhooks, or understanding Convex's reactive data model. Activates for Convex project setup, function definition, API design, or backend architecture tasks."
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Convex Fundamentals for TypeScript Agents

## Overview

Convex is a reactive backend-as-a-service that provides real-time data synchronization, ACID transactions, and TypeScript-first development. This skill covers the core mental model, function types, layered architecture patterns, and HTTP action implementation.

## TypeScript: NEVER Use `any` Type

**CRITICAL RULE:** This codebase has `@typescript-eslint/no-explicit-any` enabled. Using `any` will cause build failures.

**❌ WRONG:**

```typescript
function handleData(data: any) { ... }
const items: any[] = [];
```

**✅ CORRECT:**

```typescript
function handleData(data: { id: string; name: string }) { ... }
const items: Doc<"items">[] = [];
```

## When to Use This Skill

Use this skill when:

- Building Convex backend applications from scratch
- Creating queries, mutations, or actions
- Understanding the difference between function types
- Implementing layered architecture patterns
- Setting up HTTP webhooks with route handlers
- Migrating from other backends to Convex
- Understanding Convex's reactive data model

## Philosophy: Why Convex Feels "Wrong" (And Why That's Right)

Convex intentionally constrains you. When something feels like an anti-pattern, it's usually Convex telling you to rethink the approach.

### The Intentional Friction

| What feels wrong                            | What Convex is telling you                                                               |
| ------------------------------------------- | ---------------------------------------------------------------------------------------- |
| "I can't use `.filter()` on queries"        | Define an index. Queries should be O(log n), not O(n).                                   |
| "Actions can't access `ctx.db`"             | Side effects and transactions don't mix. Route through mutations.                        |
| "My mutation keeps failing with OCC errors" | You're writing too often to the same document. Redesign your data model or use Workpool. |
| "I can't call `fetch()` in a mutation"      | Mutations must be deterministic. Schedule an action instead.                             |
| "Queries re-run on every document change"   | You're collecting too much data. Narrow your index or denormalize.                       |
| "I can't do joins"                          | Denormalize. Embed related data or use lookup tables.                                    |

### Core Invariants

1. **Mutations are ACID transactions** — All writes succeed together or fail together.
2. **Queries are reactive** — They re-run when any read document changes.
3. **Actions are non-transactional orchestration** — No reactivity, no `ctx.db`. Can do external I/O and must call queries/mutations via `ctx.run*`.
4. **Scheduling is atomic with mutations** — If mutation fails, scheduled functions don't run.

## Core Mental Model

Everything in Convex falls into these categories:

| Kind               | Visibility    | Purpose                               |
| ------------------ | ------------- | ------------------------------------- |
| `query`            | public        | Read from DB, reactive subscriptions  |
| `mutation`         | public        | Write to DB, ACID transactions        |
| `action`           | public        | External APIs, non-deterministic work |
| `httpAction`       | public (HTTP) | Webhooks, third-party integrations    |
| `internalQuery`    | private       | Read primitives for internal use      |
| `internalMutation` | private       | Write primitives for internal use     |
| `internalAction`   | private       | Orchestration, external calls         |

**Rule: Export a thin public surface. All real logic lives in internal primitives.**

> `internal*` variants have identical execution semantics to their public counterparts. The only difference is visibility — internal functions appear on `internal.*`, not `api.*`, and cannot be called from clients.

## Layered Architecture

### Layer 1: Client Surface (Public API)

Only entrypoints live here. Thin wrappers that validate, auth-check, and delegate.

```typescript
// convex/jobs.ts — PUBLIC SURFACE
import { mutation, query } from "./_generated/server";
import { v } from "convex/values";
import { internal } from "./_generated/api";

// Public mutation: client entrypoint
export const startGeneration = mutation({
  args: { prompt: v.string() },
  returns: v.id("jobs"),
  handler: async (ctx, args) => {
    // 1. Auth check
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    // 2. Delegate to internal mutation
    const jobId = await ctx.runMutation(internal.jobs.createJob, {
      userId: identity.subject,
      prompt: args.prompt,
    });

    // 3. Schedule background work
    await ctx.scheduler.runAfter(0, internal.jobs.processJob, { jobId });

    return jobId;
  },
});

// Public query: reactive subscription
export const getJob = query({
  args: { jobId: v.id("jobs") },
  returns: v.union(
    v.object({
      _id: v.id("jobs"),
      _creationTime: v.number(),
      status: v.string(),
      prompt: v.string(),
      result: v.optional(v.string()),
    }),
    v.null()
  ),
  handler: async (ctx, args) => {
    return await ctx.db.get(args.jobId);
  },
});
```

### Layer 2: Domain Logic (Internal Primitives)

Where the real logic lives. These are your backend's private API.

```typescript
// convex/jobs.ts — INTERNAL PRIMITIVES (same file, different exports)
import { internalMutation, internalQuery } from "./_generated/server";
import { v } from "convex/values";

export const createJob = internalMutation({
  args: {
    userId: v.string(),
    prompt: v.string(),
  },
  returns: v.id("jobs"),
  handler: async (ctx, args) => {
    return await ctx.db.insert("jobs", {
      userId: args.userId,
      prompt: args.prompt,
      status: "pending",
    });
  },
});

export const markComplete = internalMutation({
  args: {
    jobId: v.id("jobs"),
    result: v.string(),
  },
  returns: v.null(),
  handler: async (ctx, args) => {
    await ctx.db.patch(args.jobId, {
      status: "completed",
      result: args.result,
    });
    return null;
  },
});

export const markFailed = internalMutation({
  args: {
    jobId: v.id("jobs"),
    error: v.string(),
  },
  returns: v.null(),
  handler: async (ctx, args) => {
    await ctx.db.patch(args.jobId, {
      status: "failed",
      error: args.error,
    });
    return null;
  },
});

export const getById = internalQuery({
  args: { jobId: v.id("jobs") },
  returns: v.union(
    v.object({
      _id: v.id("jobs"),
      _creationTime: v.number(),
      userId: v.string(),
      prompt: v.string(),
      status: v.string(),
      result: v.optional(v.string()),
      error: v.optional(v.string()),
    }),
    v.null()
  ),
  handler: async (ctx, args) => {
    return await ctx.db.get(args.jobId);
  },
});
```

### Layer 3: Orchestration (Actions + Scheduler)

For multi-step, external, or long-running work.

```typescript
// convex/jobs.ts — ORCHESTRATION
import { internalAction } from "./_generated/server";
import { v } from "convex/values";
import { internal } from "./_generated/api";

export const processJob = internalAction({
  args: { jobId: v.id("jobs") },
  returns: v.null(),
  handler: async (ctx, args) => {
    // 1. Read current state
    const job = await ctx.runQuery(internal.jobs.getById, {
      jobId: args.jobId,
    });
    if (!job || job.status !== "pending") return null;

    try {
      // 2. External API call (non-deterministic)
      const result = await fetch("https://api.example.com/generate", {
        method: "POST",
        body: JSON.stringify({ prompt: job.prompt }),
      });
      const data = await result.json();

      // 3. Write result via mutation
      await ctx.runMutation(internal.jobs.markComplete, {
        jobId: args.jobId,
        result: data.output,
      });
    } catch (e) {
      await ctx.runMutation(internal.jobs.markFailed, {
        jobId: args.jobId,
        error: String(e),
      });
    }

    return null;
  },
});
```

## HTTP Actions (Webhooks)

HTTP actions must be in `convex/http.ts` with `httpRouter`:

```typescript
// convex/http.ts
import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";
import { internal } from "./_generated/api";

const http = httpRouter();

http.route({
  path: "/webhooks/stripe",
  method: "POST",
  handler: httpAction(async (ctx, req) => {
    // 1. Validate signature
    const signature = req.headers.get("stripe-signature");
    if (!signature) {
      return new Response("Missing signature", { status: 401 });
    }

    // 2. Parse body
    const body = await req.text();

    // 3. Delegate to internal mutation
    await ctx.runMutation(internal.billing.handleStripeWebhook, {
      signature,
      body,
    });

    return new Response(null, { status: 200 });
  }),
});

export default http;
```

## Model Layer Pattern

Extract business logic into reusable model functions. Functions stay thin; models do the work.

### Why Model Layer?

1. **Reuse** — Same logic across queries, mutations, actions
2. **Testability** — Pure functions, easy to unit test
3. **Separation** — Auth checks in one place, business logic in another
4. **Type Safety** — `QueryCtx` and `MutationCtx` types for context

### Pattern: Model Functions

```typescript
// convex/model/users.ts — MODEL LAYER
import { QueryCtx, MutationCtx } from "../_generated/server";
import { Id } from "../_generated/dataModel";

// Read helper: reusable across queries
export async function getCurrentUser(ctx: QueryCtx) {
  const identity = await ctx.auth.getUserIdentity();
  if (!identity) throw new Error("Unauthorized");

  const user = await ctx.db
    .query("users")
    .withIndex("by_tokenIdentifier", (q) =>
      q.eq("tokenIdentifier", identity.tokenIdentifier)
    )
    .unique();

  if (!user) throw new Error("User not found");
  return user;
}

// Access control helper
export async function ensureHasAccess(
  ctx: QueryCtx,
  { conversationId }: { conversationId: Id<"conversations"> }
) {
  const user = await getCurrentUser(ctx);
  const conversation = await ctx.db.get(conversationId);
  if (!conversation || !conversation.members.includes(user._id)) {
    throw new Error("Unauthorized");
  }
  return { user, conversation };
}

// Write helper: encapsulates business logic
export async function addMessage(
  ctx: MutationCtx,
  {
    conversationId,
    content,
  }: { conversationId: Id<"conversations">; content: string }
) {
  const { user } = await ensureHasAccess(ctx, { conversationId });

  const messageId = await ctx.db.insert("messages", {
    conversationId,
    authorId: user._id,
    content,
    createdAt: Date.now(),
  });

  // Update denormalized lastMessageAt
  await ctx.db.patch(conversationId, { lastMessageAt: Date.now() });

  return messageId;
}
```

### Pattern: Thin Function Wrappers

```typescript
// convex/conversations.ts — THIN WRAPPERS
import { mutation, query } from "./_generated/server";
import { v } from "convex/values";
import * as Conversations from "./model/conversations";

// Query: delegates to model
export const listMessages = query({
  args: { conversationId: v.id("conversations") },
  returns: v.array(
    v.object({
      _id: v.id("messages"),
      content: v.string(),
      authorId: v.id("users"),
      createdAt: v.number(),
    })
  ),
  handler: async (ctx, args) => {
    return Conversations.listMessages(ctx, args);
  },
});

// Mutation: delegates to model
export const sendMessage = mutation({
  args: { conversationId: v.id("conversations"), content: v.string() },
  returns: v.id("messages"),
  handler: async (ctx, args) => {
    return Conversations.addMessage(ctx, args);
  },
});
```

## File Structure

Flat-first. Convex uses file-based routing:

```
convex/
  schema.ts              # Database schema
  http.ts                # HTTP actions (webhooks)
  auth.ts                # Auth helpers
  crons.ts               # Cron job definitions

  # Domain files (public + internal in same file)
  users.ts               # api.users.* + internal.users.*
  jobs.ts
  billing.ts
  audio.ts

  # Model layer (business logic)
  model/
    users.ts             # User business logic helpers
    conversations.ts     # Conversation logic
    billing.ts           # Billing logic

  # Shared utilities (NOT Convex functions)
  _lib/
    validators.ts        # Shared validators
    constants.ts         # Constants
```

**Routing:**

- `convex/users.ts` → `api.users.functionName` / `internal.users.functionName`
- `convex/audio/stems.ts` → `api.audio.stems.functionName`
- `convex/model/*.ts` → NOT routed (helper imports only)

## Function Types Quick Reference

### Import Patterns

```typescript
// Public (client-callable)
import { query, mutation, action } from "./_generated/server";

// Private (internal only)
import {
  internalQuery,
  internalMutation,
  internalAction,
} from "./_generated/server";

// HTTP
import { httpAction } from "./_generated/server";
import { httpRouter } from "convex/server";
```

### Function References

```typescript
import { api, internal } from "./_generated/api";

// Public: api.fileName.functionName
await ctx.runQuery(api.users.getUser, { userId });

// Internal: internal.fileName.functionName
await ctx.runMutation(internal.jobs.createJob, { data });
```

### Database Operations

```typescript
// Read
const doc = await ctx.db.get(id);
const docs = await ctx.db
  .query("table")
  .withIndex("by_x", (q) => q.eq("x", value))
  .collect();
const single = await ctx.db
  .query("table")
  .withIndex("by_x", (q) => q.eq("x", value))
  .unique();

// Write
const id = await ctx.db.insert("table", { field: value });
await ctx.db.patch(id, { field: newValue });
await ctx.db.replace(id, { ...fullDocument });
await ctx.db.delete(id);
```

## Common Pitfalls

### Pitfall 1: Calling fetch() in Mutations

**❌ WRONG:**

```typescript
export const createOrder = mutation({
  args: { productId: v.string() },
  returns: v.null(),
  handler: async (ctx, args) => {
    // ❌ Mutations must be deterministic - no external calls!
    const price = await fetch(
      "https://api.stripe.com/prices/" + args.productId
    );
    await ctx.db.insert("orders", { productId: args.productId, price });
    return null;
  },
});
```

**✅ CORRECT:**

```typescript
// Mutation creates order, schedules action for external call
export const createOrder = mutation({
  args: { productId: v.string() },
  returns: v.id("orders"),
  handler: async (ctx, args) => {
    const orderId = await ctx.db.insert("orders", {
      productId: args.productId,
      status: "pending",
    });
    await ctx.scheduler.runAfter(0, internal.orders.fetchPrice, { orderId });
    return orderId;
  },
});

// Action handles external API call
export const fetchPrice = internalAction({
  args: { orderId: v.id("orders") },
  returns: v.null(),
  handler: async (ctx, args) => {
    const order = await ctx.runQuery(internal.orders.getById, {
      orderId: args.orderId,
    });
    const price = await fetch(
      "https://api.stripe.com/prices/" + order.productId
    );
    await ctx.runMutation(internal.orders.updatePrice, {
      orderId: args.orderId,
      price: await price.json(),
    });
    return null;
  },
});
```

### Pitfall 2: Accessing ctx.db in Actions

**❌ WRONG:**

```typescript
export const processData = action({
  args: { id: v.string() },
  returns: v.null(),
  handler: async (ctx, args) => {
    // ❌ Actions don't have ctx.db!
    const data = await ctx.db.get(args.id);
    return null;
  },
});
```

**✅ CORRECT:**

```typescript
export const processData = action({
  args: { id: v.id("data") },
  returns: v.null(),
  handler: async (ctx, args) => {
    // ✅ Use ctx.runQuery to read data
    const data = await ctx.runQuery(internal.data.getById, { id: args.id });

    // Do external work...
    const result = await fetch("...");

    // ✅ Use ctx.runMutation to write data
    await ctx.runMutation(internal.data.update, {
      id: args.id,
      result: await result.json(),
    });

    return null;
  },
});
```

### Pitfall 3: Missing returns Validator

**❌ WRONG:**

```typescript
export const foo = mutation({
  args: {},
  handler: async (ctx) => {
    // implicitly returns undefined
  },
});
```

**✅ CORRECT:**

```typescript
export const foo = mutation({
  args: {},
  returns: v.null(),
  handler: async (ctx) => {
    return null;
  },
});
```

## Decision Guide

1. **Does this function read from DB?** → Use `query` or `internalQuery`
2. **Does this function write to DB?** → Use `mutation` or `internalMutation`
3. **Does this function call external APIs?** → Use `action` or `internalAction`
4. **Is this called by clients?** → Use public variants (`query`, `mutation`, `action`)
5. **Is this internal only?** → Use `internal*` variants
6. **Is this a webhook endpoint?** → Use `httpAction` in `convex/http.ts`
