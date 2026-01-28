---
name: data-access
description: Implement data access for the .NET 8 WPF widget host app using EF Core or Dapper. Use when creating repositories, unit of work, migrations, DbContext configuration, and query patterns while keeping clean architecture boundaries.
---

# Data Access

## Overview

Define reliable persistence patterns using EF Core while maintaining clean architecture boundaries between Infrastructure and Application layers.

## Constraints

- .NET 8 with EF Core 8
- SQLite database at `%LocalAppData%\3SC\3sc.db`
- Clean architecture boundaries
- Repository pattern with Unit of Work

## Definition of Done (DoD)

- [ ] Repository interfaces in Application layer, implementations in Infrastructure
- [ ] DbContext created per operation (factory pattern) - NOT singleton
- [ ] Read queries use `AsNoTracking()` for performance
- [ ] Write operations use explicit `SaveChangesAsync()` via Unit of Work
- [ ] No raw SQL outside Infrastructure layer
- [ ] Integration tests exist for repository operations
- [ ] Transient database errors are handled with retry logic

## Database Configuration

### DbContext Factory Pattern

```csharp
// ✅ GOOD - Factory creates context per operation
public interface IDbContextFactory
{
    AppDbContext CreateDbContext();
}

public class SqliteDbContextFactory : IDbContextFactory
{
    private readonly string _connectionString;
    
    public SqliteDbContextFactory(string dbPath)
    {
        _connectionString = $"Data Source={dbPath}";
    }
    
    public AppDbContext CreateDbContext()
    {
        var options = new DbContextOptionsBuilder<AppDbContext>()
            .UseSqlite(_connectionString)
            .Options;
        return new AppDbContext(options);
    }
}

// Usage in repository
public async Task<Widget?> GetByKeyAsync(string key, CancellationToken ct)
{
    await using var context = _factory.CreateDbContext();
    return await context.Widgets
        .AsNoTracking()
        .FirstOrDefaultAsync(w => w.WidgetKey == key, ct);
}
```

### Connection String

```csharp
// Standard location
var dbPath = Path.Combine(
    Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
    "3SC", "3sc.db");
```

## Repository Pattern

### Interface Definition (Application Layer)

```csharp
public interface IWidgetRepository
{
    Task<Widget?> GetByKeyAsync(string widgetKey, CancellationToken ct = default);
    Task<IReadOnlyList<Widget>> GetAllAsync(CancellationToken ct = default);
    Task<IReadOnlyList<Widget>> SearchAsync(string query, CancellationToken ct = default);
    Task AddAsync(Widget widget, CancellationToken ct = default);
    Task UpdateAsync(Widget widget, CancellationToken ct = default);
    Task DeleteAsync(string widgetKey, CancellationToken ct = default);
    Task<bool> ExistsAsync(string widgetKey, CancellationToken ct = default);
}
```

### Implementation (Infrastructure Layer)

```csharp
public class WidgetRepository : IWidgetRepository
{
    private readonly IDbContextFactory _factory;
    
    public WidgetRepository(IDbContextFactory factory)
    {
        _factory = factory;
    }
    
    public async Task<IReadOnlyList<Widget>> GetAllAsync(CancellationToken ct = default)
    {
        await using var context = _factory.CreateDbContext();
        return await context.Widgets
            .AsNoTracking()
            .OrderBy(w => w.DisplayName)
            .ToListAsync(ct);
    }
    
    public async Task<IReadOnlyList<Widget>> SearchAsync(string query, CancellationToken ct = default)
    {
        await using var context = _factory.CreateDbContext();
        
        // Use EF.Functions for case-insensitive search
        return await context.Widgets
            .AsNoTracking()
            .Where(w => EF.Functions.Like(w.DisplayName, $"%{query}%") ||
                        EF.Functions.Like(w.Description ?? "", $"%{query}%"))
            .OrderBy(w => w.DisplayName)
            .ToListAsync(ct);
    }
    
    public async Task AddAsync(Widget widget, CancellationToken ct = default)
    {
        await using var context = _factory.CreateDbContext();
        context.Widgets.Add(widget);
        await context.SaveChangesAsync(ct);
    }
}
```

## Unit of Work

For operations spanning multiple repositories:

