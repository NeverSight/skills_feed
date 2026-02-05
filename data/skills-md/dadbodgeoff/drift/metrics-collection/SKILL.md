---
name: metrics-collection
description: Prometheus-compatible metrics collection with counters, gauges, and histograms. Export metrics for dashboards and alerts with proper labeling.
license: MIT
compatibility: TypeScript/JavaScript, Python
metadata:
  category: observability
  time: 3h
  source: drift-masterguide
---

# Metrics Collection

Prometheus-compatible metrics for visibility into system behavior.

## When to Use This Skill

- Need visibility into request rates and latencies
- Want to track business metrics (signups, conversions)
- Building dashboards and alerts
- Debugging performance issues

## Core Concepts

Three metric types cover most use cases:

| Type | Use Case | Example |
|------|----------|---------|
| Counter | Things that only go up | Requests, errors, events |
| Gauge | Current value | Active connections, queue size |
| Histogram | Distribution of values | Request latency, response sizes |

## Implementation

### TypeScript

```typescript
interface CounterMetric {
  name: string;
  help: string;
  labels: string[];
  values: Map<string, number>;
}

interface GaugeMetric {
  name: string;
  help: string;
  labels: string[];
  values: Map<string, number>;
}

interface HistogramMetric {
  name: string;
  help: string;
  labels: string[];
  buckets: number[];
  values: Map<string, { count: number; sum: number; buckets: number[] }>;
}

class MetricsRegistry {
  private counters = new Map<string, CounterMetric>();
  private gauges = new Map<string, GaugeMetric>();
  private histograms = new Map<string, HistogramMetric>();

  // Counter methods
  registerCounter(name: string, help: string, labels: string[] = []): void {
    if (!this.counters.has(name)) {
      this.counters.set(name, { name, help, labels, values: new Map() });
    }
  }

  incrementCounter(name: string, labels: Record<string, string> = {}, value = 1): void {
    const counter = this.counters.get(name);
    if (!counter) return;

    const key = this.labelsToKey(labels);
    const current = counter.values.get(key) || 0;
    counter.values.set(key, current + value);
  }

  // Gauge methods
  registerGauge(name: string, help: string, labels: string[] = []): void {
    if (!this.gauges.has(name)) {
      this.gauges.set(name, { name, help, labels, values: new Map() });
    }
  }

  setGauge(name: string, value: number, labels: Record<string, string> = {}): void {
    const gauge = this.gauges.get(name);
    if (!gauge) return;

    const key = this.labelsToKey(labels);
    gauge.values.set(key, value);
  }

  incrementGauge(name: string, labels: Record<string, string> = {}, value = 1): void {
    const gauge = this.gauges.get(name);
    if (!gauge) return;

    const key = this.labelsToKey(labels);
    const current = gauge.values.get(key) || 0;
    gauge.values.set(key, current + value);
  }

  decrementGauge(name: string, labels: Record<string, string> = {}, value = 1): void {
    this.incrementGauge(name, labels, -value);
  }

  // Histogram methods
  registerHistogram(
    name: string,
    help: string,
    labels: string[] = [],
    buckets: number[] = [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]
  ): void {
    if (!this.histograms.has(name)) {
      this.histograms.set(name, { name, help, labels, buckets, values: new Map() });
    }
  }

  observeHistogram(name: string, value: number, labels: Record<string, string> = {}): void {
    const histogram = this.histograms.get(name);
    if (!histogram) return;

    const key = this.labelsToKey(labels);
    let data = histogram.values.get(key);

    if (!data) {
      data = { count: 0, sum: 0, buckets: new Array(histogram.buckets.length).fill(0) };
      histogram.values.set(key, data);
    }

    data.count++;
    data.sum += value;

    for (let i = 0; i < histogram.buckets.length; i++) {
      if (value <= histogram.buckets[i]) {
        data.buckets[i]++;
      }
    }
  }

  // Timer helper
  startTimer(histogramName: string, labels: Record<string, string> = {}): () => void {
    const start = performance.now();
    return () => {
      const duration = (performance.now() - start) / 1000;
      this.observeHistogram(histogramName, duration, labels);
    };
  }

  // Export to Prometheus format
  toPrometheus(): string {
    const lines: string[] = [];

    for (const counter of this.counters.values()) {
      lines.push(`# HELP ${counter.name} ${counter.help}`);
      lines.push(`# TYPE ${counter.name} counter`);
      for (const [labels, value] of counter.values) {
        const labelStr = labels ? `{${labels}}` : '';
        lines.push(`${counter.name}${labelStr} ${value}`);
      }
    }

    for (const gauge of this.gauges.values()) {
      lines.push(`# HELP ${gauge.name} ${gauge.help}`);
      lines.push(`# TYPE ${gauge.name} gauge`);
      for (const [labels, value] of gauge.values) {
        const labelStr = labels ? `{${labels}}` : '';
        lines.push(`${gauge.name}${labelStr} ${value}`);
      }
    }

    for (const histogram of this.histograms.values()) {
      lines.push(`# HELP ${histogram.name} ${histogram.help}`);
      lines.push(`# TYPE ${histogram.name} histogram`);
      for (const [labels, data] of histogram.values) {
        const labelStr = labels ? `${labels},` : '';
        for (let i = 0; i < histogram.buckets.length; i++) {
          lines.push(`${histogram.name}_bucket{${labelStr}le="${histogram.buckets[i]}"} ${data.buckets[i]}`);
        }
        lines.push(`${histogram.name}_bucket{${labelStr}le="+Inf"} ${data.count}`);
        lines.push(`${histogram.name}_sum{${labels}} ${data.sum}`);
        lines.push(`${histogram.name}_count{${labels}} ${data.count}`);
      }
    }

    return lines.join('\n');
  }

  toJSON(): object {
    return {
      counters: Object.fromEntries(
        Array.from(this.counters.entries()).map(([name, metric]) => [
          name, Object.fromEntries(metric.values),
        ])
      ),
      gauges: Object.fromEntries(
        Array.from(this.gauges.entries()).map(([name, metric]) => [
          name, Object.fromEntries(metric.values),
        ])
      ),
      histograms: Object.fromEntries(
        Array.from(this.histograms.entries()).map(([name, metric]) => [
          name, Object.fromEntries(metric.values),
        ])
      ),
    };
  }

  private labelsToKey(labels: Record<string, string>): string {
    return Object.entries(labels)
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([k, v]) => `${k}="${v}"`)
      .join(',');
  }
}

