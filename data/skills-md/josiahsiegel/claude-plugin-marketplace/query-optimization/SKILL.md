---
name: query-optimization
description: |
  T-SQL query optimization techniques for SQL Server and Azure SQL Database. Use this skill when: (1) User needs to optimize slow queries, (2) User asks about SARGability or index seeks, (3) User needs help with query hints, (4) User has parameter sniffing issues, (5) User needs to understand execution plans, (6) User asks about statistics and cardinality estimation.
---

# Query Optimization

Comprehensive guide to T-SQL query optimization techniques.

## Quick Reference

### SARGable vs Non-SARGable Patterns

| Non-SARGable (Bad) | SARGable (Good) |
|-------------------|-----------------|
| `WHERE YEAR(Date) = 2024` | `WHERE Date >= '2024-01-01' AND Date < '2025-01-01'` |
| `WHERE LEFT(Name, 3) = 'ABC'` | `WHERE Name LIKE 'ABC%'` |
| `WHERE Amount * 1.1 > 1000` | `WHERE Amount > 1000 / 1.1` |
| `WHERE ISNULL(Col, 0) = 5` | `WHERE Col = 5 OR Col IS NULL` |
| `WHERE VarcharCol = 123` | `WHERE VarcharCol = '123'` |

### Join Types Performance

| Join Type | Best For | Characteristics |
|-----------|----------|-----------------|
| Nested Loop | Small outer, indexed inner | Low memory, good for small sets |
| Merge Join | Sorted inputs, similar sizes | Efficient for sorted data |
| Hash Join | Large unsorted inputs | High memory, good for large sets |

### Query Hints Quick Reference

| Hint | Purpose |
|------|---------|
| `OPTION (RECOMPILE)` | Fresh plan each execution |
| `OPTION (OPTIMIZE FOR (@p = value))` | Optimize for specific value |
| `OPTION (OPTIMIZE FOR UNKNOWN)` | Use average statistics |
| `OPTION (MAXDOP n)` | Limit parallelism |
| `OPTION (FORCE ORDER)` | Use exact join order |
| `WITH (NOLOCK)` | Read uncommitted (dirty reads) |
| `WITH (FORCESEEK)` | Force index seek |

## Core Optimization Principles

### 1. SARGability

SARG = Search ARGument. SARGable queries can use index seeks:

```sql
-- Non-SARGable: Function on column
WHERE DATEPART(year, OrderDate) = 2024
WHERE UPPER(CustomerName) = 'JOHN'
WHERE OrderAmount + 100 > 500

-- SARGable: Preserve column
WHERE OrderDate >= '2024-01-01' AND OrderDate < '2025-01-01'
WHERE CustomerName = 'john' COLLATE SQL_Latin1_General_CP1_CI_AS
WHERE OrderAmount > 400
```

### 2. Implicit Conversions

Avoid data type mismatches:

```sql
-- Bad: Implicit conversion (varchar column compared to int)
WHERE VarcharColumn = 12345

-- Good: Match types exactly
WHERE VarcharColumn = '12345'

-- Check for implicit conversions in execution plan
-- Look for CONVERT_IMPLICIT warnings
```

### 3. OR Optimization

OR on different columns prevents seek:

```sql
-- Inefficient: OR on different columns
SELECT * FROM Orders
WHERE CustomerID = 1 OR ProductID = 2

-- Better: UNION for OR optimization
SELECT * FROM Orders WHERE CustomerID = 1
UNION ALL
SELECT * FROM Orders WHERE ProductID = 2 AND CustomerID <> 1
```

### 4. EXISTS vs IN vs JOIN

```sql
-- EXISTS: Best for semi-joins (checking existence)
SELECT * FROM Customers c
WHERE EXISTS (SELECT 1 FROM Orders o WHERE o.CustomerID = c.CustomerID)

-- IN: Good for small static lists
SELECT * FROM Products WHERE CategoryID IN (1, 2, 3)

-- JOIN: Best when you need data from both tables
SELECT c.*, o.OrderDate
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
```

