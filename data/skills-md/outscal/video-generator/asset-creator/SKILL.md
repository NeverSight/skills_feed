---
name: asset-creator
description: This skill helps in drawing any visuals. It is a versatile skill and covers every important aspect to draw anything.
---

# Asset Creator Skill

<core-responsibility>
## Core Responsibility
Create SVG assets using fetched icons and/or custom SVG elements.
- **SVG code only** - No React, no JavaScript, slight animations
- **Transparent background** - No background unless explicitly requested
</core-responsibility>
<references>
**Understand Requirements** → Determine what icons/shapes/illustrations/graphics are needed
<path-creation-ref>
### **Path Creation** → To create any lines, curves, paths, this is important that you use the learnings from this
Read [path-creation.md](./references/path-creation.md)
</path-creation-ref>
<character-creation-ref>
### **Character Creation** → Whenver scene needs characters, use this
Read [primitive-characters.md](./references/character/primitive-characters.md)
</character-creation-ref>
<arrow-creation-ref>
### **Arrow Creation** → Whenever scene needs to create arrows, use this
Read [arrow-guidelines.md](./references/arrow-guidelines.md)
</arrow-creation-ref>
</references>

<fetch-icons-ref>
High-quality assets require visual references—use the steps below to fetch icons that guide each asset's shape.

<tools-to-use>
Use the `mcp__video_gen_tools__search_icons` tool to fetch the list of icon names. Use it  multiple times with different keywords if needed to get enough candidates.
Use the `mcp__video_gen_tools__get_icons` tool to fetch SVG content for icons returned by search_icons.

For each asset, fetch multiple reference icons before selecting the best match. The agent specifies the exact number of icons to read per asset.
</tools-to-use>

---

<handling-failed-searches>

<fallback-strategies>
1. Try alternative keyword to fetch the icon list.
</fallback-strategies>

</handling-failed-searches>

---

</fetch-icons-ref>

<asset-type-handling>
## Creation Guidelines by Asset Type

### `logo`
- Fetch reference icons
- Use EXACTLY as-is. Zero modifications.
- If no matching references found: Write the name of that brand/entity inside a visual box.

### `icon`
- Fetch reference icons
- Use EXACTLY as-is. Zero modifications.
- If no matching references found: Create from scratch, keep simple like icons

### `customized`
- Fetch reference icons
- If a reference matches description → use as-is
- Only if NO reference matches → tweak the closest one
- If no direct references found → search for similar references, understand their shape, and create the asset

### `character`
- NO icon fetching
- Use <character-creation-ref> to create from scratch

</asset-type-handling>

<svg-basics>
Use whenever SVGs need to be created or used
<basic-svg-structure>
```svg
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <style>
    /* CSS styles and animations */
  </style>

  <!-- SVG elements here -->
</svg>
```
<root-element-attributes>
### Root Element Attributes

| Attribute | Purpose | Example |
|-----------|---------|---------|
| `viewBox` | Internal coordinate system | `"0 0 100 100"` |
| `xmlns` | XML namespace (required) | `"http://www.w3.org/2000/svg"` |
</root-element-attributes>
<basic-shapes>
<rectangle>
```svg
<rect x="10" y="10" width="80" height="60" rx="5" ry="5" fill="#3B82F6"/>
```

| Attribute | Purpose |
|-----------|---------|
| `x`, `y` | Position (top-left corner) |
| `width`, `height` | Dimensions |
| `rx`, `ry` | Corner radius |
| `fill` | Fill color |
</rectangle>
<circle>

```svg
<circle cx="50" cy="50" r="40" fill="#EF4444"/>
```

| Attribute | Purpose |
|-----------|---------|
| `cx`, `cy` | Center position |
| `r` | Radius |
</circle>
<ellipse>

```svg
<ellipse cx="50" cy="50" rx="40" ry="25" fill="#10B981"/>
```

| Attribute | Purpose |
|-----------|---------|
| `cx`, `cy` | Center position |
| `rx`, `ry` | X and Y radii |
</ellipse>
<line>

```svg
<line x1="10" y1="10" x2="90" y2="90" stroke="#000" stroke-width="2"/>
```
</line>
<polyline>

