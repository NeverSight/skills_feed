---
name: performance-optimization
description: Profiling, optimization techniques, and performance best practices
domain: software-engineering
version: 1.0.0
tags: [performance, profiling, optimization, caching, database, frontend]
triggers:
  keywords:
    primary: [performance, optimize, optimization, profiling, benchmark, speed]
    secondary: [caching, latency, throughput, memory, cpu, bottleneck, lighthouse]
  context_boost: [slow, fast, improve, scale]
  context_penalty: [design, architecture, security]
  priority: high
---

# Performance Optimization

## Overview

Measure first, optimize second. This guide covers profiling techniques and optimization strategies.

---

## Profiling First

### The Golden Rule

```
1. Don't optimize prematurely
2. Measure before optimizing
3. Optimize the biggest bottleneck first
4. Measure again to verify improvement
```

### CPU Profiling (Node.js)

```typescript
// Using Node.js built-in profiler
// Start with: node --prof app.js
// Process: node --prof-process isolate-*.log > profile.txt

// Or use clinic.js
// npm install -g clinic
// clinic doctor -- node app.js
// clinic flame -- node app.js

// Programmatic profiling
import { performance, PerformanceObserver } from 'perf_hooks';

const obs = new PerformanceObserver((items) => {
  items.getEntries().forEach((entry) => {
    console.log(`${entry.name}: ${entry.duration}ms`);
  });
});
obs.observe({ entryTypes: ['measure'] });

performance.mark('start');
await expensiveOperation();
performance.mark('end');
performance.measure('expensive-op', 'start', 'end');
```

### Memory Profiling

```typescript
// Check memory usage
console.log(process.memoryUsage());
// {
//   rss: 30000000,      // Resident Set Size - total memory
//   heapTotal: 7000000, // V8 heap total
//   heapUsed: 5000000,  // V8 heap used
//   external: 800000    // C++ objects bound to JS
// }

// Take heap snapshot
const v8 = require('v8');
const fs = require('fs');

const snapshotFile = `heap-${Date.now()}.heapsnapshot`;
const snapshot = v8.writeHeapSnapshot(snapshotFile);
// Open in Chrome DevTools Memory tab
```

---

## Database Optimization

### Query Optimization

```sql
-- ❌ Slow: SELECT * and no index
SELECT * FROM orders WHERE user_id = 123;

-- ✅ Better: Select only needed columns, with index
CREATE INDEX idx_orders_user_id ON orders(user_id);
SELECT id, total, status FROM orders WHERE user_id = 123;

-- ❌ N+1 query problem
-- For each user, query their orders (100 users = 101 queries)
SELECT * FROM users;
SELECT * FROM orders WHERE user_id = 1;
SELECT * FROM orders WHERE user_id = 2;
...

-- ✅ Single query with JOIN
SELECT u.*, o.* FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

-- Or batch loading
SELECT * FROM orders WHERE user_id IN (1, 2, 3, ...);
```

### Explain Analyze

```sql
EXPLAIN ANALYZE
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01'
GROUP BY u.id
ORDER BY order_count DESC
LIMIT 10;

-- Output shows:
-- - Execution plan (Seq Scan vs Index Scan)
-- - Estimated vs actual rows
-- - Time per operation
-- - Total execution time
```

### Index Strategies

```sql
-- Single column index
CREATE INDEX idx_users_email ON users(email);

-- Composite index (order matters!)
-- Good for: WHERE status = 'active' AND created_at > '2024-01-01'
CREATE INDEX idx_orders_status_created ON orders(status, created_at);

-- Partial index (smaller, faster for filtered queries)
CREATE INDEX idx_active_users ON users(email)
WHERE status = 'active';

-- Covering index (includes all needed columns)
CREATE INDEX idx_orders_user_covering ON orders(user_id)
INCLUDE (total, status, created_at);

-- When NOT to index:
-- - Small tables
-- - Columns with low cardinality (e.g., boolean)
-- - Frequently updated columns
-- - Write-heavy tables
```

---

## Caching

### Cache Strategies

```typescript
// Cache-aside pattern
async function getUser(id: string): Promise<User> {
  // Try cache first
  const cached = await cache.get(`user:${id}`);
  if (cached) return JSON.parse(cached);

  // Cache miss - fetch from DB
  const user = await db.users.findById(id);

  // Store in cache
  if (user) {
    await cache.set(`user:${id}`, JSON.stringify(user), 'EX', 3600);
  }

  return user;
}

// Write-through pattern
async function updateUser(id: string, data: Partial<User>): Promise<User> {
  // Update DB
  const user = await db.users.update(id, data);

  // Update cache immediately
  await cache.set(`user:${id}`, JSON.stringify(user), 'EX', 3600);

  return user;
}
```

### Cache Invalidation

```typescript
// Event-based invalidation
eventBus.on('user:updated', async (userId: string) => {
  await cache.del(`user:${userId}`);
  await cache.del(`user:${userId}:orders`);
});

// Tag-based invalidation
async function invalidateUserRelated(userId: string) {
  const keys = await cache.keys(`*:user:${userId}:*`);
  if (keys.length > 0) {
    await cache.del(...keys);
  }
}

// Version-based cache busting
const CACHE_VERSION = 'v2';
const cacheKey = `${CACHE_VERSION}:user:${id}`;
```

### Memoization

