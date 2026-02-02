---
name: observability
description: Implement logging, metrics, tracing, and alerting for production applications. Covers structured logging (Pino, Winston), metrics (Prometheus, DataDog, CloudWatch), distributed tracing (OpenTelemetry), and alert design. Use this skill when adding logging to services, setting up monitoring, creating alerts, debugging production issues, or designing SLIs/SLOs. Triggers on "logging", "monitoring", "alerting", "observability", "metrics", "tracing", "debug production", "correlation id", "structured logging", "dashboards", "SLI", "SLO".
---

# Observability

Implement the three pillars of observability: logs, metrics, and traces.

## The Three Pillars

| Pillar | Purpose | Key Question |
|--------|---------|--------------|
| **Logs** | Discrete events with context | What happened? |
| **Metrics** | Aggregated measurements | How much/many? |
| **Traces** | Request flow across services | Where did time go? |

**Quick pick:**
- Need to debug specific request? → Logs + Traces
- Need to alert on thresholds? → Metrics
- Need to understand system health? → All three
- Starting from zero? → Logs first, then metrics, then traces

## Logging Fundamentals

### Log Level Selection

```
FATAL → System is unusable, immediate action required
ERROR → Operation failed, needs attention soon
WARN  → Unexpected but recoverable, investigate later
INFO  → Significant business events, state changes
DEBUG → Detailed diagnostic info (never in prod default)
TRACE → Most granular, function-level (dev only)
```

**Decision guide:**

| Situation | Level | Example |
|-----------|-------|---------|
| Payment succeeded | INFO | `{ level: 'info', event: 'payment_completed', amount: 50 }` |
| Payment retry needed | WARN | `{ level: 'warn', event: 'payment_retry', attempt: 2 }` |
| Payment failed | ERROR | `{ level: 'error', event: 'payment_failed', code: 'DECLINED' }` |
| Database connection lost | FATAL | `{ level: 'fatal', event: 'db_connection_lost' }` |

### Structured Logging Pattern

```typescript
// ✅ Good: Structured, searchable
logger.info({
  event: 'order_created',
  orderId: '123',
  userId: 'user_456',
  amount: 99.99,
  duration_ms: 45
});

// ❌ Bad: String concatenation
logger.info(`Order 123 created for user user_456 with amount 99.99`);
```

**Required fields for every log:**
- `timestamp` (ISO 8601)
- `level` (string)
- `message` or `event` (what happened)
- `correlation_id` (request tracing)

**Contextual fields (when applicable):**
- `user_id`, `tenant_id` (who)
- `duration_ms` (how long)
- `error.message`, `error.stack` (what went wrong)

### Quick Setup: Pino (Recommended)

```typescript
import pino from 'pino';

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  formatters: {
    level: (label) => ({ level: label }),
  },
  timestamp: pino.stdTimeFunctions.isoTime,
  redact: ['req.headers.authorization', 'password', 'ssn'],
});

// Request-scoped logging
app.use((req, res, next) => {
  req.log = logger.child({
    correlationId: req.headers['x-correlation-id'] || crypto.randomUUID(),
    method: req.method,
    path: req.path,
  });
  next();
});
```

### Sensitive Data Handling

**Never log:**
- Passwords, API keys, tokens
- PII (SSN, credit cards, full DOB)
- Session tokens, JWTs (log sub claim only)
- Full request bodies with sensitive fields

**Redaction pattern:**
```typescript
const logger = pino({
  redact: {
    paths: ['password', '*.password', 'req.headers.authorization', 'creditCard'],
    censor: '[REDACTED]'
  }
});
```

## Metrics Fundamentals

### Metric Types

| Type | Use Case | Example |
|------|----------|---------|
| **Counter** | Things that only increase | `http_requests_total` |
| **Gauge** | Current value, can go up/down | `active_connections` |
| **Histogram** | Distribution of values | `request_duration_seconds` |
| **Summary** | Pre-calculated percentiles | `request_duration_p99` |

### The Four Golden Signals

