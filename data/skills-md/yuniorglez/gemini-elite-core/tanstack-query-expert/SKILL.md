---
name: tanstack-query-expert
description: Senior Server State Architect for TanStack Query v5 (2026). Specialized in reactive data fetching, advanced caching, and high-performance integration with React 19 and Next.js 16. Expert in eliminating waterfalls, managing complex mutation states, and leveraging platform-level caching via Next.js `"use cache"` and Partial Prerendering (PPR).
---

# 📡 Skill: tanstack-query-expert (v1.0.0)

## Executive Summary
Senior Server State Architect for TanStack Query v5 (2026). Specialized in reactive data fetching, advanced caching, and high-performance integration with React 19 and Next.js 16. Expert in eliminating waterfalls, managing complex mutation states, and leveraging platform-level caching via Next.js `"use cache"` and Partial Prerendering (PPR).

---

## 📋 The Conductor's Protocol

1.  **Architecture Choice**: Determine if data fetching should happen in RSC (via React 19 `use` hook + `"use cache"`) or on the client (via TanStack Query).
2.  **Hydration Strategy**: For SSR/PPR, always prefetch on the server and use `HydrationBoundary` to ensure instant client-side data availability.
3.  **Mutation Tracking**: Use `useMutationState` to handle global loading/pending states without prop drilling.
4.  **Verification**: Use TanStack Query Devtools v5 to audit query states, stale times, and cache invalidation.

---

## 🛠️ Mandatory Protocols (2026 Standards)

### 1. The "Object Syntax" Rule
TanStack Query v5 ONLY supports the object-based syntax for all hooks.
- **Rule**: Never use the deprecated positional argument syntax (e.g., `useQuery(key, fn)`).
- **Correct**: `useQuery({ queryKey: [...], queryFn: ... })`.

### 2. React 19 & Next.js 16 Integration
- **PPR First**: Wrap client components using TanStack Query in `<Suspense>` to allow Next.js 16 to stream content while serving the static shell.
- **"use cache" Directive**: For server-side prefetching, utilize Next.js 16's `"use cache"` to cache the prefetch results at the platform level.
- **Action Mutations**: Prefer React 19 Actions for simple form mutations; use TanStack Query mutations for complex state, optimistic updates, and background refetching.

### 3. Cache & Performance Hardening
- **Stale Time**: Default to at least `5000` (5s) to prevent excessive refetching.
- **GC Time**: Use `gcTime` (renamed from `cacheTime` in v5) to manage memory cleanup.
- **Query Keys**: Always use stable, array-based query keys. Treat keys as unique identifiers for your data.

---

## 🚀 Show, Don't Just Tell (Implementation Patterns)

### Quick Start: Modern Query with Suspense (React 19)
```tsx
"use client";

import { useSuspenseQuery } from "@tanstack/react-query";
import { queryOptions } from "@tanstack/react-query";

// Pattern: Reusable Query Options
export const userOptions = (id: string) => queryOptions({
  queryKey: ["users", id],
  queryFn: async () => {
    const res = await fetch(`/api/users/${id}`);
    if (!res.ok) throw new Error("Failed to fetch");
    return res.json();
  },
  staleTime: 1000 * 60 * 5, // 5 min
});

export function UserProfile({ id }: { id: string }) {
  // Guaranteed data availability via Suspense
  const { data: user } = useSuspenseQuery(userOptions(id));

  return <div>Welcome, {user.name}</div>;
}
```

### Advanced Pattern: Global Mutation Tracking
```tsx
import { useMutationState } from "@tanstack/react-query";

function PendingUploads() {
  const pendingVariables = useMutationState({
    filters: { status: "pending", mutationKey: ["upload"] },
    select: (mutation) => mutation.state.variables as { fileName: string },
  });

  return (
    <ul>
      {pendingVariables.map((vars, i) => (
        <li key={i} className="opacity-50 italic text-blue-400">
          Uploading {vars.fileName}...
        </li>
      ))}
    </ul>
  );
}
```

---

## 🛡️ The Do Not List (Anti-Patterns)

1.  **DO NOT** use `onSuccess`, `onError`, or `onSettled` in `useQuery`. They are removed in v5. Use `useEffect` or move logic to `queryFn`.
2.  **DO NOT** ignore `isPending`. It replaced `isLoading` in v5 for "no data yet" states.
3.  **DO NOT** use `useQuery` without a `queryKey`. It's the only way to manage the cache effectively.
4.  **DO NOT** forget to `await` prefetchQuery on the server. Non-awaited prefetches lead to hydration mismatches.
5.  **DO NOT** use `enabled` with `useSuspenseQuery`. It's incompatible with the guarantee of data presence.

---

## 📂 Progressive Disclosure (Deep Dives)

- **[v5 Migration & Breaking Changes](./references/migration.md)**: Moving from v4 to v5 safely.
- **[Next.js 16 SSR & Hydration](./references/ssr-hydration.md)**: Prefetching, `HydrationBoundary`, and `"use cache"`.
- **[Advanced Mutations & Optimistic UI](./references/mutations.md)**: useMutationState and simplified v5 patterns.
- **[Performance & Infinite Queries](./references/performance-infinite.md)**: maxPages and bi-directional pagination.

---

## 🛠️ Specialized Tools & Scripts

- `scripts/audit-query-keys.ts`: Checks for non-array query keys or unstable key generation.
- `scripts/generate-query-hook.py`: Boilerplate generator for v5 query/mutation pairs.

---

## 🎓 Learning Resources
- [TanStack Query Docs](https://tanstack.com/query/latest)
- [TkDodo's Blog (Maintainer)](https://tkdodo.eu/blog/)
- [React 19 Data Fetching Guide](https://react.dev/reference/react/use)

---
*Updated: January 23, 2026 - 16:45*
