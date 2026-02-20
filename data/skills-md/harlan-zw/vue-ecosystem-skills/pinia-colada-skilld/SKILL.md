---
name: pinia-colada-skilld
description: "ALWAYS use when writing code importing \"@pinia/colada\". Consult for debugging, best practices, or modifying @pinia/colada, pinia/colada, pinia colada, pinia-colada."
metadata:
  version: 0.21.4
  generated_by: Gemini CLI · Gemini 3 Flash
  generated_at: 2026-02-18
---

# posva/pinia-colada `@pinia/colada`

**Version:** 0.21.4 (Feb 2026)
**Tags:** latest: 0.21.4 (Feb 2026)

**References:** [Docs](./references/docs/_INDEX.md) — API reference, guides • [GitHub Issues](./references/issues/_INDEX.md) — bugs, workarounds, edge cases • [GitHub Discussions](./references/discussions/_INDEX.md) — Q&A, patterns, recipes • [Releases](./references/releases/_INDEX.md) — changelog, breaking changes, new APIs

## API Changes

This section documents version-specific API changes — prioritize recent major/minor releases.

- BREAKING: `useInfiniteQuery()` — v0.20.0 refactored: removed `merge`, changed `data` to `{ pages, pageParams }`, `initialPage` → `initialPageParam`, `loadMore` → `loadNextPage`, and `getNextPageParam` is now required (experimental) [source](./references/releases/CHANGELOG.md)

- BREAKING: `PiniaColada` installation — v0.14.0 moved global options to `queryOptions: { ... }` and requires an options object for typing: `app.use(PiniaColada, {})` [source](./references/releases/CHANGELOG.md)

- BREAKING: `useQuery()` aliases — `isFetching` was renamed to `isLoading` in v0.8.0 to better reflect its connection to `asyncStatus` [source](./references/releases/CHANGELOG.md)

- BREAKING: Status split — v0.8.0 split `status` into `status` (data: `'pending'|'success'|'error'`) and `asyncStatus` (operation: `'idle'|'loading'`) [source](./references/releases/CHANGELOG.md)

- BREAKING: Mutation IDs — v0.19.0 simplified mutation IDs to incremented numbers (starting at 1). `mutationCache.get()` now takes the ID, and `$n` suffix is removed from keys [source](./references/releases/CHANGELOG.md)

- BREAKING: Cache Key structure — v0.16.0 refactored internal cache to support deeply nested objects for keys. `toCacheKey` now returns a plain string. Stricter types disallow `undefined` in keys [source](./references/releases/CHANGELOG.md)

- BREAKING: `queryCache` method renames — `cancelQuery()` was renamed to `cancel()` in v0.11.0, and `cancelQueries()` was added for multiple cancellations [source](./references/releases/CHANGELOG.md)

- BREAKING: `setQueryState` → `setEntryState` — v0.9.0 renamed this `queryCache` action to better match its purpose [source](./references/releases/CHANGELOG.md)

- BREAKING: External `AbortError` — v0.18.0 now surfaces external abort signals as actual errors instead of silently ignoring them [source](./references/releases/CHANGELOG.md)

- BREAKING: `placeholderData` types — v0.13.0 changed `placeholderData` to only allow returning `undefined` (not `null`) to improve type inference [source](./references/releases/CHANGELOG.md)

- BREAKING: Devtools dependency — v0.21.0 removed built-in `@vue/devtools-api` dependency; use `@pinia/colada-devtools` instead [source](./references/releases/CHANGELOG.md)

- NEW: `useInfiniteQuery()` — v0.13.5 introduced infinite scrolling support (experimental) [source](./references/releases/CHANGELOG.md)

- NEW: `useQueryState()` — v0.17.0 added this for easier state management without the full `useQuery` return object [source](./references/releases/CHANGELOG.md)

- NEW: Global Query Hooks — v0.8.0 introduced `PiniaColadaQueryHooksPlugin` to manage `onSuccess`, `onError`, and `onSettled` [source](./references/releases/CHANGELOG.md)

