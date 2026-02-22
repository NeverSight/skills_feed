---
name: data-engineering-catalogs
description: "Data catalogs: Iceberg catalogs (Hive Metastore, AWS Glue, Tabular), using DuckDB as a lightweight multi-source catalog, comparisons of Amundsen/DataHub/OpenMetadata, and patterns for unified data access."
dependsOn: ["@data-engineering-storage-lakehouse", "@data-engineering-storage-remote-access", "@data-engineering-storage-authentication"]
---

# Data Catalogs

Comprehensive guide to data catalog systems: purpose, Iceberg catalog implementations (Hive Metastore, AWS Glue, Tabular), using DuckDB as a lightweight multi-source catalog, and comparisons of open-source catalog tools (Amundsen, DataHub, OpenMetadata). Learn selection criteria, setup patterns, and best practices for data discovery, governance, and unified querying.

---

## Why Catalogs Matter

Data catalogs are **centralized metadata repositories** that enable:

- **Data discovery**: Find datasets by name, schema, owner, tags
- **Governance**: Access control, data lineage, PII tagging
- **Schema management**: Track table schemas, partitions, evolution over time
- **Table format abstraction**: Iceberg/Delta/Hudi tables registered in catalog can be queried by multiple engines (Spark, Trino, Flink, DuckDB) without knowing underlying storage URIs
- **Multi-engine consistency**: Same table name across Spark/DuckDB/Trino

**Without a catalog**, you must manage table locations and schemas manually in each engine.

---

## Iceberg Catalogs

Apache Iceberg requires a catalog to store table metadata (schema, location, snapshots, partition specs). **The catalog name** → **table identifier** → **storage location** mapping.

### Catalog Types

| Catalog | Backend | Managed? | Best For |
|---------|---------|----------|----------|
| **Hive Metastore** | RDBMS (Postgres/MySQL) | Self-operated | Existing Hadoop installations, high partition counts |
| **AWS Glue** | AWS-managed (serverless) | AWS-managed | AWS-native stacks, Athena/EMR |
| **Tabular** | SaaS (Nessie-backed) | Tabular-managed | Iceberg-native, Git-like branching |
| **Custom REST** | Any HTTP service | Self-built | Custom auth, multi-cloud |

---

### Hive Metastore

**The traditional, battle-tested catalog** used by Hadoop/Hive for over a decade. Stores table metadata in a relational database.

**Setup:**
```bash
# Install Hive Metastore (Docker quickstart)
docker run -p 9083:9083 -e METASTORE_DB_TYPE=postgresql \
  -e METASTORE_DB_URL=jdbc:postgresql://localhost/metastore \
  apache/hive:4.0

# Initialize metastore schema (run once)
schematool -dbType postgresql -initSchema
```

**PyIceberg configuration:**
```python
from pyiceberg.catalog import Catalog
from pyiceberg.catalog.hive import HiveCatalog

catalog = HiveCatalog(
    name="my_hive",
    uri="thrift://localhost:9083",
    warehouse="s3://my-bucket/warehouse/",
    properties={
        "postgresql.connection": "jdbc:postgresql://localhost/metastore",
        "postgresql.user": "hive",
        "postgresql.password": "hive"
    }
)

# Create table
catalog.create_table(
    identifier=("my_db", "my_table"),
    schema=table_schema,
    location="s3://my-bucket/my_table/"
)
```

**Pros:**
- Mature, battle-tested (10+ years)
- Handles 500k+ partitions with proper DB tuning
- Works with any Hadoop ecosystem (Spark, Presto, Hive, Flink)
- No vendor lock-in

**Cons:**
- Self-managed (DB ops, backups, HA)
- Limited Iceberg-specific features (no branching/namespace)
- Thrift protocol (legacy)

---

### AWS Glue Data Catalog

**Fully managed catalog** by AWS, serverless, Hive-compatible API.

