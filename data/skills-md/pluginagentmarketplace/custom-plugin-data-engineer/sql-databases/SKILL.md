---
name: sql-databases
description: SQL query optimization, schema design, indexing strategies, and relational database mastery for production data systems
sasmp_version: "1.3.0"
bonded_agent: 01-data-engineer
bond_type: PRIMARY_BOND
skill_version: "2.0.0"
last_updated: "2025-01"
complexity: foundational
estimated_mastery_hours: 100
prerequisites: [python-programming]
unlocks: [data-warehousing, etl-tools, nosql-databases]
---

# SQL & Relational Databases

Production-grade SQL skills for designing, querying, and optimizing relational databases in data engineering workflows.

## Quick Start

```sql
-- Modern PostgreSQL 16+ query with window functions and CTEs
WITH daily_metrics AS (
    SELECT
        DATE_TRUNC('day', created_at) AS metric_date,
        category,
        COUNT(*) AS event_count,
        SUM(amount) AS total_amount,
        AVG(amount) AS avg_amount
    FROM events
    WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY 1, 2
),
ranked_categories AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY metric_date ORDER BY total_amount DESC) AS daily_rank,
        LAG(total_amount) OVER (PARTITION BY category ORDER BY metric_date) AS prev_day_amount
    FROM daily_metrics
)
SELECT
    metric_date,
    category,
    event_count,
    total_amount,
    ROUND(100.0 * (total_amount - prev_day_amount) / NULLIF(prev_day_amount, 0), 2) AS day_over_day_pct
FROM ranked_categories
WHERE daily_rank <= 5
ORDER BY metric_date DESC, daily_rank;
```

## Core Concepts

### 1. Query Optimization with EXPLAIN ANALYZE

```sql
-- Always analyze before optimizing
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.id, u.email, COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at >= '2024-01-01'
GROUP BY u.id, u.email
HAVING COUNT(o.id) > 10;

-- Reading EXPLAIN output:
-- Seq Scan = Table scan (often slow, needs index)
-- Index Scan = Using index (good)
-- Bitmap Index Scan = Multiple index conditions (acceptable)
-- Hash Join = Building hash table (memory intensive)
-- Nested Loop = Row-by-row join (slow for large tables)
```

### 2. Indexing Strategies

