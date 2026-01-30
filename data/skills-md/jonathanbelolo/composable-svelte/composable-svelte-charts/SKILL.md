---
name: composable-svelte-charts
description: Data visualization and chart components for Composable Svelte. Use when creating charts, graphs, or data visualizations. Covers chart types (scatter, line, bar, area, histogram), data binding, state-driven updates, interactive features (zoom, brush, tooltips), and responsive design from @composable-svelte/charts package built with Observable Plot and D3.
---

# Composable Svelte Charts

Interactive data visualization components built with Observable Plot and D3.

---

## PACKAGE OVERVIEW

**Package**: `@composable-svelte/charts`

**Purpose**: State-driven interactive charts and data visualizations.

**Technology Stack**:
- **Observable Plot**: Declarative visualization grammar from Observable
- **D3**: Low-level utilities for scales, shapes, and interactions
- **Motion One**: Smooth transitions and animations

**Chart Types**:
- Scatter plots
- Line charts
- Bar charts
- Area charts
- Histograms

**Interactive Features**:
- Zoom & pan
- Brush selection
- Tooltips (automatic)
- Range selection
- Responsive sizing

**State Management**:
All charts use pure reducers with type-safe actions following Composable Architecture patterns.

---

## QUICK START

```typescript
import { createStore } from '@composable-svelte/core';
import { Chart, chartReducer, createInitialChartState } from '@composable-svelte/charts';

// Sample data
const data = [
  { x: 1, y: 10, category: 'A' },
  { x: 2, y: 25, category: 'B' },
  { x: 3, y: 15, category: 'A' },
  { x: 4, y: 30, category: 'B' }
];

// Create chart store
const chartStore = createStore({
  initialState: createInitialChartState({ data }),
  reducer: chartReducer,
  dependencies: {}
});

// Render scatter plot
<Chart
  store={chartStore}
  type="scatter"
  x="x"
  y="y"
  color="category"
  width={800}
  height={400}
  enableZoom={true}
  enableTooltip={true}
/>
```

---

## CHART COMPONENT

**Purpose**: High-level wrapper for creating charts with Observable Plot.

### Props

- `store: Store<ChartState, ChartAction>` - Chart store (required)
- `type: 'scatter' | 'line' | 'bar' | 'area' | 'histogram'` - Chart type (default: 'scatter')
- `width: number` - Chart width (optional, responsive if omitted)
- `height: number` - Chart height (optional, defaults to 400px)
- `x: string | ((d) => any)` - X accessor (required)
- `y: string | ((d) => any)` - Y accessor (required)
- `color: string | ((d) => any)` - Color accessor (optional)
- `size: number` - Mark size (optional)
- `xDomain: [number, number] | 'auto'` - X domain (optional)
- `yDomain: [number, number] | 'auto'` - Y domain (optional)
- `enableZoom: boolean` - Enable zoom/pan (default: false)
- `enableBrush: boolean` - Enable brush selection (default: false)
- `enableTooltip: boolean` - Enable tooltips (default: true)
- `enableAnimations: boolean` - Enable transitions (default: true)
- `onSelectionChange: (selected: any[]) => void` - Selection callback (optional)

### Usage

```typescript
<Chart
  store={chartStore}
  type="scatter"
  x="date"
  y="value"
  color={(d) => d.category}
  size={4}
  xDomain="auto"
  yDomain={[0, 100]}
  enableZoom={true}
  enableTooltip={true}
  onSelectionChange={(selected) => console.log('Selected:', selected)}
/>
```

---

## CHART TYPES

### Scatter Plot

**Purpose**: Display individual data points in 2D space.

**Best for**: Correlations, distributions, outliers.

```typescript
<Chart
  store={chartStore}
  type="scatter"
  x="temperature"
  y="sales"
  color="region"
  size={5}
  enableZoom={true}
/>
```

**Accessories**:
- `x`: X-axis position
- `y`: Y-axis position
- `color`: Point color (optional)
- `size`: Point size (optional)

### Line Chart

**Purpose**: Show trends over time or continuous data.

**Best for**: Time series, trends, comparisons.

```typescript
<Chart
  store={chartStore}
  type="line"
  x="date"
  y="price"
  color="ticker"
  enableZoom={true}
/>
```

**Notes**:
- Data should be sorted by X for proper rendering
- Multiple series via `color` accessor
- Supports missing data (gaps in line)

### Bar Chart

**Purpose**: Compare categorical data with rectangular bars.

**Best for**: Category comparisons, rankings, distributions.

