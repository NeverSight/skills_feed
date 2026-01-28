---
name: postgres-query-expert
description: A comprehensive guide for interacting with PostgreSQL 16 databases. Use this skill for constructing standard and advanced SQL queries, optimizing performance, debugging errors, managing schema objects, and introspecting database structure.
allowed-tools: Read, Grep, Glob
---
# PostgreSQL Query Expert

This skill is a definitive reference for PostgreSQL 16, covering query construction, optimization, schema management, and system introspection.

## Instructions

### 1. General Query Standards

- **Syntax**: Adhere to ANSI SQL standards, but prefer PostgreSQL extensions (e.g., `DISTINCT ON`, `RETURNING`, `LATERAL`, `FILTER` clauses) when they provide cleaner logic or better performance.
- **Identifiers**: Use `snake_case` for all identifiers. Only quote identifiers (`"MyTable"`) if absolutely necessary; prefer lowercase unquoted names.
- **Safety**:
  - **Parameterization**: Always use parameters (`$1`, `$2`, …) for literal values. Never inject user input directly.
  - **Timeouts**: For exploratory queries on large databases, prepend `SET LOCAL statement_timeout = '30s';`.
  - **Transactions**: Use explicit `BEGIN` and `COMMIT` blocks for multi-step operations.

### 2. Performance & Optimization

- **Explain plans**: Use `EXPLAIN (ANALYZE, COSTS, VERBOSE, BUFFERS)` to diagnose bottlenecks.
- **Red flags**: `Seq Scan` on large tables, high `Buffers: shared hit` (RAM usage), or `Disk: read` (I/O).
- **Indexing**: Recommend specific index types based on usage:
  - **B-tree**: Standard equality/range (`=`, `<`, `>`) queries.
  - **GIN**: For composite types like `JSONB` (`@>`) or arrays (`&&`), and full-text search.
  - **GiST**: For geometric data and ranges.
- **CTEs**: Use Common Table Expressions (`WITH`) for readability. In PG16+, these are optimized (inlined) by default unless `MATERIALIZED` is specified.

## Introspection (Agent Capabilities)

When exploring a new database, use these queries to understand the schema.

### List All Tables

```sql
SELECT n.nspname AS schema,
       c.relname AS table,
       obj_description(c.oid) AS description
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE c.relkind = 'r'
  AND n.nspname NOT IN ('pg_catalog', 'information_schema')
ORDER BY 1, 2;
```

### Get Table Columns & Types

```sql
SELECT a.attname AS column,
       format_type(a.atttypid, a.atttypmod) AS type,
       a.attnotnull AS not_null,
       col_description(a.attrelid, a.attnum) AS comment
FROM pg_attribute a
WHERE a.attrelid = 'public.target_table_name'::regclass
  AND a.attnum > 0
  AND NOT a.attisdropped
ORDER BY a.attnum;
```

## Reference: Data Querying (DQL)

### Advanced Aggregations

- **Filter clause**: `count(*) FILTER (WHERE status = 'active')`
- **Grouping sets**: `GROUP BY GROUPING SETS ((brand), (brand, category), ())`
- **Any value**: `any_value(col)` (PG16+) returns an arbitrary value from the group.

### Window Functions

Perform calculations across a set of table rows related to the current row.

```sql
SELECT dept,
       emp_no,
       salary,
       -- Rank employees by salary within department
       dense_rank() OVER (PARTITION BY dept ORDER BY salary DESC) AS rank,
       -- Running total of salaries
       sum(salary) OVER (
         PARTITION BY dept
         ORDER BY salary
         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS running_total
FROM employees;
```

### Pattern Matching

- **LIKE**: `col LIKE 'foo%'` (simple wildcard).
- **ILIKE**: `col ILIKE 'foo%'` (case-insensitive).
- **SIMILAR TO**: `col SIMILAR TO '[a-c]%'` (SQL-regex style).
- **POSIX regex**:
  - Case-sensitive: `col ~ '^[a-z]+$'`
  - Case-insensitive: `col ~* 'foo'`

## Reference: Data Modification (DML)

### MERGE (Upsert / Conditional Ops)

