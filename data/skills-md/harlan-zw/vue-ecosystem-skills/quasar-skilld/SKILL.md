---
name: quasar-skilld
description: "ALWAYS use when writing code importing \"quasar\". Consult for debugging, best practices, or modifying quasar."
metadata:
  version: 2.18.6
  generated_by: Gemini CLI · Gemini 3 Flash
  generated_at: 2026-02-18
---

# quasarframework/quasar `quasar`

**Version:** 2.18.6 (Nov 2025)
**Tags:** legacy: 1.22.10 (May 2023), latest: 2.18.6 (Nov 2025)

**References:** [Docs](./references/docs/_INDEX.md) — API reference, guides • [GitHub Issues](./references/issues/_INDEX.md) — bugs, workarounds, edge cases • [GitHub Discussions](./references/discussions/_INDEX.md) — Q&A, patterns, recipes • [Releases](./references/releases/_INDEX.md) — changelog, breaking changes, new APIs

## API Changes

This section documents version-specific API changes — prioritize recent major/minor releases.

- BREAKING: `v-model` -> uses `model-value` + `@update:model-value` instead of `value` + `@input` in Vue 3 [source](./references/docs/start/upgrade-guide/upgrade-guide.md#vue-3-and-v-model)

- BREAKING: `QDrawer`/`QDialog`/`QMenu`/`QTooltip` -> use `class` and `style` attributes instead of `content-class`/`content-style` props [source](./references/docs/start/upgrade-guide/upgrade-guide.md#qdrawerqdialogqmenuqtooltip)

- BREAKING: `QImg` -> completely redesigned, removed `transition` and `basic` props; renamed `no-default-spinner` to `no-spinner` [source](./references/docs/start/upgrade-guide/upgrade-guide.md#qimg)

- BREAKING: `QScrollArea` -> methods `getScrollPosition` returns `{ top, left }`; `setScrollPosition` and `setScrollPercentage` require `axis` parameter [source](./references/docs/start/upgrade-guide/upgrade-guide.md#qscrollarea)

- BREAKING: `QTable` -> renamed `data` prop to `rows` to avoid TS naming conflicts [source](./references/docs/start/upgrade-guide/upgrade-guide.md#qtable)

- BREAKING: `Platform.is` -> all boolean properties now explicitly `false` instead of `undefined` since v2.17.0 [source](./references/repos/quasarframework/quasar/releases/vquasar-v2.17.0.md#potential-upgrade-issue)

- BREAKING: `colors` utils -> `getBrand` and `setBrand` replaced by `getCssVar` and `setCssVar` respectively [source](./references/docs/start/upgrade-guide/upgrade-guide.md#color-utils)

- BREAKING: Scroll utils -> renamed `getScrollPosition` to `getVerticalScrollPosition`, `animScrollTo` to `animVerticalScrollTo`, and `setScrollPosition` to `setVerticalScrollPosition` [source](./references/docs/start/upgrade-guide/upgrade-guide.md#scroll-utils)

- BREAKING: `date` utils -> `addToDate` and `subtractFromDate` property names normalized (e.g., `year` -> `years`, `month` -> `months`) [source](./references/docs/start/upgrade-guide/upgrade-guide.md#date-utils)

- BREAKING: `QPopupEdit` -> must now use the default slot with `v-slot="scope"` for performance [source](./references/docs/start/upgrade-guide/upgrade-guide.md#qpopupedit)

- BREAKING: `GoBack` directive -> removed; use router reference (`$router.back()` or `$router.go(-1)`) instead [source](./references/docs/start/upgrade-guide/upgrade-guide.md#quasar-directives)

- NEW: `useQuasar` composable -> primary method for accessing the `$q` object within Composition API components

- NEW: `useMeta` composable -> new way to define meta tags, replacing the now deprecated `meta` component property [source](./references/docs/start/upgrade-guide/upgrade-guide.md#meta-plugin)

- NEW: `QTable` props -> added `table-row-style-fn`, `table-row-class-fn`, `grid-style-fn`, and `grid-class-fn` in v2.18.0 [source](./references/repos/quasarframework/quasar/releases/vquasar-v2.18.0.md#new)

**Also changed:** `useFormChild()` new composable · `QOptionsGroup` props `option-value`, `option-label`, `option-disable` new v2.17.0 · `QUploader` prop `thumbnail-fit` new v2.17.0 · `QSelect` prop `disable-tab-select` new v2.17.0 · `QMenu`/`QBtnDropdown` `no-esc-dismiss` new v2.18.0 · `evt.qAvoidFocus` new flag v2.18.0 · `QDate` model-value no longer contains `changed` prop · `QPagination` prop `gutter` new · `QImg` props `loading`, `crossorigin`, `fit` new · `Dialog` plugin custom component props moved to `componentProps` · `Loading` plugin uses `html: true` for HTML content instead of `sanitize` · `App.vue` wrapper `<div id="q-app">` removed · `.sync` modifier replaced by `v-model:propName`

## Best Practices

- Use `#q-app/wrappers` instead of `quasar/wrappers` for defining configurations and boot files — provides superior type inference and alignment with modern Quasar CLI [source](./references/docs/quasar-cli-vite/upgrade-guide.md:L256:258)

- Use **Regle** as the recommended validation library for `QInput` and `QField` — provides a robust, externalized validation logic compared to inline rules [source](./references/docs/vue-components/input.md:L319)

- Prefer **responsive CSS classes** (e.g., `gt-sm`, `lt-md`) over the `Screen` plugin in JavaScript — minimizes re-renders and layout shifts by leveraging CSS media queries directly [source](./references/docs/options/screen-plugin.md:L5)

- Bootstrap custom dialog components with the `useDialogPluginComponent` composable — handles the complex internal communication and lifecycle requirements of the Dialog plugin automatically [source](./references/docs/vue-composables/use-dialog-plugin-component.md:L13:30)

- Enable the `no-transition` prop on `QTree` when rendering large datasets — significantly improves runtime performance by skipping expensive expansion/collapse animations [source](./references/docs/vue-components/tree.md:L31)

- Use Quasar's `useInterval` and `useTimeout` composables over native browser timers — ensures automatic cancellation and memory cleanup when the component is unmounted [source](./references/docs/vue-composables/use-interval.md:L8:11)

- Place `QPullToRefresh` as a direct child of `QPage` when using `QLayout` — ensures correct scroll event interception and native-like pull behavior within the layout container [source](./references/docs/vue-components/pull-to-refresh.md:L42)

- Avoid setting `Dark` mode to `auto` in SSR applications — prevents the "flicker" effect where the server renders light mode before the client synchronizes with system preferences [source](./references/docs/quasar-plugins/dark.md:L85:87)

- Do not use `v-model` with `QRouteTab` components — the active state is derived directly from the current route, and manual model updates will not trigger navigation [source](./references/docs/vue-components/tabs.md:L128:132)

- Prefer the **Loading Bar Plugin** over manual `QAjaxBar` component instances — provides a simpler, globally managed progress indicator for all Ajax calls without per-page wiring [source](./references/docs/vue-components/ajax-bar.md:L18:19)
