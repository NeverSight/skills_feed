---
name: pagespeed-insights
description: Audit web pages for performance optimization following PageSpeed Insights guidelines. Use when analyzing page performance, optimizing web applications, reviewing performance metrics, implementing Core Web Vitals improvements, or when the user mentions page speed, performance optimization, Lighthouse scores, or Core Web Vitals.
---

# PageSpeed Insights Auditor

## Overview

You are a **PageSpeed Insights Auditor** - an expert in web performance optimization who helps developers achieve excellent PageSpeed scores by identifying performance issues, avoiding bad practices, and implementing best practices based on Google's PageSpeed Insights guidelines.

**Core Principle**: Guide developers to achieve scores of 90+ (Good) in Performance, Accessibility, Best Practices, and SEO categories, while ensuring Core Web Vitals metrics meet the "Good" thresholds.

## Understanding PageSpeed Insights

PageSpeed Insights (PSI) analyzes page performance on mobile and desktop devices, providing both **lab data** (simulated) and **field data** (real user experiences). PSI reports on user experience metrics and provides diagnostic suggestions to improve page performance.

### Two Types of Data

1. **Lab Data**: Collected in a controlled environment using Lighthouse. Useful for debugging but may not capture real-world bottlenecks.
2. **Field Data**: Real user experience data from Chrome User Experience Report (CrUX). Useful for capturing actual user experiences but has a more limited set of metrics.

## Performance Score Thresholds

### Lab Scores (Lighthouse)

| Score Range | Rating            | Icon            |
| ----------- | ----------------- | --------------- |
| 90-100      | Good              | 🟢 Green circle |
| 50-89       | Needs Improvement | 🟡 Amber square |
| 0-49        | Poor              | 🔴 Red triangle |

**Target**: Always aim for scores of **90 or higher** in all categories.

### Core Web Vitals Thresholds

Core Web Vitals are the three most important metrics for web performance:

| Metric                              | Good         | Needs Improvement  | Poor      |
| ----------------------------------- | ------------ | ------------------ | --------- |
| **FCP** (First Contentful Paint)    | [0, 1800 ms] | [1800 ms, 3000 ms] | > 3000 ms |
| **LCP** (Largest Contentful Paint)  | [0, 2500 ms] | [2500 ms, 4000 ms] | > 4000 ms |
| **CLS** (Cumulative Layout Shift)   | [0, 0.1]     | [0.1, 0.25]        | > 0.25    |
| **INP** (Interaction to Next Paint) | [0, 200 ms]  | [200 ms, 500 ms]   | > 500 ms  |
| **TTFB** (Time to First Byte)       | [0, 800 ms]  | [800 ms, 1800 ms]  | > 1800 ms |

**Target**: Ensure the 75th percentile of all Core Web Vitals metrics are in the "Good" range.

## Key Performance Metrics

### Lab Metrics (Lighthouse)

1. **First Contentful Paint (FCP)**: Time until first content is rendered
2. **Largest Contentful Paint (LCP)**: Time until largest content element is rendered
3. **Speed Index**: How quickly content is visually displayed
4. **Cumulative Layout Shift (CLS)**: Visual stability measure
5. **Total Blocking Time (TBT)**: Sum of blocking time between FCP and TTI
6. **Time to Interactive (TTI)**: Time until page is fully interactive

### Field Metrics (CrUX)

- **FCP**: First Contentful Paint from real users
- **LCP**: Largest Contentful Paint from real users
- **CLS**: Cumulative Layout Shift from real users
- **INP**: Interaction to Next Paint (replaces FID)
- **TTFB**: Time to First Byte (experimental)

## Common Performance Issues & Solutions

### ❌ Bad Practice: Unoptimized Images

**Problem**: Large images without compression, modern formats, or proper sizing.

**Impact**: Poor LCP scores, slow page loads.

**✅ Solutions**:

- Use modern image formats (WebP, AVIF)
- Implement responsive images with `srcset`
- Compress images before uploading
- Set explicit width/height to prevent CLS
- Use lazy loading for below-the-fold images

```html
<!-- Bad -->
<img src="large-image.jpg" alt="Description" />

<!-- Good -->
<img
  src="image.webp"
  srcset="image-small.webp 400w, image-medium.webp 800w, image-large.webp 1200w"
  sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px"
  width="1200"
  height="800"
  alt="Description"
  loading="lazy"
/>
```

### ❌ Bad Practice: Render-Blocking Resources

**Problem**: CSS and JavaScript blocking initial render.

**Impact**: Poor FCP and LCP scores.

**✅ Solutions**:

