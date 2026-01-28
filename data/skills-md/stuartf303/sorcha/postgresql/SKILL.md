---
name: postgresql
description: |
  Manages PostgreSQL databases and Entity Framework Core integration.
  Use when: configuring database connections, writing migrations, creating DbContext classes, optimizing queries, or integrating with .NET Aspire.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# PostgreSQL Skill

PostgreSQL database management for Sorcha's distributed ledger platform. This project uses PostgreSQL 17 with Npgsql 8.0+ and Entity Framework Core 10, featuring dedicated schemas (`wallet`, `public`), JSONB columns for metadata, and .NET Aspire service discovery for connection management.

## Quick Start

### DbContext with PostgreSQL Schema

```csharp
// src/Common/Sorcha.Wallet.Core/Data/WalletDbContext.cs
public class WalletDbContext : DbContext
{
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.HasDefaultSchema("wallet");
        
        modelBuilder.Entity<Wallet>(entity =>
        {
            entity.ToTable("wallets");
            entity.HasKey(e => e.Address);
            
            // JSONB for metadata
            entity.Property(e => e.Metadata)
                .HasColumnType("jsonb");
            
            // Soft delete filter
            entity.HasQueryFilter(e => e.DeletedAt == null);
        });
    }
}
```

### Npgsql Configuration with Retry

```csharp
// src/Services/Sorcha.Wallet.Service/Extensions/WalletServiceExtensions.cs
services.AddNpgsqlDataSource(connectionString, dataSourceBuilder =>
{
    dataSourceBuilder.EnableDynamicJson();  // Required for Dictionary serialization
});

services.AddDbContext<WalletDbContext>(options =>
{
    options.UseNpgsql(connectionString, npgsqlOptions =>
    {
        npgsqlOptions.EnableRetryOnFailure(
            maxRetryCount: 10,
            maxRetryDelay: TimeSpan.FromSeconds(30),
            errorCodesToAdd: null);
        npgsqlOptions.MigrationsHistoryTable("__EFMigrationsHistory", "wallet");
    });
});
```

### Aspire Service Discovery

```csharp
// src/Apps/Sorcha.AppHost/AppHost.cs
var postgres = builder.AddPostgres("postgres").WithPgAdmin();
var walletDb = postgres.AddDatabase("wallet-db", "sorcha_wallet");

builder.AddProject<Projects.Sorcha_Wallet_Service>("wallet-service")
    .WithReference(walletDb);  // Auto-injects connection string
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Schema isolation | Separate domains | `modelBuilder.HasDefaultSchema("wallet")` |
| JSONB columns | Flexible metadata | `HasColumnType("jsonb")` |
| Soft deletes | Query filters | `HasQueryFilter(e => e.DeletedAt == null)` |
| Row versioning | Concurrency | `Property(e => e.RowVersion).IsRowVersion()` |
| Composite indexes | Query performance | `HasIndex(e => new { e.Owner, e.Tenant })` |
| UUID generation | Primary keys | `HasDefaultValueSql("gen_random_uuid()")` |

## Common Patterns

### High-Precision Decimal for Crypto

**When:** Storing cryptocurrency amounts

```csharp
entity.Property(e => e.Balance)
    .HasColumnType("numeric(28,18)")
    .HasPrecision(28, 18);
```

### Timestamp with Timezone

**When:** Audit trails with timezone awareness

```csharp
entity.Property(e => e.CreatedAt)
    .HasColumnType("timestamp with time zone")
    .HasDefaultValueSql("CURRENT_TIMESTAMP");
```

## See Also

- [patterns](references/patterns.md) - DbContext configuration, indexing strategies
- [workflows](references/workflows.md) - Migrations, health checks, initialization

## Related Skills

- **entity-framework** - ORM patterns and repository implementations
- **aspire** - Service discovery and connection string injection
- **docker** - PostgreSQL container configuration

## Documentation Resources

> Fetch latest PostgreSQL documentation with Context7.

**How to use Context7:**
1. Use `mcp__context7__resolve-library-id` to search for "postgresql" or "npgsql efcore"
2. **Prefer website documentation** (IDs starting with `/websites/`) over source code repositories
3. Query with `mcp__context7__query-docs` using the resolved library ID

**Library IDs:**
- PostgreSQL: `/websites/postgresql` (61K snippets, High reputation)
- Npgsql EF Core: `/websites/npgsql_efcore_index_html`
- EF Core: `/dotnet/entityframework.docs` (4K snippets, High reputation)

**Recommended Queries:**
- "Index creation strategies"
- "JSONB operators and functions"
- "Connection pooling configuration"
- "Query performance optimization"