---
name: accessible-contrast
description: Generate color ramps designed for WCAG-compliant contrast pairing. Creates 11-step scales with predictable foreground/background combinations.
license: SEE LICENSE IN LICENSE.md
metadata:
  author: ismael.fyi
  version: "1.0.0"
---

# Accessible Contrast Pairs

Generate color ramps specifically designed for accessible text/background combinations. Uses an 11-step scale for predictable WCAG-compliant pairing.

## When to Use

- "Create accessible color combinations"
- "I need WCAG compliant colors"
- "Generate high contrast pairs"
- "Make sure my text is readable"

## Installation

```bash
npx @basiclines/rampa
```

## The 11-Step Strategy

Why 11 steps? It creates predictable pairing math:

| Pair | Indices | Contrast Level |
|------|---------|----------------|
| Maximum | 0 + 10 | Highest (near white + near black) |
| AAA Normal | 1 + 9, 2 + 8 | 7:1+ ratio |
| AA Normal | 3 + 7 | 4.5:1+ ratio |
| AA Large | 4 + 6 | 3:1+ ratio |

## Recipe

```bash
rampa -C "<brand-color>" -L 98:5 --size=11 -O css --name=color
```

- `-L 98:5` ensures full range from near-white to near-black
- `--size=11` creates indices 0-10 for easy pairing
- Pairs are symmetrical: 0+10, 1+9, 2+8, etc.

## Complete Example

For brand color `#3b82f6`:

```bash
rampa -C "#3b82f6" -L 98:5 --size=11 -O css --name=blue
```

Output:
```css
:root {
  --blue-0: #f8fafc;   /* Near white */
  --blue-1: #f1f5f9;
  --blue-2: #e2e8f0;
  --blue-3: #cbd5e1;
  --blue-4: #94a3b8;
  --blue-5: #64748b;   /* Middle gray */
  --blue-6: #475569;
  --blue-7: #334155;
  --blue-8: #1e293b;
  --blue-9: #0f172a;
  --blue-10: #020617;  /* Near black */
}
```

## Contrast Pairing Guide

### For Normal Text (4.5:1 minimum - WCAG AA)

```css
/* Light backgrounds with dark text */
.light-subtle {
  background: var(--blue-0);
  color: var(--blue-7);  /* 0+7 = AA */
}

.light-default {
  background: var(--blue-1);
  color: var(--blue-8);  /* 1+8 = AA */
}

.light-strong {
  background: var(--blue-2);
  color: var(--blue-9);  /* 2+9 = AAA */
}

/* Dark backgrounds with light text */
.dark-subtle {
  background: var(--blue-10);
  color: var(--blue-3);  /* 10+3 = AA */
}

.dark-default {
  background: var(--blue-9);
  color: var(--blue-2);  /* 9+2 = AA */
}

.dark-strong {
  background: var(--blue-8);
  color: var(--blue-1);  /* 8+1 = AAA */
}
```

### For Large Text (3:1 minimum - WCAG AA)

```css
.large-text {
  background: var(--blue-3);
  color: var(--blue-7);  /* 3+7 = AA Large */
}
```

### Maximum Contrast

```css
.max-contrast {
  background: var(--blue-0);
  color: var(--blue-10);  /* 0+10 = Maximum */
}
```

## Quick Reference Table

| Background | Text for AA | Text for AAA |
|------------|-------------|--------------|
| 0 | 7, 8, 9, 10 | 8, 9, 10 |
| 1 | 7, 8, 9, 10 | 8, 9, 10 |
| 2 | 8, 9, 10 | 9, 10 |
| 3 | 8, 9, 10 | 9, 10 |
| 7 | 0, 1, 2, 3 | 0, 1, 2 |
| 8 | 0, 1, 2, 3 | 0, 1, 2 |
| 9 | 0, 1, 2 | 0, 1 |
| 10 | 0, 1, 2 | 0, 1 |

## Multiple Colors

Generate accessible ramps for multiple brand colors:

```bash
rampa -C "#3b82f6" -L 98:5 --size=11 -O css --name=blue
rampa -C "#22c55e" -L 98:5 --size=11 -O css --name=green
rampa -C "#ef4444" -L 98:5 --size=11 -O css --name=red
```

All ramps use the same index pairing logic.

## Tips

1. The `-L 98:5` range is crucial - it ensures full contrast range
2. Middle values (4, 5, 6) work for disabled/muted states
3. Always test actual rendered contrast - tools like Stark, axe can verify
4. The index math (0+10, 1+9, 2+8) makes theming predictable
5. For buttons: use index 5-6 as background, 0-1 as text
