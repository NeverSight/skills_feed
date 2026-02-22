---
name: observability
description: Monitor and debug web and Node.js applications using OpenTelemetry, console logs, network requests, and distributed tracing. Use when the user asks about distributed tracing, correlating frontend/backend requests, OpenTelemetry, Jaeger, or monitoring application behavior.
allowed-tools: Bash(browser-devtools-cli:*), Bash(node-devtools-cli:*)
---

# Observability Skill

Monitor and debug web and Node.js applications using OpenTelemetry, console logs, network requests, and distributed tracing.

## When to Use

This skill activates when:
- User asks about distributed tracing
- User wants to correlate frontend and backend requests
- User mentions OpenTelemetry, Jaeger, Zipkin, or tracing
- User needs to debug request flow across services
- User wants to monitor application behavior

## Capabilities

### Distributed Tracing
```bash
browser-devtools-cli o11y get-trace-id
browser-devtools-cli o11y new-trace-id
browser-devtools-cli o11y set-trace-id --trace-id "abc123def456..."
```

### Console Monitoring
```bash
browser-devtools-cli o11y get-console-messages
browser-devtools-cli --json o11y get-console-messages --types error,warn
browser-devtools-cli --json o11y get-console-messages --search "error"
```

### Network Observability
```bash
browser-devtools-cli --json o11y get-http-requests
browser-devtools-cli --json o11y get-http-requests --resource-type fetch,xhr
browser-devtools-cli --json o11y get-http-requests --status-min 400
```

### Performance Metrics
```bash
browser-devtools-cli --json o11y get-web-vitals
browser-devtools-cli --json o11y get-web-vitals --wait-ms 3000
browser-devtools-cli --json o11y get-web-vitals --include-debug
```

## OpenTelemetry Integration

### Trace Context
Browser DevTools MCP can inject and extract W3C Trace Context headers:
- `traceparent`: Contains trace-id, span-id, and trace flags
- `tracestate`: Vendor-specific trace information

### Correlation Flow
```
Browser Session
    │
    ├─► trace-id: abc123
    │
    ▼
Frontend Request
    │
    ├─► Header: traceparent: 00-abc123-def456-01
    │
    ▼
Backend Service
    │
    ├─► Logs with trace-id: abc123
    │
    ▼
Observability Platform
    │
    └─► Full trace visualization
```

### Backend Observability (node-devtools-cli)

When correlating frontend traces with backend behavior, use `node-devtools-cli` to inspect Node.js processes:

```bash
# Connect to backend
node-devtools-cli --session-id backend debug connect --pid 12345

# Get console logs from Node process (can correlate with trace ID in logs)
node-devtools-cli --session-id backend --json debug get-logs
node-devtools-cli --session-id backend --json debug get-logs --search "trace"

# Optional: set tracepoints on backend handlers to capture call context
node-devtools-cli --session-id backend debug put-tracepoint \
  --url-pattern "routes/api.ts" \
  --line-number 25
```

## Debugging Workflow

```bash
SESSION="--session-id trace-session"

# 1. Generate new trace ID
browser-devtools-cli $SESSION o11y new-trace-id

# 2. Navigate (requests will carry trace ID)
browser-devtools-cli $SESSION navigation go-to --url "https://app.example.com"
browser-devtools-cli $SESSION sync wait-for-network-idle

# 3. Perform actions
browser-devtools-cli $SESSION interaction click --selector "#submit"
browser-devtools-cli $SESSION sync wait-for-network-idle

# 4. Get trace ID for backend correlation
browser-devtools-cli $SESSION o11y get-trace-id

# 5. Check console errors
browser-devtools-cli $SESSION --json o11y get-console-messages --types error

# 6. Check network requests
browser-devtools-cli $SESSION --json o11y get-http-requests

# 7. Cleanup
browser-devtools-cli session delete trace-session
```

## Use Existing Trace ID

```bash
SESSION="--session-id trace-session"

# Set trace ID from backend
browser-devtools-cli $SESSION o11y set-trace-id --trace-id "abc123def456789..."

# Navigate (requests will use this trace ID)
browser-devtools-cli $SESSION navigation go-to --url "https://app.example.com"

# All subsequent requests carry the trace ID
browser-devtools-cli $SESSION interaction click --selector "#api-call"
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OTEL_ENABLE` | Enable OpenTelemetry | `false` |
| `OTEL_SERVICE_NAME` | Service identifier | `frontend` |
| `OTEL_EXPORTER_TYPE` | Export destination | `none` |
| `OTEL_EXPORTER_HTTP_URL` | Collector endpoint | - |
| `OTEL_EXPORTER_HTTP_HEADERS` | Auth headers | - |

### Exporter Types

| Type | Description |
|------|-------------|
| `none` | Disabled |
| `console` | Log to console |
| `otlp/http` | Send to OTLP collector |

## Common Platforms

### Jaeger
```bash
OTEL_EXPORTER_HTTP_URL=http://localhost:4318
```

### Grafana Tempo
```bash
OTEL_EXPORTER_HTTP_URL=http://tempo:4318
```

### Honeycomb
```bash
OTEL_EXPORTER_HTTP_URL=https://api.honeycomb.io
OTEL_EXPORTER_HTTP_HEADERS=x-honeycomb-team=YOUR_API_KEY
```

### Datadog
```bash
OTEL_EXPORTER_HTTP_URL=http://localhost:4318
```

## Best Practices

1. **Generate new trace IDs** for each test scenario
2. **Document trace IDs** in bug reports
3. **Check console first** for JavaScript errors
4. **Filter network requests** to relevant endpoints
5. **Correlate timestamps** between frontend and backend
6. **Use structured logging** with trace context
7. **Set up OTEL exporter** for full trace visibility
