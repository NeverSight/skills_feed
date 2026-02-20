---
name: vue-router-skilld
description: "ALWAYS use when writing code importing \"vue-router\". Consult for debugging, best practices, or modifying vue-router, vue router, router."
metadata:
  version: 5.0.2
  generated_by: Claude Code · Sonnet 4.5
  generated_at: 2026-02-18
---

# vuejs/router `vue-router`

**Version:** 5.0.2 (Feb 2026)
**Deps:** @babel/generator@^7.28.6, @vue-macros/common@^3.1.1, @vue/devtools-api@^8.0.0, ast-walker-scope@^0.8.3, chokidar@^5.0.0, json5@^2.2.3, local-pkg@^1.1.2, magic-string@^0.30.21, mlly@^1.8.0, muggle-string@^0.4.1, pathe@^2.0.3, picomatch@^4.0.3, scule@^1.3.0, tinyglobby@^0.2.15, unplugin@^3.0.0, unplugin-utils@^0.3.1, yaml@^2.8.2
**Tags:** next: 4.0.13 (Feb 2022), legacy: 3.6.5 (Sep 2022), edge: 4.4.0-alpha.3 (Jun 2024), beta: 5.0.0-beta.2 (Jan 2026), latest: 5.0.2 (Feb 2026)

**References:** [Docs](./references/docs/_INDEX.md) — API reference, guides • [GitHub Issues](./references/issues/_INDEX.md) — bugs, workarounds, edge cases • [GitHub Discussions](./references/discussions/_INDEX.md) — Q&A, patterns, recipes • [Releases](./references/releases/_INDEX.md) — changelog, breaking changes, new APIs

## API Changes

This section documents version-specific API changes — prioritize recent major/minor releases.

- NEW: `vue-router/vite` — v5 ships the Vite plugin (formerly `unplugin-vue-router/vite`) directly in the core package; import from `vue-router/vite` instead [source](./references/docs/guide/migration/v4-to-v5.md#2-update-imports)

- NEW: `vue-router/auto-routes` — v5 export that provides the auto-generated file-based route list; previously required `unplugin-vue-router` as a separate package [source](./references/docs/guide/migration/v4-to-v5.md#new-exports-reference)

- NEW: `vue-router/unplugin` — v5 export for Webpack/Rollup/esbuild plugins and utilities (`VueRouterAutoImports`, `EditableTreeNode`, `createRoutesContext`, etc.); previously imported from `unplugin-vue-router` [source](./references/docs/guide/migration/v4-to-v5.md#2-update-imports)

- NEW: `DataLoaderPlugin` + `defineBasicLoader` (experimental) — v5 adds data loaders directly to `vue-router/experimental`; previously in `unplugin-vue-router/data-loaders`. Install `DataLoaderPlugin` **before** the router with `app.use(DataLoaderPlugin, { router })` [source](./references/releases/v5.0.0.md#features)

- NEW: `defineColadaLoader` (experimental) — Pinia Colada-backed loader available at `vue-router/experimental/pinia-colada`; previously `unplugin-vue-router/data-loaders/pinia-colada` [source](./references/docs/guide/migration/v4-to-v5.md#2-update-imports)

- NEW: `NavigationResult` (experimental) — class from `vue-router/experimental` returned inside a loader to redirect during navigation (e.g. `return new NavigationResult('/login')`); previously did not exist in vue-router [source](./references/docs/data-loaders/defining-loaders.md#navigation-control)

- NEW: Volar plugins moved to `vue-router/volar/sfc-typed-router` and `vue-router/volar/sfc-route-blocks` — previously `unplugin-vue-router/volar/sfc-typed-router` and `unplugin-vue-router/volar/sfc-route-blocks` [source](./references/docs/guide/migration/v4-to-v5.md#2-update-imports)

- NEW: `TypesConfig` module augmentation — v4.4+ interface used to register `RouteNamedMap` for typed routes; augment with `declare module 'vue-router' { interface TypesConfig { RouteNamedMap: RouteNamedMap } }` [source](./references/docs/guide/advanced/typed-routes.md#manual-configuration)

- BREAKING: IIFE build no longer bundles `@vue/devtools-api` — v5 upgraded devtools-api to v8 which has no IIFE build; affects CDN/script-tag setups that relied on the bundled devtools [source](./references/releases/v5.0.0.md#v500)

- NEW: Query params optional by default (experimental) — v5 file-based routing makes query params optional in typed routes by default [source](./references/releases/v5.0.0.md#features)

**Also changed:** `unplugin-vue-router` types/utilities moved to `vue-router/unplugin` (renamed) · `route-map.d.ts` replaces `typed-router.d.ts` (renamed) · `meta.loaders` array on route records for manually connecting data loaders (NEW, experimental) · `router.currentRoute` is `Ref<RouteLocationNormalizedLoaded>` — access via `.value` (v4 BREAKING) · `router.onReady()` removed — use `router.isReady()` returning a Promise (v4 BREAKING) · `scrollBehavior` `x`/`y` renamed to `left`/`top` (v4 BREAKING)

## Best Practices

- Use `route.meta` directly in guards instead of iterating `to.matched` — Vue Router merges all ancestor `meta` fields non-recursively, so `to.meta.requiresAuth` already reflects inherited values from parent routes [source](./references/docs/guide/advanced/meta.md#typescript)

- Extend the `RouteMeta` interface via module augmentation to type all `meta` fields — this enforces that every route declares required fields at compile time rather than relying on runtime checks [source](./references/docs/guide/advanced/meta.md#typescript)

- Use `router.beforeResolve` (not `beforeEach`) for operations that must run after async components are resolved — it fires after all in-component guards and async route components are ready, making it the correct place for camera permission checks or final data validation [source](./references/docs/guide/advanced/navigation-guards.md#global-resolve-guards)

- Use `inject()` inside navigation guards (global or per-route) to access Pinia stores and provided values — this is supported since Vue 3.3 and avoids importing stores outside of `setup` context [source](./references/docs/guide/advanced/navigation-guards.md#global-injections-within-guards)

- Avoid the `next` callback in guards — return values (`false`, a route location, or nothing) instead; `next` is error-prone because it must be called exactly once per code path and is considered a legacy API [source](./references/docs/guide/advanced/navigation-guards.md#optional-third-argument-next)

- `await router.push()` and check the resolved value to detect navigation failures — the promise resolves to a `NavigationFailure` when blocked, or `undefined` on success; use `isNavigationFailure(result, NavigationFailureType.aborted)` to distinguish the specific failure type [source](./references/docs/guide/advanced/navigation-failures.md#detecting-navigation-failures)

- Set `props: true` (or a function) on route records to decouple components from `useRoute()` — components receiving params as props are reusable and testable without a router instance; use the function form (`props: route => ({ query: route.query.q })`) to map query params or cast types [source](./references/docs/guide/essentials/passing-props.md#function-mode)

- Watch specific `route` properties rather than the whole `route` object — `useRoute()` returns a reactive object, but watching it entirely triggers on any change (hash, query, params); narrow the watcher to `() => route.params.id` to avoid unnecessary fetches [source](./references/docs/guide/advanced/composition-api.md#accessing-the-router-and-current-route-inside-setup)

- (experimental) Use `defineBasicLoader` / `defineColadaLoader` exported from page components for navigation-aware data fetching — loaders exported from lazy-loaded route components are automatically connected to the navigation lifecycle, block the transition until resolved, and expose `isLoading`/`error` reactively; set `lazy: true` for non-critical data that should not block navigation [source](./references/docs/data-loaders/defining-loaders.md#non-blocking-loaders-with-lazy)
