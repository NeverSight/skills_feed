---
name: infographic-generator-p5
description: This skill generates an interactive infographic visualization using p5.js that read vis-network compatible JSON data. Use this skill when creating educational infographics with nodes, edges, and hover interactions where users can explore relationships between concepts. Each infographic displays shapes with labels, shows tooltips on hover, and displays detailed descriptions in a control panel below the drawing area. The nodes are placed in absolute coordinates.  The output is not a responsive design.
---
# Infographic Generator with P5.js

## Overview

Generate interactive educational infographics using p5.js that visualize relationships between concepts through nodes and edges. Infographics are data-driven visualizations that read from JSON files in vis-network format, allowing users to hover over elements to see a short definition in a tooltip and detailed information with links below the drawing area.

## Purpose

Infographics transform complex concept relationships into visual, explorable diagrams. Unlike MicroSims which focus on simulation and interaction controls, infographics emphasize information display and exploration through hover interactions. The control region is dedicated exclusively to displaying detailed information about the currently hovered item.

## When to Use This Skill

Use this skill when:

- Creating concept maps, mind maps, or knowledge graphs
- Visualizing relationships between topics, ideas, or entities
- Building interactive diagrams for educational content
- Converting vis-network data into standalone p5.js visualizations with enhanced behaviors
- Creating hover and click through based information exploration interfaces

## When to Avoid This Skill

- When you want a fully responsive design that keeps the items in the center regardless of the container size
- When you have complex diagrams where the edges that connect the concepts must be routed using curves and multiple points in a path description

## Key Differences from MicroSim

1. **Control Region Purpose**: The control area ONLY displays details of the hovered item (no sliders, buttons, or other controls)
2. **Data-Driven**: Reads node and edge data from `data.json` file
3. **Interaction Model**: Primarily hover-based exploration rather than parameter manipulation
4. **Layout**: Nodes have fixed positions defined in the data file

## Development Process

### Step 1: Define Infographic Requirements

Gather the following information:

1. **Subject Area**: What topic does this infographic visualize?
2. **Audience Level**: Elementary, Middle School, High School, Undergraduate, Graduate
3. **Node Types**: What categories/groups of nodes exist?
4. **Relationships**: What do the edges represent?
5. **Data Source**: Where will the node/edge data come from?

### Step 2: Prepare Data File (data.json)

Create a JSON file following the vis-network format with metadata, groups, nodes, and edges:

```json
{
  "metadata": {
    "title": "Topic Overview",
    "description": "An interactive infographic showing relationships between concepts",
    "author": "Your Name",
    "created": "2025-01-09"
  },
  "groups": {
    "foundation": {
      "color": "#FF6B6B",
      "borderColor": "#C92A2A",
      "shape": "ellipse"
    },
    "intermediate": {
      "color": "#4ECDC4",
      "borderColor": "#0B7285",
      "shape": "box"
    }
  },
  "nodes": [
    {
      "id": 1,
      "label": "Concept Name",
      "group": "foundation",
      "x": 100,
      "y": 100,
      "shortDescription": "Brief one-sentence description for tooltip",
      "fullDescription": "Detailed paragraph about this concept. Can include <a href='url'>links</a> and formatting."
    }
  ],
  "edges": [
    {
      "from": 1,
      "to": 2,
      "label": "depends on",
      "color": "#999999",
      "width": 2
    }
  ]
}
```

### Step 3: Generate Infographic Files

Create the following folder structure in `/docs/sims/$INFOGRAPHIC_NAME/`:

```
/docs/sims/$INFOGRAPHIC_NAME/
├── index.md              # Documentation page with iframe
├── main.html            # HTML file with p5.js CDN
├── $INFOGRAPHIC_NAME.js # p5.js JavaScript code
└── data.json            # Node and edge data
```

## Technical Architecture

### Canvas Structure (REQUIRED)

Every infographic must have two regions:

1. **Drawing Region** (top): Displays nodes, edges, labels, and tooltips
2. **Detail Display Region** (bottom): Shows full description of hovered item

