---
name: dg
description:
  Dagster CLI for project creation, scaffolding components, launching assets, listing definitions,
  viewing logs, and troubleshooting. Use when users want to interact with the dg command-line tool
  for any Dagster operation.
references:
  - create-project
  - create-workspace
  - scaffold
  - launch
  - list
  - logs
  - prototype
  - troubleshoot
---

# Dagster CLI (dg) Skill

This skill helps users interact with the Dagster CLI (`dg`) for all project management, component
scaffolding, asset execution, definition discovery, log retrieval, and troubleshooting operations.

## When to Use This Skill

Auto-invoke when users mention:

- "create a project" / "new dagster project" / "initialize project"
- "create workspace" / "new workspace" / "multi-project setup"
- "scaffold" / "generate" / "create component" / "add asset"
- "launch asset" / "run asset" / "materialize" / "execute"
- "list assets" / "show definitions" / "what assets exist"
- "view logs" / "check logs" / "show run output"
- "prototype" / "implement asset" / "full implementation"
- "troubleshoot" / "debug" / "why did it fail" / "what went wrong"
- Any other `dg` CLI operation

## Workflow Decision Tree

Choose the right `dg` workflow based on what the user needs:

```
What do you need to do?

├─ Setting up a new project?
│  ├─ Single project → /dg create project
│  └─ Multiple projects → /dg create workspace
│
├─ Creating or adding components?
│  ├─ Assets, schedules, sensors → /dg scaffold defs
│  ├─ Integrations (dbt, Fivetran, dlt) → /dg scaffold defs <integration>
│  ├─ Custom inline component → /dg scaffold defs inline-component
│  └─ Reusable component type → /dg scaffold component
│
├─ Running or executing assets?
│  ├─ Single asset → /dg launch --assets <name>
│  ├─ Multiple assets → /dg launch --assets <name1>,<name2>
│  ├─ Assets by tag/group/kind → /dg launch --assets "tag:x" / "group:y" / "kind:z"
│  ├─ Specific partition → /dg launch --assets <name> --partition <key>
│  ├─ Partition range (backfill) → /dg launch --assets <name> --partition-range <start...end>
│  └─ Predefined job → /dg launch --job <name>
│
├─ Discovering what exists?
│  ├─ All definitions → /dg list defs
│  ├─ Available component types → /dg list components
│  ├─ Environment variables → /dg list envs
│  ├─ Projects in workspace → /dg list projects
│  └─ Component tree → /dg list component-tree
│
├─ Viewing logs or output?
│  ├─ Recent runs → /dg logs
│  ├─ Specific run → /dg logs <run_id>
│  ├─ Follow live logs → /dg logs --follow
│  └─ Filter logs → /dg logs --log-level <level>
│
├─ Implementing with full code?
│  ├─ Production-ready asset → /dg prototype
│  ├─ With best practices → /dg prototype + /dagster-best-practices
│  └─ Integration-specific → /dg prototype + /dagster-integrations
│
└─ Debugging or troubleshooting?
   ├─ Failed run analysis → /dg troubleshoot <run_id>
   ├─ Component issues → /dg list defs to verify
   ├─ Environment issues → /dg list envs to check
   └─ Definition loading → /dg check defs
```

## How It Works

When this skill is invoked:

1. **Identify the user's intent** from their natural language request
2. **Map to appropriate `dg` workflow** using the decision tree above
3. **Access relevant reference documentation** from `references/` directory
4. **Provide clear command examples** with copy-pasteable syntax
5. **Explain expected output** and next steps
6. **Cross-reference related workflows** when helpful

## Core Workflows

### Project Creation

Create new Dagster projects or workspaces:

- **Single project**: `dg create project <name>` - For standalone applications
- **Workspace**: `dg create workspace <name>` - For multiple related projects

See [`references/create-project.md`](./references/create-project.md) and
[`references/create-workspace.md`](./references/create-workspace.md) for detailed guidance.

### Component Scaffolding

