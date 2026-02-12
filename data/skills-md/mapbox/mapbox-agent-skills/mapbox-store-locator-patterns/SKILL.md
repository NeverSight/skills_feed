---
name: mapbox-store-locator-patterns
description: Common patterns for building store locators, restaurant finders, and location-based search applications with Mapbox. Covers marker display, filtering, distance calculation, and interactive lists.
---

# Store Locator Patterns Skill

Comprehensive patterns for building store locators, restaurant finders, and location-based search applications with Mapbox GL JS. Covers marker display, filtering, distance calculation, interactive lists, and directions integration.

## When to Use This Skill

Use this skill when building applications that:

- Display multiple locations on a map (stores, restaurants, offices, etc.)
- Allow users to filter or search locations
- Calculate distances from user location
- Provide interactive lists synced with map markers
- Show location details in popups or side panels
- Integrate directions to selected locations

## Dependencies

**Required:**

- Mapbox GL JS v3.x
- [@turf/turf](https://turfjs.org/) - For spatial calculations (distance, area, etc.)

**Installation:**

```bash
npm install mapbox-gl @turf/turf
```

## Core Architecture

### Pattern Overview

A typical store locator consists of:

1. **Map Display** - Shows all locations as markers
2. **Location Data** - GeoJSON with store/location information
3. **Interactive List** - Side panel listing all locations
4. **Filtering** - Search, category filters, distance filters
5. **Detail View** - Popup or panel with location details
6. **User Location** - Geolocation for distance calculation
7. **Directions** - Route to selected location (optional)

### Data Structure

**GeoJSON format for locations:**

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [-77.034084, 38.909671]
      },
      "properties": {
        "id": "store-001",
        "name": "Downtown Store",
        "address": "123 Main St, Washington, DC 20001",
        "phone": "(202) 555-0123",
        "hours": "Mon-Sat: 9am-9pm, Sun: 10am-6pm",
        "category": "retail",
        "website": "https://example.com/downtown"
      }
    }
  ]
}
```

**Key properties:**

- `id` - Unique identifier for each location
- `name` - Display name
- `address` - Full address for display and geocoding
- `coordinates` - `[longitude, latitude]` format
- `category` - For filtering (retail, restaurant, office, etc.)
- Custom properties as needed (hours, phone, website, etc.)

## Basic Store Locator Implementation

### Step 1: Initialize Map and Data

```javascript
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';

mapboxgl.accessToken = 'YOUR_MAPBOX_ACCESS_TOKEN';

// Store locations data
const stores = {
  type: 'FeatureCollection',
  features: [
    {
      type: 'Feature',
      geometry: {
        type: 'Point',
        coordinates: [-77.034084, 38.909671]
      },
      properties: {
        id: 'store-001',
        name: 'Downtown Store',
        address: '123 Main St, Washington, DC 20001',
        phone: '(202) 555-0123',
        category: 'retail'
      }
    }
    // ... more stores
  ]
};

const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/standard',
  center: [-77.034084, 38.909671],
  zoom: 11
});
```

### Step 2: Add Markers to Map

**Option 1: HTML Markers (< 100 locations)**

```javascript
const markers = {};

