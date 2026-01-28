---
name: exception-hierarchies
description: Use when creating custom exceptions. Use when error handling feels chaotic. Use when catch blocks are too broad or too specific.
---

# Exception Hierarchies

## Overview

**Design exception hierarchies that enable precise catching and meaningful handling.**

Random exception classes lead to catch-all blocks or missed errors. A well-designed hierarchy lets callers catch at the right abstraction level.

## When to Use

- Creating custom exception classes
- Designing error handling strategy
- Refactoring scattered try/catch blocks
- Wrapping third-party library errors
- Debugging "unexpected error" catch-alls

## The Iron Rule

```
NEVER catch base Exception except at application boundaries.
```

**No exceptions:**
- Not for "I'll handle all cases"
- Not for "it's simpler"
- Not for "I don't know what to expect"
- Not for "the library throws too many types"

**Specific exceptions enable specific handling. Generic catches hide bugs.**

## The Three-Layer Hierarchy

Design exceptions in three layers:

```
                    ApplicationError (base)
                           │
          ┌────────────────┼────────────────┐
          │                │                │
    DomainError      InfrastructureError    ExternalError
          │                │                │
    ┌─────┴─────┐    ┌─────┴─────┐    ┌─────┴─────┐
    │           │    │           │    │           │
ValidationError  │  DatabaseError │   APIError   │
BusinessRuleError│  CacheError    │   TimeoutError│
NotFoundError    │  FileIOError   │   RateLimitError
```

### Layer 1: Root Exception

```typescript
// All application errors inherit from this
class ApplicationError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly context?: Record<string, unknown>
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
  
  toJSON() {
    return {
      name: this.name,
      message: this.message,
      code: this.code,
      context: this.context,
    };
  }
}
```

### Layer 2: Category Exceptions

```typescript
// Domain logic errors
class DomainError extends ApplicationError {
  constructor(message: string, code: string, context?: Record<string, unknown>) {
    super(message, `DOMAIN.${code}`, context);
  }
}

// Infrastructure failures
class InfrastructureError extends ApplicationError {
  constructor(message: string, code: string, context?: Record<string, unknown>) {
    super(message, `INFRA.${code}`, context);
  }
}

// External service failures
class ExternalError extends ApplicationError {
  constructor(
    message: string, 
    code: string, 
    public readonly service: string,
    context?: Record<string, unknown>
  ) {
    super(message, `EXTERNAL.${code}`, { ...context, service });
  }
}
```

### Layer 3: Specific Exceptions

```typescript
// Domain exceptions
class ValidationError extends DomainError {
  constructor(public readonly fields: Record<string, string>) {
    super('Validation failed', 'VALIDATION', { fields });
  }
}

class BusinessRuleError extends DomainError {
  constructor(rule: string, message: string) {
    super(message, 'BUSINESS_RULE', { rule });
  }
}

class NotFoundError extends DomainError {
  constructor(entity: string, id: string) {
    super(`${entity} not found: ${id}`, 'NOT_FOUND', { entity, id });
  }
}

// Infrastructure exceptions
class DatabaseError extends InfrastructureError {
  constructor(operation: string, cause?: Error) {
    super(`Database ${operation} failed`, 'DATABASE', { 
      operation, 
      cause: cause?.message 
    });
  }
}

// External service exceptions
class PaymentGatewayError extends ExternalError {
  constructor(message: string, public readonly gatewayCode: string) {
    super(message, 'PAYMENT', 'PaymentGateway', { gatewayCode });
  }
}
```

## Correct Catching Pattern

Catch at the right abstraction level:

```typescript
// ✅ CORRECT: Specific catching
async function createOrder(data: OrderData): Promise<Order> {
  try {
    return await orderService.create(data);
  } catch (error) {
    // Catch what you can handle specifically
    if (error instanceof ValidationError) {
      // Can show field-specific errors to user
      throw error; // Re-throw for controller to format response
    }
    if (error instanceof BusinessRuleError) {
      // Log business rule violation, maybe alert
      logger.warn('Business rule prevented order', { rule: error.context?.rule });
      throw error;
    }
    if (error instanceof PaymentGatewayError) {
      // Retry logic, fallback gateway, etc.
      return await retryWithFallbackGateway(data);
    }
    // Unknown error - don't swallow, let it propagate
    throw error;
  }
}

// ❌ WRONG: Catch-all that hides errors
async function createOrder(data: OrderData): Promise<Order | null> {
  try {
    return await orderService.create(data);
  } catch (error) {
    logger.error('Order failed', error);  // Lost specificity
    return null;  // Caller doesn't know why
  }
}
```

## Boundary Handling

Only catch broadly at application boundaries:

