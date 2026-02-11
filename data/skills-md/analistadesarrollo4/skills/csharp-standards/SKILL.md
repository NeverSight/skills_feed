---
name: csharp-standards
description: "C# 12 and .NET 10 coding standards: modern syntax, type safety, immutability, DI patterns, and record types. Use when writing or modifying any C# source file."
---

# C# Code Standards (.NET 10 / C# 12)

Target `.NET 10` exclusively. Leverage modern C# 12 features for cleaner, safer, and more expressive code.

## Quick Reference

| Element | Target | C# Version |
|---------|--------|------------|
| **Framework** | `net10.0` | C# 12 |
| **IDE** | Visual Studio 2022 (latest) | - |
| **Nullable** | Enabled | Required |

## Core Principles (ALWAYS Apply)

### Type Safety

**MUST:**
- Declare types explicitly (use `var` only when type is obvious: `var list = new List<int>()`)
- Enable nullable reference types
- Use `?` for nullable references: `string?`, `User?`
- Use `??` and `?.` operators appropriately

```csharp
// ✅ Type is obvious
var numbers = new List<int> { 1, 2, 3 };
var message = "Clear string";

// ❌ Type unclear
var user = GetUser(); // What type?
var result = Calculate(); // What type?
```

### Immutability

**MUST:**
- Use `record` for DTOs, Commands, Queries, Events
- Use `init` properties (not `set`) for immutable data
- Use `private set` only for controlled mutations
- Default to `internal sealed` classes

```csharp
// ✅ Records for data transfer
public record CreateUserCommand(string Email, string FullName, int Age) : IRequest<Guid>;
public record UserDto(Guid Id, string Email, string FullName);

// ✅ Controlled mutability
public class Order
{
    public Guid Id { get; init; }
    public OrderStatus Status { get; private set; }
    
    public void ChangeStatus(OrderStatus newStatus) => Status = newStatus;
}
```

### Dependency Injection

**MUST:**
- Use primary constructors for all dependency injection
- Inject interfaces, not concrete types

```csharp
public class OrderService(
    IOrderRepository repository,
    ILogger<OrderService> logger)
{
    public async Task<Order> GetAsync(Guid id)
    {
        logger.LogInformation("Fetching {OrderId}", id);
        return await repository.GetByIdAsync(id);
    }
}
```

## When to Read References

**Need modern C# 12 features?**  
→ Read [references/modern-features.md](references/modern-features.md) for:
- Primary constructors
- Collection expressions `[1, 2, 3]`
- Raw string literals `"""`
- Required properties
- Pattern matching
- Using declarations

**Working with async/await or LINQ?**  
→ Read [references/async-patterns.md](references/async-patterns.md) for:
- Async/await best practices
- CancellationToken usage
- ConfigureAwait
- LINQ optimization (AsNoTracking, projections, filtering)
- Exception handling in async code

**Questions about code style, formatting, or organization?**  
→ Read [references/code-style.md](references/code-style.md) for:
- Naming conventions
- File organization (file-scoped namespaces, using directives)
- Code formatting (Allman braces, spacing, indentation)
- Comments and documentation
- Security (never log PII, sanitize inputs)
- Member order

## Critical Rules (NEVER Violate)

### Async Operations

**MUST:**
- Use `async`/`await` for ALL I/O (database, HTTP, file system)
- Include `CancellationToken` parameter
- Use `.AsNoTracking()` for EF Core read-only queries

**NEVER:**
- Use `.Result`, `.Wait()`, or `.GetAwaiter().GetResult()` (deadlock risk)

```csharp
// ✅ Async with CancellationToken
public async Task<User?> GetUserAsync(Guid id, CancellationToken ct = default)
{
    return await _context.Users
        .AsNoTracking()
        .FirstOrDefaultAsync(u => u.Id == id, ct);
}

// ❌ Blocking call
var user = GetUserAsync(id).Result; // Deadlock risk
```

### Security

**NEVER:**
- Log sensitive data (PII, credentials, tokens)
- Use string concatenation for SQL queries
- Catch generic `Exception` (use specific exceptions)

```csharp
// ✅ Safe logging
_logger.LogInformation("Login attempt for user");

// ❌ NEVER log sensitive data
_logger.LogInformation("Password: {Password}", pwd);
```

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Classes/Records/Methods/Properties | PascalCase | `OrderService`, `GetUser()`, `UserId` |
| Parameters/Variables | camelCase | `userId`, `customerEmail` |
| Private Fields | _camelCase | `_logger`, `_repository` |
| Async Methods | Verb + "Async" | `GetUserAsync()`, `ProcessAsync()` |

## File Organization

**MUST:**
- Use file-scoped namespaces (no braces)
- Place `using` directives at top of file
- One class per file (filename = classname)

```csharp
using Microsoft.EntityFrameworkCore;
using MyCompany.Orders.Domain;

namespace MyCompany.Orders.Application;

public record CreateOrderCommand(Guid CustomerId, List<OrderLine> Lines) : IRequest<Guid>;
```