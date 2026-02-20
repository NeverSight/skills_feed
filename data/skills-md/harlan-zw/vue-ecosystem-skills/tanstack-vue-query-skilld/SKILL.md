---
name: tanstack-vue-query-skilld
description: "ALWAYS use when writing code importing \"@tanstack/vue-query\". Consult for debugging, best practices, or modifying @tanstack/vue-query, tanstack/vue-query, tanstack vue-query, tanstack vue query, query."
metadata:
  version: 5.92.9
  generated_by: Gemini CLI · Gemini 3 Flash
---

# TanStack/query `@tanstack/vue-query`

**Version:** 5.92.9 (Jan 2026)
**Deps:** @tanstack/match-sorter-utils@^8.19.4, @vue/devtools-api@^6.6.3, vue-demi@^0.14.10, @tanstack/query-core@5.90.20
**Tags:** alpha: 5.0.0-alpha.91 (Jul 2023), beta: 5.0.0-beta.35 (Sep 2023), rc: 5.0.0-rc.16 (Oct 2023), latest: 5.92.9 (Jan 2026), previous: 4.43.0 (Jan 2026)

**References:** [Docs](./references/docs/_INDEX.md) — API reference, guides • [GitHub Issues](./references/issues/_INDEX.md) — bugs, workarounds, edge cases • [GitHub Discussions](./references/discussions/_INDEX.md) — Q&A, patterns, recipes • [Releases](./references/releases/_INDEX.md) — changelog, breaking changes, new APIs

## API Changes

This section documents version-specific API changes — prioritize recent major/minor releases.

- BREAKING: `useQuery` signature — v5 requires a single object argument `{ queryKey, queryFn, ... }`. Old positional arguments are no longer supported and will result in errors [source](./references/docs/framework/vue/guides/queries.md)

- BREAKING: `useQueries` signature — v5 now takes an object with a `queries` array property: `useQueries({ queries: [...] })`. This allows for additional top-level options like `combine`

- BREAKING: `useQueries` return type — now returns a `Ref` of the results array instead of a `reactive` array, ensuring better compatibility with Vue 2 and avoiding spread reactivity loss [source](./references/docs/framework/vue/guides/migrating-to-v5.md)

- BREAKING: Callback removal — `onSuccess`, `onError`, and `onSettled` are removed from `useQuery`, `useInfiniteQuery`, and `useQueries`. Use `select` for data transformation or global `QueryCache` callbacks instead [source](./references/docs/framework/vue/guides/migrating-to-v5.md)

- BREAKING: `cacheTime` renamed — renamed to `gcTime` (Garbage Collection time) across all options and default options to better reflect its purpose [source](./references/docs/reference/QueryClient.md)

- BREAKING: `useInfiniteQuery` parameters — `getNextPageParam` and `getPreviousPageParam` now receive a single object containing `lastPage`, `allPages`, `lastPageParam`, and `allPageParams` [source](./references/docs/framework/vue/reference/useInfiniteQuery.md)

- BREAKING: `keepPreviousData` removed — the option is replaced by the `placeholderData: keepPreviousData` helper function from `@tanstack/vue-query` [source](./references/docs/framework/vue/guides/paginated-queries.md)

- NEW: `queryOptions` / `infiniteQueryOptions` — helper functions for sharing query definitions with type safety across components and for prefetching [source](./references/docs/framework/vue/reference/queryOptions.md)

- NEW: `useMutationState` — new composable to access mutation state globally by filtering for specific mutations based on keys or filters

- NEW: Options Getter support — `useQuery` and `useInfiniteQuery` now support passing a getter function (e.g., `() => options`) or a `Ref` for the entire options object, enabling easier reactivity

- NEW: `combine` for `useQueries` — allows merging multiple query results into a single value (e.g., a single object or a derived state) via the `combine` option

