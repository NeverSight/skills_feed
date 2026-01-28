---
name: oceanbase-sql-optimization
description: SQL optimization best practices for OceanBase database (MySQL & Oracle modes). Covers query optimization, index usage, execution plan analysis, slow query tuning, and performance optimization techniques. Activates for SQL optimization, query performance, index design, execution plan, slow query, database performance.
license: MIT
metadata:
  audience: developers, database-administrators
  domain: database-optimization
  compatibility: mysql-mode, oracle-mode
---

# OceanBase SQL Optimization Skill

**Expert in SQL query optimization for OceanBase distributed database (MySQL & Oracle modes).**

Provides best practices for writing efficient SQL queries, designing effective indexes, analyzing execution plans, and tuning slow queries in OceanBase. This skill covers both MySQL mode and Oracle mode.

---

## Mode-Specific Syntax Guide

While OceanBase uses the same underlying optimizer for both MySQL and Oracle modes, there are important syntax differences:

| Aspect | MySQL Mode | Oracle Mode |
|--------|-----------|-------------|
| **EXPLAIN Syntax** | `EXPLAIN [INTO table_name] [SET statement_id = string]` | `EXPLAIN [INTO table_name] [SET STATEMENT_ID = 'string']` |
| **System Views** | `oceanbase.GV$OB_SQL_AUDIT` | `GV$OB_SQL_AUDIT` (same name, different schema access) |
| **Data Types** | `BIGINT`, `VARCHAR` | `NUMBER`, `VARCHAR2` |
| **Time Functions** | `TIME_TO_USEC()`, `usec_to_time()` | `TO_DATE()`, `TO_CHAR()` |
| **Schema Access** | `database.table` | `schema.table` |
| **Limit Syntax** | `LIMIT n` | `FETCH FIRST n ROWS ONLY` |
| **String Concatenation** | `CONCAT()` | `\|\|` operator |

**Optimization Principles:**
- ✅ **Same**: Execution plan operators, join algorithms, partition pruning logic
- ✅ **Same**: Index design principles, query rewriting strategies
- ❌ **Different**: Syntax, system view access, data type names, function names

Examples in this skill are marked with mode indicators: **MySQL Mode:** or **Oracle Mode:**

---

## Core Optimization Principles

### 1. Understand Execution Plans

**Always analyze execution plans before optimization:**

**MySQL Mode:**
```sql
obclient [SALES_DB]> EXPLAIN SELECT * FROM order_table WHERE order_date >= '2024-01-01';
```

**Oracle Mode:**
```sql
obclient [SALES_DB]> EXPLAIN SELECT * FROM order_table WHERE order_date >= DATE '2024-01-01';
```

查询结果如下：

```
+------------------------------------------------------------------------------------------------+
| Query Plan                                                                                     |
+------------------------------------------------------------------------------------------------+
| ===========================================                                                    |
| |ID|OPERATOR              |NAME      |EST. ROWS|COST |                                        |
| -------------------------------------------                                                    |
| |0 |TABLE SCAN            |order_table|1000    |1000 |                                        |
| |1 | TABLE GET            |order_table|1000    |1000 |                                        |
+===========================================                                                      |
| Outputs & filters:                                                                             |
| -------------------------------------                                                          |
|   0 - output([order_table.order_id], [order_table.customer_id], [order_table.order_date]),   |
|       filter([order_table.order_date >= '2024-01-01']),                                        |
|       access([order_table.order_id], [order_table.customer_id], [order_table.order_date]),    |
|       partitions(p0)                                                                            |
+------------------------------------------------------------------------------------------------+
```

**Key indicators to check:**
- **EST. ROWS**: Estimated rows processed (lower is better)
- **EST.TIME(us)**: Estimated execution time in microseconds (lower is better)
- **OPERATOR**: Look for `TABLE SCAN` (full table scan, bad) vs `TABLE GET` (index lookup, good)
- **Partitions**: Check if partition pruning is working (e.g., `partitions(p1)` means only one partition accessed)
- **is_index_back**: `false` means no index back, `true` means index back required

