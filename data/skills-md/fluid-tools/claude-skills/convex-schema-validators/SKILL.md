---
name: convex-schema-validators
description: "Guide for Convex schema design, validators, and TypeScript types. Use when defining database schemas, creating validators for function arguments/returns, working with document types, or ensuring type safety. Activates for schema.ts creation, validator usage, Id/Doc type handling, or TypeScript integration tasks."
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Convex Schema & Validators Guide

## Overview

Convex uses a schema-first approach with built-in validators for type safety. This skill covers schema design, validator patterns, TypeScript type integration, and best practices for type-safe Convex development.

## TypeScript: NEVER Use `any` Type

**CRITICAL RULE:** This codebase has `@typescript-eslint/no-explicit-any` enabled. Using `any` will cause build failures.

**❌ WRONG:**

```typescript
const data: any = await ctx.db.get(id);
function process(items: any[]) { ... }
```

**✅ CORRECT:**

```typescript
const data: Doc<"users"> | null = await ctx.db.get(id);
function process(items: Doc<"items">[]) { ... }
```

## When to Use This Skill

Use this skill when:

- Creating or modifying `convex/schema.ts`
- Defining validators for function arguments and returns
- Working with document IDs and types
- Setting up indexes for efficient queries
- Handling optional fields and unions
- Integrating Convex types with TypeScript

## Schema Definition

### Basic Schema Structure

```typescript
// convex/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  users: defineTable({
    name: v.string(),
    email: v.string(),
    avatarUrl: v.optional(v.string()),
    role: v.union(v.literal("admin"), v.literal("user")),
    createdAt: v.number(),
  })
    .index("by_email", ["email"])
    .index("by_role", ["role"]),

  messages: defineTable({
    authorId: v.id("users"),
    channelId: v.id("channels"),
    content: v.string(),
    isDeleted: v.boolean(),
  })
    .index("by_channel", ["channelId"])
    .index("by_author", ["authorId"])
    .index("by_channel_author", ["channelId", "authorId"]),

  channels: defineTable({
    name: v.string(),
    members: v.array(v.id("users")),
    isPrivate: v.boolean(),
  }),
});
```

### Table Definition Patterns

```typescript
// defineTable takes a validator object
defineTable({
  field1: v.string(),
  field2: v.number(),
});

// Chain indexes after defineTable
defineTable({
  userId: v.id("users"),
  status: v.string(),
})
  .index("by_user", ["userId"])
  .index("by_status", ["status"])
  .index("by_user_status", ["userId", "status"]);

// Search indexes for full-text search
defineTable({
  title: v.string(),
  body: v.string(),
}).searchIndex("search_body", {
  searchField: "body",
  filterFields: ["title"],
});
```

## Validator Reference

### Primitive Validators

```typescript
import { v } from "convex/values";

v.string(); // string
v.number(); // number (float64)
v.boolean(); // boolean
v.null(); // null literal
v.int64(); // 64-bit integer (NOT v.bigint() - deprecated!)
v.bytes(); // ArrayBuffer
```

### Complex Validators

```typescript
// Document IDs
v.id("tableName"); // Id<"tableName">

// Arrays
v.array(v.string()); // string[]
v.array(v.id("users")); // Id<"users">[]
v.array(v.object({ x: v.number() })); // { x: number }[]

// Objects
v.object({
  name: v.string(),
  age: v.number(),
  email: v.optional(v.string()),
});

// Records (string keys, typed values)
v.record(v.string(), v.number()); // Record<string, number>
v.record(v.id("users"), v.string()); // Record<Id<"users">, string>

// Unions (OR types)
v.union(v.string(), v.null()); // string | null
v.union(v.literal("a"), v.literal("b")); // "a" | "b"

// Optionals (field may be missing)
v.optional(v.string()); // string | undefined

// Literals (exact values)
v.literal("active"); // "active" literal type
v.literal(42); // 42 literal type
v.literal(true); // true literal type

// Any (escape hatch - avoid if possible)
v.any(); // any (use sparingly!)
```

### Common Validator Patterns

```typescript
// Nullable field (can be null)
status: v.union(v.string(), v.null());

// Optional field (may not exist)
nickname: v.optional(v.string());

// Optional AND nullable
deletedAt: v.optional(v.union(v.number(), v.null()));

// Enum-like unions
role: v.union(v.literal("admin"), v.literal("moderator"), v.literal("user"));

// Nested objects
settings: v.object({
  theme: v.union(v.literal("light"), v.literal("dark")),
  notifications: v.object({
    email: v.boolean(),
    push: v.boolean(),
  }),
});

// Array of objects
members: v.array(
  v.object({
    userId: v.id("users"),
    role: v.string(),
    joinedAt: v.number(),
  })
);
```

## Function Validators

### CRITICAL: Every Function MUST Have `returns` Validator

