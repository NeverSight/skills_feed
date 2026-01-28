---
name: d3-visualization
description: Use when creating custom, interactive data visualizations with D3.js—building bar/line/scatter charts from scratch, creating network diagrams or geographic maps, binding changing data to visual elements, adding zoom/pan/brush interactions, animating chart transitions, or when chart libraries (Highcharts, Chart.js) don't support your specific visualization design and you need low-level control over data-driven DOM manipulation, scales, shapes, and layouts.
---

# D3.js Data Visualization

## Table of Contents

- [Read This First](#read-this-first)
- [Workflows](#workflows)
  - [Create Basic Chart Workflow](#create-basic-chart-workflow)
  - [Update Visualization with New Data](#update-visualization-with-new-data)
  - [Create Advanced Layout Workflow](#create-advanced-layout-workflow)
- [Path Selection Menu](#path-selection-menu)
- [Quick Reference](#quick-reference)

---

## Read This First

### What This Skill Does

This skill helps you create custom, interactive data visualizations using D3.js (Data-Driven Documents). D3 provides low-level building blocks for data-driven DOM manipulation, visual encoding, layout algorithms, and interactions—enabling bespoke visualizations that chart libraries can't provide.

### When to Use D3

**Use D3 when:**
- Chart libraries don't support your specific design
- You need full customization control
- Creating network graphs, hierarchies, or geographic maps
- Building interactive dashboards with linked views
- Animating data changes smoothly
- Working with complex or unconventional data structures

**Don't use D3 when:**
- Simple bar/line charts suffice (use Chart.js, Highcharts—easier)
- You need 3D visualizations (use Three.js, WebGL)
- Massive datasets >10K points without aggregation (performance limitations)
- You're unfamiliar with JavaScript/SVG/CSS (prerequisites required)

### Core Concepts

**Data Joins**: Bind arrays to DOM elements, creating one-to-one correspondence
**Scales**: Transform data values → visual values (pixels, colors, sizes)
**Shapes**: Generate SVG paths for lines, areas, arcs from data
**Layouts**: Calculate positions for complex visualizations (networks, trees, maps)
**Transitions**: Animate smooth changes between states
**Interactions**: Add zoom, pan, drag, brush selection behaviors

### Skill Structure

- **[Getting Started](resources/getting-started.md)**: Setup, prerequisites, first visualization
- **[Selections & Data Joins](resources/selections-datajoins.md)**: DOM manipulation, data binding
- **[Scales & Axes](resources/scales-axes.md)**: Data transformation, axis generation
- **[Shapes & Layouts](resources/shapes-layouts.md)**: Path generators, basic layouts
- **[Advanced Layouts](resources/advanced-layouts.md)**: Force simulation, hierarchies, geographic maps
- **[Transitions & Interactions](resources/transitions-interactions.md)**: Animations, zoom/pan/drag/brush
- **[Workflows](resources/workflows.md)**: Step-by-step guides for common chart types
- **[Common Patterns](resources/common-patterns.md)**: Reusable code templates

---

## Workflows

Choose a workflow based on your current task:

### Create Basic Chart Workflow

**Use when:** Building bar, line, or scatter charts from scratch

**Time:** 1-2 hours

**Copy this checklist and track your progress:**

```
Basic Chart Progress:
- [ ] Step 1: Set up SVG container with margins
- [ ] Step 2: Load and parse data
- [ ] Step 3: Create scales (x, y)
- [ ] Step 4: Generate axes
- [ ] Step 5: Bind data and create visual elements
- [ ] Step 6: Style and add interactivity
```

**Step 1: Set up SVG container with margins**

Create SVG element with proper dimensions. Define margins for axes: `{top: 20, right: 20, bottom: 30, left: 40}`. Calculate inner width/height: `width - margin.left - margin.right`. See [Getting Started](resources/getting-started.md#setup-svg-container).

**Step 2: Load and parse data**

Use `d3.csv('data.csv')` for external files or define data array directly. Parse dates with `d3.timeParse('%Y-%m-%d')` for time series. Convert strings to numbers for CSV data using conversion function. See [Getting Started](resources/getting-started.md#loading-data).

**Step 3: Create scales**

Choose scale types based on data: `scaleBand` (categorical), `scaleTime` (temporal), `scaleLinear` (quantitative). Set domains from data using `d3.extent()`, `d3.max()`, or manual ranges. Set ranges from SVG dimensions. See [Scales & Axes](resources/scales-axes.md#scale-types).

**Step 4: Generate axes**

Create axis generators: `d3.axisBottom(xScale)`, `d3.axisLeft(yScale)`. Append g elements positioned with transforms. Call axis generators: `.call(axis)`. Customize ticks with `.ticks()`, `.tickFormat()`. See [Scales & Axes](resources/scales-axes.md#creating-axes).

**Step 5: Bind data and create visual elements**

Use data join pattern: `svg.selectAll(type).data(array).join(type)`. Set attributes using scales and accessor functions: `.attr('x', d => xScale(d.category))`. For line charts, use `d3.line()` generator. For scatter plots, create circles with `cx`, `cy`, `r` attributes. See [Selections & Data Joins](resources/selections-datajoins.md#data-join-pattern) and [Shapes & Layouts](resources/shapes-layouts.md).

**Step 6: Style and add interactivity**

Apply colors: `.attr('fill', ...)`, `.attr('stroke', ...)`. Add hover effects: `.on('mouseover', ...)` with tooltip. Add click handlers for drill-down. Apply transitions for initial animation (optional). See [Transitions & Interactions](resources/transitions-interactions.md#tooltips) and [Common Patterns](resources/common-patterns.md#tooltip-pattern).

---

### Update Visualization with New Data

**Use when:** Refreshing charts with new data (real-time, filters, user interactions)

**Time:** 30 minutes - 1 hour

**Copy this checklist:**

```
Update Progress:
- [ ] Step 1: Encapsulate visualization in update function
- [ ] Step 2: Update scale domains if needed
- [ ] Step 3: Re-bind data with key function
- [ ] Step 4: Add transitions to join
- [ ] Step 5: Update attributes with new values
- [ ] Step 6: Trigger update on data change
```

**Step 1: Encapsulate visualization in update function**

Wrap steps 3-5 from basic chart workflow in `function update(newData) { ... }`. This makes visualization reusable for any dataset. See [Workflows](resources/workflows.md#update-pattern).

**Step 2: Update scale domains**

Recalculate domains when data range changes: `yScale.domain([0, d3.max(newData, d => d.value)])`. Update axes with transition: `svg.select('.y-axis').transition().duration(500).call(yAxis)`. See [Selections & Data Joins](resources/selections-datajoins.md#updating-scales).

**Step 3: Re-bind data with key function**

Use key function for object constancy: `.data(newData, d => d.id)`. Ensures elements track data items, not array positions. Critical for correct transitions. See [Selections & Data Joins](resources/selections-datajoins.md#key-functions).

**Step 4: Add transitions to join**

Insert `.transition().duration(500)` before attribute updates. Specify easing with `.ease(d3.easeCubicOut)`. For custom enter/exit effects, use enter/exit functions in `.join()`. See [Transitions & Interactions](resources/transitions-interactions.md#basic-transitions).

**Step 5: Update attributes with new values**

Set positions/sizes using updated scales: `.attr('y', d => yScale(d.value))`, `.attr('height', d => height - yScale(d.value))`. Transitions animate from old to new values. See [Common Patterns](resources/common-patterns.md#bar-chart-template).

**Step 6: Trigger update on data change**

Call `update(newData)` when data changes: button clicks, timers (`setInterval`), WebSocket messages, API responses. For real-time, use sliding window to limit data points. See [Workflows](resources/workflows.md#real-time-updates).

---

### Create Advanced Layout Workflow

**Use when:** Building network graphs, hierarchies, or geographic maps

**Time:** 2-4 hours

**Copy this checklist:**

```
Advanced Layout Progress:
- [ ] Step 1: Choose appropriate layout type
- [ ] Step 2: Prepare and structure data
- [ ] Step 3: Create and configure layout
- [ ] Step 4: Apply layout to data
- [ ] Step 5: Bind computed properties to elements
- [ ] Step 6: Add interactions (drag, zoom)
```

**Step 1: Choose appropriate layout type**

**Force Simulation**: Network diagrams, organic clustering. **Hierarchies**: Tree, cluster (node-link), treemap, pack, partition (space-filling). **Geographic**: Maps with projections. **Chord**: Flow diagrams. See [Advanced Layouts](resources/advanced-layouts.md#choosing-layout) for decision guidance.

**Step 2: Prepare and structure data**

**Force**: `nodes = [{id, group}]`, `links = [{source, target}]`. **Hierarchy**: Nested objects with children arrays, convert with `d3.hierarchy(data)`. **Geographic**: GeoJSON features. See [Advanced Layouts](resources/advanced-layouts.md#data-structures).

**Step 3: Create and configure layout**

**Force**: `d3.forceSimulation(nodes).force('link', d3.forceLink(links)).force('charge', d3.forceManyBody())`. **Hierarchy**: `d3.treemap().size([width, height])`. **Geographic**: `d3.geoMercator().fitExtent([[0,0], [width,height]], geojson)`. See [Advanced Layouts](resources/advanced-layouts.md) for each layout type.

**Step 4: Apply layout to data**

**Force**: Simulation runs automatically, updates node positions each tick. **Hierarchy**: Call layout on root: `treemap(root)`. **Geographic**: No application needed, projection used in path generator. See [Advanced Layouts](resources/advanced-layouts.md#applying-layouts).

**Step 5: Bind computed properties to elements**

**Force**: Update `cx`, `cy` in tick handler: `node.attr('cx', d => d.x)`. **Hierarchy**: Use `d.x0`, `d.x1`, `d.y0`, `d.y1` for rectangles. **Geographic**: Use `path(feature)` for `d` attribute. See [Workflows](resources/workflows.md) for layout-specific examples.

**Step 6: Add interactions**

**Drag** for force networks: `node.call(d3.drag().on('drag', dragHandler))`. **Zoom** for maps/large networks: `svg.call(d3.zoom().on('zoom', zoomHandler))`. **Click** for hierarchy drill-down. See [Transitions & Interactions](resources/transitions-interactions.md).

---

## Path Selection Menu

**What would you like to do?**

1. **[I'm new to D3](resources/getting-started.md)** - Setup environment, understand prerequisites, create first visualization

2. **[Build a basic chart](resources/workflows.md#basic-charts)** - Bar, line, or scatter plot step-by-step

3. **[Transform data with scales](resources/scales-axes.md)** - Map data values to visual properties (positions, colors, sizes)

4. **[Bind data to elements](resources/selections-datajoins.md)** - Connect arrays to DOM elements, handle dynamic updates

5. **[Create network/hierarchy/map](resources/advanced-layouts.md)** - Force-directed graphs, treemaps, geographic visualizations

6. **[Add animations](resources/transitions-interactions.md#transitions)** - Smooth transitions between chart states

7. **[Add interactivity](resources/transitions-interactions.md#interactions)** - Zoom, pan, drag, brush selection, tooltips

8. **[Update chart with new data](resources/workflows.md#update-pattern)** - Handle real-time data, filters, user interactions

9. **[Get code templates](resources/common-patterns.md)** - Copy-paste-modify templates for common patterns

10. **[Understand D3 concepts](resources/getting-started.md#core-concepts)** - Deep dive into data joins, scales, generators, layouts

---

## Quick Reference

### Data Join Pattern (Core D3 Workflow)

```javascript
// 1. Select container
const svg = d3.select('svg');

// 2. Bind data
svg.selectAll('circle')
  .data(dataArray)
  .join('circle')          // Create/update/remove elements automatically
    .attr('cx', d => d.x)  // Use accessor functions (d = datum, i = index)
    .attr('cy', d => d.y)
    .attr('r', 5);
```

### Scale Creation (Data → Visual Transformation)

```javascript
// For quantitative data
const xScale = d3.scaleLinear()
  .domain([0, 100])        // Data range
  .range([0, 500]);        // Pixel range

// For categorical data
const xScale = d3.scaleBand()
  .domain(['A', 'B', 'C'])
  .range([0, 500])
  .padding(0.1);

// For temporal data
const xScale = d3.scaleTime()
  .domain([new Date(2020, 0, 1), new Date(2020, 11, 31)])
  .range([0, 500]);
```

### Shape Generators (SVG Path Creation)

```javascript
// Line chart
const line = d3.line()
  .x(d => xScale(d.date))
  .y(d => yScale(d.value));

svg.append('path')
  .datum(data)           // Use .datum() for single data item
  .attr('d', line)       // Line generator creates path data
  .attr('fill', 'none')
  .attr('stroke', 'steelblue');
```

### Transitions (Animation)

```javascript
// Add transition before attribute updates
svg.selectAll('rect')
  .data(newData)
  .join('rect')
  .transition()          // Everything after this is animated
  .duration(500)         // Milliseconds
  .attr('height', d => yScale(d.value));
```

### Common Scale Types

| Data Type | Task | Scale |
|-----------|------|-------|
| Quantitative (linear) | Position, size | `scaleLinear()` |
| Quantitative (exponential) | Compress range | `scaleLog()`, `scalePow()` |
| Quantitative → Circle area | Size circles | `scaleSqrt()` |
| Categorical | Bars, groups | `scaleBand()`, `scalePoint()` |
| Categorical → Colors | Color encoding | `scaleOrdinal()` |
| Temporal | Time series | `scaleTime()` |
| Quantitative → Colors | Heatmaps | `scaleSequential()` |

### D3 Module Imports (ES6)

```javascript
// Specific functions
import { select, selectAll } from 'd3-selection';
import { scaleLinear, scaleBand } from 'd3-scale';
import { line, area } from 'd3-shape';

// Entire D3 namespace
import * as d3 from 'd3';
```

### Key Resources by Task

- **Setup & First Chart**: [Getting Started](resources/getting-started.md)
- **Data Binding**: [Selections & Data Joins](resources/selections-datajoins.md)
- **Scales & Axes**: [Scales & Axes](resources/scales-axes.md)
- **Chart Types**: [Workflows](resources/workflows.md) + [Common Patterns](resources/common-patterns.md)
- **Networks & Trees**: [Advanced Layouts](resources/advanced-layouts.md#force-simulation) + [Advanced Layouts](resources/advanced-layouts.md#hierarchies)
- **Maps**: [Advanced Layouts](resources/advanced-layouts.md#geographic-maps)
- **Animation**: [Transitions & Interactions](resources/transitions-interactions.md#transitions)
- **Interactivity**: [Transitions & Interactions](resources/transitions-interactions.md#interactions)

---

## Next Steps

1. **New to D3?** Start with [Getting Started](resources/getting-started.md)
2. **Know basics?** Jump to [Workflows](resources/workflows.md) for specific chart types
3. **Need reference?** Use [Common Patterns](resources/common-patterns.md) for templates
4. **Build custom viz?** Explore [Advanced Layouts](resources/advanced-layouts.md)
