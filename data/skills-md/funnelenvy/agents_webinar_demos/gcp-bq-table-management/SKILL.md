---
name: gcp-bq-table-management
description: Use when creating BigQuery tables, implementing partitioning or clustering, managing table schemas, or optimizing table structure. Covers time-based partitioning, range partitioning, clustering strategies, DDL commands, and table configuration.
---

# BigQuery Table Management

Use this skill when creating, modifying, or optimizing BigQuery table structures with partitioning and clustering.

## Creating Tables

### Basic Table Creation

**Using bq mk:**
```bash
bq mk -t \
  --schema 'customer_id:STRING,amount:FLOAT,date:DATE' \
  --description "Customer orders table" \
  project:dataset.orders
```

**Using SQL DDL:**
```sql
CREATE TABLE `project.dataset.orders` (
  customer_id STRING,
  amount FLOAT64,
  date DATE,
  created_at TIMESTAMP
);
```

## Partitioning Strategies

### Time-Based Partitioning

**Create time-partitioned table:**
```bash
bq mk -t \
  --schema 'timestamp:TIMESTAMP,customer_id:STRING,amount:FLOAT' \
  --time_partitioning_field timestamp \
  --time_partitioning_type DAY \
  project:dataset.orders
```

**SQL DDL version:**
```sql
CREATE TABLE `project.dataset.orders` (
  timestamp TIMESTAMP,
  customer_id STRING,
  amount FLOAT64
)
PARTITION BY DATE(timestamp);
```

**Partitioning options:**
- **DAY** - Daily partitions (most common)
- **HOUR** - Hourly partitions (for high-volume data)
- **MONTH** - Monthly partitions (for historical data)
- **YEAR** - Yearly partitions (for very old data)

### Ingestion-Time Partitioning

**Create table with automatic _PARTITIONTIME:**
```bash
bq mk -t \
  --schema 'customer_id:STRING,amount:FLOAT' \
  --time_partitioning_type DAY \
  project:dataset.orders
```

**Query with ingestion-time partition:**
```sql
SELECT * FROM `project.dataset.orders`
WHERE _PARTITIONTIME >= '2024-01-01'
```

### Range Partitioning

**Create range-partitioned table:**
```bash
bq mk -t \
  --schema 'customer_id:INTEGER,region:STRING,sales:FLOAT' \
  --range_partitioning=customer_id,0,100,10 \
  project:dataset.sales
```

**Parameters:** `field,start,end,interval`
- Creates partitions: [0,10), [10,20), [20,30), ..., [90,100)

**SQL DDL version:**
```sql
CREATE TABLE `project.dataset.sales` (
  customer_id INT64,
  region STRING,
  sales FLOAT64
)
PARTITION BY RANGE_BUCKET(customer_id, GENERATE_ARRAY(0, 100, 10));
```

## Clustering

### Basic Clustering

**Create clustered table:**
```bash
bq mk -t \
  --schema 'timestamp:TIMESTAMP,customer_id:STRING,product_id:STRING,amount:FLOAT' \
  --clustering_fields customer_id,product_id \
  project:dataset.orders
```

**SQL DDL version:**
```sql
CREATE TABLE `project.dataset.orders` (
  timestamp TIMESTAMP,
  customer_id STRING,
  product_id STRING,
  amount FLOAT64
)
CLUSTER BY customer_id, product_id;
```

**Clustering rules:**
- Up to **4 clustering columns**
- Order matters (first column has most impact)
- Works best with WHERE, GROUP BY, JOIN filters

### Partitioning + Clustering (Recommended)

**Combined approach:**
```bash
bq mk -t \
  --schema 'timestamp:TIMESTAMP,customer_id:STRING,transaction_amount:FLOAT' \
  --time_partitioning_field timestamp \
  --clustering_fields customer_id \
  --description "Partitioned by day, clustered by customer" \
  project:dataset.transactions
```

**SQL DDL version:**
```sql
CREATE TABLE `project.dataset.transactions` (
  timestamp TIMESTAMP,
  customer_id STRING,
  transaction_amount FLOAT64
)
PARTITION BY DATE(timestamp)
CLUSTER BY customer_id;
```

