---
name: query-optimization
description: Optimize database queries, add indexes, prevent N+1 queries, and improve query performance. Use when queries are slow, investigating database bottlenecks, or optimizing data access patterns.
allowed-tools: Read, Edit, Write, Bash, Grep
---

# Query Optimization Skill

This skill helps you optimize database queries using Drizzle ORM and PostgreSQL.

## When to Use This Skill

- Slow database queries
- High database CPU usage
- N+1 query problems
- Missing indexes
- Inefficient query patterns
- Database performance degradation
- Optimizing data access

## Query Performance Goals

- **Simple queries**: < 10ms
- **Complex queries**: < 100ms
- **Aggregations**: < 500ms
- **Full-text search**: < 1s

## Identifying Slow Queries

### Query Logging

```typescript
// packages/database/src/logger.ts
import { log } from "@sgcarstrends/utils/logger";

export const logQuery = (sql: string, params: unknown[], duration: number) => {
  log.info("Query executed", {
    sql: sql.substring(0, 200),  // First 200 chars
    params: params.slice(0, 5),  // First 5 params
    duration: Math.round(duration),
  });

  if (duration > 100) {
    log.warn("Slow query detected", {
      sql: sql.substring(0, 200),
      duration: Math.round(duration),
    });
  }
};
```

### PostgreSQL Logging

```sql
-- Enable slow query logging
ALTER DATABASE sgcarstrends SET log_min_duration_statement = 100;

-- View slow queries
SELECT
  query,
  calls,
  total_time,
  mean_time,
  max_time,
  stddev_time
FROM pg_stat_statements
WHERE mean_time > 100
ORDER BY mean_time DESC
LIMIT 20;
```

## Common Query Issues

### 1. N+1 Query Problem

```typescript
// ❌ N+1 queries (slow)
const posts = await db.query.posts.findMany();
for (const post of posts) {
  // This executes a query for EACH post
  post.author = await db.query.users.findFirst({
    where: eq(users.id, post.authorId),
  });
}

// ✅ Single query with join (fast)
const posts = await db.query.posts.findMany({
  with: {
    author: true,
  },
});

// ✅ Or use dataloader pattern
import DataLoader from "dataloader";

const userLoader = new DataLoader(async (ids: string[]) => {
  const users = await db.query.users.findMany({
    where: inArray(users.id, ids),
  });
  return ids.map((id) => users.find((u) => u.id === id));
});

const posts = await db.query.posts.findMany();
const postsWithAuthors = await Promise.all(
  posts.map(async (post) => ({
    ...post,
    author: await userLoader.load(post.authorId),
  }))
);
```

### 2. Missing Indexes

```typescript
// packages/database/src/schema/cars.ts
import { pgTable, text, integer, index } from "drizzle-orm/pg-core";

export const cars = pgTable(
  "cars",
  {
    id: text("id").primaryKey(),
    make: text("make").notNull(),
    model: text("model").notNull(),
    month: text("month").notNull(),
    number: integer("number").default(0).notNull(),
  },
  (table) => ({
    // ✅ Add indexes for frequently queried columns
    makeIdx: index("cars_make_idx").on(table.make),
    monthIdx: index("cars_month_idx").on(table.month),
    makeMonthIdx: index("cars_make_month_idx").on(table.make, table.month),
  })
);
```

### 3. Selecting Unnecessary Columns

```typescript
// ❌ Select all columns (wasteful)
const users = await db.query.users.findMany();

// ✅ Select only needed columns
const users = await db
  .select({
    id: users.id,
    name: users.name,
    email: users.email,
  })
  .from(users);

// ✅ Or use Drizzle's columns parameter
const users = await db.query.users.findMany({
  columns: {
    id: true,
    name: true,
    email: true,
  },
});
```

### 4. Fetching Too Much Data

```typescript
// ❌ Load all records (memory intensive)
const allCars = await db.query.cars.findMany();

// ✅ Use pagination
const cars = await db.query.cars.findMany({
  limit: 20,
  offset: (page - 1) * 20,
});

// ✅ Or cursor-based pagination
const cars = await db.query.cars.findMany({
  where: cursor ? gt(cars.id, cursor) : undefined,
  limit: 20,
  orderBy: [asc(cars.id)],
});
```

## Query Optimization Techniques

### 1. Use Indexes

```typescript
// Create index migration
// packages/database/migrations/0001_add_indexes.sql
CREATE INDEX CONCURRENTLY IF NOT EXISTS cars_make_idx ON cars (make);
CREATE INDEX CONCURRENTLY IF NOT EXISTS cars_month_idx ON cars (month);
CREATE INDEX CONCURRENTLY IF NOT EXISTS cars_make_month_idx ON cars (make, month);

-- Verify index usage
EXPLAIN ANALYZE
SELECT * FROM cars WHERE make = 'Toyota' AND month = '2024-01';

-- Should show: Index Scan using cars_make_month_idx
```

