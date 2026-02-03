---
name: dagster-best-practices
description:
  Expert guidance for Dagster data orchestration including assets, resources, automation, testing,
  ETL patterns, and project structure. Use when deciding how to structure projects, choosing
  automation methods, designing assets, or understanding Dagster patterns and best practices.
references:
  - assets
  - automation
  - etl-patterns
  - project-structure
  - resources
  - testing
---

# Dagster Best Practices Skill

Expert guidance for building production-quality Dagster projects with recommended patterns and
architectural decisions.

## When to Use This Skill

Auto-invoke when users ask about:

- "what's the best way to..." / "how should I..." / "recommended approach for..."
- "how do I structure assets" / "asset design patterns"
- "choosing automation" / "schedules vs sensors" / "automation conditions"
- "resource patterns" / "managing resources" / "dependency injection"
- "testing strategies" / "how to test assets"
- "ETL patterns" / "data pipeline patterns"
- "project structure" / "organizing code" / "components vs definitions"
- "dbt integration patterns"
- "partition strategies"
- Any architectural or design question about Dagster

## Architecture Decision Tree

Choose the right Dagster pattern based on what you're building:

```
What do you need guidance on?

├─ Structuring assets?
│  ├─ Basic asset design → references/assets.md#basic-patterns
│  ├─ Asset dependencies → references/assets.md#dependencies
│  ├─ Partitioned assets → references/assets.md#partitions
│  ├─ Multi-assets → references/assets.md#multi-assets
│  ├─ Asset groups → references/assets.md#organization
│  └─ Asset metadata → references/assets.md#metadata
│
├─ Choosing automation?
│  ├─ Modern approach → references/automation.md#declarative-automation (recommended)
│  ├─ Time-based → references/automation.md#schedules
│  ├─ Event-driven → references/automation.md#sensors
│  ├─ Partition automation → references/automation.md#partition-automation
│  └─ Backfills → references/automation.md#backfills
│
├─ Managing resources?
│  ├─ Database connections → references/resources.md#database-resources
│  ├─ API clients → references/resources.md#api-resources
│  ├─ Environment config → references/resources.md#environment-variables
│  ├─ Resource dependencies → references/resources.md#dependencies
│  └─ Testing with resources → references/resources.md#testing
│
├─ Testing strategies?
│  ├─ Unit testing assets → references/testing.md#unit-tests
│  ├─ Integration tests → references/testing.md#integration-tests
│  ├─ Asset checks → references/testing.md#asset-checks
│  ├─ Testing with resources → references/testing.md#mock-resources
│  └─ Test fixtures → references/testing.md#fixtures
│
├─ ETL patterns?
│  ├─ dbt integration → references/etl-patterns.md#dbt
│  ├─ dlt pipelines → references/etl-patterns.md#dlt
│  ├─ Sling replication → references/etl-patterns.md#sling
│  ├─ Extract-Load-Transform → references/etl-patterns.md#elt
│  └─ Data quality → references/etl-patterns.md#quality
│
└─ Project structure?
   ├─ Single project → references/project-structure.md#single-project
   ├─ Workspace (multi-project) → references/project-structure.md#workspaces
   ├─ Components vs definitions → references/project-structure.md#components
   ├─ Code locations → references/project-structure.md#code-locations
   └─ Directory conventions → references/project-structure.md#conventions
```

## When to Use This Skill vs. Others

| User Need                        | Use This Skill                               | Alternative Skill       |
| -------------------------------- | -------------------------------------------- | ----------------------- |
| "what's the best way to X"       | ✅ Yes - architectural guidance              |                         |
| "how do I structure assets"      | ✅ Yes - asset design patterns               |                         |
| "which integration should I use" | ❌ No                                        | `/dagster-integrations` |
| "create an asset"                | ❌ No                                        | `/dg` for scaffolding   |
| "launch my assets"               | ❌ No                                        | `/dg` for execution     |
| "Python code standards"          | ❌ No                                        | `/dignified-python`     |
| "how do I test assets"           | ✅ Yes - testing strategies                  |                         |
| "schedule patterns"              | ✅ Yes - automation guidance                 |                         |
| "dbt best practices"             | ✅ Yes - dbt patterns                        |                         |
| "implement X pipeline"           | ❌ First learn patterns here, then use `/dg` |                         |

## Core Philosophy