```sql
-- B-tree index (default, most common)
CREATE INDEX idx_users_email ON users(email);

-- Partial index (smaller, faster for specific queries)
CREATE INDEX idx_active_users ON users(created_at)
WHERE status = 'active';

-- Composite index (column order matters!)
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at DESC);

-- Covering index (includes all columns query needs)
CREATE INDEX idx_orders_covering ON orders(user_id)
INCLUDE (total_amount, status);

-- Expression index (for computed values)
CREATE INDEX idx_users_lower_email ON users(LOWER(email));

-- GIN index for JSONB
CREATE INDEX idx_metadata_gin ON events USING GIN(metadata jsonb_path_ops);

-- Check index usage
SELECT
    schemaname, tablename, indexname,
    idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

### 3. Window Functions (2024-2025 Essential)

```sql
-- Running totals and moving averages
SELECT
    order_date,
    amount,
    -- Running total
    SUM(amount) OVER (ORDER BY order_date) AS running_total,
    -- 7-day moving average
    AVG(amount) OVER (
        ORDER BY order_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS moving_avg_7d,
    -- Rank within partition
    RANK() OVER (PARTITION BY customer_id ORDER BY amount DESC) AS customer_rank,
    -- Percent of total within partition
    100.0 * amount / SUM(amount) OVER (PARTITION BY customer_id) AS pct_of_customer_total
FROM orders;

-- Gap and island detection
WITH numbered AS (
    SELECT
        event_date,
        ROW_NUMBER() OVER (ORDER BY event_date) AS rn,
        event_date - (ROW_NUMBER() OVER (ORDER BY event_date) * INTERVAL '1 day') AS grp
    FROM events
)
SELECT
    MIN(event_date) AS streak_start,
    MAX(event_date) AS streak_end,
    COUNT(*) AS streak_length
FROM numbered
GROUP BY grp
ORDER BY streak_start;
```

### 4. Transaction Isolation & ACID

```sql
-- Read Committed (default in PostgreSQL)
BEGIN;
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
-- Sees committed data at query start
COMMIT;

-- Repeatable Read (for consistent snapshots)
BEGIN;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
-- Same query returns same results within transaction
COMMIT;

-- Serializable (strongest, may cause retries)
BEGIN;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- Full isolation, but prepare for serialization failures
COMMIT;

-- Optimistic locking pattern
UPDATE products
SET stock = stock - 1, version = version + 1
WHERE id = $1 AND version = $2;
-- Check rows affected; if 0, concurrent modification occurred
```

### 5. Partitioning for Scale

```sql
-- Range partitioning (time-series data)
CREATE TABLE events (
    id BIGSERIAL,
    event_type TEXT NOT NULL,
    payload JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
) PARTITION BY RANGE (created_at);

-- Create partitions
CREATE TABLE events_2024_q1 PARTITION OF events
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');
CREATE TABLE events_2024_q2 PARTITION OF events
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

-- Auto-partition with pg_partman (production setup)
SELECT partman.create_parent(
    p_parent_table := 'public.events',
    p_control := 'created_at',
    p_type := 'native',
    p_interval := 'monthly',
    p_premake := 3
);

-- List partitioning (categorical data)
CREATE TABLE orders (
    id BIGSERIAL,
    region TEXT NOT NULL,
    total NUMERIC(10,2)
) PARTITION BY LIST (region);

CREATE TABLE orders_us PARTITION OF orders FOR VALUES IN ('US', 'CA');
CREATE TABLE orders_eu PARTITION OF orders FOR VALUES IN ('UK', 'DE', 'FR');
```

## Tools & Technologies

| Tool | Purpose | Version (2025) |
|------|---------|----------------|
| **PostgreSQL** | Primary OLTP database | 16+ |
| **MySQL** | Alternative OLTP | 8.0+ |
| **DBeaver** | Universal SQL client | Latest |
| **pgAdmin** | PostgreSQL admin | 8+ |
| **pgcli** | CLI with autocomplete | Latest |
| **pg_stat_statements** | Query performance | Built-in |
| **pgBouncer** | Connection pooling | 1.21+ |
| **Flyway/Liquibase** | Schema migrations | Latest |

## Learning Path

### Phase 1: Foundations (Weeks 1-2)
```
Week 1: SELECT, WHERE, JOINs, GROUP BY, ORDER BY
Week 2: Aggregations, HAVING, subqueries, UNION
```

### Phase 2: Intermediate (Weeks 3-4)
```
Week 3: Window functions, CTEs, CASE expressions
Week 4: Index fundamentals, EXPLAIN basics
```

### Phase 3: Advanced (Weeks 5-7)
```
Week 5: Query optimization, execution plans
Week 6: Transactions, locking, isolation levels
Week 7: Partitioning, schema design patterns
```

### Phase 4: Production (Weeks 8-10)
```
Week 8: Connection pooling, high availability
Week 9: Migrations, versioning, rollback strategies
Week 10: Monitoring, alerting, performance tuning
```

## Production Patterns

### Schema Design: Star Schema

```sql
-- Fact table (measures, metrics)
CREATE TABLE fact_sales (
    sale_id BIGSERIAL PRIMARY KEY,
    date_key INT NOT NULL REFERENCES dim_date(date_key),
    product_key INT NOT NULL REFERENCES dim_product(product_key),
    customer_key INT NOT NULL REFERENCES dim_customer(customer_key),
    quantity INT NOT NULL,
    unit_price NUMERIC(10,2) NOT NULL,
    total_amount NUMERIC(12,2) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
) PARTITION BY RANGE (date_key);

-- Dimension table (descriptive attributes)
CREATE TABLE dim_product (
    product_key SERIAL PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    subcategory VARCHAR(100),
    -- SCD Type 2 fields
    valid_from DATE NOT NULL DEFAULT CURRENT_DATE,
    valid_to DATE DEFAULT '9999-12-31',
    is_current BOOLEAN DEFAULT TRUE,
    UNIQUE(product_id, valid_from)
);
```

### Slow Query Detection

```sql
-- Enable pg_stat_statements
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Top 10 slowest queries
SELECT
    ROUND((total_exec_time / 1000)::numeric, 2) AS total_secs,
    calls,
    ROUND((mean_exec_time / 1000)::numeric, 4) AS mean_secs,
    ROUND((stddev_exec_time / 1000)::numeric, 4) AS stddev_secs,
    rows,
    query
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;

-- Reset stats after optimization
SELECT pg_stat_statements_reset();
```

### Connection Pooling Configuration

```ini
# pgbouncer.ini
[databases]
mydb = host=localhost port=5432 dbname=mydb

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
auth_type = scram-sha-256
auth_file = /etc/pgbouncer/userlist.txt

# Pool modes:
# session = 1 connection per client session
# transaction = 1 connection per transaction (recommended)
# statement = 1 connection per statement (limited use)
pool_mode = transaction

default_pool_size = 20
max_client_conn = 1000
reserve_pool_size = 5
```

## Troubleshooting Guide

### Common Failure Modes

| Issue | Symptoms | Root Cause | Fix |
|-------|----------|------------|-----|
| **Slow Query** | Query > 1s | Missing index, bad plan | EXPLAIN ANALYZE, add index |
| **Lock Wait** | Queries hang | Long transaction, deadlock | Check `pg_locks`, kill blocking |
| **Connection Exhausted** | "Too many connections" | No pooling, connection leak | Use pgbouncer, fix app |
| **Disk Full** | Write errors | Table bloat, WAL growth | VACUUM FULL, archive WAL |
| **Replication Lag** | Stale reads | Slow replica, network | Check `pg_stat_replication` |

### Debug Checklist

```sql
-- 1. Check active queries
SELECT pid, now() - pg_stat_activity.query_start AS duration, query, state
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY duration DESC;

-- 2. Find blocking queries
SELECT
    blocked.pid AS blocked_pid,
    blocked.query AS blocked_query,
    blocking.pid AS blocking_pid,
    blocking.query AS blocking_query
FROM pg_stat_activity blocked
JOIN pg_locks blocked_locks ON blocked.pid = blocked_locks.pid
JOIN pg_locks blocking_locks ON blocked_locks.locktype = blocking_locks.locktype
    AND blocked_locks.relation = blocking_locks.relation
    AND blocked_locks.pid != blocking_locks.pid
JOIN pg_stat_activity blocking ON blocking_locks.pid = blocking.pid
WHERE NOT blocked_locks.granted;

-- 3. Check table bloat
SELECT
    schemaname, tablename,
    pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename)) AS total_size,
    n_dead_tup AS dead_rows,
    n_live_tup AS live_rows,
    ROUND(100.0 * n_dead_tup / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS dead_pct
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC
LIMIT 10;

-- 4. Check index usage
SELECT
    schemaname, tablename, indexname,
    idx_scan AS times_used,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC  -- Least used first
LIMIT 20;
```

### Kill Long-Running Query

```sql
-- Graceful cancel (SIGINT)
SELECT pg_cancel_backend(pid);

-- Force terminate (SIGTERM)
SELECT pg_terminate_backend(pid);

-- Kill all queries older than 5 minutes
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'active'
  AND query_start < NOW() - INTERVAL '5 minutes'
  AND pid != pg_backend_pid();
```

## Unit Test Template

```python
import pytest
from sqlalchemy import create_engine, text
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="module")
def postgres_container():
    """Spin up real PostgreSQL for integration tests."""
    with PostgresContainer("postgres:16-alpine") as postgres:
        yield postgres

