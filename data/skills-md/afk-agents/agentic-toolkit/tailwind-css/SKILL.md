---
name: tailwind-css
description: Tailwind CSS v4 styling with utility-first classes, theme configuration, and modern CSS patterns. Use when writing or modifying CSS classes, configuring themes, implementing responsive designs, or migrating from v3. Triggers on Tailwind, utility classes, responsive breakpoints, dark mode styling.
---

# Tailwind CSS v4

Write modern, maintainable styles using Tailwind CSS v4's utility-first approach.

## Quick Reference

**Responsive**: `sm:`, `md:`, `lg:`, `xl:`, `2xl:` (mobile-first)
**States**: `hover:`, `focus:`, `active:`, `disabled:`, `group-hover:`, `peer-checked:`
**Dark mode**: `dark:`
**Arbitrary values**: `top-[117px]`, `bg-[#bada55]`
**CSS variables**: `bg-(--my-color)` (v4 syntax)

## Core Concepts

- **Utility-First**: Compose styles from single-purpose classes directly in HTML
- **Mobile-First**: Breakpoint prefixes apply at that width and above
- **State Variants**: Prefix utilities to apply conditionally
- **Theme Variables**: Define in `@theme { }` as CSS custom properties

## v4 Architecture

### CSS-First Configuration

Configuration moved from JS to CSS via `@theme`:

```css
/* app.css */
@import "tailwindcss";

@theme {
  --font-sans: "Inter", system-ui, sans-serif;
  --color-brand-500: oklch(0.637 0.237 25.331);
  --breakpoint-lg: 64rem;
  --spacing: 0.25rem;
}
```

Theme values generate both utility classes (`bg-brand-500`) and CSS variables (`var(--color-brand-500)`).

### Simplified Imports

Replace v3 directives with single import:
```css
/* v3 (deprecated) */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* v4 */
@import "tailwindcss";
```

### Browser Requirements

Requires: Safari 16.4+, Chrome 111+, Firefox 128+

Uses native CSS features: `@property`, `color-mix()`, cascade layers. Use v3.4 for older browsers.

### Build Tool Packages

- **CLI**: `@tailwindcss/cli`
- **PostCSS**: `@tailwindcss/postcss`
- **Vite** (recommended): `@tailwindcss/vite`

No longer need `postcss-import` or `autoprefixer` as separate dependencies.

## v3 to v4 Migration

Run `npx @tailwindcss/upgrade` for automated migration.

### Renamed Utilities

| v3 | v4 |
|----|----|
| `shadow-sm` | `shadow-xs` |
| `shadow` | `shadow-sm` |
| `blur-sm` | `blur-xs` |
| `blur` | `blur-sm` |
| `rounded-sm` | `rounded-xs` |
| `rounded` | `rounded-sm` |
| `drop-shadow-sm` | `drop-shadow-xs` |
| `drop-shadow` | `drop-shadow-sm` |
| `outline-none` | `outline-hidden` |
| `ring` | `ring-3` |

### Removed Utilities

- Opacity utilities (`bg-opacity-50`) → slash syntax (`bg-black/50`)
- `flex-shrink-*` → `shrink-*`
- `flex-grow-*` → `grow-*`
- `overflow-ellipsis` → `text-ellipsis`

### Default Value Changes

- **Border color**: `currentColor` (was `gray-200`)
- **Ring color**: `currentColor` (was `blue-500`)
- **Ring width**: `1px` (was `3px`, use `ring-3` for old default)
- **Placeholder**: 50% opacity text color (was `gray-400`)
- **Button cursor**: `default` (was `pointer`)

### Syntax Changes

- **CSS variable shorthand**: `bg-(--my-color)` instead of `bg-[--my-color]`
- **Prefix syntax**: `tw:bg-red-500` (variant-like)
- **Variant stacking**: Left-to-right order (was right-to-left)
- **Hover on mobile**: Only applies when device supports hover (`@media (hover: hover)`)

### Custom Utilities

Use `@utility` instead of `@layer utilities`:

```css
@utility btn-primary {
  background-color: var(--color-brand-500);
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
}
```

### Scoped Styles (Vue/Svelte/CSS Modules)

Use `@reference` to access theme in isolated style blocks:

```vue
<style scoped>
@reference "../app.css";

.custom { @apply bg-brand-500; }
</style>
```

Or use CSS variables directly: `var(--color-brand-500)`

## Functions & Directives

| Directive | Purpose |
|-----------|---------|
| `@import "tailwindcss"` | Import Tailwind |
| `@theme { }` | Define design tokens |
| `@source "../path"` | Include source paths for class detection |
| `@source not "../path"` | Exclude paths |
| `@utility name { }` | Custom utility classes |
| `@variant name { }` | Apply variants in CSS |
| `@custom-variant` | Define new variants |
| `@apply` | Inline utilities (needs `@reference` in modules) |
| `@reference "path"` | Import for context without output |

Functions:
- `--alpha(color / opacity)` - adjust color opacity
- `--spacing(value)` - generate spacing values
- `var(--theme-variable)` - reference theme variables

## Advanced Variants

**ARIA**: `aria-checked:`, `aria-disabled:`
**Data attributes**: `data-[size=large]:`, `data-active:`
**Has selector**: `has-[:focus]:`
**Child/descendant**: `*:p-2`, `**:rounded-full`
**Named groups**: `group/item`, `peer-checked/opt1:`

## Container Queries

```html
<div class="@container">
  <div class="@sm:grid-cols-2 @lg:grid-cols-4">
    <!-- Styles based on container width -->
  </div>
</div>
```

Named containers: `@container/sidebar`, `@lg/sidebar:`

## Reference Documentation

Read these files only when you need detailed utility reference:

- [Layout](reference/layout.md) - display, position, visibility, columns, overflow
- [Flexbox & Grid](reference/flexbox-grid.md) - flex, grid, alignment, gap
- [Spacing & Sizing](reference/spacing-sizing.md) - padding, margin, width, height
- [Typography](reference/typography.md) - fonts, text styling, lists
- [Backgrounds & Borders](reference/backgrounds-borders.md) - bg, border, radius, ring
- [Effects](reference/effects.md) - shadows, opacity, filters, blend modes
- [Transforms & Transitions](reference/transforms-transitions.md) - scale, rotate, animate
- [Interactivity](reference/interactivity.md) - cursor, scroll, form controls
- [SVG & Masks](reference/svg-masks.md) - fill, stroke, mask utilities
- [Tables](reference/tables.md) - table layout and borders
- [Colors](reference/colors.md) - palette, opacity, customization

## Common Patterns

### Centering
```html
<!-- Flex -->
<div class="flex items-center justify-center">

<!-- Grid -->
<div class="grid place-items-center">

<!-- Absolute positioning -->
<div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">
```

### Responsive Grid
```html
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
```

### Card with Shadow
```html
<div class="rounded-lg bg-white p-6 shadow-md dark:bg-gray-800">
```

### Button
```html
<button class="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
```

### Form Input
```html
<input class="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500">
```

### Truncate Text
```html
<p class="truncate">Very long text...</p>
<!-- or multi-line -->
<p class="line-clamp-3">...</p>
```
