---
name: testing-dags
description: Complex DAG testing workflows with debugging and fixing cycles. Use for multi-step testing requests like "test this dag and fix it if it fails", "test and debug", "run the pipeline and troubleshoot issues".
---

# DAG Testing Skill

Use the Airflow VS Code extension tools to test, debug, and fix DAGs in iterative cycles.

## First Action: Trigger the DAG

When the user asks to test a DAG, your first action should be:

- `trigger_dag_run` with the provided DAG ID and config

Do not do pre-flight checks unless the user asks for them.

## Testing Workflow Overview

1. Trigger and monitor
2. If success, summarize
3. If failed, debug
4. Fix and retest

## Phase 1: Trigger and Monitor

1. Trigger: `trigger_dag_run`
2. Monitor:
   - Use `get_dag_runs` to check state
   - If a specific run ID is known, use `get_dag_run_detail`

### Response Interpretation

- Success: summarize duration and outcome
- Failed: move to Phase 2
- Running: ask whether to keep polling

## Phase 2: Debug Failures

1. Use `analyse_dag_latest_run` for a full analysis of the latest run
2. If a specific run ID is known, use `get_dag_run_detail`
3. If task logs are needed, open `go_to_dag_log_view`

## Phase 3: Fix and Retest

1. Apply fixes in the DAG or related systems
2. Re-trigger with `trigger_dag_run`
3. Re-check with `get_dag_runs` or `get_dag_run_detail`

## Notes

- Prefer `analyse_dag_latest_run` for fast triage
- Use `get_dag_history` when comparing across days
