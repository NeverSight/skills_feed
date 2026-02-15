---
name: error-handling-skills
description: Universal error handling, exception management, and logging best practices for all development agents across JavaScript/TypeScript, Python, Rust, Go, and Java. Use when implementing error handling, exception management, logging, error recovery, or debugging production issues.
license: MIT
---

# Error Handling Skills

## Overview

This skill provides comprehensive error handling, exception management, and logging best practices applicable to all development work. It covers language-agnostic principles and language-specific implementations for JavaScript/TypeScript, Python, Rust, Go, and Java.

Use this skill when:
- Implementing error handling in any application
- Designing exception hierarchies
- Setting up logging infrastructure
- Handling failures and implementing recovery patterns
- Securing error messages and stack traces
- Testing error conditions
- Debugging production issues

## Core Error Handling Philosophy

### 1. Fail Fast vs Graceful Degradation

**Fail Fast** - Immediately stop execution when an error occurs:
- Use for: Critical errors, data corruption, security violations
- Benefits: Prevents cascading failures, maintains data integrity
- Example: Database connection failure, authentication breach, invalid configuration

**Graceful Degradation** - Continue operation with reduced functionality:
- Use for: Non-critical features, external service failures, optional enhancements
- Benefits: Better user experience, higher availability
- Example: Analytics service down, search feature unavailable, image optimization failed

**Decision Matrix**:
```
Critical Path? → Yes → Fail Fast
              → No → Can provide fallback? → Yes → Graceful Degradation
                                          → No → Fail Fast with clear message
```

### 2. Catch vs Propagate Errors

**When to Catch (Handle Locally)**:
- Can meaningfully recover from the error
- Can provide a useful fallback value
- Can add context before re-throwing
- At API/system boundaries (convert internal errors to user-facing)
- In retry/circuit breaker logic

**When to Propagate (Let It Bubble)**:
- Cannot recover or provide meaningful fallback
- Error handling belongs to caller's responsibility
- Preserving original error context is critical
- In library code (let application decide handling)

**Anti-Pattern**: Catching and ignoring errors
```javascript
// ❌ NEVER DO THIS
try {
  await criticalOperation();
} catch (err) {
  // Silent failure - error is lost
}
```

### 3. Error Severity Levels

**CRITICAL** - System failure, immediate attention required:
- Database down, service unreachable, security breach
- Action: Alert on-call, page immediately, log to incident tracking
- User message: "Service unavailable, we're working on it"

**ERROR** - Operation failed, manual intervention may be needed:
- API request failed, file write failed, validation failed
- Action: Log with full context, may trigger alerts if frequent
- User message: Specific actionable message (e.g., "Invalid email format")

**WARNING** - Unexpected but handled condition:
- Deprecated feature used, rate limit approaching, slow query
- Action: Log for monitoring, no immediate action
- User message: Usually none (internal only)

**INFO** - Normal operational events:
- Request started/completed, user logged in, cache hit
- Action: Log for audit/analytics
- User message: None

**DEBUG** - Detailed diagnostic information:
- Variable values, execution flow, intermediate states
- Action: Log only in development/staging
- User message: None

### 4. Error Context and Stack Traces

**Always Include**:
- Timestamp (ISO 8601 format)
- Error type/code
- User-facing message
- Request ID / Correlation ID
- User ID (if authenticated)
- Operation being performed
- Input parameters (sanitized)

**Include in Logs Only (Never Expose to Users)**:
- Full stack trace
- Internal system details
- File paths and line numbers
- Database connection strings
- Environment variables

**Example Error Context**:
```json
{
  "timestamp": "2025-11-14T10:30:45.123Z",
  "level": "ERROR",
  "error_type": "DatabaseConnectionError",
  "message": "Failed to connect to database",
  "request_id": "req_abc123",
  "user_id": "user_789",
  "operation": "create_order",
  "details": {
    "retry_count": 3,
    "last_error": "Connection timeout after 5000ms"
  },
  "stack_trace": "..."  // Internal only
}
```

## Error Handling Patterns by Language

This section provides quick-reference patterns. For detailed implementations and examples, see the language-specific reference files:
- `references/javascript-patterns.md` - JavaScript/TypeScript detailed patterns
- `references/python-patterns.md` - Python detailed patterns
- `references/rust-patterns.md` - Rust detailed patterns
- `references/go-patterns.md` - Go detailed patterns
- `references/java-patterns.md` - Java detailed patterns

