---
name: dagster-integrations
description:
  Comprehensive index of 82+ Dagster integrations organized by category. Includes AI (OpenAI,
  Anthropic), ETL (dbt, Fivetran, Airbyte, PySpark), Storage (Snowflake, BigQuery), Compute (AWS,
  Databricks, Spark), BI (Looker, Tableau), Monitoring, Alerting, and Testing. Use when discovering
  integrations or finding the right tool for a use case.
references:
  - ai
  - alerting
  - bi
  - compute
  - etl
  - monitoring
  - other
  - storage
  - testing
---

# Dagster Integrations Skill

Comprehensive catalog of 82+ Dagster integrations organized by category to help you find the right
tool for your data pipeline needs.

## When to Use This Skill

Auto-invoke when users ask about:

- "which integration for..." / "does dagster support..."
- "snowflake vs bigquery" / comparing integrations
- "what integrations are available" / discovering tools
- "how to connect to X" / integration discovery
- "best tool for Y" / choosing between similar integrations
- "dbt in dagster" / specific integration questions
- Any question about external tool integration with Dagster

## Integration Discovery Tree

Find the right integration based on your needs:

```
What do you need to do?

├─ Load data from external sources?
│  ├─ SaaS applications → references/etl.md (Fivetran, Airbyte)
│  ├─ Files/databases → references/etl.md (dlt, Sling, Meltano)
│  └─ Cloud storage → references/storage.md (S3, GCS, Azure Blob)
│
├─ Transform data?
│  ├─ SQL transformations → references/etl.md (dbt)
│  ├─ Distributed transformations → references/etl.md (PySpark)
│  ├─ DataFrame operations → references/other.md (Pandas, Polars)
│  └─ Large-scale processing → references/compute.md (Spark, Dask, Ray)
│
├─ Store data?
│  ├─ Cloud data warehouse → references/storage.md (Snowflake, BigQuery, Redshift)
│  ├─ Relational database → references/storage.md (Postgres, MySQL)
│  ├─ File/object storage → references/storage.md (S3, GCS, Azure, LakeFS)
│  ├─ Analytics database → references/storage.md (DuckDB)
│  └─ Vector embeddings → references/storage.md (Weaviate, Chroma, Qdrant)
│
├─ Validate data quality?
│  ├─ Schema validation → references/testing.md (Pandera)
│  └─ Quality checks → references/testing.md (Great Expectations)
│
├─ Run ML workloads?
│  ├─ LLM integration → references/ai.md (OpenAI, Anthropic, Gemini)
│  ├─ Experiment tracking → references/ai.md (MLflow, W&B)
│  └─ Distributed training → references/compute.md (Ray, Spark)
│
├─ Execute computation?
│  ├─ Cloud compute → references/compute.md (AWS, Azure, GCP, Databricks)
│  ├─ Containers → references/compute.md (Docker, Kubernetes)
│  └─ Distributed processing → references/compute.md (Spark, Dask, Ray)
│
├─ Monitor pipelines?
│  ├─ Team notifications → references/alerting.md (Slack, MS Teams, PagerDuty)
│  ├─ Metrics tracking → references/monitoring.md (Datadog, Prometheus)
│  └─ Log aggregation → references/monitoring.md (Papertrail)
│
└─ Visualize data?
   ├─ BI dashboards → references/bi.md (Looker, Tableau, PowerBI)
   └─ Analytics platform → references/bi.md (Sigma, Hex, Evidence)
```

## When to Use This Skill vs. Others

| User Need                  | Use This Skill                                                | Alternative Skill         |
| -------------------------- | ------------------------------------------------------------- | ------------------------- |
| "which integration for X"  | ✅ Yes - discover integrations                                |                           |
| "does dagster support X"   | ✅ Yes - check availability                                   |                           |
| "snowflake vs bigquery"    | ✅ Yes - compare options                                      |                           |
| "best practices for X"     | ❌ No                                                         | `/dagster-best-practices` |
| "implement X integration"  | ❌ First discover here, then use `/dg`                        |                           |
| "how do I use dbt"         | ❌ Discover here, learn patterns at `/dagster-best-practices` |                           |
| "create new project"       | ❌ No                                                         | `/dg` for scaffolding     |
| "scaffold dbt integration" | ❌ First discover here, then use `/dg`                        |                           |

## Quick Reference by Category

