---
name: data-engineering-storage-formats
description: "Modern data serialization formats: Parquet, Apache Arrow (Feather/IPC), Lance (ML-native), Zarr (chunked arrays), Avro, and ORC. Covers compression, partitioning, and format selection."
dependsOn: ["@data-engineering-core"]
---

# Data Storage Formats

Comprehensive guide to modern data serialization formats for analytics and machine learning: Parquet, Apache Arrow, Lance, Zarr, Avro, and ORC. Learn compression tradeoffs, partitioning strategies, and when to use each format.

## Quick Comparison

| Format | Type | Best For | Compression | Schema Evolution | Random Access |
|--------|------|----------|-------------|------------------|---------------|
| **Parquet** | Columnar | Analytics, data lakes | ✅ (Snappy, Zstd, LZ4) | ✅ (add/drop) | ✅ (row groups) |
| **Arrow/Feather** | Columnar | In-memory, IPC, ML | ✅ (LZ4, Zstd) | Limited | ✅ (record batches) |
| **Lance** | Columnar | ML pipelines, vectors | ✅ (Zstd, LZ4) | ✅ | ✅ (multi-modal) |
| **Zarr** | Chunked arrays | ML, geospatial, N-dim | ✅ (Blosc, gzip) | ✅ (chunks) | ✅ (chunk-level) |
| **Avro** | Row-based | Streaming, Kafka | ✅ (deflate, snappy) | ✅ (full schema) | ❌ (sequential) |
| **ORC** | Columnar | Hive, Hadoop | ✅ (ZLIB, Snappy) | Limited | ✅ (stripe-level) |

## When to Use Which?

### Choose Parquet when:
- You need broad compatibility (Spark, DuckDB, Polars, pandas)
- Analytics queries with filtering/aggregation
- Data lake storage with partitioning
- Mature ecosystem with best compression support

### Choose Arrow/Feather when:
- Zero-copy sharing between processes (IPC)
- Fast serialization/deserialization for ML training
- In-memory format persistence
- Need Arrow ecosystem (Kernel, CUDA, etc.)

### Choose Lance when:
- Machine learning pipelines with embeddings/vectors
- Need multi-modal data (text + images + audio + vectors)
- Versioned datasets with Git-like branching
- Cloud-native (S3/GCS) with no metadata catalog required

