---
name: grpc
description: |
  Defines gRPC services for peer-to-peer network communication in Sorcha.
  Use when: Creating service-to-service communication, implementing P2P protocols,
  defining proto contracts, configuring gRPC channels, or handling streaming RPCs.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# gRPC Skill

Sorcha uses gRPC for high-performance service-to-service communication, particularly for validator consensus, peer discovery, and wallet signing operations. The codebase follows .NET gRPC patterns with proto-first contract design.

## Quick Start

### Define a Proto Contract

```protobuf
// src/Services/Sorcha.*.Service/Protos/service_name.proto
syntax = "proto3";
package sorcha.servicename.v1;
option csharp_namespace = "Sorcha.ServiceName.Grpc.V1";

import "google/protobuf/empty.proto";

service MyService {
  rpc GetStatus(google.protobuf.Empty) returns (StatusResponse);
  rpc ProcessItem(ItemRequest) returns (ItemResponse);
}
```

### Implement the Service

```csharp
// GrpcServices/MyGrpcService.cs
public class MyGrpcService : Protos.MyService.MyServiceBase
{
    private readonly ILogger<MyGrpcService> _logger;
    
    public override async Task<StatusResponse> GetStatus(
        Empty request, ServerCallContext context)
    {
        context.CancellationToken.ThrowIfCancellationRequested();
        return new StatusResponse { IsHealthy = true };
    }
}
```

### Register and Map the Service

```csharp
// Program.cs
builder.Services.AddGrpc(options => options.EnableDetailedErrors = true);

var app = builder.Build();
app.MapGrpcService<MyGrpcService>();
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Proto-first | Define contracts in `.proto` files | `Protos/wallet_service.proto` |
| Service base | Inherit generated base class | `: WalletService.WalletServiceBase` |
| ServerCallContext | Access metadata, cancellation, deadlines | `context.CancellationToken` |
| GrpcChannel | Reusable client connection | `GrpcChannel.ForAddress(endpoint)` |
| Streaming | Server/client/bidirectional streams | `returns (stream Entry)` |

## Project Structure

```
Services/Sorcha.*.Service/
├── Protos/               # Proto contract files
│   └── service.proto
├── GrpcServices/         # Service implementations
│   └── MyGrpcService.cs
└── Program.cs            # gRPC registration
```

## Common Patterns

### gRPC Channel with Keep-Alive

**When:** Creating long-lived connections between services

```csharp
builder.Services.AddSingleton(sp =>
{
    var config = sp.GetRequiredService<ServiceConfiguration>();
    return GrpcChannel.ForAddress(config.Endpoint, new GrpcChannelOptions
    {
        HttpHandler = new SocketsHttpHandler
        {
            PooledConnectionIdleTimeout = TimeSpan.FromMinutes(5),
            KeepAlivePingDelay = TimeSpan.FromSeconds(60),
            KeepAlivePingTimeout = TimeSpan.FromSeconds(30),
            EnableMultipleHttp2Connections = true
        }
    });
});
```

### Dual-Port Kestrel Configuration

**When:** Separating gRPC (HTTP/2) from REST/health endpoints

```csharp
builder.WebHost.ConfigureKestrel(options =>
{
    // REST + health checks
    options.ListenAnyIP(8080, o => o.Protocols = HttpProtocols.Http1AndHttp2);
    // gRPC only
    options.ListenAnyIP(5000, o => o.Protocols = HttpProtocols.Http2);
});
```

## See Also

- [patterns](references/patterns.md) - Service implementation and client patterns
- [workflows](references/workflows.md) - Proto compilation and deployment workflows

## Related Skills

- **dotnet** - Runtime and C# patterns
- **aspire** - Service orchestration and discovery
- **minimal-apis** - REST endpoints alongside gRPC

## Documentation Resources

> Fetch latest gRPC documentation with Context7.

**How to use Context7:**
1. Use `mcp__context7__resolve-library-id` to search for "grpc dotnet"
2. Prefer website documentation (IDs starting with `/websites/`) when available
3. Query with `mcp__context7__query-docs` using the resolved library ID

**Recommended Queries:**
- "grpc aspnet core getting started"
- "grpc streaming server client"
- "grpc interceptors authentication"