export const metrics = new MetricsRegistry();

// Pre-register common metrics
metrics.registerCounter('http_requests_total', 'Total HTTP requests', ['method', 'path', 'status']);
metrics.registerCounter('errors_total', 'Total errors', ['type', 'source']);
metrics.registerHistogram('http_request_duration_seconds', 'HTTP request duration', ['method', 'path']);
metrics.registerGauge('active_connections', 'Active connections');
metrics.registerGauge('queue_size', 'Queue size', ['queue']);
```

### Python

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable
import time


@dataclass
class CounterMetric:
    name: str
    help: str
    labels: List[str]
    values: Dict[str, float] = field(default_factory=dict)


@dataclass
class GaugeMetric:
    name: str
    help: str
    labels: List[str]
    values: Dict[str, float] = field(default_factory=dict)


@dataclass
class HistogramData:
    count: int = 0
    sum: float = 0
    buckets: List[int] = field(default_factory=list)


@dataclass
class HistogramMetric:
    name: str
    help: str
    labels: List[str]
    bucket_bounds: List[float]
    values: Dict[str, HistogramData] = field(default_factory=dict)


class MetricsRegistry:
    DEFAULT_BUCKETS = [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]
    
    def __init__(self):
        self._counters: Dict[str, CounterMetric] = {}
        self._gauges: Dict[str, GaugeMetric] = {}
        self._histograms: Dict[str, HistogramMetric] = {}
    
    def register_counter(self, name: str, help: str, labels: List[str] = None) -> None:
        if name not in self._counters:
            self._counters[name] = CounterMetric(name, help, labels or [])
    
    def increment_counter(self, name: str, labels: Dict[str, str] = None, value: float = 1) -> None:
        counter = self._counters.get(name)
        if not counter:
            return
        
        key = self._labels_to_key(labels or {})
        counter.values[key] = counter.values.get(key, 0) + value
    
    def register_gauge(self, name: str, help: str, labels: List[str] = None) -> None:
        if name not in self._gauges:
            self._gauges[name] = GaugeMetric(name, help, labels or [])
    
    def set_gauge(self, name: str, value: float, labels: Dict[str, str] = None) -> None:
        gauge = self._gauges.get(name)
        if not gauge:
            return
        
        key = self._labels_to_key(labels or {})
        gauge.values[key] = value
    
    def increment_gauge(self, name: str, labels: Dict[str, str] = None, value: float = 1) -> None:
        gauge = self._gauges.get(name)
        if not gauge:
            return
        
        key = self._labels_to_key(labels or {})
        gauge.values[key] = gauge.values.get(key, 0) + value
    
    def register_histogram(
        self, name: str, help: str, labels: List[str] = None, buckets: List[float] = None
    ) -> None:
        if name not in self._histograms:
            self._histograms[name] = HistogramMetric(
                name, help, labels or [], buckets or self.DEFAULT_BUCKETS
            )
    
    def observe_histogram(self, name: str, value: float, labels: Dict[str, str] = None) -> None:
        histogram = self._histograms.get(name)
        if not histogram:
            return
        
        key = self._labels_to_key(labels or {})
        if key not in histogram.values:
            histogram.values[key] = HistogramData(
                buckets=[0] * len(histogram.bucket_bounds)
            )
        
        data = histogram.values[key]
        data.count += 1
        data.sum += value
        
        for i, bound in enumerate(histogram.bucket_bounds):
            if value <= bound:
                data.buckets[i] += 1
    
    def start_timer(self, histogram_name: str, labels: Dict[str, str] = None) -> Callable[[], None]:
        start = time.perf_counter()
        
        def end_timer():
            duration = time.perf_counter() - start
            self.observe_histogram(histogram_name, duration, labels)
        
        return end_timer
    
    def to_prometheus(self) -> str:
        lines = []
        
        for counter in self._counters.values():
            lines.append(f"# HELP {counter.name} {counter.help}")
            lines.append(f"# TYPE {counter.name} counter")
            for labels, value in counter.values.items():
                label_str = f"{{{labels}}}" if labels else ""
                lines.append(f"{counter.name}{label_str} {value}")
        
        for gauge in self._gauges.values():
            lines.append(f"# HELP {gauge.name} {gauge.help}")
            lines.append(f"# TYPE {gauge.name} gauge")
            for labels, value in gauge.values.items():
                label_str = f"{{{labels}}}" if labels else ""
                lines.append(f"{gauge.name}{label_str} {value}")
        
        for histogram in self._histograms.values():
            lines.append(f"# HELP {histogram.name} {histogram.help}")
            lines.append(f"# TYPE {histogram.name} histogram")
            for labels, data in histogram.values.items():
                label_prefix = f"{labels}," if labels else ""
                for i, bound in enumerate(histogram.bucket_bounds):
                    lines.append(f'{histogram.name}_bucket{{{label_prefix}le="{bound}"}} {data.buckets[i]}')
                lines.append(f'{histogram.name}_bucket{{{label_prefix}le="+Inf"}} {data.count}')
                lines.append(f"{histogram.name}_sum{{{labels}}} {data.sum}")
                lines.append(f"{histogram.name}_count{{{labels}}} {data.count}")
        
        return "\n".join(lines)
    
    def _labels_to_key(self, labels: Dict[str, str]) -> str:
        return ",".join(f'{k}="{v}"' for k, v in sorted(labels.items()))


# Singleton
metrics = MetricsRegistry()

# Pre-register common metrics
metrics.register_counter("http_requests_total", "Total HTTP requests", ["method", "path", "status"])
metrics.register_counter("errors_total", "Total errors", ["type", "source"])
metrics.register_histogram("http_request_duration_seconds", "HTTP request duration", ["method", "path"])
metrics.register_gauge("active_connections", "Active connections")
metrics.register_gauge("queue_size", "Queue size", ["queue"])
```