**Query benefits:**
```sql
-- Partition pruning + clustering optimization
SELECT * FROM `project.dataset.transactions`
WHERE DATE(timestamp) = '2024-01-15'  -- Partition filter
AND customer_id = 'CUST123'            -- Cluster filter
```

## Table Configuration Options

### Expiration

**Set table expiration:**
```bash
bq mk -t \
  --expiration 2592000 \
  --schema 'field:TYPE' \
  project:dataset.temp_table
```
**Expiration in seconds:** 2592000 = 30 days

**Update existing table:**
```bash
bq update --expiration 604800 project:dataset.table
```

**Remove expiration:**
```bash
bq update --expiration 0 project:dataset.table
```

### Labels

**Add labels:**
```bash
bq mk -t \
  --schema 'field:TYPE' \
  --label environment:production \
  --label team:analytics \
  project:dataset.table
```

**Update labels:**
```bash
bq update --set_label environment:staging project:dataset.table
```

### Description

**Set description:**
```bash
bq update \
  --description "Customer transaction history with daily partitioning" \
  project:dataset.transactions
```

## Schema Management

### Adding Columns

**Cannot add required columns to existing data:**
```bash
# Add optional column
bq query --use_legacy_sql=false \
  'ALTER TABLE `project.dataset.table`
   ADD COLUMN new_field STRING'
```

### Changing Column Modes

**REQUIRED → NULLABLE (allowed):**
```sql
ALTER TABLE `project.dataset.table`
ALTER COLUMN field_name DROP NOT NULL;
```

**NULLABLE → REQUIRED (NOT allowed if data exists)**

### Relaxing Column Types

**Allowed type changes:**
- INT64 → FLOAT64 ✅
- INT64 → NUMERIC ✅
- INT64 → BIGNUMERIC ✅
- INT64 → STRING ✅

**Example:**
```sql
ALTER TABLE `project.dataset.table`
ALTER COLUMN amount SET DATA TYPE FLOAT64;
```

## External Tables

### Create External Table (GCS)

**CSV in GCS:**
```bash
bq mk \
  --external_table_definition=gs://bucket/*.csv@CSV \
  --schema='customer_id:STRING,amount:FLOAT' \
  project:dataset.external_orders
```

**Parquet in GCS (schema auto-detected):**
```bash
bq mk \
  --external_table_definition=gs://bucket/*.parquet@PARQUET \
  project:dataset.external_data
```

**Supported formats:** CSV, JSON, AVRO, PARQUET, ORC

### External Table Limitations

- No DML operations (INSERT, UPDATE, DELETE)
- No guaranteed performance SLAs
- Data must be in GCS, Drive, or Bigtable
- Cannot be partitioned (but can use hive partitioning)

## Snapshots and Clones

### Table Snapshots

**Create snapshot:**
```sql
CREATE SNAPSHOT TABLE `project.dataset.orders_snapshot`
CLONE `project.dataset.orders`;
```

**Restore from snapshot:**
```sql
CREATE OR REPLACE TABLE `project.dataset.orders`
CLONE `project.dataset.orders_snapshot`;
```

**Snapshot retention:** 7 days by default

### Table Clones

**Create table clone:**
```sql
CREATE TABLE `project.dataset.orders_clone`
CLONE `project.dataset.orders`;
```

**Difference from snapshot:**
- Clone = new independent table
- Snapshot = point-in-time reference

## Time Travel

**Query historical data:**
```sql
-- Query table as it was 1 hour ago
SELECT * FROM `project.dataset.orders`
FOR SYSTEM_TIME AS OF TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR);

-- Query table at specific time
SELECT * FROM `project.dataset.orders`
FOR SYSTEM_TIME AS OF '2024-01-15 10:00:00 UTC';
```

**Time travel window:** 7 days (168 hours) by default

## Best Practices

### Partition Selection

**Use time-based partitioning when:**
- Data has timestamp/date column
- Queries filter by time ranges
- Data arrives chronologically
- Want automatic partition management

