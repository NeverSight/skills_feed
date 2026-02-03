---
name: d3-visualization
description: D3 ecosystem guidance for designing and implementing interactive charts/diagrams in Angular (signals-first, accessible, performant).
tags: [d3, dataviz, charts, diagrams, a11y, performance]
version: 1.0.0
---

# SKILL: D3 Visualization & Diagram Design

## Use when
- Implementing interactive visualizations using D3 (SVG/Canvas) in the Angular UI.
- You need to choose a diagram type and map it to a D3 layout/module.

## Workflow
1. Clarify purpose: compare / rank / part-to-whole / flow / hierarchy / network / geo / schedule.
2. Choose the simplest representation that answers the question (avoid novelty charts).
3. Define a **chart view model** (VM) at the Application boundary; UI receives it as Signals.
4. Pick render tech:
   - SVG for readability + a11y (small/medium)
   - Canvas/hybrid for density/perf (large)
5. Add interaction only if it reduces cognitive load (zoom/pan/hover/select/filter).
6. Build in a11y: text summary + keyboard navigation + reduced motion.

## Diagram → D3 mapping (quick guide)
- 森林圖 Forest Plot: scales/axes (`d3-scale`, `d3-axis`) + points/CI lines (`d3-shape`)
- 徑向樹 Radial Tree: `d3-hierarchy.tree()`/`cluster()` + radial links (`d3-shape`)
- 旭日圖 Sunburst: `d3-hierarchy.partition()`
- 桑基圖 Sankey: `d3-sankey`
- 環狀樹/圓形樹 Circular Tree:
  - Circle Packing: `d3-hierarchy.pack()`
  - Radial Dendrogram: `d3-hierarchy.cluster()` + radial links
- 網絡圖 Network Graph: `d3-force` (force simulation)
- 熱力圖 Heatmap: band scales + rect grid (Canvas for dense grids)
- 樹狀圖 Tree Diagram: `d3-hierarchy.tree()`
- 甘特圖 Gantt: time scale + band rows (compute schedule in Application)
- 時間線 Timeline: `d3-scale` time + annotations (`d3-shape`)
- 日曆圖 Calendar Heatmap: time bucketing + grid layout (Canvas if needed)
- 里程碑圖 Milestone Chart: timeline + point/label layout
- 時序圖 Sequence Diagram: prefer Mermaid for docs; D3 only if interactive editing is required
- 關鍵路徑圖 Critical Path: compute CPM in Application; render as highlighted Gantt/network
- 組織圖 Org Chart: `d3-hierarchy.tree()` with compact node layout
- 心智圖 Mind Map: tree/radial tree with collapsible nodes
- 因果圖 Fishbone (Ishikawa): custom layout (bones as angled branches) + labels
- 等值線圖 Contour Map: `d3-contour` (grid → isolines/filled contours)
- 分級著色 Choropleth: `d3-geo` + region fill scale
- 點密度 Dot Density: `d3-geo` + point placement (within polygons or sampled points)

## Common D3 building blocks (preferred)
- `d3-selection`, `d3-scale`, `d3-axis`, `d3-shape`, `d3-zoom`, `d3-drag`, `d3-brush`
- `d3-hierarchy`, `d3-force`, `d3-sankey`, `d3-geo`, `d3-contour`

## References
- `.github/instructions/70-d3-data-visualization-copilot-instructions.md`

