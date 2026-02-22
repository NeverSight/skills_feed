---
name: flowerpower
description: "Create and manage data pipelines using the FlowerPower framework with Hamilton DAGs and uv. Lightweight orchestration for batch ETL, data transformation, and ML pipelines. Integrates with Delta Lake, DuckDB, Polars, and cloud storage."
dependsOn: ["@data-engineering-core", "@data-engineering-storage-lakehouse", "@data-engineering-storage-remote-access", "@data-engineering-quality", "@data-engineering-best-practices"]
---

# FlowerPower Pipeline Framework

🌸 Build configuration-driven data pipelines using Hamilton DAGs. Lightweight, modular, and perfect for batch ETL, data transformation, and ML workflows.

**FlowerPower** is ideal for:
- Simple to medium complexity data pipelines (not full production orchestration)
- Teams wanting code-first DAG definitions (vs. YAML-heavy Airflow)
- Projects needing configurable parameters and multiple executors
- Rapid prototyping and batch processing

**For production orchestration** with scheduling, state persistence, and reliability features, see `@data-engineering-orchestration` (Prefect, Dagster, dbt).

---

## Skill Dependencies

This skill assumes familiarity with:
- **`@data-engineering-core`** - Polars, DuckDB, PyArrow basics
- **`@data-engineering-storage-lakehouse`** - Delta Lake, Iceberg table formats
- **`@data-engineering-storage-remote-access`** - Cloud storage (S3, GCS) and fsspec
- **`@data-engineering-quality`** - Data validation with Pandera, Great Expectations
- **`@data-engineering-best-practices`** - Medallion architecture, partitioning, incremental loads

---

## When to Use FlowerPower vs. Prefect/Dagster

| Scenario | Recommended Tool | Why |
|----------|------------------|-----|
| Simple batch ETL, data transformation scripts | **FlowerPower** | Lightweight, no infrastructure, Hamilton DAG elegance |
| Production workflows with scheduling, retries, SLA | **Prefect** | Orchestrator with cloud, robust error handling |
| Asset-based pipelines, data observability | **Dagster** | Asset lineage, materialization, sensors |
| SQL transformations, dbt ecosystem | **dbt** | SQL-first, built-in testing, documentation |
| Complex dependency graphs, multi-team | **Airflow** | Mature, scalable, operator ecosystem |

**FlowerPower limitations:**
- No built-in scheduler (use cron/systemd)
- No state persistence across restarts
- Limited observability (Hamilton UI is basic)
- Not designed for long-running, fault-tolerant production workflows

---

## Quick Start

```bash
# Install
uv pip install flowerpower[io,ui]

# Initialize project
flowerpower init --name my-pipeline-project

# Create pipeline
flowerpower pipeline new bronze_ingestion

# Run
flowerpower pipeline run bronze_ingestion
```

---

## Advanced Patterns

### Medallion Architecture with FlowerPower

Create three pipelines following bronze-silver-gold pattern:

**bronze_ingest.py** (raw ingestion, append-only)
```python
from hamilton.function_modifiers import parameterize
import polars as pl
from flowerpower.cfg import Config

PARAMS = Config.load(Path(__file__).parents[1], "bronze_ingest").pipeline.h_params

@parameterize(**PARAMS.source)
def source_uri(uri: str) -> str:
    """Source data location (S3, local, etc.)."""
    return uri

def bronze_table(source_uri: str) -> pl.LazyFrame:
    """Read raw data as-is, add ingestion metadata."""
    df = pl.scan_parquet(source_uri)
    return df.with_columns([
        pl.lit(pl.datetime.now()).alias("_ingestion_timestamp"),
        pl.lit(source_uri).alias("_source_file")
    ])

def write_bronze(bronze_table: pl.LazyFrame, output_path: str) -> str:
    """Write to Delta Lake bronze layer (partitioned by date)."""
    bronze_table.write_delta(
        output_path,
        mode="append",
        partition_by=["_ingestion_date"]
    )
    return f"Wrote {bronze_table.count()} rows to {output_path}"
```