**Use range partitioning when:**
- Partitioning on integer column (ID, age, etc.)
- Predictable value distribution
- Fixed range boundaries

**Use ingestion-time partitioning when:**
- No natural timestamp column
- Loading data from streaming sources
- Want simple partition management

### Clustering Selection

**Cluster on columns that are:**
- Frequently used in WHERE clauses
- Used in JOIN conditions
- Used in GROUP BY
- High cardinality (many distinct values)

**Order matters:**
- Most filtered column first
- Then second most filtered
- Up to 4 columns total

### Partitioning + Clustering Strategy

**Optimal pattern:**
```sql
CREATE TABLE `project.dataset.optimized` (
  event_timestamp TIMESTAMP,      -- Partition on this
  customer_id STRING,              -- Cluster on this (1st)
  product_category STRING,         -- Cluster on this (2nd)
  amount FLOAT64
)
PARTITION BY DATE(event_timestamp)
CLUSTER BY customer_id, product_category;
```

**Query pattern:**
```sql
-- Both partition and cluster benefit
SELECT SUM(amount)
FROM `project.dataset.optimized`
WHERE DATE(event_timestamp) BETWEEN '2024-01-01' AND '2024-01-31'
AND customer_id = 'CUST123'
GROUP BY product_category;
```

## Checking Table Metadata

**Get table information:**
```bash
bq show --format=prettyjson project:dataset.table
```

**Check partition info:**
```sql
SELECT
  partition_id,
  total_rows,
  total_logical_bytes,
  last_modified_time
FROM `project.dataset.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'orders'
ORDER BY partition_id DESC
LIMIT 10;
```

**Check clustering info:**
```sql
SELECT
  table_name,
  clustering_ordinal_position,
  column_name
FROM `project.dataset.INFORMATION_SCHEMA.COLUMNS`
WHERE clustering_ordinal_position IS NOT NULL
ORDER BY table_name, clustering_ordinal_position;
```

## Common Pitfalls

### ❌ Too many partitions
**Problem:** Creating 100,000+ partitions
**Limit:** 10,000 partitions per table
**Solution:** Use larger partition granularity (MONTH vs DAY)

### ❌ Wrong partition column
**Problem:** Partitioning on column not used in queries
**Solution:** Partition on columns used in WHERE clauses

### ❌ Not filtering on partition
**Problem:** Query scans all partitions
**Solution:** Always include partition filter in WHERE

### ❌ Clustering too many columns
**Problem:** Clustering on 5+ columns
**Limit:** 4 columns maximum
**Solution:** Choose most selective columns

### ❌ Wrong cluster order
**Problem:** Least selective column first
**Solution:** Put most selective column first

## Table Maintenance

### Update partition expiration

**Set partition expiration:**
```bash
bq update \
  --time_partitioning_expiration 2592000 \
  project:dataset.partitioned_table
```

**Query shows this:** Partitions older than 30 days auto-delete

### Optimize table storage

**Run optimization query:**
```sql
-- BigQuery automatically optimizes storage
-- No manual VACUUM or OPTIMIZE needed
```

BigQuery automatically:
- Compacts data
- Sorts by clustering columns
- Removes deleted rows
- Optimizes storage format

## Access Control & Security

### Row-Level Security

Row-level access policies filter data based on user/group membership. They coexist with column-level security.

**Creating row-level policies:**
```sql
CREATE ROW ACCESS POLICY policy_name
ON dataset.table
GRANT TO ("user:[email protected]")
FILTER USING (region = "US");
```

**Multiple policies:**
```sql
-- Policy for US users
CREATE ROW ACCESS POLICY us_users_policy
ON dataset.orders
GRANT TO ("group:[email protected]")
FILTER USING (region = "US");

