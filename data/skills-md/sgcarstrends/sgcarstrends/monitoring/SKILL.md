---
name: monitoring
description: Monitor AWS resources, debug production issues, check Lambda logs, and implement structured logging. Use when investigating errors, checking CloudWatch logs, debugging deployment failures, improving observability, or setting up alarms.
allowed-tools: Bash, Read, Edit, Write, Grep
---

# Monitoring Skill

Combines AWS monitoring, CloudWatch logs, and error tracking.

## Viewing Logs

### SST Console

```bash
npx sst console --stage production
npx sst logs --stage production --function api --tail
npx sst logs --stage production --function api --filter "ERROR" --since 1h
```

### AWS CLI

```bash
# Tail logs
aws logs tail "/aws/lambda/sgcarstrends-api-production" --follow

# Filter logs
aws logs filter-log-events \
  --log-group-name "/aws/lambda/sgcarstrends-api-production" \
  --filter-pattern "ERROR" \
  --start-time $(date -u -d '1 hour ago' +%s)000
```

## CloudWatch Metrics

```bash
# Lambda errors
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Errors \
  --dimensions Name=FunctionName,Value=sgcarstrends-api-production \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Sum

# Lambda duration
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Duration \
  --dimensions Name=FunctionName,Value=sgcarstrends-api-production \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Average,Maximum
```

## CloudWatch Insights Queries

```sql
-- Find all errors
fields @timestamp, @message, level, error.message
| filter level = "error"
| sort @timestamp desc
| limit 100

-- Count errors by type
fields error.name
| filter level = "error"
| stats count() by error.name

-- Slow requests
fields @timestamp, @duration
| filter @duration > 1000
| sort @duration desc

-- Error rate over time
fields @timestamp
| filter level = "error"
| stats count() as ErrorCount by bin(5m)
```

## Structured Logging

```typescript
// packages/utils/src/logger.ts
import pino from "pino";

export const log = {
  info: (message: string, data?: Record<string, unknown>) => logger.info(data, message),
  error: (message: string, error: Error, data?: Record<string, unknown>) => {
    logger.error({ ...data, error: { message: error.message, stack: error.stack } }, message);
  },
  warn: (message: string, data?: Record<string, unknown>) => logger.warn(data, message),
};

// Usage
log.info("Fetching cars", { month: "2024-01" });
log.error("Failed to fetch cars", error, { month: "2024-01" });
```

## CloudWatch Alarms

```typescript
// infra/alarms.ts
new cloudwatch.Alarm(stack, "ApiHighErrorRate", {
  metric: api.metricErrors(),
  threshold: 10,
  evaluationPeriods: 2,
  alarmDescription: "API has high error rate",
}).addAlarmAction(new cloudwatch.SnsAction(alarmTopic));
```

## Health Checks

```bash
# Test API
curl -f https://api.sgcarstrends.com/health || echo "API unhealthy"

# Test web
curl -f https://sgcarstrends.com || echo "Web unhealthy"

# Database connectivity
psql $DATABASE_URL -c "SELECT 1" || echo "Database unreachable"
```

## Debugging Production Issues

```bash
# 1. Check recent errors
npx sst logs --stage production --function api --filter "ERROR" --since 1h

# 2. Get Lambda metrics
aws cloudwatch get-metric-statistics --namespace AWS/Lambda --metric-name Errors ...

# 3. Test endpoint directly
curl -v https://api.sgcarstrends.com/health

# 4. Check stack events
aws cloudformation describe-stack-events --stack-name sgcarstrends-api-production --max-items 50
```

## Common Issues

| Issue | Investigation | Solution |
|-------|--------------|----------|
| High latency | Check duration metrics, slow queries | Increase memory, optimize queries, add caching |
| High error rate | Check error logs, external services | Fix bugs, add error handling, check rate limits |
| Cold starts | Check init duration, package size | Provisioned concurrency, reduce bundle, ARM |

## Best Practices

1. **Structured Logging**: Use JSON format with context
2. **Log Levels**: DEBUG for dev, INFO+ for prod
3. **Don't Log Secrets**: Never log passwords, tokens, keys
4. **Set Alarms**: Monitor error rate and latency
5. **Log Retention**: 7-30 days to balance cost/debugging

## References

- CloudWatch: https://docs.aws.amazon.com/cloudwatch
- Lambda Monitoring: https://docs.aws.amazon.com/lambda/latest/dg/monitoring-functions.html
- Pino Logger: https://getpino.io
