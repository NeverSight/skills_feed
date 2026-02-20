---
name: mapbox-data-visualization-patterns
description: Patterns for visualizing data on maps including choropleth maps, heat maps, 3D visualizations, data-driven styling, and animated data. Covers layer types, color scales, and performance optimization.
---

# Data Visualization Patterns Skill

Comprehensive patterns for visualizing data on Mapbox maps. Covers choropleth maps, heat maps, 3D extrusions, data-driven styling, animated visualizations, and performance optimization for data-heavy applications.

## When to Use This Skill

Use this skill when:

- Visualizing statistical data on maps (population, sales, demographics)
- Creating choropleth maps with color-coded regions
- Building heat maps or clustering for density visualization
- Adding 3D visualizations (building heights, terrain elevation)
- Implementing data-driven styling based on properties
- Animating time-series data
- Working with large datasets that require optimization

## Visualization Types

### Choropleth Maps

**Best for:** Regional data (states, counties, zip codes), statistical comparisons

**Pattern:** Color-code polygons based on data values

```javascript
map.on('load', () => {
  // Add data source (GeoJSON with properties)
  map.addSource('states', {
    type: 'geojson',
    data: 'https://example.com/states.geojson' // Features with population property
  });

  // Add fill layer with data-driven color
  map.addLayer({
    id: 'states-layer',
    type: 'fill',
    source: 'states',
    paint: {
      'fill-color': [
        'interpolate',
        ['linear'],
        ['get', 'population'],
        0,
        '#f0f9ff', // Light blue for low population
        500000,
        '#7fcdff',
        1000000,
        '#0080ff',
        5000000,
        '#0040bf', // Dark blue for high population
        10000000,
        '#001f5c'
      ],
      'fill-opacity': 0.75
    }
  });

  // Add border layer
  map.addLayer({
    id: 'states-border',
    type: 'line',
    source: 'states',
    paint: {
      'line-color': '#ffffff',
      'line-width': 1
    }
  });

  // Add hover effect with reusable popup
  const popup = new mapboxgl.Popup({
    closeButton: false,
    closeOnClick: false
  });

  map.on('mousemove', 'states-layer', (e) => {
    if (e.features.length > 0) {
      map.getCanvas().style.cursor = 'pointer';

      const feature = e.features[0];
      popup
        .setLngLat(e.lngLat)
        .setHTML(
          `
          <h3>${feature.properties.name}</h3>
          <p>Population: ${feature.properties.population.toLocaleString()}</p>
        `
        )
        .addTo(map);
    }
  });

  map.on('mouseleave', 'states-layer', () => {
    map.getCanvas().style.cursor = '';
    popup.remove();
  });
});
```

**Color Scale Strategies:**

```javascript
// Linear interpolation (continuous scale)
'fill-color': [
  'interpolate',
  ['linear'],
  ['get', 'value'],
  0, '#ffffcc',
  25, '#78c679',
  50, '#31a354',
  100, '#006837'
]

// Step intervals (discrete buckets)
'fill-color': [
  'step',
  ['get', 'value'],
  '#ffffcc',  // Default color
  25, '#c7e9b4',
  50, '#7fcdbb',
  75, '#41b6c4',
  100, '#2c7fb8'
]

// Case-based (categorical data)
'fill-color': [
  'match',
  ['get', 'category'],
  'residential', '#ffd700',
  'commercial', '#ff6b6b',
  'industrial', '#4ecdc4',
  'park', '#45b7d1',
  '#cccccc'  // Default
]
```

### Heat Maps

**Best for:** Point density, event locations, incident clustering

**Pattern:** Visualize density of points

