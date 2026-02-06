---
name: mapbox-maplibre-migration
description: Guide for migrating from MapLibre GL JS to Mapbox GL JS, covering API compatibility, token setup, style configuration, and the benefits of Mapbox's official support and ecosystem
---

# MapLibre to Mapbox Migration Skill

Expert guidance for migrating from MapLibre GL JS to Mapbox GL JS. Covers the shared history, API compatibility, migration steps, and the advantages of Mapbox's platform.

## Understanding the Fork

### History

**MapLibre GL JS** is an open-source fork of **Mapbox GL JS v1.13.0**, created in December 2020 when Mapbox changed their license starting with v2.0.

**Timeline:**
- **Pre-2020:** Mapbox GL JS was open source (BSD license)
- **Dec 2020:** Mapbox GL JS v2.0 introduced proprietary license
- **Dec 2020:** Community forked v1.13 as MapLibre GL JS
- **Present:** Both libraries continue active development

**Key Insight:** The APIs are ~95% identical because MapLibre started as a Mapbox fork. Most code works in both with minimal changes, making migration straightforward.

## Why Migrate to Mapbox?

**Compelling reasons to choose Mapbox GL JS:**

- **Official Support & SLAs**: Enterprise-grade support with guaranteed response times
- **Superior Tile Quality**: Best-in-class vector tiles with global coverage and frequent updates
- **Better Satellite Imagery**: High-resolution, up-to-date satellite and aerial imagery
- **Rich Ecosystem**: Seamless integration with Mapbox Studio, APIs, and services
- **Advanced Features**: Traffic-aware routing, turn-by-turn directions, premium datasets
- **Geocoding & Search**: World-class address search and place lookup
- **Navigation SDK**: Mobile navigation with real-time traffic
- **No Tile Infrastructure**: No need to host or maintain your own tile servers
- **Regular Updates**: Continuous improvements and new features
- **Professional Services**: Access to Mapbox solutions team for complex projects

**Mapbox offers a generous free tier:** 50,000 map loads/month, making it suitable for many applications without cost.

## Quick Comparison

| Aspect | Mapbox GL JS | MapLibre GL JS |
|--------|--------------|----------------|
| **License** | Proprietary (v2+) | BSD 3-Clause (Open Source) |
| **Support** | Official commercial support | Community support |
| **Tiles** | Premium Mapbox vector tiles | OSM or custom tile sources |
| **Satellite** | High-quality global imagery | Requires custom source |
| **Token** | Required (access token) | Optional (depends on tile source) |
| **APIs** | Full Mapbox ecosystem | Requires third-party services |
| **Studio** | Full integration | No native integration |
| **3D Terrain** | Built-in with premium data | Available (requires data source) |
| **Globe View** | v2.9+ | v3.0+ |
| **API Compatibility** | ~95% compatible with MapLibre | ~95% compatible with Mapbox |
| **Bundle Size** | ~500KB | ~450KB |
| **Setup Complexity** | Easy (just add token) | Requires tile source setup |

## Step-by-Step Migration

### 1. Create Mapbox Account

