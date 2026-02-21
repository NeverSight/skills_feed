---
name: vue-data-ui-skilld
description: "ALWAYS use when writing code importing \"vue-data-ui\". Consult for debugging, best practices, or modifying vue-data-ui, vue data ui."
metadata:
  version: 3.15.2
  generated_by: Gemini CLI · Gemini 3 Flash
  generated_at: 2026-02-18
---

# graphieros/vue-data-ui `vue-data-ui`

**Version:** 3.15.2 (Feb 2026)
**Tags:** beta: 2.15.6-beta.3 (Jul 2025), next: 3.1.19-next.1 (Sep 2025), latest: 3.15.2 (Feb 2026)

**References:** [GitHub Issues](./references/issues/_INDEX.md) — bugs, workarounds, edge cases • [GitHub Discussions](./references/discussions/_INDEX.md) — Q&A, patterns, recipes • [Releases](./references/releases/_INDEX.md) — changelog, breaking changes, new APIs

## API Changes

This section documents version-specific API changes for `vue-data-ui` v3.15.2 — prioritize recent v3.x releases.

- NEW: `useCursorPointer` (opt-in) — default changed to `false` in v3.15.0; must be set to `true` in `userOptions` to enable pointer cursor on clickable elements [source](./references/releases/v3.15.0.md#cursor-pointer-is-now-opt-in-303)

- NEW: `altCopy` action button — added to context menu in v3.15.0; exposes `dataset` and `config` in a callback to generate custom alt text [source](./references/releases/v3.15.0.md#alt-text-copy-new-action-button)

- NEW: `minimap` styling — `handleType` ('grab', 'chevron', etc.), `handleWidth`, and `additionalHeight` added in v3.15.0 to customize zoom minimap handles [source](./references/releases/v3.15.0.md#chart-zoom-minimap)

- NEW: `dashIndices` in `VueUiXy` — new dataset property in v3.15.0 allows displaying specific datapoints as dashed segments to indicate estimated data [source](./references/releases/v3.15.0.md#vueuixy)

- BREAKING: `locales` files removed — as of v3.14.3, individual locale files are removed in favor of `Intl` for computing time labels [source](./references/releases/v3.14.3.md#reduce-package-size)

- NEW: `isPrintingImg` and `isPrintingSvg` — booleans now exposed in the `#svg` slot since v3.14.10 to control content during print/export [source](./references/releases/v3.14.10.md#all-charts-with-png-andor-svg-exports)

- NEW: `zoomStart`, `zoomEnd`, and `zoomReset` — new emits added to `VueUiXy` in v3.14.9 to track zoom component interactions [source](./references/releases/v3.14.9.md#vueuixy)

- NEW: `selectAllToggle` in Legend — opt-in feature added in v3.13.0; displays a checkbox to select/unselect all series when more than 2 series exist [source](./references/releases/v3.13.0.md#legend-toggle-new-feature-297)

- NEW: `skeletonConfig` customization — `VueUiSparkline` now allows passing custom `skeletonConfig` and `skeletonDataset` in v3.13.7 [source](./references/releases/v3.13.7.md#vueuisparkline)

- NEW: `oklch` color support — added in v3.13.6, allowing the use of OKLCH color space across all components [source](./references/releases/v3.13.6.md)

- NEW: `side` in `zoom.customFormat` — the handle side ('left' | 'right') is now exposed in the zoom formatting callback since v3.13.5 [source](./references/releases/v3.13.5.md#zoom-handle-sides)

- NEW: `zoom.maxWidth` — added to multiple charts in v3.13.4 to control the maximum width of the zoom component [source](./references/releases/v3.13.4.md)

- NEW: `pulse` in `VueUiSparkline` — optional animated pulse effect with trail added to line mode in v3.13.3 [source](./references/releases/v3.13.3.md#vueuisparkline)

- NEW: `Annotator` modes — straight line and arrow modes added to the built-in annotator in v3.12.0 [source](./references/releases/v3.12.0.md#built-in-annotator)

**Also changed:** `scaleMin`/`scaleMax` on minimap v3.11.1 · `pulse` trail refinement v3.15.2 · `zoom.startIndex`/`endIndex` support v2.4.42 · `useCanvas` option (experimental) · `Annotator` pixel labels v3.14.5 · `dashIndices` in minimap v3.14.8

## Best Practices

- Use `VueUiXyCanvas` for large datasets (1000+ points) with frequent updates (e.g., 100ms) to avoid browser performance bottlenecks from managing thousands of SVG DOM nodes [source](./references/discussions/discussion-125.md#accepted-answer)

- Enable `responsive: true` specifically for `VueUiXy` and `VueUiDonut` when placing them in flexible containers, ensuring they correctly fill parent height (set `height: 100%` on parent) [source](./references/discussions/discussion-270.md#accepted-answer)

- Programmatically control series visibility using the exposed `showSeries(name)` and `hideSeries(name)` methods instead of manipulating the dataset or triggering legend events [source](./references/issues/issue-261.md#feature-request-add-methods-to-programmatically-show-and-hide-series)

- Opt-in to the cursor pointer for clickable chart elements via `userOptions.useCursorPointer: true`, as it is disabled by default for better accessibility compliance [source](./references/releases/v3.15.0.md#cursor-pointer-is-now-opt-in-303)

- Implement custom alt text for charts by enabling `userOptions.buttons.altCopy: true` and providing a tailored string through the `userOptions.callbacks.altCopy` callback [source](./references/releases/v3.15.0.md#alt-text-copy-new-action-button)

- Configure PDF export orientation and scaling directly in `userOptions.print` to handle different chart aspect ratios without requiring manual JsPDF wiring [source](./references/releases/v3.15.0.md#chart-zoom-minimap)

- Signal estimated or projected data in `VueUiXy` by passing `dashIndices` in the dataset to render specific line segments as dashed [source](./references/releases/v3.15.0.md#vueuixy)

- Prevent label overlapping in dense charts by setting `hideLabelsUnderValue` (in Donut) or `hideUnderProportion` (in Treemap) to suppress labels for small segments [source](./references/discussions/discussion-187.md#optimization-request-for-vueuidonutevolution-component---label-overlapping-and-zero-value-handling)

- Reverse the y-axis (e.g., for ranking) by providing negative values in the dataset and using absolute value `formatters` for grid labels and tooltips [source](./references/discussions/discussion-194.md#accepted-answer)

```ts
// Reversed y-axis via negative values and absolute formatting
const config = {
  chart: {
    grid: { labels: { yAxis: { formatter: ({ value }) => Math.abs(value) } } }
  }
}
```

- Fine-tune the responsive behavior of table-based charts (like `VueUiCarouselTable`) by adjusting `responsiveBreakpoint` to control exactly when the layout switches for mobile [source](./references/discussions/discussion-75.md#accepted-answer)
