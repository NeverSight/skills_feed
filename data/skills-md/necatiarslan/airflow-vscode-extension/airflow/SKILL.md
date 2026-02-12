---
name: airflow
description: Manages Apache Airflow operations including listing, running, and debugging DAGs, viewing logs, and checking server status using the VS Code extension tools.
---

# Airflow Operations

Use the Airflow VS Code extension tools for all Airflow interactions. Avoid shell commands for Airflow operations.

## Tool Quick Reference

| Tool | Purpose |
| --- | --- |
| `list_active_dags` | List active (unpaused) DAGs |
| `list_paused_dags` | List paused DAGs |
| `get_running_dags` | Show running or queued DAG runs |
| `pause_dag` | Pause a DAG |
| `unpause_dag` | Unpause a DAG |
| `trigger_dag_run` | Trigger a DAG run |
| `get_dag_runs` | List DAG runs for a DAG |
| `get_dag_history` | Daily run history for a DAG |
| `get_failed_runs` | Failed runs across DAGs |
| `analyse_dag_latest_run` | Full analysis of latest run (tasks, logs, source) |
| `get_dag_run_detail` | Full analysis of a specific run |
| `get_dag_source_code` | Retrieve DAG source code |
| `go_to_dag_view` | Open DAG view panel |
| `go_to_dag_log_view` | Open log view panel |
| `go_to_connections_view` | Open connections panel |
| `go_to_variables_view` | Open variables panel |
| `go_to_providers_view` | Open providers panel |
| `go_to_configs_view` | Open configs panel |
| `go_to_plugins_view` | Open plugins panel |
| `go_to_server_health_view` | Open server health panel |

## User Intent Patterns

### DAG Operations
- "List all DAGs" -> `list_active_dags` and `list_paused_dags`
- "Show DAG source" -> `get_dag_source_code`
- "Pause DAG X" -> `pause_dag`
- "Resume DAG X" -> `unpause_dag`

### Run Operations
- "Trigger DAG X" -> `trigger_dag_run`
- "Show recent runs" -> `get_dag_runs`
- "Why did this fail?" -> `analyse_dag_latest_run` or `get_dag_run_detail`

### Logs and Troubleshooting
- "Show logs for task" -> `go_to_dag_log_view` or `analyse_dag_latest_run`
- "Analyze latest run" -> `analyse_dag_latest_run`

### System and Config
- "Show connections" -> `go_to_connections_view`
- "Show variables" -> `go_to_variables_view`
- "Check server health" -> `go_to_server_health_view`

## Common Workflows

### Investigate a Failed Run
1. Find failures: `get_failed_runs`
2. Analyze latest run: `analyse_dag_latest_run`
3. If a specific run ID is known: `get_dag_run_detail`
4. Open logs if needed: `go_to_dag_log_view`

### Trigger and Monitor
1. Trigger: `trigger_dag_run`
2. Check status: `get_dag_runs`
3. Analyze if failed: `analyse_dag_latest_run`

### Morning Health Check
1. Check server health: `go_to_server_health_view`
2. Check running DAGs: `get_running_dags`
3. Review recent failures: `get_failed_runs`