### 2. Index Design Best Practices

**Create indexes on frequently queried columns (syntax is the same for both modes):**

```sql
-- ✅ GOOD: Index on WHERE clause column
obclient [SALES_DB]> CREATE INDEX idx_order_date ON order_table(order_date);

-- ✅ GOOD: Composite index for multi-column queries (column order matters)
obclient [SALES_DB]> CREATE INDEX idx_customer_date ON order_table(customer_id, order_date);

-- ✅ GOOD: Unique index for unique constraints
obclient [SALES_DB]> CREATE UNIQUE INDEX idx_order_number ON order_table(order_number);

-- ✅ GOOD: Index with STORING clause for covering index
obclient [SALES_DB]> CREATE INDEX idx_customer_date ON order_table(customer_id, order_date) 
                     STORING (total_amount, status);

-- ❌ BAD: Index on rarely queried columns
obclient [SALES_DB]> CREATE INDEX idx_notes ON order_table(notes);
```

**OceanBase Index Types:**
- **UNIQUE Index**: Ensures uniqueness, fast lookups
- **LOCAL Index**: Partition-local index (default for partitioned tables)
- **GLOBAL Index**: Cross-partition index
- **Function Index**: Index on expressions (e.g., `CREATE INDEX idx_expr ON t1((c1 + c2))`)

**Index selection rules:**
- Index columns used in WHERE clauses
- Index columns used in JOIN conditions
- Consider composite indexes for multi-column filters (column order matters - most selective first)
- Use STORING clause to create covering indexes (avoids index back)
- Avoid over-indexing (each index adds write overhead)
- For partitioned tables, prefer LOCAL indexes unless cross-partition queries are common

### 3. Query Writing Best Practices

**Use specific column lists instead of SELECT \*:**

```sql
-- ✅ GOOD: Select only needed columns
obclient [SALES_DB]> SELECT order_id, customer_id, total_amount 
                     FROM order_table 
                     WHERE order_date >= '2024-01-01';

-- ❌ BAD: Select all columns
obclient [SALES_DB]> SELECT * FROM order_table WHERE order_date >= '2024-01-01';
```

**Use appropriate WHERE conditions:**

```sql
-- ✅ GOOD: Use indexed column in WHERE
obclient [SALES_DB]> SELECT * FROM order_table WHERE order_id = 12345;

-- ✅ GOOD: Use range queries on indexed columns
obclient [SALES_DB]> SELECT * FROM order_table 
                     WHERE order_date BETWEEN '2024-01-01' AND '2024-12-31';

-- ❌ BAD: Function on indexed column prevents index usage
obclient [SALES_DB]> SELECT * FROM order_table WHERE YEAR(order_date) = 2024;

-- ✅ GOOD: Rewrite to use index
obclient [SALES_DB]> SELECT * FROM order_table 
                     WHERE order_date >= '2024-01-01' AND order_date < '2025-01-01';
```

---

## Partition Pruning Optimization

Partition pruning avoids accessing irrelevant partitions, significantly improving SQL execution efficiency. Always check the `partitions` field in the execution plan to verify partition pruning is working.

### Hash Partitioning

**Ensure partition key is in WHERE clause:**

```sql
-- ✅ GOOD: Partition key in WHERE clause enables partition pruning
obclient [SALES_DB]> CREATE TABLE order_table (
                     order_id INT,
                     customer_id INT,
                     order_date DATE
                     ) PARTITION BY HASH(order_id) PARTITIONS 5;

obclient [SALES_DB]> SELECT * FROM order_table WHERE order_id = 12345;
```

查询结果如下：

