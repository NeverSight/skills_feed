---
name: gcp-bq-data-loading
description: Use when loading data into BigQuery from CSV, JSON, Avro, Parquet files, Cloud Storage, or local files. Covers bq load command, source formats, schema detection, incremental loading, and handling parsing errors.
---

# BigQuery Data Loading

Use this skill when importing data into BigQuery from various file formats and sources.

## Basic Load Command

```bash
bq load \
  --location=LOCATION \
  --source_format=FORMAT \
  PROJECT:DATASET.TABLE \
  SOURCE_PATH \
  SCHEMA
```

## Loading from CSV

### Basic CSV Load

```bash
bq load \
  --source_format=CSV \
  --skip_leading_rows=1 \
  dataset.table \
  gs://bucket/data.csv \
  customer_id:STRING,amount:FLOAT,date:DATE
```

### CSV with Schema File

```bash
# Create schema.json
echo '[
  {"name": "customer_id", "type": "STRING"},
  {"name": "amount", "type": "FLOAT"},
  {"name": "date", "type": "DATE"}
]' > schema.json

# Load with schema file
bq load \
  --source_format=CSV \
  --skip_leading_rows=1 \
  dataset.table \
  gs://bucket/data.csv \
  ./schema.json
```

### CSV Options

```bash
bq load \
  --source_format=CSV \
  --skip_leading_rows=1 \
  --field_delimiter=',' \
  --quote='"' \
  --allow_quoted_newlines \
  --allow_jagged_rows \
  --max_bad_records=100 \
  --null_marker='NULL' \
  dataset.table \
  gs://bucket/data.csv \
  schema.json
```

**Key flags:**
- `--skip_leading_rows=N` - Skip header rows
- `--field_delimiter=','` - Column separator (default: comma)
- `--allow_quoted_newlines` - Allow newlines in quoted fields
- `--allow_jagged_rows` - Allow rows with missing fields
- `--max_bad_records=N` - Tolerate N parsing errors
- `--null_marker='NULL'` - String representing NULL values

### CSV with Auto-detect

```bash
bq load \
  --source_format=CSV \
  --autodetect \
  --skip_leading_rows=1 \
  dataset.table \
  gs://bucket/data.csv
```

**Warning:** Auto-detect is convenient but not recommended for production. Schema may change between loads.

## Loading from JSON

### Newline-Delimited JSON

```bash
bq load \
  --source_format=NEWLINE_DELIMITED_JSON \
  dataset.table \
  gs://bucket/data.json \
  customer_id:STRING,amount:FLOAT,date:DATE
```

**JSON format required:**
```json
{"customer_id": "C001", "amount": 99.99, "date": "2024-01-15"}
{"customer_id": "C002", "amount": 149.99, "date": "2024-01-15"}
```

**NOT** standard JSON array:
```json
// ❌ This won't work
[
  {"customer_id": "C001", "amount": 99.99},
  {"customer_id": "C002", "amount": 149.99}
]
```

### JSON with Auto-detect

```bash
bq load \
  --source_format=NEWLINE_DELIMITED_JSON \
  --autodetect \
  dataset.table \
  gs://bucket/data.json
```

### JSON with Nested Fields

**Schema with nested STRUCT:**
```json
[
  {"name": "customer_id", "type": "STRING"},
  {"name": "address", "type": "RECORD", "fields": [
    {"name": "street", "type": "STRING"},
    {"name": "city", "type": "STRING"},
    {"name": "zip", "type": "STRING"}
  ]},
  {"name": "orders", "type": "RECORD", "mode": "REPEATED", "fields": [
    {"name": "order_id", "type": "STRING"},
    {"name": "amount", "type": "FLOAT"}
  ]}
]
```

## Loading from Avro

### Basic Avro Load

```bash
bq load \
  --source_format=AVRO \
  dataset.table \
  gs://bucket/data.avro
```

**Key benefit:** Schema is auto-detected from Avro metadata. No schema specification needed!

### Avro with Wildcards

```bash
bq load \
  --source_format=AVRO \
  dataset.table \
  "gs://bucket/path/to/*.avro"
```

**Note:** Use quotes around wildcard paths.

### Avro Advantages

- **Self-describing:** Schema embedded in file
- **Efficient:** Compact binary format
- **Type-safe:** Strong typing preserved
- **No schema drift:** Schema always matches data

## Loading from Parquet

### Basic Parquet Load

