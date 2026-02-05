---
name: brand-expansion
description: Expand a single brand color into a complete multi-hue color system using harmonies. Creates primary, analogous, complementary, and split-complementary ramps.
license: SEE LICENSE IN LICENSE.md
metadata:
  author: ismael.fyi
  version: "1.0.0"
---

# Brand Expansion

Transform a single brand color into a complete, cohesive color system. Uses multiple harmony types to generate related hues - all mathematically derived from one input.

## When to Use

- "Expand my brand color into a full system"
- "I only have one color, need more"
- "Create a complete palette from this hex"
- "Build a color system from my logo color"

## Installation

```bash
npx @basiclines/rampa
```

## The Expansion Strategy

From one brand color, generate:

1. **Primary** - Full ramp of the brand color
2. **Analogous** - Adjacent colors for subtle variations
3. **Complementary** - Opposite color for contrast/CTAs
4. **Split-complementary** - Softer contrast options

## Recipe

### Step 1: Primary Ramp

The brand color expanded to full 10-shade scale:

```bash
rampa -C "<brand-color>" -L 95:10 --size=10 -O css --name=primary
```

### Step 2: Analogous Colors

Colors adjacent on the wheel (±30°) - great for subtle variations:

```bash
rampa -C "<brand-color>" --add=analogous -L 95:10 --size=10 -O css
```

Outputs: `base`, `analogous-1`, `analogous-2`

### Step 3: Complementary Color

Direct opposite for maximum contrast - perfect for CTAs:

```bash
rampa -C "<brand-color>" --add=complementary -L 95:10 --size=10 -O css
```

Outputs: `base`, `complementary-1`

### Step 4: Split-Complementary

Two colors flanking the complement - more nuanced contrast:

```bash
rampa -C "<brand-color>" --add=split-complementary -L 95:10 --size=10 -O css
```

Outputs: `base`, `split-complementary-1`, `split-complementary-2`

## Complete Example

For brand color `#7c3aed` (purple):

```bash
# Primary - the purple itself
rampa -C "#7c3aed" -L 95:10 --size=10 -O css --name=primary

# Analogous - blue and magenta variations
rampa -C "#7c3aed" --add=analogous -L 95:10 --size=10 -O css

# Complementary - lime/yellow for CTAs
rampa -C "#7c3aed" --add=complementary -L 95:10 --size=10 -O css

# Split-complementary - yellow-green options
rampa -C "#7c3aed" --add=split-complementary -L 95:10 --size=10 -O css
```

## Output Structure

```css
:root {
  /* Primary */
  --primary-0: #faf5ff;
  --primary-5: #7c3aed;
  --primary-9: #2e1065;

  /* Analogous */
  --analogous-1-0: #eff6ff;  /* Blue-ish */
  --analogous-1-5: #3b82f6;
  --analogous-2-0: #fdf2f8;  /* Pink-ish */
  --analogous-2-5: #ec4899;

  /* Complementary */
  --complementary-1-0: #fefce8;  /* Yellow/lime */
  --complementary-1-5: #84cc16;

  /* Split-complementary */
  --split-complementary-1-0: #f0fdf4;  /* Green */
  --split-complementary-2-0: #fefce8;  /* Yellow */
}
```

## Usage Guide

| Harmony | Best For |
|---------|----------|
| Primary | Main brand applications, headers, primary buttons |
| Analogous | Hover states, related sections, gradients |
| Complementary | CTAs, alerts, highlights that need attention |
| Split-complementary | Secondary actions, badges, alternative accents |

## All-in-One Command

For a quick overview with minimal output:

```bash
# See all harmonies at once
rampa -C "#7c3aed" --add=analogous --add=complementary --add=split-complementary --size=3 -O css
```

## Tips

1. Start with just primary + complementary, add more as needed
2. Analogous colors are great for gradients and transitions
3. Use complementary sparingly - it demands attention
4. Split-complementary offers contrast without the intensity of direct complement
5. All colors share mathematical relationships = automatic cohesion
