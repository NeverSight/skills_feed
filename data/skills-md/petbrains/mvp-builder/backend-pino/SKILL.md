---
name: backend-pino
description: High-performance structured JSON logging for Node.js. Use when building production APIs that need fast, structured logs for observability platforms (Datadog, ELK, CloudWatch). Provides request logging middleware, child loggers for context, and sensitive data redaction. Choose Pino over console.log for any production TypeScript backend.
allowed-tools: Read, Edit, Write, Bash (*)
---

# Pino (Structured Logging)

## Overview

Pino is the fastest JSON logger for Node.js. It outputs structured logs that integrate with observability platforms (Datadog, ELK, Splunk, CloudWatch).

**Version**: v9.x (2024-2025)  
**Performance**: ~5x faster than Winston, ~10x faster than Bunyan

**Key Benefit**: Structured JSON logs → easy parsing, filtering, and alerting in production.

## When to Use This Skill

✅ **Use Pino when:**
- Building production APIs
- Need structured JSON logs
- Integrating with observability platforms
- Require request tracing (correlation IDs)
- Must redact sensitive data (passwords, tokens)

❌ **Skip Pino when:**
- Simple scripts or CLI tools
- Early prototyping (console.log is fine)
- Client-side JavaScript

---

## Quick Start

### Installation

```bash
npm install pino pino-pretty
npm install -D @types/pino
```

### Basic Configuration

```typescript
// src/lib/logger.ts
import pino from 'pino';

const isDev = process.env.NODE_ENV === 'development';

export const logger = pino({
  level: process.env.LOG_LEVEL || (isDev ? 'debug' : 'info'),
  
  // Pretty print in development
  transport: isDev ? {
    target: 'pino-pretty',
    options: {
      colorize: true,
      translateTime: 'SYS:standard',
      ignore: 'pid,hostname',
    },
  } : undefined,
  
  // Redact sensitive fields
  redact: {
    paths: [
      'password',
      'token',
      'authorization',
      'cookie',
      '*.password',
      '*.token',
      'req.headers.authorization',
    ],
    censor: '[REDACTED]',
  },
  
  // Add base context to all logs
  base: {
    service: process.env.SERVICE_NAME || 'api',
    env: process.env.NODE_ENV,
    version: process.env.APP_VERSION,
  },
});

export default logger;
```

---

## Log Levels

```typescript
// In order of severity (lowest to highest)
logger.trace('Detailed debugging');     // level 10
logger.debug('Debug information');      // level 20
logger.info('Normal operation');        // level 30
logger.warn('Warning condition');       // level 40
logger.error('Error occurred');         // level 50
logger.fatal('App is crashing');        // level 60
```

### Level Configuration

```typescript
// Set via environment
LOG_LEVEL=debug npm start

// Or in code
const logger = pino({ level: 'debug' });
```

---

## Structured Logging

### Log Objects, Not Strings

```typescript
// ❌ Avoid string interpolation
logger.info(`User ${userId} logged in from ${ip}`);

// ✅ Use structured objects
logger.info({ userId, ip, action: 'login' }, 'User logged in');
```

### Output (JSON)

```json
{
  "level": 30,
  "time": 1702300800000,
  "service": "api",
  "userId": "user_123",
  "ip": "192.168.1.1",
  "action": "login",
  "msg": "User logged in"
}
```

---

## Child Loggers (Context)

### Request Context

```typescript
// Create child logger with request context
const requestLogger = logger.child({
  requestId: 'req_abc123',
  userId: 'user_456',
});

// All logs include context automatically
requestLogger.info('Processing request');
requestLogger.info({ orderId: 'order_789' }, 'Order created');
```

### Output

```json
{
  "requestId": "req_abc123",
  "userId": "user_456",
  "msg": "Processing request"
}
{
  "requestId": "req_abc123",
  "userId": "user_456",
  "orderId": "order_789",
  "msg": "Order created"
}
```

---

## Express Request Logging

### Middleware

```typescript
// src/middleware/request-logger.ts
import { randomUUID } from 'crypto';
import { Request, Response, NextFunction } from 'express';
import { logger } from '../lib/logger';

// Extend Express Request type
declare global {
  namespace Express {
    interface Request {
      log: typeof logger;
      requestId: string;
    }
  }
}

export function requestLogger(req: Request, res: Response, next: NextFunction) {
  const requestId = (req.headers['x-request-id'] as string) || randomUUID();
  const start = Date.now();

  // Create child logger with request context
  const childLogger = logger.child({
    requestId,
    method: req.method,
    path: req.path,
    userAgent: req.headers['user-agent'],
  });

  // Attach to request for use in handlers
  req.log = childLogger;
  req.requestId = requestId;

  // Set response header for tracing
  res.setHeader('x-request-id', requestId);

  // Log request start
  childLogger.info('Request started');

  // Log request completion
  res.on('finish', () => {
    childLogger.info({
      statusCode: res.statusCode,
      duration: Date.now() - start,
    }, 'Request completed');
  });

  next();
}
```

### Usage in Express

