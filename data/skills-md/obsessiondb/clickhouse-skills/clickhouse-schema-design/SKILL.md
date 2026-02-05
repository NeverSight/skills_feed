---
name: clickhouse-schema-design
description: "15+ schema rules for ClickHouse tables. ALWAYS LOAD when creating or modifying tables. Achieves sub-second queries, 10x compression, and automated data lifecycle."
---

# ClickHouse Schema Design

**ALWAYS LOAD** when creating or modifying ClickHouse tables.

## Goals

- Sub-second query response on billion-row tables
- 10x+ compression ratios vs raw data
- Zero-maintenance data retention and tiered storage
- Queries that scan <1% of data instead of full table scans

## Reference Documentation

- [MergeTree Engine](https://clickhouse.com/docs/engines/table-engines/mergetree-family/mergetree)
- [Primary Keys and Indexes](https://clickhouse.com/docs/optimize/sparse-primary-indexes)
- [Data Types](https://clickhouse.com/docs/sql-reference/data-types)
- [TTL](https://clickhouse.com/docs/sql-reference/statements/alter/ttl)
- [Altinity: Pick Keys Guide](https://kb.altinity.com/engines/mergetree-table-engine-family/pick-keys/)

**Search terms:** schema design, ORDER BY, PRIMARY KEY, PARTITION BY, data types, TTL, index_granularity

## Critical Rules

### [CRITICAL]

1. **ORDER BY determines query performance.** Put most-filtered columns first, low cardinality before high.
2. **PARTITION BY is for data management, not query speed.** Use ORDER BY to speed up queries.
3. **Use smallest data types possible.** UInt32 not UInt64 if values fit.

### [HIGH]

4. **LowCardinality for strings with <10K unique values.** Saves storage and speeds queries.
5. **Avoid Nullable when possible.** Use DEFAULT values instead.
6. **PRIMARY KEY can be a prefix of ORDER BY.** Reduces index size.

### [MEDIUM]

7. **3-5 columns in ORDER BY is typical.** More columns rarely help, fewer may miss optimization opportunities.

## Engine Selection

| Engine                 | Use Case                            | Key Behavior                                                |
| ---------------------- | ----------------------------------- | ----------------------------------------------------------- |
| `MergeTree`            | Append-only data (events, logs)     | Standard storage, no special merge logic                    |
| `ReplacingMergeTree`   | Deduplication, upserts              | Keeps latest row per ORDER BY key; query with `argMax` pattern |
| `SummingMergeTree`     | Pre-aggregated counters             | Automatically sums numeric columns on merge                 |
| `AggregatingMergeTree` | Complex aggregates (uniq, quantile) | Stores intermediate states; use `-State`/`-Merge` functions |
| `CollapsingMergeTree`  | Mutable rows                        | Uses +1/-1 sign column to cancel/update rows                |

**For engine examples and Materialized Views, see `clickhouse-materialized-views` skill.**

## ORDER BY Selection

### The 3-5 Column Rule

```sql
ORDER BY (
    tenant_id,      -- 1. Lowest cardinality, most filtered
    event_date,     -- 2. Time component (common filter)
    user_id,        -- 3. Medium cardinality
    event_type      -- 4. Higher cardinality (optional)
)
```

### Decision Process

1. **Which columns appear in WHERE clauses?** - These go first
2. **What's the cardinality?** - Lower cardinality columns before higher
3. **Is there a time dimension?** - Usually included for range queries

### Good vs Bad

```sql
-- BAD: High cardinality first, rarely-filtered columns
ORDER BY (user_id, timestamp, tenant_id)

-- GOOD: Low cardinality first, commonly-filtered columns
ORDER BY (tenant_id, toDate(timestamp), user_id)
```

### PRIMARY KEY as Prefix

```sql
-- Full sorting key for data layout
ORDER BY (tenant_id, event_date, user_id, event_type)

-- Shorter primary key for smaller index (optional)
PRIMARY KEY (tenant_id, event_date)
```

## PARTITION BY Guidelines

### Size Targets

| Scenario                              | Target Partition Size |
| ------------------------------------- | --------------------- |
| General MergeTree tables              | 1-300 GB              |
| SummingMergeTree / ReplacingMergeTree | 400 MB - 40 GB        |
| Small tables (<5 GB total)            | No partitioning       |

### Common Patterns

```sql
-- Monthly (most common for analytics)
PARTITION BY toYYYYMM(event_date)

-- Daily (high volume, >1TB/month)
PARTITION BY toDate(event_date)

-- Multi-tenant with time
PARTITION BY (tenant_id, toYYYYMM(event_date))

-- No partitioning (small tables)
-- Simply omit PARTITION BY clause
```

### Anti-Pattern

```sql
-- BAD: Over-partitioning creates thousands of small parts
PARTITION BY (toDate(event_date), user_id)

-- BAD: Partitioning by high-cardinality column
PARTITION BY user_id
```

## Data Type Optimization

### Numbers

```sql
-- Use smallest type that fits your data
count UInt16,           -- Max 65,535 (instead of UInt64)
percentage Float32,     -- Instead of Float64 if 6-7 digits precision is enough
flags UInt8,            -- For small integers, booleans
```

### Strings

```sql
-- LowCardinality for <10K unique values
country LowCardinality(String),
status LowCardinality(String),
event_type LowCardinality(String),

-- Regular String for high cardinality
user_agent String,
url String,
```

### Dates and Times

```sql
-- Use simplest type that meets requirements
event_date Date,                    -- If you only need date
event_time DateTime,                -- If you need seconds
event_time_precise DateTime64(3),   -- Only if you need milliseconds
```

### Avoiding Nullable

```sql
-- BAD: Nullable adds overhead and complexity
user_id Nullable(UInt64),

-- GOOD: Use DEFAULT for missing values
user_id UInt64 DEFAULT 0,

-- GOOD: Use empty string for missing text
name String DEFAULT '',
```

## TTL Configuration

### Delete Old Data

```sql
CREATE TABLE events (
    event_date Date,
    ...
) ENGINE = MergeTree()
ORDER BY (...)
TTL event_date + INTERVAL 90 DAY DELETE;
```

### Tiered Storage

```sql
CREATE TABLE events (
    event_date Date,
    ...
) ENGINE = MergeTree()
ORDER BY (...)
TTL
    event_date + INTERVAL 7 DAY TO VOLUME 'hot',
    event_date + INTERVAL 30 DAY TO VOLUME 'warm',
    event_date + INTERVAL 365 DAY DELETE;
```

### Column-Level TTL

```sql
CREATE TABLE events (
    event_date Date,
    user_id UInt64,
    -- Delete PII after 30 days, keep aggregated data
    email String TTL event_date + INTERVAL 30 DAY,
    ip_address String TTL event_date + INTERVAL 30 DAY
) ENGINE = MergeTree()
ORDER BY (event_date, user_id);
```

## Complete Example

```sql
CREATE TABLE analytics_events (
    -- Time dimension
    event_date Date,
    event_time DateTime,

    -- Identifiers (low to high cardinality)
    tenant_id UInt32,
    user_id UInt64,
    session_id String,

    -- Categorical data (use LowCardinality)
    event_type LowCardinality(String),
    country LowCardinality(String),
    device_type LowCardinality(String),

    -- Metrics
    duration_ms UInt32,

    -- Flexible data
    properties String,  -- JSON as string

    -- Skip indices for secondary lookups
    INDEX idx_user user_id TYPE bloom_filter(0.01) GRANULARITY 3,
    INDEX idx_session session_id TYPE bloom_filter(0.01) GRANULARITY 3
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(event_date)
ORDER BY (tenant_id, event_date, user_id)
TTL event_date + INTERVAL 12 MONTH DELETE
SETTINGS index_granularity = 8192;
```

## Anti-Patterns

| Anti-Pattern                               | Problem                            | Solution                               |
| ------------------------------------------ | ---------------------------------- | -------------------------------------- |
| `ORDER BY (uuid, timestamp)`               | High cardinality first             | Put low cardinality columns first      |
| `PARTITION BY toDate(ts)` for small tables | Too many small partitions          | Omit partitioning or use monthly       |
| `Nullable(UInt64)` everywhere              | Storage and query overhead         | Use DEFAULT values                     |
| `String` for status codes                  | Wastes space                       | Use `LowCardinality(String)` or `Enum` |
| `DateTime64(9)` always                     | Nanosecond precision rarely needed | Use `DateTime` or `DateTime64(3)`      |
| Putting timestamp first in ORDER BY        | Poor compression and filtering     | Put categorical columns first          |

## Verification Queries

```sql
-- Check table size and compression
SELECT
    table,
    formatReadableSize(sum(bytes_on_disk)) AS size,
    sum(rows) AS rows,
    round(sum(bytes_on_disk) / sum(rows), 2) AS bytes_per_row
FROM system.parts
WHERE active AND database = 'default'
GROUP BY table;

-- Check partition sizes
SELECT
    partition,
    count() AS parts,
    sum(rows) AS rows,
    formatReadableSize(sum(bytes_on_disk)) AS size
FROM system.parts
WHERE active AND table = 'your_table'
GROUP BY partition
ORDER BY partition;

-- Verify column types
SELECT name, type, compression_codec
FROM system.columns
WHERE database = 'default' AND table = 'your_table';
```

## Troubleshooting

**Always ask for user confirmation before applying schema changes (ALTER TABLE, recreating tables).**

### "Too Many Parts" Error

**Problem:** `DB::Exception: Too many parts`, inserts rejected, merge queue growing

**Diagnose:**

```sql
SELECT table, partition, count() AS parts
FROM system.parts
WHERE active AND database = 'default'
GROUP BY table, partition
HAVING parts > 300
ORDER BY parts DESC;
```

**Solutions:**

| Cause | Fix |
|-------|-----|
| Over-partitioning (daily + high cardinality) | Use monthly partitions: `PARTITION BY toYYYYMM(date)` |
| Too many small inserts | Batch inserts: 1000+ rows per INSERT |
| High-cardinality partition key | Remove high-cardinality columns from PARTITION BY |

```sql
-- Fix: Change from daily to monthly partitioning (requires table recreation)
CREATE TABLE events_new (...) PARTITION BY toYYYYMM(event_date) ...;
INSERT INTO events_new SELECT * FROM events;
RENAME TABLE events TO events_old, events_new TO events;
DROP TABLE events_old;
```

### Poor Compression (<3x Ratio)

**Problem:** Table using more disk than expected, compression ratio below 3x

**Diagnose:**

```sql
SELECT
    column,
    type,
    formatReadableSize(sum(column_data_compressed_bytes)) AS compressed,
    round(sum(column_data_uncompressed_bytes) / sum(column_data_compressed_bytes), 2) AS ratio
FROM system.parts_columns
WHERE active AND table = 'your_table'
GROUP BY column, type
ORDER BY ratio ASC;
```

**Solutions:**

| Cause | Fix |
|-------|-----|
| High-cardinality column first in ORDER BY | Reorder: low cardinality columns first |
| String for low-cardinality data | Use `LowCardinality(String)` |
| Wrong codec for data pattern | Use DoubleDelta for timestamps, Gorilla for floats |
| Random UUIDs in ORDER BY | Move UUID later in ORDER BY, or use different key |

```sql
-- Check cardinality to decide LowCardinality usage
SELECT uniq(status) FROM events;  -- If <10K, use LowCardinality

-- Fix column type (requires recreation or new column)
ALTER TABLE events ADD COLUMN status_new LowCardinality(String);
ALTER TABLE events UPDATE status_new = status WHERE 1;
-- Then migrate queries to use status_new
```

### Slow Queries Despite Good Schema

**Problem:** Queries slow even with proper ORDER BY and partitioning

**Diagnose:**

```sql
EXPLAIN indexes = 1 SELECT ... FROM your_table WHERE ...;
-- Check: Are granules being skipped? Is partition pruning happening?
```

**Solutions:**

| Cause | Fix |
|-------|-----|
| Query doesn't filter on ORDER BY prefix | Add ORDER BY columns to WHERE clause |
| Function on filter column | Store computed column, filter on that |
| Missing skip index for secondary lookups | Add bloom_filter index |
| Selecting too many columns | Select only needed columns |

```sql
-- Example: Table ORDER BY (tenant_id, event_date, user_id)

-- BAD: Skips ORDER BY prefix
SELECT * FROM events WHERE user_id = 123;

-- GOOD: Include prefix
SELECT * FROM events WHERE tenant_id = 1 AND event_date = today() AND user_id = 123;

-- ALT: Add skip index for direct user_id lookups
ALTER TABLE events ADD INDEX idx_user user_id TYPE bloom_filter(0.01) GRANULARITY 4;
```
