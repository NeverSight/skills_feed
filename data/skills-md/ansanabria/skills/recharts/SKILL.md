---
name: recharts
description: Build composable, responsive React charts with Recharts library. Use when creating data visualizations including line charts, area charts, bar charts, pie charts, scatter plots, and composed charts. Handles chart customization, responsive sizing, tooltips, legends, axes configuration, performance optimization, and accessibility.
---

# Recharts

React charting library built on top of D3 for composable, declarative data visualization.

## Quick Start

### 1. Install Recharts

```bash
npm install recharts
```

### 2. Basic Chart Structure

All Recharts charts follow the same pattern:

```jsx
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const data = [
  { name: 'Jan', sales: 4000, profit: 2400 },
  { name: 'Feb', sales: 3000, profit: 1398 },
  { name: 'Mar', sales: 2000, profit: 9800 },
];

<ResponsiveContainer width="100%" height={300}>
  <LineChart data={data}>
    <CartesianGrid strokeDasharray="3 3" />
    <XAxis dataKey="name" />
    <YAxis />
    <Tooltip />
    <Legend />
    <Line type="monotone" dataKey="sales" stroke="#8884d8" />
    <Line type="monotone" dataKey="profit" stroke="#82ca9d" />
  </LineChart>
</ResponsiveContainer>
```

## Core Concepts

### Data Format

Recharts expects data as an **array of objects**. Each object represents a data point:

```javascript
const data = [
  { month: 'Jan', revenue: 4000, expenses: 2400 },
  { month: 'Feb', revenue: 3000, expenses: 1398 },
];
```

Use `dataKey` props to map object properties to chart components:
- `dataKey="revenue"` - maps to the revenue property
- `dataKey={(entry) => entry.revenue - entry.expenses}` - function for computed values

### Component Composition

Charts are built by nesting specialized components:

**Sizing**: Use the `responsive` prop (v3.3+), `ResponsiveContainer` wrapper, or set `width`/`height` directly

**Chart types** (choose one):
- `LineChart` - Line and area visualizations
- `BarChart` - Bar and column charts
- `AreaChart` - Stacked and filled area charts
- `PieChart` - Pie and donut charts
- `ScatterChart` - Scatter plots and bubble charts
- `ComposedChart` - Mixed chart types
- `RadarChart` - Radar/spider charts
- `RadialBarChart` - Circular bar charts

**Common child components**:
- `XAxis` / `YAxis` - Axis configuration
- `CartesianGrid` - Grid lines
- `Tooltip` - Hover information
- `Legend` - Series identification
- `Line` / `Bar` / `Area` / `Pie` - Data series visualization

## Chart Patterns by Type

### Line Charts

```jsx
<LineChart data={data}>
  <XAxis dataKey="name" />
  <YAxis />
  <CartesianGrid strokeDasharray="3 3" />
  <Tooltip />
  <Legend />
  <Line type="monotone" dataKey="value" stroke="#8884d8" strokeWidth={2} dot={{ r: 4 }} />
</LineChart>
```

**Key props**:
- `type`: "monotone" (smooth), "linear", "step", "natural"
- `stroke`: line color
- `strokeWidth`: line thickness
- `dot`: point styling (set to `false` to hide)
- `activeDot`: hovered point styling
- `connectNulls`: true to connect gaps

### Area Charts

```jsx
<AreaChart data={data}>
  <defs>
    <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
      <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8}/>
      <stop offset="95%" stopColor="#8884d8" stopOpacity={0}/>
    </linearGradient>
  </defs>
  <XAxis dataKey="name" />
  <YAxis />
  <CartesianGrid strokeDasharray="3 3" />
  <Tooltip />
  <Area type="monotone" dataKey="value" stroke="#8884d8" fillOpacity={1} fill="url(#colorValue)" />
</AreaChart>
```

**Stacked areas**:
```jsx
<Area type="monotone" dataKey="sales" stackId="1" stroke="#8884d8" fill="#8884d8" />
<Area type="monotone" dataKey="profit" stackId="1" stroke="#82ca9d" fill="#82ca9d" />
```

### Bar Charts

```jsx
<BarChart data={data}>
  <XAxis dataKey="name" />
  <YAxis />
  <CartesianGrid strokeDasharray="3 3" />
  <Tooltip />
  <Legend />
  <Bar dataKey="sales" fill="#8884d8" radius={[4, 4, 0, 0]} />
  <Bar dataKey="profit" fill="#82ca9d" radius={[4, 4, 0, 0]} />
</BarChart>
```

**Key props**:
- `fill`: bar color
- `radius`: rounded corners [topLeft, topRight, bottomRight, bottomLeft] or single number for all corners
- `barSize`: fixed bar width
- `stackId`: group bars into stacks
- `shape`: custom bar shape (function or element)

