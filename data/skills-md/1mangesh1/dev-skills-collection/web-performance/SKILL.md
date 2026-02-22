---
name: web-performance
description: Web and frontend performance optimization. Use when user asks to "optimize performance", "improve loading time", "lazy loading", "code splitting", "bundle size", "Core Web Vitals", "image optimization", "CSS/JS minification", "caching strategies", "performance profiling", or mentions web performance and user experience metrics.
---

# Web Performance Optimization

Strategies and techniques for optimizing web application performance and user experience.

## Core Web Vitals

### Largest Contentful Paint (LCP)
- Time to largest content element visible
- Target: < 2.5 seconds
- Optimize: image size, server response, render-blocking resources

### First Input Delay (FID)
- Time for page to respond to user input
- Target: < 100 milliseconds
- Optimize: reduce JavaScript, break up tasks

### Cumulative Layout Shift (CLS)
- Visual stability of page
- Target: < 0.1
- Optimize: reserve space for images/ads, avoid layout disruptions

## Performance Metrics

| Metric | Target | Tool |
|--------|--------|------|
| First Contentful Paint (FCP) | < 1.8s | Chrome DevTools |
| Largest Contentful Paint (LCP) | < 2.5s | Lighthouse |
| Time to Interactive (TTI) | < 3.8s | WebPageTest |
| Total Blocking Time (TBT) | < 150ms | Lighthouse |

## Optimization Techniques

### Image Optimization
```html
<!-- Lazy loading -->
<img src="image.jpg" loading="lazy">

<!-- Responsive images -->
<picture>
  <source media="(max-width: 500px)" srcset="small.jpg">
  <img src="large.jpg" alt="Description">
</picture>

<!-- Modern formats -->
<picture>
  <source type="image/webp" srcset="image.webp">
  <img src="image.jpg" alt="Description">
</picture>
```

### Code Splitting
```javascript
// Dynamic import
const module = await import('./heavy-module');

// React lazy loading
const Component = React.lazy(() => import('./Component'));
```

### Caching Strategies
- Browser cache: Set Cache-Control headers
- Service workers: Offline support and cache control
- CDN: Distribute content geographically
- Redis: Server-side caching

### Minification & Compression
- Minify CSS, JavaScript, HTML
- Gzip compression
- Brotli for better compression
- Remove unused code (tree shaking)

## Performance Audit Checklist

- [ ] Optimize images (format, size, lazy load)
- [ ] Minify CSS, JS, HTML
- [ ] Enable gzip/brotli compression
- [ ] Implement code splitting
- [ ] Cache static assets
- [ ] Use CDN for assets
- [ ] Optimize critical rendering path
- [ ] Remove unused dependencies
- [ ] Lazy load non-critical routes
- [ ] Optimize fonts (subset, preload)
- [ ] Implement service workers
- [ ] Monitor Core Web Vitals

## Tools for Analysis

- **Chrome Lighthouse** - Audit performance
- **WebPageTest** - Detailed analysis
- **Speedcurve** - Continuous monitoring
- **Bundle Analyzer** - Webpack/Rollup bundle size
- **Sentry** - Error and performance monitoring

## Best Practices

1. **Measure First** - Establish baseline metrics
2. **Prioritize** - Fix biggest issues first
3. **Test Impact** - Verify improvements
4. **Monitor Continuously** - Track over time
5. **User-Centric** - Focus on real user metrics

## Example Performance Budget

```
JavaScript: < 200KB
CSS: < 50KB
Images: < 500KB total
Fonts: < 100KB
Total: < 850KB
```

## References

- Web Vitals by Google
- Chrome Developers Performance
- MDN Web Performance
- Lighthouse Documentation
- WebPageTest Blog
