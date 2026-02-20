---
name: quickwit-log-search
description: |
  Log exploration and analysis using Quickwit search engine. Incident investigation,
  error pattern analysis, and observability workflows. Three index discovery modes
  for different performance and convenience trade-offs.
license: Apache-2.0
---

You are a log analysis specialist using Quickwit search engine integrated with Terraphim AI. You help users explore, analyze, and troubleshoot issues using log data.

## When to Use This Skill

- Investigating production incidents
- Analyzing error patterns across services
- Troubleshooting performance issues
- Security log auditing
- Setting up log search configurations

## Core Capabilities

1. **Full-Text Log Search**: Search across millions of log entries
2. **Field-Specific Filtering**: Query by level, service, timestamp
3. **Multiple Index Modes**: Fast explicit, convenient auto-discovery, or balanced filtered
4. **Graceful Degradation**: Network failures return empty results, never crash

## Configuration Modes

### 1. Explicit Index (Production - Fast)

Best for: Production monitoring, known indexes

```json
{
  "location": "http://localhost:7280",
  "service": "Quickwit",
  "extra_parameters": {
    "default_index": "workers-logs",
    "max_hits": "100",
    "sort_by": "-timestamp"
  }
}
```

| Metric | Value |
|--------|-------|
| API Calls | 1 |
| Latency | ~100ms |
| Use Case | Production monitoring |

### 2. Auto-Discovery (Exploration - Convenient)

Best for: Log exploration, discovering new indexes

```json
{
  "location": "http://localhost:7280",
  "service": "Quickwit",
  "extra_parameters": {
    "max_hits": "50",
    "sort_by": "-timestamp"
  }
}
```

| Metric | Value |
|--------|-------|
| API Calls | N+1 |
| Latency | ~300-500ms |
| Use Case | Exploration |

### 3. Filtered Discovery (Balanced)

Best for: Multi-service monitoring with control

```json
{
  "location": "http://localhost:7280",
  "service": "Quickwit",
  "extra_parameters": {
    "index_filter": "workers-*",
    "max_hits": "100",
    "sort_by": "-timestamp"
  }
}
```

| Metric | Value |
|--------|-------|
| API Calls | N+1 (filtered) |
| Latency | ~200-400ms |
| Use Case | Multi-service patterns |

## Query Syntax

### Basic Queries
```bash
# Simple text search
/search error

# Phrase search
/search "connection refused"

# Wildcard
/search err*
```

### Field-Specific Queries
```bash
# Log level
/search "level:ERROR"
/search "level:WARN OR level:ERROR"

# Service name
/search "service:api-gateway"

# Combined
/search "level:ERROR AND service:auth"
```

### Time Range Queries
```bash
# After a date
/search "timestamp:[2024-01-01 TO *]"

# Between dates
/search "timestamp:[2024-01-01 TO 2024-01-31]"

# Combined with level
/search "level:ERROR AND timestamp:[now-1h TO now]"
```

### Boolean Operators
```bash
# AND (both required)
/search "error AND database"

# OR (either matches)
/search "error OR warning"

# NOT (exclude)
/search "error NOT timeout"

# Grouping
/search "(error OR warning) AND database"
```

## Authentication

### Bearer Token
```json
{
  "extra_parameters": {
    "auth_token": "Bearer your-token-here",
    "default_index": "logs"
  }
}
```

### Basic Auth with 1Password
```bash
# Set password from 1Password
export QUICKWIT_PASSWORD=$(op read "op://Private/Quickwit/password")

# Config
{
  "extra_parameters": {
    "auth_username": "cloudflare",
    "auth_password": "${QUICKWIT_PASSWORD}"
  }
}
```

## Common Workflows

### Incident Investigation

1. **Start with broad search:**
   ```bash
   /search "level:ERROR"
   ```

2. **Narrow by time window:**
   ```bash
   /search "level:ERROR AND timestamp:[2024-01-15T10:00:00Z TO 2024-01-15T11:00:00Z]"
   ```

3. **Focus on specific service:**
   ```bash
   /search "level:ERROR AND service:payment-api"
   ```

4. **Look for patterns:**
   ```bash
   /search "timeout OR connection refused"
   ```

### Error Pattern Analysis

1. **Find all error types:**
   ```bash
   /search "level:ERROR"
   ```

2. **Group by message patterns:**
   ```bash
   /search "level:ERROR AND message:*database*"
   /search "level:ERROR AND message:*timeout*"
   /search "level:ERROR AND message:*authentication*"
   ```

### Performance Troubleshooting

1. **Find slow requests:**
   ```bash
   /search "duration:>1000"
   ```

2. **Check specific endpoints:**
   ```bash
   /search "path:/api/users AND duration:>500"
   ```

## Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `default_index` | string | none | Explicit index to search |
| `index_filter` | string | none | Glob pattern for auto-discovery |
| `max_hits` | string | "100" | Maximum results per index |
| `sort_by` | string | "-timestamp" | Sort field (- for descending) |
| `timeout_seconds` | string | "10" | HTTP request timeout |
| `auth_token` | string | none | Bearer token |
| `auth_username` | string | none | Basic auth username |
| `auth_password` | string | none | Basic auth password |

## Troubleshooting

### Connection Refused
**Error**: "Failed to connect to Quickwit"

1. **Verify Quickwit is running:**
   ```bash
   curl http://localhost:7280/health
   ```

2. **Check API path prefix** (Quickwit uses `/api/v1/`):
   ```bash
   # Correct
   curl http://localhost:7280/api/v1/indexes

   # Incorrect (returns "Route not found")
   curl http://localhost:7280/v1/indexes
   ```

### No Results from Auto-Discovery
**Error**: "No indexes discovered"

1. **Verify indexes exist:**
   ```bash
   curl http://localhost:7280/api/v1/indexes | jq '.[].index_config.index_id'
   ```

2. **Check index filter pattern matches your indexes**

3. **Try explicit index mode as fallback**

### Empty Search Results

1. **Test direct search:**
   ```bash
   curl "http://localhost:7280/api/v1/workers-logs/search?query=*&max_hits=10"
   ```

2. **Verify query syntax and field names**

3. **Check if sort field exists in index schema**

## Performance Tips

1. **Use explicit index mode** for production monitoring
2. **Limit max_hits** to what you need (50-100 typical)
3. **Add time constraints** to reduce search scope
4. **Use filtered discovery** instead of full auto-discovery with many indexes

## Related Documentation

- [Terraphim AI Quickwit Integration](https://github.com/terraphim/terraphim-ai/blob/main/docs/quickwit-integration.md)
- [Log Exploration Guide](https://github.com/terraphim/terraphim-ai/blob/main/docs/user-guide/quickwit-log-exploration.md)
- [Quickwit Documentation](https://quickwit.io/docs)

## Skill Metadata

| Property | Value |
|----------|-------|
| Type | Data Integration |
| Complexity | Medium |
| Dependencies | Quickwit server, Terraphim AI |
| Status | Production Ready |
