---
name: bq-query-optimization
description: Use when writing BigQuery queries, optimizing query performance, analyzing execution plans, or avoiding common SQL gotchas. Covers parameterized queries, UDFs, scripting, window functions (QUALIFY, ROW_NUMBER, RANK, LEAD/LAG), JSON functions, ARRAY/STRUCT operations, BigQuery-specific features (EXCEPT, REPLACE, SAFE_*), CTE re-execution issues, NOT IN with NULLs, DML performance, Standard vs Legacy SQL, and performance best practices.
---

# BigQuery Query Optimization

Use this skill when writing, debugging, or optimizing BigQuery SQL queries for performance and efficiency.

## Query Execution Analysis

### Using EXPLAIN

```sql
-- Get execution plan
EXPLAIN SELECT * FROM `project.dataset.table` WHERE condition;

-- Get execution plan with runtime stats
EXPLAIN ANALYZE SELECT * FROM `project.dataset.table` WHERE condition;
```

**What the plan shows:**
- Stages of execution
- Bytes read per stage
- Slot time consumed
- Potential bottlenecks

## Performance Best Practices

### 1. Avoid SELECT *

**❌ Bad (scans all columns):**
```sql
SELECT * FROM `project.dataset.large_table`
```

**✅ Good (only needed columns):**
```sql
SELECT customer_id, amount, date
FROM `project.dataset.large_table`
```

**Impact:** Full table scan vs targeted column read. Can reduce data scanned by 90%+.

### 2. Filter Early and Often

**❌ Bad (filter after aggregation):**
```sql
SELECT customer_id, SUM(amount) as total
FROM `project.dataset.orders`
GROUP BY customer_id
HAVING SUM(amount) > 1000
```

**✅ Good (filter before aggregation):**
```sql
SELECT customer_id, SUM(amount) as total
FROM `project.dataset.orders`
WHERE amount > 100  -- Filter early
GROUP BY customer_id
HAVING SUM(amount) > 1000
```

### 3. Use Partitioned Tables

**Without partition filter:**
```sql
-- Scans entire table
SELECT * FROM `project.dataset.orders`
WHERE order_date >= '2024-01-01'
```

**With partition filter:**
```sql
-- Only scans relevant partitions
SELECT * FROM `project.dataset.orders`
WHERE DATE(order_timestamp) >= '2024-01-01'  -- Partition column
```

**Key:** Filter on the partition column for automatic partition pruning.

### 4. Break Complex Queries

**❌ Anti-pattern (one huge query):**
```sql
SELECT ...
FROM (
  SELECT ...
  FROM (
    SELECT ... -- Deeply nested
  )
)
WHERE ...
```

**✅ Good (use CTEs):**
```sql
WITH base_data AS (
  SELECT customer_id, amount, date
  FROM `project.dataset.orders`
  WHERE date >= '2024-01-01'
),
aggregated AS (
  SELECT customer_id, SUM(amount) as total
  FROM base_data
  GROUP BY customer_id
)
SELECT * FROM aggregated WHERE total > 1000
```

**✅ Better (multi-statement with temp tables):**
```sql
CREATE TEMP TABLE base_data AS
SELECT customer_id, amount, date
FROM `project.dataset.orders`
WHERE date >= '2024-01-01';

CREATE TEMP TABLE aggregated AS
SELECT customer_id, SUM(amount) as total
FROM base_data
GROUP BY customer_id;

SELECT * FROM aggregated WHERE total > 1000;
```

### 5. JOIN Optimization

**Put largest table first:**
```sql
-- ✅ Large table first
SELECT l.*, s.detail
FROM `project.dataset.large_table` l
JOIN `project.dataset.small_table` s
  ON l.id = s.id
```

**Use clustering on JOIN columns:**
- Cluster tables on frequently joined columns
- BigQuery can prune data blocks more effectively

**Consider ARRAY/STRUCT for 1:many:**
```sql
-- Instead of JOIN for 1:many relationships
SELECT
  order_id,
  ARRAY_AGG(STRUCT(product_id, quantity, price)) as items
FROM `project.dataset.order_items`
GROUP BY order_id
```

### 6. Leverage Automatic Features

BigQuery automatically performs:
- **Query rewrites** - Optimizes query structure
- **Partition pruning** - With proper filters
- **Dynamic filtering** - Reduces data scanned

**Ensure your queries enable these:**
- Filter on partition columns
- Use simple, clear predicates
- Avoid functions on partition columns in WHERE clause

## Parameterized Queries

### CLI Syntax

```bash
bq query \
  --use_legacy_sql=false \
  --parameter=start_date:DATE:2024-01-01 \
  --parameter=end_date:DATE:2024-12-31 \
  --parameter=min_amount:FLOAT64:100.0 \
  'SELECT *
   FROM `project.dataset.orders`
   WHERE order_date BETWEEN @start_date AND @end_date
   AND amount >= @min_amount'
```

### Python Syntax

```python
from google.cloud import bigquery

client = bigquery.Client()

query = """
SELECT customer_id, SUM(amount) as total
FROM `project.dataset.orders`
WHERE order_date >= @start_date
GROUP BY customer_id
"""

job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter("start_date", "DATE", "2024-01-01")
    ]
)

results = client.query_and_wait(query, job_config=job_config)
```

