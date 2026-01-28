---
name: etl-tools
description: Apache Airflow, dbt, Prefect, Dagster, and modern data orchestration for production data pipelines
sasmp_version: "1.3.0"
bonded_agent: 01-data-engineer
bond_type: PRIMARY_BOND
skill_version: "2.0.0"
last_updated: "2025-01"
complexity: intermediate
estimated_mastery_hours: 140
prerequisites: [python-programming, sql-databases]
unlocks: [big-data, data-warehousing, mlops]
---

# ETL Tools & Data Orchestration

Production-grade data pipeline development with Apache Airflow, dbt, and modern orchestration patterns.

## Quick Start

```python
# Apache Airflow 2.8+ TaskFlow API
from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import pandas as pd

default_args = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "email_on_failure": True,
    "email": ["alerts@company.com"],
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "retry_exponential_backoff": True,
    "max_retry_delay": timedelta(minutes=30),
}

@dag(
    dag_id="etl_pipeline_v2",
    schedule="0 2 * * *",  # 2 AM daily
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["production", "etl"],
    default_args=default_args,
    doc_md="""
    ## Daily Sales ETL Pipeline

    Extracts from PostgreSQL, transforms, loads to S3.

    ### Data Quality Checks
    - Row count validation
    - Schema validation
    - Freshness check
    """
)
def etl_pipeline():

    @task
    def extract_sales(execution_date: str = None) -> dict:
        """Extract daily sales from PostgreSQL."""
        hook = PostgresHook(postgres_conn_id="postgres_prod")
        query = """
            SELECT order_id, customer_id, product_id,
                   quantity, unit_price, order_date
            FROM orders
            WHERE order_date = %(date)s
        """
        df = hook.get_pandas_df(query, parameters={"date": execution_date})

        if df.empty:
            raise ValueError(f"No data for {execution_date}")

        return {"path": f"/tmp/extract_{execution_date}.parquet", "count": len(df)}

    @task
    def transform_sales(extract_result: dict) -> dict:
        """Apply business transformations."""
        df = pd.read_parquet(extract_result["path"])

        # Business logic
        df["total_amount"] = df["quantity"] * df["unit_price"]
        df["discount_tier"] = pd.cut(
            df["total_amount"],
            bins=[0, 100, 500, float("inf")],
            labels=["small", "medium", "large"]
        )

        output_path = extract_result["path"].replace("extract", "transform")
        df.to_parquet(output_path, index=False)

        return {"path": output_path, "count": len(df)}

    @task
    def load_to_s3(transform_result: dict, execution_date: str = None) -> str:
        """Load to S3 with partitioning."""
        s3_hook = S3Hook(aws_conn_id="aws_prod")

        s3_key = f"sales/year={execution_date[:4]}/month={execution_date[5:7]}/day={execution_date[8:10]}/data.parquet"

        s3_hook.load_file(
            filename=transform_result["path"],
            key=s3_key,
            bucket_name="data-lake-prod",
            replace=True
        )

        return f"s3://data-lake-prod/{s3_key}"

    @task
    def validate_load(s3_path: str) -> bool:
        """Validate data was loaded correctly."""
        s3_hook = S3Hook(aws_conn_id="aws_prod")

        # Check file exists and has content
        key = s3_path.replace("s3://data-lake-prod/", "")
        metadata = s3_hook.get_key(key, bucket_name="data-lake-prod")

        if metadata.content_length < 100:
            raise ValueError(f"File too small: {metadata.content_length} bytes")

        return True

    # DAG flow
    extracted = extract_sales()
    transformed = transform_sales(extracted)
    loaded = load_to_s3(transformed)
    validate_load(loaded)

# Instantiate DAG
etl_pipeline()
```

## Core Concepts

### 1. Airflow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Airflow Architecture                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  Scheduler   │───▶│   Executor   │───▶│   Workers    │  │
│  │              │    │ (Celery/K8s) │    │              │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                                       │           │
│         ▼                                       ▼           │
│  ┌──────────────┐                       ┌──────────────┐   │
│  │   Metadata   │                       │    Logs      │   │
│  │   Database   │                       │   Storage    │   │
│  │  (Postgres)  │                       │    (S3)      │   │
│  └──────────────┘                       └──────────────┘   │
│         │                                                   │
│         ▼                                                   │
│  ┌──────────────┐                                          │
│  │   Webserver  │  ← UI for monitoring                     │
│  └──────────────┘                                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 2. Sensor Patterns

