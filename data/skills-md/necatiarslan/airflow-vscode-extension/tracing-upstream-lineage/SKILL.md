---
name: tracing-upstream-lineage
description: Trace upstream data lineage. Use when the user asks where data comes from, what feeds a table, upstream dependencies, data sources, or needs to understand data origins.
---

# Upstream Lineage: Sources

Trace the origins of data and answer "Where does this data come from?"

## Lineage Investigation

### Step 1: Identify the Target Type

Determine what we are tracing:
- Table
- Column
- DAG

### Step 2: Find the Producing DAG

1. List DAGs: use `list_active_dags` and `list_paused_dags`
2. Read DAG source: use `get_dag_source_code`
3. If a run exists, use `analyse_dag_latest_run` to see tasks and logs

### Step 3: Trace Data Sources

From the DAG code, identify source tables and systems:
- SQL sources in FROM or JOIN clauses
- External sources via operator hooks or connection IDs
- Files in object storage

Use `go_to_connections_view` to inspect connection metadata.

### Step 4: Build the Lineage Chain

Example:

```
TARGET: analytics.orders_daily
    ^
    +-- DAG: etl_daily_orders
            ^
            +-- SOURCE: raw.orders
            |
            +-- SOURCE: dim.customers
```

### Step 5: Check Source Health

- Use `get_dag_runs` or `get_dag_history` on upstream DAGs
- For logs, use `go_to_dag_log_view`

## Lineage for Columns

1. Find the column in the target table schema
2. Search DAG source for references
3. Trace transformations and mappings

## Output: Lineage Report

Include:
- Summary of sources
- Lineage diagram
- Source details (connections, freshness)
- Transformation chain
- Data quality implications

## Related Skills

- checking-freshness
- debugging-dags
- tracing-downstream-lineage
- annotating-task-lineage
- creating-openlineage-extractors
