---
name: aspnet-api-standards
description: "ASP.NET Core Web API implementation: clean controllers with CQRS, global error handling, model validation, Swagger/OpenAPI, API versioning, security (CORS, auth), middleware pipeline, and performance patterns. Use when creating or editing controllers, filters, middleware, Program.cs, or API endpoints."
---

# ASP.NET Core API Standards

## CRITICAL DIRECTIVE

**ONLY implement what is explicitly requested.** Do NOT add unrequested features like:
- CORS configuration (unless asked for)
- Swagger/OpenAPI setup (unless asked for)
- Authentication/Authorization (unless asked for)  
- Rate limiting, caching, compression (unless asked for)
- Additional middleware (unless asked for)

When user requests ONE thing (e.g., "create an exception filter"), implement ONLY that thing.

## Core Controller Rules (ALWAYS Apply)

### Clean Controllers Pattern
```csharp
// REQUIRED structure
[ApiController]
[Route("api/[controller]")]
public class OrdersController(IMediator mediator) : ControllerBase
{
    [HttpPost]
    public async Task<IActionResult> CreateOrder(
        [FromBody] CreateOrderCommand command,
        CancellationToken cancellationToken)
    {
        var result = await mediator.Send(command, cancellationToken);
        return CreatedAtAction(nameof(GetOrder), new { id = result }, result);
    }
}
```

**MUST:**
- Inject ONLY `IMediator` (never repositories or domain services)
- Use primary constructors
- Include `CancellationToken` in all async methods
- Apply `[ApiController]` attribute for automatic validation

**NEVER:**
- Put business logic in controllers
- Inject repositories directly
- Use `.Result`, `.Wait()`, or `.GetAwaiter().GetResult()`

## When to Read References

**User asks about exception handling or error responses?**  
→ Read [references/exception-handling.md](references/exception-handling.md)

**User asks about CORS, authentication, or authorization?**  
→ Read [references/security.md](references/security.md)

**User asks about Swagger or API documentation?**  
→ Read [references/swagger.md](references/swagger.md)

**User asks about middleware pipeline or Program.cs configuration?**  
→ Read [references/middleware.md](references/middleware.md)

## FluentValidation (Apply When Creating Commands/Queries)

```csharp
public class CreateOrderCommandValidator : AbstractValidator<CreateOrderCommand>
{
    public CreateOrderCommandValidator()
    {
        RuleFor(x => x.CustomerId).NotEmpty();
        RuleFor(x => x.Items).NotEmpty().Must(items => items.Count <= 50);
    }
}
```

**Register in Program.cs:**
```csharp
builder.Services.AddValidatorsFromAssemblyContaining<CreateOrderCommandValidator>();
builder.Services.AddFluentValidationAutoValidation();
```
