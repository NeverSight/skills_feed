---
name: mongodb
description: |
  Configures MongoDB document storage and query operations for Sorcha's distributed ledger
  Use when: implementing document storage, querying collections, creating indexes, or working with Register/Transaction/Docket data
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# MongoDB Skill

MongoDB is the document store for Sorcha's Register Service, providing storage for registers, transactions, dockets, and system blueprints. The codebase uses a two-tier storage architecture: **warm-tier** (mutable `IDocumentStore<T>`) and **cold-tier** (immutable `IWormStore<T>` for WORM/ledger data).

## Quick Start

### Connection Setup

```csharp
// Program.cs - Register Service
builder.Services.AddSingleton<IMongoClient>(sp =>
{
    var connectionString = builder.Configuration.GetConnectionString("MongoDB") 
        ?? "mongodb://localhost:27017";
    return new MongoClient(connectionString);
});

builder.Services.AddSingleton<IMongoDatabase>(sp =>
{
    var client = sp.GetRequiredService<IMongoClient>();
    return client.GetDatabase("sorcha_register");
});
```

### Repository Registration

```csharp
// Use extension method from Sorcha.Storage.MongoDB
builder.Services.AddMongoClient(builder.Configuration);
builder.Services.AddMongoDatabase("sorcha_register");
builder.Services.AddMongoDocumentStore<Blueprint, string>(
    "blueprints",
    doc => doc.Id,
    doc => doc.Id
);
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Filter Builders | Type-safe queries | `Builders<T>.Filter.Eq(x => x.Id, id)` |
| Update Builders | Atomic updates | `Builders<T>.Update.Set(x => x.Height, 10)` |
| Composite Indexes | Multi-field queries | `IndexKeys.Ascending(x => x.RegisterId).Ascending(x => x.TxId)` |
| WORM Store | Immutable ledger data | `IWormStore<Transaction, string>` - no updates/deletes |
| Document Store | Mutable documents | `IDocumentStore<Blueprint, string>` - full CRUD |

## Common Patterns

### Filtered Query with Pagination

```csharp
var filter = Builders<TransactionModel>.Filter.And(
    Builders<TransactionModel>.Filter.Eq(t => t.RegisterId, registerId),
    Builders<TransactionModel>.Filter.Gte(t => t.TimeStamp, since)
);

var results = await _collection
    .Find(filter)
    .SortByDescending(t => t.TimeStamp)
    .Skip(page * pageSize)
    .Limit(pageSize)
    .ToListAsync(cancellationToken);
```

### Array Element Query

```csharp
// Find transactions where address is in RecipientsWallets array
var filter = Builders<TransactionModel>.Filter.AnyEq(
    t => t.RecipientsWallets, 
    walletAddress
);
```

## See Also

- [patterns](references/patterns.md)
- [types](references/types.md)
- [modules](references/modules.md)
- [errors](references/errors.md)

## Related Skills

- **dotnet** - Runtime and C# patterns
- **entity-framework** - Alternative ORM (PostgreSQL uses EF)
- **redis** - Caching layer integration
- **docker** - MongoDB container setup
- **xunit** - Integration tests with Testcontainers

## Documentation Resources

> Fetch latest MongoDB C# driver documentation with Context7.

**How to use Context7:**
1. Use `mcp__context7__resolve-library-id` to search for "mongodb c# driver"
2. Query with `mcp__context7__query-docs` using the resolved library ID

**Library ID:** `/mongodb/mongo-csharp-driver`

**Recommended Queries:**
- "filter builder examples CRUD operations"
- "BSON serialization attributes"
- "index creation async"
- "aggregation pipeline C#"