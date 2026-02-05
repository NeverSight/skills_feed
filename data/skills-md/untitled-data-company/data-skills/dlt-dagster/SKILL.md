---
name: dlt-dagster
description: >
  Runs dlt pipelines in Dagster as software-defined assets (Component or Pythonic @dlt_assets)
  or as a single standard Dagster asset. Use when orchestrating dlt with Dagster; scaffolding
  loads.py/defs.yaml; jobs/schedules; secrets/env; incremental/backfill via apply_hints;
  parallelization (one asset per resource); Dagster Cloud deployment; or external compute
  (ECS, Fargate — refer to dagster-integrations). Triggers: dagster-dlt, dlt on Dagster,
  deploy dlt with Dagster, standard Dagster asset, external compute.
---

# dlt on Dagster

Clarify how the user wants to run dlt (asset type and compute); then follow the Core Workflow or refer to dagster-integrations for external compute.

**Quick start:** 1) Ask: dlt assets (recommended) vs standard Dagster asset? Run on Dagster compute vs external (ECS, Fargate, etc.)? 2) Follow the Core Workflow or refer to dagster-integrations. 3) Use references as needed.

## Integration Approach Decision Tree

```
START: User wants to build/run a dlt pipeline with Dagster
│
├─→ Run on external compute (ECS, Fargate, or other engine)?
│   Schedule in Dagster, execution elsewhere.
│   │
│   YES → Use the dagster-integrations skill (see "Related skill: dagster-integrations" below).
│         Do not use dlt_assets / Component from this skill for execution.
│   │
│   NO → Run on Dagster compute. Continue:
│   │
├─→ dlt assets (recommended) or standard Dagster asset?
│   │
│   dlt assets (recommended) → Each dlt resource = Dagster asset; selective runs, parallelization.
│   │   Then: Component (defs.yaml + loads.py) or Pythonic (@dlt_assets in code)?
│   │
│   standard Dagster asset → Single asset wrapping the whole dlt pipeline; run-all-or-nothing.
│   │   Use a single @asset that runs dlt.pipeline.run(...). No dlt_assets / Component.
```

**Ask if unclear:** When someone wants to build a dlt pipeline on Dagster, ask whether they want **dlt assets** (recommended) or a **standard Dagster asset**, and whether they will run on **Dagster compute** or **external compute** (ECS, Fargate, etc.).

**Component (recommended for dlt assets):** Declarative defs in YAML, scaffold-generated structure. **Pythonic:** All definitions in Python (@dlt_assets, DagsterDltResource). **Why dlt assets:** Selective runs and parallelization; a single native asset is run-all-or-nothing.

## Core Workflow

### 1. Understand Requirements

- **Asset type:** dlt assets (recommended) or standard Dagster asset? Ask if not specified.
- **Compute:** Run on Dagster’s default compute, or schedule in Dagster but run on external compute (ECS, Fargate, etc.)? If external, use the **dagster-integrations** skill (see below).
- **Dagster project:** New or existing? Components-ready (defs in YAML) or code-only?
- **dlt source:** Verified source (e.g. GitHub, Snowflake), declarative REST, or custom Python source?
- **Destination:** DuckDB, BigQuery, Snowflake, etc.
- **Orchestration:** One-off materialization, or job/schedule?

### 2. Prepare Dagster Project

**Component approach:** Use a components-ready project (or migrate). Create project:
```bash
uvx create-dagster project my-project && cd my-project/src
source ../.venv/bin/activate
uv add dagster-dlt
```

**Pythonic approach:** Existing Dagster project; add:
```bash
uv add dagster-dlt
# or: pip install dagster-dlt
```

### 3. Define dlt Loads

**Component:** Scaffold a dlt component definition (optional `--source` and `--destination` pull in dlt source):
```bash
dg scaffold defs dagster_dlt.DltLoadCollectionComponent my_ingest --source github --destination snowflake
```
Then edit `defs/<name>/loads.py` with your dlt source and pipeline, and `defs/<name>/defs.yaml` to reference them. See [references/component.md](references/component.md).

