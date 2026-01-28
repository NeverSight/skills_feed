---
name: lgtm
description: Query observability backends (Loki logs, Prometheus metrics, Tempo traces). Use when user asks about logs, metrics, traces, or debugging production issues. IMPORTANT - Always use haiku subagents to execute queries, never run queries directly.
allowed-tools: Bash, Read, Glob, Task
license: MIT
---

# LGTM Skill - Query Observability Backends

## ⚠️ CRITICAL: DO NOT RUN QUERIES DIRECTLY

**STOP. Before running ANY lgtm command, you MUST spawn a subagent.**

Never run `lgtm` commands directly in the main conversation. Raw JSON responses will bloat context.

### Required Two-Phase Approach

**Phase 1: DISCOVERY (haiku subagent)**

First, discover what's available before querying blindly:

```
Task tool call:
  subagent_type: "Bash"
  model: "haiku"
  prompt: "Using lgtm CLI, discover available labels and services.
    Run: lgtm loki labels
    Run: lgtm loki label-values app
    Run: lgtm loki label-values namespace
    Return: list of available apps, namespaces, and other relevant labels."
```

**Phase 2: INVESTIGATION (haiku subagent)**

After discovery, query with specific filters:

```
Task tool call:
  subagent_type: "Bash"
  model: "haiku"
  prompt: "Using lgtm CLI, investigate errors in the checkout app in prod namespace.
    <specific queries based on discovery results>
    Return ONLY a concise summary."
```

### Orchestrator Pattern

- **Opus (you)**: Coordinate discovery → investigation flow. Evaluate summaries, decide next steps. NEVER execute queries.
- **Haiku subagent**: All query execution - discovery, investigation, analysis. Fast and sufficient for most tasks.
- **Sonnet subagent**: Reserved for complex multi-signal correlation or deep root cause analysis (user must explicitly request).

### Parallel Execution

Run independent queries in parallel - spawn multiple Task calls in one message when queries don't depend on each other (e.g., check logs AND metrics AND traces simultaneously after discovery).

---

## CLI Reference (FOR SUBAGENTS ONLY)

The following commands are for subagents to execute, NOT for direct use in main conversation.

### Prerequisites

The CLI should be available via:
```bash
uvx --from git+https://github.com/pokgak/lgtm-cli lgtm --help
```

### Configuration

Config file: `~/.config/lgtm/config.yaml`

### Loki (Logs)

### Discovery First

```bash
# What labels exist?
lgtm loki labels

# What values for a label?
lgtm loki label-values app
lgtm loki label-values namespace
```

### Query Logs

```bash
# Basic query (defaults: last 15 min, limit 50)
lgtm loki query '{app="myapp"}'

# Filter for errors
lgtm loki query '{app="myapp"} |= "error"'

# With custom time range and limit
lgtm loki query '{app="myapp"}' --start 2024-01-15T10:00:00Z --end 2024-01-15T11:00:00Z --limit 100
```

### Metric Queries (Aggregations)

```bash
# Count errors - use this to get overview first
lgtm loki instant 'count_over_time({app="myapp"} |= "error" [5m])'

# Errors by level
lgtm loki instant 'sum by (level) (count_over_time({app="myapp"} | json [5m]))'
```

## Prometheus/Mimir (Metrics)

### Discovery First

```bash
# What labels exist?
lgtm prom labels

# What metrics exist?
lgtm prom label-values __name__

# Metric metadata
lgtm prom metadata --metric http_requests_total
```

### Query Metrics

```bash
# Instant query
lgtm prom query 'up{job="prometheus"}'

# Rate of requests
lgtm prom query 'rate(http_requests_total[5m])'

# Range query (defaults: last 15 min, 60s step)
lgtm prom range 'rate(http_requests_total[5m])'

# Custom time range
lgtm prom range 'up' --start 2024-01-15T10:00:00Z --end 2024-01-15T11:00:00Z --step 5m
```

## Tempo (Traces)

### Discovery First

```bash
# What tags exist?
lgtm tempo tags

# What services?
lgtm tempo tag-values service.name
```

### Search Traces

```bash
# Search by service (defaults: last 15 min, limit 20)
lgtm tempo search -q '{resource.service.name="api"}'

# Error traces
lgtm tempo search -q '{status=error}'

# Slow traces
lgtm tempo search --min-duration 1s

# Combined filters
lgtm tempo search -q '{resource.service.name="api" && status=error}' --min-duration 500ms
```

### Get Specific Trace

```bash
# When you have a trace ID
lgtm tempo trace abc123def456
```

## Instance Selection

```bash
# Use specific instance
lgtm -i production loki query '{app="api"}'

# List configured instances
lgtm instances
```

## Kubernetes Port-Forward Instances

Some instances require kubectl port-forwarding to access services inside Kubernetes clusters.

### Check if Port-Forward is Required

```bash
# List all instances and their port-forward requirements
lgtm instances

# Show port-forward commands for all instances that need them
lgtm port-forward

# Show port-forward command for specific instance
lgtm -i sandbox port-forward
```

### Using Port-Forward Instances

Before querying an instance that requires port-forwarding, start the tunnel:

```bash
# 1. Get the port-forward command
lgtm -i sandbox port-forward
# Output: kubectl port-forward -n monitoring svc/victoria-metrics-server 8428:8428 --context sandbox

# 2. Start the tunnel (in background or separate terminal)
kubectl port-forward -n monitoring svc/victoria-metrics-server 8428:8428 --context sandbox &

# 3. Query the instance
lgtm -i sandbox prom query 'up'
```