```
+------------------------------------------------------------------------------------------------+
| Query Plan                                                                                     |
+------------------------------------------------------------------------------------------------+
| =================================================                                              |
| |ID|OPERATOR  |NAME       |EST. ROWS|EST.TIME(us)|                                            |
| -------------------------------------------------                                              |
| |0 |TABLE SCAN|order_table|990      |383         |                                            |
| =================================================                                              |
| Outputs & filters:                                                                             |
| -------------------------------------                                                          |
|   0 - output([order_table.order_id], [order_table.customer_id], [order_table.order_date]),  |
|       filter(nil),                                                                             |
|       access([order_table.order_id], [order_table.customer_id], [order_table.order_date]),   |
|       partitions(p1)  -- Only one partition accessed!                                         |
+------------------------------------------------------------------------------------------------+
```

```sql
-- ❌ BAD: Missing partition key prevents pruning (scans all partitions)
obclient [SALES_DB]> SELECT * FROM order_table WHERE customer_id = 1001;
-- Check execution plan: partitions(p0, p1, p2, p3, p4) - all partitions scanned
```

### Range Partitioning

**Use range conditions that match partition boundaries:**

```sql
-- ✅ GOOD: Range query matches partition boundaries
obclient [SALES_DB]> CREATE TABLE order_table (
                     order_id INT,
                     customer_id INT,
                     order_date DATE
                     ) PARTITION BY RANGE(order_date) (
                     PARTITION p0 VALUES LESS THAN('2024-01-01'),
                     PARTITION p1 VALUES LESS THAN('2024-02-01'),
                     PARTITION p2 VALUES LESS THAN('2024-03-01')
                     );

obclient [SALES_DB]> SELECT * FROM order_table 
                     WHERE order_date >= '2024-01-01' AND order_date < '2024-02-01';
```

查询结果如下：

```
+------------------------------------------------------------------------------------------------+
| Query Plan                                                                                     |
+------------------------------------------------------------------------------------------------+
| =================================================                                              |
| |ID|OPERATOR  |NAME       |EST. ROWS|EST.TIME(us)|                                            |
| -------------------------------------------------                                              |
| |0 |TABLE SCAN|order_table|1        |46          |                                            |
| =================================================                                              |
| Outputs & filters:                                                                             |
| -------------------------------------                                                          |
|   0 - output([order_table.order_id], [order_table.customer_id], [order_table.order_date]),  |
|       filter([order_table.order_date >= '2024-01-01'], [order_table.order_date < '2024-02-01']),
|       access([order_table.order_id], [order_table.customer_id], [order_table.order_date]),   |
|       partitions(p1)  -- Only partition p1 accessed!                                        |
+------------------------------------------------------------------------------------------------+
```

```sql
-- ❌ BAD: Function prevents partition pruning
obclient [SALES_DB]> SELECT * FROM order_table WHERE MONTH(order_date) = 1;
-- Check execution plan: partitions(p0, p1, p2) - all partitions scanned

-- ✅ GOOD: Rewrite to use partition pruning
obclient [SALES_DB]> SELECT * FROM order_table 
                     WHERE order_date >= '2024-01-01' AND order_date < '2024-02-01';
```

**Partition Pruning Rules:**
- For Hash/List partitions: Partition key must be in WHERE clause with equality or IN conditions
- For Range partitions: Use range conditions that match partition boundaries
- Avoid functions on partition keys in WHERE clauses
- For expressions as partition keys, the expression must appear as a whole in WHERE clause

---

## Join Optimization

OceanBase supports three join algorithms: **Nested Loop Join (NLJ)**, **Hash Join (HJ)**, and **Merge Join (MJ)**. The optimizer automatically selects the best algorithm based on statistics and cost estimation.

### Join Algorithms

**1. Nested Loop Join (NLJ)**
- Best for: Small outer table, indexed inner table
- Use when: Join condition has index on inner table
- Hint: `/*+ USE_NL(table1, table2) */`

```sql
-- ✅ GOOD: NLJ with indexed join column
obclient [SALES_DB]> CREATE INDEX idx_customer_id ON order_table(customer_id);

obclient [SALES_DB]> EXPLAIN SELECT /*+USE_NL(c, o)*/ o.order_id, c.customer_name 
                     FROM customer_table c
                     INNER JOIN order_table o ON c.customer_id = o.customer_id
                     WHERE c.customer_type = 'VIP';
```

