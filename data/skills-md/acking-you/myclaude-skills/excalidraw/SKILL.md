---
name: excalidraw
description: Generate hand-drawn style diagrams (architecture, flowcharts, system design) as .excalidraw.json files. Use when user wants diagrams, mentions Excalidraw, or needs Mermaid-to-visual conversion.
---

# Excalidraw Diagram Generation

Generate professional hand-drawn style diagrams in Excalidraw JSON format.

## Critical Rules

1. **Arrow Binding (MUST follow)**: Arrows must bind to components bidirectionally:
   - Arrow needs `startBinding` and `endBinding` pointing to component IDs
   - Rectangle needs `boundElements` array listing bound arrow IDs
   - Without both, arrows won't snap to components

2. **Text requires width/height**: Text elements must have `width` and `height` fields, otherwise they won't render

3. **Arrow labels**: Place below arrow (y + 30) or above (y - 30), never overlapping components

4. **Background region sizing (MUST follow)**: Background regions (subgraphs/phases) must fully cover all contained elements:
   - Calculate bounding box: find min/max x/y of ALL elements in the region
   - Add padding: 40px on all sides
   - Formula: `width = (maxX + maxWidth) - minX + 80`, `height = (maxY + maxHeight) - minY + 80`
   - Verify: every child element's bottom-right corner must be inside the region

5. **No overlaps (MUST follow)**: Arrows must not cross unrelated components; labels must not overlap components. See "Layout Optimization" section for strategies.

6. **Container binding (MUST follow)**: When connecting to grouped/nested structures, arrows must bind to the outer container (background region), NOT to internal elements:
   - If a phase/subgraph contains multiple internal steps, arrows from outside should connect to the container box
   - Internal element connections stay internal; external connections go to the container
   - Example: `dag → main-bg` (container), NOT `dag → read-main` (internal element)
   - This keeps the diagram semantically correct and visually clean

7. **Sibling layout (MUST follow)**: Elements at the same hierarchy level must be placed horizontally (same row), NOT vertically:
   - Siblings represent parallel/alternative paths (e.g., TCP and HTTP handlers)
   - Vertical stacking implies sequential execution, which is semantically wrong for siblings
   - Use fork arrows from parent to horizontally-aligned children

8. **Nested structure clarity (MUST follow)**: When a container has internal elements, ensure clear hierarchy and no overlaps:
   - Internal elements must have proper vertical spacing with arrows showing call sequence
   - Text labels must fit entirely within their rectangles (calculate: `rect.height >= text.height + 20`)
   - Reference annotations (file paths, line numbers) go OUTSIDE the box (below or to the right)
   - Sub-containers within a parent should be visually distinct (different opacity or color shade)

9. **Arrow path space reservation (MUST follow)**: When arrows connect nested containers, ensure sufficient space for arrow routing:
   - Problem: If containers are too close, arrows may pass through target containers instead of connecting to their edges
   - Solution: Proactively enlarge parent containers to leave 40-60px gap between child containers and the next target
   - When multiple sub-containers need to merge arrows to a shared target below, calculate: `target.y >= max(child.y + child.height) + 60`
   - If arrow crossing occurs after generation, increase container heights rather than using complex bypass paths

## Mandatory Workflow (MUST follow before writing JSON)

**Step 1: Arrow Path Analysis**
Before placing any component, list ALL arrows and their source→target pairs:
```
Arrow 1: A → B (horizontal)
Arrow 2: B → C (horizontal)
Arrow 3: C → A (return arrow - DANGER: will cross B if horizontal layout)
```

**Step 2: Identify Crossing Risks**
For each arrow, check: "Does a straight line from source to target pass through any other component?"
- If YES → mark as "needs layout adjustment" or "needs bypass path"
- Common patterns that cause crossings:
  - Return arrows in horizontal layouts (e.g., C → A when B is between them)
  - Bidirectional flows between non-adjacent components
  - Hub-and-spoke patterns with central component

**Step 3: Choose Layout Strategy**
Based on crossing risks, select appropriate layout:
- **No crossings**: Use simple horizontal/vertical layout
- **1-2 crossings**: Use bypass paths (multi-point arrows)
- **3+ crossings or complex flows**: Restructure to 2D layout (grid, triangle, diamond)

