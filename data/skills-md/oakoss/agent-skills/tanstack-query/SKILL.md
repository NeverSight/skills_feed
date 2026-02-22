---
name: tanstack-query
description: |
  TanStack Query v5 server state management for React. Covers query/mutation patterns, v4-to-v5 migration (object syntax, gcTime, isPending, keepPreviousData), optimistic updates via useMutationState, SSR/hydration with HydrationBoundary, infinite queries, offline/PWA support, error boundaries with throwOnError, and React 19 Suspense integration.

  Use when building data fetching, fixing migration errors, debugging hydration mismatches, implementing caching strategies, or configuring mutations.
license: MIT
metadata:
  author: oakoss
  version: '1.4'
  source: 'https://tanstack.com/query/latest/docs'
---

# TanStack Query

## Overview

TanStack Query is an **async state manager**, not a data fetching library. You provide a `queryFn` that returns a Promise; React Query handles caching, deduplication, background updates, and stale data management.

**When to use:** Infinite scrolling, offline-first apps, auto-refetching on focus/reconnect, complex cache invalidation, React Native, hybrid server/client apps.

**When NOT to use:** Purely synchronous state (useState/Zustand), normalized GraphQL caching (Apollo/urql), server-components-only apps (native fetch), simple fetch-and-display (server components).

## Quick Reference

| Pattern           | API                                               | Key Points                             |
| ----------------- | ------------------------------------------------- | -------------------------------------- |
| Basic query       | `useQuery({ queryKey, queryFn })`                 | Include params in queryKey             |
| Suspense query    | `useSuspenseQuery(options)`                       | No `enabled` option allowed            |
| Parallel queries  | `useQueries({ queries, combine })`                | Dynamic parallel fetching              |
| Dependent query   | `useQuery({ enabled: !!dep })`                    | Wait for prerequisite data             |
| Query options     | `queryOptions({ queryKey, queryFn })`             | Reusable, type-safe config             |
| Basic mutation    | `useMutation({ mutationFn, onSuccess })`          | Invalidate on success                  |
| Mutation state    | `useMutationState({ filters, select })`           | Cross-component mutation tracking      |
| Optimistic update | `onMutate` -> cancel -> snapshot -> set           | Rollback in `onError`                  |
| Infinite query    | `useInfiniteQuery({ initialPageParam })`          | `initialPageParam` required in v5      |
| Prefetch          | `queryClient.prefetchQuery(options)`              | Preload on hover/intent                |
| Invalidation      | `queryClient.invalidateQueries({ queryKey })`     | Fuzzy-matches by default, active only  |
| Cancellation      | `queryFn: ({ signal }) => fetch(url, { signal })` | Auto-cancel on key change              |
| Select transform  | `select: (data) => data.filter(...)`              | Structural sharing preserved           |
| Skip token        | `queryFn: id ? () => fetch(id) : skipToken`       | Type-safe conditional disabling        |
| Serial mutations  | `useMutation({ scope: { id } })`                  | Same scope ID runs mutations in serial |

## v5 Migration Quick Reference

| v4 (Removed)                   | v5 (Use Instead)                           |
| ------------------------------ | ------------------------------------------ |
| `useQuery(key, fn, opts)`      | `useQuery({ queryKey, queryFn, ...opts })` |
| `cacheTime`                    | `gcTime`                                   |
| `isLoading` (no data)          | `isPending`                                |
| `keepPreviousData: true`       | `placeholderData: keepPreviousData`        |
| `onSuccess/onError` on queries | `useEffect` or mutation callbacks          |
| `useErrorBoundary`             | `throwOnError`                             |
| No `initialPageParam`          | `initialPageParam` required                |
| Error type `unknown`           | Error type defaults to `Error`             |

## Common Mistakes

| Mistake                                    | Correct Pattern                                           |
| ------------------------------------------ | --------------------------------------------------------- |
| Checking `isPending` before `data`         | Data-first: check `data` -> `error` -> `isPending`        |
| Copying server state to local useState     | Use data directly or derived state pattern                |
| Creating QueryClient in component          | Create once outside component or in useState              |
| Using `refetch()` for parameter changes    | Include params in queryKey, let it refetch automatically  |
| Same key for useQuery and useInfiniteQuery | Use distinct key segments (different cache structures)    |
| Inline select without memoization          | Extract to stable function or useCallback                 |
| Using `catch` without re-throwing          | Throw errors in queryFn (fetch doesn't reject on 4xx/5xx) |
| Manual generics on useQuery                | Type the queryFn return, let inference work               |
| Destructuring query for type narrowing     | Keep query object intact for proper narrowing             |
| Using `enabled` with `useSuspenseQuery`    | Use conditional rendering to mount/unmount component      |
| Not awaiting prefetch for SSR              | Await `prefetchQuery` to avoid hydration mismatches       |
| `invalidateQueries` not refetching all     | Use `refetchType: 'all'` for inactive queries             |

## Delegation

- **Query pattern discovery**: Use `Explore` agent
- **Cache strategy review**: Use `Task` agent
- **Code review**: Delegate to `code-reviewer` agent

> If the `tanstack-router` skill is available, delegate route loader and preloading patterns to it.
> If the `tanstack-form` skill is available, delegate form submission and mutation coordination to it.
> If the `tanstack-table` skill is available, delegate server-side table patterns to it.
> If the `tanstack-start` skill is available, delegate server functions and SSR data loading to it.
> If the `tanstack-devtools` skill is available, delegate query cache debugging and inspection to it.
> If the `tanstack-db` skill is available, delegate reactive client-side database and live query patterns to it.
> If the `tanstack-virtual` skill is available, delegate list virtualization and infinite scroll rendering to it.
> If the `tanstack-store` skill is available, delegate shared client-side reactive state management to it.
> If the `electricsql` skill is available, delegate ElectricSQL real-time Postgres sync patterns to it.
> If the `local-first` skill is available, delegate local-first architecture decisions and sync engine selection to it.

## References

- [Basic patterns, architecture, and query variants](references/basic-patterns.md)
- [Query keys and factory patterns](references/query-keys.md)
- [Mutations, optimistic updates, and MutationCache](references/mutations.md)
- [Cache operations, staleTime vs gcTime, seeding](references/caching.md)
- [Data transformations and select patterns](references/data-transformations.md)
- [Performance optimization with render tracking and structural sharing](references/performance.md)
- [Error handling strategies](references/error-handling.md)
- [Infinite queries and pagination](references/infinite-queries.md)
- [Offline mode and persistence](references/offline-mode.md)
- [WebSocket and real-time integration](references/websocket-integration.md)
- [SSR and hydration patterns](references/ssr-hydration.md)
- [TypeScript patterns](references/typescript-patterns.md)
- [Testing with MSW and React Testing Library](references/testing.md)
- [Known v5 issues and workarounds](references/known-issues.md)
- [Caching coordination with Router](references/caching-coordination.md) — single-source caching strategy, disabling Router cache, coordinated configuration
