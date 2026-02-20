---
name: vueuse-components-skilld
description: "ALWAYS use when writing code importing \"@vueuse/components\". Consult for debugging, best practices, or modifying @vueuse/components, vueuse/components, vueuse components, vueuse."
metadata:
  version: 14.2.1
  generated_by: Gemini CLI · Gemini 3 Flash
  generated_at: 2026-02-18
---

# vueuse/vueuse `@vueuse/components`

**Version:** 14.2.1 (Feb 2026)
**Deps:** @vueuse/shared@14.2.1, @vueuse/core@14.2.1
**Tags:** next: 5.0.0 (Jun 2021), alpha: 14.0.0-alpha.3 (Sep 2025), beta: 14.0.0-beta.1 (Sep 2025), latest: 14.2.1 (Feb 2026)

**References:** [Docs](./references/docs/_INDEX.md) — API reference, guides • [GitHub Issues](./references/issues/_INDEX.md) — bugs, workarounds, edge cases • [GitHub Discussions](./references/discussions/_INDEX.md) — Q&A, patterns, recipes • [Releases](./references/releases/_INDEX.md) — changelog, breaking changes, new APIs

## API Changes

This section documents version-specific API changes for `@vueuse/components` — prioritize recent major/minor releases.

- BREAKING: `@vueuse/components` v14+ requires Vue 3.5+, following core library requirements [source](./references/releases/v14.0.0.md)

- BREAKING: Renderless components refactored for consistency in v14.0.0. Components like `OnClickOutside` and `OnLongPress` now use an `options` prop for configuration and `@trigger` emit for actions [source](./references/releases/v14.0.0.md)

- BREAKING: ESM-only package — CJS build has been dropped since v13.0.0 [source](./references/releases/v13.0.0.md)

- DEPRECATED: `VOnClickOutside` is deprecated in favor of the lowercase `vOnClickOutside` directive [source](./references/releases/v14.0.0.md)

- DEPRECATED: `VOnLongPress` is deprecated in favor of the lowercase `vOnLongPress` directive [source](./references/releases/v14.0.0.md)

- NEW: `UseDraggable` supports `autoScroll` and `restrictInView` options for constrained dragging in v14.2.0 [source](./references/releases/v14.2.0.md)

- NEW: `UseDraggable` supports `storageKey` and `storageType` props for persistent element position [source](./references/docs/useDraggable.md)

- NEW: `vOnKeyStroke` directive added for listening to keyboard events directly on elements

- NEW: `UseIdle` default slot data now includes `pause` and `resume` methods via `Stoppable` implementation [source](./references/releases/v14.0.0.md)

- NEW: `vInfiniteScroll` supports reactive `canLoadMore` option in v14.1.0 [source](./references/releases/v14.1.0.md)

- NEW: `UseElementVisibility` added `initialValue` option in v14.1.0 [source](./references/releases/v14.1.0.md)

- NEW: `UseMouseInElement` supports tracking inline-level elements in v14.1.0 [source](./references/releases/v14.1.0.md)

- NEW: `vIntersectionObserver` now supports reactive `rootMargin` option in v14.2.0 [source](./references/releases/v14.2.0.md)

- NEW: `UseOffsetPagination` emits `page-change`, `page-size-change`, and `page-count-change` events

**Also changed:** `useTransition` custom interpolators · `refManualReset` new function · `tryOnScopeDispose` failSilently · `useAsyncState` execute result · `useTimeAgoIntl` custom units

## Best Practices

- Use the `storage-key` and `storage-type` props on the `<UseDraggable>` component to automatically persist element position in `localStorage` or `sessionStorage` across sessions [source](./references/docs/useDraggable.md)

- Utilize the `ignore` option in `OnClickOutside` (component or directive) to pass an array of refs or CSS selectors for elements that should not trigger the handler, essential for complex UIs like nested modals [source](./references/docs/onClickOutside.md)

- Always provide `#loading` and `#error` slots in `<UseImage>` to prevent layout shifts and handle broken images gracefully, rather than managing loading states manually in the script [source](./references/docs/useImage.md)

- Prefer `createReusableTemplate` over extracting small, repeated UI fragments into separate files to maintain access to local scope variables and avoid tedious prop/emit definitions [source](./references/docs/createReusableTemplate.md)

- Provide a generic type to `createReusableTemplate<T>()` to enable full TypeScript support and IDE autocompletion for data passed between `DefineTemplate` and `ReuseTemplate` [source](./references/docs/createReusableTemplate.md)

- Use `createTemplatePromise` to call complex UI elements like modals or dialogs as promises, keeping the UI definition in the template while maintaining programmatic control and clean async/await flows [source](./references/docs/createTemplatePromise.md)

- Configure `@vueuse/components` directives like `v-on-click-outside` or `v-on-long-press` using the `[handler, options]` array syntax for clean, inline logic without needing a separate setup variable for options [source](./references/docs/onClickOutside.md)

```vue
<div v-if="modal" v-on-click-outside="[closeModal, { ignore: [ignoreElRef] }]">
  Hello World
</div>
```

- Use the `<UseOffsetPagination>` component to handle complex pagination state; it emits clean events (`page-change`, `page-size-change`) that are more idiomatic and easier to wire up in templates than manually watching refs [source](./references/docs/useOffsetPagination.md)

- Set `detectIframe: true` in `onClickOutside` options when building global navigation or modals to ensure they close when the user clicks inside an iframe, an edge case often missed in manual implementations [source](./references/docs/onClickOutside.md)

- Utilize the `as` prop on renderable components like `<UseElementBounding>` or `<UseFullscreen>` to render them as semantically correct HTML elements (e.g., `section`, `nav`) instead of the default `div` [source](./references/docs/useImage.md)
