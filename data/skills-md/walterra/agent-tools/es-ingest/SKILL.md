---
name: es-ingest
description: Ingest and transform large data files (CSV/JSON) into Elasticsearch indices. Stream-based processing for files up to 30GB, cross-version migration (ES 8.x ↔ 9.x), custom JavaScript transformations, and reindexing with transforms. Use when you need to load data into Elasticsearch, migrate indices, or transform data during ingestion.
metadata:
  version: "0.0.1"
  author: walterra
  repository: https://github.com/walterra/agent-tools
---

# ES Ingest

Stream-based ingestion and transformation of large data files into Elasticsearch. Built on [node-es-transformer](https://github.com/walterra/node-es-transformer).

## Features

- ✅ **Stream-based**: Handle very large files (20-30 GB tested) without running out of memory
- ✅ **High throughput**: Up to 20k documents/second on commodity hardware
- ✅ **Cross-version**: Seamlessly migrate between ES 8.x and 9.x
- ✅ **Formats**: NDJSON, CSV, Parquet, Arrow IPC
- ✅ **Transformations**: Apply custom JavaScript transforms during ingestion
- ✅ **Reindexing**: Copy and transform existing indices
- ✅ **Wildcards**: Ingest multiple files matching a pattern (e.g., `logs/*.json`)
- ✅ **Document splitting**: Transform one source document into multiple targets

## Prerequisites

- **Elasticsearch 8.x or 9.x** accessible (local or remote)
- **Node.js 22+** installed

## Setup

Before first use, install dependencies:

```bash
cd {baseDir} && npm install
```

## Basic Usage

### Ingest a JSON file

```bash
{baseDir}/scripts/ingest.js --file data.json --target my-index
```

### Stream NDJSON/CSV via stdin

```bash
# NDJSON
cat data.ndjson | {baseDir}/scripts/ingest.js --stdin --target my-index

# CSV
cat data.csv | {baseDir}/scripts/ingest.js --stdin --source-format csv --target my-index
```

### Ingest CSV directly

```bash
{baseDir}/scripts/ingest.js --file users.csv --source-format csv --target users
```

### Ingest Parquet directly

```bash
{baseDir}/scripts/ingest.js --file users.parquet --source-format parquet --target users
```

### Ingest Arrow IPC directly

```bash
{baseDir}/scripts/ingest.js --file users.arrow --source-format arrow --target users
```

> CSV/Parquet/Arrow support requires node-es-transformer >= 1.2.0.

### Ingest CSV with parser options

```bash
# csv-options.json
# {
#   "columns": true,
#   "delimiter": ";",
#   "trim": true
# }

{baseDir}/scripts/ingest.js --file users.csv --source-format csv --csv-options csv-options.json --target users
```

### Infer mappings/pipeline from CSV

```bash
{baseDir}/scripts/ingest.js --file users.csv --source-format csv --infer-mappings --target users
```

### Infer mappings with options

```bash
# infer-options.json
# {
#   "sampleBytes": 200000,
#   "lines_to_sample": 2000
# }

{baseDir}/scripts/ingest.js --file users.csv --source-format csv --infer-mappings --infer-mappings-options infer-options.json --target users
```

### Ingest with custom mappings

```bash
{baseDir}/scripts/ingest.js --file data.json --target my-index --mappings mappings.json
```

### Ingest with transformation

```bash
{baseDir}/scripts/ingest.js --file data.json --target my-index --transform transform.js
```

### Reindex from another index

```bash
{baseDir}/scripts/ingest.js --source-index old-index --target new-index
```

### Cross-cluster reindex (ES 8.x → 9.x)

```bash
{baseDir}/scripts/ingest.js --source-index logs \
  --node https://es8.example.com:9200 --api-key es8-key \
  --target new-logs \
  --target-node https://es9.example.com:9200 --target-api-key es9-key
```

## Command Reference

### Required Options

```bash
--target <index>         # Target index name
```

### Source Options (choose one)

```bash
--file <path>            # Source file (supports wildcards, e.g., logs/*.json)
--source-index <name>    # Source Elasticsearch index
--stdin                  # Read NDJSON/CSV from stdin
```

### Elasticsearch Connection

```bash
--node <url>             # ES node URL (default: http://localhost:9200)
--api-key <key>          # API key authentication
--username <user>        # Basic auth username
--password <pass>        # Basic auth password
```

### Target Connection (for cross-cluster)

```bash
--target-node <url>      # Target ES node URL (uses --node if not specified)
--target-api-key <key>   # Target API key
--target-username <user> # Target username
--target-password <pass> # Target password
```

### Index Configuration

```bash
--mappings <file.json>          # Mappings file (auto-copy from source if reindexing)
--infer-mappings                # Infer mappings/pipeline from file/stream
--infer-mappings-options <file> # Options for inference (JSON file)
--delete-index                  # Delete target index if exists
--pipeline <name>               # Ingest pipeline name
```

### Processing

```bash
--transform <file.js>    # Transform function (export as default or module.exports)
--query <file.json>      # Query file to filter source documents
--source-format <fmt>    # Source format: ndjson|csv|parquet|arrow (default: ndjson)
--csv-options <file>     # CSV parser options (JSON file)
--skip-header            # Skip first line (e.g., CSV header)
```

### Performance

```bash
--buffer-size <kb>       # Buffer size in KB (default: 5120)
--search-size <n>        # Docs per search when reindexing (default: 100)
--total-docs <n>         # Total docs for progress bar (file/stream)
--stall-warn-seconds <n> # Stall warning threshold (default: 30)
--progress-mode <mode>   # Progress output: auto|line|newline (default: auto)
--debug-events           # Log pause/resume/stall events
--quiet                  # Disable progress bars
```

## Transform Functions

Transform functions let you modify documents during ingestion. Create a JavaScript file that exports a transform function:

### Basic Transform (transform.js)

```javascript
// ES modules (default)
export default function transform(doc) {
  return {
    ...doc,
    full_name: `${doc.first_name} ${doc.last_name}`,
    timestamp: new Date().toISOString(),
  };
}

// Or CommonJS
module.exports = function transform(doc) {
  return {
    ...doc,
    full_name: `${doc.first_name} ${doc.last_name}`,
  };
};
```

### Skip Documents

Return `null` or `undefined` to skip a document:

```javascript
export default function transform(doc) {
  // Skip invalid documents
  if (!doc.email || !doc.email.includes('@')) {
    return null;
  }
  return doc;
}
```

### Split Documents

Return an array to create multiple target documents from one source:

```javascript
export default function transform(doc) {
  // Split a tweet into multiple hashtag documents
  const hashtags = doc.text.match(/#\w+/g) || [];
  return hashtags.map(tag => ({
    hashtag: tag,
    tweet_id: doc.id,
    created_at: doc.created_at,
  }));
}
```

## Mappings

### Auto-Copy Mappings (Reindexing)

When reindexing, mappings are automatically copied from the source index:

```bash
{baseDir}/scripts/ingest.js --source-index old-logs --target new-logs
```

### Custom Mappings (mappings.json)

```json
{
  "properties": {
    "@timestamp": { "type": "date" },
    "message": { "type": "text" },
    "user": {
      "properties": {
        "name": { "type": "keyword" },
        "email": { "type": "keyword" }
      }
    }
  }
}
```

```bash
{baseDir}/scripts/ingest.js --file data.json --target my-index --mappings mappings.json
```

## Query Filters

Filter source documents during reindexing with a query file:

### Query File (filter.json)

```json
{
  "range": {
    "@timestamp": {
      "gte": "2024-01-01",
      "lt": "2024-02-01"
    }
  }
}
```

```bash
{baseDir}/scripts/ingest.js \
  --source-index logs \
  --target filtered-logs \
  --query filter.json
```

## Common Patterns

### Pattern 1: Load CSV with custom mappings

```bash
# 1. Create mappings.json with your schema
cat > mappings.json << 'EOF'
{
  "properties": {
    "timestamp": { "type": "date" },
    "user_id": { "type": "keyword" },
    "action": { "type": "keyword" },
    "value": { "type": "double" }
  }
}
EOF

# 2. Ingest CSV (skip header row)
{baseDir}/scripts/ingest.js \
  --file events.csv \
  --target events \
  --mappings mappings.json \
  --skip-header
```

### Pattern 2: Migrate ES 8.x → 9.x with transforms

```bash
# 1. Create transform.js to update document structure
cat > transform.js << 'EOF'
export default function transform(doc) {
  // Update field names for ES 9.x compatibility
  return {
    ...doc,
    '@timestamp': doc.timestamp,  // Rename field
    user: {
      id: doc.user_id,
      name: doc.user_name,
    },
  };
}
EOF

# 2. Migrate with transform
{baseDir}/scripts/ingest.js \
  --source-index logs \
  --node https://es8-cluster.example.com:9200 \
  --api-key $ES8_API_KEY \
  --target logs-v2 \
  --target-node https://es9-cluster.example.com:9200 \
  --target-api-key $ES9_API_KEY \
  --transform transform.js
```

### Pattern 3: Reindex with filtering and deletion

```bash
# 1. Create filter query
cat > filter.json << 'EOF'
{
  "bool": {
    "must": [
      { "range": { "@timestamp": { "gte": "now-30d" } } }
    ],
    "must_not": [
      { "term": { "status": "deleted" } }
    ]
  }
}
EOF

# 2. Reindex with filter (delete old index first)
{baseDir}/scripts/ingest.js \
  --source-index logs-raw \
  --target logs-filtered \
  --query filter.json \
  --delete-index
```

### Pattern 4: Batch ingest multiple files

```bash
# Ingest all JSON files in a directory
{baseDir}/scripts/ingest.js \
  --file "logs/*.json" \
  --target combined-logs \
  --mappings mappings.json
```

### Pattern 5: Document enrichment during ingestion

```bash
# 1. Create enrichment transform
cat > enrich.js << 'EOF'
export default function transform(doc) {
  return {
    ...doc,
    enriched_at: new Date().toISOString(),
    source: 'batch-import',
    year: new Date(doc.timestamp).getFullYear(),
  };
}
EOF

# 2. Ingest with enrichment
{baseDir}/scripts/ingest.js \
  --file data.json \
  --target enriched-data \
  --transform enrich.js
```

## Performance Tuning

### For Large Files (>5GB)

```bash
# Increase buffer size for better throughput
{baseDir}/scripts/ingest.js \
  --file huge-file.json \
  --target my-index \
  --buffer-size 10240  # 10 MB buffer
```

### For Slow Networks

```bash
# Reduce batch size to avoid timeouts
{baseDir}/scripts/ingest.js \
  --source-index remote-logs \
  --target local-logs \
  --search-size 50  # Smaller batches
```

### Quiet Mode (for scripts)

```bash
# Disable progress bars for automated scripts
{baseDir}/scripts/ingest.js \
  --file data.json \
  --target my-index \
  --quiet
```

## When to Use

Use this skill when you need to:

- **Load large files** into Elasticsearch without memory issues
- **Migrate indices** between ES versions (8.x ↔ 9.x)
- **Transform data** during ingestion (enrich, split, filter)
- **Reindex with modifications** (rename fields, restructure documents)
- **Batch process** multiple files matching a pattern
- **Cross-cluster replication** with transformations

## When NOT to Use

Consider alternatives for:

- **Real-time ingestion**: Use [Filebeat](https://www.elastic.co/beats/filebeat) or [Elastic Agent](https://www.elastic.co/guide/en/fleet/current/fleet-overview.html)
- **Enterprise pipelines**: Use [Logstash](https://www.elastic.co/products/logstash)
- **Built-in transforms**: Use [Elasticsearch Transforms](https://www.elastic.co/guide/en/elasticsearch/reference/current/transforms.html)
- **Small files (<100MB)**: Direct Elasticsearch API calls may be simpler

## Troubleshooting

### Connection refused

Elasticsearch is not running or URL is incorrect:

```bash
# Test connection
curl http://localhost:9200

# Or with auth
curl -H "Authorization: ApiKey $API_KEY" https://es.example.com:9200
```

### Out of memory errors

Reduce buffer size:

```bash
{baseDir}/scripts/ingest.js --file data.json --target my-index --buffer-size 2048
```

### Transform function not loading

Ensure the transform file exports correctly:

```javascript
// ✓ Correct (ES modules)
export default function transform(doc) { /* ... */ }

// ✓ Correct (CommonJS)
module.exports = function transform(doc) { /* ... */ }

// ✗ Wrong
function transform(doc) { /* ... */ }
```

### Mapping conflicts

Delete and recreate the index:

```bash
{baseDir}/scripts/ingest.js \
  --file data.json \
  --target my-index \
  --mappings mappings.json \
  --delete-index
```

## References

- [node-es-transformer GitHub](https://github.com/walterra/node-es-transformer)
- [Elasticsearch Mappings](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html)
- [Elasticsearch Query DSL](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html)
- [Performance Tuning Guide](https://github.com/walterra/node-es-transformer/blob/main/PERFORMANCE.md)
