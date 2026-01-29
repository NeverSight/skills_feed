---
name: map-generator
description: This skill generates interactive maps using the Leaflet JavaScript library. Use this skill when users need to create geographic visualizations, location-based data displays, or interactive maps for educational textbooks. The skill creates complete MicroSim packages with HTML, CSS, and documentation, optimized for iframe embedding in narrow MkDocs pages with navbar and TOC.
---

# Map Generator Skill

This skill creates interactive Leaflet maps as MicroSims for intelligent textbooks built with MkDocs Material theme.

## When to Use This Skill

Use this skill when users request:

- Geographic visualizations (regions, countries, cities)
- Location-based data displays (historical sites, landmarks)
- Campus or facility maps
- Travel route visualizations
- Custom maps with markers, layers, or highlighted borders
- Educational geography content

## Workflow

### Step 1: Gather Map Requirements

Ask the user for the following information:

1. **Map Purpose**: What geographic data are we visualizing?
2. **Geographic Region**: Region name, country, city, or coordinates
3. **Markers/Points**: What locations need markers? (names, coordinates, descriptions)
4. **Map Layers**: Do you need multiple layers (satellite, terrain, street map)?
5. **Borders/Regions**: Do any borders or regions need to be highlighted?
6. **Zoom Level**: Initial zoom level (1-18, where 1 is world view, 18 is building level)
7. **Interactive Features**: Popups, custom markers, layer controls?
8. **Educational Context**: Related concepts, Bloom's taxonomy level, target audience

**Example user input**: "Create a map showing major universities in California with markers for each campus"

### Step 2: Create Directory Structure

Create the MicroSim directory:

```
docs/sims/[map-name]/
```

**Naming convention**: Use kebab-case (e.g., `california-universities`, `ancient-rome-map`, `world-capitals`)

### Step 3: Create map-data.json (Optional)

If the map includes markers or GeoJSON data, create a `map-data.json` file:

```json
{
  "center": {
    "lat": 37.7749,
    "lng": -122.4194
  },
  "zoom": 10,
  "title": "Map Title",
  "subtitle": "Map Subtitle",
  "markers": [
    {
      "lat": 37.7749,
      "lng": -122.4194,
      "title": "Location Name",
      "description": "Location description",
      "category": "category-name"
    }
  ]
}
```

**For borders/regions**: Use GeoJSON format for complex geometries.

### Step 4: Create main.html

Create `main.html` using the template from `assets/template-iframe-main.html`:

**Key elements**:

- Leaflet CDN links (CSS and JS)
- Map container div with id="map"
- Optional controls section for layer toggles
- Script reference to script.js
- Minimal padding/margins for iframe embedding

**Replace placeholders**:

- `{{TITLE}}` - Map title
- `{{SUBTITLE}}` - Map subtitle
- `{{MAP_HEIGHT}}` - Map container height (default: 400px)

### Step 5: Create style.css

Create `style.css` using the template from `assets/template-iframe-style.css`:

**Critical requirements for iframe embedding**:

- `body { margin: 0; padding: 0; }` - No body margins
- Minimal margins throughout (2px max for headings)
- Fixed height for #map container
- Responsive breakpoints for mobile
- aliceblue background (repository standard)

**Customization options**:

- Map height (adjust based on content needs)
- Control button styling
- Marker popup styling

### Step 6: Create script.js

Create `script.js` using the template from `assets/template-script.js`:

**Core functionality**:

1. Initialize Leaflet map with center coordinates and zoom level
2. Add tile layer (OpenStreetMap default, or custom)
3. Add markers with popups
4. Optional: Add GeoJSON layers for borders/regions
5. Optional: Add layer controls for toggling map types

**Replace placeholders**:

- `{{CENTER_LAT}}`, `{{CENTER_LNG}}` - Map center coordinates
- `{{ZOOM}}` - Initial zoom level
- `{{MARKERS}}` - Marker data array
- `{{TILE_LAYER}}` - Tile layer URL (OpenStreetMap, satellite, etc.)

**Common tile layers**:

- OpenStreetMap: `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`
- Satellite: `https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}`
- Terrain: `https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png`

### Step 7: Create index.md

Create `index.md` using the template from `assets/template-index.md`:

**Structure**:

- Title and overview
- iframe embed (width="100%", height="700", frameborder="0")
- Link to fullscreen view
- Features section (interactive elements)
- Customization guide (how to modify the map)
- Technical details (library version, dependencies)
- Use cases
- References

**iframe embed format**:

```markdown
<iframe src="main.html" width="100%" height="700" frameborder="0"></iframe>

[View Fullscreen](main.html){:target="_blank"}
```

