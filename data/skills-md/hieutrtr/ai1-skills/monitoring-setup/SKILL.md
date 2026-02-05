---
name: monitoring-setup
description: >-
  Application monitoring and observability setup for Python/React projects. Use when
  configuring logging, metrics collection, health checks, alerting rules, or dashboard
  creation. Covers structured logging with structlog, Prometheus metrics for FastAPI,
  health check endpoints, alert threshold design, Grafana dashboard patterns, error
  tracking with Sentry, and uptime monitoring. Does NOT cover incident response
  procedures (use incident-response) or deployment (use deployment-pipeline).
license: MIT
compatibility: 'Python 3.12+, FastAPI, structlog, OpenTelemetry, Prometheus'
metadata:
  author: platform-team
  version: '1.0.0'
  sdlc-phase: operations
allowed-tools: Read Edit Write Bash(python:*) Bash(docker:*)
context: fork
---

# Monitoring Setup

## When to Use

Activate this skill when:
- Setting up structured logging for a Python/FastAPI application
- Configuring Prometheus metrics collection and custom counters/histograms
- Implementing health check endpoints (liveness and readiness)
- Designing alert rules and thresholds for production services
- Creating Grafana dashboards for service monitoring
- Integrating Sentry for error tracking and performance monitoring
- Implementing distributed tracing with OpenTelemetry
- Reviewing or improving existing observability coverage

Do NOT use this skill for:
- Responding to active production incidents (use `incident-response`)
- Deploying monitoring infrastructure (use `deployment-pipeline`)
- Writing application business logic (use `python-backend-expert`)
- Docker container configuration (use `docker-best-practices`)

## Instructions

### Four Pillars of Observability

Every production service must implement all four pillars.

```
┌─────────────────────────────────────────────────────────────────┐
│                    OBSERVABILITY                                │
├────────────────┬───────────────┬──────────────┬────────────────┤
│    METRICS     │   LOGGING     │   TRACING    │   ALERTING     │
│                │               │              │                │
│  Prometheus    │  structlog    │ OpenTelemetry│  Alert rules   │
│  counters,     │  structured   │ distributed  │  thresholds,   │
│  histograms,   │  JSON logs,   │ trace spans, │  notification  │
│  gauges        │  context      │ correlation  │  channels      │
├────────────────┴───────────────┴──────────────┴────────────────┤
│                    DASHBOARDS (Grafana)                         │
│        Visualize metrics, logs, and traces in one place        │
└─────────────────────────────────────────────────────────────────┘
```

### Pillar 1: Metrics (Prometheus)

Use the RED method for request-driven services and USE method for resources.

**RED Method (for every API endpoint):**
- **R**ate -- Requests per second
- **E**rrors -- Failed requests per second
- **D**uration -- Request latency distribution

**USE Method (for infrastructure resources):**
- **U**tilization -- Percentage of resource used (CPU, memory, disk)
- **S**aturation -- Work queued or waiting (connection pool, queue depth)
- **E**rrors -- Error events (OOM kills, connection failures)

**Key metrics to instrument:**

```python
from prometheus_client import Counter, Histogram, Gauge, Info

# RED metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    labelnames=["method", "endpoint", "status_code"],
)

REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    labelnames=["method", "endpoint"],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
)

# USE metrics
DB_POOL_USAGE = Gauge(
    "db_connection_pool_usage",
    "Database connection pool utilization",
    labelnames=["pool_name"],
)

DB_POOL_SIZE = Gauge(
    "db_connection_pool_size",
    "Database connection pool max size",
    labelnames=["pool_name"],
)

REDIS_CONNECTIONS = Gauge(
    "redis_active_connections",
    "Active Redis connections",
)

# Business metrics
ACTIVE_USERS = Gauge(
    "active_users_total",
    "Currently active users",
)

APP_INFO = Info(
    "app",
    "Application metadata",
)
```

**FastAPI middleware for automatic metrics:**

```python
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        method = request.method
        endpoint = request.url.path
        start_time = time.perf_counter()

        response = await call_next(request)

        duration = time.perf_counter() - start_time
        status_code = str(response.status_code)

        REQUEST_COUNT.labels(
            method=method, endpoint=endpoint, status_code=status_code
        ).inc()

        REQUEST_DURATION.labels(
            method=method, endpoint=endpoint
        ).observe(duration)

        return response
```

See `references/metrics-config-template.py` for the complete setup.

### Pillar 2: Logging (structlog)

Use structured JSON logging with contextual information. Never use `print()` or unstructured logging in production.