```bash
bq load \
  --source_format=PARQUET \
  dataset.table \
  gs://bucket/data.parquet
```

**Like Avro:** Schema auto-detected from Parquet metadata.

### Parquet with Compression

```bash
bq load \
  --source_format=PARQUET \
  dataset.table \
  gs://bucket/data.snappy.parquet
```

**Supported compression:** SNAPPY, GZIP, LZO, BROTLI, LZ4, ZSTD

## Loading Strategies

### Append Data (Default)

```bash
bq load \
  --source_format=CSV \
  dataset.table \
  gs://bucket/new_data.csv \
  schema.json
```

**Behavior:** Adds rows to existing table.

### Replace Table

```bash
bq load \
  --source_format=CSV \
  --replace \
  dataset.table \
  gs://bucket/data.csv \
  schema.json
```

**Behavior:** Deletes all existing data, loads new data.

### Overwrite Partition

```bash
bq load \
  --source_format=CSV \
  --replace \
  --time_partitioning_field=date \
  dataset.table\$20240115 \
  gs://bucket/data_20240115.csv \
  schema.json
```

**Syntax:** `TABLE$YYYYMMDD` targets specific partition.

**Behavior:** Replaces only that partition, leaves others intact.

### Append or Skip

```bash
# Skip load if table already has data
bq load \
  --source_format=CSV \
  --if_not_exists \
  dataset.table \
  gs://bucket/data.csv \
  schema.json
```

## Loading from Cloud Storage

### Single File

```bash
bq load \
  --source_format=CSV \
  dataset.table \
  gs://bucket/data.csv \
  schema.json
```

### Multiple Files (List)

```bash
bq load \
  --source_format=CSV \
  dataset.table \
  gs://bucket/file1.csv,gs://bucket/file2.csv,gs://bucket/file3.csv \
  schema.json
```

### Wildcard Pattern

```bash
bq load \
  --source_format=CSV \
  dataset.table \
  "gs://bucket/path/data-*.csv" \
  schema.json
```

**Patterns:**
- `gs://bucket/*.csv` - All CSV files in bucket root
- `gs://bucket/2024/*/*.csv` - All CSV files in subdirectories
- `gs://bucket/data-[0-9]*.csv` - Files matching pattern

## Loading from Local Files

### Local CSV

```bash
bq load \
  --source_format=CSV \
  --skip_leading_rows=1 \
  dataset.table \
  /path/to/local/data.csv \
  schema.json
```

**Limitation:** Files are uploaded first, then loaded. Slower for large files. Use GCS for better performance.

## Schema Handling

### Inline Schema

```bash
bq load \
  --source_format=CSV \
  dataset.table \
  gs://bucket/data.csv \
  customer_id:STRING,amount:FLOAT64,order_date:DATE,active:BOOLEAN
```

### Schema File

```json
[
  {"name": "customer_id", "type": "STRING", "mode": "REQUIRED"},
  {"name": "amount", "type": "FLOAT64"},
  {"name": "order_date", "type": "DATE"},
  {"name": "metadata", "type": "JSON"}
]
```

**Modes:**
- `REQUIRED` - Field must have value
- `NULLABLE` - Field can be NULL (default)
- `REPEATED` - Field is an array

### Auto-detect Schema

```bash
bq load \
  --source_format=CSV \
  --autodetect \
  dataset.table \
  gs://bucket/data.csv
```

**Pros:**
- Quick for exploration
- No schema definition needed

**Cons:**
- Not reliable for production
- Schema may change between loads
- May misinterpret types

### Schema Evolution

**Add new columns:**
```bash
bq load \
  --source_format=CSV \
  --schema_update_option=ALLOW_FIELD_ADDITION \
  dataset.table \
  gs://bucket/data_with_new_column.csv \
  schema.json
```

**Relax required columns:**
```bash
bq load \
  --schema_update_option=ALLOW_FIELD_RELAXATION \
  dataset.table \
  gs://bucket/data.csv \
  schema.json
```

## Compression

### Compressed Files

BigQuery automatically detects compression:

```bash
# Gzip compressed CSV
bq load \
  --source_format=CSV \
  dataset.table \
  gs://bucket/data.csv.gz \
  schema.json
```

**Supported:** GZIP, DEFLATE, SNAPPY, BZIP2, LZ4, ZSTD

**Performance note:** Uncompressed files load faster (parallel processing). Use compression only if network/storage is bottleneck.

