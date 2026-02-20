---
name: vueuse-shared-skilld
description: "ALWAYS use when writing code importing \"@vueuse/shared\". Consult for debugging, best practices, or modifying @vueuse/shared, vueuse/shared, vueuse shared, vueuse."
metadata:
  version: 14.2.1
  generated_by: Gemini CLI · Gemini 3 Flash
  generated_at: 2026-02-18
---

# vueuse/vueuse `@vueuse/shared`

**Version:** 14.2.1 (Feb 2026)
**Tags:** next: 5.0.0 (Jun 2021), alpha: 14.0.0-alpha.3 (Sep 2025), beta: 14.0.0-beta.1 (Sep 2025), latest: 14.2.1 (Feb 2026)

**References:** [Docs](./references/docs/_INDEX.md) — API reference, guides • [GitHub Issues](./references/issues/_INDEX.md) — bugs, workarounds, edge cases • [GitHub Discussions](./references/discussions/_INDEX.md) — Q&A, patterns, recipes • [Releases](./references/releases/_INDEX.md) — changelog, breaking changes, new APIs

## API Changes

This section documents version-specific API changes — prioritize recent major/minor releases.

- BREAKING: Requires Vue 3.5 — v14 now requires Vue 3.5+ for native performance optimizations [source](./references/releases/v14.0.0.md)

- BREAKING: `useThrottleFn` alignment — v14 aligned with traditional throttle behavior (leading: true, trailing: false by default) [source](./references/releases/v14.0.0.md)

- BREAKING: ESM-only — v13 dropped CJS build support, package is now ESM-only [source](./references/releases/v13.0.0.md)

- BREAKING: `createSharedComposable` return — v14 now returns only the sharedComposable instance on the client side [source](./references/releases/v14.0.0.md)

- NEW: `refManualReset` — new function in v14 for creating refs with an explicit `reset()` method [source](./references/releases/v14.0.0.md)

- NEW: `watchAtMost` controls — v14 added `pause`, `resume`, and `count` to the return value [source](./references/releases/v14.0.0.md)

- NEW: `tryOnScopeDispose` — v14 added optional `failSilently` parameter to suppress errors outside of scope [source](./references/releases/v14.0.0.md)

- NEW: `useArrayReduce` type — v14.1.0 now exports the `UseArrayReduceReturn` type [source](./references/releases/v14.1.0.md)

- NEW: `computedWithControl` sources — v14.1.0 allows different types in watch sources array [source](./references/releases/v14.1.0.md)

- DEPRECATED: `computedEager` — v14 deprecated in favor of Vue 3.5's native `computed` optimizations [source](./references/releases/v14.0.0.md)

- DEPRECATED: `watchPausable` — v14 deprecated in favor of Vue's built-in `watch` or `pausableFilter` [source](./references/releases/v14.0.0.md)

- DEPRECATED: Alias exports — v14 deprecated secondary names like `ignorableWatch` in favor of primary `watchIgnorable` [source](./references/releases/v14.0.0.md)

- DEPRECATED: `eagerComputed` — v14 deprecated alias in favor of `computedEager` [source](./references/releases/v14.0.0.md)

- DEPRECATED: `controlledComputed` — v14 deprecated alias in favor of `computedWithControl` [source](./references/releases/v14.0.0.md)

**Also changed:** `createReactiveFn` DEPRECATED · `autoResetRef` DEPRECATED · `debouncedRef` DEPRECATED · `useDebounce` DEPRECATED · `throttledRef` DEPRECATED · `useThrottle` DEPRECATED · `controlledRef` DEPRECATED · `debouncedWatch` DEPRECATED · `ignorableWatch` DEPRECATED · `pausableWatch` DEPRECATED · `throttledWatch` DEPRECATED

## Best Practices

- Prefer Vue 3.4+ built-in `computed()` over `computedEager()` — standard computed properties now only trigger dependencies if the return value actually changes, making eager evaluation unnecessary [source](./references/docs/computedEager/index.md)

- Use `createSharedComposable()` for SSR-safe state sharing — it automatically falls back to non-shared instances during SSR to prevent cross-request state pollution, while maintaining a singleton on the client [source](./references/docs/createSharedComposable/index.md)

- Share state within the same component using `provideLocal()` and `injectLocal()` — allows accessing provided values without going through the parent/child boundary, now with full Vapor mode support [source](./references/docs/provideLocal/index.md)

- Replace manual watchers with `until()` for one-time async conditions — provides a promise-based API for flow control that resolves once a ref meets a specific requirement, reducing callback nesting [source](./references/docs/until/index.md)

```ts
// Preferred for one-time triggers
await until(isReady).toBe(true)
doSomething()
```

- Implement `refManualReset()` for easy state restoration — provides a built-in `.reset()` method to return the ref to its initial value, ideal for clearing forms or reset-to-default filters [source](./references/docs/refManualReset/index.md)

- Use `reactify()` to transform plain utility functions into reactive ones — automatically accepts refs as arguments and returns a `ComputedRef`, enabling rapid development of reactive logic [source](./references/docs/reactify/index.md)

- Optimize hot paths with `refWithControl()` using `peek()` and `lay()` — allows reading or writing a ref's value without triggering the reactivity system or tracking dependencies, minimizing unnecessary updates [source](./references/docs/refWithControl/index.md)

- Return dual object/array APIs via `makeDestructurable()` — makes your custom composables more flexible by allowing users to choose between positional (array) or named (object) destructuring [source](./references/docs/makeDestructurable/index.md)

- Convert state during synchronization with `syncRef()` custom transforms — use the `transform` option with `ltr` and `rtl` functions to map values between refs of different types [source](./references/docs/syncRef/index.md)

```ts
// Sync a number ref with a string ref
syncRef(count, stringCount, {
  transform: {
    ltr: left => String(left),
    rtl: right => Number(right)
  }
})
```

- Choose `createGlobalState()` for persistent application-wide singletons — unlike shared composables which dispose state when subscribers reach zero, global state remains alive for the entire app lifecycle [source](./references/docs/createGlobalState/index.md)