### 2. Optimize WHERE Clauses

```typescript
// ❌ Non-sargable query (can't use index)
const cars = await db
  .select()
  .from(cars)
  .where(sql`LOWER(make) = 'toyota'`);

// ✅ Sargable query (can use index)
const cars = await db.query.cars.findMany({
  where: eq(cars.make, "Toyota"),
});

// ✅ Or create functional index
// CREATE INDEX cars_make_lower_idx ON cars (LOWER(make));
```

### 3. Use Joins Instead of Subqueries

```typescript
// ❌ Subquery (slower)
const posts = await db
  .select()
  .from(posts)
  .where(
    inArray(
      posts.authorId,
      db.select({ id: users.id }).from(users).where(eq(users.role, "admin"))
    )
  );

// ✅ Join (faster)
const posts = await db
  .select({
    id: posts.id,
    title: posts.title,
    authorName: users.name,
  })
  .from(posts)
  .innerJoin(users, eq(posts.authorId, users.id))
  .where(eq(users.role, "admin"));
```

### 4. Batch Operations

```typescript
// ❌ Multiple insert queries
for (const car of cars) {
  await db.insert(cars).values(car);
}

// ✅ Single batch insert
await db.insert(cars).values(cars);

// ✅ Batch with chunks
const chunkSize = 1000;
for (let i = 0; i < cars.length; i += chunkSize) {
  const chunk = cars.slice(i, i + chunkSize);
  await db.insert(cars).values(chunk);
}
```

### 5. Use Database Functions

```typescript
// ❌ Fetch all and count in app
const cars = await db.query.cars.findMany();
const count = cars.length;

// ✅ Count in database
const [{ count }] = await db
  .select({ count: sql<number>`count(*)` })
  .from(cars);

// ✅ Use aggregations
const stats = await db
  .select({
    make: cars.make,
    count: sql<number>`count(*)`,
    avgNumber: sql<number>`avg(${cars.number})`,
    maxNumber: sql<number>`max(${cars.number})`,
  })
  .from(cars)
  .groupBy(cars.make);
```

## Query Analysis

### EXPLAIN ANALYZE

```sql
-- Analyze query execution
EXPLAIN ANALYZE
SELECT c.*, u.name as author_name
FROM posts c
INNER JOIN users u ON c.author_id = u.id
WHERE c.published_at > NOW() - INTERVAL '7 days'
ORDER BY c.published_at DESC
LIMIT 20;

-- Key metrics to check:
-- - Planning Time: Time to plan query
-- - Execution Time: Time to execute query
-- - Rows: Estimated vs actual rows
-- - Cost: Query cost estimate
-- - Buffers: Shared hits (cache) vs reads (disk)

-- Look for:
-- - Seq Scan (bad - full table scan)
-- - Index Scan (good - using index)
-- - Nested Loop (can be slow for large datasets)
-- - Hash Join (better for large datasets)
```

### Query Statistics

```sql
-- View query statistics
SELECT
  query,
  calls,
  total_time,
  mean_time,
  stddev_time,
  rows
FROM pg_stat_statements
WHERE query LIKE '%cars%'
ORDER BY mean_time DESC
LIMIT 10;

-- Reset statistics
SELECT pg_stat_statements_reset();
```

## Caching Strategies

### Application-Level Caching

```typescript
// apps/api/src/services/cars.ts
import { redis } from "@sgcarstrends/utils";

export const getCarsByMake = async (make: string) => {
  const cacheKey = `cars:make:${make}`;

  // Check cache
  const cached = await redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached as string);
  }

  // Query database
  const cars = await db.query.cars.findMany({
    where: eq(cars.make, make),
  });

  // Cache for 1 hour
  await redis.set(cacheKey, JSON.stringify(cars), { ex: 3600 });

  return cars;
};
```

### Query Result Caching

```typescript
// Memoize expensive queries
import memoize from "memoizee";

const getCarStats = memoize(
  async (month: string) => {
    return await db
      .select({
        make: cars.make,
        count: sql<number>`count(*)`,
        total: sql<number>`sum(${cars.number})`,
      })
      .from(cars)
      .where(eq(cars.month, month))
      .groupBy(cars.make);
  },
  {
    maxAge: 60000,  // Cache for 1 minute
    promise: true,
  }
);
```

## Connection Pooling

### Optimize Pool Settings

```typescript
// packages/database/src/client.ts
import { drizzle } from "drizzle-orm/postgres-js";
import postgres from "postgres";

const client = postgres(process.env.DATABASE_URL!, {
  max: 20,  // Maximum pool size
  idle_timeout: 20,  // Close idle connections after 20s
  connect_timeout: 10,  // Connection timeout
  prepare: true,  // Use prepared statements
});

export const db = drizzle(client);
```

