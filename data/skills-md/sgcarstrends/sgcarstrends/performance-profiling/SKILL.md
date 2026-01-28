---
name: performance-profiling
description: Profile application performance, identify bottlenecks, and optimize slow operations. Use when investigating performance issues, optimizing response times, or improving resource usage.
allowed-tools: Read, Edit, Write, Bash, Grep
---

# Performance Profiling Skill

This skill helps you profile and optimize application performance across the stack.

## When to Use This Skill

- Investigating slow requests
- Optimizing API response times
- Reducing Lambda cold starts
- Improving database query performance
- Optimizing frontend rendering
- Reducing bundle size
- Improving Time to First Byte (TTFB)

## Performance Metrics

### Key Performance Indicators

**Backend (API):**
- Response time: < 500ms (p95)
- Cold start: < 2s
- Memory usage: < 512MB
- Error rate: < 1%

**Frontend (Web):**
- LCP: < 2.5s
- FID: < 100ms
- CLS: < 0.1
- TTFB: < 600ms
- FCP: < 1.8s

**Database:**
- Query time: < 100ms
- Connection pool: 80% max
- Cache hit rate: > 80%

## Lambda Performance Profiling

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
  --statistics Average,Maximum,Minimum

# Get memory usage
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name MemoryUtilization \
  --dimensions Name=FunctionName,Value=sgcarstrends-api-prod \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Average,Maximum

# Get invocation count
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=sgcarstrends-api-prod \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Sum
```

### Performance Logging

```typescript
// apps/api/src/middleware/performance.ts
import { Context, Next } from "hono";
import { log } from "@sgcarstrends/utils/logger";

export const performanceMiddleware = async (c: Context, next: Next) => {
  const start = performance.now();
  const memoryBefore = process.memoryUsage();

  await next();

  const duration = performance.now() - start;
  const memoryAfter = process.memoryUsage();

  log.info("Request completed", {
    method: c.req.method,
    path: c.req.path,
    status: c.res.status,
    duration: Math.round(duration),
    memory: {
      heapUsed: Math.round((memoryAfter.heapUsed - memoryBefore.heapUsed) / 1024 / 1024),
      external: Math.round((memoryAfter.external - memoryBefore.external) / 1024 / 1024),
    },
  });

  // Warn on slow requests
  if (duration > 1000) {
    log.warn("Slow request detected", {
      path: c.req.path,
      duration: Math.round(duration),
    });
  }

  c.header("X-Response-Time", `${Math.round(duration)}ms`);
};
```

## Database Query Profiling

### Query Timing

```typescript
// packages/database/src/profiler.ts
import { performance } from "perf_hooks";
import { log } from "@sgcarstrends/utils/logger";

export const profileQuery = async <T>(
  name: string,
  query: () => Promise<T>
): Promise<T> => {
  const start = performance.now();

  try {
    const result = await query();
    const duration = performance.now() - start;

    log.info("Query executed", {
      query: name,
      duration: Math.round(duration),
    });

    if (duration > 100) {
      log.warn("Slow query detected", {
        query: name,
        duration: Math.round(duration),
      });
    }

    return result;
  } catch (error) {
    const duration = performance.now() - start;
    log.error("Query failed", error as Error, {
      query: name,
      duration: Math.round(duration),
    });
    throw error;
  }
};

// Usage
const cars = await profileQuery("cars.findMany", () =>
  db.query.cars.findMany({ limit: 100 })
);
```

### Query Analysis

```sql
-- PostgreSQL: Enable query logging
ALTER DATABASE sgcarstrends SET log_statement = 'all';
ALTER DATABASE sgcarstrends SET log_duration = on;
ALTER DATABASE sgcarstrends SET log_min_duration_statement = 100; -- Log queries > 100ms

-- Analyze slow queries
SELECT
  query,
  calls,
  total_time,
  mean_time,
  max_time
FROM pg_stat_statements
WHERE mean_time > 100
ORDER BY mean_time DESC
LIMIT 20;

-- Check query plan
EXPLAIN ANALYZE
SELECT * FROM cars
WHERE make = 'Toyota'
ORDER BY month DESC
LIMIT 100;
```

## API Profiling

### Node.js Built-in Profiler

```bash
# Profile API locally
NODE_OPTIONS="--prof" pnpm -F @sgcarstrends/api dev

# Generate profile after running
node --prof-process isolate-*.log > profile.txt

