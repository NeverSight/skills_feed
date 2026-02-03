---
name: error-handling
description: Comprehensive error handling patterns for robust applications including custom errors, error boundaries, recovery strategies, and user-facing error messages. Use this skill when designing error hierarchies, implementing React error boundaries, adding retry logic or fallbacks, creating API error responses, integrating error tracking (Sentry), or improving user error communication. Triggers on "error handling", "error boundary", "custom error", "retry logic", "graceful degradation", "error tracking", "Sentry", "user error message", "try-catch", "Result type", "circuit breaker".
---

# Error Handling

Design resilient applications through intentional error handling strategies.

## Error Handling Philosophy

```
┌─────────────────────────────────────────────────────────────────┐
│                    Error Handling Goals                         │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   Debuggable    │   Recoverable   │      User-Friendly          │
│ "What failed?"  │ "Can we retry?" │    "What should I do?"      │
├─────────────────┼─────────────────┼─────────────────────────────┤
│ Rich context    │ Retry logic     │ Clear, actionable messages  │
│ Stack traces    │ Fallbacks       │ Appropriate detail level    │
│ Correlation IDs │ Circuit breaker │ Recovery guidance           │
└─────────────────┴─────────────────┴─────────────────────────────┘
```

**Core principle:** Errors are data, not just exceptions. Design them intentionally.

## Quick Decision Guide

| Situation | Pattern | Reference |
|-----------|---------|-----------|
| Need typed error categories | Custom error classes | [error-patterns.md](references/error-patterns.md) |
| Want explicit error handling (no throws) | Result/Either type | [error-patterns.md](references/error-patterns.md) |
| React component might crash | Error boundary | [react-errors.md](references/react-errors.md) |
| API endpoint error response | Structured API errors | [api-errors.md](references/api-errors.md) |
| Network calls that might fail | Retry with backoff | [recovery-patterns.md](references/recovery-patterns.md) |
| Downstream service unreliable | Circuit breaker | [recovery-patterns.md](references/recovery-patterns.md) |
| Feature can work without dependency | Graceful degradation | [recovery-patterns.md](references/recovery-patterns.md) |

## Error Type Design

### Custom Error Classes

```typescript
// Base error with context
class AppError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly context?: Record<string, unknown>,
    public readonly cause?: Error
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }

  toJSON() {
    return {
      name: this.name,
      code: this.code,
      message: this.message,
      context: this.context,
    };
  }
}

// Domain-specific errors
class ValidationError extends AppError {
  constructor(message: string, public readonly field?: string) {
    super(message, 'VALIDATION_ERROR', { field });
  }
}

class NotFoundError extends AppError {
  constructor(resource: string, id: string) {
    super(`${resource} not found: ${id}`, 'NOT_FOUND', { resource, id });
  }
}

class AuthenticationError extends AppError {
  constructor(message = 'Authentication required') {
    super(message, 'AUTH_REQUIRED');
  }
}

class AuthorizationError extends AppError {
  constructor(action: string, resource: string) {
    super(`Not authorized to ${action} ${resource}`, 'FORBIDDEN', { action, resource });
  }
}
```

### Error Code Registry

```typescript
// Centralized error codes prevent collisions
const ErrorCodes = {
  // Auth: 1xxx
  AUTH_REQUIRED: 'E1001',
  AUTH_EXPIRED: 'E1002',
  AUTH_INVALID: 'E1003',
  
  // Validation: 2xxx
  VALIDATION_FAILED: 'E2001',
  VALIDATION_MISSING_FIELD: 'E2002',
  VALIDATION_INVALID_FORMAT: 'E2003',
  
  // Business Logic: 3xxx
  INSUFFICIENT_FUNDS: 'E3001',
  ITEM_OUT_OF_STOCK: 'E3002',
  
  // External Services: 4xxx
  SERVICE_UNAVAILABLE: 'E4001',
  RATE_LIMITED: 'E4002',
} as const;
```

## Result Pattern (No Throws)

For explicit error handling without exceptions:

```typescript
type Result<T, E = Error> = 
  | { ok: true; value: T }
  | { ok: false; error: E };

// Helper functions
const Ok = <T>(value: T): Result<T, never> => ({ ok: true, value });
const Err = <E>(error: E): Result<never, E> => ({ ok: false, error });

// Usage
async function parseUser(data: unknown): Result<User, ValidationError> {
  const parsed = userSchema.safeParse(data);
  if (!parsed.success) {
    return Err(new ValidationError(parsed.error.message));
  }
  return Ok(parsed.data);
}

// Consuming results
const result = await parseUser(input);
if (!result.ok) {
  logger.warn({ error: result.error, input });
  return res.status(400).json({ error: result.error.message });
}
const user = result.value; // Type-safe!
```

