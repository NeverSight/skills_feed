---
name: elasticsearch
description: >
  Interact with Elasticsearch and Kibana via REST API using curl. Use when querying, indexing,
  managing indices, checking cluster health, writing aggregations, deploying dashboards, or
  troubleshooting Elasticsearch. Requires cluster URL and API key. Covers: search (Query DSL),
  CRUD operations, index management, mappings, aggregations, cluster health, ILM, ES|QL,
  Kibana API (dashboards, data views, saved objects), OpenTelemetry data patterns, and common
  troubleshooting patterns.
---

# Elasticsearch

All Elasticsearch interaction is via REST API using `curl`. No SDK or client library required.

## Authentication

Every request needs the cluster URL and an API key:

```bash
# Set these for your session (or export in .env / shell profile)
ES_URL="https://your-cluster.es.cloud.elastic.co:443"
ES_API_KEY="your-base64-api-key"

# All requests follow this pattern:
curl -s "${ES_URL%/}/<endpoint>" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '<json-body>'
```

**API key format:** Base64-encoded `id:api_key` string. Pass as-is in the `Authorization: ApiKey` header.

If the user provides a URL and key, export them as `ES_URL` and `ES_API_KEY` before running commands.

**Important — variable expansion in curl:**
- Always use `$(printenv ES_API_KEY)` instead of `$ES_API_KEY` in curl headers. The `$ES_API_KEY` variable may not expand correctly in the shell, resulting in empty `Authorization` headers and 401 errors.
- Always use `${ES_URL%/}` to strip any trailing slash from the URL, preventing double-slash path issues (e.g., `//_cluster/health`).

## Quick Health Check

```bash
# Cluster health (green/yellow/red) — NOT available on serverless
curl -s "${ES_URL%/}/_cluster/health" -H "Authorization: ApiKey $(printenv ES_API_KEY)" | jq .

# Node stats summary — NOT available on serverless
curl -s "${ES_URL%/}/_cat/nodes?v&h=name,heap.percent,ram.percent,cpu,load_1m,disk.used_percent"  \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)"

# Index overview (works on both serverless and traditional)
curl -s "${ES_URL%/}/_cat/indices?v&s=store.size:desc&h=index,health,status,docs.count,store.size" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)"
```

**Serverless Elasticsearch:** If you get `api_not_available_exception` errors, the cluster is running in serverless mode. The following APIs are **not available** in serverless:
- `_cluster/health`, `_cluster/settings`, `_cluster/allocation/explain`, `_cluster/pending_tasks`
- `_cat/nodes`, `_cat/shards`
- `_nodes/hot_threads`, `_nodes/stats`
- ILM APIs (`_ilm/*`)

Use `_cat/indices` and `_search` APIs as the starting point instead — these work everywhere.

## Search (Query DSL)

```bash
# Simple match query
curl -s "${ES_URL%/}/my-index/_search" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{
    "query": { "match": { "message": "error timeout" } },
    "size": 10
  }' | jq .

# Bool query (must + filter + must_not)
curl -s "${ES_URL%/}/my-index/_search" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{
    "query": {
      "bool": {
        "must": [ { "match": { "message": "error" } } ],
        "filter": [ { "range": { "@timestamp": { "gte": "now-1h" } } } ],
        "must_not": [ { "term": { "level": "debug" } } ]
      }
    },
    "size": 20,
    "sort": [ { "@timestamp": { "order": "desc" } } ]
  }' | jq .
```

For full Query DSL reference (term, terms, range, wildcard, regexp, nested, exists, multi_match, etc.), see [references/query-dsl.md](references/query-dsl.md).

## Index & Document Operations