```javascript
map.on('load', () => {
  // Add data source (points)
  map.addSource('incidents', {
    type: 'geojson',
    data: {
      type: 'FeatureCollection',
      features: [
        {
          type: 'Feature',
          geometry: {
            type: 'Point',
            coordinates: [-122.4194, 37.7749]
          },
          properties: {
            intensity: 1
          }
        }
        // ... more points
      ]
    }
  });

  // Add heatmap layer
  map.addLayer({
    id: 'incidents-heat',
    type: 'heatmap',
    source: 'incidents',
    maxzoom: 15,
    paint: {
      // Increase weight based on intensity property
      'heatmap-weight': ['interpolate', ['linear'], ['get', 'intensity'], 0, 0, 6, 1],
      // Increase intensity as zoom level increases
      'heatmap-intensity': ['interpolate', ['linear'], ['zoom'], 0, 1, 15, 3],
      // Color ramp for heatmap
      'heatmap-color': [
        'interpolate',
        ['linear'],
        ['heatmap-density'],
        0,
        'rgba(33,102,172,0)',
        0.2,
        'rgb(103,169,207)',
        0.4,
        'rgb(209,229,240)',
        0.6,
        'rgb(253,219,199)',
        0.8,
        'rgb(239,138,98)',
        1,
        'rgb(178,24,43)'
      ],
      // Adjust radius by zoom level
      'heatmap-radius': ['interpolate', ['linear'], ['zoom'], 0, 2, 15, 20],
      // Decrease opacity at higher zoom levels
      'heatmap-opacity': ['interpolate', ['linear'], ['zoom'], 7, 1, 15, 0]
    }
  });

  // Add circle layer for individual points at high zoom
  map.addLayer({
    id: 'incidents-point',
    type: 'circle',
    source: 'incidents',
    minzoom: 14,
    paint: {
      'circle-radius': ['interpolate', ['linear'], ['zoom'], 14, 4, 22, 30],
      'circle-color': '#ff4444',
      'circle-opacity': 0.8,
      'circle-stroke-color': '#fff',
      'circle-stroke-width': 1
    }
  });
});
```

### Clustering (Point Density)

**Best for:** Grouping nearby points, aggregated counts, large point datasets

**Pattern:** Client-side clustering for visualization

Clustering is a valuable point density visualization technique alongside heat maps. Use clustering when you want **discrete grouping with exact counts** rather than a continuous density visualization.

```javascript
map.on('load', () => {
  // Add data source with clustering enabled
  map.addSource('locations', {
    type: 'geojson',
    data: {
      type: 'FeatureCollection',
      features: [
        // Your point features
      ]
    },
    cluster: true,
    clusterMaxZoom: 14, // Max zoom to cluster points
    clusterRadius: 50 // Radius of each cluster (default 50)
  });

  // Clustered circles - styled by point count
  map.addLayer({
    id: 'clusters',
    type: 'circle',
    source: 'locations',
    filter: ['has', 'point_count'],
    paint: {
      // Color clusters by count (step expression)
      'circle-color': ['step', ['get', 'point_count'], '#51bbd6', 10, '#f1f075', 30, '#f28cb1'],
      // Size clusters by count
      'circle-radius': ['step', ['get', 'point_count'], 20, 10, 30, 30, 40]
    }
  });

  // Cluster count labels
  map.addLayer({
    id: 'cluster-count',
    type: 'symbol',
    source: 'locations',
    filter: ['has', 'point_count'],
    layout: {
      'text-field': ['get', 'point_count_abbreviated'],
      'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
      'text-size': 12
    }
  });

  // Individual unclustered points
  map.addLayer({
    id: 'unclustered-point',
    type: 'circle',
    source: 'locations',
    filter: ['!', ['has', 'point_count']],
    paint: {
      'circle-color': '#11b4da',
      'circle-radius': 6,
      'circle-stroke-width': 1,
      'circle-stroke-color': '#fff'
    }
  });

  // Click handler to expand clusters
  map.on('click', 'clusters', (e) => {
    const features = map.queryRenderedFeatures(e.point, {
      layers: ['clusters']
    });
    const clusterId = features[0].properties.cluster_id;

    // Get cluster expansion zoom
    map.getSource('locations').getClusterExpansionZoom(clusterId, (err, zoom) => {
      if (err) return;

      map.easeTo({
        center: features[0].geometry.coordinates,
        zoom: zoom
      });
    });
  });

  // Change cursor on hover
  map.on('mouseenter', 'clusters', () => {
    map.getCanvas().style.cursor = 'pointer';
  });
  map.on('mouseleave', 'clusters', () => {
    map.getCanvas().style.cursor = '';
  });
});
```

