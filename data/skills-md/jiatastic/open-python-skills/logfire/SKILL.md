---
name: logfire
description: >
  Structured observability with Pydantic Logfire and OpenTelemetry. Use when: (1) Adding traces/logs to Python APIs,
  (2) Instrumenting FastAPI, HTTPX, SQLAlchemy, or LLMs, (3) Setting up service metadata,
  (4) Configuring sampling or scrubbing sensitive data, (5) Testing observability code.
---

# Logfire

Structured observability for Python using Pydantic Logfire - fast setup, powerful features, OpenTelemetry-compatible.

## Quick Start

```bash
uv pip install logfire
```

```python
import logfire

logfire.configure(service_name="my-api", service_version="1.0.0")
logfire.info("Application started")
```

## Core Patterns

### 1. Service Configuration

Always set service metadata at startup:

```python
import logfire

logfire.configure(
    service_name="backend",
    service_version="1.0.0",
    environment="production",
    console=False,           # Disable console output in production
    send_to_logfire=True,    # Send to Logfire platform
)
```

### 2. Framework Instrumentation

Instrument frameworks **before** creating clients/apps:

```python
import logfire
from fastapi import FastAPI

# Configure FIRST
logfire.configure(service_name="backend")

# Then instrument
logfire.instrument_fastapi()
logfire.instrument_httpx()
logfire.instrument_sqlalchemy()

# Then create app
app = FastAPI()
```

### 3. Log Levels and Structured Logging

```python
# All log levels (trace → fatal)
logfire.trace("Detailed trace", step=1)
logfire.debug("Debug context", variable=locals())
logfire.info("User action", action="login", success=True)
logfire.notice("Important event", event_type="milestone")
logfire.warn("Potential issue", threshold_exceeded=True)
logfire.error("Operation failed", error_code=500)
logfire.fatal("Critical failure", component="database")

# Python 3.11+ f-string magic (auto-extracts variables)
user_id = 123
status = "active"
logfire.info(f"User {user_id} status: {status}")
# Equivalent to: logfire.info("User {user_id}...", user_id=user_id, status=status)

# Exception logging with automatic traceback
try:
    risky_operation()
except Exception:
    logfire.exception("Operation failed", context="extra_info")
```

### 4. Manual Spans

```python
# Spans for tracing operations
with logfire.span("Process order {order_id}", order_id="ORD-123"):
    logfire.info("Validating cart")
    # ... processing logic
    logfire.info("Order complete")

# Dynamic span attributes
with logfire.span("Database query") as span:
    results = execute_query()
    span.set_attribute("result_count", len(results))
    span.message = f"Query returned {len(results)} results"
```

### 5. Custom Metrics

```python
# Counter - monotonically increasing
request_counter = logfire.metric_counter("http.requests", unit="1")
request_counter.add(1, {"endpoint": "/api/users", "method": "GET"})

# Gauge - current value
temperature = logfire.metric_gauge("temperature", unit="°C")
temperature.set(23.5)

# Histogram - distribution of values
latency = logfire.metric_histogram("request.duration", unit="ms")
latency.record(45.2, {"endpoint": "/api/data"})
```

### 6. LLM Observability

```python
import logfire
from pydantic_ai import Agent

logfire.configure()
logfire.instrument_pydantic_ai()  # Traces all agent interactions

agent = Agent("openai:gpt-4o", system_prompt="You are helpful.")
result = agent.run_sync("Hello!")
```

### 7. Suppress Noisy Instrumentation

```python
# Suppress entire scope (e.g., noisy library)
logfire.suppress_scopes("google.cloud.bigquery.opentelemetry_tracing")

# Suppress specific code block
with logfire.suppress_instrumentation():
    client.get("https://internal-healthcheck.local")  # Not traced
```

### 8. Sensitive Data Scrubbing

```python
import logfire

# Add custom patterns to scrub
logfire.configure(
    scrubbing=logfire.ScrubbingOptions(
        extra_patterns=["api_key", "secret", "token"]
    )
)

# Custom callback for fine-grained control
def scrubbing_callback(match: logfire.ScrubMatch):
    if match.path == ("attributes", "safe_field"):
        return match.value  # Don't scrub this field
    return None  # Use default scrubbing

logfire.configure(
    scrubbing=logfire.ScrubbingOptions(callback=scrubbing_callback)
)
```

### 9. Sampling for High-Traffic Services

```python
import logfire

# Sample 50% of traces
logfire.configure(sampling=logfire.SamplingOptions(head=0.5))

# Disable metrics to reduce volume
logfire.configure(metrics=False)
```

### 10. Testing

```python
import logfire
from logfire.testing import CaptureLogfire

def test_user_creation(capfire: CaptureLogfire):
    create_user("Alice", "alice@example.com")
    
    spans = capfire.exporter.exported_spans
    assert len(spans) >= 1
    assert spans[0].attributes["user_name"] == "Alice"
    
    capfire.exporter.clear()  # Clean up for next test
```

## Available Integrations

| Category | Integration | Method |
|----------|------------|--------|
| **Web** | FastAPI | `logfire.instrument_fastapi(app)` |
| | Starlette | `logfire.instrument_starlette(app)` |
| | Django | `logfire.instrument_django()` |
| | Flask | `logfire.instrument_flask(app)` |
| | AIOHTTP Server | `logfire.instrument_aiohttp_server()` |
| | ASGI | `logfire.instrument_asgi(app)` |
| | WSGI | `logfire.instrument_wsgi(app)` |
| **HTTP** | HTTPX | `logfire.instrument_httpx()` |
| | Requests | `logfire.instrument_requests()` |
| | AIOHTTP Client | `logfire.instrument_aiohttp_client()` |
| **Database** | SQLAlchemy | `logfire.instrument_sqlalchemy(engine)` |
| | Asyncpg | `logfire.instrument_asyncpg()` |
| | Psycopg | `logfire.instrument_psycopg()` |
| | Redis | `logfire.instrument_redis()` |
| | PyMongo | `logfire.instrument_pymongo()` |
| **LLM** | Pydantic AI | `logfire.instrument_pydantic_ai()` |
| | OpenAI | `logfire.instrument_openai()` |
| | Anthropic | `logfire.instrument_anthropic()` |
| | MCP | `logfire.instrument_mcp()` |
| **Tasks** | Celery | `logfire.instrument_celery()` |
| | AWS Lambda | `logfire.instrument_aws_lambda()` |
| **Logging** | Standard logging | `logfire.instrument_logging()` |
| | Structlog | `logfire.instrument_structlog()` |
| | Loguru | `logfire.instrument_loguru()` |
| | Print | `logfire.instrument_print()` |
| **Other** | Pydantic | `logfire.instrument_pydantic()` |
| | System Metrics | `logfire.instrument_system_metrics()` |

## Common Pitfalls

| Issue | Symptom | Fix |
|-------|---------|-----|
| Missing service name | Spans hard to find in UI | Set `service_name` in `configure()` |
| Late instrumentation | No spans captured | Call `configure()` before creating clients |
| High-cardinality attrs | Storage explosion | Use IDs, not full payloads as attributes |
| Console noise | Logs pollute stdout | Set `console=False` in production |

## References

- [Configuration Options](references/configuration.md) - All `configure()` parameters
- [Integrations Guide](references/integrations.md) - Framework-specific setup
- [Metrics Guide](references/metrics.md) - Counter, gauge, histogram, system metrics
- [Advanced Patterns](references/advanced.md) - Sampling, scrubbing, suppression, testing
- [Pitfalls & Troubleshooting](references/pitfalls.md) - Common issues and solutions
- [Official Docs](https://logfire.pydantic.dev/docs/)
