---
name: data-engineering-observability
description: "Observability and monitoring for data pipelines using OpenTelemetry (traces) and Prometheus (metrics). Covers instrumentation, dashboards, and alerting."
dependsOn: ["@data-engineering-core"]
---

# Pipeline Observability

Tracing and metrics for data pipelines using OpenTelemetry and Prometheus. Instrument code for visibility into performance, errors, and data lineage.

## Quick Reference

| Tool | Purpose | What it Measures |
|------|---------|------------------|
| **OpenTelemetry** | Distributed tracing | Pipeline stages, latency, dependencies |
| **Prometheus** | Metrics | Throughput, error rates, resource utilization |
| **Grafana** | Visualization | Dashboards combining traces + metrics |

## Why Observable?

- **Debugging**: Trace failed records through pipeline stages
- **Performance**: Identify bottlenecks, optimize slow transformations
- **Reliability**: Set alerts on error rates, SLA breaches
- **Cost**: Track resource usage, optimize expensive operations
- **Compliance**: Audit trail of data transformations

## Skill Dependencies

- `@data-engineering-core` - Pipeline structure to instrument
- `@data-engineering-orchestration` - Prefect/Dagster have built-in observability
- `@data-engineering-streaming` - Stream processing patterns need tracing

---

## OpenTelemetry Integration

OpenTelemetry (OTel) provides a vendor-neutral standard for distributed tracing, metrics, and logs.

### Installation
```bash
pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp
```

### Basic Tracing
```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
import logging

# Setup tracer provider
provider = TracerProvider()
exporter = OTLPSpanExporter(endpoint="http://localhost:4317")
provider.add_span_processor(BatchSpanProcessor(exporter))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("data_pipeline")

def run_pipeline():
    with tracer.start_as_current_span("extract") as span:
        span.set_attribute("source", "sales.parquet")
        span.set_attribute("format", "parquet")
        df = pl.scan_parquet("data/sales.parquet").collect()
        span.set_attribute("rows_read", len(df))

    with tracer.start_as_current_span("transform") as span:
        span.set_attribute("operation", "aggregation")
        result = df.group_by("category").agg(pl.col("value").sum())

    with tracer.start_as_current_span("load") as span:
        span.set_attribute("target", "duckdb.summary")
        result.to_pandas().to_sql("summary", conn, if_exists="replace")
        span.set_attribute("rows_written", len(result))

if __name__ == "__main__":
    run_pipeline()
```

### Trace Context Propagation

For multi-service pipelines, pass trace context:

```python
from opentelemetry import propagators
from opentelemetry.propagators.b3 import B3Format

# Inject trace context into message headers (Kafka, HTTP)
carrier = {}
propagator = B3Format()
propagator.inject(carrier, context=trace.get_current_span().get_context())

# Send carrier dict with message (e.g., Kafka header)
producer.produce(
    topic="events",
    key=key,
    value=json.dumps(data),
    headers=list(carrier.items())
)

# Consumer extracts context
context = propagator.extract(carrier=carrier)
with tracer.start_as_current_span("process_message", context=context):
    process(data)
```

---

## Prometheus Metrics

Prometheus collects numeric time series data. Push or pull metrics from your application.

### Installation
```bash
pip install prometheus-client
```