# Analyze profile
cat profile.txt | head -100
```

### Clinic.js

```bash
# Install clinic
pnpm add -g clinic

# Profile with Clinic Doctor
clinic doctor -- node apps/api/dist/index.js

# Profile with Clinic Flame (flamegraph)
clinic flame -- node apps/api/dist/index.js

# Profile with Clinic Bubbleprof (async operations)
clinic bubbleprof -- node apps/api/dist/index.js
```

### Custom Profiling

```typescript
// apps/api/src/profiler.ts
interface PerformanceEntry {
  name: string;
  duration: number;
  timestamp: Date;
}

class Profiler {
  private entries: PerformanceEntry[] = [];

  start(name: string): () => void {
    const startTime = performance.now();

    return () => {
      const duration = performance.now() - startTime;
      this.entries.push({
        name,
        duration,
        timestamp: new Date(),
      });

      if (duration > 100) {
        log.warn("Slow operation", {
          operation: name,
          duration: Math.round(duration),
        });
      }
    };
  }

  getStats() {
    const grouped = this.entries.reduce((acc, entry) => {
      if (!acc[entry.name]) {
        acc[entry.name] = {
          count: 0,
          total: 0,
          min: Infinity,
          max: 0,
        };
      }

      const stats = acc[entry.name];
      stats.count++;
      stats.total += entry.duration;
      stats.min = Math.min(stats.min, entry.duration);
      stats.max = Math.max(stats.max, entry.duration);

      return acc;
    }, {} as Record<string, { count: number; total: number; min: number; max: number }>);

    return Object.entries(grouped).map(([name, stats]) => ({
      name,
      count: stats.count,
      avg: stats.total / stats.count,
      min: stats.min,
      max: stats.max,
    }));
  }

  reset() {
    this.entries = [];
  }
}

export const profiler = new Profiler();

// Usage
const end = profiler.start("fetchCarData");
const data = await fetchCarData();
end();
```

## Frontend Performance

### React Profiler

```typescript
// apps/web/src/components/ProfilerWrapper.tsx
import { Profiler, ProfilerOnRenderCallback } from "react";

const onRender: ProfilerOnRenderCallback = (
  id,
  phase,
  actualDuration,
  baseDuration,
  startTime,
  commitTime
) => {
  console.log({
    id,
    phase,
    actualDuration,
    baseDuration,
    startTime,
    commitTime,
  });

  // Log slow renders
  if (actualDuration > 16) {  // > 1 frame at 60fps
    console.warn("Slow render detected", {
      component: id,
      duration: actualDuration,
    });
  }
};

export function ProfilerWrapper({ children }: { children: React.ReactNode }) {
  if (process.env.NODE_ENV === "development") {
    return (
      <Profiler id="App" onRender={onRender}>
        {children}
      </Profiler>
    );
  }

  return <>{children}</>;
}
```

### Chrome DevTools Performance

```bash
# 1. Open Chrome DevTools (F12)
# 2. Go to Performance tab
# 3. Click Record
# 4. Perform actions to profile
# 5. Stop recording
# 6. Analyze:
#    - FCP, LCP, CLS
#    - Long tasks
#    - Layout shifts
#    - JavaScript execution time
```

### Lighthouse CI

```yaml
# .github/workflows/lighthouse.yml
name: Lighthouse CI

on: [pull_request]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Run Lighthouse CI
        uses: treosh/lighthouse-ci-action@v10
        with:
          urls: |
            https://staging.sgcarstrends.com
            https://staging.sgcarstrends.com/cars
            https://staging.sgcarstrends.com/coe
          uploadArtifacts: true
          temporaryPublicStorage: true
```

## Memory Profiling

### Node.js Heap Snapshot

```typescript
// apps/api/src/debug.ts
import { writeHeapSnapshot } from "v8";
import { log } from "@sgcarstrends/utils/logger";

export const captureHeapSnapshot = () => {
  const filename = `heap-${Date.now()}.heapsnapshot`;
  writeHeapSnapshot(filename);
  log.info("Heap snapshot captured", { filename });
  return filename;
};

// Usage: Call on high memory usage
if (process.memoryUsage().heapUsed > 400 * 1024 * 1024) {  // > 400MB
  captureHeapSnapshot();
}
```

### Memory Leak Detection

```typescript
// apps/api/src/memory-monitor.ts
import { log } from "@sgcarstrends/utils/logger";

