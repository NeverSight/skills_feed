---
name: observability
description: Guidelines for implementing observability in applications.
allowed-tools: Read, Write, Edit
metadata:
  scope: [root]
  auto_invoke: "Working with observability"
---

# Observability and Monitoring Practices

You are an expert in observability, monitoring, and distributed systems debugging.

## Logging Best Practices

- Use structured logging (JSON format)
- Include correlation IDs for request tracing
- Log at appropriate levels (ERROR, WARN, INFO, DEBUG)
- Avoid logging sensitive information
- Implement log aggregation and centralization

## Metrics Implementation

- Follow the Four Golden Signals (latency, traffic, errors, saturation)
- Use standard metric naming conventions
- Implement custom business metrics
- Set up meaningful dashboards
- Define SLIs, SLOs, and error budgets

## Distributed Tracing

- Implement OpenTelemetry for vendor-neutral tracing
- Add spans for critical operations
- Include relevant context in span attributes
- Sample traces appropriately for performance
- Correlate traces with logs and metrics

## Alerting Strategy

- Alert on symptoms, not causes
- Define clear escalation policies
- Avoid alert fatigue with proper thresholds
- Include runbooks in alert descriptions
- Test alerts regularly

## Implementation Examples

### Structured Logging
```javascript
// Good: Structured logging with context
logger.info({
  event: 'user_login',
  userId: user.id,
  correlationId: req.correlationId,
  duration: Date.now() - startTime,
  metadata: {
    ipAddress: req.ip,
    userAgent: req.headers['user-agent']
  }
});
```

### Metrics
```javascript
// Good: Metric with labels
metrics.increment('api_requests_total', {
  method: req.method,
  endpoint: req.route.path,
  status: res.statusCode
});
```

## Performance Monitoring

- Monitor application performance metrics (APM)
- Track database query performance
- Implement real user monitoring (RUM)
- Monitor third-party service dependencies
- Set up synthetic monitoring for critical paths

## Best Practices

- Implement observability from the start
- Use consistent naming across metrics, logs, and traces
- Document your observability strategy
- Regularly review and update dashboards
- Practice incident response procedures
