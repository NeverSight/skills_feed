---
name: analytics-engine
description: Write and query high-cardinality event data at scale with SQL. Load when tracking user events, billing metrics, per-tenant analytics, A/B testing, API usage, or custom telemetry. Use writeDataPoint for non-blocking writes and SQL API for aggregations.
---

# Analytics Engine

Write high-cardinality event data at scale and query it with SQL. Perfect for user events, billing metrics, per-tenant analytics, and custom telemetry.

## FIRST: Create Dataset

```bash
wrangler analytics-engine create my-dataset
```

Add binding in `wrangler.jsonc`:

```jsonc
{
  "analytics_engine_datasets": [
    {
      "binding": "USER_EVENTS",
      "dataset": "my-dataset"
    }
  ]
}
```

## When to Use

| Use Case | Why Analytics Engine |
|----------|---------------------|
| User behavior tracking | High-cardinality data (userId, sessionId, etc.) |
| Billing/usage metrics | Per-tenant aggregation with doubles |
| Custom telemetry | Non-blocking writes, queryable with SQL |
| A/B test metrics | Index by experiment ID, query results |
| API usage tracking | Count requests per customer/endpoint |

## Quick Reference

| Operation | API | Notes |
|-----------|-----|-------|
| Write event | `env.DATASET.writeDataPoint({ ... })` | Non-blocking, do NOT await |
| Metrics | `doubles: [value1, value2]` | Up to 20 numeric values |
| Labels | `blobs: [label1, label2]` | Up to 20 text values |
| Grouping | `indexes: [userId]` | 1 index per datapoint (max 96 bytes) |
| Query data | SQL API via REST | GraphQL also available |

## Data Model

Analytics Engine stores datapoints with three types of fields:

| Field Type | Purpose | Limit | Example |
|------------|---------|-------|---------|
| **doubles** | Numeric metrics (counters, gauges, latency) | 20 per datapoint | `[response_time, bytes_sent]` |
| **blobs** | Text labels (URLs, names, IDs) | 20 per datapoint | `[path, event_name]` |
| **indexes** | Grouping key (userId, tenantId, etc.) | 1 per datapoint | `[userId]` |

**Key concept**: The index is the primary key that represents your app, customer, merchant, or tenant. Use it to group and filter data efficiently in SQL queries. For multiple dimensions, use blobs or create a composite index.

## Write Events Example

```typescript
interface Env {
  USER_EVENTS: AnalyticsEngineDataset;
}

export default {
  async fetch(req: Request, env: Env): Promise<Response> {
    let url = new URL(req.url);
    let path = url.pathname;
    let userId = url.searchParams.get("userId");

    // Write a datapoint for this visit, associating the data with
    // the userId as our Analytics Engine 'index'
    env.USER_EVENTS.writeDataPoint({
      // Write metrics data: counters, gauges or latency statistics
      doubles: [],
      // Write text labels - URLs, app names, event_names, etc
      blobs: [path],
      // Provide an index that groups your data correctly.
      indexes: [userId],
    });

    return Response.json({
      hello: "world",
    });
  },
};
```

## API Usage Tracking Example

```typescript
interface Env {
  API_METRICS: AnalyticsEngineDataset;
}

export default {
  async fetch(req: Request, env: Env): Promise<Response> {
    const start = Date.now();
    const url = new URL(req.url);
    const apiKey = req.headers.get("x-api-key") || "anonymous";
    const endpoint = url.pathname;

    try {
      // Handle API request...
      const response = await handleApiRequest(req);
      const duration = Date.now() - start;

      // Track successful request
      env.API_METRICS.writeDataPoint({
        doubles: [duration, response.headers.get("content-length") || 0],
        blobs: [endpoint, "success", response.status.toString()],
        indexes: [apiKey],
      });

      return response;
    } catch (error) {
      const duration = Date.now() - start;

      // Track failed request
      env.API_METRICS.writeDataPoint({
        doubles: [duration, 0],
        blobs: [endpoint, "error", error.message],
        indexes: [apiKey],
      });

      return new Response("Error", { status: 500 });
    }
  },
};
```

## Non-Blocking Writes

**IMPORTANT**: Do NOT `await` calls to `writeDataPoint()`. It is non-blocking and returns immediately.

```typescript
// ❌ WRONG - Do not await
await env.USER_EVENTS.writeDataPoint({ ... });

// ✅ CORRECT - Fire and forget
env.USER_EVENTS.writeDataPoint({ ... });
```

This allows your Worker to respond quickly without waiting for the write to complete.

## Querying with SQL API

Analytics Engine data is accessible via REST API with SQL queries:

**Endpoint**: `https://api.cloudflare.com/client/v4/accounts/{account_id}/analytics_engine/sql`

### Example: Query Recent Events

```sql
SELECT
  timestamp,
  blob1 AS path,
  index1 AS userId
FROM USER_EVENTS
WHERE timestamp > NOW() - INTERVAL '1' DAY
ORDER BY timestamp DESC
LIMIT 100
```