| Category               | Count | Common Tools                          | Reference                  |
| ---------------------- | ----- | ------------------------------------- | -------------------------- |
| **AI & ML**            | 6     | OpenAI, Anthropic, MLflow, W&B        | `references/ai.md`         |
| **ETL/ELT**            | 9     | dbt, Fivetran, Airbyte, PySpark       | `references/etl.md`        |
| **Storage**            | 35+   | Snowflake, BigQuery, Postgres, DuckDB | `references/storage.md`    |
| **Compute**            | 15+   | AWS, Databricks, Spark, Docker, K8s   | `references/compute.md`    |
| **BI & Visualization** | 7     | Looker, Tableau, PowerBI, Sigma       | `references/bi.md`         |
| **Monitoring**         | 3     | Datadog, Prometheus, Papertrail       | `references/monitoring.md` |
| **Alerting**           | 6     | Slack, PagerDuty, MS Teams, Twilio    | `references/alerting.md`   |
| **Testing**            | 2     | Great Expectations, Pandera           | `references/testing.md`    |
| **Other**              | 2+    | Pandas, Polars                        | `references/other.md`      |

## Category Taxonomy

This index aligns with Dagster's official documentation taxonomy from tags.yml:

- **ai**: Artificial intelligence and machine learning integrations (LLM APIs, experiment tracking)
- **etl**: Extract, transform, and load tools including data replication and transformation
  frameworks
- **storage**: Databases, data warehouses, object storage, and table formats
- **compute**: Cloud platforms, container orchestration, and distributed processing frameworks
- **bi**: Business intelligence and visualization platforms
- **monitoring**: Observability platforms and metrics systems for tracking performance
- **alerting**: Notification and incident management systems for pipeline alerts
- **testing**: Data quality validation and testing frameworks
- **other**: Miscellaneous integrations including DataFrame libraries

**Note**: Support levels (dagster-supported, community-supported) are shown inline in each
integration entry.

Last verified: 2026-01-27

## Finding the Right Integration

### I need to...

**Load data from external sources**

