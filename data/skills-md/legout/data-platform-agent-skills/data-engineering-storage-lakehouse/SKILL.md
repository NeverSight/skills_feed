---
name: data-engineering-storage-lakehouse
description: "Lakehouse table formats: Delta Lake, Apache Iceberg, and Apache Hudi for ACID transactions, schema evolution, and time travel on data lakes."
dependsOn: ["@data-engineering-core"]
---

# Lakehouse Formats

Lakehouse formats add ACID transactions, schema evolution, and time travel to data lakes stored on object storage (S3, GCS, Azure). This skill covers the three major open table formats: Delta Lake, Apache Iceberg, and Apache Hudi.

## Quick Comparison

| Feature | Delta Lake | Apache Iceberg | Apache Hudi |
|---------|-----------|----------------|-------------|
| **ACID Transactions** | ✅ | ✅ | ✅ |
| **Time Travel** | ✅ | ✅ | ✅ |
| **Schema Evolution** | ✅ | Advanced (branching) | ✅ |
| **Primary Ecosystem** | Spark/Databricks | Engine-agnostic | Spark (CDC focus) |
| **Write Optimization** | Copy-on-write | CoW, Merge-on-Read | CoW, Merge-on-Read |
| **Python API** | `deltalake` (pure), PySpark | `pyiceberg` (pure) | PySpark only |
| **Best For** | Spark ecosystems, Databricks | Multi-engine analytics | Change data capture, streaming |

## When to Use Which?

- **Delta Lake**: You're in the Spark/Databricks ecosystem, need mature tooling with pure-Python `deltalake` library
- **Apache Iceberg**: You need engine-agnostic tables (Spark, Trino, Flink, DuckDB), advanced schema branching
- **Apache Hudi**: You're building CDC pipelines from Kafka/DB logs, need upsert/delete support

## Interoperability

Apache XTable and Delta UniForm (2024+) enable cross-format reads without conversion. Platforms like Databricks Unity Catalog and Snowflake support multiple formats natively, reducing vendor lock-in.

## Related Skills

- `@data-engineering-storage-remote-access/integrations/delta-lake` - Delta Lake on S3/GCS/Azure
- `@data-engineering-storage-remote-access/integrations/iceberg` - Iceberg with cloud catalogs
- `@data-engineering-orchestration/dbt` - dbt adapters for Delta/Iceberg
- `@data-engineering-storage-remote-access` - fsspec, PyArrow filesystem for cloud access

## Skill Dependencies

This skill assumes familiarity with:
- `@data-engineering-core` - Polars, DuckDB, PyArrow basics
- `@data-engineering-storage-remote-access` - Cloud storage access patterns

---

## Detailed Guides

### Delta Lake
See: `@data-engineering-storage-lakehouse/delta-lake.md`

- Pure-Python API (`deltalake` package)
- PySpark integration
- Time travel (version AsOf, timestamp AsOf)
- Schema evolution (add/drop/rename/upcast)
- Vacuum and optimize
- S3/GCS/Azure storage integration

### Apache Iceberg
See: `@data-engineering-storage-lakehouse/iceberg.md`

- PyIceberg catalog abstraction (Hive, AWS Glue, REST)
- Schema evolution with branch support
- Partition evolution
- Time travel and versioning
- Local catalog for development

### Apache Hudi
See: `@data-engineering-storage-lakehouse/hudi.md`

- Copy-on-write and Merge-on-Read modes
- CDC integration (Debezium, Kafka)
- Hoodie tables, indexes, bloom filters
- Querying via Spark

---

## Common Patterns

### Time Travel Queries
```python
# Delta Lake
from deltalake import DeltaTable
dt = DeltaTable("s3://bucket/delta-table")
dt.load_version(5)  # Load specific version
df = dt.to_pandas()

# Iceberg
table = catalog.load_table("db.table")
df = table.scan(as_of_timestamp="2024-01-01T00:00:00Z").to_pandas()
```

### Schema Evolution
```python
# Delta Lake (auto-evolves on write by default)
dt = DeltaTable("s3://bucket/delta-table")
# When writing with new column, Delta adds it automatically

# Iceberg (explicit)
with table.update_schema() as update:
    update.add_column("new_field", StringType(), required=False)
```

### Incremental Processing
```python
# Read only changes since last checkpoint
delta_table = DeltaTable("s3://bucket/delta-table")
last_version = get_last_processed_version()

# Get changes as Arrow table
changes = (
    delta_table
    .history()  # Get commit history
    .filter(f"version > {last_version}")
    .to_pyarrow_table()
)
```

---

## Best Practices

1. **Use Partitions**: Partition by date/region to enable predicate pushdown
2. **Vacuum Regularly**: Clean up old files to avoid storage bloat (Delta: `vacuum()`, Iceberg: `expire_snapshots()`)
3. **Optimize Layouts**: Compaction for small files (Delta: `OPTIMIZE`, Iceberg: `rewrite_data_files()`)
4. **Catalog Choice**: Use AWS Glue for AWS, Hive Metastore for on-prem, REST for SaaS
5. **Transaction Size**: Batch writes for throughput but avoid too-large transactions
6. **Monitor Table Metadata**: Table metadata grows with operations; archive old versions

---

## References

- [Delta Lake Documentation](https://docs.delta.io/latest/index.html)
- [Apache Iceberg Documentation](https://iceberg.apache.org/docs/)
- [Apache Hudi Documentation](https://hudi.apache.org/docs/)
- [deltalake Python package](https://delta-io.github.io/delta-rs/python/quickstart.html)
- [PyIceberg Documentation](https://pyiceberg.readthedocs.io/)
