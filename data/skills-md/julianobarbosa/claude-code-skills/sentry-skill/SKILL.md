---
name: sentry-skill
description: Comprehensive skill for Sentry error monitoring and performance tracking. Use when Claude needs to (1) Configure Sentry SDKs for error tracking and performance monitoring, (2) Manage releases, source maps, and debug symbols via CLI, (3) Query issues, events, and metrics via API, (4) Set up alerting and notification rules, (5) Configure sampling strategies and quota management, (6) Deploy self-hosted Sentry instances, (7) Integrate with OpenTelemetry for distributed tracing, or any other Sentry automation task.
---

# Sentry Skill

Comprehensive guide for error monitoring, performance tracking, and application observability using Sentry.

## Quick Reference

### DSN (Data Source Name)

The DSN is the unique identifier for your Sentry project:

```
https://<PUBLIC_KEY>@<HOST>/<PROJECT_ID>
```

Example: `https://abc123@o123456.ingest.sentry.io/1234567`

### Core Concepts

| Concept | Description |
|---------|-------------|
| **Event** | Single instance of data sent to Sentry (error, transaction, etc.) |
| **Issue** | Group of similar events deduplicated by fingerprint |
| **Transaction** | Performance monitoring span representing a unit of work |
| **Span** | Individual operation within a transaction (DB query, HTTP call) |
| **Trace** | Connected series of transactions across services |
| **Release** | Version of your code deployed to an environment |
| **Environment** | Deployment target (production, staging, development) |

## SDK Installation & Configuration

### JavaScript/Node.js

```bash
npm install @sentry/node @sentry/profiling-node
```

```javascript
const Sentry = require("@sentry/node");
const { nodeProfilingIntegration } = require("@sentry/profiling-node");

Sentry.init({
  dsn: "https://public@sentry.example.com/1",
  release: process.env.RELEASE_VERSION || "1.0.0",
  environment: process.env.NODE_ENV || "development",

  // Error sampling (1.0 = 100% of errors)
  sampleRate: 1.0,

  // Performance monitoring (0.1 = 10% of transactions)
  tracesSampleRate: 0.1,

  // OR use dynamic sampling
  tracesSampler: (samplingContext) => {
    if (samplingContext.transactionContext.name === "/health") {
      return 0; // Don't sample health checks
    }
    if (samplingContext.parentSampled !== undefined) {
      return samplingContext.parentSampled; // Inherit parent decision
    }
    return 0.1; // Default 10%
  },

  // Profiling
  profilesSampleRate: 0.1,
  integrations: [nodeProfilingIntegration()],

  // Data scrubbing
  beforeSend(event) {
    if (event.request?.headers) {
      delete event.request.headers["Authorization"];
    }
    return event;
  },
});
```

### Python

```bash
pip install sentry-sdk
```

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

sentry_sdk.init(
    dsn="https://public@sentry.example.com/1",
    release="my-app@1.0.0",
    environment="production",

    # Error sampling
    sample_rate=1.0,

    # Performance monitoring
    traces_sample_rate=0.1,

    # OR dynamic sampling
    traces_sampler=lambda ctx: (
        0 if ctx.get("transaction_context", {}).get("name") == "/health"
        else 0.1
    ),

    # Profiling
    profiles_sample_rate=0.1,

    # Integrations
    integrations=[
        FlaskIntegration(),
        SqlalchemyIntegration(),
    ],

    # Data scrubbing
    before_send=lambda event, hint: scrub_sensitive_data(event),
)

def scrub_sensitive_data(event):
    if event.get("request", {}).get("headers"):
        event["request"]["headers"].pop("Authorization", None)
    return event
```

### Go

```bash
go get github.com/getsentry/sentry-go
```

```go
package main

import (
    "log"
    "time"
    "github.com/getsentry/sentry-go"
)

func main() {
    err := sentry.Init(sentry.ClientOptions{
        Dsn:              "https://public@sentry.example.com/1",
        Release:          "my-app@1.0.0",
        Environment:      "production",
        TracesSampleRate: 0.1,
        BeforeSend: func(event *sentry.Event, hint *sentry.EventHint) *sentry.Event {
            // Scrub sensitive data
            return event
        },
    })
    if err != nil {
        log.Fatalf("sentry.Init: %s", err)
    }
    defer sentry.Flush(2 * time.Second)
}
```

## Error Capturing

### Manual Error Capture

```javascript
// JavaScript
try {
  riskyOperation();
} catch (error) {
  Sentry.captureException(error, {
    tags: { component: "payment" },
    extra: { orderId: "12345" },
    user: { id: "user-123", email: "user@example.com" },
  });
}

