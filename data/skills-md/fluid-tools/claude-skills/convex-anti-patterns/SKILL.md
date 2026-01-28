---
name: convex-anti-patterns
description: "Critical rules and common mistakes to avoid in Convex development. Use when reviewing Convex code, debugging issues, or learning what NOT to do. Activates for code review, debugging OCC errors, fixing type errors, or understanding why code fails in Convex."
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Convex Anti-Patterns & Agent Rules

## Overview

This skill documents critical mistakes to avoid in Convex development and rules that agents must follow. Every pattern here has caused real production issues.

## TypeScript: NEVER Use `any` Type

**CRITICAL RULE:** This codebase has `@typescript-eslint/no-explicit-any` enabled. Using `any` will cause build failures.

**❌ WRONG:**

```typescript
function handleData(data: any) { ... }
const items: any[] = [];
args: { data: v.any() }  // Also avoid!
```

**✅ CORRECT:**

```typescript
function handleData(data: Doc<"items">) { ... }
const items: Doc<"items">[] = [];
args: { data: v.object({ field: v.string() }) }
```

## When to Use This Skill

Use this skill when:

- Reviewing Convex code for issues
- Debugging mysterious errors
- Understanding why code doesn't work as expected
- Learning Convex best practices by counter-example
- Checking code against known anti-patterns

## Critical Anti-Patterns

### Anti-Pattern 1: fetch() in Mutations

Mutations must be deterministic. External calls break this guarantee.

**❌ WRONG:**

```typescript
export const createOrder = mutation({
  args: { productId: v.string() },
  returns: v.null(),
  handler: async (ctx, args) => {
    // ❌ Mutations cannot make external HTTP calls!
    const price = await fetch(
      `https://api.stripe.com/prices/${args.productId}`
    );
    await ctx.db.insert("orders", {
      productId: args.productId,
      price: await price.json(),
    });
    return null;
  },
});
```

**✅ CORRECT:**

```typescript
// Mutation creates record, schedules action for external call
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
    if (!order) return null;

    const response = await fetch(
      `https://api.stripe.com/prices/${order.productId}`
    );
    const priceData = await response.json();

    await ctx.runMutation(internal.orders.updatePrice, {
      orderId: args.orderId,
      price: priceData.unit_amount,
    });
    return null;
  },
});
```

### Anti-Pattern 2: ctx.db in Actions

Actions don't have database access. This is a common source of TypeScript errors.

**❌ WRONG:**

```typescript
export const processData = action({
  args: { id: v.id("items") },
  returns: v.null(),
  handler: async (ctx, args) => {
    // ❌ Actions don't have ctx.db!
    const item = await ctx.db.get(args.id); // TypeScript Error!
    return null;
  },
});
```

**✅ CORRECT:**

```typescript
export const processData = action({
  args: { id: v.id("items") },
  returns: v.null(),
  handler: async (ctx, args) => {
    // ✅ Use ctx.runQuery to read
    const item = await ctx.runQuery(internal.items.getById, { id: args.id });

    // Process with external APIs...
    const result = await fetch("https://api.example.com/process", {
      method: "POST",
      body: JSON.stringify(item),
    });

    // ✅ Use ctx.runMutation to write
    await ctx.runMutation(internal.items.updateResult, {
      id: args.id,
      result: await result.json(),
    });

    return null;
  },
});
```

### Anti-Pattern 3: Missing returns Validator

Every function must have an explicit `returns` validator.

**❌ WRONG:**

```typescript
export const doSomething = mutation({
  args: { data: v.string() },
  // ❌ Missing returns!
  handler: async (ctx, args) => {
    await ctx.db.insert("items", { data: args.data });
    // Implicitly returns undefined
  },
});
```

**✅ CORRECT:**

```typescript
export const doSomething = mutation({
  args: { data: v.string() },
  returns: v.null(), // ✅ Explicit returns validator
  handler: async (ctx, args) => {
    await ctx.db.insert("items", { data: args.data });
    return null; // ✅ Explicit return value
  },
});
```

### Anti-Pattern 4: Using .filter() on Queries

`.filter()` scans the entire table. Always use indexes.

**❌ WRONG:**

```typescript
export const getActiveUsers = query({
  args: {},
  returns: v.array(v.object({ _id: v.id("users"), name: v.string() })),
  handler: async (ctx) => {
    // ❌ Full table scan!
    return await ctx.db
      .query("users")
      .filter((q) => q.eq(q.field("status"), "active"))
      .collect();
  },
});
```

**✅ CORRECT:**

```typescript
// Schema: .index("by_status", ["status"])

