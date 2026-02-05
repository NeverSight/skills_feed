---
name: mapbox-google-maps-migration
description: Migration guide for developers moving from Google Maps Platform to Mapbox GL JS, covering API equivalents, pattern translations, and key differences
---

# Mapbox Google Maps Migration Skill

Comprehensive guidance for migrating from Google Maps Platform to Mapbox GL JS. Provides API equivalents, pattern translations, and strategies for successful migration.

## Core Philosophy Differences

### Google Maps: Imperative & Object-Oriented
- Create objects (Marker, Polygon, etc.)
- Add to map with `.setMap(map)`
- Update properties with setters
- Heavy reliance on object instances

### Mapbox GL JS: Declarative & Data-Driven
- Add data sources
- Define layers (visual representation)
- Style with JSON
- Update data, not object properties

**Key Insight:** Mapbox treats everything as data + styling, not individual objects.

## Map Initialization

### Google Maps
```javascript
const map = new google.maps.Map(document.getElementById('map'), {
  center: { lat: 37.7749, lng: -122.4194 },
  zoom: 12,
  mapTypeId: 'roadmap' // or 'satellite', 'hybrid', 'terrain'
});
```

### Mapbox GL JS
```javascript
mapboxgl.accessToken = 'YOUR_MAPBOX_TOKEN';
const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/streets-v12', // or satellite-v9, outdoors-v12
  center: [-122.4194, 37.7749], // [lng, lat] - note the order!
  zoom: 12
});
```

**Key Differences:**
- **Coordinate order:** Google uses `{lat, lng}`, Mapbox uses `[lng, lat]`
- **Authentication:** Google uses API key in script tag, Mapbox uses access token in code
- **Styling:** Google uses map types, Mapbox uses full style URLs

## API Equivalents Reference

### Map Methods

| Google Maps | Mapbox GL JS | Notes |
|-------------|--------------|-------|
| `map.setCenter(latLng)` | `map.setCenter([lng, lat])` | Coordinate order reversed |
| `map.getCenter()` | `map.getCenter()` | Returns LngLat object |
| `map.setZoom(zoom)` | `map.setZoom(zoom)` | Same behavior |
| `map.getZoom()` | `map.getZoom()` | Same behavior |
| `map.panTo(latLng)` | `map.panTo([lng, lat])` | Animated pan |
| `map.fitBounds(bounds)` | `map.fitBounds([[lng,lat],[lng,lat]])` | Different bound format |
| `map.setMapTypeId(type)` | `map.setStyle(styleUrl)` | Completely different approach |
| `map.getBounds()` | `map.getBounds()` | Similar |

### Map Events

| Google Maps | Mapbox GL JS | Notes |
|-------------|--------------|-------|
| `google.maps.event.addListener(map, 'click', fn)` | `map.on('click', fn)` | Simpler syntax |
| `event.latLng` | `event.lngLat` | Event property name |
| `'center_changed'` | `'move'` / `'moveend'` | Different event names |
| `'zoom_changed'` | `'zoom'` / `'zoomend'` | Different event names |
| `'bounds_changed'` | `'moveend'` | No direct equivalent |
| `'mousemove'` | `'mousemove'` | Same |
| `'mouseout'` | `'mouseleave'` | Different name |

## Markers and Points

### Simple Marker

**Google Maps:**
```javascript
const marker = new google.maps.Marker({
  position: { lat: 37.7749, lng: -122.4194 },
  map: map,
  title: 'San Francisco',
  icon: 'custom-icon.png'
});

// Remove marker
marker.setMap(null);
```

**Mapbox GL JS:**
```javascript
// Create marker
const marker = new mapboxgl.Marker()
  .setLngLat([-122.4194, 37.7749])
  .setPopup(new mapboxgl.Popup().setText('San Francisco'))
  .addTo(map);

// Remove marker
marker.remove();
```

### Multiple Markers

**Google Maps:**
```javascript
const markers = locations.map(loc =>
  new google.maps.Marker({
    position: { lat: loc.lat, lng: loc.lng },
    map: map
  })
);
```

**Mapbox GL JS (Equivalent Approach):**
```javascript
// Same object-oriented approach
const markers = locations.map(loc =>
  new mapboxgl.Marker()
    .setLngLat([loc.lng, loc.lat])
    .addTo(map)
);
```

