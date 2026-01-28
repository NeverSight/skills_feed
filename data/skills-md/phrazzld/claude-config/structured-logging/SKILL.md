---
name: structured-logging
description: "Apply structured logging best practices using Pino for Node.js applications: JSON output, log levels, context, redaction, correlation IDs, and centralization. Use when implementing logging, reviewing log statements, or discussing observability."
---

# Structured Logging

Best practices for production-ready logging in Node.js applications using Pino and structured JSON output.

## Philosophy

**Logs are data, not text.** Structured logging treats every log entry as a queryable data point, enabling powerful analysis, alerting, and debugging in production.

**Three core principles:**
1. **Machine-readable first**: JSON structure enables programmatic querying
2. **Context-rich**: Include all relevant metadata (correlation IDs, user IDs, request info)
3. **Security-conscious**: Never log sensitive data (passwords, tokens, PII)

## Why Pino

**Pino is the recommended logging library for Node.js (2025):**
- **5x faster than Winston**: Minimal CPU overhead, async by default
- **Structured JSON**: Every log is a JSON object, no string templates
- **Low latency**: Critical for high-throughput applications
- **Async transports**: Heavy operations (file writes, network calls) happen in worker threads
- **Child loggers**: Easy context propagation
- **Redaction built-in**: Automatic sensitive data removal

### Performance Comparison

| Library | Logs/Second | CPU Usage | Memory |
|---------|-------------|-----------|---------|
| **Pino** | 50,000+ | 2-4% | ~45MB |
| Winston | ~10,000 | 10-15% | ~180MB |
| Bunyan | ~15,000 | 8-12% | ~150MB |

## Installation & Setup

```bash
# Install Pino and pretty-printing for development
pnpm add pino
pnpm add -D pino-pretty
```

## Basic Configuration

```typescript
// lib/logger.ts
import pino from 'pino'

const isDevelopment = process.env.NODE_ENV === 'development'

export const logger = pino({
  level: process.env.LOG_LEVEL || 'info',

  // Use pretty printing in development, JSON in production
  transport: isDevelopment
    ? {
        target: 'pino-pretty',
        options: {
          colorize: true,
          translateTime: 'SYS:standard',
          ignore: 'pid,hostname',
        },
      }
    : undefined,

  // Base context included in every log
  base: {
    env: process.env.NODE_ENV || 'development',
    revision: process.env.VERCEL_GIT_COMMIT_SHA || 'local',
  },

  // Format timestamps as ISO 8601
  timestamp: pino.stdTimeFunctions.isoTime,

  // Redact sensitive fields automatically
  redact: {
    paths: [
      'password',
      'passwordHash',
      'secret',
      'apiKey',
      'token',
      'accessToken',
      'refreshToken',
      'authorization',
      'cookie',
      'req.headers.authorization',
      'req.headers.cookie',
      '*.password',
      '*.passwordHash',
      '*.secret',
      '*.apiKey',
      '*.token',
    ],
    censor: '[REDACTED]',
  },
})

// Export type for use in application
export type Logger = typeof logger
```

## Log Levels

Pino supports six log levels (from lowest to highest):

```typescript
logger.trace('Extremely detailed debugging')  // Level 10
logger.debug('Detailed debugging')            // Level 20
logger.info('General information')            // Level 30
logger.warn('Warning, non-critical issue')    // Level 40
logger.error('Error, requires attention')     // Level 50
logger.fatal('Fatal error, app cannot continue') // Level 60
```

**When to use each level:**

- **trace**: Function entry/exit, loop iterations (extremely verbose)
- **debug**: Variable values, conditional branches, algorithm steps
- **info**: HTTP requests, user actions, state changes, startup/shutdown
- **warn**: Deprecated API usage, retry attempts, degraded performance
- **error**: Exceptions caught, failed operations, data validation errors
- **fatal**: Database connection lost, critical service unavailable, unrecoverable errors

**Production recommendation**: Set `LOG_LEVEL=info` by default, use `debug` or `trace` only when debugging specific issues.