**Stacked bars**:
```jsx
<Bar dataKey="sales" stackId="a" fill="#8884d8" />
<Bar dataKey="profit" stackId="a" fill="#82ca9d" />
```

**Rounded stacked bars** (use `BarStack` to round the whole stack):
```jsx
import { BarStack } from 'recharts';

<BarChart data={data}>
  <BarStack stackId="a" radius={[4, 4, 0, 0]}>
    <Bar dataKey="sales" fill="#8884d8" />
    <Bar dataKey="profit" fill="#82ca9d" />
  </BarStack>
</BarChart>
```

### Pie Charts

```jsx
const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

<PieChart>
  <Pie
    data={data}
    dataKey="value"
    nameKey="name"
    cx="50%"
    cy="50%"
    innerRadius={60}
    outerRadius={80}
    paddingAngle={5}
    shape={(props) => <Sector {...props} fill={COLORS[props.index % COLORS.length]} />}
  />
  <Tooltip />
  <Legend />
</PieChart>
```

**Key props**:
- `innerRadius`: creates donut chart when > 0
- `outerRadius`: pie size
- `paddingAngle`: gap between slices
- `startAngle` / `endAngle`: partial pie (default: 0 to 360)
- `label`: shows values on slices
- `shape`: custom render for each slice (replaces deprecated `Cell` component)

### Scatter Charts

```jsx
<ScatterChart>
  <XAxis type="number" dataKey="x" name="X Axis" />
  <YAxis type="number" dataKey="y" name="Y Axis" />
  <CartesianGrid />
  <Tooltip cursor={{ strokeDasharray: '3 3' }} />
  <Scatter name="Series A" data={data} fill="#8884d8" />
</ScatterChart>
```

### Composed Charts

Mix multiple chart types:

```jsx
<ComposedChart data={data}>
  <XAxis dataKey="name" />
  <YAxis />
  <CartesianGrid stroke="#f5f5f5" />
  <Tooltip />
  <Legend />
  <Area type="monotone" dataKey="total" fill="#8884d8" stroke="#8884d8" />
  <Bar dataKey="sales" barSize={20} fill="#413ea0" />
  <Line type="monotone" dataKey="profit" stroke="#ff7300" />
</ComposedChart>
```

## Responsive Sizing

### Option 1: `responsive` prop (Recharts 3.3+, recommended)

Set `responsive` on the chart itself. Uses standard CSS sizing rules:

```jsx
<LineChart data={data} width="100%" height={300} responsive>
  {/* chart components */}
</LineChart>
```

Works with flexbox and CSS grid layouts. Also supports CSS `style` props:

```jsx
<LineChart data={data} responsive style={{ maxWidth: 800, width: '100%', aspectRatio: '16/9' }}>
  {/* chart components */}
</LineChart>
```

### Option 2: `ResponsiveContainer` (older versions)

For Recharts < 3.3, wrap chart in `ResponsiveContainer`:

```jsx
<ResponsiveContainer width="100%" height={300}>
  <LineChart data={data}>
    {/* chart components */}
  </LineChart>
</ResponsiveContainer>
```

**Critical**: `ResponsiveContainer` must have a parent with defined dimensions. Height must be a number, not a percentage.

### Static sizing

Set `width` and `height` directly as pixels or percentages:

```jsx
<LineChart data={data} width={600} height={300}>
  {/* chart components */}
</LineChart>
```

## Axes Configuration

### XAxis / YAxis Props

```jsx
<XAxis 
  dataKey="name"           // property to display
  type="category"          // "category" or "number"
  domain={[0, 'dataMax']}    // axis range
  tick={{ fill: '#666' }}    // tick styling
  tickFormatter={(value) => `$${value}`}  // format labels
  angle={-45}               // rotate labels
  textAnchor="end"         // text alignment
  height={60}              // extra space for labels
/>
```

### Axis Types

- **Category axis** (default for X): Treats values as discrete labels
- **Number axis** (default for Y): Treats values as continuous scale

### Custom Domains

Control axis range:

```jsx
// Fixed range
<YAxis domain={[0, 100]} />

// Auto with padding
<YAxis domain={[0, 'auto']} />

// Data-based with overflow allowed
<YAxis domain={[0, 'dataMax + 100']} allowDataOverflow />

// Logarithmic scale
<YAxis type="number" scale="log" domain={['auto', 'auto']} />
```

## Customization

### Custom Tooltip

```jsx
const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="custom-tooltip">
        <p className="label">{`${label}`}</p>
        <p className="intro">{`Sales: ${payload[0].value}`}</p>
        <p className="desc">Additional info...</p>
      </div>
    );
  }
  return null;
};

<Tooltip content={<CustomTooltip />} />
```

### Custom Legend