### JavaScript/TypeScript Quick Reference

**Synchronous Errors**:
```typescript
try {
  const result = riskyOperation();
  return result;
} catch (error) {
  if (error instanceof ValidationError) {
    return handleValidationError(error);
  }
  throw error; // Propagate unknown errors
} finally {
  cleanup(); // Always runs
}
```

**Async/Await Errors**:
```typescript
try {
  const data = await fetchData();
  return processData(data);
} catch (error) {
  logger.error('Data fetch failed', { error, requestId });
  throw new ServiceError('Unable to fetch data', { cause: error });
}
```

**Promise Rejection**:
```typescript
fetchData()
  .then(processData)
  .catch(error => {
    logger.error('Pipeline failed', { error });
    return fallbackData; // Graceful degradation
  });
```

See `references/javascript-patterns.md` for custom error classes, async error boundaries, and Express/Nest.js patterns.

### Python Quick Reference

**Try-Except-Finally**:
```python
try:
    result = risky_operation()
    return result
except ValueError as e:
    logger.error(f"Validation failed: {e}", exc_info=True)
    raise ValidationError(f"Invalid input: {e}") from e
except Exception as e:
    logger.critical(f"Unexpected error: {e}", exc_info=True)
    raise
finally:
    cleanup()  # Always runs
```

**Context Managers**:
```python
with open('file.txt') as f:
    data = f.read()  # File automatically closed even if error occurs
```

**Custom Exceptions**:
```python
class ApplicationError(Exception):
    """Base exception for application errors"""
    pass

class DatabaseError(ApplicationError):
    """Database operation failed"""
    pass
```

See `references/python-patterns.md` for exception chaining, decorators, and FastAPI/Django patterns.

### Rust Quick Reference

**Result<T, E>**:
```rust
fn read_file(path: &str) -> Result<String, std::io::Error> {
    std::fs::read_to_string(path)
}

// Using ?operator to propagate
fn process() -> Result<(), Box<dyn std::error::Error>> {
    let content = read_file("config.toml")?;
    Ok(())
}
```

**Option<T>**:
```rust
fn find_user(id: u32) -> Option<User> {
    database.get(id)
}

// Using unwrap_or for fallback
let user = find_user(123).unwrap_or_default();
```

**Custom Errors with thiserror**:
```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),

    #[error("Validation failed: {0}")]
    Validation(String),
}
```

See `references/rust-patterns.md` for panic vs Result, error conversion, and anyhow patterns.

### Go Quick Reference

**Error Interface**:
```go
func readFile(path string) ([]byte, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("failed to read %s: %w", path, err)
    }
    return data, nil
}
```

**Error Wrapping**:
```go
import "github.com/pkg/errors"

if err != nil {
    return errors.Wrap(err, "additional context")
}
```

**Defer for Cleanup**:
```go
func process() error {
    f, err := os.Open("file.txt")
    if err != nil {
        return err
    }
    defer f.Close() // Runs when function exits

    // Process file...
    return nil
}
```

See `references/go-patterns.md` for custom error types, sentinel errors, and panic recovery.

### Java Quick Reference

**Try-Catch-Finally**:
```java
try {
    Result result = riskyOperation();
    return result;
} catch (ValidationException e) {
    logger.error("Validation failed", e);
    throw new ServiceException("Invalid input", e);
} catch (Exception e) {
    logger.error("Unexpected error", e);
    throw e;
} finally {
    cleanup(); // Always runs
}
```

**Try-with-Resources**:
```java
try (BufferedReader reader = new BufferedReader(new FileReader("file.txt"))) {
    return reader.readLine();
} catch (IOException e) {
    logger.error("File read failed", e);
    throw new ApplicationException("Unable to read file", e);
}
// Resource automatically closed
```

