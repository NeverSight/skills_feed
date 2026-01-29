---
name: bubble-chart-generator
description: This skill generates interactive Chart.js bubble chart visualizations for priority matrices and multi-dimensional data analysis. Use this skill when users need to create scatter plots with variable bubble sizes, particularly for 2x2 priority matrices (Impact vs Effort, Risk vs Value, etc.), portfolio analysis, or any visualization comparing items across two dimensions with a third dimension represented by size. The skill creates a complete MicroSim package with HTML, CSS, and documentation.
---

# Bubble Chart Generator

## Overview

This skill generates professional, interactive bubble chart visualizations using Chart.js. Bubble charts are ideal for displaying three-dimensional data on a 2D plane: X-axis, Y-axis, and bubble size. The skill creates a complete MicroSim package suitable for embedding in educational content or documentation sites built with MkDocs.

## When to Use This Skill

Use this skill when users request:

- **Priority matrices**: Impact vs Effort, Risk vs Value, Cost vs Benefit
- **Portfolio visualizations**: Comparing items across two dimensions with frequency/count as size
- **Multi-dimensional data**: Any dataset with three key metrics to visualize
- **Quadrant analysis**: Categorizing items into four strategic zones
- **Interactive charts**: Need for hover tooltips, clickable elements, or dynamic data display

Common trigger phrases:
- "Create a bubble chart showing..."
- "Visualize the priority matrix for..."
- "Build an interactive scatter plot with..."
- "Show a 2x2 matrix with bubble sizes representing..."

## Workflow

### Step 1: Understand the Data and Requirements

Before generating the chart, gather information about:

1. **Data structure**: What items need to be visualized?
   - Item names/labels
   - X-axis values and label (e.g., "Effort", "Risk")
   - Y-axis values and label (e.g., "Impact", "Value")
   - Size metric (e.g., "Count", "Cost", "Frequency")
   - Optional: Status/category for color coding

2. **Context**: What is the purpose of the visualization?
   - Educational content
   - Decision-making tool
   - Analysis report
   - Portfolio review

3. **Integration**: Where will the chart be used?
   - Standalone page
   - Embedded in documentation
   - Part of a presentation
   - MkDocs site integration

### Step 2: Create Directory Structure

Create a new directory for the MicroSim following this pattern:

```
docs/sims/<chart-name>/
├── main.html         # Main visualization file
├── style.css         # Styling
└── index.md          # Documentation (if part of MkDocs)
```

**Naming convention**: Use kebab-case (lowercase with hyphens) for directory names that are descriptive and URL-friendly (e.g., `skill-impact-chart`, `portfolio-analysis`, `risk-assessment-matrix`).

### Step 3: Create main.html with Chart.js

Generate the main HTML file with the following structure:

1. **HTML boilerplate** with proper meta tags
2. **Chart.js CDN import**: `https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js`
3. **Canvas element** for the chart
4. **Quadrant analysis section** (optional but recommended)
5. **JavaScript implementation**:
   - Data array with all items
   - Color scheme based on categories/status
   - Bubble size calculation function
   - Chart.js configuration with bubble chart type
   - Custom plugin for quadrant backgrounds and labels
   - Quadrant population logic

**Key Chart.js configuration elements**:

```javascript
// Data structure
const data = [
    { type: 'item-name', count: 10, impact: 6.7, effort: 1, priority: 6.67, status: 'Category' },
    // ... more items
];

// Bubble size scaling
function getBubbleSize(count) {
    const minSize = 8;
    const maxSize = 30;
    return minSize + ((count - minCount) / (maxCount - minCount)) * (maxSize - minSize);
}

// Chart options
{
    type: 'bubble',
    options: {
        aspectRatio: 1.5,
        scales: {
            x: { min: 0, max: 10, title: { text: 'X-Axis Label' } },
            y: { min: 0, max: 10, title: { text: 'Y-Axis Label' } }
        },
        plugins: {
            title: { text: 'Chart Title' },
            tooltip: { /* custom tooltip */ }
        }
    },
    plugins: [
        // Custom plugin for quadrant backgrounds and labels
    ]
}
```

**Important considerations**:

- **Prevent edge clipping**: Add padding or extend scale ranges (e.g., `min: -0.5, max: 10.5`)
- **Quadrant shading**: Use `afterDraw` plugin to add background colors
- **Label positioning**: Position labels above bubbles to avoid overlap
- **Responsive design**: Set appropriate aspect ratio and container height

### Step 4: Create style.css

Generate CSS with professional styling:

1. **Reset and base styles**: Clean defaults for cross-browser consistency
2. **Chart container**: Fixed height (typically 600px), padding, box-shadow
3. **Legend container**: Styling for quadrant analysis section
4. **Quadrant sections**: Individual styling for each priority zone
5. **Interactive elements**: Hover effects, transitions
6. **Responsive design**: Media queries for mobile/tablet
7. **Print styles**: Print-friendly adjustments

**Key design principles**:
- Use clean, modern aesthetics
- Provide clear visual hierarchy
- Add subtle shadows and borders
- Use gradients for quadrant labels
- Include hover effects for engagement
- Ensure accessibility with sufficient contrast

### Step 5: Create index.md Documentation

If the chart is part of a MkDocs site, create comprehensive documentation:

1. **Title and overview**: Brief description of the visualization
2. **Embedded iframe**: Display the chart inline
3  **Link to Fullscreen:** Markdown link to main.html with 
3. **Interpretation guide**: Explain how to read the chart
4. **Features section**: List interactive elements
5. **Customization guide**: Detailed instructions for modifying:
   - Chart margins and layout
   - Bubble sizes
   - Colors (status colors, quadrant backgrounds)
   - Data structure
   - Label positioning
   - Tooltip content
