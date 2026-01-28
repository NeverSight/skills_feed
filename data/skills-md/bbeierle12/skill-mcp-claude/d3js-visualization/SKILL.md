---
name: d3js-visualization
description: Create D3.js charts and interactive data visualizations. Use when building bar charts, line charts, scatter plots, pie charts, force-directed graphs, geographic maps, or any custom data visualization.
---

# D3.js Visualization

## Core Concepts

### Selection and Data Binding
```javascript
// Select elements
const svg = d3.select('#chart')
  .append('svg')
  .attr('width', width)
  .attr('height', height);

// Bind data to elements
svg.selectAll('rect')
  .data(data)
  .join('rect')
  .attr('x', (d, i) => i * barWidth)
  .attr('y', d => height - scale(d.value))
  .attr('width', barWidth - 1)
  .attr('height', d => scale(d.value));
```

### Scales
```javascript
// Linear scale (continuous → continuous)
const xScale = d3.scaleLinear()
  .domain([0, d3.max(data, d => d.value)])
  .range([0, width]);

// Band scale (discrete → continuous)
const xScale = d3.scaleBand()
  .domain(data.map(d => d.name))
  .range([0, width])
  .padding(0.1);

// Time scale
const xScale = d3.scaleTime()
  .domain([startDate, endDate])
  .range([0, width]);

// Color scale
const colorScale = d3.scaleOrdinal(d3.schemeCategory10);
```

### Axes
```javascript
// Create axes
const xAxis = d3.axisBottom(xScale);
const yAxis = d3.axisLeft(yScale);

// Append to SVG
svg.append('g')
  .attr('class', 'x-axis')
  .attr('transform', `translate(0, ${height})`)
  .call(xAxis);

svg.append('g')
  .attr('class', 'y-axis')
  .call(yAxis);
```

## Common Chart Types

### Bar Chart
```javascript
function createBarChart(data, container, options = {}) {
  const {
    width = 600,
    height = 400,
    margin = { top: 20, right: 20, bottom: 30, left: 40 }
  } = options;

  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  const svg = d3.select(container)
    .append('svg')
    .attr('width', width)
    .attr('height', height);

  const g = svg.append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`);

  const xScale = d3.scaleBand()
    .domain(data.map(d => d.name))
    .range([0, innerWidth])
    .padding(0.1);

  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.value)])
    .nice()
    .range([innerHeight, 0]);

  // Bars
  g.selectAll('.bar')
    .data(data)
    .join('rect')
    .attr('class', 'bar')
    .attr('x', d => xScale(d.name))
    .attr('y', d => yScale(d.value))
    .attr('width', xScale.bandwidth())
    .attr('height', d => innerHeight - yScale(d.value))
    .attr('fill', 'steelblue');

  // Axes
  g.append('g')
    .attr('transform', `translate(0,${innerHeight})`)
    .call(d3.axisBottom(xScale));

  g.append('g')
    .call(d3.axisLeft(yScale));

  return svg.node();
}
```

### Line Chart
```javascript
function createLineChart(data, container, options = {}) {
  const {
    width = 600,
    height = 400,
    margin = { top: 20, right: 20, bottom: 30, left: 40 }
  } = options;

  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  const svg = d3.select(container)
    .append('svg')
    .attr('width', width)
    .attr('height', height);

  const g = svg.append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`);

  const xScale = d3.scaleTime()
    .domain(d3.extent(data, d => d.date))
    .range([0, innerWidth]);

  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.value)])
    .nice()
    .range([innerHeight, 0]);

  // Line generator
  const line = d3.line()
    .x(d => xScale(d.date))
    .y(d => yScale(d.value))
    .curve(d3.curveMonotoneX);

  // Path
  g.append('path')
    .datum(data)
    .attr('fill', 'none')
    .attr('stroke', 'steelblue')
    .attr('stroke-width', 2)
    .attr('d', line);

  // Dots
  g.selectAll('.dot')
    .data(data)
    .join('circle')
    .attr('class', 'dot')
    .attr('cx', d => xScale(d.date))
    .attr('cy', d => yScale(d.value))
    .attr('r', 4)
    .attr('fill', 'steelblue');

  // Axes
  g.append('g')
    .attr('transform', `translate(0,${innerHeight})`)
    .call(d3.axisBottom(xScale));

  g.append('g')
    .call(d3.axisLeft(yScale));

  return svg.node();
}
```

### Pie/Donut Chart
```javascript
function createPieChart(data, container, options = {}) {
  const {
    width = 400,
    height = 400,
    innerRadius = 0, // 0 for pie, > 0 for donut
  } = options;

  const radius = Math.min(width, height) / 2;

  const svg = d3.select(container)
    .append('svg')
    .attr('width', width)
    .attr('height', height);

  const g = svg.append('g')
    .attr('transform', `translate(${width / 2},${height / 2})`);

  const color = d3.scaleOrdinal(d3.schemeCategory10);

  const pie = d3.pie()
    .value(d => d.value)
    .sort(null);

  const arc = d3.arc()
    .innerRadius(innerRadius)
    .outerRadius(radius - 10);

  const arcs = g.selectAll('.arc')
    .data(pie(data))
    .join('g')
    .attr('class', 'arc');

  arcs.append('path')
    .attr('d', arc)
    .attr('fill', d => color(d.data.name));

  arcs.append('text')
    .attr('transform', d => `translate(${arc.centroid(d)})`)
    .attr('text-anchor', 'middle')
    .text(d => d.data.name);

  return svg.node();
}
```

## Interactivity

### Tooltips
```javascript
// Create tooltip
const tooltip = d3.select('body')
  .append('div')
  .attr('class', 'tooltip')
  .style('position', 'absolute')
  .style('visibility', 'hidden')
  .style('background', 'white')
  .style('padding', '10px')
  .style('border-radius', '4px')
  .style('box-shadow', '0 2px 4px rgba(0,0,0,0.2)');

// Add to elements
bars.on('mouseover', function(event, d) {
    tooltip
      .style('visibility', 'visible')
      .html(`<strong>${d.name}</strong><br/>Value: ${d.value}`);
  })
  .on('mousemove', function(event) {
    tooltip
      .style('top', (event.pageY - 10) + 'px')
      .style('left', (event.pageX + 10) + 'px');
  })
  .on('mouseout', function() {
    tooltip.style('visibility', 'hidden');
  });
```

### Transitions
```javascript
// Animate on data update
bars.transition()
  .duration(750)
  .attr('y', d => yScale(d.value))
  .attr('height', d => innerHeight - yScale(d.value));

// Staggered animation
bars.transition()
  .delay((d, i) => i * 50)
  .duration(500)
  .attr('opacity', 1);
```

### Zoom and Pan
```javascript
const zoom = d3.zoom()
  .scaleExtent([1, 8])
  .on('zoom', (event) => {
    g.attr('transform', event.transform);
  });

svg.call(zoom);
```

## Best Practices

### Performance
- Use `join()` instead of enter/update/exit for cleaner code
- Throttle resize handlers
- Use CSS for simple styling
- Avoid excessive DOM updates

### Accessibility
- Add `aria-label` to SVG
- Use `role="img"` for decorative charts
- Provide data tables as alternatives
- Ensure sufficient color contrast

### Data Formatting
```javascript
// Parse dates
const parseDate = d3.timeParse('%Y-%m-%d');
data.forEach(d => {
  d.date = parseDate(d.dateString);
});

// Format numbers
const formatNumber = d3.format(',.0f');
const formatCurrency = d3.format('$,.2f');
const formatPercent = d3.format('.1%');
```
