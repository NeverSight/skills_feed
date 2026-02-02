---
name: convex
description: Expert Convex development assistant. Use when users want to build full-stack TypeScript apps with Convex - including setup, server functions (queries/mutations/actions), database schema, auth, file storage, real-time features, frontend integration (React, Next.js, Vue), testing, or deployment.
---

This skill provides expert guidance for building applications with Convex - the full-stack reactive database platform.

## Quick Start

When a user wants to start with Convex:

1. **New project:**
   ```bash
   npm create convex@latest
   npx convex dev
   ```

2. **Add to existing project:**
   ```bash
   npm install convex
   npx convex dev
   ```

3. **Verify:** Check dashboard at https://dashboard.convex.dev

## Core Concepts

### Three Function Types

**Queries** - Read-only, auto-reactive:
```typescript
import { query } from "./_generated/server";

export const list = query({
  args: { channelId: v.id("channels") },
  handler: async ({ db }, { channelId }) => {
    return await db.query("messages")
      .withIndex("by_channel", (q) => q.eq("channel", channelId))
      .collect();
  }
});
```

**Mutations** - Write operations, transactions:
```typescript
import { mutation } from "./_generated/server";

export const send = mutation({
  args: { body: v.string(), channel: v.id("channels") },
  handler: async ({ db }, { body, channel }) => {
    await db.insert("messages", { body, channel, createdAt: Date.now() });
  }
});
```

**Actions** - External API calls:
```typescript
import { action } from "./_generated/server";

export const summarize = action({
  args: { postId: v.id("posts") },
  handler: async (ctx, { postId }) => {
    const post = await ctx.runQuery(api.posts.get, { postId });
    const summary = await fetchLLM(post);
    await ctx.runMutation(api.posts.update, { postId, summary });
  }
});
```

### Database Operations

```typescript
// CRUD
await db.insert("table", { field: value });
const doc = await db.get(id);
await db.patch(id, { field: newValue });
await db.delete(id);

// Query methods
.collect()  // All results
.first()   // First or null
.unique()  // Exactly one (throws if not)
.paginate({ numItems: 50 })  // Pagination
```

### Schema Definition

**File:** `convex/schema.ts`

```typescript
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  messages: defineTable({
    body: v.string(),
    author: v.id("users"),
    channel: v.id("channels"),
    createdAt: v.number()
  })
  .index("by_channel", ["channel"])
  .index("by_channel_created", ["channel", "createdAt"])
});
```

**Common types:**
- `v.string()`, `v.number()`, `v.boolean()`
- `v.id("table")` - Foreign key
- `v.array(T)`, `v.object({})`
- `v.optional(T)`, `v.union(...)`

## Frontend Integration

### React

```typescript
import { ConvexProvider, ConvexReactClient } from "convex/react";

const convex = new ConvexReactClient(process.env.NEXT_PUBLIC_CONVEX_URL!);

<ConvexProvider client={convex}>
  <App />
</ConvexProvider>
```

**Usage:**
```typescript
import { useQuery, useMutation } from "convex/react";
import { api } from "../convex/_generated/api";

const messages = useQuery(api.messages.list, { channelId });
const sendMessage = useMutation(api.messages.send);
```

### Next.js App Router

**Server-side preloading:**
```typescript
import { preloadQuery } from "convex/nextjs";

const preloaded = await preloadQuery(api.posts.list);
return <ClientPage preloaded={preloaded} />;
```

**Client component:**
```typescript
"use client";
import { usePreloadedQuery } from "convex/react";

const posts = usePreloadedQuery(preloaded);
```

## Authentication

### Clerk (Recommended)

**Install:** `npm install @clerk/clerk-react`

**File:** `convex/auth.config.ts`
```typescript
import { AuthConfig } from "convex/server";

export default {
  providers: [{ domain: process.env.CLERK_JWT_ISSUER_DOMAIN!, applicationID: "convex" }]
} satisfies AuthConfig;
```

**Frontend:**
```typescript
import { ConvexProviderWithClerk } from "convex/react-clerk";

<ConvexProviderWithClerk client={convex} useAuth={useAuth}>
  <App />
</ConvexProviderWithClerk>
```

