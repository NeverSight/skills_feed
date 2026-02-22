---
name: convex-realtime
description: Realtime subscriptions and optimistic updates in Convex. Use when implementing live data updates, optimistic UI, pagination with realtime, presence indicators, typing indicators, or any feature requiring instant data synchronization.
---

# Convex Realtime

## Automatic Subscriptions

Queries in Convex automatically subscribe to updates:

```typescript
// React component - automatically updates when data changes
function TaskList({ userId }: { userId: Id<"users"> }) {
  const tasks = useQuery(api.tasks.list, { userId });

  if (tasks === undefined) return <Loading />;

  return (
    <ul>
      {tasks.map((task) => (
        <li key={task._id}>{task.title}</li>
      ))}
    </ul>
  );
}
```

## Optimistic Updates

### Basic Optimistic Update

```typescript
import { useMutation } from "convex/react";
import { api } from "../convex/_generated/api";

function AddTask() {
  const addTask = useMutation(api.tasks.create).withOptimisticUpdate(
    (localStore, args) => {
      const { title, userId } = args;

      // Get current tasks from local cache
      const currentTasks = localStore.getQuery(api.tasks.list, { userId });
      if (currentTasks === undefined) return;

      // Add optimistic task
      const optimisticTask = {
        _id: crypto.randomUUID() as Id<"tasks">,
        _creationTime: Date.now(),
        title,
        userId,
        completed: false,
      };

      // Update local cache immediately
      localStore.setQuery(api.tasks.list, { userId }, [
        optimisticTask,
        ...currentTasks,
      ]);
    }
  );

  return (
    <button onClick={() => addTask({ title: "New Task", userId })}>
      Add Task
    </button>
  );
}
```

### Optimistic Delete

```typescript
const deleteTask = useMutation(api.tasks.remove).withOptimisticUpdate(
  (localStore, args) => {
    const { taskId, userId } = args;

    const currentTasks = localStore.getQuery(api.tasks.list, { userId });
    if (currentTasks === undefined) return;

    // Remove task from local cache
    localStore.setQuery(
      api.tasks.list,
      { userId },
      currentTasks.filter((t) => t._id !== taskId)
    );
  }
);
```

### Optimistic Toggle

```typescript
const toggleTask = useMutation(api.tasks.toggle).withOptimisticUpdate(
  (localStore, args) => {
    const { taskId, userId } = args;

    const currentTasks = localStore.getQuery(api.tasks.list, { userId });
    if (currentTasks === undefined) return;

    // Toggle completed status locally
    localStore.setQuery(
      api.tasks.list,
      { userId },
      currentTasks.map((t) =>
        t._id === taskId ? { ...t, completed: !t.completed } : t
      )
    );
  }
);
```

## Paginated Realtime

```typescript
// convex/messages.ts
import { query } from "./_generated/server";
import { v } from "convex/values";
import { paginationOptsValidator } from "convex/server";

export const list = query({
  args: {
    channelId: v.id("channels"),
    paginationOpts: paginationOptsValidator,
  },
  returns: v.object({
    page: v.array(v.object({
      _id: v.id("messages"),
      _creationTime: v.number(),
      content: v.string(),
      authorId: v.id("users"),
    })),
    isDone: v.boolean(),
    continueCursor: v.string(),
  }),
  handler: async (ctx, args) => {
    return await ctx.db
      .query("messages")
      .withIndex("by_channel", (q) => q.eq("channelId", args.channelId))
      .order("desc")
      .paginate(args.paginationOpts);
  },
});
```

```typescript
// React component with pagination
function MessageList({ channelId }: { channelId: Id<"channels"> }) {
  const { results, status, loadMore } = usePaginatedQuery(
    api.messages.list,
    { channelId },
    { initialNumItems: 25 }
  );

  return (
    <div>
      {results.map((message) => (
        <Message key={message._id} message={message} />
      ))}

      {status === "CanLoadMore" && (
        <button onClick={() => loadMore(25)}>Load More</button>
      )}

      {status === "LoadingMore" && <Loading />}
    </div>
  );
}
```

## Presence Indicators

### Schema

```typescript
// convex/schema.ts
export default defineSchema({
  presence: defineTable({
    odcumentId: v.string(),
    odcumentType: v.string(),
    lastSeen: v.number(),
  })
    .index("by_user", ["userId"])
    .index("by_document", ["documentId", "documentType"]),
});
```