### Basic Instrumentation
```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

# Define metrics
ROWS_PROCESSED = Counter(
    'etl_rows_processed_total',
    'Total rows processed by ETL',
    ['source', 'stage']
)

PROCESSING_TIME = Histogram(
    'etl_processing_seconds',
    'Time spent processing',
    ['operation'],
    buckets=[0.1, 0.5, 1.0, 5.0, 10.0, 30.0, 60.0]
)

PIPELINE_ERRORS = Counter(
    'etl_errors_total',
    'Total preprocessing errors',
    ['stage', 'error_type']
)

MEMORY_USAGE = Gauge(
    'etl_memory_bytes',
    'Process memory usage in bytes'
)

# Start metrics server (Prometheus scrapes this endpoint)
start_http_server(8000)

def process_batch(stage: str, batch_id: int):
    with PROCESSING_TIME.time(operation=f"batch_{batch_id}"):
        try:
            rows = extract_and_process(batch_id)
            ROWS_PROCESSED.labels(source="kafka", stage=stage).inc(rows)
            return rows
        except Exception as e:
            PIPELINE_ERRORS.labels(stage=stage, error_type=type(e).__name__).inc()
            raise

# Periodic gauge update
import psutil
def update_memory():
    process = psutil.Process()
    MEMORY_USAGE.set(process.memory_info().rss)
```

### Custom Collector
```python
from prometheus_client import CollectorRegistry, Gauge

registry = CollectorRegistry()

# Custom gauge that computes on demand
queue_size = Gauge(
    'kafka_queue_size',
    'Number of messages in queue',
    registry=registry
)

def collect_queue_size():
    size = kafka_consumer.metrics()['fetch-metrics']['records-lag-max']
    queue_size.set(size)

# Register with push gateway or scrape
```

---

## Integration with Orchestration

### Prefect Built-in Observability
Prefect automatically records:
- Task run status (success/failure)
- Duration
- Retry counts
- Parameters

Enable Prefect Cloud/Server for UI:

```bash
prefect cloud login  # or prefect server start
prefect agent start -q 'default'
```

### Dagster Observability
Dagster Dagit UI shows:
- Asset materialization history
- Run duration and status
- Asset lineage graph
- Resource usage

Enable metrics:
```python
from dagster import DagsterMetric

@asset
def monitored_asset():
    # Dagster automatically records metrics
    pass
```

---

## Dashboards & Alerting

### Grafana Dashboard Example

Create dashboard with panels:
- **Throughput**: `rate(etl_rows_processed_total[5m])`
- **Latency**: `histogram_quantile(0.95, etl_processing_seconds_bucket)`
- **Error Rate**: `rate(etl_errors_total[5m])`
- **Memory**: `etl_memory_bytes / 1024 / 1024`

### Alert Rules (Prometheus Alertmanager)

```yaml
groups:
  - name: etl-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(etl_errors_total[5m]) > 0.1
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "ETL error rate elevated"
          description: "{{ $labels.stage }} stage error rate: {{ $value }} errors/sec"
```

---

## Best Practices

### Instrumentation
1. ✅ **Span every pipeline stage** - extract, transform, load, validate
2. ✅ **Add attributes** - dataset names, row counts, file paths
3. ✅ **Propagate context** across async boundaries (threads, processes, network)
4. ✅ **Record errors** in spans with `span.record_exception()`
5. ✅ **Sample judiciously** - 100% in dev, lower in prod (sampling policy)

### Metrics
1. ✅ **Use counters for events** (rows processed, errors)
2. ✅ **Use histograms for durations** (processing time, latency)
3. ✅ **Use gauges for state** (queue size, memory usage)
4. ✅ **Label dimensions** (stage, source, status) but avoid cardinality explosion
5. ✅ **Export endpoint** on separate port (8000) outside app port

### Production
1. ✅ **Centralized logs** - send structured logs to ELK/Datadog
2. ✅ **Correlation IDs** - Include trace IDs in log entries
3. ✅ **Alert on SLA breaches** - latency > threshold, error rate > X%
4. ✅ **Test observability** - Simulate failures, verify traces/metrics
5. ✅ **Document schema** - Define metric names and label values in README

---

## References

- [OpenTelemetry Python](https://opentelemetry.io/docs/instrumentation/python/)
- [Prometheus Python Client](https://github.com/prometheus/client_python)
- [Grafana Dashboarding](https://grafana.com/docs/grafana/latest/dashboards/)
- `@data-engineering-orchestration` - Prefect/Dagster observability features
