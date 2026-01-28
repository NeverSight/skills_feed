---
name: aspire
description: |
  Configures .NET Aspire orchestration, service discovery, and telemetry.
  Use when: Adding services to AppHost, configuring service defaults, setting up health checks, or troubleshooting service discovery.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# .NET Aspire Skill

.NET Aspire provides orchestration for this distributed ledger platform. The AppHost (`src/Apps/Sorcha.AppHost/AppHost.cs`) orchestrates 7 microservices with PostgreSQL, MongoDB, and Redis. Services use `AddServiceDefaults()` for consistent OpenTelemetry, health checks, and service discovery. JWT signing keys are generated once and shared across all services via environment variables.

## Quick Start

### Adding a Service to AppHost

```csharp
// In AppHost.cs - Add project with resource references
var myService = builder.AddProject<Projects.Sorcha_MyService>("my-service")
    .WithReference(redis)                                    // Service discovery
    .WithReference(walletDb)                                // Database connection
    .WithEnvironment("JwtSettings__SigningKey", jwtSigningKey); // Shared config
```

### Consuming Aspire in a Service

```csharp
// In Program.cs - Every service starts with this
var builder = WebApplication.CreateBuilder(args);

builder.AddServiceDefaults();                    // OpenTelemetry, health checks, discovery
builder.AddRedisOutputCache("redis");            // Reference by resource name
builder.AddRedisDistributedCache("redis");

var app = builder.Build();
app.MapDefaultEndpoints();                       // /health and /alive
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Resource Name | Identifier for service discovery | `"redis"`, `"tenant-service"` |
| WithReference | Injects connection string/URL | `.WithReference(postgres)` |
| WithEnvironment | Pass config to service | `.WithEnvironment("Key", value)` |
| WithExternalHttpEndpoints | Expose outside Aspire network | `.WithExternalHttpEndpoints()` |
| AddServiceDefaults | Shared Aspire configuration | `builder.AddServiceDefaults()` |

## Common Patterns

### Database Resources

```csharp
// PostgreSQL with multiple databases
var postgres = builder.AddPostgres("postgres").WithPgAdmin();
var tenantDb = postgres.AddDatabase("tenant-db", "sorcha_tenant");
var walletDb = postgres.AddDatabase("wallet-db", "sorcha_wallet");

// MongoDB for document storage
var mongodb = builder.AddMongoDB("mongodb").WithMongoExpress();
var registerDb = mongodb.AddDatabase("register-db", "sorcha_register");

// Redis for caching
var redis = builder.AddRedis("redis").WithRedisCommander();
```

### Service Dependencies

```csharp
// Service references other services for discovery
var validatorService = builder.AddProject<Projects.Sorcha_Validator_Service>("validator-service")
    .WithReference(redis)
    .WithReference(walletService)
    .WithReference(registerService)
    .WithReference(peerService)
    .WithReference(blueprintService);
```

### Health Endpoints

```csharp
// ServiceDefaults provides these automatically
app.MapHealthChecks("/health");           // Readiness - all checks
app.MapHealthChecks("/alive", new HealthCheckOptions
{
    Predicate = r => r.Tags.Contains("live")  // Liveness - tagged checks only
});
```

## See Also

- [patterns](references/patterns.md) - AppHost patterns, resource configuration
- [workflows](references/workflows.md) - Adding services, debugging, deployment

## Related Skills

- See the **dotnet** skill for .NET 10 patterns
- See the **minimal-apis** skill for endpoint configuration
- See the **redis** skill for cache configuration
- See the **postgresql** skill for database patterns
- See the **mongodb** skill for document storage
- See the **docker** skill for containerization

## Documentation Resources

> Fetch latest .NET Aspire documentation with Context7.

**How to use Context7:**
1. Use `mcp__context7__resolve-library-id` to search for "aspire"
2. **Prefer website documentation** (IDs starting with `/websites/`) over source code repositories when available
3. Query with `mcp__context7__query-docs` using the resolved library ID

**Library ID:** `/dotnet/docs-aspire` _(High reputation, 3264 code snippets)_

**Recommended Queries:**
- "AppHost service orchestration configuration"
- "service discovery WithReference patterns"
- "OpenTelemetry observability setup"
- "health checks readiness liveness"