**When to use Result vs throws:**
- Result: Expected failures (validation, business rules), functional pipelines
- Throws: Unexpected failures (programmer errors, system failures)

## React Error Boundaries

### Basic Error Boundary

```tsx
class ErrorBoundary extends Component<Props, State> {
  state = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    // Log to error tracking
    Sentry.captureException(error, { extra: info });
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback ?? <DefaultErrorUI error={this.state.error} />;
    }
    return this.props.children;
  }
}
```

### Boundary Placement Strategy

```
App
├── ErrorBoundary (app-level: "Something went wrong")
│   └── Layout
│       ├── ErrorBoundary (route-level: show error page)
│       │   └── DashboardPage
│       │       ├── ErrorBoundary (widget-level: show widget error)
│       │       │   └── SalesChart
│       │       └── ErrorBoundary
│       │           └── RecentOrders
```

**Rules:**
- App-level: Catches catastrophic failures, shows generic error
- Route-level: Lets navigation continue, shows error page for route
- Component-level: Isolates failures, shows component-specific fallback

## API Error Responses

### Standard Error Response Shape

```typescript
interface APIError {
  error: {
    code: string;           // Machine-readable code
    message: string;        // Human-readable message
    details?: unknown;      // Additional context
    requestId?: string;     // Correlation ID for debugging
  };
}

// Example response
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": {
      "field": "email",
      "value": "not-an-email"
    },
    "requestId": "req_abc123"
  }
}
```

### HTTP Status Code Mapping

| Error Type | Status | When to Use |
|------------|--------|-------------|
| ValidationError | 400 | Invalid input from client |
| AuthenticationError | 401 | Missing or invalid auth |
| AuthorizationError | 403 | Valid auth, insufficient permissions |
| NotFoundError | 404 | Resource doesn't exist |
| ConflictError | 409 | State conflict (duplicate, version mismatch) |
| RateLimitError | 429 | Too many requests |
| InternalError | 500 | Unexpected server error |
| ServiceUnavailableError | 503 | Downstream service failure |

### Express Error Handler

```typescript
function errorHandler(err: Error, req: Request, res: Response, next: NextFunction) {
  const requestId = req.headers['x-request-id'] as string;

  if (err instanceof AppError) {
    // Known error — safe to expose
    return res.status(getStatusCode(err)).json({
      error: {
        code: err.code,
        message: err.message,
        details: err.context,
        requestId,
      },
    });
  }

  // Unknown error — don't leak details
  logger.error({ err, requestId }, 'Unhandled error');
  Sentry.captureException(err);
  
  res.status(500).json({
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred',
      requestId,
    },
  });
}
```

## Recovery Strategies

### Retry with Exponential Backoff

```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  options: {
    maxAttempts?: number;
    baseDelay?: number;
    maxDelay?: number;
    shouldRetry?: (error: Error) => boolean;
  } = {}
): Promise<T> {
  const {
    maxAttempts = 3,
    baseDelay = 1000,
    maxDelay = 30000,
    shouldRetry = (e) => e instanceof NetworkError || e instanceof TimeoutError,
  } = options;

  let lastError: Error;
  
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;
      
      if (attempt === maxAttempts || !shouldRetry(lastError)) {
        throw lastError;
      }
      
      const delay = Math.min(baseDelay * 2 ** (attempt - 1), maxDelay);
      const jitter = delay * 0.1 * Math.random();
      await sleep(delay + jitter);
    }
  }
  
  throw lastError!;
}
```

### Circuit Breaker Pattern

```typescript
class CircuitBreaker {
  private failures = 0;
  private lastFailure?: Date;
  private state: 'closed' | 'open' | 'half-open' = 'closed';

  constructor(
    private threshold: number = 5,
    private timeout: number = 60000
  ) {}

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === 'open') {
      if (Date.now() - this.lastFailure!.getTime() > this.timeout) {
        this.state = 'half-open';
      } else {
        throw new CircuitOpenError('Circuit breaker is open');
      }
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess() {
    this.failures = 0;
    this.state = 'closed';
  }

  private onFailure() {
    this.failures++;
    this.lastFailure = new Date();
    if (this.failures >= this.threshold) {
      this.state = 'open';
    }
  }
}
```

## User-Facing Error Messages

### Message Writing Principles