// Capture message
Sentry.captureMessage("Something unexpected happened", "warning");
```

```python
# Python
try:
    risky_operation()
except Exception as e:
    sentry_sdk.capture_exception(e)
    sentry_sdk.set_tag("component", "payment")
    sentry_sdk.set_extra("order_id", "12345")
    sentry_sdk.set_user({"id": "user-123", "email": "user@example.com"})

# Capture message
sentry_sdk.capture_message("Something unexpected happened", level="warning")
```

### Breadcrumbs

```javascript
// Add context breadcrumbs
Sentry.addBreadcrumb({
  category: "auth",
  message: "User logged in",
  level: "info",
  data: { userId: "123" },
});
```

### Scopes

```javascript
// Configure scope for context
Sentry.configureScope((scope) => {
  scope.setUser({ id: "user-123" });
  scope.setTag("page_locale", "en-US");
  scope.setExtra("session_data", { cart_items: 5 });
});

// Isolated scope
Sentry.withScope((scope) => {
  scope.setTag("isolated", "true");
  Sentry.captureException(new Error("Scoped error"));
});
```

## Performance Monitoring

### Manual Transactions

```javascript
const transaction = Sentry.startTransaction({
  op: "task",
  name: "Process Order",
});

// Set transaction on scope
Sentry.getCurrentHub().configureScope((scope) => {
  scope.setSpan(transaction);
});

// Create child spans
const span = transaction.startChild({
  op: "db.query",
  description: "SELECT * FROM orders",
});

// Do work...
await queryDatabase();

span.finish();
transaction.finish();
```

### Distributed Tracing

```javascript
// Service A - Create trace
const transaction = Sentry.startTransaction({ name: "API Request" });
const traceHeader = transaction.toTraceparent();
// Pass traceHeader to Service B via HTTP header: sentry-trace

// Service B - Continue trace
const incomingTrace = request.headers["sentry-trace"];
const transaction = Sentry.startTransaction({
  name: "Process Request",
  op: "http.server",
}, { parentSampled: true });
```

## Sentry CLI

### Installation

```bash
# npm
npm install -g @sentry/cli

# curl
curl -sL https://sentry.io/get-cli/ | bash

# Homebrew
brew install getsentry/tools/sentry-cli
```

### Authentication

```bash
# Login interactively
sentry-cli login

# Or set auth token
export SENTRY_AUTH_TOKEN=your-token
export SENTRY_ORG=your-org
export SENTRY_PROJECT=your-project
```

### Release Management

```bash
# Create release
sentry-cli releases new v1.0.0

# Associate commits (auto-detect from git)
sentry-cli releases set-commits v1.0.0 --auto

# Or specify commit range
sentry-cli releases set-commits v1.0.0 --commit "repo@from_sha..to_sha"

# Upload source maps
sentry-cli releases files v1.0.0 upload-sourcemaps ./dist \
  --url-prefix '~/static/js' \
  --rewrite

# Upload debug symbols (iOS/Android/Native)
sentry-cli debug-files upload --include-sources path/to/symbols

# Deploy release to environment
sentry-cli releases deploys v1.0.0 new -e production

# Finalize release
sentry-cli releases finalize v1.0.0
```

### Source Maps Workflow

```bash
# Build with source maps
npm run build

# Create release and upload
export VERSION=$(sentry-cli releases propose-version)
sentry-cli releases new $VERSION
sentry-cli releases files $VERSION upload-sourcemaps ./dist \
  --url-prefix '~/' \
  --validate
sentry-cli releases finalize $VERSION
```

### Cron Monitoring

```bash
# Wrap a cron job
sentry-cli monitors run <monitor-slug> -- /path/to/script.sh

# Or use check-in API
sentry-cli monitors run <monitor-slug> --check-in-status in_progress
# ... run job ...
sentry-cli monitors run <monitor-slug> --check-in-status ok
```

### Send Test Event

```bash
sentry-cli send-event -m "Test event from CLI"
```

## API Reference

### Authentication

```bash
# Bearer token (recommended)
curl -H "Authorization: Bearer <AUTH_TOKEN>" \
  https://sentry.io/api/0/projects/

# DSN-based (limited endpoints)
curl -u <PUBLIC_KEY>: \
  https://sentry.io/api/<PROJECT_ID>/store/