Standard SQL method for inserting, updating, or deleting based on join conditions (PG15+).

```sql
MERGE INTO wine_stock ws
USING wine_shipments s
  ON s.winery_id = ws.winery_id
 AND s.year = ws.year
WHEN MATCHED THEN
  UPDATE SET stock = ws.stock + s.count
WHEN NOT MATCHED THEN
  INSERT (winery_id, year, stock)
  VALUES (s.winery_id, s.year, s.count);
```

### INSERT ... ON CONFLICT (Legacy Upsert)

Postgres-specific, often more concise for simple unique-key conflicts.

```sql
INSERT INTO kv_store (key, value)
VALUES ('config', '{"a":1}')
ON CONFLICT (key)
DO UPDATE SET value = EXCLUDED.value;
```

### RETURNING Clause

Return data from modified rows immediately.

```sql
DELETE FROM archived_logs
WHERE created_at < NOW() - INTERVAL '1 year'
RETURNING id, created_at;
```

## Reference: Special Data Types

### JSONB (Binary JSON)

Prefer `jsonb` over `json` for storage and indexing.

| Operator | Description | Example |
|---|---|---|
| `->` / `->>` | Get element (JSON / text) | `data->'key'` |
| `@>` | Contains (indexable) | `data @> '{"tag": "urgent"}'` |
| `?` | Key exists | `data ? 'error'` |
| `#-` | Delete path | `data #- '{info, sensitive}'` |

SQL/JSON path (PG12+):

```sql
-- Find all items with price > 10
SELECT jsonb_path_query(data, '$.items[*] ? (@.price > 10)')
FROM orders;
```

### Arrays

```sql
SELECT ARRAY[1,2,3];           -- Creation
SELECT (ARRAY[1,2,3])[1];      -- Access (1-based index)
SELECT 1 = ANY(arr_col);       -- Check if value exists in array
SELECT unnest(arr_col) FROM t; -- Expand array to rows
```

### Range Types

Useful for scheduling and validity periods.

- `tstzrange`: timestamp with time zone range.
- `int4range`, `daterange`: integer and date ranges.
- Overlap operator (`&&`): checks if two ranges overlap.

```sql
SELECT *
FROM reservations
WHERE duration && tstzrange('2023-01-01 10:00', '2023-01-01 12:00');
```

## Reference: System Administration & Stats

### Kill Long-Running Query

```sql
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'active'
  AND pid <> pg_backend_pid()
  AND query_start < NOW() - INTERVAL '5 minutes';
```

### Check Table Size (Disk Usage)

```sql
SELECT relname,
       pg_size_pretty(pg_total_relation_size(relid)) AS total_size,
       pg_size_pretty(pg_relation_size(relid)) AS data_size
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;
```

## Examples

### Scenario 1: Recursive CTE for Graph/Tree Data

Navigating an organizational hierarchy.

```sql
WITH RECURSIVE subordinates AS (
    -- Base case: the manager
    SELECT employee_id, manager_id, full_name, 0 AS level
    FROM employees
    WHERE employee_id = $1

    UNION ALL

    -- Recursive step: direct reports
    SELECT e.employee_id, e.manager_id, e.full_name, s.level + 1
    FROM employees e
    INNER JOIN subordinates s ON s.employee_id = e.manager_id
)
SELECT *
FROM subordinates;
```

### Scenario 2: Lateral Join for "Top N per Category"

Efficiently getting the latest 3 posts for each user.

```sql
SELECT u.username, p.title, p.created_at
FROM users u
CROSS JOIN LATERAL (
    SELECT title, created_at
    FROM posts
    WHERE user_id = u.id
    ORDER BY created_at DESC
    LIMIT 3
) p
WHERE u.status = 'active';
```

### Scenario 3: Full Text Search with Ranking

Searching a blog table.

```sql
SELECT id,
       title,
       ts_rank(to_tsvector('english', title || ' ' || content), query) AS rank
FROM articles,
     to_tsquery('english', 'postgres | optimization') query
WHERE to_tsvector('english', title || ' ' || content) @@ query
ORDER BY rank DESC;
```