1. Sign up at [mapbox.com](https://mapbox.com)
2. Get your access token from the account dashboard
3. Review pricing: Free tier includes 50,000 map loads/month
4. Note your token (starts with `pk.` for public tokens)

### 2. Update Package

```bash
# Remove MapLibre
npm uninstall maplibre-gl

# Install Mapbox
npm install mapbox-gl
```

### 3. Update Imports

```javascript
// Before (MapLibre)
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

// After (Mapbox)
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
```

Or with CDN:

```html
<!-- Before (MapLibre) -->
<script src='https://unpkg.com/maplibre-gl@3.0.0/dist/maplibre-gl.js'></script>
<link href='https://unpkg.com/maplibre-gl@3.0.0/dist/maplibre-gl.css' rel='stylesheet' />

<!-- After (Mapbox) -->
<script src='https://api.mapbox.com/mapbox-gl-js/v3.0.0/mapbox-gl.js'></script>
<link href='https://api.mapbox.com/mapbox-gl-js/v3.0.0/mapbox-gl.css' rel='stylesheet' />
```

### 4. Add Access Token

```javascript
// Add this before map initialization
mapboxgl.accessToken = 'pk.your_mapbox_access_token';
```

**Token best practices:**
- Use environment variables: `process.env.VITE_MAPBOX_TOKEN` or `process.env.NEXT_PUBLIC_MAPBOX_TOKEN`
- Add URL restrictions in Mapbox dashboard for security
- Use public tokens (`pk.*`) for client-side code
- Never commit tokens to git (add to `.env` and `.gitignore`)
- Rotate tokens if compromised

See `mapbox-token-security` skill for comprehensive token security guidance.

### 5. Update Map Initialization

```javascript
// Before (MapLibre)
const map = new maplibregl.Map({
  container: 'map',
  style: 'https://demotiles.maplibre.org/style.json', // or your custom style
  center: [-122.4194, 37.7749],
  zoom: 12
});

// After (Mapbox)
mapboxgl.accessToken = 'pk.your_mapbox_access_token';

const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/standard', // Mapbox style
  center: [-122.4194, 37.7749],
  zoom: 12
});
```

### 6. Update Style URL

Mapbox provides professionally designed, maintained styles:

```javascript
// Mapbox built-in styles
style: 'mapbox://styles/mapbox/standard'        // Mapbox Standard (default)
style: 'mapbox://styles/mapbox/standard-satellite'.   //  Mapbox Standard Satellite 
style: 'mapbox://styles/mapbox/streets-v12'               // Streets v12
style: 'mapbox://styles/mapbox/satellite-v9'       // Satellite imagery
style: 'mapbox://styles/mapbox/satellite-streets-v12'  // Hybrid
style: 'mapbox://styles/mapbox/outdoors-v12'       // Outdoor/recreation
style: 'mapbox://styles/mapbox/light-v11'          // Light theme
style: 'mapbox://styles/mapbox/dark-v11'           // Dark theme
style: 'mapbox://styles/mapbox/navigation-day-v1'  // Navigation (day)
style: 'mapbox://styles/mapbox/navigation-night-v1' // Navigation (night)
```

**Custom styles:**
You can also create and use custom styles from Mapbox Studio:
```javascript
style: 'mapbox://styles/your-username/your-style-id'
```

### 7. Update All References

Replace all `maplibregl` references with `mapboxgl`:

```javascript
// Markers
const marker = new mapboxgl.Marker()  // was: maplibregl.Marker()
  .setLngLat([-122.4194, 37.7749])
  .setPopup(new mapboxgl.Popup().setText('San Francisco'))
  .addTo(map);

// Controls
map.addControl(new mapboxgl.NavigationControl(), 'top-right');
map.addControl(new mapboxgl.GeolocateControl());
map.addControl(new mapboxgl.FullscreenControl());
map.addControl(new mapboxgl.ScaleControl());
```

### 8. Update Plugins (If Used)

Some MapLibre plugins should be replaced with Mapbox versions:

| MapLibre Plugin | Mapbox Alternative |
|-----------------|-------------------|
| `@maplibre/maplibre-gl-geocoder` | `@mapbox/mapbox-gl-geocoder` |
| `@maplibre/maplibre-gl-draw` | `@mapbox/mapbox-gl-draw` |
| `maplibre-gl-compare` | `mapbox-gl-compare` |

Example:
```javascript
// Before (MapLibre)
import MaplibreGeocoder from '@maplibre/maplibre-gl-geocoder';

// After (Mapbox)
import MapboxGeocoder from '@mapbox/mapbox-gl-geocoder';

map.addControl(new MapboxGeocoder({
  accessToken: mapboxgl.accessToken,
  mapboxgl: mapboxgl
}));
```

### 9. Everything Else Stays the Same

All your map code, events, layers, and sources work identically:

```javascript
// This code works EXACTLY THE SAME in both libraries
map.on('load', () => {
  map.addSource('points', {
    type: 'geojson',
    data: geojsonData
  });

  map.addLayer({
    id: 'points-layer',
    type: 'circle',
    source: 'points',
    paint: {
      'circle-radius': 8,
      'circle-color': '#ff0000'
    }
  });
});

// Events work identically
map.on('click', 'points-layer', (e) => {
  console.log(e.features[0].properties);
});

// All map methods work the same
map.setCenter([lng, lat]);
map.setZoom(12);
map.fitBounds(bounds);
map.flyTo({center: [lng, lat], zoom: 14});
```

## What Changes: Summary

**Must change:**
- Package name (`maplibre-gl` → `mapbox-gl`)
- Import statements
- Add `mapboxgl.accessToken` configuration
- Style URL (switch to `mapbox://` styles)
- Plugin packages (if used)

**Stays exactly the same:**
- All map methods (`setCenter`, `setZoom`, `fitBounds`, `flyTo`, etc.)
- All event handling (`map.on('click')`, `map.on('load')`, etc.)
- Marker/Popup APIs (100% compatible)
- Layer/source APIs (100% compatible)
- GeoJSON handling
- Custom styling and expressions
- Controls (Navigation, Geolocate, Scale, etc.)

## API Compatibility Matrix

### 100% Compatible APIs

These work identically in both libraries:

```javascript
// Map methods
map.setCenter([lng, lat])
map.setZoom(zoom)
map.fitBounds(bounds)
map.panTo([lng, lat])
map.flyTo({center, zoom})
map.getCenter()
map.getZoom()
map.getBounds()
map.resize()

// Events
map.on('load', callback)
map.on('click', callback)
map.on('move', callback)
map.on('zoom', callback)
map.on('rotate', callback)

// Markers
new mapboxgl.Marker()
marker.setLngLat([lng, lat])
marker.setPopup(popup)
marker.addTo(map)
marker.remove()
marker.setDraggable(true)

// Popups
new mapboxgl.Popup()
popup.setLngLat([lng, lat])
popup.setHTML(html)
popup.setText(text)
popup.addTo(map)

// Sources & Layers
map.addSource(id, source)
map.removeSource(id)
map.addLayer(layer)
map.removeLayer(id)
map.getSource(id)
map.getLayer(id)

// Styling
map.setPaintProperty(layerId, property, value)
map.setLayoutProperty(layerId, property, value)
map.setFilter(layerId, filter)

// Controls
map.addControl(control, position)
new mapboxgl.NavigationControl()
new mapboxgl.GeolocateControl()
new mapboxgl.FullscreenControl()
new mapboxgl.ScaleControl()
```

## Side-by-Side Example

### MapLibre GL JS (Before)

```javascript
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

// No token needed for OSM tiles

const map = new maplibregl.Map({
  container: 'map',
  style: 'https://demotiles.maplibre.org/style.json',
  center: [-122.4194, 37.7749],
  zoom: 12
});

map.on('load', () => {
  new maplibregl.Marker()
    .setLngLat([-122.4194, 37.7749])
    .setPopup(new maplibregl.Popup().setText('San Francisco'))
    .addTo(map);
});
```

### Mapbox GL JS (After)

```javascript
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';

// Add your Mapbox token
mapboxgl.accessToken = 'pk.your_mapbox_access_token';

const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/streets-v12',
  center: [-122.4194, 37.7749],
  zoom: 12
});

map.on('load', () => {
  new mapboxgl.Marker()
    .setLngLat([-122.4194, 37.7749])
    .setPopup(new mapboxgl.Popup().setText('San Francisco'))
    .addTo(map);
});
```

**What's different:** Package, import, token, and style URL. **Everything else is identical.**

## Mapbox-Exclusive Features

After migration, you gain access to these Mapbox-only features:

### Premium Vector Tiles
- **Streets**: Comprehensive road network with names, shields, and routing data
- **Satellite**: High-resolution global imagery updated regularly
- **Terrain**: Elevation data with hillshading and 3D terrain
- **Traffic**: Real-time traffic data (with Navigation SDK)

### Mapbox APIs
Use these APIs alongside your map for enhanced functionality:

```javascript
// Geocoding API - Convert addresses to coordinates
const response = await fetch(
  `https://api.mapbox.com/search/geocode/v6/forward?q=San+Francisco&access_token=${mapboxgl.accessToken}`
);

