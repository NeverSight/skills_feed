---
name: error-handling-patterns
description: "Master error handling patterns across languages including exceptions, Result types, error propagation, and graceful degradation to build resilient applications. Use when implementing error handling, designing APIs, or improving application reliability."
layer: 1
tech_stack: [dotnet, csharp, typescript]
topics: [exceptions, result-type, polly, retry, circuit-breaker, graceful-degradation]
depends_on: []
complements: [dotnet-async-patterns]
keywords: [Exception, Result, Polly, Retry, CircuitBreaker, try-catch, BusinessException]
---

# Error Handling Patterns

Build resilient applications with robust error handling strategies.

## Error Handling Philosophies

| Approach | Use When |
|----------|----------|
| Exceptions | Unexpected errors, exceptional conditions |
| Result Types | Expected errors, validation failures |
| Error Codes | C-style APIs, legacy integration |

## .NET Exception Patterns

### Custom Exception Hierarchy

```csharp
public class ApplicationException : Exception
{
    public string Code { get; }
    public ApplicationException(string message, string code) : base(message)
    {
        Code = code;
    }
}

public class ValidationException : ApplicationException
{
    public ValidationException(string message)
        : base(message, "VALIDATION_ERROR") { }
}

public class NotFoundException : ApplicationException
{
    public NotFoundException(string resource, Guid id)
        : base($"{resource} not found: {id}", "NOT_FOUND") { }
}
```

### ABP BusinessException

```csharp
// Use ABP's BusinessException for domain errors
throw new BusinessException(
    code: ClinicManagementSystemDomainErrorCodes.PatientNotFound,
    message: "Patient not found")
    .WithData("PatientId", patientId);
```

## Result Type Pattern

```typescript
type Result<T, E = Error> =
    | { ok: true; value: T }
    | { ok: false; error: E };

function Ok<T>(value: T): Result<T, never> {
    return { ok: true, value };
}

function Err<E>(error: E): Result<never, E> {
    return { ok: false, error };
}

// Usage
function parseJSON<T>(json: string): Result<T, SyntaxError> {
    try {
        return Ok(JSON.parse(json) as T);
    } catch (error) {
        return Err(error as SyntaxError);
    }
}
```

## .NET Resilience with Polly

### HTTP Retry with Exponential Backoff

```csharp
public IAsyncPolicy<HttpResponseMessage> BuildHttpRetryPolicy(int retryCount = 3)
{
    return HttpPolicyExtensions
        .HandleTransientHttpError()
        .Or<TimeoutException>()
        .WaitAndRetryAsync(
            retryCount: retryCount,
            sleepDurationProvider: retryAttempt =>
            {
                var exponentialDelay = TimeSpan.FromSeconds(Math.Pow(2, retryAttempt));
                var jitter = TimeSpan.FromMilliseconds(Random.Shared.Next(0, 1000));
                return exponentialDelay + jitter;
            },
            onRetryAsync: async (outcome, timespan, retryAttempt, context) =>
            {
                _logger.LogWarning(
                    "[Retry {Attempt}/{Total}] Waiting: {Delay:F2}s",
                    retryAttempt, retryCount, timespan.TotalSeconds);
            });
}
```

### Database Retry for Transient Errors

```csharp
public IAsyncPolicy BuildDatabaseRetryPolicy(int retryCount = 3)
{
    return Policy
        .Handle<DbUpdateConcurrencyException>()
        .Or<DbUpdateException>(ex =>
            ex.InnerException is NpgsqlException npgsqlEx &&
            IsTransientPostgresException(npgsqlEx))
        .WaitAndRetryAsync(
            retryCount: retryCount,
            sleepDurationProvider: retryAttempt =>
                TimeSpan.FromSeconds(Math.Pow(2, retryAttempt)));
}

private static bool IsTransientPostgresException(NpgsqlException ex)
{
    var transientCodes = new[] { "40001", "40P01", "55P03", "57014", "53300", "08000" };
    return transientCodes.Contains(ex.SqlState);
}
```

### Combined Policy (Retry + Circuit Breaker + Timeout)

```csharp
public IAsyncPolicy<HttpResponseMessage> BuildResilientPolicy()
{
    var timeout = Policy.TimeoutAsync<HttpResponseMessage>(TimeSpan.FromSeconds(30));

    var retry = HttpPolicyExtensions
        .HandleTransientHttpError()
        .WaitAndRetryAsync(3, attempt => TimeSpan.FromSeconds(Math.Pow(2, attempt)));

    var circuitBreaker = HttpPolicyExtensions
        .HandleTransientHttpError()
        .CircuitBreakerAsync(
            handledEventsAllowedBeforeBreaking: 5,
            durationOfBreak: TimeSpan.FromSeconds(30));

    return Policy.WrapAsync(timeout, retry, circuitBreaker);
}
```

### DI Registration

```csharp
services.AddHttpClient<IMyApiClient, MyApiClient>()
    .AddPolicyHandler((provider, _) =>
    {
        var retryService = provider.GetRequiredService<IRetryPolicyService>();
        return retryService.BuildHttpRetryPolicy();
    });
```

## Circuit Breaker Pattern

```
States:
  CLOSED  → Normal operation, tracking failures
  OPEN    → Failing, reject all requests
  HALF_OPEN → Testing recovery with limited requests

Flow:
  CLOSED --[failure threshold]--> OPEN
  OPEN --[timeout]--> HALF_OPEN
  HALF_OPEN --[success]--> CLOSED
  HALF_OPEN --[failure]--> OPEN
```

## Graceful Degradation

```csharp
// Polly Fallback Policy
public IAsyncPolicy<T> BuildFallbackPolicy<T>(Func<Task<T>> fallbackAction)
{
    return Policy<T>
        .Handle<Exception>()
        .FallbackAsync(
            fallbackAction: async (context, cancellationToken) =>
            {
                _logger.LogWarning("Primary operation failed, using fallback");
                return await fallbackAction();
            },
            onFallbackAsync: async (exception, context) =>
            {
                _logger.LogError(exception.Exception, "Fallback triggered");
            });
}

// Usage
var fallbackPolicy = BuildFallbackPolicy(() => FetchFromDatabaseAsync(userId));
var profile = await fallbackPolicy.ExecuteAsync(() => FetchFromCacheAsync(userId));
```

## When to Retry

✅ **Retry for:**
- HTTP API calls (transient network errors)
- Database operations (deadlocks, connection timeouts)
- External service integrations
- File I/O operations

❌ **Don't retry:**
- Authentication failures
- Validation errors
- Business logic errors
- Non-idempotent operations without safeguards

## Best Practices

1. **Fail Fast** - Validate input early
2. **Preserve Context** - Include stack traces, metadata
3. **Meaningful Messages** - Explain what and how to fix
4. **Log Appropriately** - Error = log, expected = don't spam
5. **Handle at Right Level** - Catch where you can meaningfully handle
6. **Clean Up Resources** - Use try-finally, using statements
7. **Don't Swallow Errors** - Log or re-throw, don't ignore
8. **Type-Safe Errors** - Use typed errors when possible

## Detailed References

For comprehensive patterns, see:
- [references/exception-hierarchy-design.md](references/exception-hierarchy-design.md)
- [references/polly-advanced-patterns.md](references/polly-advanced-patterns.md)
- [references/async-error-handling.md](references/async-error-handling.md)
