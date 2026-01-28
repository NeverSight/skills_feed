---
name: spicepod-config
description: Create and configure Spicepod manifests (spicepod.yaml). Use when asked to "create a spicepod", "configure spicepod.yaml", "set up a Spice app", "initialize Spice project", "configure caching", or "set up observability".
---

# Spicepod Configuration

A Spicepod is the configuration manifest for a Spice application, defining datasets, models, embeddings, runtime settings, and other components.

## Basic Structure

```yaml
version: v1
kind: Spicepod
name: my_app

secrets:
  - from: env
    name: env

datasets:
  - from: <connector>:<path>
    name: <dataset_name>

models:
  - from: <provider>:<model>
    name: <model_name>

embeddings:
  - from: <provider>:<model>
    name: <embedding_name>

runtime:
  # Server, caching, and telemetry settings
```

## Component Sections

| Section        | Purpose                                    | Skill Reference       |
|----------------|--------------------------------------------|-----------------------|
| `datasets`     | Data sources for SQL queries               | spice-data-connector  |
| `models`       | LLM/ML models for inference                | spice-models          |
| `embeddings`   | Embedding models for vector search         | spice-embeddings      |
| `secrets`      | Secure credential management               | spice-secrets         |
| `catalogs`     | External data catalog connections          | spice-catalogs        |
| `views`        | Virtual tables from SQL queries            | spice-views           |
| `tools`        | LLM function calling capabilities          | spice-tools           |
| `workers`      | Model load balancing and routing           | spice-workers         |
| `runtime`      | Server ports, caching, telemetry           | (this skill)          |

## Quick Start Example

```yaml
version: v1
kind: Spicepod
name: quickstart

secrets:
  - from: env
    name: env

datasets:
  - from: postgres:public.users
    name: users
    params:
      pg_host: localhost
      pg_port: 5432
      pg_user: ${ env:PG_USER }
      pg_pass: ${ env:PG_PASS }
    acceleration:
      enabled: true
      engine: duckdb
      refresh_check_interval: 5m

models:
  - from: openai:gpt-4o
    name: assistant
    params:
      openai_api_key: ${ secrets:OPENAI_API_KEY }
      tools: auto
```

## Runtime Configuration

Configure server ports, caching, and observability under `runtime`:

```yaml
runtime:
  http:
    enabled: true
    port: 8090
  flight:
    enabled: true
    port: 50051
```

### Results Caching

In-memory caching for SQL and search results (enabled by default):

```yaml
runtime:
  caching:
    sql_results:
      enabled: true
      max_size: 128MiB           # cache size limit
      item_ttl: 1s               # time-to-live per entry
      eviction_policy: lru       # lru or tiny_lfu
      encoding: none             # none or zstd (compression)
    search_results:
      enabled: true
      max_size: 128MiB
      item_ttl: 1s
    embeddings:
      enabled: true
      max_size: 128MiB
```

#### Stale-While-Revalidate

Serve stale cache entries while refreshing in background:

```yaml
runtime:
  caching:
    sql_results:
      item_ttl: 10s
      stale_while_revalidate_ttl: 10s  # serve stale for 10s while refreshing
```

### Observability & Telemetry

```yaml
runtime:
  telemetry:
    enabled: true
    otel_exporter:
      endpoint: 'localhost:4317'   # OpenTelemetry collector
      push_interval: 60s
      metrics:                     # optional: filter specific metrics
        - query_duration_ms
        - query_executions
```

Prometheus metrics endpoint runs on port `9090` by default:
```bash
curl http://localhost:9090/metrics
```

## Dataset with Acceleration

```yaml
datasets:
  - from: s3://my-bucket/data/
    name: events
    params:
      file_format: parquet
    acceleration:
      enabled: true
      engine: duckdb
      mode: file
      refresh_mode: append
      refresh_check_interval: 1h
```

See **spice-data-connector** for connector options, **spice-accelerators** for acceleration config.

## AI-Powered Application

```yaml
embeddings:
  - from: openai:text-embedding-3-small
    name: embed
    params:
      openai_api_key: ${ secrets:OPENAI_API_KEY }

datasets:
  - from: postgres:documents
    name: docs
    acceleration:
      enabled: true
    columns:
      - name: content
        embeddings:
          - from: embed
            row_id: id

models:
  - from: openai:gpt-4o
    name: assistant
    params:
      openai_api_key: ${ secrets:OPENAI_API_KEY }
      tools: auto, search
```

See **spice-models** for model providers, **spice-embeddings** for embedding config.

## CLI Commands

```bash
spice init my_app      # Create new spicepod.yaml
spice run              # Start runtime with current spicepod
spice sql              # Interactive SQL shell
spice chat             # Interactive chat with models
spice status           # Check runtime status
```

## Documentation

**Getting Started:**
- [Getting Started Guide](https://spiceai.org/docs/getting-started)
- [Spicepods Overview](https://spiceai.org/docs/getting-started/spicepods)

**Reference:**
- [Spicepod YAML Reference](https://spiceai.org/docs/reference/spicepod)
- [Datasets Reference](https://spiceai.org/docs/reference/spicepod/datasets)
- [Runtime Reference](https://spiceai.org/docs/reference/spicepod/runtime)

**Features:**
- [Caching](https://spiceai.org/docs/features/caching)
- [Data Acceleration](https://spiceai.org/docs/features/data-acceleration)
- [Search](https://spiceai.org/docs/features/search)
- [Observability](https://spiceai.org/docs/features/observability)

**Components:**
- [Data Connectors](https://spiceai.org/docs/components/data-connectors)
- [Data Accelerators](https://spiceai.org/docs/components/data-accelerators)
- [Model Providers](https://spiceai.org/docs/components/models)
- [Embedding Models](https://spiceai.org/docs/components/embeddings)
- [Secret Stores](https://spiceai.org/docs/components/secret-stores)
