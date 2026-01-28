---
name: excalidraw
description: Create Excalidraw diagrams as JSON files for flowcharts, user journeys, system architectures, wireframes, and visual documentation. Use when the user asks to create diagrams, flowcharts, visual representations, architecture diagrams, mind maps, or any Excalidraw-compatible visualizations. Outputs .excalidraw.json files that can be opened in excalidraw.com or any Excalidraw-compatible app.
---

# Excalidraw Diagram Generator

Create Excalidraw-compatible JSON diagrams. Output `.excalidraw.json` files.

## JSON Schema

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [],
  "appState": {
    "gridSize": null,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

## Coordinate System

- **Origin**: Top-left corner (0, 0)
- **X-axis**: Increases rightward
- **Y-axis**: Increases downward
- **Unit**: Pixels

## Grid-Based Layout System

Use a 20px grid for alignment. Standard positions:

```
GRID_UNIT = 20
COLUMN_WIDTH = 200    # Element + gap
ROW_HEIGHT = 150      # Element + gap

Position formula:
  x = START_X + (column * COLUMN_WIDTH)
  y = START_Y + (row * ROW_HEIGHT)

Recommended START_X = 50, START_Y = 100
```

### Standard Element Sizes

| Element | Width | Height | Use Case |
|---------|-------|--------|----------|
| Small box | 120 | 60 | Labels, simple steps |
| Standard box | 160 | 80 | Process steps |
| Large box | 200 | 100 | Detailed nodes |
| Wide box | 240 | 80 | Long text |
| Diamond | 100 | 100 | Decision points |
| Circle | 80 | 80 | Start/End nodes |
| Icon circle | 90 | 80 | With emoji |

## Text Centering Formula

**CRITICAL**: To center text inside a shape:

```
text_x = shape_x + (shape_width - text_width) / 2
text_y = shape_y + (shape_height - text_height) / 2
```

### Text Size Reference

| Font Size | Char Width | Line Height | Use |
|-----------|------------|-------------|-----|
| 11 | ~6px | 15px | Labels, annotations |
| 12 | ~7px | 16px | Secondary text |
| 14 | ~8px | 18px | Body text |
| 16 | ~9px | 20px | Primary text |
| 18 | ~10px | 24px | Headings |
| 20 | ~11px | 26px | Titles |
| 28 | ~16px | 35px | Icons/Emoji |

**Estimate text_width**: `char_count * char_width`
**Estimate text_height**: `line_count * line_height`

### Centering Example

```
Shape: x=100, y=100, width=160, height=80
Text: "Process" (7 chars), fontSize=16

text_width = 7 * 9 = 63
text_height = 1 * 20 = 20
text_x = 100 + (160 - 63) / 2 = 148.5 ≈ 148
text_y = 100 + (80 - 20) / 2 = 130
```

## Element Types

### Common Properties (required for all)

```json
{
  "id": "unique-id",
  "type": "rectangle",
  "x": 100,
  "y": 100,
  "width": 160,
  "height": 80,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "roughness": 1,
  "opacity": 100,
  "angle": 0,
  "seed": 100,
  "version": 1,
  "isDeleted": false,
  "boundElements": null,
  "link": null,
  "locked": false
}
```

### Type-Specific Properties

**Rectangle**: Add `"roundness": {"type": 3}` for rounded corners

**Text**:
```json
{
  "type": "text",
  "text": "Content\nLine 2",
  "fontSize": 16,
  "fontFamily": 1,
  "textAlign": "center",
  "verticalAlign": "middle"
}
```
- fontFamily: 1=Virgil (hand), 2=Helvetica, 3=Cascadia (mono)

**Arrow/Line**:
```json
{
  "type": "arrow",
  "points": [[0, 0], [100, 0]],
  "startArrowhead": null,
  "endArrowhead": "arrow"
}
```
- Points are relative to element's x,y
- Arrowheads: `null`, `"arrow"`, `"bar"`, `"dot"`, `"triangle"`

## Arrow Positioning

### Horizontal Arrow (Left to Right)
```
From shape at (x1, y1, w1, h1) to shape at (x2, y2, w2, h2):

arrow_x = x1 + w1           # Right edge of source
arrow_y = y1 + h1/2         # Vertical center
gap = x2 - (x1 + w1)        # Space between shapes
points = [[0, 0], [gap, 0]]
```

### Vertical Arrow (Top to Bottom)
```
arrow_x = x1 + w1/2         # Horizontal center
arrow_y = y1 + h1           # Bottom edge of source
gap = y2 - (y1 + h1)
points = [[0, 0], [0, gap]]
```

### Diagonal/Curved Arrow
```
points = [[0, 0], [dx/2, dy], [dx, dy]]  # Curved path
```

## Color Palette

| Color | Stroke | Background | Use |
|-------|--------|------------|-----|
| Blue | #1971c2 | #a5d8ff | Primary, info |
| Green | #2f9e44 | #b2f2bb | Success, start |
| Orange | #e8590c | #ffc9c9 | Warning, action |
| Red | #e03131 | #ffc9c9 | Error, end |
| Purple | #9c36b5 | #eebefa | Special, loop |
| Yellow | #f08c00 | #ffec99 | Highlight |
| Teal | #099268 | #96f2d7 | Secondary |
| Gray | #868e96 | #dee2e6 | Neutral, labels |
| Black | #1e1e1e | - | Text, borders |

## Z-Order (Element Array Order)

Elements render in array order. First = back, last = front.

**Correct order:**
1. Background shapes (containers, frames)
2. Connection lines/arrows
3. Foreground shapes (nodes, boxes)
4. Text labels
5. Icons/overlays

## Layout Patterns

### Horizontal Flow (Left to Right)

```
COL_GAP = 60  # Gap between elements

Element 1: x=50,  y=100, w=160, h=80
Arrow 1:   x=210, y=140, points=[[0,0],[60,0]]
Element 2: x=270, y=100, w=160, h=80
Arrow 2:   x=430, y=140, points=[[0,0],[60,0]]
Element 3: x=490, y=100, w=160, h=80
```

### Vertical Flow (Top to Bottom)

```
ROW_GAP = 50

Element 1: x=100, y=50,  w=160, h=80
Arrow 1:   x=180, y=130, points=[[0,0],[0,50]]
Element 2: x=100, y=180, w=160, h=80
```

### Decision Branch (Diamond)

```
Diamond:    x=300, y=200, w=100, h=100
Center:     (350, 250)

Yes path (up-right):
  arrow_x=350, arrow_y=200
  points=[[0,0], [0,-50], [100,-50]]

No path (down-right):
  arrow_x=350, arrow_y=300
  points=[[0,0], [0,50], [100,50]]
```

### Feedback Loop (Return Arrow)

```
From bottom-right back to left:
  Start: (800, 400)
  points=[
    [0, 0],        # Start
    [0, 80],       # Down
    [-400, 80],    # Left
    [-400, -150]   # Up to target
  ]
```

## Complete Node Example

```json
[
  {
    "id": "node1-box",
    "type": "rectangle",
    "x": 100, "y": 100, "width": 160, "height": 80,
    "strokeColor": "#1971c2",
    "backgroundColor": "#a5d8ff",
    "fillStyle": "solid",
    "strokeWidth": 2,
    "roughness": 1,
    "opacity": 100,
    "angle": 0,
    "seed": 100,
    "version": 1,
    "isDeleted": false,
    "boundElements": [{"id": "arrow1", "type": "arrow"}],
    "roundness": {"type": 3},
    "link": null,
    "locked": false
  },
  {
    "id": "node1-text",
    "type": "text",
    "x": 130, "y": 130,
    "width": 100, "height": 20,
    "text": "Process Step",
    "fontSize": 16,
    "fontFamily": 1,
    "textAlign": "center",
    "verticalAlign": "middle",
    "strokeColor": "#1e1e1e",
    "backgroundColor": "transparent",
    "fillStyle": "solid",
    "strokeWidth": 1,
    "roughness": 1,
    "opacity": 100,
    "angle": 0,
    "seed": 101,
    "version": 1,
    "isDeleted": false,
    "boundElements": null,
    "link": null,
    "locked": false
  }
]
```

## Positioning Checklist

Before generating:
1. ☐ Define grid: START_X, START_Y, COLUMN_WIDTH, ROW_HEIGHT
2. ☐ List all elements with row/column positions
3. ☐ Calculate exact x,y using formulas
4. ☐ Calculate text positions using centering formula
5. ☐ Calculate arrow start points and relative endpoints
6. ☐ Order elements correctly for z-order
7. ☐ Assign unique IDs and incrementing seeds

## Templates

- Basic flowchart: `assets/flowchart-template.excalidraw.json`
- Processing loop: `references/processing-loop-template.md`
- Element specs: `references/elements.md`

## Output

1. Save as `.excalidraw.json`
2. Copy to `/mnt/user-data/outputs/`
3. Tell user: "Open at excalidraw.com → Menu → Open"
