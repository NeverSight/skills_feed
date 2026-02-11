---
name: accelint-tanstack-query-best-practices
description: Use when configuring QueryClient, implementing mutations, debugging performance, or adding optimistic updates with @tanstack/react-query in Next.js App Router. Covers factory patterns, query keys, cache invalidation, observer debugging, HydrationBoundary, multi-layer caching. Keywords TanStack Query, useSuspenseQuery, useQuery, useMutation, invalidateQueries, staleTime, gcTime, refetch, hydration.
license: Apache-2.0
metadata:
  author: gohypergiant
  version: "1.3"
---

# TanStack Query Best Practices

Expert patterns for TanStack Query in modern React applications with Next.js App Router and Server Components.

## NEVER Do With TanStack Query

- **NEVER use a singleton QueryClient on the server** - Creates data leakage between users and race conditions. Each request must get its own isolated QueryClient instance to prevent cached data from one user appearing for another.
- **NEVER synchronize query data to useState** - Background refetches, invalidations, and optimistic updates all modify the cache. Local state copies become stale immediately, causing "my save didn't work" bugs. Use query data directly or derive with useMemo.
- **NEVER put queries inside list item components** - Creates N observers for N items, causing O(n) iteration on every cache update. 200 list items calling useQuery creates 200 network requests and 200 observers. Hoist queries to parent components.
- **NEVER use unstable query keys** - Arrays with non-guaranteed order, temporal queries with Date.now(), or object keys without deterministic serialization create infinite cache entries. Keys must be stable and deterministic.
- **NEVER skip enabled guards for dependent queries** - Firing queries with undefined parameters creates garbage cache entries like ['tracks', undefined] and wastes network requests before real data arrives.
- **NEVER ignore AbortController signals** - Without query cancellation support, unmounted components leave in-flight requests running, wasting bandwidth and potentially updating stale cache entries.
- **NEVER use optimistic updates for high-stakes or external mutations** - Life-critical operations, audit trail systems, and mutations triggered by external events need pessimistic updates to ensure UI matches server state.
- **NEVER assume structural sharing is free** - For datasets >1000 items updating frequently, structural sharing's O(n) deep equality checks become CPU overhead. Disable with structuralSharing: false for large, frequently-changing data.
- **NEVER skip onSettled in optimistic updates** - onSettled is your cleanup guarantee even if onError throws. Without it, UI can be left in corrupted state when error handler fails. Always pair onMutate with onSettled for resource cleanup and cache consistency.
- **NEVER assume cache invalidation is synchronous** - invalidateQueries triggers background refetches which can race with optimistic updates. Use cancelQueries in onMutate to prevent background refetches from overwriting your optimistic changes before the mutation completes.
- **NEVER use setQueryData without structural comparison** - Directly setting cache data bypasses structural sharing and breaks referential equality optimizations. Wrap in updater function to preserve references for unchanged portions: `setQueryData(key, (old) => ({ ...old, changed: value }))` instead of `setQueryData(key, newValue)`.
- **NEVER forget to handle hydration mismatches** - Server-rendered data may differ from client expectations (timestamps, user-specific data, randomized content). Use suppressHydrationWarning on containers or ensure deterministic server/client rendering with stable timestamps and consistent data sources.

## Before Using TanStack Query, Ask

### State Classification
- **Is this server state or client state?** TanStack Query manages server state (API data, database records, external system state). UI state (modals, themes, form drafts) belongs in Zustand or useState.
- **Does this data change after initial render?** Static reference data might not need TanStack Query's refetching machinery. Consider if simpler alternatives suffice.

### Cache Strategy
- **How fresh does this data need to be?** Lookup tables can have 1-hour staleTime. Real-time tracking needs 5-second staleTime with refetchInterval. Match configuration to business requirements.
- **What's the query lifecycle?** Frequently-accessed data needs higher gcTime. One-time detail views can have aggressive garbage collection.

### Observer Economics
- **How many components will subscribe to this query?** >10 observers on a single cache entry suggests hoisting queries to parent. >100 observers indicates architectural issues.
- **Am I creating N queries or 1 query with N observers?** List items should receive props from parent query, not call individual useQuery hooks.

## How to Use

This skill uses **progressive disclosure** to minimize context usage. Load references based on your scenario:

### Scenario 1: Setting Up Query Client
**MANDATORY - READ ENTIRE FILE**: Read [`query-client-setup.md`](references/query-client-setup.md) (~125 lines) and [`server-integration.md`](references/server-integration.md) (~151 lines) completely for server/client setup patterns.
**Do NOT Load** other references for initial setup.

Copy [assets/query-client.ts](assets/query-client.ts) for production-ready configuration.

### Scenario 2: Building Query Hooks
1. **MANDATORY**: Read [`query-keys.md`](references/query-keys.md) (~151 lines) for key factory setup
2. If using server components: Read [`server-integration.md`](references/server-integration.md)
3. **Do NOT Load** mutations-and-updates.md unless implementing mutations

Use decision tables below for configuration values.

### Scenario 3: Implementing Mutations
**MANDATORY - READ ENTIRE FILE**: Read [`mutations-and-updates.md`](references/mutations-and-updates.md) (~345 lines) completely. Reference [`patterns-and-pitfalls.md`](references/patterns-and-pitfalls.md) for rollback patterns.
**Do NOT Load** caching-strategy.md for basic CRUD mutations.

### Scenario 4: Debugging Performance Issues
1. First, check Observer Count Thresholds table below (lines 121-129)
2. If observer count >50: Read [`patterns-and-pitfalls.md`](references/patterns-and-pitfalls.md)
3. If large dataset issues: Read [`fundamentals.md`](references/fundamentals.md) for structural sharing
4. **Do NOT Load** all references - diagnose first, then load targeted content

### Scenario 5: Multi-Layer Caching Strategy
**MANDATORY**: Read [`caching-strategy.md`](references/caching-strategy.md) (~198 lines) for unified Next.js use cache + TanStack Query + HTTP cache patterns.
**Do NOT Load** if only using client-side TanStack Query.

## Query Configuration Decision Matrix

| Data Type | staleTime | gcTime | refetchInterval | structuralSharing | Notes |
|-----------|-----------|--------|-----------------|-------------------|-------|
| **Reference/Lookup** | 1hr | Infinity | - | true | Countries, categories, static enums |
| **User Profile** | 5min | 10min | - | true | Changes infrequently, moderate freshness |
| **Real-time Tracking** | 5s | 30s | 5s | false | High update frequency, large payloads |
| **Live Dashboard** | 2s | 1min | 2s | Depends on size | Balance freshness vs performance |
| **Detail View** | 30s | 2min | - | true | Fetched on-demand, moderate caching |
| **Search Results** | 1min | 5min | - | true | Cacheable, not time-sensitive |

## Mutation Pattern Selection

| Scenario | Pattern | When to Use |
|----------|---------|-------------|
| **Form submission** | Pessimistic | Multi-step forms, server validation required, error messages needed before proceeding |
| **Toggle/checkbox** | Optimistic | Binary state changes, low latency required, easy to rollback |
| **Drag and drop** | Optimistic | Immediate visual feedback essential, reordering operations, non-critical data |
| **Batch operations** | Pessimistic | Multiple items, partial failures possible, user needs confirmation of what succeeded |
| **Life-critical ops** | Pessimistic | Medical, financial, safety-critical systems where UI must match server reality |
| **Audit trail required** | Pessimistic | Compliance systems where operator actions must match logged events exactly |

## Query Key Architecture

Use hierarchical factories for consistent invalidation:

```typescript
// Recommended structure
export const keys = {
  all: () => ['domain'] as const,
  lists: () => [...keys.all(), 'list'] as const,
  list: (filters: string) => [...keys.lists(), filters] as const,
  details: () => [...keys.all(), 'detail'] as const,
  detail: (id: string) => [...keys.details(), id] as const,
};

// Invalidation examples
queryClient.invalidateQueries({ queryKey: keys.all() }); // Invalidate everything
queryClient.invalidateQueries({ queryKey: keys.lists() }); // Invalidate all lists
queryClient.invalidateQueries({ queryKey: keys.detail(id) }); // Invalidate one item
```

