---
name: error-tracking
description: Track errors with CloudWatch Logs, implement structured logging, and monitor application health. Use when debugging production issues, investigating errors, or improving observability.
allowed-tools: Read, Edit, Write, Bash, Grep
---

# Error Tracking Skill

This skill helps you track and debug errors in production using CloudWatch Logs and structured logging.

## When to Use This Skill

- Investigating production errors
- Monitoring application health
- Debugging intermittent issues
- Analyzing error patterns
- Setting up alerting
- Improving observability
- Troubleshooting user-reported issues

## Logging Infrastructure

### CloudWatch Logs

AWS Lambda functions automatically log to CloudWatch:

```
CloudWatch Log Groups:
├── /aws/lambda/sgcarstrends-api-prod
├── /aws/lambda/sgcarstrends-web-prod
└── /aws/lambda/sgcarstrends-workflows-prod
```

## Structured Logging

### Logger Setup

```typescript
// packages/utils/src/logger.ts
import pino from "pino";

export const logger = pino({
  level: process.env.LOG_LEVEL || "info",
  formatters: {
    level: (label) => ({ level: label }),
  },
  timestamp: pino.stdTimeFunctions.isoTime,
  base: {
    env: process.env.NODE_ENV,
    service: process.env.SERVICE_NAME,
  },
});

// Export typed logger methods
export const log = {
  info: (message: string, data?: Record<string, unknown>) => {
    logger.info(data, message);
  },
  error: (message: string, error: Error, data?: Record<string, unknown>) => {
    logger.error(
      {
        ...data,
        error: {
          message: error.message,
          stack: error.stack,
          name: error.name,
        },
      },
      message
    );
  },
  warn: (message: string, data?: Record<string, unknown>) => {
    logger.warn(data, message);
  },
  debug: (message: string, data?: Record<string, unknown>) => {
    logger.debug(data, message);
  },
};
```

### Usage in Code

```typescript
// apps/api/src/routes/cars.ts
import { log } from "@sgcarstrends/utils/logger";

export const getCars = async (c: Context) => {
  try {
    log.info("Fetching cars", {
      month: c.req.query("month"),
      userId: c.get("userId"),
    });

    const cars = await db.query.cars.findMany();

    log.info("Cars fetched successfully", {
      count: cars.length,
    });

    return c.json(cars);
  } catch (error) {
    log.error("Failed to fetch cars", error as Error, {
      month: c.req.query("month"),
    });

    return c.json({ error: "Failed to fetch cars" }, 500);
  }
};
```

## Viewing Logs

### AWS CLI

```bash
# View recent logs
aws logs tail /aws/lambda/sgcarstrends-api-prod --follow

# Filter by error level
aws logs tail /aws/lambda/sgcarstrends-api-prod \
  --filter-pattern "ERROR"

# View logs from specific time range
aws logs filter-log-events \
  --log-group-name /aws/lambda/sgcarstrends-api-prod \
  --start-time $(($(date +%s) - 3600))000 \
  --end-time $(date +%s)000 \
  --filter-pattern "ERROR"

# Search for specific message
aws logs filter-log-events \
  --log-group-name /aws/lambda/sgcarstrends-api-prod \
  --filter-pattern "Failed to fetch cars"
```

### SST Console

```bash
# Open SST console
cd apps/api
sst dev

# View logs in browser
# Navigate to Functions → sgcarstrends-api-prod → Logs
```

## Error Patterns

### Common Error Logging

```typescript
// Database errors
try {
  const result = await db.query.cars.findMany();
} catch (error) {
  log.error("Database query failed", error as Error, {
    query: "cars.findMany",
    retryable: true,
  });
  throw error;
}

// External API errors
try {
  const response = await fetch(url);
  if (!response.ok) {
    log.error("External API error", new Error("API request failed"), {
      url,
      status: response.status,
      statusText: response.statusText,
    });
  }
} catch (error) {
  log.error("External API request failed", error as Error, {
    url,
  });
}

// Validation errors
const result = schema.safeParse(data);
if (!result.success) {
  log.warn("Validation failed", {
    errors: result.error.issues,
    data,
  });
  return c.json({ error: "Invalid request" }, 400);
}

// Authentication errors
if (!user) {
  log.warn("Unauthorized access attempt", {
    path: c.req.path,
    ip: c.req.header("x-forwarded-for"),
  });
  return c.json({ error: "Unauthorized" }, 401);
}
```

