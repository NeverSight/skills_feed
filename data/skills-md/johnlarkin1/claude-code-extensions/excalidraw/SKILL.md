---
name: excalidraw
description: Generate Excalidraw diagrams (.excalidraw JSON files) for whiteboarding, flowcharts, architecture diagrams, sequence diagrams, mind maps, wireframes, and org charts. Use when user requests diagrams, visual documentation, system architecture visualization, process flows, or any hand-drawn style diagram. Triggers on requests mentioning Excalidraw, diagram creation, flowcharts, architecture diagrams, sequence diagrams, wireframes, or visual documentation.
---

# Excalidraw Diagram Generation

Generate `.excalidraw` JSON files that open directly in Excalidraw.

## Quick Start

Minimal valid file:
```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [],
  "appState": { "viewBackgroundColor": "#ffffff" },
  "files": {}
}
```

## Workflow

1. Identify diagram type (flowchart, architecture, sequence, mind map, wireframe, org chart)
2. Plan element layout with consistent spacing (use 20px grid)
3. Generate elements with unique IDs and proper bindings
4. Write complete JSON to `.excalidraw` file

## Element Patterns

### Shape with Label

Always bind text to container bidirectionally:
```json
// Rectangle
{
  "type": "rectangle",
  "id": "box_1",
  "x": 100, "y": 100, "width": 150, "height": 60,
  "backgroundColor": "#a5d8ff",
  "boundElements": [{ "id": "text_1", "type": "text" }],
  ...baseProps
}
// Bound text
{
  "type": "text",
  "id": "text_1",
  "containerId": "box_1",
  "textAlign": "center",
  "verticalAlign": "middle",
  ...textProps
}
```

### Connected Arrow

Update both arrow and shapes:
```json
// Arrow
{
  "type": "arrow",
  "id": "arrow_1",
  "points": [[0, 0], [150, 0]],
  "startBinding": { "elementId": "box_1", "fixedPoint": [1.0, 0.5001], "mode": "orbit" },
  "endBinding": { "elementId": "box_2", "fixedPoint": [0.0, 0.5001], "mode": "orbit" },
  "endArrowhead": "arrow",
  ...baseProps
}
// Both shapes need boundElements updated
"boundElements": [{ "id": "arrow_1", "type": "arrow" }]
```

## Diagram-Specific Patterns

**Flowchart:** Ellipse (start/end), Rectangle (process), Diamond (decision), vertical flow with 70px gaps

**Sequence Diagram:** Rectangles (actors) at top, dashed vertical lines (lifelines), horizontal arrows (messages)

**Architecture:** Rectangles with rounded corners, group related components, use frames for boundaries

**Mind Map:** Central ellipse, radiating lines to topic rectangles, organic layout

**Org Chart:** Rectangles with hierarchy, lines (not arrows) for connections

## Critical Rules

1. **Bidirectional bindings** - When arrow connects to shape, update BOTH:
   - Arrow's `startBinding`/`endBinding`
   - Shape's `boundElements` array

2. **fixedPoint precision** - Use `0.5001` not `0.5` to avoid floating point issues

3. **Unique IDs** - Every element needs unique `id`

4. **Calculate width/height** for lines/arrows from points array

5. **Required base properties** for every element:
   ```
   id, type, x, y, width, height, angle, strokeColor, backgroundColor,
   fillStyle, strokeWidth, strokeStyle, roughness, opacity, roundness,
   seed, version, versionNonce, isDeleted, updated, groupIds, frameId,
   boundElements, link, locked, index
   ```

## Common Values

**Colors:**
- Stroke: `#1e1e1e` (black), `#e03131` (red), `#2f9e44` (green), `#1971c2` (blue)
- Background: `#a5d8ff` (blue), `#b2f2bb` (green), `#ffec99` (yellow), `#ffc9c9` (red), `#d0bfff` (purple)

**Defaults:**
- `strokeWidth`: 2
- `roughness`: 1 (hand-drawn), 0 (smooth for text)
- `opacity`: 100
- `fontFamily`: 5 (Excalifont)
- `fontSize`: 20
- `seed`: any random integer
- `version`: 1, `versionNonce`: 0
- `index`: "a0", "a1", "a2"...

## Reference

See [references/format-spec.md](references/format-spec.md) for complete element schemas, all property values, and detailed examples.
