---
name: minimal-apis
description: |
  Defines REST endpoints using Minimal APIs with OpenAPI documentation via Scalar.
  Use when: Creating or modifying API endpoints in Sorcha services, adding new routes, configuring endpoint authentication, or documenting APIs.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# Minimal APIs Skill

Sorcha uses .NET 10 Minimal APIs exclusively—NEVER MVC controllers. All endpoints are organized via `MapGroup()` route grouping with extension methods in `Endpoints/` folders. OpenAPI documentation uses **Scalar** (NOT Swagger).

## Quick Start

### Route Group with Authorization

```csharp
// src/Services/Sorcha.Wallet.Service/Endpoints/WalletEndpoints.cs
public static IEndpointRouteBuilder MapWalletEndpoints(this IEndpointRouteBuilder app)
{
    var walletGroup = app.MapGroup("/api/v1/wallets")
        .WithTags("Wallets")
        .RequireAuthorization("CanManageWallets");

    walletGroup.MapPost("/", CreateWallet)
        .WithName("CreateWallet")
        .WithSummary("Create a new wallet")
        .WithDescription("Creates a new HD wallet with the specified algorithm");

    walletGroup.MapGet("/{address}", GetWallet)
        .WithName("GetWallet")
        .WithSummary("Get wallet by address");

    return app;
}
```

### Endpoint Handler with DI

```csharp
private static async Task<IResult> CreateWallet(
    [FromBody] CreateWalletRequest request,
    WalletManager walletManager,
    HttpContext context,
    ILogger<Program> logger,
    CancellationToken cancellationToken = default)
{
    try
    {
        var (wallet, mnemonic) = await walletManager.CreateWalletAsync(...);
        return Results.Created($"/api/v1/wallets/{wallet.Address}", response);
    }
    catch (ArgumentException ex)
    {
        return Results.BadRequest(new ProblemDetails { Title = "Invalid Request", Detail = ex.Message });
    }
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Route Groups | Shared config for related endpoints | `app.MapGroup("/api/v1/wallets").WithTags("Wallets")` |
| TypedResults | Type-safe return values | `Results<Ok<T>, NotFound, ValidationProblem>` |
| OpenAPI Metadata | `.WithName()`, `.WithSummary()` | Required on all endpoints |
| Authorization | `.RequireAuthorization("Policy")` | Apply to groups or individual endpoints |
| AllowAnonymous | Public endpoints | `.AllowAnonymous()` on login routes |
| Cache Output | Redis output caching | `.CacheOutput(p => p.Expire(...).Tag("tag"))` |

## Common Patterns

### TypedResults for Explicit Return Types

```csharp
private static async Task<Results<Ok<TokenResponse>, UnauthorizedHttpResult, ValidationProblem>> Login(
    LoginRequest request,
    ITokenService tokenService)
{
    if (string.IsNullOrWhiteSpace(request.Email))
        return TypedResults.ValidationProblem(new Dictionary<string, string[]>
        {
            ["email"] = ["Email is required"]
        });

    var token = await tokenService.LoginAsync(request);
    if (token == null) return TypedResults.Unauthorized();

    return TypedResults.Ok(token);
}
```

### Query Parameters with Defaults

```csharp
walletGroup.MapGet("/{address}/addresses", ListAddresses);

private static async Task<IResult> ListAddresses(
    string address,                              // Route parameter
    [FromQuery] string? type = null,             // Optional filter
    [FromQuery] bool? used = null,               // Optional filter
    [FromQuery] int page = 1,                    // Default pagination
    [FromQuery] int pageSize = 50)
```

## See Also

- [patterns](references/patterns.md) - Endpoint organization, error handling, caching
- [workflows](references/workflows.md) - Creating new endpoints, adding authorization

## Related Skills

- See the **aspire** skill for service orchestration and configuration
- See the **scalar** skill for OpenAPI documentation UI
- See the **jwt** skill for authentication and authorization setup
- See the **redis** skill for output caching configuration
- See the **signalr** skill for real-time endpoint notifications

## Documentation Resources

> Fetch latest ASP.NET Core Minimal APIs documentation with Context7.

**How to use Context7:**
1. Use `mcp__context7__resolve-library-id` to search for "aspnetcore"
2. Prefer `/websites/learn_microsoft_en-us_aspnet_core` for official docs
3. Query with `mcp__context7__query-docs`

**Library ID:** `/websites/learn_microsoft_en-us_aspnet_core`

**Recommended Queries:**
- "minimal apis route groups"
- "minimal apis typed results"
- "minimal apis authorization"
- "minimal apis openapi documentation"