- NEW: Injection Context — `vue-query` composables can now be used in any function that supports `injectionContext` (e.g., router guards) if used within an `effectScope` [source](./references/docs/framework/vue/guides/migrating-to-v5.md)

- DEPRECATED: `isLoading` — renamed to `isPending` in v5. The `isLoading` property now specifically means `isPending && isFetching` (fetching for the first time) [source](./references/docs/framework/vue/guides/queries.md)

- BREAKING: Vue 3.3 requirement — minimum Vue version for `@tanstack/vue-query` v5 is now 3.3 to support newer reactivity features [source](./references/docs/framework/vue/guides/migrating-to-v5.md)

**Also changed:** `isPlaceholderData` boolean result new v5 · `initialPageParam` required for `useInfiniteQuery` · `isPaused` property added to query results · `Suspense` (experimental) supported via `suspense()` method (experimental)

## Best Practices

- Use `MaybeRefOrGetter` for composable parameters to support refs, plain values, and reactive getters seamlessly [source](./references/docs/framework/vue/reactivity.md)

```ts
// Preferred: Accepts ref, getter, or value
export function useUser(id: MaybeRefOrGetter<string>) {
  return useQuery({
    queryKey: ['user', id],
    queryFn: () => fetchUser(toValue(id))
  })
}
```

- Pass the entire options object as a getter function to reactively update multiple query parameters at once (v5.91.0+) [source](./references/releases/CHANGELOG.md)

```ts
// Preferred for complex reactivity
useQuery(() => ({
  queryKey: ['todo', id.value],
  queryFn: () => fetchTodo(id.value),
  enabled: !!id.value
}))
```

- Prefer reactive getters over `computed` for simple property access to avoid unnecessary memoization overhead [source](./references/docs/framework/vue/reactivity.md)

```ts
// Preferred: No computed needed
const { data } = useUserProjects(() => props.userId)

// Avoid: Unnecessary memoization
const userId = computed(() => props.userId)
const { data } = useUserProjects(userId)
```

- Use `onServerPrefetch` with the `suspense()` helper to ensure queries are awaited during SSR [source](./references/docs/framework/vue/guides/ssr.md)

```ts
const { data, suspense } = useQuery({ queryKey: ['test'], queryFn: fetcher })
onServerPrefetch(suspense)
```

- Set `staleTime` to a value greater than 0 for SSR to prevent immediate background refetching on the client [source](./references/docs/framework/vue/guides/ssr.md)

```ts
const queryClient = new QueryClient({
  defaultOptions: { queries: { staleTime: 1000 * 60 * 5 } }
})
```

- Manually call `queryClient.clear()` after request handling if `gcTime` is set to a non-Infinity value on the server to prevent memory leaks [source](./references/docs/framework/vue/guides/ssr.md)

- Treat `useQuery` results as immutable and clone data before using it with two-way bindings like `v-model` [source](./references/docs/framework/vue/reactivity.md)

```ts
const { data } = useQuery({ ... })
const model = ref()
watch(data, (newData) => {
  model.value = JSON.parse(JSON.stringify(newData))
}, { immediate: true })
```

- Use the `queryOptions` helper to define type-safe, reusable query configurations that can be shared across components

```ts
const userOptions = (id: string) => queryOptions({
  queryKey: ['user', id],
  queryFn: () => fetchUser(id)
})

useQuery(userOptions('123'))
```

- Include all reactive dependencies in the `queryKey` to ensure Vue Query tracks them and refetches automatically on change [source](./references/docs/framework/vue/reactivity.md)

- Utilize a custom `queryClientKey` when running multiple Vue applications on the same page to prevent QueryClient instance clashing [source](./references/docs/framework/vue/guides/custom-client.md)

```ts
// Plugin configuration
app.use(VueQueryPlugin, { queryClientKey: 'AppA' })

// Usage
useQuery({ queryKey: ['data'], queryFn: fetcher, queryClientKey: 'AppA' })
```
