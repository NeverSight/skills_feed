---
name: reporting-optimization
description: >
  High Performance Reporting and Query Optimization
  Trigger: When optimizing database queries for reporting.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with reporting optimization"

## When to Use

Use this skill when:
- Optimizing slow reporting queries
- Building dashboards with heavy aggregations
- Working with large datasets
- Implementing caching strategies

---

## Decision Tree

```
Need query optimization?   → Use EXPLAIN ANALYZE
Need cached aggregations?  → Use Materialized View
Need complex breakdown?    → Use CTEs
Need row ranking?          → Use Window Functions
Need partial coverage?     → Use Partial Index
```

---

# Reporting & Optimization Guidelines

Reporting queries often scan large datasets. Inefficient queries can degrade the performance of the entire system. Follow these guidelines to ensure speed and stability.

## 1. Query Optimization

### 1.1 SELECT Efficiency
- **No `SELECT *`:** Fetching unnecessary columns increases I/O and network payload. Select only required fields.
- **SARGable Queries:** Ensure predicates (WHERE clauses) are "Search ARGument ABLE" to perform Index Seeks instead of Scans.
    - *Bad:* `WHERE YEAR(created_at) = 2023` (Function on column prevents index use).
    - *Good:* `WHERE created_at >= '2023-01-01' AND created_at < '2024-01-01'`.

### 1.2 CTEs vs Temporary Tables
- **Common Table Expressions (CTEs):** Use `WITH` clauses for readability and to break down complex logic. In modern PostgreSQL (12+), CTEs are materialized when beneficial, making them performant.
- **Temporary Tables:** For extremely complex multi-step processing involving heavy intermediate indexing, use `CREATE TEMP TABLE`.

### 1.3 Subqueries
- Avoid Correlated Subqueries in the `SELECT` list that run once per row. Rewrite them as `JOIN`s or `LATERAL` joins.
    - *Bad:* `SELECT id, (SELECT count(*) FROM orders WHERE user_id = u.id) FROM users u`
    - *Good:* `SELECT u.id, count(o.id) FROM users u LEFT JOIN orders o ON u.id = o.user_id GROUP BY u.id`

## 2. Aggregation Strategies

### 2.1 Materialized Views
- For dashboards requiring heavy aggregation (Count, Sum, Avg) over millions of rows, do not query the live transactional table every time.
- Use **Materialized Views** to cache the result:
    ```sql
    CREATE MATERIALIZED VIEW mv_daily_sales AS
    SELECT day, SUM(total) FROM sales GROUP BY day;
    ```
- Refresh explicitly: `REFRESH MATERIALIZED VIEW CONCURRENTLY mv_daily_sales;`.

### 2.2 Window Functions
- Use Window Functions (`ROW_NUMBER()`, `RANK()`, `LEAD()`, `LAG()`) for complex reporting intra-row logic instead of self-joins.

## 3. Safety Guardrails

### 3.1 Timeouts
- Set `statement_timeout` for reporting roles to prevent a runaway query from locking resources indefinitely.

### 3.2 Result Limits
- Always verify the estimated cardinality. If a report could return 1M+ rows, enforce `LIMIT` or pagination logic.

## 4. Query Profiling

### 4.1 EXPLAIN ANALYZE
Before deploying complex queries, use `EXPLAIN ANALYZE` to understand the execution plan.
- Look for **Seq Scans** on large tables (potential missing index).
- Check **Actual vs Estimated Rows** for significant discrepancies (stale statistics).
- Identify **Nested Loops** with high row counts that could be rewritten as Hash Joins.

```sql
EXPLAIN ANALYZE
SELECT u.id, COUNT(o.id)
FROM USER u
LEFT JOIN ORDER o ON u.id = o.user_id
WHERE u.is_active = TRUE
GROUP BY u.id;
```

### 4.2 Partial Indexes
Create indexes that only cover a subset of rows to save space and speed up specific queries.
- *Example:* Index only active users.
    ```sql
    CREATE INDEX idx_user_active ON USER(email) WHERE is_active = TRUE;
    ```
- Use for columns with low cardinality where only specific values are frequently queried.
