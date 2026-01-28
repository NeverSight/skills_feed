---
name: searching-mlflow-traces
description: Searches and filters MLflow traces using CLI or Python API. Use when the user asks to find traces, filter traces by status/tags/metadata/execution time, query traces, or debug failed traces. Triggers on "search traces", "find failed traces", "filter traces by", "traces slower than", "query MLflow traces".
---

# Searching MLflow Traces

## Trace Data Structure

- **TraceInfo**: `trace_id`, `status` (OK/ERROR), `timestamp_ms`, `execution_time_ms`, `tags`, `metadata`, `assessments` (human feedback, evaluation results)
- **Spans**: Tree of operations with `name`, `type`, `attributes`, `start_time`, `end_time`

## Workflow

1. **Check CLI usage** (required): `mlflow traces search --help`
2. **Build filter query** using syntax below
3. **Execute search** with appropriate flags
4. **Retrieve details** for specific traces if needed

## Step 1: Check CLI Usage

```bash
mlflow traces search --help
```

Always run this first to get accurate flags for the installed MLflow version.

## Step 2-3: Search Examples

```bash
# By status
mlflow traces search --experiment-id 1 --filter-string-string "trace.status = 'ERROR'"

# Output format (table or json)
mlflow traces search --experiment-id 1 --output json

# Include span details
mlflow traces search --experiment-id 1 --include-spans

# Order results
mlflow traces search --experiment-id 1 --order-by "timestamp_ms DESC"

# Pagination
mlflow traces search --experiment-id 1 --max-results 50 --page-token <token>

# Time range filter (timestamps in milliseconds since epoch)
# Get current time in ms: $(date +%s)000
# Last hour: $(( $(date +%s)000 - 3600000 ))
mlflow traces search --experiment-id 1 --filter-string "trace.timestamp_ms > $(( $(date +%s)000 - 3600000 ))"

# By execution time (slow traces > 1 second)
mlflow traces search --experiment-id 1 --filter-string "trace.execution_time_ms > 1000"

# By tag
mlflow traces search --experiment-id 1 --filter-string "tag.environment = 'production'"

# Escape special characters in tag/metadata names with backticks
mlflow traces search --experiment-id 1 --filter-string "tag.\`model-name\` = 'gpt-4'"
mlflow traces search --experiment-id 1 --filter-string "metadata.\`user.id\` = 'abc'"

# By metadata
mlflow traces search --experiment-id 1 --filter-string "metadata.user_id = 'user_123'"

# By assessment
mlflow traces search --experiment-id 1 --filter-string "feedback.rating = 'positive'"

# Combine conditions (AND only, no OR)
mlflow traces search --experiment-id 1 --filter-string "trace.status = 'ERROR' AND trace.execution_time_ms > 500"

# Full text search
mlflow traces search --experiment-id 1 --filter-string "trace.text LIKE '%error%'"

# Limit results
mlflow traces search --experiment-id 1 --filter-string "trace.status = 'OK'" --max-results 10
```

## Step 4: Retrieve Single Trace

```bash
mlflow traces get --trace-id <trace_id>
```

## Filter Syntax

For detailed syntax, fetch from documentation:
```
WebFetch(
  url: "https://mlflow.org/docs/latest/genai/tracing/search-traces.md",
  prompt: "Extract the filter syntax table showing supported fields, operators, and examples."
)
```

**Common filters:**
- `trace.status`: OK, ERROR, IN_PROGRESS
- `trace.execution_time_ms`, `trace.timestamp_ms`: numeric comparison
- `tag.<key>`, `metadata.<key>`: exact match or pattern
- `span.name`, `span.type`: exact match or pattern
- `feedback.<name>`, `expectation.<name>`: assessments

**Pattern operators:** `LIKE`, `ILIKE` (case-insensitive), `RLIKE` (regex)

## Python API

For `mlflow.search_traces()`, see: https://mlflow.org/docs/latest/genai/tracing/search-traces.md