### Example: Aggregate Metrics

```sql
SELECT
  index1 AS apiKey,
  COUNT(*) AS request_count,
  AVG(double1) AS avg_duration_ms,
  SUM(double2) AS total_bytes
FROM API_METRICS
WHERE timestamp > NOW() - INTERVAL '7' DAY
GROUP BY apiKey
ORDER BY request_count DESC
```

### Example: List Datasets

```bash
curl "https://api.cloudflare.com/client/v4/accounts/{account_id}/analytics_engine/sql" \
  --header "Authorization: Bearer <API_TOKEN>" \
  --data "SHOW TABLES"
```

### Field Naming in SQL

Fields are automatically numbered based on write order:

- `double1`, `double2`, ... `double20`
- `blob1`, `blob2`, ... `blob20`
- `index1`, `index2`, ... `index20`

Use `AS` aliases to make queries readable:

```sql
SELECT
  double1 AS response_time,
  blob1 AS endpoint,
  index1 AS user_id
FROM my_dataset
```

## wrangler.jsonc Configuration

```jsonc
{
  "name": "analytics-engine-example",
  "main": "src/index.ts",
  "compatibility_date": "2025-02-11",
  "analytics_engine_datasets": [
    {
      "binding": "USER_EVENTS",
      "dataset": "user-events"
    },
    {
      "binding": "API_METRICS",
      "dataset": "api-metrics"
    }
  ]
}
```

## TypeScript Types

```typescript
interface Env {
  // Analytics Engine dataset binding
  USER_EVENTS: AnalyticsEngineDataset;
}

// Datapoint structure
interface AnalyticsEngineDataPoint {
  doubles?: number[];  // Up to 20 numeric values
  blobs?: string[];    // Up to 20 text values
  indexes?: string[];  // Up to 20 grouping keys
}
```

## Detailed References

- **[references/writing.md](references/writing.md)** - Writing datapoints, field types, patterns
- **[references/querying.md](references/querying.md)** - SQL API, GraphQL, aggregations, time series
- **[references/limits.md](references/limits.md)** - Comprehensive limits, quotas, free tier, sampling behavior
- **[references/testing.md](references/testing.md)** - Mocking strategies (no local simulation available)

## Best Practices

1. **Design indexes first**: Choose grouping keys (userId, tenantId) that match your query patterns
2. **Never await writes**: `writeDataPoint()` is non-blocking for maximum performance
3. **Use doubles for metrics**: Numeric data enables aggregations (AVG, SUM, COUNT)
4. **Use blobs for dimensions**: Text labels for filtering and grouping
5. **Consistent field order**: Keep doubles/blobs/indexes in same order across all writes for consistent SQL queries
6. **Handle missing data**: Use default values or filter NULL in SQL queries
7. **Monitor cardinality**: Too many unique indexes can impact query performance
8. **Use intervals wisely**: Query with time ranges to limit data scanned

## Common Patterns

### Pattern 1: User Session Tracking

```typescript
env.SESSIONS.writeDataPoint({
  doubles: [sessionDuration, pageViews, eventsCount],
  blobs: [browser, country, deviceType],
  indexes: [userId, sessionId],
});
```

### Pattern 2: Error Tracking

```typescript
env.ERRORS.writeDataPoint({
  doubles: [1], // Error count
  blobs: [errorType, errorMessage.slice(0, 256), endpoint],
  indexes: [userId, appVersion],
});
```

### Pattern 3: Revenue Events

```typescript
env.REVENUE.writeDataPoint({
  doubles: [amountCents, taxCents, discountCents],
  blobs: [productId, currency, paymentMethod],
  indexes: [customerId, merchantId],
});
```

## Limits and Considerations

- **Write rate**: Up to 250 data points per Worker invocation
- **Field limits**: 20 doubles, 20 blobs, 1 index per datapoint
- **Blob size**: Total blobs limited to 16 KB per datapoint (increased from 5 KB in June 2025)
- **Index size**: 96 bytes maximum
- **Free tier**: 100,000 writes/day, 10,000 queries/day (not yet enforced)
- **Query performance**: ~100ms average, ~300ms p99
- **Retention**: Data retained for 3 months
- **Eventual consistency**: Small delay between write and query visibility

See **[references/limits.md](references/limits.md)** for complete details.

## Migration from Other Solutions

### From Custom D1 Tables

```typescript
// Before: D1
await env.DB.prepare("INSERT INTO events (userId, event) VALUES (?, ?)")
  .bind(userId, event)
  .run();

// After: Analytics Engine
env.EVENTS.writeDataPoint({
  blobs: [event],
  indexes: [userId],
}); // Non-blocking, no await
```

### From Third-Party Analytics

Analytics Engine provides:
- ✅ No data sampling
- ✅ Full SQL access to raw data
- ✅ No per-event cost
- ✅ Integrated with Workers (no external HTTP calls)
- ✅ High-cardinality data support