stores.features.forEach((store) => {
  // Create marker element
  const el = document.createElement('div');
  el.className = 'marker';
  el.style.backgroundImage = 'url(/marker-icon.png)';
  el.style.width = '30px';
  el.style.height = '40px';
  el.style.backgroundSize = 'cover';
  el.style.cursor = 'pointer';

  // Create marker
  const marker = new mapboxgl.Marker(el)
    .setLngLat(store.geometry.coordinates)
    .setPopup(
      new mapboxgl.Popup({ offset: 25 }).setHTML(
        `<h3>${store.properties.name}</h3>
         <p>${store.properties.address}</p>
         <p>${store.properties.phone}</p>`
      )
    )
    .addTo(map);

  // Store reference for later access
  markers[store.properties.id] = marker;

  // Handle marker click
  el.addEventListener('click', () => {
    flyToStore(store);
    createPopup(store);
    highlightListing(store.properties.id);
  });
});
```

**Option 2: Symbol Layer (100-1000 locations)**

```javascript
map.on('load', () => {
  // Add store data as source
  map.addSource('stores', {
    type: 'geojson',
    data: stores
  });

  // Add custom marker image
  map.loadImage('/marker-icon.png', (error, image) => {
    if (error) throw error;
    map.addImage('custom-marker', image);

    // Add symbol layer
    map.addLayer({
      id: 'stores-layer',
      type: 'symbol',
      source: 'stores',
      layout: {
        'icon-image': 'custom-marker',
        'icon-size': 0.8,
        'icon-allow-overlap': true,
        'text-field': ['get', 'name'],
        'text-font': ['Open Sans Bold', 'Arial Unicode MS Bold'],
        'text-offset': [0, 1.5],
        'text-anchor': 'top',
        'text-size': 12
      }
    });
  });

  // Handle marker clicks using Interactions API (recommended)
  map.addInteraction('store-click', {
    type: 'click',
    target: { layerId: 'stores-layer' },
    handler: (e) => {
      const store = e.feature;
      flyToStore(store);
      createPopup(store);
    }
  });

  // Or using traditional event listener:
  // map.on('click', 'stores-layer', (e) => {
  //   const store = e.features[0];
  //   flyToStore(store);
  //   createPopup(store);
  // });

  // Change cursor on hover
  map.on('mouseenter', 'stores-layer', () => {
    map.getCanvas().style.cursor = 'pointer';
  });

  map.on('mouseleave', 'stores-layer', () => {
    map.getCanvas().style.cursor = '';
  });
});
```

**Option 3: Clustering (> 1000 locations)**

```javascript
map.on('load', () => {
  map.addSource('stores', {
    type: 'geojson',
    data: stores,
    cluster: true,
    clusterMaxZoom: 14,
    clusterRadius: 50
  });

  // Cluster circles
  map.addLayer({
    id: 'clusters',
    type: 'circle',
    source: 'stores',
    filter: ['has', 'point_count'],
    paint: {
      'circle-color': ['step', ['get', 'point_count'], '#51bbd6', 10, '#f1f075', 30, '#f28cb1'],
      'circle-radius': ['step', ['get', 'point_count'], 20, 10, 30, 30, 40]
    }
  });

  // Cluster count labels
  map.addLayer({
    id: 'cluster-count',
    type: 'symbol',
    source: 'stores',
    filter: ['has', 'point_count'],
    layout: {
      'text-field': '{point_count_abbreviated}',
      'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
      'text-size': 12
    }
  });

  // Unclustered points
  map.addLayer({
    id: 'unclustered-point',
    type: 'circle',
    source: 'stores',
    filter: ['!', ['has', 'point_count']],
    paint: {
      'circle-color': '#11b4da',
      'circle-radius': 8,
      'circle-stroke-width': 1,
      'circle-stroke-color': '#fff'
    }
  });

  // Zoom on cluster click
  map.on('click', 'clusters', (e) => {
    const features = map.queryRenderedFeatures(e.point, {
      layers: ['clusters']
    });
    const clusterId = features[0].properties.cluster_id;
    map.getSource('stores').getClusterExpansionZoom(clusterId, (err, zoom) => {
      if (err) return;

      map.easeTo({
        center: features[0].geometry.coordinates,
        zoom: zoom
      });
    });
  });

  // Show popup on unclustered point click
  map.on('click', 'unclustered-point', (e) => {
    const coordinates = e.features[0].geometry.coordinates.slice();
    const props = e.features[0].properties;

    new mapboxgl.Popup()
      .setLngLat(coordinates)
      .setHTML(
        `<h3>${props.name}</h3>
         <p>${props.address}</p>`
      )
      .addTo(map);
  });
});
```

### Step 3: Build Interactive Location List

```javascript
function buildLocationList(stores) {
  const listingContainer = document.getElementById('listings');

  stores.features.forEach((store, index) => {
    const listing = listingContainer.appendChild(document.createElement('div'));
    listing.id = `listing-${store.properties.id}`;
    listing.className = 'listing';

    const link = listing.appendChild(document.createElement('a'));
    link.href = '#';
    link.className = 'title';
    link.id = `link-${store.properties.id}`;
    link.innerHTML = store.properties.name;

    const details = listing.appendChild(document.createElement('div'));
    details.innerHTML = `
      <p>${store.properties.address}</p>
      <p>${store.properties.phone || ''}</p>
    `;

    // Handle listing click
    link.addEventListener('click', (e) => {
      e.preventDefault();
      flyToStore(store);
      createPopup(store);
      highlightListing(store.properties.id);
    });
  });
}