### Update Presence

```typescript
// convex/presence.ts
export const heartbeat = mutation({
  args: {
    documentId: v.string(),
    documentType: v.string(),
  },
  returns: v.null(),
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) return null;

    const existing = await ctx.db
      .query("presence")
      .withIndex("by_user", (q) => q.eq("userId", identity.subject))
      .filter((q) =>
        q.and(
          q.eq(q.field("documentId"), args.documentId),
          q.eq(q.field("documentType"), args.documentType)
        )
      )
      .unique();

    if (existing) {
      await ctx.db.patch(existing._id, { lastSeen: Date.now() });
    } else {
      await ctx.db.insert("presence", {
        userId: identity.subject,
        documentId: args.documentId,
        documentType: args.documentType,
        lastSeen: Date.now(),
      });
    }
    return null;
  },
});

export const getActive = query({
  args: {
    documentId: v.string(),
    documentType: v.string(),
  },
  returns: v.array(v.object({
    userId: v.string(),
    lastSeen: v.number(),
  })),
  handler: async (ctx, args) => {
    const fiveMinutesAgo = Date.now() - 5 * 60 * 1000;

    return await ctx.db
      .query("presence")
      .withIndex("by_document", (q) =>
        q.eq("documentId", args.documentId).eq("documentType", args.documentType)
      )
      .filter((q) => q.gt(q.field("lastSeen"), fiveMinutesAgo))
      .collect();
  },
});
```

### Client Hook

```typescript
function usePresence(documentId: string, documentType: string) {
  const heartbeat = useMutation(api.presence.heartbeat);
  const activeUsers = useQuery(api.presence.getActive, {
    documentId,
    documentType,
  });

  useEffect(() => {
    // Send heartbeat every 30 seconds
    const interval = setInterval(() => {
      heartbeat({ documentId, documentType });
    }, 30000);

    // Initial heartbeat
    heartbeat({ documentId, documentType });

    return () => clearInterval(interval);
  }, [documentId, documentType, heartbeat]);

  return activeUsers ?? [];
}
```

## Typing Indicators

```typescript
// convex/typing.ts
export const setTyping = mutation({
  args: { channelId: v.id("channels"), isTyping: v.boolean() },
  returns: v.null(),
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) return null;

    const existing = await ctx.db
      .query("typing")
      .withIndex("by_channel_user", (q) =>
        q.eq("channelId", args.channelId).eq("userId", identity.subject)
      )
      .unique();

    if (args.isTyping) {
      if (existing) {
        await ctx.db.patch(existing._id, { updatedAt: Date.now() });
      } else {
        await ctx.db.insert("typing", {
          channelId: args.channelId,
          userId: identity.subject,
          updatedAt: Date.now(),
        });
      }
    } else if (existing) {
      await ctx.db.delete(existing._id);
    }
    return null;
  },
});

export const getTyping = query({
  args: { channelId: v.id("channels") },
  returns: v.array(v.string()),
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    const tenSecondsAgo = Date.now() - 10000;

    const typing = await ctx.db
      .query("typing")
      .withIndex("by_channel", (q) => q.eq("channelId", args.channelId))
      .filter((q) => q.gt(q.field("updatedAt"), tenSecondsAgo))
      .collect();

    // Exclude current user
    return typing
      .filter((t) => t.userId !== identity?.subject)
      .map((t) => t.userId);
  },
});
```

## Conditional Queries

```typescript
function UserProfile({ userId }: { userId: Id<"users"> | null }) {
  // Query only runs when userId is not null
  const user = useQuery(
    api.users.get,
    userId ? { userId } : "skip"
  );

  if (userId === null) return <GuestView />;
  if (user === undefined) return <Loading />;

  return <ProfileView user={user} />;
}
```

## Common Pitfalls

- **Stale optimistic updates** - Always verify server state matches expected
- **Over-subscribing** - Only subscribe to data you need
- **Missing loading states** - Handle `undefined` (loading) vs `null` (not found)
- **Presence cleanup** - Add scheduled job to clean old presence records

## References

- Reactivity: https://docs.convex.dev/client/react
- Optimistic Updates: https://docs.convex.dev/client/react/optimistic-updates
- Pagination: https://docs.convex.dev/database/pagination
