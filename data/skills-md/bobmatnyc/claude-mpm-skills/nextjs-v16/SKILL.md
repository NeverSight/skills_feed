---
name: nextjs-v16
description: Next.js 16 migration guide (async request APIs, "use cache", Turbopack)
version: 1.1.0
category: toolchain
progressive_disclosure:
  entry_point:
    summary: "Next.js 16 migration: async request APIs + opt-in caching"
tags: [nextjs, nextjs-16]
---

# Next.js 16

- Async `params`/`cookies`/`headers`; opt-in caching via `"use cache"`; Turbopack default.

Anti-patterns:

- ❌ Sync request APIs; ✅ `await` `params`, `cookies()`, and `headers()`.
- ❌ Keep `middleware.ts`; ✅ use `proxy.ts` and `export function proxy`.
- ❌ `revalidateTag("posts")`; ✅ `revalidateTag("posts", "max")` or `{ expire: ... }`.

References: `references/migration-checklist.md`, `references/cache-components.md`, `references/turbopack.md`