**Key points:**
- Use `@` prefix for named parameters
- Syntax: `name:TYPE:value` or `name::value` (STRING default)
- Cannot use as column/table names
- Only works with standard SQL

## User-Defined Functions (UDFs)

### SQL UDF (Simple)

```sql
CREATE TEMP FUNCTION CleanEmail(email STRING)
RETURNS STRING
AS (
  LOWER(TRIM(email))
);

SELECT CleanEmail(customer_email) as email
FROM `project.dataset.customers`;
```

### JavaScript UDF (Complex Logic)

```sql
CREATE TEMP FUNCTION ParseUserAgent(ua STRING)
RETURNS STRUCT<browser STRING, version STRING>
LANGUAGE js AS r"""
  var match = ua.match(/(Chrome|Firefox|Safari)\/(\d+)/);
  return {
    browser: match ? match[1] : 'Unknown',
    version: match ? match[2] : '0'
  };
""";

SELECT ParseUserAgent(user_agent).browser as browser
FROM `project.dataset.sessions`;
```

**Limitations:**
- INT64 unsupported in JavaScript (use FLOAT64 or STRING)
- JavaScript doesn't support 64-bit integers natively

### Persistent UDFs

```sql
-- Create once, use many times
CREATE FUNCTION `project.dataset.clean_email`(email STRING)
RETURNS STRING
AS (LOWER(TRIM(email)));

-- Use anywhere
SELECT `project.dataset.clean_email`(email) FROM ...
```

## Scripting & Procedural Language

### Variables

```sql
DECLARE total_orders INT64;
SET total_orders = (SELECT COUNT(*) FROM `project.dataset.orders`);

SELECT total_orders;
```

### Loops

**LOOP:**
```sql
DECLARE x INT64 DEFAULT 0;
LOOP
  SET x = x + 1;
  IF x >= 10 THEN
    LEAVE;
  END IF;
END LOOP;
```

**WHILE:**
```sql
DECLARE x INT64 DEFAULT 0;
WHILE x < 10 DO
  SET x = x + 1;
END WHILE;
```

**FOR with arrays:**
```sql
DECLARE ids ARRAY<STRING>;
SET ids = ['id1', 'id2', 'id3'];

FOR item IN (SELECT * FROM UNNEST(ids) as id)
DO
  -- Process each id
  SELECT id;
END FOR;
```

## Query Caching

**Automatic caching (24 hours):**
- Identical queries serve cached results (free)
- No additional cost
- Instant response

**To bypass cache:**
```bash
bq query --use_cache=false 'SELECT...'
```

## Common Anti-Patterns

### ❌ Using LIMIT to reduce cost
```sql
-- LIMIT doesn't reduce data scanned or cost!
SELECT * FROM `project.dataset.huge_table` LIMIT 10
```

**Impact:** Still scans entire table. Use WHERE filters instead.

### ❌ Functions on partition columns
```sql
-- Prevents partition pruning
WHERE CAST(date_column AS STRING) = '2024-01-01'
```

**✅ Better:**
```sql
WHERE date_column = DATE('2024-01-01')
```

### ❌ Cross joins without filters
```sql
-- Cartesian product = huge result
SELECT * FROM table1 CROSS JOIN table2
```

**Impact:** Can generate millions/billions of rows.

### ❌ Correlated subqueries
```sql
-- Runs subquery for each row
SELECT *
FROM orders o
WHERE amount > (SELECT AVG(amount) FROM orders WHERE customer_id = o.customer_id)
```

**✅ Better (use window functions):**
```sql
SELECT *
FROM (
  SELECT *, AVG(amount) OVER (PARTITION BY customer_id) as avg_amount
  FROM orders
)
WHERE amount > avg_amount
```

## Common SQL Gotchas

### CTE Re-execution (CRITICAL COST ISSUE)

**Problem:** When a CTE is referenced multiple times, BigQuery re-executes it each time, billing you multiple times.

**❌ Bad (CTE runs 3 times - billed 3x):**
```sql
WITH expensive_cte AS (
  SELECT * FROM `project.dataset.huge_table`
  WHERE complex_conditions
  AND lots_of_joins
)
SELECT COUNT(*) FROM expensive_cte
UNION ALL
SELECT SUM(amount) FROM expensive_cte
UNION ALL
SELECT MAX(date) FROM expensive_cte;
```

**Impact:** If the CTE scans 10 TB, you're billed for 30 TB (10 TB × 3).

**✅ Good (use temp table - billed 1x):**
```sql
CREATE TEMP TABLE expensive_data AS
SELECT * FROM `project.dataset.huge_table`
WHERE complex_conditions
AND lots_of_joins;

SELECT COUNT(*) FROM expensive_data
UNION ALL
SELECT SUM(amount) FROM expensive_data
UNION ALL
SELECT MAX(date) FROM expensive_data;
```

**When CTEs are OK:**
- Referenced only once
- Very small result set
- Part of larger query (BigQuery may optimize)

**When to use temp tables:**
- CTE referenced 2+ times
- Large data volumes
- Complex/expensive CTE query

---

### NOT IN with NULL Values (SILENT FAILURE)

**Problem:** `NOT IN` returns NOTHING (empty result) if ANY NULL exists in the subquery.

**❌ Broken (returns empty if blocked_customers has any NULL):**
```sql
SELECT * FROM customers
WHERE customer_id NOT IN (
  SELECT customer_id FROM blocked_customers  -- If ANY NULL, returns 0 rows!
);
```