## Error Handling

### Allow Bad Records

```bash
bq load \
  --source_format=CSV \
  --max_bad_records=1000 \
  dataset.table \
  gs://bucket/data.csv \
  schema.json
```

**Behavior:** Skip up to 1000 rows with errors, load the rest.

### Ignore Unknown Values

```bash
bq load \
  --source_format=JSON \
  --ignore_unknown_values \
  dataset.table \
  gs://bucket/data.json \
  schema.json
```

**Behavior:** Ignore JSON fields not in schema.

### Validate Only (Dry Run)

```bash
bq load \
  --dry_run \
  --source_format=CSV \
  dataset.table \
  gs://bucket/data.csv \
  schema.json
```

**Behavior:** Validate schema and format without loading data.

## Loading to Partitioned Tables

### Time-Partitioned Table

```bash
bq load \
  --source_format=CSV \
  --time_partitioning_field=order_date \
  --time_partitioning_type=DAY \
  dataset.partitioned_orders \
  gs://bucket/orders_2024.csv \
  order_id:STRING,customer_id:STRING,order_date:DATE,amount:FLOAT
```

### Load Specific Partition

```bash
# Load into 2024-01-15 partition
bq load \
  --source_format=CSV \
  dataset.orders\$20240115 \
  gs://bucket/orders_20240115.csv \
  schema.json
```

### Range-Partitioned Table

```bash
bq load \
  --source_format=CSV \
  --range_partitioning=customer_id,0,1000,100 \
  dataset.range_partitioned \
  gs://bucket/data.csv \
  customer_id:INTEGER,amount:FLOAT
```

## Performance Optimization

### Parallel Loading

BigQuery automatically parallelizes loads from:
- Multiple files with wildcards
- Uncompressed files (internal parallelization)

**Optimal:** Split large files into 1GB chunks

### File Format Recommendations

**Best performance:**
1. **Avro** - Fastest, self-describing, splittable
2. **Parquet** - Fast, columnar, good compression
3. **CSV uncompressed** - Good for parallel processing
4. **JSON** - Flexible but slower

**Avoid:**
- Very large single files (>10GB)
- CSV with complex escaping
- Highly compressed files (limits parallelism)

## Monitoring Loads

### Check Load Jobs

```bash
bq ls --jobs --max_results=10
```

### Job Details

```bash
bq show -j JOB_ID
```

### Failed Loads

```sql
SELECT
  job_id,
  user_email,
  error_result.message as error_message,
  creation_time
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE
  job_type = 'LOAD'
  AND state = 'DONE'
  AND error_result IS NOT NULL
  AND creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)
ORDER BY creation_time DESC;
```

## Common Patterns

### Daily Batch Load

```bash
#!/bin/bash
DATE=$(date +%Y%m%d)
bq load \
  --source_format=CSV \
  --replace \
  dataset.daily_data\$$DATE \
  gs://bucket/data_$DATE.csv \
  schema.json
```

### Incremental Load with Deduplication

```bash
# Load to staging
bq load \
  --source_format=CSV \
  dataset.staging_orders \
  gs://bucket/new_orders.csv \
  schema.json

# Merge to production (dedup)
bq query --use_legacy_sql=false '
MERGE `project.dataset.orders` T
USING `project.dataset.staging_orders` S
ON T.order_id = S.order_id
WHEN NOT MATCHED THEN INSERT ROW
'
```

## Troubleshooting

### "Too many errors"

**Problem:** Exceeds max_bad_records
**Solution:** Increase `--max_bad_records` or fix data quality

### "Schema mismatch"

**Problem:** CSV columns don't match schema
**Solution:** Verify column order and count

### "Invalid CSV format"

**Problem:** Unescaped quotes or newlines
**Solution:** Use `--allow_quoted_newlines`

### "Permission denied"

**Problem:** No access to GCS bucket
**Solution:** Grant BigQuery service account Storage Object Viewer role

## Quick Reference

**Format priorities (fastest first):**
1. Avro (splittable, self-describing)
2. Parquet (columnar, efficient)
3. CSV uncompressed (parallel)
4. JSON (flexible)

**Schema strategies:**
- Production: Explicit schema file
- Development: Auto-detect
- Evolution: Allow field addition/relaxation

**Loading strategies:**
- New data: Append (default)
- Replace all: `--replace`
- Replace partition: `TABLE$YYYYMMDD`
- Incremental: Load staging → MERGE