```typescript
<Chart
  store={chartStore}
  type="bar"
  x="category"
  y="count"
  color="segment"
  enableTooltip={true}
/>
```

**Variants**:
- Vertical bars (default)
- Grouped bars (via `color`)
- Stacked bars (via config)

### Area Chart

**Purpose**: Line chart with filled area below.

**Best for**: Cumulative data, part-to-whole relationships.

```typescript
<Chart
  store={chartStore}
  type="area"
  x="date"
  y="value"
  color="category"
  enableZoom={true}
/>
```

**Notes**:
- Multiple series stack by default
- Baseline at Y=0 unless configured

### Histogram

**Purpose**: Distribution of numerical data into bins.

**Best for**: Data distributions, frequency analysis.

```typescript
<Chart
  store={chartStore}
  type="histogram"
  x="value"
  enableTooltip={true}
/>
```

**Notes**:
- Automatically bins data
- Y-axis shows frequency count
- Customize bins via state actions

---

## STATE MANAGEMENT

### ChartState Interface

```typescript
interface ChartState<T = unknown> {
  // Data
  data: T[];                    // Original data
  filteredData: T[];             // After filters applied

  // Visualization config
  spec: PlotSpec;                // Observable Plot spec
  dimensions: {
    width: number;
    height: number;
  };

  // Selection
  selection: {
    type: 'none' | 'point' | 'range' | 'brush';
    selectedData: T[];
    selectedIndices: number[];
    brushExtent?: [[number, number], [number, number]];
    range?: [number, number];
  };

  // Zoom/pan
  transform: {
    x: number;
    y: number;
    k: number;  // scale factor
  };
  targetTransform?: ZoomTransform;  // For animated zoom

  // Animation
  isAnimating: boolean;
  transitionDuration: number;
}
```

### ChartAction Types

```typescript
type ChartAction<T = unknown> =
  // Data
  | { type: 'setData'; data: T[] }
  | { type: 'filterData'; predicate: (d: T) => boolean }
  | { type: 'clearFilters' }

  // Selection
  | { type: 'selectPoint'; data: T; index: number }
  | { type: 'selectRange'; range: [number, number] }
  | { type: 'brushStart'; position: [number, number] }
  | { type: 'brushMove'; extent: [[number, number], [number, number]] }
  | { type: 'brushEnd' }
  | { type: 'clearSelection' }

  // Zoom/pan
  | { type: 'zoom'; transform: ZoomTransform }
  | { type: 'zoomAnimated'; targetTransform: ZoomTransform }
  | { type: 'zoomProgress'; transform: ZoomTransform }
  | { type: 'zoomComplete' }
  | { type: 'resetZoom' }

  // Dimensions
  | { type: 'resize'; dimensions: { width: number; height: number } }

  // Config
  | { type: 'updateSpec'; spec: Partial<PlotSpec> };
```

### Creating Initial State

```typescript
import { createInitialChartState } from '@composable-svelte/charts';

const initialState = createInitialChartState({
  data: myData,
  dimensions: { width: 800, height: 400 },
  transitionDuration: 300
});
```

---

## INTERACTIVE FEATURES

### Zoom & Pan

**Enable**: `enableZoom={true}`

**Controls**:
- Mouse wheel: Zoom in/out
- Click + drag: Pan
- Double-click: Reset zoom

**Programmatic zoom**:
```typescript
// Zoom in
chartStore.dispatch({
  type: 'zoom',
  transform: { x: 0, y: 0, k: 2 }  // 2x zoom
});

// Reset zoom
chartStore.dispatch({ type: 'resetZoom' });

// Animated zoom
chartStore.dispatch({
  type: 'zoomAnimated',
  targetTransform: { x: 100, y: 50, k: 1.5 }
});
```

### Brush Selection

**Enable**: `enableBrush={true}`

**Controls**:
- Click + drag: Create brush
- Drag corners: Resize brush
- Drag center: Move brush
- Click outside: Clear brush

**Access selected data**:
```typescript
const selected = $chartStore.selection.selectedData;
console.log('Selected points:', selected);
```

**Callback**:
```typescript
<Chart
  store={chartStore}
  enableBrush={true}
  onSelectionChange={(selected) => {
    console.log('Selected:', selected);
    // Do something with selected data
  }}
/>
```

### Tooltips

**Enable**: `enableTooltip={true}` (default)

**Behavior**:
- Hover over data points to show tooltip
- Automatically displays data values
- Tooltip content customizable via Observable Plot

