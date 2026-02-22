---
name: convex-migrations
description: Database migrations and schema evolution in Convex. Use when adding new fields, changing data structures, backfilling data, renaming fields, or performing zero-downtime schema changes.
---

# Convex Migrations

## Migration Strategy

Convex uses a "progressive migration" approach:

1. Add new optional field to schema
2. Deploy code that writes to both old and new fields
3. Run migration to backfill existing data
4. Deploy code that only uses new field
5. Remove old field from schema

## Adding a New Field

### Step 1: Update Schema (Optional Field)

```typescript
// convex/schema.ts
export default defineSchema({
  users: defineTable({
    name: v.string(),
    email: v.string(),
    // New field - optional during migration
    displayName: v.optional(v.string()),
  }),
});
```

### Step 2: Write to Both Fields

```typescript
// convex/users.ts
export const create = mutation({
  args: { name: v.string(), email: v.string() },
  returns: v.id("users"),
  handler: async (ctx, args) => {
    return await ctx.db.insert("users", {
      name: args.name,
      email: args.email,
      displayName: args.name, // Write new field
    });
  },
});
```

### Step 3: Backfill Migration

```typescript
// convex/migrations.ts
import { internalMutation } from "./_generated/server";
import { v } from "convex/values";

const BATCH_SIZE = 100;

export const backfillDisplayName = internalMutation({
  args: { cursor: v.optional(v.string()) },
  returns: v.union(v.string(), v.null()),
  handler: async (ctx, args) => {
    const result = await ctx.db
      .query("users")
      .paginate({ numItems: BATCH_SIZE, cursor: args.cursor ?? null });

    for (const user of result.page) {
      if (user.displayName === undefined) {
        await ctx.db.patch(user._id, { displayName: user.name });
      }
    }

    // Return cursor for next batch, or null if done
    return result.isDone ? null : result.continueCursor;
  },
});
```

### Step 4: Run Migration

```typescript
// convex/migrations.ts
export const runDisplayNameMigration = internalMutation({
  args: {},
  returns: v.null(),
  handler: async (ctx) => {
    let cursor: string | null = null;

    do {
      cursor = await ctx.runMutation(internal.migrations.backfillDisplayName, {
        cursor: cursor ?? undefined,
      });
    } while (cursor !== null);

    return null;
  },
});
```

Or use scheduler for async processing:

```typescript
export const startMigration = internalMutation({
  args: {},
  returns: v.null(),
  handler: async (ctx) => {
    await ctx.scheduler.runAfter(0, internal.migrations.backfillDisplayName, {});
    return null;
  },
});

export const backfillDisplayName = internalMutation({
  args: { cursor: v.optional(v.string()) },
  returns: v.null(),
  handler: async (ctx, args) => {
    const result = await ctx.db
      .query("users")
      .paginate({ numItems: BATCH_SIZE, cursor: args.cursor ?? null });

    for (const user of result.page) {
      if (user.displayName === undefined) {
        await ctx.db.patch(user._id, { displayName: user.name });
      }
    }

    // Schedule next batch
    if (!result.isDone) {
      await ctx.scheduler.runAfter(0, internal.migrations.backfillDisplayName, {
        cursor: result.continueCursor,
      });
    }
    return null;
  },
});
```

## Renaming a Field

### Step 1: Add New Field

```typescript
// Schema with both fields
users: defineTable({
  userName: v.string(),  // Old field
  name: v.optional(v.string()),  // New field
}),
```

### Step 2: Write to Both, Read from New

```typescript
export const update = mutation({
  args: { userId: v.id("users"), name: v.string() },
  returns: v.null(),
  handler: async (ctx, args) => {
    await ctx.db.patch(args.userId, {
      userName: args.name,  // Old field
      name: args.name,      // New field
    });
    return null;
  },
});

export const get = query({
  args: { userId: v.id("users") },
  returns: v.union(v.object({ name: v.string() }), v.null()),
  handler: async (ctx, args) => {
    const user = await ctx.db.get(args.userId);
    if (!user) return null;

    // Read from new field with fallback
    return { name: user.name ?? user.userName };
  },
});
```

### Step 3: Backfill and Complete

After migration, update schema to require new field and remove old:

```typescript
users: defineTable({
  name: v.string(),  // Now required, userName removed
}),
```

## Changing Field Type

### Example: String to Array

