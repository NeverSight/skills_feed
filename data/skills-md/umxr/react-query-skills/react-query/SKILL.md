---
name: react-query
description: TanStack Query (React Query) best practices and patterns from TkDodo's authoritative guides. Use when writing, reviewing, or debugging React Query code including queries, mutations, caching, optimistic updates, and TypeScript integration. Triggers on useQuery, useMutation, useInfiniteQuery, QueryClient, queryKey, staleTime, cacheTime, gcTime, invalidateQueries, or React Query patterns.
license: MIT
metadata:
  author: community
  version: "1.0.0"
  source: "TkDodo's Blog (tkdodo.eu)"
---

# TanStack Query (React Query) Best Practices

Comprehensive guide for TanStack Query based on TkDodo's authoritative blog posts. TkDodo (Dominik Dorfmeister) is a core maintainer of TanStack Query. Contains patterns across 17 categories covering queries, mutations, caching, TypeScript, testing, and advanced patterns.

## When to Apply

Reference these guidelines when:
- Writing new `useQuery`, `useMutation`, or `useInfiniteQuery` hooks
- Structuring query keys for a feature or application
- Implementing optimistic updates or cache synchronization
- Debugging unexpected refetches or stale data issues
- Integrating React Query with TypeScript
- Testing components that use React Query
- Deciding between React Query and other solutions

## Rule Categories by Priority

| Priority | Category | Impact | Key Concept |
|----------|----------|--------|-------------|
| 1 | Mental Model | CRITICAL | React Query is an async state manager, not a fetching library |
| 2 | Query Keys | CRITICAL | Keys are dependencies - include all variables that affect data |
| 3 | Status Handling | HIGH | Check data first, then error, then loading |
| 4 | Mutations | HIGH | Invalidation vs direct cache updates, optimistic patterns |
| 5 | TypeScript | HIGH | Prefer inference over explicit generics |
| 6 | Cache Management | MEDIUM-HIGH | placeholderData vs initialData, seeding strategies |
| 7 | Error Handling | MEDIUM-HIGH | Global callbacks, Error Boundaries, granular throwOnError |
| 8 | Render Optimization | MEDIUM | Tracked queries, structural sharing, select |
| 9 | Testing | MEDIUM | Fresh QueryClient per test, disable retries, use MSW |
| 10 | Advanced Patterns | LOW-MEDIUM | WebSockets, Router integration, Infinite queries |

---

## Quick Reference

### 1. Core Mental Model (CRITICAL)

- `mental-not-fetching-lib` - React Query is an async state manager, not a fetching library
- `mental-server-vs-client` - Server state is borrowed; client state is owned
- `mental-stale-time` - staleTime controls when data becomes eligible for background refetch
- `mental-gc-time` - gcTime controls when inactive cache entries are garbage collected
- `mental-no-sync-to-state` - Never copy query data to local state with useState/useEffect

### 2. Query Keys (CRITICAL)

- `keys-array-format` - Always use array keys: `['todos']` not `'todos'`
- `keys-generic-to-specific` - Structure from most generic to most specific
- `keys-include-dependencies` - Include all variables that determine what data to fetch
- `keys-factory-pattern` - Use query key factories for consistency and type safety
- `keys-exact-match` - Keys must match exactly: `['item', '1']` !== `['item', 1]`

### 3. Status Handling (HIGH)

- `status-data-first` - Check data availability before error state
- `status-avoid-status-first` - Don't hide cached data during background refetch errors
- `status-fetch-status` - Use fetchStatus for paused/fetching states separate from data status

### 4. Mutations (HIGH)

- `mutation-invalidation` - Prefer invalidation over direct cache updates for safety
- `mutation-return-promise` - Return invalidation promises to keep mutations in loading state
- `mutation-prefer-mutate` - Prefer mutate() over mutateAsync() to avoid manual error handling
- `mutation-single-arg` - Mutations accept one variable - use objects for multiple values
- `mutation-callback-lifecycle` - Query logic in useMutation callbacks; UI actions in mutate() callbacks
- `mutation-optimistic-when` - Use optimistic updates for high-confidence toggles, not navigation

### 5. TypeScript (HIGH)

- `ts-prefer-inference` - Let TypeScript infer from well-typed queryFn return types
- `ts-no-destructure` - Keep query object intact for proper type narrowing
- `ts-query-options` - Use queryOptions() helper for type-safe reusable query definitions
- `ts-factories-with-options` - Combine key factories with queryOptions for full type safety

### 6. Cache Management (MEDIUM-HIGH)

- `cache-placeholder-vs-initial` - placeholderData for fake data; initialData for real cached data
- `cache-initial-data-updated-at` - Specify initialDataUpdatedAt for proper stale time calculation
- `cache-seed-pull` - Pull from list cache to detail cache with initialData
- `cache-seed-push` - Push to detail caches after fetching lists with setQueryData
- `cache-prefetch` - Use prefetchQuery in loaders or on hover for instant navigation

### 7. Error Handling (MEDIUM-HIGH)

- `error-boundaries` - Use throwOnError with Error Boundaries for critical errors
- `error-granular-throw` - Use function throwOnError for selective error boundary routing
- `error-global-callbacks` - Use QueryCache onError for background refetch toasts
- `error-fetch-api` - Check response.ok with fetch API - it doesn't reject on 4xx/5xx
- `error-rethrow` - Always re-throw errors after logging in catch blocks

