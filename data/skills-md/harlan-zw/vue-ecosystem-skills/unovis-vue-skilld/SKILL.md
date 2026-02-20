---
name: unovis-vue-skilld
description: "ALWAYS use when writing code importing \"@unovis/vue\". Consult for debugging, best practices, or modifying @unovis/vue, unovis/vue, unovis vue, unovis."
metadata:
  version: 1.6.4
  generated_by: Gemini CLI · Gemini 3 Flash
  generated_at: 2026-02-18
---

# f5/unovis `@unovis/vue`

**Version:** 1.6.4 (Jan 2026)
**Tags:** beta: 1.6.5-topojson.0 (Feb 2026), latest: 1.6.4 (Jan 2026)

**References:** [Docs](./references/docs/_INDEX.md) — API reference, guides • [GitHub Issues](./references/issues/_INDEX.md) — bugs, workarounds, edge cases • [GitHub Discussions](./references/discussions/_INDEX.md) — Q&A, patterns, recipes • [Releases](./references/releases/_INDEX.md) — changelog, breaking changes, new APIs

## API Changes

This section documents version-specific API changes for `@unovis/vue` — prioritize recent major/minor releases.

- NEW: `VisPlotband` and `VisPlotline` — new auxiliary components for highlighting data ranges or specific values [source](./references/releases/v1.6.md)

- NEW: `VisRollingPinLegend` — new specialized legend component added in v1.6.0 [source](./references/releases/v1.6.md)

- NEW: `VisTreemap` — new hierarchical data visualization component; includes `tileShowHtmlTooltip` and `topLevelParent` props as of v1.6.4 [source](./references/releases/v1.6.md)

- NEW: `VisAnnotations` — new component for adding callouts and annotations to charts [source](./references/releases/v1.4.0.md)

- NEW: `onRenderComplete` — new callback available in `VisXYContainer` and `VisSingleContainer` to detect when rendering is finished [source](./references/releases/v1.6.4.md)

- NEW: `VisArea` enhancements — added `stackMinHeight` for better visibility of small values and optional line display via core config [source](./references/releases/v1.6.4.md)

- NEW: `VisSankey` updates — new `onLayoutCalculated` callback, `getSankeyDepth` method, and support for Zoom/Pan and Node selection [source](./references/releases/v1.6.4.md)

- NEW: `VisGraph` features — support for custom node rendering functions, SVG link labels, and Zoom start/end callbacks [source](./references/releases/v1.5.0.md)

- NEW: `VisCrosshair` additions — new `forceShowAt` prop, `onCrosshairMove` callback, and `skipRangeCheck` configuration [source](./references/releases/v1.6.md)

- NEW: SSR Readiness — major internal refactor to support SSR (Server-Side Rendering) for Nuxt and other frameworks [source](./references/releases/v1.6.4.md)

- NEW: Reactive Map Data — `VisLeafletMap` data property is now fully reactive in Vue [source](./references/releases/v1.6.1.md)

- NEW: Automatic Tooltip Placement — `VisTooltip` now automatically aligns when used in conjunction with `VisCrosshair` [source](./references/releases/v1.5.0.md)

- NEW: `VisBulletLegend` — now supports multiple colors per legend item [source](./references/releases/v1.6.md)

- NEW: `VisXYContainer` — improved `scaleByDomain` behavior to ensure consistency across multiple chart types [source](./references/releases/v1.4.0.md)

**Also changed:** `calc()` support in Annotations · `theme-patterns` accessible theme · `VisFlowLegend` refactored wrapper · `axis grid line dasharray` CSS variables · `skipRangeCheck` Crosshair prop

## Best Practices

- Support ordinal values in XY components by returning the data index in the `x` accessor and providing a `tickFormat` to the `VisAxis` [source](./references/docs/guides/tips-and-tricks.mdx)

```vue
<script setup lang="ts">
const x = (d, i: number) => i
const tickFormat = (i: number) => data[i].category
</script>

<template>
  <VisXYContainer :data="data">
    <VisStackedBar :x="x" :y="d => d.value" />
    <VisAxis type="x" :tick-format="tickFormat" />
  </VisXYContainer>
</template>
```

- Define custom SVG gradients or patterns using the `svgDefs` property on `VisXYContainer` or `VisSingleContainer` [source](./references/docs/guides/tips-and-tricks.mdx)

```vue
<template>
  <VisXYContainer :svg-defs="gradientDef">
    <VisArea :x="d => d.x" :y="d => d.y" color="url(#gradient-id)" />
  </VisXYContainer>
</template>
```

- Display continuous lines across missing data points by filtering `null` values and passing the dataset directly to `VisLine` instead of the container [source](./references/discussions/discussion-333.md)

```vue
<template>
  <VisXYContainer>

    <VisLine :data="data.filter(d => d.value !== null)" :x="x" :y="y" />
  </VisXYContainer>
</template>
```

- Attach events to axis ticks or other sub-elements using the `events` prop and component-specific selectors [source](./references/discussions/discussion-219.md)

```vue
<script setup lang="ts">
import { VisAxisSelectors } from '@unovis/vue'
const axisEvents = {
  [VisAxisSelectors.tick]: {
    click: (val: number) => console.log('Clicked tick:', val)
  }
}
</script>

<template>
  <VisAxis type="x" :events="axisEvents" />
</template>
```

- Wrap Unovis components in `<ClientOnly>` when using Nuxt or SSR to prevent errors from top-level `document` or `window` references [source](./references/issues/issue-607.md)

```vue
<template>
  <ClientOnly>
    <VisXYContainer :data="data">
      <VisLine :x="x" :y="y" />
    </VisXYContainer>
  </ClientOnly>
</template>
```

- Enable tooltips or interactions on TopoJSON map areas using the `feature` selector [source](./references/discussions/discussion-524.md)

```vue
<script setup lang="ts">
import { VisTopoJSONMapSelectors } from '@unovis/vue'
const triggers = {
  [VisTopoJSONMapSelectors.feature]: d => d.properties.name
}
</script>

<template>
  <VisTopoJSONMap :triggers="triggers" ... />
</template>
```

- Fix clipped top or bottom axis labels by increasing the `margin` property on the `VisXYContainer` [source](./references/discussions/discussion-354.md)

```vue
<template>

  <VisXYContainer :margin="{ top: 10, right: 10, bottom: 10, left: 10 }">
    <VisStackedBar ... />
  </VisXYContainer>
</template>
```

- Use `tickTextWidth` on `VisAxis` to enable automatic label wrapping and trimming for long axis labels [source](./references/releases/v1.6.md)

```vue
<template>
  <VisAxis type="x" :tick-text-width="100" />
</template>
```

- Display multiple colors within a single legend bullet by passing an array to the `color` property of a legend item [source](./references/docs/auxiliary/BulletLegend.mdx)

```vue
<script setup lang="ts">
const items = [
  { name: 'Multi-segment', color: ['#ff0000', '#00ff00', '#0000ff'] }
]
</script>

<template>
  <VisBulletLegend :items="items" />
</template>
```

- Programmatically control crosshair visibility and position using the `forceShowAt` property for custom sync or interaction logic [source](./references/releases/v1.6.md)

```vue
<template>

  <VisCrosshair :force-show-at="{ x: 1707093300 }" />
</template>
```