export const getActiveUsers = query({
  args: {},
  returns: v.array(v.object({ _id: v.id("users"), name: v.string() })),
  handler: async (ctx) => {
    // ✅ Uses index
    return await ctx.db
      .query("users")
      .withIndex("by_status", (q) => q.eq("status", "active"))
      .collect();
  },
});
```

### Anti-Pattern 5: Unbounded .collect()

Never collect without limits on potentially large tables.

**❌ WRONG:**

```typescript
export const getAllMessages = query({
  args: { channelId: v.id("channels") },
  returns: v.array(v.object({ content: v.string() })),
  handler: async (ctx, args) => {
    // ❌ Could return millions of records!
    return await ctx.db
      .query("messages")
      .withIndex("by_channel", (q) => q.eq("channelId", args.channelId))
      .collect();
  },
});
```

**✅ CORRECT:**

```typescript
export const getRecentMessages = query({
  args: { channelId: v.id("channels") },
  returns: v.array(v.object({ content: v.string() })),
  handler: async (ctx, args) => {
    // ✅ Bounded with take()
    return await ctx.db
      .query("messages")
      .withIndex("by_channel", (q) => q.eq("channelId", args.channelId))
      .order("desc")
      .take(50);
  },
});
```

### Anti-Pattern 6: .collect().length for Counts

Collecting just to count is wasteful.

**❌ WRONG:**

```typescript
export const getMessageCount = query({
  args: { channelId: v.id("channels") },
  returns: v.number(),
  handler: async (ctx, args) => {
    // ❌ Loads all messages just to count!
    const messages = await ctx.db
      .query("messages")
      .withIndex("by_channel", (q) => q.eq("channelId", args.channelId))
      .collect();
    return messages.length;
  },
});
```

**✅ CORRECT:**

```typescript
// Option 1: Bounded count with "99+" display
export const getMessageCount = query({
  args: { channelId: v.id("channels") },
  returns: v.string(),
  handler: async (ctx, args) => {
    const messages = await ctx.db
      .query("messages")
      .withIndex("by_channel", (q) => q.eq("channelId", args.channelId))
      .take(100);
    return messages.length === 100 ? "99+" : String(messages.length);
  },
});

// Option 2: Denormalized counter (best for high traffic)
// Maintain messageCount field in channels table
export const getMessageCount = query({
  args: { channelId: v.id("channels") },
  returns: v.number(),
  handler: async (ctx, args) => {
    const channel = await ctx.db.get(args.channelId);
    return channel?.messageCount ?? 0;
  },
});
```

### Anti-Pattern 7: N+1 Query Pattern

Loading related documents one by one.

**❌ WRONG:**

```typescript
export const getPostsWithAuthors = query({
  args: {},
  returns: v.array(
    v.object({
      post: v.object({ title: v.string() }),
      author: v.object({ name: v.string() }),
    })
  ),
  handler: async (ctx) => {
    const posts = await ctx.db.query("posts").take(10);

    // ❌ N additional queries!
    const postsWithAuthors = await Promise.all(
      posts.map(async (post) => ({
        post: { title: post.title },
        author: await ctx.db
          .get(post.authorId)
          .then((a) => ({ name: a!.name })),
      }))
    );

    return postsWithAuthors;
  },
});
```

**✅ CORRECT:**

```typescript
import { getAll } from "convex-helpers/server/relationships";

export const getPostsWithAuthors = query({
  args: {},
  returns: v.array(
    v.object({
      post: v.object({ title: v.string() }),
      author: v.union(v.object({ name: v.string() }), v.null()),
    })
  ),
  handler: async (ctx) => {
    const posts = await ctx.db.query("posts").take(10);

    // ✅ Batch fetch all authors
    const authorIds = [...new Set(posts.map((p) => p.authorId))];
    const authors = await getAll(ctx.db, authorIds);
    const authorMap = new Map(
      authors
        .filter((a): a is NonNullable<typeof a> => a !== null)
        .map((a) => [a._id, a])
    );

    return posts.map((post) => ({
      post: { title: post.title },
      author: authorMap.get(post.authorId)
        ? { name: authorMap.get(post.authorId)!.name }
        : null,
    }));
  },
});
```

### Anti-Pattern 8: Global Counter (Hot Spot)

Single document updates cause OCC conflicts under load.

**❌ WRONG:**

```typescript
export const incrementPageViews = mutation({
  args: {},
  returns: v.null(),
  handler: async (ctx) => {
    // ❌ Every request writes to same document!
    const stats = await ctx.db.query("globalStats").unique();
    await ctx.db.patch(stats!._id, { views: stats!.views + 1 });
    return null;
  },
});
```

**✅ CORRECT:**

```typescript
// Option 1: Sharding
export const incrementPageViews = mutation({
  args: {},
  returns: v.null(),
  handler: async (ctx) => {
    // ✅ Write to random shard
    const shardId = Math.floor(Math.random() * 10);
    await ctx.db.insert("viewShards", { shardId, delta: 1 });
    return null;
  },
});

