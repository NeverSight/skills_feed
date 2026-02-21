---
name: tanstack-vue-router-skilld
description: "ALWAYS use when writing code importing \"@tanstack/vue-router\". Consult for debugging, best practices, or modifying @tanstack/vue-router, tanstack/vue-router, tanstack vue-router, tanstack vue router, router."
metadata:
  version: 1.161.1
  generated_by: Gemini CLI · Gemini 3 Flash
  generated_at: 2026-02-18
---

# TanStack/router `@tanstack/vue-router`

**Version:** 1.161.1 (Feb 2026)
**Deps:** @tanstack/vue-store@^0.8.0, @vue/runtime-dom@^3.5.25, isbot@^5.1.22, jsesc@^3.0.2, tiny-invariant@^1.3.3, tiny-warning@^1.0.3, @tanstack/history@1.154.14, @tanstack/router-core@1.161.1
**Tags:** latest: 1.161.1 (Feb 2026)

**References:** [Docs](./references/docs/_INDEX.md) — API reference, guides • [GitHub Issues](./references/issues/_INDEX.md) — bugs, workarounds, edge cases • [GitHub Discussions](./references/discussions/_INDEX.md) — Q&A, patterns, recipes • [Releases](./references/releases/_INDEX.md) — changelog, breaking changes, new APIs

## API Changes

This section documents version-specific API changes — prioritize recent major/minor releases.

- BREAKING: `NotFoundRoute` & `notFoundRoute` — v1.x deprecated the `NotFoundRoute` API and the `routerOptions.notFoundRoute` property. Use `notFoundComponent` in route options or `defaultNotFoundComponent` in `createRouter` instead [source](./references/docs/router/guide/not-found-errors.md:L5)

- BREAKING: `opts.navigate` — `opts.navigate` inside `beforeLoad` and `loader` is deprecated since v1.x. Use `throw redirect({ to: '...' })` for navigation-triggered redirects instead [source](./references/docs/router/api/router/RouteOptionsType.md:L118)

- DEPRECATED: `parseParams` & `stringifyParams` — these top-level route properties are deprecated in favor of nested `params.parse` and `params.stringify` objects for better organization [source](./references/docs/router/api/router/RouteOptionsType.md:L68)

- DEPRECATED: `preSearchFilters` & `postSearchFilters` — deprecated since v1.x in favor of the more powerful `search.middlewares` array for transforming search parameters [source](./references/docs/router/api/router/RouteOptionsType.md:L225)

- DEPRECATED: `<ScrollRestoration />` — the component is deprecated. Use the `useScrollRestoration` hook or the `defaultHashScrollIntoView` router option for automatic hash scrolling [source](./references/docs/router/guide/scroll-restoration.md:L64)

- NEW: `protocolAllowlist` — new `createRouter` option to prevent XSS by restricting allowed URL protocols in links and redirects (defaults to safe web protocols) [source](./references/docs/router/api/router/RouterOptionsType.md:L178)

- NEW: SSR Methods — `head`, `headers`, and `scripts` methods added to route options for server-side SEO metadata, script injection, and custom HTTP headers [source](./references/docs/router/api/router/RouteOptionsType.md:L305:360)

- NEW: `search.middlewares` — new array-based middleware system supporting `retainSearchParams` and `stripSearchParams` helpers to manage query params in generated links [source](./references/docs/router/guide/search-params.md#transforming-search-with-search-middlewares)

- NEW: Validation Adapters — `@tanstack/zod-adapter`, `@tanstack/valibot-adapter`, and `@tanstack/arktype-adapter` provide type-safe validation with distinct input/output type inference [source](./references/docs/router/guide/search-params.md#zod)

- NEW: `defaultViewTransition` — added to `createRouter` to enable native View Transitions API support during navigation where supported by the browser [source](./references/docs/router/api/router/RouterOptionsType.md:L201)

- NEW: `rewrite` — `createRouter` option for bidirectional URL transformation, allowing patterns like stripping locale prefixes before matching and adding them back in links [source](./references/docs/router/api/router/RouterOptionsType.md:L236)

- NEW: `Wrap` & `InnerWrap` — new `createRouter` properties for injecting global providers (e.g., Theme, Auth) that wrap the entire router or its inner content [source](./references/docs/router/api/router/RouterOptionsType.md:L291)

- NEW: `codeSplitGroupings` — provides fine-grained control over how the router groups lazy-loaded route assets (loader, component, etc.) into chunks [source](./references/docs/router/api/router/RouteOptionsType.md:L361)

- DEPRECATED: Router Classes — `Router`, `Route`, `RootRoute`, and `FileRoute` classes are deprecated in favor of factory functions like `createRouter`, `createRoute`, and `createFileRoute` [source](./references/docs/router/api/router/RouterClass.md:L7)

**Also changed:** `rootRouteWithContext` renamed to `createRootRouteWithContext` · `defaultRemountDeps` new · `defaultStructuralSharing` new · `NotFoundError.global` deprecated · `search.strict` new · `SearchSchemaInput` new tag · `standard-schema` support new

## Best Practices

- Use `getRouteApi(routeId)` for type-safe hook access in child components to avoid circular dependencies with route definitions [source](./references/docs/router/api/router/getRouteApiFunction.md#getrouteapi-returns)

- Follow the specific property order (e.g., `beforeLoad` before `loader`) in `createFileRoute` to ensure correct TypeScript inference for `context` and other properties [source](./references/docs/router/eslint/create-route-property-order.md:L1:15)

- Throw `redirect()` from `beforeLoad` for authentication to stop the loading lifecycle before any child route or loader executes [source](./references/docs/router/guide/authenticated-routes.md#redirecting)

- Use `zodValidator` with the `fallback()` generic from `@tanstack/zod-adapter` to provide defaults for invalid search params, keeping `Link` search props optional and type-safe [source](./references/docs/router/guide/search-params.md#zod)

- Configure `retainSearchParams` middleware in the root route to automatically persist global URL state (like themes or sessions) across all generated links [source](./references/docs/router/guide/search-params.md#transforming-search-with-search-middlewares)

- Include only necessary search params in `loaderDeps` to prevent unrelated URL changes from triggering redundant loader executions [source](./references/docs/router/guide/data-loading.md#using-loaderdeps-to-access-search-params)

- Pass the `abortController.signal` from loader context to async fetch calls to automatically cancel stale requests when users navigate away [source](./references/docs/router/guide/data-loading.md#using-the-abort-signal)

- Return promises directly from loaders for deferred data loading—manual wrapping with `defer()` is no longer required as promises are handled automatically [source](./references/docs/router/api/router/deferFunction.md:L5:10)

- Set `defaultPreload: 'intent'` in `createRouter` to enable global hover/touch-based preloading, which significantly improves perceived performance for most applications [source](./references/docs/router/guide/preloading.md#supported-preloading-strategies)

- Enable `defaultStructuralSharing: true` in `createRouter` to preserve object references in search param selectors and minimize unnecessary Vue component re-renders [source](./references/docs/router/guide/render-optimizations.md#structural-sharing-with-fine-grained-selectors)
