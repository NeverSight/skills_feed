---
name: performance-audit
description: Web performance testing via Playwright MCP - Core Web Vitals, Lighthouse
requires_mcp: playwright
integrates_with:
  - playwright-automation
  - react-best-practices
---

# Performance Audit

Measure and optimize web performance using Playwright MCP.

## Core Web Vitals

| Metric | Good | Needs Work | Poor |
|--------|------|------------|------|
| **LCP** (Largest Contentful Paint) | ≤2.5s | ≤4.0s | >4.0s |
| **INP** (Interaction to Next Paint) | ≤200ms | ≤500ms | >500ms |
| **CLS** (Cumulative Layout Shift) | ≤0.1 | ≤0.25 | >0.25 |

## Quick Audit via Playwright

```javascript
// Run via playwright_evaluate
const performance = window.performance;
const timing = performance.timing;
const paintEntries = performance.getEntriesByType('paint');
const lcpEntries = performance.getEntriesByType('largest-contentful-paint');

return {
  ttfb: timing.responseStart - timing.requestStart,
  fcp: paintEntries.find(e => e.name === 'first-contentful-paint')?.startTime,
  lcp: lcpEntries[lcpEntries.length - 1]?.startTime,
  domContentLoaded: timing.domContentLoadedEventEnd - timing.navigationStart,
  windowLoad: timing.loadEventEnd - timing.navigationStart
};
```

## Common Issues & Fixes

### 1. Large Images
```html
<!-- Bad -->
<img src="hero-4000x3000.jpg">

<!-- Good -->
<img src="hero.webp"
     srcset="hero-400.webp 400w, hero-800.webp 800w"
     sizes="(max-width: 600px) 400px, 800px"
     loading="lazy">
```

### 2. Render-Blocking Resources
```html
<!-- Bad -->
<link rel="stylesheet" href="styles.css">

<!-- Good: Critical CSS inline -->
<style>/* critical styles */</style>
<link rel="stylesheet" href="styles.css" media="print" onload="this.media='all'">
```

### 3. Unoptimized JavaScript
```html
<!-- Bad -->
<script src="bundle.js"></script>

<!-- Good -->
<script src="bundle.js" defer></script>
```

### 4. Layout Shifts
```css
/* Bad: No dimensions */
img { }

/* Good: Reserve space */
img { aspect-ratio: 16/9; width: 100%; }
```

### 5. Too Many Requests
- Bundle CSS/JS files
- Use HTTP/2
- Implement caching headers

## Audit Workflow

1. **Navigate**: `playwright_navigate` to URL
2. **Measure**: `playwright_evaluate` performance API
3. **Screenshot**: Capture above-fold content
4. **Analyze**: Check resource loading
5. **Report**: Metrics + recommendations

## Playwright MCP Commands

```
Navigate to [URL] and measure page load performance

Get all network requests and their sizes

Find render-blocking resources

Measure time to first contentful paint

Check for layout shift issues
```

## Performance Budget

| Resource | Budget |
|----------|--------|
| Total page size | <1.5MB |
| JavaScript | <300KB |
| CSS | <100KB |
| Images | <500KB |
| Fonts | <100KB |
| Time to Interactive | <3.5s |

## Optimization Checklist

- [ ] Images optimized (WebP, proper sizing)
- [ ] JavaScript deferred/async
- [ ] CSS critical path inlined
- [ ] Fonts preloaded
- [ ] Caching headers set
- [ ] Gzip/Brotli compression
- [ ] CDN for static assets
- [ ] No layout shifts
- [ ] Lazy loading for below-fold
- [ ] Resource hints (preconnect, prefetch)

## React/Next.js Specific

- Use `next/image` for automatic optimization
- Implement `next/dynamic` for code splitting
- Enable ISR for static pages
- Use React.lazy for component splitting
- Memoize expensive calculations
