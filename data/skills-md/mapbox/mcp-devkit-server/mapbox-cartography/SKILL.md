---
name: mapbox-cartography
description: Expert guidance on map design principles, color theory, visual hierarchy, typography, and cartographic best practices for creating effective and beautiful maps with Mapbox. Use when designing map styles, choosing colors, or making cartographic decisions.
---

# Mapbox Cartography Skill

This skill provides expert cartographic knowledge to help you design effective, beautiful, and functional maps using Mapbox.

## Core Cartographic Principles

### Visual Hierarchy

Maps must guide the viewer's attention to what matters most:

- **Most important**: POIs, user location, route highlights
- **Secondary**: Major roads, city labels, landmarks
- **Tertiary**: Minor streets, administrative boundaries
- **Background**: Water, land use, terrain

**Implementation:**

- Use size, color intensity, and contrast to establish hierarchy
- Primary features: high contrast, larger symbols, bold colors
- Background features: low contrast, muted colors, smaller text

### Color Theory for Maps

**Color Harmony:**

- **Analogous colors**: Use colors next to each other on color wheel (blue-green-teal) for cohesive designs
- **Complementary colors**: Use opposite colors (blue/orange, red/green) for high contrast emphasis
- **Monochromatic**: Single hue with varying saturation/brightness for elegant, minimal designs

**Color Psychology:**

- **Blue**: Water, trust, calm, professional (default for water bodies)
- **Green**: Parks, nature, growth, eco-friendly (vegetation, parks)
- **Red/Orange**: Urgent, important, dining (alerts, restaurants)
- **Yellow**: Caution, highlight, attention (warnings, selected items)
- **Gray**: Neutral, background, roads (infrastructure)

**Accessibility:**

- Ensure 4.5:1 contrast ratio for text (WCAG AA)
- Don't rely solely on color to convey information
- Test designs with colorblind simulators
- Avoid red/green combinations for critical distinctions

### Typography Best Practices

**Font Selection:**

- **Sans-serif** (Roboto, Open Sans): Modern, clean, high legibility at small sizes - use for labels
- **Serif** (Noto Serif): Traditional, formal - use sparingly for titles or historic maps
- **Monospace**: Technical data, coordinates

**Text Sizing:**

```
Place labels (cities, POIs): 11-14px
Street labels: 9-11px
Feature labels (parks): 10-12px
Map title: 16-20px
Attribution: 8-9px
```

**Label Placement:**

- Point labels: Center or slightly offset (avoid overlap with symbol)
- Line labels: Follow line curve, repeat for long features
- Area labels: Center in polygon, sized appropriately
- Prioritize: Major features get labels first, minor features labeled if space allows

### Map Context Considerations

**Know Your Audience:**

- **General public**: Simplify, use familiar patterns (Google/Apple style)
- **Technical users**: Include more detail, technical layers, data precision
- **Domain experts**: Show specialized data, use domain-specific symbology

**Use Case Optimization:**

- **Navigation**: Emphasize roads, clear hierarchy, route visibility
- **Data visualization**: Muted base map, let data stand out
- **Storytelling**: Guide viewer attention, establish mood with colors
- **Location selection**: Show POIs clearly, provide context
- **Analysis**: Include relevant layers, maintain clarity at different zooms

**Platform Considerations:**

- **Mobile**: Larger touch targets (44x44px minimum), simpler designs, readable at arm's length
- **Desktop**: Can include more detail, hover interactions, complex overlays
- **Print**: Higher contrast, larger text, consider CMYK color space
- **Outdoor/Bright**: Higher contrast, avoid subtle grays

## Mapbox-Specific Guidance

### Style Layer Best Practices

**Layer Ordering (bottom to top):**

1. Background (solid color or pattern)
2. Landuse (parks, residential, commercial)
3. Water bodies (oceans, lakes, rivers)
4. Terrain/hillshade (if using elevation)
5. Buildings (3D or 2D footprints)
6. Roads (highways → local streets)
7. Borders (country, state lines)
8. Labels (place names, street names)
9. POI symbols
10. User-generated content (routes, markers)

### Zoom Level Strategy

**Zoom 0-4** (World to Continent):

- Major country boundaries
- Ocean and sea labels
- Capital cities only

**Zoom 5-8** (Country to State):

- State/province boundaries
- Major cities
- Major highways
- Large water bodies

**Zoom 9-11** (Metro Area):

