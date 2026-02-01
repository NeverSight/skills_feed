---
name: mapbox-web-performance-patterns
description: Performance optimization patterns for Mapbox GL JS web applications. Covers initialization waterfalls, bundle size, rendering performance, memory management, and web optimization. Prioritized by impact on user experience.
---

# Mapbox Performance Patterns Skill

This skill provides performance optimization guidance for building fast, efficient Mapbox applications. Patterns are prioritized by impact on user experience, starting with the most critical improvements.

**Performance philosophy:** These aren't micro-optimizations. They show up as waiting time, jank, and repeat costs that hit every user session.

## Priority Levels

Performance issues are prioritized by their impact on user experience:

- **🔴 Critical (Fix First)**: Directly causes slow initial load or visible jank
- **🟡 High Impact**: Noticeable delays or increased resource usage
- **🟢 Optimization**: Incremental improvements for polish

---

## 🔴 Critical: Eliminate Initialization Waterfalls

**Problem:** Sequential loading creates cascading delays where each resource waits for the previous one.

**Note:** Modern bundlers (Vite, Webpack, etc.) and ESM dynamic imports automatically handle code splitting and library loading. The primary waterfall to eliminate is **data loading** - fetching map data sequentially instead of in parallel with map initialization.

### Anti-Pattern: Sequential Data Loading

```javascript
// ❌ BAD: Data loads AFTER map initializes
async function initMap() {
  const map = new mapboxgl.Map({
    container: 'map',
    accessToken: MAPBOX_TOKEN,
    style: 'mapbox://styles/mapbox/streets-v12'
  });

  // Wait for map to load, THEN fetch data
  map.on('load', async () => {
    const data = await fetch('/api/data'); // Waterfall!
    map.addSource('data', { type: 'geojson', data: await data.json() });
  });
}
```

**Timeline:** Map init (0.5s) → Data fetch (1s) = **1.5s total**

### ✅ Solution: Parallel Data Loading

```javascript
// ✅ GOOD: Data fetch starts immediately
async function initMap() {
  // Start data fetch immediately (don't wait for map)
  const dataPromise = fetch('/api/data').then((r) => r.json());

  const map = new mapboxgl.Map({
    container: 'map',
    accessToken: MAPBOX_TOKEN,
    style: 'mapbox://styles/mapbox/streets-v12'
  });

  // Data is ready when map loads
  map.on('load', async () => {
    const data = await dataPromise;
    map.addSource('data', { type: 'geojson', data });
    map.addLayer({
      id: 'data-layer',
      type: 'circle',
      source: 'data'
    });
  });
}
```

**Timeline:** Max(map init, data fetch) = **~1s total**

### Preload Critical Tiles

```javascript
// ✅ Preload tiles for initial viewport
const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/streets-v12',
  center: [-122.4194, 37.7749],
  zoom: 13,
  // Preload tiles 1 zoom level up
  maxBounds: [
    [-122.5, 37.7], // Southwest
    [-122.3, 37.85] // Northeast
  ]
});

// Prefetch tiles before user interaction
map.once('idle', () => {
  // Map is ready, tiles are cached
  console.log('Initial tiles loaded');
});
```

### Defer Non-Critical Features

```javascript
// ✅ Load critical features first, defer others
const map = new mapboxgl.Map({
  /* config */
});

map.on('load', () => {
  // 1. Add critical layers immediately
  addCriticalLayers(map);

  // 2. Defer secondary features (classic styles only)
  // Note: 3D buildings cannot be deferred with Mapbox Standard style
  requestIdleCallback(
    () => {
      add3DBuildings(map); // For classic styles only
      addTerrain(map);
    },
    { timeout: 2000 }
  );

  // 3. Defer analytics and non-visual features
  setTimeout(() => {
    initializeAnalytics(map);
  }, 3000);
});
```

**Impact:** Reduces time-to-interactive by 50-70%

---

## 🔴 Critical: Optimize Initial Bundle Size

**Problem:** Large bundles delay time-to-interactive on slow networks.

