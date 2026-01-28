---
name: convex-performance-patterns
description: "Guide for Convex performance optimization including denormalization, index design, avoiding N+1 queries, OCC (Optimistic Concurrency Control), and handling hot spots. Use when optimizing query performance, designing data models, handling high-contention writes, or troubleshooting OCC errors. Activates for performance issues, index optimization, denormalization patterns, or concurrency control tasks."
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Convex Performance Patterns

## Overview

Convex is designed for performance, but requires specific patterns to achieve optimal results. This skill covers denormalization strategies, index design, avoiding common performance pitfalls, and handling concurrency with OCC (Optimistic Concurrency Control).

## TypeScript: NEVER Use `any` Type

**CRITICAL RULE:** This codebase has `@typescript-eslint/no-explicit-any` enabled. Using `any` will cause build failures.

## When to Use This Skill

Use this skill when:

- Queries are running slowly or causing too many re-renders
- Designing indexes for efficient data access
- Avoiding N+1 query patterns
- Handling high-contention writes (OCC errors)
- Denormalizing data to improve read performance
- Optimizing reactive queries
- Working with counters or aggregations

## Core Performance Principles

### Principle 1: Queries Should Be O(log n), Not O(n)

Convex queries should use indexes for efficient data retrieval. If you're scanning entire tables, you're doing it wrong.

### Principle 2: Denormalize Aggressively

Convex has no joins. Embed related data or maintain lookup tables.

### Principle 3: Minimize Document Reads

Each document read in a query creates a dependency. Fewer reads = fewer re-renders.

### Principle 4: Avoid Hot Spots

Single documents that are frequently written will cause OCC conflicts.

## Denormalization Patterns

### Pattern 1: Embed Related Data

**❌ BAD: N+1 queries**

```typescript
export const getTeamWithMembers = query({
  args: { teamId: v.id("teams") },
  returns: v.null(),
  handler: async (ctx, args) => {
    const team = await ctx.db.get(args.teamId);
    if (!team) return null;

    // ❌ This triggers N additional reads, each causing re-renders
    const members = await Promise.all(
      team.memberIds.map((id) => ctx.db.get(id))
    );
    return { team, members };
  },
});
```

**✅ GOOD: Denormalize member info into team**

```typescript
// Schema: teams.members: v.array(v.object({ userId: v.id("users"), name: v.string(), avatar: v.string() }))
export const getTeamWithMembers = query({
  args: { teamId: v.id("teams") },
  returns: v.union(
    v.object({
      _id: v.id("teams"),
      _creationTime: v.number(),
      name: v.string(),
      members: v.array(
        v.object({
          userId: v.id("users"),
          name: v.string(),
          avatar: v.string(),
        })
      ),
    }),
    v.null()
  ),
  handler: async (ctx, args) => {
    return await ctx.db.get(args.teamId); // Single read, includes members
  },
});
```

### Pattern 2: Denormalized Counts

Never `.collect()` just to count.

**❌ BAD: Unbounded read**

```typescript
const messages = await ctx.db
  .query("messages")
  .withIndex("by_channel", (q) => q.eq("channelId", channelId))
  .collect();
const count = messages.length;
```

**✅ GOOD: Show "99+" pattern**

```typescript
const messages = await ctx.db
  .query("messages")
  .withIndex("by_channel", (q) => q.eq("channelId", channelId))
  .take(100);
const count = messages.length === 100 ? "99+" : String(messages.length);
```

**✅ BEST: Denormalized counter table**

```typescript
// Maintain a separate "channelStats" table with messageCount field
// Update it in the same mutation that inserts messages

export const getMessageCount = query({
  args: { channelId: v.id("channels") },
  returns: v.number(),
  handler: async (ctx, args) => {
    const stats = await ctx.db
      .query("channelStats")
      .withIndex("by_channel", (q) => q.eq("channelId", args.channelId))
      .unique();
    return stats?.messageCount ?? 0;
  },
});

export const addMessage = mutation({
  args: { channelId: v.id("channels"), content: v.string() },
  returns: v.id("messages"),
  handler: async (ctx, args) => {
    const messageId = await ctx.db.insert("messages", {
      channelId: args.channelId,
      content: args.content,
    });

    // Update denormalized count
    const stats = await ctx.db
      .query("channelStats")
      .withIndex("by_channel", (q) => q.eq("channelId", args.channelId))
      .unique();

    if (stats) {
      await ctx.db.patch(stats._id, { messageCount: stats.messageCount + 1 });
    } else {
      await ctx.db.insert("channelStats", {
        channelId: args.channelId,
        messageCount: 1,
      });
    }

    return messageId;
  },
});
```