### Monitor Connections

```sql
-- View active connections
SELECT
  pid,
  usename,
  application_name,
  client_addr,
  state,
  query,
  query_start
FROM pg_stat_activity
WHERE datname = 'sgcarstrends';

-- Check connection pool usage
SELECT
  count(*) as total_connections,
  sum(CASE WHEN state = 'active' THEN 1 ELSE 0 END) as active,
  sum(CASE WHEN state = 'idle' THEN 1 ELSE 0 END) as idle
FROM pg_stat_activity
WHERE datname = 'sgcarstrends';
```

## Materialized Views

### Create Materialized View

```sql
-- Create materialized view for expensive aggregation
CREATE MATERIALIZED VIEW car_stats_by_month AS
SELECT
  month,
  make,
  COUNT(*) as model_count,
  SUM(number) as total_registrations,
  AVG(number) as avg_registrations
FROM cars
GROUP BY month, make;

-- Create index on materialized view
CREATE INDEX car_stats_month_idx ON car_stats_by_month (month);

-- Refresh materialized view
REFRESH MATERIALIZED VIEW car_stats_by_month;

-- Use in queries
SELECT * FROM car_stats_by_month
WHERE month = '2024-01'
ORDER BY total_registrations DESC;
```

### Auto-Refresh with Cron

```sql
-- Schedule refresh every hour
SELECT cron.schedule(
  'refresh-car-stats',
  '0 * * * *',
  'REFRESH MATERIALIZED VIEW CONCURRENTLY car_stats_by_month'
);
```

## Query Optimization Checklist

- [ ] Add indexes for WHERE, JOIN, ORDER BY columns
- [ ] Avoid N+1 queries (use joins or dataloader)
- [ ] Select only needed columns
- [ ] Use pagination for large datasets
- [ ] Batch insert/update operations
- [ ] Use database aggregations
- [ ] Enable query caching
- [ ] Monitor query performance
- [ ] Use EXPLAIN ANALYZE to find bottlenecks
- [ ] Optimize connection pool settings

## Best Practices

### 1. Always Use Indexes

```typescript
// ✅ Good: Add indexes for frequently queried columns
export const cars = pgTable(
  "cars",
  {
    make: text("make").notNull(),
    month: text("month").notNull(),
    // ...
  },
  (table) => ({
    makeIdx: index("cars_make_idx").on(table.make),
    monthIdx: index("cars_month_idx").on(table.month),
  })
);
```

### 2. Avoid SELECT *

```typescript
// ❌ Fetches all columns
const users = await db.select().from(users);

// ✅ Select only what you need
const users = await db
  .select({
    id: users.id,
    name: users.name,
  })
  .from(users);
```

### 3. Use Transactions

```typescript
// ✅ Use transactions for multiple operations
await db.transaction(async (tx) => {
  await tx.insert(posts).values(post);
  await tx.update(users).set({ postCount: sql`post_count + 1` });
});
```

### 4. Monitor Query Performance

```typescript
// ✅ Log slow queries
const start = performance.now();
const result = await db.query.cars.findMany();
const duration = performance.now() - start;

if (duration > 100) {
  log.warn("Slow query", { duration, query: "cars.findMany" });
}
```

## Troubleshooting

### Query Timeout

```sql
-- Increase statement timeout
SET statement_timeout = '30s';

-- Or in connection string
postgresql://user:pass@host/db?options=-c%20statement_timeout=30s
```

### Lock Contention

```sql
-- View locks
SELECT
  locktype,
  relation::regclass,
  mode,
  granted,
  pid
FROM pg_locks
WHERE NOT granted;

-- Kill blocking query
SELECT pg_terminate_backend(pid);
```

### High CPU Usage

```sql
-- Find expensive queries
SELECT
  query,
  calls,
  total_time,
  mean_time,
  max_time
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;

-- Optimize or add indexes
```

## References

- PostgreSQL Performance: https://www.postgresql.org/docs/current/performance-tips.html
- Drizzle ORM: https://orm.drizzle.team/docs/overview
- Query Optimization: https://use-the-index-luke.com
- Related files:
  - `packages/database/src/schema/` - Schema definitions
  - Root CLAUDE.md - Database guidelines

## Best Practices Summary

1. **Index Everything**: Add indexes for frequently queried columns
2. **Avoid N+1**: Use joins or batch loading
3. **Select Wisely**: Only fetch needed columns
4. **Paginate**: Don't fetch all records at once
5. **Use Prepared Statements**: Enable prepared statements in driver
6. **Monitor Performance**: Track query times and optimize slow ones
7. **Cache Results**: Cache expensive queries
8. **Use Database Features**: Leverage aggregations, functions, materialized views