class MemoryMonitor {
  private baseline: NodeJS.MemoryUsage | null = null;

  start() {
    this.baseline = process.memoryUsage();
    log.info("Memory monitoring started", {
      baseline: this.formatMemory(this.baseline),
    });
  }

  check() {
    const current = process.memoryUsage();
    if (!this.baseline) return;

    const diff = {
      heapUsed: current.heapUsed - this.baseline.heapUsed,
      external: current.external - this.baseline.external,
      rss: current.rss - this.baseline.rss,
    };

    log.info("Memory usage", {
      current: this.formatMemory(current),
      diff: this.formatMemory(diff),
    });

    // Warn on memory growth
    if (diff.heapUsed > 100 * 1024 * 1024) {  // > 100MB growth
      log.warn("High memory growth detected", {
        growth: Math.round(diff.heapUsed / 1024 / 1024),
      });
    }
  }

  private formatMemory(mem: Partial<NodeJS.MemoryUsage>) {
    return Object.entries(mem).reduce((acc, [key, value]) => {
      acc[key] = `${Math.round((value || 0) / 1024 / 1024)}MB`;
      return acc;
    }, {} as Record<string, string>);
  }
}

export const memoryMonitor = new MemoryMonitor();
```

## Performance Optimization

### Lambda Optimization

```typescript
// infra/api.ts
export function API({ stack }: StackContext) {
  const api = new Function(stack, "api", {
    handler: "apps/api/src/index.handler",
    runtime: "nodejs20.x",
    architecture: "arm64",  // Graviton2 for better performance
    memory: "1024 MB",  // More memory = faster CPU
    timeout: "30 seconds",
    environment: {
      NODE_ENV: "production",
      LOG_LEVEL: "info",
    },
    nodejs: {
      esbuild: {
        minify: true,
        bundle: true,
        target: "node20",
        sourcemap: true,
        external: ["@aws-sdk/*"],  // Don't bundle AWS SDK
      },
    },
  });
}
```

### Caching Strategy

```typescript
// apps/api/src/cache.ts
import { redis } from "@sgcarstrends/utils";

export const withCache = async <T>(
  key: string,
  ttl: number,
  fn: () => Promise<T>
): Promise<T> => {
  const start = performance.now();

  // Check cache
  const cached = await redis.get(key);
  if (cached) {
    const duration = performance.now() - start;
    log.info("Cache hit", {
      key,
      duration: Math.round(duration),
    });
    return JSON.parse(cached as string);
  }

  // Cache miss - execute function
  const result = await fn();
  await redis.set(key, JSON.stringify(result), { ex: ttl });

  const duration = performance.now() - start;
  log.info("Cache miss", {
    key,
    duration: Math.round(duration),
  });

  return result;
};

// Usage
const cars = await withCache("cars:all", 3600, async () => {
  return await db.query.cars.findMany();
});
```

## Performance Testing

### Load Testing with k6

```javascript
// load-test.js
import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  stages: [
    { duration: "2m", target: 100 },  // Ramp up to 100 users
    { duration: "5m", target: 100 },  // Stay at 100 users
    { duration: "2m", target: 200 },  // Ramp up to 200 users
    { duration: "5m", target: 200 },  // Stay at 200 users
    { duration: "2m", target: 0 },    // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ["p(95)<500"],  // 95% of requests < 500ms
    http_req_failed: ["rate<0.01"],    // < 1% failures
  },
};

export default function () {
  const res = http.get("https://api.sgcarstrends.com/api/v1/cars/makes");

  check(res, {
    "status is 200": (r) => r.status === 200,
    "response time < 500ms": (r) => r.timings.duration < 500,
  });

  sleep(1);
}
```

```bash
# Run load test
k6 run load-test.js

# Run with more virtual users
k6 run --vus 500 --duration 5m load-test.js
```

## Performance Dashboard

### CloudWatch Dashboard

```typescript
// infra/dashboard.ts
import { aws_cloudwatch as cloudwatch } from "aws-cdk-lib";

