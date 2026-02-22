---
name: data-engineering-storage-remote-access-libraries-obstore
description: "High-performance Rust-based remote filesystem library. Covers store creation, basic operations, async API, streaming uploads, Arrow integration, and fsspec compatibility wrapper."
dependsOn: ["@data-engineering-core", "@data-engineering-storage-authentication"]
---

# obstore: High-Performance Rust-Based Storage

obstore (released 2025) provides a minimal, stateless API built on Rust's `object_store` crate, offering superior performance for concurrent operations (up to 9x faster than Python-based alternatives).

## Installation

```bash
pip install obstore

# Or with conda
conda install -c conda-forge obstore
```

## Core Concepts

obstore uses **top-level functions** (not methods) and a functional API. All operations are functions like `obs.get(store, path)`, not `store.get(path)`.

## Creating Stores

```python
import obstore as obs
from obstore.store import S3Store, GCSStore, AzureStore, LocalStore

# S3 Store
s3 = S3Store(
    bucket="my-bucket",
    region="us-east-1",
    access_key_id="AKIA...",
    secret_access_key="...",
    # Or use environment credentials
)

# GCS Store
gcs = GCSStore(
    bucket="my-bucket",
    # Uses GOOGLE_APPLICATION_CREDENTIALS by default
)

# Azure Store
azure = AzureStore(
    container="my-container",
    account_name="myaccount",
    account_key="...",
    # Or use DefaultAzureCredential
)

# Local filesystem
local = LocalStore("/path/to/root")

# From environment (picks up standard env vars)
s3 = S3Store.from_env(bucket="my-bucket")
gcs = GCSStore.from_env(bucket="my-bucket")
```

## Basic Operations

```python
import obstore as obs

store = S3Store(bucket="my-bucket", region="us-east-1")

# Put object (bytes)
obs.put(store, "hello.txt", b"Hello, World!")

# Put from file
with open("local-file.csv", "rb") as f:
    obs.put(store, "data/file.csv", f)

# Get object
response = obs.get(store, "hello.txt")
print(response.bytes())   # b"Hello, World!"
print(response.meta)      # Object metadata (size, mtime, etag, etc.)

# Get range (efficient partial reads)
partial = obs.get_range(store, "large-file.bin", offset=0, length=1024)

# Stream download
stream = obs.get(store, "large-file.bin")
for chunk in stream.stream(min_chunk_size=8 * 1024 * 1024):
    process(chunk)

# List objects (streaming, no pagination needed!)
for obj in obs.list(store, prefix="data/2024/"):
    print(f"{obj['path']}: {obj['size']} bytes")

# List with delimiter (like directory listing)
result = obs.list_with_delimiter(store, prefix="data/")
print(result["common_prefixes"])  # "directories"
print(result["objects"])          # files

# Delete
obs.delete(store, "old-file.txt")

# Copy within same store
obs.copy(store, "src/file.txt", "dst/file.txt")

# Rename/move
obs.rename(store, "old-name.txt", "new-name.txt")

# Check existence (via head)
try:
    meta = obs.head(store, "file.txt")
    print(f"Exists: {meta['size']} bytes")
except obs.NotFoundError:
    print("File not found")
```

## Async API

```python
import asyncio
import obstore as obs
from obstore.store import S3Store

async def main():
    store = S3Store(bucket="my-bucket", region="us-east-1")

    # Concurrent uploads
    await asyncio.gather(
        obs.put_async(store, "file1.txt", b"content1"),
        obs.put_async(store, "file2.txt", b"content2"),
        obs.put_async(store, "file3.txt", b"content3"),
    )

    # Concurrent downloads
    responses = await asyncio.gather(
        obs.get_async(store, "file1.txt"),
        obs.get_async(store, "file2.txt"),
        obs.get_async(store, "file3.txt"),
    )

    for resp in responses:
        print(await resp.bytes_async())

asyncio.run(main())
```

## Streaming Uploads

```python
import asyncio
import obstore as obs
from obstore.store import S3Store

store = S3Store(bucket="my-bucket")

# Upload from generator (streaming, memory-efficient)
def data_generator():
    for i in range(1000):
        yield f"Row {i}\n".encode()

obs.put(store, "output.txt", data_generator())

# Upload from async iterator
async def async_data():
    for i in range(1000):
        await asyncio.sleep(0)
        yield f"Row {i}\n".encode()

async def upload_async():
    await obs.put_async(store, "output-async.txt", async_data())

asyncio.run(upload_async())

# Automatic multipart upload for large files
# (triggered automatically based on size)
with open("huge-file.bin", "rb") as f:
    obs.put(store, "huge-file.bin", f)  # Multi-part automatically
```

## Arrow Integration

```python
import obstore as obs
from obstore.store import S3Store

store = S3Store(bucket="my-bucket")

# Return list results as Arrow table (faster, more memory-efficient)
arrow_table = obs.list(store, prefix="data/", return_arrow=True)
print(arrow_table.schema)
# pyarrow.Schema
# ├── path: string
# ├── size: int64
# ├── last_modified: timestamp[ns]
# └── etag: string

# Process with PyArrow/Polars
import polars as pl
df = pl.from_arrow(arrow_table)
```

## fsspec Compatibility

obstore provides an fsspec-compatible wrapper:

```python
from obstore.fsspec import FsspecStore, register
import pyarrow.parquet as pq

# Method 1: Register as default handler for protocols
register()
# Now fsspec uses obstore internally
import fsspec
fs = fsspec.filesystem("s3", region="us-east-1")

# Method 2: Use FsspecStore directly
fs = FsspecStore("s3", bucket="my-bucket", region="us-east-1")
# or
fs = FsspecStore.from_store(s3_store_object)

# Use with PyArrow
parquet_file = pq.ParquetFile(
    "s3://bucket/data/file.parquet",
    filesystem=fs
)
```

## When to Use obstore

Choose obstore when:
- ✅ **Performance is paramount** (many small files, high concurrency)
- ✅ **You need async/await** for concurrent operations
- ✅ **Minimal dependencies** are desired (Rust-based, no Python C extensions)
- ✅ **Streaming uploads** from generators/iterators
- ✅ **Large-scale data ingestion/egestion**

## Performance Comparison

| Operation | fsspec | pyarrow.fs | obstore |
|-----------|--------|------------|---------|
| Concurrent small files | Moderate | Moderate | **9x faster** |
| Async support | Yes (aiohttp) | Limited | **Native** |
| Streaming uploads | Yes | Limited | **Yes (efficient)** |
| Parquet pushdown | Via PyArrow | **Excellent** | Via PyArrow |
| Maturity (2025) | Very high | High | Rapidly growing |

## Authentication

See `@data-engineering-storage-authentication` for credential patterns. All `S3Store`, `GCSStore`, `AzureStore` constructors accept explicit credentials or use environment variables via `from_env()`.

---

## References

- [obstore Documentation](https://developmentseed.org/obstore/)
- [PyPI: obstore](https://pypi.org/project/obstore/)
- [object_store (Rust)](https://docs.rs/object_store/latest/object_store/)