**Custom tooltips**:
```typescript
// Via Plot spec
const spec = {
  marks: [
    Plot.dot(data, {
      x: 'x',
      y: 'y',
      title: (d) => `${d.name}: ${d.value}` // Custom tooltip
    })
  ]
};
```

### Point Selection

**Enable**: Click on points when `enableBrush={false}`

```typescript
// Listen for point selection
$effect(() => {
  if ($chartStore.selection.type === 'point') {
    const selected = $chartStore.selection.selectedData[0];
    console.log('Selected point:', selected);
  }
});

// Programmatic selection
chartStore.dispatch({
  type: 'selectPoint',
  data: myDataPoint,
  index: 5
});

// Clear selection
chartStore.dispatch({ type: 'clearSelection' });
```

---

## DATA BINDING

### Static Data

```typescript
const data = [
  { x: 1, y: 10 },
  { x: 2, y: 20 },
  { x: 3, y: 15 }
];

const chartStore = createStore({
  initialState: createInitialChartState({ data }),
  reducer: chartReducer,
  dependencies: {}
});
```

### Dynamic Data Updates

```typescript
// Update data
chartStore.dispatch({
  type: 'setData',
  data: newData
});

// Filter data
chartStore.dispatch({
  type: 'filterData',
  predicate: (d) => d.value > 10
});

// Clear filters
chartStore.dispatch({ type: 'clearFilters' });
```

### Real-time Data

```typescript
// Append new point
const currentData = $chartStore.data;
chartStore.dispatch({
  type: 'setData',
  data: [...currentData, newPoint]
});

// Update via Effect
Effect.run(async (dispatch) => {
  const newData = await fetchLatestData();
  dispatch({ type: 'setData', data: newData });
});
```

---

## RESPONSIVE DESIGN

### Auto-sizing

Omit `width` and `height` for responsive sizing:

```typescript
<Chart
  store={chartStore}
  type="scatter"
  x="x"
  y="y"
/>
```

Chart will:
- Use container width (100%)
- Default height (400px)
- Resize on window resize

### Fixed Dimensions

```typescript
<Chart
  store={chartStore}
  type="scatter"
  x="x"
  y="y"
  width={800}
  height={600}
/>
```

### Container-based Sizing

```svelte
<div class="chart-container">
  <Chart store={chartStore} ... />
</div>

<style>
  .chart-container {
    width: 100%;
    height: 500px;
  }
</style>
```

### Responsive Breakpoints

```typescript
let chartWidth = $state(800);

$effect(() => {
  const updateWidth = () => {
    chartWidth = window.innerWidth < 768 ? 400 : 800;
  };

  window.addEventListener('resize', updateWidth);
  updateWidth();

  return () => window.removeEventListener('resize', updateWidth);
});

<Chart store={chartStore} width={chartWidth} ... />
```

---

## ACCESSIBILITY

### ARIA Labels

Chart component includes:
- `role="img"` - Marks as image
- `aria-label` - Describes chart content
- `aria-describedby` - Links to summary

```svelte
<Chart
  store={chartStore}
  type="scatter"
  x="x"
  y="y"
  aria-label="Scatter plot showing relationship between X and Y"
/>
```

### Screen Reader Summary

Auto-generated summary includes:
- Chart type
- Number of data points
- Selection status
- Filter status

**Example output**:
```
"Scatter plot showing 42 data points, 5 selected"
```

### Keyboard Navigation

- `Tab`: Focus chart
- `Arrow keys`: Pan (when zoomed)
- `+/-`: Zoom in/out
- `0`: Reset zoom
- `Escape`: Clear selection

---

## COMPLETE EXAMPLES

### Basic Scatter Plot

```typescript
<script lang="ts">
import { createStore } from '@composable-svelte/core';
import { Chart, chartReducer, createInitialChartState } from '@composable-svelte/charts';

const data = [
  { x: 10, y: 20, category: 'A' },
  { x: 15, y: 35, category: 'B' },
  { x: 20, y: 25, category: 'A' },
  { x: 25, y: 45, category: 'B' }
];

const chartStore = createStore({
  initialState: createInitialChartState({ data }),
  reducer: chartReducer,
  dependencies: {}
});
</script>

<Chart
  store={chartStore}
  type="scatter"
  x="x"
  y="y"
  color="category"
  size={6}
  width={800}
  height={400}
  enableZoom={true}
  enableTooltip={true}
/>
```

### Time Series Line Chart