// Directions API - Get turn-by-turn directions
const directions = await fetch(
  `https://api.mapbox.com/directions/v5/mapbox/driving/-122.42,37.78;-122.45,37.76?access_token=${mapboxgl.accessToken}`
);

// Isochrone API - Calculate travel time polygons
const isochrone = await fetch(
  `https://api.mapbox.com/isochrone/v1/mapbox/driving/-122.42,37.78?contours_minutes=5,10,15&access_token=${mapboxgl.accessToken}`
);
```

### Mapbox Studio
- Visual style editor with live preview
- Dataset management and editing
- Tilesets with custom data upload
- Collaborative team features
- Style versioning and publishing

### Advanced Features (v2.9+)
- **Globe projection**: Seamless transition from globe to Mercator
- **3D buildings**: Extrusion with real building footprints
- **Custom terrain**: Use your own DEM sources
- **Sky layer**: Realistic atmospheric rendering

## Framework Integration

Migration works identically across all frameworks. See `mapbox-web-integration-patterns` skill for detailed React, Vue, Svelte, Angular patterns.

### React Example

```jsx
import { useRef, useEffect } from 'react';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';

// Set token once (can be in app initialization)
mapboxgl.accessToken = process.env.REACT_APP_MAPBOX_TOKEN;

function MapComponent() {
  const mapRef = useRef(null);
  const mapContainerRef = useRef(null);

  useEffect(() => {
    mapRef.current = new mapboxgl.Map({
      container: mapContainerRef.current,
      style: 'mapbox://styles/mapbox/streets-v12',
      center: [-122.4194, 37.7749],
      zoom: 12
    });

    return () => {
      mapRef.current.remove();
    };
  }, []);

  return <div ref={mapContainerRef} style={{ height: '100vh' }} />;
}
```

Just replace `maplibregl` with `mapboxgl` and update token/style - everything else is identical!

### Vue Example

```vue
<template>
  <div ref="mapContainer" class="map-container"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';

mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN;

const mapContainer = ref(null);
let map = null;

onMounted(() => {
  map = new mapboxgl.Map({
    container: mapContainer.value,
    style: 'mapbox://styles/mapbox/streets-v12',
    center: [-122.4194, 37.7749],
    zoom: 12
  });
});

onUnmounted(() => {
  map?.remove();
});
</script>

<style scoped>
.map-container {
  height: 100vh;
}
</style>
```

## Common Migration Issues

### Issue 1: Token Not Set

**Problem:**
```javascript
// Error: "A valid Mapbox access token is required to use Mapbox GL"
const map = new mapboxgl.Map({...});
```

**Solution:**
```javascript
// Set token BEFORE creating map
mapboxgl.accessToken = 'pk.your_token';
const map = new mapboxgl.Map({...});
```

### Issue 2: Token in Git

**Problem:**
```javascript
// Token hardcoded in source
mapboxgl.accessToken = 'pk.eyJ1Ijoi...';
```

**Solution:**
```javascript
// Use environment variables
mapboxgl.accessToken = process.env.VITE_MAPBOX_TOKEN;

// Add to .env file (not committed to git)
VITE_MAPBOX_TOKEN=pk.your_token

// Add .env to .gitignore
echo ".env" >> .gitignore
```

### Issue 3: Wrong Style URL Format

**Problem:**
```javascript
// MapLibre-style URL won't work optimally
style: 'https://demotiles.maplibre.org/style.json'
```

**Solution:**
```javascript
// Use Mapbox style URL for better performance and features
style: 'mapbox://styles/mapbox/streets-v12'
```

### Issue 4: Plugin Compatibility

**Problem:**
```javascript
// MapLibre plugin won't work
import MaplibreGeocoder from '@maplibre/maplibre-gl-geocoder';
```

**Solution:**
```javascript
// Use Mapbox plugin
import MapboxGeocoder from '@mapbox/mapbox-gl-geocoder';
```

### Issue 5: CDN URLs

**Problem:**
```javascript
// Wrong CDN
<script src='https://unpkg.com/maplibre-gl@3.0.0/dist/maplibre-gl.js'></script>
```

**Solution:**
```javascript
// Use Mapbox CDN
<script src='https://api.mapbox.com/mapbox-gl-js/v3.0.0/mapbox-gl.js'></script>
<link href='https://api.mapbox.com/mapbox-gl-js/v3.0.0/mapbox-gl.css' rel='stylesheet' />
```

## Migration Checklist

Complete these steps for a successful migration:

- [ ] **Create Mapbox account** and get access token
- [ ] **Update package**: `npm install mapbox-gl` (remove maplibre-gl)
- [ ] **Update imports**: `maplibre-gl` → `mapbox-gl`
- [ ] **Update CSS imports**: `maplibre-gl.css` → `mapbox-gl.css`
- [ ] **Add token**: Set `mapboxgl.accessToken = 'pk.xxx'`
- [ ] **Use environment variables**: Store token in `.env`
- [ ] **Update style URL**: Change to `mapbox://styles/mapbox/streets-v12`
- [ ] **Update all references**: Replace `maplibregl.` with `mapboxgl.`
- [ ] **Update plugins**: Install Mapbox versions of plugins (if used)
- [ ] **Configure token security**: Add URL restrictions in dashboard
- [ ] **Test all functionality**: Verify map loads, interactions work
- [ ] **Set up billing alerts**: Monitor usage in Mapbox dashboard
- [ ] **Update documentation**: Document token setup for team
- [ ] **Add .env to .gitignore**: Ensure tokens not committed