**Custom Exceptions**:
```java
public class ApplicationException extends Exception {
    public ApplicationException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

See `references/java-patterns.md` for checked vs unchecked exceptions, exception hierarchies, and Spring Boot patterns.

## Logging Best Practices

For comprehensive logging guidance, see `references/logging-best-practices.md`.

### Log Levels Usage

**CRITICAL**: System-wide failure requiring immediate attention
```
Database connection pool exhausted
Authentication service unreachable
Configuration file corrupted
```

**ERROR**: Operation failed but system continues
```
API request failed after retries
File upload failed validation
Payment processing declined
```

**WARNING**: Unexpected condition that was handled
```
Using deprecated API endpoint
Rate limit at 80% capacity
Slow database query (>1s)
```

**INFO**: Normal operational events
```
User logged in successfully
Order created: order_id=12345
Cache invalidated for key=users
```

**DEBUG**: Detailed diagnostic information
```
Query executed: SELECT * FROM users WHERE id=?
Variable state: cart_items=[...]
Function called: processPayment(amount=100.00)
```

### Structured Logging Format

Use JSON format for production logs:
```json
{
  "timestamp": "2025-11-14T10:30:45.123Z",
  "level": "ERROR",
  "service": "order-service",
  "environment": "production",
  "request_id": "req_abc123",
  "user_id": "user_789",
  "operation": "create_order",
  "message": "Payment processing failed",
  "error_type": "PaymentDeclinedError",
  "error_code": "insufficient_funds",
  "duration_ms": 1250,
  "stack_trace": "...",
  "metadata": {
    "amount": 99.99,
    "currency": "USD",
    "payment_method": "card"
  }
}
```

### What to Log

**ALWAYS Log**:
- Request start/completion with duration
- Authentication events (login, logout, failures)
- Authorization failures (access denied)
- Data mutations (create, update, delete)
- External service calls with response times
- Error conditions with full context

**NEVER Log**:
- Passwords or password hashes
- API keys, tokens, secrets
- Credit card numbers or CVV codes
- Social security numbers
- Private encryption keys
- Session IDs or JWTs
- Personal health information (PHI)
- Any personally identifiable information (PII) unless required by compliance

### Sanitization Pattern

```typescript
function sanitizeForLogging(data: any): any {
  const sensitive = ['password', 'token', 'apiKey', 'secret', 'ssn', 'cvv'];
  const sanitized = { ...data };

  for (const key of Object.keys(sanitized)) {
    if (sensitive.some(s => key.toLowerCase().includes(s))) {
      sanitized[key] = '[REDACTED]';
    }
  }

  return sanitized;
}

logger.info('User created', sanitizeForLogging(userData));
```

## Security Considerations

For detailed security guidance, see `references/security-checklist.md`.

### Critical Security Rules

**1. Never Expose Internal Errors to Users**:
```typescript
// ❌ BAD - Exposes internal details
catch (error) {
  res.status(500).json({
    error: error.message,  // Might contain sensitive paths
    stack: error.stack     // Reveals code structure
  });
}

// ✅ GOOD - Generic user message, detailed internal logging
catch (error) {
  logger.error('Database query failed', { error, query, userId });
  res.status(500).json({
    error: 'An unexpected error occurred. Please try again later.',
    errorId: requestId  // User can reference this with support
  });
}
```

**2. Sanitize Error Messages**:
```typescript
function sanitizeErrorMessage(error: Error): string {
  // Remove file paths
  let message = error.message.replace(/\/[\w\/]+\.[\w]+/g, '[FILE]');

  // Remove SQL queries
  message = message.replace(/SELECT .+ FROM/gi, '[QUERY]');

  // Remove IP addresses
  message = message.replace(/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/g, '[IP]');

  return message;
}
```

**3. Rate Limit Error Responses**:
```typescript
// Prevent attackers from probing for vulnerabilities
const errorRateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 error responses per window
  message: 'Too many errors from this IP'
});

app.use('/api/', errorRateLimiter);
```

**4. Different Messages for Different Audiences**:
```typescript
class ApplicationError extends Error {
  constructor(
    public userMessage: string,      // Safe for users
    public internalMessage: string,  // Detailed for logs
    public code: string
  ) {
    super(internalMessage);
  }
}

// Usage
throw new ApplicationError(
  'Invalid credentials',              // User sees this
  'Password hash mismatch for user_id=123',  // Logs show this
  'AUTH_FAILED'
);
```

## Error Recovery Patterns

### 1. Retry with Exponential Backoff

Use for transient failures (network issues, temporary service unavailability):

```typescript
async function retryWithBackoff<T>(
  operation: () => Promise<T>,
  maxRetries: number = 3,
  baseDelay: number = 1000
): Promise<T> {
  let lastError: Error;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await operation();
    } catch (error) {
      lastError = error as Error;

      if (attempt < maxRetries - 1) {
        const delay = baseDelay * Math.pow(2, attempt);
        logger.warn(`Retry attempt ${attempt + 1}/${maxRetries} after ${delay}ms`, { error });
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }

  throw new Error(`Operation failed after ${maxRetries} retries: ${lastError.message}`);
}