**silver_clean.py** (validation, standardization)
```python
def validate_schema(bronze_table: pl.LazyFrame) -> pl.LazyFrame:
    """Apply schema checks using Pandera."""
    import pandera as pa
    from pandera.polars import DataFrameSchema, Column

    schema = DataFrameSchema({
        "order_id": Column(pl.Int64, nullable=False, unique=True),
        "customer_id": Column(pl.Int32, nullable=False),
        "amount": Column(pl.Float64, pa.Check.ge(0)),
        "_ingestion_timestamp": Column(pl.Datetime)
    })

    # Validate (raises if invalid)
    validated_df = schema.validate(bronze_table.collect())
    return validated_df.lazy()

def standardize_data(validated: pl.LazyFrame) -> pl.LazyFrame:
    """Standardize dates, currencies, etc."""
    return validated.with_columns([
        pl.col("order_date").str.strptime(pl.Date, fmt="%Y-%m-%d"),
        pl.col("amount").round(2)
    ])

def write_silver(standardize_data: pl.LazyFrame, silver_path: str) -> str:
    """Write to Silver Delta table, overwrite partition."""
    standardize_data.write_delta(
        silver_path,
        mode="overwrite",
        partition_filters=[("ingestion_date", "=", "2024-01-01")]
    )
```

**gold_aggregate.py** (business-ready aggregates)
```python
def daily_sales(silver_table: pl.LazyFrame) -> pl.DataFrame:
    """Aggregate sales by day, region."""
    return silver_table.group_by(["order_date", "region"]).agg([
        pl.sum("amount").alias("total_sales"),
        pl.count().alias("order_count")
    ]).collect()

def write_gold(daily_sales: pl.DataFrame, gold_path: str) -> str:
    """Write Gold table (Parquet, no ACID needed)."""
    daily_sales.write_parquet(
        gold_path,
        compression="zstd",
        stat_getters=["min", "max"]  # For predicate pushdown
    )
```

---

### Delta Lake Integration with Schema Evolution

Use `delta_scan()` and `write_delta()` with merge schema:

```yaml
# conf/pipelines/delta_incremental.yml
params:
  delta_table: "s3://lakehouse/silver/orders/"
  source_parquet: "s3://raw/orders/"

run:
  final_vars:
    - write_result
  executor:
    type: threadpool
    max_workers: 4
```

```python
# pipelines/delta_incremental.py
def source_data(source_parquet: str) -> pl.LazyFrame:
    return pl.scan_parquet(source_parquet)

def merge_delta(source_data: pl.LazyFrame, delta_table: str) -> str:
    """Append with schema evolution."""
    source_data.write_delta(
        delta_table,
        mode="append",
        delta_write_options={"schema_mode": "merge"}  # Auto-add new columns
    )
    return f"Appended {len(source_data.collect())} rows"
```

---

### Watermark/Incremental Load Pattern

```python
# Use DuckDB to manage watermarks
def get_last_watermark(con, table_name: str) -> datetime:
    """Query watermark table."""
    result = con.execute(f"""
        SELECT watermark_value
        FROM watermark_table
        WHERE table_name = '{table_name}'
    """).fetchone()
    return result[0] if result else datetime(1970,1,1)

def incremental_load(source: str, target: str, timestamp_col: str = "updated_at"):
    """Load only new/updated records."""
    import duckdb
    con = duckdb.connect(":memory:")

    old_wm = get_last_watermark(con, target)
    new_wm = pl.scan_parquet(source).select(pl.max(timestamp_col)).collect()[0,0]

    df = pl.scan_parquet(source).filter(
        (pl.col(timestamp_col) > old_wm) &
        (pl.col(timestamp_col) <= new_wm)
    )

    df.write_delta(target, mode="append")

    # Update watermark
    con.execute("""
        INSERT OR REPLACE INTO watermark_table (table_name, watermark_value)
        VALUES (?, ?)
    """, [target, new_wm])
```

