---
name: pinia-skilld
description: "ALWAYS use when writing code importing \"pinia\". Consult for debugging, best practices, or modifying pinia."
metadata:
  version: 3.0.4
  generated_by: Claude Code · Sonnet 4.5
  generated_at: 2026-02-18
---

# vuejs/pinia `pinia`

**Version:** 3.0.4 (Nov 2025)
**Deps:** @vue/devtools-api@^7.7.7
**Tags:** next: 2.0.0-rc.10 (Sep 2021), beta: 2.1.8-beta.0 (Apr 2024), latest: 3.0.4 (Nov 2025)

**References:** [Docs](./references/docs/_INDEX.md) — API reference, guides • [GitHub Issues](./references/issues/_INDEX.md) — bugs, workarounds, edge cases • [GitHub Discussions](./references/discussions/_INDEX.md) — Q&A, patterns, recipes • [Releases](./references/releases/_INDEX.md) — changelog, breaking changes, new APIs

## API Changes

This section documents version-specific API changes — prioritize recent major/minor releases.

- BREAKING: `defineStore({ id: 'storeName', ... })` — object signature with `id` property removed in v3.0.0; use `defineStore('storeName', { ... })` instead. Old object syntax silently compiled but is now a runtime error [source](./references/releases/CHANGELOG.md#300-2025-02-11)

- BREAKING: `PiniaStorePlugin` type — removed in v3.0.0; use `PiniaPlugin` instead. Code using `PiniaStorePlugin` will fail to compile [source](./references/releases/CHANGELOG.md#300-2025-02-11)

- BREAKING: Vue 2 support dropped in v3.0.0 — Pinia v3 requires Vue 3 only. Users on Vue 2 must stay on Pinia v2 [source](./references/docs/cookbook/migration-v2-v3.md#new-versions)

- BREAKING: TypeScript 5 or newer required in v3.0.0 — uses native `Awaited` type introduced in TS 4.5; TS 5+ recommended [source](./references/releases/CHANGELOG.md#300-2025-02-11)

- BREAKING: IIFE bundle no longer bundles Vue Devtools in v3.0.0 — devtools API was too large; must be included manually depending on your workflow [source](./references/releases/CHANGELOG.md#300-2025-02-11)

- BREAKING: Package is now published as `type: module` in v3.0.0 — CJS dist files still provided but the package root is ESM. May break setups relying on implicit CJS resolution [source](./references/releases/CHANGELOG.md#300-2025-02-11)

- NEW: `action(fn, name?)` helper in setup stores — added in v2.2.0, available via `SetupStoreHelpers` parameter. Wraps a function so it is tracked by `$onAction` when called within the store; intended for advanced use cases like Pinia Colada [source](./references/releases/CHANGELOG.md#220-2024-07-26)

- NEW: `disposePinia(pinia)` — added in v2.1.7, stops the pinia effect scope and removes state, plugins, and stores. Useful in tests or multi-pinia apps; disposed instance cannot be reused [source](./references/releases/CHANGELOG.md#218-beta0-2024-04-17)

- NEW: `SetupStoreDefinition<Id, SS>` type — added in v2.1.7 for the return type of `defineStore()` when using a setup function. Extends `StoreDefinition` and enables better IDE support for setup stores [source](./references/releases/CHANGELOG.md#217-2023-10-13)

- NEW: `mapWritableState` now picks up writable `computed`s in setup stores — added in v2.3.0. Previously only `ref` state was mapped; `WritableComputedRef` returns from setup stores are now included [source](./references/releases/CHANGELOG.md#230-2024-12-04)

**Also changed:** `mapGetters` DEPRECATED (alias for `mapState`, still exported) · `getActivePinia()` returns `Pinia | undefined` (typed more strictly since v2.0.35) · `skipHydrate(obj)` stable — skips SSR hydration for non-state objects returned from setup stores · `shouldHydrate(obj)` exported utility for plugin authors

## Best Practices

- Use `$patch()` with a function callback rather than an object when mutating arrays or performing multiple related changes — the function form groups all mutations into a single devtools entry and avoids creating intermediate collections [source](./references/docs/core-concepts/state.md#mutating-the-state)

- Use `$subscribe()` instead of `watch()` on store state — subscriptions fire only once per `$patch` call regardless of how many individual properties changed, avoiding redundant callbacks when using the function form of `$patch` [source](./references/docs/core-concepts/state.md#subscribing-to-the-state)

- Pass `{ detached: true }` to `$subscribe()` and `true` as the second arg to `$onAction()` when you need listeners to outlive the component — by default both are automatically removed on component unmount [source](./references/docs/core-concepts/state.md#detaching-subscriptions)

- In setup stores, use `skipHydrate()` to wrap state properties that must not be picked up from SSR initial state (e.g., composables backed by `localStorage`, client-only refs) — without it, the server's serialized value will override the intended client-side source [source](./references/docs/cookbook/composables.md#ssr)

```ts
return {
  lastColor: skipHydrate(lastColor), // won't be overwritten by SSR state
  open,
}
```

- When a plugin adds new state properties, set the value on both `store.$state` (for SSR serialization and devtools) and `store` via `toRef(store.$state, 'key')` — setting only one breaks devtools display or reactivity sharing [source](./references/docs/core-concepts/plugins.md#adding-new-state)

- Wrap non-reactive external objects (router, class instances, third-party lib instances) with `markRaw()` before assigning them in plugins — prevents Vue from trying to deeply observe objects that aren't meant to be reactive [source](./references/docs/core-concepts/plugins.md#adding-new-external-properties)

- When composing stores that reference each other, place `useOtherStore()` calls before any `await` in async actions — after an `await` the active pinia context may have changed, causing the wrong instance to be returned in SSR [source](./references/docs/cookbook/composing-stores.md#shared-actions)

- Use `createTestingPinia()` from `@pinia/testing` for component tests rather than `createPinia()` — it stubs all actions by default and makes them inspectable as spies; pass plugins via the `plugins` option, not via `testingPinia.use()` [source](./references/docs/cookbook/testing.md#unit-testing-components)

- In options store getters, prefer arrow functions that receive `state` as the first parameter over regular functions using `this` — arrow function return types are inferred automatically, while `this`-based getters require an explicit return type annotation [source](./references/docs/core-concepts/getters.md#getters)