**Advanced: Custom Cluster Properties**

```javascript
map.addSource('locations', {
  type: 'geojson',
  data: data,
  cluster: true,
  clusterMaxZoom: 14,
  clusterRadius: 50,
  // Calculate custom cluster properties
  clusterProperties: {
    // Sum total values
    sum: ['+', ['get', 'value']],
    // Calculate max value
    max: ['max', ['get', 'value']]
  }
});

// Use custom properties in styling
'circle-color': [
  'interpolate',
  ['linear'],
  ['get', 'sum'],
  0,
  '#51bbd6',
  100,
  '#f1f075',
  1000,
  '#f28cb1'
];
```

**When to use clustering vs heatmaps:**

| Use Case                         | Clustering                       | Heatmap                    |
| -------------------------------- | -------------------------------- | -------------------------- |
| **Visual style**                 | Discrete circles with counts     | Continuous gradient        |
| **Interaction**                  | Click to expand/zoom             | Visual density only        |
| **Data granularity**             | Exact counts visible             | Approximate density        |
| **Best for**                     | Store locators, event listings   | Crime maps, incident areas |
| **Performance with many points** | Excellent (groups automatically) | Good                       |
| **User understanding**           | Clear (numbered clusters)        | Intuitive (heat analogy)   |

### 3D Extrusions

**Best for:** Building heights, elevation data, volumetric representation

**Pattern:** Extrude polygons based on data

> **Note:** The example below works with **classic styles only** (`streets-v12`, `dark-v11`, `light-v11`, etc.). The **Mapbox Standard style** includes 3D buildings with much greater detail by default.

```javascript
map.on('load', () => {
  // Insert the layer beneath any symbol layer for proper ordering
  const layers = map.getStyle().layers;
  const labelLayerId = layers.find((layer) => layer.type === 'symbol' && layer.layout['text-field']).id;

  // Add 3D buildings from basemap
  map.addLayer(
    {
      id: 'add-3d-buildings',
      source: 'composite',
      'source-layer': 'building',
      filter: ['==', 'extrude', 'true'],
      type: 'fill-extrusion',
      minzoom: 15,
      paint: {
        'fill-extrusion-color': '#aaa',
        // Smoothly transition height on zoom
        'fill-extrusion-height': ['interpolate', ['linear'], ['zoom'], 15, 0, 15.05, ['get', 'height']],
        'fill-extrusion-base': ['interpolate', ['linear'], ['zoom'], 15, 0, 15.05, ['get', 'min_height']],
        'fill-extrusion-opacity': 0.6
      }
    },
    labelLayerId
  );

  // Enable pitch and bearing for 3D view
  map.setPitch(45);
  map.setBearing(-17.6);
});
```

**Using Custom Data Source:**

```javascript
map.on('load', () => {
  // Add your own buildings data
  map.addSource('custom-buildings', {
    type: 'geojson',
    data: 'https://example.com/buildings.geojson'
  });

  // Add 3D buildings layer
  map.addLayer({
    id: '3d-custom-buildings',
    type: 'fill-extrusion',
    source: 'custom-buildings',
    paint: {
      // Height in meters
      'fill-extrusion-height': ['get', 'height'],
      // Base height if building on terrain
      'fill-extrusion-base': ['get', 'base_height'],
      // Color by building type or height
      'fill-extrusion-color': [
        'interpolate',
        ['linear'],
        ['get', 'height'],
        0,
        '#fafa6e',
        50,
        '#eca25b',
        100,
        '#e64a45',
        200,
        '#a63e3e'
      ],
      'fill-extrusion-opacity': 0.9
    }
  });
});
```

**Data-Driven 3D Heights:**

```javascript
// Population density visualization
'fill-extrusion-height': [
  'interpolate',
  ['linear'],
  ['get', 'density'],
  0, 0,
  1000, 500,    // 1000 people/sq mi = 500m height
  10000, 5000
]

// Revenue visualization (scale for visibility)
'fill-extrusion-height': [
  '*',
  ['get', 'revenue'],
  0.001  // Scale factor
]
```

