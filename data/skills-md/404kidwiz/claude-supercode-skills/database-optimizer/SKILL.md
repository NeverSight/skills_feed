---
name: database-optimizer
description: Use when user needs database query optimization, performance tuning, index strategies, execution plan analysis, or scalability across PostgreSQL, MySQL, MongoDB, Redis, and other database systems.
---

# Database Optimizer

## Purpose

Provides expert database performance tuning and optimization across major database systems (PostgreSQL, MySQL, MongoDB, Redis) specializing in query optimization, index design, execution plan analysis, and system configuration. Achieves sub-second query performance and optimal resource utilization through systematic optimization approaches.

## When to Use

- Query execution time exceeds performance targets (>100ms for OLTP, >5s for analytics)
- Database CPU/memory/I/O utilization consistently above 70%
- Application experiencing database connection exhaustion or timeouts
- Slow query log shows problematic patterns or missing indexes
- Database struggling to handle expected load or traffic spikes
- Replication lag exceeding acceptable thresholds (>1s for critical systems)
- Need to optimize database configuration for specific workload (OLTP vs OLAP)
- Planning database capacity or horizontal scaling strategy

## Quick Start

**Invoke this skill when:**
- Slow queries need optimization (EXPLAIN ANALYZE shows issues)
- Index strategy needs design or review
- Database configuration tuning required
- Capacity planning or scaling decisions needed

**Do NOT invoke when:**
- Simple CRUD operations with no performance issues
- Schema design without optimization focus (use database-administrator)
- Application-level caching only (use backend-developer)

## Core Capabilities

### Query Optimization
- Analyzing execution plans and identifying bottlenecks
- Rewriting queries for optimal performance
- Optimizing joins, subqueries, and aggregations
- Implementing query result caching strategies

### Index Design
- Designing appropriate index types (B-tree, GIN, BRIN, hash)
- Creating composite indexes for multi-column queries
- Implementing partial indexes for specific query patterns
- Managing index maintenance and avoiding bloat

### Database Configuration
- Tuning database parameters for specific workloads
- Optimizing memory allocation (buffer pool, cache sizes)
- Configuring connection pooling and concurrency settings
- Implementing partitioning strategies for large tables

### Performance Monitoring
- Setting up query performance monitoring and alerting
- Analyzing slow query logs and identifying patterns
- Implementing database metrics collection (EXPLAIN ANALYZE)
- Creating performance baselines and capacity planning

## Decision Framework

### Optimization Priority Matrix

| Symptom | First Action | Tool |
|---------|--------------|------|
| Query >100ms | EXPLAIN ANALYZE | Execution plan review |
| High CPU | pg_stat_statements | Find top queries |
| High I/O | Index review | Missing index detection |
| Connection exhaustion | Pool tuning | PgBouncer/connection limits |
| Replication lag | Write optimization | Batch operations |

### Index Decision Tree

```
Query Performance Issue
│
├─ WHERE clause filtering?
│  └─ Create B-tree index on filter columns
│
├─ JOIN operations slow?
│  └─ Index foreign key columns
│
├─ ORDER BY/GROUP BY expensive?
│  └─ Include sort columns in index
│
├─ Covering index possible?
│  └─ Add INCLUDE columns to avoid heap fetches
│
└─ Selective queries (status='active')?
   └─ Use partial index with WHERE clause
```

## Core Workflow: Slow Query Optimization

**Scenario**: Production query taking 3.2s, needs to be <100ms

**Step 1: Capture baseline with EXPLAIN ANALYZE**

```sql
EXPLAIN (ANALYZE, BUFFERS, VERBOSE) 
SELECT u.id, u.email, COUNT(o.id) as order_count, SUM(o.total) as total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at >= '2024-01-01'
  AND u.status = 'active'
GROUP BY u.id, u.email
ORDER BY total_spent DESC
LIMIT 100;
```

**Step 2: Identify issues from execution plan**
- Sequential scans instead of index scans
- High shared reads (cache misses)
- Missing indexes on filter/join columns

**Step 3: Create strategic indexes**

```sql
-- Covering index for users with partial index
CREATE INDEX CONCURRENTLY idx_users_status_created_active 
  ON users (status, created_at) 
  INCLUDE (id, email)
  WHERE status = 'active';

-- Covering index for orders JOIN
CREATE INDEX CONCURRENTLY idx_orders_user_id_total 
  ON orders (user_id) 
  INCLUDE (id, total);

-- Update statistics
ANALYZE users;
ANALYZE orders;
```

**Step 4: Verify optimization**

```sql
EXPLAIN (ANALYZE, BUFFERS, VERBOSE) 
-- Same query - should now show:
-- - Index Only Scan instead of Seq Scan
-- - Heap Fetches: 0
-- - Execution Time: <100ms
```

**Expected outcome**:
- Execution time reduced by 95%+ (3205ms -> 87ms)
- Buffer reads eliminated (all hits from cache)
- Sequential scans replaced with index scans
- Query plan stable and predictable

## Quick Reference: Performance Targets

| Metric | OLTP Target | Analytics Target |
|--------|-------------|------------------|
| P50 latency | <50ms | <2s |
| P95 latency | <100ms | <5s |
| P99 latency | <200ms | <10s |
| Cache hit ratio | >95% | >90% |
| Index usage | >95% | >80% |

## Quick Reference: Configuration Guidelines

| Parameter | Formula | Example (32GB RAM) |
|-----------|---------|-------------------|
| shared_buffers | 25% of RAM | 8GB |
| effective_cache_size | 75% of RAM | 24GB |
| work_mem | RAM / max_connections / 4 | 40MB |
| maintenance_work_mem | 10% of RAM | 2GB |
| random_page_cost | 1.1 (SSD) / 4.0 (HDD) | 1.1 |

## Red Flags - When to Escalate

| Observation | Action |
|-------------|--------|
| Query complexity explosion | Escalate to architect for schema redesign |
| Replication lag >10s | Escalate to DBA for infrastructure review |
| Connection pool exhaustion | Review application connection handling |
| Disk I/O saturation | Consider read replicas or caching layer |

## Additional Resources

- **Detailed Technical Reference**: See [REFERENCE.md](REFERENCE.md)
  - Database configuration tuning workflows
  - Partitioning strategies for time-series data
  - Advanced monitoring queries
  
- **Code Examples & Patterns**: See [EXAMPLES.md](EXAMPLES.md)
  - Anti-patterns (over-indexing, premature denormalization)
  - Quality checklist for optimization projects
  - Index monitoring and maintenance queries