```javascript
// Canvas dimensions - REQUIRED structure
let canvasWidth = 800;              // Initial width (responsive)
let drawHeight = 600;               // Drawing area height
let controlHeight = 120;            // Detail display area height
let canvasHeight = drawHeight + controlHeight;
let margin = 20;                    // Margin for visual elements
let defaultTextSize = 16;           // Base text size

// Data variables
let infographicData;
let nodes = [];
let edges = [];
let groups = {};
let hoveredNode = null;
let tooltipData = null;

function preload() {
  infographicData = loadJSON('data.json');
}

function setup() {
  updateCanvasSize();
  const canvas = createCanvas(canvasWidth, canvasHeight);
  canvas.parent(document.querySelector('main'));

  // Parse data
  parseData();

  describe('Interactive infographic showing concept relationships', LABEL);
}

function draw() {
  updateCanvasSize();

  // Drawing area background
  fill('aliceblue');
  rect(0, 0, width, drawHeight);

  // Detail display area background
  fill('white');
  rect(0, drawHeight, width, controlHeight);

  // Draw edges first (behind nodes)
  drawEdges();

  // Draw nodes
  drawNodes();

  // Draw tooltip if hovering over a node
  drawTooltip();

  // Draw detail panel for hovered node
  drawDetailPanel();
}
```

### Data Parsing

```javascript
function parseData() {
  // Parse groups
  if (infographicData.groups) {
    groups = infographicData.groups;
  }

  // Parse nodes
  nodes = infographicData.nodes.map(n => ({
    id: n.id,
    label: n.label || '',
    x: n.x || 0,
    y: n.y || 0,
    group: n.group || 'default',
    shortDescription: n.shortDescription || '',
    fullDescription: n.fullDescription || '',
    shape: n.shape || (groups[n.group]?.shape || 'ellipse'),
    color: n.color || (groups[n.group]?.color || '#97C2FC'),
    borderColor: n.borderColor || (groups[n.group]?.borderColor || '#2B7CE9'),
    borderWidth: n.borderWidth || 2,
    size: n.size || 40,
    icon: n.icon || null
  }));

  // Parse edges
  edges = infographicData.edges.map(e => ({
    from: e.from,
    to: e.to,
    label: e.label || '',
    color: e.color || '#848484',
    width: e.width || 1,
    dashes: e.dashes || false,
    smooth: e.smooth || { type: 'continuous', roundness: 0.5 }
  }));
}
```

### Node Drawing

```javascript
function drawNodes() {
  hoveredNode = null;

  for (let node of nodes) {
    // Check if mouse is hovering over this node
    let d = dist(mouseX, mouseY, node.x, node.y);
    let isHovered = d < node.size;

    if (isHovered && mouseY < drawHeight) {
      hoveredNode = node;
    }

    // Draw node shape
    push();
    stroke(node.borderColor);
    strokeWeight(isHovered ? node.borderWidth + 1 : node.borderWidth);
    fill(node.color);

    if (node.shape === 'ellipse' || node.shape === 'circle') {
      ellipse(node.x, node.y, node.size * 2);
    } else if (node.shape === 'box' || node.shape === 'square') {
      rectMode(CENTER);
      rect(node.x, node.y, node.size * 1.8, node.size * 1.8);
    } else if (node.shape === 'diamond') {
      drawDiamond(node.x, node.y, node.size);
    }

    // Draw icon if available
    if (node.icon) {
      // Icon drawing code here
    }

    pop();

    // Draw label
    fill(0);
    noStroke();
    textAlign(CENTER, CENTER);
    textSize(14);
    text(node.label, node.x, node.y + node.size + 15);
  }
}

function drawDiamond(x, y, size) {
  beginShape();
  vertex(x, y - size);           // top
  vertex(x + size, y);           // right
  vertex(x, y + size);           // bottom
  vertex(x - size, y);           // left
  endShape(CLOSE);
}
```

### Edge Drawing