```typescript
// ✅ CORRECT: HTTP boundary translates to responses
app.use((error: Error, req: Request, res: Response, next: NextFunction) => {
  // This is the ONLY place catch-all is acceptable
  
  if (error instanceof ValidationError) {
    return res.status(400).json({
      error: 'Validation failed',
      fields: error.fields,
    });
  }
  
  if (error instanceof NotFoundError) {
    return res.status(404).json({
      error: error.message,
    });
  }
  
  if (error instanceof BusinessRuleError) {
    return res.status(422).json({
      error: error.message,
      code: error.code,
    });
  }
  
  if (error instanceof ExternalError) {
    // Log full context, return generic message
    logger.error('External service error', error.toJSON());
    return res.status(502).json({
      error: 'External service unavailable',
      retryAfter: 30,
    });
  }
  
  if (error instanceof InfrastructureError) {
    logger.error('Infrastructure error', error.toJSON());
    return res.status(503).json({
      error: 'Service temporarily unavailable',
    });
  }
  
  // Truly unexpected - log everything
  logger.error('Unhandled error', { 
    error: error.message,
    stack: error.stack,
    request: { method: req.method, path: req.path }
  });
  return res.status(500).json({
    error: 'Internal server error',
  });
});
```

## Wrapping Third-Party Errors

Never let raw library errors leak:

```typescript
// ✅ CORRECT: Wrap at the adapter boundary
class PostgresUserRepository implements UserRepository {
  async findById(id: string): Promise<User> {
    try {
      const result = await this.client.query(
        'SELECT * FROM users WHERE id = $1', 
        [id]
      );
      if (!result.rows[0]) {
        throw new NotFoundError('User', id);
      }
      return this.mapToUser(result.rows[0]);
    } catch (error) {
      if (error instanceof NotFoundError) throw error;
      
      // Wrap postgres-specific error
      if (error instanceof pg.DatabaseError) {
        throw new DatabaseError('query', error);
      }
      throw error;
    }
  }
}

// ❌ WRONG: Let pg.DatabaseError leak to controllers
// ❌ WRONG: Catch Error and throw generic Error
```

## Pressure Resistance Protocol

### 1. "Just Catch Exception, It's Simpler"
**Pressure:** "Don't overcomplicate with hierarchy"

**Response:** Catching `Exception` hides bugs and prevents specific handling. You'll debug for hours when a specific catch would have told you immediately.

**Action:** Create hierarchy. Catch specifically. Worth the upfront time.

### 2. "The Library Throws 10 Different Exceptions"
**Pressure:** "I can't anticipate all of them"

**Response:** Wrap at the boundary. Your code shouldn't know about library internals.

**Action:** Create adapter that catches library exceptions, throws your domain exceptions.

### 3. "I Don't Know What Errors to Expect"
**Pressure:** "Let me catch all and log"

**Response:** Logging isn't handling. If you don't know what to expect, let it propagate. The boundary handler will catch it.

**Action:** Don't catch what you can't handle specifically. Add catches as you learn.

### 4. "Error Codes Are Enough"
**Pressure:** "We use error codes, not exception types"

**Response:** Codes require string comparison, are easy to typo, and don't provide type safety.

**Action:** Exception types for control flow. Codes for serialization/logging.

## Red Flags - STOP and Reconsider

If you notice ANY of these, refactor:

- `catch (Exception e)` in non-boundary code
- `catch (Error e) { throw new Error(e.message) }` (losing type)
- Same exception type for different failure modes
- Library-specific exceptions in business logic
- No base exception for the application
- Catch blocks that log and continue
- `instanceof` checks for exception codes, not types

**All of these mean: Redesign the exception hierarchy.**

## Exception Design Checklist

| Requirement | Check |
|-------------|-------|
| All app errors inherit from base class | ☐ |
| Category exceptions for domain/infra/external | ☐ |
| Specific exceptions carry relevant context | ☐ |
| Third-party errors wrapped at boundary | ☐ |
| HTTP codes mapped in error middleware | ☐ |
| No raw `Exception` catches outside middleware | ☐ |
| Exceptions are immutable (readonly fields) | ☐ |
| `toJSON()` for structured logging | ☐ |

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "Hierarchy is over-engineering" | Hierarchy enables handling. Catch-all hides bugs. |
| "I'll just catch Exception" | You'll lose why it failed and how to handle it. |
| "Error codes work fine" | Types are compile-checked. Codes are strings. |
| "Library errors are fine to throw" | Library coupling spreads. Wrap at boundaries. |
| "I'll add types when I need them" | By then catch-all is everywhere. Start with types. |
| "Logging in catch is handling" | Logging isn't handling. Bubble or handle specifically. |

## Quick Reference

| Scenario | Action |
|----------|--------|
| New project | Create ApplicationError base + category classes |
| Using third-party library | Wrap in adapter, throw your exceptions |
| Don't know what to catch | Don't catch - let boundary handle it |
| Multiple failure modes | One exception class per mode |
| Catch block just logs | Remove catch, let it propagate |
| Need error details | Add context to exception constructor |

## The Bottom Line

**Design exception hierarchies that enable precise catching.**

Catch specifically what you can handle. Let everything else propagate to boundaries. Wrap third-party exceptions at adapters. Never catch base Exception in business logic.
