---
name: svg
description: Create precise, production-ready SVG graphics for technical and business contexts (diagrams, P&IDs, HMI/SCADA widgets, process flow visuals, PowerPoint/Office illustrations, UI icons, annotations). Use when the user asks to generate, edit, standardize, optimize, or export SVG artwork; convert requirements (dimensions, scale, line weights, layers, symbols) into clean SVG markup; or produce multiple layout/variant files (editable vs outlined text, light/dark, monochrome).
---

# SVG Creation Guide

Create clean, scalable SVG that is easy to edit, prints well, and survives “real-world” tooling (PowerPoint, browser, PDF export, HMI toolchains).

## Working rules (keep SVG dependable)

- Use a `viewBox` on every SVG.
- Keep geometry simple: prefer `path`, `rect`, `circle`, `line`, `polyline`, `polygon`.
- Prefer strokes for technical drawings; prefer fills for pictograms.
- Use consistent naming and grouping: `id` on key groups, `class` for reusable styling.
- Avoid renderer-fragile features unless asked:
  - Avoid: `filter`, `mask`, `clipPath`, `foreignObject`, blend modes, external images/fonts.
  - Use gradients sparingly; keep them simple (`linearGradient`/`radialGradient`).
- Keep decimal precision reasonable (typically 2–3 decimals). Do not over-optimize readability away.

## Requirements to capture (ask only what matters)

Capture enough to produce the correct output on the first pass.

1. **Target environment** (drives compatibility)
   - Web / inline HTML
   - PowerPoint / Office
   - HMI/SCADA tool (name/version if known)
   - Engineering doc pipeline (PDF export, Visio, etc.)

2. **Canvas + scale**
   - Desired physical size (mm/in) or slide size intent
   - Coordinate system preference (e.g., “0–100 grid”, “millimeters”, “pixels”)
   - Any snapping/grid requirements

   Useful conversions (SVG assumes 96 DPI for CSS pixels):
   - $1\,\text{in} = 96\,\text{px}$
   - $1\,\text{mm} = 96/25.4 \approx 3.7795\,\text{px}$

3. **Styling constraints**
   - Stroke widths (e.g., 1.5 for primary lines, 1.0 for secondary)
   - Line caps/joins (round vs square)
   - Color palette (include corporate colors if relevant)
   - Light/dark background expectations

4. **Content + semantics**
   - What objects exist (symbols, instruments, pipes, arrows, labels)
   - Layering needs (background, pipework, instrumentation, callouts)
   - Text rules (font family, size, casing, alignment)

5. **Deliverables**
   - Number of variants (size/layout/color)
   - Editable text vs outlined text requirements
   - File naming convention and destination folder

## Output patterns (choose the right one)

### Pattern A: Technical diagram / P&ID style

Use strokes, consistent line weights, and a simple palette. Prefer `vector-effect="non-scaling-stroke"` when objects will be scaled.

Key tips:
- Keep symbols as `<g id="symbol-*">` groups.
- Use `stroke="currentColor"` on symbols when you want themeable line art.
- Align to a grid; keep elbows crisp with `polyline`.

### Pattern B: PowerPoint/Office-friendly illustration

Prioritize compatibility:
- Prefer inline presentation attributes (`fill`, `stroke`, `stroke-width`) over heavy CSS.
- Avoid: masks/filters, complex gradients, `marker` arrows (Office support varies).
- Keep text as `<text>` if the user wants to edit labels in PPT.
- If the user needs pixel-perfect portability, provide an “outlined” version (text converted to paths) and warn it is no longer editable.

### Pattern C: HMI/SCADA widget

Design for clarity at small sizes and for interaction:
- Use generous hit areas (transparent rect with `fill="transparent"` for click/touch zones).
- Keep state styling isolated (`.state-ok`, `.state-alarm`, `.state-disabled`).
- Separate “skin” from “labels” so integrators can map tags and states.

## SVG skeleton (recommended)

Use this as the default structure.

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="300" height="200" role="img" aria-labelledby="title desc">
  <title id="title">Diagram title</title>
  <desc id="desc">Short description of what is shown</desc>

  <defs>
    <style>
      .line { fill: none; stroke: #111827; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
      .thin { stroke-width: 1; }
      .fill { fill: #F3F4F6; }
      .text { fill: #111827; font-family: Arial, sans-serif; font-size: 12px; }
    </style>
  </defs>

  <g id="layer-background"></g>
  <g id="layer-geometry"></g>
  <g id="layer-annotations"></g>
</svg>
```

If targeting PowerPoint/Office and compatibility is uncertain, repeat critical attributes inline on elements (Office can be picky about CSS).

## Reference examples (copy/paste building blocks)

### 1) P&ID-style pipe with arrow and tag

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 80" width="240" height="80">
  <g id="pipe" stroke="#111827" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke">
    <polyline points="20,40 160,40" />
    <!-- arrow head (Office-friendly: polygon instead of marker) -->
    <polygon points="160,32 160,48 178,40" fill="#111827" stroke="none" />
  </g>

  <g id="tag">
    <rect x="185" y="24" width="45" height="32" rx="6" fill="#FFFFFF" stroke="#111827" stroke-width="2" />
    <text x="207.5" y="45" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#111827">P-101</text>
  </g>
</svg>
```

### 2) Simple valve symbol (line-art)

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 40" width="120" height="40">
  <g id="valve" stroke="#111827" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke">
    <line x1="10" y1="20" x2="35" y2="20" />
    <line x1="85" y1="20" x2="110" y2="20" />
    <polygon points="35,8 60,20 35,32" />
    <polygon points="85,8 60,20 85,32" />
  </g>
</svg>
```

### 3) HMI button (states via classes)

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 70" width="220" height="70">
  <defs>
    <style>
      .btn { stroke: #0F172A; stroke-width: 2; rx: 12; }
      .ok { fill: #22C55E; }
      .alarm { fill: #EF4444; }
      .disabled { fill: #CBD5E1; }
      .label { fill: #0F172A; font-family: Arial, sans-serif; font-size: 16px; font-weight: 700; }
    </style>
  </defs>

  <g id="button" class="ok">
    <rect class="btn ok" x="10" y="10" width="200" height="50" />
    <text class="label" x="110" y="42" text-anchor="middle" dominant-baseline="middle">START</text>
    <!-- hit area -->
    <rect x="10" y="10" width="200" height="50" fill="transparent" />
  </g>
</svg>
```

## Quality checklist (run mentally before delivering)

- Include `viewBox`; ensure shapes fit the viewBox with sane margins.
- Keep stroke widths consistent and intentional.
- Ensure text alignment is correct (`text-anchor`, `dominant-baseline`).
- Keep groups layered predictably (`layer-*`).
- Avoid external dependencies (no linked fonts/images) unless requested.
- If PowerPoint/Office is the target, avoid unsupported features and prefer inline attributes.

## File outputs

When saving multiple variants, use a naming convention that encodes intent:

- `asset-name__v1__editable.svg`
- `asset-name__v1__outlined.svg`
- `asset-name__dark.svg`
- `asset-name__light.svg`
- `asset-name__scale-0-100.svg`

Save files into a logical folder (e.g., `assets/svg/` or a user-specified directory).