### Pattern 3: Denormalized Boolean Fields

When you need to filter by computed conditions, denormalize the result:

```typescript
// Schema
export default defineSchema({
  posts: defineTable({
    body: v.string(),
    tags: v.array(v.string()),
    // Denormalized: computed on write
    isImportant: v.boolean(),
  }).index("by_important", ["isImportant"]),
});

// Mutation: compute on write
export const createPost = mutation({
  args: { body: v.string(), tags: v.array(v.string()) },
  returns: v.id("posts"),
  handler: async (ctx, args) => {
    return await ctx.db.insert("posts", {
      body: args.body,
      tags: args.tags,
      isImportant: args.tags.includes("important"), // Denormalize!
    });
  },
});

// Query: O(log n) lookup
export const getImportantPosts = query({
  args: {},
  returns: v.array(
    v.object({
      _id: v.id("posts"),
      _creationTime: v.number(),
      body: v.string(),
      isImportant: v.boolean(),
    })
  ),
  handler: async (ctx) => {
    return await ctx.db
      .query("posts")
      .withIndex("by_important", (q) => q.eq("isImportant", true))
      .collect();
  },
});
```

## Index Design

### Compound Index Strategy

Indexes are prefix-searchable. Design compound indexes to serve multiple queries.

```typescript
// Schema
export default defineSchema({
  messages: defineTable({
    channelId: v.id("channels"),
    authorId: v.id("users"),
    content: v.string(),
    isDeleted: v.boolean(),
  })
    // ✅ This single index serves THREE query patterns:
    // 1. All messages in channel: .eq("channelId", id)
    // 2. Messages by author in channel: .eq("channelId", id).eq("authorId", id)
    // 3. Non-deleted messages by author: .eq("channelId", id).eq("authorId", id).eq("isDeleted", false)
    .index("by_channel_author_deleted", ["channelId", "authorId", "isDeleted"]),
});

// ❌ REDUNDANT: Don't create by_channel if you have by_channel_author_deleted
// The compound index can serve channel-only queries by partial prefix match
```

### Index Naming Convention

Include all fields: `by_field1_and_field2_and_field3`

```typescript
.index("by_channel", ["channelId"])
.index("by_channel_and_author", ["channelId", "authorId"])
.index("by_user_and_status_and_createdAt", ["userId", "status", "createdAt"])
```

### Avoiding Filter

Never use `.filter()`. Use indexes or filter in TypeScript.

**❌ BAD: filter() scans entire table**

```typescript
const activeUsers = await ctx.db
  .query("users")
  .filter((q) => q.eq(q.field("status"), "active"))
  .collect();
```

**✅ GOOD: Index-based**

```typescript
const activeUsers = await ctx.db
  .query("users")
  .withIndex("by_status", (q) => q.eq("status", "active"))
  .collect();
```

**✅ ACCEPTABLE: Small dataset, complex filter**

```typescript
// Only if the dataset is bounded!
const allUsers = await ctx.db.query("users").take(1000);
const filtered = allUsers.filter(
  (u) => u.status === "active" && u.role !== "bot"
);
```

## Concurrency & OCC (Optimistic Concurrency Control)

Convex uses OCC for transactions. When two mutations read and write the same document simultaneously, one will be retried automatically.

### Problem: Hot Spots

**❌ BAD: Counter that's always conflicting**

```typescript
export const incrementCounter = mutation({
  args: {},
  returns: v.null(),
  handler: async (ctx) => {
    const counter = await ctx.db.query("counters").unique();
    await ctx.db.patch(counter!._id, { count: counter!.count + 1 });
    return null;
  },
});

// If 100 users click at once, 99 will retry → cascading OCC errors
```

### Solution 1: Sharding

Split hot data across multiple documents:

```typescript
// Schema: counterShards table
export default defineSchema({
  counterShards: defineTable({
    shardId: v.number(),
    delta: v.number(),
  }).index("by_shard", ["shardId"]),
});

// On write: pick random shard
export const incrementCounter = mutation({
  args: {},
  returns: v.null(),
  handler: async (ctx) => {
    const shardId = Math.floor(Math.random() * 10);
    await ctx.db.insert("counterShards", { shardId, delta: 1 });
    return null;
  },
});

// On read: sum all shards
export const getCount = query({
  args: {},
  returns: v.number(),
  handler: async (ctx) => {
    const shards = await ctx.db.query("counterShards").collect();
    return shards.reduce((sum, s) => sum + s.delta, 0);
  },
});
```

