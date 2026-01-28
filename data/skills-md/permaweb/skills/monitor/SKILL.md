---
name: monitor
description: Node.js CLI for interacting with the AO Task Monitor API - get system health, alerts, logs, and task metrics for AO processes
license: MIT
compatibility: node
metadata:
  audience: developers
  workflow: monitoring
  runtime: Node.js 18+
---

# AO Monitor CLI

A Node.js command-line interface for the AO Task Monitor service. Query system health, view alerts, analyze logs, and monitor AO process performance.

## Overview

- **Location**: `skills/monitor/index.mjs`
- **Runtime**: Node.js 18+
- **Dependencies**: None (uses built-in fetch)
- **Default API**: `https://ao-task-monitor.onrender.com`

## When to Use

Use this CLI when you need to:
- Monitor AO process health and performance
- Check for system alerts or failing tasks
- View and filter execution logs
- Analyze task metrics and success rates
- Troubleshoot AO process issues
- Get quick status updates on AO processes

## Authentication Setup

The CLI requires an API key set via environment variable.

### Get Your API Key

Contact the AO Task Monitor service administrator to obtain your API key.

### Configure Environment

**For zsh (~/.zshrc):**
```bash
# Add to ~/.zshrc
export AO_MONITOR_KEY="YOUR_KEY_HERE"

# Reload
source ~/.zshrc
```

**For bash (~/.bashrc):**
```bash
# Add to ~/.bashrc
export AO_MONITOR_KEY="YOUR_KEY_HERE"

# Reload
source ~/.bashrc
```

**Temporary (current session only):**
```bash
export AO_MONITOR_KEY="YOUR_KEY_HERE"
```

**Per-command override:**
```bash
node skills/monitor/index.mjs summary --token "YOUR_KEY_HERE"
```

## Commands

### summary

Get a system-wide overview of all monitored tasks.

```bash
node skills/monitor/index.mjs summary
```

**Options:**
- `--period <1h|4h|8h|24h|48h>` - Time window for metrics
- `--include <csv>` - Fields to include (e.g., `counts,kpis,latency`)
- `--format <json|text>` - Response format (default: json)

**Examples:**
```bash
# Default summary
node skills/monitor/index.mjs summary

# Last 24 hours, text format
node skills/monitor/index.mjs summary --period 24h --format text

# Only counts and KPIs
node skills/monitor/index.mjs summary --include counts,kpis
```

### task

Get detailed metrics for a specific task.

```bash
node skills/monitor/index.mjs task <taskId>
```

**Options:**
- `--period <1h|4h|8h|24h|48h>` - Time window for metrics
- `--include <csv>` - Fields to include
- `--format <json|text>` - Response format

**Examples:**
```bash
# Get ao-token-info task details
node skills/monitor/index.mjs task ao-token-info

# With 48-hour window and text output
node skills/monitor/index.mjs task ao-token-info --period 48h --format text
```

### alerts

View current system alerts and issues.

```bash
node skills/monitor/index.mjs alerts
```

**Options:**
- `--period <1h|4h|8h|24h|48h>` - Time window for alerts
- `--format <json|text>` - Response format

**Examples:**
```bash
# Current alerts
node skills/monitor/index.mjs alerts

# Last 4 hours, text format
node skills/monitor/index.mjs alerts --period 4h --format text
```

### logs

View execution logs, optionally filtered by task.

```bash
# All logs
node skills/monitor/index.mjs logs

# Task-specific logs
node skills/monitor/index.mjs logs <taskId>
```

**Options:**
- `--limit <n>` - Maximum results (default: 100, max: 1000)
- `--offset <n>` - Pagination offset
- `--status <success|failure|timeout>` - Filter by execution status
- `--error-type <string>` - Filter by error message substring
- `--since <isoTimestamp>` - Logs after this time
- `--until <isoTimestamp>` - Logs before this time
- `--task-id <taskId>` - Filter by task ID (alternative to positional arg)

**Examples:**
```bash
# Recent logs
node skills/monitor/index.mjs logs

# Task-specific logs
node skills/monitor/index.mjs logs ao-token-info

# Failed executions only
node skills/monitor/index.mjs logs --status failure

# Logs with 503 errors
node skills/monitor/index.mjs logs --error-type 503

# Last 50 logs since yesterday
node skills/monitor/index.mjs logs --limit 50 --since 2024-01-01T00:00:00Z

# Paginated results
node skills/monitor/index.mjs logs --limit 100 --offset 100
```

### docs

Retrieve API documentation from the server.

```bash
node skills/monitor/index.mjs docs
```

### request

Make a generic API request for endpoints not covered by other commands.

```bash
node skills/monitor/index.mjs request <endpoint> <method> [body]
```

**Arguments:**
- `endpoint` - API path (e.g., `/v1/summary`)
- `method` - HTTP method (GET, POST, PUT, DELETE)
- `body` - JSON body for POST/PUT requests (optional)

