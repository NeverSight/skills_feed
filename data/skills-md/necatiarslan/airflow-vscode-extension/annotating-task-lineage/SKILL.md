---
name: annotating-task-lineage
description: Annotate Airflow tasks with data lineage using inlets and outlets. Use when the user wants to add lineage metadata to tasks, specify input/output datasets, or enable lineage tracking for operators without built-in OpenLineage extraction.
---

# Annotating Task Lineage with Inlets and Outlets

This skill guides you through adding manual lineage annotations to Airflow tasks using `inlets` and `outlets`.

## When to Use This Approach

| Scenario | Use Inlets/Outlets? |
| --- | --- |
| Operator has OpenLineage methods | No, modify the OL method directly |
| Operator has no built-in OpenLineage extractor | Yes |
| Simple table-level lineage is sufficient | Yes |
| Quick lineage setup without custom code | Yes |
| Need column-level lineage | No, use OpenLineage methods or custom extractor |
| Complex extraction logic needed | No, use OpenLineage methods or custom extractor |

## Supported Types for Inlets/Outlets

### OpenLineage Datasets (recommended)

```python
from openlineage.client.event_v2 import Dataset

source_table = Dataset(
    namespace="postgres://mydb:5432",
    name="public.orders",
)
```

### Airflow Assets (Airflow 3+)

```python
from airflow.sdk import Asset

orders_asset = Asset(uri="s3://my-bucket/data/orders")
```

### Airflow Datasets (Airflow 2.4+)

```python
from airflow.datasets import Dataset

orders_dataset = Dataset(uri="s3://my-bucket/data/orders")
```

## Basic Usage

### Setting Inlets and Outlets on Operators

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from openlineage.client.event_v2 import Dataset
import pendulum

source_table = Dataset(namespace="snowflake://account", name="raw.orders")
target_table = Dataset(namespace="snowflake://account", name="staging.orders_clean")
output_file = Dataset(namespace="s3://my-bucket", name="exports/orders.parquet")

with DAG(
    dag_id="etl_with_lineage",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    schedule="@daily",
) as dag:

    transform = BashOperator(
        task_id="transform_orders",
        bash_command="echo 'transforming...'",
        inlets=[source_table],
        outlets=[target_table],
    )

    export = BashOperator(
        task_id="export_to_s3",
        bash_command="echo 'exporting...'",
        inlets=[target_table],
        outlets=[output_file],
    )

    transform >> export
```

### Multiple Inputs and Outputs

```python
from openlineage.client.event_v2 import Dataset

customers = Dataset(namespace="postgres://crm:5432", name="public.customers")
orders = Dataset(namespace="postgres://sales:5432", name="public.orders")
products = Dataset(namespace="postgres://inventory:5432", name="public.products")

daily_summary = Dataset(namespace="snowflake://account", name="analytics.daily_summary")
customer_metrics = Dataset(namespace="snowflake://account", name="analytics.customer_metrics")

aggregate_task = PythonOperator(
    task_id="build_daily_aggregates",
    python_callable=build_aggregates,
    inlets=[customers, orders, products],
    outlets=[daily_summary, customer_metrics],
)
```

## Custom Operators

### Option 1: Implement OpenLineage Methods (recommended)

```python
from airflow.models import BaseOperator

class MyCustomOperator(BaseOperator):
    def __init__(self, source_table: str, target_table: str, **kwargs):
        super().__init__(**kwargs)
        self.source_table = source_table
        self.target_table = target_table

    def execute(self, context):
        self.log.info(f"Processing {self.source_table} -> {self.target_table}")

    def get_openlineage_facets_on_complete(self, task_instance):
        from openlineage.client.event_v2 import Dataset
        from airflow.providers.openlineage.extractors import OperatorLineage

        return OperatorLineage(
            inputs=[Dataset(namespace="warehouse://db", name=self.source_table)],
            outputs=[Dataset(namespace="warehouse://db", name=self.target_table)],
        )
```

### Option 2: Set Inlets/Outlets Dynamically

```python
from airflow.models import BaseOperator
from openlineage.client.event_v2 import Dataset

class MyCustomOperator(BaseOperator):
    def __init__(self, source_table: str, target_table: str, **kwargs):
        super().__init__(**kwargs)
        self.source_table = source_table
        self.target_table = target_table

    def execute(self, context):
        self.inlets = [Dataset(namespace="warehouse://db", name=self.source_table)]
        self.outlets = [Dataset(namespace="warehouse://db", name=self.target_table)]
```
