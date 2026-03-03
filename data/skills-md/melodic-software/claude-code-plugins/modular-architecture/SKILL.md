---
name: modular-architecture
description: Module organization patterns including ports and adapters (hexagonal), module communication, and data isolation. Use when structuring modular monoliths, defining module boundaries, setting up inter-module communication, or isolating database contexts. Includes MediatR patterns for internal events.
allowed-tools: Read, Write, Glob, Grep, Skill
---

# Modular Architecture

## When to Use This Skill

Use this skill when you need to:

- Structure a modular monolith application
- Define boundaries between modules (bounded contexts)
- Set up inter-module communication patterns
- Implement ports and adapters (hexagonal) architecture
- Isolate database contexts between modules
- Configure MediatR for internal domain events

**Keywords:** modular monolith, modules, bounded contexts, ports and adapters, hexagonal architecture, module communication, data isolation, separate DbContext, MediatR, domain events, internal events, module boundaries

## Module Structure Pattern

### Core Principle

Organize code by **modules (business capabilities)**, not layers. Each module is a self-contained vertical slice with its own:

- Domain entities and value objects
- Application services and handlers
- Infrastructure implementations
- Data transfer objects for external communication

### Standard Module Layout

```text
src/
├── Modules/
│   ├── Ordering/
│   │   ├── Ordering.Core/           # Domain + Application
│   │   │   ├── Domain/              # Entities, Value Objects, Events
│   │   │   ├── Application/         # Commands, Queries, Handlers
│   │   │   └── Ports/               # Interfaces (driven/driving)
│   │   ├── Ordering.Infrastructure/ # External dependencies
│   │   │   ├── Persistence/         # EF Core, DbContext
│   │   │   └── Adapters/            # External service implementations
│   │   └── Ordering.DataTransfer/   # DTOs for module-to-module communication
│   ├── Inventory/
│   │   ├── Inventory.Core/
│   │   ├── Inventory.Infrastructure/
│   │   └── Inventory.DataTransfer/
│   └── Shared/                      # Truly shared kernel (minimal)
│       └── Shared.Kernel/           # Common value objects, interfaces
└── Host/                            # Composition root, startup
    └── Api/                         # Controllers, middleware
```

### Key Principles

1. **No cross-module domain references** - Modules cannot reference each other's Core projects
2. **DataTransfer for communication** - Use DTOs to pass data between modules
3. **Infrastructure stays internal** - Each module owns its persistence
4. **Minimal shared kernel** - Only truly universal concepts go in Shared

## Ports and Adapters (Hexagonal) Pattern

The hexagonal architecture separates business logic from external concerns through ports (interfaces) and adapters (implementations).

**Detailed guide:** See `references/ports-adapters-guide.md`

### Quick Reference

```text
┌─────────────────────────────────────────────────────────────┐
│                    DRIVING SIDE (Primary)                   │
│         Controllers, CLI, Message Handlers, Tests           │
│                           │                                 │
│                    ┌──────▼──────┐                          │
│                    │   PORTS     │  (Input interfaces)      │
│                    │ IOrderService│                         │
│                    └──────┬──────┘                          │
│                           │                                 │
│              ┌────────────▼────────────┐                    │
│              │      APPLICATION        │                    │
│              │    (Use Cases/Handlers) │                    │
│              └────────────┬────────────┘                    │
│                           │                                 │
│              ┌────────────▼────────────┐                    │
│              │        DOMAIN           │                    │
│              │  (Entities, Value Objs) │                    │
│              └────────────┬────────────┘                    │
│                           │                                 │
│                    ┌──────▼──────┐                          │
│                    │   PORTS     │  (Output interfaces)     │
│                    │IOrderRepository│                       │
│                    └──────┬──────┘                          │
│                           │                                 │
│                    DRIVEN SIDE (Secondary)                  │
│         Databases, External APIs, File Systems, Queues      │
└─────────────────────────────────────────────────────────────┘
```

**Driving Ports:** Interfaces the application exposes (implemented by the application)
**Driven Ports:** Interfaces the application needs (implemented by adapters)

## Module Communication

Modules must communicate without creating tight coupling. Two primary patterns:

**Detailed guide:** See `references/module-communication.md`

### Synchronous Communication (DataTransfer)

For query operations where immediate response is needed:

```csharp
// In Inventory module - needs to check product availability
public class CheckStockHandler
{
    private readonly IOrderingModuleApi _orderingApi;

    public async Task<StockStatus> Handle(CheckStockQuery query)
    {
        // Get order info through DataTransfer DTO
        var orderDto = await _orderingApi.GetOrderSummary(query.OrderId);
        // orderDto is from Ordering.DataTransfer project
    }
}
```

