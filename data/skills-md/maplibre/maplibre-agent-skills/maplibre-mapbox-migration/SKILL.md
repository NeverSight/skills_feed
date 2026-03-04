---
name: maplibre-mapbox-migration
description: Migrating from Mapbox GL JS to MapLibre GL JS — package and import changes, removing the access token, choosing tile sources, plugin equivalents, and what you gain or give up. Use when moving an existing Mapbox map to MapLibre.
---

# Mapbox to MapLibre Migration

This skill guides you through migrating an application from **Mapbox GL JS** to **MapLibre GL JS**. The two libraries share a common ancestry (MapLibre forked from Mapbox GL JS v1.13 in December 2020), so the API is largely the same. The main changes are: swap the package, replace the namespace, remove the Mapbox access token, and **choose a new tile source** (MapLibre does not use `mapbox://` styles).

**Primary reference:** [MapLibre official Mapbox migration guide](https://maplibre.org/maplibre-gl-js/docs/guides/mapbox-migration-guide/).

## When to Use This Skill

- Migrating an existing Mapbox GL JS app to MapLibre
- Evaluating MapLibre as an open-source alternative to Mapbox
- Understanding API compatibility and what breaks
- Choosing tile sources and services after moving off Mapbox

## Why Migrate to MapLibre?

Common reasons teams switch from Mapbox to MapLibre:

- **Open-source license** — MapLibre is BSD-3-Clause; no vendor lock-in or proprietary terms
- **No access token** — The library does not require a Mapbox token; tile sources may have their own keys or none (e.g. OpenFreeMap)
- **Cost** — Avoid Mapbox map-load and API pricing; use free or fixed-cost tile and geocoding providers
- **Self-hosting** — Use your own tiles (PMTiles, tileserver-gl, martin) or any third-party source
- **Community** — MapLibre is maintained by the MapLibre organization and community; style spec and APIs evolve in the open
- **Community-supported funding** — MapLibre is funded by donations from many companies and individuals; there is no single commercial backer, so the project stays aligned with the community
- **Open vector tile format (MLT)** — MapLibre offers [MapLibre Tile (MLT)](https://maplibre.org/maplibre-tile-spec/), a modern alternative to Mapbox Vector Tiles (MVT) with better compression and support for 3D coordinates and elevation; supported in GL JS and Native, and can be generated with Planetiler

**What you give up:** Mapbox Studio integration, Mapbox-hosted tiles and styles, Mapbox Search/Directions/Geocoding APIs, official Mapbox support.

## Understanding the Fork

- **Dec 2020:** Mapbox GL JS v2.0 switched to a proprietary license. The community forked v1.13 as **MapLibre GL JS**. [MapLibre organization](https://github.com/maplibre) and [GL JS repo](https://github.com/maplibre/maplibre-gl-js) are the canonical homes.
- **API:** MapLibre GL JS v1.x is largely backward compatible with Mapbox GL JS v1.x. Most map code (methods, events, layers, sources) works with minimal changes.
- **Releases since the fork:** MapLibre has moved ahead with its own version line. v2/v3 brought WebGL2, a modern renderer, and features like hillshade and terrain; v4 introduced Promises in public APIs (replacing many callbacks); v5 added globe view and the [Adaptive Composite Map Projection](https://maplibre.org/maplibre-gl-js/docs/API/). See [releases](https://github.com/maplibre/maplibre-gl-js/releases) and [CHANGELOG](https://github.com/maplibre/maplibre-gl-js/blob/main/CHANGELOG.md).
- **Style spec:** MapLibre maintains its own [MapLibre Style Specification](https://maplibre.org/maplibre-style-spec/) (forked from the Mapbox spec). It is compatible for most styles but has added and diverged in places; check the [style spec site](https://maplibre.org/maplibre-style-spec/) when using newer or MapLibre-specific features.
- **Ecosystem:** Besides GL JS, the MapLibre org hosts [MapLibre Native](https://maplibre.org/projects/native/) (iOS, Android, desktop), [Martin](https://maplibre.org/martin/) (vector tile server from PostGIS/PMTiles/MBTiles), and the [MapLibre Tile (MLT)](https://maplibre.org/maplibre-tile-spec/) format. Roadmaps and news: [maplibre.org/roadmap](https://maplibre.org/roadmap/), [maplibre.org/news](https://maplibre.org/news/).

## Step-by-Step Migration

### 1. Install the Package

```bash
npm install maplibre-gl
```

### 2. Update Imports and CSS

```javascript
// Before (Mapbox)
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';

// After (MapLibre)
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
```

**CDN:** Replace Mapbox script/link with MapLibre:

- Script: `https://api.mapbox.com/mapbox-gl-js/v*.*.*/mapbox-gl.js` → `https://unpkg.com/maplibre-gl@*.*.*/dist/maplibre-gl.js`
- CSS: same pattern (mapbox-gl.css → maplibre-gl.css).

### 3. Replace the Namespace

Replace all `mapboxgl` with `maplibregl` (and `mapbox-gl` with `maplibre-gl` in package names or paths). Examples:

```javascript
// Before (Mapbox)
const map = new mapboxgl.Map({ ... });
new mapboxgl.Marker().setLngLat([lng, lat]).addTo(map);
map.addControl(new mapboxgl.NavigationControl());

// After (MapLibre)
const map = new maplibregl.Map({ ... });
new maplibregl.Marker().setLngLat([lng, lat]).addTo(map);
map.addControl(new maplibregl.NavigationControl());
```

**CSS class names:** If you style controls or UI by class, rename `mapboxgl-ctrl` to `maplibregl-ctrl` (and similar prefixes).

### 4. Remove the Access Token

MapLibre does not use `mapboxgl.accessToken`. Remove any line that sets it.

Tile and API keys (e.g. for hosted tile services or geocoding) are configured per service, not on the map instance. See [maplibre-tile-sources](../maplibre-tile-sources/SKILL.md) for providers that need a key.

### 5. Replace the Style URL (Critical)

Mapbox styles (`mapbox://styles/...`) will not work in MapLibre. You must point the map to a style that uses non-Mapbox tile sources, sprites, and glyphs.

The simplest option is to use a style URL that does not require an API key, like [OpenFreeMap](https://openfreemap.org/). Once you have tested and verified your migration works, you can explore the many available options (see [awesome-maplibre](https://github.com/maplibre/awesome-maplibre) or [MapLibre Tile Sources](../maplibre-tile-sources/SKILL.md) for further suggestions).

Example:

```javascript
// Before (Mapbox)
const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/streets-v12',
  center: [-122.42, 37.78],
  zoom: 12
});

// After (MapLibre)
const map = new maplibregl.Map({
  container: 'map',
  style: 'https://tiles.openfreemap.org/styles/liberty', // or your chosen style
  center: [-122.42, 37.78],
  zoom: 12
});
```

From there, you can install the [MapLibre Style Specification & Utilities](https://maplibre.org/maplibre-style-spec/) to validate and debug styles:

```bash
npm install @maplibre/maplibre-style-spec
```

**Custom Mapbox styles:** If you designed a style in Mapbox Studio, you cannot load it directly in MapLibre. [Export the style JSON](https://docs.mapbox.com/help/dive-deeper/transfer-styles-between-accounts/) and replace Mapbox source URLs with URLs for your chosen tile source. **Your styles will not render unless and until you adjust all references to the Mapbox tile schema to match the tile schema of your new tile source.** In addition to updating source URLs, this means adapting the `id`, `source`, and `source-layer` properties in your style JSON to match the new source and layer names.

Most properties in Mapbox styles are compatible with MapLibre. Check the [MapLibre Style Specification](https://maplibre.org/maplibre-style-spec/) for details on supported properties and types. You can use [Maputnik](https://maputnik.github.io/), MapLibre's style editor, to visually test and debug your style JSON, and [MapLibre Style Spec CLI Tools](https://github.com/maplibre/maplibre-style-spec?tab=readme-ov-file#cli-tools) to check for compatibility and other validation issues.

```bash
gl-style-validate style.json
```

### 6. Update Plugins (If Used)

Many Mapbox plugins work with MapLibre unchanged, and many have been forked or replaced with MapLibre-native versions. Where a MapLibre-native alternative exists, prefer it for long-term compatibility.

Check the User Interface Plugins, Geocoding & Search Plugins, and Map Rendering Plugins sections of [awesome-maplibre](https://github.com/maplibre/awesome-maplibre) to find compatible plugins and alternatives.

### 7. Replace Mapbox APIs (Search, Directions, etc.)

If your app calls Mapbox Geocoding, Directions, or other REST APIs, replace them with open or third-party services:

- **Geocoding / search:** [Nominatim](https://nominatim.org/), [Photon](https://photon.komoot.io/), [Pelias](https://pelias.io/), or [MapTiler Geocoding](https://docs.maptiler.com/cloud/api/geocoding/)
- **Directions / routing:** [OSRM](https://project-osrm.org/), [OpenRouteService](https://openrouteservice.org/), [Valhalla](https://github.com/valhalla/valhalla)

Update your code to use the new endpoints and response formats; the map layer and interaction code (e.g. adding a route line) stays the same with MapLibre.

### 8. What Stays the Same

Most of your map code does not change:

- Map methods: `setCenter`, `setZoom`, `fitBounds`, `flyTo`, `getBounds`, etc.
- Events: `map.on('load')`, `map.on('click', layerId, callback)`, etc.
- Markers, popups, controls (Navigation, Geolocate, Fullscreen, Scale)
- Sources and layers: `addSource`, `addLayer`, `setPaintProperty`, `setFilter`
- GeoJSON and expressions in the style spec

So after swapping the package, namespace, token, and style (and any plugins/APIs), the rest of your logic can stay as is.

## Checklist

- [ ] Uninstall `mapbox-gl`, install `maplibre-gl`
- [ ] Replace imports and CSS (mapbox-gl → maplibre-gl)
- [ ] Replace all `mapboxgl` with `maplibregl` (and CSS classes `mapboxgl-` → `maplibregl-`)
- [ ] Remove `mapboxgl.accessToken`
- [ ] Set `style` to a non-Mapbox URL (hosted or your own style)
- [ ] Replace incompatible Mapbox plugins with MapLibre or open alternatives
- [ ] Replace Mapbox Geocoding/Directions with Nominatim, OSRM, or other open alternatives
- [ ] Test map load, controls, and any API-driven features

## Related Skills

- [**maplibre-tile-sources**](../maplibre-tile-sources/SKILL.md) — Choosing and configuring tile sources (OpenFreeMap, MapTiler, PMTiles, self-hosted)
- [**maplibre-pmtiles-patterns**](../maplibre-pmtiles-patterns/SKILL.md) — Serverless tiles with PMTiles

## Sources Used for This Skill

These sources were used when creating this skill. You may want to involve contributors who maintain or have contributed to them:

1. **MapLibre official migration guide** — [maplibre.org/maplibre-gl-js/docs/guides/mapbox-migration-guide/](https://maplibre.org/maplibre-gl-js/docs/guides/mapbox-migration-guide/) — Primary step-by-step reference (package, namespace, CSS, CDN).
2. **MapLibre GL JS documentation** — [maplibre.org/maplibre-gl-js/docs/](https://maplibre.org/maplibre-gl-js/docs/) — API and concepts.
3. **MapLibre GL JS GitHub** — [github.com/maplibre/maplibre-gl-js](https://github.com/maplibre/maplibre-gl-js) — README, releases, and fork history.
4. **mapbox-agent-skills** — The `mapbox-maplibre-migration` skill (Mapbox repo) covers the reverse direction (MapLibre → Mapbox). Topic structure and comparison elements were adapted for this Mapbox → MapLibre skill. Copyright (c) Mapbox, Inc. for adapted portions.
5. **This repo’s skills** — [maplibre-tile-sources](../maplibre-tile-sources/SKILL.md), [maplibre-pmtiles-patterns](../maplibre-pmtiles-patterns/SKILL.md); maplibre-open-search-patterns and maplibre-geospatial-operations not yet in repo — for tile source and service alternatives after migration.