**Setup:**
```python
from pyiceberg.catalog.glue import GlueCatalog

catalog = GlueCatalog(
    name="my_glue",
    region="us-east-1",
    warehouse="s3://my-bucket/warehouse/"
)

# Tables automatically appear in AWS Glue console
```

**Unity Catalog Federation** (Databricks):
```python
# Databricks can read AWS Glue tables via federation
catalog = GlueCatalog(
    name="aws_glue_fed",
    region="us-east-1"
)
# Spark on Databricks queries glue catalog
```

**Pros:**
- Serverless, no operations
- Integrated with Athena, EMR, Redshift Spectrum
- Fine-grained IAM permissions via Lake Formation
- Works with Delta Lake, Iceberg, Hudi

**Cons:**
- Performance degrades >10k partitions (known issue)
- Limited metadata operations (slow operations)
- AWS lock-in

---

### Tabular (Iceberg-Native SaaS)

**Tabular** is a managed catalog service built for Iceberg with **Nessie-like versioning** (branching, tags, time travel on metadata).

```python
from pyiceberg.catalog.tabular import TabularCatalog

catalog = TabularCatalog(
    name="tabular",
    warehouse="s3://my-bucket/warehouse/",
    token="tabular-token-..."
)

# Git-like operations
catalog.create_table("my_table", schema)
catalog.create_branch("dev")  # Branch for development
catalog.set_current_branch("dev")
# Later merge to main
```

**Pros:**
- Native Iceberg features (branching, tags, atomic multi-table ops)
- No ops overhead
- Git-like workflow for datasets

**Cons:**
- Commercial SaaS (cost)
- Newer ecosystem

---

## Using DuckDB as a Multi-Source Catalog

**DuckDB does NOT provide a production data catalog service** (no REST API, limited concurrency). However, you can use it as a **lightweight embedded catalog** to unify queries across multiple heterogeneous sources using the `ATTACH` statement. This pattern is suitable for:

- **Single-user analytics notebooks**
- **PoC/mVP data platforms**
- **Local dev environments**
- **Small teams** (< 10 users)

### Architecture

```
DuckDB Process
    ├── ATTACH 'postgres://...' AS postgres
    ├── ATTACH 's3://lakehouse/delta/' AS delta_uc (TYPE unity_catalog)
    ├── ATTACH 's3://lakehouse/iceberg/' AS iceberg
    ├── ATTACH 'ducklake:data/catalog.ducklake' AS ducklake
    └── CREATE VIEW unified_dataset AS
          SELECT 'postgres' AS source, * FROM postgres.public.orders
          UNION ALL
          SELECT 'delta' AS source, * FROM delta.default.orders
          UNION ALL
          SELECT 'iceberg' AS source, * FROM iceberg.db.orders
```

### Attaching PostgreSQL

Use Postgres as a **metadata storage backend** (DuckLake) or query external Postgres tables:

```sql
-- Attach external Postgres database
ATTACH 'postgres://user:pass@host:5432/mydb' AS pg_db;

-- Query Postgres tables
SELECT * FROM pg_db.public.orders LIMIT 10;
```

**DuckLake pattern:** Attach a Postgres database as a DuckLake catalog:

```sql
-- Install and load DuckLake extension
INSTALL ducklake;
LOAD ducklake;

-- Attach Postgres as DuckLake catalog
ATTACH 'postgres://user:pass@host:5432/lakehouse_catalog' AS my_lakehouse (
    DATA_PATH 's3://my-bucket/lakehouse/'
);

-- Create Delta/Iceberg tables managed by DuckLake
CREATE TABLE my_lakehouse.silver.orders (
    order_id BIGINT,
    amount DOUBLE,
    order_date DATE
) USING DELTA;  -- Or USING ICEBERG
```

**Benefits:** Single SQL catalog with ACID transactions, time travel via Postgres WAL.

---

### Attaching Delta Lake (Unity Catalog)

Use the Unity Catalog extension (experimental, works without Databricks):