**Logging principles:**
1. **Structured** -- JSON format, machine-parseable
2. **Contextual** -- Include request ID, user ID, trace ID in every log
3. **Leveled** -- Use appropriate log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
4. **Actionable** -- Every WARNING/ERROR log should indicate what to investigate

**Log levels and when to use them:**

| Level | When to Use | Example |
|-------|-------------|---------|
| DEBUG | Detailed diagnostic info, disabled in production | `Processing item 42 of 100` |
| INFO | Normal operations, significant events | `User created`, `Payment processed` |
| WARNING | Unexpected but handled situation | `Retry attempt 2 of 3`, `Cache miss` |
| ERROR | Operation failed, needs attention | `Database query failed`, `External API timeout` |
| CRITICAL | System-level failure, immediate action | `Cannot connect to database`, `Out of memory` |

**structlog setup:**

```python
import structlog

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)
```

**Adding request context:**

```python
from starlette.middleware.base import BaseHTTPMiddleware
import structlog
import uuid

class LoggingContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
        )
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
```

See `references/logging-config-template.py` for the complete setup.

### Pillar 3: Tracing (OpenTelemetry)

Distributed tracing connects logs and metrics across service boundaries.

**Trace setup for FastAPI:**

```python
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

def setup_tracing(app, service_name: str = "backend"):
    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)

    exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317")
    provider.add_span_processor(BatchSpanProcessor(exporter))

    trace.set_tracer_provider(provider)

    # Auto-instrument FastAPI, SQLAlchemy, Redis
    FastAPIInstrumentor.instrument_app(app)
    SQLAlchemyInstrumentor().instrument()
    RedisInstrumentor().instrument()
```

**Custom spans for business logic:**

```python
tracer = trace.get_tracer(__name__)

async def process_order(order_id: str):
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order.id", order_id)

        with tracer.start_as_current_span("validate_order"):
            await validate_order(order_id)

        with tracer.start_as_current_span("charge_payment"):
            result = await charge_payment(order_id)
            span.set_attribute("payment.status", result.status)

        with tracer.start_as_current_span("send_confirmation"):
            await send_confirmation(order_id)
```

### Pillar 4: Alerting

Alerts must be actionable. Every alert should indicate what is broken and what to do.

**Alert design principles:**
1. **Page only for user-impacting issues** -- Do not page for non-urgent warnings
2. **Set thresholds based on SLOs** -- Not arbitrary numbers
3. **Avoid alert fatigue** -- If an alert fires often without action, fix or remove it
4. **Include runbook links** -- Every alert should link to a remediation guide
5. **Use multi-window burn rates** -- Detect issues faster without false positives

**Alert thresholds for a typical FastAPI application:**

| Alert | Condition | Severity | Action |
|-------|-----------|----------|--------|
| High error rate | `http_requests_total{status=~"5.."}` > 5% of total for 5 min | SEV2 | Check logs, consider rollback |
| High latency | `http_request_duration_seconds` p99 > 2s for 5 min | SEV3 | Check DB queries, dependencies |
| Service down | Health check fails for 2 min | SEV1 | Restart, check logs, escalate |
| DB connections high | Pool usage > 80% for 5 min | SEV3 | Check for connection leaks |
| DB connections critical | Pool usage > 95% for 2 min | SEV2 | Restart app, investigate |
| Memory high | Container memory > 85% for 10 min | SEV3 | Check for memory leaks |
| Disk space low | Disk usage > 85% | SEV3 | Clean logs, expand volume |
| Certificate expiry | SSL cert expires in < 14 days | SEV4 | Renew certificate |

See `references/alert-rules-template.yml` for Prometheus alerting rules.

### Health Check Endpoints

Every service must expose two health endpoints.

**Liveness (`/health`):** Is the process running? Returns 200 if the application is alive.

**Readiness (`/health/ready`):** Can the service handle requests? Checks all dependencies.

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from datetime import datetime, timezone

router = APIRouter(tags=["health"])