```bash
# Create index with mappings
curl -s -X PUT "${ES_URL%/}/my-index" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{
    "settings": { "number_of_shards": 1, "number_of_replicas": 1 },
    "mappings": {
      "properties": {
        "message":    { "type": "text" },
        "@timestamp": { "type": "date" },
        "level":      { "type": "keyword" },
        "count":      { "type": "integer" }
      }
    }
  }'

# Index a document (auto-generate ID)
curl -s -X POST "${ES_URL%/}/my-index/_doc" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{ "message": "hello world", "@timestamp": "2026-01-31T12:00:00Z", "level": "info" }'

# Index with specific ID
curl -s -X PUT "${ES_URL%/}/my-index/_doc/doc-123" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{ "message": "specific doc", "level": "warn" }'

# Get document
curl -s "${ES_URL%/}/my-index/_doc/doc-123" -H "Authorization: ApiKey $(printenv ES_API_KEY)" | jq .

# Update document (partial)
curl -s -X POST "${ES_URL%/}/my-index/_update/doc-123" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{ "doc": { "level": "error" } }'

# Delete document
curl -s -X DELETE "${ES_URL%/}/my-index/_doc/doc-123" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)"

# Bulk operations (newline-delimited JSON)
curl -s -X POST "${ES_URL%/}/_bulk" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/x-ndjson" \
  --data-binary @- << 'EOF'
{"index":{"_index":"my-index"}}
{"message":"bulk doc 1","level":"info","@timestamp":"2026-01-31T12:00:00Z"}
{"index":{"_index":"my-index"}}
{"message":"bulk doc 2","level":"warn","@timestamp":"2026-01-31T12:01:00Z"}
EOF
```

## Aggregations

```bash
# Terms aggregation (top values)
curl -s "${ES_URL%/}/my-index/_search?size=0" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{
    "aggs": {
      "levels": { "terms": { "field": "level", "size": 10 } }
    }
  }' | jq '.aggregations'

# Date histogram + nested metric
curl -s "${ES_URL%/}/my-index/_search?size=0" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{
    "query": { "range": { "@timestamp": { "gte": "now-24h" } } },
    "aggs": {
      "over_time": {
        "date_histogram": { "field": "@timestamp", "fixed_interval": "1h" },
        "aggs": {
          "avg_count": { "avg": { "field": "count" } }
        }
      }
    }
  }' | jq '.aggregations'
```

For more aggregation types (cardinality, percentiles, composite, filters, significant_terms, etc.), see [references/aggregations.md](references/aggregations.md).

## Mappings & Index Management

```bash
# Get mapping
curl -s "${ES_URL%/}/my-index/_mapping" -H "Authorization: ApiKey $(printenv ES_API_KEY)" | jq .

# Add field to existing mapping (mappings are additive — you can't change existing field types)
curl -s -X PUT "${ES_URL%/}/my-index/_mapping" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{ "properties": { "new_field": { "type": "keyword" } } }'

# Reindex (change mappings, rename index, etc.)
curl -s -X POST "${ES_URL%/}/_reindex" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{
    "source": { "index": "old-index" },
    "dest":   { "index": "new-index" }
  }'

# Delete index
curl -s -X DELETE "${ES_URL%/}/my-index" -H "Authorization: ApiKey $(printenv ES_API_KEY)"

# Index aliases
curl -s -X POST "${ES_URL%/}/_aliases" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{
    "actions": [
      { "add": { "index": "my-index-v2", "alias": "my-index" } },
      { "remove": { "index": "my-index-v1", "alias": "my-index" } }
    ]
  }'

# Index templates (for time-series / rollover patterns)
curl -s -X PUT "${ES_URL%/}/_index_template/my-template" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{
    "index_patterns": ["logs-*"],
    "template": {
      "settings": { "number_of_shards": 1 },
      "mappings": {
        "properties": {
          "message":    { "type": "text" },
          "@timestamp": { "type": "date" }
        }
      }
    }
  }'
```

## Cluster & Troubleshooting

> **Note:** Most APIs in this section are **not available on serverless** Elasticsearch. They only work on self-managed or traditional Elastic Cloud deployments.

