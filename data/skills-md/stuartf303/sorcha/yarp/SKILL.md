---
name: yarp
description: |
  Configures YARP reverse proxy for API gateway routing.
  Use when: Setting up API gateway routes, configuring path transformations, proxying requests to backend services, or aggregating microservice endpoints.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# YARP Skill

YARP (Yet Another Reverse Proxy) is the .NET reverse proxy used for API gateway routing in Sorcha. The gateway routes external requests to internal microservices while handling path transformations, security headers, and CORS. Key pattern: gateway-specific endpoints execute BEFORE `MapReverseProxy()` which must be called last.

## Quick Start

### Basic Setup

```csharp
// Program.cs - Add YARP with configuration-based routes
builder.Services.AddReverseProxy()
    .LoadFromConfig(builder.Configuration.GetSection("ReverseProxy"));

// CRITICAL: MapReverseProxy() must be called LAST
app.MapReverseProxy();
```

### Route Configuration

```json
{
  "ReverseProxy": {
    "Routes": {
      "blueprint-route": {
        "ClusterId": "blueprint-cluster",
        "Match": { "Path": "/api/blueprint/{**catch-all}" },
        "Transforms": [{ "PathPattern": "/api/{**catch-all}" }]
      }
    },
    "Clusters": {
      "blueprint-cluster": {
        "Destinations": {
          "destination1": { "Address": "http://blueprint-service:8080" }
        }
      }
    }
  }
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Route | Maps external path to cluster | `"Path": "/api/blueprint/{**catch-all}"` |
| Cluster | Backend service destination(s) | `"Address": "http://service:8080"` |
| Transform | Rewrites path before forwarding | `"PathPattern": "/api/{**catch-all}"` |
| Catch-all | Captures remaining path segments | `{**catch-all}` or `{*any}` |

## Common Patterns

### Path Prefix Stripping

**When:** External API has service prefix, backend doesn't

```json
{
  "Match": { "Path": "/api/blueprint/{**catch-all}" },
  "Transforms": [{ "PathPattern": "/api/{**catch-all}" }]
}
```
Request: `GET /api/blueprint/blueprints` → Backend: `GET /api/blueprints`

### Health Endpoint Mapping

**When:** Unified health checks across services

```json
{
  "blueprint-status-route": {
    "ClusterId": "blueprint-cluster",
    "Match": { "Path": "/api/blueprint/status" },
    "Transforms": [{ "PathPattern": "/api/health" }]
  }
}
```

### X-Forwarded Headers

**When:** Backend needs original client info

```json
"Transforms": [
  { "PathPattern": "/api/{**catch-all}" },
  { "X-Forwarded": "Set" }
]
```

## See Also

- [patterns](references/patterns.md) - Route patterns and transformations
- [workflows](references/workflows.md) - Setup and testing workflows

## Related Skills

- See the **aspire** skill for service discovery integration
- See the **minimal-apis** skill for gateway-specific endpoints
- See the **jwt** skill for authentication pass-through
- See the **docker** skill for container networking

## Documentation Resources

> Fetch latest YARP documentation with Context7.

**How to use Context7:**
1. Use `mcp__context7__resolve-library-id` to search for "yarp"
2. Query with `mcp__context7__query-docs` using the resolved library ID

**Library ID:** `/dotnet/yarp`

**Recommended Queries:**
- "YARP configuration routes clusters transforms"
- "YARP load balancing health checks"
- "YARP request transforms path rewriting"