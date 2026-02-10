---
name: svg-art
description: Create SVG graphics through programmatic code generation. Use this skill when the user asks to create icons, logos, illustrations, diagrams, data visualizations, generative art, patterns, fractals, or any vector graphics. Provides executable Python scripts for grids, radial patterns, fractals, waves, particles, charts, icons, and optimization.
---

# SVG Art: Programmatic Generation

Generate high-quality SVG graphics using Python scripts. All scripts output valid SVG to stdout (or file with `-o`).

## Available Scripts

| Script | Purpose | Key Options |
|--------|---------|-------------|
| `generate_grid.py` | Grid patterns | `--cols`, `--rows`, `--shape`, `--vary-*` |
| `generate_radial.py` | Radial/spiral/sunburst | `--spiral`, `--concentric`, `--sunburst` |
| `generate_fractal.py` | Fractals (tree, koch, sierpinski) | `--tree`, `--koch`, `--sierpinski`, `--depth` |
| `generate_wave.py` | Waves and audio viz | `--layers`, `--noise`, `--bars` |
| `generate_particles.py` | Scatter/cluster/constellation | `--cluster`, `--gradient`, `--constellation` |
| `generate_chart.py` | Data visualization | `--bar`, `--line`, `--pie`, `--donut` |
| `generate_icon.py` | Common UI icons | `--icon NAME`, `--list`, `--filled` |
| `optimize_svg.py` | Minify/optimize SVG | `--aggressive`, `--stats` |

## Quick Examples

```bash
# Grid with size variation
python scripts/generate_grid.py -c 6 -r 6 --vary-size --vary-opacity -o grid.svg

# Spiral pattern
python scripts/generate_radial.py --spiral -n 60 --turns 4 -o spiral.svg

# Fractal tree
python scripts/generate_fractal.py --tree --depth 8 --vary-angle -o tree.svg

# Layered waves with fill
python scripts/generate_wave.py --layers 5 --fill -o waves.svg

# Constellation network
python scripts/generate_particles.py --constellation -n 30 --connect-distance 25 -o network.svg

# Bar chart
python scripts/generate_chart.py --bar --data "30,50,80,45,90" --labels "A,B,C,D,E" -o chart.svg

# Heart icon
python scripts/generate_icon.py --icon heart --filled --stroke "#E11D48" -o heart.svg

# Optimize existing SVG
python scripts/optimize_svg.py input.svg --aggressive -o output.svg
```

## Script Usage Patterns

### Grid Patterns
```bash
python scripts/generate_grid.py \
  -c 8 -r 8           # columns and rows
  -s 10 -g 2          # size and gap
  --shape circle      # rect, circle, or diamond
  --vary-size         # random size variation
  --vary-opacity      # random opacity
  --vary-hue          # color variation
  --seed 42           # reproducible randomness
```

### Radial Patterns
```bash
# Concentric rings
python scripts/generate_radial.py --concentric --rings 5 --vary-hue

# Sunburst rays
python scripts/generate_radial.py --sunburst -n 24 --vary-length
```

### Fractals
```bash
# Koch snowflake
python scripts/generate_fractal.py --koch --depth 4 --fill "#3B82F6"

# Sierpinski triangle
python scripts/generate_fractal.py --sierpinski --depth 5
```

### Charts
```bash
# Line chart with points
python scripts/generate_chart.py --line --data "10,30,20,50" --show-points --smooth

# Donut chart
python scripts/generate_chart.py --donut --data "40,30,20,10" --labels "A,B,C,D"
```

### Icons
```bash
# List all available icons
python scripts/generate_icon.py --list

# Common icons: check, x, plus, menu, search, home, user, settings,
# mail, heart, star, play, file, download, edit, share, sun, moon, etc.
```

## Common Options (All Scripts)

- `--fill COLOR`: Fill color (default: #3B82F6)
- `--stroke COLOR`: Stroke color
- `--stroke-width N`: Stroke width
- `--seed N`: Random seed for reproducibility
- `-o FILE`: Output to file instead of stdout

## Piping and Composition

Scripts can be piped together:
```bash
# Generate and optimize
python scripts/generate_grid.py -c 10 -r 10 | python scripts/optimize_svg.py --aggressive

# Check optimization stats
python scripts/generate_fractal.py --tree --depth 10 | python scripts/optimize_svg.py --stats
```

## SVG Fundamentals Reference

See [references/svg-fundamentals.md](references/svg-fundamentals.md) for:
- Core SVG structure and viewBox
- Element types (rect, circle, path, etc.)
- Path command syntax
- Gradients and patterns
- Accessibility requirements
