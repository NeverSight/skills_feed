---
name: dlt-skill
description: >
  Creates and maintains dlt (data load tool) pipelines from APIs, databases, and other sources.
  Use when the user wants to build or debug pipelines; use verified sources (e.g. Salesforce, GitHub, Stripe)
  or declarative REST API or custom Python; configure destinations (e.g. DuckDB, BigQuery, Snowflake);
  implement incremental loading; or edit .dlt config and secrets.
  Use when the user mentions data ingestion, dlt pipeline, dlt init, rest_api_source, incremental load, or pipeline dashboard.
---

# dlt Pipeline Creator

Choose pipeline type with the decision tree below; then follow the Core Workflow.

**Quick start:** 1) Use the decision tree. 2) Follow the Core Workflow. 3) Use patterns and references as needed.

## Pipeline Type Decision Tree

When a user requests a dlt pipeline, determine which type to create:

```
START: User wants to create a dlt pipeline
│
├─→ Is there a dlt verified source available for this platform?
│   (Check: https://dlthub.com/docs/dlt-ecosystem/verified-sources)
│   │
│   YES → Use VERIFIED SOURCE approach
│   │     Examples: Salesforce, GitHub, Stripe, HubSpot, Slack
│   │     Action: Guide user through `dlt init <source> <destination>`
│   │
│   NO → Continue to next question
│
├─→ Is this a REST API with standard patterns?
│   (Standard auth, pagination, JSON responses)
│   │
│   YES → Use DECLARATIVE REST API approach
│   │     Examples: Pokemon API, simple REST APIs with clear endpoints
│   │     Action: Create config-based pipeline with rest_api_source
│   │
│   NO → Continue to next question
│
└─→ Does this require custom logic or Python packages?
    │
    YES → Use CUSTOM PYTHON approach
          Examples: Python packages (simple-salesforce), complex transformations,
                   non-standard APIs, custom data sources
          Action: Create custom source with @dlt.source and @dlt.resource decorators
```

## Core Workflow

### 1. Understand Requirements

Ask clarifying questions:
- **Source**: What is the data source? (API URL, platform name, database, etc.)
- **Source type**: Does this match a verified source, REST API, or require custom code?
- **Destination**: Where should data be loaded? (DuckDB, BigQuery, Snowflake, etc.)
- **Resources**: What specific data/endpoints are needed?
- **Incremental**: Should the pipeline load incrementally or do full refreshes?
- **Authentication**: What credentials are required?

### 2. Choose Pipeline Approach

Based on the decision tree above, select:
- **Verified source** - Pre-built, tested connector
- **Declarative REST API** - Config-based REST API pipeline
- **Custom Python** - Full control with Python code

### 3. Initialize or Create Pipeline

#### Verified source
```bash
dlt init <source_name> <destination_name>
```
Examples:
- `dlt init salesforce bigquery`
- `dlt init github duckdb`
- `dlt init stripe snowflake`

#### Declarative REST API or Custom Python
Use templates from this skill's [assets/templates/](assets/templates/) (copy into the project if needed):
- `declarative_rest_pipeline.py` - For REST APIs
- `custom_python_pipeline.py` - For custom sources

### 4. Install Required Packages

**Recommended:** Use the helper script (detects pip/uv/poetry):
```bash
python scripts/install_packages.py --destination <destination_name>
```

**Manual:** `pip install "dlt[<destination>,workspace]"` (e.g. `bigquery`, `snowflake`). For DuckDB use `dlt[workspace]` only. The `workspace` extra is required for `dlt pipeline <name> show` and the dashboard.

### 5. Configure Credentials

Create or update `.dlt/secrets.toml`:

**Structure:**
```toml
[sources.<source_name>]
# Source credentials here

[destination.<destination_name>]
# Destination credentials here
```

Use the template: [assets/templates/.dlt/secrets.toml](assets/templates/.dlt/secrets.toml)

**Important**: Remind user to add `.dlt/secrets.toml` to `.gitignore`!

**Note for DuckDB**: DuckDB doesn't require credentials in secrets.toml. Just specify the database file path in the pipeline or config.toml.

### 6. Configure Pipeline Settings

Create or update `.dlt/config.toml` for non-sensitive settings:

```toml
[sources.<source_name>]
base_url = "https://api.example.com"
timeout = 30

[destination.<destination_name>]
location = "US"
```

