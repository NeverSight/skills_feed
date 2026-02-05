---
name: bigquery-analytics
description: Use this skill when the user asks about "BigQuery", "analytics queries", "data warehouse", "partitioning", "clustering", "SQL queries", or any BigQuery-related work. Provides BigQuery table design, query optimization, and Node.js integration patterns.
---

# BigQuery Best Practices

## Table Design

### Partitioning (REQUIRED for tables > 1GB)

```sql
CREATE TABLE `project.dataset.events` (
  event_id STRING,
  shop_id STRING,
  event_type STRING,
  created_at TIMESTAMP,
  data JSON
)
PARTITION BY DATE(created_at)
CLUSTER BY shop_id, event_type;
```

| Data Size | Partition By |
|-----------|--------------|
| < 1GB | Not needed |
| 1GB - 1TB | DATE/TIMESTAMP |
| > 1TB | DATE + consider sharding |

---

## Query Patterns

### Always Use Partition Filter

```sql
-- ❌ BAD: No partition filter (full scan)
SELECT * FROM events WHERE shop_id = 'shop_123';

-- ✅ GOOD: Partition filter included
SELECT * FROM events
WHERE created_at >= '2024-01-01'
  AND created_at < '2024-02-01'
  AND shop_id = 'shop_123';
```

### Select Only Needed Columns

```sql
-- ❌ BAD: SELECT *
SELECT * FROM events;

-- ✅ GOOD: Select specific columns
SELECT event_id, event_type, created_at FROM events;
```

---

## Node.js Integration

### Always Batch Inserts

```javascript
// ✅ GOOD: Single batch insert
await table.insert(batch.map(row => ({
  ...row,
  time: new Date()
})));

// ❌ BAD: Insert one row at a time
for (const row of batch) {
  await table.insert([row]);
}
```

| Scenario | Max Batch Size |
|----------|----------------|
| Streaming inserts | 500-1000 rows |
| High throughput | Up to 10,000 rows |

---

## Cost Control

```javascript
// Dry run before expensive queries
const [job] = await bigquery.createQueryJob({
  query: sql,
  dryRun: true
});
const estimatedCost = (job.statistics.totalBytesProcessed / 1e12) * 5;
```

---

## Checklist

```
□ Large tables (>1GB) have partitioning
□ Queries include partition column in WHERE
□ Tables clustered by frequently filtered columns
□ No SELECT * - select specific columns
□ Using parameterized queries
□ Batch inserts (not row-by-row)
```