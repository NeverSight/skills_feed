---
name: tanstack-vue-store-skilld
description: "ALWAYS use when writing code importing \"@tanstack/vue-store\". Consult for debugging, best practices, or modifying @tanstack/vue-store, tanstack/vue-store, tanstack vue-store, tanstack vue store, store."
metadata:
  version: 0.9.1
  generated_by: Gemini CLI · Gemini 3 Flash
  generated_at: 2026-02-18
---

# TanStack/store `@tanstack/vue-store`

**Version:** 0.9.1 (Feb 2026)
**Deps:** vue-demi@^0.14.10, @tanstack/store@0.9.1
**Tags:** latest: 0.9.1 (Feb 2026)

**References:** [Docs](./references/docs/_INDEX.md) — API reference, guides • [GitHub Issues](./references/issues/_INDEX.md) — bugs, workarounds, edge cases • [GitHub Discussions](./references/discussions/_INDEX.md) — Q&A, patterns, recipes • [Releases](./references/releases/_INDEX.md) — changelog, breaking changes, new APIs

## API Changes

This section documents version-specific API changes — prioritize recent major/minor releases.

- BREAKING: `new Store()` -> `createStore()` — v0.9.0 replaced the class constructor with a factory function for all store instantiations [source](./references/releases/@tanstack/vue-store@0.9.0.md)

- BREAKING: `new Derived()` -> `createStore(fn)` — v0.9.0 unified derived and simple state creation into the single `createStore` API [source](./references/releases/@tanstack/vue-store@0.9.0.md)

- BREAKING: `new Effect()` -> `store.subscribe()` — v0.9.0 removed the `Effect` class; side effects are now handled directly via store subscriptions [source](./references/releases/@tanstack/vue-store@0.9.0.md)

- NEW: `createStore(initialValue)` — now the standard way to initialize a store instance with a given initial state [source](./references/docs/quick-start.md)

- NEW: `createStore((prev) => next)` — creates a derived store that automatically updates when dependencies change, receiving the optional `prev` state [source](./references/docs/quick-start.md)

- NEW: `createAtom()` — creates a generic signal-based atom for granular reactivity, re-exported from `@tanstack/store` [source](./references/docs/reference/functions/createAtom.md)

- NEW: `createAsyncAtom()` — factory for creating reactive atoms from asynchronous functions or Promises [source](./references/docs/reference/functions/createAsyncAtom.md)

- NEW: `batch(fn)` — utility to group multiple state updates into a single notification cycle to optimize performance [source](./references/docs/reference/functions/batch.md)

- NEW: `flush()` — manually triggers all pending updates across stores for immediate state consistency [source](./references/docs/reference/functions/flush.md)

- NEW: `toObserver()` — utility to convert callback functions into a formal `Observer` object for subscriptions [source](./references/docs/reference/functions/toObserver.md)

- NEW: `shallow()` with expanded support — v0.9.1 added `Date`, `Map`, and `Set` comparison to the `shallow` utility to fix stale values in selectors

- NEW: `useStore` equality check — `useStore(store, selector, { equal })` now accepts a custom equality function for rendering control [source](./references/docs/framework/vue/reference/functions/useStore.md)

- CHANGED: `alien-signals` core — v0.9.0 switched internal reactivity to `alien-signals` for significantly improved performance [source](./references/releases/@tanstack/vue-store@0.9.0.md)

- NEW: `NoInfer` in `useStore` — improved TypeScript inference for selected state using the `NoInfer` utility in function signatures

**Also changed:** `ReadOnlyStore` class · `Subscribable` interface · `AtomOptions` with `compare` · `AsyncAtomState` type · `Subscription` object

## Best Practices

- Prefer `createStore()` over the deprecated `new Store()` constructor — aligns with v0.9.0+ idiomatic patterns and internal optimizations [source](./references/releases/@tanstack/vue-store@0.9.0.md)

- Use a factory function within `createStore()` for derived state — replaces the removed `Derived` class for better composition and efficient updates [source](./references/releases/@tanstack/vue-store@0.9.0.md)

```ts
const store = createStore({ count: 1 })
const doubled = createStore(() => store.state.count * 2)
```

- Pass a selector function to `useStore()` for fine-grained reactivity — ensures the Vue component only re-renders when the specific selected slice of state changes [source](./references/docs/framework/vue/reference/functions/useStore.md)

- Leverage the default `shallow` equality in `useStore()` for object selections — prevents unnecessary re-renders when your selector returns new object/array references with identical values

- Group multiple state updates within `batch()` — minimizes reactive triggers and improves performance in high-frequency update scenarios [source](./references/docs/reference/functions/batch.md)

- Use `createAsyncAtom()` to manage asynchronous data — automatically tracks loading, error, and data states in a standardized format [source](./references/docs/reference/functions/createAsyncAtom.md)

- Use `store.subscribe()` for side effects instead of the removed `new Effect()` — provides a cleaner, lifecycle-aware API for observing state changes outside of components [source](./references/releases/@tanstack/vue-store@0.9.0.md)

- Define and export stores from central modules — enables seamless state sharing across multiple Vue components and facilitates better testability [source](./references/docs/framework/vue/quick-start.md)

- Provide a custom `compare` function in `AtomOptions` for complex state — allows fine-grained control over when an atom's value is considered "changed" to optimize downstream computations [source](./references/docs/reference/interfaces/AtomOptions.md)

- Rely on `NoInfer` in `useStore` selectors for accurate type safety — ensures TypeScript correctly infers the state type without being influenced by the return type of the selector