export function PerformanceDashboard({ stack }: StackContext) {
  new cloudwatch.Dashboard(stack, "PerformanceDashboard", {
    dashboardName: "sgcarstrends-performance",
    widgets: [
      [
        // Lambda duration
        new cloudwatch.GraphWidget({
          title: "API Response Time",
          left: [
            new cloudwatch.Metric({
              namespace: "AWS/Lambda",
              metricName: "Duration",
              dimensionsMap: {
                FunctionName: "sgcarstrends-api-prod",
              },
              statistic: "Average",
            }),
          ],
        }),

        // Error rate
        new cloudwatch.GraphWidget({
          title: "Error Rate",
          left: [
            new cloudwatch.Metric({
              namespace: "AWS/Lambda",
              metricName: "Errors",
              dimensionsMap: {
                FunctionName: "sgcarstrends-api-prod",
              },
              statistic: "Sum",
            }),
          ],
        }),
      ],

      [
        // Memory usage
        new cloudwatch.GraphWidget({
          title: "Memory Usage",
          left: [
            new cloudwatch.Metric({
              namespace: "AWS/Lambda",
              metricName: "MemoryUtilization",
              dimensionsMap: {
                FunctionName: "sgcarstrends-api-prod",
              },
              statistic: "Average",
            }),
          ],
        }),

        // Invocations
        new cloudwatch.GraphWidget({
          title: "Invocations",
          left: [
            new cloudwatch.Metric({
              namespace: "AWS/Lambda",
              metricName: "Invocations",
              dimensionsMap: {
                FunctionName: "sgcarstrends-api-prod",
              },
              statistic: "Sum",
            }),
          ],
        }),
      ],
    ],
  });
}
```

## Best Practices

### 1. Profile Before Optimizing

```typescript
// ❌ Optimize without profiling
// Just guessing what's slow

// ✅ Profile first, then optimize
const end = profiler.start("operation");
await operation();
end();

// Check profiler stats to find bottleneck
console.log(profiler.getStats());
```

### 2. Set Performance Budgets

```javascript
// lighthouse.config.js
module.exports = {
  ci: {
    collect: {
      numberOfRuns: 3,
    },
    assert: {
      assertions: {
        "categories:performance": ["error", { minScore: 0.9 }],
        "first-contentful-paint": ["error", { maxNumericValue: 1800 }],
        "largest-contentful-paint": ["error", { maxNumericValue: 2500 }],
        "cumulative-layout-shift": ["error", { maxNumericValue: 0.1 }],
      },
    },
  },
};
```

### 3. Monitor Continuously

```typescript
// ✅ Continuous monitoring
setInterval(() => {
  memoryMonitor.check();
}, 60000);  // Check every minute

// ✅ Log performance metrics
app.use(performanceMiddleware);
```

## Troubleshooting

### High Response Times

```bash
# 1. Check CloudWatch metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Duration \
  --dimensions Name=FunctionName,Value=sgcarstrends-api-prod \
  --statistics Average,Maximum \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300

# 2. Check logs for slow operations
aws logs filter-log-events \
  --log-group-name /aws/lambda/sgcarstrends-api-prod \
  --filter-pattern "duration > 1000"

# 3. Profile locally
NODE_OPTIONS="--prof" pnpm -F @sgcarstrends/api dev

# 4. Optimize bottleneck
```

### Memory Issues

```bash
# 1. Check memory usage
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name MemoryUtilization \
  --dimensions Name=FunctionName,Value=sgcarstrends-api-prod \
  --statistics Average,Maximum

# 2. Capture heap snapshot
# Add to code: captureHeapSnapshot()

# 3. Analyze with Chrome DevTools
# Load .heapsnapshot file in DevTools Memory tab

# 4. Fix memory leaks
```

## References

- Node.js Profiling: https://nodejs.org/en/docs/guides/simple-profiling
- Chrome DevTools: https://developer.chrome.com/docs/devtools/performance
- Lighthouse: https://developer.chrome.com/docs/lighthouse
- k6 Load Testing: https://k6.io/docs
- Related files:
  - `apps/api/src/middleware/performance.ts` - Performance middleware
  - Root CLAUDE.md - Performance guidelines

## Best Practices Summary

1. **Profile First**: Always profile before optimizing
2. **Monitor Continuously**: Track performance metrics
3. **Set Budgets**: Define performance budgets and enforce them
4. **Log Performance**: Log slow operations automatically
5. **Cache Aggressively**: Cache expensive operations
6. **Optimize Critical Path**: Focus on user-facing operations
7. **Load Test**: Test under realistic load
8. **Memory Awareness**: Monitor memory usage and prevent leaks