```typescript
// ❌ WRONG: Missing returns
export const foo = mutation({
  args: {},
  handler: async (ctx) => {
    // implicitly returns undefined
  },
});

// ✅ CORRECT: Explicit v.null()
export const foo = mutation({
  args: {},
  returns: v.null(),
  handler: async (ctx) => {
    return null;
  },
});
```

### Query with Validators

```typescript
import { query } from "./_generated/server";
import { v } from "convex/values";

export const getUser = query({
  args: {
    userId: v.id("users"),
  },
  returns: v.union(
    v.object({
      _id: v.id("users"),
      _creationTime: v.number(),
      name: v.string(),
      email: v.string(),
      role: v.string(),
    }),
    v.null()
  ),
  handler: async (ctx, args) => {
    return await ctx.db.get(args.userId);
  },
});
```

### Mutation with Validators

```typescript
import { mutation } from "./_generated/server";
import { v } from "convex/values";

export const createUser = mutation({
  args: {
    name: v.string(),
    email: v.string(),
    role: v.optional(v.union(v.literal("admin"), v.literal("user"))),
  },
  returns: v.id("users"),
  handler: async (ctx, args) => {
    return await ctx.db.insert("users", {
      name: args.name,
      email: args.email,
      role: args.role ?? "user",
      createdAt: Date.now(),
    });
  },
});
```

### Action with Validators

```typescript
import { action } from "./_generated/server";
import { v } from "convex/values";

export const processImage = action({
  args: {
    imageUrl: v.string(),
    options: v.object({
      width: v.number(),
      height: v.number(),
      format: v.union(v.literal("png"), v.literal("jpeg")),
    }),
  },
  returns: v.object({
    processedUrl: v.string(),
    size: v.number(),
  }),
  handler: async (ctx, args) => {
    // Process image...
    return {
      processedUrl: "https://...",
      size: 1024,
    };
  },
});
```

## TypeScript Types

### Importing Types

```typescript
import { Doc, Id } from "./_generated/dataModel";

// Document type for a table
type User = Doc<"users">;
// {
//   _id: Id<"users">;
//   _creationTime: number;
//   name: string;
//   email: string;
//   ...
// }

// ID type for a table
type UserId = Id<"users">;
```

### Using Types in Code

```typescript
import { Doc, Id } from "./_generated/dataModel";

// Function parameter types
async function getUserName(
  ctx: QueryCtx,
  userId: Id<"users">
): Promise<string | null> {
  const user = await ctx.db.get(userId);
  return user?.name ?? null;
}

// Variable types
const users: Doc<"users">[] = await ctx.db.query("users").collect();

// Record with Id keys
const userMap: Record<Id<"users">, string> = {};
for (const user of users) {
  userMap[user._id] = user.name;
}
```

### Context Types

```typescript
import { QueryCtx, MutationCtx, ActionCtx } from "./_generated/server";

// Query context - read-only
async function readUser(ctx: QueryCtx, id: Id<"users">) {
  return await ctx.db.get(id);
}

// Mutation context - read and write
async function createUser(ctx: MutationCtx, name: string) {
  return await ctx.db.insert("users", { name, createdAt: Date.now() });
}

// Action context - no db, uses runQuery/runMutation
async function processUser(ctx: ActionCtx, id: Id<"users">) {
  const user = await ctx.runQuery(internal.users.getById, { id });
  // ...
}
```

## Index Design

### Index Naming Convention

Include all fields in the index name: `by_field1_and_field2_and_field3`

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

### Index Usage

```typescript
// Using indexes in queries
const messages = await ctx.db
  .query("messages")
  .withIndex("by_channel_author_deleted", (q) =>
    q.eq("channelId", channelId).eq("authorId", authorId).eq("isDeleted", false)
  )
  .collect();

// Partial prefix match (uses first field only)
const allChannelMessages = await ctx.db
  .query("messages")
  .withIndex("by_channel_author_deleted", (q) => q.eq("channelId", channelId))
  .collect();
```

## Validator Extraction from Schema

### Reusing Schema Validators

```typescript
// convex/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

// Define shared validators
export const userValidator = v.object({
  name: v.string(),
  email: v.string(),
  role: v.union(v.literal("admin"), v.literal("user")),
});

export default defineSchema({
  users: defineTable(userValidator),
});
```

```typescript
// convex/users.ts
import { mutation, query } from "./_generated/server";
import { v } from "convex/values";
import schema from "./schema";

// Extract validator from schema and extend with system fields
const userDoc = schema.tables.users.validator.extend({
  _id: v.id("users"),
  _creationTime: v.number(),
});

export const getUser = query({
  args: { userId: v.id("users") },
  returns: v.union(userDoc, v.null()),
  handler: async (ctx, args) => {
    return await ctx.db.get(args.userId);
  },
});
```

## Common Patterns

### Pattern 1: Status Enum