### Choose Zarr when:
- N-dimensional arrays (tensors, satellite imagery, medical scans)
- Chunked, compressed storage for ML
- Parallel reads/writes across chunks
- Cloud-optimized (s3://, gs:// with fsspec)

### Choose Avro when:
- Streaming to Kafka/Kinesis
- Schema evolution is critical (backward/forward)
- Row-based access pattern
- Need to serialize objects/records

### Choose ORC when:
- Working primarily with Hive/Hadoop
- Hive ACID transactions
- Legacy big data pipelines

## Skill Dependencies

- `@data-engineering-core` - Polars/DuckDB to read/write these formats
- `@data-engineering-storage-remote-access` - Cloud storage backends
- `@data-engineering-storage-lakehouse` - Table formats (Delta/Iceberg/Hudi) built on these

---

## Detailed Guides

### Parquet
See: `parquet.md` (detailed deep dive)

Parquet is the de facto standard for columnar analytics storage.

```python
import polars as pl
import pyarrow.parquet as pq
import pyarrow as pa

# Write with Polars
df = pl.DataFrame({"id": [1, 2, 3], "value": [100.0, 200.0, 150.0]})
df.write_parquet("data.parquet", compression="zstd")

# Write with PyArrow (more control)
table = pa.Table.from_pandas(df)
pq.write_table(
    table,
    "data.parquet",
    compression="ZSTD",
    compression_level=3,
    row_group_size=100000,  # Target rows per row group
    use_dictionary=True     # Dictionary encoding for strings
)

# Read with column pruning
df = pl.read_parquet("data.parquet", columns=["id", "value"])

# Dataset scanning with predicate pushdown
lazy_df = pl.scan_parquet("s3://bucket/dataset/**/*.parquet")
result = lazy_df.filter(pl.col("value") > 100).collect()
```

**Key concepts:**
- Row groups: Horizontal partitioning, enables skipping files
- Column chunks: Within each row group, each column stored separately
- Pages: Smallest unit (within column chunks), enables column pruning
- Statistics: min/max/null count for predicate pushdown
- Dictionary encoding: For low-cardinality strings

---

### Apache Arrow (Feather/IPC)

Arrow is an in-memory columnar format. Feather (v1/v2) and IPC are on-disk/serialization formats.

```python
import pyarrow as pa
import polars as pl

# Create Arrow table
table = pa.table({
    "id": [1, 2, 3],
    "value": [100.0, 200.0, 150.0],
    "category": ["A", "B", "A"]
})

# Write Feather file (Arrow IPC on disk)
pa.feather.write_feather(table, "data.feather")

# Read back
table2 = pa.feather.read_table("data.feather")

# Polars integration (zero-copy)
df = pl.from_arrow(table)  # No copy!
df.write_ipc("data.ipc")   # IPC format (stream or file)

# Arrow Flight RPC (network streaming)
from pyarrow.flight import FlightClient, FlightDescriptor

client = FlightClient("grpc+tcp://localhost:5005")
reader = client.do_get(descriptor)
table = reader.read_all()
```

**When to use Arrow/Feather:**
- Fast serialization for ML (TensorFlow, PyTorch)
- Inter-process communication (shared memory, files)
- Zero-copy between Polars/Pandas/PyArrow
- Not ideal for large-scale data lakes (no built-in partitioning)

---

### Lance

Lance is an ML-native columnar format built on Arrow, with integrated vector search and versioning.

```python
import lancedb
import polars as pl
from sentence_transformers import SentenceTransformer

# Create Lance dataset
db = lancedb.connect("./data.lance")
df = pl.DataFrame({
    "id": [1, 2, 3],
    "text": ["Hello world", "Goodbye world", "Machine learning"],
    "vector": [[0.1] * 128, [0.2] * 128, [0.3] * 128]  # Embeddings
})

# Write (creates .lance directory)
table = db.create_table("my_table", df)

# Append more data
table.add(df2)

# Vector search
results = table.search([0.1] * 128).limit(5).to_pandas()

# Versioned updates (like git)
table = db.create_table("versioned", df, mode="overwrite")
# Each overwrite creates a new version
table.checkout(version=1)  # Access previous version

# Cloud storage
db = lancedb.connect("s3://bucket/dataset/")
```

**Lance advantages:**
- Built-in vector indexes (IVF_PQ, HNSW) - no separate DB needed
- Multi-modal: store images, audio, text, vectors in same table
- Version control for datasets
- Zero-copy reads via memory mapping
- No metadata catalog needed (self-contained)

---

### Zarr

Zarr is a chunked, compressed N-dimensional array format, popular in ML, geospatial, and scientific computing.

```python
import zarr
import numpy as np

# Create Zarr array (chunked, compressed)
z = zarr.open(
    'data.zarr',
    mode='w',
    shape=(1000000, 1000),  # Large 2D array
    chunks=(10000, 1000),    # Chunk size
    dtype='f4',
    compressor=zarr.Blosc(cname='zstd', clevel=3)
)

# Write chunks
z[:10000, :] = np.random.rand(10000, 1000).astype('f4')

# Read partial (only loads needed chunks)
slice = z[5000:6000, :]

# Group (like HDF5 groups)
g = zarr.open_group('experiment.zarr', mode='w')
g.create_dataset('images', data=image_array, chunks=True)
g.create_dataset('labels', data=label_array)

# Cloud storage (s3://)
import s3fs
fs = s3fs.S3FileSystem(anon=False)
store = s3fs.S3Map(root='mybucket/data.zarr', s3=fs)
zarr.open(store=store, mode='w', shape=(1000, 1000), chunks=(100, 100), dtype='f4')
```

**Zarr advantages:**
- Parallel reads/writes across chunks
- Cloud-optimized (each chunk is a separate object)
- Schema flexibility (groups, hierarchies)
- Good for terabyte-scale arrays
- Growing ecosystem: xarray, dask, napari

---

### Avro

Row-based format with rich schema evolution. Common in streaming (Kafka).

```python
import fastavro
import json

# Define schema
schema = {
    "type": "record",
    "name": "Event",
    "fields": [
        {"name": "id", "type": "int"},
        {"name": "event_type", "type": "string"},
        {"name": "timestamp", "type": "long"}  # Unix epoch
    ]
}

# Write Avro file
with open("events.avro", "wb") as out:
    fastavro.writer(out, schema, [
        {"id": 1, "event_type": "click", "timestamp": 1700000000},
        {"id": 2, "event_type": "view", "timestamp": 1700000001}
    ])

# Read
with open("events.avro", "rb") as fo:
    records = list(fastavro.reader(fo))

# Kafka integration (confluent-kafka)
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry.avro import AvroSerializer

# Schema Registry integration ensures compatibility
```

**Avro vs Parquet:**
- Avro: row-based, append-only, streaming-friendly
- Parquet: columnar, analytics-friendly, predicate pushdown
- Convert: `polars.read_avro()` → `write_parquet()` for ETL

---

### ORC

Optimized Row Columnar, primarily for Hive/Hadoop ecosystems.

```python
import pyarrow.orc as orc

# Write
table = pa.table({
    "id": [1, 2, 3],
    "value": [100.0, 200.0, 150.0]
})
orc.write_table(table, "data.orc")

# Read
table = orc.read_table("data.orc")
df = table.to_pandas()

# Stripe-level statistics (similar to Parquet row groups)
```

**ORC vs Parquet:**
- ORC: Hive-centric, ACID transactions, better compression for Hive queries
- Parquet: More ecosystem support (Spark, DuckDB, Polars), better column pruning
- Modern stacks typically prefer Parquet

---

## Format Selection Guide

### Use Case Matrix

| Use Case | Recommended Format | Reason |
|-----------|-------------------|--------|
| Data lake analytics | **Parquet** | Mature, partitioning, ecosystem |
| ML training data | **Arrow/Feather** or **Lance** | Zero-copy, vector support |
| Geospatial arrays | **Zarr** | Chunked, N-dimensional, cloud-optimized |
| Streaming/Kafka | **Avro** | Schema evolution, row-based |
| Legacy Hive | **ORC** | Compatibility |
| Feature stores | **Lance** or **Delta** | Versioning, vectors |
| IPC between processes | **Arrow IPC** or **Feather** | Zero-copy, fast |
| Quick exports | **Parquet** (Zstd) | Good compression/decompression speed |

### Compression Codec Comparison

| Codec | Compression Ratio | Speed (Compress/Decompress) | Best For |
|-------|-------------------|-----------------------------|----------|
| **Snappy** | Low (~2:1) | ⚡⚡⚡ Fast | Fast analytics, default Parquet |
| **Zstd** | Medium-High (~4:1) | ⚡⚡ Fast | General purpose, good balance |
| **LZ4** | Low-Medium (~2.5:1) | ⚡⚡⚡ Very fast | Real-time streaming |
| **Gzip** | High (~5:1) | ⚡ Slow | Archival, cold storage |
| **Blosc (zstd)** | Medium | ⚡⚡ | Zarr arrays |

---

## Advanced Patterns

### Converting Formats

```python
# Avro → Parquet (ETL)
import polars as pl
df = pl.read_avro("input.avro")
df.write_parquet("output.parquet")

# Arrow → Lance (ML pipeline)
import lancedb
table = pa.feather.read_table("data.feather")
db = lancedb.connect("./dataset.lance")
db.create_table("embeddings", table)

# Zarr → Parquet (geospatial to analytics)
import dask.array as da
z = da.from_zarr("sar.zarr")
df = z.mean(axis=0).to_dataframe()  # Aggregate and convert
df.to_parquet("summary.parquet")
```

### Partitioning Strategies

**Parquet partition discovery:**
```python
# Hive-style: year=2024/month=01/day=01/
dataset = ds.dataset(
    "s3://bucket/events/",
    filesystem=s3_fs,
    format="parquet",
    partitioning=ds.HivePartitioning.discover()
)

# Directory partitioning: year/2024/month/01/
dataset = ds.dataset(
    "s3://bucket/events/year=2024/month=01/",
    filesystem=s3_fs
)
```

**Lance partitioning:** Built-in via `to_lance()`:
```python
df.write_lance("data.lance", partition_by=["year", "month"])
```

**Zarr chunking:**
```python
# Chunk by spatial region for geospatial
z = zarr.open(
    "satellite.zarr",
    mode='w',
    shape=(10000, 10000),  # 10000x10000 pixels
    chunks=(1000, 1000),   # 1000x1000 tiles
    dtype='float32'
)
```

---

## Performance Tuning

### Parquet
- Row group size: 100K-1M rows for optimal skipping
- Dictionary encoding: Enable for low-cardinality strings
- Compression: Zstd level 3 for balance, Snappy for speed
- Column order: Put high-selectivity columns first (min/max statistics better)

### Lance
- Vector index type: IVF_PQ for large datasets (>1M), HNSW for smaller/higher recall
- Use `create_index()` after bulk load, not during writes
- Batch writes for throughput

### Zarr
- Chunk size: Align with access pattern (e.g., time-series: chunk by time)
- Compression: Blosc+zstd, tune clevel (3-5)
- Consider Zipf+Shuffle filters for structured arrays

---

## Emerging Formats (2024-2025)

- **Lance** (2022): Gaining traction in ML community, integrated with RAPIDS, Polars, PyTorch
- **Soar** (2023): Columnar format optimized for AI training (similar to Lance, different ecosystem)
- **Vortex**: Not widely adopted yet - if you mean **Arrow**'s compute kernels (not a format)
- **DuckDB's `.duckdb` format**: Embedded SQLite-like for DuckDB persistence
- **Delta Lake / Iceberg** (table formats): Already in lakehouse skill

---

## Best Practices

1. ✅ **Default to Parquet** - Broadest compatibility, good compression, ecosystem tooling
2. ✅ **Use Arrow/Feather for ML staging** - Zero-copy between training frameworks
3. ✅ **Use Lance when vectors are first-class** - No separate vector DB needed
4. ✅ **Use Zarr for N-dim arrays** - Geospatial, video, 3D data
5. ✅ **Compress everything** - Snappy (fast) or Zstd (balanced)
6. ✅ **Partition wisely** - By date/region/tenant to enable pruning
7. ❌ **Don't** use Avro for analytics (no column pruning, row-based)
8. ❌ **Don't** use ORC unless in Hive Hadoop world
9. ❌ **Don't** store wide tables in single Parquet files - Partition or use Delta/Iceberg

---

## References

- [Apache Parquet Format](https://parquet.apache.org/)
- [Apache Arrow Format](https://arrow.apache.org/docs/format/)
- [Lance Format](https://lancedb.github.io/lancedb/concepts/storage_format/)
- [Zarr Format](https://zarr.readthedocs.io/en/stable/spec/v2.html)
- [Apache Avro Specification](https://avro.apache.org/docs/current/spec.html)
- `@data-engineering-core` - Reading/writing with Polars/DuckDB
- `@data-engineering-storage-lakehouse` - Table formats built on these (Delta/Iceberg)
- `@data-engineering-storage-remote-access` - Using these formats with cloud storage backends (S3, GCS, Azure)
- `@data-engineering-storage-authentication` - Credential patterns for accessing cloud storage
