---
name: monitoring-observability
description: OpenTelemetry, structured logging, distributed tracing, alerting, and dashboards
---

# Monitoring & Observability

## Overview

This skill covers the three pillars of observability -- traces, metrics, and logs -- along with alerting, dashboards, and health check patterns. It focuses on OpenTelemetry as the vendor-neutral standard, structured logging for queryability, distributed tracing for microservice debugging, and SLO-based alerting to reduce noise.

Use this skill when instrumenting applications for production visibility, setting up monitoring infrastructure, debugging distributed systems, configuring alerts that matter, or building dashboards for operations and product teams.

---

## Core Principles

1. **Instrument at boundaries** - Trace every external call (HTTP, database, queue, cache). Internal function tracing adds noise; boundary tracing reveals system behavior.
2. **Structured over unstructured** - Every log entry must be JSON with correlation IDs, service name, and context. Unstructured logs are unsearchable at scale.
3. **Alert on symptoms, not causes** - Alert when users are affected (error rate, latency SLO breach), not when a specific server metric spikes. Symptom-based alerting reduces noise by 80%.
4. **Correlate across signals** - A trace ID should connect logs, traces, and metrics for a single request. Without correlation, debugging distributed issues requires guesswork.
5. **Budget your error rate** - Define SLOs (99.9% availability = 43 minutes/month downtime budget). Alert when the error budget burn rate is too fast, not on individual errors.

---

## Key Patterns

### Pattern 1: OpenTelemetry Instrumentation (Node.js)

**When to use:** Any production Node.js service that needs traces, metrics, and log correlation.

**Implementation:**

```typescript
// tracing.ts - Must be imported BEFORE any other module
import { NodeSDK } from "@opentelemetry/sdk-node";
import { OTLPTraceExporter } from "@opentelemetry/exporter-trace-otlp-http";
import { OTLPMetricExporter } from "@opentelemetry/exporter-metrics-otlp-http";
import { PeriodicExportingMetricReader } from "@opentelemetry/sdk-metrics";
import { getNodeAutoInstrumentations } from "@opentelemetry/auto-instrumentations-node";
import { Resource } from "@opentelemetry/resources";
import {
  ATTR_SERVICE_NAME,
  ATTR_SERVICE_VERSION,
  ATTR_DEPLOYMENT_ENVIRONMENT,
} from "@opentelemetry/semantic-conventions";

const sdk = new NodeSDK({
  resource: new Resource({
    [ATTR_SERVICE_NAME]: process.env.SERVICE_NAME ?? "my-service",
    [ATTR_SERVICE_VERSION]: process.env.SERVICE_VERSION ?? "0.0.0",
    [ATTR_DEPLOYMENT_ENVIRONMENT]: process.env.NODE_ENV ?? "development",
  }),
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT ?? "http://localhost:4318/v1/traces",
  }),
  metricReader: new PeriodicExportingMetricReader({
    exporter: new OTLPMetricExporter({
      url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT ?? "http://localhost:4318/v1/metrics",
    }),
    exportIntervalMillis: 30_000,
  }),
  instrumentations: [
    getNodeAutoInstrumentations({
      // Disable noisy fs instrumentation
      "@opentelemetry/instrumentation-fs": { enabled: false },
      // Configure HTTP to capture request/response headers
      "@opentelemetry/instrumentation-http": {
        requestHook: (span, request) => {
          span.setAttribute("http.request.header.x-request-id",
            request.headers?.["x-request-id"] ?? "unknown"
          );
        },
      },
    }),
  ],
});

sdk.start();

process.on("SIGTERM", () => {
  sdk.shutdown().then(() => process.exit(0));
});
```

```typescript
// Custom span creation for business logic
import { trace, SpanStatusCode, context } from "@opentelemetry/api";

const tracer = trace.getTracer("order-service");

async function processOrder(orderId: string): Promise<Order> {
  return tracer.startActiveSpan("process_order", async (span) => {
    try {
      span.setAttribute("order.id", orderId);

      const order = await tracer.startActiveSpan("fetch_order", async (fetchSpan) => {
        const result = await db.orders.findUnique({ where: { id: orderId } });
        fetchSpan.setAttribute("order.total", result?.total ?? 0);
        fetchSpan.end();
        return result;
      });

      if (!order) {
        span.setStatus({ code: SpanStatusCode.ERROR, message: "Order not found" });
        throw new OrderNotFoundError(orderId);
      }

      await tracer.startActiveSpan("charge_payment", async (paymentSpan) => {
        paymentSpan.setAttribute("payment.amount", order.total);
        await paymentService.charge(order);
        paymentSpan.end();
      });

      span.setStatus({ code: SpanStatusCode.OK });
      return order;
    } catch (error) {
      span.setStatus({ code: SpanStatusCode.ERROR, message: String(error) });
      span.recordException(error as Error);
      throw error;
    } finally {
      span.end();
    }
  });
}
```