---

### Data Quality Validation (Pandera)

```python
import pandera as pa
from pandera.polars import DataFrameSchema, Column

def validate_silver(silver_df: pl.DataFrame) -> pl.DataFrame:
    """Validate against Pandera schema."""
    schema = DataFrameSchema({
        "customer_id": Column(pl.Int32, pa.Check.gt(0)),
        "email": Column(pl.Utf8, pa.Check.str_contains("@")),
        "signup_date": Column(pl.Date, pa.Check(lambda s: s >= "2020-01-01"))
    })

    try:
        validated = schema.validate(silver_df, lazy=True)
        return validated
    except pa.errors.SchemaErrors as e:
        # Log failures, write to quarantine
        print(f"Validation failed: {e.failure_cases}")
        raise
```

---

### Cloud Storage (S3) with fsspec

```yaml
# conf/pipelines/s3_ingest.yml
params:
  s3_path: "s3://my-bucket/raw/orders/"
  local_cache: "/tmp/cache"

run:
  executor:
    type: threadpool
    max_workers: 8
```

```python
# pipelines/s3_ingest.py
def list_s3_files(s3_path: str) -> list[str]:
    """List files to process."""
    import fsspec
    fs = fsspec.filesystem('s3')
    return fs.glob(f"{s3_path}*.parquet")

def read_s3_file(file_path: str) -> pl.LazyFrame:
    """Read individual file with fsspec."""
    import fsspec
    fs = fsspec.filesystem('s3')
    with fs.open(file_path, 'rb') as f:
        return pl.read_parquet(f)

def process_files(list_s3_files: list[str]) -> pl.LazyFrame:
    """Process all files and union."""
    frames = [read_s3_file(f) for f in list_s3_files]
    return pl.concat(frames)
```

---

## Best Practices for FlowerPower

1. **Use lazy evaluation** (Polars LazyFrame) for large datasets
2. **Set appropriate executor**: threadpool for I/O, processpool for CPU
3. **Add retries** in config for external API calls
4. **Use configuration** for all parameters (no hardcoded paths)
5. **Log strategically** - Hamilton captures node outputs
6. **Implement idempotency** - pipelines should be re-runnable
7. **Monitor with Hamilton UI** for DAG visualization
8. **Use partitioning** for Delta Lake tables (by date/tenant)
9. **Validate at Silver layer** with Pandera/Great Expectations
10. **Handle schema evolution** with `schema_mode="merge"` for appends

---

## Limitations & Gotchas

- **No built-in scheduling** - pair with cron/systemd/Prefect
- **No state persistence** - track watermarks externally (DuckDB)
- **No SLA alerts** - implement custom `on_failure` hooks
- **Hamilton cache** can grow indefinitely - configure `cache: false` or prune
- **Multi-node execution** requires Ray/Dask setup (advanced)

---

## See Also

- **`@data-engineering-best-practices`** - Medallion architecture, incremental loads, partitioning, file sizing
- **`@data-engineering-storage-lakehouse`** - Delta Lake, Iceberg table formats and operations
- **`@data-engineering-storage-remote-access`** - Cloud storage backends (S3, GCS) and libraries
- **`@data-engineering-quality`** - Data validation frameworks (Pandera, Great Expectations)
- **`@data-engineering-catalogs`** - Data catalog systems for discovery and governance
- **`@data-engineering-orchestration`** - Production orchestration (Prefect, Dagster, dbt) when you need more than FlowerPower

---

## References

- [FlowerPower Documentation](https://legout.github.io/flowerpower/)
- [Hamilton Framework](https://hamilton.apache.org/)
- [FlowerPower GitHub](https://github.com/legout/flowerpower)
- `@data-engineering-orchestration` - Comparison of orchestration tools
