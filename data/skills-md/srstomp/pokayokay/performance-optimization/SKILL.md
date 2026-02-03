---
name: performance-optimization
description: Performance analysis, optimization techniques, and performance testing for web applications. Covers profiling, bottleneck identification, frontend optimization (bundle size, rendering, Core Web Vitals), backend optimization (query optimization, caching, async patterns), load testing (k6, Artillery), and monitoring (performance budgets, SLIs). Use this skill when analyzing performance issues, optimizing slow pages or APIs, setting up load testing, implementing caching, reducing bundle sizes, or establishing performance budgets. Triggers on "performance", "slow", "optimize", "bundle size", "load testing", "cache", "bottleneck", "latency", "Core Web Vitals", "LCP", "FCP", "lighthouse", "profiling".
---

# Performance Optimization

Systematic approach to identifying and fixing performance bottlenecks.

## Performance Analysis Workflow

```
1. Measure First
   └─→ Never optimize without data
   └─→ Establish baseline metrics

2. Identify Bottleneck Type
   ├─→ Network? (TTFB, downloads)
   ├─→ CPU? (parsing, execution)
   ├─→ Memory? (leaks, GC pressure)
   ├─→ I/O? (disk, database)
   └─→ Rendering? (layout, paint)

3. Apply Targeted Fix
   └─→ One change at a time
   └─→ Re-measure after each change

4. Validate Improvement
   └─→ Compare against baseline
```

## Quick Wins Checklist

### Frontend Quick Wins

| Action | Impact | Effort |
|--------|--------|--------|
| Enable gzip/brotli compression | 60-80% smaller | Low |
| Add caching headers | Eliminate repeat downloads | Low |
| Lazy load below-fold images | Faster initial paint | Low |
| Preconnect to critical origins | 100-300ms savings | Low |
| Remove unused CSS/JS | 20-50% smaller | Medium |
| Code split by route | 50%+ smaller initial | Medium |

### Backend Quick Wins

| Action | Impact | Effort |
|--------|--------|--------|
| Add database indexes | 10-100x faster queries | Low |
| Enable query result caching | Eliminate repeat queries | Low |
| Use connection pooling | Better throughput | Low |
| Fix N+1 queries | 90%+ fewer queries | Medium |
| Add response caching | Sub-ms responses | Medium |

## Core Web Vitals

| Metric | Good | Needs Work | Poor |
|--------|------|------------|------|
| **LCP** (Largest Contentful Paint) | < 2.5s | < 4.0s | > 4.0s |
| **INP** (Interaction to Next Paint) | < 200ms | < 500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | < 0.1 | < 0.25 | > 0.25 |
| **TTFB** (Time to First Byte) | < 800ms | < 1.8s | > 1.8s |

**LCP optimization:**
- Preload LCP image with `fetchpriority="high"`
- Avoid lazy loading LCP element
- Inline critical CSS
- Use SSR/SSG for critical content

**CLS prevention:**
- Always set width/height on images
- Reserve space for ads/embeds
- Use `font-display: swap` for fonts

**INP optimization:**
- Break long tasks (>50ms) with `scheduler.yield()` or `setTimeout`
- Move heavy work to Web Workers
- Debounce event handlers

## Optimization by Layer

### Network Layer

**Caching strategy decision:**

```
Is content user-specific?
├─→ Yes: private, max-age=0 + ETag
└─→ No: Is static (hashed filename)?
    ├─→ Yes: public, max-age=31536000, immutable
    └─→ No: public, max-age=3600, stale-while-revalidate
```

### JavaScript Performance

**Bundle size targets:**
- Initial JS: < 200KB compressed
- Per-route chunks: < 50KB compressed
- Parse cost: ~1ms per 10KB on mobile

**Code splitting pattern:**

```typescript
// Route-based splitting
const Dashboard = lazy(() => import('./Dashboard'));

// Feature-based splitting
if (showAdvanced) {
  import('./AdvancedFeatures').then(m => m.init());
}
```

### Rendering Performance

**Stable references prevent re-renders:**

```typescript
const handleClick = useCallback(() => doSomething(id), [id]);
const sortedData = useMemo(() => data.sort(...), [data]);
```