**Why:** OpenTelemetry provides vendor-neutral instrumentation. Auto-instrumentation captures HTTP, database, and gRPC calls automatically. Custom spans add business context (order IDs, payment amounts) that make traces actionable for debugging.

---

### Pattern 2: Structured Logging with Correlation

**When to use:** Every application that produces logs (which is every application).

**Implementation:**

```typescript
import pino from "pino";
import { context, trace } from "@opentelemetry/api";

// Create logger with trace correlation
const logger = pino({
  level: process.env.LOG_LEVEL ?? "info",
  formatters: {
    level: (label) => ({ level: label }),
  },
  mixin() {
    // Automatically inject trace context into every log line
    const span = trace.getSpan(context.active());
    if (span) {
      const spanContext = span.spanContext();
      return {
        traceId: spanContext.traceId,
        spanId: spanContext.spanId,
        traceFlags: spanContext.traceFlags,
      };
    }
    return {};
  },
  // Redact sensitive fields
  redact: ["req.headers.authorization", "password", "token", "apiKey"],
});

// Usage - always log structured data, not string interpolation
logger.info({ orderId, userId, total: order.total }, "Order processed successfully");

// NOT this:
// logger.info(`Order ${orderId} processed for user ${userId} with total ${order.total}`);

// Error logging with context
logger.error(
  {
    err: error,
    orderId,
    operation: "payment_charge",
    paymentProvider: "stripe",
  },
  "Payment processing failed"
);

// Child loggers for request-scoped context
function createRequestLogger(req: Request) {
  return logger.child({
    requestId: req.headers.get("x-request-id") ?? crypto.randomUUID(),
    path: req.url,
    method: req.method,
    userAgent: req.headers.get("user-agent"),
  });
}
```

**Why:** Structured logs are queryable. You can filter by `orderId`, correlate with traces via `traceId`, and aggregate error rates by `operation`. String-interpolated logs require regex to extract fields, which breaks at scale.

---

### Pattern 3: SLO-Based Alerting

**When to use:** Setting up production alerting that reduces noise and focuses on user impact.

**Implementation:**

```yaml
# Prometheus alerting rules based on SLOs
groups:
  - name: slo-alerts
    rules:
      # Availability SLO: 99.9% success rate
      # Alert when burning through error budget too fast
      - alert: HighErrorBudgetBurn
        expr: |
          (
            sum(rate(http_requests_total{status=~"5.."}[5m]))
            /
            sum(rate(http_requests_total[5m]))
          ) > (1 - 0.999) * 14.4
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Error budget burn rate is 14.4x (will exhaust in 1 hour)"
          dashboard: "https://grafana.internal/d/slo-overview"

      # Latency SLO: 99% of requests under 500ms
      - alert: HighLatencyBudgetBurn
        expr: |
          (
            sum(rate(http_request_duration_seconds_bucket{le="0.5"}[5m]))
            /
            sum(rate(http_request_duration_seconds_count[5m]))
          ) < 0.99
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Latency SLO breach: >1% of requests exceeding 500ms"

      # Multi-window multi-burn-rate alert (Google SRE book pattern)
      - alert: SLOBreach_MultiWindow
        expr: |
          (
            error_ratio:rate1h > (14.4 * 0.001)
            and
            error_ratio:rate5m > (14.4 * 0.001)
          )
          or
          (
            error_ratio:rate6h > (6 * 0.001)
            and
            error_ratio:rate30m > (6 * 0.001)
          )
        labels:
          severity: critical
```

```typescript
// Application-level SLO tracking with custom metrics
import { metrics } from "@opentelemetry/api";

const meter = metrics.getMeter("slo-metrics");

const requestCounter = meter.createCounter("http.requests.total", {
  description: "Total HTTP requests",
});

const requestDuration = meter.createHistogram("http.request.duration", {
  description: "HTTP request duration in seconds",
  unit: "s",
});

// Middleware to track SLO metrics
function sloMiddleware(req: Request, res: Response, next: NextFunction) {
  const start = performance.now();

  res.on("finish", () => {
    const duration = (performance.now() - start) / 1000;
    const attributes = {
      method: req.method,
      route: req.route?.path ?? "unknown",
      status: String(res.statusCode),
      success: String(res.statusCode < 500),
    };

    requestCounter.add(1, attributes);
    requestDuration.record(duration, attributes);
  });

  next();
}
```

**Why:** Traditional threshold-based alerts (CPU > 80%, errors > 10) generate noise. SLO-based alerting asks "are users affected?" and "how fast are we burning our error budget?" This approach pages only when action is needed.

---