6. **Technical details**: Dependencies, browser compatibility, file structure
7. **Use cases**: Other applications for this pattern
8. **References**: Links to Chart.js docs and related resources

**Documentation structure template**:

```markdown
# [Chart Title]

[Brief description]

## Interactive Chart

<iframe src="main.html" width="100%" height="900" frameborder="0"></iframe>

## Overview

[Detailed explanation of what the chart shows]

## Features

### Interactive Elements
- Hover tooltips
- Labeled bubbles
- Quadrant backgrounds

### Visual Design
- Bubble sizes
- Status colors
- Grid lines

## Customization Guide

### Adjusting Chart Margins and Layout
[Specific code examples]

### Adjusting Bubble Sizes
[Specific code examples]

### Changing Colors
[Specific code examples]

## Technical Details
- Dependencies
- Browser compatibility
- File structure

## Use Cases
[Other applications]
```

### Step 6: Integrate into Navigation (MkDocs)

If using MkDocs, add the chart to the navigation in `mkdocs.yml`:

```yaml
- MicroSims:
    - Introduction: sims/index.md
    - [Chart Name]: sims/[chart-name]/index.md
    - [Other sims...]: ...
```

Place the entry in a logical position based on:
- Related content (group similar visualizations)
- Alphabetical order
- Creation order

### Step 7: Test and Validate

Before considering the chart complete:

1. **Visual testing**:
   - Open `main.html` in a browser directly
   - Test with `mkdocs serve` if applicable
   - Check all breakpoints (desktop, tablet, mobile)
   - Verify no bubbles are clipped at edges
   - Confirm labels are readable and positioned correctly

2. **Interactive testing**:
   - Hover over all bubbles to verify tooltips
   - Check quadrant list population
   - Test on different browsers

3. **Documentation review**:
   - Verify all code examples are accurate
   - Test customization instructions
   - Check all internal links

4. **Data validation**:
   - Confirm all data points are plotted correctly
   - Verify calculations (e.g., priority scores)
   - Check category assignments

## Best Practices

### Data Preparation

1. **Normalize scales**: Use consistent 0-10 scales for comparability
2. **Calculate derived metrics**: Include priority scores or ratios
3. **Categorize logically**: Group items by meaningful status or type
4. **Validate completeness**: Ensure all required fields are present

### Visual Design

1. **Color coding**: Use intuitive colors (green=good, red=caution)
2. **Bubble sizing**: Scale proportionally with clear min/max bounds
3. **Quadrant shading**: Use subtle backgrounds (5-10% opacity)
4. **Label clarity**: Ensure text is always readable against backgrounds
5. **Spacing**: Prevent overlap with appropriate margins

### Documentation

1. **Code examples**: Provide exact line numbers and snippets
2. **Before/after**: Show the effect of customizations
3. **Parameter ranges**: Suggest appropriate value ranges
4. **Common issues**: Address edge clipping, overlap, performance

### MkDocs Integration

1. **Iframe sizing**: Use `height="900"` for full chart visibility
2. **Path references**: Use relative paths (`../sims/...`)
3. **Navigation placement**: Group with related MicroSims
4. **Responsive embedding**: Add border and border-radius for polish

## Common Variations

### Simple Scatter Plot (No Bubbles)
For uniform sizing, set all bubbles to the same radius:

```javascript
function getBubbleSize(count) {
    return 10; // Fixed size
}
```

### Color by Quadrant
Instead of status, color bubbles by their quadrant position:

```javascript
function getQuadrantColor(impact, effort) {
    if (impact > 5 && effort <= 5) return 'green';
    if (impact > 5 && effort > 5) return 'yellow';
    if (impact <= 5 && effort <= 5) return 'lightblue';
    return 'red';
}
```

### Three or More Categories
Expand the color scheme and datasets:

```javascript
const colors = {
    'High': 'rgba(40, 167, 69, 0.8)',
    'Medium': 'rgba(255, 193, 7, 0.8)',
    'Low': 'rgba(220, 53, 69, 0.8)'
};
```

### Time-Series Animation
Add data for multiple time periods and animate transitions (requires additional Chart.js configuration).

## Troubleshooting

### Bubbles Clipped at Edges
**Solution**: Extend scale ranges or add layout padding:
```javascript
scales: {
    x: { min: -0.5, max: 10.5 }
}
```

### Labels Overlapping
**Solution**: Increase label offset or reduce font size:
```javascript
element.y - element.options.radius - 12  // Increase offset
```

### Performance Issues
**Solution**: Reduce data points or disable animations:
```javascript
animation: false
```

### Quadrant Colors Not Showing
**Solution**: Verify the `afterDraw` plugin is registered and `ctx.globalAlpha` is set appropriately (0.05-0.1).

## References

This skill uses the following assets and references:

### Assets
- **Chart.js CDN**: `https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js`
- No local assets required (Chart.js loaded from CDN)

### References
- [Chart.js Documentation](https://www.chartjs.org/docs/latest/)
- [Bubble Chart Guide](https://www.chartjs.org/docs/latest/charts/bubble.html)
- [Chart.js Plugins](https://www.chartjs.org/docs/latest/developers/plugins.html)

### Example Implementation
See the skill-impact-chart example at `/docs/sims/skill-impact-chart/` for a complete reference implementation.