**Examples:**
```bash
# GET request
node skills/monitor/index.mjs request /v1/summary GET

# GET with query params
node skills/monitor/index.mjs request "/v1/summary?format=text" GET

# POST with JSON body
node skills/monitor/index.mjs request /v1/api/agent POST '{"task_id":"123","status":"running"}'

# PUT request
node skills/monitor/index.mjs request /v1/api/agent/456 PUT '{"name":"Updated Agent"}'
```

## Global Options

These options work with all commands:

| Option | Description |
|--------|-------------|
| `--base-url <url>` | Override API base URL |
| `--token <token>` | Override auth token (instead of AO_MONITOR_KEY) |
| `--timeout-ms <ms>` | Request timeout in milliseconds (default: 30000) |
| `--help, -h` | Show help message |

**Examples:**
```bash
# Use different API server
node skills/monitor/index.mjs summary --base-url https://my-monitor.example.com

# Override token for single request
node skills/monitor/index.mjs alerts --token "different_key"

# Longer timeout for slow connections
node skills/monitor/index.mjs logs --timeout-ms 60000
```

## Query Parameters Reference

### For summary, task, alerts

| Parameter | Values | Description |
|-----------|--------|-------------|
| `--period` | `1h`, `4h`, `8h`, `24h`, `48h` | Time window for metrics |
| `--include` | CSV of fields | Fields to include in response |
| `--format` | `json`, `text` | Response format |

**Include field options:**
- `counts` - Execution counts
- `kpis` - Key performance indicators
- `latency` - Response time metrics

### For logs

| Parameter | Type | Description |
|-----------|------|-------------|
| `--limit` | integer | Max results (1-1000, default: 100) |
| `--offset` | integer | Pagination offset |
| `--status` | string | `success`, `failure`, or `timeout` |
| `--error-type` | string | Filter by error substring |
| `--since` | ISO timestamp | Logs after this time |
| `--until` | ISO timestamp | Logs before this time |
| `--task-id` | string | Filter by task ID |

## Common Use Cases

### Check System Health

```bash
# Quick overview
node skills/monitor/index.mjs summary --format text

# Check for any alerts
node skills/monitor/index.mjs alerts
```

### Investigate Task Failures

```bash
# See if task has issues
node skills/monitor/index.mjs task ao-token-info --period 24h

# Get recent failures
node skills/monitor/index.mjs logs ao-token-info --status failure --limit 20

# Search for specific error
node skills/monitor/index.mjs logs --error-type "503" --limit 50
```

### View Recent Activity

```bash
# Last 100 logs
node skills/monitor/index.mjs logs

# Last hour of logs
node skills/monitor/index.mjs logs --since "$(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ)"

# Successful runs only
node skills/monitor/index.mjs logs --status success --limit 50
```

### Monitor Specific Task

```bash
# Task metrics
node skills/monitor/index.mjs task ao-token-info --include counts,kpis,latency

# Task logs
node skills/monitor/index.mjs logs ao-token-info --limit 50
```

### Debug Timeouts

```bash
# Find timeout issues
node skills/monitor/index.mjs logs --status timeout

# Check latency metrics
node skills/monitor/index.mjs summary --include latency
```

## Error Handling

### Missing Authentication

If `AO_MONITOR_KEY` is not set and no `--token` provided:
```
Error: No authentication token provided.

Set the AO_MONITOR_KEY environment variable:
  export AO_MONITOR_KEY="your_key_here"

Or use the --token flag:
  node skills/monitor/index.mjs summary --token "your_key_here"
```

### Authentication Failures

**401 Unauthorized** or **403 Forbidden**:
- Verify your `AO_MONITOR_KEY` is correct
- Check if the key has expired
- Ensure the key has access to the requested resource

### API Errors

Non-2xx responses display:
- HTTP status code
- Error message from server

```
Error: Request failed with status 404
Not Found: Task 'invalid-task' does not exist
```

### Network/Timeout Errors

- Default timeout is 30 seconds
- Increase with `--timeout-ms` for slow connections
- Check network connectivity if requests fail

## Examples Cheatsheet

```bash
# System overview
node skills/monitor/index.mjs summary

# Text format summary
node skills/monitor/index.mjs summary --format text

# Last 24h summary
node skills/monitor/index.mjs summary --period 24h

# Check alerts
node skills/monitor/index.mjs alerts

# Task details
node skills/monitor/index.mjs task ao-token-info

# Recent logs
node skills/monitor/index.mjs logs

# Task logs
node skills/monitor/index.mjs logs ao-token-info

# Failed runs
node skills/monitor/index.mjs logs --status failure

# Search errors
node skills/monitor/index.mjs logs --error-type "503"

# API docs
node skills/monitor/index.mjs docs

# Custom request
node skills/monitor/index.mjs request /v1/summary GET
```
