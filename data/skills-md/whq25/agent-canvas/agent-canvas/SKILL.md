---
name: agent-canvas
description: Draw diagrams, flowcharts, and visualizations on an Excalidraw canvas. Use when the user asks to draw, visualize, create diagrams, or sketch ideas.
allowed-tools: Bash(agent-canvas:*)
license: MIT
metadata:
  author: WHQ25
  version: "0.6.0"
  repository: https://github.com/WHQ25/agent-canvas
---

# Agent Canvas

A CLI tool to interact with an Excalidraw canvas for creating diagrams and visualizations.

## Installation

Before using, check if CLI is installed:

```bash
which agent-canvas && agent-canvas --version
```

- **If not installed**: Ask the user which package manager they prefer (bun or npm), then install:
  ```bash
  bun add -g @agent-canvas/cli@0.6.0
  # or
  npm install -g @agent-canvas/cli@0.6.0
  ```

- **If installed but version differs from 0.5.1**: Upgrade using the same package manager:
  - Path contains `.bun` → `bun add -g @agent-canvas/cli@0.6.0`
  - Otherwise → `npm install -g @agent-canvas/cli@0.6.0`

- **After install/upgrade**: Verify with `agent-canvas --version` to confirm version is 0.5.1

## Quick Start

1. Start the canvas (opens in browser):
   ```bash
   agent-canvas start
   ```

2. Use CLI commands to draw on the canvas.

## Commands Reference

### Start Canvas
```bash
agent-canvas start                    # Start server and open browser
agent-canvas start -f file.excalidraw # Load existing file on start
```
**When loading from file (`-f`)**: Remember the file path and save back to it with `agent-canvas save <original-file>`.

### Add Text
```bash
agent-canvas add-text -t "<text>" --ax <x> --ay <y> [options]
```
- Options: `--font-size <size>`, `--text-align <left|center|right>`, `-a/--anchor <anchor>`, `--stroke-color <hex>`, `-n/--note <text>`
- Font sizes: S=16, M=20 (default), L=28, XL=36
- **Anchor** (`-a`): Controls which point of the text bounding box the anchor coordinates (--ax, --ay) refer to:
  ```
  topLeft ────── topCenter ────── topRight
      │                               │
  leftCenter ────── center ────── rightCenter
      │                               │
  bottomLeft ── bottomCenter ── bottomRight
  ```
  Default: `bottomLeft` (text flows right and up from anchor point). Use `center` to place text centered on a point, `topCenter` for text below a point, etc.
- Returns: `Text created (id: <id>, x: <x>, y: <y>, <width>x<height>)` — actual top-left position and dimensions for precise layout

### Add Drawing Elements

