---
name: status-from-accent
description: Generate success, warning, danger, and info status colors that harmonize with your brand using square harmony. All colors mathematically derived from one input.
license: SEE LICENSE IN LICENSE.md
metadata:
  author: ismael.fyi
  version: "1.0.0"
---

# Status Colors from Accent

Generate a complete set of status/feedback colors (success, warning, danger, info) that are mathematically related to your brand color using square harmony.

## When to Use

- "Create status colors that match my brand"
- "I need success, warning, error colors"
- "Generate feedback colors from my accent"
- "Make danger/success colors that feel on-brand"

## Installation

```bash
npx @basiclines/rampa
```

## The Square Harmony Approach

Square harmony generates 4 colors at 90° intervals on the color wheel. This gives you maximum distinction while maintaining mathematical relationships.

```bash
rampa -C "<brand-color>" --add=square -L 95:15 --size=10 -O css
```

This outputs 4 ramps:
- `base` - your brand color (use as info/primary)
- `square-1` - +90° rotation
- `square-2` - +180° rotation (opposite)
- `square-3` - +270° rotation

## Mapping Hues to Status

The actual colors depend on your input. After generation, map based on hue:

| Hue Range | Typical Status |
|-----------|---------------|
| 80-150° | Success (green/teal) |
| 30-80° | Warning (yellow/orange) |
| 0-30° or 330-360° | Danger (red/pink) |
| 180-270° | Info (blue/purple) |

**Example:** If your brand is blue (#3b82f6, ~220°):
- base (220°) → Info
- square-1 (310°) → Danger (magenta/red zone)
- square-2 (40°) → Warning (orange zone)
- square-3 (130°) → Success (green zone)

## Complete Example

```bash
# Generate all 4 status ramps from blue brand
rampa -C "#3b82f6" --add=square -L 95:15 --size=10 -O css
```

Output includes 4 full ramps - assign semantic meaning based on hue:

```css
:root {
  /* Info (base - blue) */
  --base-0: #eff6ff;
  --base-5: #3b82f6;
  --base-9: #1e3a8a;

  /* Danger (square-1 - magenta/red) */
  --square-1-0: #fdf2f8;
  --square-1-5: #ec4899;
  --square-1-9: #831843;

  /* Warning (square-2 - orange) */
  --square-2-0: #fff7ed;
  --square-2-5: #f97316;
  --square-2-9: #7c2d12;

  /* Success (square-3 - green) */
  --square-3-0: #f0fdf4;
  --square-3-5: #22c55e;
  --square-3-9: #14532d;
}
```

## Renaming for Semantics

After identifying which ramp is which, you can re-run with explicit names:

```bash
# If you know square-3 is your green/success
rampa -C "#22c55e" -L 95:15 --size=10 -O css --name=success
```

Or map in your CSS:
```css
:root {
  --success: var(--square-3-5);
  --warning: var(--square-2-5);
  --danger: var(--square-1-5);
  --info: var(--base-5);
}
```

## Alternative: Custom Status Base

If the generated hues don't land exactly where you want, adjust the input:

```bash
# Start from green to ensure success is the base
rampa -C "#22c55e" --add=square -L 95:15 --size=10 -O css
# Now: base=green, square-1=blue, square-2=red, square-3=yellow
```

## Tips

1. Square harmony guarantees maximum visual distinction
2. All 4 colors share the same "mathematical DNA"
3. The `-L 95:15` range works well for status colors (light bg, dark text)
4. Use `--size=10` for full ramp, `--size=5` for minimal
5. Mid-ramp values (4-6) work best for badges, buttons, alerts
