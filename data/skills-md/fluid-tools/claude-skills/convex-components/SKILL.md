---
name: convex-components
description: "Guide for authoring Convex components - isolated, reusable backend modules with their own schema and functions. Use when building reusable libraries, packaging Convex functionality for NPM, creating isolated sub-systems, or integrating third-party components. Activates for component authoring, convex.config.ts setup, component testing, or NPM publishing tasks."
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Authoring Convex Components

## Overview

Convex components are isolated, reusable backend modules that can be packaged and shared. Each component has its own schema, functions, and namespace, enabling modular architecture and library distribution via NPM.

## TypeScript: NEVER Use `any` Type

**CRITICAL RULE:** This codebase has `@typescript-eslint/no-explicit-any` enabled. Using `any` will cause build failures.

## When to Use This Skill

Use this skill when:

- Building reusable backend modules for your app
- Packaging Convex functionality for NPM distribution
- Creating isolated sub-systems with separate schemas
- Integrating third-party Convex components
- Building libraries with Convex backends (rate limiters, workpools, etc.)

## Component Types

| Type         | Use Case                        | Location                       |
| ------------ | ------------------------------- | ------------------------------ |
| **Local**    | Private modules within your app | `convex/myComponent/`          |
| **Packaged** | Published NPM packages          | `node_modules/@org/component/` |
| **Hybrid**   | Shared internal packages        | `packages/my-component/`       |

## Component Anatomy

### Directory Structure

```
my-component/
├── package.json           # NPM package config
├── src/
│   └── component/
│       ├── convex.config.ts    # Component definition
│       ├── schema.ts           # Component schema
│       ├── public.ts           # Public API functions
│       ├── internal.ts         # Internal functions
│       └── _generated/         # Generated types (gitignored)
└── src/
    └── client/
        └── index.ts            # Client-side wrapper class
```

### convex.config.ts

The component definition file:

```typescript
// src/component/convex.config.ts
import { defineComponent } from "convex/server";

export default defineComponent("myComponent");
```

### Component Schema

```typescript
// src/component/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  items: defineTable({
    key: v.string(),
    value: v.string(),
    expiresAt: v.optional(v.number()),
  }).index("by_key", ["key"]),
});
```

### Public API Functions

```typescript
// src/component/public.ts
import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

export const set = mutation({
  args: {
    key: v.string(),
    value: v.string(),
    ttl: v.optional(v.number()),
  },
  returns: v.null(),
  handler: async (ctx, args) => {
    const existing = await ctx.db
      .query("items")
      .withIndex("by_key", (q) => q.eq("key", args.key))
      .unique();

    const data = {
      key: args.key,
      value: args.value,
      expiresAt: args.ttl ? Date.now() + args.ttl : undefined,
    };

    if (existing) {
      await ctx.db.replace(existing._id, data);
    } else {
      await ctx.db.insert("items", data);
    }

    return null;
  },
});

export const get = query({
  args: { key: v.string() },
  returns: v.union(v.string(), v.null()),
  handler: async (ctx, args) => {
    const item = await ctx.db
      .query("items")
      .withIndex("by_key", (q) => q.eq("key", args.key))
      .unique();

    if (!item) return null;
    if (item.expiresAt && item.expiresAt < Date.now()) return null;

    return item.value;
  },
});
```

## Installing Components in Host App

### Host App convex.config.ts

```typescript
// convex/convex.config.ts
import { defineApp } from "convex/server";
import myComponent from "@org/my-component/convex.config";

const app = defineApp();
app.use(myComponent, { name: "cache" }); // Mount with a name

export default app;
```

### Accessing Component Functions

```typescript
// convex/myFunctions.ts
import { mutation } from "./_generated/server";
import { components } from "./_generated/api";
import { v } from "convex/values";

export const cacheValue = mutation({
  args: { key: v.string(), value: v.string() },
  returns: v.null(),
  handler: async (ctx, args) => {
    // Call component function via components.<name>.<module>.<function>
    await ctx.runMutation(components.cache.public.set, {
      key: args.key,
      value: args.value,
      ttl: 3600000, // 1 hour
    });
    return null;
  },
});
```

