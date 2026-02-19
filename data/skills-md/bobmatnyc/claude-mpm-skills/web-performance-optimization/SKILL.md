---
name: web-performance-optimization
description: "Optimize web performance using Core Web Vitals, modern patterns (View Transitions, Speculation Rules), and framework-specific techniques"
updated_at: 2025-12-02T00:00:00Z
tags: [performance, optimization, lighthouse, core-web-vitals, frontend]
progressive_disclosure:
  entry_point:
    summary: "Optimize web performance through Core Web Vitals, modern browser APIs, and framework-specific patterns for fast, responsive experiences"
    when_to_use: "When improving Lighthouse scores, reducing load times, implementing modern performance patterns, or debugging bottlenecks"
    quick_start: "1. Audit with Lighthouse 2. Apply Quick Wins (lazy loading, compression, preconnect) 3. Optimize Core Web Vitals (LCP, CLS, INP) 4. Add modern patterns (View Transitions, Speculation Rules) 5. Monitor continuously"
  references:
    - quick-wins.md
    - core-web-vitals.md
    - optimization-techniques.md
    - modern-patterns-2025.md
    - framework-specific.md
    - monitoring.md
---

# Web Performance Optimization

Optimize web performance through Core Web Vitals, modern browser APIs (View Transitions, Speculation Rules), and framework-specific techniques.

## When to Use This Skill

- Improving Lighthouse scores (target: 90+)
- Reducing page load times (target: <2.5s LCP)
- Optimizing Core Web Vitals for SEO rankings
- Implementing modern performance patterns (2025)
- Debugging performance bottlenecks
- Setting up continuous performance monitoring

**Business Impact:** 1 second delay = 7% conversion loss. 0.1s improvement = 8% increase in conversions.

## Start Here: Quick Wins

**High-ROI optimizations by time investment:**

**1 Hour Quick Wins (⭐⭐⭐⭐⭐ ROI):**
- Add `loading="lazy"` to below-fold images (40-60% weight reduction)
- Enable compression (gzip/brotli) (70-80% transfer size reduction)
- Add `rel="preconnect"` for critical origins (100-500ms savings)

**1 Day Investments (⭐⭐⭐⭐ ROI):**
- Implement code splitting (30-50% bundle reduction)
- Optimize LCP image with `fetchpriority="high"` (200-400ms improvement)
- Add basic service worker (instant repeat visits)

**1 Week Comprehensive (⭐⭐⭐⭐⭐ ROI):**
- Full caching strategy (HTTP headers + service workers)
- Bundle optimization (tree shaking, 40-60% reduction)
- Performance monitoring (Lighthouse CI + RUM)

**→ See [quick-wins.md](./references/quick-wins.md) for complete implementation details**

## Core Web Vitals at a Glance

| Metric | Target | Weight | Key Optimization |
|--------|--------|--------|------------------|
| **LCP** (Largest Contentful Paint) | <2.5s | 25% | Optimize images, preload critical resources |
| **INP** (Interaction to Next Paint) | <200ms | 30% | Reduce JavaScript, break up long tasks |
| **CLS** (Cumulative Layout Shift) | <0.1 | 25% | Reserve space, optimize fonts |
| **TBT** (Total Blocking Time) | <200ms | 30% | Code splitting, defer non-critical JS |
| **FCP** (First Contentful Paint) | <1.8s | 10% | Eliminate render-blocking resources |

**→ See [core-web-vitals.md](./references/core-web-vitals.md) for deep dive on each metric**

## Modern Patterns (2025)

**View Transitions API** - Smooth page transitions without JavaScript
```css
@view-transition { navigation: auto; }
```

**Speculation Rules API** - Prerender pages for instant navigation  
**React Server Components** - Zero-bundle server components  
**Priority Hints** - `fetchpriority="high"` for LCP optimization  
**Content Visibility** - CSS-based rendering optimization

**→ See [modern-patterns-2025.md](./references/modern-patterns-2025.md) for cutting-edge techniques**

## Navigation

### Quick Start (Load First)
- **[⚡ Quick Wins](./references/quick-wins.md)** - Time-boxed optimizations (1hr/1day/1week) with ROI ratings. Load FIRST for immediate impact.

### Deep Dives
- **[📊 Core Web Vitals](./references/core-web-vitals.md)** - LCP, INP, CLS optimization strategies with debugging workflows. Load when targeting specific metrics.
- **[🔧 Optimization Techniques](./references/optimization-techniques.md)** - Image, JavaScript, CSS, resource loading, caching patterns. Load when implementing specific optimizations.

### Modern Features
- **[✨ Modern Patterns 2025](./references/modern-patterns-2025.md)** - View Transitions, Speculation Rules, RSC, Islands Architecture. Load when adopting cutting-edge patterns.

### Framework-Specific
- **[⚛️ Framework Patterns](./references/framework-specific.md)** - Next.js, React, Vue, Vite, Astro, SvelteKit optimizations. Load for your framework.

### Measurement & Monitoring
- **[📈 Monitoring](./references/monitoring.md)** - Lighthouse CI, RUM setup, performance budgets, debugging tools. Load when setting up continuous monitoring.

## Key Reminders

- **Measure first, optimize second** - Always baseline with Lighthouse/WebPageTest before changes
- **Focus on user-centric metrics** - Core Web Vitals > vanity metrics
- **Test on real devices** - 53% of mobile users abandon after 3 seconds
- **Monitor continuously** - Performance degrades over time without vigilance
- **Prioritize by ROI** - Start with Quick Wins (high impact, low effort)

## Red Flags

Stop and reconsider if:
- Optimizing without baseline measurement
- Focusing only on Lighthouse score (ignoring field data)
- Ignoring mobile performance (53% abandon rate after 3s)
- Loading all resources eagerly (no lazy loading)
- No caching strategy implemented
- Third-party scripts loaded synchronously
- Missing performance monitoring/budgets

## Integration with Other Skills

- **nextjs-core** - Next.js Image component, font optimization, static generation
- **react** - Component optimization, memoization, code splitting
- **vite** - Build optimization, chunk splitting
- **typescript-core** - Type-safe performance patterns

## Real-World Impact

**Conversion Impact:**
- Pinterest: 40% faster perceived wait = 15% more sign-ups + 15% more SEO traffic
- Zalando: 0.1s improvement = 0.7% revenue increase
- AutoAnything: 50% faster load = 12-13% sales increase

**SEO Impact:**
- Core Web Vitals are ranking factors (June 2021+)
- 75% of users passing Core Web Vitals = ranking boost
- Mobile-first indexing prioritizes mobile performance

---

**Remember:** Performance is a feature, not an afterthought. Every millisecond counts. Start with Quick Wins for immediate impact.