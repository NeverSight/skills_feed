---
name: tanstack-query
description: |
  TanStack Query (React Query) v5 best practices for data fetching, caching, mutations, and server state management.
  Use when building data-driven React applications, setting up query configurations, implementing mutations/optimistic updates,
  configuring caching strategies, integrating with SSR, or fixing v4→v5 migration errors.
metadata:
  tags: tanstack-query, react-query, data-fetching, caching, mutations, server-state, react, typescript
---

# TanStack Query v5

**Version**: @tanstack/react-query@5.90.x
**Requires**: React 18.0+, TypeScript 4.7+

## v5 New Features

- **useMutationState** — cross-component mutation tracking without prop drilling
- **Simplified optimistic updates** — via `variables` from pending mutations, no cache manipulation needed
- **throwOnError** — renamed from `useErrorBoundary`
- **networkMode** — offline/PWA support (`online` | `always` | `offlineFirst`)
- **useQueries with combine** — merge parallel query results into single object
- **infiniteQueryOptions** — type-safe factory for infinite queries (parallel to `queryOptions`)
- **maxPages** — limit pages in cache for infinite queries (requires bi-directional pagination)
- **Mutation callback signature change (v5.89+)** — `onError`/`onSuccess`/`onSettled` now receive 4 params (added `onMutateResult`)

## Quick Setup

```bash
npm install @tanstack/react-query@latest @tanstack/react-query-devtools@latest
```

```tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 min
      gcTime: 1000 * 60 * 60,   // 1 hour
      refetchOnWindowFocus: false,
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <YourApp />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  )
}
```

### Unified Devtools (Recommended with Multiple TanStack Libraries)

If using Query + Router (or other TanStack libraries), use the unified `TanStackDevtools` shell instead of individual devtools components:

```bash
npm install -D @tanstack/react-devtools
```

```tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtoolsPanel } from '@tanstack/react-query-devtools'
import { TanStackDevtools } from '@tanstack/react-devtools'

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <YourApp />
      <TanStackDevtools
        config={{ position: 'bottom-right' }}
        plugins={[
          { name: 'TanStack Query', render: <ReactQueryDevtoolsPanel /> },
          // Add more plugins: Router, etc.
        ]}
      />
    </QueryClientProvider>
  )
}
```

Use `*Panel` variants (`ReactQueryDevtoolsPanel`, `TanStackRouterDevtoolsPanel`) when embedding inside `TanStackDevtools`.

```tsx
import { useQuery, useMutation, useQueryClient, queryOptions } from '@tanstack/react-query'

const todosQueryOptions = queryOptions({
  queryKey: ['todos'],
  queryFn: async () => {
    const res = await fetch('/api/todos')
    if (!res.ok) throw new Error('Failed to fetch')
    return res.json()
  },
})

function useTodos() {
  return useQuery(todosQueryOptions)
}

function useAddTodo() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: async (newTodo: { title: string }) => {
      const res = await fetch('/api/todos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newTodo),
      })
      if (!res.ok) throw new Error('Failed to add')
      return res.json()
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] })
    },
  })
}
```

## Rule Categories

| Priority | Category | Rule File | Impact |
|----------|----------|-----------|--------|
| CRITICAL | Query Keys | `rules/qk-query-keys.md` | Prevents cache bugs and data inconsistencies |
| CRITICAL | Caching | `rules/cache-configuration.md` | Optimizes performance and data freshness |
| HIGH | Invalidation | `rules/cache-invalidation.md` | Ensures stale data is properly refreshed |
| HIGH | Mutations | `rules/mut-basics.md` | Ensures data integrity after writes |
| HIGH | Optimistic Updates | `rules/mut-optimistic-updates.md` | Responsive UI during mutations |
| HIGH | Error Handling | `rules/err-error-handling.md` | Prevents poor user experiences |
| MEDIUM | Prefetching | `rules/pf-prefetching.md` | Improves perceived performance |
| MEDIUM | Infinite Queries | `rules/inf-infinite-queries.md` | Prevents pagination bugs |
| MEDIUM | SSR/Hydration | `rules/ssr-hydration.md` | Enables proper server rendering |
| MEDIUM | Parallel Queries | `rules/parallel-queries.md` | Dynamic parallel fetching |
| LOW | Performance | `rules/perf-optimization.md` | Reduces unnecessary re-renders |
| LOW | Offline Support | `rules/offline-support.md` | Enables offline-first patterns |