**Note:** Modern bundlers (Vite, Webpack, etc.) automatically handle code splitting for framework-based applications. The guidance below is most relevant for optimizing what gets bundled and when.

### Style JSON Bundle Impact

```javascript
// ❌ BAD: Inline massive style JSON (can be 500+ KB)
const style = {
  version: 8,
  sources: {
    /* 100s of lines */
  },
  layers: [
    /* 100s of layers */
  ]
};

// ✅ GOOD: Reference Mapbox-hosted styles
const map = new mapboxgl.Map({
  style: 'mapbox://styles/mapbox/streets-v12' // Fetched on demand
});

// ✅ OR: Store large custom styles externally
const map = new mapboxgl.Map({
  style: '/styles/custom-style.json' // Loaded separately
});
```

**Impact:** Reduces initial bundle by 30-50%

---

## 🟡 High Impact: Optimize Marker Count

**Problem:** Too many markers causes slow rendering and interaction lag.

### Performance Thresholds

- **< 500 markers**: HTML markers OK (Marker class)
- **500-100,000 markers**: Use Canvas markers or simple symbols
- **100,000-250,000 markers**: Clustering required
- **> 250,000 markers**: Server-side clustering + vector tiles

### Anti-Pattern: Thousands of HTML Markers

```javascript
// ❌ BAD: 5,000 HTML markers = 5+ second render, janky pan/zoom
restaurants.forEach((restaurant) => {
  const marker = new mapboxgl.Marker()
    .setLngLat([restaurant.lng, restaurant.lat])
    .setPopup(new mapboxgl.Popup().setHTML(restaurant.name))
    .addTo(map);
});
```

**Result:** 5,000 DOM elements, slow interactions, high memory

### ✅ Solution: Use Symbol Layers (GeoJSON)

```javascript
// ✅ GOOD: GPU-accelerated rendering, smooth at 10,000+ features
map.addSource('restaurants', {
  type: 'geojson',
  data: {
    type: 'FeatureCollection',
    features: restaurants.map((r) => ({
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [r.lng, r.lat] },
      properties: { name: r.name, type: r.type }
    }))
  }
});

map.addLayer({
  id: 'restaurants',
  type: 'symbol',
  source: 'restaurants',
  layout: {
    'icon-image': 'restaurant',
    'icon-size': 0.8,
    'text-field': ['get', 'name'],
    'text-size': 12,
    'text-offset': [0, 1.5],
    'text-anchor': 'top'
  }
});

// Click handler (one listener for all features)
map.on('click', 'restaurants', (e) => {
  const feature = e.features[0];
  new mapboxgl.Popup()
    .setLngLat(feature.geometry.coordinates)
    .setHTML(feature.properties.name)
    .addTo(map);
});
```

**Performance:** 10,000 features render in <100ms

### ✅ Solution: Clustering for High Density

```javascript
// ✅ GOOD: 50,000 markers → ~500 clusters at low zoom
map.addSource('restaurants', {
  type: 'geojson',
  data: restaurantsGeoJSON,
  cluster: true,
  clusterMaxZoom: 14, // Stop clustering at zoom 15
  clusterRadius: 50 // Cluster radius in pixels
});

// Cluster circle layer
map.addLayer({
  id: 'clusters',
  type: 'circle',
  source: 'restaurants',
  filter: ['has', 'point_count'],
  paint: {
    'circle-color': [
      'step',
      ['get', 'point_count'],
      '#51bbd6',
      100,
      '#f1f075',
      750,
      '#f28cb1'
    ],
    'circle-radius': ['step', ['get', 'point_count'], 20, 100, 30, 750, 40]
  }
});

// Cluster count label
map.addLayer({
  id: 'cluster-count',
  type: 'symbol',
  source: 'restaurants',
  filter: ['has', 'point_count'],
  layout: {
    'text-field': '{point_count_abbreviated}',
    'text-size': 12
  }
});

// Individual point layer
map.addLayer({
  id: 'unclustered-point',
  type: 'circle',
  source: 'restaurants',
  filter: ['!', ['has', 'point_count']],
  paint: {
    'circle-color': '#11b4da',
    'circle-radius': 6
  }
});
```