## Child Loggers (Context Propagation)

Create child loggers to add context that persists across multiple log statements:

```typescript
// Without child logger (repetitive)
logger.info({ userId: '123', requestId: 'abc' }, 'User logged in')
logger.info({ userId: '123', requestId: 'abc' }, 'Profile fetched')
logger.info({ userId: '123', requestId: 'abc' }, 'Settings updated')

// With child logger (clean)
const requestLogger = logger.child({ userId: '123', requestId: 'abc' })
requestLogger.info('User logged in')
requestLogger.info('Profile fetched')
requestLogger.info('Settings updated')
```

### Middleware Pattern (Express/Next.js)

```typescript
// middleware/logging.ts
import { v4 as uuidv4 } from 'uuid'
import { logger } from '@/lib/logger'
import type { NextRequest } from 'next/server'

export function createRequestLogger(req: NextRequest) {
  // Generate correlation ID for request tracing
  const correlationId = req.headers.get('x-correlation-id') || uuidv4()

  // Create child logger with request context
  return logger.child({
    correlationId,
    method: req.method,
    path: req.nextUrl.pathname,
    userAgent: req.headers.get('user-agent'),
    ip: req.headers.get('x-forwarded-for') || req.headers.get('x-real-ip'),
  })
}

// Usage in API route
export async function GET(req: NextRequest) {
  const log = createRequestLogger(req)

  log.info('Processing request')

  try {
    const data = await fetchData()
    log.info({ dataCount: data.length }, 'Data fetched successfully')
    return Response.json(data)
  } catch (error) {
    log.error({ error }, 'Failed to fetch data')
    return Response.json({ error: 'Internal error' }, { status: 500 })
  }
}
```

## Structured Logging Patterns

### ✅ Good: Structured Fields

```typescript
// Queryable, analyzable
logger.info({
  event: 'user_login',
  userId: user.id,
  email: user.email,
  provider: 'google',
  duration: 150,
}, 'User authenticated')

// Easy queries:
// - All Google logins: event='user_login' AND provider='google'
// - Slow logins: event='user_login' AND duration > 1000
// - Specific user: event='user_login' AND userId='123'
```

### ❌ Bad: String Templates

```typescript
// Not queryable, hard to parse
logger.info(`User ${user.email} logged in via ${provider} in ${duration}ms`)

// Cannot easily query by provider or filter by duration
```

### Error Logging

```typescript
// ✅ Good: Include error object with structured context
try {
  await riskyOperation()
} catch (error) {
  logger.error({
    error,
    operation: 'riskyOperation',
    userId: user.id,
    retryCount: 3,
  }, 'Operation failed after retries')
}

// ❌ Bad: Lose stack trace and context
try {
  await riskyOperation()
} catch (error) {
  logger.error(`Operation failed: ${error.message}`)
}
```

**Note on Error serialization:** Pino handles Error objects natively, but `JSON.stringify(new Error("msg"))` returns `{}` because `message`, `name`, `stack` are non-enumerable. For custom loggers, manually extract:

```typescript
function serializeError(err: unknown): Record<string, unknown> {
  if (err instanceof Error) {
    return { name: err.name, message: err.message, stack: err.stack };
  }
  return { value: String(err) };
}
```

### Performance Logging

```typescript
// Track operation duration
const startTime = Date.now()

try {
  const result = await fetchFromDatabase(query)
  const duration = Date.now() - startTime

  logger.info({
    event: 'database_query',
    query: query.type,
    duration,
    resultCount: result.length,
  }, 'Query completed')

  // Alert if slow
  if (duration > 1000) {
    logger.warn({
      event: 'slow_query',
      query: query.type,
      duration,
    }, 'Database query exceeded threshold')
  }

  return result
} catch (error) {
  logger.error({
    error,
    event: 'database_error',
    query: query.type,
    duration: Date.now() - startTime,
  }, 'Query failed')
  throw error
}
```

