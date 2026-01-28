---
name: test-observability
description: Integrate Playwright tests with OpenTelemetry, Grafana, Prometheus, Loki, and Tempo. Use when debugging test failures across distributed systems, measuring test performance, creating test dashboards, or correlating tests with backend traces.
---

# Test Observability

## Overview

Connect your Playwright tests to your observability stack (Grafana, Prometheus, Loki, Tempo) for:

- **Trace Correlation**: See full trace from browser click → backend → database
- **Test Metrics**: Dashboard with pass rates, durations, flakiness
- **Log Aggregation**: Test logs alongside application logs
- **Failure Analysis**: Quickly identify root cause across distributed systems

---

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Playwright     │────▶│  OTEL Collector  │────▶│  Tempo (Traces) │
│  Tests          │     │                  │────▶│  Loki (Logs)    │
│                 │     │                  │────▶│  Prometheus     │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                                          │
                                                          ▼
                                                  ┌─────────────────┐
                                                  │    Grafana      │
                                                  │  Test Dashboard │
                                                  └─────────────────┘
```

---

## Quick Start: OTEL Reporter

### 1. Install Dependencies

```bash
npm install playwright-opentelemetry-reporter @opentelemetry/sdk-node @opentelemetry/exporter-trace-otlp-http
```

### 2. Configure Reporter

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  reporter: [
    ['html'],
    ['playwright-opentelemetry-reporter', {
      serviceName: 'playwright-tests',
      endpoint: process.env.OTEL_ENDPOINT || 'http://localhost:4318/v1/traces',
    }],
  ],
});
```

### 3. Run Tests

```bash
# With local OTEL collector
OTEL_ENDPOINT=http://localhost:4318/v1/traces npx playwright test

# With Railway OTEL collector
OTEL_ENDPOINT=http://otel-collector.railway.internal:4318/v1/traces npx playwright test
```

### 4. View in Grafana

- Open Grafana → Explore → Tempo
- Search for `service.name = "playwright-tests"`
- See test spans with duration, status, steps

---

## Tracetest Integration (Advanced)

Tracetest enables **trace-based testing** - assert on any span in the distributed trace.

### Installation

```bash
npm install @tracetest/playwright
```

### Configuration

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  reporter: [
    ['html'],
    ['@tracetest/playwright', {
      serverUrl: process.env.TRACETEST_URL || 'http://localhost:11633',
      apiKey: process.env.TRACETEST_API_KEY,
    }],
  ],
});
```

### Trace-Based Assertions

```typescript
// tests/checkout.spec.ts
import { test, expect } from '@playwright/test';
import { Tracetest } from '@tracetest/playwright';

test('checkout creates order', async ({ page }) => {
  const tracetest = new Tracetest();

  // Start trace capture
  await tracetest.capture();

  // Perform user action
  await page.goto('/checkout');
  await page.click('#place-order');
  await expect(page.locator('.order-confirmation')).toBeVisible();

  // Assert on backend trace!
  await tracetest.assertOnTrace({
    assertions: [
      // API response time
      {
        selector: 'span[name="POST /api/orders"]',
        assertion: 'attr:http.status_code = 201',
      },
      // Database query time
      {
        selector: 'span[name="INSERT orders"]',
        assertion: 'attr:db.duration < 100ms',
      },
      // Payment service
      {
        selector: 'span[name="payment.process"]',
        assertion: 'attr:payment.status = "success"',
      },
    ],
  });
});
```

### Benefits

- **80% faster debugging**: See exactly where failures occur
- **Full visibility**: Browser → API → Database → Services
- **Backend assertions**: Test database queries, service calls
- **Performance validation**: Assert on span durations

---

## Grafana Dashboard

### Import Dashboard

1. Open Grafana → Dashboards → Import
2. Upload `dashboards/test-results-dashboard.json`
3. Select Prometheus and Tempo data sources

### Key Panels

| Panel | Query | Purpose |
|-------|-------|---------|
| Pass Rate | `sum(playwright_test_passed) / sum(playwright_test_total)` | Overall health |
| Test Duration (p95) | `histogram_quantile(0.95, playwright_test_duration_bucket)` | Performance |
| Failed Tests | `playwright_test_failed{status="failed"}` | Quick triage |
| Flaky Tests | `playwright_test_retries > 1` | Identify flakiness |
| Slowest Tests | `topk(10, playwright_test_duration)` | Optimization targets |

### Custom Metrics

```typescript
// Export custom metrics from tests
import { test } from '@playwright/test';
import { metrics } from '@opentelemetry/api';

const testMeter = metrics.getMeter('playwright-tests');
const testDuration = testMeter.createHistogram('test.duration');
const testCounter = testMeter.createCounter('test.count');

