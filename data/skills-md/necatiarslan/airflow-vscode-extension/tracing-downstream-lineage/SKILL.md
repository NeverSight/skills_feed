---
name: tracing-downstream-lineage
description: Trace downstream data lineage and impact analysis. Use when the user asks what depends on this data, what breaks if something changes, downstream dependencies, or needs to assess change risk before modifying a table or DAG.
---

# Downstream Lineage: Impacts

Answer the question: "What breaks if I change this?"

## Impact Analysis

### Step 1: Identify Direct Consumers

For tables:
1. List DAGs using `list_active_dags` and `list_paused_dags`
2. Search DAG source using `get_dag_source_code` for table references

For DAGs:
1. Determine outputs from DAG source
2. Trace consumer DAGs that read those outputs

### Step 2: Build Dependency Tree

Example:

```
SOURCE: fct.orders
    |
    +-- TABLE: agg.daily_sales -> Dashboard: Executive KPIs
    +-- TABLE: ml.order_features -> Model: Forecasting
```

### Step 3: Categorize by Criticality

- Critical: production dashboards, customer-facing apps
- High: internal ops dashboards, downstream ETL
- Medium: ad-hoc analysis
- Low: deprecated or test data

### Step 4: Assess Change Risk

Consider:
- Schema changes
- Data timing changes
- Deletion or deprecation

### Step 5: Find Stakeholders

- DAG owners in DAG definitions
- Dashboard owners in BI tools

## Output: Impact Report

Include:
- Summary of downstream assets
- Impact diagram
- Detailed impacts and owners
- Risk assessment and mitigations

## Related Skills

- tracing-upstream-lineage
- checking-freshness
- debugging-dags
- annotating-task-lineage
- creating-openlineage-extractors