Generate Dagster components, assets, and integrations:

- **Assets**: `dg scaffold defs dagster.asset <path>`
- **Schedules**: `dg scaffold defs dagster.schedule <name>`
- **Sensors**: `dg scaffold defs dagster.sensor <name>`
- **dbt**: `dg scaffold defs dagster_dbt.DbtProjectComponent <name>`
- **Fivetran**: `dg scaffold defs fivetran.FivetranComponent <name>`
- **dlt**: `dg scaffold defs dagster_dlt.DltResource <name>`
- **Sling**: `dg scaffold defs sling.SlingReplicationComponent <name>`
- **Inline components**: `dg scaffold defs inline-component <path> --typename <Name>`
- **Component types**: `dg scaffold component <name>`

**Discovery-first workflow**: Always use `dg list components` before scaffolding to see available
types.

See [`references/scaffold.md`](./references/scaffold.md) for comprehensive scaffolding
documentation.

### Asset Execution

Launch (materialize) Dagster assets:

- **Single asset**: `dg launch --assets my_asset`
- **Multiple assets**: `dg launch --assets asset1,asset2`
- **All assets**: `dg launch --assets "*"`
- **By tag**: `dg launch --assets "tag:priority=high"`
- **By group**: `dg launch --assets "group:sales"`
- **By kind**: `dg launch --assets "kind:dbt"`
- **With partition**: `dg launch --assets my_asset --partition 2024-01-15`
- **Partition range**: `dg launch --assets my_asset --partition-range "2024-01-01...2024-01-31"`
- **Specific job**: `dg launch --job my_daily_job`

**Environment setup**: Use `.env` files with `uv run dg launch` or
`set -a; source .env; set +a; dg launch`

See [`references/launch.md`](./references/launch.md) for execution details.

### Definition Discovery

Inspect your Dagster project definitions:

- **All definitions**: `dg list defs`
- **As JSON**: `dg list defs --json`
- **Filter assets**: `dg list defs --assets "tag:x"`
- **Component types**: `dg list components`
- **By package**: `dg list components --package dagster_dbt`
- **Environment vars**: `dg list envs`
- **Projects**: `dg list projects` (workspace only)
- **Component tree**: `dg list component-tree`

See [`references/list.md`](./references/list.md) for discovery operations.

### Log Retrieval

View run logs and execution output:

- **Recent runs**: `dg logs`
- **Specific run**: `dg logs <run_id>`
- **Follow live**: `dg logs --follow`
- **Log level filter**: `dg logs --log-level ERROR`
- **Step logs**: `dg logs <run_id> --step <step_name>`
- **Compute logs**: `dg logs <run_id> --compute-logs`

See [`references/logs.md`](./references/logs.md) for log viewing.

### Prototyping

Generate production-ready asset implementations:

- **Guided implementation**: `dg prototype` - Interactive workflow
- **Direct creation**: Implement assets with full logic, not just scaffolds
- **Best practices**: Combine with `/dagster-best-practices` for patterns

See [`references/prototype.md`](./references/prototype.md) for implementation guidance.

### Troubleshooting

Debug failed runs and issues:

- **Analyze failure**: `dg troubleshoot <run_id>`
- **Recent failures**: `dg troubleshoot` (analyzes most recent)
- **Failure patterns**: Identifies common issues and solutions
- **Component validation**: `dg check defs`

See [`references/troubleshoot.md`](./references/troubleshoot.md) for debugging.

## When to Use This Skill vs. Others

| User Need                         | Use This Skill (/dg)                | Alternative Skill         |
| --------------------------------- | ----------------------------------- | ------------------------- |
| "create an asset"                 | ✅ Yes - `/dg` → scaffold reference |                           |
| "launch my assets"                | ✅ Yes - `/dg` → launch reference   |                           |
| "list definitions"                | ✅ Yes - `/dg` → list reference     |                           |
| "best practices for assets"       | ❌ No                               | `/dagster-best-practices` |
| "which integration to use"        | ❌ No                               | `/dagster-integrations`   |
| "Python code standards"           | ❌ No                               | `/dignified-python`       |
| "create project + best practices" | ✅ Yes, then cross-reference        | `/dagster-best-practices` |
| "scaffold dbt + learn patterns"   | ✅ Yes, then cross-reference        | `/dagster-integrations`   |