### Solution 2: Workpool (convex-helpers)

Serialize writes to avoid conflicts:

```typescript
import { Workpool } from "@convex-dev/workpool";
import { components } from "./_generated/api";

const counterPool = new Workpool(components.counterWorkpool, {
  maxParallelism: 1, // Serialize all counter updates
});

export const incrementCounter = mutation({
  args: {},
  returns: v.null(),
  handler: async (ctx) => {
    await counterPool.enqueueMutation(ctx, internal.counters.doIncrement, {});
    return null;
  },
});
```

### Solution 3: Aggregate Component

For counts/sums, use the Convex Aggregate component:

```typescript
import { Aggregate } from "@convex-dev/aggregate";

// Atomic increments without OCC conflicts
await aggregate.insert(ctx, "pageViews", 1);
const total = await aggregate.sum(ctx);
```

### When to Use Workpool vs Scheduler

- Use `ctx.scheduler` for one-off background jobs with no coordination needs.
- Use Workpool when you need concurrency control, fan-out parallelism, or serialization to avoid OCC conflicts.

## Transaction Boundaries

### Consolidate Reads

Multiple `ctx.runQuery` calls in an action are NOT transactional:

**❌ BAD: Race condition between queries**

```typescript
export const processTeam = action({
  args: { teamId: v.id("teams") },
  returns: v.null(),
  handler: async (ctx, args) => {
    const team = await ctx.runQuery(internal.teams.getTeam, {
      teamId: args.teamId,
    });
    const owner = await ctx.runQuery(internal.users.getUser, {
      userId: team.ownerId,
    });
    // Owner might have changed between the two queries!
    return null;
  },
});
```

**✅ GOOD: Single transactional query**

```typescript
export const processTeam = action({
  args: { teamId: v.id("teams") },
  returns: v.null(),
  handler: async (ctx, args) => {
    const teamWithOwner = await ctx.runQuery(internal.teams.getTeamWithOwner, {
      teamId: args.teamId,
    });
    // Team and owner fetched atomically
    return null;
  },
});
```

### Batch Writes

Multiple mutations in an action are NOT atomic:

**❌ BAD: Partial failure possible**

```typescript
export const createUsers = action({
  args: { users: v.array(v.object({ name: v.string() })) },
  returns: v.null(),
  handler: async (ctx, args) => {
    for (const user of args.users) {
      await ctx.runMutation(internal.users.insert, { user });
    }
    // If third insert fails, first two still exist!
    return null;
  },
});
```

**✅ GOOD: Single transaction**

```typescript
export const createUsers = mutation({
  args: { users: v.array(v.object({ name: v.string() })) },
  returns: v.array(v.id("users")),
  handler: async (ctx, args) => {
    const ids: Id<"users">[] = [];
    for (const user of args.users) {
      ids.push(
        await ctx.db.insert("users", { name: user.name, createdAt: Date.now() })
      );
    }
    return ids; // All succeed or all fail together
  },
});
```

## Query Optimization

### Use take() with Reasonable Limits

```typescript
// ❌ BAD: Unbounded collect
const allMessages = await ctx.db
  .query("messages")
  .withIndex("by_channel", (q) => q.eq("channelId", channelId))
  .collect();

// ✅ GOOD: Bounded with take()
const recentMessages = await ctx.db
  .query("messages")
  .withIndex("by_channel", (q) => q.eq("channelId", channelId))
  .order("desc")
  .take(50);
```

### Parallel Data Fetching

```typescript
export const getDashboard = query({
  args: { userId: v.id("users") },
  returns: v.object({
    user: v.object({ _id: v.id("users"), name: v.string() }),
    stats: v.object({ messageCount: v.number(), channelCount: v.number() }),
  }),
  handler: async (ctx, args) => {
    // Fetch in parallel - both queries run simultaneously
    const [user, stats] = await Promise.all([
      ctx.db.get(args.userId),
      ctx.db
        .query("userStats")
        .withIndex("by_user", (q) => q.eq("userId", args.userId))
        .unique(),
    ]);

    if (!user) throw new Error("User not found");

    return {
      user: { _id: user._id, name: user.name },
      stats: stats ?? { messageCount: 0, channelCount: 0 },
    };
  },
});
```

