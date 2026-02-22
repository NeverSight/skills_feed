---
name: convex-queries
description: Best practices for Convex database queries, indexes, and filtering. Use when writing or reviewing database queries in Convex, working with `.filter()`, `.collect()`, `.withIndex()`, defining indexes in schema.ts, or optimizing query performance.
---

# Convex Queries

## Query Pattern with Index

```typescript
export const listUserTasks = query({
  args: { userId: v.id("users") },
  returns: v.array(v.object({
    _id: v.id("tasks"),
    _creationTime: v.number(),
    title: v.string(),
    completed: v.boolean(),
  })),
  handler: async (ctx, args) => {
    return await ctx.db
      .query("tasks")
      .withIndex("by_user", (q) => q.eq("userId", args.userId))
      .order("desc")
      .collect();
  },
});
```

## Avoid `.filter()` on Database Queries

Use `.withIndex()` instead - `.filter()` has same performance as filtering in code:

```typescript
// Bad - using .filter()
const tomsMessages = await ctx.db
  .query("messages")
  .filter((q) => q.eq(q.field("author"), "Tom"))
  .collect();

// Good - use an index
const tomsMessages = await ctx.db
  .query("messages")
  .withIndex("by_author", (q) => q.eq("author", "Tom"))
  .collect();

// Good - filter in code (if index not needed)
const allMessages = await ctx.db.query("messages").collect();
const tomsMessages = allMessages.filter((m) => m.author === "Tom");
```

**Finding `.filter()` usage:** Search with regex `\.filter\(\(?q`

**Exception:** Paginated queries benefit from `.filter()`.

## Only Use `.collect()` with Small Result Sets

For 1000+ documents, use indexes, pagination, or limits:

```typescript
// Bad - potentially unbounded
const allMovies = await ctx.db.query("movies").collect();

// Good - use .take() with "99+" display
const movies = await ctx.db
  .query("movies")
  .withIndex("by_user", (q) => q.eq("userId", userId))
  .take(100);
const count = movies.length === 100 ? "99+" : movies.length.toString();

// Good - paginated
const movies = await ctx.db
  .query("movies")
  .withIndex("by_user", (q) => q.eq("userId", userId))
  .order("desc")
  .paginate(paginationOptions);
```

## Index Configuration

```typescript
// convex/schema.ts
export default defineSchema({
  messages: defineTable({
    channelId: v.id("channels"),
    authorId: v.id("users"),
    content: v.string(),
    sentAt: v.number(),
  })
    .index("by_channel", ["channelId"])
    .index("by_channel_and_author", ["channelId", "authorId"])
    .index("by_channel_and_time", ["channelId", "sentAt"]),
});
```

## Check for Redundant Indexes

`by_foo` and `by_foo_and_bar` are usually redundant - keep only `by_foo_and_bar`:

```typescript
// Bad - redundant
.index("by_team", ["team"])
.index("by_team_and_user", ["team", "user"])

// Good - single combined index works for both
const allTeamMembers = await ctx.db
  .query("teamMembers")
  .withIndex("by_team_and_user", (q) => q.eq("team", teamId))  // Omit user
  .collect();

const specificMember = await ctx.db
  .query("teamMembers")
  .withIndex("by_team_and_user", (q) => q.eq("team", teamId).eq("user", userId))
  .unique();
```

**Exception:** `by_foo` is really `foo` + `_creationTime`. Keep separate if you need that sort order.

## Don't Use `Date.now()` in Queries

Queries don't re-run when `Date.now()` changes:

```typescript
// Bad - stale results, cache thrashing
const posts = await ctx.db
  .query("posts")
  .withIndex("by_released_at", (q) => q.lte("releasedAt", Date.now()))
  .take(100);

// Good - boolean field updated by scheduled function
const posts = await ctx.db
  .query("posts")
  .withIndex("by_is_released", (q) => q.eq("isReleased", true))
  .take(100);
```

## Write Conflict Avoidance (OCC)

Make mutations idempotent:

```typescript
// Good - idempotent, early return if already done
export const completeTask = mutation({
  args: { taskId: v.id("tasks") },
  returns: v.null(),
  handler: async (ctx, args) => {
    const task = await ctx.db.get("tasks", args.taskId);
    if (!task || task.status === "completed") return null;  // Idempotent
    await ctx.db.patch("tasks", args.taskId, { status: "completed" });
    return null;
  },
});

// Good - patch directly without reading when possible
export const updateNote = mutation({
  args: { id: v.id("notes"), content: v.string() },
  returns: v.null(),
  handler: async (ctx, args) => {
    await ctx.db.patch("notes", args.id, { content: args.content });
    return null;
  },
});

// Good - parallel updates with Promise.all
export const reorderItems = mutation({
  args: { itemIds: v.array(v.id("items")) },
  returns: v.null(),
  handler: async (ctx, args) => {
    await Promise.all(
      args.itemIds.map((id, index) => ctx.db.patch("items", id, { order: index }))
    );
    return null;
  },
});
```

## References

- Indexes: https://docs.convex.dev/database/indexes
- Best Practices: https://docs.convex.dev/understanding/best-practices/
