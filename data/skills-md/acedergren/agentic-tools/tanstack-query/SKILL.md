---
name: tanstack-query
version: 3.0.0
license: MIT
description: |
  TanStack Query v5 expert guidance - migration gotchas (v4→v5 breaking changes),
  performance pitfalls (infinite refetch loops, staleness traps), and decision
  frameworks (when NOT to use queries, SWR vs React Query trade-offs).

  Use when: (1) debugging v4→v5 migration errors (gcTime, isPending, throwOnError),
  (2) infinite refetch loops, (3) SSR hydration mismatches, (4) choosing between
  React Query vs SWR vs fetch, (5) optimistic update patterns not working.

  NOT for basic setup (see official docs). Focuses on non-obvious decisions and
  patterns that cause production issues.

  Triggers: React Query, TanStack Query, v5 migration, refetch loop, stale data,
  SSR hydration, query invalidation, optimistic updates debugging.
user-invocable: true
---

# TanStack Query v5 - Expert Troubleshooting

**Assumption**: You know `useQuery` basics. This covers what breaks in production.

---

## Before Using React Query: Strategic Assessment

**Ask yourself these questions BEFORE adding useQuery:**

### 1. Data Source Analysis
- **Where does this data come from?**
  - URL params/path → Framework loader (Next.js, Remix), not React Query
  - Computation/derivation → useMemo, not React Query
  - Form input → React Hook Form, not React Query
  - REST/GraphQL → React Query ✅

### 2. Update Frequency & Caching Strategy
- **How often does this data change?**
  - Real-time (>1/sec) → WebSocket + Zustand (React Query overhead too high)
  - Frequent (<1/min) → React Query with aggressive staleTime (30s-1min)
  - Moderate (5-30min) → React Query standard (staleTime: 5min)
  - Infrequent (>1hr) → React Query with long staleTime (30min+)

### 3. Cost of Stale Data
- **What happens if user sees old data?**
  - Critical (money, auth tokens) → staleTime: 0 (always fresh)
  - Important (user content, messages) → staleTime: 1-5min
  - Nice-to-have (analytics, recommendations) → staleTime: 30min+

---

## Critical Decision: When NOT to Use React Query

```
Need data fetching?
│
├─ Data from URL (search params, path) → DON'T use queries
│   └─ Use framework loaders (Next.js, Remix) or URL state
│      WHY: Queries cache by key, URL is already your cache key
│
├─ Derived/computed data → DON'T use queries
│   └─ Use useMemo or Zustand
│      WHY: No server, no stale data, no refetch needed
│
├─ Form state → DON'T use queries
│   └─ Use React Hook Form or controlled state
│      WHY: Forms are local state, not server cache
│
├─ WebSocket/realtime data → MAYBE use queries
│   ├─ High-frequency updates (> 1/sec) → DON'T use queries (use Zustand)
│   └─ Low-frequency (<1/min) → Use queries with manual updates
│      WHY: Queries designed for request/response, not streaming
│
└─ REST/GraphQL server state → USE queries
    (This is what React Query is for)
```

**The trap**: Developers use React Query for everything. It's a **server cache**, not a state manager.

---

## Breaking Changes: v4 → v5 Migration Gotchas

### ❌ #1: `cacheTime` Renamed to `gcTime`
**Problem**: Silent failure - code runs but cache doesn't work as expected

```typescript
// WRONG - v4 syntax, silently ignored in v5
useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  cacheTime: 10 * 60 * 1000,  // ❌ Ignored in v5
})

// CORRECT - v5 syntax
useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  gcTime: 10 * 60 * 1000,  // ✅ Garbage collection time
})
```

**Why it breaks**: TypeScript won't error if using `any` or loose types. Cache appears to work but garbage collects immediately.

**Why this is deceptively hard to debug**: No error messages—app runs perfectly. Cache appears functional initially. Only after 5+ minutes in production do you notice data refetching too frequently and Network tab lighting up. DevTools shows query has 0ms gcTime but you SET 10 minutes. The property is silently ignored—no warnings, no TypeScript errors. Takes 20-30 minutes of cache inspection comparing v4 docs to v5 docs to realize the property was renamed. Searches for "cacheTime not working" find v4 results, not v5 migration notes.

### ❌ #2: `isLoading` Removed, Use `isPending`
**Problem**: Loading spinners disappear too early

