---
name: data-engineering-storage-remote-access-libraries-fsspec
description: "Comprehensive guide to fsspec: the universal filesystem interface for Python. Covers S3, GCS, Azure via s3fs, gcsfs, adlfs; protocol chaining, caching, async operations, and integration with the data ecosystem."
dependsOn: ["@data-engineering-core", "@data-engineering-storage-authentication"]
---

# fsspec: Universal Filesystem Interface

fsspec provides a unified API for local and remote filesystems, integrating seamlessly with pandas, xarray, Dask, and many other Python data tools.

## Installation

```bash
# Core only (no remote support)
pip install fsspec

# With specific backends
pip install fsspec[s3]        # S3 via s3fs
pip install fsspec[gcs]       # GCS via gcsfs
pip install fsspec[s3,gcs,azure]  # Multiple backends

# Or install backends directly
pip install s3fs gcsfs adlfs
```

## Basic Usage

```python
import fsspec
import pandas as pd

# List available protocols
print(fsspec.available_protocols())
# ['file', 'memory', 'http', 'https', 's3', 's3a', 'gcs', 'gs', 'abfss', ...]

# Create filesystem instances
local_fs = fsspec.filesystem('file')
s3_fs = fsspec.filesystem('s3', anon=False)  # Uses boto3 credentials
gcs_fs = fsspec.filesystem('gcs')             # Uses GCP credentials

# Basic operations
s3_fs.ls('my-bucket/data/')                   # List files
s3_fs.exists('my-bucket/data/file.csv')       # Check existence
s3_fs.mkdir('my-bucket/new-folder')           # Create directory

# Read file as bytes
with s3_fs.open('s3://my-bucket/data/file.txt', 'rb') as f:
    content = f.read()

# Read CSV directly into pandas
with s3_fs.open('s3://my-bucket/data/large.csv', 'rb') as f:
    df = pd.read_csv(f, compression='gzip')
```

## Protocol Chaining & Caching

```python
# SimpleCache: Cache remote files locally for faster repeated access
import fsspec

# First read downloads, subsequent reads use cache
cached_file = fsspec.open_local(
    "simplecache::s3://my-bucket/large-file.nc",
    simplecache={'cache_storage': '/tmp/fsspec_cache', 'compression': None}
)

# Chain multiple protocols
# Read from HTTPS, cache locally, decompress on the fly
with fsspec.open(
    "simplecache::gzip::https://example.com/data.csv.gz",
    compression='gzip'
) as f:
    df = pd.read_csv(f)

# Other useful wrappers:
# - "filecache::" - Persistent disk cache
# - "gzip::" - Decompression
# - "zip::" - Zip file access
```

## Advanced S3 Features

```python
import s3fs

# Detailed S3 configuration
fs = s3fs.S3FileSystem(
    key='AKIA...',
    secret='...',
    token='...',              # Temporary session token
    client_kwargs={
        'region_name': 'us-east-1',
        'endpoint_url': 'https://s3-compatible.local',  # MinIO, etc.
    },
    config_kwargs={
        'max_pool_connections': 50,
        'retries': {'max_attempts': 5}
    },
    skip_instance_cache=True   # Don't cache bucket listings
)

# Async operations
import asyncio

async def read_multiple():
    fs = s3fs.S3FileSystem(asynchronous=True)
    await fs.set_session()  # Establish async session

    # Concurrent reads (use _cat_file for bytes)
    data = await asyncio.gather(
        fs._cat_file('bucket/file1.parquet'),
        fs._cat_file('bucket/file2.parquet'),
        fs._cat_file('bucket/file3.parquet')
    )
    return data

# S3-specific features
fs.find('my-bucket', prefix='data/2024')  # List with prefix
fs.du('my-bucket/data')                   # Disk usage
fs.rm('my-bucket/temp/', recursive=True)  # Recursive delete
```

## Authentication

fsspec backends follow standard cloud authentication:
1. Explicit credentials (passed to constructor)
2. Environment variables (AWS_ACCESS_KEY_ID, GOOGLE_APPLICATION_CREDENTIALS, etc.)
3. Config files (~/.aws/credentials, gcloud CLI)
4. IAM roles / managed identities

See `@data-engineering-storage-authentication` for detailed patterns.

## When to Use fsspec

Choose fsspec when:
- You need broad ecosystem compatibility (pandas, xarray, Dask)
- Working with multiple storage backends (S3, GCS, Azure, HTTP)
- You need protocol chaining and caching features
- Your workflow involves diverse data formats beyond Parquet

## Performance Considerations

- ✅ Use `filecache::` instead of `simplecache::` for persistent caching across sessions
- ✅ Increase `max_pool_connections` for high concurrency
- ✅ Use async API for many concurrent small file operations
- ⚠️ For pure Parquet workflows with high throughput, consider `pyarrow.fs` instead
- ⚠️ For maximum performance on large concurrent operations, consider `obstore`

## Integration with Data Engineering Tools

- **Polars**: `pl.read_parquet("s3://bucket/file.parquet", storage_options={...})`
- **DuckDB**: `duckdb.register_filesystem(fsspec.filesystem('s3'))`
- **Pandas**: `pd.read_csv("s3://bucket/file.csv")` (auto-detects fsspec)
- **PyArrow**: Wrap fsspec with `pyarrow.fs.PyFileSystem(fs.FSSpecHandler(fs))`

For detailed integration patterns, see:
- `@data-engineering-storage-remote-access/integrations/polars`
- `@data-engineering-storage-remote-access/integrations/duckdb`
- `@data-engineering-storage-remote-access/integrations/pandas`

---

## References

- [fsspec Documentation](https://filesystem-spec.readthedocs.io/)
- [s3fs Documentation](https://s3fs.readthedocs.io/)
- [gcsfs Documentation](https://gcsfs.readthedocs.io/)
- [adlfs Documentation](https://github.com/fsspec/adlfs)
