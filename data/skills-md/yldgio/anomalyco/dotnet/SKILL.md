---
name: dotnet
description: ASP.NET Core patterns, dependency injection, middleware, async/await, and security
---

## .NET Code Review Rules

### Dependency Injection
- Register services with appropriate lifetime:
  - `Singleton`: stateless, thread-safe services
  - `Scoped`: per-request services (DbContext, etc.)
  - `Transient`: lightweight, stateless services
- Avoid captive dependencies (Singleton depending on Scoped)
- Use `IOptions<T>` pattern for configuration

### Async/Await
- Use `async`/`await` for I/O-bound operations
- Always pass `CancellationToken` and respect it
- Avoid `.Result` or `.Wait()` (causes deadlocks)
- Use `ConfigureAwait(false)` in library code
- Prefer `ValueTask` for hot paths that often complete synchronously

### Controllers
- Keep controllers thin (delegate to services)
- Use `[ApiController]` attribute for automatic model validation
- Return `ActionResult<T>` for type safety
- Use `[ProducesResponseType]` for API documentation

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

### Security
- Use `[Authorize]` attribute with policies
- Validate anti-forgery tokens for forms
- Use parameterized queries (EF Core does this by default)
- Don't log sensitive data
- Use HTTPS redirection middleware

### Entity Framework Core
- Use `AsNoTracking()` for read-only queries
- Avoid N+1 queries (use `Include()` or projection)
- Use migrations for schema changes
- Don't expose entities directly (use DTOs)
