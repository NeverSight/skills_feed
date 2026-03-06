---
name: sql
description: Write SQL queries, optimize execution plans, and design schemas. Use for query optimization, complex joins, or database design.
---

# SQL Development

Write efficient SQL queries and design schemas.

## When to Use

- Writing complex queries
- Query optimization
- Schema design
- Index strategy
- Migration planning

## Query Patterns

### Window Functions

```sql
-- Running totals
SELECT
    date,
    amount,
    SUM(amount) OVER (ORDER BY date) as running_total,
    AVG(amount) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as moving_avg_7d
FROM transactions;

-- Ranking
SELECT
    name,
    score,
    RANK() OVER (ORDER BY score DESC) as rank,
    DENSE_RANK() OVER (ORDER BY score DESC) as dense_rank,
    ROW_NUMBER() OVER (ORDER BY score DESC) as row_num
FROM players;

-- Partition by category
SELECT
    category,
    product,
    sales,
    sales * 100.0 / SUM(sales) OVER (PARTITION BY category) as pct_of_category
FROM products;
```

### CTEs (Common Table Expressions)

```sql
WITH
monthly_sales AS (
    SELECT
        DATE_TRUNC('month', order_date) as month,
        SUM(amount) as total
    FROM orders
    GROUP BY 1
),
growth AS (
    SELECT
        month,
        total,
        LAG(total) OVER (ORDER BY month) as prev_month,
        (total - LAG(total) OVER (ORDER BY month)) / NULLIF(LAG(total) OVER (ORDER BY month), 0) * 100 as growth_pct
    FROM monthly_sales
)
SELECT * FROM growth WHERE growth_pct < 0;
```

### Recursive CTEs

```sql
-- Hierarchical data (org chart, categories)
WITH RECURSIVE subordinates AS (
    SELECT id, name, manager_id, 1 as level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.manager_id, s.level + 1
    FROM employees e
    JOIN subordinates s ON e.manager_id = s.id
)
SELECT * FROM subordinates ORDER BY level, name;
```

## Query Optimization

### Index Strategy

```sql
-- Composite index for common queries
CREATE INDEX idx_orders_user_date ON orders(user_id, order_date DESC);

-- Partial index for filtered queries
CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';

-- Check query plan
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 123;
```

### Common Issues

| Problem         | Symptom         | Solution                   |
| --------------- | --------------- | -------------------------- |
| Missing index   | Seq Scan        | Add appropriate index      |
| N+1 queries     | Many small hits | Use JOIN or batch          |
| SELECT \*       | Slow + memory   | Select only needed columns |
| No LIMIT        | Large result    | Add pagination             |
| Function on col | Index not used  | Rewrite condition          |

## Schema Design

```sql
-- Normalized schema
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    total DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status) WHERE status != 'completed';
```

## Examples

**Input:** "Optimize this slow query"
**Action:** Run EXPLAIN, identify bottlenecks, add indexes or rewrite query

**Input:** "Get top 10 customers by revenue"
**Action:** Write aggregation with proper joins, ordering, and limit
