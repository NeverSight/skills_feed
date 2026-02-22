---
name: data-engineering-storage-remote-access-libraries-pyarrow-fs
description: "Native Arrow filesystem integration with PyArrow. Optimized for Parquet workflows, zero-copy data transfer, predicate pushdown, and column pruning. Covers S3, GCS, HDFS with PyArrow datasets."
dependsOn: ["@data-engineering-core", "@data-engineering-storage-authentication"]
---

# PyArrow.fs: Native Arrow Filesystems

PyArrow provides its own filesystem abstraction optimized for Arrow/Parquet workflows with zero-copy integration.

## Installation

```bash
# Bundled with PyArrow - no extra deps
pip install pyarrow
```

## Basic Usage

```python
import pyarrow.fs as fs
from pyarrow import parquet as pq

# From URI - auto-detects filesystem type
s3_fs, path = fs.FileSystem.from_uri("s3://bucket/path/to/data/")
print(type(s3_fs))  # <class 'pyarrow._fs.S3FileSystem'>
print(path)         # 'path/to/data/'

# GCS via URI
gcs_fs, path = fs.FileSystem.from_uri("gs://my-bucket/data/")

# Local filesystem
local_fs, path = fs.FileSystem.from_uri("file:///home/user/data/")
```

## S3 Configuration

```python
import pyarrow.fs as fs
from pyarrow.fs import S3FileSystem

# Method 1: From URI with options
s3_fs = S3FileSystem(
    access_key='AKIA...',
    secret_key='...',
    session_token='...',           # For temporary credentials
    region='us-west-2',
    endpoint_override='https://minio.local:9000',  # S3-compatible
    scheme='https',
    proxy_options={'scheme': 'http', 'host': 'proxy.company.com', 'port': 8080},
    allow_bucket_creation=True,
    retry_strategy=fs.AwsStandardS3RetryStrategy(max_attempts=5)
)

# Method 2: From URI (reads from environment/AWS config)
s3_fs, path = fs.FileSystem.from_uri("s3://my-bucket/data/")

# File operations (bucket/key paths, not s3:// URIs)
info = s3_fs.get_file_info("bucket/file.parquet")
print(info.size)           # File size in bytes
print(info.mtime)          # Modification time

# Open input stream
with s3_fs.open_input_stream("bucket/file.parquet") as f:
    data = f.read()

# Open output stream for writing
with s3_fs.open_output_stream("bucket/output.parquet") as f:
    f.write(parquet_bytes)

# Copy and delete
s3_fs.copy_file("bucket/src.parquet", "bucket/dst.parquet")
s3_fs.delete_file("bucket/old.parquet")
```

## Working with Parquet Datasets

```python
import pyarrow.dataset as ds
import pyarrow.fs as fs

# Create S3 filesystem
s3_fs = fs.S3FileSystem(region='us-east-1')

# Load partitioned dataset
dataset = ds.dataset(
    "bucket/dataset/",
    filesystem=s3_fs,
    format="parquet",
    partitioning=ds.HivePartitioning.discover()
)

print(dataset.schema)
print(f"Rows: {dataset.count_rows()}")

# Filter pushdown (only reads relevant files)
table = dataset.to_table(
    filter=(ds.field("year") == 2024) & (ds.field("month") > 6),
    columns=["id", "value", "timestamp"]  # Column pruning
)

# Scan with custom options
scanner = dataset.scanner(
    filter=ds.field("value") > 100,
    batch_size=65536,
    use_threads=True
)

for batch in scanner.to_batches():
    process(batch)
```

## Azure Support via FSSpec Bridge

```python
import adlfs
import pyarrow.fs as fs
import pyarrow.dataset as ds

# Create Azure filesystem via fsspec
azure_fs = adlfs.AzureBlobFileSystem(
    account_name="myaccount",
    account_key="...",
    tenant_id="...",
    client_id="...",
    client_secret="..."
)

# Wrap in PyArrow filesystem
pa_fs = fs.PyFileSystem(fs.FSSpecHandler(azure_fs))

# Use with PyArrow dataset
dataset = ds.dataset(
    "container/path/",
    filesystem=pa_fs,
    format="parquet"
)
```

## Authentication

See `@data-engineering-storage-authentication` for S3, GCS, Azure credential configuration.

## When to Use PyArrow.fs

Choose pyarrow.fs when:
- Your pipeline is Arrow/Parquet-native
- You need zero-copy integration with PyArrow datasets
- Predicate pushdown and column pruning are critical
- Working with partitioned Parquet datasets
- You want minimal dependencies (included in PyArrow)

## Performance Considerations

- ✅ **Column pruning**: Use `columns=` parameter to read only needed columns
- ✅ **Predicate pushdown**: Filter at dataset level to skip reading irrelevant files
- ✅ **Batch scanning**: Use `scanner.to_batches()` for large datasets
- ✅ **Threading**: Enable `use_threads=True` for CPU-bound operations
- ⚠️ For ecosystem integration (pandas, Dask, etc.), fsspec may be more convenient
- ⚠️ For maximum async performance with many small files, consider obstore

## Integration

- **Polars**: `pl.scan_pyarrow_dataset(dataset)` for lazy evaluation
- **PyArrow datasets**: Native integration (this is the PyArrow API)
- **Delta Lake/Iceberg**: Use PyArrow filesystem when constructing dataset objects

---

## References

- [PyArrow Filesystems Documentation](https://arrow.apache.org/docs/python/filesystems.html)
- [PyArrow Dataset Guide](https://arrow.apache.org/docs/python/dataset.html)
