---
name: prometheus-api
description: Query and interact with Prometheus HTTP API for monitoring data. Use when Claude needs to query Prometheus metrics, execute PromQL queries, retrieve targets/alerts/rules status, access metadata about series/labels, manage TSDB operations, or troubleshoot monitoring infrastructure. Supports instant queries, range queries, metadata endpoints, admin APIs, and alerting information.
---

# Prometheus API Skill

Query Prometheus monitoring systems via HTTP API at `/api/v1`.

## Quick Reference

### Instant Query

```bash
curl 'http://<prometheus>:9090/api/v1/query?query=<promql>&time=<timestamp>'
```

### Range Query

```bash
curl 'http://<prometheus>:9090/api/v1/query_range?query=<promql>&start=<ts>&end=<ts>&step=<duration>'
```

## Response Format

All responses return JSON:

```json
{
  "status": "success" | "error",
  "data": <result>,
  "errorType": "<string>",
  "error": "<string>",
  "warnings": ["<string>"]
}
```

HTTP codes: `400` (bad params), `422` (expression error), `503` (timeout).

## Query Endpoints

| Endpoint | Purpose | Key Parameters |
|----------|---------|----------------|
| `/api/v1/query` | Instant query | `query`, `time`, `timeout`, `limit` |
| `/api/v1/query_range` | Range query | `query`, `start`, `end`, `step`, `timeout`, `limit` |
| `/api/v1/format_query` | Format PromQL | `query` |
| `/api/v1/series` | Find series by labels | `match[]`, `start`, `end`, `limit` |
| `/api/v1/labels` | List label names | `start`, `end`, `match[]`, `limit` |
| `/api/v1/label/<name>/values` | Label values | `start`, `end`, `match[]`, `limit` |
| `/api/v1/query_exemplars` | Query exemplars | `query`, `start`, `end` |

## Metadata & Status Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/api/v1/targets` | Target discovery status (`state=active\|dropped\|any`) |
| `/api/v1/targets/metadata` | Metric metadata from targets |
| `/api/v1/metadata` | All metric metadata |
| `/api/v1/rules` | Alerting/recording rules |
| `/api/v1/alerts` | Active alerts |
| `/api/v1/alertmanagers` | Alertmanager discovery |
| `/api/v1/status/config` | Current config YAML |
| `/api/v1/status/flags` | CLI flags |
| `/api/v1/status/runtimeinfo` | Runtime info |
| `/api/v1/status/buildinfo` | Build info |
| `/api/v1/status/tsdb` | TSDB cardinality stats |
| `/api/v1/status/walreplay` | WAL replay progress |

## Admin Endpoints (require `--web.enable-admin-api`)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/admin/tsdb/snapshot` | POST | Create TSDB snapshot |
| `/api/v1/admin/tsdb/delete_series` | POST | Delete series (`match[]`, `start`, `end`) |
| `/api/v1/admin/tsdb/clean_tombstones` | POST | Clean deleted data |

## Common PromQL Patterns

```promql
# Rate of counter over 5m
rate(http_requests_total[5m])

# Sum by label
sum by (job) (rate(http_requests_total[5m]))

# Percentile from histogram
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Filter by label
up{job="prometheus", instance=~".*:9090"}

# Increase over time
increase(http_requests_total[1h])

# Average over time range
avg_over_time(process_cpu_seconds_total[5m])
```

## Result Types

- **vector**: `[{"metric": {...}, "value": [timestamp, "value"]}]`
- **matrix**: `[{"metric": {...}, "values": [[ts, "val"], ...]}]`
- **scalar**: `[timestamp, "value"]`
- **string**: `[timestamp, "string"]`

## Scripts

Query script: `scripts/prom_query.py`

```bash
# Instant query
python scripts/prom_query.py http://localhost:9090 'up'

# Range query
python scripts/prom_query.py http://localhost:9090 'rate(http_requests_total[5m])' \
  --start '2024-01-01T00:00:00Z' --end '2024-01-01T01:00:00Z' --step '1m'

# Output: table, json, csv
python scripts/prom_query.py http://localhost:9090 'up' --format table
```

Health check: `scripts/prom_health.py`

```bash
python scripts/prom_health.py http://localhost:9090
```

## Detailed Reference

For complete API documentation: [references/api_reference.md](references/api_reference.md)

For PromQL functions: [references/promql_functions.md](references/promql_functions.md)
