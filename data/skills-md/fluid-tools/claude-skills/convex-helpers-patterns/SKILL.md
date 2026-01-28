---
name: convex-helpers-patterns
description: "Guide for convex-helpers library patterns including Triggers, Row-Level Security (RLS), Relationship helpers, Custom Functions, Rate Limiting, and Workpool. Use when implementing automatic side effects, access control, relationship traversal, auth wrappers, or concurrency management. Activates for triggers setup, RLS implementation, custom function wrappers, or convex-helpers integration tasks."
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Convex Helpers Library Patterns

## Overview

The `convex-helpers` library provides battle-tested patterns for common Convex development needs. This skill covers Triggers (automatic side effects), Row-Level Security, Relationship helpers, Custom Functions, Rate Limiting, and Workpool for concurrency control.

## Installation

```bash
npm install convex-helpers @convex-dev/workpool
```

## TypeScript: NEVER Use `any` Type

**CRITICAL RULE:** This codebase has `@typescript-eslint/no-explicit-any` enabled. Using `any` will cause build failures.

## When to Use This Skill

Use this skill when:

- Implementing automatic side effects on document changes (Triggers)
- Adding declarative access control (Row-Level Security)
- Traversing relationships between documents
- Creating reusable authenticated function wrappers
- Implementing rate limiting
- Managing concurrent writes with Workpool
- Building custom function builders

## Key Patterns Overview

| Pattern                  | Use Case                                               |
| ------------------------ | ------------------------------------------------------ |
| **Triggers**             | Run code automatically on document changes             |
| **Row-Level Security**   | Declarative access control at the database layer       |
| **Relationship Helpers** | Simplified traversal of document relations             |
| **Custom Functions**     | Wrap queries/mutations with auth, logging, etc.        |
| **Rate Limiter**         | Application-level rate limiting                        |
| **Workpool**             | Fan-out parallel jobs, serialize conflicting mutations |
| **Migrations**           | Schema migrations with state tracking                  |

## Triggers (Automatic Side Effects)

Triggers run code automatically when documents change. They execute atomically within the same transaction as the mutation.

### Setting Up Triggers

```typescript
// convex/functions.ts
import { mutation as rawMutation } from "./_generated/server";
import { Triggers } from "convex-helpers/server/triggers";
import {
  customCtx,
  customMutation,
} from "convex-helpers/server/customFunctions";
import { DataModel } from "./_generated/dataModel";

const triggers = new Triggers<DataModel>();

// 1. Compute fullName on every user change
triggers.register("users", async (ctx, change) => {
  if (change.newDoc) {
    const fullName = `${change.newDoc.firstName} ${change.newDoc.lastName}`;
    if (change.newDoc.fullName !== fullName) {
      await ctx.db.patch(change.id, { fullName });
    }
  }
});

// 2. Keep denormalized count (careful: single doc = write contention)
triggers.register("users", async (ctx, change) => {
  const countDoc = (await ctx.db.query("userCount").unique())!;
  if (change.operation === "insert") {
    await ctx.db.patch(countDoc._id, { count: countDoc.count + 1 });
  } else if (change.operation === "delete") {
    await ctx.db.patch(countDoc._id, { count: countDoc.count - 1 });
  }
});

// 3. Cascading deletes
triggers.register("users", async (ctx, change) => {
  if (change.operation === "delete") {
    const messages = await ctx.db
      .query("messages")
      .withIndex("by_author", (q) => q.eq("authorId", change.id))
      .collect();
    for (const msg of messages) {
      await ctx.db.delete(msg._id);
    }
  }
});

// Export wrapped mutation that runs triggers
export const mutation = customMutation(rawMutation, customCtx(triggers.wrapDB));
```

### Trigger Change Object

```typescript
interface Change<Doc> {
  id: Id<TableName>;
  operation: "insert" | "update" | "delete";
  oldDoc: Doc | null; // null for inserts
  newDoc: Doc | null; // null for deletes
}
```

### Trigger Warnings

> **Warning:** Triggers run inside the same transaction as the mutation. Writing to hot-spot documents (e.g., global counters) inside triggers will cause OCC conflicts under load. Use sharding or Workpool for high-contention writes.