@router.get("/health")
async def liveness():
    """Liveness probe -- is the process running?"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": settings.APP_VERSION,
    }

@router.get("/health/ready")
async def readiness(db: AsyncSession = Depends(get_db)):
    """Readiness probe -- can we handle traffic?"""
    checks = {}

    # Check database
    try:
        await db.execute(text("SELECT 1"))
        checks["database"] = {"status": "ok", "latency_ms": 0}
    except Exception as e:
        checks["database"] = {"status": "error", "error": str(e)}

    # Check Redis
    try:
        start = time.perf_counter()
        await redis.ping()
        latency = (time.perf_counter() - start) * 1000
        checks["redis"] = {"status": "ok", "latency_ms": round(latency, 2)}
    except Exception as e:
        checks["redis"] = {"status": "error", "error": str(e)}

    all_ok = all(c["status"] == "ok" for c in checks.values())
    return JSONResponse(
        status_code=200 if all_ok else 503,
        content={
            "status": "ready" if all_ok else "not_ready",
            "checks": checks,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )
```

### Error Tracking with Sentry

Sentry captures unhandled exceptions and performance data.

**Setup:**

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    environment=settings.APP_ENV,
    release=settings.APP_VERSION,
    traces_sample_rate=0.1,  # 10% of requests for performance monitoring
    profiles_sample_rate=0.1,
    integrations=[
        FastApiIntegration(),
        SqlalchemyIntegration(),
    ],
    # Do not send PII
    send_default_pii=False,
    # Filter out health check noise
    before_send=filter_health_checks,
)

def filter_health_checks(event, hint):
    """Do not send health check errors to Sentry."""
    if "request" in event and event["request"].get("url", "").endswith("/health"):
        return None
    return event
```

### Dashboard Design

Grafana dashboards should follow a consistent layout pattern.

**Standard dashboard sections:**
1. **Overview row** -- Key SLIs at a glance (error rate, latency, throughput)
2. **RED metrics row** -- Rate, Errors, Duration for each endpoint
3. **Infrastructure row** -- CPU, memory, disk, network
4. **Dependencies row** -- Database, Redis, external API health
5. **Business metrics row** -- Application-specific KPIs

**Dashboard layout:**

```
┌─────────────────────────────────────────────────────────┐
│  Service Overview                                       │
│  [Error Rate %] [p99 Latency] [Requests/s] [Uptime]    │
├────────────────────────┬────────────────────────────────┤
│  Request Rate          │  Error Rate                    │
│  (by endpoint)         │  (by endpoint, status code)    │
├────────────────────────┼────────────────────────────────┤
│  Latency (p50/p95/p99) │  Active Connections            │
│  (by endpoint)         │  (DB pool, Redis)              │
├────────────────────────┴────────────────────────────────┤
│  Infrastructure                                         │
│  [CPU %] [Memory %] [Disk %] [Network IO]              │
├─────────────────────────────────────────────────────────┤
│  Dependencies                                           │
│  [DB Latency] [Redis Latency] [External API Status]    │
└─────────────────────────────────────────────────────────┘
```

See `references/dashboard-template.json` for a complete Grafana dashboard template.

### Uptime Monitoring

External uptime monitoring validates the service from a user's perspective.

**What to monitor externally:**
- `/health` endpoint from multiple geographic regions
- Key user-facing pages (login, dashboard, API docs)
- SSL certificate validity and expiration
- DNS resolution time

**Recommended check intervals:**

| Check | Interval | Timeout | Regions |
|-------|----------|---------|---------|
| Health endpoint | 30 seconds | 10 seconds | 3+ regions |
| Key pages | 1 minute | 15 seconds | 2+ regions |
| SSL certificate | 6 hours | 30 seconds | 1 region |
| DNS resolution | 5 minutes | 5 seconds | 3+ regions |

### Quick Reference

**Set up logging:**
```python
# See references/logging-config-template.py
from app.logging_config import setup_logging
setup_logging(log_level="INFO", json_format=True)
```

**Add Prometheus metrics:**
```python
# See references/metrics-config-template.py
from app.metrics import setup_metrics
setup_metrics(app)
```

**Configure alerts:**
```yaml
# See references/alert-rules-template.yml
# Copy to your Prometheus alert rules directory
```

**Create dashboard:**
```json
// See references/dashboard-template.json
// Import into Grafana via Dashboard -> Import -> Upload JSON
```

### Monitoring Checklist for New Services

- [ ] structlog configured with JSON output
- [ ] Request logging middleware with request ID correlation
- [ ] Prometheus metrics endpoint exposed at `/metrics`
- [ ] RED metrics instrumented (request count, errors, duration)
- [ ] Health check endpoints implemented (`/health`, `/health/ready`)
- [ ] Sentry SDK initialized with environment and release tags
- [ ] Alert rules defined for error rate, latency, and availability
- [ ] Grafana dashboard created with standard sections
- [ ] External uptime monitoring configured
- [ ] Log retention policy defined (default: 30 days)