- Defer non-critical CSS
- Inline critical CSS
- Use `async` or `defer` for JavaScript
- Remove unused CSS/JS
- Split code and lazy load routes

```html
<!-- Bad -->
<link rel="stylesheet" href="styles.css" />
<script src="app.js"></script>

<!-- Good -->
<link
  rel="stylesheet"
  href="styles.css"
  media="print"
  onload="this.media='all'"
/>
<link rel="preload" href="critical.css" as="style" />
<script src="app.js" defer></script>
```

### ❌ Bad Practice: Missing Resource Hints

**Problem**: Not preconnecting to important origins or prefetching critical resources.

**Impact**: Slow TTFB and LCP.

**✅ Solutions**:

- Use `rel="preconnect"` for third-party origins
- Use `rel="dns-prefetch"` for DNS resolution
- Use `rel="preload"` for critical resources
- Use `rel="prefetch"` for likely next-page resources

```html
<!-- Good -->
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="dns-prefetch" href="https://api.example.com" />
<link rel="preload" href="hero-image.webp" as="image" />
```

### ❌ Bad Practice: Layout Shift (CLS)

**Problem**: Content shifting during page load.

**Impact**: Poor CLS scores, bad user experience.

**✅ Solutions**:

- Set explicit dimensions for images and videos
- Reserve space for ads and embeds
- Avoid inserting content above existing content
- Use CSS aspect-ratio for responsive containers
- Prefer transform animations over layout-triggering properties

```css
/* Bad */
.image-container {
  width: 100%;
  /* height not set - causes CLS */
}

/* Good */
.image-container {
  width: 100%;
  aspect-ratio: 16 / 9;
  /* or */
  height: 0;
  padding-bottom: 56.25%; /* 16:9 ratio */
}
```

### ❌ Bad Practice: Large JavaScript Bundles

**Problem**: Loading unnecessary JavaScript code.

**Impact**: Poor TTI, high TBT.

**✅ Solutions**:

- Code splitting and lazy loading
- Remove unused code (tree shaking)
- Minimize and compress JavaScript
- Use dynamic imports for routes
- Avoid large third-party libraries when possible

```javascript
// Bad - loading everything upfront
import { heavyLibrary } from "./heavy-library";

// Good - lazy load when needed
const loadHeavyLibrary = () => import("./heavy-library");
```

### ❌ Bad Practice: Inefficient Font Loading

**Problem**: Fonts causing FOIT (Flash of Invisible Text) or FOUT (Flash of Unstyled Text).

**Impact**: Poor FCP, layout shifts.

**✅ Solutions**:

- Use `font-display: swap` or `optional`
- Preload critical fonts
- Subset fonts to include only needed characters
- Use system fonts when possible

```css
/* Good */
@font-face {
  font-family: "CustomFont";
  src: url("font.woff2") format("woff2");
  font-display: swap; /* or optional */
}
```

### ❌ Bad Practice: No Caching Strategy

**Problem**: Resources not cached, causing repeated downloads.

**Impact**: Slow repeat visits, poor performance.

**✅ Solutions**:

- Set appropriate Cache-Control headers
- Use service workers for offline caching
- Implement HTTP/2 server push for critical resources
- Use CDN for static assets

```
Cache-Control: public, max-age=31536000, immutable
```

### ❌ Bad Practice: Third-Party Scripts Blocking Render

**Problem**: Analytics, ads, or widgets blocking page load.

**Impact**: Poor TTI, high TBT.

**✅ Solutions**:

- Load third-party scripts asynchronously
- Defer non-critical third-party code
- Use `rel="noopener"` for external links
- Consider self-hosting analytics when possible

```html
<!-- Good -->
<script async src="https://www.google-analytics.com/analytics.js"></script>
```

## Accessibility Best Practices

### ❌ Bad Practice: Missing Alt Text

**Problem**: Images without descriptive alt attributes.

**Impact**: Poor accessibility score.

**✅ Solution**: Always provide meaningful alt text.

```html
<!-- Bad -->
<img src="chart.png" />

<!-- Good -->
<img src="chart.png" alt="Sales increased 25% from Q1 to Q2" />
```

### ❌ Bad Practice: Poor Color Contrast

**Problem**: Text not readable due to low contrast.

**Impact**: Poor accessibility score.

**✅ Solution**: Ensure contrast ratio of at least 4.5:1 for normal text, 3:1 for large text.

### ❌ Bad Practice: Missing ARIA Labels

**Problem**: Interactive elements without proper labels.

**Impact**: Poor accessibility score.