```typescript
<script lang="ts">
import { createStore } from '@composable-svelte/core';
import { Chart, chartReducer, createInitialChartState } from '@composable-svelte/charts';

interface DataPoint {
  date: Date;
  value: number;
  series: string;
}

const data: DataPoint[] = [
  { date: new Date('2024-01-01'), value: 100, series: 'A' },
  { date: new Date('2024-01-02'), value: 120, series: 'A' },
  { date: new Date('2024-01-03'), value: 115, series: 'A' },
  { date: new Date('2024-01-01'), value: 80, series: 'B' },
  { date: new Date('2024-01-02'), value: 95, series: 'B' },
  { date: new Date('2024-01-03'), value: 105, series: 'B' }
];

const chartStore = createStore({
  initialState: createInitialChartState({ data }),
  reducer: chartReducer,
  dependencies: {}
});
</script>

<Chart
  store={chartStore}
  type="line"
  x="date"
  y="value"
  color="series"
  width={1000}
  height={400}
  enableZoom={true}
  enableTooltip={true}
/>
```

### Interactive Bar Chart

```typescript
<script lang="ts">
import { createStore } from '@composable-svelte/core';
import { Chart, chartReducer, createInitialChartState } from '@composable-svelte/charts';

const data = [
  { category: 'Q1', revenue: 45000, expenses: 32000 },
  { category: 'Q2', revenue: 52000, expenses: 38000 },
  { category: 'Q3', revenue: 48000, expenses: 35000 },
  { category: 'Q4', revenue: 61000, expenses: 42000 }
];

const chartStore = createStore({
  initialState: createInitialChartState({ data }),
  reducer: chartReducer,
  dependencies: {}
});

let selectedCategory = $state<string | null>(null);

function handleSelection(selected: any[]) {
  selectedCategory = selected[0]?.category || null;
}
</script>

<div>
  <Chart
    store={chartStore}
    type="bar"
    x="category"
    y="revenue"
    enableBrush={true}
    enableTooltip={true}
    onSelectionChange={handleSelection}
  />

  {#if selectedCategory}
    <p>Selected: {selectedCategory}</p>
  {/if}
</div>
```

### Real-time Data Visualization

```typescript
<script lang="ts">
import { createStore, Effect } from '@composable-svelte/core';
import { Chart, chartReducer, createInitialChartState } from '@composable-svelte/charts';
import { onMount } from 'svelte';

let data = $state<Array<{ time: number; value: number }>>([]);

const chartStore = createStore({
  initialState: createInitialChartState({ data }),
  reducer: chartReducer,
  dependencies: {}
});

// Simulate real-time data stream
let intervalId: number;

onMount(() => {
  let time = 0;

  intervalId = setInterval(() => {
    const newPoint = {
      time: time++,
      value: Math.random() * 100
    };

    data = [...data.slice(-50), newPoint]; // Keep last 50 points

    chartStore.dispatch({
      type: 'setData',
      data
    });
  }, 100);

  return () => clearInterval(intervalId);
});
</script>

<Chart
  store={chartStore}
  type="line"
  x="time"
  y="value"
  yDomain={[0, 100]}
  enableAnimations={true}
/>
```

---

## COMMON PATTERNS

### Multiple Charts with Shared Selection

```typescript
<script lang="ts">
const data = [...]; // Shared data

const chartStore1 = createStore({...});
const chartStore2 = createStore({...});

let selectedData = $state<any[]>([]);

function syncSelection(selected: any[]) {
  selectedData = selected;

  // Update both charts
  const indices = selected.map(d => data.indexOf(d));
  chartStore1.dispatch({ type: 'selectRange', range: [indices[0], indices[indices.length - 1]] });
  chartStore2.dispatch({ type: 'selectRange', range: [indices[0], indices[indices.length - 1]] });
}
</script>

<Chart store={chartStore1} ... onSelectionChange={syncSelection} />
<Chart store={chartStore2} ... onSelectionChange={syncSelection} />
```

### Linked Zoom

```typescript
<script lang="ts">
const masterStore = createStore({...});
const detailStore = createStore({...});

$effect(() => {
  const transform = $masterStore.transform;
  detailStore.dispatch({ type: 'zoom', transform });
});
</script>

<Chart store={masterStore} enableZoom={true} />
<Chart store={detailStore} /> <!-- Zooms with master -->
```

### Dynamic Filtering

