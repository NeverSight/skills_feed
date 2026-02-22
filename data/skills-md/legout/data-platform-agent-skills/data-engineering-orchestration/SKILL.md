---
name: data-engineering-orchestration
description: "Pipeline orchestration and workflow management with Prefect, Dagster, and dbt. Covers scheduling, dependency management, retries, and integration patterns."
dependsOn: ["@data-engineering-core"]
---

# Pipeline Orchestration

Workflow orchestration tools for data pipelines: Prefect, Dagster, and dbt. These tools handle scheduling, dependency resolution, retries, monitoring, and state management for production data pipelines.

## Quick Comparison

| Tool | Paradigm | Best For | Learning Curve |
|------|----------|----------|----------------|
| **Prefect** | Flow-based | Pythonic workflows, quick prototypes, cloud-first | Moderate |
| **Dagster** | Asset-based | Data asset lineage, reproducibility, type checking | Steeper |
| **dbt** | SQL transformations | Analytics engineering, ELT, data warehouses | Low (SQL-focused) |
| **FlowerPower** | Hamilton DAGs | Lightweight batch ETL, configuration-driven pipelines | Low-Moderate |

## When to Use Which?

- **Prefect**: You want Python code flexibility, Prefect Cloud UI, and quick setup. Good for general-purpose data pipelines, ETL, and API integrations.

- **Dagster**: You care about data asset observability, type safety, and reproducibility. Good for complex data platforms with clear asset dependencies.

- **dbt**: Your transformations are primarily SQL and you're building analytics marts in a data warehouse. Great for analytics engineering teams.

## Skill Dependencies

Assumes familiarity with:
- `@data-engineering-core` - Polars, DuckDB, PyArrow
- `@data-engineering-storage-remote-access` - Cloud storage for intermediate data

Related:
- `@data-engineering-quality` - Data validation integrated into orchestration
- `@data-engineering-observability` - Monitoring and tracing
- `@data-engineering-storage-lakehouse` - Delta/Iceberg for state management

---

## Detailed Guides

### Prefect
See: `@data-engineering-orchestration/prefect.md`

- Flows and tasks with decorators
- Retries, caching, and parameters
- Prefect Cloud (serverless) vs Prefect Server (self-hosted)
- Deployment patterns

### Dagster
See: `@data-engineering-orchestration/dagster.md`

- Asset-based programming model
- Materialization and partitions
- Type checking with Dagster types
- Sensors and schedules
- Integration with data platforms

### dbt (Data Build Tool)
See: `@data-engineering-orchestration/dbt.md`

- Projects, models, tests, snapshots, seeds
- Jinja templating and macros
- Data testing (schema, cardinality, custom)
- Documentation generation
- Package management (dbt packages)
- Adapters (DuckDB, Postgres, Snowflake, BigQuery, Spark)

### FlowerPower (Lightweight Alternative)

**FlowerPower** is a lightweight DAG orchestration framework built on Apache Hamilton, ideal for batch ETL and data transformation scripts without the overhead of full orchestrators.

**Key characteristics:**
- **Hamilton-based**: Define pipelines as Python functions; DAG auto-constructed
- **Configuration-driven**: YAML files for parameters and execution settings
- **Lightweight**: No database, no scheduler, no state persistence (batch-only)
- **Multiple executors**: synchronous, threadpool, processpool, ray, dask
- **I/O plugins**: Delta Lake, DuckDB, Polars, Pandas, S3, PostgreSQL, and more

**When to choose FlowerPower over Prefect/Dagster:**
- Simple batch pipelines (daily/Hourly ETL)
- Quick prototyping that can grow
- Teams that prefer code-first (Python functions) over YAML/UI
- No need for sophisticated scheduling, SLA tracking, or long-running state

**When NOT to use:**
- Production 24/7 workflows requiring reliability guarantees
- Complex dependency graphs with cross-dependencies
- Need for built-in retry policies with circuit breakers
- Workflows requiring checkpoints and state recovery
- Multi-team orchestration with fine-grained permissions

**FlowerPower limitations vs. Prefect/Dagster:**
| Feature | Prefect/Dagster | FlowerPower |
|---------|----------------|-------------|
| Scheduling | Native (cron, intervals) | External (cron/systemd) |
| State persistence | Database/cloud | None (ephemeral) |
| Retry policies | Configurable per task | Per-pipeline via YAML |
| Observability | Rich UI, lineage | Basic Hamilton UI |
| Production readiness | High | Moderate (batch jobs) |

**Integration with data-engineering stack:**
- Uses **Polars/DuckDB** for DataFrame operations (`@data-engineering-core`)
- **Delta Lake** for ACID table formats (`@data-engineering-storage-lakehouse`)
- **fsspec/S3** for cloud storage (`@data-engineering-storage-remote-access`)
- **Pandera** for data validation (`@data-engineering-quality`)
- Follows **medallion architecture** (`@data-engineering-best-practices`)

**Skill reference:** `@flowerpower` - Complete guide to FlowerPower with advanced production patterns (watermarks, data quality, incremental loads, cloud deployment).

---

### Cloud Storage Integration
See: `@data-engineering-orchestration/integrations/cloud-storage.md`

- dbt + S3/GCS via HTTPFS (DuckDB), aws_s3 extension (Postgres)
- Configuration patterns for profiles.yml
- Credential management best practices

---

## Common Patterns

### Retry Pattern (All Orchestrators)
```python
# Prefect: @task(retries=3, retry_delay_seconds=60)
# Dagster: @asset(retry_policy=RetryPolicy(...))
# dbt: --fail-fast flag + custom macro retry logic
```

### Idempotency
All orchestrators assume idempotent operations - running twice should produce identical results. Design your `INSERT`, `UPDATE`, `MERGE` operations to be idempotent.

### State Management
- **Prefect**: Flow run state persisted to database/cloud
- **Dagster**: Asset materialization events tracked
- **dbt**: Model run status in `dbt_run_results.json`; uses `SELECT` + `INSERT` by default

### Dependency Management
- **Prefect**: Explicit task dependencies (`task1 >> task2`)
- **Dagster**: Asset dependencies (`@asset(depends_on=[other_asset])`)
- **dbt**: DAG built from DAG from `ref()` calls in models

---

## Production Recommendations

1. **Version control everything**: Code, configs, dbt models, Prefect/Dagster definitions
2. **Test locally first**: Use unit tests for transformation logic, integration tests for pipeline runs
3. **Use environment variables** for credentials (never hardcode)
4. **Monitor pipeline runs**: Prefect Cloud UI, Dagster Dagit, dbt Cloud or custom alerts
5. **Alert on failures**: Configure email/Slack/webhook notifications
6. **Log aggregation**: Send orchestrator logs to centralized system (Datadog, CloudWatch)
7. **Idempotent writes**: Avoid duplicate data on retries
8. **Schema evolution**: Handle schema changes gracefully (additive only preferred)

---

## References

- [Prefect Documentation](https://docs.prefect.io/)
- [Dagster Documentation](https://docs.dagster.io/)
- [dbt Documentation](https://docs.getdbt.com/)
- [dbt-Labs/dbt-duckdb adapter](https://github.com/dbt-labs/dbt-duckdb)