### Circle/Bubble Maps

**Best for:** Point data with magnitude, proportional symbols

**Pattern:** Size circles based on data values

```javascript
map.on('load', () => {
  map.addSource('earthquakes', {
    type: 'geojson',
    data: 'https://example.com/earthquakes.geojson'
  });

  // Size by magnitude, color by depth
  map.addLayer({
    id: 'earthquakes',
    type: 'circle',
    source: 'earthquakes',
    paint: {
      // Size circles by magnitude
      'circle-radius': ['interpolate', ['exponential', 2], ['get', 'mag'], 0, 2, 5, 20, 8, 100],
      // Color by depth
      'circle-color': [
        'interpolate',
        ['linear'],
        ['get', 'depth'],
        0,
        '#ffffcc',
        50,
        '#a1dab4',
        100,
        '#41b6c4',
        200,
        '#2c7fb8',
        300,
        '#253494'
      ],
      'circle-stroke-color': '#ffffff',
      'circle-stroke-width': 1,
      'circle-opacity': 0.75
    }
  });

  // Add popup on click
  map.on('click', 'earthquakes', (e) => {
    const props = e.features[0].properties;
    new mapboxgl.Popup()
      .setLngLat(e.features[0].geometry.coordinates)
      .setHTML(
        `
        <h3>Magnitude ${props.mag}</h3>
        <p>Depth: ${props.depth} km</p>
        <p>Time: ${new Date(props.time).toLocaleString()}</p>
      `
      )
      .addTo(map);
  });
});
```

### Line Data Visualization

**Best for:** Routes, flows, connections, networks

**Pattern:** Style lines based on data

```javascript
map.on('load', () => {
  map.addSource('traffic', {
    type: 'geojson',
    data: 'https://example.com/traffic.geojson'
  });

  // Traffic flow with data-driven styling
  map.addLayer({
    id: 'traffic-lines',
    type: 'line',
    source: 'traffic',
    paint: {
      // Width by traffic volume
      'line-width': ['interpolate', ['exponential', 2], ['get', 'volume'], 0, 1, 1000, 5, 10000, 15],
      // Color by speed (congestion)
      'line-color': [
        'interpolate',
        ['linear'],
        ['get', 'speed'],
        0,
        '#d73027', // Red: stopped
        15,
        '#fc8d59', // Orange: slow
        30,
        '#fee08b', // Yellow: moderate
        45,
        '#d9ef8b', // Light green: good
        60,
        '#91cf60', // Green: free flow
        75,
        '#1a9850'
      ],
      'line-opacity': 0.8
    }
  });
});
```

## Animated Data Visualizations

### Time-Series Animation

**Pattern:** Animate data over time

```javascript
let currentTime = 0;
const times = [0, 6, 12, 18, 24]; // Hours of day
let animationId;

map.on('load', () => {
  map.addSource('hourly-data', {
    type: 'geojson',
    data: getDataForTime(currentTime)
  });

  map.addLayer({
    id: 'data-layer',
    type: 'circle',
    source: 'hourly-data',
    paint: {
      'circle-radius': 8,
      'circle-color': ['get', 'color']
    }
  });

  // Animation loop
  function animate() {
    currentTime = (currentTime + 1) % times.length;

    // Update data
    map.getSource('hourly-data').setData(getDataForTime(times[currentTime]));

    // Update UI
    document.getElementById('time-display').textContent = `${times[currentTime]}:00`;

    animationId = setTimeout(animate, 1000); // Update every second
  }

  // Start animation
  document.getElementById('play-button').addEventListener('click', () => {
    if (animationId) {
      clearTimeout(animationId);
      animationId = null;
    } else {
      animate();
    }
  });
});

function getDataForTime(hour) {
  // Fetch or generate data for specific time
  return {
    type: 'FeatureCollection',
    features: data.filter((d) => d.properties.hour === hour)
  };
}
```

### Real-Time Data Updates

**Pattern:** Update data from live sources