**Mapbox GL JS (Data-Driven Approach - Recommended for 100+ points):**
```javascript
// Add as GeoJSON source + layer (uses WebGL, not DOM)
map.addSource('points', {
  type: 'geojson',
  data: {
    type: 'FeatureCollection',
    features: locations.map(loc => ({
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [loc.lng, loc.lat] },
      properties: { name: loc.name }
    }))
  }
});

map.addLayer({
  id: 'points-layer',
  type: 'circle', // or 'symbol' for icons
  source: 'points',
  paint: {
    'circle-radius': 8,
    'circle-color': '#ff0000'
  }
});
```

**Performance Advantage:** Google Maps renders all markers as DOM elements (even when using the Data Layer), which becomes slow with 500+ markers. Mapbox's circle and symbol layers are rendered by WebGL, making them much faster for large datasets (1,000-10,000+ points). This is a significant advantage when building applications with many points.

## Info Windows / Popups

### Google Maps
```javascript
const infowindow = new google.maps.InfoWindow({
  content: '<h3>Title</h3><p>Content</p>'
});

marker.addListener('click', () => {
  infowindow.open(map, marker);
});
```

### Mapbox GL JS
```javascript
// Option 1: Attach to marker
const marker = new mapboxgl.Marker()
  .setLngLat([-122.4194, 37.7749])
  .setPopup(new mapboxgl.Popup().setHTML('<h3>Title</h3><p>Content</p>'))
  .addTo(map);

// Option 2: On layer click (for data-driven markers)
map.on('click', 'points-layer', (e) => {
  const coordinates = e.features[0].geometry.coordinates.slice();
  const description = e.features[0].properties.description;

  new mapboxgl.Popup()
    .setLngLat(coordinates)
    .setHTML(description)
    .addTo(map);
});
```

## Polygons and Shapes

### Google Maps
```javascript
const polygon = new google.maps.Polygon({
  paths: [
    { lat: 37.7749, lng: -122.4194 },
    { lat: 37.7849, lng: -122.4094 },
    { lat: 37.7649, lng: -122.4094 }
  ],
  strokeColor: '#FF0000',
  strokeOpacity: 0.8,
  strokeWeight: 2,
  fillColor: '#FF0000',
  fillOpacity: 0.35,
  map: map
});
```

### Mapbox GL JS
```javascript
map.addSource('polygon', {
  type: 'geojson',
  data: {
    type: 'Feature',
    geometry: {
      type: 'Polygon',
      coordinates: [[
        [-122.4194, 37.7749],
        [-122.4094, 37.7849],
        [-122.4094, 37.7649],
        [-122.4194, 37.7749] // Close the ring
      ]]
    }
  }
});

map.addLayer({
  id: 'polygon-layer',
  type: 'fill',
  source: 'polygon',
  paint: {
    'fill-color': '#FF0000',
    'fill-opacity': 0.35
  }
});

// Add outline
map.addLayer({
  id: 'polygon-outline',
  type: 'line',
  source: 'polygon',
  paint: {
    'line-color': '#FF0000',
    'line-width': 2,
    'line-opacity': 0.8
  }
});
```

## Polylines / Lines

### Google Maps
```javascript
const line = new google.maps.Polyline({
  path: [
    { lat: 37.7749, lng: -122.4194 },
    { lat: 37.7849, lng: -122.4094 }
  ],
  strokeColor: '#0000FF',
  strokeWeight: 3,
  map: map
});
```

### Mapbox GL JS
```javascript
map.addSource('route', {
  type: 'geojson',
  data: {
    type: 'Feature',
    geometry: {
      type: 'LineString',
      coordinates: [
        [-122.4194, 37.7749],
        [-122.4094, 37.7849]
      ]
    }
  }
});

map.addLayer({
  id: 'route-layer',
  type: 'line',
  source: 'route',
  paint: {
    'line-color': '#0000FF',
    'line-width': 3
  }
});
```

## Custom Icons and Symbols

### Google Maps
```javascript
const marker = new google.maps.Marker({
  position: { lat: 37.7749, lng: -122.4194 },
  map: map,
  icon: {
    url: 'marker.png',
    scaledSize: new google.maps.Size(32, 32)
  }
});
```

### Mapbox GL JS

