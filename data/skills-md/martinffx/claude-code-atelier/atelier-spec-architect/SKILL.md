---
name: atelier-spec-architect
description: DDD and hexagonal architecture with functional core pattern. Use when designing features, modeling domains, breaking down tasks, or understanding component responsibilities.
user-invocable: false
---

# Architect Skill

Domain-Driven Design and hexagonal architecture with functional core pattern for feature design.

## Architecture Model

Unified view of functional core and effectful edge:

```
          Effectful Edge (IO)              Functional Core (Pure)
┌─────────────────────────────────┐    ┌──────────────────────────┐
│  Router    → request parsing    │    │  Service  → orchestration│
│  Consumer  → event handling     │───▶│  Entity   → domain rules │
│  Client    → external APIs      │    │            → validation  │
│  Producer  → event publishing   │◀───│            → transforms  │
│  Repository→ data persistence   │    │                          │
└─────────────────────────────────┘    └──────────────────────────┘
```

**Key Principle:** Business logic lives in the functional core (Service + Entity). IO operations live in the effectful edge. Core defines interfaces; edge implements them (dependency inversion).

## Functional Core

Pure, deterministic components containing all business logic.

### Service Layer

**Responsibility:** Orchestrate business operations, coordinate between entities and repositories.

**Characteristics:**
- Pure functions that take data and return results
- No IO operations (database, HTTP, file system)
- Calls repositories through interfaces (dependency injection)
- Composes entity operations into workflows
- Returns success/error results

**Example:**
```typescript
class OrderService {
  async createOrder(request: CreateOrderRequest): Promise<Result<Order>> {
    // Validate with entity
    const order = Order.fromRequest(request);
    const validation = order.validate();
    if (!validation.ok) return validation;

    // Check business rules
    const inventory = await this.inventoryRepo.checkAvailability(order.items);
    if (!inventory.available) return Err('Items not available');

    // Coordinate persistence
    await this.inventoryRepo.reserve(order.items);
    const saved = await this.orderRepo.save(order.toRecord());

    return Ok(Order.fromRecord(saved));
  }
}
```

### Entity Layer

**Responsibility:** Domain models, validation, business rules, data transformations.

**Characteristics:**
- Pure data structures with behavior
- All validation logic
- Data transformations (fromRequest, toRecord, toResponse)
- Business rules and invariants
- No IO, no framework dependencies

**Example:**
```typescript
class Order {
  constructor(
    public readonly id: string,
    public readonly customerId: string,
    public readonly items: OrderItem[],
    public readonly status: OrderStatus,
    public readonly total: number
  ) {}

  static fromRequest(req: CreateOrderRequest): Order {
    return new Order(
      generateId(),
      req.customerId,
      req.items.map(i => new OrderItem(i)),
      'pending',
      req.items.reduce((sum, i) => sum + i.price * i.quantity, 0)
    );
  }

  toRecord(): OrderRecord {
    return {
      id: this.id,
      customer_id: this.customerId,
      items: JSON.stringify(this.items),
      status: this.status,
      total: this.total
    };
  }

  validate(): Result<Order> {
    if (this.items.length === 0) {
      return Err('Order must have at least one item');
    }
    if (this.total < 0) {
      return Err('Order total cannot be negative');
    }
    return Ok(this);
  }

  canCancel(): boolean {
    return ['pending', 'confirmed'].includes(this.status);
  }
}
```

## Effectful Edge

IO-performing components that interact with the outside world.

### Router

**Responsibility:** HTTP request handling, parsing, response formatting.

**Characteristics:**
- Parses HTTP requests into domain types
- Calls service layer with parsed data
- Formats service results into HTTP responses
- Handles HTTP-specific concerns (status codes, headers)
- No business logic

**Example:**
```typescript
router.post('/orders', async (req, res) => {
  const result = await orderService.createOrder(req.body);

  if (result.ok) {
    res.status(201).json(result.value.toResponse());
  } else {
    res.status(400).json({ error: result.error });
  }
});
```

### Repository

**Responsibility:** Data persistence and retrieval.

**Characteristics:**
- Implements data access interface used by services
- Converts between domain entities and database records
- Handles database queries and transactions
- No business logic or validation

**Example:**
```typescript
class OrderRepository {
  async save(record: OrderRecord): Promise<OrderRecord> {
    return await db.orders.create(record);
  }

  async findById(id: string): Promise<OrderRecord | null> {
    return await db.orders.findOne({ id });
  }
}
```

## Component Matrix

Quick reference for where things belong:

| Concern | Component | Layer | Testability |
|---------|-----------|-------|-------------|
| Domain model | Entity | Core | Unit test (pure) |
| Validation | Entity | Core | Unit test (pure) |
| Business rules | Entity | Core | Unit test (pure) |
| Orchestration | Service | Core | Unit test (stub repos) |
| Data transforms | Entity | Core | Unit test (pure) |
| HTTP parsing | Router | Edge | Integration test |
| Data access | Repository | Edge | Integration test |
| External APIs | Client | Edge | Integration test |
| Event handling | Consumer | Edge | Integration test |
| Event publishing | Producer | Edge | Integration test |

## Task Breakdown

### Bottom-Up Dependency Ordering

Implementation order follows dependency chain:

```
1. Entity   → Domain models, validation, transforms
2. Repository → Data access interfaces and implementations
3. Service  → Business logic orchestration
4. Router   → HTTP endpoints
```

**Rationale:** Each layer depends on layers below. Can't implement service without entity, can't implement router without service.

### Task Granularity

**One task per layer:**
- Implement Order entity with validation
- Implement OrderRepository with data access
- Implement OrderService with business logic
- Implement order API endpoints

**For complex features, break down further:**
- Entity: Order, OrderItem, OrderStatus
- Repository: OrderRepository, InventoryRepository
- Service: OrderService, PaymentService
- Router: Order routes, Payment routes

## Architect → Testing Flow

Architectural decisions inform testing strategy:

```
Architect Outputs           →    Testing Inputs
────────────────────────────────────────────────
Component responsibilities  →    What to test
Layer boundaries           →    Where to test
Pure vs effectful          →    Unit vs integration
Entity transformations     →    Property-based tests
Service orchestration      →    Stub-driven tests
```

The testing skill uses architectural structure to determine:
- What gets unit tested (core) vs integration tested (edge)
- Where to place test boundaries
- What to stub and what to test for real
- What test cases validate business rules

## Reference Materials

For detailed patterns and examples:

- **See [references/ddd-patterns.md](references/ddd-patterns.md)** - Aggregates, Value Objects, Domain Events, Bounded Contexts, composition patterns
- **See [references/data-modeling.md](references/data-modeling.md)** - Entity design principles, schema patterns, access pattern optimization, data transformation
- **See [references/api-design.md](references/api-design.md)** - REST conventions, request/response contracts, error handling, versioning patterns
