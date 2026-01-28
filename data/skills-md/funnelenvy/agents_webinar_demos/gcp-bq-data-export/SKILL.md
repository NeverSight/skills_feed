---
name: gcp-bq-data-export
description: Use when exporting BigQuery data to Cloud Storage, extracting tables to CSV, JSON, Avro, or Parquet formats, or using EXPORT DATA statements. Covers bq extract command, format options, compression, and wildcard exports.
---

# BigQuery Data Export

Use this skill when exporting data from BigQuery to Cloud Storage or local files.

## Basic Extract Command

```bash
bq extract \
  --location=LOCATION \
  --destination_format=FORMAT \
  --compression=COMPRESSION \
  PROJECT:DATASET.TABLE \
  gs://bucket/file.ext
```

## Extract to CSV

### Basic CSV Export

```bash
bq extract \
  --destination_format=CSV \
  --print_header=true \
  dataset.table \
  gs://bucket/export.csv
```

### CSV with Options

```bash
bq extract \
  --destination_format=CSV \
  --compression=GZIP \
  --field_delimiter=',' \
  --print_header=true \
  dataset.table \
  gs://bucket/export.csv.gz
```

**CSV flags:**
- `--field_delimiter=','` - Column separator
- `--print_header=true/false` - Include header row

### Tab-Delimited Export

```bash
bq extract \
  --destination_format=CSV \
  --field_delimiter=$'\t' \
  dataset.table \
  gs://bucket/export.tsv
```

## Extract to JSON

### Newline-Delimited JSON

```bash
bq extract \
  --destination_format=NEWLINE_DELIMITED_JSON \
  --compression=GZIP \
  dataset.table \
  gs://bucket/export.json.gz
```

**Output format:**
```json
{"id": 1, "name": "Alice", "amount": 100.50}
{"id": 2, "name": "Bob", "amount": 250.75}
```

## Extract to Avro

```bash
bq extract \
  --destination_format=AVRO \
  --compression=SNAPPY \
  dataset.table \
  gs://bucket/export.avro
```

**Benefits:**
- Preserves schema
- Efficient binary format
- Fast re-import to BigQuery

## Extract to Parquet

```bash
bq extract \
  --destination_format=PARQUET \
  dataset.table \
  gs://bucket/export.parquet
```

**Benefits:**
- Columnar format
- Good compression
- Compatible with many analytics tools

## Compression Options

**Available compression:**
- `GZIP` - Good compression, slower (CSV, JSON, Avro)
- `SNAPPY` - Fast, moderate compression (Avro, Parquet)
- `DEFLATE` - Similar to GZIP (Avro)
- `NONE` - No compression (fastest)

**Example:**
```bash
bq extract \
  --destination_format=CSV \
  --compression=GZIP \
  dataset.table \
  gs://bucket/export.csv.gz
```

## Large Table Exports

### Using Wildcards (>1 GB)

**BigQuery limitation:** 1 GB per file

**Solution:** Use wildcard in destination
```bash
bq extract \
  --destination_format=CSV \
  dataset.large_table \
  'gs://bucket/export-*.csv'
```

**Output:**
```
gs://bucket/export-000000000000.csv
gs://bucket/export-000000000001.csv
gs://bucket/export-000000000002.csv
...
```

### Shard Pattern

```bash
# Create sharded exports
bq extract \
  --destination_format=AVRO \
  dataset.large_table \
  'gs://bucket/shard/data-*.avro'
```

**Note:** Number of files depends on data size, not configurable.

## Export Specific Partitions

### Single Partition

```bash
# Export 2024-01-15 partition only
bq extract \
  --destination_format=CSV \
  dataset.partitioned_table\$20240115 \
  gs://bucket/export_20240115.csv
```

### Date Range (use WHERE in EXPORT DATA)

See EXPORT DATA section below.

## EXPORT DATA SQL Statement

### Basic EXPORT DATA

```sql
EXPORT DATA OPTIONS(
  uri='gs://bucket/export-*.csv',
  format='CSV',
  overwrite=true,
  header=true,
  field_delimiter=','
) AS
SELECT * FROM `project.dataset.table`
WHERE date >= '2024-01-01';
```

### Export Query Results

```sql
EXPORT DATA OPTIONS(
  uri='gs://bucket/aggregated-*.parquet',
  format='PARQUET',
  overwrite=true
) AS
SELECT
  customer_id,
  DATE(order_timestamp) as order_date,
  SUM(amount) as total_amount,
  COUNT(*) as order_count
FROM `project.dataset.orders`
WHERE DATE(order_timestamp) >= '2024-01-01'
GROUP BY customer_id, order_date;
```

### Format Options

**CSV:**
```sql
EXPORT DATA OPTIONS(
  uri='gs://bucket/*.csv',
  format='CSV',
  header=true,
  field_delimiter=',',
  compression='GZIP'
) AS SELECT ...;
```

**JSON:**
```sql
EXPORT DATA OPTIONS(
  uri='gs://bucket/*.json',
  format='JSON',
  compression='GZIP'
) AS SELECT ...;
```

**Avro:**
```sql
EXPORT DATA OPTIONS(
  uri='gs://bucket/*.avro',
  format='AVRO',
  compression='SNAPPY'
) AS SELECT ...;
```

**Parquet:**
```sql
EXPORT DATA OPTIONS(
  uri='gs://bucket/*.parquet',
  format='PARQUET'
) AS SELECT ...;
```

## Export to Local Files (Not Recommended)

### Small Results via Query

```bash
# For small datasets only
bq query \
  --format=csv \
  --max_rows=10000 \
  --use_legacy_sql=false \
  'SELECT * FROM `project.dataset.table` LIMIT 10000' \
  > local_export.csv
```

