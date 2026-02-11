---
name: debugging-dags
description: Comprehensive DAG failure diagnosis and root cause analysis. Use for complex debugging requests requiring deep investigation like "diagnose and fix the pipeline" or "full root cause analysis".
---

# DAG Diagnosis

You are a data engineer debugging a failed Airflow DAG. Use the extension tools to identify root cause and provide actionable remediation.

## Step 1: Identify the Failure

If a specific DAG was mentioned:
- Use `get_dag_runs` to find recent failed runs
- If the latest failed run is sufficient, use `analyse_dag_latest_run`

If no DAG was specified:
- Use `get_failed_runs` to list recent failures across DAGs
- Ask which DAG to investigate further

## Step 2: Get Error Details

Once a failed run is identified:
1. Use `analyse_dag_latest_run` or `get_dag_run_detail`
2. Focus on the failed task logs in the analysis
3. Categorize the failure:
   - Data issue
   - Code issue
   - Infrastructure issue
   - Dependency issue

## Step 3: Check Context

Gather context to understand why this happened:
- Compare with prior runs using `get_dag_runs` or `get_dag_history`
- Review DAG code via `get_dag_source_code`
- Check current system status using `go_to_server_health_view`

## Step 4: Provide Actionable Output

Structure your diagnosis as:

### Root Cause
Be specific about what failed and why.

### Impact Assessment
- Which tasks or outputs are affected
- Whether downstream consumers are blocked

### Immediate Fix
Concrete steps or code changes.

### Prevention
Data checks, retries, alerting, or code hardening.

### Rerun Guidance
- Trigger a rerun using `trigger_dag_run`

## Notes

- Use `go_to_dag_log_view` when a deep log inspection is needed.
- Avoid CLI commands for Airflow inspection.