```javascript
map.on('load', () => {
  map.addSource('live-data', {
    type: 'geojson',
    data: {
      type: 'FeatureCollection',
      features: []
    }
  });

  map.addLayer({
    id: 'live-points',
    type: 'circle',
    source: 'live-data',
    paint: {
      'circle-radius': 6,
      'circle-color': '#ff4444'
    }
  });

  // Poll for updates every 5 seconds
  setInterval(async () => {
    const response = await fetch('https://api.example.com/live-data');
    const data = await response.json();

    // Update source
    map.getSource('live-data').setData(data);
  }, 5000);

  // Or use WebSocket for real-time updates
  const ws = new WebSocket('wss://api.example.com/live');

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    map.getSource('live-data').setData(data);
  };
});
```

### Smooth Transitions

**Pattern:** Animate property changes

```javascript
// Smoothly transition circle sizes
function updateVisualization(newData) {
  map.getSource('data-source').setData(newData);

  // Animate circle radius
  const currentRadius = map.getPaintProperty('data-layer', 'circle-radius');
  const targetRadius = ['get', 'newSize'];

  // Use setPaintProperty with transition
  map.setPaintProperty('data-layer', 'circle-radius', targetRadius);

  // Or use expressions for smooth interpolation
  map.setPaintProperty('data-layer', 'circle-radius', ['interpolate', ['linear'], ['get', 'value'], 0, 2, 100, 20]);
}
```

## Performance Optimization

### Vector Tiles vs GeoJSON

**When to use each:**

| Data Size | Format                  | Reason                                  |
| --------- | ----------------------- | --------------------------------------- |
| < 1 MB    | GeoJSON                 | Simple, no processing needed            |
| 1-10 MB   | GeoJSON or Vector Tiles | Consider data update frequency          |
| > 10 MB   | Vector Tiles            | Better performance, progressive loading |

**Vector Tile Pattern:**

```javascript
map.addSource('large-dataset', {
  type: 'vector',
  tiles: ['https://example.com/tiles/{z}/{x}/{y}.mvt'],
  minzoom: 0,
  maxzoom: 14
});

map.addLayer({
  id: 'data-layer',
  type: 'fill',
  source: 'large-dataset',
  'source-layer': 'data-layer-name', // Layer name in the tileset
  paint: {
    'fill-color': ['get', 'color'],
    'fill-opacity': 0.7
  }
});
```

### Feature State for Dynamic Styling

**Pattern:** Update styling without modifying geometry

```javascript
map.on('load', () => {
  map.addSource('states', {
    type: 'geojson',
    data: statesData,
    generateId: true // Important for feature state
  });

  map.addLayer({
    id: 'states',
    type: 'fill',
    source: 'states',
    paint: {
      'fill-color': [
        'case',
        ['boolean', ['feature-state', 'hover'], false],
        '#ff0000', // Hover color
        '#3b9ddd' // Default color
      ]
    }
  });

  let hoveredStateId = null;

  // Update feature state on hover
  map.on('mousemove', 'states', (e) => {
    if (e.features.length > 0) {
      if (hoveredStateId !== null) {
        map.setFeatureState({ source: 'states', id: hoveredStateId }, { hover: false });
      }

      hoveredStateId = e.features[0].id;

      map.setFeatureState({ source: 'states', id: hoveredStateId }, { hover: true });
    }
  });

  map.on('mouseleave', 'states', () => {
    if (hoveredStateId !== null) {
      map.setFeatureState({ source: 'states', id: hoveredStateId }, { hover: false });
    }
    hoveredStateId = null;
  });
});
```

### Filtering Large Datasets

**Pattern:** Filter data client-side for performance

```javascript
map.on('load', () => {
  map.addSource('all-data', {
    type: 'geojson',
    data: largeDataset
  });

  map.addLayer({
    id: 'filtered-data',
    type: 'circle',
    source: 'all-data',
    filter: ['>=', ['get', 'value'], 50], // Only show values >= 50
    paint: {
      'circle-radius': 6,
      'circle-color': '#ff4444'
    }
  });

  // Update filter dynamically
  function updateFilter(minValue) {
    map.setFilter('filtered-data', ['>=', ['get', 'value'], minValue]);
  }

  // Slider for dynamic filtering
  document.getElementById('filter-slider').addEventListener('input', (e) => {
    updateFilter(parseFloat(e.target.value));
  });
});
```