查询结果如下：

```
+------------------------------------------------------------------------------------------------+
| Query Plan                                                                                     |
+------------------------------------------------------------------------------------------------+
| ===========================================                                                    |
| |ID|OPERATOR        |NAME  |EST. ROWS|EST.TIME(us)|                                           |
| -------------------------------------------                                                    |
| |0 |NESTED-LOOP JOIN|      |990      |37346       |                                           |
| |1 | TABLE SCAN     |c     |999      |669         |                                           |
| |2 | TABLE GET      |o     |1        |36          |  -- Index lookup!                         |
| ===========================================                                                    |
| Outputs & filters:                                                                             |
| -------------------------------------                                                          |
|   0 - output([o.order_id], [c.customer_name]), filter(nil),                                   |
|       conds(nil), nl_params_([c.customer_id])                                                 |
|   1 - output([c.customer_id], [c.customer_name]), filter([c.customer_type = 'VIP']),         |
|       access([c.customer_id], [c.customer_name]), partitions(p0)                             |
|   2 - output([o.order_id]), filter(nil),                                                      |
|       access([o.order_id]), partitions(p0),                                                    |
|       range_key([o.customer_id]), range([? = o.customer_id])  -- Index used!                  |
+------------------------------------------------------------------------------------------------+
```

**2. Hash Join (HJ)**
- Best for: Large datasets, equal join conditions
- Use when: Both tables are large and join condition is equality
- Hint: `/*+ USE_HASH(table1, table2) */`

```sql
-- ✅ GOOD: Hash Join for large table joins
obclient [SALES_DB]> EXPLAIN SELECT /*+USE_HASH(o, c)*/ o.order_id, c.customer_name 
                     FROM order_table o
                     INNER JOIN customer_table c ON o.customer_id = c.customer_id;
```

查询结果如下：

```
+------------------------------------------------------------------------------------------------+
| Query Plan                                                                                     |
+------------------------------------------------------------------------------------------------+
| =======================================                                                        |
| |ID|OPERATOR   |NAME|EST. ROWS|EST.TIME(us)|                                                   |
| ---------------------------------------                                                        |
| |0 |HASH JOIN  |    |98010000 |66774608    |                                                   |
| |1 | TABLE SCAN|o   |100000   |68478       |                                                   |
| |2 | TABLE SCAN|c   |100000   |68478       |                                                   |
| =======================================                                                        |
| Outputs & filters:                                                                             |
| -------------------------------------                                                          |
|   0 - output([o.order_id], [c.customer_name]), filter(nil),                                    |
|       equal_conds([o.customer_id = c.customer_id]), other_conds(nil)                           |
+------------------------------------------------------------------------------------------------+
```

**3. Merge Join (MJ)**
- Best for: Pre-sorted data, ordered results needed
- Use when: Both inputs are already sorted or can be sorted efficiently
- Hint: `/*+ USE_MERGE(table1, table2) */`

```sql
-- ✅ GOOD: Merge Join when data is sorted
obclient [SALES_DB]> EXPLAIN SELECT /*+USE_MERGE(o, c)*/ o.order_id, c.customer_name 
                     FROM order_table o
                     INNER JOIN customer_table c ON o.customer_id = c.customer_id
                     ORDER BY o.customer_id;
```

### Join Order

**Use LEADING hint to control join order:**

```sql
-- ✅ GOOD: Control join order explicitly
obclient [SALES_DB]> SELECT /*+LEADING(c, o)*/ o.order_id, c.customer_name 
                     FROM customer_table c
                     INNER JOIN order_table o ON c.customer_id = o.customer_id
                     WHERE c.customer_type = 'VIP'
                     AND o.order_date >= '2024-01-01';

-- ❌ BAD: Let optimizer choose suboptimal order
obclient [SALES_DB]> SELECT o.order_id, c.customer_name 
                     FROM order_table o
                     INNER JOIN customer_table c ON o.customer_id = c.customer_id
                     WHERE c.customer_type = 'VIP';
```