@pytest.fixture
def db_connection(postgres_container):
    """Create connection with transaction rollback."""
    engine = create_engine(postgres_container.get_connection_url())
    with engine.connect() as conn:
        trans = conn.begin()
        yield conn
        trans.rollback()

class TestQueryOptimization:

    def test_index_is_used(self, db_connection):
        # Arrange
        db_connection.execute(text("""
            CREATE TABLE test_users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) NOT NULL
            );
            CREATE INDEX idx_email ON test_users(email);
            INSERT INTO test_users (email)
            SELECT 'user' || i || '@test.com' FROM generate_series(1, 10000) i;
            ANALYZE test_users;
        """))

        # Act
        result = db_connection.execute(text("""
            EXPLAIN (FORMAT JSON)
            SELECT * FROM test_users WHERE email = 'user5000@test.com'
        """)).fetchone()

        plan = result[0][0]

        # Assert
        assert "Index Scan" in str(plan) or "Index Only Scan" in str(plan)

    def test_window_function_correctness(self, db_connection):
        # Arrange
        db_connection.execute(text("""
            CREATE TABLE test_sales (id SERIAL, amount NUMERIC);
            INSERT INTO test_sales (amount) VALUES (100), (200), (300);
        """))

        # Act
        result = db_connection.execute(text("""
            SELECT amount, SUM(amount) OVER (ORDER BY id) AS running_total
            FROM test_sales ORDER BY id
        """)).fetchall()

        # Assert
        assert result[0][1] == 100  # First running total
        assert result[1][1] == 300  # 100 + 200
        assert result[2][1] == 600  # 100 + 200 + 300
