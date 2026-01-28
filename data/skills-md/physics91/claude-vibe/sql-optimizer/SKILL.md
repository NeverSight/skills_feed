---
name: sql-optimizer
description: |
  WHEN: SQL query review, query optimization, index usage, N+1 detection, performance analysis
  WHAT: Query plan analysis + Index recommendations + N+1 detection + Join optimization + Performance tuning
  WHEN NOT: Schema design → schema-reviewer, ORM code → orm-reviewer
---

# SQL Optimizer Skill

## Purpose
Analyzes and optimizes SQL queries for performance, index usage, and best practices.

## When to Use
- SQL query optimization
- Query performance review
- Index usage analysis
- N+1 query detection
- Slow query troubleshooting

## Project Detection
- `.sql` files
- Query strings in code
- Database migration files
- ORM query logs

## Workflow

### Step 1: Analyze Query
```
**Database**: PostgreSQL/MySQL/SQLite
**Tables**: users, orders, products
**Query Type**: SELECT with JOINs
**Estimated Rows**: 100K+
```

### Step 2: Select Review Areas
**AskUserQuestion:**
```
"Which areas to review?"
Options:
- Full query optimization (recommended)
- Index usage analysis
- Join optimization
- Subquery refactoring
- N+1 detection
multiSelect: true
```

## Detection Rules

### Index Usage
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Full table scan | Add appropriate index | CRITICAL |
| Index not used | Check column order | HIGH |
| Too many indexes | Consolidate indexes | MEDIUM |
| Missing composite index | Add multi-column index | HIGH |

```sql
-- BAD: No index on filter columns
SELECT * FROM orders
WHERE created_at > '2024-01-01'
AND status = 'pending';
-- Full table scan!

-- GOOD: Add composite index
CREATE INDEX idx_orders_status_created
ON orders(status, created_at);

-- Index order matters!
-- For WHERE status = ? AND created_at > ?
-- Index(status, created_at) ✓
-- Index(created_at, status) ✗ (less effective)
```

### SELECT Optimization
| Check | Recommendation | Severity |
|-------|----------------|----------|
| SELECT * | Select specific columns | HIGH |
| Unnecessary columns | Remove unused columns | MEDIUM |
| No LIMIT | Add LIMIT for large results | HIGH |

```sql
-- BAD: SELECT * with large result
SELECT * FROM orders
WHERE user_id = 123;
-- Returns all columns, no limit

-- GOOD: Specific columns, limited results
SELECT id, status, total, created_at
FROM orders
WHERE user_id = 123
ORDER BY created_at DESC
LIMIT 20;
```

### JOIN Optimization
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Cartesian product | Add join condition | CRITICAL |
| Join on non-indexed column | Add index | HIGH |
| Too many joins | Consider denormalization | MEDIUM |
| Implicit join | Use explicit JOIN syntax | LOW |

```sql
-- BAD: Implicit join (harder to read, error-prone)
SELECT o.*, u.name
FROM orders o, users u
WHERE o.user_id = u.id;

-- GOOD: Explicit JOIN
SELECT o.id, o.total, u.name
FROM orders o
INNER JOIN users u ON o.user_id = u.id;

-- BAD: Join on non-indexed column
SELECT o.*, p.name
FROM orders o
JOIN products p ON o.product_code = p.code;
-- If products.code has no index → slow!

-- FIX: Add index
CREATE INDEX idx_products_code ON products(code);
```

### Subquery Optimization
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Correlated subquery | Convert to JOIN | HIGH |
| IN with subquery | Use EXISTS or JOIN | MEDIUM |
| Subquery in SELECT | Move to JOIN | HIGH |

```sql
-- BAD: Correlated subquery (runs for each row)
SELECT *
FROM orders o
WHERE total > (
    SELECT AVG(total)
    FROM orders
    WHERE user_id = o.user_id
);

-- GOOD: Use window function
SELECT *
FROM (
    SELECT *,
           AVG(total) OVER (PARTITION BY user_id) as avg_total
    FROM orders
) sub
WHERE total > avg_total;

-- BAD: IN with large subquery
SELECT * FROM users
WHERE id IN (SELECT user_id FROM orders WHERE status = 'vip');

-- GOOD: Use EXISTS or JOIN
SELECT u.* FROM users u
WHERE EXISTS (
    SELECT 1 FROM orders o
    WHERE o.user_id = u.id AND o.status = 'vip'
);

-- Or with JOIN
SELECT DISTINCT u.*
FROM users u
INNER JOIN orders o ON o.user_id = u.id
WHERE o.status = 'vip';
```

