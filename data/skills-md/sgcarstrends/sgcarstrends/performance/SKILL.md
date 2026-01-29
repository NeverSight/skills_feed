---
name: performance
description: Optimize application performance - bundle size, API response times, database queries, React rendering, and Lambda cold starts. Use when investigating slow pages, profiling, load testing, or before production deployments.
allowed-tools: Read, Edit, Bash, Grep, Glob
---

# Performance Skill

## Performance Targets

**Frontend (Web Vitals):** LCP < 2.5s, FID < 100ms, CLS < 0.1, FCP < 1.8s, TTFB < 600ms
**Backend:** Response time < 500ms (p95), cold start < 2s, error rate < 1%
**Database:** Query time < 100ms, cache hit rate > 80%

## Measure Performance

```bash
# Lighthouse audit
npx lighthouse https://sgcarstrends.com --view

# Bundle analysis
cd apps/web && ANALYZE=true pnpm build

# Load test with k6
k6 run --vus 100 --duration 5m load-test.js
```

## Bundle Size Optimization

### Dynamic Imports

```typescript
// ❌ Static import (loads immediately)
import { HeavyComponent } from "./heavy-component";

// ✅ Dynamic import (lazy load)
import dynamic from "next/dynamic";
const HeavyComponent = dynamic(() => import("./heavy-component"), {
  loading: () => <div>Loading...</div>,
  ssr: false,
});
```

### Tree Shaking

```typescript
// ❌ Imports entire library
import _ from "lodash";

// ✅ Import only what you need
import uniq from "lodash/uniq";
```

## React Performance

### Prevent Re-renders

```typescript
// useMemo for expensive calculations
const processed = useMemo(() => expensiveOperation(data), [data]);

// useCallback for stable function references
const handleClick = useCallback(() => doSomething(), []);

// React.memo for pure components
const Child = React.memo(function Child({ name }) {
  return <div>{name}</div>;
});
```

### Virtualize Long Lists

```typescript
import { FixedSizeList } from "react-window";

<FixedSizeList height={600} itemCount={items.length} itemSize={100} width="100%">
  {({ index, style }) => <Item style={style} data={items[index]} />}
</FixedSizeList>
```

## Database Query Optimization

### Add Indexes

```typescript
// packages/database/src/schema/cars.ts
export const cars = pgTable("cars", {
  make: text("make").notNull(),
  month: text("month").notNull(),
}, (table) => ({
  makeIdx: index("cars_make_idx").on(table.make),
}));
```

### Avoid N+1 Queries

```typescript
// ❌ N+1 queries
for (const post of posts) {
  post.author = await db.query.users.findFirst({ where: eq(users.id, post.authorId) });
}

// ✅ Single query with relation
const posts = await db.query.posts.findMany({ with: { author: true } });
```

### Select Only Needed Columns

```typescript
// ❌ Selects all columns
const users = await db.query.users.findMany();

// ✅ Select specific columns
const users = await db.select({ id: users.id, name: users.name }).from(users);
```

### Use Pagination

```typescript
const cars = await db.query.cars.findMany({
  limit: 20,
  offset: (page - 1) * 20,
});
```

## Caching

### Redis Caching

```typescript
import { redis } from "@sgcarstrends/utils";

export async function getCarsWithCache(make: string) {
  const cacheKey = `cars:${make}`;
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached as string);

  const cars = await db.query.cars.findMany({ where: eq(cars.make, make) });
  await redis.set(cacheKey, JSON.stringify(cars), { ex: 3600 });
  return cars;
}
```

### Next.js Caching

```typescript
// Revalidate every hour
export const revalidate = 3600;

// Or use fetch with caching
const data = await fetch(url, { next: { revalidate: 3600 } });
```

## Image Optimization

```typescript
import Image from "next/image";

// ✅ Optimized image with priority for above-fold
<Image
  src="/hero.jpg"
  alt="Hero"
  fill
  sizes="(max-width: 768px) 100vw, 50vw"
  priority
/>
```

## Lambda Optimization

```typescript
// infra/api.ts - SST Function construct
{
  handler: "apps/api/src/index.handler",
  runtime: "nodejs20.x",
  architecture: "arm64",  // Graviton2 for better performance
  memory: 1024,           // More memory = faster CPU
  nodejs: {
    esbuild: { minify: true, bundle: true },
  },
}
```

## Profiling

### Performance Middleware

```typescript
// apps/api/src/middleware/performance.ts
export const performanceMiddleware = async (c: Context, next: Next) => {
  const start = performance.now();
  await next();
  const duration = performance.now() - start;

  c.header("X-Response-Time", `${Math.round(duration)}ms`);

  if (duration > 1000) {
    log.warn("Slow request", { path: c.req.path, duration: Math.round(duration) });
  }
};
```

### Query Profiling

```typescript
const start = performance.now();
const result = await db.query.cars.findMany();
const duration = performance.now() - start;

if (duration > 100) {
  console.warn(`Slow query: ${duration}ms`);
}
```

### CloudWatch Metrics

```bash
# Get Lambda duration metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Duration \
  --dimensions Name=FunctionName,Value=sgcarstrends-api-prod \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Average,Maximum
```

## Load Testing

```javascript
// load-test.js (k6)
import http from "k6/http";
import { check } from "k6";

export const options = {
  stages: [
    { duration: "2m", target: 100 },
    { duration: "5m", target: 100 },
    { duration: "2m", target: 0 },
  ],
  thresholds: {
    http_req_duration: ["p(95)<500"],
    http_req_failed: ["rate<0.01"],
  },
};

export default function() {
  const res = http.get("https://api.sgcarstrends.com/api/v1/cars/makes");
  check(res, { "status 200": (r) => r.status === 200 });
}
```

## Performance Checklist

- [ ] Bundle size < 200KB (initial load)
- [ ] LCP < 2.5s, FID < 100ms, CLS < 0.1
- [ ] API responses < 500ms
- [ ] Database queries < 100ms
- [ ] Images optimized (WebP/AVIF)
- [ ] Code splitting implemented
- [ ] Caching strategy in place
- [ ] Long lists virtualized
- [ ] Compression enabled

## Quick Wins

1. **Compression**: Enable gzip/brotli (60-80% size reduction)
2. **Image Optimization**: Use Next.js Image component
3. **Caching**: Cache expensive operations in Redis
4. **Indexes**: Add indexes to frequently queried columns
5. **Code Splitting**: Lazy load heavy components
6. **Memoization**: Use useMemo/useCallback for expensive operations

## References

- Web Vitals: https://web.dev/vitals
- Next.js Performance: https://nextjs.org/docs/app/building-your-application/optimizing
- k6 Load Testing: https://k6.io/docs
