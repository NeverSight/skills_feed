---
name: rampa-colors
description: Generate mathematically accurate color palettes using OKLCH color space. Use when creating design systems, color ramps, accessible palettes, CSS variables for themes, or when user asks about color generation.
license: SEE LICENSE IN LICENSE.md
metadata:
  author: ismael.fyi
  version: "1.0.1"
---

# Rampa Color Palette Generator

Generate perceptually uniform color palettes from a base color using the OKLCH color space.

## Installation

```bash
# Run directly
npx @basiclines/rampa -C "#3b82f6"

# Or install globally
npm install -g @basiclines/rampa
```

## Quick Examples

### Generate a basic 10-color palette
```bash
rampa -C "#3b82f6"
```

### Output as CSS variables
```bash
rampa -C "#3b82f6" -O css --name=primary
```
Output:
```css
:root {
  --primary-0: #000000;
  --primary-1: #1e3a5f;
  --primary-2: #2d5a8a;
  ...
}
```

### Output as JSON
```bash
rampa -C "#3b82f6" -O json
```

### Add complementary harmony
```bash
rampa -C "#3b82f6" --add=complementary -O css
```

### Custom lightness and saturation ranges
```bash
rampa -C "#3b82f6" -L 15:95 -S 100:20
```

### Use Fibonacci distribution scale
```bash
rampa -C "#3b82f6" --lightness-scale=fibonacci
```

### Generate 5 colors with triadic harmony
```bash
rampa -C "#3b82f6" --size=5 --add=triadic -O css --name=brand
```

## All Options

| Flag | Alias | Description | Default |
|------|-------|-------------|---------|
| `--color` | `-C` | **Required.** Base color (hex, rgb, hsl, or named) | - |
| `--size` | - | Number of colors in palette | 10 |
| `--output` | `-O` | Output format: `text`, `json`, `css` | text |
| `--format` | `-F` | Color format: `hex`, `rgb`, `hsl`, `oklch` | hex |
| `--name` | - | Palette name (for CSS/JSON output) | base |
| `--lightness` | `-L` | Lightness range (e.g., `15:95`) | 0:100 |
| `--saturation` | `-S` | Saturation range (e.g., `100:20`) | 100:0 |
| `--hue` | `-H` | Hue shift range (e.g., `-10:10`) | -10:10 |
| `--lightness-scale` | - | Distribution scale for lightness | linear |
| `--saturation-scale` | - | Distribution scale for saturation | linear |
| `--hue-scale` | - | Distribution scale for hue | linear |
| `--add` | - | Add harmony ramp | - |
| `--tint-color` | - | Tint overlay color | - |
| `--tint-opacity` | - | Tint opacity (0-100) | 10 |
| `--tint-blend` | - | Tint blend mode | overlay |
| `--no-preview` | - | Hide color preview blocks | false |

## Scale Types

Control how values are distributed across the palette:

- `linear` - Even spacing (default)
- `fibonacci` - Fibonacci sequence
- `golden-ratio` - Golden ratio progression
- `ease-in` - Slow start, fast end
- `ease-out` - Fast start, slow end
- `ease-in-out` - Slow start and end
- `geometric` - Exponential growth
- `logarithmic` - Logarithmic curve

## Harmony Types

Generate related color ramps:

- `complementary` - Opposite on color wheel (+1 ramp)
- `triadic` - 3 colors, 120° apart (+2 ramps)
- `analogous` - Adjacent colors, 30° apart (+2 ramps)
- `split-complementary` - 2 colors near opposite (+2 ramps)
- `square` - 4 colors, 90° apart (+3 ramps)

## Blend Modes (for tinting)

`normal` · `multiply` · `screen` · `overlay` · `darken` · `lighten` · `color-dodge` · `color-burn` · `hard-light` · `soft-light`

## When to Use This Skill

- User asks to "generate a color palette"
- User needs "CSS color variables"
- User wants "accessible colors" or "design system colors"
- User mentions "color ramp" or "color scale"
- User needs "complementary/triadic/analogous colors"
- User wants "perceptually uniform" colors
- User is building a theme or design tokens

## Tips

1. For dark mode themes, use `-L 5:85` to avoid pure black/white
2. For muted palettes, use `-S 60:20`
3. Use `--add=analogous` for harmonious multi-color themes
4. Use `-O json` when you need to process colors programmatically
5. Combine with `--size=5` for minimal palettes
