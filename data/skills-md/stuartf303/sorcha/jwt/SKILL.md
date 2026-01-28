---
name: jwt
description: |
  Implements JWT Bearer authentication for service-to-service and user authorization.
  Use when: Configuring authentication, creating authorization policies, issuing/validating tokens, or troubleshooting 401/403 errors.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# JWT Authentication Skill

Sorcha uses **JWT Bearer authentication** with the **Tenant Service** as the token issuer. All services validate tokens using shared `JwtSettings` from `Sorcha.ServiceDefaults`. Tokens support three types: user (email/password), service (client credentials), and delegated (service acting on behalf of user).

## Quick Start

### Service Authentication Setup

```csharp
// Program.cs - Any Sorcha service
var builder = WebApplication.CreateBuilder(args);

// 1. Add JWT authentication (shared key auto-generated in dev)
builder.AddJwtAuthentication();

// 2. Add service-specific authorization policies
builder.Services.AddBlueprintAuthorization();

var app = builder.Build();

// 3. CRITICAL: Order matters!
app.UseAuthentication();
app.UseAuthorization();

app.MapBlueprintEndpoints();
app.Run();
```

### Protect an Endpoint

```csharp
// Minimal API pattern
group.MapPost("/", CreateBlueprint)
    .WithName("CreateBlueprint")
    .RequireAuthorization("CanManageBlueprints");
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Token Types | Differentiate user vs service | `token_type` claim: `"user"` or `"service"` |
| Organization Scope | Isolate tenant data | `org_id` claim in token |
| Signing Key | Symmetric HMAC-SHA256 | Auto-generated in dev, Azure Key Vault in prod |
| Token Lifetime | Configurable per type | Access: 60min, Refresh: 24hr, Service: 8hr |

## Common Patterns

### Custom Authorization Policy

**When:** Endpoint requires specific claims beyond role-based auth.

```csharp
// AuthenticationExtensions.cs
options.AddPolicy("CanManageBlueprints", policy =>
    policy.RequireAssertion(context =>
    {
        var hasOrgId = context.User.Claims.Any(c => c.Type == "org_id" && !string.IsNullOrEmpty(c.Value));
        var isService = context.User.Claims.Any(c => c.Type == "token_type" && c.Value == "service");
        return hasOrgId || isService;
    }));
```

### Extract Claims in Handler

**When:** Need user/org context in endpoint logic.

```csharp
async Task<IResult> HandleRequest(ClaimsPrincipal user, ...)
{
    var userId = user.FindFirst(JwtRegisteredClaimNames.Sub)?.Value;
    var orgId = user.FindFirst("org_id")?.Value;
    
    if (string.IsNullOrEmpty(orgId))
        return Results.Forbid();
    
    // Use orgId for data isolation
}
```

## See Also

- [patterns](references/patterns.md) - Token generation, validation, policies
- [workflows](references/workflows.md) - Setup, testing, troubleshooting

## Related Skills

- See the **minimal-apis** skill for endpoint configuration with `.RequireAuthorization()`
- See the **aspire** skill for shared configuration via `ServiceDefaults`
- See the **redis** skill for token revocation tracking
- See the **yarp** skill for gateway-level authentication

## Documentation Resources

> Fetch latest JWT/authentication documentation with Context7.

**How to use Context7:**
1. Use `mcp__context7__resolve-library-id` to search for "asp.net core authentication jwt"
2. **Prefer website documentation** (IDs starting with `/websites/`) over source code repositories
3. Query with `mcp__context7__query-docs` using the resolved library ID

**Recommended Queries:**
- "JWT Bearer authentication setup"
- "authorization policies claims"
- "token validation parameters"