**Limitation:** Not suitable for large datasets. Use GCS for production.

## Export Scheduled (Automation)

### Using Cloud Scheduler + EXPORT DATA

```bash
# Create scheduled query
bq mk --transfer_config \
  --target_dataset=dataset \
  --display_name='Daily Export' \
  --schedule='every 24 hours' \
  --params='{"query":"EXPORT DATA OPTIONS(uri='\''gs://bucket/daily-*.csv'\'', format='\''CSV'\'') AS SELECT * FROM dataset.table WHERE date = CURRENT_DATE()"}' \
  --data_source=scheduled_query
```

### Using Cloud Composer (Airflow)

```python
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator

export_task = BigQueryInsertJobOperator(
    task_id='export_to_gcs',
    configuration={
        'extract': {
            'sourceTable': {
                'projectId': 'project',
                'datasetId': 'dataset',
                'tableId': 'table'
            },
            'destinationUris': ['gs://bucket/export-*.csv'],
            'destinationFormat': 'CSV'
        }
    }
)
```

## Monitoring Exports

### Check Extract Jobs

```bash
bq ls --jobs --max_results=10
```

### Job Details

```bash
bq show -j JOB_ID
```

### Failed Exports

```sql
SELECT
  job_id,
  user_email,
  error_result.message as error_message,
  creation_time
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE
  job_type = 'EXTRACT'
  AND state = 'DONE'
  AND error_result IS NOT NULL
  AND creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)
ORDER BY creation_time DESC;
```

## Export Best Practices

### Format Selection

**CSV:**
- ✅ Human-readable
- ✅ Universal compatibility
- ❌ Larger file size
- ❌ No schema preservation

**JSON:**
- ✅ Human-readable
- ✅ Preserves nested structures
- ❌ Larger file size

**Avro:**
- ✅ Preserves schema
- ✅ Efficient binary format
- ✅ Fast BigQuery re-import
- ❌ Not human-readable

**Parquet:**
- ✅ Columnar format
- ✅ Good compression
- ✅ Analytics tool compatible
- ❌ Not human-readable

### Compression Recommendations

**For long-term storage:** GZIP (best compression)
**For processing pipelines:** SNAPPY (fast)
**For network transfer:** GZIP (smaller size)
**For speed:** NONE (no compression overhead)

### Wildcards for Large Exports

**Always use wildcards for:**
- Tables >500 MB
- Unknown data size
- Distributed processing

**Example:**
```bash
bq extract dataset.large_table 'gs://bucket/export-*.avro'
```

## Cost Considerations

### Export Costs

- **BigQuery extract:** FREE
- **GCS storage:** Standard GCS pricing
- **Network egress:** Free within same region

### Optimization

**Reduce costs:**
- Export only needed columns (use EXPORT DATA with SELECT)
- Filter rows before export (WHERE clause)
- Use compression (smaller files)
- Export to GCS in same region as BigQuery

**Example - filtered export:**
```sql
EXPORT DATA OPTIONS(
  uri='gs://bucket/*.parquet',
  format='PARQUET'
) AS
SELECT customer_id, order_date, amount  -- Only needed columns
FROM `project.dataset.orders`
WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)  -- Last 30 days only
  AND amount > 0;  -- Filter out zero amounts
```

## Common Patterns

### Daily Export

```bash
#!/bin/bash
DATE=$(date +%Y%m%d)
bq extract \
  --destination_format=CSV \
  --compression=GZIP \
  dataset.table\$$DATE \
  gs://bucket/exports/daily_export_$DATE.csv.gz
```

### Incremental Export

```sql
-- Create temp table with new data
CREATE TEMP TABLE new_data AS
SELECT * FROM `project.dataset.table`
WHERE updated_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR);

-- Export only new data
EXPORT DATA OPTIONS(
  uri='gs://bucket/incremental/data-*.parquet',
  format='PARQUET'
) AS
SELECT * FROM new_data;
```

### Export with Transformation

```sql
EXPORT DATA OPTIONS(
  uri='gs://bucket/transformed-*.csv',
  format='CSV'
) AS
SELECT
  customer_id,
  UPPER(customer_name) as customer_name,
  ROUND(amount, 2) as amount,
  FORMAT_DATE('%Y-%m-%d', order_date) as order_date
FROM `project.dataset.orders`
WHERE order_date >= '2024-01-01';
```

## Troubleshooting

### "Permission denied"

**Problem:** No write access to GCS bucket
**Solution:** Grant BigQuery service account Storage Object Creator role

### "Table too large"

**Problem:** Export exceeds 1GB without wildcard
**Solution:** Use wildcard pattern `gs://bucket/export-*.csv`

### "Invalid URI"

**Problem:** Incorrect GCS path format
**Solution:** Use `gs://bucket/path/file` format, not `https://`

### "Quota exceeded"

**Problem:** Too many extract jobs
**Solution:** Batch exports or increase quota

## Quick Reference

**Format recommendations:**
- Re-import to BigQuery → Avro
- Analytics tools → Parquet
- Data exchange → CSV
- API consumption → JSON

**Compression guide:**
- Best ratio → GZIP
- Fastest → SNAPPY or NONE
- Balance → SNAPPY

**Size limits:**
- 1 GB per file (use wildcards)
- 10 TB per extract job
- 50,000 URIs per export

**Syntax patterns:**
```bash
# Single file
gs://bucket/file.csv

# Wildcard (recommended)
'gs://bucket/prefix-*.csv'

# Sharded with path
'gs://bucket/path/to/shard-*.parquet'
```
