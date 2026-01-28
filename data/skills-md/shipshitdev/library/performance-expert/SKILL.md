---
name: performance-expert
description: Expert in performance optimization for React, Next.js, NestJS applications covering frontend rendering, API response times, database queries, and infrastructure optimization
---

# Performance Expert Skill

Expert in performance optimization for React, Next.js, NestJS applications, MongoDB, and AWS infrastructure.

## When to Use This Skill

- Optimizing React components or Next.js pages
- Improving API response times
- Optimizing database queries
- Analyzing bundle sizes
- Implementing caching strategies
- Optimizing images or assets
- Configuring CDN or caching
- Reviewing Core Web Vitals

## Project Context Discovery

1. Check `.agent/SYSTEM/ARCHITECTURE.md` for performance architecture
2. Identify performance tools (Lighthouse CI, APM)
3. Review existing optimizations and caching strategies
4. Check for `[project]-performance-expert` skill

## Core Performance Principles

### Frontend (React/Next.js)

**Bundle Optimization:** Code splitting, dynamic imports, tree shaking, remove unused deps

**React Optimization:** useMemo, useCallback, React.memo, virtualization, lazy loading

**Next.js:** Server Components, SSG, ISR, next/image, font optimization

**Assets:** WebP images, font subset, CSS minify, Gzip/Brotli

### Backend (NestJS)

**API Response Times:** Target < 200ms (p95), caching, background jobs, connection pooling

**Query Optimization:** Indexes, projections, pagination, optimized aggregations

### Database (MongoDB)

**Indexes:** On frequently queried fields, compound indexes, monitor usage

**Queries:** Early $match, projection before expensive ops, sort with indexes

### Infrastructure (AWS)

**CDN:** CloudFront caching, cache headers, edge optimization

**Lambda:** Cold start optimization, memory allocation, provisioned concurrency

## Performance Metrics

### Frontend (Core Web Vitals)

- **LCP:** < 2.5s
- **FID:** < 100ms
- **CLS:** < 0.1
- **FCP:** < 1.8s

### Backend

- **API p50:** < 100ms
- **API p95:** < 200ms
- **DB Query p95:** < 50ms
- **Error Rate:** < 0.1%

## Quick Checklist

### Frontend

- [ ] Bundle size < 200KB initial
- [ ] Code splitting implemented
- [ ] Images optimized and lazy loaded
- [ ] React components memoized

### Backend

- [ ] Database queries optimized
- [ ] Indexes created and used
- [ ] Caching implemented
- [ ] Background jobs for heavy operations

---

**For complete React memoization patterns, Next.js optimization examples, database query optimization code, caching strategy implementation, N+1 query solutions, performance testing commands, and detailed checklists, see:** `references/full-guide.md`
