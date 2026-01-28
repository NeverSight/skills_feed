---
name: oceanbase-schema-design
description: Schema design best practices for OceanBase database (MySQL & Oracle modes). Covers table design, partitioning strategies, table groups, index design, and schema optimization principles. Activates for schema design, table design, partition design, index design, database design, DDL.
license: MIT
metadata:
  audience: developers, database-administrators, database-designers
  domain: database-schema-design
  compatibility: mysql-mode, oracle-mode
---

# OceanBase Schema Design Skill

**Expert in database schema design for OceanBase distributed database (MySQL & Oracle modes).**

Provides best practices for designing efficient table structures, partitioning strategies, table groups, indexes, and schema optimization in OceanBase. This skill covers both MySQL mode and Oracle mode.

---

## Mode-specific syntax guide

While OceanBase uses the same underlying storage and partitioning mechanisms for both MySQL and Oracle modes, there are important syntax differences:

| Aspect | MySQL Mode | Oracle Mode |
|--------|-----------|-------------|
| **Data Types** | `BIGINT`, `VARCHAR`, `DATETIME` | `NUMBER`, `VARCHAR2`, `DATE`, `TIMESTAMP` |
| **Schema Access** | `database.table` | `schema.table` |
| **Default Index** | LOCAL (for partitioned tables) | GLOBAL (for partitioned tables) |
| **Time Functions** | `NOW()`, `CURRENT_TIMESTAMP` | `SYSDATE`, `SYSTIMESTAMP` |
| **String Functions** | `CONCAT()` | `\|\|` operator |

**Design Principles:**
- ✅ **Same**: Partitioning types, table group concepts, index types
- ✅ **Same**: Design best practices, normalization principles
- ❌ **Different**: Data type names, default index behavior, function syntax

Examples in this skill are marked with mode indicators: **MySQL Mode:** or **Oracle Mode:**

---

## Table design fundamentals

### Database normalization

**Three Normal Forms:**
- **1NF**: All field values must be atomic (indivisible)
- **2NF**: Every column must be fully dependent on the primary key
- **3NF**: No transitive dependencies (columns must be directly dependent on primary key)

**Important:** Schema design should prioritize business performance over strict normalization. Appropriate data redundancy is acceptable to reduce table joins and improve performance. Redundancy fields should not be frequently modified and not be very long VARCHAR fields.

### Table structure design standards

**1. Primary key design:**

```sql
-- ✅ GOOD: Use business fields as primary key
obclient [SALES_DB]> CREATE TABLE order_table (
                     order_id BIGINT PRIMARY KEY,
                     customer_id BIGINT NOT NULL,
                     gmt_create TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- MySQL: CURRENT_TIMESTAMP, Oracle: SYSDATE
                     gmt_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                     ) COMMENT='Order table';

-- ✅ GOOD: Composite primary key
obclient [SALES_DB]> CREATE TABLE order_item_table (
                     order_id BIGINT,
                     item_id BIGINT,
                     PRIMARY KEY (order_id, item_id)
                     );
```

**Key points:**
- OceanBase uses Index-Organized Table (IOT) model
- If no primary key is specified, system automatically generates a hidden primary key
- Recommend using business fields as primary key (avoid auto-increment)
- Include required fields: `gmt_create`, `gmt_modified`
- All fields should have `COMMENT` attributes and be `NOT NULL` with appropriate `DEFAULT` values
- Use `TINYINT UNSIGNED` for boolean fields (1=yes, 0=no)
- Join fields must have consistent data types to avoid implicit conversion

---

## Partition design

### When to use partitioning

**Use partitioning when:**
- Data volume is large and access is concentrated
- Table is a history table or transaction log table
- Table has obvious access hotspots
- Need to improve query performance through partition pruning

### Partition key selection

**Critical Rule:**
- For partitioned tables, every primary key and unique key must include at least one field that is part of the partition key

**Partition key selection principles:**

- **Hash partition**: Choose high cardinality field that appears most frequently in WHERE clauses (e.g., User ID, Order ID)
- **Range/List partition**: Choose fields based on business rules (e.g., time-based for log tables), partition count should not be too small