function flyToStore(store) {
  map.flyTo({
    center: store.geometry.coordinates,
    zoom: 15,
    duration: 1000
  });
}

function createPopup(store) {
  const popups = document.getElementsByClassName('mapboxgl-popup');
  // Remove existing popups
  if (popups[0]) popups[0].remove();

  new mapboxgl.Popup({ closeOnClick: true })
    .setLngLat(store.geometry.coordinates)
    .setHTML(
      `<h3>${store.properties.name}</h3>
       <p>${store.properties.address}</p>
       <p>${store.properties.phone}</p>
       ${store.properties.website ? `<a href="${store.properties.website}" target="_blank">Visit Website</a>` : ''}`
    )
    .addTo(map);
}

function highlightListing(id) {
  // Remove existing highlights
  const activeItem = document.getElementsByClassName('active');
  if (activeItem[0]) {
    activeItem[0].classList.remove('active');
  }

  // Add highlight to selected listing
  const listing = document.getElementById(`listing-${id}`);
  listing.classList.add('active');

  // Scroll to listing
  listing.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Build the list on load
map.on('load', () => {
  buildLocationList(stores);
});
```

### Step 4: Add Search/Filter Functionality

**Text Search:**

```javascript
function filterStores(searchTerm) {
  const filtered = {
    type: 'FeatureCollection',
    features: stores.features.filter((store) => {
      const name = store.properties.name.toLowerCase();
      const address = store.properties.address.toLowerCase();
      const search = searchTerm.toLowerCase();

      return name.includes(search) || address.includes(search);
    })
  };

  // Update map source
  if (map.getSource('stores')) {
    map.getSource('stores').setData(filtered);
  }

  // Rebuild listing
  document.getElementById('listings').innerHTML = '';
  buildLocationList(filtered);

  // Fit map to filtered results
  if (filtered.features.length > 0) {
    const bounds = new mapboxgl.LngLatBounds();
    filtered.features.forEach((feature) => {
      bounds.extend(feature.geometry.coordinates);
    });
    map.fitBounds(bounds, { padding: 50 });
  }
}

// Add search input handler
document.getElementById('search-input').addEventListener('input', (e) => {
  filterStores(e.target.value);
});
```

**Category Filter:**

```javascript
function filterByCategory(category) {
  const filtered =
    category === 'all'
      ? stores
      : {
          type: 'FeatureCollection',
          features: stores.features.filter((store) => store.properties.category === category)
        };

  // Update map and list
  if (map.getSource('stores')) {
    map.getSource('stores').setData(filtered);
  }

  document.getElementById('listings').innerHTML = '';
  buildLocationList(filtered);
}

// Category dropdown
document.getElementById('category-select').addEventListener('change', (e) => {
  filterByCategory(e.target.value);
});
```

### Step 5: Add Geolocation and Distance Calculation

```javascript
let userLocation = null;

// Add geolocation control
map.addControl(
  new mapboxgl.GeolocateControl({
    positionOptions: {
      enableHighAccuracy: true
    },
    trackUserLocation: true,
    showUserHeading: true
  })
);

// Get user location
navigator.geolocation.getCurrentPosition(
  (position) => {
    userLocation = [position.coords.longitude, position.coords.latitude];

    // Calculate distances and sort
    const storesWithDistance = stores.features.map((store) => {
      const distance = calculateDistance(userLocation, store.geometry.coordinates);
      return {
        ...store,
        properties: {
          ...store.properties,
          distance: distance
        }
      };
    });

    // Sort by distance
    storesWithDistance.sort((a, b) => a.properties.distance - b.properties.distance);

    // Update data
    stores.features = storesWithDistance;

    // Rebuild list with distances
    document.getElementById('listings').innerHTML = '';
    buildLocationList(stores);
  },
  (error) => {
    console.error('Error getting location:', error);
  }
);

// Calculate distance using Turf.js (recommended)
import * as turf from '@turf/turf';

function calculateDistance(from, to) {
  const fromPoint = turf.point(from);
  const toPoint = turf.point(to);
  const distance = turf.distance(fromPoint, toPoint, { units: 'miles' });
  return distance.toFixed(1); // Distance in miles
}

// Update listing to show distance
function buildLocationList(stores) {
  const listingContainer = document.getElementById('listings');

  stores.features.forEach((store) => {
    const listing = listingContainer.appendChild(document.createElement('div'));
    listing.id = `listing-${store.properties.id}`;
    listing.className = 'listing';

    const link = listing.appendChild(document.createElement('a'));
    link.href = '#';
    link.className = 'title';
    link.innerHTML = store.properties.name;

    const details = listing.appendChild(document.createElement('div'));
    details.innerHTML = `
      ${store.properties.distance ? `<p class="distance">${store.properties.distance} mi</p>` : ''}
      <p>${store.properties.address}</p>
      <p>${store.properties.phone || ''}</p>
    `;

    link.addEventListener('click', (e) => {
      e.preventDefault();
      flyToStore(store);
      createPopup(store);
      highlightListing(store.properties.id);
    });
  });
}
```

### Step 6: Integrate Directions (Optional)

```javascript
async function getDirections(from, to) {
  const query = await fetch(
    `https://api.mapbox.com/directions/v5/mapbox/driving/${from[0]},${from[1]};${to[0]},${to[1]}?` +
      `steps=true&geometries=geojson&access_token=${mapboxgl.accessToken}`
  );

  const data = await query.json();
  const route = data.routes[0];

  // Display route on map
  if (map.getSource('route')) {
    map.getSource('route').setData({
      type: 'Feature',
      geometry: route.geometry
    });
  } else {
    map.addSource('route', {
      type: 'geojson',
      data: {
        type: 'Feature',
        geometry: route.geometry
      }
    });

    map.addLayer({
      id: 'route',
      type: 'line',
      source: 'route',
      paint: {
        'line-color': '#3b9ddd',
        'line-width': 5,
        'line-opacity': 0.75
      }
    });
  }

  // Display directions info
  const duration = Math.floor(route.duration / 60);
  const distance = (route.distance * 0.000621371).toFixed(1); // Convert to miles

  return { duration, distance, steps: route.legs[0].steps };
}

// Add "Get Directions" button to popup
function createPopup(store) {
  const popups = document.getElementsByClassName('mapboxgl-popup');
  if (popups[0]) popups[0].remove();

  const popup = new mapboxgl.Popup({ closeOnClick: true })
    .setLngLat(store.geometry.coordinates)
    .setHTML(
      `<h3>${store.properties.name}</h3>
       <p>${store.properties.address}</p>
       <p>${store.properties.phone}</p>
       ${userLocation ? '<button id="get-directions">Get Directions</button>' : ''}`
    )
    .addTo(map);

  // Handle directions button
  if (userLocation) {
    document.getElementById('get-directions').addEventListener('click', async () => {
      const directions = await getDirections(userLocation, store.geometry.coordinates);

      // Update popup with directions
      popup.setHTML(
        `<h3>${store.properties.name}</h3>
         <p><strong>${directions.distance} mi • ${directions.duration} min</strong></p>
         <p>${store.properties.address}</p>
         <div class="directions-steps">
           ${directions.steps.map((step) => `<p>${step.maneuver.instruction}</p>`).join('')}
         </div>`
      );
    });
  }
}
```

## Styling Patterns

### Layout Structure

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Store Locator</title>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link href="https://api.mapbox.com/mapbox-gl-js/v3.0.0/mapbox-gl.css" rel="stylesheet" />
    <style>
      body {
        margin: 0;
        padding: 0;
        font-family: 'Arial', sans-serif;
      }

      #app {
        display: flex;
        height: 100vh;
      }

      /* Sidebar */
      .sidebar {
        width: 400px;
        height: 100vh;
        overflow-y: scroll;
        background-color: #fff;
        border-right: 1px solid #ddd;
      }

      .sidebar-header {
        padding: 20px;
        background-color: #f8f9fa;
        border-bottom: 1px solid #ddd;
      }

      .sidebar-header h1 {
        margin: 0 0 10px 0;
        font-size: 24px;
      }

      /* Search */
      .search-box {
        width: 100%;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 4px;
        font-size: 14px;
        box-sizing: border-box;
      }

      .filter-group {
        margin-top: 10px;
      }

      .filter-group select {
        width: 100%;
        padding: 8px;
        border: 1px solid #ddd;
        border-radius: 4px;
        font-size: 14px;
      }

      /* Listings */
      #listings {
        padding: 0;
      }

      .listing {
        padding: 15px 20px;
        border-bottom: 1px solid #eee;
        cursor: pointer;
        transition: background-color 0.2s;
      }

      .listing:hover {
        background-color: #f8f9fa;
      }

      .listing.active {
        background-color: #e3f2fd;
        border-left: 3px solid #2196f3;
      }

      .listing .title {
        display: block;
        color: #333;
        font-weight: bold;
        font-size: 16px;
        text-decoration: none;
        margin-bottom: 5px;
      }

      .listing .title:hover {
        color: #2196f3;
      }

      .listing p {
        margin: 5px 0;
        font-size: 14px;
        color: #666;
      }

      .listing .distance {
        color: #2196f3;
        font-weight: bold;
      }

      /* Map */
      #map {
        flex: 1;
        height: 100vh;
      }

      /* Popups */
      .mapboxgl-popup-content {
        padding: 15px;
        font-family: 'Arial', sans-serif;
      }

      .mapboxgl-popup-content h3 {
        margin: 0 0 10px 0;
        font-size: 18px;
      }

      .mapboxgl-popup-content p {
        margin: 5px 0;
        font-size: 14px;
      }

      .mapboxgl-popup-content button {
        margin-top: 10px;
        padding: 8px 16px;
        background-color: #2196f3;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 14px;
      }

      .mapboxgl-popup-content button:hover {
        background-color: #1976d2;
      }

      /* Responsive */
      @media (max-width: 768px) {
        #app {
          flex-direction: column;
        }

        .sidebar {
          width: 100%;
          height: 50vh;
        }

        #map {
          height: 50vh;
        }
      }
    </style>
  </head>
  <body>
    <div id="app">
      <div class="sidebar">
        <div class="sidebar-header">
          <h1>Store Locator</h1>
          <input type="text" id="search-input" class="search-box" placeholder="Search by name or address..." />
          <div class="filter-group">
            <select id="category-select">
              <option value="all">All Categories</option>
              <option value="retail">Retail</option>
              <option value="restaurant">Restaurant</option>
              <option value="office">Office</option>
            </select>
          </div>
        </div>
        <div id="listings"></div>
      </div>
      <div id="map"></div>
    </div>

    <script src="https://api.mapbox.com/mapbox-gl-js/v3.0.0/mapbox-gl.js"></script>
    <script src="app.js"></script>
  </body>
</html>
```

### Custom Marker Styling

```css
/* Custom marker styles */
.marker {
  background-size: cover;
  width: 30px;
  height: 40px;
  cursor: pointer;
  transition: transform 0.2s;
}

.marker:hover {
  transform: scale(1.1);
}

/* Category-specific marker colors */
.marker.retail {
  background-color: #2196f3;
}

.marker.restaurant {
  background-color: #f44336;
}

.marker.office {
  background-color: #4caf50;
}
```

## Performance Optimization

### Debounced Search

```javascript
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

const debouncedFilter = debounce(filterStores, 300);

document.getElementById('search-input').addEventListener('input', (e) => {
  debouncedFilter(e.target.value);
});
```

## Best Practices

### Data Management

```javascript
// ✅ GOOD: Load data once, filter in memory
const allStores = await fetch('/api/stores').then((r) => r.json());

function filterStores(criteria) {
  return {
    type: 'FeatureCollection',
    features: allStores.features.filter(criteria)
  };
}

// ❌ BAD: Fetch on every filter
async function filterStores(criteria) {
  return await fetch(`/api/stores?filter=${criteria}`).then((r) => r.json());
}
```

### Error Handling

```javascript
// Geolocation error handling
navigator.geolocation.getCurrentPosition(
  successCallback,
  (error) => {
    let message = 'Unable to get your location.';

    switch (error.code) {
      case error.PERMISSION_DENIED:
        message = 'Please enable location access to see nearby stores.';
        break;
      case error.POSITION_UNAVAILABLE:
        message = 'Location information is unavailable.';
        break;
      case error.TIMEOUT:
        message = 'Location request timed out.';
        break;
    }

    showNotification(message);
  },
  {
    enableHighAccuracy: true,
    timeout: 5000,
    maximumAge: 0
  }
);

// API error handling
async function loadStores() {
  try {
    const response = await fetch('/api/stores');

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Failed to load stores:', error);
    showNotification('Unable to load store locations. Please try again.');
    return { type: 'FeatureCollection', features: [] };
  }
}
```

### Accessibility

```javascript
// Add ARIA labels
document.getElementById('search-input').setAttribute('aria-label', 'Search stores');

// Keyboard navigation
document.querySelectorAll('.listing').forEach((listing, index) => {
  listing.setAttribute('tabindex', '0');
  listing.setAttribute('role', 'button');
  listing.setAttribute('aria-label', `View ${listing.querySelector('.title').textContent}`);

  listing.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      listing.click();
    }
  });
});

// Focus management
function highlightListing(id) {
  const listing = document.getElementById(`listing-${id}`);
  listing.classList.add('active');
  listing.focus();
  listing.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}
```

## Common Variations

### Mobile-First Layout

```css
/* Mobile first: stack sidebar on top */
@media (max-width: 768px) {
  #app {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    height: 40vh;
    max-height: 40vh;
  }

  #map {
    height: 60vh;
  }

  /* Toggle sidebar */
  .sidebar.collapsed {
    height: 60px;
  }
}
```

### Fullscreen Map with Overlay

```javascript
// Map takes full screen, list appears as overlay
const listOverlay = document.createElement('div');
listOverlay.className = 'list-overlay';
listOverlay.innerHTML = `
  <button id="toggle-list">View All Locations (${stores.features.length})</button>
  <div id="listings" class="hidden"></div>
`;

document.getElementById('toggle-list').addEventListener('click', () => {
  document.getElementById('listings').classList.toggle('hidden');
});
```

### Map-Only View

```javascript
// No sidebar, everything in popups
function createDetailedPopup(store) {
  const popup = new mapboxgl.Popup({ maxWidth: '400px' })
    .setLngLat(store.geometry.coordinates)
    .setHTML(
      `
      <div class="store-popup">
        <h3>${store.properties.name}</h3>
        <p class="address">${store.properties.address}</p>
        <p class="phone">${store.properties.phone}</p>
        <p class="hours">${store.properties.hours}</p>
        ${store.properties.distance ? `<p class="distance">${store.properties.distance} mi away</p>` : ''}
        <div class="actions">
          <button onclick="getDirections('${store.properties.id}')">Directions</button>
          <button onclick="callStore('${store.properties.phone}')">Call</button>
          ${store.properties.website ? `<a href="${store.properties.website}" target="_blank">Website</a>` : ''}
        </div>
      </div>
    `
    )
    .addTo(map);
}
```

## Framework Integration

### React Implementation

```jsx
import { useEffect, useRef, useState } from 'react';
import mapboxgl from 'mapbox-gl';

function StoreLocator({ stores }) {
  const mapContainer = useRef(null);
  const map = useRef(null);
  const [selectedStore, setSelectedStore] = useState(null);
  const [filteredStores, setFilteredStores] = useState(stores);

  useEffect(() => {
    if (map.current) return;

    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: 'mapbox://styles/mapbox/standard',
      center: [-77.034084, 38.909671],
      zoom: 11
    });

    map.current.on('load', () => {
      map.current.addSource('stores', {
        type: 'geojson',
        data: filteredStores
      });

      map.current.addLayer({
        id: 'stores',
        type: 'circle',
        source: 'stores',
        paint: {
          'circle-color': '#2196f3',
          'circle-radius': 8
        }
      });

      map.current.on('click', 'stores', (e) => {
        setSelectedStore(e.features[0]);
      });
    });

    return () => map.current.remove();
  }, []);

  // Update source when filtered stores change
  useEffect(() => {
    if (map.current && map.current.getSource('stores')) {
      map.current.getSource('stores').setData(filteredStores);
    }
  }, [filteredStores]);

  return (
    <div className="store-locator">
      <Sidebar
        stores={filteredStores}
        selectedStore={selectedStore}
        onStoreClick={setSelectedStore}
        onFilter={setFilteredStores}
      />
      <div ref={mapContainer} className="map-container" />
    </div>
  );
}
```

## Resources

- [Turf.js](https://turfjs.org/) - Spatial analysis library (recommended for distance calculations)
- [Mapbox GL JS API](https://docs.mapbox.com/mapbox-gl-js/)
- [Interactions API Guide](https://docs.mapbox.com/mapbox-gl-js/guides/user-interactions/interactions/)
- [GeoJSON Specification](https://geojson.org/)
- [Directions API](https://docs.mapbox.com/api/navigation/directions/)
- [Store Locator Tutorial](https://docs.mapbox.com/help/tutorials/building-a-store-locator/)
