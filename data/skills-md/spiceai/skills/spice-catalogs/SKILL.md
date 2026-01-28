---
name: spice-catalogs
description: Configure catalog connectors in Spice (Unity Catalog, Databricks, Iceberg, Glue). Use when asked to "add a catalog", "connect to Unity Catalog", "configure Iceberg catalog", or "set up data catalog".
---

# Spice Catalog Connectors

Catalog connectors expose external data catalogs for federated SQL queries, preserving the source schema hierarchy.

## Basic Configuration

```yaml
catalogs:
  - from: <connector>
    name: <catalog_name>
    params:
      # connector-specific parameters
    include:
      - 'schema.*'     # optional: filter tables
```

## Supported Catalogs

| Connector       | From Format      | Description                    |
|-----------------|------------------|--------------------------------|
| `unity_catalog` | `unity_catalog`  | Databricks Unity Catalog       |
| `databricks`    | `databricks`     | Databricks with Spark Connect  |
| `iceberg`       | `iceberg`        | Apache Iceberg catalogs        |
| `spice.ai`      | `spice.ai`       | Spice.ai Cloud Platform        |
| `glue`          | `glue`           | AWS Glue Data Catalog          |

## Examples

### Unity Catalog
```yaml
catalogs:
  - from: unity_catalog
    name: unity
    params:
      unity_catalog_endpoint: https://my-workspace.cloud.databricks.com
      databricks_token: ${ secrets:DATABRICKS_TOKEN }
    include:
      - 'my_schema.*'
```

### Iceberg with S3
```yaml
catalogs:
  - from: iceberg
    name: iceberg_catalog
    params:
      iceberg_catalog_type: rest
      iceberg_rest_uri: https://my-iceberg-catalog.com
```

### Spice.ai Platform
```yaml
catalogs:
  - from: spice.ai
    name: spiceai
    include:
      - 'tpch.*'
```

## Querying Catalog Tables

Tables are accessed using the full path: `<catalog>.<schema>.<table>`

```sql
SELECT * FROM unity.my_schema.customers LIMIT 10;
```

## Include Patterns

Filter which tables to expose using glob patterns:

```yaml
include:
  - 'prod_schema.*'           # all tables in prod_schema
  - '*.customers'             # customers table in any schema
  - 'analytics.sales_*'       # tables starting with sales_ in analytics
```

## Documentation

- [Catalog Connectors Overview](https://spiceai.org/docs/components/catalogs)
- [Catalogs Reference](https://spiceai.org/docs/reference/spicepod/catalogs)