```

## Best Practices

### Query Writing
```sql
-- ✅ DO: Use explicit JOINs
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- ❌ DON'T: Use implicit joins
SELECT u.name, o.total
FROM users u, orders o
WHERE u.id = o.user_id;

-- ✅ DO: Use EXISTS for existence checks
SELECT * FROM users u
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id);

-- ❌ DON'T: Use IN with subquery for large datasets
SELECT * FROM users
WHERE id IN (SELECT user_id FROM orders);

-- ✅ DO: Paginate with keyset (cursor)
SELECT * FROM events
WHERE id > $last_seen_id
ORDER BY id
LIMIT 100;

-- ❌ DON'T: Use OFFSET for deep pagination
SELECT * FROM events
ORDER BY id
LIMIT 100 OFFSET 1000000;  -- Slow!
```

### Schema Design
```sql
-- ✅ DO: Use appropriate data types
CREATE TABLE metrics (
    id BIGSERIAL PRIMARY KEY,  -- Use BIGSERIAL for high-volume
    value NUMERIC(10,2),       -- Precise decimal
    created_at TIMESTAMPTZ     -- Always use timezone-aware
);

-- ✅ DO: Add constraints
ALTER TABLE orders
ADD CONSTRAINT chk_positive_amount CHECK (amount > 0);

-- ✅ DO: Use JSONB for flexible schema
CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    event_type TEXT NOT NULL,
    payload JSONB NOT NULL DEFAULT '{}'
);
```

## Resources

### Official Documentation
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [MySQL Reference Manual](https://dev.mysql.com/doc/refman/8.0/en/)
- [SQL Standard](https://modern-sql.com/)

### Performance Tuning
- [Use The Index, Luke](https://use-the-index-luke.com/)
- [PostgreSQL EXPLAIN Visualizer](https://explain.dalibo.com/)
- [pgMustard](https://www.pgmustard.com/)

### Books
- "SQL Performance Explained" by Markus Winand
- "High Performance MySQL" by Schwartz et al.
- "The Art of PostgreSQL" by Dimitri Fontaine

## Next Skills

After mastering SQL databases:
- → `data-warehousing` - Snowflake, BigQuery, dimensional modeling
- → `etl-tools` - Build pipelines with Airflow
- → `nosql-databases` - MongoDB, Redis, DynamoDB
- → `big-data` - Spark SQL at scale

---

**Skill Certification Checklist:**
- [ ] Can write complex queries with CTEs and window functions
- [ ] Can analyze and optimize query performance with EXPLAIN
- [ ] Can design normalized schemas (3NF, BCNF)
- [ ] Can implement partitioning strategies
- [ ] Can configure connection pooling and monitoring
