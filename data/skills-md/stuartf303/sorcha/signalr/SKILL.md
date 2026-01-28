---
name: signalr
description: |
  Implements real-time WebSocket communication using SignalR for action notifications and register events.
  Use when: Adding real-time notifications, creating hub endpoints, broadcasting to groups, or testing WebSocket communication.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# SignalR Skill

ASP.NET Core SignalR implementation for real-time client-server communication. Sorcha uses two hubs: `ActionsHub` (Blueprint Service) for workflow notifications and `RegisterHub` (Register Service) for ledger events. Both use group-based broadcasting with JWT authentication via query parameters.

## Quick Start

### Hub Implementation

```csharp
// Strongly-typed hub with client interface
public class RegisterHub : Hub<IRegisterHubClient>
{
    public async Task SubscribeToRegister(string registerId)
    {
        await Groups.AddToGroupAsync(Context.ConnectionId, $"register:{registerId}");
    }
}

public interface IRegisterHubClient
{
    Task RegisterCreated(string registerId, string name);
    Task TransactionConfirmed(string registerId, string transactionId);
}
```

### Sending from Services

```csharp
public class NotificationService
{
    private readonly IHubContext<ActionsHub> _hubContext;

    public async Task NotifyActionConfirmedAsync(ActionNotification notification, CancellationToken ct)
    {
        await _hubContext.Clients
            .Group($"wallet:{notification.WalletAddress}")
            .SendAsync("ActionConfirmed", notification, ct);
    }
}
```

### Client Connection (Testing)

```csharp
var connection = new HubConnectionBuilder()
    .WithUrl($"{baseUrl}/actionshub?access_token={jwt}")
    .Build();

connection.On<ActionNotification>("ActionConfirmed", notification => { /* handle */ });
await connection.StartAsync();
await connection.InvokeAsync("SubscribeToWallet", walletAddress);
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Groups | Route messages to subscribers | `wallet:{address}`, `register:{id}`, `tenant:{id}` |
| Typed Hubs | Compile-time safety | `Hub<IRegisterHubClient>` |
| IHubContext | Send from services | Inject `IHubContext<THub>` |
| JWT Auth | Query parameter auth | `?access_token={jwt}` |

## Common Patterns

### Service Abstraction Over Hub

**When:** Decoupling business logic from SignalR implementation

```csharp
// Interface in Services/Interfaces/
public interface INotificationService
{
    Task NotifyActionAvailableAsync(ActionNotification notification, CancellationToken ct = default);
}

// Register in DI
builder.Services.AddScoped<INotificationService, NotificationService>();
```

### Hub Registration in Program.cs

```csharp
builder.Services.AddSignalR();

// Map after authentication middleware
app.MapHub<ActionsHub>("/actionshub");
app.MapHub<RegisterHub>("/hubs/register");
```

## See Also

- [patterns](references/patterns.md) - Hub patterns, group routing, typed clients
- [workflows](references/workflows.md) - Testing, scaling, authentication setup

## Related Skills

- **aspire** - Service orchestration and configuration
- **jwt** - Authentication token setup for hub connections
- **redis** - Backplane configuration for scaling
- **xunit** - Integration testing patterns
- **fluent-assertions** - Test assertions for hub tests

## Documentation Resources

> Fetch latest SignalR documentation with Context7.

**How to use Context7:**
1. Use `mcp__context7__resolve-library-id` to search for "signalr aspnetcore"
2. **Prefer website documentation** (IDs starting with `/websites/`) over source code
3. Query with `mcp__context7__query-docs` using the resolved library ID

**Library ID:** `/websites/learn_microsoft_en-us_aspnet_core` _(ASP.NET Core docs including SignalR)_

**Recommended Queries:**
- "SignalR hub groups authentication"
- "SignalR Redis backplane scaling"
- "SignalR strongly typed hubs"