```typescript
// Schema
const statusValidator = v.union(
  v.literal("pending"),
  v.literal("processing"),
  v.literal("completed"),
  v.literal("failed")
);

export default defineSchema({
  jobs: defineTable({
    status: statusValidator,
    data: v.string(),
  }).index("by_status", ["status"]),
});

// Usage in functions
export const getJobsByStatus = query({
  args: {
    status: v.union(
      v.literal("pending"),
      v.literal("processing"),
      v.literal("completed"),
      v.literal("failed")
    ),
  },
  returns: v.array(
    v.object({
      _id: v.id("jobs"),
      _creationTime: v.number(),
      status: v.string(),
      data: v.string(),
    })
  ),
  handler: async (ctx, args) => {
    return await ctx.db
      .query("jobs")
      .withIndex("by_status", (q) => q.eq("status", args.status))
      .collect();
  },
});
```

### Pattern 2: Polymorphic Documents

```typescript
// Schema with discriminated union pattern
export default defineSchema({
  notifications: defineTable({
    userId: v.id("users"),
    type: v.union(
      v.literal("message"),
      v.literal("mention"),
      v.literal("system")
    ),
    // Common fields
    read: v.boolean(),
    createdAt: v.number(),
    // Type-specific data stored as object
    data: v.union(
      v.object({ type: v.literal("message"), messageId: v.id("messages") }),
      v.object({
        type: v.literal("mention"),
        messageId: v.id("messages"),
        mentionedBy: v.id("users"),
      }),
      v.object({
        type: v.literal("system"),
        title: v.string(),
        body: v.string(),
      })
    ),
  }).index("by_user", ["userId"]),
});
```

### Pattern 3: Timestamps Pattern

```typescript
// Helper for timestamp fields
const timestampsValidator = {
  createdAt: v.number(),
  updatedAt: v.number(),
};

export default defineSchema({
  posts: defineTable({
    title: v.string(),
    body: v.string(),
    authorId: v.id("users"),
    ...timestampsValidator,
  }),
});
```

### Pattern 4: Soft Deletes

```typescript
export default defineSchema({
  items: defineTable({
    content: v.string(),
    deletedAt: v.optional(v.number()),
  }).index("by_active", ["deletedAt"]),
});

// Query active items only
const activeItems = await ctx.db
  .query("items")
  .withIndex("by_active", (q) => q.eq("deletedAt", undefined))
  .collect();
```

## Common Pitfalls

### Pitfall 1: Using v.bigint() (Deprecated)

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

### Pitfall 2: Missing System Fields in Return Validators

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
    return await ctx.db.get(args.userId);
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

### Pitfall 3: Using string Instead of v.id()

**❌ WRONG:**

```typescript
export const getMessage = query({
  args: { messageId: v.string() }, // ❌ Should be v.id()
  returns: v.null(),
  handler: async (ctx, args) => {
    // Type error: can't use string as Id
    return await ctx.db.get(args.messageId);
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

### Pitfall 4: Redundant Indexes

**❌ WRONG:**

```typescript
export default defineSchema({
  messages: defineTable({
    channelId: v.id("channels"),
    authorId: v.id("users"),
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
  })
    // ✅ Single compound index serves both queries
    .index("by_channel_author", ["channelId", "authorId"]),
});
// Use .eq("channelId", id) for channel-only queries (prefix match)
// Use .eq("channelId", id).eq("authorId", authorId) for both
```

## Quick Reference

### Validator Cheat Sheet

| Type        | Validator                          | TypeScript               |
| ----------- | ---------------------------------- | ------------------------ |
| String      | `v.string()`                       | `string`                 |
| Number      | `v.number()`                       | `number`                 |
| Boolean     | `v.boolean()`                      | `boolean`                |
| Null        | `v.null()`                         | `null`                   |
| 64-bit Int  | `v.int64()`                        | `bigint`                 |
| Bytes       | `v.bytes()`                        | `ArrayBuffer`            |
| Document ID | `v.id("table")`                    | `Id<"table">`            |
| Array       | `v.array(v.string())`              | `string[]`               |
| Object      | `v.object({ x: v.number() })`      | `{ x: number }`          |
| Record      | `v.record(v.string(), v.number())` | `Record<string, number>` |
| Union       | `v.union(v.string(), v.null())`    | `string \| null`         |
| Optional    | `v.optional(v.string())`           | `string \| undefined`    |
| Literal     | `v.literal("active")`              | `"active"`               |

### Type Import Cheat Sheet

```typescript
// Document and ID types
import { Doc, Id } from "./_generated/dataModel";

// Context types
import { QueryCtx, MutationCtx, ActionCtx } from "./_generated/server";

// Function builders
import { query, mutation, action } from "./_generated/server";
import {
  internalQuery,
  internalMutation,
  internalAction,
} from "./_generated/server";

// Validators
import { v } from "convex/values";

// Schema builders
import { defineSchema, defineTable } from "convex/server";
```
