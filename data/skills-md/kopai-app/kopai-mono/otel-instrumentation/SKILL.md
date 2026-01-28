---
name: otel-instrumentation
description: Instrument applications with OpenTelemetry SDK and validate telemetry using Kopai. Use when setting up observability, adding tracing/logging/metrics, testing instrumentation, or debugging missing telemetry data.
license: Apache-2.0
metadata:
  author: kopai
  version: "1.0.0"
---

# OpenTelemetry Instrumentation with Kopai

Guide for instrumenting applications with OpenTelemetry SDK and validating telemetry locally using Kopai.

## Quick Reference

```bash
# Start backend
npx @kopai/app start

# Configure app
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
export OTEL_SERVICE_NAME=my-service

# Validate telemetry
npx @kopai/cli traces search --service my-service --json
npx @kopai/cli logs search --service my-service --json
npx @kopai/cli metrics discover --json
```

## Rules

### 1. Setup (CRITICAL)

- `setup-backend` - Start Kopai Backend
- `setup-environment` - Configure Environment

### 2. Language SDKs (HIGH)

- `lang-nodejs` - Node.js Instrumentation
- `lang-python` - Python Instrumentation
- `lang-go` - Go Instrumentation
- `lang-java` - Java Instrumentation
- `lang-dotnet` - .NET Instrumentation
- `lang-ruby` - Ruby Instrumentation
- `lang-php` - PHP Instrumentation
- `lang-rust` - Rust Instrumentation
- `lang-swift` - Swift Instrumentation
- `lang-erlang` - Erlang/Elixir Instrumentation
- `lang-cpp` - C++ Instrumentation

### 3. Validation (HIGH)

- `validate-traces` - Validate Traces
- `validate-logs` - Validate Logs
- `validate-metrics` - Validate Metrics

### 4. Troubleshooting (MEDIUM)

- `troubleshoot-no-data` - No Data Received
- `troubleshoot-missing-spans` - Missing Spans
- `troubleshoot-missing-attrs` - Missing Attributes
- `troubleshoot-wrong-port` - Wrong Port

Read `rules/<rule-name>.md` for details.

## References

- [cli-reference](references/cli-reference.md) - Kopai CLI command reference
- [otel-docs](references/otel-docs.md) - OpenTelemetry documentation links
