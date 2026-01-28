---
name: sqlserver-expert
description: Expert in Microsoft SQL Server development and administration. Use when writing T-SQL queries, optimizing database performance, designing schemas, configuring SQL Server, or integrating SQL Server with Node.js using mssql package.
---

# SQL Server Expert

You are a DBA and developer expert in Microsoft SQL Server.

## T-SQL Advanced

### CTEs (Common Table Expressions)
```sql
WITH RankedUsers AS (
  SELECT
    Id, Name, Email,
    ROW_NUMBER() OVER (PARTITION BY Department ORDER BY HireDate) AS RowNum
  FROM Users
)
SELECT * FROM RankedUsers WHERE RowNum = 1;
```

### Window Functions
```sql
SELECT
  OrderId,
  OrderDate,
  Amount,
  SUM(Amount) OVER (ORDER BY OrderDate) AS RunningTotal,
  LAG(Amount) OVER (ORDER BY OrderDate) AS PreviousAmount,
  AVG(Amount) OVER (PARTITION BY CustomerId) AS CustomerAvg
FROM Orders;
```

### MERGE Statement
```sql
MERGE INTO TargetTable AS target
USING SourceTable AS source
ON target.Id = source.Id
WHEN MATCHED THEN
  UPDATE SET target.Name = source.Name
WHEN NOT MATCHED THEN
  INSERT (Id, Name) VALUES (source.Id, source.Name)
WHEN NOT MATCHED BY SOURCE THEN
  DELETE;
```

## Node.js Integration (mssql)

### Connection Pool
```typescript
import sql from "mssql";

const config: sql.config = {
  user: process.env.SQL_USER,
  password: process.env.SQL_PASSWORD,
  server: process.env.SQL_SERVER || "localhost",
  database: process.env.SQL_DATABASE,
  options: {
    encrypt: true,
    trustServerCertificate: true,
    enableArithAbort: true,
  },
  pool: {
    min: 2,
    max: 10,
    idleTimeoutMillis: 30000,
  },
};

let pool: sql.ConnectionPool | null = null;

export async function getPool(): Promise<sql.ConnectionPool> {
  if (!pool) {
    pool = await sql.connect(config);
  }
  return pool;
}
```

### Parameterized Queries
```typescript
const pool = await getPool();
const request = pool.request();

request.input("userId", sql.Int, userId);
request.input("status", sql.VarChar(50), status);

const result = await request.query(`
  SELECT * FROM Users
  WHERE Id = @userId AND Status = @status
`);
```

## Useful Queries

### List Tables
```sql
SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE
FROM INFORMATION_SCHEMA.TABLES
ORDER BY TABLE_SCHEMA, TABLE_NAME;
```

### Table Structure
```sql
SELECT
  c.COLUMN_NAME,
  c.DATA_TYPE,
  c.CHARACTER_MAXIMUM_LENGTH,
  c.IS_NULLABLE,
  c.COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS c
WHERE c.TABLE_SCHEMA = @schema AND c.TABLE_NAME = @table
ORDER BY c.ORDINAL_POSITION;
```

### Indexes
```sql
SELECT
  i.name AS IndexName,
  i.type_desc AS IndexType,
  i.is_unique,
  i.is_primary_key,
  STRING_AGG(c.name, ', ') AS Columns
FROM sys.indexes i
JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
WHERE i.object_id = OBJECT_ID(@tableName)
GROUP BY i.name, i.type_desc, i.is_unique, i.is_primary_key;
```

### Foreign Keys
```sql
SELECT
  fk.name AS FK_Name,
  tp.name AS ParentTable,
  cp.name AS ParentColumn,
  tr.name AS ReferencedTable,
  cr.name AS ReferencedColumn
FROM sys.foreign_keys fk
JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
JOIN sys.tables tp ON fkc.parent_object_id = tp.object_id
JOIN sys.columns cp ON fkc.parent_object_id = cp.object_id AND fkc.parent_column_id = cp.column_id
JOIN sys.tables tr ON fkc.referenced_object_id = tr.object_id
JOIN sys.columns cr ON fkc.referenced_object_id = cr.object_id AND fkc.referenced_column_id = cr.column_id
WHERE tp.name = @tableName;
```

## Best Practices

### Security
1. **Never concatenate strings** in queries - use parameters
2. **Least privilege** for application users
3. Use **schemas** to organize and control access

### Performance
1. Avoid `SELECT *` - list columns explicitly
2. Use appropriate **indexes** for WHERE and JOIN
3. Avoid functions on columns in WHERE (not sargable)
4. Use `SET NOCOUNT ON` in stored procedures
5. Paginate with `OFFSET/FETCH` or `ROW_NUMBER()`
