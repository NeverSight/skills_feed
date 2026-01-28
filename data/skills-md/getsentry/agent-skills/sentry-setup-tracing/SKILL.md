---
name: sentry-setup-tracing
description: Setup Sentry Tracing (Performance Monitoring) in any project. Use when asked to enable tracing, track transactions/spans, measure latency, or add performance monitoring. Supports JavaScript, Python, and Ruby.
---

# Setup Sentry Tracing

Configure Sentry's performance monitoring to track transactions and spans.

## Invoke This Skill When

- User asks to "enable tracing" or "add performance monitoring"
- User wants to track API response times, page loads, or latency
- User asks about `tracesSampleRate` or custom spans

## Quick Reference

| Platform | Enable | Custom Span |
|----------|--------|-------------|
| JS/Browser | `tracesSampleRate` + `browserTracingIntegration()` | `Sentry.startSpan()` |
| Next.js | `tracesSampleRate` (auto-integrated) | `Sentry.startSpan()` |
| Node.js | `tracesSampleRate` | `Sentry.startSpan()` |
| Python | `traces_sample_rate` | `@sentry_sdk.trace` or `start_span()` |
| Ruby | `traces_sample_rate` | `start_span()` |

## JavaScript Setup

### Enable tracing
```javascript
Sentry.init({
  dsn: "YOUR_DSN",
  tracesSampleRate: 1.0,  // 1.0 = 100%, lower for production
  integrations: [Sentry.browserTracingIntegration()],  // Browser/React only
  tracePropagationTargets: ["localhost", /^https:\/\/api\./],
});
```

### Custom spans
```javascript
// Async operation
const result = await Sentry.startSpan(
  { name: "fetch-user", op: "http.client" },
  async () => {
    return await fetch("/api/user").then(r => r.json());
  }
);

// Nested spans
await Sentry.startSpan({ name: "checkout", op: "transaction" }, async () => {
  await Sentry.startSpan({ name: "validate", op: "validation" }, validateCart);
  await Sentry.startSpan({ name: "payment", op: "payment" }, processPayment);
});
```

### Dynamic sampling
```javascript
tracesSampler: ({ name, parentSampled }) => {
  if (name.includes("healthcheck")) return 0;
  if (name.includes("checkout")) return 1.0;
  if (parentSampled !== undefined) return parentSampled;
  return 0.1;
},
```

## Python Setup

### Enable tracing
```python
sentry_sdk.init(
    dsn="YOUR_DSN",
    traces_sample_rate=1.0,
)
```

### Custom spans
```python
# Decorator
@sentry_sdk.trace
def expensive_function():
    return do_work()

# Context manager
with sentry_sdk.start_span(name="process-order", op="task") as span:
    span.set_data("order.id", order_id)
    process(order_id)
```

### Dynamic sampling
```python
def traces_sampler(ctx):
    name = ctx.get("transaction_context", {}).get("name", "")
    if "healthcheck" in name: return 0
    if "checkout" in name: return 1.0
    return 0.1

sentry_sdk.init(dsn="YOUR_DSN", traces_sampler=traces_sampler)
```

## Ruby Setup

```ruby
Sentry.init do |config|
  config.dsn = "YOUR_DSN"
  config.traces_sample_rate = 1.0
end
```

## Common Operation Types

| `op` Value | Use Case |
|------------|----------|
| `http.client` | Outgoing HTTP |
| `http.server` | Incoming HTTP |
| `db` / `db.query` | Database |
| `cache` | Cache operations |
| `task` | Background jobs |
| `function` | Function calls |

## Sampling Recommendations

| Traffic | Rate |
|---------|------|
| Development | `1.0` |
| Low (<1K req/min) | `0.5 - 1.0` |
| Medium (1K-10K) | `0.1 - 0.5` |
| High (>10K) | `0.01 - 0.1` |

## Distributed Tracing

Configure `tracePropagationTargets` to send trace headers to your APIs:
```javascript
tracePropagationTargets: ["localhost", "https://api.yourapp.com"],
```

For Next.js 14+ App Router, add to root layout:
```typescript
export async function generateMetadata() {
  return { other: { ...Sentry.getTraceData() } };
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Transactions not appearing | Check `tracesSampleRate > 0`, verify DSN |
| Browser traces missing | Add `browserTracingIntegration()` |
| Distributed traces disconnected | Check `tracePropagationTargets`, CORS headers |
| Too many transactions | Lower sample rate, use `tracesSampler` to filter |
