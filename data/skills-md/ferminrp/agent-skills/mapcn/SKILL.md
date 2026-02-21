---
name: mapcn
description: >
  Technical guide to integrate mapcn in React + shadcn projects.
  Use when the user asks to integrate mapcn, add mapcn to a shadcn app,
  use mapcn MapControls/Markers/Routes/Clusters, implement controlled
  viewport state, use the useMap hook, or access MapLibre through mapcn.
---

# mapcn

## When to Use This Skill

Use this skill when the user needs to install, integrate, customize, or troubleshoot mapcn in a React + shadcn/ui codebase.

Typical triggers:

- `integrate mapcn`
- `add mapcn to shadcn project`
- `mapcn MapControls/Markers/Routes/Clusters`
- `controlled map viewport with mapcn`
- `useMap hook mapcn`
- `MapLibre with mapcn components`

## Library Overview

mapcn provides copy-paste style map components built on top of MapLibre GL JS and aligned with shadcn/ui workflows.

Assumptions:

- Project uses React.
- Tailwind CSS is already configured.
- shadcn/ui is already configured.

Default behavior:

- mapcn uses free CARTO tiles by default.
- No API key is required for the default tile setup.

## Installation

Canonical install command:

```bash
npx shadcn@latest add @mapcn/map
```

Expected integration result:

- UI map components are added to the project (typically under `components/ui`).
- Import pattern usually follows:

```ts
import { Map } from "@/components/ui/map";
```

## Quick Start

Use a fixed-height container and render `Map` with `MapControls`.

```tsx
import { Map, MapControls } from "@/components/ui/map";

export function BasicMap() {
  return (
    <div className="h-[500px] w-full overflow-hidden rounded-xl border">
      <Map
        initialViewState={{
          longitude: -58.3816,
          latitude: -34.6037,
          zoom: 11,
        }}
      >
        <MapControls
          showZoom
          showCompass
          showLocate
          showFullscreen
          position="top-right"
        />
      </Map>
    </div>
  );
}
```

Important:

- The map container must have an explicit height, otherwise the map may render blank.

## Core Components

### Map and Controlled Viewport

Use uncontrolled mode for simple cases, and controlled mode when state synchronization is needed.

```tsx
const [viewport, setViewport] = useState({
  longitude: -58.3816,
  latitude: -34.6037,
  zoom: 11,
});

<Map viewport={viewport} onViewportChange={setViewport} />
```

### Controls

`MapControls` supports common toggles and placement:

- `showZoom`
- `showCompass`
- `showLocate`
- `showFullscreen`
- `position`

### Markers and Marker UI Family

Use marker composition for richer UI:

- `MapMarker`
- `MarkerContent`
- `MarkerPopup`
- `MarkerTooltip`
- `MarkerLabel`

### Standalone Popups

Use `MapPopup` for popup UI not strictly attached to a marker component.

### Routes

Use `MapRoute` to draw path-based overlays and route-like lines.

### Clusters

Use `MapClusterLayer` with GeoJSON input for dense point datasets.

## Advanced Integration

### `MapRef`

Use `MapRef` for imperative map actions such as `flyTo`, custom camera transitions, and direct map instance operations.

### `useMap`

Use `useMap` to access map context safely and wire event listeners with lifecycle-aware cleanup.

### Custom Styles

Use `styles` prop (or the corresponding map style config option) with MapLibre-compatible style URLs/specs when default tiles are not enough.

## Performance Guidelines

- DOM markers are fine for small to medium volumes (typically up to a few hundred points).
- For large datasets, prefer GeoJSON layer-based rendering and clustering (`MapClusterLayer`).
- Avoid excessive re-renders by stabilizing props and handlers.
- Always clean up event listeners when using advanced map events.

## Troubleshooting

### Blank Map

Check:

- Container height is explicitly set.
- Style URL/spec is valid.
- Tile requests are not blocked (network/CORS).

### Hydration / App Framework Issues

- Ensure map rendering is client-safe in SSR app setups.
- Avoid direct map instance access before mount.

### Missing Controls or Markers

- Confirm components are nested under the correct map context.
- Verify expected children hierarchy for marker and popup components.

### Type/Coordinate Errors

- Validate coordinate shape/order and prop types.
- Keep callback signatures aligned with component expectations.

## Workflow for Agents

1. Detect user intent: install, basic map, markers, popups, routes, clusters, advanced events.
2. Implement the smallest working integration first.
3. Move to controlled viewport only when state sync is required.
4. Switch to cluster/layer patterns when point count grows.
5. Return concise code, then explain decisions and next steps.

## Out of Scope

- Non-React frameworks.
- Unrequested wrapper migration/comparison work.
- Hosted map vendor account setup beyond mapcn default/no-key baseline.

## References

Local references:

- `references/docs-pages.md`
- `references/api-cheatsheet.md`

Canonical docs:

- `https://www.mapcn.dev/docs`
- `https://www.mapcn.dev/docs/installation`
- `https://www.mapcn.dev/docs/api-reference`
- `https://www.mapcn.dev/docs/basic-map`
- `https://www.mapcn.dev/docs/controls`
- `https://www.mapcn.dev/docs/markers`
- `https://www.mapcn.dev/docs/popups`
- `https://www.mapcn.dev/docs/routes`
- `https://www.mapcn.dev/docs/clusters`
- `https://www.mapcn.dev/docs/advanced-usage`