// Usage
const data = await retryWithBackoff(() => fetchFromAPI('/users'));
```

### 2. Circuit Breaker Pattern

Prevent cascading failures by stopping requests to failing services:

```typescript
class CircuitBreaker {
  private failureCount = 0;
  private lastFailureTime?: number;
  private state: 'CLOSED' | 'OPEN' | 'HALF_OPEN' = 'CLOSED';

  constructor(
    private threshold: number = 5,
    private timeout: number = 60000  // 1 minute
  ) {}

  async execute<T>(operation: () => Promise<T>): Promise<T> {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailureTime! > this.timeout) {
        this.state = 'HALF_OPEN';
      } else {
        throw new Error('Circuit breaker is OPEN');
      }
    }

    try {
      const result = await operation();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess() {
    this.failureCount = 0;
    this.state = 'CLOSED';
  }

  private onFailure() {
    this.failureCount++;
    this.lastFailureTime = Date.now();

    if (this.failureCount >= this.threshold) {
      this.state = 'OPEN';
      logger.error('Circuit breaker opened', { failureCount: this.failureCount });
    }
  }
}

// Usage
const breaker = new CircuitBreaker();
const data = await breaker.execute(() => fetchFromAPI('/users'));
```

### 3. Fallback Values

Provide default values when operations fail:

```typescript
async function getUserPreferences(userId: string): Promise<Preferences> {
  try {
    return await fetchPreferences(userId);
  } catch (error) {
    logger.warn('Failed to fetch preferences, using defaults', { userId, error });
    return DEFAULT_PREFERENCES;
  }
}
```

### 4. Transaction Rollback

Ensure data consistency by rolling back on errors:

```typescript
async function transferFunds(fromAccount: string, toAccount: string, amount: number) {
  const transaction = await db.beginTransaction();

  try {
    await db.debit(fromAccount, amount, { transaction });
    await db.credit(toAccount, amount, { transaction });
    await transaction.commit();
    logger.info('Transfer completed', { fromAccount, toAccount, amount });
  } catch (error) {
    await transaction.rollback();
    logger.error('Transfer failed, rolled back', { fromAccount, toAccount, amount, error });
    throw new TransferError('Transfer failed', { cause: error });
  }
}
```

## Custom Error Classes

### When to Create Custom Errors

Create custom error classes when:
- Errors need to be caught and handled differently
- Errors need additional context or metadata
- Building error hierarchies for different error categories
- Providing domain-specific errors (e.g., `OrderNotFoundError`, `PaymentDeclinedError`)

### Error Hierarchy Pattern

```typescript
// Base application error
class ApplicationError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500,
    public isOperational: boolean = true
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
}

// Domain-specific errors
class ValidationError extends ApplicationError {
  constructor(message: string, public fields: Record<string, string>) {
    super(message, 'VALIDATION_ERROR', 400);
  }
}

class NotFoundError extends ApplicationError {
  constructor(resource: string, id: string) {
    super(`${resource} not found: ${id}`, 'NOT_FOUND', 404);
  }
}

class UnauthorizedError extends ApplicationError {
  constructor(message: string = 'Unauthorized') {
    super(message, 'UNAUTHORIZED', 401);
  }
}

// Usage
if (!user) {
  throw new NotFoundError('User', userId);
}

if (!isValid(data)) {
  throw new ValidationError('Invalid input', {
    email: 'Invalid format',
    age: 'Must be at least 18'
  });
}
```

### Error Codes vs Error Types

**Error Types** (Class-based):
- Use for programmatic error handling (catch specific errors)
- Provides inheritance hierarchy
- Better for typed languages

**Error Codes** (String-based):
- Use for client-facing APIs
- Easier to document and version
- Language-agnostic

**Best Practice**: Use both
```typescript
class PaymentError extends ApplicationError {
  constructor(code: string, message: string) {
    super(message, code, 402);
  }
}

// Error codes enumeration
enum PaymentErrorCode {
  INSUFFICIENT_FUNDS = 'INSUFFICIENT_FUNDS',
  INVALID_CARD = 'INVALID_CARD',
  EXPIRED_CARD = 'EXPIRED_CARD',
  DECLINED = 'DECLINED'
}