**Think in Assets**: Dagster is built around the asset abstraction—persistent objects like tables,
files, or models that your pipeline produces. Assets provide:

- **Clear Lineage**: Explicit dependencies define data flow
- **Better Observability**: Track what data exists and how it was created
- **Improved Testability**: Assets are just Python functions that can be tested directly
- **Declarative Pipelines**: Focus on _what_ to produce, not _how_ to execute

**Assets over Ops**: For most data pipelines, prefer assets over ops. Use ops only when the asset
abstraction doesn't fit (non-data workflows, complex execution patterns).

**Environment Separation**: Use resources and `EnvVar` to maintain separate configurations for dev,
staging, and production without code changes.

---

## Quick Reference

| If you're writing...                   | Check this section/reference                                                                    |
| -------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `@dg.asset`                            | [Assets](#assets-quick-reference) or `references/assets.md`                                     |
| `ConfigurableResource`                 | [Resources](#resources-quick-reference) or `references/resources.md`                            |
| `AutomationCondition`                  | [Declarative Automation](#declarative-automation-quick-reference) or `references/automation.md` |
| `@dg.schedule` or `ScheduleDefinition` | [Automation](#automation-quick-reference) or `references/automation.md`                         |
| `@dg.sensor`                           | [Sensors](#sensors-quick-reference) or `references/automation.md`                               |
| `PartitionsDefinition`                 | [Partitions](#partitions-quick-reference) or `references/automation.md`                         |
| Tests with `dg.materialize()`          | [Testing](#testing-quick-reference) or `references/testing.md`                                  |
| `@asset_check`                         | `references/testing.md#asset-checks`                                                            |
| `@dlt_assets` or `@sling_assets`       | `references/etl-patterns.md`                                                                    |
| `@dbt_assets`                          | [dbt Integration](#dbt-integration) or `dbt-development` skill                                  |
| `Definitions` or code locations        | `references/project-structure.md`                                                               |
| Components (`defs.yaml`)               | `references/project-structure.md#components`                                                    |

---

## Core Concepts

**Asset**: A persistent object (table, file, model) that your pipeline produces. Define with
`@dg.asset`.

**Resource**: External services/tools (databases, APIs) shared across assets. Define with
`ConfigurableResource`.

**Job**: A selection of assets to execute together. Create with `dg.define_asset_job()`.

**Schedule**: Time-based automation for jobs. Create with `dg.ScheduleDefinition`.

**Sensor**: Event-driven automation that watches for changes. Define with `@dg.sensor`.

**Partition**: Logical divisions of data (by date, category). Define with `PartitionsDefinition`.

**Definitions**: The container for all Dagster objects in a code location.

**Component**: Reusable, declarative building blocks that generate `Definitions` from configuration
(YAML). Use for standardized patterns.

**Declarative Automation**: Modern automation framework where you set conditions on assets rather
than scheduling jobs.

---

## Assets Quick Reference

### Basic Asset

```python
import dagster as dg

@dg.asset
def my_asset() -> None:
    """Asset description appears in the UI."""
    # Your computation logic here
    pass
```

### Asset with Dependencies

```python
@dg.asset
def downstream_asset(upstream_asset) -> dict:
    """Depends on upstream_asset by naming it as a parameter."""
    return {"processed": upstream_asset}
```

### Asset with Metadata

```python
@dg.asset(
    group_name="analytics",
    key_prefix=["warehouse", "staging"],
    description="Cleaned customer data",
    owners=["team:data-engineering", "alice@example.com"],
    tags={"priority": "high", "domain": "sales"},
    code_version="1.2.0",
)
def customers() -> None:
    pass
```

**Best Practices**:

- **Naming**: Use nouns describing what is produced (`customers`, `daily_revenue`), not verbs
  (`load_customers`)
- **Tags**: Primary mechanism for organization (use liberally)
- **Owners**: Specify team or individual owners for accountability
- **code_version**: Track when asset logic changes for lineage

---

## Resources Quick Reference

### Define a Resource

```python
from dagster import ConfigurableResource

class DatabaseResource(ConfigurableResource):
    connection_string: str

    def query(self, sql: str) -> list:
        # Implementation here
        pass
```

### Use in Assets

```python
@dg.asset
def my_asset(database: DatabaseResource) -> None:
    results = database.query("SELECT * FROM table")
```

### Register in Definitions

```python
dg.Definitions(
    assets=[my_asset],
    resources={"database": DatabaseResource(connection_string="...")},
)
```

---

## Automation Quick Reference

### Schedule

```python
import dagster as dg
from my_project.defs.jobs import my_job

my_schedule = dg.ScheduleDefinition(
    job=my_job,
    cron_schedule="0 0 * * *",  # Daily at midnight
)
```

### Common Cron Patterns

| Pattern     | Meaning            |
| ----------- | ------------------ |
| `0 * * * *` | Every hour         |
| `0 0 * * *` | Daily at midnight  |
| `0 0 * * 1` | Weekly on Monday   |
| `0 0 1 * *` | Monthly on the 1st |
| `0 0 5 * *` | Monthly on the 5th |

---

## Declarative Automation Quick Reference

**Modern automation pattern**: Set conditions on assets instead of scheduling jobs.

### AutomationCondition Examples

```python
from dagster import AutomationCondition

# Update when upstream data changes
@dg.asset(
    automation_condition=AutomationCondition.on_missing()
)
def my_asset() -> None:
    pass

# Update daily at a specific time
@dg.asset(
    automation_condition=AutomationCondition.on_cron("0 9 * * *")
)
def daily_report() -> None:
    pass

# Combine conditions
@dg.asset(
    automation_condition=(
        AutomationCondition.on_missing()
        | AutomationCondition.on_cron("0 0 * * *")
    )
)
def flexible_asset() -> None:
    pass
```

**Benefits over Schedules**:

- More expressive condition logic
- Asset-native (no separate job definitions needed)
- Automatic dependency-aware execution
- Better for complex automation scenarios

**When to Use**:

- Asset-centric pipelines with complex update logic
- Condition-based triggers (data availability, freshness)
- Prefer over schedules for new projects

---

## Sensors Quick Reference

### Basic Sensor Pattern

```python
@dg.sensor(job=my_job)
def my_sensor(context: dg.SensorEvaluationContext):
    # 1. Read cursor (previous state)
    previous_state = json.loads(context.cursor) if context.cursor else {}
    current_state = {}
    runs_to_request = []

    # 2. Check for changes
    for item in get_items_to_check():
        current_state[item.id] = item.modified_at
        if item.id not in previous_state or previous_state[item.id] != item.modified_at:
            runs_to_request.append(dg.RunRequest(
                run_key=f"run_{item.id}_{item.modified_at}",
                run_config={...}
            ))

    # 3. Return result with updated cursor
    return dg.SensorResult(
        run_requests=runs_to_request,
        cursor=json.dumps(current_state)
    )
```

**Key**: Use cursors to track state between sensor evaluations.

---

## Partitions Quick Reference

### Time-Based Partition

```python
weekly_partition = dg.WeeklyPartitionsDefinition(start_date="2023-01-01")

@dg.asset(partitions_def=weekly_partition)
def weekly_data(context: dg.AssetExecutionContext) -> None:
    partition_key = context.partition_key  # e.g., "2023-01-01"
    # Process data for this partition
```

### Static Partition

```python
region_partition = dg.StaticPartitionsDefinition(["us-east", "us-west", "eu"])

@dg.asset(partitions_def=region_partition)
def regional_data(context: dg.AssetExecutionContext) -> None:
    region = context.partition_key
```

### Partition Types

| Type                          | Use Case                              |
| ----------------------------- | ------------------------------------- |
| `DailyPartitionsDefinition`   | One partition per day                 |
| `WeeklyPartitionsDefinition`  | One partition per week                |
| `MonthlyPartitionsDefinition` | One partition per month               |
| `HourlyPartitionsDefinition`  | One partition per hour                |
| `StaticPartitionsDefinition`  | Fixed set of partitions               |
| `DynamicPartitionsDefinition` | Partitions created at runtime         |
| `MultiPartitionsDefinition`   | Combine multiple partition dimensions |

**Best Practice**: Limit partitions to **100,000 or fewer per asset** for optimal UI performance.

---

## Testing Quick Reference

### Direct Function Testing

```python
def test_my_asset():
    result = my_asset()
    assert result == expected_value
```

### Testing with Materialization

```python
def test_asset_graph():
    result = dg.materialize(
        assets=[asset_a, asset_b],
        resources={"database": mock_database},
    )
    assert result.success
    assert result.output_for_node("asset_b") == expected
```

### Mocking Resources

```python
from unittest.mock import Mock

def test_with_mocked_resource():
    mocked_resource = Mock()
    mocked_resource.query.return_value = [{"id": 1}]

    result = dg.materialize(
        assets=[my_asset],
        resources={"database": mocked_resource},
    )
    assert result.success
```

### Asset Checks

```python
@dg.asset_check(asset=my_asset)
def validate_non_empty(my_asset):
    return dg.AssetCheckResult(
        passed=len(my_asset) > 0,
        metadata={"row_count": len(my_asset)},
    )
```

---

## dbt Integration

For dbt integration, **prefer the component-based approach** for standard dbt projects. Use Pythonic
assets only when you need custom logic or fine-grained control.

### Component-Based dbt (Recommended)

Use `DbtProjectComponent` with remote Git repository:

```yaml
# defs/transform/defs.yaml
type: dagster_dbt.DbtProjectComponent

attributes:
  project:
    repo_url: https://github.com/dagster-io/jaffle-platform.git
    repo_relative_path: jdbt
  dbt:
    target: dev
```

**When to use**:

- Standard dbt transformations
- Remote dbt project in Git repository
- Declarative configuration preferred
- Component reusability desired

**For private repositories**:

```yaml
attributes:
  project:
    repo_url: https://github.com/your-org/dbt-project.git
    repo_relative_path: dbt
    token: "{{ env.GIT_TOKEN }}"
  dbt:
    target: dev
```

### Pythonic dbt Assets

For custom logic or local development:

```python
from dagster_dbt import DbtCliResource, dbt_assets
from pathlib import Path

dbt_project_dir = Path(__file__).parent / "dbt_project"

@dbt_assets(manifest=dbt_project_dir / "target" / "manifest.json")
def my_dbt_assets(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()

dg.Definitions(
    assets=[my_dbt_assets],
    resources={"dbt": DbtCliResource(project_dir=dbt_project_dir)},
)
```

**When to use**:

- Custom transformation logic needed
- Local development with frequent dbt code changes
- Fine-grained control over dbt execution

**Full patterns**: See [Dagster dbt docs](https://docs.dagster.io/integrations/libraries/dbt)

---

## When to Load References

### Load `references/assets.md` when:

- Defining complex asset dependencies
- Adding metadata, groups, or key prefixes
- Working with asset factories
- Understanding asset materialization patterns

### Load `references/resources.md` when:

- Creating custom `ConfigurableResource` classes
- Integrating with databases, APIs, or cloud services
- Understanding resource scoping and lifecycle

### Load `references/automation.md` when:

- Creating schedules with complex cron patterns
- Building sensors with cursors and state management
- Implementing partitions and backfills
- Using declarative automation conditions
- Automating dbt or other integration runs

### Load `references/testing.md` when:

- Writing unit tests for assets
- Mocking resources and dependencies
- Using `dg.materialize()` for integration tests
- Creating asset checks for data validation

### Load `references/etl-patterns.md` when:

- Using dlt for embedded ETL
- Using Sling for database replication
- Loading data from files or APIs
- Integrating external ETL tools

### Load `references/project-structure.md` when:

- Setting up a new Dagster project
- Configuring `Definitions` and code locations
- Using `dg` CLI for scaffolding
- Organizing large projects with Components

---

## Project Structure

### Recommended Layout

```
my_project/
├── pyproject.toml
├── src/
│   └── my_project/
│       ├── definitions.py     # Main Definitions
│       └── defs/
│           ├── assets/
│           │   ├── __init__.py
│           │   └── my_assets.py
│           ├── jobs.py
│           ├── schedules.py
│           ├── sensors.py
│           └── resources.py
└── tests/
    └── test_assets.py
```

### Definitions Pattern (Modern)

**Auto-Discovery (Simplest)**:

```python
# src/my_project/definitions.py
from dagster import Definitions
from dagster_dg import load_defs

# Automatically discovers all definitions in defs/ folder
defs = Definitions.merge(
    load_defs()
)
```

**Combining Components with Pythonic Assets**:

```python
# src/my_project/definitions.py
from dagster import Definitions
from dagster_dg import load_defs
from my_project.assets import custom_assets

# Load component definitions from defs/ folder
component_defs = load_defs()

# Define pythonic assets separately
pythonic_defs = Definitions(
    assets=custom_assets,
    resources={...}
)

# Merge them together
defs = Definitions.merge(component_defs, pythonic_defs)
```

**Traditional (Explicit)**:

```python
# src/my_project/definitions.py
from dagster import Definitions
from my_project.defs import assets, jobs, schedules, resources

defs = Definitions(
    assets=assets,
    jobs=jobs,
    schedules=schedules,
    resources=resources,
)
```

### Scaffolding with dg CLI

```bash
# Create new project
uvx create-dagster my_project

# Scaffold new asset file
dg scaffold defs dagster.asset assets/new_asset.py

# Scaffold schedule
dg scaffold defs dagster.schedule schedules.py

# Scaffold sensor
dg scaffold defs dagster.sensor sensors.py

# Validate definitions
dg check defs
```

---

## Common Patterns

### Job Definition

```python
trip_update_job = dg.define_asset_job(
    name="trip_update_job",
    selection=["taxi_trips", "taxi_zones"],
)
```

### Run Configuration

```python
from dagster import Config

class MyAssetConfig(Config):
    filename: str
    limit: int = 100

@dg.asset
def configurable_asset(config: MyAssetConfig) -> None:
    print(f"Processing {config.filename} with limit {config.limit}")
```

### Asset Dependencies with External Sources

```python
@dg.asset(deps=["external_table"])
def derived_asset() -> None:
    """Depends on external_table which isn't managed by Dagster."""
    pass
```

---

## Anti-Patterns to Avoid

| Anti-Pattern                         | Better Approach                           |
| ------------------------------------ | ----------------------------------------- |
| Hardcoding credentials in assets     | Use `ConfigurableResource` with env vars  |
| Giant assets that do everything      | Split into focused, composable assets     |
| Ignoring asset return types          | Use type annotations for clarity          |
| Skipping tests for assets            | Test assets like regular Python functions |
| Not using partitions for time-series | Use `DailyPartitionsDefinition` etc.      |
| Putting all assets in one file       | Organize by domain in separate modules    |

---

## CLI Quick Reference

### dg CLI (Recommended for Modern Projects)

```bash
# Development
dg dev                          # Start Dagster UI (port 3000)
dg check defs                   # Validate definitions load correctly
dg list defs                    # Show all loaded definitions
dg list components              # Show available components

# Scaffolding
dg scaffold defs dagster.asset assets/file.py
dg scaffold defs dagster.schedule schedules.py
dg scaffold defs dagster.sensor sensors.py
dg scaffold defs dagster.resources resources.py

# Execution
dg launch --assets my_asset                    # Materialize specific asset
dg launch --assets asset1 asset2               # Multiple assets
dg launch --assets "*"                         # Materialize all assets
dg launch --assets "tag:priority=high"         # Assets by tag
dg launch --assets "group:sales_analytics"     # Assets by group
dg launch --assets "kind:dbt"                  # Assets by kind
dg launch --job my_job                         # Execute a job

# Partitions
dg launch --assets my_asset --partition 2024-01-15              # Single partition
dg launch --assets my_asset --partition-range "2024-01-01...2024-01-31"  # Backfill range

# Configuration
dg launch --assets my_asset --config-json '{"ops": {"my_asset": {"config": {"param": "value"}}}}'

# Environment Variables
uv run dg launch --assets my_asset             # Auto-loads .env with uv
set -a; source .env; set +a; dg launch --assets my_asset  # Manual .env loading

# See /dg:launch command for comprehensive launch documentation
```

### dagster CLI (Legacy/General Purpose)

```bash
# Use for non-dg projects or advanced scenarios
dagster dev                     # Start Dagster UI
dagster job execute -j my_job   # Execute a job
dagster asset materialize -a my_asset  # Materialize an asset
```

**Use `dg` CLI for projects created with `create-dagster`**. It provides auto-discovery,
scaffolding, and modern workflow support.

---

## References

- **Assets**: `references/assets.md` - Detailed asset patterns and launching guidance
- **Resources**: `references/resources.md` - Resource configuration
- **Automation**: `references/automation.md` - Schedules, sensors, partitions
- **Testing**: `references/testing.md` - Testing patterns and asset checks
- **ETL Patterns**: `references/etl-patterns.md` - dlt, Sling, file/API ingestion
- **Project Structure**: `references/project-structure.md` - Definitions, Components
- **Launch Command**: `/dg:launch` - Comprehensive asset launching documentation
- **Official Docs**: https://docs.dagster.io
- **API Reference**: https://docs.dagster.io/api/dagster