### Index on Join Columns

**Always index foreign key columns:**

```sql
-- ✅ GOOD: Index on join column enables efficient joins
obclient [SALES_DB]> CREATE INDEX idx_customer_id ON order_table(customer_id);

-- Then join queries can use index (NLJ with TABLE GET)
obclient [SALES_DB]> SELECT o.*, c.customer_name 
                     FROM order_table o
                     INNER JOIN customer_table c ON o.customer_id = c.customer_id;
```

---

## Aggregation Optimization

### Use Appropriate Aggregation Functions

```sql
-- ✅ GOOD: COUNT(*) is optimized
obclient [SALES_DB]> SELECT COUNT(*) FROM order_table WHERE order_date >= '2024-01-01';

-- ✅ GOOD: COUNT(column) when you need non-NULL count
obclient [SALES_DB]> SELECT COUNT(customer_id) FROM order_table;

-- ❌ BAD: COUNT(DISTINCT) on large datasets can be slow
obclient [SALES_DB]> SELECT COUNT(DISTINCT customer_id) FROM order_table;

-- ✅ GOOD: Use GROUP BY with LIMIT (MySQL) or FETCH FIRST (Oracle) for top N
-- MySQL Mode:
obclient [SALES_DB]> SELECT customer_id, SUM(total_amount) AS total
                     FROM order_table
                     GROUP BY customer_id
                     ORDER BY total DESC
                     LIMIT 10;

-- Oracle Mode:
obclient [SALES_DB]> SELECT customer_id, SUM(total_amount) AS total
                     FROM order_table
                     GROUP BY customer_id
                     ORDER BY total DESC
                     FETCH FIRST 10 ROWS ONLY;
```

---

## Subquery Optimization

### Convert Correlated Subqueries to JOINs

```sql
-- ❌ BAD: Correlated subquery (executes for each row)
obclient [SALES_DB]> SELECT o.order_id, o.total_amount
                     FROM order_table o
                     WHERE o.total_amount > (
                         SELECT AVG(total_amount) 
                         FROM order_table 
                         WHERE customer_id = o.customer_id
                     );

-- ✅ GOOD: Convert to JOIN
obclient [SALES_DB]> SELECT o.order_id, o.total_amount
                     FROM order_table o
                     INNER JOIN (
                         SELECT customer_id, AVG(total_amount) as avg_amount
                         FROM order_table
                         GROUP BY customer_id
                     ) avg_orders ON o.customer_id = avg_orders.customer_id
                     WHERE o.total_amount > avg_orders.avg_amount;
```

### Use EXISTS instead of IN for large datasets

**Syntax is the same for both modes:**

```sql
-- ✅ GOOD: EXISTS stops at first match
obclient [SALES_DB]> SELECT * FROM order_table o
                     WHERE EXISTS (
                         SELECT 1 FROM customer_table c
                         WHERE c.customer_id = o.customer_id
                         AND c.customer_type = 'VIP'
                     );

-- ⚠️ OK: IN works but may be slower for large lists
obclient [SALES_DB]> SELECT * FROM order_table
                     WHERE customer_id IN (SELECT customer_id FROM customer_table WHERE customer_type = 'VIP');
```

---

## Slow Query Tuning

### Enable SQL Audit

**Configure SQL Audit settings:**

```sql
-- Enable SQL Audit
obclient> ALTER SYSTEM SET enable_sql_audit = true;

-- Set SQL Audit memory percentage (default: 3%, range: [0,80])
obclient> SET GLOBAL ob_sql_audit_percentage = 3;
```

### Identify Slow Queries

**Query TOP SQL by CPU usage:**

