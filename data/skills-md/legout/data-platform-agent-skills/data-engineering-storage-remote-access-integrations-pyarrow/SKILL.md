---
name: data-engineering-storage-remote-access-integrations-pyarrow
description: "Using PyArrow's parquet and dataset modules with remote filesystems (S3, GCS, Azure). Covers native filesystems, fsspec bridge, and obstore wrapper."
dependsOn: ["@data-engineering-core", "@data-engineering-storage-authentication"]
---

# PyArrow Remote Storage Integration

PyArrow's parquet and dataset modules work seamlessly with cloud storage through its native filesystem abstraction and fsspec compatibility.

## Native PyArrow Filesystem

```python
import pyarrow.parquet as pq
import pyarrow.dataset as ds
import pyarrow.fs as fs

# Create S3 filesystem
s3_fs = fs.S3FileSystem(region="us-east-1")

# Read single file with column filtering
table = pq.read_table(
    "bucket/file.parquet",  # Note: no s3:// prefix
    filesystem=s3_fs,
    columns=["id", "value"]  # Column pruning
)

# Dataset with filtering and partitioning
dataset = ds.dataset(
    "bucket/dataset/",
    filesystem=s3_fs,
    format="parquet",
    partitioning=ds.HivePartitioning.discover()
)

# Filter pushdown (only reads matching files/row groups)
table = dataset.to_table(
    filter=(ds.field("year") == 2024) & (ds.field("value") > 100),
    columns=["id", "value", "timestamp"]
)

# Batch scanning for large datasets
scanner = dataset.scanner(
    filter=ds.field("value") > 0,
    batch_size=65536,
    use_threads=True
)
for batch in scanner.to_batches():
    process(batch)
```

## fsspec Integration

PyArrow automatically bridges to fsspec for Parquet files:

```python
import fsspec
import pyarrow.parquet as pq

fs = fsspec.filesystem("s3")

# Open via fsspec
with fs.open("s3://bucket/file.parquet", "rb") as f:
    table = pq.read_table(f)

# Or use URI directly (fsspec auto-detected if installed)
table = pq.read_table("s3://bucket/file.parquet")
```

## obstore fsspec Wrapper

Use obstore's high-performance fsspec wrapper for concurrent operations:

```python
from obstore.fsspec import FsspecStore
import pyarrow.parquet as pq

# Create obstore-backed fsspec filesystem
fs = FsspecStore("s3", bucket="my-bucket", region="us-east-1")

# Use with PyArrow
table = pq.read_table("data/file.parquet", filesystem=fs)
```

## Dataset Scanning Patterns

See `@data-engineering-storage-remote-access/patterns.md` for advanced patterns including:
- Incremental loading with checkpoint tracking
- Partitioned writes with Hive partitioning
- Cross-cloud copying
- Performance optimizations (predicate pushdown, column pruning)

## Authentication

See `@data-engineering-storage-authentication` for S3, GCS, Azure credential configuration with PyArrow filesystems.

## Performance Tips

1. **Column pruning**: Always specify `columns=[...]` to reduce data transfer
2. **Filter pushdown**: Use `dataset.scanner(filter=...)` for predicate pushdown
3. **Row group pruning**: Parquet row groups enable partial file reads
4. **Threading**: Enable `use_threads=True` in scanner for CPU-bound ops
5. **Batch size**: Tune `batch_size` based on downstream processing needs
6. **File format**: Prefer Parquet over CSV/JSON for compression and pushdown

---

## References

- [PyArrow Filesystems Guide](https://arrow.apache.org/docs/python/filesystems.html)
- [PyArrow Dataset Guide](https://arrow.apache.org/docs/python/dataset.html)
- `@data-engineering-storage-remote-access/libraries/pyarrow-fs` - PyArrow.fs library details
