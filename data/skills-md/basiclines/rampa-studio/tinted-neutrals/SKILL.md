---
name: tinted-neutrals
description: Generate neutral gray palettes with subtle brand color tinting. Use when you want grays that feel connected to your brand rather than pure neutral grays.
license: SEE LICENSE IN LICENSE.md
metadata:
  author: ismael.fyi
  version: "1.0.0"
---

# Tinted Neutrals

Create neutral palettes that carry a subtle hint of your brand color. Instead of pure grays, get warm or cool neutrals that feel cohesive with your design system.

## When to Use

- "Create grays that match my brand"
- "I want warm/cool neutrals"
- "Make my grays less boring"
- "Tint my neutral palette with brand color"

## Installation

```bash
npx @basiclines/rampa
```

## Recipe

### 1. Pure Neutral (Desaturated Brand)

Start with neutrals derived from your brand color's hue but heavily desaturated:

```bash
rampa -C "<brand-color>" -L 98:5 -S 3:8 --size=10 -O css --name=neutral
```

### 2. Tinted Neutral

Apply your brand color as a subtle overlay tint:

```bash
rampa -C "<brand-color>" -L 98:5 -S 3:8 --tint-color="<brand-color>" --tint-opacity=8 --tint-blend=overlay --size=10 -O css --name=neutral-tinted
```

**Key:** The `--tint-color` uses the same brand color - no hardcoded values!

## Tint Intensity Options

### Subtle Tint (5-8%)
Barely noticeable but adds warmth/coolness:
```bash
--tint-opacity=6 --tint-blend=overlay
```

### Medium Tint (10-15%)
Clearly tinted but still neutral:
```bash
--tint-opacity=12 --tint-blend=overlay
```

### Strong Tint (18-25%)
Obviously colored neutrals:
```bash
--tint-opacity=20 --tint-blend=soft-light
```

## Blend Mode Options

| Mode | Effect |
|------|--------|
| `overlay` | Balanced tint, good default |
| `soft-light` | Gentler, more subtle |
| `multiply` | Darker, richer tones |
| `screen` | Lighter, airier tones |
| `color` | Applies hue without changing lightness |

## Complete Example

For brand color `#7c3aed` (purple):

```bash
# Pure neutral (cool-ish from purple hue)
rampa -C "#7c3aed" -L 98:5 -S 3:8 --size=10 -O css --name=gray

# Tinted neutral (purple tint)
rampa -C "#7c3aed" -L 98:5 -S 3:8 --tint-color="#7c3aed" --tint-opacity=8 --tint-blend=overlay --size=10 -O css --name=gray-tinted

# Compare: extra warm variant
rampa -C "#7c3aed" -L 98:5 -S 3:8 --tint-color="#7c3aed" --tint-opacity=15 --tint-blend=soft-light --size=10 -O css --name=gray-warm
```

## Output Structure

```css
:root {
  /* Pure neutral */
  --gray-0: #fafafa;
  --gray-1: #f4f4f5;
  --gray-9: #18181b;

  /* Tinted neutral */
  --gray-tinted-0: #faf8fc;
  --gray-tinted-1: #f3f0f7;
  --gray-tinted-9: #1a1720;
}
```

## Tips

1. Always use the brand color as tint source - never hardcode gray
2. `overlay` blend mode works for most cases
3. Keep opacity under 15% for "still feels neutral"
4. Test on both light and dark backgrounds
5. Tinted neutrals make white text pop more on dark backgrounds