**Why it fails:**
- SQL three-valued logic: TRUE, FALSE, UNKNOWN
- `NULL IN (...)` evaluates to UNKNOWN
- `NOT UNKNOWN` is still UNKNOWN
- Rows with UNKNOWN are filtered out

**✅ Solution 1: Use NOT EXISTS (safest):**
```sql
SELECT * FROM customers c
WHERE NOT EXISTS (
  SELECT 1 FROM blocked_customers b
  WHERE b.customer_id = c.customer_id
);
```

**✅ Solution 2: Filter NULLs explicitly:**
```sql
SELECT * FROM customers
WHERE customer_id NOT IN (
  SELECT customer_id
  FROM blocked_customers
  WHERE customer_id IS NOT NULL  -- Explicit NULL filter
);
```

**✅ Solution 3: Use LEFT JOIN:**
```sql
SELECT c.*
FROM customers c
LEFT JOIN blocked_customers b
  ON c.customer_id = b.customer_id
WHERE b.customer_id IS NULL;
```

**Best practice:** Prefer `NOT EXISTS` - it's clearer, safer, and often faster.

---

### DML Statement Performance

**Problem:** BigQuery is optimized for analytics (OLAP), not transactional updates (OLTP). DML statements are slow and expensive.

**Why DML is slow in BigQuery:**
- Columnar storage (not row-based)
- Designed for bulk reads, not individual updates
- No indexes for fast row lookups
- Every update rewrites affected partitions

**❌ Very slow (row-by-row updates):**
```sql
-- Don't do this - takes minutes/hours
UPDATE `project.dataset.orders`
SET status = 'processed'
WHERE order_id = '12345';

-- This is even worse - runs once per row
FOR record IN (SELECT order_id FROM orders_to_update)
DO
  UPDATE orders SET status = 'processed' WHERE order_id = record.order_id;
END FOR;
```

**⚠️ Better (batch updates):**
```sql
UPDATE `project.dataset.orders`
SET status = 'processed'
WHERE order_id IN (SELECT order_id FROM orders_to_update);
```

**✅ Best (recreate table - fastest):**
```sql
CREATE OR REPLACE TABLE `project.dataset.orders` AS
SELECT
  * EXCEPT(status),
  CASE
    WHEN order_id IN (SELECT order_id FROM orders_to_update)
      THEN 'processed'
    ELSE status
  END AS status
FROM `project.dataset.orders`;
```

**For INSERT/UPSERT - use MERGE:**
```sql
MERGE `project.dataset.customers` AS target
USING `project.dataset.customer_updates` AS source
ON target.customer_id = source.customer_id
WHEN MATCHED THEN
  UPDATE SET name = source.name, updated_at = CURRENT_TIMESTAMP()
WHEN NOT MATCHED THEN
  INSERT (customer_id, name, created_at)
  VALUES (customer_id, name, CURRENT_TIMESTAMP());
```

**Best practices:**
- Batch updates instead of row-by-row
- Use MERGE for upserts
- Consider recreating table for large updates
- Partition tables to limit update scope
- Avoid frequent small DML operations

---

### Data Type Gotchas

**INT64 is the only integer type:**
```sql
-- All of these are the same: INT64
CREATE TABLE example (
  col1 INT64,      -- ✅ Explicit
  col2 INTEGER,    -- Converted to INT64
  col3 INT,        -- Converted to INT64
  col4 SMALLINT,   -- Converted to INT64
  col5 BIGINT      -- Converted to INT64
);
```

**No UUID type - use STRING:**
```sql
-- PostgreSQL
CREATE TABLE users (id UUID);

-- BigQuery
CREATE TABLE users (id STRING);  -- Store UUID as string
```

**NUMERIC precision limits:**
```sql
-- NUMERIC: 38 digits precision, 9 decimal places
NUMERIC(38, 9)

-- BIGNUMERIC: 76 digits precision, 38 decimal places
BIGNUMERIC(76, 38)

-- Example
SELECT
  CAST('12345678901234567890.123456789' AS NUMERIC) AS num,
  CAST('12345678901234567890.123456789' AS BIGNUMERIC) AS bignum;
```

**TIMESTAMP vs DATETIME vs DATE:**
```sql
-- TIMESTAMP: UTC, timezone-aware
SELECT CURRENT_TIMESTAMP();  -- 2024-01-15 10:30:45.123456 UTC

-- DATETIME: No timezone
SELECT CURRENT_DATETIME();   -- 2024-01-15 10:30:45.123456

-- DATE: Date only
SELECT CURRENT_DATE();       -- 2024-01-15

-- Conversion
SELECT
  TIMESTAMP('2024-01-15 10:30:45'),          -- Assumes UTC
  DATETIME(TIMESTAMP '2024-01-15 10:30:45'), -- Loses timezone
  DATE(TIMESTAMP '2024-01-15 10:30:45');     -- Loses time
```

**Type coercion in JOINs:**
```sql
-- ❌ Implicit cast can prevent optimization
SELECT * FROM table1 t1
JOIN table2 t2
  ON t1.id = CAST(t2.id AS STRING);  -- Prevents clustering optimization

-- ✅ Match types explicitly
SELECT * FROM table1 t1
JOIN table2 t2
  ON t1.id = t2.id;  -- Both STRING
```

---