```svg
<polyline points="10,90 50,10 90,90" fill="none" stroke="#000" stroke-width="2"/>
```
</polyline>
<polygon>

```svg
<polygon points="50,10 90,90 10,90" fill="#F59E0B"/>
```
</polygon>
</basic-shapes>
<path-element>
The `<path>` element is the most powerful SVG element, using commands to draw complex shapes.
<path-commands>

| Command | Name | Parameters | Example |
|---------|------|------------|---------|
| `M` | Move to | x, y | `M 10 10` |
| `L` | Line to | x, y | `L 90 90` |
| `H` | Horizontal line | x | `H 50` |
| `V` | Vertical line | y | `V 50` |
| `C` | Cubic Bezier | x1,y1 x2,y2 x,y | `C 20,20 80,20 90,90` |
| `Q` | Quadratic Bezier | x1,y1 x,y | `Q 50,0 90,90` |
| `A` | Arc | rx ry rotation large-arc sweep x y | `A 25 25 0 0 1 50 50` |
| `Z` | Close path | - | `Z` |

Lowercase commands use relative coordinates (relative to current position).
</path-commands>
<path-example>

```svg
<!-- Triangle -->
<path d="M 50 10 L 90 90 L 10 90 Z" fill="#8B5CF6"/>

<!-- Curved shape -->
<path d="M 10 50 Q 50 10 90 50 T 170 50" stroke="#000" fill="none"/>
```
</path-example>
</path-element>
<groups-transforms>
<group-element>
Use `<g>` to group elements and apply shared transforms or styles:

```svg
<g transform="translate(50, 50)" fill="#3B82F6">
  <circle r="20"/>
  <rect x="-10" y="25" width="20" height="10"/>
</g>
```
</group-element>
<transform-attribute>

| Transform | Syntax | Example |
|-----------|--------|---------|
| Translate | `translate(x, y)` | `translate(50, 50)` |
| Scale | `scale(s)` or `scale(sx, sy)` | `scale(2)` |
| Rotate | `rotate(deg)` or `rotate(deg, cx, cy)` | `rotate(45)` |
| Skew | `skewX(deg)` or `skewY(deg)` | `skewX(10)` |
</transform-attribute>
</groups-transforms>
<styling>
<fill-stroke>

```svg
<rect
  fill="#3B82F6"           /* Fill color */
  fill-opacity="0.8"       /* Fill transparency */
  stroke="#1D4ED8"         /* Stroke color */
  stroke-width="2"         /* Stroke width */
  stroke-opacity="0.9"     /* Stroke transparency */
  stroke-linecap="round"   /* Line end style: butt | round | square */
  stroke-linejoin="round"  /* Corner style: miter | round | bevel */
  stroke-dasharray="5 3"   /* Dash pattern */
/>
```
</fill-stroke>
<colors>
```svg
fill="#3B82F6"           /* Hex */
fill="rgb(59, 130, 246)" /* RGB */
fill="rgba(59, 130, 246, 0.5)" /* RGBA */
fill="currentColor"      /* Inherit from parent */
fill="none"              /* Transparent */
```
</colors>
<embedded-css>

```svg
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <style>
    .primary { fill: #3B82F6; }
    .secondary { fill: #EF4444; }
    .outline { fill: none; stroke: #000; stroke-width: 2; }
  </style>

  <circle class="primary" cx="50" cy="50" r="30"/>
</svg>
```
</embedded-css>
</styling>
<defs-reuse>
<defs-element>
Store reusable elements that won't render directly:

```svg
<defs>
  <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#3B82F6"/>
    <stop offset="100%" stop-color="#8B5CF6"/>
  </linearGradient>
</defs>

<rect fill="url(#grad1)" x="10" y="10" width="80" height="80"/>
```
</defs-element>
<transform-attribute-2>

| Transform | Syntax | Example |
|-----------|--------|---------|
| Translate | `translate(x, y)` | `translate(50, 50)` |
| Scale | `scale(s)` or `scale(sx, sy)` | `scale(2)` |
| Rotate | `rotate(deg)` or `rotate(deg, cx, cy)` | `rotate(45)` |
| Skew | `skewX(deg)` or `skewY(deg)` | `skewX(10)` |
</transform-attribute-2>
<use-element>

Reference defined elements:

