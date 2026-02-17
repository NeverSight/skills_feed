---
name: dask
description: Use when "Dask", "parallel computing", "distributed computing", "larger than memory", or asking about "parallel pandas", "parallel numpy", "out-of-core", "multi-file processing", "cluster computing", "lazy evaluation dataframe"
version: 1.0.0
---

# Dask Parallel and Distributed Computing

Scale pandas/NumPy workflows beyond memory and across clusters.

## When to Use

- Datasets exceed available RAM
- Need to parallelize pandas or NumPy operations
- Processing multiple files efficiently (CSVs, Parquet)
- Building custom parallel workflows
- Distributing workloads across multiple cores/machines

---

## Dask Collections

| Collection | Like | Use Case |
|------------|------|----------|
| **DataFrame** | pandas | Tabular data, CSV/Parquet |
| **Array** | NumPy | Numerical arrays, matrices |
| **Bag** | list | Unstructured data, JSON logs |
| **Delayed** | Custom | Arbitrary Python functions |

**Key concept**: All collections are lazy—computation happens only when you call `.compute()`.

---

## Lazy Evaluation

| Function | Behavior | Use |
|----------|----------|-----|
| `dd.read_csv()` | Lazy load | Large CSVs |
| `dd.read_parquet()` | Lazy load | Large Parquet |
| Operations | Build graph | Chain transforms |
| `.compute()` | Execute | Get final result |

**Key concept**: Dask builds a task graph of operations, optimizes it, then executes in parallel. Call `.compute()` once at the end, not after every operation.

---

## Schedulers

| Scheduler | Best For | Start |
|-----------|----------|-------|
| **threaded** | NumPy/Pandas (releases GIL) | Default |
| **processes** | Pure Python (GIL bound) | `scheduler='processes'` |
| **synchronous** | Debugging | `scheduler='synchronous'` |
| **distributed** | Monitoring, scaling, clusters | `Client()` |

### Distributed Scheduler

| Feature | Benefit |
|---------|---------|
| Dashboard | Real-time progress monitoring |
| Cluster scaling | Add/remove workers |
| Fault tolerance | Retry failed tasks |
| Worker resources | Memory management |

---

## Chunking Concepts

### DataFrame Partitions

| Concept | Description |
|---------|-------------|
| **Partition** | Subset of rows (like a mini DataFrame) |
| **npartitions** | Number of partitions |
| **divisions** | Index boundaries between partitions |

### Array Chunks

| Concept | Description |
|---------|-------------|
| **Chunk** | Subset of array (n-dimensional block) |
| **chunks** | Tuple of chunk sizes per dimension |
| **Optimal size** | ~100 MB per chunk |

**Key concept**: Chunk size is critical. Too small = scheduling overhead. Too large = memory issues. Target ~100 MB.

---

## DataFrame Operations

### Supported (parallel)

| Category | Operations |
|----------|------------|
| **Selection** | `filter`, `loc`, column selection |
| **Aggregation** | `groupby`, `sum`, `mean`, `count` |
| **Transforms** | `apply` (row-wise), `map_partitions` |
| **Joins** | `merge`, `join` (shuffles data) |
| **I/O** | `read_csv`, `read_parquet`, `to_parquet` |

### Avoid or Use Carefully

| Operation | Issue | Alternative |
|-----------|-------|-------------|
| `iterrows` | Kills parallelism | `map_partitions` |
| `apply(axis=1)` | Slow | `map_partitions` |
| Repeated `compute()` | Inefficient | Single `compute()` at end |
| `sort_values` | Expensive shuffle | Avoid if possible |

---

## Common Patterns

### ETL Pipeline

1. `scan_*` or `read_*` (lazy load)
2. Chain filters and transforms
3. Single `.compute()` or `.to_parquet()`

### Multi-File Processing

| Pattern | Description |
|---------|-------------|
| Glob patterns | `dd.read_csv('data/*.csv')` |
| Partition per file | Natural parallelism |
| Output partitioned | `to_parquet('output/')` |

### Custom Operations

| Method | Use Case |
|--------|----------|
| `map_partitions` | Apply function to each partition |
| `map_blocks` | Apply function to each array block |
| `delayed` | Wrap arbitrary Python functions |

---

## Best Practices

| Practice | Why |
|----------|-----|
| Don't load locally first | Let Dask handle loading |
| Single compute() at end | Avoid redundant computation |
| Use Parquet | Faster than CSV, columnar |
| Match partition to files | One partition per file |
| Check task graph size | `len(ddf.__dask_graph__())` < 100k |
| Use distributed for debugging | Dashboard shows progress |

---

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Loading with pandas first | Use `dd.read_*` directly |
| compute() in loops | Collect all, single compute() |
| Too many partitions | Repartition to ~100 MB each |
| Memory errors | Reduce chunk size, add workers |
| Slow shuffles | Avoid sorts/joins when possible |

---

## vs Alternatives

| Tool | Best For | Trade-off |
|------|----------|-----------|
| **Dask** | Scale pandas/NumPy, clusters | Setup complexity |
| **Polars** | Fast in-memory | Must fit in RAM |
| **Vaex** | Out-of-core single machine | Limited operations |
| **Spark** | Enterprise, SQL-heavy | Infrastructure |

## Resources

- Docs: <https://docs.dask.org/>
- Best Practices: <https://docs.dask.org/en/stable/best-practices.html>
- Examples: <https://examples.dask.org/>
