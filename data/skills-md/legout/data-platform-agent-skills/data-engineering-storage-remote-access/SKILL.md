---
name: data-engineering-storage-remote-access
description: "Cloud storage access in Python: fsspec, pyarrow.fs, obstore libraries, plus integrations with Polars, DuckDB, PyArrow, Delta Lake, and Iceberg."
dependsOn: ["@data-engineering-core", "@data-engineering-storage-authentication", "@data-engineering-storage-formats"]
---

# Remote Storage Access

Comprehensive guide to accessing cloud storage (S3, GCS, Azure) and remote filesystems in Python. Covers three major libraries - **fsspec**, **pyarrow.fs**, and **obstore** - and their integration with data engineering tools.

## Quick Comparison

| Feature | fsspec | pyarrow.fs | obstore |
|---------|--------|------------|---------|
| **Best For** | Broad compatibility, ecosystem integration | Arrow-native workflows, Parquet | High-throughput, performance-critical |
| **Backends** | S3, GCS, Azure, HTTP, FTP, 20+ more | S3, GCS, HDFS, local | S3, GCS, Azure, local |
| **Performance** | Good (with caching) | Excellent for Parquet | **9x faster** for concurrent ops |
| **Dependencies** | Backend-specific (s3fs, gcsfs) | Bundled with PyArrow | **Zero Python deps** (Rust) |
| **Async Support** | Yes (aiohttp) | Limited | Native sync/async |
| **DataFrame Integration** | Universal | PyArrow-native | Via fsspec wrapper |
| **Maturity** | Very mature (2018+) | Mature | New (2025), rapidly evolving |

## When to Use Which?

### Use fsspec when:
- You need broad ecosystem compatibility (pandas, xarray, Dask)
- Working with multiple storage backends (S3, GCS, Azure, HTTP)
- You need protocol chaining and caching features
- Your workflow involves diverse data formats beyond Parquet

### Use pyarrow.fs when:
- Your pipeline is Arrow/Parquet-native
- You need zero-copy integration with PyArrow datasets
- Predicate pushdown and column pruning are critical
- Working with partitioned Parquet datasets

### Use obstore when:
- Performance is paramount (many small files, high concurrency)
- You need async/await support for concurrent operations
- You want minimal dependencies (Rust-based)
- Working with large-scale data ingestion/egestion

## Skill Dependencies

Prerequisites:
- `@data-engineering-core` - Polars, DuckDB, PyArrow basics
- `@data-engineering-storage-authentication` - AWS, GCP, Azure auth patterns
- `@data-engineering-storage-formats` - Parquet, Arrow, Lance, Zarr, Avro, ORC

Related:
- `@data-engineering-storage-lakehouse` - Delta Lake, Iceberg on cloud storage
- `@data-engineering-orchestration` - dbt with cloud storage

---

## Detailed Guides

### Library Deep Dives
- `@data-engineering-storage-remote-access-libraries-fsspec` - Universal filesystem interface
- `@data-engineering-storage-remote-access-libraries-pyarrow-fs` - Native Arrow integration
- `@data-engineering-storage-remote-access-libraries-obstore` - High-performance Rust

### DataFrame Integrations
- `@data-engineering-storage-remote-access-integrations-polars` - Polars + cloud URIs
- `@data-engineering-storage-remote-access-integrations-duckdb` - DuckDB HTTPFS extension
- `@data-engineering-storage-remote-access-integrations-pandas` - Pandas + remote files
- `@data-engineering-storage-remote-access-integrations-pyarrow` - PyArrow datasets
- `@data-engineering-storage-remote-access-integrations-delta-lake` - Delta on S3/GCS/Azure
- `@data-engineering-storage-remote-access-integrations-iceberg` - Iceberg with cloud catalogs

### Infrastructure Patterns
- `@data-engineering-storage-authentication` - AWS, GCP, Azure auth patterns, IAM roles, service principals
- See `performance.md` in this skill - Caching, concurrency, async
- See `patterns.md` in this skill - Incremental loading, partitioned writes, cross-cloud copy

### Storage Formats
- `@data-engineering-storage-formats` - Parquet, Arrow/Feather, Lance, Zarr, Avro, ORC

---

## Quick Start Example

```python
import fsspec
import pyarrow.fs as fs
import obstore as obs

# Method 1: fsspec (universal)
s3_fs = fsspec.filesystem('s3')
with s3_fs.open('s3://bucket/data.parquet', 'rb') as f:
    df = pl.read_parquet(f)

# Method 2: pyarrow.fs (Arrow-native)
s3_pa = fs.S3FileSystem(region='us-east-1')
table = pq.read_table("bucket/data.parquet", filesystem=s3_pa)

# Method 3: obstore (high-performance)
from obstore.store import S3Store
store = S3Store(bucket='my-bucket', region='us-east-1')
data = obs.get(store, 'data.parquet').bytes()

# All approaches work - choose based on your performance and ecosystem needs
```

---

## Authentication

All three libraries follow standard cloud authentication patterns: explicit credentials → environment variables → config files → IAM roles/Managed Identities.

**See:** `@data-engineering-storage-authentication`

## Performance Optimization

Key strategies:
- **Caching**: fsspec's `SimpleCache` for repeated access
- **Concurrency**: obstore async API for many small files
- **Predicate pushdown**: Filter at storage layer using partitioning
- **Column pruning**: Read only required columns

**See:** `@data-engineering-storage-remote-access/performance.md`

---

## References

- [fsspec Documentation](https://filesystem-spec.readthedocs.io/)
- [PyArrow Filesystems](https://arrow.apache.org/docs/python/filesystems.html)
- [obstore Documentation](https://developmentseed.org/obstore/)
- [s3fs Documentation](https://s3fs.readthedocs.io/)
- [gcsfs Documentation](https://gcsfs.readthedocs.io/)