```python
from airflow.sensors.sql import SqlSensor
from airflow.sensors.s3 import S3KeySensor
from airflow.providers.http.sensors.http import HttpSensor

@dag(...)
def sensor_pipeline():

    # Wait for upstream data
    wait_for_source = SqlSensor(
        task_id="wait_for_source_data",
        conn_id="postgres_prod",
        sql="""
            SELECT COUNT(*) > 0
            FROM source_table
            WHERE date = '{{ ds }}'
        """,
        mode="reschedule",  # Release worker while waiting
        poke_interval=300,  # Check every 5 minutes
        timeout=3600 * 6,   # 6 hour timeout
        exponential_backoff=True,
    )

    # Wait for file in S3
    wait_for_file = S3KeySensor(
        task_id="wait_for_s3_file",
        bucket_name="source-bucket",
        bucket_key="data/{{ ds }}/complete.flag",
        aws_conn_id="aws_prod",
        mode="reschedule",
        poke_interval=60,
        timeout=3600,
    )

    # Wait for API to be healthy
    check_api = HttpSensor(
        task_id="check_api_health",
        http_conn_id="api_conn",
        endpoint="/health",
        response_check=lambda response: response.json()["status"] == "healthy",
        mode="poke",
        poke_interval=30,
        timeout=300,
    )

    [wait_for_source, wait_for_file, check_api] >> process_data()
```

### 3. Dynamic Task Generation

```python
from airflow.decorators import dag, task
from airflow.utils.task_group import TaskGroup

@dag(...)
def dynamic_pipeline():

    @task
    def get_partitions() -> list:
        """Dynamically determine partitions to process."""
        return ["us", "eu", "apac"]

    @task
    def process_partition(partition: str) -> dict:
        """Process single partition."""
        # Processing logic
        return {"partition": partition, "status": "success"}

    @task
    def aggregate_results(results: list) -> None:
        """Combine results from all partitions."""
        for result in results:
            print(f"Partition {result['partition']}: {result['status']}")

    partitions = get_partitions()

    # Dynamic task mapping (Airflow 2.3+)
    processed = process_partition.expand(partition=partitions)

    aggregate_results(processed)

# Alternative: Task Groups for organization
@dag(...)
def grouped_pipeline():
    with TaskGroup("extraction") as extract_group:
        extract_users = extract("users")
        extract_orders = extract("orders")
        extract_products = extract("products")

    with TaskGroup("transformation") as transform_group:
        transform_all = transform()

    with TaskGroup("loading") as load_group:
        load_warehouse = load()

    extract_group >> transform_group >> load_group
```

### 4. dbt Integration

```sql
-- models/staging/stg_orders.sql
{{
    config(
        materialized='incremental',
        unique_key='order_id',
        on_schema_change='sync_all_columns'
    )
}}

WITH source AS (
    SELECT * FROM {{ source('raw', 'orders') }}
    {% if is_incremental() %}
    WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})
    {% endif %}
),

cleaned AS (
    SELECT
        order_id,
        customer_id,
        COALESCE(product_id, 'UNKNOWN') AS product_id,
        quantity,
        unit_price,
        quantity * unit_price AS total_amount,
        order_date,
        updated_at
    FROM source
    WHERE order_id IS NOT NULL
)

SELECT * FROM cleaned
```

```yaml
# dbt_project.yml
name: 'data_warehouse'
version: '1.0.0'

profile: 'production'

model-paths: ["models"]
test-paths: ["tests"]
macro-paths: ["macros"]

models:
  data_warehouse:
    staging:
      +materialized: view
      +schema: staging
    marts:
      +materialized: table
      +schema: analytics

vars:
  start_date: '2024-01-01'
```

```python
# Airflow + dbt integration
from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig

@dag(...)
def dbt_pipeline():

    dbt_transform = DbtTaskGroup(
        group_id="dbt_transform",
        project_config=ProjectConfig(
            dbt_project_path="/opt/dbt/project",
        ),
        profile_config=ProfileConfig(
            profile_name="production",
            target_name="prod",
        ),
        default_args={"retries": 2},
    )

    extract() >> dbt_transform >> notify()
```

### 5. Data Quality with Great Expectations

```python
from airflow.decorators import dag, task
from great_expectations.checkpoint import Checkpoint
import great_expectations as gx

@dag(...)
def quality_pipeline():

    @task
    def validate_data(dataset_path: str) -> dict:
        """Run Great Expectations validation."""
        context = gx.get_context()

        # Define expectations
        validator = context.sources.pandas_default.read_csv(dataset_path)

        validator.expect_column_to_exist("order_id")
        validator.expect_column_values_to_not_be_null("order_id")
        validator.expect_column_values_to_be_unique("order_id")
        validator.expect_column_values_to_be_between(
            "quantity", min_value=1, max_value=1000
        )
        validator.expect_column_values_to_be_in_set(
            "status", ["pending", "completed", "cancelled"]
        )

        results = validator.validate()

        if not results.success:
            raise ValueError(f"Data quality check failed: {results}")

        return {"success": True, "stats": results.statistics}

    @task.branch
    def check_quality_result(result: dict) -> str:
        """Branch based on quality results."""
        if result.get("success"):
            return "proceed_to_load"
        return "alert_and_stop"
```

