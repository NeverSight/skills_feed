---
name: oceanbase-examples
description: Create SQL examples for OceanBase documentation with proper formatting, meaningful names, and separated results. Use when writing or reviewing example sections in OceanBase documentation.
license: MIT
metadata:
  audience: technical-writers
  domain: documentation-examples
---

# OceanBase Documentation Examples

This skill provides guidelines for creating SQL examples in OceanBase documentation.

## Example structure

### SQL statements

**Always prefix with prompt:**

- `obclient>` for default prompt
- `obclient [SCHEMA]>` when schema context is relevant

**Include semicolons** in executable statements.

**Example:**

```sql
obclient [KILL_USER]> SHOW PROCESSLIST;
```

### Query results

**Separate from SQL statements:**

- Place SQL in one code block
- Place results in another code block
- Connect with descriptive text like "查询结果如下：" or "Query results:"

**Example:**

```sql
obclient [KILL_USER]> SHOW PROCESSLIST;
```

查询结果如下：

```
+------------+-----------+----------------------+-----------+---------+------+--------+------------------+
| ID         | USER      | HOST                 | DB        | COMMAND | TIME | STATE  | INFO             |
+------------+-----------+----------------------+-----------+---------+------+--------+------------------+
| 3221487726 | KILL_USER | 100.xx.xxx.xxx:34803 | KILL_USER | Query   |    0 | ACTIVE | SHOW PROCESSLIST |
+------------+-----------+----------------------+-----------+---------+------+--------+------------------+
1 row in set
```

## Naming conventions

### Use meaningful names

**Avoid simple names:**

- ❌ `t1`, `t2`, `tg1`, `db1`
- ❌ `test_table`, `temp_db`

**Use business-meaningful names:**

- ✅ Table groups: `order_tg`, `product_tg`, `inventory_tg`
- ✅ Tables: `order_table`, `user_info`, `product_catalog`
- ✅ Databases: `sales_db`, `customer_db`, `warehouse_db`

**Why:**

- Helps users understand real-world scenarios
- Makes examples more relatable
- Demonstrates practical applications

### Example scenarios

**E-commerce:**

- Tables: `orders`, `order_items`, `customers`, `products`
- Table groups: `order_tg`, `product_tg`
- Databases: `ecommerce_db`

**Financial:**

- Tables: `transactions`, `accounts`, `balances`
- Table groups: `transaction_tg`, `account_tg`
- Databases: `banking_db`

**Inventory:**

- Tables: `warehouses`, `inventory_items`, `stock_movements`
- Table groups: `warehouse_tg`, `inventory_tg`
- Databases: `logistics_db`

## What to include

### Include:

- ✅ Query result tables (when helpful)
- ✅ Error messages (when demonstrating error handling)
- ✅ Descriptive output (when it adds value)

### Exclude:

- ❌ "Query OK" messages
- ❌ "Query OK, 0 rows affected"
- ❌ "Query OK, 1 row affected"
- ❌ Generic success messages

**Exception:** Only include these if they provide meaningful information for understanding the example.

## Example workflow

### Step 1: Create context

Set up meaningful scenario:

```sql
obclient [SYS]> CREATE USER sales_user IDENTIFIED BY 'password123';
obclient [SYS]> GRANT CREATE SESSION TO sales_user;
obclient [SYS]> CREATE DATABASE sales_db;
obclient [SYS]> USE sales_db;
```

### Step 2: Create objects

Use meaningful names:

```sql
obclient [SALES_DB]> CREATE TABLE order_table (
    order_id BIGINT PRIMARY KEY,
    customer_id BIGINT,
    order_date DATE,
    total_amount DECIMAL(10,2)
);
```

### Step 3: Demonstrate feature

Show the SQL statement:

```sql
obclient [SALES_DB]> SELECT * FROM order_table WHERE order_date >= '2024-01-01';
```

### Step 4: Show results

Separate code block with descriptive text:

查询结果如下：

```
+----------+-------------+------------+--------------+
| order_id | customer_id | order_date | total_amount |
+----------+-------------+------------+--------------+
|      101 |        1001 | 2024-01-15 |      1250.00 |
|      102 |        1002 | 2024-01-20 |       850.50 |
+----------+-------------+------------+--------------+
2 rows in set
```

## Complex examples

### Multi-step examples

For complex workflows, break into logical steps:

**Step 1: Setup**

```sql
obclient [SYS]> CREATE USER admin_user IDENTIFIED BY 'admin123';
obclient [SYS]> GRANT ALTER SYSTEM TO admin_user;
```

**Step 2: Create table group**

```sql
obclient [ADMIN_USER]> CREATE TABLEGROUP order_tg;
```

**Step 3: Create table**

```sql
obclient [ADMIN_USER]> CREATE TABLE order_table (
    order_id BIGINT PRIMARY KEY,
    customer_id BIGINT
) TABLEGROUP = order_tg;
```

**Step 4: Verify**

```sql
obclient [ADMIN_USER]> SHOW TABLEGROUPS;
```

查询结果如下：

```
+-----------+------------+
| TableName | TableGroup |
+-----------+------------+
| order_table | order_tg  |
+-----------+------------+
1 row in set
```

## Error examples

When demonstrating error handling:

```sql
obclient [USER]> CREATE TABLE invalid_table (
    id INT PRIMARY KEY,
    name VARCHAR(10)
) PARTITION BY HASH(id) PARTITIONS 0;
```

错误信息如下：

```
ERROR 1235 (42000): Invalid partition count
```

## Best practices

1. **Start simple, add complexity gradually**
2. **Use consistent naming throughout example**
3. **Show realistic data in results**
4. **Include comments when helpful** (but keep them concise)
5. **Test examples** to ensure they work
6. **Follow test cases** when they differ from parser definitions

## Quality checklist

- [ ] SQL statements have `obclient>` prefix
- [ ] SQL and results in separate code blocks
- [ ] Meaningful, business-oriented names used
- [ ] No unnecessary "Query OK" messages
- [ ] Results formatted clearly
- [ ] Example demonstrates real-world usage
- [ ] All statements are executable and tested