**Also changed:** `serializeTreeMap` replaces `serialize` v0.14.0 · `transformError` removed v0.12.0 · `EntryKey` replaces `EntryNodeKey` v0.17.0 · `TResult` renamed `TData` v0.16.0 · `QueryPlugin` → `PiniaColada` v0.8.0 · `delayLoadingRef` removed v0.12.0 · `invalidateKeys` moved to plugin v0.10.0

## Best Practices

- Use the grouped `state` object for type-safe narrowing in templates — TypeScript cannot narrow destructured `data` or `error` refs based on the `status` ref due to Vue's `Ref` wrapper limitations [source](./references/docs/guide/queries.md)

```vue
<script setup lang="ts">
const { state } = useQuery({ key: ['user'], query: fetchUser })
</script>

<template>
  <div v-if="state.status === 'success'">{{ state.data.name }}</div>
  <div v-else-if="state.status === 'error'">{{ state.error.message }}</div>
</template>
```

- Wrap shared reactive state in `defineQuery()` to prevent desynchronization — regular composables recreate refs for each component instance, causing only the first component to successfully trigger key-based reactivity [source](./references/docs/advanced/reusable-queries.md)

```ts
export const useFilteredTodos = defineQuery(() => {
  const search = ref('')
  const query = useQuery({
    key: () => ['todos', { search: search.value }],
    query: () => fetchTodos(search.value),
  })
  return { ...query, search }
})
```

- Combine hierarchical key factories with `defineQueryOptions()` for strict type safety — this enables automatic type inference in `queryCache` methods without manual type casting or string-based key typos [source](./references/docs/guide/query-keys.md)

```ts
export const todoOptions = defineQueryOptions((id: string) => ({
  key: ['todos', id],
  query: () => fetchTodo(id),
}))
// Inferred TData: queryCache.getQueryData(todoOptions('1').key)
```

- Handle side effects via `watch` or global plugins instead of query options — `useQuery` intentionally lacks `onSuccess`/`onError` to prevent side-effect duplication across multiple component instances [source](./references/docs/cookbook/query-hooks.md)

- Prefer `refresh()` over `refetch()` for standard UI updates — `refresh()` respects `staleTime` and deduplicates in-flight requests, whereas `refetch()` forces a network call regardless of cache status [source](./references/docs/guide/queries.md)

- Use the `meta` property for declarative cross-cutting concerns — attach metadata to queries to drive global UI behavior (like toast messages) within the `PiniaColadaQueryHooksPlugin` [source](./references/docs/cookbook/query-hooks.md)

- Verify cache state before performing optimistic rollbacks — always check if the current cache value matches the optimistic value in `onError` to avoid overwriting concurrent successful updates from other mutations [source](./references/docs/guide/optimistic-updates.md)

```ts
onError(err, vars, { newTodo, oldTodo }) {
  if (newTodo === queryCache.getQueryData(['todos'])) {
    queryCache.setQueryData(['todos'], oldTodo)
  }
}
```

- Use `queryCache.setEntryState()` for manual status synchronization — this is the preferred way to manually update an entry as setting data to `undefined` via `setQueryData()` is no longer supported for state resets [source](./references/releases/CHANGELOG.md)

- Explicitly import `useRoute` from `vue-router` in Nuxt `defineQuery` definitions — the Nuxt auto-imported version can cause unnecessary query triggers or `undefined` values due to Suspense integration [source](./references/docs/advanced/reusable-queries.md)

- Use the `enabled` getter to guard "immortal" queries in global stores — prevents queries inside Pinia stores from making invalid network requests when required reactive parameters (like route params) are absent [source](./references/docs/guide/queries.md)

```ts
const result = useQuery({
  key: () => ['deck', route.params.id],
  query: () => fetchDeck(route.params.id),
  enabled: () => !!route.params.id,
})
```
