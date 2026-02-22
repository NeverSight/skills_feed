---
name: data-engineering-storage-remote-access-integrations-pandas
description: "Reading and writing data with Pandas from/to cloud storage (S3, GCS, Azure) using fsspec and PyArrow filesystems."
dependsOn: ["@data-engineering-core", "@data-engineering-storage-authentication"]
---

# Pandas Integration with Remote Storage

Pandas leverages fsspec under the hood for cloud storage access (s3://, gs://, etc.). This makes reading from and writing to cloud storage straightforward.

## Auto-Detection (Simplest)

Pandas automatically uses fsspec for cloud URIs:

```python
import pandas as pd

# Read CSV/Parquet directly from cloud URIs
df = pd.read_csv("s3://bucket/data.csv")
df = pd.read_parquet("s3://bucket/data.parquet")
df = pd.read_json("gs://bucket/data.json")

# Compression is auto-detected
df = pd.read_csv("s3://bucket/data.csv.gz")  # Automatically decompressed
```

**Note:** Auto-detection uses default credentials. For explicit auth, see below.

## Explicit Filesystem (More Control)

```python
import fsspec
import pandas as pd

# Create fsspec filesystem with configuration
fs = fsspec.filesystem("s3", anon=False)  # Uses default credentials chain

# Open file through filesystem
with fs.open("s3://bucket/data.csv") as f:
    df = pd.read_csv(f)

# Or pass filesystem directly (recommended for performance)
df = pd.read_parquet(
    "s3://bucket/data.parquet",
    filesystem=fs,
    columns=["id", "value"],  # Column pruning reduces data transfer
    filters=[("date", ">=", "2024-01-01")]  # Row group filtering
)
```

## PyArrow Filesystem Backend

For better Arrow integration and zero-copy transfers:

```python
import pyarrow.fs as fs
import pandas as pd

s3_fs = fs.S3FileSystem(region="us-east-1")

# Read with column filtering
df = pd.read_parquet(
    "bucket/data.parquet",  # Note: no s3:// prefix when using filesystem
    filesystem=s3_fs,
    columns=["id", "name", "value"]
)

# Write to cloud storage
df.to_parquet(
    "s3://bucket/output/",
    filesystem=s3_fs,
    partition_cols=["year", "month"]  # Partitioned write
)
```

## Partitioned Writes

Write partitioned datasets efficiently:

```python
import pandas as pd

df = pd.DataFrame({
    "id": [1, 2, 3],
    "year": [2024, 2024, 2023],
    "month": [1, 2, 12],
    "value": [100.0, 200.0, 150.0]
})

# Using fsspec
fs = fsspec.filesystem("s3")
df.to_parquet(
    "s3://bucket/output/",
    partition_cols=["year", "month"],
    filesystem=fs
)
# Output structure: s3://bucket/output/year=2024/month=1/part-0.parquet
```

## Authentication

- **Auto-detection**: Uses default credential chain (AWS_PROFILE, ~/.aws/credentials, IAM role)
- **Explicit**: Pass `key=`, `secret=` to `fsspec.filesystem()` constructor
- **For S3-compatible** (MinIO, Ceph):
  ```python
  fs = fsspec.filesystem("s3", client_kwargs={
      "endpoint_url": "http://minio.local:9000"
  })
  ```

See `@data-engineering-storage-authentication` for detailed patterns.

## Performance Tips

1. **Column pruning**: `pd.read_parquet(columns=[...])` only reads needed columns
2. **Row group filtering**: Use `filters=` parameter for partitioned data
3. **Cache results**: Wrap filesystem with `simplecache::` or `filecache::`
   ```python
   cached_fs = fsspec.filesystem("simplecache", target_protocol="s3")
   df = pd.read_parquet("simplecache::s3://bucket/data.parquet", filesystem=cached_fs)
   ```
4. **Use Parquet, not CSV**: Parquet supports pushdown, compression, and typed storage
5. **For large datasets**: Consider PySpark or Dask instead of pandas (pandas loads everything into memory)

## Limitations

- pandas loads entire DataFrame into memory - not suitable for datasets larger than RAM
- For lazy evaluation and better performance with large files, use `@data-engineering-core` (Polars)
- Multi-file reads require manual iteration (use `fs.glob()` + list comprehension)

## Alternatives

- **Polars** (`@data-engineering-core`): Faster, memory-mapped, lazy evaluation
- **Dask**: Parallel pandas for out-of-core computation
- **PySpark**: Distributed processing for big data

---

## References

- [pandas I/O documentation](https://pandas.pydata.org/docs/user_guide/io.html)
- [fsspec documentation](https://filesystem-spec.readthedocs.io/)
- `@data-engineering-storage-remote-access/libraries/fsspec`