## Why Choose Mapbox

### For Production Applications

**Reliability & Support:**
- 99.9% uptime SLA for enterprise customers
- 24/7 support with guaranteed response times
- Dedicated solutions engineers for complex projects
- Regular platform updates and improvements

**Performance:**
- Global CDN for fast tile delivery
- Optimized vector tiles for minimal bandwidth
- Automatic scaling for traffic spikes
- WebGL-accelerated rendering

**Features:**
- Professional cartography and design
- Regular map data updates
- Traffic and routing data
- Premium satellite imagery
- 3D terrain and buildings

### For Development Teams

**Developer Experience:**
- Comprehensive documentation with examples
- Active community and forums
- Regular SDK updates
- TypeScript support (via `@types/mapbox-gl`)
- Extensive example gallery

**Ecosystem Integration:**
- Seamless Studio integration
- API consistency across services
- Mobile SDKs (iOS, Android, React Native)
- Unity and Unreal Engine plugins
- Analytics and monitoring tools

### For Business

**Predictable Costs:**
- Clear, usage-based pricing
- Free tier for development and small apps
- No infrastructure costs
- Scalable pricing for growth

**Compliance & Security:**
- SOC 2 Type II certified
- GDPR compliant
- Enterprise security features
- Audit logs and monitoring

**No Infrastructure Burden:**
- No tile servers to maintain
- No storage or bandwidth concerns
- No update management
- Focus on your application, not infrastructure

## Performance Comparison

Both libraries have similar rendering performance as they share the same core codebase:

| Metric | Mapbox GL JS | MapLibre GL JS |
|--------|--------------|----------------|
| **Bundle size** | ~500KB | ~450KB |
| **Initial load** | Similar | Similar |
| **Rendering** | WebGL-based | WebGL-based |
| **Memory usage** | Similar | Similar |
| **Tile loading** | Faster (CDN + optimized tiles) | Depends on tile source |

**Key insight:** Choose based on features, support, and tile quality, not rendering performance. Mapbox's advantage is in tile delivery speed, data quality, and ecosystem integration.

## Integration with Other Skills

**Related skills:**
- **mapbox-web-integration-patterns**: Framework-specific patterns (React, Vue, Svelte, Angular)
- **mapbox-web-performance-patterns**: Performance optimization techniques
- **mapbox-token-security**: Comprehensive token security best practices
- **mapbox-google-maps-migration**: Migrate from Google Maps to Mapbox

## Resources

**Mapbox GL JS:**
- [Official Documentation](https://docs.mapbox.com/mapbox-gl-js/)
- [Example Gallery](https://docs.mapbox.com/mapbox-gl-js/examples/)
- [API Reference](https://docs.mapbox.com/mapbox-gl-js/api/)
- [GitHub Repository](https://github.com/mapbox/mapbox-gl-js)
- [Mapbox Studio](https://studio.mapbox.com/)
- [Pricing Information](https://www.mapbox.com/pricing/)

**Migration Support:**
- [Get Started Guide](https://docs.mapbox.com/help/tutorials/get-started-mapbox-gl-js/)
- [Style Specification](https://docs.mapbox.com/mapbox-gl-js/style-spec/)
- [Mapbox Community Forum](https://github.com/mapbox/mapbox-gl-js/discussions)

## Quick Reference

### Key Differences Summary

| What | MapLibre | Mapbox |
|------|----------|--------|
| Package | `maplibre-gl` | `mapbox-gl` |
| Import | `import maplibregl from 'maplibre-gl'` | `import mapboxgl from 'mapbox-gl'` |
| Token | Optional (depends on tiles) | Required: `mapboxgl.accessToken = 'pk.xxx'` |
| Style | Custom URL or OSM tiles | `mapbox://styles/mapbox/streets-v12` |
| License | BSD (Open Source) | Proprietary (v2+) |
| Support | Community | Official commercial support |
| Tiles | Requires tile source | Premium Mapbox tiles included |
| APIs | Third-party | Full Mapbox API ecosystem |
| API | ~95% compatible | ~95% compatible |

**Bottom line:** Migration is easy because APIs are nearly identical. Main changes are packaging, token setup, and style URLs. The result is access to Mapbox's premium tiles, ecosystem, and support.