**Key stability rules:**
- Deterministic serialization (sort arrays before joining)
- No temporal values (Date.now(), random IDs)
- Type consistency (don't mix '1' and 1)
- Stable object shapes (use sorted keys or serialize)

## Server-Client Integration Pattern

| Layer | Purpose | Invalidation Method | Cache Scope |
|-------|---------|---------------------|-------------|
| **Next.js use cache** | Reduce database load | revalidateTag() or updateTag() | Cross-request, server-side |
| **TanStack Query** | Client-side state management | queryClient.invalidateQueries() | Per-browser-tab |
| **Browser HTTP cache** | Eliminate network requests | Cache-Control headers | Per-browser |

**Unified invalidation strategy:**
1. Use same key factories for both server and client caches
2. Server mutations call updateTag(...keys.detail(id))
3. Client mutations call queryClient.invalidateQueries({ queryKey: keys.detail(id) })
4. Both caches stay synchronized with same hierarchy

## Observer Count Thresholds

| Observer Count | Performance Impact | Action Required |
|----------------|-------------------|------------------|
| 1-5 | Negligible | None |
| 6-20 | Minimal | Monitor, no immediate action |
| 21-50 | Noticeable on updates | Consider hoisting queries to parent |
| 51-100 | Significant overhead | Refactor: hoist queries or use select |
| 100+ | Critical impact | Immediate refactor: single query with props distribution |

**Diagnosis:**
1. Open TanStack Query DevTools in development
2. Find cache entries with high observer counts
3. Search codebase for useQuery calls with those keys
4. Refactor to parent components or shared cache entries

## Query Hook Patterns

| Pattern | Use Case | Example |
|---------|----------|---------|
| **useSuspenseQuery** | Server Components integration, Suspense boundaries | `useSuspenseQuery({ queryKey, queryFn })` |
| **useQuery with enabled** | Dependent queries, conditional fetching | `useQuery({ queryKey, queryFn, enabled: !!userId })` |
| **useQuery with select** | Data transformation, subset selection | `useQuery({ queryKey, queryFn, select: selectFn })` — extract `selectFn` to a stable module-level variable; inline functions re-run on every render |
| **useMutation optimistic** | Low-latency UI updates, easily reversible | `useMutation({ onMutate, onError, onSettled })` |
| **useMutation pessimistic** | High-stakes operations, server validation | `useMutation({ onSuccess })` |

## Common Error Patterns and Fixes

| Symptom | Root Cause | Solution | Fallback if Solution Fails |
|---------|------------|----------|---------------------------|
| Data doesn't update after save | Copied query data to useState | Use query data directly, derive with useMemo | Force refetch with refetch() method, check network tab for actual API response |
| Infinite requests | Unstable query keys (Date.now(), unsorted arrays) | Use deterministic key construction | Add staleness detection: `const requestCount = useRef(0); useEffect(() => { requestCount.current++; if (requestCount.current > 10) console.error('Infinite loop detected', queryKey); }, [data]);` See fundamentals.md for key stability patterns |
| N duplicate requests | Query in every list item | Hoist query to parent, pass data as props | Ensure all components use identical queryKey (same object reference or values): `const queryKey = useMemo(() => keys.list(filters), [filters]);` Increase staleTime to 30s to deduplicate rapid requests |
| Query fires with undefined params | Missing enabled guard | Add `enabled: Boolean(dependency)` | Use placeholderData to show loading state, add type guards in queryFn to throw early |
| Slow list rendering | N queries + N observers | Single parent query, distribute via props | Use select to subscribe to subset, implement virtual scrolling to reduce mounted components |
| Cache never clears | gcTime: Infinity on frequently-changing data | Match gcTime to data lifecycle | Force removal with queryClient.removeQueries(), monitor cache size with DevTools |
| UI shows stale data flash | Server cache stale, client cache fresh | Unified invalidation with same keys | Use initialData from server props, set refetchOnMount: false for hydrated queries |
| Optimistic update won't rollback | onError not restoring context | Use context from onMutate in onError | Force invalidation with invalidateQueries, implement manual rollback with previous state snapshot |
| Server hydration mismatch | Timestamp/user-specific data in SSR | Use suppressHydrationWarning on container | Client-only rendering with dynamic import and ssr: false, or normalize timestamps to UTC |
| Query never refetches | enabled: false guard blocking, or gcTime expired | Check enabled conditions, verify query isn't filtered by predicate | Increase gcTime to keep cache alive longer, use refetchInterval for polling behavior, check if staleTime: Infinity is preventing background refetches |
| Server action not invalidating | updateTag/revalidateTag using different keys than queryClient | Use same key factories for both server and client caches | Manually call router.refresh() after server action, verify tag names match query key hierarchy |
| Mutation succeeds but UI doesn't update | Missing onSuccess invalidation or wrong queryKey | Add `onSuccess: () => queryClient.invalidateQueries({ queryKey })` | Use setQueryData to manually update cache: `queryClient.setQueryData(keys.detail(id), newData)`, verify queryKey matches exactly |

## Troubleshooting Decision Tree

### Performance Issues

**Step 1: Check observer count in DevTools** (use thresholds at lines 136-145)
- **>100 observers** → Immediate refactor: hoist queries to parent component, distribute data via props
- **51-100 observers** → Refactor: hoist queries or use select to subscribe to data subsets
- **<50 observers** → Issue is elsewhere, continue to Step 2

**Step 2: Check data size and update frequency**
- **>1000 items + frequent updates** → Disable structural sharing: `structuralSharing: false` (see fundamentals.md for details)
- **Large payloads (>500KB)** → Check network tab, consider pagination or infinite queries
- **Fast updates (<1s interval)** → Lower staleTime or use refetchInterval, verify cache strategy

**Step 3: Check React DevTools Profiler**
- Look for unnecessary re-renders in components using query data
- Verify select function isn't recreated on every render (use useCallback)
- Check if derived data should use useMemo instead of inline transformation
- Profile component render times to identify bottlenecks

### Network Issues

**Flaky connections:**
- Configure retry logic: `retry: 3, retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000)`
- See query-client-setup.md for production retry configuration

**Token refresh needed:**
- Implement auth interceptor pattern in queryFn wrapper
- Use queryClient.setQueryDefaults() for global auth headers
- See patterns-and-pitfalls.md for token refresh patterns

**Race conditions:**
- Review invalidation timing: use cancelQueries before setQueryData
- Check if optimistic updates compete with background refetches
- Verify mutation onMutate uses await cancelQueries({ queryKey })

### Hydration Issues

**SSR mismatch (hydration error in console):**
- Add suppressHydrationWarning to container element
- Normalize data: ensure server and client produce identical output (stable timestamps, sorted arrays)
- Check if user-specific data is being rendered server-side

**Client-server data drift:**
- Verify revalidateTag timing on server mutations
- Check if server cache (Next.js use cache) is stale while client cache is fresh
- Use initialData from server props: `initialData: serverData, refetchOnMount: false`

**HydrationBoundary not working:**
- Verify client component boundaries: HydrationBoundary must wrap 'use client' components
- Check if dehydratedState is being serialized correctly from server
- Ensure shouldDehydrateQuery includes queries you want to hydrate

## Freedom Calibration

**Calibrate guidance specificity to mutation risk:**

| Task Type | Freedom Level | Guidance Format | Example |
|-----------|---------------|-----------------|---------|
| **Query configuration** | High freedom | Principles with tables for common patterns | "Match staleTime to business requirements" |
| **Optimistic updates** | Medium freedom | Complete pattern with rollback handling | "Use onMutate/onError/onSettled callbacks" |
| **QueryClient setup** | Low freedom | Exact code with critical security warning | "NEVER use singleton on server - use factory" |

**The test:** "If the agent makes a mistake, what's the consequence?"
- Server singleton mistake → Data leakage between users (critical security issue)
- Observer count mistake → Performance degradation (medium impact)
- staleTime tuning → Suboptimal freshness (low impact)

## Important Notes

- Query keys are hashed deterministically - ['tracks', '1'] and ['tracks', 1] create different cache entries
- Query keys must be JSON-serializable for cache persistence across page reloads and hydration
- shouldDehydrateQuery with pending status enables streaming without await in server components
- HydrationBoundary must wrap client components only - server components bypass the boundary
- revalidateTag vs updateTag matters: revalidateTag uses stale-while-revalidate, updateTag invalidates immediately
- Background refetches run even when no components are mounted if gcTime hasn't expired
- Structural sharing runs twice when using select: once on raw data, once on transformed data
- `select` only runs on successfully cached data — it is never called in error states; put validation and error throwing in `queryFn`
- cancelQueries in onMutate is critical - background refetches can overwrite optimistic updates
- Context returned from onMutate is passed to onError and onSettled for rollback state
