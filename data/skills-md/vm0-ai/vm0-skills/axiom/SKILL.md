---
name: axiom
description: Axiom observability platform for logs, events, and analytics via REST API
vm0_secrets:
  - AXIOM_API_TOKEN
---

# Axiom

Axiom is a cloud-native observability platform for storing, querying, and analyzing log and event data at scale. Use the REST API to ingest data, run queries using APL (Axiom Processing Language), and manage datasets programmatically.

> Official docs: `https://axiom.co/docs/restapi/introduction`

---

## When to Use

Use this skill when you need to:

- Send logs, metrics, or event data to Axiom
- Query and analyze data using APL (Axiom Processing Language)
- Manage datasets, monitors, and annotations
- Build observability pipelines and dashboards

---

## Prerequisites

1. Create an Axiom account at https://app.axiom.co/register
2. Create an API token with appropriate permissions (Settings > API Tokens)
3. Create a dataset to store your data

### Token Types

Axiom supports two token types:

| Type | Prefix | Use Case |
|------|--------|----------|
| **API Token** | `xaat-` | Most operations (datasets, ingest, queries, monitors) |
| **Personal Access Token (PAT)** | `xapt-` | Full account access (required for `/v2/user` endpoint) |

Set environment variables:

```bash
# Required: API Token for most operations
export AXIOM_API_TOKEN="xaat-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"'
> ```

## How to Use

### Base URLs

- **Ingest (US East)**: `https://us-east-1.aws.edge.axiom.co`
- **Ingest (EU Central)**: `https://eu-central-1.aws.edge.axiom.co`
- **API**: `https://api.axiom.co`

### 1. List Datasets

```bash
bash -c 'curl -s "https://api.axiom.co/v2/datasets" -H "Authorization: Bearer ${AXIOM_API_TOKEN}"'
```

### 2. Get Dataset Info

```bash
bash -c 'curl -s "https://api.axiom.co/v2/datasets/my-logs" -H "Authorization: Bearer ${AXIOM_API_TOKEN}"'
```

### 3. Create Dataset

Write to `/tmp/axiom_request.json`:

```json
{
  "name": "my-logs",
  "description": "Application logs"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.axiom.co/v2/datasets" -H "Authorization: Bearer ${AXIOM_API_TOKEN}" -H "Content-Type: application/json" -d @/tmp/axiom_request.json'
```

### 4. Ingest Data (JSON)

Write to `/tmp/axiom_request.json`:

```json
[
  {"message": "User logged in", "user_id": "123", "level": "info"}
]
```

Then run:

```bash
bash -c 'curl -s -X POST "https://us-east-1.aws.edge.axiom.co/v1/ingest/my-logs" -H "Authorization: Bearer ${AXIOM_API_TOKEN}" -H "Content-Type: application/json" -d @/tmp/axiom_request.json'
```

### 5. Ingest Data (NDJSON)

Write to `/tmp/axiom_ndjson.ndjson`:

```
{"message": "Event 1", "level": "info"}
{"message": "Event 2", "level": "warn"}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://us-east-1.aws.edge.axiom.co/v1/ingest/my-logs" -H "Authorization: Bearer ${AXIOM_API_TOKEN}" -H "Content-Type: application/x-ndjson" -d @/tmp/axiom_ndjson.ndjson'
```

### 6. Query Data with APL

Write to `/tmp/axiom_request.json`:

```json
{
  "apl": "[\"my-logs\"] | where level == \"error\" | limit 10",
  "startTime": "2024-01-01T00:00:00Z",
  "endTime": "2025-12-31T23:59:59Z"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.axiom.co/v1/datasets/_apl?format=tabular" -H "Authorization: Bearer ${AXIOM_API_TOKEN}" -H "Content-Type: application/json" -d @/tmp/axiom_request.json'
```

### 7. Query with Aggregation

Write to `/tmp/axiom_request.json`:

```json
{
  "apl": "[\"my-logs\"] | summarize count() by level",
  "startTime": "2024-01-01T00:00:00Z",
  "endTime": "2025-12-31T23:59:59Z"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.axiom.co/v1/datasets/_apl?format=tabular" -H "Authorization: Bearer ${AXIOM_API_TOKEN}" -H "Content-Type: application/json" -d @/tmp/axiom_request.json'
```

### 8. Create Annotation

Write to `/tmp/axiom_request.json`:

```json
{
  "datasets": ["my-logs"],
  "type": "deployment",
  "title": "v1.2.0 deployed",
  "time": "2024-12-24T10:00:00Z"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.axiom.co/v2/annotations" -H "Authorization: Bearer ${AXIOM_API_TOKEN}" -H "Content-Type: application/json" -d @/tmp/axiom_request.json'
```

### 9. List Monitors

```bash
bash -c 'curl -s "https://api.axiom.co/v2/monitors" -H "Authorization: Bearer ${AXIOM_API_TOKEN}"'
```

### 10. Delete Dataset

```bash
bash -c 'curl -s -X DELETE "https://api.axiom.co/v2/datasets/my-logs" -H "Authorization: Bearer ${AXIOM_API_TOKEN}"'
```

---

## APL Query Examples

APL (Axiom Processing Language) is similar to Kusto Query Language (KQL). Use `["dataset-name"]` syntax for dataset names with special characters.

| Query | Description |
|-------|-------------|
| `["dataset"] \| limit 10` | Get first 10 events |
| `["dataset"] \| where level == "error"` | Filter by field value |
| `["dataset"] \| where message contains "timeout"` | Search in text |
| `["dataset"] \| summarize count() by level` | Count by group |
| `["dataset"] \| summarize avg(duration_ms) by bin(_time, 1h)` | Hourly average |
| `["dataset"] \| sort by _time desc \| limit 100` | Latest 100 events |
| `["dataset"] \| where _time > ago(1h)` | Events in last hour |

---

## Guidelines

1. **Use Edge URLs for Ingest**: Always use the edge endpoint (`us-east-1.aws.edge.axiom.co` or `eu-central-1.aws.edge.axiom.co`) for data ingestion, not `api.axiom.co`
2. **Batch Events**: Send multiple events in a single request for better performance
3. **Include Timestamps**: Events without timestamps will use server receive time
4. **Rate Limits**: Check `X-RateLimit-Remaining` header to avoid hitting limits
5. **APL Time Range**: Always specify `startTime` and `endTime` for queries to improve performance
6. **Data Formats**: JSON array is recommended; NDJSON and CSV are also supported
