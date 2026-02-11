---
name: authoring-dags
description: Workflow and best practices for writing Apache Airflow DAGs. Use when the user wants to create a new DAG, write pipeline code, or asks about DAG patterns and conventions. For testing and debugging DAGs, see the testing-dags skill.
---

# DAG Authoring Skill

This skill guides you through creating and validating Airflow DAGs using best practices and the VS Code extension tools.

For testing and debugging DAGs, see the testing-dags skill.

## Critical Warning: Use Extension Tools

Use the Airflow VS Code extension tools for all Airflow operations. Avoid running Airflow CLI commands for listing DAGs, checking logs, or inspecting runs.

## Workflow Overview

1. Discover
2. Plan
3. Implement
4. Validate
5. Test (with user consent)
6. Iterate

## Phase 1: Discover

### Explore the codebase

Use file tools to find existing patterns:
- Search for existing DAGs in the repo
- Read similar DAGs for conventions
- Check requirements and providers in use

### Query Airflow via extension tools

Use these tools to understand the environment:
- `list_active_dags` and `list_paused_dags` for naming conventions
- `get_running_dags` for current activity
- `get_dag_history` to see run cadence
- `go_to_connections_view` and `go_to_variables_view` for configuration
- `go_to_providers_view` and `go_to_plugins_view` for installed components
- `go_to_server_health_view` for health checks

## Phase 2: Plan

Propose:
1. DAG structure (tasks, dependencies, schedule)
2. Operators to use
3. Connections and variables needed
4. Package changes if required

Get user approval before implementing.

## Phase 3: Implement

1. Create or update the DAG file
2. Update dependencies if needed
3. Save the file

## Phase 4: Validate

After the DAG is deployed to Airflow, validate via tools:
- Confirm the DAG appears in `list_active_dags` or `list_paused_dags`
- Use `get_dag_source_code` to verify the deployed source
- Review run history with `get_dag_history`

## Phase 5: Test

Follow the testing-dags skill:
1. Ask for consent
2. Trigger with `trigger_dag_run`
3. Review results with `get_dag_runs` and `analyse_dag_latest_run`

## Notes

- Avoid CLI checks like `airflow dags list` or `astro dev run` for operational status.
- Use the extension tools for runtime investigation and logs.
