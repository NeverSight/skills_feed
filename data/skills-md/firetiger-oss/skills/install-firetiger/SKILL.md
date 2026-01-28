---
name: install-firetiger
description: Add OpenTelemetry instrumentation to Node.js, Python, Go, or Rust applications for Firetiger observability—use when asked to "instrument my app", "add observability", "set up tracing", "add telemetry", "configure OpenTelemetry", "otel setup", "firetiger instrumentation", "install firetiger", or send traces/metrics/logs to Firetiger.
---

# Install Firetiger Instrumentation

## Prerequisites

Requires Firetiger MCP server. If `get_ingest_credentials` fails, prompt user:
```bash
set_firetiger_deployment <cloud> <deployment>
```

## Workflow

### Step 1: Detect Project Type

Check for project files in priority order:

| File | Language | Template Directory |
|------|----------|-------------------|
| `package.json` | Node.js/TS | `assets/nodejs/` |
| `pyproject.toml` | Python | `assets/python/` |
| `requirements.txt` | Python | `assets/python/` |
| `go.mod` | Go | `assets/go/` |
| `Cargo.toml` | Rust | `assets/rust/` |

- Multiple matches → ask user which to instrument
- No matches → ask user for project type

### Step 2: Derive Service Name

Extract automatically, confirm with user:

- **Node.js**: `name` from `package.json`
- **Python**: `name` from `pyproject.toml`, else directory name
- **Go**: last segment of module path in `go.mod`
- **Rust**: `name` from `Cargo.toml`

### Step 3: Fetch Credentials

Call `get_ingest_credentials` MCP tool. Extract:
- `Ingest URL` → `{{INGEST_URL}}`
- `Authorization: Basic ...` value → `{{AUTH_HEADER}}`

### Step 4: Install Dependencies & Create Files

Read the appropriate template from `assets/<language>/`. Each template directory contains:
- `instrumentation.*` - Main instrumentation file
- `dependencies.md` - Install commands

Replace placeholders: `{{INGEST_URL}}`, `{{AUTH_HEADER}}`, `{{SERVICE_NAME}}`

### Step 5: Wire Entry Point

Guide user to import instrumentation at the **top** of their entry file (before other imports).

### Step 6: Verify

Provide env vars for production:
```bash
export OTEL_EXPORTER_OTLP_ENDPOINT="{{INGEST_URL}}"
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Basic {{AUTH_HEADER}}"
export OTEL_SERVICE_NAME="{{SERVICE_NAME}}"
```

Suggest triggering a request and checking Firetiger UI.

## References

- `references/troubleshooting.md` - Common issues and fixes
- `references/manual-instrumentation.md` - Adding custom spans
- `references/signals.md` - When to use traces vs metrics vs logs
