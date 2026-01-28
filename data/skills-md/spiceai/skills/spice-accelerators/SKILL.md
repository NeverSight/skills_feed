---
name: spice-accelerators
description: Configure data accelerators for local caching in Spice (Arrow, DuckDB, SQLite, PostgreSQL). Use when asked to "accelerate data", "enable caching", "configure refresh", or "set up local storage".
---

# Spice Data Accelerators

Data accelerators cache data locally for faster queries and reduced load on source systems.

## Basic Configuration

```yaml
datasets:
  - from: postgres:my_table
    name: my_table
    acceleration:
      enabled: true
      engine: duckdb           # arrow, duckdb, sqlite, postgres, cayenne
      mode: memory             # memory or file
      refresh_check_interval: 1h
```

## Supported Engines

| Engine    | Mode           | Best For                              |
|-----------|----------------|---------------------------------------|
| `arrow`   | `memory`       | Small datasets, fastest queries       |
| `duckdb`  | `memory/file`  | Complex SQL, medium datasets          |
| `sqlite`  | `memory/file`  | Simple queries, low overhead          |
| `cayenne` | `file`         | Large datasets (100GB+), analytics    |
| `postgres`| N/A            | External PostgreSQL integration       |

## Refresh Modes

| Mode      | Description                                    |
|-----------|------------------------------------------------|
| `full`    | Replace entire dataset on each refresh         |
| `append`  | Add new records based on `time_column`         |
| `changes` | CDC-based incremental updates                  |

## Common Configurations

### Memory Cache with Interval Refresh
```yaml
acceleration:
  enabled: true
  engine: arrow
  refresh_check_interval: 5m
```

### File-Based with Time Window
```yaml
acceleration:
  enabled: true
  engine: duckdb
  mode: file
  refresh_mode: append
  refresh_check_interval: 1h
  refresh_data_window: 7d
```

### With Retention Policy
```yaml
datasets:
  - from: postgres:events
    name: events
    time_column: created_at
    acceleration:
      enabled: true
      engine: duckdb
      retention_check_enabled: true
      retention_period: 30d
      retention_check_interval: 1h
```

### With Indexes
```yaml
acceleration:
  enabled: true
  engine: sqlite
  indexes:
    user_id: enabled
    '(created_at, status)': unique
  primary_key: id
```

## Engine-Specific Parameters

### DuckDB
```yaml
acceleration:
  engine: duckdb
  mode: file
  params:
    duckdb_file: ./data/cache.db
```

### SQLite
```yaml
acceleration:
  engine: sqlite
  mode: file
  params:
    sqlite_file: ./data/cache.sqlite
```

## Documentation

- [Data Accelerators Overview](https://spiceai.org/docs/components/data-accelerators)
- [Datasets Reference](https://spiceai.org/docs/reference/spicepod/datasets)
- [Data Refresh](https://spiceai.org/docs/features/data-acceleration/data-refresh)
- [Indexes](https://spiceai.org/docs/features/data-acceleration/indexes)