## Window Functions

Window functions perform calculations across a set of rows related to the current row, without collapsing the result set.

### Basic Syntax

```sql
<function> OVER (
  [PARTITION BY partition_expression]
  [ORDER BY sort_expression]
  [window_frame_clause]
)
```

### Ranking Functions

**ROW_NUMBER() - Sequential numbering:**
```sql
SELECT
  customer_id,
  order_date,
  amount,
  ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) AS row_num
FROM orders;
```

**Common use: Deduplication**
```sql
SELECT * EXCEPT(row_num)
FROM (
  SELECT
    *,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) AS row_num
  FROM customers
)
WHERE row_num = 1;
```

**RANK() - Rank with gaps:**
```sql
SELECT
  product_name,
  revenue,
  RANK() OVER (ORDER BY revenue DESC) AS rank
FROM products;

-- Results:
-- Product A: $1000, rank 1
-- Product B: $900,  rank 2
-- Product C: $900,  rank 2  (tie)
-- Product D: $800,  rank 4  (gap after tie)
```

**DENSE_RANK() - Rank without gaps:**
```sql
SELECT
  product_name,
  revenue,
  DENSE_RANK() OVER (ORDER BY revenue DESC) AS dense_rank
FROM products;

-- Results:
-- Product A: $1000, rank 1
-- Product B: $900,  rank 2
-- Product C: $900,  rank 2  (tie)
-- Product D: $800,  rank 3  (no gap)
```

**NTILE() - Divide into N buckets:**
```sql
SELECT
  customer_id,
  total_spend,
  NTILE(4) OVER (ORDER BY total_spend DESC) AS quartile
FROM customer_totals;
```

---

### Analytical Functions

**LEAD() and LAG() - Access rows before/after:**
```sql
-- Time series analysis
SELECT
  date,
  revenue,
  LAG(revenue) OVER (ORDER BY date) AS prev_day_revenue,
  LEAD(revenue) OVER (ORDER BY date) AS next_day_revenue,
  revenue - LAG(revenue) OVER (ORDER BY date) AS daily_change,
  ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY date)) / LAG(revenue) OVER (ORDER BY date), 2) AS pct_change
FROM daily_sales
ORDER BY date;
```

**With PARTITION BY:**
```sql
-- Per-customer analysis
SELECT
  customer_id,
  order_date,
  amount,
  LAG(amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_order_amount,
  amount - LAG(amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS amount_diff
FROM orders;
```

**FIRST_VALUE() and LAST_VALUE():**
```sql
SELECT
  date,
  revenue,
  FIRST_VALUE(revenue) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS first_day_revenue,
  LAST_VALUE(revenue) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_day_revenue
FROM daily_sales;
```

**NTH_VALUE() - Get Nth value:**
```sql
SELECT
  product_id,
  date,
  sales,
  NTH_VALUE(sales, 2) OVER (PARTITION BY product_id ORDER BY date) AS second_day_sales
FROM product_sales;
```

---

### Aggregate Window Functions

**SUM/AVG/COUNT as window functions:**
```sql
SELECT
  date,
  revenue,
  SUM(revenue) OVER (ORDER BY date) AS cumulative_revenue,
  AVG(revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS moving_avg_7day,
  COUNT(*) OVER (ORDER BY date ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) AS rolling_30day_count
FROM daily_sales;
```

**Running totals:**
```sql
SELECT
  customer_id,
  order_date,
  amount,
  SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS customer_lifetime_value
FROM orders;
```

---

### QUALIFY Clause (BigQuery-Specific)

**QUALIFY filters on window function results - no subquery needed!**

**❌ Standard SQL (verbose):**
```sql
SELECT *
FROM (
  SELECT
    *,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) AS row_num
  FROM orders
)
WHERE row_num = 1;
```

**✅ BigQuery with QUALIFY (clean):**
```sql
SELECT customer_id, order_date, amount
FROM orders
QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) = 1;
```

**More QUALIFY examples:**
```sql
-- Get top 3 products per category
SELECT category, product_name, revenue
FROM products
QUALIFY RANK() OVER (PARTITION BY category ORDER BY revenue DESC) <= 3;

-- Filter outliers (keep middle 80%)
SELECT *
FROM measurements
QUALIFY NTILE(10) OVER (ORDER BY value) BETWEEN 2 AND 9;

-- Get first order per customer
SELECT customer_id, order_date, amount
FROM orders
QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date ASC) = 1;
```

---

### Window Frame Clauses

**Control which rows are included in the window:**

```sql
-- ROWS: Physical row count
ROWS BETWEEN 3 PRECEDING AND CURRENT ROW  -- Last 4 rows including current

-- RANGE: Logical range (based on ORDER BY values)
RANGE BETWEEN INTERVAL 7 DAY PRECEDING AND CURRENT ROW  -- Last 7 days

-- Examples:
SELECT
  date,
  sales,
  -- Last 7 rows
  AVG(sales) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS avg_7rows,

  -- Last 7 days (logical)
  AVG(sales) OVER (ORDER BY date RANGE BETWEEN INTERVAL 7 DAY PRECEDING AND CURRENT ROW) AS avg_7days,

  -- All preceding rows
  SUM(sales) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_sum,

  -- Centered window (3 before, 3 after)
  AVG(sales) OVER (ORDER BY date ROWS BETWEEN 3 PRECEDING AND 3 FOLLOWING) AS centered_avg
FROM daily_sales;
```