## Tools & Technologies

| Tool | Purpose | Version (2025) |
|------|---------|----------------|
| **Apache Airflow** | Workflow orchestration | 2.8+ |
| **dbt Core** | SQL transformation | 1.7+ |
| **Prefect** | Modern orchestration | 2.14+ |
| **Dagster** | Data-aware orchestration | 1.5+ |
| **Great Expectations** | Data quality | 0.18+ |
| **Airbyte** | Data integration | 0.55+ |
| **Fivetran** | Managed EL | Latest |
| **Apache NiFi** | Data flow automation | 2.0+ |

## Learning Path

### Phase 1: Foundations (Weeks 1-3)
```
Week 1: ETL vs ELT concepts, batch vs streaming
Week 2: Airflow basics, DAGs, operators
Week 3: Connections, variables, XComs
```

### Phase 2: Intermediate (Weeks 4-7)
```
Week 4: TaskFlow API, dynamic tasks
Week 5: Sensors, triggers, callbacks
Week 6: dbt fundamentals, models, tests
Week 7: dbt macros, packages, documentation
```

### Phase 3: Advanced (Weeks 8-11)
```
Week 8: Data quality frameworks
Week 9: Airflow + dbt integration (Cosmos)
Week 10: Custom operators, plugins
Week 11: Performance tuning, parallelism
```

### Phase 4: Production (Weeks 12-14)
```
Week 12: CI/CD for pipelines
Week 13: Monitoring, alerting, SLAs
Week 14: Multi-environment deployment
```

## Production Patterns

### Idempotent Pipeline Design

```python
@task
def load_data_idempotent(data: dict, execution_date: str) -> None:
    """
    Idempotent load: can be safely re-run without duplicates.
    """
    hook = PostgresHook(postgres_conn_id="postgres")

    # Delete existing data for this run
    hook.run(
        "DELETE FROM fact_sales WHERE load_date = %(date)s",
        parameters={"date": execution_date}
    )

    # Insert new data
    hook.insert_rows(
        table="fact_sales",
        rows=data["rows"],
        target_fields=["order_id", "amount", "load_date"]
    )
```

### SLA and Alerting

```python
from airflow.exceptions import AirflowSensorTimeout
from airflow.models import Variable

@dag(
    sla_miss_callback=sla_alert_callback,
    default_args={
        "sla": timedelta(hours=4),  # Pipeline SLA
    }
)
def sla_pipeline():

    @task(sla=timedelta(hours=1))  # Task-level SLA
    def critical_transform():
        pass

    @task.on_failure_callback
    def alert_on_failure(context):
        """Send alert on task failure."""
        task_instance = context["task_instance"]
        exception = context["exception"]

        slack_webhook = Variable.get("slack_webhook")
        message = f"""
        :red_circle: Pipeline Failed
        DAG: {task_instance.dag_id}
        Task: {task_instance.task_id}
        Error: {str(exception)[:500]}
        """
        # Send to Slack/PagerDuty
```

## Troubleshooting Guide

### Common Failure Modes

| Issue | Symptoms | Root Cause | Fix |
|-------|----------|------------|-----|
| **Task Stuck** | Task in "queued" state | No available workers | Scale workers, check executor |
| **DAG Not Found** | DAG missing in UI | Parse error, wrong folder | Check logs, fix syntax |
| **Connection Error** | Task fails on connect | Wrong credentials, network | Verify connection in UI |
| **XCom Too Large** | Task fails after success | Returning large data | Use external storage |
| **Zombie Tasks** | Tasks never complete | Worker died mid-task | Enable heartbeat, set timeout |

### Debug Checklist

```bash
# 1. Check DAG parse errors
airflow dags list-import-errors

# 2. Test DAG syntax
python /path/to/dag.py

# 3. Test specific task
airflow tasks test dag_id task_id 2024-01-01

# 4. Check task logs
airflow tasks logs dag_id task_id 2024-01-01

# 5. Clear failed tasks for retry
airflow tasks clear dag_id -s 2024-01-01 -e 2024-01-01

# 6. Check scheduler health
airflow jobs check --job-type SchedulerJob --limit 1

# 7. List running tasks
airflow tasks states-for-dag-run dag_id 2024-01-01
```

### Log Interpretation

```python
# Common log patterns and meanings

# ✅ Success
# [2024-01-01 02:00:00] INFO - Task completed successfully

# ⚠️ Retry
# [2024-01-01 02:00:00] WARNING - Retry 1/3: Connection refused
# [2024-01-01 02:05:00] INFO - Task completed on retry 2

# ❌ Failure after retries
# [2024-01-01 02:15:00] ERROR - Task failed after 3 retries
# [2024-01-01 02:15:00] ERROR - Exception: ConnectionError(...)

# 🔍 Resource issue
# [2024-01-01 02:00:00] WARNING - Celery worker memory: 95%
# [2024-01-01 02:00:00] ERROR - Worker killed by OOM
```