**Impact:** 50,000 markers → 60 FPS, instant interaction

---

## 🟡 High Impact: Optimize Data Loading Strategy

**Problem:** Loading all data upfront wastes bandwidth and slows initial render.

### GeoJSON vs Vector Tiles Decision Matrix

| Scenario                  | Use GeoJSON | Use Vector Tiles |
| ------------------------- | ----------- | ---------------- |
| < 5 MB data               | ✅          | ❌               |
| 5-20 MB data              | ⚠️ Consider | ✅               |
| > 20 MB data              | ❌          | ✅               |
| Data changes frequently   | ✅          | ❌               |
| Static data, global scale | ❌          | ✅               |
| Need server-side updates  | ❌          | ✅               |

### ✅ Viewport-Based Loading (GeoJSON)

**Note:** This pattern is applicable when hosting GeoJSON data locally or on external servers. Mapbox-hosted data sources are already optimized for viewport-based loading.

```javascript
// ✅ Only load data in current viewport
async function loadVisibleData(map) {
  const bounds = map.getBounds();
  const bbox = [
    bounds.getWest(),
    bounds.getSouth(),
    bounds.getEast(),
    bounds.getNorth()
  ].join(',');

  const data = await fetch(`/api/data?bbox=${bbox}&zoom=${map.getZoom()}`);

  map.getSource('data').setData(await data.json());
}

// Update on viewport change (with debounce)
let timeout;
map.on('moveend', () => {
  clearTimeout(timeout);
  timeout = setTimeout(() => loadVisibleData(map), 300);
});
```

### ✅ Progressive Data Loading

**Note:** This pattern is applicable when hosting GeoJSON data locally or on external servers.

```javascript
// ✅ Load basic data first, add details progressively
async function loadDataProgressive(map) {
  // 1. Load simplified data first (low-res)
  const simplified = await fetch('/api/data?detail=low');
  map.addSource('data', {
    type: 'geojson',
    data: await simplified.json()
  });
  addLayers(map);

  // 2. Load full detail in background
  const detailed = await fetch('/api/data?detail=high');
  map.getSource('data').setData(await detailed.json());
}
```

### ✅ Vector Tiles for Large Datasets

