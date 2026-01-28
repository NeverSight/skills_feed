---
name: root-cause-analysis
description: Analyze telemetry data for root cause analysis using Kopai CLI. Use when debugging errors, investigating latency issues, tracing request flows across services, or correlating logs with traces.
license: Apache-2.0
metadata:
  author: kopai
  version: "1.0.0"
---

# Root Cause Analysis with Kopai

Guide for debugging production issues using telemetry data (traces, logs, metrics) via Kopai CLI.

## Prerequisites

Ensure access to Kopai app backend.
Make sure the services are set up to send their OpenTelemetry data to Kopai.
See otel-instrumentation skill for setup.

## RCA Workflow Summary

1. Find error traces
2. Get full trace context
3. Correlate logs with trace
4. Check related metrics
5. Identify root cause

## Rules

### 1. Workflow (CRITICAL)

- `workflow-find-errors` - Find Error Traces
- `workflow-get-context` - Get Full Trace Context
- `workflow-correlate-logs` - Correlate Logs with Trace
- `workflow-check-metrics` - Check Related Metrics

### 2. Patterns (HIGH)

- `pattern-http-errors` - HTTP Error Debugging
- `pattern-slow-requests` - Slow Request Analysis
- `pattern-distributed` - Distributed Failure Tracing
- `pattern-log-driven` - Log-Driven Investigation

Read `rules/<rule-name>.md` for details.

## Tips

1. Always use `--json` for programmatic analysis
2. Pipe to `jq` for filtering/aggregation
3. Start with errors, then trace backwards
4. Check span Duration to find bottlenecks
5. Correlate TraceId across traces, logs, metrics

## References

- [trace-filters](references/trace-filters.md) - Trace search filter options
- [log-filters](references/log-filters.md) - Log search filter options
- [metric-filters](references/metric-filters.md) - Metric search filter options