**Pythonic:** In Python, define a dlt source (verified, REST, or custom) and a `dlt.pipeline`. Create a `@dlt_assets` definition and add `DagsterDltResource` to `Definitions`. See [references/pythonic.md](references/pythonic.md).

### 4. Configure Secrets and Config

dlt credentials can be provided via environment variables (recommended with Dagster). Use Dagster’s env/secrets for both Dagster and dlt. No need for a local `.dlt/secrets.toml` if everything is in env.

Example env vars (names depend on source/destination):
```
SOURCES__GITHUB__ACCESS_TOKEN=...
DESTINATION__SNOWFLAKE__CREDENTIALS__DATABASE=...
DESTINATION__SNOWFLAKE__CREDENTIALS__PASSWORD=...
# etc.
```
See [references/secrets-and-env.md](references/secrets-and-env.md).

### 5. Run and Materialize

- **Component:** `dg dev` (or your deployment), then in the UI: Assets → select dlt assets → Materialize.
- **Pythonic:** Same: run Dagster, then materialize the dlt assets from the UI (or via job).

### 6. Add Jobs and Schedules (Optional)

Define asset jobs that select your dlt assets; attach schedules if you want recurring runs. See [references/jobs-and-schedules.md](references/jobs-and-schedules.md).

### 7. Cloud deployment (Optional)

Deploy to Dagster Cloud (serverless): connect repo → set env vars in Cloud UI → push; GitHub Actions updates the code location. See [references/cloud-deployment.md](references/cloud-deployment.md).

## Patterns

### Component — loads.py + defs.yaml

In `loads.py`: define source and pipeline (e.g. `source = github_stargazers(...)`, `pipeline = dlt.pipeline(...)`). In `defs.yaml`: `type: dagster_dlt.DltLoadCollectionComponent`, `attributes.loads` with `source:` and `pipeline:` pointing at those objects. See [references/component.md](references/component.md).

### Pythonic — @dlt_assets + Definitions

`@dlt_assets(dlt_source=..., dlt_pipeline=..., name=..., group_name=...)`; function takes `context` and `dlt_resource: DagsterDltResource`, body `yield from dlt_resource.run(context=context)`. Add `DagsterDltResource()` to `Definitions(resources={"dlt": ...})`. See [references/pythonic.md](references/pythonic.md).

### Component — Customize asset metadata

Use `translation` in defs.yaml for `group_name`, `description`, or `metadata` (e.g. `{{ resource.name }}`). See [references/component.md](references/component.md) §4.

### Dynamic incremental/backfill

`source.<resource>.apply_hints(incremental=dlt.sources.incremental(..., initial_value=os.getenv("MY_INITIAL_VALUE", "...")))`. Optional backfill: only apply when both initial and end env vars set. See [references/incremental-backfill-parallel.md](references/incremental-backfill-parallel.md).

### Parallelization

One asset per resource: `source.with_resources(resource_name)`, unique pipeline name per resource, `define_asset_job(..., executor_def=multi_process_executor, config={"max_concurrent": N})`. See [references/incremental-backfill-parallel.md](references/incremental-backfill-parallel.md).

### Standard Dagster asset (run-all-or-nothing)

Single `@asset` that builds `dlt.pipeline(...)`, gets the dlt source, and calls `pipeline.run(source)`. Add to `Definitions(assets=[...])`. No `dagster-dlt` or Component; use when the user explicitly wants one asset for the whole pipeline.

## Best Practices

- **Secrets:** Use env vars (Dagster deployment) for dlt; avoid committing `.dlt/secrets.toml`.
- **Component vs Pythonic:** Prefer Component for new projects; Pythonic when you already use code-only Definitions.
- **dlt sources:** Keep resources in a dlt source. For building or debugging dlt pipeline code, use the **dlt-skill** if available (see "Related skill: dlt-skill" below); this skill is for running pipelines in Dagster.
- **Incremental/backfill:** Env vars + `apply_hints`; **parallel:** one asset per resource, unique pipeline names, `multi_process_executor` + `max_concurrent`.

