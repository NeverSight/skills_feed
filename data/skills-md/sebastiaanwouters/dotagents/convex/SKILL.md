---
name: convex
description: Convex backend development - database, queries, mutations, actions, and real-time APIs
references:
  - references/chat-app-example.md
---

# Convex Guidelines

## Function Syntax

ALWAYS use the new function syntax with args, returns, and handler:

```typescript
import { query } from "./_generated/server";
import { v } from "convex/values";

export const f = query({
  args: { name: v.string() },
  returns: v.string(),
  handler: async (ctx, args) => {
    return "Hello " + args.name;
  },
});
```

### HTTP Endpoints

```typescript
import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";

const http = httpRouter();
http.route({
  path: "/echo",
  method: "POST",
  handler: httpAction(async (ctx, req) => {
    const body = await req.bytes();
    return new Response(body, { status: 200 });
  }),
});
```

## Validators

| Type    | TS Type     | Validator                    | Notes                                    |
|---------|-------------|------------------------------|------------------------------------------|
| Id      | string      | `v.id(tableName)`            |                                          |
| Null    | null        | `v.null()`                   | Use instead of undefined                 |
| Int64   | bigint      | `v.int64()`                  | NOT `v.bigint()` (deprecated)            |
| Float64 | number      | `v.number()`                 |                                          |
| Boolean | boolean     | `v.boolean()`                |                                          |
| String  | string      | `v.string()`                 |                                          |
| Bytes   | ArrayBuffer | `v.bytes()`                  |                                          |
| Array   | Array       | `v.array(values)`            | Max 8192 values                          |
| Object  | Object      | `v.object({prop: value})`    | Max 1024 entries                         |
| Record  | Record      | `v.record(keys, values)`     | Keys: ASCII, nonempty, no $ or _ prefix  |

### Discriminated Unions
```typescript
v.union(
  v.object({ kind: v.literal("error"), errorMessage: v.string() }),
  v.object({ kind: v.literal("success"), value: v.number() }),
)
```

## Function Registration

- **Public**: `query`, `mutation`, `action` - exposed to internet
- **Internal**: `internalQuery`, `internalMutation`, `internalAction` - only callable by other Convex functions

ALWAYS include argument AND return validators. Use `returns: v.null()` if no return value.

## Function Calling

- `ctx.runQuery` - call query from query/mutation/action
- `ctx.runMutation` - call mutation from mutation/action  
- `ctx.runAction` - call action from action (only for crossing runtimes V8↔Node)

Use `FunctionReference` (from `api` or `internal` objects), NOT the function directly:
```typescript
// Correct
await ctx.runQuery(api.example.f, { name: "Bob" });
// Wrong
await ctx.runQuery(f, { name: "Bob" });
```

For same-file calls, add type annotation to avoid circularity:
```typescript
const result: string = await ctx.runQuery(api.example.f, { name: "Bob" });
```

## Function References

- `api.path.to.functionName` - public functions
- `internal.path.to.functionName` - internal functions

File-based routing: `convex/messages/access.ts` → `api.messages.access.functionName`

## Schema

Define in `convex/schema.ts`:
```typescript
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  messages: defineTable({
    channelId: v.id("channels"),
    content: v.string(),
  }).index("by_channel", ["channelId"]),
});
```

System fields auto-added: `_id` (`v.id(tableName)`), `_creationTime` (`v.number()`)

Index naming: include all fields → `by_field1_and_field2`

## Queries

- Do NOT use `filter()` - use `withIndex()` instead
- No `.delete()` - collect results, iterate, call `ctx.db.delete(row._id)`
- `.unique()` for single document (throws if multiple match)
- Default order: ascending `_creationTime`

```typescript
const messages = await ctx.db
  .query("messages")
  .withIndex("by_channel", (q) => q.eq("channelId", channelId))
  .order("desc")
  .take(10);
```

### Full Text Search
```typescript
const messages = await ctx.db
  .query("messages")
  .withSearchIndex("search_body", (q) =>
    q.search("body", "hello hi").eq("channel", "#general"),
  )
  .take(10);
```

### Pagination
```typescript
import { paginationOptsValidator } from "convex/server";

export const list = query({
  args: { paginationOpts: paginationOptsValidator, author: v.string() },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("messages")
      .withIndex("by_author", (q) => q.eq("author", args.author))
      .order("desc")
      .paginate(args.paginationOpts);
  },
});
```
Returns: `{ page, isDone, continueCursor }`

## Mutations

- `ctx.db.patch(id, fields)` - shallow merge
- `ctx.db.replace(id, doc)` - full replace

## Actions

Add `"use node";` at top for Node.js modules. Actions have NO `ctx.db` access.

```typescript
"use node";
import { action } from "./_generated/server";

export const myAction = action({
  args: {},
  returns: v.null(),
  handler: async (ctx, args) => {
    // Use ctx.runQuery/ctx.runMutation for DB access
    return null;
  },
});
```

## Scheduling

### Crons
```typescript
import { cronJobs } from "convex/server";
import { internal } from "./_generated/api";

const crons = cronJobs();
crons.interval("job name", { hours: 2 }, internal.crons.myFunc, {});
export default crons;
```

Only use `crons.interval` or `crons.cron`. NOT `crons.hourly/daily/weekly`.

## File Storage

```typescript
const url = await ctx.storage.getUrl(storageId); // Returns signed URL or null

// Get metadata via system table
const metadata = await ctx.db.system.get(storageId);
// Returns: { _id, _creationTime, contentType?, sha256, size }
```

## TypeScript

- Use `Id<'tableName'>` from `./_generated/dataModel` for typed IDs
- `as const` for string literals in unions
- Add `@types/node` to package.json when using Node.js modules

```typescript
import { Id } from "./_generated/dataModel";
const idToName: Record<Id<"users">, string> = {};
```

## Examples

- **Chat app with AI**: See [chat-app-example.md](references/chat-app-example.md)
