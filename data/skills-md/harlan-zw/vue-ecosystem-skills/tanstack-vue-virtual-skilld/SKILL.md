---
name: tanstack-vue-virtual-skilld
description: "ALWAYS use when writing code importing \"@tanstack/vue-virtual\". Consult for debugging, best practices, or modifying @tanstack/vue-virtual, tanstack/vue-virtual, tanstack vue-virtual, tanstack vue virtual, virtual."
metadata:
  version: 3.13.18
  generated_by: Gemini CLI · Gemini 3 Flash
  generated_at: 2026-02-18
---

# TanStack/virtual `@tanstack/vue-virtual`

**Version:** 3.13.18 (Jan 2026)
**Deps:** @tanstack/virtual-core@3.13.18
**Tags:** beta: 3.0.0-beta.68 (Oct 2023), latest: 3.13.18 (Jan 2026)

**References:** [Docs](./references/docs/_INDEX.md) — API reference, guides • [GitHub Issues](./references/issues/_INDEX.md) — bugs, workarounds, edge cases • [GitHub Discussions](./references/discussions/_INDEX.md) — Q&A, patterns, recipes • [Releases](./references/releases/_INDEX.md) — changelog, breaking changes, new APIs

## API Changes

This section documents version-specific API changes — prioritize recent major/minor releases.

- BREAKING: `useVirtualizer` — replaces `useVirtual` in v3 migration; older positional arguments or v2 option names are no longer supported [source](./references/docs/framework/vue/vue-virtual.md)

- BREAKING: `Ref<Virtualizer>` return type — v3 `useVirtualizer` returns a Vue `Ref` instead of a raw object; instance methods must be accessed via `.value` (e.g., `rowVirtualizer.value.getVirtualItems()`)

- BREAKING: `count` — replaces `size` option in v3 migration; using `size` will result in zero items being virtualized [source](./references/docs/api/virtualizer.md)

- BREAKING: `getScrollElement` — replaces `parentRef` option in v3 migration; must be a function that returns the scrollable element or `null` [source](./references/docs/api/virtualizer.md)

- BREAKING: `measureElement` — replaces `measureRef` pattern from v2; you must now pass `virtualizer.value.measureElement` to the `ref` attribute and set `data-index` on the element [source](./references/docs/api/virtualizer.md)

- NEW: `getTotalSize()` auto-updates — as of v3.13.13, the virtualizer automatically notifies the framework when the `count` option changes, ensuring `getTotalSize()` and the UI update correctly without manual workarounds for filtering or search [source](./references/releases/@tanstack/vue-virtual@3.13.13.md)

- NEW: `lanes` — new in v3; allows dividing the list into multiple columns (vertical) or rows (horizontal) to support grid-like or masonry layouts [source](./references/docs/api/virtualizer.md)

- NEW: `gap` — new in v3; specifies the spacing between items in pixels, removing the need for manual margin or padding calculations [source](./references/docs/api/virtualizer.md)

- NEW: `useWindowVirtualizer` — specialized adapter for window-based scrolling; simplifies configuration when the browser window is the scroll container [source](./references/docs/framework/vue/vue-virtual.md)

- NEW: `scrollMargin` — allows specifying the offset between the scroll container's start and the beginning of the virtualized list; essential for lists preceded by headers [source](./references/docs/api/virtualizer.md)

- NEW: `isRtl` — built-in support for right-to-left language locales; inverts horizontal scrolling logic when enabled [source](./references/docs/api/virtualizer.md)

- NEW: `useScrollendEvent` — utilizes the native `scrollend` event where available to reset `isScrolling` state, falling back to a debounced timer if disabled [source](./references/docs/api/virtualizer.md)

- NEW: `shouldAdjustScrollPositionOnItemSizeChange` — provides fine-grained control over scroll position adjustments when dynamic items differ from their estimated size [source](./references/docs/api/virtualizer.md)

- NEW: `useAnimationFrameWithResizeObserver` — added in v3.13.x; defers ResizeObserver measurement processing to the next animation frame to batch DOM mutations [source](./references/docs/api/virtualizer.md)

**Also changed:** `isScrollingResetDelay` new in v3 · `rangeExtractor` now receives `Range` object · `VirtualItem` adds `lane` property · `resizeItem` method for manual size overrides · `enabled` option to pause observers

## Best Practices

- Account for `scrollMargin` in absolute positioning — when using a shared scroll container with static headers, subtract the margin from the item's start position to maintain correct layout [source](./references/docs/api/virtualizer.md)

```vue
<script setup>
const rowVirtualizer = useVirtualizer({
  count: 1000,
  scrollMargin: 100, // Height of header
  // ...
})
</script>

<template>
  <div v-for="item in rowVirtualizer.getVirtualItems()" :key="item.key"
    :style="{
      transform: `translateY(${item.start - rowVirtualizer.options.scrollMargin}px)`
    }"
  >
    {{ item.index }}
  </div>
</template>
```

- Overestimate `estimateSize` for dynamic elements — providing a "maximum likely" size prevents the scrollbar from jumping and items from "resetting" their position when scrolling upwards into unmeasured territory [source](./references/docs/api/virtualizer.md)

- Implement `shouldAdjustScrollPositionOnItemSizeChange` for chat/messaging UIs — use this callback to control scroll adjustments when prepending items, preventing visual jumps as new elements are measured [source](./references/docs/api/virtualizer.md)

- Attach `data-index` when using `measureElement` — the virtualizer requires this attribute on the measured DOM element to correctly map the size back to the item's internal state [source](./references/docs/api/virtualizer.md)

```vue
<div
  v-for="item in virtualizer.getVirtualItems()"
  :key="item.key"
  :data-index="item.index"
  :ref="virtualizer.measureElement"
>
  {{ item.index }}
</div>
```

- Pass configuration via `computed` or `Ref` — the Vue adapter's `useVirtualizer` watch-triggers `setOptions` automatically, allowing the instance to reactively update `count` or `overscan` without manual re-instantiation

- Avoid `useAnimationFrameWithResizeObserver` for performance — native `ResizeObserver` is already batched; enabling this adds a ~16ms delay that can cause visual flickering or stale measurements during fast scrolls [source](./references/docs/api/virtualizer.md)

- Provide a stable `getItemKey` for persistent state — using a unique identifier (like a database ID) instead of the default index ensures that item state (focus, internal refs) is preserved during reorders or filtering [source](./references/docs/api/virtualizer.md)

- Wrap initial `scrollToIndex` in `requestAnimationFrame` — for "scroll-to-bottom" initialization (e.g. chat), deferring the scroll ensures the DOM is rendered and initial measurements are processed by the virtualizer [source](./references/discussions/discussion-911.md)

- Use built-in `gap` over manual CSS margins — the `gap` option ensures the virtualizer accounts for item spacing in its internal `getTotalSize()` calculation, which manual margins do not [source](./references/docs/api/virtualizer.md)

- Pause observers with `enabled: false` — instead of unmounting the virtualizer, toggle the `enabled` option to pause monitoring (e.g., when a tab is hidden). This preserves existing measurements while saving CPU cycles [source](./references/docs/api/virtualizer.md)
