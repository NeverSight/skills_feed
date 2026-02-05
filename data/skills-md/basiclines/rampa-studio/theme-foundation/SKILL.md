---
name: theme-foundation
description: Create a complete theme foundation with accent, secondary, and neutral color ramps from a single brand color. Use when building light/dark mode themes or starting a new design system.
license: SEE LICENSE IN LICENSE.md
metadata:
  author: ismael.fyi
  version: "1.0.0"
---

# Theme Foundation

Generate a complete theme color system from a single brand color. Creates primary accent, secondary accent (complementary), and neutral ramps - all mathematically derived.

## When to Use

- "Create a theme from my brand color"
- "I need colors for light and dark mode"
- "Generate a color system for my app"
- "Start a new design system with this color"

## Installation

```bash
npx @basiclines/rampa
```

## Recipe

Given a user's brand color, generate three ramp types:

### 1. Primary Accent Ramp

The main brand color expanded to a full 10-shade scale.

```bash
rampa -C "<brand-color>" -L 95:10 --size=10 -O css --name=accent
```

### 2. Secondary Accent (Complementary)

Mathematically opposite on the color wheel - perfect for CTAs, highlights, or secondary actions.

```bash
rampa -C "<brand-color>" --add=complementary -L 95:10 --size=10 -O css
```

This outputs two ramps:
- `base` - the primary accent
- `complementary-1` - the secondary accent

### 3. Neutral Ramp

Derived from the brand color but heavily desaturated. This creates "warm" or "cool" neutrals that feel cohesive with the brand.

```bash
rampa -C "<brand-color>" -L 98:5 -S 5:10 --size=10 -O css --name=neutral
```

## Complete Example

For brand color `#3b82f6` (blue):

```bash
# Primary accent
rampa -C "#3b82f6" -L 95:10 --size=10 -O css --name=accent

# Secondary + Primary together
rampa -C "#3b82f6" --add=complementary -L 95:10 --size=10 -O css

# Neutrals (slightly warm from the blue)
rampa -C "#3b82f6" -L 98:5 -S 5:10 --size=10 -O css --name=neutral
```

## Output Structure

```css
:root {
  /* Primary Accent */
  --accent-0: #f0f7ff;
  --accent-1: #dbeafe;
  /* ... */
  --accent-9: #1e3a5f;

  /* Secondary Accent (complementary) */
  --complementary-1-0: #fff7ed;
  --complementary-1-1: #ffedd5;
  /* ... */

  /* Neutrals */
  --neutral-0: #fafafa;
  --neutral-1: #f5f5f5;
  /* ... */
  --neutral-9: #171717;
}
```

## Light vs Dark Mode

The same ramps work for both modes - just map them differently:

**Light Mode:**
- Background: `neutral-0` to `neutral-2`
- Text: `neutral-8` to `neutral-9`
- Accent: `accent-5` to `accent-7`

**Dark Mode:**
- Background: `neutral-9` to `neutral-7`
- Text: `neutral-0` to `neutral-2`
- Accent: `accent-3` to `accent-5`

## Tips

1. The complementary color is mathematically guaranteed to contrast with the primary
2. Neutrals inherit subtle warmth/coolness from the brand color
3. Use `--size=11` for more granular control
4. Adjust `-L` range for more/less contrast (e.g., `-L 90:20` for less extreme)