Use the template: [assets/templates/.dlt/config.toml](assets/templates/.dlt/config.toml)

### 7. Implement Pipeline Logic

Flesh out the pipeline code based on requirements:

**For verified sources**:
- Customize resource selection with `.with_resources()`
- Configure incremental loading with `.apply_hints()`
- See: [references/verified-sources.md](references/verified-sources.md)

**For Declarative REST API**:
- Define client configuration (base_url, auth)
- Configure resources and endpoints
- Set up pagination and incremental loading
- See: [references/rest-api-source.md](references/rest-api-source.md)

**For Custom Python**:
- Implement `@dlt.source` and `@dlt.resource` functions
- Use generators and yield patterns
- Configure write dispositions and primary keys
- See: [references/custom-sources.md](references/custom-sources.md)

### 8. Configure Incremental Loading (If Needed)

For pipelines that should load only new/changed data:
- Identify cursor field (timestamp, ID)
- Set write disposition to `merge`
- Define primary key for deduplication
- Configure incremental parameters

See: [references/incremental-loading.md](references/incremental-loading.md)

### 9. Test and Run Pipeline

```python
python <pipeline_file>.py
```

Check for errors and verify data is loaded correctly.

### 10. Inspect Results

**Prerequisite**: Ensure `dlt[workspace]` is installed (included by default when using `install_packages.py`).

Open the dlt dashboard to inspect loaded data:
```bash
dlt pipeline <pipeline_name> show
```

Or use the helper script:
```bash
python scripts/open_dashboard.py <pipeline_name>
```

## Pipeline Patterns

### Pattern 1: Verified source — Select specific resources

```python
from salesforce import salesforce_source

source = salesforce_source()
pipeline = dlt.pipeline(
    pipeline_name='salesforce_pipeline',
    destination='bigquery',
    dataset_name='salesforce_data'
)

# Load only specific Salesforce objects
pipeline.run(source.with_resources("Account", "Opportunity", "Contact"))
```

### Pattern 2: Declarative REST API - Simple Endpoints

```python
from dlt.sources.rest_api import rest_api_source

config = {
    "client": {
        "base_url": "https://pokeapi.co/api/v2/",
    },
    "resources": [
        "pokemon",
        {
            "name": "pokemon_details",
            "endpoint": "pokemon/{name}",
            "write_disposition": "merge",
            "primary_key": "id"
        }
    ]
}

pipeline = dlt.pipeline(
    pipeline_name="pokemon",
    destination="duckdb",
    dataset_name="pokemon_data"
)
pipeline.run(rest_api_source(config))
```

### Pattern 3: Custom Python - Using Python Package

```python
import dlt
from simple_salesforce import Salesforce

@dlt.source
def salesforce_custom(username=dlt.secrets.value, password=dlt.secrets.value):
    sf = Salesforce(username=username, password=password)

    @dlt.resource(write_disposition='merge', primary_key='Id')
    def accounts():
        records = sf.query_all("SELECT Id, Name FROM Account")
        yield records['records']

    return accounts

pipeline = dlt.pipeline(
    pipeline_name='salesforce_custom',
    destination='duckdb',
    dataset_name='salesforce'
)
pipeline.run(salesforce_custom())
```

### Pattern 4: Incremental Loading with REST API

```python
config = {
    "client": {
        "base_url": "https://api.github.com/repos/dlt-hub/dlt/",
        "auth": {"token": dlt.secrets["github_token"]}
    },
    "resources": [
        {
            "name": "issues",
            "endpoint": {
                "path": "issues",
                "params": {
                    "state": "all",
                    "since": "{incremental.start_value}"
                }
            },
            "incremental": {
                "cursor_path": "updated_at",
                "initial_value": "2024-01-01T00:00:00Z"
            },
            "write_disposition": "merge",
            "primary_key": "id"
        }
    ]
}
```

### Pattern 5: Non-endpoint resources for REST API sources (e.g. Database-Seeded or File-Seeded parameters)

Use non-endpoint resources (e.g. Database-Seeded or File-Seeded parameters) to drive REST API calls from a database, file, or other non-API source. Pre-fetch data **outside** the dlt pipeline context to avoid `dlt.attach()` / context conflicts. The seed resource must **yield a list** of dicts so each row drives one API request.

