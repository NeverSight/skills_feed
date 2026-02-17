---
name: polars
description: Use when "Polars", "fast dataframe", "lazy evaluation", "Arrow backend", or asking about "pandas alternative", "parallel dataframe", "large CSV processing", "ETL pipeline", "expression API"
version: 1.0.0
---

# Polars Fast DataFrame Library

Lightning-fast DataFrame library with lazy evaluation and parallel execution.

## When to Use

- Pandas is too slow for your dataset
- Working with 1-100GB datasets that fit in RAM
- Need lazy evaluation for query optimization
- Building ETL pipelines
- Want parallel execution without extra config

---

## Lazy vs Eager Evaluation

| Mode | Function | Executes | Use Case |
|------|----------|----------|----------|
| **Eager** | `read_csv()` | Immediately | Small data, exploration |
| **Lazy** | `scan_csv()` | On `.collect()` | Large data, pipelines |

**Key concept**: Lazy mode builds a query plan that gets optimized before execution. The optimizer applies predicate pushdown (filter early) and projection pushdown (select columns early).

---

## Core Operations

### Data Selection

| Operation | Purpose |
|-----------|---------|
| `select()` | Choose columns |
| `filter()` | Choose rows by condition |
| `with_columns()` | Add/modify columns |
| `drop()` | Remove columns |
| `head(n)` / `tail(n)` | First/last n rows |

### Aggregation

| Operation | Purpose |
|-----------|---------|
| `group_by().agg()` | Group and aggregate |
| `pivot()` | Reshape wide |
| `melt()` | Reshape long |
| `unique()` | Distinct values |

### Joins

| Join Type | Description |
|-----------|-------------|
| **inner** | Matching rows only |
| **left** | All left + matching right |
| **outer** | All rows from both |
| **cross** | Cartesian product |
| **semi** | Left rows with match |
| **anti** | Left rows without match |

---

## Expression API

**Key concept**: Polars uses expressions (`pl.col()`) instead of indexing. Expressions are lazily evaluated and optimized.

### Common Expressions

| Expression | Purpose |
|------------|---------|
| `pl.col("name")` | Reference column |
| `pl.lit(value)` | Literal value |
| `pl.all()` | All columns |
| `pl.exclude(...)` | All except |

### Expression Methods

| Category | Methods |
|----------|---------|
| **Aggregation** | `.sum()`, `.mean()`, `.min()`, `.max()`, `.count()` |
| **String** | `.str.contains()`, `.str.replace()`, `.str.to_lowercase()` |
| **DateTime** | `.dt.year()`, `.dt.month()`, `.dt.day()` |
| **Conditional** | `.when().then().otherwise()` |
| **Window** | `.over()`, `.rolling_mean()`, `.shift()` |

---

## Pandas Migration

| Pandas | Polars |
|--------|--------|
| `df['col']` | `df.select('col')` |
| `df[df['col'] > 5]` | `df.filter(pl.col('col') > 5)` |
| `df['new'] = df['col'] * 2` | `df.with_columns((pl.col('col') * 2).alias('new'))` |
| `df.groupby('col').mean()` | `df.group_by('col').agg(pl.all().mean())` |
| `df.apply(func)` | `df.map_rows(func)` (avoid if possible) |

**Key concept**: Polars prefers explicit operations over implicit indexing. Use `.alias()` to name computed columns.

---

## File I/O

| Format | Read | Write | Notes |
|--------|------|-------|-------|
| **CSV** | `read_csv()` / `scan_csv()` | `write_csv()` | Human readable |
| **Parquet** | `read_parquet()` / `scan_parquet()` | `write_parquet()` | Fast, compressed |
| **JSON** | `read_json()` / `scan_ndjson()` | `write_json()` | Newline-delimited |
| **IPC/Arrow** | `read_ipc()` / `scan_ipc()` | `write_ipc()` | Zero-copy |

**Key concept**: Use Parquet for performance. Use `scan_*` for large files to enable lazy optimization.

---

## Performance Tips

| Tip | Why |
|-----|-----|
| Use lazy mode | Query optimization |
| Use Parquet | Column-oriented, compressed |
| Select columns early | Projection pushdown |
| Filter early | Predicate pushdown |
| Avoid Python UDFs | Breaks parallelism |
| Use expressions | Vectorized operations |
| Set dtypes on read | Avoid inference overhead |

---

## vs Alternatives

| Tool | Best For | Limitations |
|------|----------|-------------|
| **Polars** | 1-100GB, speed critical | Must fit in RAM |
| **Pandas** | Small data, ecosystem | Slow, memory hungry |
| **Dask** | Larger than RAM | More complex API |
| **Spark** | Cluster computing | Infrastructure overhead |
| **DuckDB** | SQL interface | Different API style |

## Resources

- Docs: <https://pola.rs/>
- User Guide: <https://docs.pola.rs/user-guide/>
- Cookbook: <https://docs.pola.rs/user-guide/misc/cookbook/>