```sql
INSTALL unity_catalog;
LOAD unity_catalog;

-- Create a Unity Catalog connection
CREATE SECRET uc_cred (
    TYPE 'aws',
    REGION 'us-east-1',
    ACCESS_KEY_ID 'AKIA...',
    SECRET_ACCESS_KEY '...'
);

ATTACH 'my_uc' AS uc (
    TYPE unity_catalog,
    ENDPOINT 'https://api.uc.tabular.io',
    SECRET 'uc_cred'
);

-- Query Delta tables
SELECT * FROM uc.my_db.my_delta_table;
```

**Note:** This is experimental and may require Tabular's hosted Unity Catalog. For local Delta tables, use `delta_scan()` directly:

```sql
INSTALL delta;
LOAD delta;

SELECT * FROM delta_scan('s3://bucket/delta_table/');
```

---

### Attaching Iceberg

Use Iceberg extension or read via REST catalog:

```python
from duckdb import DuckDBPyConnection

con = duckdb.connect()
con.execute("INSTALL iceberg; LOAD iceberg;")

# Attach Iceberg catalog
con.execute("""
ATTACH 'iceberg_catalog' (
    TYPE iceberg,
    CATALOG 'hive',
    URI 'thrift://localhost:9083',
    WAREHOUSE 's3://bucket/warehouse/'
);
""")

# Query
df = con.execute("SELECT * FROM iceberg.db.my_table").df()
```

---

### Unified Multi-Source View

Create a virtual view that unions data from all sources:

```sql
CREATE VIEW unified_orders AS
SELECT
    'postgres' AS source_system,
    o.order_id,
    o.amount,
    o.order_date,
    NULL AS metadata
FROM pg_db.public.orders o
UNION ALL
SELECT
    'delta' AS source_system,
    o.order_id,
    o.amount,
    o.order_date,
    o._metadata
FROM uc.production.orders o
UNION ALL
SELECT
    'iceberg' AS source_system,
    o.order_id,
    o.amount,
    o.order_date,
    o._metadata
FROM iceberg.analytics.orders o;
```

Now query the unified view:

```sql
SELECT source_system, COUNT(*) FROM unified_orders GROUP BY source_system;
```

**Use case:** Cross-platform migration validation (ensure counts match between Postgres source and Delta target).

---

### Limitations of DuckDB-as-Catalog

| Limitation | Impact | Workaround |
|------------|---------|------------|
| **No REST API** | Only in-process access; no multi-service sharing | Run query gateway (FastAPI) that wraps DuckDB (but single point of failure) |
| **Write lock** | Only one writer at a time (file-based DB) | Use Postgres as DuckLake backend for multi-client |
| **No fine-grained auth** | All queries share same DB credentials | Use separate DuckDB files per user (not shared) |
| **Scalability** | Metadata fits in memory; works for ≤ 100k tables | Large enterprises need dedicated catalog service (Glue, Hive, Tabular) |
| **Availability** | Single file corruption = total loss | Back up catalog DB frequently |

**Conclusion:** Use DuckDB for **single-user/developer** catalog or **small team PoC**. For production multi-user data platforms, use **AWS Glue** (AWS), **Hive Metastore** (self-hosted), or **Tabular** (Iceberg-native).

---

## Open Source Catalogs Comparison (2024)

### Amundsen (Lyft)

**Focus:** Data discovery, lightweight

- **Metadata store:** Neo4j (graph) + MySQL (text search)
- **Lineage:** Limited (no built-in column-level)
- **Search:** Simple keyword search, easy to use
- **Governance:** Minimal
- **Deployment:** Easiest (fewer services)
- **Best for:** Small teams needing basic discovery
- **Status:** Slower development post-2023 acquisition

---

### DataHub (LinkedIn)

**Focus:** Scalable, enterprise-grade

- **Metadata store:** MySQL (RDBMS) + Kafka (streaming updates)
- **Lineage:** Full end-to-end (auto-ingested from Spark, Flink, etc.)
- **Search:** Advanced faceted search, elastic
- **Governance:** Strong (PII tagging, access policies)
- **Deployment:** Complex (requires multiple services)
- **Best for:** Large enterprises ( LinkedIn-scale)
- **Extensibility:** High (many metadata source connectors)

