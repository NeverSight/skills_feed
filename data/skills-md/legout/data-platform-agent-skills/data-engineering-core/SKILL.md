---
name: data-engineering-core
description: "Core Python data engineering: Polars, DuckDB, PyArrow, PostgreSQL, ETL patterns, performance tuning, and resilient pipeline construction. Use when building or reviewing batch ETL/dataframe/SQL pipelines in Python."
---

# Core Data Engineering

Use this skill for day-to-day Python data engineering decisions: dataframe processing, embedded OLAP SQL, Arrow interchange, ETL structure, and resilience patterns.

## When to use this skill

Use this skill when the task involves one or more of:
- Polars transformations and lazy query optimization
- DuckDB SQL analytics, MERGE/upsert, or Parquet querying
- PyArrow table/dataset interchange and Parquet scans
- Python ETL pipeline structure (extract/transform/load, logging, retries, idempotency)
- PostgreSQL-to-lake/warehouse ingestion patterns

If the task is primarily about cloud storage auth/connectors, use:
- `@data-engineering-storage-remote-access`
- `@data-engineering-storage-authentication`

If the task is primarily about ACID lakehouse table behavior, use:
- `@data-engineering-storage-lakehouse`

---

## Quick tool selection

| Need | Default choice | Why |
|---|---|---|
| DataFrame transformation in Python | **Polars** | Fast lazy engine, strong expression API |
| SQL over files/DataFrames | **DuckDB** | Embedded OLAP + Parquet/Arrow native |
| Interchange format between systems | **PyArrow** | Zero-copy table/batch ecosystem |
| OLTP source extraction | **psycopg2 / postgres driver** | Stable DB connectivity |

Rule of thumb:
1. Start transformations in **Polars lazy**.
2. Use **DuckDB** for heavy SQL/windowing/joins over files.
3. Keep boundaries in **Arrow/Parquet**.

---

## Core implementation rules

### 1) Prefer lazy execution

- Use `pl.scan_*` over `pl.read_*` for large inputs.
- Chain filters/projections before `collect()`.
- Avoid row-wise loops.

### 2) Push work down

- Push filtering into file scans (predicate pushdown).
- Select only needed columns (column pruning).
- Partition data by query dimensions (typically date/tenant/region).

### 3) Keep writes idempotent

- Prefer MERGE/upsert semantics where possible.
- If append-only, track watermark/checkpoints.
- Ensure retries do not duplicate side effects.

### 4) Protect boundaries

- Use parameterized SQL for values.
- Treat dynamic identifiers (table/column names) separately and validate.
- Never hardcode secrets.

### 5) Instrument and validate

- Log row counts and stage durations.
- Validate schema/required columns at stage boundaries.
- Record checkpoints/watermarks for incremental flows.

---

## Minimal safe ETL shape

```python
import polars as pl
import duckdb


def run_etl(source_path: str, target_table: str) -> None:
    lazy = (
        pl.scan_parquet(source_path)
        .filter(pl.col("value").is_not_null())
        .select(["id", "event_ts", "value", "category"])
    )

    df = lazy.collect()

    with duckdb.connect("analytics.db") as con:
        con.sql("CREATE OR REPLACE TABLE staging AS SELECT * FROM df")
        con.sql(f"""
            CREATE TABLE IF NOT EXISTS {target_table} AS
            SELECT * FROM staging WHERE 1=0
        """)
        con.sql(f"INSERT INTO {target_table} SELECT * FROM staging")
```

For production-grade structure, use:
- `templates/complete_etl_pipeline.py`

---

## Progressive disclosure (read next as needed)

- `patterns/etl.md` — canonical ETL pipeline structure
- `patterns/incremental.md` — watermark/CDC/incremental loading patterns
- `templates/complete_etl_pipeline.py` — full template with logging and checkpoints
- `core-detailed.md` — comprehensive reference (extended examples)

---

## Related skills

- `@data-engineering-storage-lakehouse` — Delta/Iceberg/Hudi behavior
- `@data-engineering-storage-remote-access` — fsspec/pyarrow.fs/obstore cloud access
- `@data-engineering-orchestration` — Prefect/Dagster/dbt orchestration
- `@data-engineering-quality` — Pandera / Great Expectations validation
- `@data-engineering-observability` — OTel + Prometheus monitoring
- `@data-engineering-ai-ml` — embedding/vector/RAG pipelines

---

## References

- [Polars Documentation](https://pola.rs/)
- [DuckDB Documentation](https://duckdb.org/docs/)
- [PyArrow Documentation](https://arrow.apache.org/docs/python/)
- [psycopg Documentation](https://www.psycopg.org/docs/)