throw new PaymentError(PaymentErrorCode.INSUFFICIENT_FUNDS, 'Insufficient funds');
```

## Testing Error Paths

For comprehensive testing guidance, see testing-methodology-skills and `references/testing-patterns.md`.

### Testing Error Conditions

**Unit Tests**:
```typescript
describe('UserService', () => {
  it('should throw NotFoundError when user does not exist', async () => {
    mockDb.findUser.mockResolvedValue(null);

    await expect(userService.getUser('invalid-id'))
      .rejects
      .toThrow(NotFoundError);
  });

  it('should log error when database fails', async () => {
    mockDb.findUser.mockRejectedValue(new Error('Connection failed'));

    await expect(userService.getUser('user-123')).rejects.toThrow();
    expect(mockLogger.error).toHaveBeenCalledWith(
      expect.stringContaining('Failed to fetch user'),
      expect.objectContaining({ userId: 'user-123' })
    );
  });
});
```

**Mocking Errors**:
```typescript
// Mock external service failure
jest.spyOn(externalApi, 'fetchData').mockRejectedValue(
  new Error('Service unavailable')
);

// Mock network timeout
jest.spyOn(httpClient, 'get').mockImplementation(() =>
  new Promise((_, reject) =>
    setTimeout(() => reject(new Error('Timeout')), 100)
  )
);
```

### Error Coverage Checklist

Ensure tests cover:
- ✅ Happy path (no errors)
- ✅ Validation errors (invalid input)
- ✅ Not found errors (missing resources)
- ✅ Authentication/authorization errors
- ✅ Network errors (timeout, connection refused)
- ✅ External service failures
- ✅ Database errors (connection, constraint violations)
- ✅ Concurrent access errors (race conditions)
- ✅ Rate limiting errors
- ✅ Retry logic and exponential backoff
- ✅ Circuit breaker state transitions
- ✅ Transaction rollback on failure
- ✅ Cleanup in finally/defer blocks

## Common Error Handling Scenarios

### Database Connection Error

```typescript
class DatabaseError extends ApplicationError {
  constructor(operation: string, cause: Error) {
    super(
      `Database operation failed: ${operation}`,
      'DATABASE_ERROR',
      503
    );
    this.cause = cause;
  }
}

async function queryDatabase<T>(query: string, params: any[]): Promise<T[]> {
  try {
    return await db.query(query, params);
  } catch (error) {
    logger.error('Database query failed', {
      query,
      params: sanitizeForLogging(params),
      error
    });

    if (error.code === 'ECONNREFUSED') {
      throw new DatabaseError('Connection refused', error);
    }

    if (error.code === '23505') { // Unique constraint violation
      throw new ValidationError('Duplicate entry', { field: 'email' });
    }

    throw new DatabaseError(query, error);
  }
}
```

### API Request Error

```typescript
async function fetchFromAPI<T>(endpoint: string): Promise<T> {
  try {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      headers: { 'Authorization': `Bearer ${getToken()}` },
      timeout: 5000
    });

    if (!response.ok) {
      if (response.status === 401) {
        throw new UnauthorizedError('API authentication failed');
      }
      if (response.status === 404) {
        throw new NotFoundError('API Resource', endpoint);
      }
      if (response.status >= 500) {
        throw new ApplicationError(
          'API server error',
          'API_ERROR',
          response.status
        );
      }
      throw new ApplicationError(
        'API request failed',
        'API_ERROR',
        response.status
      );
    }

    return await response.json();
  } catch (error) {
    if (error instanceof ApplicationError) {
      throw error;
    }

    // Network errors
    logger.error('API request failed', { endpoint, error });
    throw new ApplicationError(
      'Unable to connect to API',
      'NETWORK_ERROR',
      503
    );
  }
}
```

### File I/O Error

```typescript
async function readConfigFile(path: string): Promise<Config> {
  try {
    const content = await fs.readFile(path, 'utf-8');
    return JSON.parse(content);
  } catch (error) {
    if (error.code === 'ENOENT') {
      logger.warn('Config file not found, using defaults', { path });
      return DEFAULT_CONFIG;
    }

    if (error instanceof SyntaxError) {
      logger.error('Invalid JSON in config file', { path, error });
      throw new ValidationError('Config file is not valid JSON', { path });
    }

    logger.error('Failed to read config file', { path, error });
    throw new ApplicationError('Unable to read configuration', 'CONFIG_ERROR');
  }
}
```

### Authentication Error

```typescript
async function authenticateUser(email: string, password: string): Promise<User> {
  try {
    const user = await db.findUserByEmail(email);

    if (!user) {
      // Don't reveal whether email exists
      logger.warn('Login attempt for non-existent user', { email });
      throw new UnauthorizedError('Invalid credentials');
    }

    const isValid = await bcrypt.compare(password, user.passwordHash);

    if (!isValid) {
      logger.warn('Invalid password attempt', { userId: user.id, email });
      await incrementFailedLoginAttempts(user.id);
      throw new UnauthorizedError('Invalid credentials');
    }

    if (user.isLocked) {
      logger.warn('Login attempt for locked account', { userId: user.id });
      throw new UnauthorizedError('Account is locked');
    }

    logger.info('User authenticated successfully', { userId: user.id });
    return user;
  } catch (error) {
    if (error instanceof UnauthorizedError) {
      throw error;
    }

    logger.error('Authentication error', { email, error });
    throw new ApplicationError('Authentication failed', 'AUTH_ERROR');
  }
}
```

### Validation Error

```typescript
interface ValidationResult {
  isValid: boolean;
  errors: Record<string, string>;
}

