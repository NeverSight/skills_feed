---
name: error-responses
description: Use when returning errors from APIs. Use when exposing internal errors. Use when error responses lack structure.
---

# Error Responses

## Overview

**Never expose internal errors. Return structured, safe error responses.**

Raw error messages leak implementation details, aid attackers, and confuse users. Errors should be safe, consistent, and actionable.

## When to Use

- Implementing error handling in APIs
- Returning error responses to clients
- Catching exceptions in controllers
- Asked to "just return the error message"

## The Iron Rule

```
NEVER expose raw error messages or stack traces to clients.
```

**No exceptions:**
- Not for "it helps debugging"
- Not for "internal API only"
- Not for "we're in development"
- Not for "the frontend needs details"

## Detection: Leak Smell

If errors expose internals, STOP:

```typescript
// ❌ VIOLATION: Exposing internals
app.get('/users/:id', async (req, res) => {
  try {
    const user = await db.query('SELECT * FROM users WHERE id = $1', [req.params.id]);
    res.json(user);
  } catch (error) {
    res.status(500).json({ message: error.message });  // Leaks!
  }
});
```

What could leak:
- `"relation \"users\" does not exist"` - Database schema
- `"connect ECONNREFUSED 10.0.1.5:5432"` - Internal IPs
- Stack traces with file paths
- SQL queries with table names

## The Correct Pattern: Safe Error Responses

```typescript
// ✅ CORRECT: Structured, safe errors

// Custom error classes
class AppError extends Error {
  constructor(
    public statusCode: number,
    public code: string,
    message: string
  ) {
    super(message);
  }
}

class NotFoundError extends AppError {
  constructor(resource: string) {
    super(404, 'NOT_FOUND', `${resource} not found`);
  }
}

class ValidationError extends AppError {
  constructor(public details: Record<string, string[]>) {
    super(400, 'VALIDATION_ERROR', 'Validation failed');
  }
}

// Error handler middleware
app.use((error: Error, req: Request, res: Response, next: NextFunction) => {
  // Log full error internally
  console.error('Error:', {
    message: error.message,
    stack: error.stack,
    path: req.path,
    method: req.method,
  });
  
  // Return safe response
  if (error instanceof ValidationError) {
    return res.status(400).json({
      error: {
        code: error.code,
        message: error.message,
        details: error.details,
      }
    });
  }
  
  if (error instanceof AppError) {
    return res.status(error.statusCode).json({
      error: {
        code: error.code,
        message: error.message,
      }
    });
  }
  
  // Unknown errors - never expose
  res.status(500).json({
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred',
    }
  });
});

// Usage in routes
app.get('/users/:id', async (req, res, next) => {
  try {
    const user = await userService.findById(req.params.id);
    if (!user) throw new NotFoundError('User');
    res.json(user);
  } catch (error) {
    next(error);  // Pass to error handler
  }
});
```

## Error Response Structure

Consistent structure for all errors:

```typescript
interface ErrorResponse {
  error: {
    code: string;        // Machine-readable: 'VALIDATION_ERROR'
    message: string;     // Human-readable: 'Validation failed'
    details?: unknown;   // Additional info (validation errors, etc.)
    requestId?: string;  // For support/debugging
  }
}

// Examples:
// 400 Bad Request
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": {
      "email": ["Invalid email format"],
      "age": ["Must be at least 18"]
    }
  }
}

// 404 Not Found
{
  "error": {
    "code": "NOT_FOUND",
    "message": "User not found"
  }
}

// 500 Internal Error
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An unexpected error occurred",
    "requestId": "req_abc123"
  }
}
```

## HTTP Status Codes

| Code | When to Use |
|------|-------------|
| 400 | Bad request, validation errors |
| 401 | Not authenticated |
| 403 | Authenticated but not authorized |
| 404 | Resource not found |
| 409 | Conflict (duplicate, state issue) |
| 422 | Unprocessable entity |
| 429 | Rate limited |
| 500 | Server error (hide details!) |
| 502 | Upstream service failed |
| 503 | Service unavailable |

## Pressure Resistance Protocol

### 1. "It Helps Debugging"
**Pressure:** "Developers need to see the full error"

**Response:** Log full errors server-side. Return request IDs for correlation.

**Action:** `{ requestId: "abc123" }` - developers can look up logs.

### 2. "Internal API Only"
**Pressure:** "Only our services call this"

**Response:** Internal services get compromised. Logs get leaked. Protect everything.

**Action:** Same safe error handling everywhere.

### 3. "Development Mode"
**Pressure:** "Show details in dev, hide in prod"

**Response:** Dev code becomes prod code. Habits matter.

**Action:** Same handling in all environments. Use logging for debugging.

## Red Flags - STOP and Reconsider

- `res.json({ message: error.message })`
- Stack traces in responses
- SQL queries in error messages
- Internal IPs or paths exposed
- Different error formats per endpoint

**All of these mean: Implement proper error handling.**

## Quick Reference

| Exposed (Bad) | Safe (Good) |
|---------------|-------------|
| Database error messages | "An error occurred" |
| Stack traces | Request ID for log lookup |
| Internal paths | Generic error code |
| SQL queries | "Validation failed" |
| Variable dumps | Structured error object |

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "Helps debugging" | Log server-side, return request ID. |
| "Internal API" | Internal gets compromised too. |
| "Development mode" | Same handling everywhere. |
| "Frontend needs details" | Return safe, structured details. |
| "It's faster" | Error handling is cheap. Breaches aren't. |

## The Bottom Line

**Log everything internally. Expose nothing externally.**

Return consistent, structured errors with machine-readable codes and human-readable messages. Never leak stack traces, queries, or internal details. Use request IDs for debugging.
