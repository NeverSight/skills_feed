---
name: dotnet
description: ASP.NET Core patterns, dependency injection, middleware, async/await, and security
---

## .NET Code Review Rules

### Security (Critical)
- Use `[Authorize]` attribute with policies
- Validate anti-forgery tokens for forms
- Use parameterized queries (EF Core does this by default)
- Don't log sensitive data
- Use HTTPS redirection middleware
- Store secrets in Azure Key Vault or environment variables
- Use User Secrets for local development
- Never commit secrets to source control
- Validate and sanitize all user input to prevent injection attacks
- Avoid storing sensitive data or security-relevant instructions in HTML comments

### Dependency Injection
- Register services with appropriate lifetime:
  - `Singleton`: stateless, thread-safe services
  - `Scoped`: per-request services (DbContext, etc.)
  - `Transient`: lightweight, stateless services
- Avoid captive dependencies (Singleton depending on Scoped)
- Use `IOptions<T>` pattern for configuration

### Async/Await
- Use `async`/`await` for I/O-bound operations (database, HTTP calls, file system)
- Always pass `CancellationToken` and respect it
- Avoid `.Result` or `.Wait()` (causes deadlocks)
- Use `ConfigureAwait(false)` in library code

### Advanced Async Patterns
- Prefer `ValueTask` for hot paths that often complete synchronously

### Controllers
- Keep controllers thin (delegate to services)
- Use `[ApiController]` attribute for automatic model validation
- Return `ActionResult<T>` for type safety
- Use `[ProducesResponseType]` for API documentation
- Implement API versioning (URL, header, or query string)
- Use consistent versioning strategy across endpoints

### Middleware
- Order matters: add middleware in correct sequence
- Authentication before Authorization
- Error handling middleware should be first (to catch all exceptions)
- Use `app.UseExceptionHandler()` for production error handling

### Model Validation
- Use Data Annotations or FluentValidation
- Validate at API boundary, not deep in business logic
- Return `400 Bad Request` for validation failures
- Include validation errors in response body

### Entity Framework Core (Essential)
- Use `AsNoTracking()` for read-only queries
- Avoid N+1 queries (use `Include()` or projection)
- Use migrations for schema changes
- Don't expose entities directly (use DTOs)
- Manage DbContext lifetime properly (scoped per request)
- Use async methods for database operations

### Advanced EF Core Patterns
- Use compiled queries for hot paths that execute frequently
- Use raw SQL via `FromSqlInterpolated`/`ExecuteSqlInterpolated` for complex queries while keeping parameters parameterized
- Define global query filters for concerns like soft deletes or multi-tenancy
- Consider splitting DbContexts by bounded context to keep models focused and reduce migration complexity

### Logging and Exception Handling
- Use structured logging with `ILogger<T>`
- Include correlation IDs for request tracing
- Log exceptions at appropriate levels (Error, Warning, Information)
- Use centralized exception handling middleware
- Don't catch exceptions unless you can handle them
- Include relevant context in log messages

### Thread Safety
- Singleton services must be thread-safe
- Avoid mutable shared state in singletons
- Use `lock`, `SemaphoreSlim`, or `ConcurrentDictionary` for shared resources
- Be cautious with static fields

### Testing
- Write unit tests for business logic
- Use in-memory providers for EF Core in tests
- Mock external dependencies with interfaces
- Test controller actions with integration tests
- Use `WebApplicationFactory` for integration testing