### Pattern 4: Health Checks and Readiness Probes

**When to use:** Any service deployed to Kubernetes or behind a load balancer.

**Implementation:**

```typescript
import { Router } from "express";

interface HealthCheckResult {
  status: "healthy" | "degraded" | "unhealthy";
  checks: Record<string, {
    status: "pass" | "fail" | "warn";
    latencyMs: number;
    message?: string;
  }>;
  uptime: number;
  version: string;
}

const healthRouter = Router();

// Liveness probe - is the process alive?
// Should NEVER check dependencies. Only checks if the process can respond.
healthRouter.get("/healthz", (req, res) => {
  res.status(200).json({ status: "alive" });
});

// Readiness probe - can this instance serve traffic?
// Checks critical dependencies.
healthRouter.get("/readyz", async (req, res) => {
  const checks: HealthCheckResult["checks"] = {};

  // Check database
  const dbStart = performance.now();
  try {
    await db.$queryRaw`SELECT 1`;
    checks.database = { status: "pass", latencyMs: performance.now() - dbStart };
  } catch (err) {
    checks.database = {
      status: "fail",
      latencyMs: performance.now() - dbStart,
      message: (err as Error).message,
    };
  }

  // Check Redis
  const redisStart = performance.now();
  try {
    await redis.ping();
    checks.redis = { status: "pass", latencyMs: performance.now() - redisStart };
  } catch (err) {
    checks.redis = {
      status: "fail",
      latencyMs: performance.now() - redisStart,
      message: (err as Error).message,
    };
  }

  const allPassing = Object.values(checks).every((c) => c.status === "pass");
  const anyFailing = Object.values(checks).some((c) => c.status === "fail");

  const result: HealthCheckResult = {
    status: anyFailing ? "unhealthy" : allPassing ? "healthy" : "degraded",
    checks,
    uptime: process.uptime(),
    version: process.env.SERVICE_VERSION ?? "unknown",
  };

  res.status(anyFailing ? 503 : 200).json(result);
});
```

**Why:** Kubernetes uses liveness probes to restart stuck processes and readiness probes to stop sending traffic to unready instances. Getting these wrong causes cascading failures: a liveness probe that checks the database will restart healthy pods during a database outage, making things worse.

---

## Grafana Dashboard Quick Reference

```json
{
  "panels": [
    {
      "title": "Request Rate",
      "type": "timeseries",
      "targets": [{ "expr": "sum(rate(http_requests_total[5m])) by (status)" }]
    },
    {
      "title": "Error Rate (%)",
      "type": "stat",
      "targets": [{
        "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m])) * 100"
      }],
      "thresholds": [
        { "value": 0, "color": "green" },
        { "value": 0.1, "color": "yellow" },
        { "value": 1, "color": "red" }
      ]
    },
    {
      "title": "P99 Latency",
      "type": "timeseries",
      "targets": [{
        "expr": "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, route))"
      }]
    }
  ]
}
```

---

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Better Approach |
|---|---|---|
| Logging with `console.log` in production | No structure, no correlation, no levels | Use pino or winston with JSON output |
| Alerting on every 5xx error | Alert fatigue, team ignores alerts | Alert on SLO breach / error budget burn rate |
| Liveness probe checks database | Restarts pods during DB outage (cascade) | Liveness checks process only; readiness checks deps |
| No trace context propagation | Cannot follow requests across services | Use W3C traceparent header, inject in all clients |
| Sampling 100% of traces | Storage costs explode at scale | Head-based sampling (10-20%) or tail-based for errors |
| Logging PII (emails, IPs) | GDPR/privacy violation | Redact sensitive fields in logger config |
| Dashboard with 50 panels | Information overload, slow to load | Four golden signals: rate, errors, duration, saturation |

---

## Checklist

- [ ] OpenTelemetry SDK initialized before all other imports
- [ ] Auto-instrumentation enabled for HTTP, database, and queue clients
- [ ] Custom spans added at business-logic boundaries with relevant attributes
- [ ] Structured JSON logging with trace ID correlation
- [ ] Sensitive fields redacted in logger configuration
- [ ] Liveness probe: checks process only (no dependency checks)
- [ ] Readiness probe: checks all critical dependencies
- [ ] SLOs defined for availability and latency
- [ ] Alerts based on error budget burn rate, not raw thresholds
- [ ] Dashboard with four golden signals per service
- [ ] Trace sampling strategy configured for production scale
- [ ] Log aggregation pipeline shipping to centralized store

---

## Related Resources

- **Skills:** `performance-engineering` (latency optimization), `application-security` (security logging)
- **Rules:** `rules/stacks/fullstack-nextjs-nestjs.md` (NestJS instrumentation patterns)
- **Rules:** `rules/tooling/troubleshooting.md` (debugging with logs)