**Option 1: HTML Marker**
```javascript
const el = document.createElement('div');
el.className = 'marker';
el.style.backgroundImage = 'url(marker.png)';
el.style.width = '32px';
el.style.height = '32px';

new mapboxgl.Marker(el)
  .setLngLat([-122.4194, 37.7749])
  .addTo(map);
```

**Option 2: Symbol Layer (Better Performance)**
```javascript
// Load image
map.loadImage('marker.png', (error, image) => {
  if (error) throw error;
  map.addImage('custom-marker', image);

  map.addLayer({
    id: 'markers',
    type: 'symbol',
    source: 'points',
    layout: {
      'icon-image': 'custom-marker',
      'icon-size': 1
    }
  });
});
```

## Geocoding

### Google Maps
```javascript
const geocoder = new google.maps.Geocoder();

geocoder.geocode({ address: '1600 Amphitheatre Parkway' }, (results, status) => {
  if (status === 'OK') {
    map.setCenter(results[0].geometry.location);
  }
});
```

### Mapbox GL JS
```javascript
// Use Mapbox Geocoding API v6
fetch(`https://api.mapbox.com/search/geocode/v6/forward?q=1600+Amphitheatre+Parkway&access_token=${mapboxgl.accessToken}`)
  .then(response => response.json())
  .then(data => {
    const [lng, lat] = data.features[0].geometry.coordinates;
    map.setCenter([lng, lat]);
  });

// Or use mapbox-gl-geocoder plugin
const geocoder = new MapboxGeocoder({
  accessToken: mapboxgl.accessToken,
  mapboxgl: mapboxgl
});

map.addControl(geocoder);
```

## Directions / Routing

### Google Maps
```javascript
const directionsService = new google.maps.DirectionsService();
const directionsRenderer = new google.maps.DirectionsRenderer();
directionsRenderer.setMap(map);

directionsService.route({
  origin: 'San Francisco, CA',
  destination: 'Los Angeles, CA',
  travelMode: 'DRIVING'
}, (response, status) => {
  if (status === 'OK') {
    directionsRenderer.setDirections(response);
  }
});
```

### Mapbox GL JS
```javascript
// Use Mapbox Directions API
const origin = [-122.4194, 37.7749];
const destination = [-118.2437, 34.0522];

fetch(`https://api.mapbox.com/directions/v5/mapbox/driving/${origin.join(',')};${destination.join(',')}?geometries=geojson&access_token=${mapboxgl.accessToken}`)
  .then(response => response.json())
  .then(data => {
    const route = data.routes[0].geometry;

    map.addSource('route', {
      type: 'geojson',
      data: {
        type: 'Feature',
        geometry: route
      }
    });

    map.addLayer({
      id: 'route',
      type: 'line',
      source: 'route',
      paint: {
        'line-color': '#3887be',
        'line-width': 5
      }
    });
  });

// Or use @mapbox/mapbox-gl-directions plugin
const directions = new MapboxDirections({
  accessToken: mapboxgl.accessToken
});

map.addControl(directions, 'top-left');
```

## Controls

### Google Maps
```javascript
// Controls are automatic, can configure:
map.setOptions({
  zoomControl: true,
  mapTypeControl: true,
  streetViewControl: false,
  fullscreenControl: true
});
```

### Mapbox GL JS
```javascript
// Add controls explicitly
map.addControl(new mapboxgl.NavigationControl()); // Zoom + rotation
map.addControl(new mapboxgl.FullscreenControl());
map.addControl(new mapboxgl.GeolocateControl());
map.addControl(new mapboxgl.ScaleControl());

// Position controls
map.addControl(new mapboxgl.NavigationControl(), 'top-right');
```

## Clustering

### Google Maps
```javascript
// Requires MarkerClusterer library
import MarkerClusterer from '@googlemaps/markerclustererplus';

const markers = locations.map(loc =>
  new google.maps.Marker({ position: loc, map: map })
);

new MarkerClusterer(map, markers, {
  imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'
});
```

### Mapbox GL JS
```javascript
// Built-in clustering support
map.addSource('points', {
  type: 'geojson',
  data: geojsonData,
  cluster: true,
  clusterMaxZoom: 14,
  clusterRadius: 50
});