```

### Common Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/0/organizations/` | GET | List organizations |
| `/api/0/organizations/{org}/projects/` | GET | List projects |
| `/api/0/projects/{org}/{project}/issues/` | GET | List issues |
| `/api/0/organizations/{org}/issues/{issue_id}/` | GET | Get issue details |
| `/api/0/projects/{org}/{project}/events/` | GET | List events |
| `/api/0/organizations/{org}/releases/` | GET/POST | List/Create releases |
| `/api/0/projects/{org}/{project}/keys/` | GET | List DSN keys |

### Query Issues

```bash
# List issues with filters
curl -H "Authorization: Bearer $TOKEN" \
  "https://sentry.io/api/0/projects/{org}/{project}/issues/?query=is:unresolved+level:error&statsPeriod=24h"

# Get issue details
curl -H "Authorization: Bearer $TOKEN" \
  "https://sentry.io/api/0/organizations/{org}/issues/{issue_id}/"

# Resolve issue
curl -X PUT -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "resolved"}' \
  "https://sentry.io/api/0/organizations/{org}/issues/{issue_id}/"
```

### Create Release via API

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "version": "v1.0.0",
    "projects": ["my-project"],
    "refs": [{
      "repository": "org/repo",
      "commit": "abc123"
    }]
  }' \
  "https://sentry.io/api/0/organizations/{org}/releases/"
```

### Pagination

```bash
# Response includes Link header
Link: <https://sentry.io/api/0/...?cursor=123:0:0>; rel="previous"; results="false",
      <https://sentry.io/api/0/...?cursor=456:0:0>; rel="next"; results="true"
```

### Rate Limiting

- Default: 40 requests/second for most endpoints
- Bulk endpoints: Lower limits
- Headers: `X-Sentry-Rate-Limit-Remaining`, `X-Sentry-Rate-Limit-Reset`

## Alerting Configuration

### Issue Alerts (via UI/API)

```json
{
  "name": "High Error Rate Alert",
  "conditions": [
    {
      "id": "sentry.rules.conditions.event_frequency.EventFrequencyCondition",
      "interval": "1h",
      "value": 100
    }
  ],
  "actions": [
    {
      "id": "sentry.integrations.slack.notify_action.SlackNotifyServiceAction",
      "channel": "#alerts",
      "workspace": "workspace-id"
    }
  ],
  "actionMatch": "all",
  "filterMatch": "all",
  "frequency": 30
}
```

### Metric Alerts

```yaml
# Example: Alert on error rate > 5%
triggers:
  - alertThreshold: 5
    label: critical
    actions:
      - type: slack
        channel: "#critical-alerts"
  - alertThreshold: 2
    label: warning
    actions:
      - type: email
        targetIdentifier: "team@example.com"
```

## OpenTelemetry Integration

### OTLP Exporter to Sentry

```javascript
const { NodeSDK } = require("@opentelemetry/sdk-node");
const { OTLPTraceExporter } = require("@opentelemetry/exporter-trace-otlp-http");

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({
    url: "https://sentry.io/api/<PROJECT_ID>/envelope/",
    headers: {
      "sentry-trace": "...",
    },
  }),
});

sdk.start();
```

### Sentry with OpenTelemetry

```javascript
const Sentry = require("@sentry/node");