### 8. Render Optimization (MEDIUM)

- `render-tracked-queries` - Use tracked queries (default v4+) for automatic optimization
- `render-select` - Use select option for computed data and partial subscriptions
- `render-structural-sharing` - Leverage structural sharing; disable for large datasets
- `render-no-spread` - Avoid spreading query result to preserve tracked query benefits

### 9. Testing (MEDIUM)

- `test-fresh-client` - Create new QueryClient for each test for isolation
- `test-disable-retries` - Set retry: false in test configuration
- `test-use-msw` - Use Mock Service Worker for network mocking
- `test-wait-for` - Use waitFor with expect() for async assertions

### 10. Advanced Patterns (LOW-MEDIUM)

- `advanced-websocket-invalidate` - Use WebSocket events to invalidateQueries
- `advanced-ws-stale-time` - Set high staleTime when WebSockets handle updates
- `advanced-router-loader` - Combine router loaders with React Query caching
- `advanced-infinite-page-param` - Use getNextPageParam returning null for end of list
- `advanced-context-provider` - Use Context to guarantee data availability without undefined
- `advanced-suspense-query` - Use useSuspenseQuery for guaranteed data in components

---

## Detailed Rules

### mental-not-fetching-lib
React Query is agnostic about how you fetch. It only needs a Promise that resolves or rejects. Handle baseURLs, headers, and GraphQL in your data layer.

### mental-server-vs-client
Server state is a snapshot you don't own - other users can modify it. Client state (dark mode, UI toggles) is synchronous and yours. Treating them the same leads to problems.

### keys-factory-pattern
```typescript
const todoKeys = {
  all: ['todos'] as const,
  lists: () => [...todoKeys.all, 'list'] as const,
  list: (filters: Filters) => [...todoKeys.lists(), { filters }] as const,
  details: () => [...todoKeys.all, 'detail'] as const,
  detail: (id: number) => [...todoKeys.details(), id] as const,
}
```

### status-data-first
```typescript
// Correct: prioritize cached data
if (query.data) return <Content data={query.data} />
if (query.error) return <Error error={query.error} />
return <Loading />
```

### mutation-return-promise
```typescript
// Correct: mutation stays loading during invalidation
onSuccess: () => queryClient.invalidateQueries({ queryKey: ['todos'] })

// Wrong: mutation completes before invalidation
onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['todos'] }) }
```

### ts-query-options
```typescript
const todosQuery = queryOptions({
  queryKey: ['todos'],
  queryFn: fetchTodos,
})

// Reusable and type-safe
useQuery(todosQuery)
queryClient.prefetchQuery(todosQuery)
const data = queryClient.getQueryData(todosQuery.queryKey) // Typed!
```

### cache-placeholder-vs-initial
- **placeholderData**: Observer-level, never cached, always refetches, use for "fake" data
- **initialData**: Cache-level, persisted, respects staleTime, use for "real" data from other cache entries

### error-global-callbacks
```typescript
const queryClient = new QueryClient({
  queryCache: new QueryCache({
    onError: (error, query) => {
      // Only toast for background refetch failures (has existing data)
      if (query.state.data !== undefined) {
        toast.error(`Background update failed: ${error.message}`)
      }
    },
  }),
})
```

### advanced-router-loader
```typescript
// Loader
export const loader = (queryClient: QueryClient) =>
  async ({ params }: LoaderFunctionArgs) => {
    const query = todoQuery(params.id!)
    return queryClient.getQueryData(query.queryKey) ??
           await queryClient.fetchQuery(query)
  }

// Component - instant data from loader, background updates from React Query
const { data } = useQuery({ ...todoQuery(id), initialData: useLoaderData() })
```

---

## Anti-Patterns to Avoid

### Don't sync to local state
```typescript
// Anti-pattern
const { data } = useQuery({...})
const [localData, setLocalData] = useState(data)
useEffect(() => { setLocalData(data) }, [data])

// Correct: use data directly, or use select for transformations
const { data } = useQuery({...})
```

### Don't use QueryCache as state manager
`setQueryData` is for optimistic updates and mutation responses only. Background refetches will override manually-set data.

### Don't create unstable QueryClient
```typescript
// Wrong: recreates on every render
function App() {
  const queryClient = new QueryClient()
  return <QueryClientProvider client={queryClient}>...</QueryClientProvider>
}

// Correct: stable reference
const queryClient = new QueryClient()
function App() {
  return <QueryClientProvider client={queryClient}>...</QueryClientProvider>
}
```

---

## When NOT to Use React Query

1. **React Server Components**: Use framework-native data fetching
2. **Next.js/Remix with simple needs**: Built-in solutions may suffice
3. **GraphQL with normalized cache needs**: Consider Apollo Client or urql
4. **No background refetch requirements**: Static SSR may be enough

---

## Resources

- **Official docs**: https://tanstack.com/query
- **TkDodo's blog**: https://tkdodo.eu/blog (authoritative source for best practices)
- **Key articles**: Practical React Query, Thinking in React Query, Effective React Query Keys

For complete explanations and code examples, see `references/react-query-context-source.md`