// Cluster circles
map.addLayer({
  id: 'clusters',
  type: 'circle',
  source: 'points',
  filter: ['has', 'point_count'],
  paint: {
    'circle-color': [
      'step',
      ['get', 'point_count'],
      '#51bbd6', 100,
      '#f1f075', 750,
      '#f28cb1'
    ],
    'circle-radius': [
      'step',
      ['get', 'point_count'],
      20, 100,
      30, 750,
      40
    ]
  }
});

// Cluster count labels
map.addLayer({
  id: 'cluster-count',
  type: 'symbol',
  source: 'points',
  filter: ['has', 'point_count'],
  layout: {
    'text-field': '{point_count_abbreviated}',
    'text-size': 12
  }
});

// Unclustered points
map.addLayer({
  id: 'unclustered-point',
  type: 'circle',
  source: 'points',
  filter: ['!', ['has', 'point_count']],
  paint: {
    'circle-color': '#11b4da',
    'circle-radius': 8
  }
});
```

**Key Advantage:** Mapbox clustering is built-in and highly performant.

## Styling and Appearance

### Map Types vs. Styles

**Google Maps:**
- Limited map types: roadmap, satellite, hybrid, terrain
- Styling via `styles` array (complex)

**Mapbox GL JS:**
- Full control over every visual element
- Pre-built styles: standard, standard-satellite, streets, outdoors, light, dark
- Custom styles via Mapbox Studio for unique branding and design
- Dynamic styling based on data properties
- For classic styles (pre Mapbox Standard) you can modify style programmatically by using the setPaintProperty()

### Custom Styling Example

**Google Maps:**
```javascript
const styledMapType = new google.maps.StyledMapType([
  { elementType: 'geometry', stylers: [{ color: '#242f3e' }] },
  { elementType: 'labels.text.stroke', stylers: [{ color: '#242f3e' }] },
  // ... many more rules
], { name: 'Dark' });

map.mapTypes.set('dark', styledMapType);
map.setMapTypeId('dark');
```

**Mapbox GL JS:**
```javascript
// Use pre-built style
map.setStyle('mapbox://styles/mapbox/dark-v11');

// Or create custom style in Mapbox Studio and reference it
map.setStyle('mapbox://styles/yourusername/your-style-id');

// Modify classic styles programmatically
map.setPaintProperty('water', 'fill-color', '#242f3e');
```

## Data Updates

### Google Maps
```javascript
// Update marker position
marker.setPosition({ lat: 37.7849, lng: -122.4094 });

// Update polygon path
polygon.setPath(newCoordinates);
```

### Mapbox GL JS
```javascript
// Update source data
map.getSource('points').setData(newGeojsonData);