### N+1 Query Detection
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Loop with query | Batch fetch | CRITICAL |
| Lazy load in loop | Eager load | CRITICAL |

```sql
-- N+1 Pattern (application code)
-- Query 1: Get all users
SELECT * FROM users;

-- Then for each user (N queries):
SELECT * FROM orders WHERE user_id = 1;
SELECT * FROM orders WHERE user_id = 2;
SELECT * FROM orders WHERE user_id = 3;
-- ... N more queries

-- SOLUTION 1: JOIN
SELECT u.*, o.*
FROM users u
LEFT JOIN orders o ON o.user_id = u.id;

-- SOLUTION 2: IN query (for separate queries)
SELECT * FROM orders WHERE user_id IN (1, 2, 3, ...);
```

### Aggregation Optimization
| Check | Recommendation | Severity |
|-------|----------------|----------|
| COUNT(*) on large table | Use approximate count | MEDIUM |
| GROUP BY without index | Add index | HIGH |
| HAVING vs WHERE | Filter early with WHERE | MEDIUM |

```sql
-- BAD: COUNT on entire table
SELECT COUNT(*) FROM orders;
-- Scans entire table

-- GOOD: Approximate count (PostgreSQL)
SELECT reltuples::bigint AS estimate
FROM pg_class
WHERE relname = 'orders';

-- BAD: WHERE in HAVING
SELECT user_id, COUNT(*)
FROM orders
GROUP BY user_id
HAVING status = 'completed';  -- Wrong place!

-- GOOD: Filter before grouping
SELECT user_id, COUNT(*)
FROM orders
WHERE status = 'completed'  -- Filter first
GROUP BY user_id;

-- Index for GROUP BY
CREATE INDEX idx_orders_user_status
ON orders(user_id, status);
```

### EXPLAIN Analysis
```sql
-- PostgreSQL EXPLAIN
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.name, COUNT(o.id)
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
GROUP BY u.id;

-- Look for:
-- ✗ Seq Scan (full table scan)
-- ✗ Nested Loop with high rows
-- ✗ Hash Join with large hash
-- ✓ Index Scan
-- ✓ Index Only Scan
-- ✓ Bitmap Index Scan
```

## Response Template
```
## SQL Query Optimization Results

**Database**: PostgreSQL 15
**Query Type**: SELECT with JOIN
**Estimated Impact**: ~10x improvement

### Index Usage
| Status | Issue | Recommendation |
|--------|-------|----------------|
| CRITICAL | Full table scan on orders | Add index on (status, created_at) |

### Join Analysis
| Status | Issue | Recommendation |
|--------|-------|----------------|
| HIGH | Non-indexed join column | Add index on products.code |

### Query Structure
| Status | Issue | Recommendation |
|--------|-------|----------------|
| HIGH | SELECT * with no LIMIT | Select specific columns, add LIMIT |

### Recommended Indexes
```sql
CREATE INDEX idx_orders_status_created ON orders(status, created_at);
CREATE INDEX idx_products_code ON products(code);
```

### Optimized Query
```sql
SELECT o.id, o.total, p.name
FROM orders o
INNER JOIN products p ON o.product_id = p.id
WHERE o.status = 'pending'
ORDER BY o.created_at DESC
LIMIT 100;
```
```

## Best Practices
1. **Indexes**: Add for WHERE, JOIN, ORDER BY columns
2. **SELECT**: Only needed columns, with LIMIT
3. **JOINs**: Explicit syntax, indexed columns
4. **Subqueries**: Prefer JOINs or CTEs
5. **EXPLAIN**: Always analyze query plans

## Integration
- `schema-reviewer`: Database design
- `orm-reviewer`: ORM query patterns
- `perf-analyzer`: Application performance