```svg
<defs>
  <circle id="dot" r="5"/>
</defs>

<use href="#dot" x="20" y="20" fill="red"/>
<use href="#dot" x="50" y="50" fill="blue"/>
<use href="#dot" x="80" y="80" fill="green"/>
```
</use-element>
</defs-reuse>
<gradients>
<linear-gradient>

```svg
<defs>
  <linearGradient id="linear" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#3B82F6"/>
    <stop offset="100%" stop-color="#EF4444"/>
  </linearGradient>
</defs>
```
</linear-gradient>
<radial-gradient>
```svg
<defs>
  <radialGradient id="radial" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="#FFF"/>
    <stop offset="100%" stop-color="#3B82F6"/>
  </radialGradient>
</defs>
```
</radial-gradient>
</gradients>
<clipping-masking>
<clip-path>

```svg
<defs>
  <clipPath id="circle-clip">
    <circle cx="50" cy="50" r="40"/>
  </clipPath>
</defs>

<rect clip-path="url(#circle-clip)" x="0" y="0" width="100" height="100" fill="#3B82F6"/>
```
</clip-path>
<mask>

```svg
<defs>
  <mask id="fade-mask">
    <linearGradient id="fade" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="white"/>
      <stop offset="100%" stop-color="black"/>
    </linearGradient>
    <rect fill="url(#fade)" width="100" height="100"/>
  </mask>
</defs>

<rect mask="url(#fade-mask)" fill="#3B82F6" width="100" height="100"/>
```
</mask>
</clipping-masking>
<best-practices>

1. **Always use viewBox** - Enables proper scaling
2. **Use transparent background** - No background rect unless needed
3. **Group related elements** - Use `<g>` for organization and shared transforms
4. **Use meaningful IDs** - For gradients, clips, and reusable elements
5. **Optimize paths** - Remove unnecessary precision (2 decimal places max)
6. **Use classes for styling** - Separate presentation from structure
</best-practices>
</basic-svg-structure>
</svg-basics>
<position-elements>
Important to position anything in the scene
<understanding-viewbox>
The `viewBox` attribute defines the internal coordinate system of an SVG:

```svg
<svg viewBox="minX minY width height" xmlns="http://www.w3.org/2000/svg">
```

| Parameter | Meaning |
|-----------|---------|
| `minX` | Left edge X coordinate (usually 0) |
| `minY` | Top edge Y coordinate (usually 0) |
| `width` | Internal width in SVG units |
| `height` | Internal height in SVG units |
</understanding-viewbox>

<coordinate-system>

```
(0,0) ─────────────────────────► X (width)
  │
  │     (25%,25%)        (75%,25%)
  │        ●────────────────●
  │        │                │
  │        │   (50%,50%)    │
  │        │       ●        │
  │        │    center      │
  │        │                │
  │        ●────────────────●
  │     (25%,75%)        (75%,75%)
  │
  ▼
 Y (height)
```

| Position | Formula |
|----------|---------|
| Top-left | (0, 0) |
| Top-center | (width/2, 0) |
| Center | (width/2, height/2) |
| Bottom-center | (width/2, height) |
</coordinate-system>
<safe-zone-max-scale>

Keep icon centers within 10%-90% of viewBox to prevent clipping:

```
availableSpace = viewBoxSize * 0.8
maxScale = availableSpace / iconViewBoxSize
```
</safe-zone-max-scale>
<transparent-background>
SVGs are transparent by default. To maintain transparency:
- Do NOT add background rectangles unless requested
- Do NOT set fill on root SVG
- Apply fill only to icon paths
</transparent-background>
<aligning-effects>
When adding effects (muzzle flash, sparks, etc.) to specific points on an icon, position them using the icon's coordinate system.

**Process:**
1. **Identify the attachment point** in the icon's original coordinate space (e.g., gun barrel tip)
2. **Position the effect** at that coordinate using `transform="translate(x, y)"`

**Example: Gun with muzzle flash**
```svg
<!-- Gun icon with viewBox 0 0 512 512, barrel tip at (486, 175) -->
<svg viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
  <path d="M79.238 115.768..." fill="#333"/>  <!-- Gun icon -->

  <!-- Position muzzle flash at barrel tip coordinates -->
  <g transform="translate(486, 175)">
    <polygon points="0,0 15,-8 12,0 15,8" fill="#FF6600">
      <animate attributeName="opacity" values="1;0;1" dur="0.1s" repeatCount="indefinite"/>
    </polygon>
  </g>
</svg>
```