```javascript
function drawEdges() {
  for (let edge of edges) {
    let fromNode = nodes.find(n => n.id === edge.from);
    let toNode = nodes.find(n => n.id === edge.to);

    if (!fromNode || !toNode) continue;

    push();
    stroke(edge.color);
    strokeWeight(edge.width);

    if (edge.dashes) {
      drawingContext.setLineDash([5, 5]);
    }

    // Draw curved or straight line based on smooth parameter
    if (edge.smooth && edge.smooth.type === 'curvedCW') {
      // Draw curved line clockwise
      noFill();
      let controlX = (fromNode.x + toNode.x) / 2 + 50;
      let controlY = (fromNode.y + toNode.y) / 2;
      bezier(fromNode.x, fromNode.y, controlX, controlY,
             controlX, controlY, toNode.x, toNode.y);
    } else {
      // Draw straight line
      line(fromNode.x, fromNode.y, toNode.x, toNode.y);
    }

    drawingContext.setLineDash([]);
    pop();

    // Draw edge label if exists
    if (edge.label) {
      let midX = (fromNode.x + toNode.x) / 2;
      let midY = (fromNode.y + toNode.y) / 2;
      fill(100);
      noStroke();
      textAlign(CENTER, CENTER);
      textSize(12);
      text(edge.label, midX, midY);
    }
  }
}
```

### Tooltip Display (REQUIRED)

Tooltips must always remain visible within the drawing area, even when hovering near edges:

```javascript
function drawTooltip() {
  if (!hoveredNode || mouseY >= drawHeight) return;

  let tooltipText = hoveredNode.shortDescription;
  if (!tooltipText) return;

  // Measure tooltip dimensions
  textSize(14);
  let tooltipWidth = textWidth(tooltipText) + 20;
  let tooltipHeight = 30;
  let padding = 10;

  // Position tooltip near mouse, but keep within drawing bounds
  let tooltipX = mouseX + 15;
  let tooltipY = mouseY - 20;

  // Adjust if tooltip would go off right edge
  if (tooltipX + tooltipWidth > width - padding) {
    tooltipX = mouseX - tooltipWidth - 15;
  }

  // Adjust if tooltip would go off left edge
  if (tooltipX < padding) {
    tooltipX = padding;
  }

  // Adjust if tooltip would go off top edge
  if (tooltipY < padding) {
    tooltipY = mouseY + 20;
  }

  // Adjust if tooltip would go off bottom of drawing area
  if (tooltipY + tooltipHeight > drawHeight - padding) {
    tooltipY = drawHeight - tooltipHeight - padding;
  }

  // Draw tooltip background
  push();
  fill(255, 255, 220);
  stroke(150);
  strokeWeight(1);
  rect(tooltipX, tooltipY, tooltipWidth, tooltipHeight, 5);

  // Draw tooltip text
  fill(0);
  noStroke();
  textAlign(LEFT, CENTER);
  textSize(14);
  text(tooltipText, tooltipX + 10, tooltipY + tooltipHeight / 2);
  pop();
}
```

### Detail Panel Display (REQUIRED)

The control region exclusively displays the full description of the hovered item:

```javascript
function drawDetailPanel() {
  push();
  fill(0);
  noStroke();
  textAlign(LEFT, TOP);
  textSize(defaultTextSize);

  let panelX = margin;
  let panelY = drawHeight + 10;
  let panelWidth = width - 2 * margin;

  if (hoveredNode) {
    // Display node label as header
    textSize(18);
    textStyle(BOLD);
    text(hoveredNode.label, panelX, panelY);

    // Display full description
    textSize(defaultTextSize);
    textStyle(NORMAL);

    // Note: p5.js doesn't render HTML, so strip tags for display
    let displayText = hoveredNode.fullDescription.replace(/<[^>]*>/g, '');

    // Wrap text to fit panel width
    let words = displayText.split(' ');
    let line = '';
    let y = panelY + 25;

    for (let word of words) {
      let testLine = line + word + ' ';
      if (textWidth(testLine) > panelWidth && line.length > 0) {
        text(line, panelX, y);
        line = word + ' ';
        y += 20;
      } else {
        line = testLine;
      }
    }
    text(line, panelX, y);
  } else {
    // Default message when nothing is hovered
    textStyle(ITALIC);
    fill(100);
    text('Hover over a concept to see details...', panelX, panelY);
  }

  pop();
}
```