---

### Window Function Performance Tips

**1. Partition appropriately:**
```sql
-- ✅ Good: Partitions reduce data scanned
SELECT *
FROM events
WHERE date >= '2024-01-01'  -- Partition filter
QUALIFY ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY timestamp DESC) = 1;
```

**2. Avoid window functions in WHERE:**
```sql
-- ❌ Wrong: Can't use window functions in WHERE
SELECT * FROM orders
WHERE ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY date) = 1;  -- ERROR

-- ✅ Use QUALIFY instead
SELECT * FROM orders
QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY date) = 1;
```

**3. Reuse window definitions:**
```sql
SELECT
  date,
  revenue,
  ROW_NUMBER() OVER w AS row_num,
  RANK() OVER w AS rank,
  AVG(revenue) OVER w AS avg_revenue
FROM sales
WINDOW w AS (PARTITION BY category ORDER BY revenue DESC);
```

---

## JSON Functions

BigQuery provides rich functions for parsing, extracting, and manipulating JSON data.

### Extracting JSON Values

**JSON_VALUE() - Extract scalar values (Standard SQL):**
```sql
SELECT
  JSON_VALUE(json_column, '$.user.name') AS user_name,
  JSON_VALUE(json_column, '$.user.email') AS email,
  CAST(JSON_VALUE(json_column, '$.amount') AS FLOAT64) AS amount,
  CAST(JSON_VALUE(json_column, '$.quantity') AS INT64) AS quantity
FROM events;
```

**JSON_QUERY() - Extract objects or arrays:**
```sql
SELECT
  JSON_QUERY(json_column, '$.user') AS user_object,
  JSON_QUERY(json_column, '$.items') AS items_array
FROM events;
```

**JSON_EXTRACT() - Legacy, still widely used:**
```sql
SELECT
  JSON_EXTRACT(json_column, '$.user.name') AS user_name,
  JSON_EXTRACT_SCALAR(json_column, '$.user.email') AS email  -- Returns STRING
FROM events;
```

**JSONPath syntax:**
```sql
-- Dot notation
'$.user.name'

-- Array index
'$.items[0].product_id'

-- Array slice
'$.items[0:3]'

-- Wildcard
'$.users[*].name'

-- Recursive descent
'$..name'  -- All 'name' fields at any level
```

---

### Working with JSON Arrays

**JSON_EXTRACT_ARRAY() - Extract array elements:**
```sql
SELECT
  event_id,
  tag
FROM events,
UNNEST(JSON_EXTRACT_ARRAY(tags_json, '$')) AS tag;
```

**JSON_VALUE_ARRAY() - Extract array of scalars:**
```sql
SELECT
  product_id,
  tag
FROM products,
UNNEST(JSON_VALUE_ARRAY(tags_json, '$')) AS tag;
```

**Complete example:**
```sql
-- JSON: {"product_id": "A123", "tags": ["electronics", "sale", "featured"]}
SELECT
  JSON_VALUE(product_json, '$.product_id') AS product_id,
  tag
FROM products,
UNNEST(JSON_VALUE_ARRAY(product_json, '$.tags')) AS tag;

-- Results:
-- A123, electronics
-- A123, sale
-- A123, featured
```

---

### Creating JSON

**TO_JSON_STRING() - Convert to JSON:**
```sql
SELECT
  customer_id,
  TO_JSON_STRING(STRUCT(
    name,
    email,
    created_at
  )) AS customer_json
FROM customers;
```

**Create JSON objects:**
```sql
SELECT
  TO_JSON_STRING(STRUCT(
    'John' AS name,
    30 AS age,
    ['reading', 'hiking'] AS hobbies,
    STRUCT('123 Main St' AS street, 'Boston' AS city) AS address
  )) AS person_json;

-- Result:
-- {"name":"John","age":30,"hobbies":["reading","hiking"],"address":{"street":"123 Main St","city":"Boston"}}
```

**Aggregate into JSON:**
```sql
SELECT
  customer_id,
  TO_JSON_STRING(
    ARRAY_AGG(
      STRUCT(order_id, amount, date)
      ORDER BY date DESC
      LIMIT 5
    )
  ) AS recent_orders_json
FROM orders
GROUP BY customer_id;
```

---

### Parsing JSON Strings

**PARSE_JSON() - Convert string to JSON:**
```sql
SELECT
  JSON_VALUE(PARSE_JSON('{"name":"Alice","age":25}'), '$.name') AS name;
```

**Safe JSON parsing (avoid errors):**
```sql
SELECT
  SAFE.JSON_VALUE(invalid_json, '$.name') AS name  -- Returns NULL on error
FROM events;
```

---

### Complex JSON Examples

**Nested JSON extraction:**
```sql
-- JSON structure:
-- {
--   "order": {
--     "id": "ORD123",
--     "items": [
--       {"product": "A", "qty": 2, "price": 10.50},
--       {"product": "B", "qty": 1, "price": 25.00}
--     ]
--   }
-- }

SELECT
  JSON_VALUE(data, '$.order.id') AS order_id,
  JSON_VALUE(item, '$.product') AS product,
  CAST(JSON_VALUE(item, '$.qty') AS INT64) AS quantity,
  CAST(JSON_VALUE(item, '$.price') AS FLOAT64) AS price
FROM events,
UNNEST(JSON_EXTRACT_ARRAY(data, '$.order.items')) AS item;
```

