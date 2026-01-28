---
name: architecture
description: Clean architecture patterns for the 3SC widget host. Defines layer boundaries, dependency rules, composition root patterns, and abstraction strategies.
---

# Architecture

## Overview

3SC follows Clean Architecture principles adapted for a WPF desktop application. This ensures testability, maintainability, and clear separation of concerns.

## Layer Structure

```
┌─────────────────────────────────────────────────────────────┐
│                        3SC.UI                               │
│  • WPF Views & Windows                                      │
│  • ViewModels (CommunityToolkit.Mvvm)                       │
│  • UI Services (Navigation, Dialogs)                        │
│  • Composition Root (ServiceLocator)                        │
├─────────────────────────────────────────────────────────────┤
│                    3SC.Application                          │
│  • Repository Interfaces                                    │
│  • Service Abstractions                                     │
│  • DTOs / Request-Response Models                           │
│  • Use Case Orchestration (future)                          │
├─────────────────────────────────────────────────────────────┤
│                   3SC.Infrastructure                        │
│  • EF Core DbContext & Repositories                         │
│  • External API Clients                                     │
│  • File System Operations                                   │
│  • Security Implementations                                 │
├─────────────────────────────────────────────────────────────┤
│                      3SC.Domain                             │
│  • Entities (Widget, Layout, etc.)                          │
│  • Value Objects (WidgetSize, WidgetPosition)               │
│  • Domain Rules & Validation                                │
│  • No External Dependencies                                 │
└─────────────────────────────────────────────────────────────┘
```

## Dependency Rules

| Layer | Can Reference | Cannot Reference |
|-------|---------------|------------------|
| Domain | Nothing | Everything else |
| Application | Domain | Infrastructure, UI |
| Infrastructure | Domain, Application | UI |
| UI | All layers | - |

## Definition of Done (DoD)

- [ ] New types are in the correct layer
- [ ] Domain has no external package references
- [ ] Infrastructure types implement Application interfaces
- [ ] ViewModels depend on interfaces, not implementations
- [ ] No circular dependencies between projects
- [ ] Composition happens only in ServiceLocator

## Composition Root Pattern

All dependencies are wired in `ServiceLocator.cs`:

```csharp
public sealed class ServiceLocator : IDisposable
{
    // Use Lazy<T> for deferred initialization
    private readonly Lazy<IWidgetRepository> _widgetRepository;
    
    private ServiceLocator()
    {
        // Wire dependencies in constructor
        _widgetRepository = new Lazy<IWidgetRepository>(() => 
            new WidgetRepository(DbContext));
    }
    
    public IWidgetRepository WidgetRepository => _widgetRepository.Value;
}
```

### Best Practices

1. **Register interfaces, not implementations**
2. **Use Lazy<T> for expensive services**
3. **Avoid service location in ViewModels** - inject via constructor
4. **Dispose resources properly** - implement IDisposable chain

## Abstraction Strategy

### When to Abstract

| Scenario | Abstract? | Example |
|----------|-----------|---------|
| External dependencies | ✅ Yes | File system, HTTP, time |
| Infrastructure concerns | ✅ Yes | Database, caching |
| Cross-cutting concerns | ✅ Yes | Logging, telemetry |
| Simple utilities | ❌ No | String helpers, math |
| Framework types | ❌ No | List<T>, Dictionary<K,V> |

### Required Abstractions

```csharp
// These MUST be abstracted for testability:
public interface IDateTimeProvider
{
    DateTimeOffset UtcNow { get; }
    DateTimeOffset Now { get; }
}

public interface IFileSystem
{
    bool FileExists(string path);
    bool DirectoryExists(string path);
    string[] GetFiles(string path, string searchPattern);
    string ReadAllText(string path);
    void WriteAllText(string path, string content);
    Stream OpenRead(string path);
}

public interface IEnvironmentProvider
{
    string GetFolderPath(Environment.SpecialFolder folder);
    string MachineName { get; }
    string UserName { get; }
}
```

## Cross-Cutting Concerns

### Logging
- Inject `ILogger<T>` via constructor
- Use structured logging with Serilog
- Include correlation IDs for request tracing

### Validation
- Domain validation in entities (guard clauses)
- Input validation in ViewModels (ObservableValidator)
- API validation in Infrastructure (data annotations)

### Error Handling
- Domain: Throw domain exceptions
- Application: Catch and translate to results
- Infrastructure: Wrap external errors
- UI: Display user-friendly messages

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Service Locator in VMs | Hidden dependencies, hard to test | Constructor injection |
| Static dependencies | Global state, race conditions | Instance methods, DI |
| God classes | Too many responsibilities | Single Responsibility |
| Leaky abstractions | Infrastructure in domain | Clean interfaces |
| Anemic domain | Logic outside entities | Rich domain model |

## Project References

```
3SC.UI
├── 3SC.Application
├── 3SC.Infrastructure  
└── 3SC.Domain

3SC.Application
└── 3SC.Domain

3SC.Infrastructure
├── 3SC.Application
└── 3SC.Domain

3SC.Domain
└── (no references)
```

## Testing Strategy

- **Domain**: Unit tests, no mocks needed
- **Application**: Unit tests with mocked interfaces
- **Infrastructure**: Integration tests with test database
- **UI/ViewModels**: Unit tests with mocked services

## References

- [Clean Architecture by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Dependency Injection in .NET](https://docs.microsoft.com/en-us/dotnet/core/extensions/dependency-injection)