```jsx
const CustomLegend = ({ payload }) => (
  <ul>
    {payload.map((entry, index) => (
      <li key={`item-${index}`} style={{ color: entry.color }}>
        {entry.value}
      </li>
    ))}
  </ul>
);

<Legend content={<CustomLegend />} />
```

### Custom Shapes

**Custom bar shape**:
```jsx
const CustomBar = (props) => {
  const { x, y, width, height, fill } = props;
  return <path d={`M${x},${y} ...`} fill={fill} />;
};

<Bar shape={<CustomBar />} dataKey="sales" />
// OR
<Bar shape={(props) => <CustomBar {...props} />} dataKey="sales" />
```

### Custom Labels

```jsx
<Line 
  dataKey="sales" 
  label={{ position: 'top', fill: '#666', fontSize: 12 }}
/>

// Custom label component
<Line 
  dataKey="sales" 
  label={<CustomLabel />}
/>
```

### Styling

**Chart styles**:
```jsx
<LineChart style={{ backgroundColor: '#f5f5f5' }}>
```

**Axis styling**:
```jsx
<XAxis 
  axisLine={{ stroke: '#666' }}
  tickLine={{ stroke: '#666' }}
  tick={{ fill: '#666', fontSize: 12 }}
/>
```

**Grid styling**:
```jsx
<CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
```

## Interactions

### Active Elements and Interaction Control

The `Tooltip` component controls active element highlighting. Do not use `activeIndex` prop (removed in v3).

**Tooltip interaction props**:
- `defaultIndex`: Sets initial highlighted item on render
- `active`: If true, tooltip remains active after interaction ends
- `trigger`: `"hover"` (default) or `"click"` for click-based interaction
- `content`: Custom content or `() => null` to hide tooltip text while keeping highlight
- `cursor`: Visual cursor in plot area, set to `false` to hide

```jsx
{/* Click-based interaction with hidden tooltip text */}
<Tooltip trigger="click" content={() => null} cursor={false} />

{/* Default highlighted item on render */}
<Tooltip defaultIndex={2} />
```

### Click Events

```jsx
<LineChart onClick={(e) => console.log(e)}>
  <Bar 
    dataKey="sales" 
    onClick={(data, index) => console.log('Bar clicked:', data)}
  />
</LineChart>
```

### Synchronized Charts

Link multiple charts with `syncId`:

```jsx
<LineChart data={data1} syncId="anyId">
  {/* components */}
</LineChart>

<LineChart data={data2} syncId="anyId">
  {/* components - tooltips synchronize */}
</LineChart>
```

### Brush for Zooming

```jsx
<LineChart data={data}>
  {/* other components */}
  <Brush dataKey="name" height={30} stroke="#8884d8" />
</LineChart>
```

## Performance Optimization

### 1. Stable References

Use `useMemo` and `useCallback` for props:

```jsx
// BAD - new function on every render
<Line dataKey={(entry) => entry.sales * 2} />

// GOOD - stable reference
const dataKey = useCallback((entry) => entry.sales * 2, []);
<Line dataKey={dataKey} />
```

### 2. Memoize Components

```jsx
const MemoizedChart = React.memo(({ data }) => (
  <LineChart data={data}>
    {/* components */}
  </LineChart>
));
```

### 3. Isolate Changing Components

Separate frequently updating components:

```jsx
const Chart = () => {
  const [hoveredData, setHoveredData] = useState(null);
  
  return (
    <LineChart>
      {/* Static components */}
      <Line dataKey="sales" />
      
      {/* Dynamic overlay */}
      <ReferenceLine x={hoveredData?.x} stroke="red" />
    </LineChart>
  );
};
```

### 4. Debounce Events

```jsx
import { useDebouncedCallback } from 'use-debounce';

const handleMouseMove = useDebouncedCallback((e) => {
  setPosition(e.activeLabel);
}, 10);

<LineChart onMouseMove={handleMouseMove}>
```

### 5. Reduce Data Points

For large datasets, consider aggregation:

```jsx
// Bin data before rendering
const binnedData = useMemo(() => {
  return d3.bin().value(d => d.x)(rawData);
}, [rawData]);
```

## Accessibility

Recharts includes built-in accessibility support:

```jsx
<LineChart accessibilityLayer={true}>
  <Line dataKey="sales" name="Monthly Sales" />
</LineChart>
```

**Accessibility is enabled by default**. The chart is keyboard navigable and screen reader compatible.

**ARIA props**:
```jsx
<LineChart role="img" aria-label="Sales chart showing monthly revenue">
```

## Common Patterns

### Multiple Data Series

```jsx
<LineChart data={data}>
  <XAxis dataKey="month" />
  <YAxis />
  <Tooltip />
  <Legend />
  <Line type="monotone" dataKey="productA" name="Product A" stroke="#8884d8" />
  <Line type="monotone" dataKey="productB" name="Product B" stroke="#82ca9d" />
  <Line type="monotone" dataKey="productC" name="Product C" stroke="#ffc658" />
</LineChart>
```