**Transform relational data to JSON:**
```sql
SELECT
  category,
  TO_JSON_STRING(
    STRUCT(
      category AS category_name,
      COUNT(*) AS product_count,
      ROUND(AVG(price), 2) AS avg_price,
      ARRAY_AGG(
        STRUCT(product_name, price)
        ORDER BY price DESC
        LIMIT 3
      ) AS top_products
    )
  ) AS category_summary
FROM products
GROUP BY category;
```

---

### JSON Performance Tips

**1. Extract once, reuse:**
```sql
-- ❌ Bad: Multiple extractions
SELECT
  JSON_VALUE(data, '$.user.id'),
  JSON_VALUE(data, '$.user.name'),
  JSON_VALUE(data, '$.user.email')
FROM events;

-- ✅ Better: Extract object once
WITH extracted AS (
  SELECT JSON_QUERY(data, '$.user') AS user_json
  FROM events
)
SELECT
  JSON_VALUE(user_json, '$.id'),
  JSON_VALUE(user_json, '$.name'),
  JSON_VALUE(user_json, '$.email')
FROM extracted;
```

**2. Consider STRUCT columns instead of JSON:**
```sql
-- If schema is known and stable, use STRUCT
CREATE TABLE events (
  user STRUCT<id STRING, name STRING, email STRING>,
  timestamp TIMESTAMP
);

-- Query with dot notation (faster than JSON extraction)
SELECT user.id, user.name, user.email
FROM events;
```

**3. Materialize frequently accessed JSON fields:**
```sql
-- Add extracted columns to table
ALTER TABLE events
ADD COLUMN user_id STRING AS (JSON_VALUE(data, '$.user.id'));

-- Now queries can filter efficiently
SELECT * FROM events WHERE user_id = 'U123';
```

---

## ARRAY and STRUCT

BigQuery's native support for nested and repeated data allows for powerful denormalization and performance optimization.

### ARRAY Basics

**Creating arrays:**
```sql
SELECT
  [1, 2, 3, 4, 5] AS numbers,
  ['apple', 'banana', 'cherry'] AS fruits,
  [DATE '2024-01-01', DATE '2024-01-02'] AS dates;
```

**ARRAY_AGG() - Aggregate into array:**
```sql
SELECT
  customer_id,
  ARRAY_AGG(order_id ORDER BY order_date DESC) AS order_ids,
  ARRAY_AGG(amount) AS order_amounts
FROM orders
GROUP BY customer_id;
```

**With LIMIT:**
```sql
SELECT
  customer_id,
  ARRAY_AGG(order_id ORDER BY order_date DESC LIMIT 5) AS recent_order_ids
FROM orders
GROUP BY customer_id;
```

---

### UNNEST - Flattening Arrays

**Basic UNNEST:**
```sql
SELECT element
FROM UNNEST(['a', 'b', 'c']) AS element;

-- Results:
-- a
-- b
-- c
```

**UNNEST with table:**
```sql
-- Table: customers
-- customer_id | order_ids
-- 1           | [101, 102, 103]
-- 2           | [201, 202]

SELECT
  customer_id,
  order_id
FROM customers,
UNNEST(order_ids) AS order_id;

-- Results:
-- 1, 101
-- 1, 102
-- 1, 103
-- 2, 201
-- 2, 202
```

**UNNEST with OFFSET (get array index):**
```sql
SELECT
  item,
  idx
FROM UNNEST(['first', 'second', 'third']) AS item WITH OFFSET AS idx;

-- Results:
-- first, 0
-- second, 1
-- third, 2
```

---

### STRUCT - Nested Records

**Creating structs:**
```sql
SELECT
  STRUCT('John' AS name, 30 AS age, 'Engineer' AS role) AS person,
  STRUCT('123 Main St' AS street, 'Boston' AS city, '02101' AS zip) AS address;
```

**Querying struct fields:**
```sql
SELECT
  person.name,
  person.age,
  address.city
FROM (
  SELECT
    STRUCT('John' AS name, 30 AS age) AS person,
    STRUCT('Boston' AS city) AS address
);
```

---

### ARRAY of STRUCT (Most Powerful Pattern)

**Create:**
```sql
SELECT
  customer_id,
  ARRAY_AGG(
    STRUCT(
      order_id,
      amount,
      order_date,
      status
    )
    ORDER BY order_date DESC
  ) AS orders
FROM orders
GROUP BY customer_id;
```

**Query:**
```sql
-- Flatten array of struct
SELECT
  customer_id,
  order.order_id,
  order.amount,
  order.order_date
FROM customers,
UNNEST(orders) AS order
WHERE order.status = 'completed';
```

**Filter array elements:**
```sql
SELECT
  customer_id,
  ARRAY(
    SELECT AS STRUCT order_id, amount
    FROM UNNEST(orders) AS order
    WHERE order.status = 'completed'
    ORDER BY amount DESC
    LIMIT 3
  ) AS top_completed_orders
FROM customers;
```

---

### ARRAY Functions

**ARRAY_LENGTH():**
```sql
SELECT
  customer_id,
  ARRAY_LENGTH(order_ids) AS total_orders
FROM customers;
```