**MySQL Mode:** Use `oceanbase.GV$OB_SQL_AUDIT` with `TIME_TO_USEC(NOW())`  
**Oracle Mode:** Use `GV$OB_SQL_AUDIT` with `SYSDATE - INTERVAL '30' MINUTE`

```sql
-- Find TOP SQL by CPU usage in last 30 minutes
obclient> SELECT sql_id, COUNT(*) AS executions, SUM(execute_time) AS tot_cpu_time,
                AVG(execute_time) AS avg_cpu_time,
                SUM(execute_time)/(30*60*1000*1000) AS cpu_cnt, query_sql
         FROM oceanbase.GV$OB_SQL_AUDIT  -- MySQL: add 'oceanbase.' prefix
         WHERE tenant_id = 'mysql001'  -- MySQL: string, Oracle: number
           AND request_time BETWEEN (TIME_TO_USEC(NOW())-30*60*1000*1000) AND TIME_TO_USEC(NOW())  -- MySQL
           -- Oracle: BETWEEN (SYSDATE - INTERVAL '30' MINUTE) AND SYSDATE
           AND is_executor_rpc = 0
         GROUP BY sql_id
         HAVING COUNT(*) > 1
         ORDER BY cpu_cnt DESC
         LIMIT 10;  -- MySQL: LIMIT, Oracle: FETCH FIRST 10 ROWS ONLY
```

**Query slow queries by execution time:**

**MySQL Mode:** Use `usec_to_time()` function  
**Oracle Mode:** Use `TO_CHAR()` function

```sql
-- Find queries with execution time > 100ms
obclient> SELECT request_id,
                usec_to_time(request_time) AS request_time,  -- MySQL
                -- TO_CHAR(request_time, 'YYYY-MM-DD HH24:MI:SS.FF') AS request_time,  -- Oracle
                elapsed_time, queue_time, execute_time, flt_trace_id, query_sql
         FROM oceanbase.v$ob_sql_audit  -- MySQL: add 'oceanbase.' prefix
         WHERE elapsed_time > 100000  -- > 100ms in microseconds
         ORDER BY elapsed_time DESC
         LIMIT 10;  -- MySQL: LIMIT, Oracle: FETCH FIRST 10 ROWS ONLY
```

### Analyze Query Performance

**Get detailed execution statistics:**

**MySQL Mode:** Use `oceanbase.gv$ob_sql_audit`  
**Oracle Mode:** Use `GV$OB_SQL_AUDIT` (no schema prefix)

```sql
-- Get detailed statistics for a specific SQL
obclient> SELECT sql_id, query_sql, executions, elapsed_time, execute_time,
                queue_time, return_rows, affected_rows, partition_cnt,
                table_scan, is_hit_plan, plan_id
         FROM oceanbase.gv$ob_sql_audit  -- MySQL: add 'oceanbase.' prefix
         WHERE sql_id = 'your_sql_id'
         ORDER BY elapsed_time DESC;
```

**Get execution plan for slow query:**

**MySQL Mode:** Use `oceanbase.GV$OB_PLAN_CACHE_PLAN_STAT`  
**Oracle Mode:** Use `GV$OB_PLAN_CACHE_PLAN_STAT` (no schema prefix)

```sql
-- Get execution plan from plan cache
obclient> SELECT tenant_id, svr_ip, svr_port, sql_id, plan_id,
                last_active_time, first_load_time, outline_data
         FROM oceanbase.GV$OB_PLAN_CACHE_PLAN_STAT  -- MySQL: add 'oceanbase.' prefix
         WHERE tenant_id = 1002 AND sql_id = 'your_sql_id'
           AND svr_ip = 'xxx.xxx.xxx.xxx' AND svr_port = 35046;

-- Get plan details
obclient> SELECT operator, name, rows, cost
         FROM oceanbase.GV$OB_PLAN_CACHE_PLAN_EXPLAIN  -- MySQL: add 'oceanbase.' prefix
         WHERE tenant_id = 1002 AND plan_id = 741
           AND svr_ip = 'xxx.xxx.xxx.xxx' AND svr_port = 35046;
```