```csharp
public interface IUnitOfWork : IDisposable
{
    IWidgetRepository Widgets { get; }
    IWidgetInstanceRepository WidgetInstances { get; }
    ILayoutRepository Layouts { get; }
    
    Task<int> SaveChangesAsync(CancellationToken ct = default);
    Task BeginTransactionAsync(CancellationToken ct = default);
    Task CommitAsync(CancellationToken ct = default);
    Task RollbackAsync();
}

// Usage
await using var uow = _unitOfWorkFactory.Create();
await uow.Widgets.AddAsync(widget, ct);
await uow.WidgetInstances.AddAsync(instance, ct);
await uow.SaveChangesAsync(ct);
```

## Query Patterns

### Projections (Recommended for Read)

```csharp
// ✅ GOOD - Select only needed fields
public async Task<IReadOnlyList<WidgetSummary>> GetSummariesAsync(CancellationToken ct)
{
    await using var context = _factory.CreateDbContext();
    return await context.Widgets
        .AsNoTracking()
        .Select(w => new WidgetSummary
        {
            WidgetKey = w.WidgetKey,
            DisplayName = w.DisplayName,
            InstanceCount = w.Instances.Count
        })
        .ToListAsync(ct);
}
```

### Pagination

```csharp
public async Task<PagedResult<Widget>> GetPagedAsync(
    int page, int pageSize, CancellationToken ct = default)
{
    await using var context = _factory.CreateDbContext();
    var query = context.Widgets.AsNoTracking();
    
    var totalCount = await query.CountAsync(ct);
    var items = await query
        .OrderBy(w => w.DisplayName)
        .Skip((page - 1) * pageSize)
        .Take(pageSize)
        .ToListAsync(ct);
    
    return new PagedResult<Widget>(items, totalCount, page, pageSize);
}
```

### Includes (Use Sparingly)

```csharp
// Only when you need related data
public async Task<Widget?> GetWithInstancesAsync(string key, CancellationToken ct)
{
    await using var context = _factory.CreateDbContext();
    return await context.Widgets
        .Include(w => w.Instances)
        .AsNoTracking()
        .FirstOrDefaultAsync(w => w.WidgetKey == key, ct);
}
```

## SQLite Resilience

```csharp
// Handle SQLITE_BUSY and SQLITE_LOCKED
public async Task<int> SaveChangesWithRetryAsync(
    DbContext context, CancellationToken ct, int maxRetries = 3)
{
    var delay = TimeSpan.FromMilliseconds(50);
    
    for (int attempt = 0; attempt <= maxRetries; attempt++)
    {
        try
        {
            return await context.SaveChangesAsync(ct);
        }
        catch (DbUpdateException ex) 
            when (ex.InnerException is SqliteException { SqliteErrorCode: 5 or 6 })
        {
            if (attempt == maxRetries) throw;
            
            Log.Warning("Database busy, retrying in {Delay}ms", delay.TotalMilliseconds);
            await Task.Delay(delay, ct);
            delay *= 2;  // Exponential backoff
        }
    }
    
    throw new InvalidOperationException("Should not reach here");
}
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Singleton DbContext | Concurrency issues, stale data | Factory pattern, context per operation |
| Missing AsNoTracking | Unnecessary memory, slower reads | Add AsNoTracking for read queries |
| ToList() in Where clause | Loads all data to memory | Keep query as IQueryable |
| N+1 queries | Multiple DB roundtrips | Use Include or projections |
| String interpolation in queries | SQL injection risk | Use parameterized queries |

## Testing

```csharp
public class WidgetRepositoryTests : IDisposable
{
    private readonly AppDbContext _context;
    private readonly WidgetRepository _repository;
    
    public WidgetRepositoryTests()
    {
        var options = new DbContextOptionsBuilder<AppDbContext>()
            .UseSqlite("DataSource=:memory:")
            .Options;
        
        _context = new AppDbContext(options);
        _context.Database.OpenConnection();
        _context.Database.EnsureCreated();
        
        var factory = new TestDbContextFactory(_context);
        _repository = new WidgetRepository(factory);
    }
    
    public void Dispose()
    {
        _context.Database.CloseConnection();
        _context.Dispose();
    }
}
```

## References

- `references/ef-core.md` for configuration and migrations
- `references/repositories-uow.md` for repository patterns
- [EF Core Performance](https://docs.microsoft.com/en-us/ef/core/performance/)