---

### OpenMetadata

**Focus:** Unified governance & quality

- **Metadata store:** Postgres + Elasticsearch/OpenSearch
- **Lineage:** Built-in, column-level
- **Search:** Good
- **Governance:** Excellent (workflows, tasks, approvals, data quality tests integration)
- **Deployment:** Moderate (needs Postgres, OpenSearch, Airflow for ingestion)
- **Best for:** Teams needing strong governance + quality testing
- **Modern UI:** Cleanest interface

---

### Comparison Summary

| Tool | Discovery | Lineage | Governance | Scale | Ops Complexity |
|------|-----------|---------|------------|-------|----------------|
| Amundsen | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | Small | Low |
| DataHub | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Enterprise | High |
| OpenMetadata | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Medium-Large | Moderate |

**Recommendation:**
- **Start with OpenMetadata** for new projects (governance + quality focus)
- **Use DataHub** if you need massive scale and lineage automation
- **Avoid Amundsen** for new deployments (stale)

---

## Catalog Selection Matrix for Lakehouse

| Scenario | Recommended Catalog |
|----------|---------------------|
| **AWS-native (Athena, Redshift)** | AWS Glue |
| **Azure-native (Synapse, Fabric)** | Azure Data Catalog / Unity Catalog |
| **Self-hosted Hadoop/Spark** | Hive Metastore |
| **Iceberg-first, multi-cloud** | Tabular or Hive Metastore |
| **Small team, PoC** | DuckDB + DuckLake (single file) |
| **Governance-heavy** | OpenMetadata (with separate metastore for Iceberg/Delta) |
| **LinkedIn-scale** | DataHub |

---

## Setting Up a Multi-Source Catalog (DuckDB Pattern)

Use this concise flow in the main skill:

1. Create a local DuckDB catalog DB and load extensions (`httpfs`, `postgres`, `delta`, `iceberg`, `ducklake`)
2. Attach each source system (Postgres, Delta, Iceberg)
3. Build a unified view over all sources
4. Run validation queries across sources

For complete runnable examples, see:
- `duckdb-multisource.md`

---

## Best Practices

### Catalog Selection

1. **Default to Hive Metastore** if you have existing Hadoop investments.
2. **Use AWS Glue** for pure AWS stacks (Athena, EMR).
3. **Choose Tabular** for Iceberg-first with branching needs.
4. **Keep separate** Iceberg catalog from business metadata catalog (OpenMetadata) - they serve different purposes.

### DuckDB Multi-Source Pattern

1. **Use for development only** - Not production multi-user
2. **Store catalog DuckDB file** in version control (encrypted if credentials)
3. **Separate credentials** from catalog - use environment variables or secret manager
4. **Read-only attaches** for source systems - prevent accidental writes
5. **Back up DuckDB** regularly if using as primary catalog

---

## References

- `@data-engineering-storage-lakehouse` - Delta Lake, Iceberg table formats
- **`@data-engineering-best-practices`** - Medallion architecture, dataset lifecycle, partitioning, schema evolution
- `duckdb-multisource.md` - Step-by-step DuckDB multi-source catalog setup
- [Apache Iceberg Catalog Documentation](https://iceberg.apache.org/docs/latest/catalog/)
- [PyIceberg Catalog API](https://py.iceberg.apache.org/reference/pyiceberg/catalog/)
- [DuckDB ATTACH Documentation](https://duckdb.org/docs/stable/sql/statements/attach.html)
- [DuckLake Documentation](https://ducklake.select/docs/stable/duckdb/usage/)
- [Unity Catalog Extension](https://duckdb.org/docs/stable/core_extensions/unity_catalog.html)
- [OpenMetadata vs DataHub vs Amundsen](https://atlan.com/open-source-data-catalog-tools/)