## Key Differences from Regular Convex

### 1. Id Types Are Opaque

Component IDs are branded strings, not `Id<"table">`:

```typescript
// ❌ WRONG: Can't use Id<"items"> from component
import { Id } from "./_generated/dataModel";
const id: Id<"items"> = ...;  // Error!

// ✅ CORRECT: Use string or branded type from component
export const processItem = mutation({
  args: { itemId: v.string() },  // Accept as string
  returns: v.null(),
  handler: async (ctx, args) => {
    // Pass to component functions as-is
    await ctx.runMutation(components.myComponent.public.process, {
      itemId: args.itemId,
    });
    return null;
  },
});
```

### 2. No Environment Variables

Components cannot access `process.env`. Pass configuration explicitly:

```typescript
// ✅ CORRECT: Component accepts config via function args
// src/component/public.ts
export const initialize = mutation({
  args: {
    apiKey: v.string(),
    endpoint: v.string(),
  },
  returns: v.null(),
  handler: async (ctx, args) => {
    await ctx.db.insert("config", {
      apiKey: args.apiKey,
      endpoint: args.endpoint,
    });
    return null;
  },
});

// Host app passes env vars
export const setup = mutation({
  args: {},
  returns: v.null(),
  handler: async (ctx) => {
    await ctx.runMutation(components.myComponent.public.initialize, {
      apiKey: process.env.API_KEY!,
      endpoint: process.env.API_ENDPOINT!,
    });
    return null;
  },
});
```

### 3. No ctx.auth

Components don't have access to authentication context. Pass user info explicitly:

```typescript
// ❌ WRONG: Components can't access ctx.auth
export const createItem = mutation({
  args: { data: v.string() },
  returns: v.null(),
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity(); // Error!
    return null;
  },
});

// ✅ CORRECT: Accept userId as argument
export const createItem = mutation({
  args: {
    userId: v.string(),
    data: v.string(),
  },
  returns: v.id("items"),
  handler: async (ctx, args) => {
    return await ctx.db.insert("items", {
      userId: args.userId,
      data: args.data,
    });
  },
});

// Host app handles auth and passes user info
export const createItemWithAuth = mutation({
  args: { data: v.string() },
  returns: v.string(),
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    const itemId = await ctx.runMutation(
      components.myComponent.public.createItem,
      {
        userId: identity.subject,
        data: args.data,
      }
    );

    return itemId; // Return as string
  },
});
```

### 4. Pagination Cursors Are Strings

Component pagination uses string cursors:

```typescript
// src/component/public.ts
export const list = query({
  args: {
    cursor: v.optional(v.string()),
    limit: v.number(),
  },
  returns: v.object({
    items: v.array(
      v.object({
        id: v.string(),
        data: v.string(),
      })
    ),
    nextCursor: v.union(v.string(), v.null()),
  }),
  handler: async (ctx, args) => {
    const results = await ctx.db
      .query("items")
      .paginate({ cursor: args.cursor ?? null, numItems: args.limit });

    return {
      items: results.page.map((item) => ({
        id: item._id,
        data: item.data,
      })),
      nextCursor: results.continueCursor,
    };
  },
});
```

## Client Code Patterns

### Class-Based Client Wrapper

Provide a convenient client class for host apps:

```typescript
// src/client/index.ts
import {
  FunctionReference,
  GenericMutationCtx,
  GenericQueryCtx,
} from "convex/server";
import { api } from "../component/_generated/api";

// Re-export the component config
export { default } from "../component/convex.config";

// Type for the installed component
type ComponentApi = typeof api;

export class MyComponentClient {
  private component: ComponentApi;

  constructor(component: ComponentApi) {
    this.component = component;
  }

  // Wrapper methods for cleaner API
  async set(
    ctx: GenericMutationCtx<Record<string, never>>,
    key: string,
    value: string,
    ttl?: number
  ): Promise<void> {
    await ctx.runMutation(this.component.public.set, { key, value, ttl });
  }

  async get(
    ctx: GenericQueryCtx<Record<string, never>>,
    key: string
  ): Promise<string | null> {
    return await ctx.runQuery(this.component.public.get, { key });
  }
}
```

