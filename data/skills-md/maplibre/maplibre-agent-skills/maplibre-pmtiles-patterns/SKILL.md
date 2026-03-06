---
name: maplibre-pmtiles-patterns
description: Serverless vector and raster tiles with PMTiles for MapLibre GL JS — single-file format, HTTP range requests, hosting on S3/R2/GitHub Pages, generating with Planetiler or tippecanoe, and the pmtiles protocol. Use when you need no tile server or want to host tiles from static storage.
---

# MapLibre PMTiles Patterns

PMTiles is a single-file format for vector or raster map tiles. You host one (or a few) files on any static host; MapLibre requests byte ranges over HTTP. No tile server, no dynamic backend. This skill covers when to use PMTiles, how to generate and host them, and how to connect them to MapLibre GL JS.

## When to Use This Skill

- Hosting map tiles without running a tile server (S3, Cloudflare R2, GitHub Pages, etc.)
- Building a fully static or serverless map stack
- Serving large tile sets from a CDN with range requests
- Generating PMTiles from OSM or other sources (Planetiler, tippecanoe)
- Using Overture Maps or other single-file tile datasets with MapLibre

## What PMTiles Is and Why It Matters

- **Vector and raster** — PMTiles supports both. A file can contain vector layers (e.g. water, roads, POIs), raster imagery (PNG/JPEG), or raster-dem (elevation, e.g. Terrarium format for terrain). In the style you use `type: 'vector'`, `type: 'raster'`, or `type: 'raster-dem'` accordingly.
- **Single file per map** — One `.pmtiles` file typically contains the full tile pyramid (all zoom levels) and all layers (vector or raster) in one archive. The format stores tiles in a compact layout (e.g. Hilbert curve) so the client can request only the byte ranges it needs. For very large coverage you may split by region into multiple files.
- **HTTP range requests** — The client requests only the byte ranges it needs (e.g. one tile), so the server does not need to understand x/y/z. Any host that supports `Range` headers works.
- **Serving** — You can serve directly from static storage (S3, R2, GitHub Pages, Netlify): the client uses range requests, so no tile server is required. Alternatively, [tileserver-gl](https://github.com/maptiler/tileserver-gl) or [Martin](https://maplibre.org/martin/) can serve PMTiles (from local paths, HTTP URLs, or S3), useful if you want one server that also provides styles, glyphs, or other sources.
- **Creating** — You can get PMTiles by converting from MBTiles (PMTiles CLI) or by generating from source data (Planetiler, tippecanoe, GDAL, etc.). Alternatively, [**Protomaps**](https://protomaps.com) is a provider where you can download pre-built PMTiles (e.g. global or regional basemaps) and serve them yourself, or create custom extracts via the PMTiles CLI—no need to generate from OSM yourself. See _The PMTiles CLI_ and _Generating PMTiles_ below.
- **Good for CDNs** — Range requests cache well; put the file behind a CDN for fast global access.

**When to prefer PMTiles over a traditional tile server:**

- You want zero server logic (static hosting only).
- You have a bounded dataset (country, region, theme) that fits in one or a few files.
- You want simple deployment and low ops (upload file, set cache headers, done).

**When to prefer a tile server (e.g. tileserver-gl, martin):**

- You need dynamic tiles from a database (PostGIS) or frequently updated data.
- You have a very large global dataset and want to generate tiles on demand or by region only.

## MapLibre Integration: The PMTiles Protocol

MapLibre does not speak PMTiles natively. You use the **PMTiles** library to add a protocol handler so that a `pmtiles://` (or `https://` to a .pmtiles file) source works.

**Install:**

```bash
npm install pmtiles
```

**Register the protocol and use in a style:**

```javascript
import * as pmtiles from 'pmtiles';
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

// Add PMTiles protocol so sources can reference .pmtiles URLs
const protocol = new pmtiles.Protocol();
maplibregl.addProtocol('pmtiles', protocol.tile);

const map = new maplibregl.Map({
  container: 'map',
  style: {
    version: 8,
    sources: {
      tiles: {
        type: 'vector',
        url: 'pmtiles://https://example.com/data.pmtiles'
      }
    },
    layers: [
      {
        id: 'background',
        type: 'background',
        paint: { 'background-color': '#f8f4f0' }
      },
      {
        id: 'water',
        type: 'fill',
        source: 'tiles',
        'source-layer': 'water',
        paint: { 'fill-color': '#a0c8f0' }
      }
      // add more layers as needed — each uses the same source, different 'source-layer'
    ]
  },
  center: [0, 0],
  zoom: 2
});

// Optional: remove protocol on map teardown
// map.on('remove', () => maplibregl.removeProtocol('pmtiles'));
```

**Referencing layers:** The style has one source (e.g. `sources.tiles`) pointing at the .pmtiles URL. Each layer in the `layers` array that draws from that file uses `source: 'tiles'` and `"source-layer": "layerName"`, where `layerName` is the name of a vector layer inside the file (from whatever schema the tiles use). Add multiple style layers with different `source-layer` values to show roads, labels, etc. from the same file.

**Important:** The `url` can be `pmtiles://https://...` (protocol + HTTPS URL to the .pmtiles file). The library will fetch the file via range requests. Your style must still define glyphs and sprite if you use labels or icons (see [maplibre-tile-sources](../maplibre-tile-sources/SKILL.md)).

**Raster and raster-dem:** The same protocol works for raster PMTiles. Use a `type: 'raster'` source for imagery. For terrain/elevation, use a `type: 'raster-dem'` source with `"encoding": "terrarium"` (or `"mapbox"`) so MapLibre can apply hillshade or 3D terrain; then reference it in the style’s `terrain` property. Example source:

```json
"elevation": {
  "type": "raster-dem",
  "url": "pmtiles://https://example.com/elevation.pmtiles",
  "encoding": "terrarium"
}
```

**Using PMTiles with React:** Register the protocol once at application startup, not inside each component, so MapLibre has the handler before any map mounts. For example, call `maplibregl.addProtocol('pmtiles', protocol.tile)` in a root-level effect or when your map provider initializes. On unmount of the last map (or when the app tears down), call `maplibregl.removeProtocol('pmtiles')` to avoid leaks. See [PMTiles for MapLibre GL](https://docs.protomaps.com/pmtiles/maplibre) (Protomaps) for a React-oriented setup.

## Hosting PMTiles

Any host that serves the file and supports **HTTP Range requests** is suitable.

- **AWS S3** — Enable public read (or signed URLs); S3 supports Range. Set `Cache-Control` and optionally use CloudFront.
- **Cloudflare R2** — S3-compatible; enable public access or use signed URLs. Put behind Cloudflare for caching.
- **GitHub Pages** — MapLibre GL JS can load tiles from a .pmtiles file in the same repo as long as the file size is under 100 MB.
- **Netlify / Vercel** — Upload the .pmtiles file; static hosting typically supports Range. Check each provider’s file size limits.
- **Any static host** — Ensure the server returns `Accept-Ranges: bytes` and responds correctly to `Range` headers.

**CORS:** Browsers will send cross-origin requests to the PMTiles URL. The host must send `Access-Control-Allow-Origin: *` (or your domain) and `Access-Control-Allow-Headers: Range` (or allow all). Otherwise MapLibre will fail to load tiles.

**Cache headers:** For better performance, set long cache for the .pmtiles file (e.g. `Cache-Control: public, max-age=31536000` if the file is immutable). CDNs will cache range responses.

## The PMTiles CLI

The [pmtiles CLI](https://docs.protomaps.com/pmtiles/cli) is the official command-line tool for working with PMTiles (and MBTiles for conversion). It’s a single binary with no runtime dependencies—you download it and run it.

**Why install and use it:**

- **Convert MBTiles to PMTiles** — Many tools (tippecanoe, GDAL, martin-cp) output MBTiles. One command turns any .mbtiles file into a .pmtiles file: `pmtiles convert in.mbtiles out.pmtiles`. This is often the simplest way to get PMTiles when your pipeline already produces MBTiles.
- **Inspect and verify archives** — `pmtiles show <file>` prints header and metadata (bounds, zoom range, tile count). `pmtiles verify <file>` checks archive integrity. Useful for debugging or confirming a file before uploading.
- **Extract subsets** — `pmtiles extract` creates a smaller .pmtiles file from an existing one (e.g. by bounding box or zoom range), so you can ship a region or a limited zoom band without regenerating from source.

**Install:** Download the binary for your OS/arch from [GitHub Releases (go-pmtiles)](https://github.com/protomaps/go-pmtiles/releases), or use Docker: `protomaps/go-pmtiles`.

**What it does not do:** The CLI only works with tile archives (MBTiles and PMTiles). It does not read GeoJSON, Shapefile, OSM, or other source formats. To create PMTiles from those, use a tool that generates tiles (see _Generating PMTiles_ below) and, if that tool outputs MBTiles, run `pmtiles convert` to get PMTiles.

## Generating PMTiles

**Two paths:** **(1) Convert** — The PMTiles CLI converts MBTiles ↔ PMTiles only; it does not read GeoJSON, Shapefile, OSM, or other source formats. **(2) Generate from source data** — Tools like tippecanoe, Planetiler, and GDAL read from many file types or databases and produce vector tiles (PMTiles or MBTiles). If they output MBTiles, use `pmtiles convert` to get PMTiles.

### PMTiles CLI (convert only: MBTiles ↔ PMTiles)

See _The PMTiles CLI_ above for why to install it and other commands (`show`, `verify`, `extract`). To convert MBTiles to PMTiles:

```bash
pmtiles convert input.mbtiles output.pmtiles
```

The following tools **generate tiles from source data** (GeoJSON, OSM, Shapefile, PostGIS, etc.). They output PMTiles or MBTiles; if MBTiles, run `pmtiles convert` to get PMTiles.

### Planetiler (OSM / OpenMapTiles schema)

[Planetiler](https://github.com/onthegomap/planetiler) reads OpenStreetMap (or other sources) and outputs PMTiles or MBTiles in the OpenMapTiles schema.

```bash
# Example: build a PMTiles file for a region (e.g. from a .osm.pbf download)
java -jar planetiler.jar --area=monaco --output=monaco.pmtiles
```

See Planetiler docs for area names, custom sources, and schema options. Output is a single .pmtiles file you can upload to S3/R2/static host.

### tippecanoe

[tippecanoe](https://github.com/felt/tippecanoe) **generates** vector tiles from source formats: GeoJSON, FlatGeobuf, CSV. From v2.17 onward it can **output PMTiles directly** (`-o output.pmtiles`). You can also output MBTiles and convert with `pmtiles convert`.

```bash
# Direct PMTiles output (v2.17+)
tippecanoe -zg -o output.pmtiles input.geojson
# Or MBTiles then convert: tippecanoe -o output.mbtiles -z 14 input.geojson && pmtiles convert output.mbtiles output.pmtiles
```

### ogr2ogr (GDAL)

GDAL’s `ogr2ogr` **generates** tiles from many geospatial formats (Shapefile, PostGIS, GeoJSON, etc.) and can write MBTiles or PMTiles (GDAL 3.8+). Best for smaller datasets; tippecanoe is more efficient for large vector tile sets.

### Raster and raster-dem PMTiles

PMTiles supports **raster** tiles (PNG/JPEG, e.g. satellite or pre-rendered imagery) and **raster-dem** (elevation/terrain, e.g. Terrarium or Mapbox encoding). Use tools that produce raster or raster-dem PMTiles; the same protocol and hosting apply. In the style use `type: 'raster'` for imagery or `type: 'raster-dem'` with `"encoding": "terrarium"` (or `"mapbox"`) for terrain—see _MapLibre Integration_ above for an example.

## Overture Maps

[Overture Maps](https://overturemaps.org/) publishes global open map data. Some providers distribute Overture-derived data as PMTiles (e.g. for buildings, places, transportation). You can also build PMTiles from Overture data with Planetiler or other pipelines. Use the PMTiles URL in your MapLibre style as above.

## Performance Tips

- **CDN** — Serve the .pmtiles file from a CDN (CloudFront, Cloudflare) so range requests are fast globally.
- **Compression** — PMTiles stores tiles compressed; the library handles decompression. Ensure the server does not double-compress (e.g. gzip) the whole file in a way that breaks range requests.
- **Multiple files** — For very large coverage, split by region into several .pmtiles files and switch the source URL or use multiple sources by bounds.
- **Caching** — Set strong cache headers on the file; the browser and CDN will cache range responses.

## Related Skills

- [**maplibre-tile-sources**](../maplibre-tile-sources/SKILL.md) — Choosing tile sources (OpenFreeMap, MapTiler, PMTiles, self-hosted); glyphs and sprites.
- **maplibre-style-patterns** — Layer and paint configuration for vector sources (including PMTiles-backed sources). (Not yet in repo.)

## References

- [MapLibre GL JS: PMTiles source and protocol](https://maplibre.org/maplibre-gl-js/docs/examples/pmtiles/) — Official example: adding the protocol, vector and raster sources.
- [PMTiles for MapLibre GL](https://docs.protomaps.com/pmtiles/maplibre) (Protomaps) — Setup, vector/raster/raster-dem (Terrarium) sources, React usage.
- [PMTiles](https://github.com/protomaps/PMTiles) — Format and protocol
- [pmtiles CLI](https://docs.protomaps.com/pmtiles/cli) — Simplest way to create PMTiles (`convert`, `show`, `verify`, `extract`)
- [Planetiler](https://github.com/onthegomap/planetiler) — OSM → PMTiles/MBTiles
- [MapLibre GL JS](https://maplibre.org/maplibre-gl-js/docs/) — Style spec and API