```typescript
// WRONG - v4 syntax
const { isLoading } = useQuery(...)
if (isLoading) return <Spinner />  // ❌ isLoading undefined in v5

// CORRECT - v5 syntax
const { isPending } = useQuery(...)
if (isPending) return <Spinner />  // ✅ Shows while query pending
```

**Why different**:
- `isLoading` (v4): `true` only for first fetch (no cached data)
- `isPending` (v5): `true` for first fetch + refetches (more accurate)

**Migration trap**: If you have cached data and refetch, `isPending` stays `true` but `isLoading` was `false`. UI shows stale data + spinner in v5.

**Why this is deceptively hard to debug**: `isLoading` is undefined but JavaScript doesn't error—`if (undefined)` is falsy, so spinner never shows. UI appears to work in initial testing (data loads fine). Only in specific edge case—user navigates away and back with cached data—does the bug appear: no loading state during refetch. Users report "page feels broken" but can't reproduce consistently. DevTools shows `isLoading: undefined` but that's easy to miss in large state object. Takes 15-20 minutes to realize v5 removed the property entirely and you need `isPending` instead.

### ❌ #3: `keepPreviousData` Removed, Use `placeholderData`
**Problem**: Pagination breaks - flickers on page change

```typescript
// WRONG - v4 syntax
useQuery({
  queryKey: ['todos', page],
  queryFn: () => fetchTodos(page),
  keepPreviousData: true,  // ❌ Removed in v5
})

// CORRECT - v5 syntax
useQuery({
  queryKey: ['todos', page],
  queryFn: () => fetchTodos(page),
  placeholderData: (previousData) => previousData,  // ✅ Function form
})
```

**Why it breaks**: `keepPreviousData: true` was boolean. `placeholderData` is data OR function. If you pass `true`, TypeScript error but runtime breaks.

### ❌ #4: Query Functions Must Return Non-Void
**Problem**: Mutations that don't return data break

```typescript
// WRONG - void return breaks v5
queryFn: async () => {
  await api.deleteTodo(id)  // ❌ Returns void
}

// CORRECT - return something
queryFn: async () => {
  await api.deleteTodo(id)
  return { success: true }  // ✅ Return data
}
```

**Why it breaks**: v5 type system requires `Promise<TData>`, not `Promise<void>`. Silent runtime error if using `any`.

---

## Performance Pitfalls

### ❌ Infinite Refetch Loop
**Problem**: Query refetches forever, browser freezes

```typescript
// WRONG - creates infinite loop
useQuery({
  queryKey: ['user', user],  // ❌ Object in key
  queryFn: () => fetchUser(user.id),
})

// WHY IT LOOPS:
// 1. Query runs, gets data
// 2. Component re-renders
// 3. New `user` object created (different reference)
// 4. Key changes → query refetches
// 5. Goto 1 (infinite)

// CORRECT - use primitive values
useQuery({
  queryKey: ['user', user.id],  // ✅ String is stable
  queryFn: () => fetchUser(user.id),
})
```

**Detection**: React DevTools shows component re-rendering every frame. Network tab shows identical requests hammering server.

**Why this is deceptively hard to debug**: Page loads fine initially—first query succeeds. Then browser tab becomes unresponsive. CPU spikes to 100%. Network tab shows 50+ identical requests per second. React DevTools Profiler is unusable (too many renders). The cause—object reference in queryKey—is invisible in the network requests (they all look identical). Error isn't obvious: no stack trace, no warning, just performance death. Takes 10-15 minutes to realize it's React Query, then another 10-15 to isolate which query. Only after adding `console.log` to every query do you see one logging hundreds of times. The fix (extract primitive from object) is obvious once found, but finding the culprit query in a codebase with 50+ queries is the hard part.

### ❌ Stale Data Trap
**Problem**: Data never updates despite changes on server

```typescript
// WRONG - data stuck in cache
useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  staleTime: Infinity,  // ❌ Never marks stale
})

// User adds todo on another tab → never sees it

// CORRECT - reasonable staleTime
useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  staleTime: 5 * 60 * 1000,  // ✅ 5 minutes
})
```

**Trade-off**:
- `staleTime: 0` → Refetch on every focus/mount (expensive)
- `staleTime: Infinity` → Never refetch (stale data)
- `staleTime: 5min` → Balance (refetch after 5min of inactivity)