**Note:** The `minzoom`/`maxzoom` optimization shown below is primarily for self-hosted vector tilesets. Mapbox-hosted tilesets have built-in optimization via [Mapbox Tiling Service (MTS)](https://docs.mapbox.com/mapbox-tiling-service/guides/) recipes that handle zoom-level optimizations automatically.

```javascript
// ✅ Server generates tiles, client loads only visible area (self-hosted tilesets)
map.addSource('large-dataset', {
  type: 'vector',
  tiles: ['https://api.example.com/tiles/{z}/{x}/{y}.pbf'],
  minzoom: 0,
  maxzoom: 14
});

map.addLayer({
  id: 'large-dataset-layer',
  type: 'fill',
  source: 'large-dataset',
  'source-layer': 'data', // Layer name in .pbf
  paint: {
    'fill-color': '#088',
    'fill-opacity': 0.6
  }
});
```

**Impact:** 10 MB dataset → 500 KB per viewport, 20x faster load

---

## 🟡 High Impact: Optimize Map Interactions

**Problem:** Unthrottled event handlers cause performance degradation.

### Anti-Pattern: Expensive Operations on Every Event

```javascript
// ❌ BAD: Runs 100+ times per second during pan
map.on('move', () => {
  updateVisibleFeatures(); // Expensive query
  fetchDataFromAPI(); // Network request
  updateUI(); // DOM manipulation
});
```

### ✅ Solution: Debounce/Throttle Events

```javascript
// ✅ GOOD: Throttle during interaction, finalize on idle
let throttleTimeout;

// Lightweight updates during move (throttled)
map.on('move', () => {
  if (throttleTimeout) return;
  throttleTimeout = setTimeout(() => {
    updateMapCenter(); // Cheap update
    throttleTimeout = null;
  }, 100);
});

// Expensive operations after interaction stops
map.on('moveend', () => {
  updateVisibleFeatures();
  fetchDataFromAPI();
  updateUI();
});
```

### ✅ Optimize Feature Queries

```javascript
// ❌ BAD: Query all features (expensive with many layers)
map.on('click', (e) => {
  const features = map.queryRenderedFeatures(e.point);
  console.log(features); // Could be 100+ features
});

// ✅ GOOD: Query specific layers with radius
map.on('click', (e) => {
  const features = map.queryRenderedFeatures(e.point, {
    layers: ['restaurants', 'shops'], // Only query these layers
    radius: 5 // 5px radius around click point
  });

  if (features.length > 0) {
    showPopup(features[0]);
  }
});

// ✅ EVEN BETTER: Use filter to reduce results
const features = map.queryRenderedFeatures(e.point, {
  layers: ['restaurants'],
  filter: ['==', ['get', 'type'], 'pizza'] // Only pizza restaurants
});
```

### ✅ Batch DOM Updates

```javascript
// ❌ BAD: Update DOM for every feature
map.on('mousemove', 'restaurants', (e) => {
  e.features.forEach((feature) => {
    document.getElementById(feature.id).classList.add('highlight');
  });
});

// ✅ GOOD: Batch updates with requestAnimationFrame
let pendingUpdates = new Set();
let rafScheduled = false;

map.on('mousemove', 'restaurants', (e) => {
  e.features.forEach((f) => pendingUpdates.add(f.id));

  if (!rafScheduled) {
    rafScheduled = true;
    requestAnimationFrame(() => {
      pendingUpdates.forEach((id) => {
        document.getElementById(id).classList.add('highlight');
      });
      pendingUpdates.clear();
      rafScheduled = false;
    });
  }
});
```

**Impact:** 60 FPS maintained during interaction vs 15-20 FPS without optimization

---

## 🟢 Optimization: Memory Management

**Problem:** Memory leaks cause browser tabs to become unresponsive over time.

### ✅ Always Clean Up Map Resources

```javascript
// ✅ Essential cleanup pattern
function cleanupMap(map) {
  if (!map) return;

  // 1. Remove event listeners
  map.off('load', handleLoad);
  map.off('move', handleMove);

  // 2. Remove layers (if adding/removing dynamically)
  if (map.getLayer('dynamic-layer')) {
    map.removeLayer('dynamic-layer');
  }

  // 3. Remove sources (if adding/removing dynamically)
  if (map.getSource('dynamic-source')) {
    map.removeSource('dynamic-source');
  }

  // 4. Remove controls
  map.removeControl(navigationControl);

  // 5. CRITICAL: Remove map instance
  map.remove();
}

// React example
useEffect(() => {
  const map = new mapboxgl.Map({
    /* config */
  });

  return () => {
    cleanupMap(map); // Called on unmount
  };
}, []);
```

### ✅ Clean Up Popups and Markers

```javascript
// ❌ BAD: Creates new popup on every click (memory leak)
map.on('click', 'restaurants', (e) => {
  new mapboxgl.Popup()
    .setLngLat(e.lngLat)
    .setHTML(e.features[0].properties.name)
    .addTo(map);
  // Popup never removed!
});

// ✅ GOOD: Reuse single popup instance
let popup = new mapboxgl.Popup({ closeOnClick: true });

map.on('click', 'restaurants', (e) => {
  popup.setLngLat(e.lngLat).setHTML(e.features[0].properties.name).addTo(map);
  // Popup removed when map closes or new popup shows
});

// Cleanup
function cleanup() {
  popup.remove();
  popup = null;
}
```

### ✅ Use Feature State Instead of New Layers

```javascript
// ❌ BAD: Create new layer for hover (memory overhead)
let hoveredFeatureId = null;

map.on('mousemove', 'restaurants', (e) => {
  if (map.getLayer('hover-layer')) {
    map.removeLayer('hover-layer');
  }
  map.addLayer({
    id: 'hover-layer',
    type: 'circle',
    source: 'restaurants',
    filter: ['==', ['id'], e.features[0].id],
    paint: { 'circle-color': 'yellow' }
  });
});

// ✅ GOOD: Use feature state (efficient, no layer creation)
map.on('mousemove', 'restaurants', (e) => {
  if (e.features.length > 0) {
    // Remove previous hover state
    if (hoveredFeatureId !== null) {
      map.setFeatureState(
        { source: 'restaurants', id: hoveredFeatureId },
        { hover: false }
      );
    }

    // Set new hover state
    hoveredFeatureId = e.features[0].id;
    map.setFeatureState(
      { source: 'restaurants', id: hoveredFeatureId },
      { hover: true }
    );
  }
});

// Style uses feature state
map.addLayer({
  id: 'restaurants',
  type: 'circle',
  source: 'restaurants',
  paint: {
    'circle-color': [
      'case',
      ['boolean', ['feature-state', 'hover'], false],
      '#ffff00', // Yellow when hover
      '#0000ff' // Blue otherwise
    ]
  }
});
```

**Impact:** Prevents memory growth from 200 MB → 2 GB over session

---

## 🟢 Optimization: Mobile Performance

**Problem:** Mobile devices have limited resources (CPU, GPU, memory, battery).

### Mobile-Specific Optimizations

```javascript
// Detect mobile device
const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/streets-v12',

  // Mobile optimizations
  ...(isMobile && {
    // Reduce tile quality on mobile (30% smaller tiles)
    transformRequest: (url, resourceType) => {
      if (resourceType === 'Tile') {
        return {
          url: url.replace('@2x', '') // Use 1x tiles instead of 2x
        };
      }
    },

    // Disable expensive features on mobile
    maxPitch: 45, // Limit 3D perspective (battery saver)

    // Simplify rendering
    fadeDuration: 100 // Faster transitions = less GPU work
  })
});

// Load fewer features on mobile
map.on('load', () => {
  if (isMobile) {
    // Simple marker rendering
    map.addLayer({
      id: 'markers-mobile',
      type: 'circle',
      source: 'data',
      paint: {
        'circle-radius': 8,
        'circle-color': '#007cbf'
      }
    });
  } else {
    // Rich desktop rendering with icons and labels
    map.addLayer({
      id: 'markers-desktop',
      type: 'symbol',
      source: 'data',
      layout: {
        'icon-image': 'marker',
        'icon-size': 1,
        'text-field': ['get', 'name'],
        'text-size': 12,
        'text-offset': [0, 1.5]
      }
    });
  }
});
```

### Touch Event Optimization

```javascript
// ✅ Optimize touch interactions
map.touchZoomRotate.disableRotation(); // Disable rotation (simpler gestures)

// Debounce expensive operations during touch
let touchTimeout;
map.on('touchmove', () => {
  if (touchTimeout) clearTimeout(touchTimeout);
  touchTimeout = setTimeout(() => {
    updateVisibleData();
  }, 500); // Wait for touch to settle
});
```

### Battery-Conscious Loading

```javascript
// ✅ Respect battery status
if ('getBattery' in navigator) {
  navigator.getBattery().then((battery) => {
    const isLowBattery = battery.level < 0.2;

    if (isLowBattery) {
      // Reduce quality and features
      map.setMaxZoom(15); // Limit detail
      disableAnimations(map);
      disableTerrain(map);
    }
  });
}
```

**Impact:** 50% reduction in battery drain, smoother interactions on older devices

---

## 🟢 Optimization: Layer and Style Performance

### Consolidate Layers

```javascript
// ❌ BAD: 20 separate layers for restaurant types
restaurantTypes.forEach((type) => {
  map.addLayer({
    id: `restaurants-${type}`,
    type: 'symbol',
    source: 'restaurants',
    filter: ['==', ['get', 'type'], type],
    layout: { 'icon-image': `${type}-icon` }
  });
});

// ✅ GOOD: Single layer with data-driven styling
map.addLayer({
  id: 'restaurants',
  type: 'symbol',
  source: 'restaurants',
  layout: {
    'icon-image': [
      'match',
      ['get', 'type'],
      'pizza',
      'pizza-icon',
      'burger',
      'burger-icon',
      'sushi',
      'sushi-icon',
      'default-icon' // fallback
    ]
  }
});
```

**Impact:** 20 layers → 1 layer = 95% fewer draw calls

### Simplify Paint Properties

```javascript
// ❌ BAD: Complex expression evaluated per frame
map.addLayer({
  id: 'buildings',
  type: 'fill-extrusion',
  source: 'buildings',
  paint: {
    'fill-extrusion-color': [
      'interpolate',
      ['linear'],
      ['get', 'height'],
      0,
      '#dedede',
      10,
      '#c0c0c0',
      20,
      '#a0a0a0',
      50,
      '#808080',
      100,
      '#606060'
    ],
    'fill-extrusion-height': [
      '*',
      ['get', 'height'],
      ['case', ['>', ['zoom'], 16], 1.5, 1.0]
    ]
  }
});

// ✅ GOOD: Pre-compute where possible
// Pre-process data to add computed properties
const buildingsWithPrecomputed = {
  type: 'FeatureCollection',
  features: buildings.features.map((f) => ({
    ...f,
    properties: {
      ...f.properties,
      displayHeight: f.properties.height * 1.5, // Pre-computed
      heightColor: getColorForHeight(f.properties.height) // Pre-computed
    }
  }))
};

map.addLayer({
  id: 'buildings',
  type: 'fill-extrusion',
  paint: {
    'fill-extrusion-color': ['get', 'heightColor'],
    'fill-extrusion-height': ['get', 'displayHeight']
  }
});
```

### Use Zoom-Based Layer Visibility

```javascript
// ✅ Only render layers when visible
map.addLayer({
  id: 'building-details',
  type: 'fill',
  source: 'buildings',
  minzoom: 15, // Only render at zoom 15+
  maxzoom: 22,
  paint: { 'fill-color': '#aaa' }
});

map.addLayer({
  id: 'poi-labels',
  type: 'symbol',
  source: 'pois',
  minzoom: 12, // Hide at low zoom levels
  layout: {
    'text-field': ['get', 'name'],
    visibility: 'visible'
  }
});
```

**Impact:** 40% reduction in GPU usage at low zoom levels

---

## Summary: Performance Checklist

When building a Mapbox application, verify these optimizations in order:

### 🔴 Critical (Do First)

- [ ] Load map library and data in parallel (eliminate waterfalls)
- [ ] Use dynamic imports for map code (reduce initial bundle)
- [ ] Defer non-critical features (3D, terrain, analytics)
- [ ] Use clustering or symbol layers for > 100 markers
- [ ] Implement viewport-based data loading for large datasets

### 🟡 High Impact

- [ ] Debounce/throttle map event handlers
- [ ] Optimize queryRenderedFeatures with layers and radius
- [ ] Use GeoJSON for < 1 MB, vector tiles for > 10 MB
- [ ] Implement progressive data loading

### 🟢 Optimization

- [ ] Always call map.remove() on cleanup
- [ ] Reuse popup instances (don't create on every interaction)
- [ ] Use feature state instead of dynamic layers
- [ ] Consolidate multiple layers with data-driven styling
- [ ] Add mobile-specific optimizations (simpler rendering, battery awareness)
- [ ] Set minzoom/maxzoom on layers to avoid rendering when not visible

### Measurement

Use these tools to measure impact:

```javascript
// Measure initial load time
console.time('map-load');
map.on('load', () => {
  console.timeEnd('map-load');
  console.log('Tiles loaded:', map.isStyleLoaded());
});

// Monitor frame rate
let frameCount = 0;
map.on('render', () => frameCount++);
setInterval(() => {
  console.log('FPS:', frameCount);
  frameCount = 0;
}, 1000);

// Check memory usage (Chrome DevTools → Performance → Memory)
```

**Target metrics:**

- **Time to Interactive:** < 2 seconds on 3G
- **Frame Rate:** 60 FPS during pan/zoom
- **Memory Growth:** < 10 MB per hour of usage
- **Bundle Size:** < 500 KB initial (map lazy-loaded)
