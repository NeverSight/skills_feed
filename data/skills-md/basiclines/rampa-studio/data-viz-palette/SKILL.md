---
name: data-viz-palette
description: Generate distinct, accessible colors for charts, graphs, and data visualizations. Uses color harmonies for maximum perceptual distinction.
license: SEE LICENSE IN LICENSE.md
metadata:
  author: ismael.fyi
  version: "1.0.0"
---

# Data Visualization Palette

Generate color sets optimized for charts, graphs, and dashboards. Colors are mathematically spaced for maximum distinction and equal visual weight.

## When to Use

- "Create colors for my chart"
- "I need a data visualization palette"
- "Generate distinct colors for a graph"
- "Colors for dashboard charts"

## Installation

```bash
npx @basiclines/rampa
```

## Key Principles

1. **Fixed lightness** - All colors at same lightness = equal visual weight
2. **Fixed saturation** - Consistent vibrancy across the palette
3. **Maximum hue spacing** - Use harmonies for perceptual distinction
4. **Single shade per color** - Data viz needs distinct hues, not ramps

## Recipes by Color Count

### 3 Colors (Triadic)

Perfect for pie charts, simple bar charts:

```bash
rampa -C "<brand-color>" --add=triadic --size=2 -L 50:50 -S 70:70 -O css
```

Outputs: `base`, `triadic-1`, `triadic-2` (120° apart)

### 4 Colors (Square)

Good for quarterly data, four-category comparisons:

```bash
rampa -C "<brand-color>" --add=square --size=2 -L 50:50 -S 70:70 -O css
```

Outputs: `base`, `square-1`, `square-2`, `square-3` (90° apart)

### 4 Colors (Compound)

Alternative with complementary + split for more nuance:

```bash
rampa -C "<brand-color>" --add=compound --size=2 -L 50:50 -S 75:75 -O css
```

### 6 Colors

Combine triadic with complementary:

```bash
rampa -C "<brand-color>" --add=triadic -L 50:50 -S 70:70 --size=2 -O json
# Then run complementary of each triadic color
```

Or use two interlocking triads at different lightness:

```bash
# Primary triad
rampa -C "<brand-color>" --add=triadic --size=2 -L 45:45 -S 70:70 -O css

# Offset triad (shift hue by 60°)
rampa -C "<brand-color>" --add=triadic --size=2 -L 60:60 -S 70:70 -H 60:60 -O css
```

## Complete Example

For brand color `#3b82f6`:

```bash
# 4-color chart palette
rampa -C "#3b82f6" --add=square --size=2 -L 50:50 -S 70:70 -O css
```

Output:
```css
:root {
  --base-0: #3b82f6;      /* Blue */
  --square-1-0: #a855f7;  /* Purple */
  --square-2-0: #f97316;  /* Orange */
  --square-3-0: #22c55e;  /* Green */
}
```

## Lightness Recommendations

| Background | Recommended Lightness |
|------------|----------------------|
| White (#fff) | 45-55% |
| Light gray (#f5f5f5) | 45-55% |
| Dark (#1a1a1a) | 55-65% |
| Black (#000) | 60-70% |

## Saturation Guidelines

| Use Case | Saturation |
|----------|------------|
| Bold, attention-grabbing | 75-85% |
| Professional, muted | 55-65% |
| Accessible (colorblind-friendly) | 60-70% |

## Colorblind Considerations

For colorblind-safe palettes:

1. **Avoid red-green pairs** as primary distinction
2. **Vary lightness slightly** if using similar hues
3. **Use patterns/shapes** as backup identifiers

Example with lightness variation:
```bash
rampa -C "#3b82f6" --add=square --size=1 -L 40:40 -S 70:70 -O css  # darker
rampa -C "#3b82f6" --add=square --size=1 -L 60:60 -S 70:70 -O css  # lighter
```

## Tips

1. `--size=2` gives minimal ramps (2 shades each) - good for data viz
2. Keep saturation consistent across all colors
3. Test on both light and dark chart backgrounds
4. For legends, the order should match visual prominence
5. Add a neutral gray for "no data" or baseline values