**Why this is deceptively hard to debug**: Works perfectly in development—you refresh constantly, clearing cache. In production, users keep tabs open for hours. They report "data doesn't update" but you can't reproduce (your dev habits differ). When you check DevTools, query shows fresh data (because you just opened DevTools, triggering window focus refetch if you have default settings). The user's `staleTime: Infinity` is buried in a hook 3 files deep. No error, no warning. You check the API—returns fresh data. You check network—no requests being made (that's the clue, but easy to miss). Takes 20-30 minutes of user reproduction videos to notice they never see network requests after initial load. Only then do you search the codebase for `staleTime` settings.

### ❌ Over-Invalidation
**Problem**: Unrelated data refetches on every mutation

```typescript
// WRONG - nukes entire cache
onSuccess: () => {
  queryClient.invalidateQueries()  // ❌ Refetches EVERYTHING
}

// User updates profile → todos, posts, comments all refetch

// CORRECT - targeted invalidation
onSuccess: () => {
  queryClient.invalidateQueries({ queryKey: ['user', userId] })  // ✅ Only user
}
```

**Why it hurts**: 100 queries in cache → 100 network requests on every mutation. Kills mobile users.

---

## Decision Frameworks

### When to Use Optimistic Updates vs Invalidation

```
Mutation completes...
│
├─ Simple list append/prepend → Optimistic (useMutationState)
│   └─ Add todo, add comment, add item
│      WHY: No complex logic, just show pending item
│
├─ Complex computed data → Invalidation
│   └─ Change affects aggregates, filters, sorts
│      WHY: Server computes, client doesn't duplicate logic
│
├─ Risk of conflicts → Invalidation
│   └─ Multiple users editing same data
│      WHY: Optimistic update may be wrong, let server resolve
│
└─ Must feel instant → Optimistic + rollback on error
    └─ Toggle like, toggle favorite
       WHY: User expects immediate feedback
```

### React Query vs SWR

```
Choose React Query when:
✅ Need fine-grained cache control (gc, stale times)
✅ Complex invalidation patterns
✅ Optimistic updates with rollback
✅ Infinite queries (pagination)
✅ Already using TanStack ecosystem (Table, Router)

Choose SWR when:
✅ Simpler API (less configuration)
✅ Automatic revalidation on focus is main use case
✅ Smaller bundle size priority
✅ Using Next.js (first-party support)
```

**Real-world**: React Query wins for complex apps, SWR wins for simple dashboards.

---

## SSR Hydration Patterns (Next.js App Router)

### ❌ Common Hydration Mismatch

```typescript
// WRONG - server renders loading, client renders data
function Page() {
  const { data, isPending } = useQuery({
    queryKey: ['todos'],
    queryFn: fetchTodos,
  })

  if (isPending) return <div>Loading...</div>  // ❌ Mismatch
  return <div>{data.map(...)}</div>
}

// SERVER: Renders "Loading..."
// CLIENT: Has cached data → renders list
// RESULT: Hydration error
```

### ✅ Correct Pattern with Prefetch

```typescript
// app/page.tsx (Server Component)
import { dehydrate, HydrationBoundary, QueryClient } from '@tanstack/react-query'

export default async function Page() {
  const queryClient = new QueryClient()

  // Prefetch on server
  await queryClient.prefetchQuery({
    queryKey: ['todos'],
    queryFn: fetchTodos,
  })

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <TodoList />  {/* Client Component */}
    </HydrationBoundary>
  )
}

// components/TodoList.tsx (Client Component)
'use client'

export function TodoList() {
  const { data } = useQuery({
    queryKey: ['todos'],
    queryFn: fetchTodos,
  })

  // No isPending check - data guaranteed from server
  return <div>{data.map(...)}</div>
}
```

**Why it works**: Server prefetches, client hydrates with same data, no mismatch.

---

## Debugging Commands

### Find refetch loops
```typescript
// Add to QueryClient
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      onSuccess: (data, query) => {
        console.count(`Refetch: ${query.queryKey}`)
        // If count > 10 in 1 second → infinite loop
      }
    }
  }
})
```

### Visualize cache state
```typescript
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'

// Add to app
<ReactQueryDevtools initialIsOpen={false} />
// Click query → see refetch count, staleness, gc time
```

### Test staleTime behavior
```typescript
// Force immediate stale (for testing)
queryClient.invalidateQueries({ queryKey: ['todos'] })

// Check if query is stale
const state = queryClient.getQueryState(['todos'])
console.log(state?.isInvalidated)  // true = will refetch on next mount
```

---

## Error Recovery Procedures

### When Hydration Mismatch Occurs (SSR)
**Recovery steps**:
1. Verify data equality: Add `console.log(JSON.stringify(data))` in server and client components
2. Check prefetch completion: Inspect `dehydrate(queryClient)` output—should contain queries object
3. Confirm queryKey match: Server and client must use EXACT same key (including array order)
4. **Fallback**: If still mismatching, bypass prefetch and use `initialData` from server props:
   ```typescript
   // Server passes data via props
   export default function Page() {
     const data = await fetchTodos()
     return <TodoList initialTodos={data} />
   }

   // Client receives and uses as initialData
   function TodoList({ initialTodos }) {
     const { data } = useQuery({
       queryKey: ['todos'],
       queryFn: fetchTodos,
       initialData: initialTodos,  // Hydrates without mismatch
     })
   }
   ```

### When Infinite Refetch Loop Detected
**Recovery steps**:
1. Add refetch logging: `console.count(\`Refetch: \${JSON.stringify(queryKey)}\`)` in queryFn
2. Identify the culprit: Check which count exceeds 10 in first 2 seconds
3. Extract primitives from queryKey: Replace objects/arrays with IDs/strings
4. **Fallback**: If key MUST contain object (rare), memoize it AND disable `structuralSharing`:
   ```typescript
   const stableKey = useMemo(() => ['user', user], [user.id])
   useQuery({
     queryKey: stableKey,
     queryFn: () => fetchUser(user.id),
     structuralSharing: false,  // Prevents reference comparison issues
   })
   ```

### When Stale Data Persists
**Recovery steps**:
1. Check `staleTime` setting: Search codebase for `staleTime: Infinity` or very large values
2. Force invalidation: `queryClient.invalidateQueries({ queryKey: ['your-key'] })`
3. Verify refetch: Check Network tab for request after invalidation
4. **Fallback**: If data still stale, cache may be corrupted → clear and refetch:
   ```typescript
   queryClient.removeQueries({ queryKey: ['your-key'] })
   queryClient.refetchQueries({ queryKey: ['your-key'] })
   ```
   Or nuclear option: `queryClient.clear()` (clears entire cache)

### When v4→v5 Migration Breaks Silently
**Recovery steps**:
1. Enable strict TypeScript: Add `strict: true` to `tsconfig.json` to catch removed properties
2. Search for v4 property names: `grep -r "cacheTime\|isLoading\|keepPreviousData" src/`
3. Replace with v5 equivalents: Use find-replace for codebase-wide fixes
4. **Fallback**: If TypeScript still doesn't catch it, add runtime warning in development:
   ```typescript
   // In QueryClient setup
   const queryClient = new QueryClient({
     defaultOptions: {
       queries: {
         // @ts-ignore - intentionally check for v4 props
         ...(process.env.NODE_ENV === 'development' && {
           // Warn if someone passes v4 props
           onError: (err, query) => {
             if ('cacheTime' in query) console.warn('⚠️ cacheTime removed in v5, use gcTime')
             if ('isLoading' in query) console.warn('⚠️ isLoading removed in v5, use isPending')
           }
         })
       }
     }
   })
   ```

---

## When to Load Full Reference

**MANDATORY - READ ENTIRE FILE**: `references/v5-features.md` when:
- Using 3+ v5-specific features simultaneously (useMutationState, throwOnError, infinite queries)
- Need complete API reference for 5+ advanced hook options (select, placeholderData, notifyOnChangeProps)
- Implementing complex patterns (optimistic updates with rollback, parallel/dependent queries, suspense mode)
- Building custom hooks wrapping React Query with 4+ configuration options

**MANDATORY - READ ENTIRE FILE**: `references/migration-guide.md` when:
- Migrating codebase with 10+ query usages from v4 to v5
- Need exhaustive breaking changes checklist (20+ items to verify)
- Encountering 3+ different v4→v5 migration errors
- Setting up automated migration with codemods for large codebase (100+ queries)

**Do NOT load references** for:
- Single breaking change fix (use this core framework's Breaking Changes section)
- Basic troubleshooting (infinite loops, stale data, hydration—covered in core)
- Simple optimistic update (use Decision Frameworks section)

---

## Resources

- **Official Docs**: https://tanstack.com/query/latest (for API reference)
- **This Skill**: Production issues, migration gotchas, decision frameworks
