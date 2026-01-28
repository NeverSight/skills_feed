---
name: tailwindcss
description: This skill should be used when the user asks to "style with Tailwind", "add CSS", "configure theme", "use @theme", "add custom colors", "implement dark mode", "use container queries", "add responsive design", "use OKLCH colors", or discusses styling, theming, or visual design. Always use the latest Tailwind CSS version and modern patterns.
version: 1.0.0
---

# Tailwind CSS Development

This skill provides guidance for styling applications with Tailwind CSS, focusing on **always using the latest version** and modern patterns.

> **Philosophy:** Use CSS-first configuration with `@theme`. Use OKLCH colors for perceptual uniformity. Prefer `@container` queries over media queries when appropriate.

## Quick Reference

| Feature | Modern Approach | Legacy (Avoid) |
|---------|----------------|----------------|
| Configuration | CSS `@theme` directive | `tailwind.config.js` |
| Colors | OKLCH color space | RGB/HSL colors |
| Container queries | `@container` | Media queries only |
| Content detection | Automatic | Manual `content: []` config |
| PostCSS plugin | `@tailwindcss/postcss` | `tailwindcss` package |

## Installation (Next.js)

```bash
npm install tailwindcss @tailwindcss/postcss postcss
```

```js
// postcss.config.mjs
export default {
  plugins: {
    '@tailwindcss/postcss': {}
  }
}
```

```css
/* app/globals.css */
@import "tailwindcss";
```

## CSS-First Configuration

### The @theme Directive

Define your design system directly in CSS:

```css
@import "tailwindcss";

@theme {
  /* Colors */
  --color-brand: oklch(0.6 0.15 250);
  --color-brand-light: oklch(0.8 0.1 250);
  --color-brand-dark: oklch(0.4 0.15 250);

  /* Fonts */
  --font-display: "Cal Sans", sans-serif;
  --font-body: "Inter", system-ui, sans-serif;

  /* Spacing */
  --spacing-18: 4.5rem;
  --spacing-128: 32rem;

  /* Border radius */
  --radius-xl: 1rem;
  --radius-2xl: 1.5rem;

  /* Shadows */
  --shadow-soft: 0 4px 12px oklch(0 0 0 / 0.08);

  /* Animations */
  --animate-fade-in: fade-in 0.3s ease-out;
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(-4px); }
  to { opacity: 1; transform: translateY(0); }
}
```

Use in HTML:

```html
<div class="bg-brand text-white font-display p-18 rounded-xl shadow-soft animate-fade-in">
  Styled with custom theme
</div>
```

## OKLCH Color System

OKLCH provides perceptually uniform colors:

```css
@theme {
  /* Primary palette */
  --color-primary-50: oklch(0.98 0.01 250);
  --color-primary-100: oklch(0.95 0.03 250);
  --color-primary-200: oklch(0.90 0.06 250);
  --color-primary-300: oklch(0.82 0.10 250);
  --color-primary-400: oklch(0.70 0.14 250);
  --color-primary-500: oklch(0.60 0.16 250);
  --color-primary-600: oklch(0.50 0.14 250);
  --color-primary-700: oklch(0.40 0.12 250);
  --color-primary-800: oklch(0.30 0.08 250);
  --color-primary-900: oklch(0.20 0.05 250);
  --color-primary-950: oklch(0.12 0.03 250);

  /* Semantic colors */
  --color-success: oklch(0.65 0.15 145);
  --color-warning: oklch(0.75 0.15 85);
  --color-error: oklch(0.55 0.2 25);
}
```

OKLCH format: `oklch(lightness chroma hue)`
- **Lightness**: 0 (black) to 1 (white)
- **Chroma**: 0 (gray) to ~0.4 (vivid)
- **Hue**: 0-360 degrees (red=25, yellow=85, green=145, blue=250)

## Container Queries

Style based on container size, not viewport:

```html
<!-- Define container -->
<div class="@container">
  <!-- Respond to container width -->
  <div class="flex flex-col @md:flex-row @lg:grid @lg:grid-cols-3 gap-4">
    <div class="p-4 @sm:p-6 @md:p-8">
      Content adapts to container
    </div>
  </div>
</div>
```

### Named Containers

```html
<div class="@container/sidebar">
  <nav class="block @md/sidebar:flex">
    Navigation
  </nav>
</div>

<div class="@container/main">
  <article class="@lg/main:grid @lg/main:grid-cols-2">
    Main content
  </article>
</div>
```

### Container Breakpoints

| Modifier | Min Width |
|----------|-----------|
| `@xs` | 20rem (320px) |
| `@sm` | 24rem (384px) |
| `@md` | 28rem (448px) |
| `@lg` | 32rem (512px) |
| `@xl` | 36rem (576px) |
| `@2xl` | 42rem (672px) |

## Dark Mode

### Using CSS Variables

```css
@theme {
  /* Light mode (default) */
  --color-surface: oklch(0.99 0 0);
  --color-surface-elevated: oklch(1 0 0);
  --color-text: oklch(0.15 0 0);
  --color-text-muted: oklch(0.4 0 0);

  /* Dark mode overrides */
  @variant dark {
    --color-surface: oklch(0.15 0 0);
    --color-surface-elevated: oklch(0.2 0 0);
    --color-text: oklch(0.95 0 0);
    --color-text-muted: oklch(0.7 0 0);
  }
}
```

