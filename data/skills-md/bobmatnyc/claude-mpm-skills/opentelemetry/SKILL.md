---
name: opentelemetry
description: "OpenTelemetry observability patterns: traces, metrics, logs, context propagation, OTLP export, Collector pipelines, and troubleshooting"
version: 1.0.0
category: universal
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Instrument services with OpenTelemetry and export OTLP traces/metrics/logs through a Collector for correlation and troubleshooting"
    when_to_use: "When building production observability, adding tracing to distributed systems, or standardizing telemetry across languages"
    quick_start: "1. Set service.name 2. Add auto-instrumentation 3. Export OTLP 4. Deploy Collector 5. Correlate logs with trace IDs"
  token_estimate:
    entry: 150
    full: 9000
context_limit: 900
tags:
  - observability
  - opentelemetry
  - tracing
  - metrics
  - logs
  - otlp
requires_tools: []
---

# OpenTelemetry

## Quick Start (signal design)

- Export OTLP via an OpenTelemetry Collector (vendor-neutral endpoint).
- Standardize resource attributes: `service.name`, `service.version`, `deployment.environment`.
- Start with auto-instrumentation, then add manual spans and log correlation.

## Load Next (References)

- `references/concepts.md` — traces/metrics/logs, context propagation, sampling, semantic conventions
- `references/collector-and-otlp.md` — Collector pipelines, processors, deployment patterns, tail sampling
- `references/instrumentation-and-troubleshooting.md` — manual spans, propagation pitfalls, cardinality, debugging
