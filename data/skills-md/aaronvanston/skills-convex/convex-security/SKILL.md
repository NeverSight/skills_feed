---
name: convex-security
description: Security best practices for Convex functions including ConvexError handling, argument/return validation, authentication helpers, access control, rate limiting, and internal functions. Use when writing public queries/mutations/actions, implementing authentication, adding authorization checks, handling errors, or reviewing Convex functions for security.
---

# Convex Security

## Error Handling with ConvexError

Use `ConvexError` for user-facing errors with structured error codes:

```typescript
import { ConvexError } from "convex/values";

export const updateTask = mutation({
  args: { taskId: v.id("tasks"), title: v.string() },
  returns: v.null(),
  handler: async (ctx, args) => {
    const task = await ctx.db.get("tasks", args.taskId);

    if (!task) {
      throw new ConvexError({
        code: "NOT_FOUND",
        message: "Task not found",
      });
    }

    await ctx.db.patch("tasks", args.taskId, { title: args.title });
    return null;
  },
});
```

**Common error codes:** `UNAUTHENTICATED`, `FORBIDDEN`, `NOT_FOUND`, `RATE_LIMITED`, `VALIDATION_ERROR`

## Argument AND Return Validators

Always define both `args` and `returns` validators:

```typescript
export const createTask = mutation({
  args: {
    title: v.string(),
    priority: v.union(v.literal("low"), v.literal("medium"), v.literal("high")),
  },
  returns: v.id("tasks"),  // Always include returns!
  handler: async (ctx, args) => {
    return await ctx.db.insert("tasks", {
      title: args.title,
      priority: args.priority,
      completed: false,
    });
  },
});
```

**ESLint:** Use `@convex-dev/require-argument-validators` rule.

## Authentication Helpers

Create reusable auth helpers:

```typescript
// convex/lib/auth.ts
import { QueryCtx, MutationCtx } from "./_generated/server";
import { ConvexError } from "convex/values";
import { Doc } from "./_generated/dataModel";

export async function getUser(ctx: QueryCtx | MutationCtx): Promise<Doc<"users"> | null> {
  const identity = await ctx.auth.getUserIdentity();
  if (!identity) return null;

  return await ctx.db
    .query("users")
    .withIndex("by_tokenIdentifier", (q) =>
      q.eq("tokenIdentifier", identity.tokenIdentifier)
    )
    .unique();
}

export async function requireAuth(ctx: QueryCtx | MutationCtx): Promise<Doc<"users">> {
  const user = await getUser(ctx);
  if (!user) {
    throw new ConvexError({
      code: "UNAUTHENTICATED",
      message: "Authentication required",
    });
  }
  return user;
}

type UserRole = "user" | "moderator" | "admin";
const roleHierarchy: Record<UserRole, number> = { user: 0, moderator: 1, admin: 2 };

export async function requireRole(
  ctx: QueryCtx | MutationCtx,
  minRole: UserRole
): Promise<Doc<"users">> {
  const user = await requireAuth(ctx);
  const userLevel = roleHierarchy[user.role as UserRole] ?? 0;

  if (userLevel < roleHierarchy[minRole]) {
    throw new ConvexError({
      code: "FORBIDDEN",
      message: `Role '${minRole}' or higher required`,
    });
  }
  return user;
}
```

**Usage:**
```typescript
export const adminOnly = mutation({
  args: {},
  returns: v.null(),
  handler: async (ctx) => {
    await requireRole(ctx, "admin");
    // ... admin logic
    return null;
  },
});
```

## Row-Level Access Control

Verify ownership before operations:

```typescript
export const updateTask = mutation({
  args: { taskId: v.id("tasks"), title: v.string() },
  returns: v.null(),
  handler: async (ctx, args) => {
    const user = await requireAuth(ctx);
    const task = await ctx.db.get("tasks", args.taskId);

    if (!task || task.userId !== user._id) {
      throw new ConvexError({ code: "FORBIDDEN", message: "Not authorized" });
    }

    await ctx.db.patch("tasks", args.taskId, { title: args.title });
    return null;
  },
});
```

## Rate Limiting

Prevent abuse with rate limiting:

```typescript
const RATE_LIMITS = {
  message: { requests: 10, windowMs: 60000 },  // 10 per minute
  upload: { requests: 5, windowMs: 300000 },   // 5 per 5 minutes
};

export const checkRateLimit = mutation({
  args: { userId: v.string(), action: v.string() },
  returns: v.object({ allowed: v.boolean(), retryAfter: v.optional(v.number()) }),
  handler: async (ctx, args) => {
    const limit = RATE_LIMITS[args.action];
    const windowStart = Date.now() - limit.windowMs;

    const requests = await ctx.db
      .query("rateLimits")
      .withIndex("by_user_and_action", (q) =>
        q.eq("userId", args.userId).eq("action", args.action)
      )
      .filter((q) => q.gt(q.field("timestamp"), windowStart))
      .collect();

    if (requests.length >= limit.requests) {
      return { allowed: false, retryAfter: requests[0].timestamp + limit.windowMs - Date.now() };
    }

    await ctx.db.insert("rateLimits", {
      userId: args.userId,
      action: args.action,
      timestamp: Date.now(),
    });
    return { allowed: true };
  },
});
```

## Internal Functions Only for Scheduling

Always use `internal.*` for `ctx.run*` and scheduling:

```typescript
// Bad - exposes public function
await ctx.scheduler.runAfter(0, api.tasks.process, { id });

// Good - uses internal function
await ctx.scheduler.runAfter(0, internal.tasks.process, { id });

// Internal function definition
export const process = internalMutation({
  args: { id: v.id("tasks") },
  returns: v.null(),
  handler: async (ctx, args) => {
    // ... processing logic
    return null;
  },
});
```

**Tip:** Never import `api` from `_generated/api.ts` in Convex functions.

## Include Table Name in ctx.db

Always include table name as first argument:

```typescript
// Bad
await ctx.db.get(movieId);
await ctx.db.patch(movieId, { title: "Whiplash" });

// Good
await ctx.db.get("movies", movieId);
await ctx.db.patch("movies", movieId, { title: "Whiplash" });
```

**ESLint:** Use `@convex-dev/explicit-table-ids` rule with autofix.

## References

- Error Handling: https://docs.convex.dev/functions/error-handling
- Authentication: https://docs.convex.dev/auth/functions-auth
- Production Security: https://docs.convex.dev/production