// Or update specific features
const source = map.getSource('points');
const data = source._data;
data.features[0].geometry.coordinates = [-122.4094, 37.7849];
source.setData(data);
```

## Performance Considerations

### Google Maps
- Individual objects for each feature
- Can be slow with 1000+ markers
- Requires MarkerClusterer for performance

### Mapbox GL JS
- Data-driven rendering
- WebGL-based (hardware accelerated)
- Handles 10,000+ points smoothly
- Built-in clustering

**Migration Tip:** If you have performance issues with Google Maps (many markers), Mapbox will likely perform significantly better.

## Common Migration Patterns

### Pattern 1: Store Locator

**Google Maps approach:**
1. Create marker for each store
2. Add click listeners to each marker
3. Show info window on click

**Mapbox approach:**
1. Add all stores as GeoJSON source
2. Add symbol layer for markers
3. Use layer click event for all markers
4. More performant, cleaner code

### Pattern 2: Drawing Tools

**Google Maps:**
- Use Drawing Manager library
- Creates overlay objects

**Mapbox:**
- Use Mapbox Draw plugin
- More powerful, customizable
- Better for complex editing

### Pattern 3: Heatmaps

**Google Maps:**
```javascript
const heatmap = new google.maps.visualization.HeatmapLayer({
  data: points,
  map: map
});
```

**Mapbox:**
```javascript
map.addLayer({
  id: 'heatmap',
  type: 'heatmap',
  source: 'points',
  paint: {
    'heatmap-intensity': 1,
    'heatmap-radius': 50,
    'heatmap-color': [
      'interpolate',
      ['linear'],
      ['heatmap-density'],
      0, 'rgba(0,0,255,0)',
      0.5, 'lime',
      1, 'red'
    ]
  }
});
```

## Migration Strategy

### Step 1: Audit Current Implementation

Identify all Google Maps features you use:
- [ ] Basic map with markers
- [ ] Info windows/popups
- [ ] Polygons/polylines
- [ ] Geocoding
- [ ] Directions
- [ ] Clustering
- [ ] Custom styling
- [ ] Drawing tools
- [ ] Street View (no Mapbox equivalent)
- [ ] Other advanced features

### Step 2: Set Up Mapbox

```html
<!-- Replace Google Maps script -->
<script src="https://api.mapbox.com/mapbox-gl-js/v3.18.1/mapbox-gl.js"></script>
<link href="https://api.mapbox.com/mapbox-gl-js/v3.18.1/mapbox-gl.css" rel="stylesheet">
```

### Step 3: Convert Core Map

Start with basic map initialization:
1. Replace `new google.maps.Map()` with `new mapboxgl.Map()`
2. Fix coordinate order (lat,lng → lng,lat)
3. Update zoom/center

### Step 4: Convert Features One by One

Prioritize by complexity:
1. **Easy:** Map controls, basic markers
2. **Medium:** Popups, polygons, lines
3. **Complex:** Clustering, custom styling, data updates

### Step 5: Update Event Handlers

Change event syntax:
- `google.maps.event.addListener()` → `map.on()`
- Update event property names (`latLng` → `lngLat`)

### Step 6: Optimize for Mapbox

Take advantage of Mapbox features:
- Convert multiple markers to data-driven layers
- Use clustering (built-in)
- Leverage vector tiles for custom styling
- Use expressions for dynamic styling

### Step 7: Test Thoroughly

- Cross-browser testing
- Mobile responsiveness
- Performance with real data volumes
- Touch/gesture interactions

## Gotchas and Common Issues

### ❌ Coordinate Order
```javascript
// Google Maps
{ lat: 37.7749, lng: -122.4194 }

// Mapbox (REVERSED!)
[-122.4194, 37.7749]
```

**Always double-check coordinate order!**

### ❌ Event Properties
```javascript
// Google Maps
map.on('click', (e) => {
  console.log(e.latLng.lat(), e.latLng.lng());
});

// Mapbox
map.on('click', (e) => {
  console.log(e.lngLat.lat, e.lngLat.lng);
});
```

### ❌ Timing Issues
```javascript
// Google Maps - immediate
const marker = new google.maps.Marker({ map: map });

// Mapbox - wait for load
map.on('load', () => {
  map.addSource(...);
  map.addLayer(...);
});
```

### ❌ Removing Features
```javascript
// Google Maps
marker.setMap(null);