## Row-Level Security (RLS)

Declarative access control at the database layer. RLS wraps the database context to enforce rules on every read and write.

### Setting Up RLS

```typescript
// convex/functions.ts
import {
  Rules,
  wrapDatabaseReader,
  wrapDatabaseWriter,
} from "convex-helpers/server/rowLevelSecurity";
import {
  customCtx,
  customQuery,
  customMutation,
} from "convex-helpers/server/customFunctions";
import { query, mutation } from "./_generated/server";
import { QueryCtx } from "./_generated/server";
import { DataModel } from "./_generated/dataModel";

async function rlsRules(ctx: QueryCtx) {
  const identity = await ctx.auth.getUserIdentity();

  return {
    users: {
      read: async (_, user) => {
        // Unauthenticated users can only read users over 18
        if (!identity && user.age < 18) return false;
        return true;
      },
      insert: async () => true,
      modify: async (_, user) => {
        if (!identity) throw new Error("Must be authenticated");
        // Users can only modify their own record
        return user.tokenIdentifier === identity.tokenIdentifier;
      },
    },

    messages: {
      read: async (_, message) => {
        // Only read messages in conversations you're a member of
        const conversation = await ctx.db.get(message.conversationId);
        return conversation?.members.includes(identity?.subject ?? "") ?? false;
      },
      modify: async (_, message) => {
        // Only modify your own messages
        return message.authorId === identity?.subject;
      },
    },

    // Table with no restrictions
    publicPosts: {
      read: async () => true,
      insert: async () => true,
      modify: async () => true,
    },
  } satisfies Rules<QueryCtx, DataModel>;
}

// Wrap query/mutation with RLS
export const queryWithRLS = customQuery(
  query,
  customCtx(async (ctx) => ({
    db: wrapDatabaseReader(ctx, ctx.db, await rlsRules(ctx)),
  }))
);

export const mutationWithRLS = customMutation(
  mutation,
  customCtx(async (ctx) => ({
    db: wrapDatabaseWriter(ctx, ctx.db, await rlsRules(ctx)),
  }))
);
```

### Using RLS-Wrapped Functions

```typescript
// convex/messages.ts
import { queryWithRLS, mutationWithRLS } from "./functions";
import { v } from "convex/values";

// This query automatically enforces RLS rules
export const list = queryWithRLS({
  args: { conversationId: v.id("conversations") },
  returns: v.array(
    v.object({
      _id: v.id("messages"),
      _creationTime: v.number(),
      content: v.string(),
      authorId: v.string(),
    })
  ),
  handler: async (ctx, args) => {
    // RLS automatically filters out unauthorized messages
    return await ctx.db
      .query("messages")
      .withIndex("by_conversation", (q) =>
        q.eq("conversationId", args.conversationId)
      )
      .collect();
  },
});

// This mutation automatically enforces RLS rules
export const update = mutationWithRLS({
  args: { messageId: v.id("messages"), content: v.string() },
  returns: v.null(),
  handler: async (ctx, args) => {
    // RLS checks if user can modify this message
    await ctx.db.patch(args.messageId, { content: args.content });
    return null;
  },
});
```

## Relationship Helpers

Simplify traversing relationships without manual lookups.

### Available Helpers

```typescript
import {
  getAll,
  getOneFrom,
  getManyFrom,
  getManyVia,
} from "convex-helpers/server/relationships";
```

### One-to-One Relationship

```typescript
// Get single related document via back reference
const profile = await getOneFrom(
  ctx.db,
  "profiles", // target table
  "userId", // index field
  user._id // value to match
);
```

### One-to-Many (by ID array)

```typescript
// Load multiple documents by IDs
const users = await getAll(ctx.db, userIds);
// Returns array of documents in same order as IDs (null for missing)
```

### One-to-Many (via index)

```typescript
// Get all posts by author
const posts = await getManyFrom(
  ctx.db,
  "posts", // target table
  "by_authorId", // index name
  author._id // value to match
);
```

### Many-to-Many (via join table)

