---
name: query-metrics
description: Runs metrics queries against Axiom MetricsDB via scripts. Discovers available metrics, tags, and tag values. Use when asked to query metrics, explore metric datasets, check metric values, or investigate OTel metrics data.
---

> **CRITICAL:** ALL script paths are relative to this skill's folder. Run them with full path (e.g., `scripts/metrics-query`).

# Querying Axiom Metrics

Query OpenTelemetry metrics stored in Axiom's MetricsDB.

## Setup

Run `scripts/setup` to check requirements (curl, jq, ~/.axiom.toml).

Config in `~/.axiom.toml` (shared with axiom-sre):
```toml
[deployments.prod]
url = "https://api.axiom.co"
token = "xaat-your-token"
org_id = "your-org-id"
```

The target dataset must be of kind `otel-metrics-v1`.

---

## Learning the Metrics Query Syntax

The query endpoint is self-describing. Before writing any query, fetch the full specification:

```bash
scripts/metrics-spec <deployment>
```

This returns the complete metrics query specification with syntax, operators, and examples. Read it to understand query structure before composing queries.

---

## Workflow

1. **Learn the language**: Run `scripts/metrics-spec <deployment>` to read the metrics query spec
2. **Discover metrics**: If possible use the find-metrics command, otherwise list available metrics via the info scripts
3. **Explore tags**: List tags and tag values to understand filtering options
4. **Write and execute query**: Compose a metrics query and run it via `scripts/metrics-query`
5. **Iterate**: Refine filters, aggregations, and groupings based on results

If you are unsure what to query, start by searching for metrics that match a relevant tag value:
```bash
scripts/metrics-info <deployment> <dataset> find-metrics "frontend"
```
This finds metrics associated with a known value (e.g., a service name or host), giving you a starting point for building queries.

---

## Query Metrics

Execute a metrics query against a dataset:

```bash
scripts/metrics-query <deployment> '<apl>' '<startTime>' '<endTime>'
```

**Example:**
```bash
scripts/metrics-query prod \
  'my-dataset:http.server.duration | align to 5m using avg' \
  '2025-06-01T00:00:00Z' \
  '2025-06-02T00:00:00Z'
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `deployment` | Yes | Name from `~/.axiom.toml` (e.g., `prod`) |
| `apl` | Yes | Metrics query string. Dataset is extracted from the query itself. |
| `startTime` | Yes | RFC3339 timestamp only (e.g., `2025-01-01T00:00:00Z`). Relative expressions like `now-1h` are **not** supported. |
| `endTime` | Yes | RFC3339 timestamp only (e.g., `2025-01-02T00:00:00Z`). Relative expressions like `now` are **not** supported. |

---

## Discovery (Info Endpoints)

Use `scripts/metrics-info` to explore what metrics, tags, and values exist in a dataset before writing queries. Time range defaults to the last 24 hours; override with `--start` and `--end`.

### List metrics in a dataset

```bash
scripts/metrics-info <deployment> <dataset> metrics
```

### List tags in a dataset

```bash
scripts/metrics-info <deployment> <dataset> tags
```

### List values for a specific tag

```bash
scripts/metrics-info <deployment> <dataset> tags <tag> values
```

### List tags for a specific metric

```bash
scripts/metrics-info <deployment> <dataset> metrics <metric> tags
```

### List tag values for a specific metric and tag

```bash
scripts/metrics-info <deployment> <dataset> metrics <metric> tags <tag> values
```

### Find metrics matching a tag value

```bash
scripts/metrics-info <deployment> <dataset> find-metrics "<search-value>"
```

### Custom time range

All info commands accept `--start` and `--end` for custom time ranges:

```bash
scripts/metrics-info prod my-dataset metrics \
  --start 2025-06-01T00:00:00Z \
  --end 2025-06-02T00:00:00Z
```

---

## Error Handling

HTTP errors return JSON with `message` and `error` fields:
```json
{"message": "description", "error": "detail"}
```

Common status codes:
- 400 — Invalid query syntax or bad dataset name
- 401 — Missing or invalid authentication
- 403 — No permission to query/ingest this dataset
- 404 — Dataset not found
- 429 — Rate limited
- 500 — Internal server error

On a **500 error**, re-run the failing script call with `curl -v` flags to capture response headers, then report the `traceparent` or `x-axiom-trace-id` header value to the user. This trace ID is essential for debugging the failure with the backend team.

---

## Scripts

| Script | Usage |
|--------|-------|
| `scripts/setup` | Check requirements and config |
| `scripts/metrics-spec <deploy>` | Fetch metrics query specification |
| `scripts/metrics-query <deploy> <apl> <start> <end>` | Execute a metrics query |
| `scripts/metrics-info <deploy> <dataset> ...` | Discover metrics, tags, and values |
| `scripts/axiom-api <deploy> <method> <path> [body]` | Low-level API calls |

Run any script without arguments to see full usage.