**✅ Solution**: Use ARIA labels for screen readers.

```html
<!-- Good -->
<button aria-label="Close dialog">×</button>
```

## SEO Best Practices

### ❌ Bad Practice: Missing Meta Tags

**Problem**: No title, description, or viewport meta tags.

**Impact**: Poor SEO score.

**✅ Solution**: Include essential meta tags.

```html
<!-- Good -->
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<meta name="description" content="Page description" />
<title>Page Title</title>
```

### ❌ Bad Practice: Non-Descriptive Links

**Problem**: Links with generic text like "click here".

**Impact**: Poor SEO score.

**✅ Solution**: Use descriptive link text.

```html
<!-- Bad -->
<a href="/about">Click here</a>

<!-- Good -->
<a href="/about">Learn more about our company</a>
```

## Best Practices Checklist

### Performance

- [ ] Images optimized (WebP/AVIF, compressed, responsive)
- [ ] Critical CSS inlined
- [ ] Non-critical CSS deferred
- [ ] JavaScript code-split and lazy-loaded
- [ ] Render-blocking resources minimized
- [ ] Resource hints implemented (preconnect, preload, dns-prefetch)
- [ ] Fonts optimized with font-display
- [ ] Caching strategy implemented
- [ ] Third-party scripts loaded asynchronously
- [ ] Layout shifts prevented (explicit dimensions, aspect-ratio)

### Core Web Vitals

- [ ] LCP < 2.5 seconds (75th percentile)
- [ ] FCP < 1.8 seconds (75th percentile)
- [ ] CLS < 0.1 (75th percentile)
- [ ] INP < 200ms (75th percentile)
- [ ] TTFB < 800ms (75th percentile)

### Accessibility

- [ ] All images have alt text
- [ ] Color contrast meets WCAG standards
- [ ] ARIA labels on interactive elements
- [ ] Semantic HTML used
- [ ] Keyboard navigation supported

### SEO

- [ ] Meta tags present (title, description, viewport)
- [ ] Descriptive link text
- [ ] Proper heading hierarchy (h1-h6)
- [ ] Structured data implemented
- [ ] Mobile-friendly design

## Audit Workflow

When auditing a page for PageSpeed optimization:

1. **Analyze Current State**

   - Check current PageSpeed scores
   - Identify Core Web Vitals metrics
   - Review lab and field data differences

2. **Identify Issues**

   - List all performance problems
   - Prioritize by impact (Core Web Vitals first)
   - Categorize by type (images, JS, CSS, etc.)

3. **Provide Solutions**

   - Suggest specific optimizations
   - Provide code examples
   - Explain expected improvements

4. **Verify Improvements**
   - Re-test after changes
   - Ensure scores reach 90+
   - Confirm Core Web Vitals are "Good"

## Common Mistakes to Avoid

### ❌ Focusing Only on Lab Data

**Problem**: Optimizing only for Lighthouse scores without considering real user data.

**✅ Solution**: Balance both lab and field data. Field data shows real-world performance.

### ❌ Over-Optimizing

**Problem**: Implementing too many optimizations at once, making debugging difficult.

**✅ Solution**: Make incremental changes and test after each optimization.

### ❌ Ignoring Mobile Performance

**Problem**: Optimizing only for desktop.

**✅ Solution**: Mobile-first approach. Most users are on mobile devices.

### ❌ Not Testing After Changes

**Problem**: Assuming optimizations worked without verification.

**✅ Solution**: Always re-run PageSpeed Insights after implementing changes.

## Performance Optimization Priority

1. **Critical Path**: Optimize resources needed for initial render
2. **Core Web Vitals**: Focus on LCP, CLS, and INP first
3. **Render-Blocking**: Eliminate blocking CSS and JS
4. **Images**: Optimize largest contentful paint element
5. **Third-Party**: Minimize impact of external scripts
6. **Caching**: Implement proper caching strategies

## Tools & Resources

- **PageSpeed Insights**: https://pagespeed.web.dev/
- **Lighthouse**: Built into Chrome DevTools
- **Chrome User Experience Report**: Real-world performance data
- **Web Vitals Extension**: Monitor Core Web Vitals in real-time

## Specification Reference

This skill is based on the official [PageSpeed Insights documentation](https://developers.google.com/speed/docs/insights/v5/about?hl=es-419) from Google Developers.

All thresholds, metrics, and best practices in this skill follow the official PageSpeed Insights guidelines and Core Web Vitals specifications. For complete documentation, refer to the [official PageSpeed Insights documentation](https://developers.google.com/speed/docs/insights/v5/about?hl=es-419).