```typescript
// Schema:
// posts: { title: v.string() }
// categories: { name: v.string() }
// postCategories: { postId: v.id("posts"), categoryId: v.id("categories") }
//   .index("by_post", ["postId"])
//   .index("by_category", ["categoryId"])

// Get all categories for a post
const categories = await getManyVia(
  ctx.db,
  "postCategories", // join table
  "categoryId", // field pointing to target
  "by_post", // index to query join table
  post._id // source ID
);

// Get all posts in a category
const posts = await getManyVia(
  ctx.db,
  "postCategories",
  "postId",
  "by_category",
  category._id
);
```

### Complete Example

```typescript
// convex/posts.ts
import { query } from "./_generated/server";
import { v } from "convex/values";
import {
  getOneFrom,
  getManyFrom,
  getManyVia,
} from "convex-helpers/server/relationships";

export const getPostWithDetails = query({
  args: { postId: v.id("posts") },
  returns: v.union(
    v.object({
      post: v.object({
        _id: v.id("posts"),
        title: v.string(),
        body: v.string(),
      }),
      author: v.union(
        v.object({
          _id: v.id("users"),
          name: v.string(),
        }),
        v.null()
      ),
      comments: v.array(
        v.object({
          _id: v.id("comments"),
          body: v.string(),
        })
      ),
      categories: v.array(
        v.object({
          _id: v.id("categories"),
          name: v.string(),
        })
      ),
    }),
    v.null()
  ),
  handler: async (ctx, args) => {
    const post = await ctx.db.get(args.postId);
    if (!post) return null;

    const [author, comments, categories] = await Promise.all([
      // One-to-one: post -> author
      ctx.db.get(post.authorId),

      // One-to-many: post -> comments
      getManyFrom(ctx.db, "comments", "by_post", post._id),

      // Many-to-many: post -> categories (via join table)
      getManyVia(ctx.db, "postCategories", "categoryId", "by_post", post._id),
    ]);

    return {
      post: { _id: post._id, title: post.title, body: post.body },
      author: author ? { _id: author._id, name: author.name } : null,
      comments: comments.map((c) => ({ _id: c._id, body: c.body })),
      categories: categories
        .filter((c): c is NonNullable<typeof c> => c !== null)
        .map((c) => ({ _id: c._id, name: c.name })),
    };
  },
});
```

## Custom Functions (Auth Wrappers)

Create reusable function wrappers with built-in authentication.

### Basic Auth Wrapper

```typescript
// convex/functions.ts
import {
  customQuery,
  customMutation,
} from "convex-helpers/server/customFunctions";
import { query, mutation } from "./_generated/server";
import { Doc } from "./_generated/dataModel";

// Query that requires authentication
export const authedQuery = customQuery(query, {
  args: {},
  input: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    const user = await ctx.db
      .query("users")
      .withIndex("by_token", (q) =>
        q.eq("tokenIdentifier", identity.tokenIdentifier)
      )
      .unique();

    if (!user) throw new Error("User not found");

    return { ctx: { ...ctx, user }, args };
  },
});

// Mutation that requires authentication
export const authedMutation = customMutation(mutation, {
  args: {},
  input: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    const user = await ctx.db
      .query("users")
      .withIndex("by_token", (q) =>
        q.eq("tokenIdentifier", identity.tokenIdentifier)
      )
      .unique();

    if (!user) throw new Error("User not found");

    return { ctx: { ...ctx, user }, args };
  },
});
```

### Using Authed Functions

```typescript
// convex/profile.ts
import { authedQuery, authedMutation } from "./functions";
import { v } from "convex/values";

// ctx.user is guaranteed to exist
export const getMyProfile = authedQuery({
  args: {},
  returns: v.object({
    _id: v.id("users"),
    name: v.string(),
    email: v.string(),
  }),
  handler: async (ctx) => {
    // ctx.user is typed and guaranteed to exist!
    return {
      _id: ctx.user._id,
      name: ctx.user.name,
      email: ctx.user.email,
    };
  },
});

export const updateMyName = authedMutation({
  args: { name: v.string() },
  returns: v.null(),
  handler: async (ctx, args) => {
    await ctx.db.patch(ctx.user._id, { name: args.name });
    return null;
  },
});
```

### Role-Based Auth Wrapper

