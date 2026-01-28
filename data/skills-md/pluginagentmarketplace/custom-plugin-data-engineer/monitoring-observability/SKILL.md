---
name: monitoring-observability
description: Prometheus, Grafana, logging, alerting, and data pipeline observability
sasmp_version: "1.3.0"
bonded_agent: 03-devops-engineer
bond_type: PRIMARY_BOND
skill_version: "2.0.0"
last_updated: "2025-01"
complexity: intermediate
estimated_mastery_hours: 100
prerequisites: [python-programming, containerization]
unlocks: [mlops, cloud-platforms]
---

# Monitoring & Observability

Production monitoring with Prometheus, Grafana, structured logging, and data quality observability.

## Quick Start

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import structlog
import time

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)
logger = structlog.get_logger()

# Prometheus metrics
RECORDS_PROCESSED = Counter('records_processed_total', 'Total records processed', ['pipeline', 'status'])
PROCESSING_TIME = Histogram('processing_duration_seconds', 'Processing duration', ['pipeline'])
QUEUE_SIZE = Gauge('queue_size', 'Current queue size', ['queue_name'])

def process_batch(batch: list, pipeline_name: str):
    start_time = time.time()

    try:
        for record in batch:
            # Process record...
            RECORDS_PROCESSED.labels(pipeline=pipeline_name, status='success').inc()

        duration = time.time() - start_time
        PROCESSING_TIME.labels(pipeline=pipeline_name).observe(duration)

        logger.info("batch_processed",
            pipeline=pipeline_name,
            count=len(batch),
            duration_seconds=duration
        )

    except Exception as e:
        RECORDS_PROCESSED.labels(pipeline=pipeline_name, status='error').inc()
        logger.error("batch_failed", pipeline=pipeline_name, error=str(e))
        raise

# Start metrics server
start_http_server(8000)
```

## Core Concepts

### 1. Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge, Summary

# Counter: monotonically increasing value
http_requests = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)
http_requests.labels(method='GET', endpoint='/api/data', status='200').inc()

# Histogram: distribution of values (latency, sizes)
request_latency = Histogram(
    'request_latency_seconds',
    'Request latency in seconds',
    ['endpoint'],
    buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

with request_latency.labels(endpoint='/api/data').time():
    # Process request
    pass

# Gauge: value that can go up and down
active_connections = Gauge('active_connections', 'Active connections')
active_connections.inc()  # Connection opened
active_connections.dec()  # Connection closed

# Summary: similar to histogram with percentiles
response_size = Summary('response_size_bytes', 'Response size', ['endpoint'])
response_size.labels(endpoint='/api/data').observe(1024)
```

### 2. Grafana Dashboard (JSON)

```json
{
  "title": "Data Pipeline Dashboard",
  "panels": [
    {
      "title": "Records Processed",
      "type": "stat",
      "targets": [{
        "expr": "sum(rate(records_processed_total[5m]))",
        "legendFormat": "Records/sec"
      }]
    },
    {
      "title": "Processing Latency P95",
      "type": "graph",
      "targets": [{
        "expr": "histogram_quantile(0.95, rate(processing_duration_seconds_bucket[5m]))",
        "legendFormat": "P95 Latency"
      }]
    },
    {
      "title": "Error Rate",
      "type": "gauge",
      "targets": [{
        "expr": "sum(rate(records_processed_total{status='error'}[5m])) / sum(rate(records_processed_total[5m])) * 100",
        "legendFormat": "Error %"
      }]
    }
  ]
}
```

### 3. Structured Logging

```python
import structlog
from datetime import datetime

# Configure structlog
structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
)

logger = structlog.get_logger()

# Usage with context
log = logger.bind(service="etl-pipeline", environment="production")

def process_order(order_id: str, user_id: str):
    order_log = log.bind(order_id=order_id, user_id=user_id)

    order_log.info("processing_started")

    try:
        # Process...
        order_log.info("processing_completed", duration_ms=150)
    except Exception as e:
        order_log.error("processing_failed", error=str(e), exc_info=True)
        raise
```

### 4. Alerting Rules (Prometheus)

```yaml
# alerting_rules.yml
groups:
  - name: data-pipeline-alerts
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(records_processed_total{status="error"}[5m]))
          / sum(rate(records_processed_total[5m])) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate in data pipeline"
          description: "Error rate is {{ $value | humanizePercentage }}"

      - alert: PipelineStalled
        expr: |
          sum(rate(records_processed_total[10m])) == 0
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Data pipeline is not processing records"

      - alert: HighLatency
        expr: |
          histogram_quantile(0.95, rate(processing_duration_seconds_bucket[5m])) > 5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High processing latency detected"
```

## Tools & Technologies

| Tool | Purpose | Version (2025) |
|------|---------|----------------|
| **Prometheus** | Metrics collection | 2.50+ |
| **Grafana** | Visualization | 10.3+ |
| **Loki** | Log aggregation | 2.9+ |
| **Alertmanager** | Alert routing | 0.27+ |
| **OpenTelemetry** | Tracing standard | 1.24+ |
| **Datadog** | Full observability | Latest |
| **Monte Carlo** | Data observability | Latest |

## Troubleshooting Guide

| Issue | Symptoms | Root Cause | Fix |
|-------|----------|------------|-----|
| **Missing Metrics** | Gaps in graphs | Scrape failure | Check targets, network |
| **High Cardinality** | Prometheus OOM | Too many labels | Reduce label values |
| **Alert Fatigue** | Too many alerts | Sensitive thresholds | Tune thresholds, add for duration |
| **Log Volume** | High storage cost | Verbose logging | Adjust log levels |

## Best Practices

```python
# ✅ DO: Use appropriate metric types
# Counter for totals, Histogram for latency

# ✅ DO: Add meaningful labels (but limit cardinality)
REQUESTS.labels(method='GET', status='200', endpoint='/api').inc()

# ✅ DO: Include correlation IDs in logs
logger.info("request_completed", request_id=request_id)

# ✅ DO: Set up dashboards for key metrics

# ❌ DON'T: High cardinality labels (user_id, request_id as labels)
# ❌ DON'T: Log sensitive data
# ❌ DON'T: Alert on every error
```

## Resources

- [Prometheus Docs](https://prometheus.io/docs/)
- [Grafana Tutorials](https://grafana.com/tutorials/)
- [OpenTelemetry](https://opentelemetry.io/)

---

**Skill Certification Checklist:**
- [ ] Can instrument applications with Prometheus metrics
- [ ] Can create Grafana dashboards
- [ ] Can implement structured logging
- [ ] Can set up alerting rules
- [ ] Can troubleshoot observability issues
