---
name: data-engineering-storage-remote-access-integrations-polars
description: "Integrating Polars with remote filesystems (S3, GCS, Azure). Covers native cloud support, fsspec integration, PyArrow dataset scanning, and partitioned writes."
dependsOn: ["@data-engineering-core", "@data-engineering-storage-authentication"]
---

# Polars Integration with Remote Storage

Polars has native cloud storage support via multiple backends, plus integration with fsspec and PyArrow filesystems.

## Native Cloud Access (object_store)

Polars uses the Rust `object_store` crate internally for direct cloud URI access:

```python
import polars as pl

# Read from cloud URIs directly (s3://, gs://, az://)
df = pl.read_parquet("s3://bucket/data/file.parquet")
df = pl.read_parquet("gs://bucket/data/file.parquet")
df = pl.read_csv("s3://bucket/data/file.csv.gz", infer_schema_length=1000)

# Lazy scanning with predicate and column pushdown
lazy_df = pl.scan_parquet("s3://bucket/dataset/**/*.parquet")
result = (
    lazy_df
    .filter(pl.col("date") > "2024-01-01")  # Pushed to storage layer
    .group_by("category")
    .agg([
        pl.col("value").sum().alias("total_value"),
        pl.col("id").count().alias("count")
    ])
    .collect()
)

# Write to cloud storage
df.write_parquet("s3://bucket/output/data.parquet")

# Partitioned write (Hive-style)
df.write_parquet(
    "s3://bucket/output/",
    partition_by=["year", "month"],
    use_pyarrow=True  # Requires PyArrow
)
```

**Supported protocols:** `s3://`, `gs://`, `az://`, `file://`

## Via fsspec

Use fsspec for broader compatibility and protocol chaining:

```python
import fsspec
import polars as pl

# Create fsspec filesystem
fs = fsspec.filesystem("s3", config_kwargs={"region": "us-east-1"})

# Open file through fsspec
with fs.open("s3://bucket/data.csv") as f:
    df = pl.read_csv(f)

# Use fsspec caching wrapper
cached_fs = fsspec.filesystem(
    "simplecache",
    target_protocol="s3",
    target_options={"anon": False}
)
df = pl.read_parquet("simplecache::s3://bucket/cached.parquet")
```

## Via PyArrow Dataset (Advanced)

For Hive-partitioned datasets with complex pushdown:

```python
import pyarrow.fs as fs
import pyarrow.dataset as ds
import polars as pl

s3_fs = fs.S3FileSystem(region="us-east-1")

# Load partitioned dataset
dataset = ds.dataset(
    "bucket/dataset/",
    filesystem=s3_fs,
    format="parquet",
    partitioning=ds.HivePartitioning.discover()
)

# Convert to Polars lazy frame
lazy_df = pl.scan_pyarrow_dataset(dataset)

# Query with full pushdown
result = (
    lazy_df
    .filter((pl.col("year") == 2024) & (pl.col("month") <= 6))
    .select(["id", "value", "timestamp"])
    .collect()
)
```

## Authentication

Native Polars cloud access inherits credentials from:
- **AWS**: Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`), `~/.aws/credentials`, IAM roles
- **GCP**: `GOOGLE_APPLICATION_CREDENTIALS`, gcloud CLI, metadata server
- **Azure**: `AZURE_STORAGE_ACCOUNT`, `AZURE_STORAGE_KEY`, managed identity

For explicit credentials, use fsspec or PyArrow filesystem constructors.

## Performance Tips

- ✅ **Use native `s3://` URIs** for best performance (direct object_store usage)
- ✅ **Lazy evaluation** with predicates for pushdown
- ✅ **Partitioned writes** for large datasets (avoid huge single files)
- ✅ **Column selection** in lazy queries to read only needed data
- ⚠️ For complex authentication (SSO, temporary creds), use fsspec/ PyArrow constructors
- ⚠️ For caching, use fsspec's `simplecache::` or `filecache::` wrappers

## Common Patterns

### Incremental Load from Partitioned Data
```python
# Only read recent partitions
lazy_df = pl.scan_parquet("s3://bucket/events/")
last_month = datetime.now() - timedelta(days=30)

result = (
    lazy_df
    .filter(pl.col("date") >= last_month)
    .collect()
)
```

### Cross-Cloud Copy
```python
# Read from S3, write to GCS (Polars doesn't support mixed URIs directly)
# Use PyArrow bridge:
import pyarrow.fs as fs
import pyarrow.dataset as ds

s3 = fs.S3FileSystem()
gcs = fs.GcsFileSystem()

dataset = ds.dataset("s3://bucket/input/", filesystem=s3, format="parquet")
table = dataset.to_table()
gcs_file = fs.GcsFileSystem().open_output_stream("gs://bucket/output.parquet")
pq.write_table(table, gcs_file)
```

---

## References

- [Polars Cloud Storage Guide](https://pola.rs/posts/polars_cloud_storage/)
- [Polars File System Backends](https://pola.rs/posts/polars_file_format_backends/)
- `@data-engineering-storage-remote-access/libraries/fsspec` - fsspec usage
- `@data-engineering-storage-remote-access/libraries/pyarrow-fs` - PyArrow filesystem