```typescript
<script lang="ts">
let minValue = $state(0);
let maxValue = $state(100);

$effect(() => {
  chartStore.dispatch({
    type: 'filterData',
    predicate: (d) => d.value >= minValue && d.value <= maxValue
  });
});
</script>

<input type="range" bind:value={minValue} min="0" max="100" />
<input type="range" bind:value={maxValue} min="0" max="100" />
<Chart store={chartStore} ... />
```

---

## PERFORMANCE CONSIDERATIONS

### Large Datasets

**Problem**: Rendering 10,000+ points can be slow.

**Solutions**:
1. **Data aggregation**: Bin/group data before rendering
2. **Sampling**: Show subset of data (e.g., every 10th point)
3. **Level-of-detail**: Show more detail when zoomed in
4. **WebGL rendering**: Use Plot's WebGL marks (future)

```typescript
// Example: Downsample data
const downsample = (data: any[], factor: number) =>
  data.filter((_, i) => i % factor === 0);

const displayData = data.length > 1000
  ? downsample(data, Math.ceil(data.length / 1000))
  : data;

chartStore.dispatch({ type: 'setData', data: displayData });
```

### Frequent Updates

**Problem**: Real-time data updates cause re-renders.

**Solutions**:
1. **Batch updates**: Update every N milliseconds, not every data point
2. **Sliding window**: Keep fixed number of points (e.g., last 100)
3. **Throttle**: Limit update frequency

```typescript
// Throttle updates
let pendingData: any[] = [];
let updateTimer: number | null = null;

function queueUpdate(newData: any[]) {
  pendingData = newData;

  if (updateTimer === null) {
    updateTimer = setTimeout(() => {
      chartStore.dispatch({ type: 'setData', data: pendingData });
      updateTimer = null;
    }, 100); // Update max once per 100ms
  }
}
```

### Animation Performance

Disable animations for large datasets or frequent updates:

```typescript
<Chart
  store={chartStore}
  enableAnimations={false}
  ...
/>
```

---

## TESTING

### Basic Chart Testing

```typescript
import { TestStore } from '@composable-svelte/core';
import { chartReducer, createInitialChartState } from '@composable-svelte/charts';

const store = new TestStore({
  initialState: createInitialChartState({ data: [] }),
  reducer: chartReducer,
  dependencies: {}
});

// Test data update
await store.send({
  type: 'setData',
  data: [{ x: 1, y: 10 }]
}, (state) => {
  expect(state.data.length).toBe(1);
  expect(state.filteredData.length).toBe(1);
});

// Test filtering
await store.send({
  type: 'filterData',
  predicate: (d) => d.y > 5
}, (state) => {
  expect(state.filteredData.length).toBe(1);
});
```

### Selection Testing

```typescript
await store.send({
  type: 'selectPoint',
  data: { x: 1, y: 10 },
  index: 0
}, (state) => {
  expect(state.selection.type).toBe('point');
  expect(state.selection.selectedData.length).toBe(1);
  expect(state.selection.selectedIndices).toEqual([0]);
});

await store.send({ type: 'clearSelection' }, (state) => {
  expect(state.selection.type).toBe('none');
  expect(state.selection.selectedData.length).toBe(0);
});
```

---

## TROUBLESHOOTING

**Chart not rendering**:
- Check Observable Plot installed: `npm install @observablehq/plot`
- Verify data is non-empty array
- Ensure x/y accessors match data properties

**Tooltips not showing**:
- Verify `enableTooltip={true}`
- Check Observable Plot version (0.6+ required)
- Ensure data points have valid values (not null/undefined)

**Zoom not working**:
- Verify `enableZoom={true}`
- Check chart has fixed dimensions (not 100% width/height)
- Ensure D3-zoom is installed

**Poor performance**:
- Reduce data points (aggregate, sample, or downsample)
- Disable animations for large datasets
- Use simpler mark types (dots vs complex shapes)

**Selection not updating**:
- Check `onSelectionChange` callback
- Verify `enableBrush={true}` or `enableSelection={true}`
- Ensure store is reactive (`$chartStore.selection`)

---

## CROSS-REFERENCES

**Related Skills**:
- **composable-svelte-core**: Store, reducer, Effect system
- **composable-svelte-components**: UI components (Button, Slider, etc.)
- **composable-svelte-testing**: TestStore for testing chart reducers

**When to Use Each Package**:
- **charts**: 2D data visualization, interactive charts
- **graphics**: 3D scenes, WebGPU/WebGL (see composable-svelte-graphics)
- **maps**: Geospatial data (see composable-svelte-maps)
- **code**: Code editors, media players (see composable-svelte-code)