### Host App Usage

```typescript
// convex/cache.ts
import { MyComponentClient } from "@org/my-component";
import { components } from "./_generated/api";
import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

const cache = new MyComponentClient(components.cache);

export const setValue = mutation({
  args: { key: v.string(), value: v.string() },
  returns: v.null(),
  handler: async (ctx, args) => {
    await cache.set(ctx, args.key, args.value, 3600000);
    return null;
  },
});

export const getValue = query({
  args: { key: v.string() },
  returns: v.union(v.string(), v.null()),
  handler: async (ctx, args) => {
    return await cache.get(ctx, args.key);
  },
});
```

## Building & Publishing

### package.json Setup

```json
{
  "name": "@org/my-component",
  "version": "1.0.0",
  "type": "module",
  "main": "./dist/client/index.js",
  "types": "./dist/client/index.d.ts",
  "exports": {
    ".": {
      "types": "./dist/client/index.d.ts",
      "import": "./dist/client/index.js"
    },
    "./convex.config": {
      "types": "./dist/component/convex.config.d.ts",
      "import": "./dist/component/convex.config.js"
    }
  },
  "files": ["dist", "src"],
  "scripts": {
    "build": "npm run build:esm && npm run build:cjs",
    "build:esm": "tsc --project tsconfig.json",
    "typecheck": "tsc --noEmit",
    "prepare": "npm run build"
  },
  "dependencies": {
    "convex": "^1.17.0"
  },
  "devDependencies": {
    "typescript": "^5.0.0"
  },
  "peerDependencies": {
    "convex": "^1.17.0"
  }
}
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### Generate Types Before Publishing

```bash
# In component directory
cd src/component
npx convex codegen

# Build the package
cd ../..
npm run build

# Publish
npm publish
```

## Testing Components

### Using convex-test

```typescript
// tests/component.test.ts
import { convexTest } from "convex-test";
import { describe, expect, it } from "vitest";
import schema from "../src/component/schema";
import { api } from "../src/component/_generated/api";

describe("MyComponent", () => {
  it("should set and get values", async () => {
    const t = convexTest(schema);

    // Set a value
    await t.mutation(api.public.set, {
      key: "test-key",
      value: "test-value",
    });

    // Get the value
    const result = await t.query(api.public.get, {
      key: "test-key",
    });

    expect(result).toBe("test-value");
  });

  it("should respect TTL expiration", async () => {
    const t = convexTest(schema);

    // Set with TTL of 0 (immediate expiry)
    await t.mutation(api.public.set, {
      key: "expiring-key",
      value: "expiring-value",
      ttl: -1000, // Already expired
    });

    // Should return null for expired item
    const result = await t.query(api.public.get, {
      key: "expiring-key",
    });

    expect(result).toBeNull();
  });
});
```

### Testing with Mock Data

```typescript
// tests/with-data.test.ts
import { convexTest } from "convex-test";
import { describe, expect, it } from "vitest";
import schema from "../src/component/schema";
import { api } from "../src/component/_generated/api";

describe("MyComponent with data", () => {
  it("should handle existing data", async () => {
    const t = convexTest(schema);

    // Seed data directly
    await t.run(async (ctx) => {
      await ctx.db.insert("items", {
        key: "seeded-key",
        value: "seeded-value",
      });
    });

    // Query should find seeded data
    const result = await t.query(api.public.get, {
      key: "seeded-key",
    });

    expect(result).toBe("seeded-value");
  });
});
```

## Local Component Pattern

For app-internal modularity without NPM publishing:

```
convex/
├── convex.config.ts           # Main app config
├── schema.ts                  # Main app schema
├── myLocalComponent/          # Local component
│   ├── convex.config.ts       # Component definition
│   ├── schema.ts              # Component schema
│   └── functions.ts           # Component functions
└── functions.ts               # Main app functions
```

```typescript
// convex/convex.config.ts
import { defineApp } from "convex/server";
import myLocalComponent from "./myLocalComponent/convex.config";