## Cross-Skill References

### Use `/dagster-best-practices` for:

- Deciding how to structure assets
- Choosing automation patterns (schedules vs sensors vs automation conditions)
- Understanding when to use resources
- Learning testing strategies
- ETL pattern guidance
- Project architecture decisions

### Use `/dagster-integrations` for:

- Discovering available integration libraries
- Understanding integration-specific patterns
- Choosing between similar integrations
- Learning integration best practices

### Use `/dignified-python` for:

- Python type annotation standards
- Exception handling patterns
- CLI implementation guidelines
- Pathlib best practices
- Modern Python syntax (3.10-3.13)

## Common Usage Patterns

### New Project Setup

```bash
# 1. Create project
dg create project my_analytics

cd my_analytics

# 2. List available components
dg list components --package dagster_dbt
dg list components --package fivetran

# 3. Scaffold integrations
dg scaffold defs dagster_dbt.DbtProjectComponent dbt_project
dg scaffold defs fivetran.FivetranComponent salesforce --json-params '{...}'

# 4. Scaffold downstream assets
dg scaffold defs dagster.asset analytics/revenue --format python

# 5. Scaffold automation
dg scaffold defs dagster.schedule daily_refresh --format python

# 6. Verify structure
dg list defs

# 7. Test execution
dg launch --assets revenue
```

### Development Workflow

```bash
# 1. Check what exists
dg list defs

# 2. Scaffold new asset
dg scaffold defs dagster.asset sales/customers --format python

# 3. Edit the asset (implement logic)
vim defs/sales/customers/defs.py

# 4. Verify it loads
dg list defs

# 5. Test execution
dg launch --assets customers

# 6. View logs if needed
dg logs --follow

# 7. Debug if failed
dg troubleshoot
```

### Discovery Workflow

```bash
# 1. What assets exist?
dg list defs

# 2. What component types can I scaffold?
dg list components

# 3. Are my environment variables set?
dg list envs

# 4. What's the project structure?
dg list component-tree
```

## Implementation Notes

- This skill delegates to comprehensive reference documentation in `references/`
- All `dg` CLI operations are covered (create, scaffold, launch, list, logs, prototype,
  troubleshoot)
- **Dynamic command generation**: Some subcommands (like `scaffold defs`) are dynamically generated
  based on installed packages
- Always encourage **discovery-first workflows**: `dg list components` before `dg scaffold`
- Provide **working examples** with realistic parameters
- Guide users through **interactive disambiguation** when component names are ambiguous
- Cross-reference other skills (`/dagster-best-practices`, `/dagster-integrations`) when
  architectural guidance is needed

## Reference Documentation

Full detailed documentation for each workflow:

- [`create-project.md`](./references/create-project.md) - Creating new Dagster projects
- [`create-workspace.md`](./references/create-workspace.md) - Creating multi-project workspaces
- [`scaffold.md`](./references/scaffold.md) - Scaffolding components, assets, and integrations
- [`launch.md`](./references/launch.md) - Materializing assets and executing jobs
- [`list.md`](./references/list.md) - Discovering definitions and components
- [`logs.md`](./references/logs.md) - Viewing run logs and output
- [`prototype.md`](./references/prototype.md) - Implementing production-ready assets
- [`troubleshoot.md`](./references/troubleshoot.md) - Debugging failed runs and issues

## See Also

- **Architectural guidance**: `/dagster-best-practices` - Learn patterns for assets, automation,
  testing, project structure
- **Integration discovery**: `/dagster-integrations` - Find and understand integration libraries
- **Python standards**: `/dignified-python` - Production Python code quality patterns