### Subagent Prompt Example for Port-Forward Instances

When querying instances that require port-forwarding:

```
Task tool call:
  subagent_type: "Bash"
  model: "haiku"
  prompt: "Query sandbox cluster metrics using lgtm CLI.

    1. First check if port-forward is needed:
       uvx --from git+https://github.com/pokgak/lgtm-cli lgtm -i sandbox port-forward

    2. If port-forward is needed, start it in background:
       kubectl port-forward -n monitoring svc/victoria-metrics-server 8428:8428 --context sandbox &
       sleep 2  # Wait for tunnel to establish

    3. Run the query:
       uvx --from git+https://github.com/pokgak/lgtm-cli lgtm -i sandbox prom query 'sandbox_running_count'

    4. Return a summary of the results."
```

## Best Practices Workflow

### 1. Discover → Filter → Query

```bash
# Step 1: What's available?
lgtm loki labels
lgtm loki label-values app

# Step 2: Get overview with aggregation
lgtm loki instant 'sum by (app) (count_over_time({namespace="prod"} |= "error" [15m]))'

# Step 3: Narrow down to specific app
lgtm loki query '{namespace="prod", app="checkout"} |= "error"' --limit 20
```

### 2. Use Specific Identifiers

```bash
# If you have a trace ID, fetch directly
lgtm tempo trace abc123def456

# Filter logs by request ID
lgtm loki query '{app="api"} |= "request_id=abc123"'

# Filter by pod name
lgtm loki query '{pod="api-server-xyz123"}'
```

### 3. Aggregations Over Raw Data

```bash
# BAD: Fetching all error logs
lgtm loki query '{app="api"} |= "error"'

# GOOD: Count first, then drill down
lgtm loki instant 'count_over_time({app="api"} |= "error" [5m])'
```

## Subagent Prompt Examples

**Example: Discovery (run this FIRST)**

Use Task tool with `subagent_type: "Bash"` and `model: "haiku"`:
```
Discover available observability data using lgtm CLI.

1. Get Loki labels: lgtm loki labels
2. Get app values: lgtm loki label-values app
3. Get namespace values: lgtm loki label-values namespace
4. Get Tempo services: lgtm tempo tag-values service.name

Return a concise list:
- Available apps: [list]
- Available namespaces: [list]
- Available services in traces: [list]
- Any other relevant labels discovered
```

**Example: Investigate Error Spike (after discovery)**

Use Task tool with `subagent_type: "Bash"` and `model: "haiku"`:
```
Investigate errors in the checkout service over the last hour using the lgtm CLI.

1. First get error counts: lgtm loki instant 'sum by (level) (count_over_time({app="checkout"} | json [1h]))'
2. If errors found, get sample logs: lgtm loki query '{app="checkout"} |= "error"' --limit 30
3. Check for related traces: lgtm tempo search -q '{resource.service.name="checkout" && status=error}'

Summarize findings:
- Total error count and trend (up/down from normal)
- Top 3 most frequent error messages
- When the errors started
- Affected components/pods
- Any correlated trace IDs for debugging

Return ONLY the summary, not raw JSON output.
```

**Example: Service Health Check**

Use Task tool with `subagent_type: "Bash"` and `model: "haiku"`:
```
Check health of the payment-service using lgtm CLI.

1. Error rate: lgtm loki instant 'sum(count_over_time({app="payment-service"} |= "error" [15m]))'
2. Request latency: lgtm prom query 'histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{service="payment"}[5m]))'
3. Recent errors: lgtm loki query '{app="payment-service"} |= "error"' --limit 10

Return a brief health summary:
- Status: healthy/degraded/unhealthy
- Error rate (errors per minute)
- P95 latency
- Any critical issues found
```

**Example: Trace Investigation**

Use Task tool with `subagent_type: "Bash"` and `model: "haiku"`:
```
Investigate slow requests in the API gateway using lgtm CLI.

1. Find slow traces: lgtm tempo search -q '{resource.service.name="api-gateway"}' --min-duration 2s --limit 10
2. For the slowest trace, get details: lgtm tempo trace <traceID>
3. Check if downstream services are slow: lgtm tempo search -q '{resource.service.name="api-gateway"} >> {duration > 1s}'

Summarize:
- How many slow requests in the last 15 min
- Which downstream service is causing delays
- Common patterns in slow requests
```

**NEVER paste raw JSON output into the main conversation.** The subagent processes all data and returns only a concise summary. This is critical for maintaining context efficiency.

## Output Formatting

All commands output JSON. Use `jq` for formatting:

```bash
# Extract just log lines
lgtm loki query '{app="api"}' | jq -r '.data.result[].values[][] | select(type == "string")'

# Extract metric values
lgtm prom query 'up' | jq -r '.data.result[] | "\(.metric.instance): \(.value[1])"'

# Trace summary
lgtm tempo search -q '{status=error}' | jq -r '.traces[] | "\(.traceID) | \(.rootServiceName) | \(.durationMs)ms"'
```

## Reference

For query syntax, see:
- `reference/logql.md` - LogQL syntax for Loki
- `reference/promql.md` - PromQL syntax for Prometheus
- `reference/traceql.md` - TraceQL syntax for Tempo