- City boundaries
- Neighborhoods
- All highways and major roads
- Parks and landmarks

**Zoom 12-15** (Neighborhood):

- All streets
- Building footprints
- POIs (restaurants, shops)
- Street names

**Zoom 16-22** (Street Level):

- All detail
- House numbers
- Parking lots
- Fine-grained POIs

### Color Palette Templates

**Light Theme (Day/Professional):**

```json
{
  "background": "#f5f5f5",
  "water": "#a0c8f0",
  "parks": "#d4e7c5",
  "roads": "#ffffff",
  "buildings": "#e0e0e0",
  "text": "#333333"
}
```

**Dark Theme (Night Mode):**

```json
{
  "background": "#1a1a1a",
  "water": "#0d47a1",
  "parks": "#2e7d32",
  "roads": "#3a3a3a",
  "buildings": "#2d2d2d",
  "text": "#ffffff"
}
```

**High Contrast (Accessibility):**

```json
{
  "background": "#000000",
  "water": "#0066ff",
  "parks": "#00ff00",
  "roads": "#ffffff",
  "buildings": "#808080",
  "text": "#ffffff"
}
```

**Vintage/Retro:**

```json
{
  "background": "#f4e8d0",
  "water": "#b8d4d4",
  "parks": "#c8d4a4",
  "roads": "#d4c4a8",
  "buildings": "#e4d4c4",
  "text": "#4a3828"
}
```

## Common Mapping Scenarios

### Scenario: Restaurant Finder App

**Requirements:**

- Restaurants must be highly visible
- Street context for navigation
- Muted background (food photos overlay)

**Recommendations:**

- Use bold, warm colors for restaurant markers (red, orange)
- Gray out background (low saturation)
- Keep street labels clear but not dominant
- High contrast for selected restaurant
- Mobile-optimized touch targets

### Scenario: Real Estate Map

**Requirements:**

- Property boundaries clearly visible
- Neighborhood context
- Price differentiation

**Recommendations:**

- Use color scale for price ranges (green=affordable, red=expensive)
- Show parks and amenities prominently
- Include school zones if relevant
- Label neighborhoods clearly
- Show transit access

### Scenario: Data Visualization Overlay

**Requirements:**

- Data layer is primary focus
- Base map provides context only
- Multiple data points may cluster

**Recommendations:**

- Monochromatic, low-contrast base map
- Use data-ink ratio principle (minimize non-data elements)
- Base map grayscale or single muted hue
- Remove unnecessary labels
- Consider using light base for dark data, vice versa

### Scenario: Navigation/Routing

**Requirements:**

- Route must be unmissable
- Turn-by-turn clarity
- Current location always visible

**Recommendations:**

- Route in high-contrast color (blue or purple)
- Animate route line or use dashed pattern
- Large, clear turn indicators
- Dim unrelated features
- User location: pulsing blue dot
- Next turn: prominent arrow/icon

## Performance Optimization

**Style Performance:**

- Minimize layer count (combine similar layers)
- Use expressions instead of multiple layers for variants
- Simplify complex geometries at lower zooms
- Use sprite sheets for repeated icons
- Leverage tileset simplification

**Loading Speed:**

- Preload critical zoom levels
- Use style optimization tools
- Minimize external resource calls
- Compress images in sprite sheets

## Testing Your Design

**Checklist:**

- [ ] View at all relevant zoom levels
- [ ] Test in different lighting conditions
- [ ] Check on actual devices (mobile, desktop)
- [ ] Verify color accessibility (colorblind.org)
- [ ] Review with target users
- [ ] Test with real data density
- [ ] Check label collision/overlap
- [ ] Verify performance on slower devices

## Common Mistakes to Avoid

1. **Too many colors**: Stick to 5-7 main colors maximum
2. **Insufficient contrast**: Text must be readable
3. **Overcrowding**: Not everything needs a label
4. **Ignoring zoom levels**: Show appropriate detail for scale
5. **Poor label hierarchy**: Organize by importance
6. **Inconsistent styling**: Maintain visual consistency
7. **Neglecting performance**: Complex styles slow rendering
8. **Forgetting mobile**: Test on actual devices

## When to Use This Skill

Invoke this skill when:

- Designing a new map style
- Choosing colors for map elements
- Making decisions about visual hierarchy
- Optimizing for specific use cases
- Troubleshooting visibility issues
- Ensuring accessibility
- Creating themed maps (dark mode, vintage, etc.)