## CloudWatch Insights

### Query Logs

```sql
-- Find all errors in last hour
fields @timestamp, @message, level, error.message
| filter level = "error"
| sort @timestamp desc
| limit 100

-- Count errors by type
fields error.name
| filter level = "error"
| stats count() by error.name
| sort count() desc

-- Find slow requests
fields @timestamp, @message, duration
| filter level = "info" and @message like /Request completed/
| filter duration > 1000
| sort duration desc

-- Track error rate over time
fields @timestamp
| filter level = "error"
| stats count() as ErrorCount by bin(5m)

-- Find errors for specific user
fields @timestamp, @message, userId, error.message
| filter level = "error" and userId = "user123"
| sort @timestamp desc
```

### Common Queries

```sql
-- Database connection errors
fields @timestamp, @message, error.message
| filter error.message like /connection/
| sort @timestamp desc

-- Memory errors
fields @timestamp, @message, error.message
| filter error.message like /memory/ or error.message like /heap/
| sort @timestamp desc

-- Timeout errors
fields @timestamp, @message, error.message
| filter error.message like /timeout/ or error.message like /timed out/
| sort @timestamp desc

-- Rate limit errors
fields @timestamp, @message, error.message
| filter error.message like /rate limit/ or error.message like /too many requests/
| sort @timestamp desc
```

## Error Monitoring

### CloudWatch Alarms

```typescript
// infra/monitoring.ts
import { Alarm } from "sst/constructs";

export function Monitoring({ stack }: StackContext) {
  // Error rate alarm
  new Alarm(stack, "HighErrorRate", {
    sns: {
      topicArn: process.env.SNS_TOPIC_ARN,
    },
    alarm: (props) => ({
      alarmName: "sgcarstrends-high-error-rate",
      evaluationPeriods: 2,
      threshold: 10,
      comparisonOperator: "GreaterThanThreshold",
      metric: new Metric({
        namespace: "AWS/Lambda",
        metricName: "Errors",
        dimensions: {
          FunctionName: props.functionName,
        },
        statistic: "Sum",
        period: Duration.minutes(5),
      }),
    }),
  });

  // High latency alarm
  new Alarm(stack, "HighLatency", {
    sns: {
      topicArn: process.env.SNS_TOPIC_ARN,
    },
    alarm: (props) => ({
      alarmName: "sgcarstrends-high-latency",
      evaluationPeriods: 3,
      threshold: 1000,  // 1 second
      comparisonOperator: "GreaterThanThreshold",
      metric: new Metric({
        namespace: "AWS/Lambda",
        metricName: "Duration",
        dimensions: {
          FunctionName: props.functionName,
        },
        statistic: "Average",
        period: Duration.minutes(5),
      }),
    }),
  });
}
```

## Error Aggregation

### Group Similar Errors

```typescript
// packages/utils/src/error-tracker.ts
interface ErrorGroup {
  fingerprint: string;
  message: string;
  count: number;
  lastSeen: Date;
  firstSeen: Date;
}

export class ErrorTracker {
  private errors: Map<string, ErrorGroup> = new Map();

  track(error: Error, context?: Record<string, unknown>) {
    const fingerprint = this.getFingerprint(error);

    const existing = this.errors.get(fingerprint);
    if (existing) {
      existing.count++;
      existing.lastSeen = new Date();
    } else {
      this.errors.set(fingerprint, {
        fingerprint,
        message: error.message,
        count: 1,
        lastSeen: new Date(),
        firstSeen: new Date(),
      });
    }

    // Log error
    log.error("Error tracked", error, {
      ...context,
      fingerprint,
      count: this.errors.get(fingerprint)?.count,
    });
  }

  private getFingerprint(error: Error): string {
    // Create fingerprint from error type and message
    const parts = [
      error.name,
      error.message.replace(/\d+/g, "N"),  // Replace numbers
      error.stack?.split("\n")[1],  // First stack frame
    ];
    return parts.filter(Boolean).join("|");
  }

  getTopErrors(limit = 10): ErrorGroup[] {
    return Array.from(this.errors.values())
      .sort((a, b) => b.count - a.count)
      .slice(0, limit);
  }
}
```