```
┌─────────────────────────────────────────────────────────────┐
│                    Four Golden Signals                      │
├──────────────┬──────────────┬──────────────┬───────────────┤
│   Latency    │   Traffic    │    Errors    │  Saturation   │
│  How fast?   │  How much?   │  How often?  │   How full?   │
├──────────────┼──────────────┼──────────────┼───────────────┤
│ p50, p95,    │ req/sec      │ error_rate   │ CPU, memory   │
│ p99 latency  │ concurrent   │ 5xx count    │ queue depth   │
└──────────────┴──────────────┴──────────────┴───────────────┘
```

**Essential metrics for any service:**
```typescript
// Latency
const httpDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.01, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]
});

// Traffic
const httpRequests = new Counter({
  name: 'http_requests_total',
  help: 'Total HTTP requests',
  labelNames: ['method', 'route', 'status_code']
});

// Errors
const httpErrors = new Counter({
  name: 'http_errors_total',
  help: 'Total HTTP errors',
  labelNames: ['method', 'route', 'error_type']
});

// Saturation
const activeConnections = new Gauge({
  name: 'active_connections',
  help: 'Number of active connections'
});
```

### Naming Conventions

```
<namespace>_<name>_<unit>

✅ http_request_duration_seconds
✅ database_query_total
✅ cache_hit_ratio
✅ queue_messages_pending

❌ requestTime (no unit, camelCase)
❌ db-queries (hyphens)
❌ numRequests (abbreviations)
```

**Label guidelines:**
- Use labels for dimensions you'll filter/group by
- Keep cardinality low (< 1000 unique combinations)
- Never use high-cardinality values as labels (user IDs, request IDs)

## Alerting Principles

### Alert Quality Matrix

```
                        Fires Appropriately
                              ↑
                    No    │     Yes
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
  Low   │  Broken Alert   │  Noisy Alert    │  High
 Noise  │  (silent fail)  │  (tune down)    │  Noise
        │                 │                 │
        ├─────────────────┼─────────────────┤
        │                 │                 │
        │  Good Alert     │  Perfect Alert  │
        │  (but rare?)    │  (goal)         │
        │                 │                 │
        └─────────────────┴─────────────────┘
                        Actionability →
```

### Alert Design Rules

1. **Page only for user-facing impact**
   - Revenue loss
   - Complete feature unavailability
   - Data integrity issues

2. **Every alert needs a runbook**
   - What does this alert mean?
   - How do I investigate?
   - What are the fix options?

3. **Alert fatigue = alert failure**
   - If it pages >5x/week without action → fix or delete
   - Group related alerts
   - Use escalation tiers

### SLI/SLO Basics

**SLI (Service Level Indicator):** Measurable metric
**SLO (Service Level Objective):** Target for the SLI
**Error Budget:** How much "failure" is acceptable

```
Common SLIs:
- Availability: successful_requests / total_requests
- Latency: p99_response_time < threshold
- Error rate: errors / total_requests

Example SLO:
- "99.9% of requests complete successfully"
- "p99 latency < 200ms"
```

### Alert Severity Levels

| Level | Response Time | Criteria | Channel |
|-------|---------------|----------|---------|
| **P1 Critical** | Immediate | User-facing outage, data loss | PagerDuty + phone |
| **P2 High** | < 4 hours | Degraded service, partial outage | PagerDuty + Slack |
| **P3 Medium** | < 24 hours | Non-critical issues, single user | Slack only |
| **P4 Low** | Best effort | Warnings, approaching limits | Dashboard |

## Tracing Fundamentals

### Distributed Tracing Concepts

```
Request Flow:
┌────────────┐    ┌────────────┐    ┌────────────┐
│   API GW   │ →  │  Service A │ →  │  Service B │
│  Span 1    │    │   Span 2   │    │   Span 3   │
└────────────┘    └────────────┘    └────────────┘
                         ↓
                  ┌────────────┐
                  │  Database  │
                  │   Span 4   │
                  └────────────┘

Trace = Collection of all spans for one request
Span  = Single unit of work with timing
```

### Correlation IDs

**Implementation pattern:**
```typescript
// Generate at entry point (API gateway, load balancer)
const correlationId = req.headers['x-correlation-id'] || crypto.randomUUID();

// Propagate to all downstream calls
const response = await fetch('http://service-b/api', {
  headers: { 'x-correlation-id': correlationId }
});

// Include in all logs
logger.info({ correlationId, event: 'request_received' });
```

**Header standards:**
- `x-correlation-id` (common)
- `x-request-id` (also common)
- `traceparent` (W3C standard for distributed tracing)