## Correlation IDs (Request Tracing)

Correlation IDs enable tracing a single request through multiple services and log statements.

```typescript
// middleware/correlation.ts
import { v4 as uuidv4 } from 'uuid'

export function correlationMiddleware(req: Request, res: Response, next: NextFunction) {
  // Extract or generate correlation ID
  const correlationId = req.headers['x-correlation-id'] || uuidv4()

  // Add to response headers for client
  res.setHeader('x-correlation-id', correlationId)

  // Attach logger with correlation ID to request
  req.log = logger.child({ correlationId })

  next()
}

// Usage in route
app.get('/api/users', async (req, res) => {
  req.log.info('Fetching users')

  const users = await fetchUsers()
  req.log.info({ count: users.length }, 'Users fetched')

  res.json(users)
})

// All logs will include the same correlationId:
// {"level":"info","correlationId":"abc-123","msg":"Fetching users"}
// {"level":"info","correlationId":"abc-123","count":42,"msg":"Users fetched"}
```

## Sensitive Data Redaction

**Critical security practice**: Never log sensitive information.

### Automatic Redaction (configured in setup)

```typescript
// Pino automatically redacts these fields (from setup above)
logger.info({
  user: {
    email: 'user@example.com',
    password: 'secret123',  // Will be [REDACTED]
  },
  apiKey: 'sk_live_123',    // Will be [REDACTED]
}, 'User data processed')

// Output:
// {
//   "user": {
//     "email": "user@example.com",
//     "password": "[REDACTED]"
//   },
//   "apiKey": "[REDACTED]",
//   "msg": "User data processed"
// }
```

### Manual Redaction for Dynamic Fields

```typescript
// Utility function for safe logging
function sanitizeForLogging<T extends Record<string, any>>(obj: T): T {
  const sensitivePatterns = [
    /password/i,
    /secret/i,
    /token/i,
    /key/i,
    /authorization/i,
  ]

  const sanitized = { ...obj }

  for (const key in sanitized) {
    if (sensitivePatterns.some(pattern => pattern.test(key))) {
      sanitized[key] = '[REDACTED]'
    }
  }

  return sanitized
}

// Usage
logger.info(sanitizeForLogging(userData), 'User updated')
```

## Convex-Specific Logging

Convex functions run in a managed environment with built-in logging, but structured logging still applies:

```typescript
// convex/users.ts
import { query } from './_generated/server'
import { v } from 'convex/values'

export const getUser = query({
  args: { userId: v.id('users') },
  handler: async (ctx, args) => {
    // Use console with structured data
    console.info({
      operation: 'getUser',
      userId: args.userId,
      timestamp: Date.now(),
    })

    try {
      const user = await ctx.db.get(args.userId)

      if (!user) {
        console.warn({
          operation: 'getUser',
          userId: args.userId,
          result: 'not_found',
        })
        return null
      }

      console.info({
        operation: 'getUser',
        userId: args.userId,
        result: 'success',
      })

      return user
    } catch (error) {
      console.error({
        operation: 'getUser',
        userId: args.userId,
        error: error.message,
      })
      throw error
    }
  },
})
```

**Note**: Convex console.log/info/error are automatically structured in the dashboard. Use objects instead of strings for better filtering.

## Centralization & Observability

In production, centralize logs to a log aggregation service:

### Option 1: Datadog (Recommended for Enterprise)

```typescript
// lib/logger.ts
import pino from 'pino'

const logger = pino({
  // ... base config

  transport: {
    target: 'pino-datadog-transport',
    options: {
      apiKey: process.env.DATADOG_API_KEY,
      service: 'my-app',
      env: process.env.NODE_ENV,
      tags: ['team:engineering', 'project:webapp'],
    },
  },
})
```

### Option 2: Graylog (Self-Hosted)

```typescript
import pino from 'pino'

const logger = pino({
  transport: {
    target: 'pino-socket',
    options: {
      address: process.env.GRAYLOG_HOST,
      port: 12201,
      mode: 'udp',
    },
  },
})
```