### Progressive Loading

**Pattern:** Load data in chunks as needed

```javascript
// Helper to check if feature is in bounds
function isFeatureInBounds(feature, bounds) {
  const coords = feature.geometry.coordinates;

  // Handle different geometry types
  if (feature.geometry.type === 'Point') {
    return bounds.contains(coords);
  } else if (feature.geometry.type === 'LineString') {
    return coords.some((coord) => bounds.contains(coord));
  } else if (feature.geometry.type === 'Polygon') {
    return coords[0].some((coord) => bounds.contains(coord));
  }
  return false;
}

const bounds = map.getBounds();
const visibleData = allData.features.filter((feature) => isFeatureInBounds(feature, bounds));

map.getSource('data-source').setData({
  type: 'FeatureCollection',
  features: visibleData
});

// Reload on map move with debouncing
let updateTimeout;
map.on('moveend', () => {
  clearTimeout(updateTimeout);
  updateTimeout = setTimeout(() => {
    const bounds = map.getBounds();
    const visibleData = allData.features.filter((feature) => isFeatureInBounds(feature, bounds));

    map.getSource('data-source').setData({
      type: 'FeatureCollection',
      features: visibleData
    });
  }, 150);
});
```

## Legends and UI Controls

### Color Scale Legend

```html
<div class="legend">
  <h4>Population Density</h4>
  <div class="legend-scale">
    <div class="legend-item">
      <span class="legend-color" style="background: #f0f9ff;"></span>
      <span>0-500</span>
    </div>
    <div class="legend-item">
      <span class="legend-color" style="background: #7fcdff;"></span>
      <span>500-1000</span>
    </div>
    <div class="legend-item">
      <span class="legend-color" style="background: #0080ff;"></span>
      <span>1000-5000</span>
    </div>
    <div class="legend-item">
      <span class="legend-color" style="background: #001f5c;"></span>
      <span>5000+</span>
    </div>
  </div>
</div>

<style>
  .legend {
    position: absolute;
    bottom: 30px;
    right: 10px;
    background: white;
    padding: 10px;
    border-radius: 3px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    font-family: Arial, sans-serif;
    font-size: 12px;
  }

  .legend h4 {
    margin: 0 0 10px 0;
    font-size: 14px;
  }

  .legend-item {
    display: flex;
    align-items: center;
    margin-bottom: 5px;
  }

  .legend-color {
    width: 20px;
    height: 20px;
    margin-right: 10px;
    border: 1px solid #ccc;
  }
</style>
```

### Interactive Data Inspector

```javascript
map.on('click', 'data-layer', (e) => {
  const feature = e.features[0];
  const properties = feature.properties;

  // Build properties table
  const propsTable = Object.entries(properties)
    .map(([key, value]) => `<tr><td><strong>${key}:</strong></td><td>${value}</td></tr>`)
    .join('');

  new mapboxgl.Popup()
    .setLngLat(e.lngLat)
    .setHTML(
      `
      <div style="max-width: 300px;">
        <h3>Feature Details</h3>
        <table style="width: 100%; font-size: 12px;">
          ${propsTable}
        </table>
      </div>
    `
    )
    .addTo(map);
});
```

## Best Practices

### Color Accessibility

```javascript
// Use ColorBrewer scales for accessibility
// https://colorbrewer2.org/

// Good: Sequential (single hue)
const sequentialScale = ['#f0f9ff', '#bae4ff', '#7fcdff', '#0080ff', '#001f5c'];

// Good: Diverging (two hues)
const divergingScale = ['#d73027', '#fc8d59', '#fee08b', '#d9ef8b', '#91cf60', '#1a9850'];

// Good: Qualitative (distinct categories)
const qualitativeScale = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00'];

// Avoid: Red-green for color-blind accessibility
// Use: Blue-orange or purple-green instead
```

