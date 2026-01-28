---
name: scalar
description: |
  Generates and configures Scalar OpenAPI UI for API documentation.
  Use when: Adding API documentation to services, configuring OpenAPI endpoints, customizing documentation themes
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# Scalar Skill

Scalar replaces Swagger/Swashbuckle as the OpenAPI documentation UI in this codebase. All services use .NET 10's built-in `AddOpenApi()` with Scalar's `MapScalarApiReference()` for the UI. The project enforces Purple theme consistency across all microservices.

## Quick Start

### Standard Service Configuration

```csharp
// Program.cs - Service setup
builder.Services.AddOpenApi();

var app = builder.Build();
app.MapOpenApi();

if (app.Environment.IsDevelopment())
{
    app.MapScalarApiReference(options =>
    {
        options
            .WithTitle("Blueprint Service")
            .WithTheme(ScalarTheme.Purple)
            .WithDefaultHttpClient(ScalarTarget.CSharp, ScalarClient.HttpClient);
    });
}
```

### API Gateway with Aggregated Documentation

```csharp
// Aggregated OpenAPI from all services
app.MapGet("/openapi/aggregated.json", async (OpenApiAggregationService service) =>
{
    var spec = await service.GetAggregatedOpenApiAsync();
    return Results.Json(spec);
})
.ExcludeFromDescription();

app.MapScalarApiReference(options =>
{
    options
        .WithTitle("Sorcha API Gateway - All Services")
        .WithTheme(ScalarTheme.Purple)
        .WithDefaultHttpClient(ScalarTarget.CSharp, ScalarClient.HttpClient)
        .WithOpenApiRoutePattern("/openapi/aggregated.json");
});
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| `AddOpenApi()` | Register OpenAPI services | `builder.Services.AddOpenApi()` |
| `MapOpenApi()` | Expose `/openapi/v1.json` | `app.MapOpenApi()` |
| `MapScalarApiReference()` | Mount Scalar UI at `/scalar` | See examples above |
| `ScalarTheme` | Visual theme enum | `ScalarTheme.Purple` |
| `ScalarTarget` | Code generation target | `ScalarTarget.CSharp` |
| `ScalarClient` | HTTP client library | `ScalarClient.HttpClient` |

## Common Patterns

### Document Endpoints for Scalar

```csharp
app.MapPost("/api/wallets", handler)
    .WithName("CreateWallet")
    .WithSummary("Create a new wallet")
    .WithDescription("Creates an HD wallet with the specified algorithm")
    .WithTags("Wallets");
```

### Rich OpenAPI Descriptions with Markdown

```csharp
builder.Services.AddOpenApi(options =>
{
    options.AddDocumentTransformer((document, context, ct) =>
    {
        document.Info.Title = "Register Service API";
        document.Info.Version = "1.0.0";
        document.Info.Description = """
            # Register Service
            
            ## Overview
            Provides a **distributed ledger** for immutable transactions.
            
            ## Key Features
            - Cryptographic signatures
            - Chain integrity verification
            """;
        return Task.CompletedTask;
    });
});
```

## See Also

- [patterns](references/patterns.md)
- [workflows](references/workflows.md)

## Related Skills

- See the **minimal-apis** skill for endpoint documentation patterns
- See the **aspire** skill for service discovery integration
- See the **yarp** skill for API Gateway configuration

## Documentation Resources

> Fetch latest Scalar documentation with Context7.

**How to use Context7:**
1. Use `mcp__context7__resolve-library-id` to search for "scalar"
2. Prefer website documentation (`/websites/guides_scalar`) over source repositories
3. Query with `mcp__context7__query-docs` using the resolved library ID

**Library ID:** `/websites/guides_scalar`

**Recommended Queries:**
- "Scalar .NET ASP.NET Core configuration options themes"
- "Scalar themes available dark mode customization"
- "Scalar API reference configuration fluent API"