- SaaS applications → [ETL](#etl) (Fivetran, Airbyte)
- Files/databases → [ETL](#etl) (dlt, Sling, Meltano)
- Cloud storage → [Storage](#storage) (S3, GCS, Azure Blob)

**Transform data**

- SQL transformations → [ETL](#etl) (dbt)
- Distributed transformations → [ETL](#etl) (PySpark)
- DataFrame operations → [Other](#other) (Pandas, Polars)
- Large-scale processing → [Compute](#compute) (Spark, Dask, Ray)

**Store data**

- Cloud data warehouse → [Storage](#storage) (Snowflake, BigQuery, Redshift)
- Relational database → [Storage](#storage) (Postgres, MySQL)
- File/object storage → [Storage](#storage) (S3, GCS, Azure, LakeFS)
- Analytics database → [Storage](#storage) (DuckDB)
- Vector embeddings → [Storage](#storage) (Weaviate, Chroma, Qdrant)

**Validate data quality**

- Schema validation → [Testing](#testing) (Pandera)
- Quality checks → [Testing](#testing) (Great Expectations)

**Run ML workloads**

- LLM integration → [AI](#ai) (OpenAI, Anthropic, Gemini)
- Experiment tracking → [AI](#ai) (MLflow, W&B)
- Distributed training → [Compute](#compute) (Ray, Spark)

**Execute computation**

- Cloud compute → [Compute](#compute) (AWS, Azure, GCP, Databricks)
- Containers → [Compute](#compute) (Docker, Kubernetes)
- Distributed processing → [Compute](#compute) (Spark, Dask, Ray)

**Monitor pipelines**

- Team notifications → [Alerting](#alerting) (Slack, MS Teams, PagerDuty)
- Metrics tracking → [Monitoring](#monitoring) (Datadog, Prometheus)
- Log aggregation → [Monitoring](#monitoring) (Papertrail)

**Visualize data**

- BI dashboards → [BI](#bi) (Looker, Tableau, PowerBI)
- Analytics platform → [BI](#bi) (Sigma, Hex, Evidence)

## Integration Categories

### AI & ML

Artificial intelligence and machine learning platforms, including LLM APIs and experiment tracking.

**Key integrations:**

- **OpenAI** - GPT models and embeddings API
- **Anthropic** - Claude AI models
- **Gemini** - Google's multimodal AI
- **MLflow** - Experiment tracking and model registry
- **Weights & Biases** - ML experiment tracking
- **NotDiamond** - LLM routing and optimization

See `references/ai.md` for all AI/ML integrations.

### ETL/ELT

Extract, transform, and load tools for data ingestion, transformation, and replication.

**Key integrations:**

- **dbt** - SQL-based transformation with automatic dependencies
- **Fivetran** - Automated SaaS data ingestion (component-based)
- **Airbyte** - Open-source ELT platform
- **dlt** - Python-based data loading (component-based)
- **Sling** - High-performance data replication (component-based)
- **PySpark** - Distributed data transformation
- **Meltano** - ELT for the modern data stack

See `references/etl.md` for all ETL/ELT integrations.

### Storage

Data warehouses, databases, object storage, vector databases, and table formats.

**Key integrations:**

- **Snowflake** - Cloud data warehouse with IO managers
- **BigQuery** - Google's serverless data warehouse
- **DuckDB** - In-process SQL analytics
- **Postgres** - Open-source relational database
- **Weaviate** - Vector database for AI search
- **Delta Lake** - ACID transactions for data lakes
- **DataHub** - Metadata catalog and lineage

See `references/storage.md` for all storage integrations.

### Compute

Cloud platforms, container orchestration, and distributed processing frameworks.

**Key integrations:**

- **AWS** - Cloud compute services (Glue, EMR, Lambda)
- **Databricks** - Unified analytics platform
- **GCP** - Google Cloud compute (Dataproc, Cloud Run)
- **Spark** - Distributed data processing engine
- **Dask** - Parallel computing framework
- **Docker** - Container execution with Pipes
- **Kubernetes** - Cloud-native orchestration
- **Ray** - Distributed computing for ML

See `references/compute.md` for all compute integrations.

### BI & Visualization

Business intelligence and visualization platforms for analytics and reporting.

**Key integrations:**

- **Looker** - Google's BI platform
- **Tableau** - Interactive dashboards
- **PowerBI** - Microsoft's BI tool
- **Sigma** - Cloud analytics platform
- **Hex** - Collaborative notebooks
- **Evidence** - Markdown-based BI
- **Cube** - Semantic layer platform

See `references/bi.md` for all BI integrations.

### Monitoring

Observability platforms and metrics systems for tracking pipeline performance.

**Key integrations:**

- **Datadog** - Comprehensive observability platform
- **Prometheus** - Time-series metrics collection
- **Papertrail** - Centralized log management

See `references/monitoring.md` for all monitoring integrations.

### Alerting

Notification and incident management systems for pipeline alerts.

**Key integrations:**

- **Slack** - Team messaging and alerts
- **PagerDuty** - Incident management for on-call
- **MS Teams** - Microsoft Teams notifications
- **Twilio** - SMS and voice notifications
- **Apprise** - Universal notification platform
- **DingTalk** - Team communication for Asian markets

See `references/alerting.md` for all alerting integrations.

### Testing

Data quality validation and testing frameworks for ensuring data reliability.

**Key integrations:**

- **Great Expectations** - Data validation with expectations
- **Pandera** - Statistical data validation for DataFrames

See `references/testing.md` for all testing integrations.

### Other

Miscellaneous integrations including DataFrame libraries and utility tools.

**Key integrations:**

- **Pandas** - In-memory DataFrame library
- **Polars** - Fast DataFrame library with columnar storage

See `references/other.md` for other integrations.

## References

Integration details are organized in the following files:

- **AI & ML**: `references/ai.md` - AI and ML platforms, LLM APIs, experiment tracking
- **ETL/ELT**: `references/etl.md` - Data ingestion, transformation, and replication tools
- **Storage**: `references/storage.md` - Warehouses, databases, object storage, vector DBs
- **Compute**: `references/compute.md` - Cloud platforms, containers, distributed processing
- **BI & Visualization**: `references/bi.md` - Business intelligence and analytics platforms
- **Monitoring**: `references/monitoring.md` - Observability and metrics systems
- **Alerting**: `references/alerting.md` - Notifications and incident management
- **Testing**: `references/testing.md` - Data quality and validation frameworks
- **Other**: `references/other.md` - DataFrame libraries and miscellaneous tools

## Using Integrations

Most Dagster integrations follow a common pattern:

1. **Install the package**:

   ```bash
   pip install dagster-<integration>
   ```

2. **Import and configure a resource**:

   ```python
   from dagster_<integration> import <Integration>Resource

   resource = <Integration>Resource(
       config_param=dg.EnvVar("ENV_VAR")
   )
   ```

3. **Use in your assets**:
   ```python
   @dg.asset
   def my_asset(integration: <Integration>Resource):
       # Use the integration
       pass
   ```

For component-based integrations (dbt, Fivetran, dlt, Sling), see the specific reference files for
scaffolding and configuration patterns.