### Avoid Collecting When You Need One

```typescript
// ❌ BAD: Collecting then taking first
const users = await ctx.db
  .query("users")
  .withIndex("by_email", (q) => q.eq("email", email))
  .collect();
const user = users[0];

// ✅ GOOD: Use .first() or .unique()
const user = await ctx.db
  .query("users")
  .withIndex("by_email", (q) => q.eq("email", email))
  .first();

// For exactly-one semantics (throws if multiple)
const user = await ctx.db
  .query("users")
  .withIndex("by_email", (q) => q.eq("email", email))
  .unique();
```

## Common Pitfalls

### Pitfall 1: N+1 Query Pattern

**❌ WRONG:**

```typescript
const posts = await ctx.db.query("posts").take(10);
const postsWithAuthors = await Promise.all(
  posts.map(async (post) => ({
    ...post,
    author: await ctx.db.get(post.authorId), // N additional queries!
  }))
);
```

**✅ CORRECT: Denormalize or batch**

```typescript
// Option 1: Denormalize author info into posts
// Schema: posts.author: v.object({ id: v.id("users"), name: v.string() })

// Option 2: Batch fetch with getAll (from convex-helpers)
import { getAll } from "convex-helpers/server/relationships";

const posts = await ctx.db.query("posts").take(10);
const authorIds = [...new Set(posts.map((p) => p.authorId))];
const authors = await getAll(ctx.db, authorIds);
const authorMap = new Map(authors.map((a) => [a._id, a]));

const postsWithAuthors = posts.map((post) => ({
  ...post,
  author: authorMap.get(post.authorId),
}));
```

### Pitfall 2: Unbounded Queries Without Indexes

**❌ WRONG:**

```typescript
// Full table scan!
const allItems = await ctx.db.query("items").collect();
```

**✅ CORRECT:**

```typescript
// With pagination or limits
const items = await ctx.db.query("items").take(100);

// Or with index if filtering
const items = await ctx.db
  .query("items")
  .withIndex("by_status", (q) => q.eq("status", "active"))
  .take(100);
```

### Pitfall 3: Single Document Hot Spot

**❌ WRONG:**

```typescript
// Global counter - constant OCC conflicts under load
const global = await ctx.db.query("globals").unique();
await ctx.db.patch(global!._id, { viewCount: global!.viewCount + 1 });
```

**✅ CORRECT: Use sharding or aggregates**

```typescript
// Sharded counter
const shardId = Math.floor(Math.random() * 10);
await ctx.db.insert("viewShards", { shardId, delta: 1, timestamp: Date.now() });

// Periodic aggregation job consolidates shards
```

## Performance Checklist

Before deploying, verify:

- [ ] All queries use indexes (no `.filter()` on database)
- [ ] No unbounded `.collect()` calls without `take(n)`
- [ ] Related data is denormalized to avoid N+1 patterns
- [ ] High-write documents use sharding or Workpool
- [ ] Compound indexes serve multiple query patterns
- [ ] No redundant indexes (compound indexes cover prefixes)
- [ ] Counts use denormalized counters, not `.collect().length`
- [ ] Mutations batch related writes in single transactions

## Quick Reference

### Query Patterns

| Pattern       | Method                         | Use Case                                  |
| ------------- | ------------------------------ | ----------------------------------------- |
| Get by ID     | `ctx.db.get(id)`               | Single document lookup                    |
| Get multiple  | `ctx.db.query().collect()`     | Multiple documents (use `take(n)`)        |
| Get first     | `ctx.db.query().first()`       | First matching document                   |
| Get unique    | `ctx.db.query().unique()`      | Exactly one document (throws if multiple) |
| Indexed query | `.withIndex("name", q => ...)` | Efficient filtered query                  |

### Index Usage

```typescript
// Equality on all fields
.withIndex("by_a_b_c", (q) => q.eq("a", 1).eq("b", 2).eq("c", 3))

// Prefix match (uses first N fields)
.withIndex("by_a_b_c", (q) => q.eq("a", 1).eq("b", 2))

// Range on last field
.withIndex("by_a_b_c", (q) => q.eq("a", 1).eq("b", 2).gt("c", 0))

// Cannot skip fields in the middle!
// ❌ .withIndex("by_a_b_c", (q) => q.eq("a", 1).eq("c", 3))
```
