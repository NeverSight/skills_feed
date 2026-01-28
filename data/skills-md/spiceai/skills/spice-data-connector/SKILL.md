---
name: spice-data-connector
description: Connect Spice to data sources like PostgreSQL, MySQL, S3, Databricks, Snowflake, and more. Use when asked to "add a dataset", "connect to a database", "load data from S3", or "configure a data source".
---

# Spice Data Connectors

Data Connectors enable federated SQL queries across databases, data warehouses, data lakes, and files.

## Basic Dataset Configuration

```yaml
datasets:
  - from: <connector>:<identifier>
    name: <dataset_name>
    params:
      # connector-specific parameters
    acceleration:
      enabled: true          # optional: enable local caching
      engine: duckdb         # arrow, duckdb, sqlite, postgres
```

## Supported Connectors

| Connector     | From Format                          | Status  |
|---------------|--------------------------------------|---------|
| PostgreSQL    | `postgres:schema.table`              | Stable  |
| MySQL         | `mysql:schema.table`                 | Stable  |
| S3            | `s3://bucket/path/`                  | Stable  |
| DuckDB        | `duckdb:database.table`              | Stable  |
| Databricks    | `databricks:catalog.schema.table`    | Stable  |
| Snowflake     | `snowflake:database.schema.table`    | Beta    |
| File          | `file:./path/to/file.parquet`        | Stable  |
| Delta Lake    | `delta_lake:/path/to/delta/`         | Stable  |
| MongoDB       | `mongodb:collection`                 | Alpha   |
| Clickhouse    | `clickhouse:database.table`          | Alpha   |

## Documentation

- [Data Connectors Overview](https://spiceai.org/docs/components/data-connectors)
- [Data Accelerators](https://spiceai.org/docs/components/data-accelerators)