## Reference Documentation — When to Read What

- **Component setup (scaffold, loads.py, defs.yaml)** → [references/component.md](references/component.md)
- **Pythonic setup (@dlt_assets, DagsterDltResource, Definitions)** → [references/pythonic.md](references/pythonic.md)
- **Secrets and environment variables for dlt in Dagster** → [references/secrets-and-env.md](references/secrets-and-env.md)
- **Jobs and schedules for dlt assets** → [references/jobs-and-schedules.md](references/jobs-and-schedules.md)
- **Incremental loading, backfilling, parallelization** → [references/incremental-backfill-parallel.md](references/incremental-backfill-parallel.md)
- **Dagster Cloud (serverless) deployment** → [references/cloud-deployment.md](references/cloud-deployment.md)
- **Errors, venv, imports, defs paths** → [references/troubleshooting.md](references/troubleshooting.md)

## Further reading

- [Deploy dlt with Dagster](https://dlthub.com/docs/walkthroughs/deploy-a-pipeline/deploy-with-dagster) — dlt docs
- [Dagster & dlt (Component)](https://docs.dagster.io/integrations/libraries/dlt) — Component setup
- [Dagster & dlt (Pythonic)](https://docs.dagster.io/integrations/libraries/dlt/dlt-pythonic) — @dlt_assets setup


## Related skill: dlt-skill

When the task requires **building or designing dlt pipelines** (choosing verified sources, declarative REST API, custom Python sources, destinations, incremental loading in dlt, or editing `.dlt` config and secrets), use the **dlt-skill** if it is available. This skill (dlt-dagster) focuses on running existing dlt pipelines in Dagster; the dlt-skill covers creating and maintaining the dlt pipeline itself.

**If the dlt-skill is not installed:** Tell the user that a dedicated skill named **dlt-skill** exists for creating and maintaining dlt pipelines (verified sources, REST API, custom sources, destinations, incremental loading). With the user’s approval, they can install it with:

```bash
npx skills add untitled-data-company/data-skills --skill dlt-skill
```

(Use the repo URL that hosts the dlt-skill if different.)

## Related skill: dagster-integrations

When the user wants to **schedule a dlt pipeline (or any job) via Dagster but run it on external compute** (e.g. ECS, Fargate, or other compute engines), use the **dagster-integrations** skill if it is available. This skill (dlt-dagster) focuses on running dlt pipelines as Dagster assets on Dagster’s compute; dagster-integrations covers running work on other engines.

**If dagster-integrations is not installed:** Tell the user that a skill named **dagster-integrations** exists for running Dagster jobs on external compute (ECS, Fargate, etc.). With the user’s approval, they can install it with:

```bash
npx skills add https://github.com/dagster-io/skills --skill dagster-integrations
```

## Templates and Scripts

### Asset templates

- **[assets/templates/loads.py](assets/templates/loads.py)** — Minimal Component `loads.py` (source + pipeline)
- **[assets/templates/defs.yaml](assets/templates/defs.yaml)** — Minimal Component `defs.yaml` for one load

No scripts are required; use `dg scaffold defs` and `dg dev` / Dagster deployment.

## Key Reminders

- **Ask when unclear:** dlt assets (recommended) vs standard Dagster asset? Run on Dagster compute vs external (ECS, Fargate)? If external compute → use **dagster-integrations** skill.
- **Component:** `dg scaffold defs dagster_dlt.DltLoadCollectionComponent <name> [--source ...] [--destination ...]` → edit `loads.py` and `defs.yaml`.
- **Pythonic:** `DagsterDltResource` in `Definitions`; in `@dlt_assets` call `yield from dlt_resource.run(context=context)`.
