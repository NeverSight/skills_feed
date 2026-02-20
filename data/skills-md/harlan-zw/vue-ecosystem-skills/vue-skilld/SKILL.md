---
name: vue-skilld
description: "ALWAYS use when editing or working with *.vue files or code importing \"vue\". Consult for debugging, best practices, or modifying vue, core."
metadata:
  version: 3.6.0-beta.6
  generated_by: Claude Code · Sonnet 4.5
  generated_at: 2026-02-18
---

# vuejs/core `vue`

**Version:** 3.6.0-beta.6 (Feb 2026)
**Deps:** @vue/shared@3.6.0-beta.6, @vue/runtime-dom@3.6.0-beta.6, @vue/runtime-vapor@3.6.0-beta.6, @vue/compiler-dom@3.6.0-beta.6, @vue/compiler-sfc@3.6.0-beta.6, @vue/server-renderer@3.6.0-beta.6
**Tags:** csp: 1.0.28-csp (Sep 2016), legacy: 2.7.16 (Dec 2023), v2-latest: 2.7.16 (Dec 2023), rc: 3.5.0-rc.1 (Aug 2024), alpha: 3.6.0-alpha.7 (Dec 2025), beta: 3.6.0-beta.6 (Feb 2026), latest: 3.5.28 (Feb 2026)

**References:** [Docs](./references/docs/_INDEX.md) — API reference, guides • [GitHub Issues](./references/issues/_INDEX.md) — bugs, workarounds, edge cases • [GitHub Discussions](./references/discussions/_INDEX.md) — Q&A, patterns, recipes • [Releases](./references/releases/_INDEX.md) — changelog, breaking changes, new APIs

## API Changes

This section documents version-specific API changes — prioritize recent major/minor releases.

