---
name: observability-patterns
description: Observability patterns for metrics, logs, and traces. Use when implementing monitoring, setting up Prometheus/Grafana, configuring logging pipelines, implementing distributed tracing, or designing alerting systems.
---

# Observability Patterns

Best practices for implementing comprehensive observability with metrics, logs, and traces.

## The Three Pillars

### 1. Metrics (Prometheus)

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - /etc/prometheus/rules/*.yml

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

scrape_configs:
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
```

### Application Metrics (Python)

```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import time

# Define metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint'],
    buckets=[.005, .01, .025, .05, .1, .25, .5, 1, 2.5, 5, 10]
)

ACTIVE_REQUESTS = Gauge(
    'http_requests_active',
    'Active HTTP requests'
)

# Middleware example
def metrics_middleware(request, call_next):
    ACTIVE_REQUESTS.inc()
    start_time = time.time()

    try:
        response = call_next(request)
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.path,
            status=response.status_code
        ).inc()
        return response
    finally:
        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=request.path
        ).observe(time.time() - start_time)
        ACTIVE_REQUESTS.dec()
```

### 2. Logs (Structured Logging)

```python
import structlog
import logging

# Configure structlog
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Usage with context
def process_order(order_id: str, user_id: str):
    log = logger.bind(order_id=order_id, user_id=user_id)

    log.info("processing_order_started")

    try:
        # Process order
        result = do_processing()
        log.info("processing_order_completed", items_count=len(result.items))
        return result
    except Exception as e:
        log.error("processing_order_failed", error=str(e), exc_info=True)
        raise
```

### Log Aggregation (Loki)

```yaml
# loki-config.yaml
auth_enabled: false

server:
  http_listen_port: 3100

ingester:
  lifecycler:
    ring:
      kvstore:
        store: inmemory
      replication_factor: 1

schema_config:
  configs:
    - from: 2020-10-24
      store: boltdb-shipper
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 24h

storage_config:
  boltdb_shipper:
    active_index_directory: /loki/index
    cache_location: /loki/cache
    shared_store: filesystem
  filesystem:
    directory: /loki/chunks

limits_config:
  enforce_metric_name: false
  reject_old_samples: true
  reject_old_samples_max_age: 168h
```

### 3. Traces (OpenTelemetry)

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

# Initialize tracing
def init_tracing(service_name: str):
    provider = TracerProvider(
        resource=Resource.create({
            "service.name": service_name,
            "service.version": "1.0.0",
        })
    )

    exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317")
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

    # Auto-instrument libraries
    RequestsInstrumentor().instrument()
    SQLAlchemyInstrumentor().instrument()

# Manual instrumentation
tracer = trace.get_tracer(__name__)

@tracer.start_as_current_span("process_payment")
def process_payment(payment_id: str, amount: float):
    span = trace.get_current_span()
    span.set_attribute("payment.id", payment_id)
    span.set_attribute("payment.amount", amount)

    with tracer.start_as_current_span("validate_payment"):
        validate(payment_id)

    with tracer.start_as_current_span("charge_card"):
        result = charge(payment_id, amount)
        span.set_attribute("payment.status", result.status)

    return result
```

## Alerting Rules

### Prometheus Alerting Rules

```yaml
# alerts.yml
groups:
  - name: application
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m]))
          / sum(rate(http_requests_total[5m])) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High error rate detected
          description: "Error rate is {{ $value | humanizePercentage }}"

      - alert: HighLatency
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
          ) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High latency detected
          description: "P95 latency is {{ $value }}s"

      - alert: PodCrashLooping
        expr: |
          increase(kube_pod_container_status_restarts_total[1h]) > 5
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: Pod is crash looping
          description: "Pod {{ $labels.pod }} has restarted {{ $value }} times"
```

## Grafana Dashboards

### Dashboard JSON Template

```json
{
  "title": "Application Overview",
  "panels": [
    {
      "title": "Request Rate",
      "type": "timeseries",
      "targets": [
        {
          "expr": "sum(rate(http_requests_total[5m])) by (endpoint)",
          "legendFormat": "{{ endpoint }}"
        }
      ]
    },
    {
      "title": "Error Rate",
      "type": "stat",
      "targets": [
        {
          "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m])) * 100"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "percent",
          "thresholds": {
            "steps": [
              {"color": "green", "value": null},
              {"color": "yellow", "value": 1},
              {"color": "red", "value": 5}
            ]
          }
        }
      }
    },
    {
      "title": "Latency Distribution",
      "type": "heatmap",
      "targets": [
        {
          "expr": "sum(rate(http_request_duration_seconds_bucket[5m])) by (le)",
          "format": "heatmap"
        }
      ]
    }
  ]
}
```

## SLO/SLI Definitions

```yaml
# SLO definitions
slos:
  - name: availability
    description: Service should be available 99.9% of the time
    sli:
      events:
        good: http_requests_total{status!~"5.."}
        total: http_requests_total
    objectives:
      - target: 0.999
        window: 30d

  - name: latency
    description: 95% of requests should complete within 200ms
    sli:
      events:
        good: http_request_duration_seconds_bucket{le="0.2"}
        total: http_request_duration_seconds_count
    objectives:
      - target: 0.95
        window: 30d

  - name: error_budget
    description: Monthly error budget
    calculation: |
      1 - (
        sum(http_requests_total{status=~"5.."})
        / sum(http_requests_total)
      )
```

## Health Check Endpoints

```python
from fastapi import FastAPI, Response
from enum import Enum

class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

app = FastAPI()

@app.get("/health/live")
async def liveness():
    """Kubernetes liveness probe - is the process running?"""
    return {"status": "ok"}

@app.get("/health/ready")
async def readiness():
    """Kubernetes readiness probe - can we serve traffic?"""
    checks = {
        "database": check_database(),
        "cache": check_cache(),
        "dependencies": check_dependencies(),
    }

    all_healthy = all(c["healthy"] for c in checks.values())
    status_code = 200 if all_healthy else 503

    return Response(
        content=json.dumps({"status": "ready" if all_healthy else "not_ready", "checks": checks}),
        status_code=status_code,
        media_type="application/json"
    )

@app.get("/health/startup")
async def startup():
    """Kubernetes startup probe - has initialization completed?"""
    return {"status": "started", "initialized": True}
```

## References

- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/)
- [Grafana Dashboards](https://grafana.com/docs/grafana/latest/dashboards/)
- [Google SRE Book - Monitoring](https://sre.google/sre-book/monitoring-distributed-systems/)
