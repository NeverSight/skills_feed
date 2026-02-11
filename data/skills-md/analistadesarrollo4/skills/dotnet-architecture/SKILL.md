---
name: dotnet-architecture
description: "DDD and CQRS architecture for .NET solutions: domain modeling (entities, aggregates, value objects), CQRS patterns (commands/queries with MediatR), layer boundaries, and infrastructure composition. Use when: (1) Designing domain models or aggregate boundaries, (2) Implementing commands, queries, or handlers, (3) Questions about entities vs value objects vs domain services, (4) Structuring layers (Domain, Application, Infrastructure, Presentation), (5) Setting up DI with extension methods in Infrastructure/Extensions, (6) Creating AddPersistence, AddRepositories, AddServices, AddExternalServices, AddConfigurations, or AddKeyVault methods, or (7) Organizing Program.cs composition."
---

# .NET Architecture (DDD/CQRS)

Architecture using Domain-Driven Design (DDD) and CQRS patterns for clean, maintainable solutions.

## Core Architectural Patterns

### Domain-Driven Design (DDD)

Structure code around the business domain, not technical concerns.

- **Focus on domain first:** Design models that reflect business semantics, not database structures.
- **Ubiquitous Language:** Use business terminology consistently.
- **Bounded Contexts:** Partition system into logical domains with clear boundaries.

**For detailed guidance on Entities, Aggregates, Value Objects, Domain Services, and lifecycle patterns:**
→ See [references/ddd-concepts.md](references/ddd-concepts.md)

### CQRS (Command Query Responsibility Segregation)

Separate read and write operations at the architectural level.

- **Commands:** Represent intent to change state → Return void or result object.
- **Queries:** Request data with no side effects → Return DTOs.
- **Orchestration:** Use **MediatR** to dispatch commands and queries to handlers.

**For detailed command/query patterns, handler examples, and DTOs:**
→ See [references/cqrs-patterns.md](references/cqrs-patterns.md)

## Layer Architecture

Four distinct layers with clear responsibilities:

### Domain Layer

Pure business logic, no infrastructure dependencies.

- Contains: Entities, Aggregates, Value Objects, Domain Services.
- No I/O, database access, or external calls.
- Encapsulates business rules and aggregate consistency.

```csharp
public class Order // Aggregate Root
{
    public Guid OrderId { get; private set; }
    private readonly List<OrderLine> _lines = new();
    
    public void AddLine(Product product, int quantity)
    {
        if (Status != OrderStatus.Pending)
            throw new InvalidOperationException();
        _lines.Add(new OrderLine(product, quantity));
    }
}
```

### Application Layer

Orchestration and command/query handling.

- Contains: Command/Query Handlers (CQRS).
- Defines interfaces (repositories, external services).
- Contains DTOs and mapping logic.
- Handlers are thin; delegate to Domain.

```csharp
public record CreateOrderCommand(Guid CustomerId, List<OrderLineDto> Lines) : IRequest<Guid>;

public class CreateOrderCommandHandler : IRequestHandler<CreateOrderCommand, Guid>
{
    public async Task<Guid> Handle(CreateOrderCommand command, CancellationToken ct)
    {
        var order = Order.CreateNew(customer, orderLines);
        await _orderRepository.AddAsync(order, ct);
        await _unitOfWork.SaveChangesAsync(ct);
        return order.OrderId;
    }
}
```

### Infrastructure Layer

Technical concerns and external integrations.

- Implements repositories and external service interfaces.
- Handles database persistence (EF Core).
- Manages external integrations (APIs, brokers, caching).
- Configures DI composition via extension methods.

### Presentation Layer (API)

HTTP entry/exit points.

- Controllers receive requests and delegate to MediatR.
- No business logic in controllers.
- Return DTOs, not domain models.
- Handle HTTP concerns: routing, versioning, error responses.

```csharp
[ApiController]
[Route("api/[controller]")]
public class OrdersController : ControllerBase
{
    private readonly IMediator _mediator;
    
    [HttpPost]
    public async Task<IActionResult> CreateOrder(CreateOrderCommand command)
    {
        var orderId = await _mediator.Send(command);
        return CreatedAtAction(nameof(GetOrder), new { id = orderId }, orderId);
    }
}
```

## Quick Reference

### When to Use Each DDD Concept

- **Entity:** Object with unique identity (User, Order, Product).
- **Value Object:** Immutable object defined by attributes (Money, Email, Address).
- **Aggregate:** Cluster of objects with a root entity (Order with OrderLines).
- **Domain Service:** Logic spanning multiple aggregates or too complex for one entity.

### CQRS Guidelines

- **Commands:** Use imperative verbs (`CreateOrderCommand`, `CancelOrderCommand`).
- **Queries:** Use nouns (`GetOrderByIdQuery`, `ListOrdersQuery`).
- **DTOs:** Never expose domain models directly to clients.
- **AsNoTracking:** Always use for queries to optimize performance.

```csharp
// Query example with AsNoTracking
var orders = await _context.Orders
    .AsNoTracking()
    .Where(o => o.CustomerId == customerId)
    .Select(o => new OrderDto(o.OrderId, o.Status, o.Total))
    .ToListAsync();
```

## Infrastructure Composition

Organize DI configuration using extension methods in `Infrastructure/Extensions`.

### Required Extension Methods

Create these in separate files under `Infrastructure/Extensions`:

1. **AddPersistence** - Database context and Unit of Work
2. **AddRepositories** - All repository implementations
3. **AddServices** - Domain and application services
4. **AddExternalServices** - HTTP clients, RabbitMQ, Redis, etc.
5. **AddConfigurations** - Configuration objects as singletons
6. **AddKeyVault** (IConfigurationBuilder) - Azure Key Vault setup

### Program.cs Example

```csharp
var builder = WebApplication.CreateBuilder(args);

// Configure Key Vault
builder.Configuration.AddAzureKeyVault(builder.Configuration);

// Add services via extension methods
builder.Services.AddPersistence(builder.Configuration);
builder.Services.AddRepositories();
builder.Services.AddServices();
builder.Services.AddExternalServices(builder.Configuration);
builder.Services.AddConfigurations(builder.Configuration);

// Add MediatR
builder.Services.AddMediatR(cfg => 
    cfg.RegisterServicesFromAssembly(typeof(Program).Assembly));

builder.Services.AddControllers();

var app = builder.Build();
app.MapControllers();
app.Run();
```

**For complete extension method implementations with examples:**
→ See [references/infrastructure-composition.md](references/infrastructure-composition.md)

## Best Practices

### Domain Layer

- Keep domain pure; no infrastructure dependencies.
- Enforce invariants within aggregates.
- Use value objects to make implicit concepts explicit.
- Keep aggregates focused and reasonably sized.

### Application Layer

- Keep handlers thin; complex logic belongs in domain.
- Use Unit of Work for transactional consistency.
- Validate commands but enforce business rules in domain.
- Map domain models to DTOs for external consumption.

### Infrastructure Layer

- Use extension methods for clean DI composition.
- Prioritize environment variables over appsettings for secrets.
- Validate required configuration at startup.
- Use Polly for resilience (retries, circuit breakers).

### CQRS

- Separate command and query concerns strictly.
- Optimize queries with projections and AsNoTracking.
- Return identifiers from commands, not full objects.
- Use DTOs as contracts between layers.