### Asynchronous Communication (MediatR Domain Events)

For state changes that other modules need to react to:

```csharp
// In Ordering module - publishes event after order is placed
public class PlaceOrderHandler
{
    private readonly IMediator _mediator;

    public async Task Handle(PlaceOrderCommand command)
    {
        // ... create order ...

        // Publish integration event (handled by other modules)
        await _mediator.Publish(new OrderPlacedIntegrationEvent(
            order.Id, order.Items.Select(i => i.ProductId)));
    }
}

// In Inventory module - handles the event
public class OrderPlacedHandler : INotificationHandler<OrderPlacedIntegrationEvent>
{
    public async Task Handle(OrderPlacedIntegrationEvent notification, CancellationToken ct)
    {
        // Reserve inventory for the order
        await _inventoryService.ReserveStock(notification.ProductIds);
    }
}
```

## Data Isolation Patterns

Each module should own its data to prevent tight coupling at the database level.

**Detailed guide:** See `references/data-patterns.md`

### Separate DbContext Per Module

```csharp
// Ordering module's DbContext
public class OrderingDbContext : DbContext
{
    public DbSet<Order> Orders { get; set; }
    public DbSet<OrderItem> OrderItems { get; set; }

    protected override void OnModelCreating(ModelBuilder builder)
    {
        // Only configure Ordering entities
        builder.ApplyConfigurationsFromAssembly(typeof(OrderingDbContext).Assembly);
    }
}

// Inventory module's DbContext
public class InventoryDbContext : DbContext
{
    public DbSet<Product> Products { get; set; }
    public DbSet<StockLevel> StockLevels { get; set; }
}
```

### Key Rules

1. **No foreign keys between modules** - Use IDs as value objects instead
2. **No shared tables** - Each module owns its tables completely
3. **Same database is acceptable** - Separate schema/prefix per module
4. **Eventual consistency** - Accept that cross-module data may be stale

## MediatR Integration

MediatR provides the messaging infrastructure for both in-module CQRS and cross-module integration events.

**Detailed guide:** See `references/mediatr-integration.md`

### Registration Pattern

```csharp
// In each module's registration
public static class OrderingModule
{
    public static IServiceCollection AddOrderingModule(this IServiceCollection services)
    {
        services.AddMediatR(cfg =>
            cfg.RegisterServicesFromAssembly(typeof(OrderingModule).Assembly));

        services.AddScoped<IOrderingModuleApi, OrderingModuleApi>();
        services.AddDbContext<OrderingDbContext>();

        return services;
    }
}
```

### Event Types

| Type | Scope | Use Case |
| --- | --- | --- |
| Domain Event | Within module | Aggregate state changes |
| Integration Event | Cross-module | Notify other modules of changes |

## Integration with Event Storming

This skill works with the `event-storming` skill for bounded context discovery:

1. **Event Storming** discovers bounded contexts and events
2. **Modular Architecture** implements those contexts as modules
3. Events become MediatR integration events
4. Context boundaries become module boundaries

**Workflow:**

```text
Event Storming (discover "what")
    ↓
Bounded Contexts identified
    ↓
Modular Architecture (implement "where")
    ↓
Module structure created
    ↓
Fitness Functions (enforce boundaries)
```

## Fitness Functions

Use the `fitness-functions` skill to enforce module boundaries:

- **No cross-module domain references**
- **DataTransfer project rules** (only DTOs)
- **Infrastructure isolation** (no leaking implementations)

## Quick Start Checklist

When starting a new modular monolith:

- [ ] Create Modules/ directory structure
- [ ] Define Shared.Kernel with minimal shared types
- [ ] Create per-module projects (Core, Infrastructure, DataTransfer)
- [ ] Configure separate DbContext per module
- [ ] Set up MediatR for domain/integration events
- [ ] Add architecture tests to enforce boundaries
- [ ] Document module APIs in DataTransfer projects

## References

- `references/ports-adapters-guide.md` - Detailed hexagonal architecture patterns
- `references/module-communication.md` - Sync and async communication patterns
- `references/data-patterns.md` - Database isolation strategies
- `references/mediatr-integration.md` - MediatR configuration and patterns

## Version History

- **v1.0.0** (2025-12-22): Initial release
  - Module structure patterns
  - Ports and adapters overview
  - Module communication (sync/async)
  - Data isolation patterns
  - MediatR integration
  - Event storming integration

---

## Last Updated

**Date:** 2025-12-22
**Model:** claude-opus-4-5-20251101