// Read by aggregating shards
export const getPageViews = query({
  args: {},
  returns: v.number(),
  handler: async (ctx) => {
    const shards = await ctx.db.query("viewShards").collect();
    return shards.reduce((sum, s) => sum + s.delta, 0);
  },
});

// Option 2: Use Workpool to serialize
import { Workpool } from "@convex-dev/workpool";

const counterPool = new Workpool(components.workpool, { maxParallelism: 1 });

export const incrementPageViews = mutation({
  args: {},
  returns: v.null(),
  handler: async (ctx) => {
    await counterPool.enqueueMutation(ctx, internal.stats.doIncrement, {});
    return null;
  },
});
```

### Anti-Pattern 9: Using v.bigint() (Deprecated)

**❌ WRONG:**

```typescript
export default defineSchema({
  counters: defineTable({
    value: v.bigint(), // ❌ Deprecated!
  }),
});
```

**✅ CORRECT:**

```typescript
export default defineSchema({
  counters: defineTable({
    value: v.int64(), // ✅ Use v.int64()
  }),
});
```

### Anti-Pattern 10: Missing System Fields in Return Validators

**❌ WRONG:**

```typescript
export const getUser = query({
  args: { userId: v.id("users") },
  returns: v.object({
    // ❌ Missing _id and _creationTime!
    name: v.string(),
    email: v.string(),
  }),
  handler: async (ctx, args) => {
    return await ctx.db.get(args.userId); // Returns full doc including system fields
  },
});
```

**✅ CORRECT:**

```typescript
export const getUser = query({
  args: { userId: v.id("users") },
  returns: v.union(
    v.object({
      _id: v.id("users"), // ✅ Include system fields
      _creationTime: v.number(),
      name: v.string(),
      email: v.string(),
    }),
    v.null()
  ),
  handler: async (ctx, args) => {
    return await ctx.db.get(args.userId);
  },
});
```

### Anti-Pattern 11: Public Functions for Internal Logic

**❌ WRONG:**

```typescript
// ❌ This is callable by any client!
export const deleteUserData = mutation({
  args: { userId: v.id("users") },
  returns: v.null(),
  handler: async (ctx, args) => {
    // Dangerous operation exposed publicly
    await ctx.db.delete(args.userId);
    return null;
  },
});
```

**✅ CORRECT:**

```typescript
// Internal mutation - not callable by clients
export const deleteUserData = internalMutation({
  args: { userId: v.id("users") },
  returns: v.null(),
  handler: async (ctx, args) => {
    await ctx.db.delete(args.userId);
    return null;
  },
});

// Public mutation with auth check
export const requestAccountDeletion = mutation({
  args: {},
  returns: v.null(),
  handler: async (ctx) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    const user = await ctx.db
      .query("users")
      .withIndex("by_token", (q) =>
        q.eq("tokenIdentifier", identity.tokenIdentifier)
      )
      .unique();

    if (!user) throw new Error("User not found");

    // Schedule internal mutation
    await ctx.scheduler.runAfter(0, internal.users.deleteUserData, {
      userId: user._id,
    });

    return null;
  },
});
```

### Anti-Pattern 12: Non-Transactional Actions for Data Consistency

**❌ WRONG:**

```typescript
export const transferFunds = action({
  args: { from: v.id("accounts"), to: v.id("accounts"), amount: v.number() },
  returns: v.null(),
  handler: async (ctx, args) => {
    // ❌ These are separate transactions - could leave inconsistent state!
    await ctx.runMutation(internal.accounts.debit, {
      accountId: args.from,
      amount: args.amount,
    });

    // If this fails, money was debited but not credited!
    await ctx.runMutation(internal.accounts.credit, {
      accountId: args.to,
      amount: args.amount,
    });

    return null;
  },
});
```

**✅ CORRECT:**

```typescript
// Single atomic mutation
export const transferFunds = mutation({
  args: { from: v.id("accounts"), to: v.id("accounts"), amount: v.number() },
  returns: v.null(),
  handler: async (ctx, args) => {
    // ✅ All in one transaction - all succeed or all fail
    const fromAccount = await ctx.db.get(args.from);
    const toAccount = await ctx.db.get(args.to);

    if (!fromAccount || !toAccount) throw new Error("Account not found");
    if (fromAccount.balance < args.amount)
      throw new Error("Insufficient funds");

    await ctx.db.patch(args.from, {
      balance: fromAccount.balance - args.amount,
    });
    await ctx.db.patch(args.to, { balance: toAccount.balance + args.amount });

    return null;
  },
});
```

### Anti-Pattern 13: Redundant Indexes

**❌ WRONG:**

```typescript
export default defineSchema({
  messages: defineTable({
    channelId: v.id("channels"),
    authorId: v.id("users"),
    content: v.string(),
  })
    .index("by_channel", ["channelId"]) // ❌ Redundant!
    .index("by_channel_author", ["channelId", "authorId"]),
});
```

**✅ CORRECT:**

```typescript
export default defineSchema({
  messages: defineTable({
    channelId: v.id("channels"),
    authorId: v.id("users"),
    content: v.string(),
  })
    // ✅ Single compound index serves both query patterns
    .index("by_channel_author", ["channelId", "authorId"]),
});