```typescript
// Simple memoization
function memoize<T extends (...args: any[]) => any>(fn: T): T {
  const cache = new Map();

  return ((...args: Parameters<T>) => {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);

    const result = fn(...args);
    cache.set(key, result);
    return result;
  }) as T;
}

// With TTL
function memoizeWithTTL<T extends (...args: any[]) => any>(
  fn: T,
  ttlMs: number
): T {
  const cache = new Map<string, { value: any; expires: number }>();

  return ((...args: Parameters<T>) => {
    const key = JSON.stringify(args);
    const cached = cache.get(key);

    if (cached && cached.expires > Date.now()) {
      return cached.value;
    }

    const result = fn(...args);
    cache.set(key, { value: result, expires: Date.now() + ttlMs });
    return result;
  }) as T;
}
```

---

## Frontend Performance

### Core Web Vitals

| Metric | Good | Description |
|--------|------|-------------|
| LCP | < 2.5s | Largest Contentful Paint |
| INP | < 200ms | Interaction to Next Paint |
| CLS | < 0.1 | Cumulative Layout Shift |

### Code Splitting

```typescript
// React lazy loading
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./Dashboard'));
const Settings = lazy(() => import('./Settings'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}

// Dynamic import for heavy libraries
async function processImage(file: File) {
  const sharp = await import('sharp');
  return sharp(file).resize(800).toBuffer();
}
```

### Image Optimization

```html
<!-- Responsive images -->
<img
  src="image-800.jpg"
  srcset="
    image-400.jpg 400w,
    image-800.jpg 800w,
    image-1200.jpg 1200w
  "
  sizes="(max-width: 600px) 400px, 800px"
  loading="lazy"
  alt="Description"
/>

<!-- Modern formats with fallback -->
<picture>
  <source srcset="image.avif" type="image/avif" />
  <source srcset="image.webp" type="image/webp" />
  <img src="image.jpg" alt="Description" />
</picture>
```

### Bundle Optimization

```javascript
// webpack.config.js
module.exports = {
  optimization: {
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          chunks: 'all',
        },
        // Separate large libraries
        react: {
          test: /[\\/]node_modules[\\/](react|react-dom)[\\/]/,
          name: 'react',
          chunks: 'all',
        },
      },
    },
  },
};
```

---

## Backend Performance

### Connection Pooling

```typescript
// Database connection pool
import { Pool } from 'pg';

const pool = new Pool({
  max: 20,                    // Maximum connections
  idleTimeoutMillis: 30000,   // Close idle connections after 30s
  connectionTimeoutMillis: 2000, // Fail if can't connect in 2s
});

// Use pool, not individual connections
async function getUser(id: string) {
  const result = await pool.query('SELECT * FROM users WHERE id = $1', [id]);
  return result.rows[0];
}

// HTTP connection keep-alive
import http from 'http';

const agent = new http.Agent({
  keepAlive: true,
  maxSockets: 50,
});

fetch('https://api.example.com', { agent });
```

### Async Processing

```typescript
// Move slow operations out of request path
app.post('/api/orders', async (req, res) => {
  // Quick: Create order
  const order = await db.orders.create(req.body);

  // Don't wait: Queue async tasks
  await queue.add('send-confirmation-email', { orderId: order.id });
  await queue.add('update-inventory', { items: order.items });
  await queue.add('notify-warehouse', { orderId: order.id });

  // Respond immediately
  res.status(201).json(order);
});

// Process queue separately
queue.process('send-confirmation-email', async (job) => {
  const order = await db.orders.findById(job.data.orderId);
  await emailService.sendOrderConfirmation(order);
});
```

### Response Compression

```typescript
import compression from 'compression';
import express from 'express';

const app = express();

// Compress responses > 1KB
app.use(compression({
  threshold: 1024,
  filter: (req, res) => {
    if (req.headers['x-no-compression']) {
      return false;
    }
    return compression.filter(req, res);
  }
}));
```

---

## Algorithm Optimization

### Time Complexity

```typescript
// O(n²) → O(n) with Set
// Find duplicates
function hasDuplicates(arr: number[]): boolean {
  // ❌ O(n²)
  for (let i = 0; i < arr.length; i++) {
    for (let j = i + 1; j < arr.length; j++) {
      if (arr[i] === arr[j]) return true;
    }
  }
  return false;

  // ✅ O(n)
  const seen = new Set<number>();
  for (const num of arr) {
    if (seen.has(num)) return true;
    seen.add(num);
  }
  return false;
}

// O(n) → O(1) with Map
// Lookup by key
class UserCache {
  // ❌ O(n) lookup
  private users: User[] = [];

  find(id: string) {
    return this.users.find(u => u.id === id);
  }

  // ✅ O(1) lookup
  private usersMap = new Map<string, User>();

  findFast(id: string) {
    return this.usersMap.get(id);
  }
}
```

### Space vs Time Tradeoff

```typescript
// Trade memory for speed: Precompute
class TaxCalculator {
  private taxRates = new Map<string, number>();

  constructor() {
    // Precompute all tax rates
    for (const state of US_STATES) {
      this.taxRates.set(state, this.computeTaxRate(state));
    }
  }

  // O(1) instead of O(complex calculation)
  getTaxRate(state: string): number {
    return this.taxRates.get(state) ?? 0;
  }
}
```

---

## Monitoring Performance

```typescript
// Application metrics
import { Counter, Histogram } from 'prom-client';

const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests',
  labelNames: ['method', 'route', 'status'],
  buckets: [0.1, 0.5, 1, 2, 5]
});

app.use((req, res, next) => {
  const start = Date.now();

  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    httpRequestDuration
      .labels(req.method, req.route?.path || 'unknown', res.statusCode.toString())
      .observe(duration);
  });

  next();
});
```

---

## Related Skills

- [[database]] - Database optimization details
- [[frontend]] - Frontend performance
- [[monitoring-observability]] - Performance monitoring
