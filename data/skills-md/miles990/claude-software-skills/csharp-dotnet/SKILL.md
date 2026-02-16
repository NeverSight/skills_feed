---
name: csharp-dotnet
description: C# and .NET development patterns
domain: programming-languages
version: 1.0.0
tags: [csharp, dotnet, async, linq, aspnet]
triggers:
  keywords:
    primary: [csharp, c#, dotnet, .net, aspnet, asp.net, nuget]
    secondary: [linq, async, entity framework, ef core, blazor, maui]
  context_boost: [enterprise, windows, azure, backend, game, unity]
  context_penalty: [python, javascript, java, go]
  priority: high
---

# C# & .NET

## Overview

Modern C# and .NET development patterns including async programming, LINQ, and ASP.NET Core.

---

## Modern C# Features

### Records and Init-Only Properties

```csharp
// Record type (immutable by default)
public record User(
    string Id,
    string Email,
    string Name,
    DateTime CreatedAt
);

// With-expressions for immutable updates
var user = new User("1", "test@example.com", "Test User", DateTime.UtcNow);
var updated = user with { Name = "Updated Name" };

// Record with validation
public record ValidatedUser
{
    public required string Id { get; init; }
    public required string Email { get; init; }
    public required string Name { get; init; }

    public ValidatedUser()
    {
        // Validation in constructor
    }

    // Custom validation
    public static ValidatedUser Create(string email, string name)
    {
        if (!email.Contains("@"))
            throw new ArgumentException("Invalid email");

        return new ValidatedUser
        {
            Id = Guid.NewGuid().ToString(),
            Email = email,
            Name = name
        };
    }
}

// Init-only properties
public class Config
{
    public required string ConnectionString { get; init; }
    public int Timeout { get; init; } = 30;
}
```

### Pattern Matching

```csharp
// Type patterns
public string Describe(object obj) => obj switch
{
    string s => $"String of length {s.Length}",
    int i when i > 0 => $"Positive integer: {i}",
    int i => $"Non-positive integer: {i}",
    IEnumerable<int> list => $"Integer list with {list.Count()} items",
    null => "Null value",
    _ => "Unknown type"
};

// Property patterns
public decimal CalculateDiscount(Order order) => order switch
{
    { Total: > 1000, Customer.IsPremium: true } => order.Total * 0.2m,
    { Total: > 1000 } => order.Total * 0.1m,
    { Customer.IsPremium: true } => order.Total * 0.05m,
    _ => 0
};

// List patterns (C# 11)
public string DescribeList(int[] numbers) => numbers switch
{
    [] => "Empty",
    [var single] => $"Single element: {single}",
    [var first, var second] => $"Two elements: {first}, {second}",
    [var first, .. var middle, var last] => $"First: {first}, Last: {last}, Middle count: {middle.Length}",
};

// Positional patterns with deconstruct
public record Point(int X, int Y);

public string Quadrant(Point point) => point switch
{
    (0, 0) => "Origin",
    (> 0, > 0) => "First quadrant",
    (< 0, > 0) => "Second quadrant",
    (< 0, < 0) => "Third quadrant",
    (> 0, < 0) => "Fourth quadrant",
    (_, 0) or (0, _) => "On an axis"
};
```

### Nullable Reference Types

```csharp
#nullable enable

public class UserService
{
    // Non-nullable (compiler ensures not null)
    public User GetUser(string id)
    {
        return _repository.Find(id)
            ?? throw new NotFoundException($"User {id} not found");
    }

    // Nullable return
    public User? FindUser(string id)
    {
        return _repository.Find(id);
    }

    // Null handling
    public string GetDisplayName(User? user)
    {
        // Null-conditional
        var name = user?.Name;

        // Null-coalescing
        return user?.Name ?? "Anonymous";

        // Null-coalescing assignment
        // user ??= CreateDefaultUser();
    }

    // Null-forgiving operator (use sparingly)
    public void ProcessUser(User? user)
    {
        // When you know it's not null but compiler doesn't
        var name = user!.Name;
    }
}

// Required members (C# 11)
public class RequiredUser
{
    public required string Id { get; init; }
    public required string Email { get; init; }
    public string? Nickname { get; init; }
}
```

---

## Async Programming

```csharp
using System.Threading.Tasks;
using System.Threading;

public class AsyncService
{
    // Basic async method
    public async Task<User> GetUserAsync(string id, CancellationToken ct = default)
    {
        var response = await _httpClient.GetAsync($"/users/{id}", ct);
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<User>(ct)
            ?? throw new InvalidOperationException("Null response");
    }

    // Parallel execution
    public async Task<IReadOnlyList<User>> GetUsersAsync(IEnumerable<string> ids)
    {
        var tasks = ids.Select(id => GetUserAsync(id));
        return await Task.WhenAll(tasks);
    }

    // With error handling
    public async Task<Result<User>> SafeGetUserAsync(string id)
    {
        try
        {
            var user = await GetUserAsync(id);
            return Result<User>.Success(user);
        }
        catch (Exception ex)
        {
            return Result<User>.Failure(ex.Message);
        }
    }

    // ValueTask for potentially synchronous operations
    public ValueTask<User?> GetCachedUserAsync(string id)
    {
        if (_cache.TryGetValue(id, out var user))
        {
            return ValueTask.FromResult<User?>(user);
        }

        return new ValueTask<User?>(FetchAndCacheUserAsync(id));
    }

    // Async enumerable (IAsyncEnumerable)
    public async IAsyncEnumerable<User> StreamUsersAsync(
        [EnumeratorCancellation] CancellationToken ct = default)
    {
        var page = 1;
        while (true)
        {
            var users = await FetchPageAsync(page, ct);
            if (!users.Any()) yield break;

            foreach (var user in users)
            {
                yield return user;
            }
            page++;
        }
    }

    // Consuming async enumerable
    public async Task ProcessAllUsersAsync()
    {
        await foreach (var user in StreamUsersAsync())
        {
            await ProcessUserAsync(user);
        }
    }
}

// Channels for producer-consumer
public class ChannelExample
{
    private readonly Channel<Message> _channel = Channel.CreateBounded<Message>(100);

    public async Task ProduceAsync(Message message)
    {
        await _channel.Writer.WriteAsync(message);
    }

    public async Task ConsumeAsync(CancellationToken ct)
    {
        await foreach (var message in _channel.Reader.ReadAllAsync(ct))
        {
            await ProcessMessageAsync(message);
        }
    }
}
```

---

## LINQ

```csharp
using System.Linq;

public class LinqExamples
{
    // Query syntax
    public IEnumerable<User> GetActiveUsers(IEnumerable<User> users)
    {
        return from user in users
               where user.IsActive
               orderby user.Name
               select user;
    }

    // Method syntax (more common)
    public IEnumerable<string> GetActiveUserEmails(IEnumerable<User> users)
    {
        return users
            .Where(u => u.IsActive)
            .OrderBy(u => u.Name)
            .Select(u => u.Email);
    }

    // Grouping
    public IDictionary<string, List<User>> GroupByDomain(IEnumerable<User> users)
    {
        return users
            .GroupBy(u => u.Email.Split('@')[1])
            .ToDictionary(g => g.Key, g => g.ToList());
    }

    // Join
    public IEnumerable<OrderWithUser> JoinOrdersWithUsers(
        IEnumerable<Order> orders,
        IEnumerable<User> users)
    {
        return orders.Join(
            users,
            order => order.UserId,
            user => user.Id,
            (order, user) => new OrderWithUser(order, user));
    }

    // Aggregate
    public OrderStats GetOrderStats(IEnumerable<Order> orders)
    {
        return new OrderStats(
            Count: orders.Count(),
            Total: orders.Sum(o => o.Amount),
            Average: orders.Average(o => o.Amount),
            Max: orders.Max(o => o.Amount)
        );
    }

    // SelectMany (flatten)
    public IEnumerable<OrderItem> GetAllItems(IEnumerable<Order> orders)
    {
        return orders.SelectMany(o => o.Items);
    }

    // Complex pipeline
    public IEnumerable<UserSummary> GetTopCustomers(
        IEnumerable<User> users,
        IEnumerable<Order> orders)
    {
        return orders
            .GroupBy(o => o.UserId)
            .Select(g => new
            {
                UserId = g.Key,
                TotalSpent = g.Sum(o => o.Amount),
                OrderCount = g.Count()
            })
            .OrderByDescending(x => x.TotalSpent)
            .Take(10)
            .Join(users, x => x.UserId, u => u.Id, (x, u) => new UserSummary(
                u.Name,
                x.TotalSpent,
                x.OrderCount
            ));
    }
}
```

---

## Dependency Injection

```csharp
using Microsoft.Extensions.DependencyInjection;

// Service registration
public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddApplicationServices(this IServiceCollection services)
    {
        // Transient - new instance each time
        services.AddTransient<IEmailService, EmailService>();

        // Scoped - one per request
        services.AddScoped<IUserRepository, UserRepository>();

        // Singleton - one instance for app lifetime
        services.AddSingleton<ICacheService, RedisCacheService>();

        // Factory registration
        services.AddScoped<IDbConnection>(sp =>
        {
            var config = sp.GetRequiredService<IConfiguration>();
            return new SqlConnection(config.GetConnectionString("Default"));
        });

        // Options pattern
        services.Configure<EmailOptions>(configuration.GetSection("Email"));

        return services;
    }
}

// Constructor injection
public class UserService
{
    private readonly IUserRepository _repository;
    private readonly IEmailService _emailService;
    private readonly ILogger<UserService> _logger;

    public UserService(
        IUserRepository repository,
        IEmailService emailService,
        ILogger<UserService> logger)
    {
        _repository = repository;
        _emailService = emailService;
        _logger = logger;
    }

    public async Task<User> CreateUserAsync(CreateUserRequest request)
    {
        _logger.LogInformation("Creating user {Email}", request.Email);

        var user = new User(request.Email, request.Name);
        await _repository.AddAsync(user);
        await _emailService.SendWelcomeEmailAsync(user);

        return user;
    }
}

// Primary constructor (C# 12)
public class UserServiceNew(
    IUserRepository repository,
    IEmailService emailService,
    ILogger<UserServiceNew> logger)
{
    public async Task<User> CreateUserAsync(CreateUserRequest request)
    {
        logger.LogInformation("Creating user {Email}", request.Email);
        // Use repository, emailService directly
        return null!;
    }
}
```

---

## Generic Patterns

```csharp
// Generic repository
public interface IRepository<T> where T : class, IEntity
{
    Task<T?> FindAsync(string id);
    Task<IReadOnlyList<T>> FindAllAsync();
    Task AddAsync(T entity);
    Task UpdateAsync(T entity);
    Task DeleteAsync(string id);
}

public class Repository<T> : IRepository<T> where T : class, IEntity
{
    private readonly DbContext _context;

    public Repository(DbContext context)
    {
        _context = context;
    }

    public async Task<T?> FindAsync(string id)
    {
        return await _context.Set<T>().FindAsync(id);
    }

    public async Task<IReadOnlyList<T>> FindAllAsync()
    {
        return await _context.Set<T>().ToListAsync();
    }

    public async Task AddAsync(T entity)
    {
        await _context.Set<T>().AddAsync(entity);
        await _context.SaveChangesAsync();
    }

    // ...
}

// Generic constraints
public class Service<TEntity, TId>
    where TEntity : class, IEntity<TId>, new()
    where TId : struct
{
    // ...
}

// Covariance and contravariance
public interface IProducer<out T>
{
    T Produce();
}

public interface IConsumer<in T>
{
    void Consume(T item);
}
```

---

## Error Handling

```csharp
// Result type pattern
public readonly struct Result<T>
{
    public T? Value { get; }
    public string? Error { get; }
    public bool IsSuccess => Error is null;

    private Result(T value)
    {
        Value = value;
        Error = null;
    }

    private Result(string error)
    {
        Value = default;
        Error = error;
    }

    public static Result<T> Success(T value) => new(value);
    public static Result<T> Failure(string error) => new(error);

    public TResult Match<TResult>(
        Func<T, TResult> success,
        Func<string, TResult> failure) =>
        IsSuccess ? success(Value!) : failure(Error!);
}

// Custom exceptions
public class DomainException : Exception
{
    public string Code { get; }

    public DomainException(string code, string message)
        : base(message)
    {
        Code = code;
    }
}

public class ValidationException : DomainException
{
    public IDictionary<string, string[]> Errors { get; }

    public ValidationException(IDictionary<string, string[]> errors)
        : base("VALIDATION_ERROR", "Validation failed")
    {
        Errors = errors;
    }
}

// Exception filter middleware
public class ExceptionMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<ExceptionMiddleware> _logger;

    public async Task InvokeAsync(HttpContext context)
    {
        try
        {
            await _next(context);
        }
        catch (ValidationException ex)
        {
            context.Response.StatusCode = 400;
            await context.Response.WriteAsJsonAsync(new { ex.Code, ex.Errors });
        }
        catch (NotFoundException ex)
        {
            context.Response.StatusCode = 404;
            await context.Response.WriteAsJsonAsync(new { ex.Code, ex.Message });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Unhandled exception");
            context.Response.StatusCode = 500;
            await context.Response.WriteAsJsonAsync(new { Code = "INTERNAL_ERROR" });
        }
    }
}
```

---

## Related Skills

- [[backend]] - ASP.NET Core development
- [[database]] - Entity Framework Core
- [[testing]] - xUnit, NUnit