const app = defineApp();
app.use(myLocalComponent, { name: "localCache" });

export default app;
```

## Common Pitfalls

### Pitfall 1: Using Id Types from Component

**❌ WRONG:**

```typescript
import { Id } from "./_generated/dataModel";

export const getItem = query({
  args: { itemId: v.id("items") }, // ❌ Not accessible!
  handler: async (ctx, args) => {
    return await ctx.db.get(args.itemId);
  },
});
```

**✅ CORRECT:**

```typescript
export const getItem = query({
  args: { itemId: v.string() }, // ✅ Accept as string
  returns: v.union(
    v.object({
      id: v.string(),
      data: v.string(),
    }),
    v.null()
  ),
  handler: async (ctx, args) => {
    // Look up by index or iterate
    const item = await ctx.db
      .query("items")
      .filter((q) => q.eq(q.field("_id"), args.itemId))
      .first();

    if (!item) return null;
    return { id: item._id, data: item.data };
  },
});
```

### Pitfall 2: Accessing process.env in Component

**❌ WRONG:**

```typescript
// src/component/functions.ts
export const callApi = action({
  args: {},
  returns: v.null(),
  handler: async () => {
    // ❌ Components can't access process.env!
    const apiKey = process.env.API_KEY;
    await fetch("...", { headers: { Authorization: apiKey } });
    return null;
  },
});
```

**✅ CORRECT:**

```typescript
// src/component/functions.ts
export const callApi = action({
  args: { apiKey: v.string() }, // ✅ Accept as argument
  returns: v.null(),
  handler: async (ctx, args) => {
    await fetch("...", { headers: { Authorization: args.apiKey } });
    return null;
  },
});

// Host app passes env var
await ctx.runAction(components.myComponent.functions.callApi, {
  apiKey: process.env.API_KEY!,
});
```

### Pitfall 3: Expecting ctx.auth in Component

**❌ WRONG:**

```typescript
// src/component/functions.ts
export const userAction = mutation({
  args: { data: v.string() },
  returns: v.null(),
  handler: async (ctx, args) => {
    // ❌ Components don't have ctx.auth!
    const identity = await ctx.auth.getUserIdentity();
    return null;
  },
});
```

**✅ CORRECT:**

```typescript
// src/component/functions.ts
export const userAction = mutation({
  args: {
    userId: v.string(), // ✅ Accept user info as argument
    data: v.string(),
  },
  returns: v.null(),
  handler: async (ctx, args) => {
    await ctx.db.insert("userActions", {
      userId: args.userId,
      data: args.data,
    });
    return null;
  },
});

// Host app handles auth
export const doUserAction = mutation({
  args: { data: v.string() },
  returns: v.null(),
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    await ctx.runMutation(components.myComponent.functions.userAction, {
      userId: identity.subject,
      data: args.data,
    });
    return null;
  },
});
```

## Quick Reference

### Component Definition

```typescript
// convex.config.ts
import { defineComponent } from "convex/server";
export default defineComponent("componentName");
```

### Host App Installation

```typescript
// convex/convex.config.ts
import { defineApp } from "convex/server";
import myComponent from "@org/my-component/convex.config";

const app = defineApp();
app.use(myComponent, { name: "mountName" });
export default app;
```

### Calling Component Functions

```typescript
import { components } from "./_generated/api";

// In mutations/queries/actions
await ctx.runMutation(components.mountName.module.function, args);
await ctx.runQuery(components.mountName.module.function, args);
await ctx.runAction(components.mountName.module.function, args);
```

### Component Limitations

| Feature             | Available in Components? |
| ------------------- | ------------------------ |
| `ctx.db`            | Yes (own schema only)    |
| `ctx.auth`          | No                       |
| `process.env`       | No                       |
| `ctx.scheduler`     | Yes                      |
| `Id<"table">` types | No (use strings)         |
| Pagination cursors  | String only              |
