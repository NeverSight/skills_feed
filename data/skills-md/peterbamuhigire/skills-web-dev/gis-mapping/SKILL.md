---
name: gis-mapping
description: "Use for web apps that need Leaflet-first GIS mapping, location selection, map-driven UIs, or geofencing validation. Covers Leaflet setup, optional tile providers, data storage, and backend validation patterns."
---

# GIS Mapping (Leaflet-First)

## Quick Summary

- Leaflet-first mapping for web apps (default engine)
- Optional OpenStreetMap tiles or other providers
- Location selection (marker, polygon, rectangle) + map UI patterns
- Geofencing enforcement with client + server validation (see geofencing.md)
- Performance, clustering, and safe storage of spatial data

## Capability Index (Leaflet-First)

Use this index to load only the section you need. Details live in
[skills/gis-mapping/references/leaflet-capabilities.md](skills/gis-mapping/references/leaflet-capabilities.md).

1. **Basic Mapping & Visualization** (core Leaflet)
2. **Spatial Queries** (Turf.js)
3. **Geocoding** (Nominatim or Leaflet Control Geocoder)
4. **Buffering & Zone Analysis** (Turf.js)
5. **Heatmaps & Density** (leaflet.heat)
6. **Routing & Network Analysis** (OSRM / GraphHopper + leaflet-routing-machine)
7. **Drawing & Editing** (leaflet.draw / Geoman)
8. **Measurement Tools** (leaflet-measure or custom)
9. **Clustering & Aggregation** (leaflet.markercluster)
10. **Spatial Analysis** (Turf.js)
11. **Time-Based Analysis** (custom + heat)
12. **Export & Printing** (html2canvas/jsPDF + GeoJSON export)

## When to Use

- You need interactive maps for customers, assets, farms, or delivery zones
- Users must select or edit locations on a map
- You must enforce geo-fencing or boundary validation
- You need GIS data display with filters, legends, and clustering

## Key Patterns

- Leaflet is the default mapping engine.
- Always include attribution for the chosen tile provider.
- Capture geometry in GeoJSON and validate server-side.
- Use bounding-box checks before deeper polygon math.
- Cluster markers when data is large or dense.
- Store optional tile provider API keys in system settings (e.g., `osm_api_key`) and load them at runtime.
- Default to terrain tiles (OpenTopoMap) for administrative borders.

## Leaflet Standardization (BIRDC)

- Use a shared Leaflet configuration for tile URLs, attribution, and defaults.
- Prefer a shared loader or include pattern so Leaflet CSS/JS is consistent across pages.
- Use [public/farmer-profile.php](public/farmer-profile.php) as the canonical Leaflet UI reference.

## Stack Choices (Frontend)

- **Leaflet (default)**: Lightweight, fastest to implement, best for most apps.
- **OpenLayers (optional)**: Heavyweight GIS controls and projections.
- **MapLibre GL JS (optional)**: Vector tiles, smoother at scale.

## Data Model & Storage

- **Point**: `latitude` + `longitude` (DECIMAL(10,7))
- **Polygon/Boundary**: Store as GeoJSON (TEXT/JSON)
- **Metadata**: `location_label`, `address`, `last_updated_at`

Recommended formats:

- GeoJSON for portability across JS + backend
- WKT only if your DB tooling depends on it

## Map Initialization (Leaflet)

```html
<link
  rel="stylesheet"
  href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
```

```javascript
const map = L.map("map").setView([0.3476, 32.5825], 12);
const osmApiKey = window.osmApiKey || "";
const osmTileUrl = osmApiKey
  ? `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png?api_key=${osmApiKey}`
  : "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";

const osm = L.tileLayer(osmTileUrl, {
  attribution: "© OpenStreetMap contributors",
  maxZoom: 19,
});

const terrain = L.tileLayer(
  "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
  {
    attribution: "© OpenTopoMap",
    maxZoom: 17,
  },
);

terrain.addTo(map);
```

## Location Selection Patterns

### Marker (Point)

- Single click adds/updates a marker
- Store coordinates in hidden inputs

```javascript
let marker;
map.on("click", (e) => {
  if (marker) map.removeLayer(marker);
  marker = L.marker(e.latlng).addTo(map);
  document.querySelector("#latitude").value = e.latlng.lat;
  document.querySelector("#longitude").value = e.latlng.lng;
});
```

### Polygon / Rectangle (Area)

Use Leaflet Draw or Geoman. Store GeoJSON geometry.

```javascript
const drawn = new L.FeatureGroup().addTo(map);
const drawControl = new L.Control.Draw({
  draw: { polygon: true, rectangle: true, marker: false, circle: false },
  edit: { featureGroup: drawn },
});
map.addControl(drawControl);

map.on("draw:created", (e) => {
  drawn.clearLayers();
  drawn.addLayer(e.layer);
  document.querySelector("#boundary_geojson").value = JSON.stringify(
    e.layer.toGeoJSON(),
  );
});
```

## Geofencing (Overview)

Geofencing must be enforced at two levels:

- **UI constraint**: prevent invalid selections in the browser
- **Server constraint**: verify boundaries in backend validation

See geofencing.md for full patterns, point-in-polygon checks, and multi-geometry rules.

## UI Patterns

- Filters + stats in a side card, map in a large canvas
- Legend to toggle categories (customer groups, territories)
- Clustering when markers exceed ~200

## Performance & UX

- Debounce search and map redraw
- Use marker clustering or server-side tiling
- Lazy load heavy layers
- Simplify large polygons for UI display

## Backend Validation

Always validate coordinates server-side:

- Ensure latitude is between -90 and 90
- Ensure longitude is between -180 and 180
- Enforce geofence boundaries with the same logic as UI
- Load optional tile provider keys (for example `osm_api_key`) from system settings when building map pages

## Privacy & Security

- Location data is sensitive: protect with permissions
- Never trust client-only validation
- Avoid exposing private coordinates without authorization

## Recommended Plugins

- Leaflet Draw or Leaflet Geoman (drawing tools)
- Leaflet MarkerCluster (performance)
- Leaflet Control Geocoder (search)
- Turf.js (geospatial analysis)

## References

- geofencing.md (sub-skill)
- references/leaflet-capabilities.md
- references/leaflet-arcgis-equivalents.md (index)
