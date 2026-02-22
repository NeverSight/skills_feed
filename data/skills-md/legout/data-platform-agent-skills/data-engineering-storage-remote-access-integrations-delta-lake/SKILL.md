---
name: data-engineering-storage-remote-access-integrations-delta-lake
description: "Delta Lake integration with cloud storage (S3, GCS, Azure). Covers storage_options, PyArrow filesystem, time travel, and partitioned writes."
dependsOn: ["@data-engineering-storage-lakehouse", "@data-engineering-storage-authentication"]
---

# Delta Lake on Cloud Storage

Integrating Delta Lake tables with cloud storage (S3, GCS, Azure) using the pure-Python `deltalake` package.

## Installation

```bash
pip install deltalake pyarrow
```

## Configuration Patterns

### Method 1: storage_options (Recommended)

The simplest approach using dictionary-based configuration:

```python
from deltalake import DeltaTable, write_deltalake
import pyarrow as pa

# S3 configuration
storage_options = {
    "AWS_ACCESS_KEY_ID": "AKIA...",
    "AWS_SECRET_ACCESS_KEY": "...",
    "AWS_REGION": "us-east-1"
}
# Alternatively, use environment variables (preferred for production)
# os.environ['AWS_ACCESS_KEY_ID'], etc.

# Write Delta table
write_deltalake(
    "s3://bucket/delta-table",
    data=pa_table,
    storage_options=storage_options,
    mode="overwrite",
    partition_by=["date"]
)

# Read Delta table
dt = DeltaTable(
    "s3://bucket/delta-table",
    storage_options=storage_options
)
df = dt.to_pandas()
```

**GCS configuration:**
```python
storage_options = {
    "GOOGLE_SERVICE_ACCOUNT_KEY_JSON": "/path/to/key.json"
    # Or use env var GOOGLE_APPLICATION_CREDENTIALS
}
```

**Azure configuration:**
```python
storage_options = {
    "AZURE_STORAGE_CONNECTION_STRING": "...",
    # OR: "AZURE_STORAGE_ACCOUNT_NAME" + "AZURE_STORAGE_ACCOUNT_KEY"
}
```

### Method 2: PyArrow Filesystem (Advanced)

Use PyArrow filesystem objects for more control:

```python
import pyarrow.fs as fs
from deltalake import write_deltalake, DeltaTable

# Create filesystem
raw_fs, subpath = fs.FileSystem.from_uri("s3://bucket/delta-table")
filesystem = fs.SubTreeFileSystem(subpath, raw_fs)

# Write
write_deltalake(
    "delta-table",  # relative to filesystem root
    data=pa_table,
    filesystem=filesystem,
    mode="append"
)

# Read
dt = DeltaTable("delta-table", filesystem=filesystem)
```

## Time Travel

```python
from deltalake import DeltaTable

dt = DeltaTable("s3://bucket/delta-table")

# Load specific version
dt.load_version(5)
df_v5 = dt.to_pandas()

# Load by timestamp
dt.load_with_datetime("2024-01-01T12:00:00Z")
df_ts = dt.to_pandas()

# Get history
history = dt.history().to_pandas()
print(history[["version", "timestamp", "operation"]])
```

## Maintenance Operations

```python
# Vacuum old files (retention in hours)
dt.vacuum(retention_hours=24)  # Clean files older than 24h

# Optimize compaction (combine small files)
dt.optimize().execute()

# Get file list
files = dt.files()
print(files)  # List of Parquet files in the table

# Get metadata
details = dt.details()
print(details)
```

## Incremental Processing

For change data capture (CDC) patterns:

```python
from deltalake import DeltaTable
from datetime import datetime

dt = DeltaTable("s3://bucket/delta-table")

# Get changes since last checkpoint
last_version = get_checkpoint()  # Your checkpoint tracking

# Read only added/modified files
changes = (
    dt.history()
    .filter(f"version > {last_version}")
    .to_pyarrow_table()
)

# Or read full snapshot and compare
df = dt.to_pandas()
# ... compare with previous snapshot ...

# Update checkpoint
save_checkpoint(dt.version())
```

## Best Practices

1. ✅ **Use environment variables** for credentials in production (never hardcode)
2. ✅ **Partition tables** by date/region for efficient querying
3. ✅ **Vacuum regularly** to clean up old files (but retain enough for your time travel needs)
4. ✅ **Optimize** periodically to compact small files
5. ✅ **Track versions** for incremental processing using `dt.version()` and `dt.history()`
6. ⚠️ **Don't** disable vacuum entirely - storage bloat
7. ⚠️ **Don't** vacuum too aggressively - you'll lose time travel capability

## Authentication

See `@data-engineering-storage-authentication` for detailed cloud auth patterns.

For S3:
- Environment: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`
- IAM roles (EC2, ECS, Lambda) override env vars
- For S3-compatible (MinIO): `AWS_ENDPOINT_URL` or in `storage_options`

## Related

- `@data-engineering-storage-lakehouse/delta-lake` - Delta Lake concepts and API
- `@data-engineering-core` - Using Delta with DuckDB
- `@data-engineering-storage-lakehouse` - Comparisons with Iceberg, Hudi

---

## References

- [deltalake Python API](https://delta-io.github.io/delta-rs/python/quickstart.html)
- [Delta Lake Documentation](https://docs.delta.io/latest/index.html)
