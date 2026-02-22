---
name: convex-patterns
description: Code organization patterns and TypeScript best practices for Convex. Use when structuring a Convex project, writing helper functions, defining schemas, working with types like QueryCtx/MutationCtx/ActionCtx, or organizing code in a convex/model directory.
---

# Convex Patterns

## Always Define Return Validators

Every function should have a `returns` validator:

```typescript
export const getUser = query({
  args: { userId: v.id("users") },
  returns: v.union(
    v.object({
      _id: v.id("users"),
      _creationTime: v.number(),
      name: v.string(),
      email: v.string(),
    }),
    v.null()
  ),
  handler: async (ctx, args) => {
    return await ctx.db.get("users", args.userId);
  },
});
```

## Project Structure

```
convex/
├── _generated/
├── lib/              # Shared utilities
│   └── auth.ts       # Auth helpers
├── model/            # Business logic
│   ├── users.ts
│   └── tasks.ts
├── schema.ts         # Database schema
├── users.ts          # Public API (thin wrappers)
└── tasks.ts
```

## Helper Functions Pattern

Business logic in `model/`, thin wrappers in public API:

```typescript
// convex/model/users.ts
import { QueryCtx, MutationCtx } from '../_generated/server';
import { Doc, Id } from '../_generated/dataModel';
import { ConvexError } from "convex/values";

export async function getCurrentUser(ctx: QueryCtx | MutationCtx): Promise<Doc<"users">> {
  const identity = await ctx.auth.getUserIdentity();
  if (!identity) {
    throw new ConvexError({ code: "UNAUTHENTICATED", message: "Not logged in" });
  }

  const user = await ctx.db
    .query("users")
    .withIndex("by_tokenIdentifier", (q) => q.eq("tokenIdentifier", identity.tokenIdentifier))
    .unique();

  if (!user) {
    throw new ConvexError({ code: "NOT_FOUND", message: "User not found" });
  }
  return user;
}

export async function getById(ctx: QueryCtx, userId: Id<"users">): Promise<Doc<"users"> | null> {
  return await ctx.db.get("users", userId);
}
```

```typescript
// convex/users.ts (thin wrapper)
import { query } from "./_generated/server";
import { v } from "convex/values";
import * as Users from "./model/users";

export const get = query({
  args: { userId: v.id("users") },
  returns: v.union(v.object({ _id: v.id("users"), name: v.string() }), v.null()),
  handler: async (ctx, args) => Users.getById(ctx, args.userId),
});
```

## Schema Definition

```typescript
// convex/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  users: defineTable({
    tokenIdentifier: v.string(),
    name: v.string(),
    email: v.string(),
    role: v.union(v.literal("user"), v.literal("admin")),
  })
    .index("by_tokenIdentifier", ["tokenIdentifier"])
    .index("by_email", ["email"]),

  tasks: defineTable({
    title: v.string(),
    description: v.optional(v.string()),
    userId: v.id("users"),
    status: v.union(v.literal("pending"), v.literal("done")),
    priority: v.union(v.literal("low"), v.literal("medium"), v.literal("high")),
  })
    .index("by_user", ["userId"])
    .index("by_user_and_status", ["userId", "status"]),
});
```

## TypeScript Types

```typescript
// Context types
import { QueryCtx, MutationCtx, ActionCtx } from "./_generated/server";

// Document and ID types
import { Doc, Id } from "./_generated/dataModel";
type User = Doc<"users">;
type UserId = Id<"users">;

// Infer types from validators
import { Infer, v } from "convex/values";
const priorityValidator = v.union(v.literal("low"), v.literal("medium"), v.literal("high"));
type Priority = Infer<typeof priorityValidator>;  // "low" | "medium" | "high"

// Without system fields (for inserts)
import { WithoutSystemFields } from "convex/server";
type NewUser = WithoutSystemFields<Doc<"users">>;

// Client-side return types
import { FunctionReturnType } from "convex/server";
type UserData = FunctionReturnType<typeof api.users.get>;
```

## Validator Types Reference

| Validator | TypeScript | Example |
|-----------|-----------|---------|
| `v.string()` | `string` | `"hello"` |
| `v.number()` | `number` | `42` |
| `v.boolean()` | `boolean` | `true` |
| `v.null()` | `null` | `null` |
| `v.id("table")` | `Id<"table">` | Document reference |
| `v.array(v)` | `T[]` | `[1, 2, 3]` |
| `v.object({})` | `{ ... }` | `{ name: "..." }` |
| `v.optional(v)` | `T \| undefined` | Optional field |
| `v.union(...)` | `T1 \| T2` | Multiple types |
| `v.literal(x)` | `"x"` | Exact value |

## Reusable Validators

```typescript
// convex/validators.ts
import { v } from "convex/values";

export const userValidator = v.object({
  _id: v.id("users"),
  _creationTime: v.number(),
  name: v.string(),
  email: v.string(),
  role: v.union(v.literal("user"), v.literal("admin")),
});

export const taskValidator = v.object({
  _id: v.id("tasks"),
  _creationTime: v.number(),
  title: v.string(),
  userId: v.id("users"),
  status: v.union(v.literal("pending"), v.literal("done")),
});
```

## References

- TypeScript: https://docs.convex.dev/understanding/best-practices/typescript
- Schemas: https://docs.convex.dev/database/schemas