```typescript
// src/app.ts
import express from 'express';
import { requestLogger } from './middleware/request-logger';

const app = express();
app.use(requestLogger);

app.get('/users/:id', async (req, res) => {
  req.log.info({ userId: req.params.id }, 'Fetching user');
  
  try {
    const user = await getUser(req.params.id);
    req.log.debug({ user }, 'User found');
    res.json(user);
  } catch (error) {
    req.log.error({ error }, 'Failed to fetch user');
    res.status(500).json({ error: 'Internal error' });
  }
});
```

---

## tRPC Logging Middleware

```typescript
// src/server/middleware/logging.ts
import { middleware } from '../trpc';
import { logger } from '@/lib/logger';

export const loggerMiddleware = middleware(async ({ path, type, next, ctx }) => {
  const start = Date.now();
  const log = ctx.log || logger;
  
  log.debug({ path, type }, 'tRPC procedure started');

  try {
    const result = await next();
    
    log.info({
      path,
      type,
      duration: Date.now() - start,
    }, 'tRPC procedure completed');
    
    return result;
  } catch (error) {
    log.error({
      path,
      type,
      duration: Date.now() - start,
      error,
    }, 'tRPC procedure failed');
    
    throw error;
  }
});

// Apply to all procedures
export const loggedProcedure = publicProcedure.use(loggerMiddleware);
```

---

## Error Logging

### With Stack Traces

```typescript
try {
  await riskyOperation();
} catch (error) {
  // Pino serializes Error objects automatically
  logger.error({ err: error }, 'Operation failed');
}
```

### Custom Error Serializer

```typescript
const logger = pino({
  serializers: {
    err: pino.stdSerializers.err,  // Default error serializer
    error: (error) => ({
      type: error.constructor.name,
      message: error.message,
      stack: error.stack,
      code: error.code,
      // Add custom fields
      ...(error.details && { details: error.details }),
    }),
  },
});
```

---

## Sensitive Data Redaction

### Configuration

```typescript
const logger = pino({
  redact: {
    paths: [
      'password',
      'secret',
      'token',
      'apiKey',
      'authorization',
      'cookie',
      'creditCard',
      '*.password',           // Nested fields
      '*.secret',
      'req.headers.cookie',
      'req.headers.authorization',
      'user.email',           // PII
    ],
    censor: '[REDACTED]',
    remove: false,            // Keep key, redact value
  },
});
```

### Output

```json
{
  "user": {
    "id": "123",
    "email": "[REDACTED]",
    "password": "[REDACTED]"
  }
}
```

---

## Production Configuration

```typescript
// src/lib/logger.ts
import pino from 'pino';

const isProduction = process.env.NODE_ENV === 'production';

export const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  
  // No transport in production (JSON to stdout)
  transport: isProduction ? undefined : {
    target: 'pino-pretty',
  },
  
  // Faster serialization in production
  formatters: {
    level: (label) => ({ level: label }),
  },
  
  // ISO timestamp
  timestamp: pino.stdTimeFunctions.isoTime,
  
  // Redaction
  redact: ['password', 'token', '*.password'],
  
  // Base context
  base: {
    service: process.env.SERVICE_NAME,
    version: process.env.APP_VERSION,
    env: process.env.NODE_ENV,
  },
});
```

---

## Rules

### Do ✅

- Use structured objects, not string interpolation
- Create child loggers for request context
- Redact sensitive data (passwords, tokens, PII)
- Include correlation IDs for tracing
- Use appropriate log levels
- Log errors with `{ err: error }`

### Avoid ❌

- `console.log()` in production code
- Logging sensitive data (passwords, tokens)
- String interpolation for structured data
- Excessive debug logging in production
- Blocking I/O in log transports

---

## Log Level Guidelines

| Level | Use Case | Production |
|-------|----------|------------|
| `trace` | Very detailed debugging | Off |
| `debug` | Development debugging | Off |
| `info` | Normal operations | On |
| `warn` | Potential issues | On |
| `error` | Errors (handled) | On |
| `fatal` | App crashing | On |

---

## Troubleshooting

```yaml
"Logs not appearing":
  → Check LOG_LEVEL environment variable
  → Verify level: logger.level returns current level
  → Debug level is often disabled in production

"pino-pretty not working":
  → Only use in development
  → Check transport configuration
  → npm install pino-pretty

"Sensitive data in logs":
  → Add paths to redact array
  → Use wildcards: '*.password'
  → Verify with test logs

"Performance issues":
  → Remove pino-pretty in production
  → Reduce log level
  → Check for sync logging (avoid)
```

---

## Integration with Observability

### Datadog

```typescript
// Datadog expects JSON logs to stdout
const logger = pino({
  formatters: {
    level: (label) => ({ level: label }),
  },
  // Datadog trace correlation
  mixin: () => ({
    dd: {
      trace_id: getCurrentTraceId(),
      span_id: getCurrentSpanId(),
    },
  }),
});
```

### ELK Stack

```typescript
// Elasticsearch-friendly format
const logger = pino({
  timestamp: pino.stdTimeFunctions.isoTime,
  formatters: {
    level: (label) => ({ level: label }),
  },
});
```

---

## File Structure

```
src/
├── lib/
│   └── logger.ts           # Logger configuration
├── middleware/
│   └── request-logger.ts   # Express middleware
└── server/
    └── middleware/
        └── logging.ts      # tRPC middleware
```

## References

- https://getpino.io — Official documentation
- https://github.com/pinojs/pino — GitHub
- https://github.com/pinojs/pino-pretty — Pretty printing
