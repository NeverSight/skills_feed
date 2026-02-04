---
name: clickhouse-architect
description: ClickHouse schema design and optimization. TRIGGERS - ClickHouse schema, compression codecs, MergeTree, ORDER BY tuning, partition key.
allowed-tools: Read, Bash, Grep, Skill
---

# ClickHouse Architect

<!-- ADR: 2025-12-09-clickhouse-architect-skill -->

Prescriptive schema design, compression selection, and performance optimization for ClickHouse (v24.4+). Covers both ClickHouse Cloud (SharedMergeTree) and self-hosted (ReplicatedMergeTree) deployments.

## When to Use This Skill

Use this skill when:

- Designing ClickHouse table schemas with ORDER BY key selection
- Selecting compression codecs for column types
- Configuring partition keys for data lifecycle management
- Adding performance accelerators (projections, indexes, dictionaries)
- Auditing and optimizing existing ClickHouse schemas

## Core Methodology

### Schema Design Workflow

Follow this sequence when designing or reviewing ClickHouse schemas:

1. **Define ORDER BY key** (3-5 columns, lowest cardinality first)
2. **Select compression codecs** per column type
3. **Configure PARTITION BY** for data lifecycle management
4. **Add performance accelerators** (projections, indexes)
5. **Validate with audit queries** (see scripts/)
6. **Document with COMMENT statements** (see [`references/schema-documentation.md`](./references/schema-documentation.md))

### ORDER BY Key Selection

The ORDER BY clause is the most critical decision in ClickHouse schema design.

**Rules**:

- Limit to 3-5 columns maximum (each additional column has diminishing returns)
- Place lowest cardinality columns first (e.g., `tenant_id` before `timestamp`)
- Include all columns used in WHERE clauses for range queries
- PRIMARY KEY must be a prefix of ORDER BY (or omit to use full ORDER BY)

**Example**:

```sql
-- Correct: Low cardinality first, 4 columns
CREATE TABLE trades (
    exchange LowCardinality(String),
    symbol LowCardinality(String),
    timestamp DateTime64(3),
    trade_id UInt64,
    price Float64,
    quantity Float64
) ENGINE = MergeTree()
ORDER BY (exchange, symbol, timestamp, trade_id);

-- Wrong: High cardinality first (10x slower queries)
ORDER BY (trade_id, timestamp, symbol, exchange);
```

### Compression Codec Quick Reference

| Column Type              | Default Codec              | Read-Heavy Alternative    | Example                                            |
| ------------------------ | -------------------------- | ------------------------- | -------------------------------------------------- |
| DateTime/DateTime64      | `CODEC(DoubleDelta, ZSTD)` | `CODEC(DoubleDelta, LZ4)` | `timestamp DateTime64(3) CODEC(DoubleDelta, ZSTD)` |
| Float prices/gauges      | `CODEC(Gorilla, ZSTD)`     | `CODEC(Gorilla, LZ4)`     | `price Float64 CODEC(Gorilla, ZSTD)`               |
| Integer counters         | `CODEC(T64, ZSTD)`         | —                         | `count UInt64 CODEC(T64, ZSTD)`                    |
| Slowly changing integers | `CODEC(Delta, ZSTD)`       | `CODEC(Delta, LZ4)`       | `version UInt32 CODEC(Delta, ZSTD)`                |
| String (low cardinality) | `LowCardinality(String)`   | —                         | `status LowCardinality(String)`                    |
| General data             | `CODEC(ZSTD(3))`           | `CODEC(LZ4)`              | Default compression level 3                        |

**When to use LZ4 over ZSTD**: LZ4 provides 1.76x faster decompression. Use LZ4 for read-heavy workloads with monotonic sequences (timestamps, counters). Use ZSTD (default) when compression ratio matters or data patterns are unknown.

**Note on codec combinations**:

Delta/DoubleDelta + Gorilla combinations are blocked by default (`allow_suspicious_codecs`) because Gorilla already performs implicit delta compression internally—combining them is **redundant**, not dangerous. A historical corruption bug (PR #45615, Jan 2023) was fixed, but the blocking remains as a best practice guardrail.

Use each codec family independently for its intended data type:

```sql
-- Correct usage
price Float64 CODEC(Gorilla, ZSTD)              -- Floats: use Gorilla
timestamp DateTime64 CODEC(DoubleDelta, ZSTD)   -- Timestamps: use DoubleDelta
timestamp DateTime64 CODEC(DoubleDelta, LZ4)    -- Read-heavy: use LZ4
```

### PARTITION BY Guidelines

PARTITION BY is for **data lifecycle management**, NOT query optimization.

**Rules**:

- Partition by time units (month, week) for TTL and data management
- Keep partition count under 1000 total across all tables
- Each partition should contain 1-300 parts maximum
- Never partition by high-cardinality columns

**Example**:

```sql
-- Correct: Monthly partitions for TTL management
PARTITION BY toYYYYMM(timestamp)

-- Wrong: Daily partitions (too many parts)
PARTITION BY toYYYYMMDD(timestamp)

-- Wrong: High-cardinality partition key
PARTITION BY user_id
```

### Anti-Patterns Checklist (v24.4+)

| Pattern                         | Severity | Modern Status      | Fix                                   |
| ------------------------------- | -------- | ------------------ | ------------------------------------- |
| Too many parts (>300/partition) | Critical | Still critical     | Reduce partition granularity          |
| Small batch inserts (<1000)     | Critical | Still critical     | Batch to 10k-100k rows                |
| High-cardinality first ORDER BY | Critical | Still critical     | Reorder: lowest cardinality first     |
| No memory limits                | High     | Still critical     | Set `max_memory_usage`                |
| Denormalization overuse         | High     | Still critical     | Use dictionaries + materialized views |
| Large JOINs                     | Medium   | **180x improved**  | Still avoid for ultra-low-latency     |
| Mutations (UPDATE/DELETE)       | Medium   | **1700x improved** | Use lightweight updates (v24.4+)      |

### Table Engine Selection

| Deployment          | Engine                | Use Case                        |
| ------------------- | --------------------- | ------------------------------- |
| ClickHouse Cloud    | `SharedMergeTree`     | Default for cloud deployments   |
| Self-hosted cluster | `ReplicatedMergeTree` | Multi-node with replication     |
| Self-hosted single  | `MergeTree`           | Single-node development/testing |

**Cloud (SharedMergeTree)**:

```sql
CREATE TABLE trades (...)
ENGINE = SharedMergeTree('/clickhouse/tables/{shard}/trades', '{replica}')
ORDER BY (exchange, symbol, timestamp);
```

**Self-hosted (ReplicatedMergeTree)**:

```sql
CREATE TABLE trades (...)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/trades', '{replica}')
ORDER BY (exchange, symbol, timestamp);
```

## Skill Delegation Guide

<!-- ADR: 2025-12-10-clickhouse-skill-delegation -->

This skill is the **hub** for ClickHouse-related tasks. When the user's needs extend beyond schema design, invoke the related skills below.

### Delegation Decision Matrix

| User Need                                       | Invoke Skill                               | Trigger Phrases                                      |
| ----------------------------------------------- | ------------------------------------------ | ---------------------------------------------------- |
| Create database users, manage permissions       | `devops-tools:clickhouse-cloud-management` | "create user", "GRANT", "permissions", "credentials" |
| Configure DBeaver, generate connection JSON     | `devops-tools:clickhouse-pydantic-config`  | "DBeaver", "client config", "connection setup"       |
| Validate schema contracts against live database | `quality-tools:schema-e2e-validation`      | "validate schema", "Earthly E2E", "schema contract"  |

### Typical Workflow Sequence

1. **Schema Design** (THIS SKILL) → Design ORDER BY, compression, partitioning
2. **User Setup** → `clickhouse-cloud-management` (if cloud credentials needed)
3. **Client Config** → `clickhouse-pydantic-config` (generate DBeaver JSON)
4. **Validation** → `schema-e2e-validation` (CI/CD schema contracts)

### Example: Full Stack Request

**User**: "I need to design a trades table for ClickHouse Cloud and set up DBeaver to query it."

**Expected behavior**:

1. Use THIS skill for schema design
2. Invoke `clickhouse-cloud-management` for creating database user
3. Invoke `clickhouse-pydantic-config` for DBeaver configuration

## Performance Accelerators

### Projections

Create alternative sort orders that ClickHouse automatically selects:

```sql
ALTER TABLE trades ADD PROJECTION trades_by_symbol (
    SELECT * ORDER BY symbol, timestamp
);
ALTER TABLE trades MATERIALIZE PROJECTION trades_by_symbol;
```

### Materialized Views

Pre-compute aggregations for dashboard queries:

```sql
CREATE MATERIALIZED VIEW trades_hourly_mv
ENGINE = SummingMergeTree()
ORDER BY (exchange, symbol, hour)
AS SELECT
    exchange,
    symbol,
    toStartOfHour(timestamp) AS hour,
    sum(quantity) AS total_volume,
    count() AS trade_count
FROM trades
GROUP BY exchange, symbol, hour;
```

### Dictionaries

Replace JOINs with O(1) dictionary lookups for **large-scale star schemas**:

**When to use dictionaries (v24.4+)**:

- Fact tables with 100M+ rows joining dimension tables
- Dimension tables 1k-500k rows with monotonic keys
- LEFT ANY JOIN semantics required

**When JOINs are sufficient (v24.4+)**:

- Dimension tables <500 rows (JOIN overhead negligible)
- v24.4+ predicate pushdown provides 8-180x improvements
- Complex JOIN types (FULL, RIGHT, multi-condition)

**Benchmark context**: 6.6x speedup measured on Star Schema Benchmark (1.4B rows).

```sql
CREATE DICTIONARY symbol_info (
    symbol String,
    name String,
    sector String
)
PRIMARY KEY symbol
SOURCE(CLICKHOUSE(TABLE 'symbols'))
LAYOUT(FLAT())  -- Best for <500k entries with monotonic keys
LIFETIME(3600);

-- Use in queries (O(1) lookup)
SELECT
    symbol,
    dictGet('symbol_info', 'name', symbol) AS symbol_name
FROM trades;
```

## Scripts

Execute comprehensive schema audit:

```bash
clickhouse-client --multiquery < scripts/schema-audit.sql
```

The audit script checks:

- Part count per partition (threshold: 300)
- Compression ratios by column
- Query performance patterns
- Replication lag (if applicable)
- Memory usage patterns

## Additional Resources

### Reference Files

| Reference                                                                                  | Content                                        |
| ------------------------------------------------------------------------------------------ | ---------------------------------------------- |
| [`references/schema-design-workflow.md`](./references/schema-design-workflow.md)           | Complete workflow with examples                |
| [`references/compression-codec-selection.md`](./references/compression-codec-selection.md) | Decision tree + benchmarks                     |
| [`references/anti-patterns-and-fixes.md`](./references/anti-patterns-and-fixes.md)         | 13 deadly sins + v24.4+ status                 |
| [`references/audit-and-diagnostics.md`](./references/audit-and-diagnostics.md)             | Query interpretation guide                     |
| [`references/idiomatic-architecture.md`](./references/idiomatic-architecture.md)           | Parameterized views, dictionaries, dedup       |
| [`references/schema-documentation.md`](./references/schema-documentation.md)               | COMMENT patterns + naming for AI understanding |
| [`references/cache-schema-evolution.md`](./references/cache-schema-evolution.md)           | Cache invalidation + schema evolution patterns |

### External Documentation

- [ClickHouse Best Practices](https://clickhouse.com/docs/best-practices)
- [Altinity Knowledge Base](https://kb.altinity.com/)
- [ClickHouse Blog](https://clickhouse.com/blog)

## Python Driver Policy

<!-- ADR: 2025-12-10-clickhouse-python-driver-policy -->

**Use `clickhouse-connect` (official) for all Python integrations.**

```python
# ✅ RECOMMENDED: clickhouse-connect (official, HTTP)
import clickhouse_connect

client = clickhouse_connect.get_client(
    host='localhost',
    port=8123,  # HTTP port
    username='default',
    password=''
)
result = client.query("SELECT * FROM trades LIMIT 1000")
df = client.query_df("SELECT * FROM trades")  # Pandas integration
```

### Why NOT `clickhouse-driver`

| Factor          | clickhouse-connect | clickhouse-driver   |
| --------------- | ------------------ | ------------------- |
| Maintainer      | ClickHouse Inc.    | Solo developer      |
| Weekly commits  | Yes (active)       | Sparse (months)     |
| Open issues     | 41 (addressed)     | 76 (accumulating)   |
| Downloads/week  | 2.7M               | 1.5M                |
| Bus factor risk | Low (company)      | **High (1 person)** |

**Do NOT use `clickhouse-driver`** despite its ~26% speed advantage for large exports. The maintenance risk outweighs performance gains:

- Single maintainer (mymarilyn) with no succession plan
- Issues accumulating without response
- Risk of abandonment breaks production code

**Exception**: Only consider `clickhouse-driver` if you have extreme performance requirements (exporting millions of rows) AND accept the maintenance risk.

## Related Skills

| Skill                                      | Purpose                       |
| ------------------------------------------ | ----------------------------- |
| `devops-tools:clickhouse-cloud-management` | User/permission management    |
| `devops-tools:clickhouse-pydantic-config`  | DBeaver connection generation |
| `quality-tools:schema-e2e-validation`      | YAML schema contracts         |
| `quality-tools:multi-agent-e2e-validation` | Database migration validation |

---

## Troubleshooting

| Issue                        | Cause                          | Solution                                         |
| ---------------------------- | ------------------------------ | ------------------------------------------------ |
| Too many parts               | Over-partitioned               | Reduce partition granularity (monthly not daily) |
| Slow queries                 | Wrong ORDER BY order           | Put lowest cardinality columns first             |
| High memory usage            | No memory limits set           | Configure max_memory_usage setting               |
| Codec error on Delta+Gorilla | Suspicious codec combination   | Use each codec family independently              |
| Projection not used          | Optimizer chose different plan | Check EXPLAIN to verify projection selection     |
| Dictionary stale             | Lifetime expired               | Increase LIFETIME or trigger refresh             |
| Replication lag              | Part merges falling behind     | Check merge_tree settings, add resources         |
| INSERT too slow              | Small batch sizes              | Batch to 10k-100k rows per INSERT                |