## Best Practices

### 1. Log Context

```typescript
// ❌ No context
log.error("Error occurred", error);

// ✅ With context
log.error("Failed to process payment", error, {
  userId: user.id,
  amount: payment.amount,
  currency: payment.currency,
  paymentId: payment.id,
});
```

### 2. Use Structured Logs

```typescript
// ❌ String concatenation
console.log(`User ${userId} performed action ${action}`);

// ✅ Structured logging
log.info("User action", {
  userId,
  action,
  timestamp: new Date().toISOString(),
});
```

### 3. Don't Log Sensitive Data

```typescript
// ❌ Logging sensitive data
log.info("User logged in", {
  email: user.email,
  password: user.password,  // NEVER log passwords!
  creditCard: user.creditCard,
});

// ✅ Safe logging
log.info("User logged in", {
  userId: user.id,
  email: user.email.replace(/(?<=.{2}).(?=.*@)/g, "*"),  // Mask email
});
```

### 4. Set Appropriate Log Levels

```typescript
// Production
log.debug("Database query", { query });  // Not logged in prod
log.info("Request completed", { duration });  // Logged
log.warn("Cache miss", { key });  // Logged
log.error("Database error", error);  // Logged

// Development
// All levels logged
```

## Debugging Production Issues

### Step-by-Step Process

```bash
# 1. Identify the issue
# Check CloudWatch Logs for errors
aws logs tail /aws/lambda/sgcarstrends-api-prod --filter-pattern "ERROR"

# 2. Find error pattern
# Search for similar errors
aws logs filter-log-events \
  --log-group-name /aws/lambda/sgcarstrends-api-prod \
  --filter-pattern "Failed to fetch cars"

# 3. Check error context
# View logs with context
aws logs get-log-events \
  --log-group-name /aws/lambda/sgcarstrends-api-prod \
  --log-stream-name 2024/01/15/[$LATEST]abc123 \
  --start-from-head

# 4. Analyze error frequency
# Use CloudWatch Insights
# Query: Count errors by type

# 5. Reproduce locally
# Use error context to reproduce

# 6. Fix and deploy
# Create fix, test, deploy

# 7. Verify fix
# Monitor logs after deployment
aws logs tail /aws/lambda/sgcarstrends-api-prod --follow
```

## Troubleshooting

### Logs Not Appearing

```bash
# Issue: Logs not showing in CloudWatch
# Solution: Check Lambda execution role permissions

# Ensure Lambda has CloudWatch Logs permissions:
# - logs:CreateLogGroup
# - logs:CreateLogStream
# - logs:PutLogEvents
```

### Too Many Logs

```bash
# Issue: Too much logging causing high costs
# Solution: Adjust log level and retention

# Set log level in production
LOG_LEVEL=info

# Reduce retention period
aws logs put-retention-policy \
  --log-group-name /aws/lambda/sgcarstrends-api-prod \
  --retention-in-days 7
```

### Cannot Find Specific Error

```bash
# Issue: Can't find error in logs
# Solution: Improve search with CloudWatch Insights

# Use more specific filters
fields @timestamp, @message
| filter @message like /specific pattern/
| sort @timestamp desc
```

## References

- AWS CloudWatch Logs: https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/
- CloudWatch Insights: https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html
- Pino Logger: https://getpino.io
- Related files:
  - `packages/utils/src/logger.ts` - Logger configuration
  - Root CLAUDE.md - Logging guidelines

## Best Practices Summary

1. **Structured Logging**: Use structured logs with context
2. **Appropriate Levels**: Use correct log levels (debug, info, warn, error)
3. **Don't Log Secrets**: Never log sensitive data
4. **Add Context**: Include relevant context for debugging
5. **Monitor Errors**: Set up CloudWatch Alarms
6. **Aggregate Errors**: Group similar errors together
7. **Log Retention**: Set appropriate retention periods
8. **Use Insights**: Leverage CloudWatch Insights for analysis