### Find Currently Running Slow Queries

**MySQL Mode:**
```sql
obclient> SELECT user, tenant, sql_id, concat(time, 's') AS time, info,
                svr_ip, svr_port, trace_id
         FROM oceanbase.GV$OB_PROCESSLIST
         WHERE state = 'ACTIVE' ORDER BY time DESC LIMIT 10;
```

**Oracle Mode:**
```sql
obclient> SELECT user_name, tenant_name, sql_id, time || 's' AS time, info,
                svr_ip, svr_port, trace_id
         FROM GV$OB_PROCESSLIST
         WHERE state = 'ACTIVE' ORDER BY time DESC FETCH FIRST 10 ROWS ONLY;
```

---

## Real-World Optimization Case

### Case: Type Conversion Preventing Index Usage

**Problem:** SQL execution time was 2 seconds, CPU usage exceeded 70% of server resources.

**Root Cause Analysis:**

1. **Identify TOP SQL:**
   ```sql
   obclient> SELECT sql_id, COUNT(*) AS executions, AVG(execute_time) AS avg_cpu_time
            FROM oceanbase.GV$OB_SQL_AUDIT
            WHERE tenant_id = 'mysql001'
              AND request_time BETWEEN (TIME_TO_USEC(NOW())-30*60*1000*1000) AND TIME_TO_USEC(NOW())
            GROUP BY sql_id
            ORDER BY SUM(execute_time) DESC
            LIMIT 1;
   ```

2. **Analyze Execution Plan:**
   ```sql
   obclient> EXPLAIN SELECT ... FROM v_tt01 WHERE COL001 IN (20017476);
   ```
   
   Execution plan showed:
   - High cost on `TBL3(IDX_TBL3_COL170)` index scan
   - `range(MIN,MIN ; MAX,MAX)always true` - index not used for matching
   - `filter([20017476 = cast(cast(TBL3.COL170, VARCHAR2(20 BYTE)), NUMBER)])` - type conversion happening

3. **Root Cause:**
   - View `V_TT01` had `TO_NUMBER` conversion on `COL001`
   - Table `TBL3.COL170` was `VARCHAR2(20)` but compared with `NUMBER`
   - Type conversion prevented index usage

**Optimization Steps:**

1. **Remove unnecessary TO_NUMBER conversion:**
   ```sql
   -- Before: View had TO_NUMBER conversion
   CREATE VIEW V_TT01_OLD AS
   SELECT To_number("tt01"."col001") AS "COL001", ...
   
   -- After: Remove TO_NUMBER (COL001 is already NUMBER)
   CREATE VIEW V_TT01 AS
   SELECT "tt01"."col001" AS "COL001", ...
   ```
   Result: SQL RT reduced from 2s to 150ms

2. **Unify data types:**
   ```sql
   -- Before: TBL3.COL170 was VARCHAR2(20)
   CREATE TABLE TBL3 (
     COL170 VARCHAR2(20) NOT NULL,
     ...
   );
   
   -- After: Change to NUMBER(20) to match join condition
   ALTER TABLE TBL3 MODIFY COL170 NUMBER(20) NOT NULL;
   ```
   Result: SQL RT further reduced to 20ms

3. **Partition and table group optimization:**
   ```sql
   -- Add hash partitioning on join keys
   ALTER TABLE TBL1 PARTITION BY HASH(COL001) PARTITIONS 8;
   ALTER TABLE TBL2 PARTITION BY HASH(COL004) PARTITIONS 8;
   ALTER TABLE TBL3 PARTITION BY HASH(COL170) PARTITIONS 8;
   ALTER TABLE TT01 PARTITION BY HASH(COL001) PARTITIONS 8;
   
   -- Create table group to avoid cross-partition joins
   CREATE TABLEGROUP order_tg PARTITION BY HASH(COL001) PARTITIONS 8;
   ALTER TABLE TBL1 SET TABLEGROUP order_tg;
   ALTER TABLE TBL2 SET TABLEGROUP order_tg;
   ALTER TABLE TBL3 SET TABLEGROUP order_tg;
   ALTER TABLE TT01 SET TABLEGROUP order_tg;
   ```
   Result: SQL RT further reduced to 4ms