## Critical Rules

### Always Do

- **Object syntax for all hooks**: `useQuery({ queryKey, queryFn, ...options })`
- **Array query keys**: `['todos']`, `['todos', id]`, `['todos', { filter }]`
- **Throw errors in queryFn**: `if (!res.ok) throw new Error('Failed')`
- **isPending for initial loading**: `if (isPending) return <Loading />`
- **Invalidate after mutations**: `onSuccess: () => queryClient.invalidateQueries({ queryKey: ['todos'] })`
- **queryOptions factory**: reuse across `useQuery`, `useSuspenseQuery`, `prefetchQuery`
- **gcTime (not cacheTime)**: renamed in v5

### Never Do

- **v4 array/function syntax**: `useQuery(['todos'], fetchTodos)` — removed in v5
- **Query callbacks**: `onSuccess`/`onError`/`onSettled` removed from queries (still work in mutations) — use `useEffect` instead
- **isLoading for "no data yet"**: meaning changed in v5 — use `isPending`
- **enabled with useSuspenseQuery**: not available — use conditional rendering
- **keepPreviousData**: removed — use `placeholderData: keepPreviousData`
- **refetch() for changed parameters**: include params in queryKey instead, query auto-refetches

## v4→v5 Migration Cheatsheet

| v4 | v5 | Notes |
|----|-----|-------|
| `useQuery(['key'], fn, opts)` | `useQuery({ queryKey, queryFn, ...opts })` | Object syntax only |
| `cacheTime` | `gcTime` | Renamed |
| `isLoading` (no data) | `isPending` | `isLoading` = `isPending && isFetching` |
| `keepPreviousData: true` | `placeholderData: keepPreviousData` | Import `keepPreviousData` helper |
| `useErrorBoundary` | `throwOnError` | Renamed |
| `onSuccess/onError/onSettled` on queries | Removed | Use `useEffect` for side effects |
| `pageParam = 0` default | `initialPageParam: 0` | Required for infinite queries |
| `status: 'loading'` | `status: 'pending'` | Renamed |
| `onError(err, vars, ctx)` | `onError(err, vars, onMutateResult, ctx)` | v5.89+ added 4th param |

## Known Issues (v5.90.x)

- **Streaming SSR hydration mismatch** — `void prefetchQuery` + `useSuspenseQuery` with conditional `isFetching` render causes hydration errors. Workaround: `await` prefetch or don't render based on `fetchStatus`
- **useQuery hydration error with prefetching** — `useQuery` + server prefetch can mismatch `isLoading` between server/client. Use `useSuspenseQuery` instead
- **refetchOnMount ignored for errored queries** — errors are always stale. Use `retryOnMount: false` in addition to `refetchOnMount: false`
- **useMutationState types** — `mutation.state.variables` typed as `unknown` due to fuzzy matching. Cast explicitly in `select` callback
- **invalidateQueries only refetches active queries** — use `refetchType: 'all'` to include inactive queries
- **Readonly query keys break in v5.90.8** — fixed in v5.90.9+

## Key Patterns

```tsx
// Dependent queries (B waits for A)
const { data: user } = useQuery({ queryKey: ['user', id], queryFn: () => fetchUser(id) })
const { data: posts } = useQuery({
  queryKey: ['posts', user?.id],
  queryFn: () => fetchPosts(user!.id),
  enabled: !!user,
})

// Parallel queries
const results = useQueries({
  queries: ids.map(id => ({ queryKey: ['item', id], queryFn: () => fetchItem(id) })),
  combine: (results) => ({ data: results.map(r => r.data), pending: results.some(r => r.isPending) }),
})

// Prefetch on hover
const handleHover = () => queryClient.prefetchQuery({ queryKey: ['item', id], queryFn: () => fetchItem(id) })

// Infinite scroll
useInfiniteQuery({
  queryKey: ['posts'],
  queryFn: ({ pageParam }) => fetchPosts(pageParam),
  initialPageParam: 0,
  getNextPageParam: (lastPage) => lastPage.nextCursor,
})

// Query cancellation
queryFn: async ({ signal }) => {
  const res = await fetch(`/api/search?q=${query}`, { signal })
  return res.json()
}

// Data transformation
useQuery({ queryKey: ['todos'], queryFn: fetchTodos, select: (data) => data.filter(t => t.completed) })
```