## Parameter Sniffing Solutions

### Problem
```sql
-- First execution with CustomerID=1 (10 rows) creates plan
-- Subsequent execution with CustomerID=999 (1M rows) uses same plan
CREATE PROCEDURE GetOrders @CustomerID INT AS
    SELECT * FROM Orders WHERE CustomerID = @CustomerID
```

### Solution 1: OPTION (RECOMPILE)
```sql
CREATE PROCEDURE GetOrders @CustomerID INT AS
    SELECT * FROM Orders
    WHERE CustomerID = @CustomerID
    OPTION (RECOMPILE)
-- Best for: Infrequent queries, highly variable data distribution
```

### Solution 2: OPTIMIZE FOR
```sql
-- Optimize for specific value
OPTION (OPTIMIZE FOR (@CustomerID = 1))

-- Optimize for unknown (average statistics)
OPTION (OPTIMIZE FOR UNKNOWN)
```

### Solution 3: Local Variables
```sql
CREATE PROCEDURE GetOrders @CustomerID INT AS
BEGIN
    DECLARE @LocalID INT = @CustomerID
    SELECT * FROM Orders WHERE CustomerID = @LocalID
END
-- Hides parameter from optimizer, similar to OPTIMIZE FOR UNKNOWN
```

### Solution 4: Query Store Hints (SQL 2022+)
```sql
EXEC sys.sp_query_store_set_hints
    @query_id = 12345,
    @hints = N'OPTION (RECOMPILE)'
-- Apply hints without code changes
```

### Solution 5: PSP Optimization (SQL 2022+)
```sql
-- Enable Parameter Sensitive Plan optimization
ALTER DATABASE YourDB SET COMPATIBILITY_LEVEL = 160
-- Automatically creates multiple plans based on parameter values
```

## Execution Plan Analysis

### Key Operators to Watch

| Operator | Warning Sign | Action |
|----------|--------------|--------|
| Table Scan | Missing index | Add appropriate index |
| Index Scan | Non-SARGable predicate | Rewrite query |
| Key Lookup | Missing covering index | Add INCLUDE columns |
| Sort | Missing index for ORDER BY | Add sorted index |
| Hash Match | Large memory grant | Consider index |
| Spools | Repeated scans | Restructure query |

### Estimated vs Actual Rows
```sql
-- Large difference indicates statistics problem
-- Check if stats need updating:
UPDATE STATISTICS TableName WITH FULLSCAN

-- Or enable auto-update:
ALTER DATABASE YourDB SET AUTO_UPDATE_STATISTICS ON
```

### Finding Missing Indexes
```sql
SELECT
    CONVERT(DECIMAL(18,2), migs.avg_user_impact) AS AvgImpact,
    mid.statement AS TableName,
    mid.equality_columns,
    mid.inequality_columns,
    mid.included_columns
FROM sys.dm_db_missing_index_groups mig
JOIN sys.dm_db_missing_index_group_stats migs ON mig.index_group_handle = migs.group_handle
JOIN sys.dm_db_missing_index_details mid ON mig.index_handle = mid.index_handle
WHERE mid.database_id = DB_ID()
ORDER BY migs.avg_user_impact DESC
```

## Statistics Management

### View Statistics Info
```sql
DBCC SHOW_STATISTICS('TableName', 'IndexName')
```

### Update Statistics
```sql
-- Update all statistics on table
UPDATE STATISTICS TableName

-- Update with full scan (most accurate)
UPDATE STATISTICS TableName WITH FULLSCAN

-- Update specific statistics
UPDATE STATISTICS TableName StatisticsName
```

### Auto-Update Settings
```sql
-- Enable async auto-update (better for OLTP)
ALTER DATABASE YourDB SET AUTO_UPDATE_STATISTICS_ASYNC ON
```

## Additional References

For deeper coverage of performance diagnostics, see:

- `references/dmv-diagnostic-queries.md` - DMV queries for performance analysis
