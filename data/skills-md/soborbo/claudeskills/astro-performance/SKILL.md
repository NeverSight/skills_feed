---
name: astro-performance
description: Core Web Vitals and performance optimization for Astro sites. LCP, CLS, INP optimization, bundle size, fonts, third-party scripts. Use for performance tuning.
---

# Astro Performance Skill

## Purpose

Achieve 90+ Lighthouse scores and pass Core Web Vitals. Direct impact on SEO rankings and conversion rates.

## Core Rules

- Preload LCP elements (hero images/text) with fetchpriority="high"
- Set explicit dimensions on all images and iframes to prevent CLS
- Use font-display: swap for all web fonts
- Self-host fonts and subset to reduce file size
- Defer third-party scripts until after load or user interaction
- Break up long tasks to keep INP under 200ms
- Use AVIF/WebP formats with responsive images
- Keep JS bundle under 100KB gzipped
- Implement edge caching with long cache headers for assets
- Monitor real user metrics with web-vitals library

## Core Web Vitals Targets

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| **LCP** (Largest Contentful Paint) | ≤2.5s | 2.5-4s | >4s |
| **INP** (Interaction to Next Paint) | ≤200ms | 200-500ms | >500ms |
| **CLS** (Cumulative Layout Shift) | ≤0.1 | 0.1-0.25 | >0.25 |

## Bundle Size Budgets

| Asset Type | Budget |
|------------|--------|
| Total JS | <100KB (gzipped) |
| Total CSS | <50KB (gzipped) |
| Hero image | <200KB |
| Any single image | <100KB |

## References

### Core Web Vitals
- [LCP Optimization](references/lcp-optimization.md) - Hero images, preloading, server response
- [CLS Prevention](references/cls-prevention.md) - Dimensions, skeletons, font display
- [INP Optimization](references/inp-optimization.md) - Task chunking, debouncing, content-visibility

### Assets & Resources
- [Bundle Size](references/bundle-size.md) - Analysis, tree shaking, dynamic imports
- [Fonts](references/fonts.md) - Self-hosting, subsetting, variable fonts
- [Images](references/images.md) - Format priority, responsive images

### Infrastructure
- [Third-Party Scripts](references/third-party-scripts.md) - GTM, facades, loading attributes
- [Caching](references/caching.md) - Cloudflare headers, cache control
- [Testing](references/testing.md) - Lighthouse, WebPageTest, real user monitoring

## Forbidden

- Render-blocking CSS in body
- Synchronous third-party scripts in head
- Unoptimized images
- Web fonts without `font-display: swap`
- Layout shifts from dynamic content
- Main thread blocking >50ms

## Definition of Done

- [ ] Lighthouse Performance ≥90
- [ ] LCP ≤2.5s
- [ ] CLS ≤0.1
- [ ] INP ≤200ms
- [ ] Total JS <100KB gzipped
- [ ] Hero image preloaded
- [ ] Fonts self-hosted with swap
- [ ] Third-party scripts deferred