**Finding attachment points:**

| Icon Type | Attachment Point | How to Find |
|-----------|------------------|-------------|
| Guns/Weapons | Barrel tip | Rightmost X, mid-height Y in icon's coordinate space |
| Swords/Blades | Blade tip | Topmost or rightmost point in icon's coordinate space |
| Characters | Hand position | Look for arm/hand path segments, note their coordinates |
| Vehicles | Exhaust/Wheels | Bottom or rear coordinates in icon's coordinate space |

**Debugging tip:** Add a visible circle at the attachment point to verify position:
```svg
<circle cx="486" cy="175" r="5" fill="red"/>  <!-- Shows barrel tip location -->
```
</aligning-effects>
</position-elements>
<animations>
Use whenever any object might need animation. This master document provides an overview of all animation patterns available for SVG assets.
<animation-categories>
<rotation-animations-ref>
- **[rotation-animations.md](./references/animations/rotation-animations.md) - READ THIS FOR ANY OBJECT THAT ROTATES** - Works for ANY rotating element (wheels, gears, doors, levers, etc.). Contains guidelines and links to example files covering every type of rotation pattern from simple pivots to complex systems with attached objects.
</rotation-animations-ref>
<path-following-ref>
- **[path-following.md](./references/animations/path-following.md) - READ THIS FOR ANY OBJECT FOLLOWING A PATH** - Explains how to make and object follow any path. Works with `<animateMotion>` + `<mpath>` for any SVG element.
</path-following-ref>
<path-drawing-ref>
- **[path-drawing.md](./references/animations/path-drawing.md) - READ THIS FOR DRAWING/REVEALING PATHS** - Animates the drawing of a path itself (line appearing on screen). Uses `stroke-dasharray` and `stroke-dashoffset` technique.
</path-drawing-ref>
</animation-categories>
</animations>
<reference-map>
<core-references>
`./references/fetching-icons.md` — Search & retrieve SVG icons from Bootstrap, Font Awesome, Game Icons via MCP tools
`./references/path-creation.md` — Generate SVG path `d` attributes using Python scripts
`./references/arrow-guidelines.md` - Guidelines to create the correct arrows tip
</core-references>
<path-types>
`./references/paths_guidelines.md` - All paths types along with example and script command for each path style
</path-types>
<animations-ref>
`./references/animations/rotation-animations.md` — All rotation patterns with pivot point calculations
`./references/animations/path-following.md` — Objects following paths via `<animateMotion>` + `<mpath>`
`./references/animations/path-drawing.md` — Path "drawing itself" using stroke-dasharray technique
</animations-ref>
<pivot-types>
`./references/animations/pivots/end-pivot-examples.md` — Rotation from fixed anchor (clocks, pendulums, doors)
`./references/animations/pivots/center-pivot-examples.md` — Spinning around center (fans, wheels, gears)
`./references/animations/pivots/edge-point-pivot-examples.md` — Rotation from arbitrary perimeter points
`./references/animations/pivots/attached-objects-examples.md` — Parent rotates with attached children (seesaws, Ferris wheels)
</pivot-types>

<character-ref>
`./references/character/emotions.md` — Facial expressions and clipPath-based eye blink animations
`./references/character/primitive-characters.md` — Cute geometric mascot characters with consistent proportions
</character-ref>
</reference-map>
<output-format>

<rotation-system>
## Rotation System
```
0° = pointing up
Positive = clockwise
Negative = counter-clockwise
```
**To achieve a target orientation:**
1. Draw shape pointing UP (0°)
2. Apply `rotate(target_degrees)` — positive rotates clockwise

| Target | Transform |
|--------|-----------|
| 45° (up-right) | `rotate(45)` ✓ |
| 135° (down-right) | `rotate(135)` ✓ |
| 270° (left) | `rotate(270)` or `rotate(-90)` ✓ |

❌ **Wrong:** `rotate(-45)` for 45° gives 315° (up-left), not 45°

</rotation-system>

</output-format>
