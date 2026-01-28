---
name: entity-framework
description: |
  Handles Entity Framework Core database access, migrations, and repository patterns for PostgreSQL.
  Use when: Creating DbContext classes, writing migrations, implementing repositories, configuring entity relationships, or optimizing database queries.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# Entity Framework Core Skill

Sorcha uses EF Core 9+ with PostgreSQL (Npgsql) as the primary relational data store. The codebase implements a layered repository pattern with generic and specialized repositories, soft delete via query filters, and automatic migrations on startup.

## Quick Start

### Register DbContext with PostgreSQL

```csharp
// src/Common/Sorcha.Storage.EFCore/Extensions/EFCoreServiceExtensions.cs
services.AddDbContext<WalletDbContext>((sp, options) =>
{
    var dataSource = sp.GetRequiredService<NpgsqlDataSource>();
    options.UseNpgsql(dataSource, npgsql =>
    {
        npgsql.EnableRetryOnFailure(maxRetryCount: 10, maxRetryDelay: TimeSpan.FromSeconds(30), errorCodesToAdd: null);
        npgsql.MigrationsHistoryTable("__EFMigrationsHistory", "wallet");
    });
});
```

### Create a Migration

```bash
# From project directory containing DbContext
dotnet ef migrations add InitialSchema --project src/Common/Sorcha.Wallet.Core --startup-project src/Services/Sorcha.Wallet.Service
```

### Apply Migrations Programmatically

```csharp
// Startup pattern used in Sorcha services
var pending = await dbContext.Database.GetPendingMigrationsAsync();
if (pending.Any())
    await dbContext.Database.MigrateAsync();
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| DbContext | Schema definition + change tracking | `WalletDbContext`, `TenantDbContext` |
| Repository | Data access abstraction | `EFCoreRepository<T, TId, TContext>` |
| Soft Delete | Query filter on `DeletedAt` | `.HasQueryFilter(e => e.DeletedAt == null)` |
| JSONB | PostgreSQL JSON columns | `.HasColumnType("jsonb")` |
| ExecuteUpdate | Bulk updates without loading | `ExecuteUpdateAsync(s => s.SetProperty(...))` |

## Common Patterns

### Repository with Optional Eager Loading

```csharp
// src/Common/Sorcha.Wallet.Core/Repositories/EfCoreWalletRepository.cs
public async Task<WalletEntity?> GetByAddressAsync(string address, bool includeAddresses = false)
{
    IQueryable<WalletEntity> query = _context.Wallets;
    
    if (includeAddresses)
        query = query.Include(w => w.Addresses);
    
    return await query.AsNoTracking().FirstOrDefaultAsync(w => w.Address == address);
}
```

### Soft Delete with Filter Bypass

```csharp
// Bypass query filter for admin operations
var deleted = await _context.Wallets
    .IgnoreQueryFilters()
    .FirstOrDefaultAsync(w => w.Address == address);
```

## See Also

- [patterns](references/patterns.md) - DbContext configuration, entity mapping, query optimization
- [workflows](references/workflows.md) - Migration commands, testing patterns, deployment

## Related Skills

- See the **postgresql** skill for connection configuration and PostgreSQL-specific features
- See the **aspire** skill for service registration and health checks
- See the **xunit** skill for testing DbContext with InMemory provider

## Documentation Resources

> Fetch latest EF Core documentation with Context7.

**Library ID:** `/dotnet/entityframework.docs`

**Recommended Queries:**
- "DbContext pooling configuration dependency injection"
- "migrations code-first apply production deployment"
- "query filters soft delete global filters"
- "bulk operations ExecuteUpdate ExecuteDelete"