## Usage Examples

### HTTP Request Tracking

```typescript
async function withMetrics(
  handler: () => Promise<Response>,
  method: string,
  path: string
): Promise<Response> {
  const endTimer = metrics.startTimer('http_request_duration_seconds', { method, path });

  try {
    const response = await handler();
    metrics.incrementCounter('http_requests_total', {
      method, path, status: String(response.status),
    });
    return response;
  } catch (error) {
    metrics.incrementCounter('http_requests_total', { method, path, status: '500' });
    metrics.incrementCounter('errors_total', { type: 'http', source: path });
    throw error;
  } finally {
    endTimer();
  }
}
```

### Queue Monitoring

```typescript
class JobQueue {
  private queue: Job[] = [];

  add(job: Job): void {
    this.queue.push(job);
    metrics.setGauge('queue_size', this.queue.length, { queue: 'jobs' });
  }

  process(): Job | undefined {
    const job = this.queue.shift();
    metrics.setGauge('queue_size', this.queue.length, { queue: 'jobs' });
    return job;
  }
}
```

### Business Metrics

```typescript
metrics.registerCounter('predictions_generated', 'Predictions generated', ['tier']);
metrics.registerCounter('user_signups', 'User signups', ['source']);

async function generatePrediction(userId: string, tier: string) {
  const endTimer = metrics.startTimer('prediction_latency_seconds');
  try {
    const prediction = await mlPipeline.generate();
    metrics.incrementCounter('predictions_generated', { tier });
    return prediction;
  } finally {
    endTimer();
  }
}
```

### Metrics Endpoint

```typescript
app.get('/metrics', (req, res) => {
  res.set('Content-Type', 'text/plain; charset=utf-8');
  res.send(metrics.toPrometheus());
});
```

## Best Practices

1. Use consistent naming (snake_case, units in name)
2. Keep cardinality low (avoid high-cardinality labels)
3. Pre-register metrics at startup
4. Use histograms for latencies, not gauges
5. Include units in metric names (_seconds, _bytes)

## Common Mistakes

- High cardinality labels (user_id as label)
- Using gauges for latency (use histograms)
- Not pre-registering metrics
- Missing units in names
- Too many buckets in histograms

## Related Patterns

- health-checks - Health endpoints for probes
- anomaly-detection - Alert on metric anomalies
- logging-observability - Correlate logs with metrics
