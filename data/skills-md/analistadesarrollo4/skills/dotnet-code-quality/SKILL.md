---
name: dotnet-code-quality
description: "Code quality standards, optimization, and SonarQube compliance for .NET applications. Use when: (1) Reviewing or refactoring code for complexity (cyclomatic complexity > 10-15), (2) Optimizing EF Core queries with AsNoTracking for read-only operations, (3) Implementing caching strategies (memory cache, Redis), (4) Ensuring SonarQube/SonarCloud rule compliance, (5) Applying SOLID principles and clean code practices, (6) Performance optimization questions, or (7) Evaluating code smells and maintainability issues."
---

# Code Quality Standards

## Critical Rules (MUST Follow)

### Cyclomatic Complexity

**MUST:**
- Immediately refactor any method with complexity > **10-15**
- Break down complex methods into smaller, focused methods
- Use early returns to reduce nesting
- Extract complex conditions into well-named methods

**For refactoring examples:**  
→ See [references/refactoring-examples.md](references/refactoring-examples.md)

### Entity Framework Core

**MUST:**
- Use `AsNoTracking()` for **ALL** read-only queries
- Use projections (`Select`) to fetch only needed fields
- Implement pagination for large datasets
- Use eager loading (`Include`) to avoid N+1 queries

```csharp
// ✅ Optimized read-only query
var users = await _context.Users
    .AsNoTracking()
    .Where(u => u.IsActive)
    .Select(u => new UserDto { Id = u.Id, Name = u.Name })
    .ToListAsync();

// ❌ Performance issues
var users = await _context.Users // Tracking enabled
    .Where(u => u.IsActive)
    .ToListAsync(); // Fetches all columns
```

### Security

**NEVER:**
- Log sensitive data (PII, passwords, tokens)
- Use string concatenation for SQL queries
- Deploy with outdated dependencies

**MUST:**
- Validate all user input
- Use parameterized queries (EF Core does this automatically)
- Implement proper authentication/authorization

## SonarQube Integration

- Code must comply with **SonarQube/SonarCloud** rules
- Integrate with CI/CD for automatic analysis  
- Maintain passing quality gates for production
- Configure analyzers in `.editorconfig`

```ini
[*.cs]
dotnet_diagnostic.CA1806.severity = warning
dotnet_diagnostic.S1541.severity = warning # Complexity warning
```

## Caching Strategies

Implement caching for frequently accessed, rarely changing data.

```csharp
public class CachedUserService(IMemoryCache cache, IUserRepository repository)
{
    public async Task<User> GetUserAsync(int userId)
    {
        var cacheKey = $"user_{userId}";
        
        if (!cache.TryGetValue(cacheKey, out User user))
        {
            user = await repository.GetByIdAsync(userId);
            
            var options = new MemoryCacheEntryOptions()
                .SetSlidingExpiration(TimeSpan.FromMinutes(5))
                .SetAbsoluteExpiration(TimeSpan.FromHours(1));
            
            cache.Set(cacheKey, user, options);
        }
        
        return user;
    }
}
```

**Consider:**
- Distributed caching (Redis) for multi-instance deployments
- Appropriate cache expiration policies
- Cache invalidation strategies

## SOLID Principles

- **Single Responsibility**: One class, one reason to change
- **Open/Closed**: Open for extension, closed for modification
- **Liskov Substitution**: Subtypes must be substitutable for base types
- **Interface Segregation**: Many specific interfaces over one general
- **Dependency Inversion**: Depend on abstractions, not concretions

## Code Smells to Avoid

- God objects (large classes doing too much)
- Long methods (> 20-30 lines)
- Long parameter lists (> 3-4 parameters)
- Duplicate code
- Dead code
- Feature envy (excessive coupling)

**For God Class refactoring examples:**  
→ See [references/refactoring-examples.md](references/refactoring-examples.md#god-class-refactoring)

## Performance Considerations

- Use `StringBuilder` for string concatenation in loops
- Use `ValueTask<T>` for frequently called async methods
- Use `struct` for small, immutable types
- Avoid unnecessary boxing/unboxing
- Profile before optimizing (avoid premature optimization)

## Health Checks

- **Omit during initial setup**: Do not implement health checks initially
- Add health checks when application matures and requires monitoring
