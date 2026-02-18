---
name: sketch-implement-design
description: >
  Translate Sketch layers into production-ready code with 1:1 visual fidelity using
  Sketch MCP tools (`run_code`, `get_selection_as_image`) for live design context,
  screenshots, and asset export. Use when implementing or updating UI from an open
  Sketch document, current selection, or specific Sketch layer IDs.
metadata:
  short-description: Implement Sketch designs with Sketch MCP
---

# Sketch Implement Design

## Overview

Implement UI from Sketch with high visual fidelity by querying live document data
through Sketch MCP. Use `run_code` to inspect and export data, and
`get_selection_as_image` as the visual source of truth.

## Prerequisites

- Keep Sketch open with the target document available.
- Enable Sketch MCP in Sketch settings:
  **General** -> **Allow AI tools to interact with open documents**.
- Configure Codex MCP to point to the local Sketch server address shown in Sketch settings.
  - Default address is usually `http://localhost:31126/mcp`.
- Select the layer or frame to implement in Sketch before calling `get_selection_as_image`.

## Required Workflow

Follow these steps in order. Do not skip steps.

### Step 0: Confirm Sketch MCP connectivity

If Sketch MCP calls fail:

1. Check that Sketch is running and MCP is enabled in settings.
2. Check the MCP server URL in your MCP client config.
3. Retry after confirming the server address in Sketch settings.

### Step 1: Identify the implementation target

Use these approaches in priority order:

- User gives a Sketch share link like
  `https://sketch.com/s/<document-share-uuid>/f/<canvas-frame-uuid>`: extract
  the `/f/<canvas-frame-uuid>` value, find that layer, and select it. Prefer
  this target over current selection or name-based matching.
- User gives layer identifiers or names: use `run_code` to locate matching
  layers and ask for confirmation.
- User selects the exact frame/component in Sketch.

Use `run_code` with the `find` function and this pattern when a share link is provided:

```js
const sketch = require('sketch')
const frameId = '4A2E31FF-56BD-4C29-92D2-829548D19C1D'
const frame = find(`#${frameId}`)
if (frame) sketch.getSelectedDocument().selectedLayers = [frame]
```

When multiple matches exist, stop and ask which layer to implement.

### Step 2: Fetch structured design context via `run_code`

Run `run_code` to collect design data for the selected root layer (and relevant descendants):

- Hierarchy: IDs, names, types, visibility, lock state
- Layout: frame, resizing behavior, pins, stack layout, clipping
- Typography: font family, size, weight, line height, alignment, decoration
- Styling: fills, borders, shadows, blur, corner radii, opacity, tint
- Reusable styling: shared text/layer style names and source library names
- Variables/swatches: color variable names and optional source library names
- Symbols: nested symbols and override-capable fields
- Export settings and image sources

Always start scripts with:

```js
const sketch = require('sketch')
```

Pass a short `title` argument to `run_code` and keep scripts minified unless the
user asks otherwise.

If output is too large:

1. Fetch a shallow tree map first (IDs, names, types only).
2. Fetch detailed context per critical child subtree.
3. Continue only after all required nodes are covered.

### Step 3: Capture visual reference via `get_selection_as_image`

Call `get_selection_as_image` on the same selected target. Use this image as the primary visual
reference for implementation and validation.

If selection is empty, stop and ask the user to select the intended layer/frame in Sketch.

### Step 4: Export required assets via `run_code`

Export icons, bitmaps, and other assets from Sketch instead of inventing placeholders.

Rules:

- Use assets from Sketch output; do not add new icon packs unless explicitly requested.
- Use absolute output paths.
- For `sketch.export`, always pass both `output` and `filename` (with extension).

Example:

```js
const sketch=require('sketch');const d=sketch.getSelectedDocument()
const l=d.selectedLayers.layers[0]
sketch.export(l,{
  output:'/tmp/sketch-assets',
  filename:`${l.id}.png`,
  formats:['png']
});console.log('ok')
```

### Step 5: Translate Sketch output to project conventions

Treat Sketch data as design intent, then map to project standards:

- Reuse existing UI components before creating new ones.
- Map Sketch values to project tokens (color, spacing, type scale, radius).
- Match established architecture and state/data patterns.
- Keep generated code maintainable and idiomatic for the target stack.

### Step 6: Implement for 1:1 visual parity

Aim for visual parity with the Sketch screenshot and context:

- Match spacing, alignment, sizing, and hierarchy.
- Match typography and color usage.
- Preserve intended behavior for responsive/constraint-based layouts.
- Use tokenized values when possible; avoid unnecessary hardcoded values.

### Step 7: Validate against Sketch before completion

Validate implemented UI against the screenshot and design context checklist:

- Layout and spacing
- Typography
- Colors and effects
- States and interactions
- Asset rendering
- Responsiveness/constraints
- Accessibility basics

If mismatch remains, re-query with `run_code` for the affected subtree and iterate.

## Implementation Rules

- Prefer incremental updates over broad rewrites.
- Keep component boundaries consistent with the design hierarchy.
- Document intentional deviations (technical or accessibility constraints).
- Do not assume stale design data; re-query Sketch when unsure.

## Common Issues

### `Empty selection` from `get_selection_as_image`

Cause: Nothing selected in Sketch.
Fix: Ask the user to select the target layer/frame, then retry.

### `No document` from MCP tools

Cause: No open Sketch document or Sketch not running.
Fix: Open the document in Sketch and retry.

### `run_code` output is too large or truncated

Cause: Selection tree is too large.
Fix: Query shallow tree first, then fetch detailed context by subtree.

### Missing or incorrect exported assets

Cause: Invalid export options or relative output path.
Fix: Use absolute paths and pass both `output` and `filename`.

### Implementation does not match visual design

Cause: Incomplete context capture or token mismatch.
Fix: Re-capture screenshot and inspect exact node values via `run_code`.

## References

- [Sketch MCP server docs](https://www.sketch.com/docs/mcp-server/)
- [Sketch API reference](https://developer.sketch.com/reference/api/llms.txt)