```typescript
// Old: tags: v.string() (comma-separated)
// New: tags: v.array(v.string())

// Step 1: Add new field
tags: v.optional(v.string()),
tagsArray: v.optional(v.array(v.string())),

// Step 2: Migration
export const migrateTagsToArray = internalMutation({
  args: { cursor: v.optional(v.string()) },
  returns: v.null(),
  handler: async (ctx, args) => {
    const result = await ctx.db
      .query("posts")
      .paginate({ numItems: 100, cursor: args.cursor ?? null });

    for (const post of result.page) {
      if (post.tags && !post.tagsArray) {
        const tagsArray = post.tags.split(",").map((t) => t.trim());
        await ctx.db.patch(post._id, { tagsArray });
      }
    }

    if (!result.isDone) {
      await ctx.scheduler.runAfter(0, internal.migrations.migrateTagsToArray, {
        cursor: result.continueCursor,
      });
    }
    return null;
  },
});
```

## Index Changes

### Adding an Index

Indexes are created automatically when you push schema changes:

```typescript
// Just add to schema - no migration needed
users: defineTable({
  email: v.string(),
  createdAt: v.number(),
})
  .index("by_email", ["email"])
  .index("by_created", ["createdAt"]),  // New index
```

### Removing an Index

Remove from schema and redeploy - old index is dropped automatically.

## Migration Tracking

Track migration progress:

```typescript
// convex/schema.ts
migrations: defineTable({
  name: v.string(),
  startedAt: v.number(),
  completedAt: v.optional(v.number()),
  processedCount: v.number(),
  status: v.union(v.literal("running"), v.literal("completed"), v.literal("failed")),
  error: v.optional(v.string()),
}).index("by_name", ["name"]),

// convex/migrations.ts
export const runMigration = internalMutation({
  args: { name: v.string() },
  returns: v.null(),
  handler: async (ctx, args) => {
    // Check if already running
    const existing = await ctx.db
      .query("migrations")
      .withIndex("by_name", (q) => q.eq("name", args.name))
      .unique();

    if (existing?.status === "running") {
      throw new ConvexError({ code: "CONFLICT", message: "Migration already running" });
    }

    // Create migration record
    const migrationId = await ctx.db.insert("migrations", {
      name: args.name,
      startedAt: Date.now(),
      processedCount: 0,
      status: "running",
    });

    // Start migration
    await ctx.scheduler.runAfter(0, internal.migrations.processBatch, {
      migrationId,
      cursor: undefined,
    });
    return null;
  },
});
```

## Common Patterns

### Soft Delete Migration

```typescript
// Add deletedAt field for soft deletes
export const migrateSoftDelete = internalMutation({
  args: { cursor: v.optional(v.string()) },
  returns: v.null(),
  handler: async (ctx, args) => {
    const result = await ctx.db
      .query("items")
      .paginate({ numItems: 100, cursor: args.cursor ?? null });

    for (const item of result.page) {
      if (item.deletedAt === undefined) {
        await ctx.db.patch(item._id, { deletedAt: null });
      }
    }

    if (!result.isDone) {
      await ctx.scheduler.runAfter(0, internal.migrations.migrateSoftDelete, {
        cursor: result.continueCursor,
      });
    }
    return null;
  },
});
```

### Data Normalization

```typescript
// Normalize email addresses to lowercase
export const normalizeEmails = internalMutation({
  args: { cursor: v.optional(v.string()) },
  returns: v.null(),
  handler: async (ctx, args) => {
    const result = await ctx.db
      .query("users")
      .paginate({ numItems: 100, cursor: args.cursor ?? null });

    for (const user of result.page) {
      const normalized = user.email.toLowerCase();
      if (user.email !== normalized) {
        await ctx.db.patch(user._id, { email: normalized });
      }
    }

    if (!result.isDone) {
      await ctx.scheduler.runAfter(0, internal.migrations.normalizeEmails, {
        cursor: result.continueCursor,
      });
    }
    return null;
  },
});
```

## Common Pitfalls

- **Breaking changes** - Always use optional fields during migration
- **Large batches** - Keep batch size under 100 to avoid timeouts
- **Missing cursor** - Always use pagination for large datasets
- **No tracking** - Log migration progress for debugging
- **Skipping backfill** - Don't assume code handles missing fields forever

## References

- Schema: https://docs.convex.dev/database/schemas
- Best Practices: https://docs.convex.dev/understanding/best-practices/
