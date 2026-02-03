---
name: use-tailwind-v4
description: "Tailwind CSS v4 reference and migration guide. Use for v4 projects, syntax changes, upgrading from v3, and troubleshooting v4-specific utility patterns or configuration differences."
---

# Tailwind CSS v4

## v4 Syntax At a Glance

### Imports and Setup

```css
/* v4 import (replaces @tailwind directives) */
@import "tailwindcss";

/* Custom utilities (replaces @layer utilities) */
@utility tab-4 {
  tab-size: 4;
}

/* Loading JS config (if still needed) */
@config "../../tailwind.config.js";
```

### CSS Variables for Theme

v4 exposes all theme values as CSS variables. Prefer these over `theme()`:

```css
background-color: var(--color-red-500);
font-family: var(--font-sans);
```

## Quick Reference: v3 → v4 Changes

### Renamed Utilities

| v3 | v4 | Notes |
|----|-----|-------|
| `shadow-sm` | `shadow-xs` | Scale shifted |
| `shadow` | `shadow-sm` | Scale shifted |
| `drop-shadow-sm` | `drop-shadow-xs` | Scale shifted |
| `drop-shadow` | `drop-shadow-sm` | Scale shifted |
| `blur-sm` | `blur-xs` | Scale shifted |
| `blur` | `blur-sm` | Scale shifted |
| `backdrop-blur-sm` | `backdrop-blur-xs` | Scale shifted |
| `backdrop-blur` | `backdrop-blur-sm` | Scale shifted |
| `rounded-sm` | `rounded-xs` | Scale shifted |
| `rounded` | `rounded-sm` | Scale shifted |
| `outline-none` | `outline-hidden` | `outline-none` now sets `outline-style: none` |
| `ring` | `ring-3` | Default changed from 3px to 1px |

### Deprecated Utilities (Use Opacity Modifiers)

```html
<!-- v3: opacity utilities -->
<div class="bg-black bg-opacity-50">

<!-- v4: opacity modifiers -->
<div class="bg-black/50">
```

Also: `flex-shrink-*` → `shrink-*`, `flex-grow-*` → `grow-*`, `overflow-ellipsis` → `text-ellipsis`

### Default Changes

| What | v3 Default | v4 Default |
|------|------------|------------|
| Border color | `gray-200` | `currentColor` |
| Ring width | `3px` | `1px` |
| Ring color | `blue-500` | `currentColor` |
| Button cursor | `pointer` | `default` |

### Variant Stacking Order

Changed from right-to-left to left-to-right:

```html
<!-- v3 -->
<ul class="first:*:pt-0">

<!-- v4 -->
<ul class="*:first:pt-0">
```

### Variable Syntax in Arbitrary Values

```html
<!-- v3: square brackets -->
<div class="bg-[--brand-color]">

<!-- v4: parentheses -->
<div class="bg-(--brand-color)">
```

### Prefix Syntax

```html
<!-- v4 prefixes are at the start, like variants -->
<div class="tw:flex tw:bg-red-500 tw:hover:bg-red-600">
```

## Upgrading Projects

For project migrations, run the automated upgrade tool:

```bash
npx @tailwindcss/upgrade
```

Requires Node.js 20+. Run in a new branch and review changes.

For complete migration details (PostCSS/Vite/CLI config, custom utilities, framework-specific issues), see [references/upgrade-guide.md](references/upgrade-guide.md).