- NEW: `createVaporApp()` (experimental) — new in v3.6, creates a Vapor-mode app instance without pulling in the Virtual DOM runtime; use `createApp()` for standard VDOM apps [source](./references/releases/v3.6.0-alpha.1.md#about-vapor-mode)

- NEW: `vaporInteropPlugin` (experimental) — new in v3.6, install into a VDOM `createApp()` instance to allow Vapor components inside VDOM trees; without it, Vapor SFCs cannot be used in VDOM apps [source](./references/releases/v3.6.0-beta.1.md#about-vapor-mode)

- NEW: `<script setup vapor>` attribute (experimental) — new in v3.6, opts an SFC into Vapor Mode compilation; only works with `<script setup>`; does not support Options API, `app.config.globalProperties`, or `getCurrentInstance()` [source](./references/releases/v3.6.0-beta.1.md#opting-in-to-vapor-mode)

- NEW: `useTemplateRef(key)` — new in v3.5, preferred replacement for plain `ref` variable names matching `ref="key"` attributes; supports dynamic string IDs at runtime unlike the old static-only pattern [source](./references/releases/blog-3.5.md#usetemplateref)

- NEW: `useId()` — new in v3.5, generates stable unique IDs per component instance guaranteed to match between SSR and client hydration; replaces manual ID management for form/accessibility attributes [source](./references/releases/blog-3.5.md#useid)

- NEW: `onWatcherCleanup(fn)` — new in v3.5, registers a cleanup callback inside a `watch` or `watchEffect` callback; replaces the `onCleanup` parameter pattern and can be called from nested functions [source](./references/releases/blog-3.5.md#onwatchercleanup)

- NEW: `hydrateOnVisible()`, `hydrateOnIdle()`, `hydrateOnInteraction()`, `hydrateOnMediaQuery()` — new in v3.5, lazy hydration strategies passed to `defineAsyncComponent({ hydrate: hydrateOnVisible() })`; without the `hydrate` option, async components hydrate immediately [source](./references/releases/blog-3.5.md#lazy-hydration)

- NEW: `defineModel()` stable — promoted from experimental in v3.3 to stable in v3.4; automatically declares a prop and returns a mutable ref; replaces the manual `defineProps` + `defineEmits('update:modelValue')` pattern [source](./references/releases/blog-3.4.md#definemodel-is-now-stable)

- NEW: `defineProps` destructure with defaults — stabilized in v3.5 (was experimental in v3.3); `const { count = 0 } = defineProps<{ count?: number }>()` replaces `withDefaults(defineProps<...>(), { count: 0 })`; destructured vars must be wrapped in getters to pass to `watch()` or composables [source](./references/releases/blog-3.5.md#reactive-props-destructure)

- BREAKING: `@vnodeXXX` event listeners — removed in v3.4, are now a compiler error; use `@vue:XXX` listeners instead (e.g. `@vue:mounted`) [source](./references/releases/blog-3.4.md#other-removed-features)

- BREAKING: Reactivity Transform (`$ref`, `$computed`, etc.) — removed in v3.4 after being deprecated in v3.3; was experimental and distinct from the now-stable props destructure feature; use Vue Macros plugin to continue using it [source](./references/releases/blog-3.4.md#other-removed-features)

- BREAKING: Global `JSX` namespace — no longer registered by default since v3.4; set `jsxImportSource: "vue"` in `tsconfig.json` or import `vue/jsx` to restore it; affects TSX users only [source](./references/releases/blog-3.4.md#global-jsx-namespace)

- BREAKING: `app.config.unwrapInjectedRef` — removed in v3.4; ref unwrapping in `inject()` is now always enabled and cannot be disabled [source](./references/releases/blog-3.4.md#other-removed-features)

- NEW: `<Teleport defer>` prop — new in v3.5, mounts the teleport after the current render cycle so the target element can be rendered by Vue in the same component tree; requires explicit `defer` attribute for backwards compatibility [source](./references/releases/blog-3.5.md#deferred-teleport)

**Also changed:** `defineSlots<{}>()` macro NEW v3.3 for typed slot declarations · `defineOptions({})` macro NEW v3.3 to set component options without a separate `<script>` block · `toRef(() => getter)` enhanced in v3.3 to accept plain values and getters · `toValue()` NEW v3.3 normalizes values/getters/refs to values (inverse of `toRef`) · `v-bind` same-name shorthand NEW v3.4 (`:id` shorthand for `:id="id"`) · `data-allow-mismatch` attribute NEW v3.5 to suppress hydration mismatch warnings · `useHost()` / `useShadowRoot()` NEW v3.5 for custom element host access · `v-is` directive REMOVED v3.4 (use `is="vue:ComponentName"` instead) · reactivity system alien-signals refactor in v3.6 improves memory usage with no API changes

## Best Practices

- Use reactive props destructure (3.5+) with native default value syntax instead of `withDefaults()` — destructured variables are reactive and the compiler rewrites accesses to `props.x` automatically. When passing to composables or `watch`, wrap in a getter: `watch(() => count, ...)` [source](./references/docs/api/sfc-script-setup.md#reactive-props-destructure)

- Use `toValue()` in composables to normalize `MaybeRefOrGetter<T>` arguments — handles plain values, refs, and getter functions uniformly so callers can pass any form without the composable caring [source](./references/docs/api/reactivity-utilities.md#tovalue)

- Use `onWatcherCleanup()` (3.5+) instead of the `onCleanup` callback parameter in `watch` and `watchEffect` — it can be called from any helper function in the sync execution stack, not just the top-level callback, making cleanup logic easier to extract [source](./references/docs/api/reactivity-core.md#onwatchercleanup)

- Use `useTemplateRef()` (3.5+) instead of a plain `ref` with a matching variable name for template refs — supports dynamic ref IDs and provides better IDE auto-completion and type checking via `@vue/language-tools` 2.1 [source](./references/docs/api/composition-api-helpers.md#usetemplateref)

- Use `useId()` (3.5+) for form element and accessibility IDs in SSR apps — generated IDs are stable across server and client renders, preventing hydration mismatches. Avoid calling inside `computed()` as it can cause instance conflicts [source](./references/docs/api/composition-api-helpers.md#useid)

- Use `shallowRef()` / `shallowReactive()` for large immutable data structures — deep reactivity tracks every property access via proxy traps; shallow variants avoid this overhead while still reacting to root `.value` replacement [source](./references/docs/guide/best-practices/performance.md#reduce-reactivity-overhead-for-large-immutable-structures)

- Pass computed values directly as `active` props rather than IDs for comparison — child components re-render when any received prop changes, so passing a stable boolean avoids re-rendering every list item when only one item's active state changes [source](./references/docs/guide/best-practices/performance.md#props-stability)

- When a computed returns a new object on every evaluation, accept `oldValue` and return it unchanged when data is equivalent — avoids unnecessary downstream effect triggers since Vue 3.4+ only triggers effects when the computed value reference changes [source](./references/docs/guide/best-practices/performance.md#computed-stability)

- Use `defineAsyncComponent` with a lazy hydration strategy (3.5+) for SSR — `hydrateOnVisible()`, `hydrateOnIdle()`, `hydrateOnInteraction()`, and `hydrateOnMediaQuery()` are tree-shakable and defer hydration until the component is actually needed

```ts
import { defineAsyncComponent, hydrateOnVisible } from 'vue'

const AsyncComp = defineAsyncComponent({
  loader: () => import('./Comp.vue'),
  hydrate: hydrateOnVisible()
})
```

[source](./references/docs/guide/components/async.md#lazy-hydration)

- (experimental) Opt in to Vapor Mode per-component with `<script setup vapor>` when targeting performance-sensitive UI — Vapor avoids Virtual DOM diffing entirely and achieves Solid/Svelte 5 benchmark parity, but does not support Options API, `app.config.globalProperties`, or `getCurrentInstance()`. Use `vaporInteropPlugin` to mix Vapor and VDOM components in an existing app [source](./references/releases/v3.6.0-beta.1.md#about-vapor-mode)