```sql
-- ✅ GOOD: Hash partition on high-cardinality field
obclient [SALES_DB]> CREATE TABLE order_table (
                     order_id BIGINT PRIMARY KEY,
                     customer_id BIGINT,
                     order_date DATE
                     ) PARTITION BY HASH(order_id) PARTITIONS 8;

-- ✅ GOOD: Range partition for time-based data
obclient [SALES_DB]> CREATE TABLE order_log_table (
                     log_id BIGINT,
                     log_date DATE NOT NULL,
                     PRIMARY KEY (log_id, log_date)
                     ) PARTITION BY RANGE COLUMNS(log_date) (
                     PARTITION p202401 VALUES LESS THAN('2024-02-01'),
                     PARTITION p202402 VALUES LESS THAN('2024-03-01'),
                     PARTITION pMAX VALUES LESS THAN MAXVALUE
                     );
```

**Limitations:** Hash partition is not suitable for range queries on partition key. Range partition is better for time-based queries.

### Partition types

**Supported partition types:**

- **Hash**: Even data distribution, point queries (high cardinality field)
- **Range**: Time-based data, historical data (date or numeric with clear ranges)
- **List**: Discrete value sets (field with limited distinct values)
- **Key**: Similar to Hash, uses MySQL's internal hashing function
- **Composite**: Combines two partition types (e.g., Hash + Range)

```sql
-- Hash partition
obclient [SALES_DB]> CREATE TABLE order_table (
                     order_id BIGINT PRIMARY KEY,
                     customer_id BIGINT
                     ) PARTITION BY HASH(order_id) PARTITIONS 8;

-- Range partition
obclient [SALES_DB]> CREATE TABLE order_table (
                     order_id BIGINT,
                     order_date DATE NOT NULL,
                     PRIMARY KEY (order_id, order_date)
                     ) PARTITION BY RANGE COLUMNS(order_date) (
                     PARTITION p2024Q1 VALUES LESS THAN('2024-04-01'),
                     PARTITION p2024Q2 VALUES LESS THAN('2024-07-01'),
                     PARTITION pMAX VALUES LESS THAN MAXVALUE
                     );

-- Composite partition (Hash + Range)
obclient [SALES_DB]> CREATE TABLE order_table (
                     order_id BIGINT,
                     customer_id BIGINT,
                     order_date DATE NOT NULL,
                     PRIMARY KEY (order_id, customer_id, order_date)
                     ) PARTITION BY HASH(customer_id) PARTITIONS 8
                     SUBPARTITION BY RANGE COLUMNS(order_date) (
                     PARTITION p0 (
                         SUBPARTITION sp0_q1 VALUES LESS THAN('2024-04-01'),
                         SUBPARTITION sp0_q2 VALUES LESS THAN('2024-07-01')
                     )
                     -- ... more partitions
                     );
```

### Partition pruning

**Partition pruning** avoids accessing irrelevant partitions, significantly improving SQL execution efficiency.

**Rules:**
- **Hash/List**: Partition key must be in WHERE clause with equality or IN conditions
- **Range**: Use range conditions that match partition boundaries, avoid functions on partition keys

```sql
-- ✅ GOOD: Partition pruning works
obclient [SALES_DB]> SELECT * FROM order_table WHERE order_id = 12345;
-- Execution plan shows: partitions(p1) - only one partition accessed

-- ❌ BAD: No partition pruning (missing partition key or function on partition key)
obclient [SALES_DB]> SELECT * FROM order_table WHERE customer_id = 1001;
-- Execution plan shows: all partitions scanned
```

---

## Table group design

### Table group overview

**Table Group** is a logical concept representing a collection of tables. It controls the physical storage proximity of related tables to enable **Partition Wise Join**.

### SHARDING attributes

**1. SHARDING = 'NONE':** All partitions co-located on same machine, no partition restrictions

**2. SHARDING = 'PARTITION':** Tables sharded by first-level partitions, all tables must have identical first-level partition definitions

**3. SHARDING = 'ADAPTIVE' (Default):** Tables sharded adaptively, enables Partition Wise Join for both first-level and second-level partitions

**Use table groups when:** Multiple tables are frequently joined together, tables have related partition keys, need to avoid cross-partition joins

```sql
-- Create table group and add tables
obclient [SALES_DB]> CREATE TABLEGROUP order_tg SHARDING = 'PARTITION'
                     PARTITION BY HASH(customer_id) PARTITIONS 8;

obclient [SALES_DB]> CREATE TABLE order_table (
                     order_id BIGINT,
                     customer_id BIGINT,
                     PRIMARY KEY (order_id, customer_id)
                     ) PARTITION BY HASH(customer_id) PARTITIONS 8;

obclient [SALES_DB]> ALTER TABLE order_table SET TABLEGROUP order_tg;
-- Now JOIN queries can use Partition Wise Join
```

