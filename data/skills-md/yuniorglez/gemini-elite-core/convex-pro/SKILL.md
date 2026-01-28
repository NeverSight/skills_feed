---
name: convex-pro
description: Senior Backend Architect for Convex.dev (2026). Specialized in reactive database design, type-safe full-stack synchronization, and hardened authorization patterns. Expert in building low-latency, real-time applications using Convex v2+ features like RLS (Row Level Security), HTTP Actions, File Storage, and advanced indexing.
---

# ⚡ Skill: convex-pro (v1.0.0)

## Executive Summary
Senior Backend Architect for Convex.dev (2026). Specialized in reactive database design, type-safe full-stack synchronization, and hardened authorization patterns. Expert in building low-latency, real-time applications using Convex v2+ features like RLS (Row Level Security), HTTP Actions, File Storage, and advanced indexing.

---

## 📋 The Conductor's Protocol

1.  **Schema First**: Always define the data model in `convex/schema.ts` before writing functions.
2.  **Auth Validation**: Every public function MUST validate `ctx.auth.getUserIdentity()`.
3.  **Indexing**: Never use `.filter()` on unbounded datasets; define and use `.withIndex()`.
4.  **Transactionality**: Group related database operations into a single mutation to ensure consistency.

---

## 🛠️ Mandatory Protocols (2026 Standards)

### 1. Hardened Authorization (Beyond RLS)
While Convex supports RLS, the standard for 2026 is **Explicit Authorization at the Function Boundary**.
- **Rule**: Throw `ConvexError` with structured data for all unauthorized attempts.
- **Pattern**: Use "unguessable IDs" or `userId` from `getUserIdentity()` for all sensitive queries.

### 2. Reactive Query Efficiency
- **Rule**: Queries are reactive by default. Minimize the surface area of returned data to reduce bandwidth.
- **Pagination**: Use `paginationOpts` for all list-style queries expected to grow beyond 100 items.

### 3. Mutational Integrity (OCC)
Convex uses Optimistic Concurrency Control.
- **Rule**: Mutations must be **idempotent**. Check the current state of a document before patching or deleting to avoid redundant operations and handle retries gracefully.

---

## 🚀 Show, Don't Just Tell (Implementation Patterns)

### Quick Start: Hardened Mutation with Auth (React 19)
```tsx
// convex/tasks.ts
import { mutation } from "./_generated/server";
import { v, ConvexError } from "convex/values";

export const createTask = mutation({
  args: { title: v.string() },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) {
      throw new ConvexError({ code: "UNAUTHORIZED", message: "Login required" });
    }

    const taskId = await ctx.db.insert("tasks", {
      title: args.title,
      userId: identity.subject, // Unique provider ID (e.g. Clerk ID)
      completed: false,
    });
    
    return taskId;
  },
});
```

### Advanced Pattern: Transactional Internal Logic
```tsx
// convex/users.ts
import { internalMutation } from "./_generated/server";

export const _onboardUser = internalMutation({
  args: { userId: v.id("users") },
  handler: async (ctx, args) => {
    // Single transaction for atomicity
    await ctx.db.patch(args.userId, { status: "active" });
    await ctx.db.insert("logs", { type: "ONBOARDING_COMPLETE", userId: args.userId });
  }
});
```

---

## 🛡️ The Do Not List (Anti-Patterns)

1.  **DO NOT** use `npx convex deploy` unless specifically asked; use `npx convex dev` for local development.
2.  **DO NOT** use `Array.filter()` inside a query handler for large datasets. Use `ctx.db.query(...).withIndex(...)`.
3.  **DO NOT** pass `userId` as a plain argument from the client if it's used for security; always derive it from `ctx.auth.getUserIdentity()`.
4.  **DO NOT** use `ctx.runQuery` or `ctx.runMutation` inside an action if the logic can be moved to a single mutation. It breaks transactionality.
5.  **DO NOT** ignore return validators. Always specify `returns: v.any()` or a strict object schema.

---

## 📂 Progressive Disclosure (Deep Dives)

- **[Auth & RLS Strategies](./references/auth-rls.md)**: Integrating Clerk/Auth.js and enforcing access control.
- **[Advanced Indexing](./references/indexing.md)**: Search indexes, vector indexes (AI), and performance optimization.
- **[HTTP Actions & Webhooks](./references/http-actions.md)**: External API integration and Hono on Convex.
- **[File Storage Mastery](./references/storage.md)**: Large file uploads, transformations, and access URLs.

---

## 🛠️ Specialized Tools & Scripts

- `scripts/sync-schema.ts`: Automatically generates Zod schemas from your Convex data model.
- `scripts/audit-indexes.py`: Scans your functions to find queries without proper indexing.

---

## 🎓 Learning Resources
- [Convex Documentation](https://docs.convex.dev/)
- [Convex Templates (Next.js 16)](https://convex.dev/templates)
- [Convex Stack (Community Guide)](https://stack.convex.dev/)

---
*Updated: January 23, 2026 - 16:15*