```html
<div class="bg-surface text-text">
  Automatically adapts to dark mode
</div>
```

### Class-Based Dark Mode

```html
<html class="dark">
  <body class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
    <button class="bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700">
      Button
    </button>
  </body>
</html>
```

## Responsive Design

### Mobile-First Breakpoints

```html
<div class="
  w-full          /* mobile: full width */
  sm:w-1/2        /* ≥640px: half width */
  md:w-1/3        /* ≥768px: third width */
  lg:w-1/4        /* ≥1024px: quarter width */
  xl:w-1/5        /* ≥1280px: fifth width */
">
  Responsive element
</div>
```

### Breakpoint Reference

| Prefix | Min Width | CSS |
|--------|-----------|-----|
| `sm` | 640px | `@media (min-width: 640px)` |
| `md` | 768px | `@media (min-width: 768px)` |
| `lg` | 1024px | `@media (min-width: 1024px)` |
| `xl` | 1280px | `@media (min-width: 1280px)` |
| `2xl` | 1536px | `@media (min-width: 1536px)` |

## Typography

```html
<!-- Headings -->
<h1 class="text-4xl font-bold tracking-tight">Heading 1</h1>
<h2 class="text-3xl font-semibold">Heading 2</h2>
<h3 class="text-2xl font-medium">Heading 3</h3>

<!-- Body text -->
<p class="text-base leading-relaxed">Regular paragraph</p>
<p class="text-sm text-gray-600">Small muted text</p>

<!-- Text styles -->
<span class="font-bold">Bold</span>
<span class="italic">Italic</span>
<span class="underline">Underlined</span>
<span class="line-through">Strikethrough</span>
```

## Flexbox & Grid

### Flexbox

```html
<!-- Horizontal layout -->
<div class="flex items-center justify-between gap-4">
  <div>Left</div>
  <div>Right</div>
</div>

<!-- Centered content -->
<div class="flex items-center justify-center min-h-screen">
  <div>Centered</div>
</div>

<!-- Wrap items -->
<div class="flex flex-wrap gap-4">
  <div class="flex-1 min-w-[200px]">Item</div>
</div>
```

### Grid

```html
<!-- Basic grid -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>

<!-- Complex layout -->
<div class="grid grid-cols-12 gap-4">
  <aside class="col-span-12 md:col-span-3">Sidebar</aside>
  <main class="col-span-12 md:col-span-9">Main</main>
</div>

<!-- Auto-fill -->
<div class="grid grid-cols-[repeat(auto-fill,minmax(250px,1fr))] gap-4">
  <!-- Items auto-fill available space -->
</div>
```

## States and Variants

```html
<!-- Hover, focus, active -->
<button class="
  bg-blue-500
  hover:bg-blue-600
  focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
  active:bg-blue-700
">
  Button
</button>

<!-- Group hover -->
<div class="group">
  <h3 class="group-hover:text-blue-500">Title</h3>
  <p class="group-hover:text-gray-700">Description</p>
</div>

<!-- Peer states -->
<input class="peer" type="checkbox" />
<label class="peer-checked:text-blue-500">Label</label>

<!-- First, last, odd, even -->
<ul>
  <li class="first:pt-0 last:pb-0 odd:bg-gray-50">Item</li>
</ul>
```

## Animations

```html
<!-- Built-in animations -->
<div class="animate-pulse">Loading skeleton</div>
<div class="animate-spin">Spinner</div>
<div class="animate-bounce">Bounce</div>
<div class="animate-ping">Ping effect</div>

<!-- Transitions -->
<button class="transition-colors duration-200 ease-in-out hover:bg-blue-600">
  Smooth color change
</button>

<div class="transition-all duration-300 hover:scale-105 hover:shadow-lg">
  Transform on hover
</div>

<!-- Motion preferences -->
<div class="motion-safe:animate-bounce motion-reduce:animate-none">
  Respects user preferences
</div>
```

## Common Patterns

### Card

```html
<div class="rounded-lg border bg-white p-6 shadow-sm">
  <h3 class="text-lg font-semibold">Card Title</h3>
  <p class="mt-2 text-gray-600">Card description</p>
</div>
```

### Button

```html
<button class="
  inline-flex items-center justify-center
  rounded-md bg-blue-500 px-4 py-2
  text-sm font-medium text-white
  hover:bg-blue-600
  focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
  disabled:opacity-50 disabled:pointer-events-none
">
  Button
</button>
```

### Input

```html
<input class="
  w-full rounded-md border border-gray-300 px-3 py-2
  text-sm placeholder:text-gray-400
  focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500
  disabled:bg-gray-100 disabled:cursor-not-allowed
" />
```

## Additional Resources

For detailed patterns, see reference files:
- **`references/theme-directive.md`** - Complete @theme configuration
- **`references/colors.md`** - OKLCH color system deep dive