### Horizontal Bar Chart

```jsx
<BarChart layout="vertical" data={data}>
  <XAxis type="number" />
  <YAxis type="category" dataKey="name" />
  <Bar dataKey="value" />
</BarChart>
```

### Donut Chart

```jsx
const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

<PieChart>
  <Pie
    data={data}
    innerRadius={60}
    outerRadius={80}
    paddingAngle={5}
    dataKey="value"
    shape={(props) => <Sector {...props} fill={COLORS[props.index % COLORS.length]} />}
  />
</PieChart>
```

> **Note**: `Cell` component is deprecated and will be removed in Recharts 4.0. Use the `shape` prop on `Bar`, `Pie`, `Scatter`, etc. instead.

### Reference Lines/Areas

```jsx
<LineChart data={data}>
  {/* ... */}
  <ReferenceLine y={5000} label="Target" stroke="red" strokeDasharray="3 3" />
  <ReferenceArea x1="Jan" x2="Mar" fill="#8884d8" fillOpacity={0.1} />
</LineChart>
```

### Error Bars

```jsx
<ScatterChart>
  <Scatter data={data}>
    <ErrorBar dataKey="errorX" width={4} strokeWidth={2} />
    <ErrorBar dataKey="errorY" width={4} strokeWidth={2} direction="y" />
  </Scatter>
</ScatterChart>
```

## Integration Patterns

### With State Management

```jsx
const SalesChart = () => {
  const [timeRange, setTimeRange] = useState('month');
  const data = useSelector(state => selectSalesData(state, timeRange));
  
  return (
    <ResponsiveContainer>
      <LineChart data={data}>
        {/* components */}
      </LineChart>
    </ResponsiveContainer>
  );
};
```

### With Real-time Data

```jsx
const RealtimeChart = () => {
  const [data, setData] = useState([]);
  
  useEffect(() => {
    const interval = setInterval(() => {
      setData(prev => [...prev.slice(-20), newDataPoint]);
    }, 1000);
    return () => clearInterval(interval);
  }, []);
  
  return (
    <LineChart data={data}>
      <XAxis dataKey="time" />
      <YAxis domain={['auto', 'auto']} />
      <Line type="monotone" dataKey="value" isAnimationActive={false} />
    </LineChart>
  );
};
```

## Z-Index and Layering (v3.4+)

Components render in a default order (grid < axes < chart elements < tooltip/legend). Override with `zIndex` prop:

```jsx
<Line dataKey="sales" zIndex={10} />  // Render on top
```

For components without direct `zIndex` support, wrap in `ZIndexLayer`:

```jsx
import { ZIndexLayer } from 'recharts';

<ZIndexLayer zIndex={5}>
  <CustomAnnotation />
</ZIndexLayer>
```

## Coordinate Systems

Recharts has three coordinate systems:

1. **Domain coordinates** - Data values (e.g., `x="March"`, `y=5000`). Used by `ReferenceLine`, `ReferenceDot`, `ReferenceArea`. Automatically converted to pixels.
2. **Pixel coordinates** - Positions relative to chart viewBox. Used for custom SVG shapes. Access via `usePlotArea()`, `useOffset()`, `useChartWidth()` hooks.
3. **Mouse event coordinates** - Browser viewport coordinates. Convert with `getRelativeCoordinate(event, element)`.

**Converting between systems**:
- Data to pixels: `useXAxisScale()`, `useYAxisScale()`
- Pixels to data: `useXAxisInverseScale()`, `useYAxisInverseScale()`

## Troubleshooting

### Chart Not Rendering

- Ensure `ResponsiveContainer` has a parent with defined dimensions
- Check that height is a number (not percentage in ResponsiveContainer)
- Verify data is an array of objects

### Tooltip Not Showing

- Ensure Tooltip component is included
- Check that dataKey values exist in data objects

### Axis Labels Overlapping

- Rotate labels: `<XAxis angle={-45} textAnchor="end" height={80} />`
- Use interval: `<XAxis interval={0} />` (0 = show all, 'preserveStartEnd' = auto)

### Animation Issues

- Disable: `<Line isAnimationActive={false} />`
- Reduce duration: `<Line animationDuration={500} />`

## Resources

### References

- **[API Reference](references/api_reference.md)** - Complete component props and API details
- **[Examples](references/examples.md)** - Common chart patterns and code snippets
- **[Best Practices](references/best_practices.md)** - Performance and design guidelines

### External Resources

- [Official Documentation](https://recharts.github.io/en-US/)
- [Storybook](https://recharts.github.io/en-US/storybook/)
- [GitHub](https://github.com/recharts/recharts)