### Responsive Design (REQUIRED)

```javascript
function windowResized() {
  updateCanvasSize();
  resizeCanvas(canvasWidth, canvasHeight);
}

function updateCanvasSize() {
  const container = document.querySelector('main');
  if (container) {
    canvasWidth = container.offsetWidth;
  }
}
```

## File Templates

### main.html Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Infographic Title</title>
    <script src="https://cdn.jsdelivr.net/npm/p5@1.11.10/lib/p5.js"></script>
    <style>
        body {
            margin: 0px;
            padding: 0px;
            font-family: Arial, Helvetica, sans-serif;
        }
    </style>
    <script src="infographic-name.js"></script>
</head>
<body>
    <main></main>
    <br/>
    <a href=".">Back to Documentation</a>
</body>
</html>
```

### index.md Template

```markdown
---
title: Infographic Title
description: Brief description of the infographic content
---

# Infographic Title

<iframe src="main.html" height="722px" scrolling="no"></iframe>

[View Fullscreen](./main.html){ .md-button .md-button--primary }

## Description

[Description of what this infographic visualizes]

## How to Use

1. **Hover** over any concept to see a brief description
2. **Read** the detailed information in the panel below the diagram
3. **Explore** the relationships shown by the connecting lines

## Legend

[Explanation of colors, shapes, and edge types]
```

## Data Format Specification

### Node Properties

Each node in the `nodes` array supports these properties:

- **id** (required): Unique integer identifier
- **label** (required): Display text (max 30 characters recommended)
- **x** (required): Horizontal position in pixels
- **y** (required): Vertical position in pixels
- **shortDescription** (required): One-sentence tooltip text (no HTML)
- **fullDescription** (required): Detailed paragraph (can include HTML links)
- **group** (optional): Group identifier for styling
- **shape** (optional): 'ellipse', 'box', 'diamond', 'circle', 'square'
- **color** (optional): Fill color (hex or named color)
- **borderColor** (optional): Border color
- **borderWidth** (optional): Border thickness in pixels
- **size** (optional): Node radius/size in pixels
- **icon** (optional): Icon identifier (future use)

### Edge Properties

Each edge in the `edges` array supports these properties:

- **from** (required): Source node ID
- **to** (required): Target node ID
- **label** (optional): Text label for the edge
- **color** (optional): Edge color (default: '#999999')
- **width** (optional): Line thickness (default: 1)
- **dashes** (optional): Boolean for dashed line (default: false)
- **smooth** (optional): Object with type and roundness for curved edges

### Group Properties

Groups define default styling for node categories:

- **color**: Default fill color for nodes in this group
- **borderColor**: Default border color
- **shape**: Default shape type

## Quality Standards

Every infographic must meet these criteria:

- ✅ Loads and parses data.json without errors
- ✅ All nodes are visible and properly positioned
- ✅ Tooltips remain within drawing bounds
- ✅ Detail panel displays full descriptions correctly
- ✅ Responsive design adapts to container width
- ✅ Clear visual hierarchy and readable labels
- ✅ Edges don't obscure important information

## Deployment

After generating the infographic files:

1. Place the folder in `/docs/sims/$INFOGRAPHIC_NAME/`
2. Update `mkdocs.yml` navigation to include the new infographic
3. Test locally with `mkdocs serve`
4. Deploy with `mkdocs gh-deploy`

## Common Use Cases

### Concept Maps
Show relationships between educational concepts with hierarchical or network structures.

### Timeline Visualizations
Display historical events or process steps as connected nodes.

### System Diagrams
Visualize components and their relationships in complex systems.

### Knowledge Graphs
Create explorable networks of related topics or ideas.

## Areas for Extension

- make the design responsive
- allow items to be placed relative to other items (above, below, right-of, left-of)
- create animated lines between items to show flows

## References

This skill uses vis-network compatible data formats. For detailed parameter documentation, see `references/vis-network-parameters.md`.

Template files are available in `assets/` for quick start:
- `assets/template-main.html`
- `assets/template-infographic.js`
- `assets/template-data.json`
