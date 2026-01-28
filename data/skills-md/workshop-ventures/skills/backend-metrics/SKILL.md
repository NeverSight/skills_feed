---
name: backend-metrics
description: Add OpenTelemetry metrics and observability to the backend. Use when asked to "add metrics", "add observability", "track requests", or "add OpenTelemetry".
---

# Backend Metrics and Observability

This skill adds OpenTelemetry metrics to track HTTP requests and response times.

## Overview

OpenTelemetry provides vendor-neutral observability. This setup tracks:
- Total HTTP requests (counter)
- Response time distribution (histogram)

## Installation

```bash
npm install @opentelemetry/api @opentelemetry/sdk-node @opentelemetry/sdk-metrics @opentelemetry/exporter-metrics-otlp-grpc
```

## Implementation

### Step 1: Create Metrics Library

Create `apps/backend/src/lib/metrics.ts`:

```typescript
import { metrics, Meter } from '@opentelemetry/api';
import { MeterProvider } from '@opentelemetry/sdk-metrics';
import { OTLPMetricExporter } from '@opentelemetry/exporter-metrics-otlp-grpc';
import { Resource } from '@opentelemetry/resources';
import {
  ATTR_SERVICE_NAME,
  ATTR_SERVICE_VERSION,
  ATTR_DEPLOYMENT_ENVIRONMENT_NAME,
} from '@opentelemetry/semantic-conventions';

import config from '../config';
import { createLogger } from './logger';

const log = createLogger('metrics');

let meterProvider: MeterProvider | null = null;

/**
 * Initialize OpenTelemetry metrics
 * Call this early in application startup
 */
export function initializeTelemetry(): void {
  if (!config.telemetry.enabled) {
    log.info('Telemetry disabled');
    return;
  }

  const resource = new Resource({
    [ATTR_SERVICE_NAME]: config.telemetry.serviceName,
    [ATTR_SERVICE_VERSION]: config.telemetry.serviceVersion,
    [ATTR_DEPLOYMENT_ENVIRONMENT_NAME]: config.telemetry.environment,
  });

  const metricExporter = new OTLPMetricExporter({
    url: config.telemetry.otlpEndpoint,
  });

  meterProvider = new MeterProvider({
    resource,
    readers: [
      {
        exporter: metricExporter,
        exportIntervalMillis: 60000, // Export every 60 seconds
      },
    ],
  });

  metrics.setGlobalMeterProvider(meterProvider);

  log.info(
    { endpoint: config.telemetry.otlpEndpoint },
    'Telemetry initialized'
  );
}

/**
 * Get a meter for creating instruments
 */
export function getMeter(name: string, version: string = '1.0.0'): Meter {
  return metrics.getMeter(name, version);
}

/**
 * Graceful shutdown
 */
export async function shutdownTelemetry(): Promise<void> {
  if (meterProvider) {
    await meterProvider.shutdown();
    log.info('Telemetry shutdown complete');
  }
}
```

### Step 2: Add Config

Add to `apps/backend/src/config/index.ts`:

```typescript
const config = {
  // ... existing config ...

  telemetry: {
    enabled: process.env.OTEL_ENABLED === 'true',
    serviceName: process.env.SERVICE_NAME || 'my-backend',
    environment: process.env.ENVIRONMENT || 'dev',
    serviceVersion: process.env.SERVICE_VERSION || '1.0.0',
    otlpEndpoint: process.env.OTEL_COLLECTOR_ENDPOINT || 'grpc://localhost:4317',
  },
};

export default config;
```

### Step 3: Create Metrics Middleware

Create `apps/backend/src/middleware/metrics.ts`:

```typescript
import { Context, Next } from 'koa';
import { getMeter } from '../lib/metrics';
import { createLogger } from '../lib/logger';

const log = createLogger('metrics-middleware');
const meter = getMeter('http-metrics');

// Create instruments
const requestCounter = meter.createCounter('http_requests_total', {
  description: 'Total number of HTTP requests',
});

const responseTimeHistogram = meter.createHistogram('http_response_time_ms', {
  description: 'HTTP response time in milliseconds',
  advice: {
    explicitBucketBoundaries: [10, 25, 50, 100, 250, 500, 1000, 2500, 5000],
  },
});

/**
 * Middleware to track HTTP metrics
 */
export async function metricsMiddleware(ctx: Context, next: Next): Promise<void> {
  const startTime = Date.now();

  await next();

  const duration = Date.now() - startTime;

  try {
    // Use matched route pattern if available, fallback to path
    const route = ctx._matchedRoute || ctx.path;
    const methodRoute = `${ctx.method} ${route}`;

    requestCounter.add(1, {
      method_route: methodRoute,
      status_code: ctx.status.toString(),
    });

    responseTimeHistogram.record(duration, {
      method_route: methodRoute,
      status_code: ctx.status.toString(),
    });
  } catch (err) {
    log.error({ err }, 'Error recording metric');
  }
}
```

### Step 4: Initialize in main.ts

Update `apps/backend/src/main.ts`:

```typescript
import { initializeTelemetry, shutdownTelemetry } from './lib/metrics';
import { metricsMiddleware } from './middleware/metrics';

// Initialize telemetry early (before app setup)
initializeTelemetry();

// ... app setup ...

// Add metrics middleware (after logging, before routes)
app.use(metricsMiddleware);

// ... routes ...

// Graceful shutdown
process.on('SIGTERM', async () => {
  await shutdownTelemetry();
  process.exit(0);
});
```

## Metrics Reference

### Request Counter

```typescript
http_requests_total{method_route="GET /api/users", status_code="200"}
```

Labels:
- `method_route`: HTTP method and route pattern
- `status_code`: HTTP status code

### Response Time Histogram

```typescript
http_response_time_ms{method_route="GET /api/users", status_code="200"}
```

Bucket boundaries: 10ms, 25ms, 50ms, 100ms, 250ms, 500ms, 1s, 2.5s, 5s

## Custom Metrics

Add custom metrics for business logic:

```typescript
import { getMeter } from '../lib/metrics';

const meter = getMeter('business-metrics');

// Counter for specific events
const orderCounter = meter.createCounter('orders_total', {
  description: 'Total orders placed',
});

// Use in your code
orderCounter.add(1, { status: 'completed', payment_method: 'card' });

// Gauge for current values
const activeUsersGauge = meter.createObservableGauge('active_users', {
  description: 'Number of currently active users',
});

activeUsersGauge.addCallback((result) => {
  result.observe(getActiveUserCount());
});
```

## Environment Variables

```bash
OTEL_ENABLED=true
SERVICE_NAME=my-backend
ENVIRONMENT=production
SERVICE_VERSION=1.2.3
OTEL_COLLECTOR_ENDPOINT=grpc://otel-collector:4317
```

## Checklist

1. **Install dependencies**: `npm install @opentelemetry/api @opentelemetry/sdk-node @opentelemetry/sdk-metrics @opentelemetry/exporter-metrics-otlp-grpc @opentelemetry/resources @opentelemetry/semantic-conventions`
2. **Create** `lib/metrics.ts` with initialization and getMeter
3. **Add config** for telemetry settings
4. **Create** `middleware/metrics.ts` for HTTP tracking
5. **Initialize** in `main.ts` before app setup
6. **Add shutdown** handler for graceful cleanup
7. **Configure** environment variables for your collector