```bash
# Allocation explanation (why is a shard unassigned?) — NOT serverless
curl -s "${ES_URL%/}/_cluster/allocation/explain" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{ "index": "my-index", "shard": 0, "primary": true }' | jq .

# Pending tasks
curl -s "${ES_URL%/}/_cluster/pending_tasks" -H "Authorization: ApiKey $(printenv ES_API_KEY)" | jq .

# Hot threads (performance debugging)
curl -s "${ES_URL%/}/_nodes/hot_threads" -H "Authorization: ApiKey $(printenv ES_API_KEY)"

# Shard allocation
curl -s "${ES_URL%/}/_cat/shards?v&s=store:desc&h=index,shard,prirep,state,docs,store,node" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)"

# Task management (long-running operations)
curl -s "${ES_URL%/}/_tasks?actions=*search&detailed" -H "Authorization: ApiKey $(printenv ES_API_KEY)" | jq .

# Cluster settings (persistent + transient)
curl -s "${ES_URL%/}/_cluster/settings?include_defaults=false" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" | jq .
```

For Kibana API operations (dashboards, data views, saved objects, alerting rules), see [references/kibana-api.md](references/kibana-api.md).

## Data Streams & ILM

> **Note:** ILM APIs (`_ilm/*`) are **not available on serverless**. Data stream listing works on both.

```bash
# List data streams
curl -s "${ES_URL%/}/_data_stream" -H "Authorization: ApiKey $(printenv ES_API_KEY)" | jq .

# Create ILM policy
curl -s -X PUT "${ES_URL%/}/_ilm/policy/my-policy" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{
    "policy": {
      "phases": {
        "hot":    { "actions": { "rollover": { "max_age": "7d", "max_size": "50gb" } } },
        "warm":   { "min_age": "30d", "actions": { "shrink": { "number_of_shards": 1 } } },
        "delete": { "min_age": "90d", "actions": { "delete": {} } }
      }
    }
  }'

# Check ILM status for an index
curl -s "${ES_URL%/}/my-index/_ilm/explain" -H "Authorization: ApiKey $(printenv ES_API_KEY)" | jq .
```

## ES|QL (Elasticsearch Query Language)

For Elasticsearch 8.11+, ES|QL offers a pipe-based query syntax:

```bash
curl -s -X POST "${ES_URL%/}/_query" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "FROM logs-* | WHERE level == \"error\" | STATS count = COUNT(*) BY service.name | SORT count DESC | LIMIT 10"
  }' | jq .
```

For querying OpenTelemetry data (OTEL logs, traces, metrics, correlation patterns), see [references/otel-data.md](references/otel-data.md).

## Ingest Pipelines

```bash
# Create pipeline
curl -s -X PUT "${ES_URL%/}/_ingest/pipeline/my-pipeline" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{
    "processors": [
      { "grok": { "field": "message", "patterns": ["%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} %{GREEDYDATA:msg}"] } },
      { "date": { "field": "timestamp", "formats": ["ISO8601"] } },
      { "remove": { "field": "timestamp" } }
    ]
  }'

# Test pipeline
curl -s -X POST "${ES_URL%/}/_ingest/pipeline/my-pipeline/_simulate" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{
    "docs": [
      { "_source": { "message": "2026-01-31T12:00:00Z ERROR something broke" } }
    ]
  }' | jq .
```

## Tips

- **Always use `jq`** to format JSON output — Elasticsearch responses are verbose.
- **`?size=0`** on search requests when you only want aggregations (skip hits).
- **`_cat` APIs** (`_cat/indices`, `_cat/shards`, `_cat/nodes`) give human-readable tabular output — add `?v` for headers, `?format=json` for JSON.
- **Scroll/PIT for large exports** — don't use `from`/`size` beyond 10,000 hits. Use search_after + PIT instead.
- **Field types matter** — `keyword` for exact match/aggs, `text` for full-text search. Check mappings before querying.
- **Date math in index names** — `logs-{now/d}` resolves to today's date. Useful for time-based indices.