---

## Index design

### Index types

**1. Local Index (LOCAL):**
- Index data stored with table partition data
- Default for MySQL mode partitioned tables
- Better for DML performance, preferred choice

**2. Global Index (GLOBAL):**
- Index separately partitioned
- Default for Oracle mode partitioned tables
- May cause distributed transactions, use only when necessary

```sql
-- MySQL Mode: Default is LOCAL
obclient [SALES_DB]> CREATE INDEX idx_customer_date ON order_table(customer_id, order_date);
-- Creates LOCAL index by default

-- Create GLOBAL index explicitly
obclient [SALES_DB]> CREATE INDEX idx_customer_date ON order_table(customer_id, order_date) GLOBAL;
```

### Index design principles

**1. Leftmost prefix principle:** Index must match query pattern from leftmost column

```sql
-- ✅ GOOD: Index matches query
obclient [SALES_DB]> CREATE INDEX idx_customer_date ON order_table(customer_id, order_date);
obclient [SALES_DB]> SELECT * FROM order_table 
                     WHERE customer_id = 1001 AND order_date >= '2024-01-01';

-- ❌ BAD: Missing leftmost column prevents index usage
obclient [SALES_DB]> SELECT * FROM order_table WHERE order_date >= '2024-01-01';
-- Execution plan shows: TABLE SCAN (full table scan)
```

**2. Composite index column order:** Place high cardinality columns first

```sql
-- ✅ GOOD: High cardinality column first
obclient [SALES_DB]> CREATE INDEX idx_customer_date ON order_table(customer_id, order_date);
```

**3. Covering index:** Include all query columns to avoid table lookup

```sql
obclient [SALES_DB]> CREATE INDEX idx_customer_date_amount ON order_table(customer_id, order_date) 
                     STORING (total_amount, status);
```

**4. ORDER BY optimization:** Index can support ORDER BY if WHERE conditions match leftmost columns

**5. Join field indexes:** Always index join columns for efficient joins

### Index design best practices

**General principles:**
- Indexed fields should be `NOT NULL` with appropriate `DEFAULT` values
- Business-unique fields should be primary keys
- Join fields must have consistent data types
- Place high cardinality columns first in composite indexes
- Use single composite index instead of multiple single-column indexes
- Add ORDER BY/GROUP BY columns to index for covering index

**Partitioned table index:**
- Prefer LOCAL index → Global partitioned index → Global index
- Reduce unnecessary global indexes (high maintenance cost)
- Primary key must include partition key

**Index maintenance:**
- Confirm new index is effective before deploying SQL
- Index modification: Create new index → Verify → Delete old index
- Delete unused indexes to avoid index bloat
- Never mix `ALTER TABLE ADD INDEX` and `DROP INDEX` in one DDL

**Common mistakes to avoid:**
- ❌ Creating one index per query
- ❌ Believing indexes severely slow down updates
- ❌ Using "check then insert" instead of unique indexes
- ❌ Creating redundant indexes (e.g., idx_abc already covers idx_a and idx_ab)

---

## Schema design checklist

Before deploying a table schema to production:

- [ ] Primary key defined (preferably business fields)
- [ ] Required fields included (gmt_create, gmt_modified)
- [ ] All fields have COMMENT attributes and are NOT NULL with DEFAULT values
- [ ] Join fields have consistent data types
- [ ] Partition key selected appropriately and included in primary key/unique key
- [ ] Table group created if tables are frequently joined
- [ ] Indexes designed following leftmost prefix principle, on join columns
- [ ] LOCAL index preferred for partitioned tables, no redundant indexes
- [ ] Schema tested with production-like data volume

---

## Quick reference

**Partition types:** Hash (even distribution, point queries) | Range (time-based data) | List (discrete value sets) | Key (similar to Hash) | Composite (two partition types)

**Table group SHARDING:** NONE (no restriction) | PARTITION (first-level partitions must match) | ADAPTIVE (all first-level or all second-level must match)

**Index types:** LOCAL (default MySQL, better DML performance) | GLOBAL (default Oracle, cross-partition queries)