```typescript
// convex/functions.ts
export const adminQuery = customQuery(query, {
  args: {},
  input: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    const user = await ctx.db
      .query("users")
      .withIndex("by_token", (q) =>
        q.eq("tokenIdentifier", identity.tokenIdentifier)
      )
      .unique();

    if (!user) throw new Error("User not found");
    if (user.role !== "admin") throw new Error("Admin access required");

    return { ctx: { ...ctx, user }, args };
  },
});

// Usage
export const listAllUsers = adminQuery({
  args: {},
  returns: v.array(
    v.object({
      _id: v.id("users"),
      name: v.string(),
      role: v.string(),
    })
  ),
  handler: async (ctx) => {
    const users = await ctx.db.query("users").collect();
    return users.map((u) => ({ _id: u._id, name: u.name, role: u.role }));
  },
});
```

## Workpool (Concurrency Control)

Workpool manages concurrent execution with parallelism limits, useful for:

- Serializing writes to avoid OCC conflicts
- Fan-out parallel processing with limits
- Rate-limited external API calls

### Setting Up Workpool

First, install and configure the Workpool component:

```typescript
// convex/convex.config.ts
import { defineApp } from "convex/server";
import workpool from "@convex-dev/workpool/convex.config";

const app = defineApp();
app.use(workpool, { name: "workpool" });

export default app;
```

### Using Workpool

```typescript
// convex/counters.ts
import { Workpool } from "@convex-dev/workpool";
import { components, internal } from "./_generated/api";
import { mutation, internalMutation } from "./_generated/server";
import { v } from "convex/values";

// Create workpool with parallelism limit
const counterPool = new Workpool(components.workpool, {
  maxParallelism: 1, // Serialize all counter updates
});

// Public mutation enqueues work
export const incrementCounter = mutation({
  args: {},
  returns: v.null(),
  handler: async (ctx) => {
    await counterPool.enqueueMutation(ctx, internal.counters.doIncrement, {});
    return null;
  },
});

// Internal mutation does the actual work
export const doIncrement = internalMutation({
  args: {},
  returns: v.null(),
  handler: async (ctx) => {
    const counter = await ctx.db.query("counters").unique();
    if (counter) {
      await ctx.db.patch(counter._id, { count: counter.count + 1 });
    }
    return null;
  },
});
```

### Parallel Processing with Limits

```typescript
// Process many items with limited concurrency
const processingPool = new Workpool(components.workpool, {
  maxParallelism: 5, // Process 5 items at a time
});

export const processAll = mutation({
  args: { itemIds: v.array(v.id("items")) },
  returns: v.null(),
  handler: async (ctx, args) => {
    for (const itemId of args.itemIds) {
      await processingPool.enqueueAction(ctx, internal.items.processOne, {
        itemId,
      });
    }
    return null;
  },
});
```

## Rate Limiting

Application-level rate limiting using convex-helpers.

### Setting Up Rate Limiter

```typescript
// convex/rateLimit.ts
import { RateLimiter } from "convex-helpers/server/rateLimit";
import { components } from "./_generated/api";

export const rateLimiter = new RateLimiter(components.rateLimit, {
  // Global rate limit
  global: {
    kind: "token bucket",
    rate: 100, // 100 requests
    period: 60000, // per minute
  },

  // Per-user rate limit
  perUser: {
    kind: "token bucket",
    rate: 10,
    period: 60000,
  },
});
```

### Using Rate Limiter

```typescript
// convex/api.ts
import { mutation } from "./_generated/server";
import { v } from "convex/values";
import { rateLimiter } from "./rateLimit";

export const createPost = mutation({
  args: { title: v.string(), body: v.string() },
  returns: v.union(
    v.id("posts"),
    v.object({
      error: v.string(),
      retryAfter: v.number(),
    })
  ),
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    // Check rate limit
    const { ok, retryAfter } = await rateLimiter.limit(ctx, "perUser", {
      key: identity.subject,
    });

    if (!ok) {
      // Add jitter to prevent thundering herd
      const jitter = Math.random() * 1000;
      return {
        error: "Rate limit exceeded",
        retryAfter: retryAfter + jitter,
      };
    }

    const postId = await ctx.db.insert("posts", {
      title: args.title,
      body: args.body,
      authorId: identity.subject,
    });

    return postId;
  },
});
```