**Final Execution Plan:** Shows `PX PARTITION ITERATOR` (partition pruning working) and `TABLE SCAN` with index `INDEX_TBL3_COL170` (index used efficiently)

**Key Learnings:**
- Always check execution plan for type conversions in filters
- Ensure join column data types match
- Use partition pruning and table groups for distributed queries
- Remove unnecessary type conversions in views

---

## Common Anti-patterns

### ❌ Avoid These Patterns

**1. N+1 Query Problem:**
```sql
-- ❌ BAD: Multiple queries in loop
-- Instead, use JOIN or batch queries
```

**2. SELECT * in Production:**
```sql
-- ❌ BAD: SELECT * returns unnecessary data
SELECT * FROM order_table;

-- ✅ GOOD: Select only needed columns
SELECT order_id, customer_id, total_amount FROM order_table;
```

**3. Functions on Indexed Columns:**
```sql
-- ❌ BAD: Prevents index usage
WHERE UPPER(customer_name) = 'JOHN'

-- ✅ GOOD: Store normalized data or use function-based index
WHERE customer_name = 'JOHN'
```

**4. Implicit Type Conversions:**
```sql
-- ❌ BAD: String to number conversion
WHERE order_id = '12345'

-- ✅ GOOD: Match data types
WHERE order_id = 12345
```

---

## Performance Monitoring

### Key Metrics to Monitor

```sql
-- Check table statistics
obclient [SALES_DB]> ANALYZE TABLE order_table;

-- View table size and row count
obclient [SALES_DB]> SELECT 
                         table_name,
                         table_rows,
                         data_length,
                         index_length
                     FROM information_schema.tables
                     WHERE table_schema = 'SALES_DB';

-- Check index usage
obclient [SALES_DB]> SHOW INDEX FROM order_table;
```

---

## Optimization Checklist

Before deploying SQL queries to production:

- [ ] Execution plan reviewed (EXPLAIN)
- [ ] Appropriate indexes created
- [ ] Partition pruning enabled (if partitioned)
- [ ] SELECT columns limited to needed fields
- [ ] WHERE conditions use indexed columns
- [ ] JOIN conditions indexed
- [ ] Subqueries optimized (JOINs preferred)
- [ ] Aggregations use efficient functions
- [ ] No functions on indexed columns in WHERE
- [ ] Data types match in comparisons
- [ ] Query tested with production-like data volume

---

## Quick Reference

### Execution Plan Operators

| Operator | Meaning | Optimization |
|----------|---------|--------------|
| TABLE SCAN / TABLE FULL SCAN | Full table scan | Add index or use partition key |
| TABLE RANGE SCAN | Range scan on table | ✅ Good, but consider index |
| TABLE GET | Direct row access via primary key | ✅ Best |
| HASH JOIN | Hash join algorithm | ✅ Good for large equal joins |
| NESTED-LOOP JOIN | Nested loop join | ✅ Good for small outer table with indexed inner |
| MERGE JOIN | Merge join algorithm | ✅ Good for pre-sorted data |
| SORT | Sorting operation | Add ORDER BY index or use sorted index |
| AGGREGATE | Aggregation | Consider materialized views |
| PX PARTITION ITERATOR | Parallel partition iterator | ✅ Good, partition pruning working |
| EXCHANGE OUT DISTR | Distributed exchange | Indicates distributed execution |

### Index Types

- **Primary Key**: Automatically indexed, unique
- **Unique Index**: Ensures uniqueness, fast lookups
- **Composite Index**: Multiple columns, order matters
- **Covering Index**: Contains all query columns
