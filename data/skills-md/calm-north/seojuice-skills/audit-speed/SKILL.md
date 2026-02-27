---
name: audit-speed
description: >
  Deep Core Web Vitals and page speed audit. Use when the user asks about page
  speed, Core Web Vitals, LCP, CLS, INP, FCP, TTFB, Lighthouse scores, why a
  page is slow, performance optimization, or resource size analysis. For broader
  technical SEO issues, see diagnose-seo.
metadata:
  version: 1.0.0
---

# Audit Speed

Deep Core Web Vitals audit with root-cause analysis trees and resource
optimization recommendations.

## Core Web Vitals Thresholds

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP (Largest Contentful Paint) | < 2.5s | 2.5s - 4.0s | > 4.0s |
| CLS (Cumulative Layout Shift) | < 0.1 | 0.1 - 0.25 | > 0.25 |
| INP (Interaction to Next Paint) | < 200ms | 200ms - 500ms | > 500ms |
| FCP (First Contentful Paint) | < 1.8s | 1.8s - 3.0s | > 3.0s |
| TTFB (Time to First Byte) | < 800ms | 800ms - 1800ms | > 1800ms |

## Before You Start

Gather this context:

1. **Which pages?** Homepage, key landing pages, or specific slow pages.
2. **Current scores.** If the user has Lighthouse or PageSpeed Insights data, start there.
3. **Tech stack.** CMS, framework, hosting — this determines which optimizations are available.
4. **Known constraints.** Third-party scripts they can't remove, design requirements that limit optimization.

If no data is available, suggest running Google PageSpeed Insights on the key URLs.

## LCP Root-Cause Tree

LCP measures when the largest visible element finishes rendering. Diagnose:

**Is TTFB slow (> 800ms)?**
- → Server response time issue
- Check: hosting quality, CDN configuration, database queries, server-side rendering time
- Fix: upgrade hosting, add CDN, optimize server-side code, enable caching

**Is the LCP element an image?**
- → Image optimization issue
- Check: image format (use WebP/AVIF), image size (serve responsive sizes), lazy loading on LCP image (should NOT be lazy loaded)
- Fix: convert to modern formats, add `width`/`height` attributes, use `fetchpriority="high"` on LCP image, preload the LCP image

**Is the LCP element text?**
- → Font loading issue
- Check: custom fonts blocking render, font file size, font-display strategy
- Fix: use `font-display: swap` or `optional`, preload critical fonts, subset fonts to used characters

**Is render-blocking CSS/JS delaying the LCP?**
- Check: large CSS files in `<head>`, synchronous JS before content
- Fix: inline critical CSS, defer non-critical CSS, async/defer JS

## CLS Root-Cause Tree

CLS measures unexpected layout shifts. Diagnose:

**Do images/videos lack dimensions?**
- → Browser can't reserve space before loading
- Fix: add `width` and `height` attributes to all `<img>` and `<video>` elements, use CSS `aspect-ratio`

**Do ads or embeds inject content?**
- → Dynamic content pushing existing content down
- Fix: reserve space for ad slots with min-height, use `contain-intrinsic-size` for lazy content

**Do fonts cause text reflow?**
- → FOUT (Flash of Unstyled Text) causes layout shift when custom font loads
- Fix: use `font-display: optional` (no swap = no shift), or match fallback font metrics

**Does dynamic content insert above the fold?**
- → Banners, cookie notices, notifications pushing content
- Fix: use overlays instead of inline insertions, or reserve space with fixed-height containers

## INP Root-Cause Tree

INP measures responsiveness to user interactions. Diagnose:

**Is the main thread blocked by long tasks?**
- Check: JavaScript execution time, third-party scripts, large DOM
- Fix: break long tasks with `requestIdleCallback` or `setTimeout`, code-split heavy modules

**Do event handlers do heavy synchronous work?**
- Check: click handlers that trigger large DOM updates, form validation on every keystroke
- Fix: debounce inputs, use requestAnimationFrame for visual updates, offload work to web workers

**Are third-party scripts competing for the main thread?**
- Check: analytics, chat widgets, A/B testing tools, social embeds
- Fix: defer loading until after interaction, use `loading="lazy"` for embeds, consider removing low-value scripts

## Resource Analysis

Break down the total page weight:

| Resource Type | Size | Assessment | Action |
|---|---|---|---|
| HTML | [x] KB | [ok/large] | Compress, reduce inline styles/scripts |
| CSS | [x] KB | [ok/large] | Remove unused CSS, minify, critical CSS extraction |
| JavaScript | [x] KB | [ok/large] | Code-split, tree-shake, defer non-critical |
| Images | [x] KB | [ok/large] | Modern formats, responsive sizes, lazy load below fold |
| Fonts | [x] KB | [ok/large] | Subset, limit families/weights, preload critical |
| Third-party | [x] KB | [ok/large] | Audit necessity, defer, self-host if possible |

**Benchmarks:**
- Total page weight under 1.5 MB is good
- JavaScript under 300 KB (compressed) for most sites
- CSS under 100 KB (compressed)
- First-party fonts under 100 KB

## Output Format

### Speed Audit: [URL or domain]

**Core Web Vitals**

| Metric | Value | Rating | Root Cause |
|--------|-------|--------|------------|
| LCP | [value] | Good / Needs Improvement / Poor | [identified cause] |
| CLS | [value] | ... | ... |
| INP | [value] | ... | ... |
| FCP | [value] | ... | ... |
| TTFB | [value] | ... | ... |

**Resource Breakdown**
[Table from Resource Analysis]

**Priority Fixes**

For each failing metric, ordered by impact:

1. **[Metric]: [Root cause]**
   - Current: [value]
   - Target: [threshold]
   - Fix: [specific action]
   - Estimated impact: [high/medium/low]

2. ...

**Quick Wins**
List optimizations that require minimal effort:
- [ ] Add `width`/`height` to images
- [ ] Set `fetchpriority="high"` on LCP image
- [ ] Defer non-critical JavaScript
- [ ] ...

---

> **Pro Tip:** Use the free [CWV Impact Calculator](https://seojuice.com/tools/cwv-impact/)
> to estimate the traffic impact of fixing Core Web Vitals, and the
> [Critical CSS Generator](https://seojuice.com/tools/critical-css-generator/) to extract
> above-the-fold CSS. SEOJuice MCP users can run `/seojuice:page-audit [domain] [url]` for
> instant CWV scores, Lighthouse data, and resource breakdowns.
