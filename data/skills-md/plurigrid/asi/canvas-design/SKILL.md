---
name: canvas-design
description: Create beautiful visual art in .png and .pdf documents using design philosophy.
version: 1.0.0
---


# Canvas Design

Create visually striking static designs using HTML Canvas or Python imaging libraries.

## Design Principles

### Composition
- **Rule of Thirds**: Place key elements along grid lines
- **Visual Hierarchy**: Size, color, and position indicate importance
- **White Space**: Embrace negative space for elegance
- **Balance**: Symmetrical for formal, asymmetrical for dynamic

### Color Theory
- **Complementary**: Colors opposite on wheel (high contrast)
- **Analogous**: Adjacent colors (harmonious)
- **Triadic**: Three equidistant colors (vibrant)
- Limit palette to 3-5 colors

### Typography
- Pair one display font with one body font
- Maintain consistent hierarchy
- Ensure readability (contrast, size)

## Python Canvas (Pillow + Cairo)

```python
from PIL import Image, ImageDraw, ImageFont
import cairo

# Create canvas
width, height = 1200, 800
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background gradient
pattern = cairo.LinearGradient(0, 0, 0, height)
pattern.add_color_stop_rgb(0, 0.1, 0.1, 0.2)
pattern.add_color_stop_rgb(1, 0.05, 0.05, 0.1)
ctx.set_source(pattern)
ctx.paint()

# Draw shapes
ctx.set_source_rgba(1, 0.3, 0.3, 0.8)
ctx.arc(600, 400, 150, 0, 2 * 3.14159)
ctx.fill()

# Add text
ctx.set_source_rgb(1, 1, 1)
ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(48)
ctx.move_to(400, 600)
ctx.show_text("Hello Design")

# Save
surface.write_to_png("design.png")
```

## HTML Canvas to Image

```javascript
const canvas = document.createElement('canvas');
canvas.width = 1200;
canvas.height = 800;
const ctx = canvas.getContext('2d');

// Draw
ctx.fillStyle = '#1a1a2e';
ctx.fillRect(0, 0, 1200, 800);

ctx.fillStyle = '#e94560';
ctx.beginPath();
ctx.arc(600, 400, 150, 0, Math.PI * 2);
ctx.fill();

// Export
const dataUrl = canvas.toDataURL('image/png');
```

## Design Styles

- **Minimalist**: Limited colors, lots of whitespace, clean lines
- **Brutalist**: Raw, bold typography, stark contrasts
- **Glassmorphism**: Frosted glass effects, subtle borders
- **Retro/Vintage**: Muted colors, textures, classic typography
- **Abstract**: Geometric shapes, gradients, artistic composition



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 4. Pattern Matching

**Concepts**: unification, match, segment variables, pattern

### GF(3) Balanced Triad

```
canvas-design (−) + SDF.Ch4 (+) + [balancer] (○) = 0
```

**Skill Trit**: -1 (MINUS - verification)


### Connection Pattern

Pattern matching extracts structure. This skill recognizes and transforms patterns.
## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.