### Option 3: Vercel Log Drains (for Next.js on Vercel)

Vercel automatically collects logs and can forward to:
- Datadog
- LogDNA
- Logtail
- New Relic
- Sentry
- Custom HTTPS endpoints

Configure in Vercel Dashboard → Project → Settings → Log Drains

### Querying Logs

With centralized structured logs, you can query efficiently:

```
# Datadog query
service:my-app AND env:production AND level:error AND @userId:123

# Find slow database queries
service:my-app AND event:database_query AND duration > 1000

# Track user journey
service:my-app AND @correlationId:abc-123-def
```

## Testing & Development

### Development: Pretty Printing

```bash
# Pretty output for development
NODE_ENV=development pnpm dev

# Raw JSON for testing centralization
NODE_ENV=production pnpm dev
```

### Testing: Log Capture

```typescript
// test/logger.test.ts
import { describe, it, expect, vi } from 'vitest'
import { logger } from '@/lib/logger'

describe('Logger', () => {
  it('redacts sensitive fields', () => {
    const logSpy = vi.spyOn(logger, 'info')

    logger.info({
      email: 'user@example.com',
      password: 'secret',
    }, 'User data')

    expect(logSpy).toHaveBeenCalledWith(
      expect.objectContaining({
        email: 'user@example.com',
        password: '[REDACTED]',
      }),
      'User data'
    )
  })
})
```

## Best Practices Summary

### Do ✅

- **Use structured JSON**: `{ userId: '123', action: 'login' }` not `"User 123 logged in"`
- **Include context**: Add all relevant fields (IDs, timestamps, metadata)
- **Use correlation IDs**: Track requests across services
- **Redact sensitive data**: Passwords, tokens, PII automatically filtered
- **Log at appropriate levels**: info for normal flow, error for failures
- **Use child loggers**: Add context once, reuse across log statements
- **Centralize in production**: Send logs to Datadog/Graylog/ELK
- **Query your logs**: Use structured fields for powerful analysis

### Don't ❌

- **Don't use string templates**: Breaks queryability
- **Don't log sensitive data**: Passwords, tokens, credit cards, SSNs
- **Don't log in tight loops**: Excessive logs hurt performance
- **Don't ignore log levels**: Trace/debug should be off in production
- **Don't concatenate error messages**: Log full error object with stack
- **Don't use console.log in production**: Use proper logging library
- **Don't skip correlation IDs**: Makes debugging multi-service flows impossible

## Quick Setup Checklist

For a new Node.js/Next.js project:

- [ ] Install Pino: `pnpm add pino pino-pretty`
- [ ] Create logger singleton in `lib/logger.ts`
- [ ] Configure redaction for sensitive fields
- [ ] Set up correlation ID middleware
- [ ] Create child logger pattern for requests
- [ ] Configure pretty printing for development
- [ ] Set up log transport for production (Datadog/Graylog)
- [ ] Add environment variable: `LOG_LEVEL`
- [ ] Test redaction with unit tests
- [ ] Document logging patterns in project README

## Philosophy

**"Logs are the voice of your production application."**

Structured logging transforms logs from debug statements into queryable data. In production, logs enable:
- **Debugging**: Trace requests, find errors, understand behavior
- **Monitoring**: Track metrics, detect anomalies, set alerts
- **Analytics**: Understand user behavior, measure performance
- **Security**: Detect attacks, audit access, investigate incidents

Invest in logging infrastructure early. The cost is minimal; the value is immense.

---

When agents implement logging, they should:
- Default to Pino for Node.js applications (5x faster than Winston)
- Use structured JSON fields, not string templates
- Include correlation IDs for request tracing
- Redact sensitive fields automatically
- Use child loggers for context propagation
- Log at appropriate levels (info for normal, error for failures)
- Centralize logs in production (Datadog, Graylog, or Vercel Log Drains)
- Never log passwords, tokens, API keys, or PII