// Mapbox - must remove both
map.removeLayer('layer-id');
map.removeSource('source-id');
```

## API Services Comparison

| Service | Google Maps | Mapbox | Notes |
|---------|-------------|--------|-------|
| **Geocoding** | Geocoding API | Geocoding API | Similar capabilities |
| **Reverse Geocoding** | ✅ | ✅ | Similar |
| **Directions** | Directions API | Directions API | Mapbox has traffic-aware routing |
| **Distance Matrix** | Distance Matrix API | Matrix API | Similar |
| **Isochrones** | ❌ | ✅ | Mapbox exclusive |
| **Optimization** | ❌ | ✅ | Mapbox exclusive (TSP) |
| **Street View** | ✅ | ❌ | Google exclusive |
| **Static Maps** | ✅ | ✅ | Both supported |
| **Satellite Imagery** | ✅ | ✅ | Both supported |
| **Tilesets** | Limited | Full API | Mapbox more flexible |

## Pricing Differences

### Google Maps Platform
- Charges per API call
- Free tier: $200/month credit
- Different rates for different APIs
- Can get expensive with high traffic

### Mapbox
- Charges per map load
- Free tier: 50,000 map loads/month
- Unlimited API requests per map session
- More predictable costs

**Migration Tip:** Understand how pricing models differ for your use case.

## Plugins and Extensions

### Google Maps Plugins → Mapbox Alternatives

| Google Maps Plugin | Mapbox Alternative |
|-------------------|-------------------|
| MarkerClusterer | Built-in clustering |
| Drawing Manager | @mapbox/mapbox-gl-draw |
| Geocoder | @mapbox/mapbox-gl-geocoder |
| Directions | @mapbox/mapbox-gl-directions |
| - | @mapbox/mapbox-gl-traffic |
| - | @mapbox/mapbox-gl-compare |

## Framework Integration

### React

**Google Maps:**
```javascript
import { GoogleMap, Marker } from '@react-google-maps/api';
```

**Mapbox:**
```javascript
import Map, { Marker } from 'react-map-gl';
// or
import { useMap } from '@mapbox/mapbox-gl-react';
```

### Vue

**Google Maps:**
```javascript
import { GoogleMap } from 'vue3-google-map';
```

**Mapbox:**
```javascript
import { MglMap } from 'vue-mapbox';
```

See `mapbox-web-integration-patterns` skill for detailed framework guidance.

## Testing Strategy

### Unit Tests
```javascript
// Mock mapboxgl
jest.mock('mapbox-gl', () => ({
  Map: jest.fn(() => ({
    on: jest.fn(),
    addSource: jest.fn(),
    addLayer: jest.fn()
  })),
  Marker: jest.fn()
}));
```

### Integration Tests
- Test map initialization
- Test data loading and updates
- Test user interactions (click, pan, zoom)
- Test API integrations (geocoding, directions)

### Visual Regression Tests
- Compare before/after screenshots
- Ensure visual parity with Google Maps version

## Checklist: Migration Complete

- [ ] Map initializes correctly
- [ ] All markers/features display
- [ ] Click/hover interactions work
- [ ] Popups/info windows display
- [ ] Geocoding integrated
- [ ] Directions/routing working
- [ ] Custom styling applied
- [ ] Controls positioned correctly
- [ ] Mobile/touch gestures work
- [ ] Performance is acceptable
- [ ] Cross-browser tested
- [ ] API keys secured
- [ ] Error handling in place
- [ ] Analytics/monitoring updated
- [ ] Documentation updated
- [ ] Team trained on Mapbox

## When NOT to Migrate

Consider staying with Google Maps if:
- **Street View is critical** - Mapbox doesn't have equivalent
- **Tight Google Workspace integration** - Places API deeply integrated
- **Already heavily optimized** - Migration cost > benefits
- **Team expertise** - Retraining costs too high
- **Short-term project** - Not worth migration effort

## Additional Resources

- [Mapbox GL JS Documentation](https://docs.mapbox.com/mapbox-gl-js/)
- [Official Google Maps to Mapbox Migration Guide](https://docs.mapbox.com/help/tutorials/google-to-mapbox/)
- [Mapbox Examples](https://docs.mapbox.com/mapbox-gl-js/examples/)
- [Style Specification](https://docs.mapbox.com/mapbox-gl-js/style-spec/)

## Integration with Other Skills

**Works with:**
- **mapbox-web-integration-patterns**: Framework-specific migration guidance
- **mapbox-web-performance-patterns**: Optimize after migration
- **mapbox-token-security**: Secure your Mapbox tokens properly
- **mapbox-geospatial-operations**: Use Mapbox's geospatial tools effectively
- **mapbox-search-patterns**: Migrate geocoding/search functionality

## Quick Reference: Side-by-Side Comparison

```javascript
// GOOGLE MAPS
const map = new google.maps.Map(el, {
  center: { lat: 37.7749, lng: -122.4194 },
  zoom: 12
});

const marker = new google.maps.Marker({
  position: { lat: 37.7749, lng: -122.4194 },
  map: map
});

google.maps.event.addListener(map, 'click', (e) => {
  console.log(e.latLng.lat(), e.latLng.lng());
});

// MAPBOX GL JS
mapboxgl.accessToken = 'YOUR_TOKEN';
const map = new mapboxgl.Map({
  container: el,
  center: [-122.4194, 37.7749], // REVERSED!
  zoom: 12,
  style: 'mapbox://styles/mapbox/streets-v12'
});

const marker = new mapboxgl.Marker()
  .setLngLat([-122.4194, 37.7749]) // REVERSED!
  .addTo(map);

map.on('click', (e) => {
  console.log(e.lngLat.lat, e.lngLat.lng);
});
```

**Remember:** lng, lat order in Mapbox!
