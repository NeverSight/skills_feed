---
name: geometric-elements
description: Generate decorative geometric elements (corners, lines, arcs, frames) with precise control over colors, gradients, and transparency. Use when creating design assets, slide decorations, or any vector-like graphics programmatically. Can also analyze reference images and recreate geometric patterns.
---

# Geometric Elements Generator

Create decorative geometric elements with code using Pixie-python.

## Quick Start

```bash
# Install dependency (first time only)
pip install pixie-python

# Generate element (ask user for brand color or check their brand guidelines)
python .claude/skills/geometric-elements/scripts/generate.py corner-accent \
  --color "#HEX_COLOR" \
  --size 200 \
  --output media/output/corner.png
```

**Important:** Always ask user for brand colors or check their brand guidelines skill (e.g., `/thepexcel-brand-guidelines`) before generating.

## Available Elements

| Element | Command | Description |
|---------|---------|-------------|
| **Basic Shapes** | `shape` | circle, star, heart, hexagon, arrow, etc. |
| Corner Accent | `corner-accent` | L-shaped corner decoration |
| Line Divider | `line-divider` | Horizontal divider with gradient |
| Arc Accent | `arc-accent` | Curved arc |
| Frame Border | `frame-border` | 4-corner bracket frame |
| Pattern | `pattern` | Repeating dots/crosses/diamonds |
| Mandala | `mandala` | Sacred geometry / complex patterns |

## Common Options

| Option | Description | Default |
|--------|-------------|---------|
| `--color` | Primary color (hex) | `#D4A84B` |
| `--color2` | Secondary color for gradient | None |
| `--size` | Element size in pixels | 200 |
| `--width` | Canvas width | 400 |
| `--height` | Canvas height | 400 |
| `--stroke` | Stroke width | 4 |
| `--output` | Output file path | `output.png` |
| `--gradient` | `linear` or `radial` | None |
| `--opacity` | 0.0-1.0 | 1.0 |
| `--fill` | Fill shape (vs stroke) | False |

## Examples

### Basic Shapes
```bash
# Circle (stroke)
python scripts/generate.py shape --style circle --color "#HEX" --size 100 --stroke 3

# Star (filled)
python scripts/generate.py shape --style star --color "#HEX" --size 100 --sides 5 --fill

# Available: circle, ellipse, rectangle, square, rounded-rect, triangle,
#   polygon, star, diamond, ring, cross, arrow, heart, hexagon, octagon, crescent
```

### Corner Accent
```bash
python scripts/generate.py corner-accent --color "#HEX" --size 150 --stroke 4
```

### Gradient Line Divider
```bash
python scripts/generate.py line-divider --color "#HEX" --color2 "#FFFFFF" --gradient linear --width 800
```

### Mandala (Sacred Geometry)
```bash
python scripts/generate.py mandala --color "#CCC" --bg "#0A0A0A" --size 400 --rings 8 --layers 4 --stroke 1.5
```

→ More examples: [references/element-catalog.md](references/element-catalog.md)

## Custom Elements (On-the-fly)

For complex patterns not in predefined commands, write Python directly:

```python
import pixie
import math

image = pixie.Image(400, 400)
paint = pixie.Paint(pixie.SOLID_PAINT)
paint.color = pixie.Color(0.83, 0.66, 0.29, 1.0)  # RGB 0-1 range

ctx = image.new_context()
ctx.stroke_style = paint
ctx.line_width = 2
ctx.stroke_segment(50, 50, 350, 350)

image.write_file("output.png")
```

→ Full API: [references/pixie-api.md](references/pixie-api.md)

## From Reference Image

User can send reference images for Claude to analyze and recreate:

1. **User sends image** — screenshot, design reference, pattern
2. **Claude analyzes** — identifies shapes, colors, proportions
3. **Claude writes code** — using pixie-python API
4. **Output** — PNG ready to use

**Tips for good reference:** Clear image, geometric patterns (not photos), specify hex colors if needed.

## Tips

1. **Transparent bg** — All outputs have transparent background by default
2. **High DPI** — Use `--size` 2x for retina displays
3. **Gradients** — Combine `--gradient linear` with `--color` and `--color2`
4. **Brand colors** — Always confirm with user or their brand guidelines first
