---
name: dagster-expert
description:
  Expert guidance for working with Dagster and the dg CLI. ALWAYS use before doing any task that requires
  knowledge specific to Dagster, or that references assets, materialization, or data pipelines.
  Common tasks may include creating a new project, adding new definitions, understanding the current project structure, answering general questions about the codebase (finding asset, schedule, sensor, component or job definitions), debugging issues, or providing deep information about a specific Dagster concept.
---

# Dagster Expert Skill

Expert guidance for building production-quality Dagster projects. Routes you to detailed reference documentation for assets, automation, project structure, and CLI commands.

> **IMPORTANT**: For new assets, schedules, or sensors, ALWAYS use `dg scaffold` before manual file creation. See [cli/scaffold.md](references/cli/scaffold.md).
>
> **Invoke EARLY**: If the task involves automation conditions, scheduling logic, or integration components (dbt, Fivetran, etc.), invoke this skill or the appropriate sub-skill BEFORE exploring the codebase. The references contain all needed patterns.

## Task Router

| What do you need?                                                   | Reference                                                                                             |
| ------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Create a project                                                    | Quick Reference below (use `uvx create-dagster project`)                                              |
| **Add an asset/schedule/sensor**                                    | **[cli/scaffold.md](references/cli/scaffold.md)** (ALWAYS scaffold first) + pattern docs              |
| Add integration component (dbt, Fivetran, Airbyte, Snowflake, etc.) | **Invoke dagster-integrations skill** (contains scaffolding, YAML schema, adapter requirements)       |
| Complex scheduling / different triggers per dependency              | [automation/declarative-automation/README.md](references/automation/declarative-automation/README.md) |
| Run/materialize assets                                              | [cli/launch.md](references/cli/launch.md)                                                             |
| Select specific assets                                              | [cli/asset-selection.md](references/cli/asset-selection.md)                                           |
| List definitions                                                    | [cli/list.md](references/cli/list.md)                                                                 |
| Validate project                                                    | [cli/check.md](references/cli/check.md)                                                               |
| Understand asset patterns                                           | [assets.md](references/assets.md)                                                                     |
| Understand project layout                                           | [project-structure.md](references/project-structure.md)                                               |
| Set up automation                                                   | [automation/README.md](references/automation/README.md)                                               |
| Debug/get logs                                                      | [cli/api.md](references/cli/api.md)                                                                   |
| Configure env vars                                                  | [env-vars.md](references/env-vars.md)                                                                 |
| Implementation workflow                                             | [implementation-workflow.md](references/implementation-workflow.md)                                   |

## Keyword Router

| Keywords                                                                                                         | Reference                                                                                             |
| ---------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| create project, new project, init, setup                                                                         | Quick Reference below                                                                                 |
| workspace, multi-project, multiple projects                                                                      | Quick Reference below                                                                                 |
| scaffold, generate, create asset/schedule/sensor                                                                 | [cli/scaffold.md](references/cli/scaffold.md)                                                         |
| dbt, fivetran, airbyte, snowflake, bigquery, external tool, integration component, dagster_dbt, dagster_fivetran | **Invoke dagster-integrations skill directly**                                                        |
| complex triggers, different triggers, hot/cold dependencies, conditional automation                              | [automation/declarative-automation/README.md](references/automation/declarative-automation/README.md) |
| automation_condition, AutomationCondition, eager(), any_downstream_conditions                                    | [automation/declarative-automation/README.md](references/automation/declarative-automation/README.md) |
| list, show, find, discover, what assets                                                                          | [cli/list.md](references/cli/list.md)                                                                 |
| validate, check, verify, test config                                                                             | [cli/check.md](references/cli/check.md)                                                               |
| launch, run, materialize, execute, backfill                                                                      | [cli/launch.md](references/cli/launch.md)                                                             |
| select, filter, tag, group, kind, upstream, downstream                                                           | [cli/asset-selection.md](references/cli/asset-selection.md)                                           |
| logs, debug, troubleshoot run                                                                                    | [cli/api.md](references/cli/api.md)                                                                   |
| deploy, plus, cloud                                                                                              | [cli/api.md](references/cli/api.md)                                                                   |
| asset, dependency, metadata, partition                                                                           | [assets.md](references/assets.md)                                                                     |
| schedule, cron, time-based                                                                                       | [automation/schedules.md](references/automation/schedules.md)                                         |
| sensor, event-driven, trigger                                                                                    | [automation/sensors/](references/automation/sensors/)                                                 |
| declarative automation, conditions                                                                               | [automation/declarative-automation/](references/automation/declarative-automation/)                   |
| project structure, code location, definitions                                                                    | [project-structure.md](references/project-structure.md)                                               |
| environment variables, env, config                                                                               | [env-vars.md](references/env-vars.md)                                                                 |

## Quick Reference

```bash
# Project Setup
uvx create-dagster project <name> --uv-sync  # --uv-sync creates venv and installs deps
uvx create-dagster workspace <name>          # For multiple related projects
# Output confirms success—no verification needed

# Scaffold (ALWAYS use for new definitions)
# NOTE: Paths are RELATIVE TO defs/ directory, not project root
dg scaffold defs dagster.asset assets/my_asset.py
dg scaffold defs dagster.schedule schedules/daily.py
dg scaffold defs dagster.sensor sensors/file_watcher.py

# Discover
dg list defs
dg list defs --assets "group:analytics"
dg list components

# Validate
dg check defs

# Launch
dg launch --assets "tag:priority=high"
dg launch --assets "+my_asset"  # with upstream
dg launch --assets my_asset --partition 2024-01-15
```

## Core Dagster Concepts

Brief definitions only (see reference files for detailed examples):

- **Asset**: Persistent object (table, file, model) produced by your pipeline
- **Job**: Selection of assets to execute together
- **Schedule**: Time-based automation using cron
- **Sensor**: Event-driven automation that watches for changes
- **Declarative Automation**: Modern automation where you set conditions on assets
- **Partition**: Logical division of data (by date, category)
- **Component**: Reusable, declarative building block (YAML-based)

## UV Compatibility

Projects use `uv` for dependency management:

```bash
uv run dg list defs
uv run dg launch --assets my_asset
```

## Related Skills

- **dagster-integrations** - Find and configure integration components (dbt, Fivetran, Sling, etc.)
