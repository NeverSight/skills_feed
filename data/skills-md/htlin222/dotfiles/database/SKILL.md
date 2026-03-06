---
name: database
description: Database optimization, query tuning, migrations, and administration. Use for database performance issues, schema design, or operational tasks.
---

# Database Management

Optimize queries, manage schemas, and ensure reliability.

## When to Use

- Slow query optimization
- Schema design and migrations
- Index strategy
- Database operations
- Performance tuning

## Query Optimization

### Analyze Queries

```sql
-- PostgreSQL
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM orders WHERE user_id = 123;

-- MySQL
EXPLAIN ANALYZE
SELECT * FROM orders WHERE user_id = 123;
```

### Common Optimizations

```sql
-- Add missing index
CREATE INDEX CONCURRENTLY idx_orders_user_id
ON orders(user_id);

-- Composite index for common queries
CREATE INDEX idx_orders_user_date
ON orders(user_id, created_at DESC);

-- Partial index for filtered queries
CREATE INDEX idx_active_orders
ON orders(user_id) WHERE status = 'active';

-- Cover index to avoid table lookup
CREATE INDEX idx_orders_covering
ON orders(user_id) INCLUDE (total, status);
```

## Migration Best Practices

```sql
-- Safe column addition (no lock)
ALTER TABLE users ADD COLUMN preferences JSONB;

-- Safe column rename (use view for compatibility)
ALTER TABLE users RENAME COLUMN name TO full_name;
CREATE VIEW users_compat AS
  SELECT *, full_name as name FROM users;

-- Safe index creation
CREATE INDEX CONCURRENTLY idx_new ON table(column);

-- Backfill in batches
UPDATE users SET new_col = compute(old_col)
WHERE id BETWEEN 1 AND 10000;
-- Repeat for next batch
```

## Operational Queries

### Health Checks

```sql
-- Active connections (PostgreSQL)
SELECT state, count(*)
FROM pg_stat_activity
GROUP BY state;

-- Long running queries
SELECT pid, now() - query_start as duration, query
FROM pg_stat_activity
WHERE state = 'active' AND now() - query_start > '5 minutes'::interval;

-- Table sizes
SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC
LIMIT 10;

-- Index usage
SELECT indexrelname, idx_scan, idx_tup_read
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

### Maintenance

```sql
-- PostgreSQL vacuum and analyze
VACUUM ANALYZE table_name;

-- Reindex
REINDEX INDEX CONCURRENTLY idx_name;

-- Kill long query
SELECT pg_terminate_backend(pid);
```

## Caching Strategy

```python
import redis

cache = redis.Redis()

def get_user(user_id: int) -> dict:
    # Try cache first
    cached = cache.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)

    # Query database
    user = db.query("SELECT * FROM users WHERE id = %s", user_id)

    # Cache with TTL
    cache.setex(f"user:{user_id}", 3600, json.dumps(user))
    return user

def invalidate_user(user_id: int):
    cache.delete(f"user:{user_id}")
```

## Examples

**Input:** "This query is slow"
**Action:** Run EXPLAIN, identify missing index or bad plan, optimize

**Input:** "Set up database backups"
**Action:** Configure pg_dump/mysqldump, set schedule, test restore
