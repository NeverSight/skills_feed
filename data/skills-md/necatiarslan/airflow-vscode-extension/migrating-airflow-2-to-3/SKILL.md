---
name: migrating-airflow-2-to-3
description: Guide for migrating Apache Airflow 2.x projects to Airflow 3.x. Use when the user mentions Airflow 3 migration, upgrade, compatibility issues, breaking changes, or wants to modernize their Airflow codebase.
---

# Airflow 2 to 3 Migration

This skill helps migrate Airflow 2.x DAG code to Airflow 3.x, focusing on code changes (imports, operators, hooks, context, API usage).

Important: Before migrating to Airflow 3, strongly recommend upgrading to Airflow 2.11 first, then to at least Airflow 3.0.11 (ideally 3.1).

## Migration at a Glance

1. Run Ruff Airflow migration rules:
   - `ruff check --preview --select AIR --fix --unsafe-fixes .`
2. Scan for remaining issues using a manual checklist:
   - Direct metadata DB access
   - Legacy imports
   - Scheduling and context changes
   - XCom pickling
   - Datasets to assets
   - REST API and auth
   - Plugins and file paths
3. Plan changes per file and issue type
4. Implement changes incrementally and re-run Ruff
5. Explain changes and advise testing

## Architecture and Metadata DB Access

Airflow 3 changes how components talk to the metadata database:
- Workers no longer connect directly to the metadata DB
- Task code runs via the Task Execution API
- The DAG processor is separate from the scheduler

Direct ORM access now fails with:

```
RuntimeError: Direct database access via the ORM is not allowed in Airflow 3.x
```

### Patterns to search for

- `provide_session`, `create_session`, `@provide_session`
- `from airflow.settings import Session`
- `from airflow.settings import engine`
- ORM usage with models: `session.query(DagModel)...`

### Replacement: Airflow Python client

Add to requirements.txt:

```
apache-airflow-client==<your-airflow-runtime-version>
```

Example:

```python
import os
import airflow_client.client
from airflow_client.client.api.dag_api import DAGApi

_HOST = os.getenv("AIRFLOW__API__BASE_URL", "https://<your-org>.astronomer.run/<deployment>/")
_TOKEN = os.getenv("DEPLOYMENT_API_TOKEN")

config = airflow_client.client.Configuration(host=_HOST, access_token=_TOKEN)
with airflow_client.client.ApiClient(config) as api_client:
    dag_api = DAGApi(api_client)
    dags = dag_api.get_dags(limit=10)
```

## Ruff Airflow Migration Rules

- AIR30 / AIR301 / AIR302: removed code and imports
- AIR31 / AIR311 / AIR312: deprecated code and imports

Commands:

```bash
ruff check --preview --select AIR --fix --unsafe-fixes .
ruff check --preview --select AIR .
```

## Key Import Changes

| Airflow 2.x | Airflow 3 |
| --- | --- |
| airflow.operators.dummy_operator.DummyOperator | airflow.providers.standard.operators.empty.EmptyOperator |
| airflow.operators.bash.BashOperator | airflow.providers.standard.operators.bash.BashOperator |
| airflow.operators.python.PythonOperator | airflow.providers.standard.operators.python.PythonOperator |
| airflow.decorators.dag | airflow.sdk.dag |
| airflow.decorators.task | airflow.sdk.task |
| airflow.datasets.Dataset | airflow.sdk.Asset |

## Context Key Changes

| Removed Key | Replacement |
| --- | --- |
| execution_date | context["dag_run"].logical_date |
| tomorrow_ds / yesterday_ds | use macros.ds_add |
| triggering_dataset_events | triggering_asset_events |
| templates_dict | context["params"] |

## Default Behavior Changes

| Setting | Airflow 2 Default | Airflow 3 Default |
| --- | --- | --- |
| schedule | timedelta(days=1) | None |
| catchup | True | False |

## Resources

- https://www.astronomer.io/docs/astro/airflow3/upgrade-af3
- https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html