### Step 8: Create metadata.json

Create `metadata.json` using the template from `assets/template-metadata.json`:

**Dublin Core fields**:

- title, description, subject, creator, date, type, format, language
- coverage, rights, audience

**Map-specific fields**:

- `map_type`: "interactive", "choropleth", "route", etc.
- `center_lat`, `center_lng`: Center coordinates
- `zoom_level`: Initial zoom level
- `marker_count`: Number of markers
- `concepts`: Array of related concepts
- `bloom_taxonomy`: Cognitive level (Remember, Understand, Apply, etc.)

### Step 9: Update mkdocs.yml Navigation

Add the new map to the navigation in `mkdocs.yml`:

```yaml
nav:
  - MicroSims:
      - Introduction: sims/index.md
      - [Map Name]: sims/[map-name]/index.md
```

**Naming**: Use Title Case for navigation labels

### Step 10: Test and Validate

Perform these validation steps:

1. **Direct HTML test**: Open `docs/sims/[map-name]/main.html` in browser
   - Verify map loads correctly
   - Test zoom and pan controls
   - Click markers to verify popups
   - Test responsive behavior (resize window)

2. **MkDocs test**: Run `mkdocs serve` and navigate to the map page
   - Verify iframe embedding works
   - Check margins/padding (should be minimal)
   - Test fullscreen link
   - Verify navigation link works

3. **Browser compatibility**: Test in Chrome, Firefox, Safari

4. **Mobile test**: Verify responsive behavior on mobile devices

## Common Map Patterns

### Simple Marker Map

Basic map with multiple markers:

```javascript
const markers = [
  { lat: 40.7128, lng: -74.0060, title: "New York", description: "The Big Apple" },
  { lat: 34.0522, lng: -118.2437, title: "Los Angeles", description: "City of Angels" }
];

markers.forEach(marker => {
  L.marker([marker.lat, marker.lng])
    .bindPopup(`<b>${marker.title}</b><br>${marker.description}`)
    .addTo(map);
});
```

### Highlighted Region (GeoJSON)

Show a highlighted border or region:

```javascript
const region = {
  "type": "Feature",
  "geometry": {
    "type": "Polygon",
    "coordinates": [[...]]
  }
};

L.geoJSON(region, {
  style: { color: 'red', weight: 3, fillOpacity: 0.2 }
}).addTo(map);
```

### Layer Controls

Toggle between map types:

```javascript
const street = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');
const satellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}');

const baseMaps = {
  "Street": street,
  "Satellite": satellite
};

L.control.layers(baseMaps).addTo(map);
street.addTo(map); // Default layer
```

### Custom Marker Icons

Use custom icons for different categories:

```javascript
const universityIcon = L.icon({
  iconUrl: 'university-icon.png',
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32]
});

L.marker([lat, lng], { icon: universityIcon }).addTo(map);
```

## Educational Considerations

### Bloom's Taxonomy Alignment

- **Remember**: Identify locations on a map
- **Understand**: Explain geographic relationships
- **Apply**: Use maps for problem-solving (routes, distances)
- **Analyze**: Compare geographic patterns
- **Evaluate**: Assess geographic data quality
- **Create**: Design custom maps for specific purposes

### Accessibility

- Ensure marker popups have descriptive text
- Provide text alternatives for visual information
- Use high-contrast colors for highlighted regions
- Include keyboard navigation support

### Performance

- Limit markers to <100 for optimal performance
- Use marker clustering for large datasets:
  ```javascript
  const markers = L.markerClusterGroup();
  markers.addLayer(L.marker([lat, lng]));
  map.addLayer(markers);
  ```

## Troubleshooting

### Map not displaying

- Check that Leaflet CDN links are correct
- Verify `#map` div has a fixed height in CSS
- Ensure coordinates are in decimal format (not DMS)

### Markers not appearing

- Verify latitude/longitude order (lat first, lng second)
- Check that coordinates are within valid ranges (-90 to 90 lat, -180 to 180 lng)
- Ensure markers are added after map initialization

### Iframe not fitting properly

- Verify `body { margin: 0; padding: 0; }` in CSS
- Check iframe height in index.md (adjust if needed)
- Ensure container has minimal margins

## References

- [Leaflet Documentation](https://leafletjs.com/reference.html)
- [Leaflet Tutorials](https://leafletjs.com/examples.html)
- [OpenStreetMap Tile Usage Policy](https://operations.osmfoundation.org/policies/tiles/)
- [GeoJSON Format Specification](https://geojson.org/)

## Version History

- v1.0 (2025-01-16): Initial release with basic marker maps, layer controls, and GeoJSON support