**ARRAY_CONCAT():**
```sql
SELECT ARRAY_CONCAT([1, 2], [3, 4], [5]) AS combined;
-- Result: [1, 2, 3, 4, 5]
```

**ARRAY_TO_STRING():**
```sql
SELECT ARRAY_TO_STRING(['apple', 'banana', 'cherry'], ', ') AS fruits;
-- Result: 'apple, banana, cherry'
```

**GENERATE_ARRAY():**
```sql
SELECT GENERATE_ARRAY(1, 10) AS numbers;
-- Result: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

SELECT GENERATE_ARRAY(0, 100, 10) AS multiples_of_10;
-- Result: [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
```

**ARRAY_REVERSE():**
```sql
SELECT ARRAY_REVERSE([1, 2, 3, 4, 5]) AS reversed;
-- Result: [5, 4, 3, 2, 1]
```

---

### Performance: ARRAY vs JOIN

**Traditional approach (2 tables, JOIN):**
```sql
-- Table 1: customers (1M rows)
-- Table 2: orders (10M rows)

SELECT
  c.customer_id,
  c.name,
  o.order_id,
  o.amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE c.customer_id = '12345';

-- Scans: customers (1M) + orders (10M) = 11M rows
-- Join cost: High
```

**Array approach (1 table with ARRAY):**
```sql
-- Table: customers (1M rows with nested orders array)

SELECT
  customer_id,
  name,
  order.order_id,
  order.amount
FROM customers,
UNNEST(orders) AS order
WHERE customer_id = '12345';

-- Scans: customers (1M) only
-- No join cost
-- 50-80% faster for 1:many relationships
```

**When to use ARRAY:**
- 1:many relationships (orders per customer)
- Moderate array size (< 1000 elements)
- Frequent filtering by parent entity
- Want to reduce JOINs

**When NOT to use ARRAY:**
- Many:many relationships
- Very large arrays (> 10,000 elements)
- Need to query array elements independently
- Array elements frequently updated

---

### Complete Example: Denormalized Design

**Traditional normalized:**
```sql
-- 3 tables, 2 JOINs
SELECT
  c.customer_id,
  c.name,
  o.order_id,
  oi.product_id,
  oi.quantity
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id;
```

**Denormalized with ARRAY/STRUCT:**
```sql
-- 1 table, no JOINs
CREATE TABLE customers_denormalized AS
SELECT
  c.customer_id,
  c.name,
  ARRAY_AGG(
    STRUCT(
      o.order_id,
      o.order_date,
      o.status,
      ARRAY(
        SELECT AS STRUCT product_id, quantity, price
        FROM order_items
        WHERE order_id = o.order_id
      ) AS items
    )
    ORDER BY o.order_date DESC
  ) AS orders
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;

-- Query (no JOINs!)
SELECT
  customer_id,
  name,
  order.order_id,
  item.product_id,
  item.quantity
FROM customers_denormalized,
UNNEST(orders) AS order,
UNNEST(order.items) AS item
WHERE customer_id = '12345';
```

**Performance improvement:** 3-5x faster for typical queries.

---

## BigQuery-Specific Features

### EXCEPT and REPLACE in SELECT

**EXCEPT - Exclude columns:**
```sql
-- Select all except sensitive columns
SELECT * EXCEPT(ssn, password, credit_card)
FROM customers;

-- Combine with WHERE
SELECT * EXCEPT(internal_notes)
FROM orders
WHERE status = 'shipped';
```

**REPLACE - Modify columns:**
```sql
-- Replace column values
SELECT * REPLACE(UPPER(name) AS name, ROUND(price, 2) AS price)
FROM products;

-- Anonymize data
SELECT * REPLACE('***' AS ssn, '***' AS credit_card)
FROM customers;
```

**Combine EXCEPT and REPLACE:**
```sql
SELECT * EXCEPT(password) REPLACE(LOWER(email) AS email)
FROM users;
```

---

### SAFE Functions (NULL Instead of Errors)

**SAFE_CAST() - Returns NULL on error:**
```sql
-- Regular CAST throws error on invalid input
SELECT CAST('invalid' AS INT64);  -- ERROR

-- SAFE_CAST returns NULL
SELECT SAFE_CAST('invalid' AS INT64) AS result;  -- NULL
```

**SAFE_DIVIDE() - Returns NULL on division by zero:**
```sql
SELECT
  revenue,
  orders,
  SAFE_DIVIDE(revenue, orders) AS avg_order_value  -- NULL if orders = 0
FROM daily_metrics;
```

**Other SAFE functions:**
```sql
-- SAFE_SUBTRACT (for dates)
SELECT SAFE_SUBTRACT(DATE '2024-01-01', DATE '2024-12-31');  -- NULL (negative)

-- SAFE_NEGATE
SELECT SAFE_NEGATE(9223372036854775807);  -- NULL (overflow)

-- SAFE_ADD
SELECT SAFE_ADD(9223372036854775807, 1);  -- NULL (overflow)
```

**Use case: Data quality checks:**
```sql
SELECT
  COUNT(*) AS total_rows,
  COUNT(SAFE_CAST(amount AS FLOAT64)) AS valid_amounts,
  COUNT(*) - COUNT(SAFE_CAST(amount AS FLOAT64)) AS invalid_amounts
FROM transactions;
```

---

### GROUP BY with Column Numbers