-- Policy for managers (see all regions)
CREATE ROW ACCESS POLICY managers_policy
ON dataset.orders
GRANT TO ("group:[email protected]")
FILTER USING (TRUE);
```

**Viewing policies:**
```sql
SELECT * FROM dataset.INFORMATION_SCHEMA.ROW_ACCESS_POLICIES
WHERE table_name = 'orders';
```

**Dropping policies:**
```sql
DROP ROW ACCESS POLICY policy_name ON dataset.table;
```

### Column-Level Security

Use policy tags from Data Catalog to restrict access to sensitive columns:

**Creating table with policy tags:**
```sql
CREATE TABLE dataset.customers (
  customer_id STRING,
  name STRING,
  email STRING,
  ssn STRING OPTIONS(
    policy_tags=("projects/PROJECT/locations/LOCATION/taxonomies/TAXONOMY/policyTags/PII_TAG")
  ),
  credit_score INT64 OPTIONS(
    policy_tags=("projects/PROJECT/locations/LOCATION/taxonomies/TAXONOMY/policyTags/SENSITIVE_TAG")
  )
);
```

**Adding policy tags to existing columns:**
```sql
ALTER TABLE dataset.customers
ALTER COLUMN ssn SET OPTIONS(
  policy_tags=("projects/PROJECT/locations/LOCATION/taxonomies/TAXONOMY/policyTags/PII_TAG")
);
```

**How it works:**
1. Create taxonomy and policy tags in Data Catalog
2. Apply policy tags to table columns
3. Grant IAM roles on policy tags (datacatalog.categoryFineGrainedReader)
4. Users without permission cannot query those columns

### Authorized Views

Views that allow users to query data without direct table access:

**Use cases:**
- Sharing specific columns/rows without full table access
- Implementing business logic in access control
- Best performance for row/column filtering

**Setup process:**
```sql
-- 1. Create view in dataset A
CREATE VIEW datasetA.public_orders AS
SELECT order_id, customer_id, amount, order_date
FROM datasetA.orders
WHERE status = 'completed';

-- 2. Grant dataset B's view access to dataset A's table
-- This is done via dataset permissions in Cloud Console or:
bq update --source datasetA.orders \
  --view datasetB.public_view
```

**Example authorized view:**
```sql
-- View in shared_views dataset
CREATE VIEW shared_views.customer_summary AS
SELECT
  customer_id,
  COUNT(*) as order_count,
  SUM(amount) as total_spent
FROM private_data.orders
GROUP BY customer_id;

-- Grant access to view (not underlying table)
-- Users can query shared_views.customer_summary
-- but cannot access private_data.orders
```

**Benefits:**
- Row/column filtering without policy overhead
- Business logic in SQL (e.g., only show completed orders)
- Best query performance
- Centralized access control

### Security Best Practices

**1. Layered security:**
- Use row-level policies for user-based filtering
- Use column-level security for sensitive data (PII, PHI)
- Use authorized views for complex access patterns

**2. Performance:**
- Authorized views: Best performance (compiled into query)
- Row-level policies: Slight overhead (filter applied)
- Column-level: No performance impact

**3. Combining approaches:**
```sql
-- Table with column-level security AND row-level policy
CREATE TABLE dataset.sensitive_data (
  user_id STRING,
  region STRING,
  ssn STRING OPTIONS(policy_tags=("...")),
  data JSON
)
PARTITION BY DATE(created_at);

-- Row-level policy
CREATE ROW ACCESS POLICY regional_access
ON dataset.sensitive_data
GRANT TO ("group:[email protected]")
FILTER USING (region = "US");
```

**4. Auditing:**
Monitor access with Cloud Audit Logs:
```sql
SELECT
  timestamp,
  principal_email,
  resource_name,
  method_name
FROM `PROJECT.DATASET.cloudaudit_googleapis_com_data_access_*`
WHERE resource.type = "bigquery_dataset"
ORDER BY timestamp DESC;
```

## Quick Reference

**Partition types:**
- Time-based: HOUR, DAY, MONTH, YEAR
- Ingestion-time: Automatic _PARTITIONTIME
- Range: Integer column ranges

**Clustering:**
- Max 4 columns
- Order matters
- Works with or without partitioning

**Security:**
- Row-level: Filter by user/group
- Column-level: Policy tags for sensitive data
- Authorized views: Business logic filtering

**Limits:**
- 10,000 partitions per table
- 4 clustering columns
- 7-day time travel window
- 10,000 columns per table
- 100 row-level policies per table