### OpenTelemetry Quick Start

```typescript
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT,
  }),
  instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();
```

## Production Debugging Workflow

```
1. Identify the symptom
   └─→ Alert fired? Error spike? User report?

2. Find correlation ID
   └─→ From error tracking, user report, or API response header

3. Search logs with correlation ID
   └─→ Follow the request path

4. Check metrics dashboard
   └─→ When did it start? What changed?

5. Examine traces (if available)
   └─→ Which service/span is slow or failing?

6. Form hypothesis and verify
   └─→ Check code, config, dependencies

7. Fix and verify
   └─→ Deploy fix, confirm resolution
```

### Log Analysis Patterns

```bash
# Find all errors in last hour (structured logs in JSON)
cat app.log | jq 'select(.level == "error")' | head -20

# Group errors by type
cat app.log | jq 'select(.level == "error") | .error.type' | sort | uniq -c | sort -rn

# Find specific correlation ID
cat app.log | jq 'select(.correlationId == "abc-123")'

# Calculate error rate
echo "scale=4; $(grep -c '"level":"error"' app.log) / $(wc -l < app.log)" | bc
```

## Anti-Patterns

### ❌ Logging Everything

```typescript
// BAD: Too verbose, costs money
logger.debug({ req: req.body, res: res.body, headers: req.headers });

// GOOD: Log what you need
logger.info({ event: 'api_request', path: req.path, status: res.statusCode });
```

### ❌ Alert on Every Error

```yaml
# BAD: Alerts on transient errors
alert: AnyErrorOccurred
expr: http_errors_total > 0

# GOOD: Alert on sustained error rate
alert: HighErrorRate
expr: rate(http_errors_total[5m]) / rate(http_requests_total[5m]) > 0.01
for: 5m  # Must persist for 5 minutes
```

### ❌ High-Cardinality Labels

```typescript
// BAD: Millions of unique combinations
httpRequests.inc({ userId: user.id, requestId: req.id });

// GOOD: Bounded cardinality
httpRequests.inc({ userTier: user.tier, route: req.route });
```

### ❌ Missing Context in Logs

```typescript
// BAD: No way to trace
logger.error('Payment failed');

// GOOD: Full context for debugging
logger.error({
  event: 'payment_failed',
  correlationId,
  userId,
  paymentId,
  error: { message: err.message, code: err.code }
});
```

## Integration Points

**With CI/CD (ci-cd-expert):**
- Deployment markers in metrics
- Log version/commit hash
- Canary metrics for deployment validation

**With error tracking (Sentry):**
- Link traces to error events
- Breadcrumbs from structured logs
- User context propagation

**With incident management:**
- Alert → PagerDuty/OpsGenie
- Runbook links in alerts
- Post-incident metrics analysis

## Skill Usage

**Adding logging to a service:**
1. Install Pino or Winston
2. Read [references/logging-patterns.md](references/logging-patterns.md)
3. Implement request-scoped logging with correlation IDs
4. Configure redaction for sensitive fields

**Setting up monitoring:**
1. Identify the four golden signals for your service
2. Read [references/metrics-guide.md](references/metrics-guide.md)
3. Instrument with Prometheus/DataDog/CloudWatch
4. Create dashboards for key metrics

**Creating alerts:**
1. Define SLIs and SLOs
2. Read [references/alerting-guide.md](references/alerting-guide.md)
3. Create runbooks for each alert
4. Generate ohno tasks for alert implementation

**Adding distributed tracing:**
1. Implement correlation ID propagation
2. Read [references/tracing-basics.md](references/tracing-basics.md)
3. Set up OpenTelemetry if needed

**Debugging production issues:**
1. Follow the debugging workflow above
2. Use correlation IDs to trace requests
3. Correlate logs, metrics, and traces

---

**References:**
- [references/logging-patterns.md](references/logging-patterns.md) — Pino/Winston setup, structured logging, log aggregation
- [references/metrics-guide.md](references/metrics-guide.md) — Prometheus, DataDog, CloudWatch, dashboard patterns
- [references/alerting-guide.md](references/alerting-guide.md) — Alert design, runbook templates, SLI/SLO deep dive
- [references/tracing-basics.md](references/tracing-basics.md) — OpenTelemetry setup, Jaeger, trace analysis