```
❌ "Error: ETIMEDOUT"
✅ "We're having trouble connecting. Please check your internet and try again."

❌ "Null pointer exception at line 42"  
✅ "Something went wrong. We've been notified and are working on it."

❌ "Validation failed"
✅ "Please enter a valid email address"
```

**Guidelines:**
1. **Be specific about the problem** (when safe to do so)
2. **Suggest what to do next** (retry, contact support, try different input)
3. **Never expose technical details** (stack traces, internal codes)
4. **Match the tone to severity** (casual for minor, serious for major)

### Error Message Templates

```typescript
const userMessages = {
  network: {
    offline: "You appear to be offline. Please check your connection.",
    timeout: "This is taking longer than expected. Please try again.",
    serverError: "We're experiencing technical difficulties. Please try again in a few minutes.",
  },
  validation: {
    required: (field: string) => `${field} is required`,
    invalid: (field: string) => `Please enter a valid ${field}`,
    tooLong: (field: string, max: number) => `${field} must be ${max} characters or less`,
  },
  auth: {
    expired: "Your session has expired. Please sign in again.",
    unauthorized: "You don't have permission to perform this action.",
  },
};
```

## Error Tracking Integration

### Sentry Setup

```typescript
import * as Sentry from '@sentry/node';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 0.1,
  beforeSend(event) {
    // Scrub sensitive data
    if (event.request?.data) {
      delete event.request.data.password;
    }
    return event;
  },
});

// Adding context
Sentry.setUser({ id: user.id, email: user.email });
Sentry.setTag('feature', 'checkout');
Sentry.setContext('order', { orderId, amount });
```

### What to Track

**Always track:**
- Unhandled exceptions
- Critical business logic failures
- External service failures

**Don't track:**
- Expected validation errors (unless aggregating)
- User cancellations
- Rate limit hits (use metrics instead)

## Anti-Patterns

### ❌ Swallowing Errors

```typescript
// BAD: Silent failure
try {
  await saveToDatabase(data);
} catch (e) {
  // nothing
}

// GOOD: Handle or propagate
try {
  await saveToDatabase(data);
} catch (e) {
  logger.error({ error: e, data }, 'Failed to save');
  throw new DatabaseError('Save failed', { cause: e });
}
```

### ❌ Generic Catch-All

```typescript
// BAD: Losing error type information
catch (e) {
  throw new Error('Something went wrong');
}

// GOOD: Preserve context
catch (e) {
  throw new AppError('Operation failed', 'OP_FAILED', { originalOp: 'createUser' }, e);
}
```

### ❌ Inconsistent Error Shapes

```typescript
// BAD: Different error shapes across API
{ "error": "Invalid email" }           // endpoint 1
{ "message": "Not found", "code": 404 } // endpoint 2
{ "errors": ["Bad request"] }          // endpoint 3

// GOOD: Consistent shape everywhere
{ "error": { "code": "...", "message": "...", "requestId": "..." } }
```

## Integration Points

**With observability:**
- Include correlation IDs in all errors
- Log errors with full context
- Create alerts for error rate thresholds

**With API design:**
- Use consistent error response shape
- Map error types to HTTP status codes
- Include request ID in responses

**With testing:**
- Test error paths explicitly
- Verify error boundary fallbacks
- Mock failures in integration tests

## Skill Usage

**Designing error hierarchy:**
1. Read [references/error-patterns.md](references/error-patterns.md)
2. Define base AppError with context support
3. Create domain-specific error classes
4. Establish error code registry

**Adding React error boundaries:**
1. Read [references/react-errors.md](references/react-errors.md)
2. Implement error boundary component
3. Add boundaries at appropriate levels
4. Create fallback UIs

**Implementing recovery strategies:**
1. Read [references/recovery-patterns.md](references/recovery-patterns.md)
2. Add retry logic for transient failures
3. Implement circuit breaker for unreliable services
4. Design graceful degradation paths

**Designing API error responses:**
1. Read [references/api-errors.md](references/api-errors.md)
2. Define consistent error response shape
3. Implement centralized error handler
4. Map error types to status codes

---

**References:**
- [references/error-patterns.md](references/error-patterns.md) — Custom errors, Result types, error hierarchies
- [references/react-errors.md](references/react-errors.md) — Error boundaries, Suspense, React error handling
- [references/api-errors.md](references/api-errors.md) — HTTP errors, response shapes, status codes
- [references/recovery-patterns.md](references/recovery-patterns.md) — Retry, circuit breaker, fallbacks, degradation