**Avoid layout thrashing:**

```typescript
// ❌ Read-write-read-write
elements.forEach(el => {
  const h = el.offsetHeight; // Read
  el.style.height = h + 10 + 'px'; // Write
});

// ✅ Batch reads then batch writes
const heights = elements.map(el => el.offsetHeight);
elements.forEach((el, i) => el.style.height = heights[i] + 10 + 'px');
```

### Database Layer

**Index selection:**

```sql
-- Composite index: most selective column first
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Covering index for common queries
CREATE INDEX idx_orders_covering ON orders(user_id) INCLUDE (total, created_at);
```

**N+1 detection:**

```typescript
// ❌ N+1: 1 + N queries
const posts = await db.posts.findMany();
for (const post of posts) {
  post.author = await db.users.findUnique({ where: { id: post.authorId } });
}

// ✅ Eager loading: 2 queries total
const posts = await db.posts.findMany({ include: { author: true } });
```

## Performance Budgets

**Setting budgets:**
1. Measure competitors or industry benchmarks
2. Set targets 20% better than current
3. Enforce in CI (fail builds that exceed)

**Example budget:**

```javascript
{
  "budgets": [
    { "resourceType": "script", "budget": 200 },    // KB
    { "metric": "lcp", "budget": 2500 },            // ms
    { "metric": "fcp", "budget": 1500 }             // ms
  ]
}
```

**CI enforcement:**

```yaml
# Lighthouse CI
- name: Run Lighthouse
  run: lhci autorun
  
# lighthouserc.json
{
  "assertions": {
    "categories:performance": ["error", { "minScore": 0.9 }],
    "largest-contentful-paint": ["error", { "maxNumericValue": 2500 }]
  }
}
```

## Profiling Quick Reference

| Tool | Use For |
|------|---------|
| **Chrome Performance** | CPU profiling, flame charts, main thread |
| **Chrome Network** | Request waterfall, timing breakdown |
| **Chrome Lighthouse** | Automated audits, Core Web Vitals |
| **Chrome Memory** | Heap snapshots, allocation timeline |
| **Chrome Coverage** | Unused JS/CSS detection |
| **Node --inspect** | CPU/memory profiling with DevTools |
| **0x / clinic** | Node.js flame graphs |

## Anti-Patterns

**❌ Premature optimization:**
Profile first, optimize what matters. Most code doesn't need memoization.

**❌ Over-caching:**
Cache strategically—expensive computations that tolerate staleness.

**❌ Blocking main thread:**

```typescript
// ❌ Large sync operation
const result = JSON.parse(hugeJsonString);

// ✅ Offload or chunk
worker.postMessage(hugeJsonString);
// or yield between chunks
```

## Skill Usage

**Analyzing performance issues:**
1. Gather baseline metrics (Lighthouse, RUM)
2. Identify bottleneck type using workflow above
3. Check quick wins checklist first
4. Read relevant reference for deep optimization

**Frontend optimization:**
1. Run Lighthouse audit
2. Read [references/frontend-perf.md](references/frontend-perf.md)
3. Check Core Web Vitals section
4. Implement fixes, re-measure

**Backend optimization:**
1. Profile with APM or Node inspector
2. Read [references/backend-perf.md](references/backend-perf.md)
3. Focus on database queries first
4. Add caching where beneficial

**Load testing:**
1. Define performance requirements
2. Read [references/load-testing.md](references/load-testing.md)
3. Create k6 or Artillery scripts
4. Run tests, identify limits

**Setting up profiling:**
1. Read [references/profiling-guide.md](references/profiling-guide.md)
2. Choose appropriate tool for the layer
3. Generate profiles under realistic load

---

**References:**
- [references/frontend-perf.md](references/frontend-perf.md) — Bundle analysis, rendering, Core Web Vitals
- [references/backend-perf.md](references/backend-perf.md) — Query optimization, caching, async patterns
- [references/load-testing.md](references/load-testing.md) — k6, Artillery patterns, CI integration
- [references/profiling-guide.md](references/profiling-guide.md) — Chrome DevTools, Node profiling, flame graphs