**Step 4: Verify Before Finalizing**
After generating JSON, mentally trace each arrow path and confirm:
- [ ] No arrow passes through any component it doesn't connect to
- [ ] No label overlaps any component
- [ ] All background regions fully contain their elements

## Core Elements

### Base Template
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

### Element Templates

**Rectangle (Component Box)**
```json
{
  "id": "unique-id",
  "type": "rectangle",
  "x": 100, "y": 100,
  "width": 140, "height": 60,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#a5d8ff",
  "roundness": { "type": 3 },
  "boundElements": [{"id": "arrow-id", "type": "arrow"}]
}
```

**Text** (width/height required, fontFamily: 4 required)
```json
{
  "id": "unique-id",
  "type": "text",
  "x": 120, "y": 120,
  "width": 80, "height": 24,
  "text": "Label",
  "fontSize": 16,
  "fontFamily": 4,
  "textAlign": "center"
}
```

Text centering formula (to center text inside a rectangle):
- `text.x = rect.x + (rect.width - text.width) / 2`
- `text.y = rect.y + (rect.height - text.height) / 2`

**Arrow**
```json
{
  "id": "unique-id",
  "type": "arrow",
  "x": 240, "y": 130,
  "points": [[0, 0], [100, 0]],
  "startBinding": { "elementId": "source-id", "focus": 0, "gap": 5 },
  "endBinding": { "elementId": "target-id", "focus": 0, "gap": 5 },
  "endArrowhead": "arrow"
}
```

Arrow coordinate system:
- `x`, `y`: absolute position of arrow start point
- `points`: relative offsets from (x, y). First point is always [0, 0]
- Example: `x: 100, y: 200, points: [[0,0], [50, 0], [50, 100]]` draws L-shaped arrow starting at (100, 200)

**Background Region** - Use rectangle with `"opacity": 30`

### Default Values (can be omitted)
```json
"fillStyle": "solid", "strokeWidth": 2, "roughness": 1,
"opacity": 100, "angle": 0, "seed": 1, "version": 1
```

## Color System

| Purpose | Background | Stroke |
|---------|------------|--------|
| Primary / Phase 1 | `#a5d8ff` | `#1971c2` |
| Secondary / Phase 2 | `#b2f2bb` | `#2f9e44` |
| Accent / Shared | `#fff3bf` | `#e67700` |
| Storage / State | `#d0bfff` | `#7048e8` |

## Layout Rules

- Align coordinates to multiples of 20
- Component spacing: 100-150px
- Standard component size: `140×60`
- Background regions: `opacity: 30`
- Render order: earlier elements in array appear behind

## Common Diagram Patterns

### Sequence Diagram Layout
For sequence diagrams (multiple participants with message flows):
- Place participants horizontally at top (y = 100)
- Each phase/stage gets its own vertical section below
- Use background regions to separate phases
- Vertical lifelines are implicit (not drawn as elements)
- Messages flow left-to-right or right-to-left between participants

Layout strategy:
```
Phase 1 (y: 80-300):   [A] -----> [B] -----> [C]
                            msg1       msg2
                       [A] <----- [B]
                            response

Phase 2 (y: 320-500):  [A'] ----> [B'] ----> [C']
                       (duplicate participants at new y)
```

Key insight: For multi-phase sequence diagrams, duplicate participant boxes in each phase rather than drawing long vertical lifelines. This avoids arrow crossing issues.

## Layout Optimization (Avoiding Overlaps)

### Prevent Arrow Overlap
When multiple arrows connect to the same component:
- Use `focus` parameter to offset arrow positions on component edge
- `focus: -0.5` = upper half, `focus: 0.5` = lower half, `focus: 0` = center
- Example: two horizontal arrows can use `focus: -0.5` and `focus: 0.5` to separate vertically

### Prevent Arrows Crossing Components
When arrows would cross unrelated components, restructure the layout:

**3 components with return arrow (A→B→C, C→A)**:
- Triangle layout: A at top, B bottom-left, C bottom-right
- All arrows flow along triangle edges, no crossings

**4 components with return arrow (A→B→C→D, D→A)**:
- Diamond layout: A at top, B left, C bottom, D right
- Or 2×2 grid with diagonal return arrow
- Or use bypass path for return arrow (route above/below the row)

