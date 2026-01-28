---
name: error-handling
description: Implement robust error handling in Node.js with custom error classes, async patterns, Express middleware, and production monitoring
version: "2.1.0"
sasmp_version: "1.3.0"
bonded_agent: 06-testing-debugging
bond_type: PRIMARY_BOND
---

# Node.js Error Handling Skill

Master error handling patterns for building resilient Node.js applications that fail gracefully and provide meaningful feedback.

## Quick Start

Error handling in 4 layers:
1. **Custom Error Classes** - Typed, informative errors
2. **Try/Catch Patterns** - Sync and async handling
3. **Express Middleware** - Centralized API errors
4. **Process Handlers** - Uncaught exceptions

## Core Concepts

### Custom Error Classes
```javascript
// Base application error
class AppError extends Error {
  constructor(message, statusCode, code) {
    super(message);
    this.statusCode = statusCode;
    this.code = code;
    this.isOperational = true;
    Error.captureStackTrace(this, this.constructor);
  }
}

// Specific error types
class ValidationError extends AppError {
  constructor(message, details = []) {
    super(message, 400, 'VALIDATION_ERROR');
    this.details = details;
  }
}

class NotFoundError extends AppError {
  constructor(resource = 'Resource') {
    super(`${resource} not found`, 404, 'NOT_FOUND');
  }
}

class UnauthorizedError extends AppError {
  constructor(message = 'Authentication required') {
    super(message, 401, 'UNAUTHORIZED');
  }
}

class ForbiddenError extends AppError {
  constructor(message = 'Access denied') {
    super(message, 403, 'FORBIDDEN');
  }
}
```

### Async Error Handling
```javascript
// Async wrapper for Express routes
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

// Usage
router.get('/users/:id', asyncHandler(async (req, res) => {
  const user = await User.findById(req.params.id);
  if (!user) throw new NotFoundError('User');
  res.json(user);
}));
```

### Express Error Middleware
```javascript
const errorHandler = (err, req, res, next) => {
  // Log error
  logger.error({
    message: err.message,
    stack: err.stack,
    code: err.code,
    url: req.originalUrl
  });

  // Handle operational errors
  if (err.isOperational) {
    return res.status(err.statusCode).json({
      success: false,
      error: {
        message: err.message,
        code: err.code,
        ...(err.details && { details: err.details })
      }
    });
  }

  // Production: hide internal errors
  if (process.env.NODE_ENV === 'production') {
    return res.status(500).json({
      success: false,
      error: { message: 'Internal server error', code: 'INTERNAL_ERROR' }
    });
  }

  // Development: show stack
  res.status(500).json({
    success: false,
    error: { message: err.message, stack: err.stack }
  });
};
```

## Learning Path

### Beginner (1-2 weeks)
- ✅ Understand Error types
- ✅ Try/catch for sync code
- ✅ Promise .catch() handling
- ✅ Basic Express error middleware

### Intermediate (3-4 weeks)
- ✅ Custom error classes
- ✅ Async error wrapper
- ✅ Centralized error handling
- ✅ Error logging with Winston

### Advanced (5-6 weeks)
- ✅ Production error monitoring
- ✅ Graceful shutdown
- ✅ Circuit breaker patterns
- ✅ Error recovery strategies

## Process-Level Error Handling
```javascript
// Uncaught exceptions
process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error);
  logger.fatal({ error }, 'Uncaught exception');
  process.exit(1);
});

// Unhandled promise rejections
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection:', reason);
  logger.error({ reason }, 'Unhandled rejection');
});

// Graceful shutdown
process.on('SIGTERM', async () => {
  console.log('SIGTERM received. Graceful shutdown...');
  server.close(() => console.log('HTTP server closed'));
  await mongoose.connection.close();
  process.exit(0);
});
```

## Retry with Exponential Backoff
```javascript
async function retryOperation(fn, options = {}) {
  const { maxRetries = 3, delay = 1000, backoff = 2 } = options;
  let lastError;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      if (attempt === maxRetries) throw error;

      const waitTime = delay * Math.pow(backoff, attempt - 1);
      await new Promise(resolve => setTimeout(resolve, waitTime));
    }
  }
  throw lastError;
}
```

## Error Response Format
```javascript
// Success
{ "success": true, "data": { ... } }

// Error
{
  "success": false,
  "error": {
    "message": "User not found",
    "code": "NOT_FOUND",
    "details": [],
    "timestamp": "2024-01-15T10:30:00.000Z"
  }
}
```

## Unit Test Template
```javascript
describe('Error Handling', () => {
  describe('ValidationError', () => {
    it('should create error with correct properties', () => {
      const error = new ValidationError('Invalid input', [
        { field: 'email', message: 'Required' }
      ]);

      expect(error.statusCode).toBe(400);
      expect(error.code).toBe('VALIDATION_ERROR');
      expect(error.isOperational).toBe(true);
    });
  });

  describe('asyncHandler', () => {
    it('should catch async errors', async () => {
      const mockNext = jest.fn();
      const handler = asyncHandler(async () => {
        throw new Error('Test error');
      });

      await handler({}, {}, mockNext);
      expect(mockNext).toHaveBeenCalledWith(expect.any(Error));
    });
  });
});
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Unhandled rejection warnings | Missing .catch() | Add process handler + local catches |
| Error swallowed silently | Empty catch block | Log or rethrow errors |
| Stack trace missing | Error.captureStackTrace not called | Use AppError base class |
| Memory leak from errors | Storing error references | Use WeakMap or clean up |

## When to Use

Use proper error handling when:
- Building production Node.js applications
- Creating REST APIs with Express
- Handling database operations
- Processing external API calls
- Implementing retry logic

## Related Skills

- Express REST API (API error responses)
- Async Programming (promise rejections)
- Testing & Debugging (error testing)

## Resources

- [Node.js Error Handling](https://nodejs.org/en/docs/guides/error-handling/)
- [Express Error Handling](https://expressjs.com/en/guide/error-handling.html)
- [Sentry for Node.js](https://docs.sentry.io/platforms/node/)