// Use prefix matching for channel-only queries:
// .withIndex("by_channel_author", (q) => q.eq("channelId", id))
```

### Anti-Pattern 14: Using v.string() for IDs

**❌ WRONG:**

```typescript
export const getMessage = query({
  args: { messageId: v.string() }, // ❌ Should be v.id()
  returns: v.null(),
  handler: async (ctx, args) => {
    // Type error or runtime error
    return await ctx.db.get(args.messageId as Id<"messages">);
  },
});
```

**✅ CORRECT:**

```typescript
export const getMessage = query({
  args: { messageId: v.id("messages") }, // ✅ Proper ID type
  returns: v.union(
    v.object({
      _id: v.id("messages"),
      _creationTime: v.number(),
      content: v.string(),
    }),
    v.null()
  ),
  handler: async (ctx, args) => {
    return await ctx.db.get(args.messageId);
  },
});
```

### Anti-Pattern 15: Retry Without Backoff or Jitter

**❌ WRONG:**

```typescript
export const processWithRetry = internalAction({
  args: { jobId: v.id("jobs"), attempt: v.number() },
  returns: v.null(),
  handler: async (ctx, args) => {
    try {
      // Process...
    } catch (error) {
      if (args.attempt < 5) {
        // ❌ Fixed delay causes thundering herd!
        await ctx.scheduler.runAfter(5000, internal.jobs.processWithRetry, {
          jobId: args.jobId,
          attempt: args.attempt + 1,
        });
      }
    }
    return null;
  },
});
```

**✅ CORRECT:**

```typescript
export const processWithRetry = internalAction({
  args: { jobId: v.id("jobs"), attempt: v.number() },
  returns: v.null(),
  handler: async (ctx, args) => {
    try {
      // Process...
    } catch (error) {
      if (args.attempt < 5) {
        // ✅ Exponential backoff + jitter
        const baseDelay = Math.pow(2, args.attempt) * 1000;
        const jitter = Math.random() * 1000;
        await ctx.scheduler.runAfter(
          baseDelay + jitter,
          internal.jobs.processWithRetry,
          {
            jobId: args.jobId,
            attempt: args.attempt + 1,
          }
        );
      }
    }
    return null;
  },
});
```

## Agent Rules Summary

### Must Do

1. **Always include `returns` validator** on every function
2. **Always use indexes** instead of `.filter()`
3. **Always use `take(n)`** for potentially large queries
4. **Always use `v.id("table")`** for document ID arguments
5. **Always use `internalMutation`/`internalAction`** for sensitive operations
6. **Always handle errors** in actions and update status in database
7. **Always use exponential backoff with jitter** for retries

### Must Not Do

1. **Never call `fetch()`** in mutations
2. **Never access `ctx.db`** in actions
3. **Never use `.filter()`** on database queries
4. **Never use `.collect()`** without limits on large tables
5. **Never use `v.bigint()`** (deprecated, use `v.int64()`)
6. **Never use `any` type** (ESLint rule enforced)
7. **Never write to hot-spot documents** without sharding/workpool
8. **Never expose dangerous operations** as public functions
9. **Never rely on multiple mutations** for atomic operations

### Quick Checklist

Before submitting Convex code, verify:

- [ ] All functions have `returns` validators
- [ ] All queries use indexes (no `.filter()`)
- [ ] All `.collect()` calls are bounded with `.take(n)`
- [ ] All ID arguments use `v.id("tableName")`
- [ ] External API calls are in actions, not mutations
- [ ] Actions use `ctx.runQuery`/`ctx.runMutation` for DB access
- [ ] Sensitive operations use internal functions
- [ ] No `any` types in the codebase
- [ ] High-write documents use sharding or Workpool
- [ ] Retries use exponential backoff with jitter