test('custom metrics', async ({ page }) => {
  const start = Date.now();

  await page.goto('/');
  await page.click('.action');

  // Record custom metric
  testDuration.record(Date.now() - start, {
    test: 'homepage-action',
    browser: 'chromium',
  });

  testCounter.add(1, { status: 'passed' });
});
```

---

## Railway Integration

Connect to your existing Railway observability stack.

### Environment Variables

```bash
# Set in Railway service or .env
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector.railway.internal:4318
OTEL_SERVICE_NAME=playwright-tests
```

### Playwright Config

```typescript
// playwright.config.ts
export default defineConfig({
  reporter: [
    ['playwright-opentelemetry-reporter', {
      serviceName: process.env.OTEL_SERVICE_NAME || 'playwright-tests',
      endpoint: process.env.OTEL_EXPORTER_OTLP_ENDPOINT,
      headers: {
        // Add auth if needed
        'Authorization': `Bearer ${process.env.OTEL_AUTH_TOKEN}`,
      },
    }],
  ],
});
```

### Verify Connection

```bash
# Test OTEL collector is receiving data
curl -X POST http://otel-collector.railway.internal:4318/v1/traces \
  -H "Content-Type: application/json" \
  -d '{"resourceSpans":[]}'
# Should return 200 OK
```

---

## Log Correlation

Send test logs to Loki alongside traces.

### Winston + OTEL

```typescript
// tests/fixtures/logger.ts
import winston from 'winston';
import { OTLPLogExporter } from '@opentelemetry/exporter-logs-otlp-http';

export const logger = winston.createLogger({
  transports: [
    new winston.transports.Console(),
    // Send to OTEL collector → Loki
    new OTLPLogTransport({
      endpoint: process.env.OTEL_ENDPOINT,
    }),
  ],
});

// In tests
import { logger } from './fixtures/logger';

test('with logging', async ({ page }) => {
  logger.info('Starting test', { test: 'checkout' });

  await page.goto('/checkout');
  logger.debug('Page loaded', { url: page.url() });

  await page.click('#submit');
  logger.info('Order submitted');
});
```

### View Logs in Grafana

```
1. Grafana → Explore → Loki
2. Query: {service="playwright-tests"}
3. Filter: |= "error" or |json | level="error"
```

---

## Alerting

Set up alerts for test failures.

### Prometheus Alert Rules

```yaml
# alerts/test-alerts.yml
groups:
  - name: playwright-tests
    rules:
      - alert: TestFailureRate
        expr: |
          (sum(rate(playwright_test_failed[5m])) / sum(rate(playwright_test_total[5m]))) > 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High test failure rate (>10%)"

      - alert: TestDurationSpike
        expr: |
          histogram_quantile(0.95, playwright_test_duration_bucket) > 30
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Test duration p95 > 30 seconds"
```

### Grafana Alert

1. Edit dashboard panel
2. Alert tab → Create alert
3. Condition: `avg() of A is above 0.1`
4. Notifications: Slack, email, PagerDuty

---

## Workflow: Debugging with Traces

### 1. Test Fails in CI

```
❌ tests/checkout.spec.ts:15 - Order creation failed
   Expected: Order confirmation visible
   Actual: Error page shown
```

### 2. Find Trace in Grafana

```
Grafana → Explore → Tempo
Query: service.name="playwright-tests" AND name="checkout.spec.ts"
```

### 3. Analyze Trace

```
Browser click "Place Order" (50ms)
  └─ POST /api/orders (200ms)
       └─ Validate cart (10ms)
       └─ Process payment ❌ (timeout after 30s)
           └─ Payment gateway unreachable
       └─ Create order (skipped)
```

### 4. Root Cause

**Found**: Payment gateway timeout caused order failure.

**Without traces**: Would have debugged browser-side for hours.

---

## Best Practices

### 1. Add Trace Context to Tests

```typescript
import { context, trace } from '@opentelemetry/api';

test('with trace context', async ({ page }) => {
  const tracer = trace.getTracer('playwright');

  await tracer.startActiveSpan('checkout-flow', async (span) => {
    span.setAttribute('test.name', 'checkout');
    span.setAttribute('test.browser', 'chromium');

    await page.goto('/checkout');
    await page.click('#submit');

    span.setStatus({ code: 1 }); // OK
    span.end();
  });
});
```

### 2. Propagate Context to Backend

```typescript
// Ensure trace ID passes from browser to backend
test('trace propagation', async ({ page }) => {
  // Get current trace ID
  const traceId = trace.getActiveSpan()?.spanContext().traceId;

  // Add to request headers
  await page.route('**/*', route => {
    route.continue({
      headers: {
        ...route.request().headers(),
        'traceparent': `00-${traceId}-${spanId}-01`,
      },
    });
  });
});
```

### 3. Tag Tests for Filtering

```typescript
test('with tags', async ({ page }) => {
  const span = trace.getActiveSpan();
  span?.setAttribute('test.suite', 'e2e');
  span?.setAttribute('test.priority', 'critical');
  span?.setAttribute('test.feature', 'checkout');

  // Now filter in Grafana: test.feature="checkout"
});
```

---

## References

- `references/tracetest-integration.md` - Full Tracetest setup
- `references/otel-reporter-setup.md` - OTEL reporter configuration
- `references/grafana-dashboards.md` - Dashboard creation guide
- `dashboards/test-results-dashboard.json` - Ready-to-import dashboard

---

**Test observability transforms debugging from guesswork to precision - see the full picture from click to database.**