## Combining Patterns

### Triggers + RLS + Custom Functions

```typescript
// convex/functions.ts
import {
  mutation as rawMutation,
  query as rawQuery,
} from "./_generated/server";
import { Triggers } from "convex-helpers/server/triggers";
import {
  wrapDatabaseReader,
  wrapDatabaseWriter,
} from "convex-helpers/server/rowLevelSecurity";
import {
  customCtx,
  customQuery,
  customMutation,
} from "convex-helpers/server/customFunctions";

// Set up triggers
const triggers = new Triggers<DataModel>();
triggers.register("posts", async (ctx, change) => {
  if (change.operation === "insert") {
    // Update author's post count
    const author = await ctx.db.get(change.newDoc!.authorId);
    if (author) {
      await ctx.db.patch(author._id, {
        postCount: (author.postCount ?? 0) + 1,
      });
    }
  }
});

// Set up RLS rules
async function rlsRules(ctx: QueryCtx) {
  const identity = await ctx.auth.getUserIdentity();
  return {
    posts: {
      read: async () => true,
      modify: async (_, post) => post.authorId === identity?.subject,
    },
  };
}

// Combine everything into authenticated, RLS-protected, trigger-enabled functions
export const authedMutation = customMutation(rawMutation, {
  args: {},
  input: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    const user = await ctx.db
      .query("users")
      .withIndex("by_token", (q) =>
        q.eq("tokenIdentifier", identity.tokenIdentifier)
      )
      .unique();

    if (!user) throw new Error("User not found");

    // Wrap DB with triggers and RLS
    const wrappedDb = wrapDatabaseWriter(
      ctx,
      triggers.wrapDB(ctx).db,
      await rlsRules(ctx)
    );

    return { ctx: { ...ctx, user, db: wrappedDb }, args };
  },
});
```

## Common Pitfalls

### Pitfall 1: Triggers Causing OCC Conflicts

**❌ WRONG:**

```typescript
// This trigger updates a single global counter - will cause OCC under load
triggers.register("posts", async (ctx, change) => {
  if (change.operation === "insert") {
    const stats = await ctx.db.query("globalStats").unique();
    await ctx.db.patch(stats!._id, { postCount: stats!.postCount + 1 });
  }
});
```

**✅ CORRECT:**

```typescript
// Use sharding or Workpool for high-contention updates
triggers.register("posts", async (ctx, change) => {
  if (change.operation === "insert") {
    const shardId = Math.floor(Math.random() * 10);
    await ctx.db.insert("postCountShards", { shardId, delta: 1 });
  }
});
```

### Pitfall 2: RLS Rules Missing Tables

**❌ WRONG:**

```typescript
// Missing rules for some tables - they'll be unprotected!
async function rlsRules(ctx: QueryCtx) {
  return {
    users: { read: async () => true, modify: async () => false },
    // Missing posts, messages, etc.!
  };
}
```

**✅ CORRECT:**

```typescript
// Define rules for ALL tables
async function rlsRules(ctx: QueryCtx) {
  return {
    users: { read: async () => true, modify: async () => false },
    posts: { read: async () => true, modify: async () => true },
    messages: { read: async () => true, modify: async () => true },
    // ... all other tables
  } satisfies Rules<QueryCtx, DataModel>;
}
```

## Quick Reference

### Import Patterns

```typescript
// Triggers
import { Triggers } from "convex-helpers/server/triggers";

// RLS
import {
  Rules,
  wrapDatabaseReader,
  wrapDatabaseWriter,
} from "convex-helpers/server/rowLevelSecurity";

// Custom Functions
import {
  customCtx,
  customQuery,
  customMutation,
} from "convex-helpers/server/customFunctions";

// Relationships
import {
  getAll,
  getOneFrom,
  getManyFrom,
  getManyVia,
} from "convex-helpers/server/relationships";

// Workpool
import { Workpool } from "@convex-dev/workpool";

// Rate Limiter
import { RateLimiter } from "convex-helpers/server/rateLimit";
```
