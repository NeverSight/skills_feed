---
name: tailwind-ssr
description: TailwindCSS v4 and SSR expert. Use when configuring TailwindCSS, implementing SSR strategies, optimizing critical CSS, or solving styling performance issues.
---

# TailwindCSS v4 & SSR Expert

Expert assistant for TailwindCSS v4 configuration, SSR/SSG styling strategies, critical CSS optimization, and frontend performance.

## How It Works

1. Identifies TailwindCSS version and framework context
2. Queries Context7 documentation (`/websites/tailwindcss`)
3. Provides configuration and optimization solutions
4. Addresses SSR-specific styling challenges

## Documentation Resources

**Context7 Library IDs:**
- TailwindCSS v4: `/websites/tailwindcss` (2333 snippets)
- TailwindCSS v3: `/websites/v3_tailwindcss` (2691 snippets, Score: 85.9)

**Official Documentation:**
- Docs: `https://tailwindcss.com/docs`
- Upgrade Guide: `https://tailwindcss.com/docs/upgrade-guide`

## TailwindCSS v4 Key Changes

### CSS-First Configuration

```css
/* v4 uses CSS @import instead of @tailwind directives */
@import "tailwindcss";

/* Design tokens as CSS variables */
@theme {
  --color-primary: oklch(0.7 0.15 200);
  --font-display: "Inter", sans-serif;
  --breakpoint-3xl: 1920px;
}
```

### Automatic Content Detection

```css
/* v4 auto-detects content, no config needed */
/* Manual override if needed: */
@source "../components/**/*.tsx";
```

### New Features

```css
/* Container queries */
@container (min-width: 400px) {
  .card { /* styles */ }
}

/* 3D transforms */
.element {
  @apply rotate-x-45 perspective-500;
}

/* Modern color functions */
.button {
  background: oklch(0.7 0.15 200);
}
```

## SSR Performance Checklist

### Critical CSS
- [ ] Inline above-the-fold CSS
- [ ] Defer non-critical stylesheets
- [ ] Use `<link rel="preload">` for fonts

### Hydration
- [ ] Avoid layout shifts during hydration
- [ ] Match server and client class generation
- [ ] Test with JavaScript disabled

### FOUC Prevention
```html
<!-- Add loading state -->
<html class="no-js">
<head>
  <script>document.documentElement.classList.remove('no-js')</script>
  <style>.no-js .lazy-load { visibility: hidden; }</style>
</head>
```

## Framework Integration

### SvelteKit

```svelte
<!-- +layout.svelte -->
<script>
  import '../app.css';
</script>
```

```css
/* app.css */
@import "tailwindcss";
```

### Next.js

```tsx
// app/layout.tsx
import './globals.css';
```

```css
/* globals.css */
@import "tailwindcss";
```

## Performance Optimization

### PurgeCSS (Production)
```css
/* v4 handles this automatically */
/* Ensure all dynamic classes are detectable */
```

### Custom Variants
```css
@variant hocus (&:hover, &:focus);
@variant group-hocus (:merge(.group):hover &, :merge(.group):focus &);
```

### Reduce Bundle Size
```css
/* Disable unused core plugins */
@import "tailwindcss" layer(utilities);
@import "tailwindcss/preflight" layer(base);
```

## Browser Compatibility

**TailwindCSS v4 requires:**
- Safari 16.4+
- Chrome 111+
- Firefox 128+
- Edge 111+

## Present Results to User

When providing TailwindCSS solutions:
- Specify v3 vs v4 syntax differences
- Provide copy-paste ready configuration
- Consider SSR framework-specific integration
- Note browser compatibility requirements
- Include performance implications

## Troubleshooting

**"Styles not applying"**
- Check content detection paths
- Verify CSS import is correct
- Clear build cache

**"FOUC (Flash of Unstyled Content)"**
- Inline critical CSS
- Add proper preload hints
- Check hydration timing

**"Build too slow"**
- Reduce content glob patterns
- Use specific file extensions
- Enable caching in build tool
