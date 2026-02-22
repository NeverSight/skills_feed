---
name: extract-theme
description: Extract a website's complete visual theme (colors, typography, spacing, gradients, shadows, border radii) using Chrome DevTools and convert it to a tweakcn-compatible shadcn/ui CSS theme. Use when the user wants to clone or replicate a website's design system into their Tailwind CSS / shadcn project.
metadata:
  author: occult
  version: "1.0"
---

# Extract Website Theme to Tweakcn

Extract a website's visual theme using Chrome DevTools and convert it to a tweakcn-compatible shadcn/ui CSS theme (HSL format).

## Step 1: Provide Extraction Script

Tell the user to open Chrome DevTools Console on the target site and run this script. It copies a full theme JSON to their clipboard:

```js
(() => {
  const res = { typography: [], spacing: [], gradients: [], shadows: [], borders: [], radii: [], colors: new Set() };
  const typoMap = new Map(), spacingMap = new Map(), radiiMap = new Map();
  document.querySelectorAll('*').forEach(el => {
    const s = getComputedStyle(el);
    const tk = `${s.fontSize}|${s.fontWeight}|${s.lineHeight}|${s.letterSpacing}`;
    if (!typoMap.has(tk)) typoMap.set(tk, { fontSize: s.fontSize, fontWeight: s.fontWeight, lineHeight: s.lineHeight, letterSpacing: s.letterSpacing, tag: el.tagName, sample: el.textContent?.trim().slice(0, 30) });
    ['padding','margin','gap'].forEach(p => { const v = s[p]; if (v && v !== '0px' && v !== 'normal') spacingMap.set(v, (spacingMap.get(v)||0)+1); });
    if (s.backgroundImage !== 'none' && s.backgroundImage.includes('gradient')) res.gradients.push(s.backgroundImage);
    if (s.boxShadow !== 'none') res.shadows.push(s.boxShadow);
    if (s.borderStyle !== 'none' && s.borderWidth !== '0px') res.borders.push(`${s.borderWidth} ${s.borderStyle} ${s.borderColor} r:${s.borderRadius}`);
    if (s.borderRadius !== '0px') radiiMap.set(s.borderRadius, (radiiMap.get(s.borderRadius)||0)+1);
    [s.color, s.backgroundColor, s.borderColor].forEach(c => { if (c && c !== 'rgba(0, 0, 0, 0)') res.colors.add(c); });
  });
  res.typography = [...typoMap.values()].sort((a, b) => parseFloat(b.fontSize) - parseFloat(a.fontSize)).slice(0, 20);
  res.spacing = [...spacingMap.entries()].sort((a, b) => b[1] - a[1]).slice(0, 20).map(([v, c]) => ({ value: v, count: c }));
  res.radii = [...radiiMap.entries()].sort((a, b) => b[1] - a[1]).slice(0, 10).map(([v, c]) => ({ radius: v, count: c }));
  res.gradients = [...new Set(res.gradients)];
  res.shadows = [...new Set(res.shadows)];
  res.borders = [...new Set(res.borders)].slice(0, 15);
  res.colors = [...res.colors];
  copy(JSON.stringify(res, null, 2));
  console.log('Copied full theme extraction to clipboard');
})();
```

Also ask the user for a screenshot of the site for visual reference, and the site URL if public.

## Step 2: Analyze Extraction Data

When the user pastes the JSON output, analyze all sections:

### Colors
Identify and categorize every color by role:
- **Background**: The dominant dark or light page background
- **Foreground**: Default text color (usually white on dark, dark on light)
- **Card**: Elevated surface color (slightly lighter/darker than background)
- **Popover**: Dropdown/popover bg (slightly elevated from card)
- **Primary**: Main brand/action color (CTAs, active nav, links)
- **Secondary**: Supporting surface color (nav pills, tags, badges)
- **Muted**: Subdued backgrounds (search bars, disabled states, inactive)
- **Muted foreground**: Placeholder text, hints, secondary text
- **Accent**: Highlight/emphasis color (can differ from primary, e.g. neon vs standard)
- **Destructive**: Error/danger/alert color
- **Border**: Default border color (often transparent white/black on dark/light)
- **Input**: Input field border or background
- **Ring**: Focus ring / glow color

### Typography
- Font family (ask if not already provided)
- Base font size and line-height
- Weight distribution: identify which weights are used (400, 500, 600, 700)
- Letter-spacing patterns
- Type scale: map sizes to heading levels (h1-h4, body, small, caption)

### Spacing
- Identify the base spacing unit (most frequent value)
- Note the spacing scale: common increments (4px, 8px, 12px, 16px, etc.)
- Common padding patterns (e.g. "8px 16px" for buttons)

### Border Radii
- Find the dominant radius by usage count
- Map to shadcn radius scale: `--radius` controls `sm = radius - 4px`, `md = radius - 2px`, `lg = radius`, `xl = radius + 4px`
- Pick `--radius` so the dominant site radius maps to the most-used shadcn class (usually md or lg)
- Note if the site uses pill shapes (9999px) for specific elements

### Gradients
- List key gradients with their CSS values
- Categorize: gold/premium, brand, overlay/fade, glow

### Shadows
- Elevation shadows (soft, medium, heavy)
- Glow effects (colored shadows, neon outlines)
- Inset shadows

### Borders
- Border color patterns (solid vs transparency-based)
- Border widths

## Step 3: Generate Tweakcn Theme

Output a complete CSS theme with `:root` (light) and `.dark` sections using **HSL format** (space-separated, no commas, e.g. `153 52% 44%`).

Required tokens to map:

```
--background, --foreground
--card, --card-foreground
--popover, --popover-foreground
--primary, --primary-foreground
--secondary, --secondary-foreground
--muted, --muted-foreground
--accent, --accent-foreground
--destructive, --destructive-foreground
--border, --input, --ring
--chart-1 through --chart-5
--radius
--sidebar, --sidebar-foreground
--sidebar-primary, --sidebar-primary-foreground
--sidebar-accent, --sidebar-accent-foreground
--sidebar-border, --sidebar-ring
```

Guidelines:
- Convert all rgb() values to HSL
- If the site is dark-mode dominant, still generate a light companion using the same hues at lighter values
- For chart colors, use 5 distinct vibrant colors from the site's palette
- Sidebar variants should be slightly darker (dark mode) or lighter (light mode) than main background

## Step 4: Provide Summary

After the theme CSS, include:

### Mapping Table
A table showing each token, the source element/color from the site, and the hex value.

### Extra Elements
Things tweakcn can't capture but define the site's visual identity:
- Font family + weights to import (with Google Fonts URL if applicable)
- Key gradients with full CSS values
- Glow/shadow effects for hover states
- Special radius patterns (e.g. pill buttons)
- Notable spacing or typography conventions
- Any distinctive visual patterns (gold borders, neon outlines, transparency layers)

## Conversion Reference

### RGB to HSL
To convert `rgb(r, g, b)` to HSL: normalize to 0-1, find min/max, compute hue from channel differences, saturation from lightness, output as `H S% L%`.

### Common Patterns
- `rgba(255, 255, 255, 0.1)` on dark bg → use a solid color that's ~10% lighter than background for borders
- `rgba(0, 0, 0, 0.1)` on light bg → use a solid color that's ~10% darker than background
- Neon/glow borders → map to `--ring` for focus states
- Gold gradients → note separately, suggest using for badges/premium indicators