### Data Preprocessing

```javascript
// Calculate statistical breaks for choropleth
// Using classybrew library (npm install classybrew)
import classybrew from 'classybrew';

function calculateJenksBreaks(values, numClasses) {
  const brew = new classybrew();
  brew.setSeries(values);
  brew.setNumClasses(numClasses);
  brew.classify('jenks');
  return brew.getBreaks();
}

// Normalize data for better visualization
function normalizeData(features, property) {
  const values = features.map((f) => f.properties[property]);
  const max = Math.max(...values);
  const min = Math.min(...values);
  const range = max - min;

  // Handle case where all values are the same
  if (range === 0) {
    return features.map((feature) => ({
      ...feature,
      properties: {
        ...feature.properties,
        normalized: 0.5
      }
    }));
  }

  return features.map((feature) => ({
    ...feature,
    properties: {
      ...feature.properties,
      normalized: (feature.properties[property] - min) / range
    }
  }));
}
```

### Error Handling

```javascript
// Handle missing or invalid data
map.on('load', () => {
  map.addSource('data', {
    type: 'geojson',
    data: dataUrl
  });

  map.addLayer({
    id: 'data-viz',
    type: 'fill',
    source: 'data',
    paint: {
      'fill-color': [
        'case',
        ['has', 'value'], // Check if property exists
        ['interpolate', ['linear'], ['get', 'value'], 0, '#f0f0f0', 100, '#0080ff'],
        '#cccccc' // Default color for missing data
      ]
    }
  });

  // Handle source errors
  map.on('error', (e) => {
    if (e.source === 'data') {
      console.error('Failed to load data:', e);
      showNotification('Unable to load visualization data');
    }
  });
});
```

## Common Use Cases

### Election Results Map

```javascript
map.addLayer({
  id: 'election-results',
  type: 'fill',
  source: 'districts',
  paint: {
    'fill-color': [
      'match',
      ['get', 'winner'],
      'democrat',
      '#3b82f6',
      'republican',
      '#ef4444',
      'independent',
      '#a855f7',
      '#94a3b8' // No data
    ],
    'fill-opacity': [
      'interpolate',
      ['linear'],
      ['get', 'margin'],
      0,
      0.3, // Close race: light
      20,
      0.9 // Landslide: dark
    ]
  }
});
```

### COVID-19 Case Map

```javascript
map.addLayer({
  id: 'covid-cases',
  type: 'fill',
  source: 'counties',
  paint: {
    'fill-color': [
      'step',
      ['/', ['get', 'cases'], ['get', 'population']], // Cases per capita
      '#ffffb2',
      0.001,
      '#fed976',
      0.005,
      '#feb24c',
      0.01,
      '#fd8d3c',
      0.02,
      '#fc4e2a',
      0.05,
      '#e31a1c',
      0.1,
      '#b10026'
    ]
  }
});
```

### Real Estate Price Heatmap

```javascript
map.addLayer({
  id: 'real-estate',
  type: 'circle',
  source: 'properties',
  paint: {
    'circle-radius': ['interpolate', ['exponential', 2], ['get', 'price'], 100000, 5, 1000000, 20, 10000000, 50],
    'circle-color': [
      'interpolate',
      ['linear'],
      ['get', 'price_per_sqft'],
      0,
      '#ffffcc',
      200,
      '#a1dab4',
      400,
      '#41b6c4',
      600,
      '#2c7fb8',
      800,
      '#253494'
    ],
    'circle-opacity': 0.6,
    'circle-stroke-color': '#ffffff',
    'circle-stroke-width': 1
  }
});
```

## Resources

- [Mapbox Expression Reference](https://docs.mapbox.com/style-spec/reference/expressions/)
- [ColorBrewer](https://colorbrewer2.org/) - Color scales for maps
- [Turf.js](https://turfjs.org/) - Spatial analysis
- [Simple Statistics](https://simplestatistics.org/) - Data classification
- [Data Visualization Tutorials](https://docs.mapbox.com/help/tutorials/#data-visualization)