## Unit Test Template

```python
import pytest
from datetime import datetime
from airflow.models import DagBag, TaskInstance
from airflow.utils.state import State
from unittest.mock import patch, MagicMock

class TestDAGIntegrity:
    """Test DAG structure and configuration."""

    @pytest.fixture
    def dagbag(self):
        return DagBag(dag_folder="dags/", include_examples=False)

    def test_no_import_errors(self, dagbag):
        assert len(dagbag.import_errors) == 0, f"Import errors: {dagbag.import_errors}"

    def test_dag_has_required_tags(self, dagbag):
        for dag_id, dag in dagbag.dags.items():
            assert "production" in dag.tags or "development" in dag.tags

    def test_dag_has_owner(self, dagbag):
        for dag_id, dag in dagbag.dags.items():
            assert dag.default_args.get("owner") is not None

    def test_dag_has_retries(self, dagbag):
        for dag_id, dag in dagbag.dags.items():
            assert dag.default_args.get("retries", 0) >= 2


class TestTaskLogic:
    """Test individual task logic."""

    @patch("dags.etl_pipeline.PostgresHook")
    def test_extract_returns_data(self, mock_hook):
        from dags.etl_pipeline import extract_sales

        # Arrange
        mock_hook.return_value.get_pandas_df.return_value = pd.DataFrame({
            "order_id": [1, 2, 3],
            "amount": [100, 200, 300]
        })

        # Act
        result = extract_sales(execution_date="2024-01-01")

        # Assert
        assert result["count"] == 3
        assert "path" in result

    @patch("dags.etl_pipeline.PostgresHook")
    def test_extract_raises_on_empty(self, mock_hook):
        from dags.etl_pipeline import extract_sales

        mock_hook.return_value.get_pandas_df.return_value = pd.DataFrame()

        with pytest.raises(ValueError, match="No data"):
            extract_sales(execution_date="2024-01-01")
```

## Best Practices

### Pipeline Design
```python
# ✅ DO: Make tasks atomic and idempotent
@task
def process_chunk(chunk_id: str, execution_date: str):
    # Can be re-run safely
    clear_existing(chunk_id, execution_date)
    process_and_insert(chunk_id, execution_date)

# ✅ DO: Use meaningful task IDs
extract_customer_data = ...  # Good
task1 = ...  # Bad

# ✅ DO: Keep DAGs simple, split complex pipelines
# Instead of one 50-task DAG, create multiple focused DAGs

# ❌ DON'T: Put business logic in DAG file
# Keep DAG definition separate from processing code

# ❌ DON'T: Return large data via XCom
@task
def bad_practice():
    return huge_dataframe  # Don't do this

@task
def good_practice():
    save_to_s3(huge_dataframe)
    return {"s3_path": "s3://bucket/data.parquet"}
```

### Error Handling
```python
# ✅ DO: Use appropriate retry configuration
default_args = {
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "retry_exponential_backoff": True,
    "max_retry_delay": timedelta(minutes=60),
}

# ✅ DO: Add failure callbacks
@task(on_failure_callback=alert_team)
def critical_task():
    pass

# ✅ DO: Set reasonable timeouts
@task(execution_timeout=timedelta(hours=2))
def long_running_task():
    pass
```

## Resources

### Official Documentation
- [Apache Airflow Docs](https://airflow.apache.org/docs/)
- [dbt Docs](https://docs.getdbt.com/)
- [Prefect Docs](https://docs.prefect.io/)
- [Dagster Docs](https://docs.dagster.io/)

### Best Practices
- [Astronomer Guides](https://www.astronomer.io/guides/)
- [dbt Best Practices](https://docs.getdbt.com/guides/best-practices)
- [Data Engineering Weekly](https://www.dataengineeringweekly.com/)

### Community
- [Apache Airflow Slack](https://apache-airflow-slack.herokuapp.com/)
- [dbt Community](https://community.getdbt.com/)
- [r/dataengineering](https://reddit.com/r/dataengineering)

## Next Skills

After mastering ETL Tools:
- → `big-data` - Scale with Spark
- → `data-warehousing` - Design data models
- → `mlops` - Orchestrate ML pipelines
- → `monitoring-observability` - Production observability

---

**Skill Certification Checklist:**
- [ ] Can design idempotent, fault-tolerant DAGs
- [ ] Can use TaskFlow API and dynamic task mapping
- [ ] Can integrate dbt with Airflow
- [ ] Can implement data quality checks
- [ ] Can debug and monitor pipelines in production