All drawing commands share common style options:
- **Stroke**: `--stroke-color <hex>` (default: #1e1e1e), `--stroke-width <1-4>` (default: 2), `--stroke-style <solid|dashed|dotted>` (default: solid)
- **Fill** (shapes only): `--background-color <hex>` (default: transparent), `--fill-style <solid|hachure|cross-hatch>` (default: solid)
- **Meta**: `-n/--note <text>` - semantic description for the element. **Use liberally** - notes help understand diagram intent when reading back later.

**Recommended Colors** (from Excalidraw palette):
| Color  | Stroke (dark) | Background (light) |
|--------|---------------|-------------------|
| Red    | #e03131       | #ffc9c9           |
| Blue   | #1971c2       | #a5d8ff           |
| Green  | #2f9e44       | #b2f2bb           |
| Yellow | #f08c00       | #ffec99           |
| Cyan   | #0c8599       | #99e9f2           |
| Violet | #6741d9       | #b197fc           |
| Gray   | #495057       | #dee2e6           |

#### Shapes
```bash
agent-canvas add-shape -t <type> -x <x> -y <y> [-w <width>] [-h <height>] [-l <label>]
```
- Types: `rectangle`, `ellipse`, `diamond`
- Use `-l/--label` to add text inside the shape (fontSize: 16 by default), `--label-font-size <n>` to adjust
- **Returns**: `Shape created (id: <id> x=<x> y=<y> w=<width> h=<height>)` — actual dimensions after auto-sizing for labels

**⚠️ Label Sizing - CRITICAL: Calculate BEFORE drawing**

If shape size is too small, Excalidraw auto-expands, breaking arrow coordinates. **You MUST:**
1. Calculate minimum dimensions using the formulas below
2. Use the calculated values directly — **NEVER estimate or use smaller values**

```
Step 1: Calculate text dimensions (fontSize=16 by default)
  textWidth = charCount × fontSize × 0.6  (English/numbers)
  textWidth = charCount × fontSize        (CJK characters)
  textHeight = lineCount × fontSize × 1.35

Step 2: Calculate minimum shape size (use these values, not smaller!)
  rectangle: width = textWidth + 50,  height = textHeight + 50
  ellipse:   width = textWidth × 1.42 + 55,  height = textHeight × 1.42 + 55
  diamond:   width = textWidth × 2 + 60,  height = textHeight × 2 + 60
```

**Example**: Label "Message Queue" (13 chars) in ellipse
```
textWidth = 13 × 16 × 0.6 = 124.8
textHeight = 1 × 16 × 1.35 = 21.6
ellipse width = 124.8 × 1.42 + 55 = 232
ellipse height = 21.6 × 1.42 + 55 = 86
→ Use: -w 232 -h 86 (or round up to -w 240 -h 90)
```

**Tip**: For long labels, insert `\n` manually, then recalculate with updated lineCount.

#### Lines & Arrows
```bash
agent-canvas add-line -x <x1> -y <y1> --end-x <x2> --end-y <y2>
agent-canvas add-arrow -x <x1> -y <y1> --end-x <x2> --end-y <y2>
```
- Arrow-specific: `--start-arrowhead`, `--end-arrowhead` (arrow, bar, dot, triangle, diamond, none)

**Arrow Types** (`--arrow-type`):
| Type | Description | Use Case |
|------|-------------|----------|
| `sharp` | Straight line (default) | Direct connections |
| `round` | Curved line with control point | Organic flows, avoiding overlaps |
| `elbow` | Right-angle turns (90°) | Flowcharts, circuit diagrams |

**Intermediate Points** (`--via`):
Use `--via` to specify intermediate points as absolute coordinates in format `"x1,y1;x2,y2;..."`:

```bash
# Round arrow: one control point determines curve direction
# Vertical arrow curving left (control point at x=50, left of the line)
agent-canvas add-arrow -x 100 -y 100 --end-x 100 --end-y 300 --arrow-type round --via "50,200"

# Elbow arrow: multiple points for 90° turns
# Loop back pattern: down → left → up (for flowchart iterations)
agent-canvas add-arrow -x 175 -y 520 --end-x 175 --end-y 280 --arrow-type elbow --via "120,520;120,280"
```

**Tips**:
- For `round`: curve bends toward the control point (offset from straight path)
- For `elbow`: points define the corners of the 90° path

#### Polygon
```bash
agent-canvas add-polygon -p '[{"x":0,"y":0},{"x":100,"y":0},{"x":50,"y":100}]'
```

### Manipulate Elements
```bash
agent-canvas delete-elements -i <id1>,<id2>,...
agent-canvas rotate-elements -i <id1>,<id2>,... -a <degrees>
agent-canvas move-elements -i <id1>,<id2>,... --delta-x <dx> --delta-y <dy>
agent-canvas group-elements -i <id1>,<id2>,...
agent-canvas ungroup-element -i <id>
```

### Read Scene
```bash
agent-canvas read                # TOON format (compact, ~7% of JSON size)
agent-canvas read --with-style   # Include stroke/bg colors
agent-canvas read --json         # Raw Excalidraw scene JSON
```

**TOON output structure:**
```
shapes[N]{id,type,x,y,w,h,angle,labelId,note}       # rectangle, ellipse, diamond, polygon
lines[N]{id,type,x,y,endX,endY,via,angle,note}      # line, arrow
labels[N]{id,containerId,content,x,y,w,h}           # text bound to shapes (via labelId)
texts[N]{id,content,x,y,w,h,angle,note}              # standalone text elements
groups[N]{id,elementIds}                             # element groupings
```

- `labelId` in shapes links to `id` in labels
- `via` shows intermediate points in same format as `--via` input (`"x1,y1;x2,y2"` or `null` if none)
- `--with-style` adds `stroke`, `bg` fields
- `--json` returns full Excalidraw format (use with `jq` to query specific elements)

### Save, Export and Clear
```bash
agent-canvas save file.excalidraw
agent-canvas export -o out.png [--scale 2] [--dark] [--no-background]
agent-canvas clear                # Clear all elements from the canvas
```
**Note**: Before running `clear`, ask the user if they want to save or export the current canvas first.

## Design Philosophy

**You are a perfectionist. If it looks slightly off, it IS off. Fix it.**

Core principles:
- **Alignment**: Snap to grid (e.g., 50px units). Same X for vertical alignment, same Y for horizontal
- **Spacing**: Identical gaps between same-level elements; consistent margins throughout
- **Color**: Max 3-4 colors; same color = same meaning; less is more
- **Size**: Same-type nodes share identical dimensions; important = larger
- **Details**: Arrows connect precisely to shape edges; review via `export` and fix imperfections

## IMPERATIVE GUIDE

1. **Coordinates**: Origin (0,0) is top-left. X→right, Y→down. Colors in hex (`#FF5733`) or `transparent`.

2. **Workflow**: Read canvas → Plan layout → Draw shapes FIRST → Then add arrows/lines.
   - **IMPORTANT**: Canvas content is auto-saved to browser localStorage. Always run `agent-canvas read` first to check for existing content before drawing.
   - If old content exists, ask the user whether to: (a) continue editing, (b) clear and start fresh, or (c) save/export first then clear.
   - Shapes define the layout and provide exact coordinates
   - Arrow endpoints depend on shape positions — drawing arrows first leads to misalignment

3. **Progressive Canvas Reading**:
   - `read` - Start here. Compact TOON format (~7% of JSON size)
   - `read --with-style` - Add color info when styling matters
   - `export -o canvas.png` + view image - For visual/spatial understanding
   - `read --json | jq '.elements[] | select(.id=="<id>")'` - Query specific element details

4. **Batch Commands**: Chain with `&&` for efficiency. DO NOT WRITE BASH COMMENT IN DRAWING COMMANDS
   ```bash
   agent-canvas add-shape -t rectangle -x 100 -y 100 -l "A" && \
   agent-canvas add-shape -t rectangle -x 300 -y 100 -l "B" && \
   agent-canvas add-arrow -x 220 -y 130 --end-x 300 --end-y 130
   ```

## Drawing Tutorials

**Before drawing, identify the diagram type and check for tutorials:**

1. Determine what type of diagram the user wants (flowchart, architecture, mindmap, UI mockup, etc.)
2. Read [references/REFERENCE.md](references/REFERENCE.md) — this is the **tutorial index** listing all available diagram tutorials
3. **If a matching tutorial exists**: Read the specific tutorial FIRST before drawing — tutorials contain type-specific rules, layout patterns, and best practices
4. Apply the tutorial guidelines while drawing