```python
import duckdb
import dlt
from dlt.sources.rest_api import rest_api_source

# 1. Pre-fetch data from database (outside dlt context)
def get_locations():
    conn = duckdb.connect("locations.duckdb", read_only=True)
    result = conn.execute("SELECT id, lat, lng FROM locations").fetchall()
    conn.close()
    return [{"id": r[0], "lat": r[1], "lng": r[2]} for r in result]

# 2. Create seed resource
@dlt.resource(selected=False)
def locations():
    yield get_locations()  # Yield as LIST

# 3. Configure REST API with resolve
config = {
    "client": {"base_url": "https://api.weather.com/"},
    "resources": [
        locations(),
        {
            "name": "weather",
            "endpoint": {
                "path": "forecast",
                "params": {
                    "lat": "{resources.locations.lat}",
                    "lng": "{resources.locations.lng}"
                },
                "data_selector": "$",
                "paginator": "single_page"
            },
            "include_from_parent": ["id"],
            "primary_key": "_locations_id"
        }
    ]
}

source = rest_api_source(config)
pipeline = dlt.pipeline(
    pipeline_name="weather",
    destination="duckdb",
    dataset_name="weather_data"
)
pipeline.run(source)
```

See: [references/rest-api-source.md](references/rest-api-source.md) (Non-REST Endpoint Resources, Query/Path Params, Single-Object Responses, include_from_parent).

## Best Practices (Data Engineering)

- **Secrets**: Use `.dlt/secrets.toml`; never hardcode; add to `.gitignore`
- **Primary keys**: Set for merge operations and deduplication
- **Write dispositions**: `append` (events), `merge` (stateful), `replace` (snapshots)
- **Performance**: Yield pages not rows; use incremental loading when possible

See [references/performance-tuning.md](references/performance-tuning.md), [references/incremental-loading.md](references/incremental-loading.md), and [references/troubleshooting.md](references/troubleshooting.md) for more.

## Common Challenges and Solutions

**Auth (OAuth2):** In REST config use `"auth": {"type": "oauth2_client_credentials", ...}`. For custom Python use `dlt.sources.helpers.rest_client.auth.OAuth2ClientCredentials` with `paginate()`. See [references/rest-api-source.md](references/rest-api-source.md).

**Custom pagination / nested data / performance:** See [references/rest-api-source.md](references/rest-api-source.md), [references/custom-sources.md](references/custom-sources.md), [references/performance-tuning.md](references/performance-tuning.md).

## Reference Documentation — When to Read What

- **Full workflow / step-by-step example** → [examples.md](examples.md)
- **Verified source** → [references/verified-sources.md](references/verified-sources.md)
- **Declarative REST API** → [references/rest-api-source.md](references/rest-api-source.md)
- **Custom Python source** → [references/custom-sources.md](references/custom-sources.md)
- **Incremental loading** → [references/incremental-loading.md](references/incremental-loading.md)
- **Performance** → [references/performance-tuning.md](references/performance-tuning.md)
- **Errors / debugging** → [references/troubleshooting.md](references/troubleshooting.md)
- **dlt basics** → [references/core-concepts.md](references/core-concepts.md)

## Templates and Scripts

### Templates (assets/templates/)

- **[custom_python_pipeline.py](assets/templates/custom_python_pipeline.py)** - Custom Python pipeline skeleton
- **[verified_source_pipeline.py](assets/templates/verified_source_pipeline.py)** - Verified source pipeline skeleton
- **[declarative_rest_pipeline.py](assets/templates/declarative_rest_pipeline.py)** - Declarative REST API pipeline skeleton
- **[.dlt/config.toml](assets/templates/.dlt/config.toml)** - Configuration file template
- **[.dlt/secrets.toml](assets/templates/.dlt/secrets.toml)** - Secrets file template
- **[.gitignore](assets/templates/.gitignore)** - Git ignore template for dlt projects

### Scripts (scripts/)

- **[install_packages.py](scripts/install_packages.py)** - Install dlt + destination extras (includes `workspace`). Run when setting up a new project or adding a destination.
- **[open_dashboard.py](scripts/open_dashboard.py)** - Open pipeline dashboard (`dlt pipeline <name> show`). Run after a pipeline run to inspect loaded data.

## Key Reminders
- **Always ask about destination** - Don't assume
- **Security first** - Never commit secrets; use `.dlt/secrets.toml` and provide `.gitignore`
- **Start simple** - Use verified sources when available; test incrementally
- **Read references** - Load detailed docs only when needed