Sentry.init({
  dsn: "...",
  instrumenter: "otel", // Use OpenTelemetry for instrumentation
  tracesSampleRate: 0.1,
});
```

## Self-Hosted Deployment

### System Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| CPU | 4 cores | 8+ cores |
| RAM | 16 GB | 32+ GB |
| Swap | 16 GB | - |
| Disk | 100 GB SSD | 500+ GB SSD |
| Docker | 19.03+ | Latest |
| Docker Compose | 2.19+ | Latest |

### Installation

```bash
# Clone repository
VERSION=$(curl -Ls -o /dev/null -w %{url_effective} \
  https://github.com/getsentry/self-hosted/releases/latest)
VERSION=${VERSION##*/}

git clone https://github.com/getsentry/self-hosted.git
cd self-hosted
git checkout ${VERSION}

# Run installer
./install.sh

# Start services
docker compose up -d

# Access at http://localhost:9000
```

### Configuration (`sentry/config.yml`)

```yaml
# Mail
mail.backend: 'smtp'
mail.host: 'smtp.example.com'
mail.port: 587
mail.username: 'sentry@example.com'
mail.password: 'password'
mail.use-tls: true
mail.from: 'sentry@example.com'

# System
system.url-prefix: 'https://sentry.example.com'
system.secret-key: 'your-secret-key'

# Features
features.organizations:early-adopter: False
```

### External Storage (GCS/S3)

```yaml
# sentry/config.yml
filestore.backend: 'gcs'
filestore.options:
  bucket_name: 'sentry-files'

# Or S3
filestore.backend: 's3'
filestore.options:
  access_key: 'AWS_ACCESS_KEY'
  secret_key: 'AWS_SECRET_KEY'
  bucket_name: 'sentry-files'
  region_name: 'us-east-1'
```

### External Databases

```yaml
# PostgreSQL
SENTRY_POSTGRES_HOST: 'postgres.example.com'
SENTRY_POSTGRES_PORT: '5432'
SENTRY_DB_NAME: 'sentry'
SENTRY_DB_USER: 'sentry'
SENTRY_DB_PASSWORD: 'password'

# Redis
SENTRY_REDIS_HOST: 'redis.example.com'
SENTRY_REDIS_PORT: '6379'

# Kafka
SENTRY_KAFKA_HOST: 'kafka.example.com:9092'
```

### Scaling Workers

```bash
# Scale specific services
docker compose up -d --scale worker=4 --scale snuba-consumer=2
```

### Monitoring Self-Hosted

```yaml
# Enable StatsD metrics
SENTRY_METRICS_BACKEND: 'statsd'
SENTRY_METRICS_OPTIONS:
  host: 'statsd.example.com'
  port: 8125
```

## Best Practices

### Sampling Strategy

```javascript
// Dynamic sampling based on context
tracesSampler: (ctx) => {
  // Always sample errors
  if (ctx.transactionContext.name.includes("error")) return 1.0;

  // Lower rate for high-volume endpoints
  if (ctx.transactionContext.name === "/api/health") return 0;
  if (ctx.transactionContext.name.startsWith("/api/v1/")) return 0.05;

  // Default rate
  return 0.1;
}
```

### Data Scrubbing

```javascript
beforeSend(event) {
  // Remove PII
  if (event.user) {
    delete event.user.email;
    delete event.user.ip_address;
  }

  // Scrub sensitive headers
  if (event.request?.headers) {
    delete event.request.headers["Authorization"];
    delete event.request.headers["Cookie"];
  }

  // Filter local errors in production
  if (event.exception?.values?.[0]?.type === "ChunkLoadError") {
    return null; // Drop event
  }

  return event;
}
```

### Release Tracking

```bash
# CI/CD Pipeline Example
export SENTRY_RELEASE=$(git rev-parse --short HEAD)

# Before deploy
sentry-cli releases new $SENTRY_RELEASE
sentry-cli releases set-commits $SENTRY_RELEASE --auto
sentry-cli releases files $SENTRY_RELEASE upload-sourcemaps ./dist

# After deploy
sentry-cli releases deploys $SENTRY_RELEASE new -e production
sentry-cli releases finalize $SENTRY_RELEASE
```

### Quota Management

```javascript
// Client-side rate limiting
Sentry.init({
  dsn: "...",
  maxBreadcrumbs: 50,
  maxValueLength: 1000,

  // Limit events per session
  beforeSend(event, hint) {
    if (sessionEventCount++ > 100) {
      return null; // Drop after 100 events
    }
    return event;
  }
});
```

## Common Operations

### Debug Integration Issues

```bash
# Enable debug mode
Sentry.init({ debug: true });

# Test event delivery
sentry-cli send-event -m "Test message"

# Verify source maps
sentry-cli releases files <release> list
sentry-cli sourcemaps explain <event-id>
```

### Resolve Issues in Bulk

```bash
# Via API
curl -X PUT -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "resolved"}' \
  "https://sentry.io/api/0/projects/{org}/{project}/issues/?id=123&id=456"
```

### Export Events

```bash
# Query events via Discover
curl -H "Authorization: Bearer $TOKEN" \
  "https://sentry.io/api/0/organizations/{org}/events/?field=title&field=count()&query=event.type:error&statsPeriod=7d"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Events not appearing | Check DSN, verify network connectivity, enable `debug: true` |
| Source maps not working | Verify release matches, check URL prefix, use `sourcemaps explain` |
| High event volume | Implement sampling, use `beforeSend` to filter |
| Performance overhead | Reduce `tracesSampleRate`, disable unnecessary integrations |
| Self-hosted OOM | Increase memory, add swap, scale horizontally |

## Reference Documentation

- **[SDK Configuration](references/sdk_configuration.md)**: Detailed SDK options
- **[CLI Commands](references/cli_commands.md)**: Complete CLI reference
- **[API Endpoints](references/api_endpoints.md)**: Full API documentation
- **[Self-Hosting](references/self_hosting.md)**: Deployment guide
- **[Alerting](references/alerting.md)**: Alert configuration patterns