function validateUserInput(data: any): ValidationResult {
  const errors: Record<string, string> = {};

  if (!data.email || !isValidEmail(data.email)) {
    errors.email = 'Valid email is required';
  }

  if (!data.password || data.password.length < 8) {
    errors.password = 'Password must be at least 8 characters';
  }

  if (!data.age || data.age < 18) {
    errors.age = 'Must be at least 18 years old';
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
}

async function createUser(data: any): Promise<User> {
  const validation = validateUserInput(data);

  if (!validation.isValid) {
    logger.warn('User validation failed', { errors: validation.errors });
    throw new ValidationError('Invalid user data', validation.errors);
  }

  try {
    return await db.createUser(data);
  } catch (error) {
    logger.error('Failed to create user', { data: sanitizeForLogging(data), error });
    throw new DatabaseError('create user', error);
  }
}
```

## References

This skill includes detailed reference documentation:

- **references/javascript-patterns.md** - JavaScript/TypeScript error handling patterns, async error boundaries, Express/Nest.js integration
- **references/python-patterns.md** - Python exception patterns, decorators, context managers, FastAPI/Django integration
- **references/rust-patterns.md** - Rust Result/Option patterns, thiserror/anyhow usage, panic handling
- **references/go-patterns.md** - Go error interface patterns, error wrapping, panic/recover
- **references/java-patterns.md** - Java exception hierarchy, checked vs unchecked, Spring Boot integration
- **references/security-checklist.md** - Comprehensive security checklist for error handling
- **references/logging-best-practices.md** - Detailed logging patterns, structured logging, log aggregation

Load these references when working with specific languages or needing detailed implementation guidance.

## Quick Decision Tree

```
Error Occurred
├─ Can recover meaningfully?
│  ├─ Yes → Handle locally (try-catch)
│  │     └─ Log with context
│  │     └─ Return fallback or retry
│  └─ No → Propagate to caller
│        └─ Add context if helpful
│        └─ Let higher level decide
│
├─ User-facing error?
│  ├─ Yes → Generic message + error ID
│  │     └─ Log detailed error internally
│  └─ No → Detailed error message OK
│
├─ Transient failure?
│  ├─ Yes → Retry with backoff
│  └─ No → Fail immediately
│
└─ Critical system error?
   ├─ Yes → Fail fast + alert
   └─ No → Graceful degradation
```

## Summary

Error handling is not an afterthought—it's a critical part of building reliable, secure, and maintainable systems. Follow these principles:

1. **Be Intentional**: Decide whether to catch or propagate based on whether you can meaningfully recover
2. **Provide Context**: Always log errors with full context (request ID, user ID, operation, parameters)
3. **Secure by Default**: Never expose internal errors to users, sanitize all error messages
4. **Test Error Paths**: Error handling code is code—test it thoroughly
5. **Monitor and Alert**: Use structured logging and monitoring to catch issues before users do
6. **Fail Gracefully**: When possible, degrade gracefully rather than failing completely
7. **Learn from Errors**: Use error logs to identify patterns and improve system reliability

Use the language-specific reference files for detailed implementations and examples.