**4+ components in sequence with return arrows**:
- Split into rows: forward flow on top row, return flow on bottom row
- Or use vertical bypass: return arrows route above/below all components
  ```json
  "points": [[0, 0], [0, -80], [-400, -80], [-400, 0]]
  ```

**Hub-and-spoke (central component connects to many)**:
- Place hub in center, spokes radially around it
- Avoid placing spokes in a line with hub in middle

**Default assumption**: If there's a return arrow, horizontal layout will likely fail—plan for bypass or 2D layout upfront.

## Complete Example

**Flow with Return Arrow (using bypass path)**
A → B → C, then C → A (return arrow routes above to avoid crossing B)

Arrow analysis:
- Arrow 1: A → B (horizontal) ✓
- Arrow 2: B → C (horizontal) ✓
- Arrow 3: C → A (return) ⚠️ Would cross B → use bypass path above

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [
    {"id": "a", "type": "rectangle", "x": 100, "y": 150, "width": 140, "height": 60, "backgroundColor": "#a5d8ff", "strokeColor": "#1971c2", "roundness": {"type": 3}, "boundElements": [{"id": "arr1", "type": "arrow"}, {"id": "arr3", "type": "arrow"}]},
    {"id": "a-label", "type": "text", "x": 155, "y": 168, "width": 30, "height": 24, "text": "A", "fontSize": 16, "fontFamily": 4, "textAlign": "center"},
    {"id": "b", "type": "rectangle", "x": 340, "y": 150, "width": 140, "height": 60, "backgroundColor": "#b2f2bb", "strokeColor": "#2f9e44", "roundness": {"type": 3}, "boundElements": [{"id": "arr1", "type": "arrow"}, {"id": "arr2", "type": "arrow"}]},
    {"id": "b-label", "type": "text", "x": 395, "y": 168, "width": 30, "height": 24, "text": "B", "fontSize": 16, "fontFamily": 4, "textAlign": "center"},
    {"id": "c", "type": "rectangle", "x": 580, "y": 150, "width": 140, "height": 60, "backgroundColor": "#d0bfff", "strokeColor": "#7048e8", "roundness": {"type": 3}, "boundElements": [{"id": "arr2", "type": "arrow"}, {"id": "arr3", "type": "arrow"}]},
    {"id": "c-label", "type": "text", "x": 635, "y": 168, "width": 30, "height": 24, "text": "C", "fontSize": 16, "fontFamily": 4, "textAlign": "center"},
    {"id": "arr1", "type": "arrow", "x": 245, "y": 180, "points": [[0, 0], [90, 0]], "endArrowhead": "arrow", "startBinding": {"elementId": "a", "focus": 0, "gap": 5}, "endBinding": {"elementId": "b", "focus": 0, "gap": 5}},
    {"id": "arr2", "type": "arrow", "x": 485, "y": 180, "points": [[0, 0], [90, 0]], "endArrowhead": "arrow", "startBinding": {"elementId": "b", "focus": 0, "gap": 5}, "endBinding": {"elementId": "c", "focus": 0, "gap": 5}},
    {"id": "arr3", "type": "arrow", "x": 650, "y": 145, "points": [[0, 0], [0, -60], [-480, -60], [-480, 0]], "endArrowhead": "arrow", "strokeStyle": "dashed", "startBinding": {"elementId": "c", "focus": 0, "gap": 5}, "endBinding": {"elementId": "a", "focus": 0, "gap": 5}},
    {"id": "arr3-label", "type": "text", "x": 380, "y": 60, "width": 60, "height": 20, "text": "return", "fontSize": 12, "fontFamily": 4, "textAlign": "center"}
  ],
  "appState": {"viewBackgroundColor": "#ffffff"},
  "files": {}
}
```

## Output

- Filename: `{descriptive-name}.excalidraw.json`
- Location: project root or `docs/` folder
- Tell user: drag into https://excalidraw.com or open with VS Code Excalidraw extension

## Notes

- IDs must be unique across the file
- `fontFamily`: 1=Virgil, 2=Helvetica, 3=Cascadia, 4=Comic Shanns (MUST use for hand-drawn style)
- `strokeWidth` usage in software diagrams:
  - `1` (thin): background regions, container borders, secondary connections
  - `2` (normal/default): primary components, main flow arrows
  - `4` (bold): emphasis, critical paths, highlighted elements
- Dashed arrows: add `"strokeStyle": "dashed"`