```sql
-- ✅ Valid: Group by column position
SELECT
  customer_id,
  DATE(order_date) AS order_date,
  SUM(amount) AS total
FROM orders
GROUP BY 1, 2;  -- Same as: GROUP BY customer_id, DATE(order_date)

-- ✅ Also valid: Mix names and numbers
SELECT
  customer_id,
  DATE(order_date) AS order_date,
  SUM(amount) AS total
FROM orders
GROUP BY customer_id, 2;
```

**When useful:**
- Long expressions in SELECT
- Complex CASE statements
- Simplifies GROUP BY clause

---

### TABLESAMPLE - Random Sampling

**System sampling (fast, approximate):**
```sql
-- Sample ~10% of data (by blocks)
SELECT * FROM large_table
TABLESAMPLE SYSTEM (10 PERCENT);
```

**Use cases:**
- Quick data exploration
- Testing queries on large tables
- Statistical sampling

**Note:** SYSTEM sampling is block-based, not truly random. For exact percentages, use ROW_NUMBER() with RAND().

---

### PIVOT and UNPIVOT

**PIVOT - Columns to rows:**
```sql
SELECT *
FROM (
  SELECT product, quarter, sales
  FROM quarterly_sales
)
PIVOT (
  SUM(sales)
  FOR quarter IN ('Q1', 'Q2', 'Q3', 'Q4')
);

-- Before:
-- product | quarter | sales
-- A       | Q1      | 100
-- A       | Q2      | 150

-- After:
-- product | Q1  | Q2  | Q3  | Q4
-- A       | 100 | 150 | ... | ...
```

**UNPIVOT - Rows to columns:**
```sql
SELECT *
FROM quarterly_totals
UNPIVOT (
  sales FOR quarter IN (Q1, Q2, Q3, Q4)
);

-- Before:
-- product | Q1  | Q2  | Q3  | Q4
-- A       | 100 | 150 | 200 | 250

-- After:
-- product | quarter | sales
-- A       | Q1      | 100
-- A       | Q2      | 150
```

---

### Standard SQL vs Legacy SQL

**BigQuery has two SQL dialects:**

| Feature | Standard SQL | Legacy SQL |
|---------|-------------|------------|
| **ANSI Compliance** | ✅ Yes | ❌ No |
| **Recommended** | ✅ Yes | ❌ Deprecated |
| **Table Reference** | \`project.dataset.table\` | [project:dataset.table] |
| **CTEs (WITH)** | ✅ Yes | ❌ No |
| **Window Functions** | ✅ Full support | ⚠️ Limited |
| **ARRAY/STRUCT** | ✅ Native | ⚠️ Limited |
| **Portability** | ✅ High | ❌ BigQuery-only |

**How to detect Legacy SQL:**
```sql
-- Legacy SQL indicators:
-- 1. Square brackets for tables
SELECT * FROM [project:dataset.table]

-- 2. GROUP EACH BY
SELECT customer_id, COUNT(*) FROM orders GROUP EACH BY customer_id

-- 3. FLATTEN
SELECT * FROM FLATTEN([project:dataset.table], field)

-- 4. TABLE_DATE_RANGE
SELECT * FROM TABLE_DATE_RANGE([dataset.table_], TIMESTAMP('2024-01-01'), TIMESTAMP('2024-12-31'))
```

**Standard SQL equivalent:**
```sql
-- 1. Backticks
SELECT * FROM `project.dataset.table`

-- 2. Regular GROUP BY
SELECT customer_id, COUNT(*) FROM orders GROUP BY customer_id

-- 3. UNNEST
SELECT * FROM `project.dataset.table`, UNNEST(field)

-- 4. Partitioned table filter
SELECT * FROM `project.dataset.table`
WHERE _PARTITIONTIME BETWEEN TIMESTAMP('2024-01-01') AND TIMESTAMP('2024-12-31')
```

**Migration:**
```bash
# Set default to Standard SQL
bq query --use_legacy_sql=false 'SELECT ...'

# Or in Python
job_config = bigquery.QueryJobConfig(use_legacy_sql=False)
```

---

## Performance Checklist

Before running expensive queries:

1. ☐ Use `--dry_run` to estimate cost
2. ☐ Check if partition pruning is active
3. ☐ Verify clustering on JOIN/WHERE columns
4. ☐ Remove SELECT *
5. ☐ Filter early with WHERE
6. ☐ Use EXPLAIN to analyze plan
7. ☐ Consider materialized views for repeated queries
8. ☐ Test with LIMIT first on full query
9. ☐ Avoid CTE re-execution (use temp tables if referenced 2+ times)
10. ☐ Use NOT EXISTS instead of NOT IN
11. ☐ Batch DML operations (avoid row-by-row updates)
12. ☐ Consider ARRAY/STRUCT for 1:many relationships

## Monitoring Query Performance

```sql
-- Check query statistics
SELECT
  job_id,
  user_email,
  total_bytes_processed,
  total_slot_ms,
  TIMESTAMP_DIFF(end_time, start_time, SECOND) as duration_sec
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
ORDER BY total_bytes_processed DESC
LIMIT 10;
```

## Quick Wins

**Immediate improvements:**
1. Add partition filter → 50-90% cost reduction
2. Remove SELECT * → 30-70% cost reduction
3. Use clustering → 20-50% performance improvement
4. Break complex queries → 2-5x faster execution
5. Enable query cache → Free repeated queries