**In functions:**
```typescript
const identity = await ctx.auth.getUserIdentity();
if (!identity) throw new Error("Unauthorized");
```

## File Storage

```typescript
// Upload
const storageId = await ctx.storage.store(fileBlob);
await db.insert("files", { storageId, name });

// Download
const url = await ctx.storage.getUrl(storageId);

// Delete
await ctx.storage.delete(storageId);
```

## HTTP Endpoints

**File:** `convex/http.ts`

```typescript
import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";

const http = httpRouter();

http.route({
  path: "/webhooks/stripe",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    const payload = await request.json();
    await ctx.runMutation(internal.payments.process, { payload });
    return new Response(null, { status: 200 });
  }),
});

export default http;
```

**URL:** `https://<deployment>.convex.site`

## Scheduled Tasks

**Cron Jobs (File: `convex/crons.ts`):**
```typescript
import { cronJobs } from "convex/server";

const crons = cronJobs();
crons.interval("cleanup", { hours: 1 }, internal.tasks.cleanup);
crons.daily("digest", { hourUTC: 9 }, internal.notifications.send);
export default crons;
```

**Scheduler API (in mutations/actions):**
```typescript
// Schedule for later
await ctx.scheduler.runAfter(delayMs, internal.tasks.process, { id });

// Schedule at specific time
await ctx.scheduler.runAt(timestamp, internal.tasks.remind, { userId });
```

## Best Practices

### ✅ DO
- Use indexes for queried fields
- Filter in application code, not with `.filter()` on queries
- Validate auth in protected functions
- Use pagination for large datasets
- Use `ConvexError` for structured errors clients can handle
- Direct function calls, not multiple sequential `ctx.runQuery`

### ❌ DON'T
- Use `.filter()` on queries (use indexes or filter in code)
- Make multiple sequential `runQuery/runMutation` calls (consolidate)
- Forget to validate authentication
- Fetch entire tables without pagination

### Error Handling

```typescript
import { ConvexError } from "convex/values";

// Throw structured errors
if (!identity) {
  throw new ConvexError({ code: "UNAUTHORIZED", message: "Login required" });
}

// Client catches and handles
if (error instanceof ConvexError) {
  console.error(error.data.code, error.data.message);
}
```

## Deployment

**Production:**
```bash
npx convex deploy
```

**With frontend build:**
```bash
npx convex deploy --cmd 'npm run build'
```

**Environment:** Set `CONVEX_DEPLOY_KEY` for production

## Testing

**Install:** `npm install convex-test vitest --save-dev`

```typescript
import { convexTest } from "convex-test";

const t = convexTest(schema);

// Test mutations
await t.mutation(api.posts.create, { title: "Test" });

// Test queries
const posts = await t.query(api.posts.list);
expect(posts).toHaveLength(1);
```

## Common Issues

| Problem | Solution |
|---------|----------|
| Function not found | Run `npx convex dev` to regenerate types |
| Real-time not working | Check ConvexProvider wraps app |
| Type errors | Restart TypeScript server, regenerate types |
| Deploy fails | Verify `CONVEX_DEPLOY_KEY` is set |

## Progressive Disclosure

**Advanced topics in references:**
- **Complete setup**: [QUICK_START.md](references/QUICK_START.md)
- **Deep dive on functions**: [CORE_CONCEPTS.md](references/CORE_CONCEPTS.md)
- **Auth patterns**: [AUTH.md](references/AUTH.md)
- **Framework integration**: [FRONTEND.md](references/FRONTEND.md)
- **Performance patterns**: [BEST_PRACTICES.md](references/BEST_PRACTICES.md)
- **Production deployment**: [DEPLOYMENT.md](references/DEPLOYMENT.md)
- **Troubleshooting**: [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)
- **HTTP endpoints, cron, vector search, Convex Auth**: [ADVANCED.md](references/ADVANCED.md)

## Your Approach

1. **Assess first:** New project or existing? Framework? Goals?
2. **Start simple:** Quick start → add complexity progressively
3. **Embrace reactivity:** Leverage automatic real-time updates
4. **Type safety:** Use TypeScript validation throughout
5. **Index for performance:** Always use indexes on queried fields
6. **Validate auth:** Check authentication in protected functions
7. **Test before deploying:** Use convex-test for unit tests
