---
name: architecture-patterns
description: Software architecture patterns and best practices
domain: software-design
version: 1.0.0
tags: [architecture, microservices, monolithic, event-driven, serverless, ddd]
triggers:
  keywords:
    primary: [architecture, microservices, monolith, serverless, event-driven, ddd]
    secondary: [hexagonal, clean architecture, cqrs, saga, domain driven, modular]
  context_boost: [design, structure, enterprise, scale]
  context_penalty: [frontend, css, ui]
  priority: high
---

# Architecture Patterns

## Overview

Architecture patterns provide proven solutions for structuring software systems. Choosing the right architecture is crucial for scalability, maintainability, and team productivity.

## Patterns

### Monolithic Architecture

**Description**: Single deployable unit containing all application functionality.

**Key Features**:
- Simple deployment and development
- Shared database and memory
- Straightforward debugging

**Use Cases**:
- MVPs and startups
- Small teams (< 10 developers)
- Simple domain logic

**Best Practices**:
```
src/
├── modules/          # Feature-based organization
│   ├── users/
│   ├── orders/
│   └── products/
├── shared/           # Cross-cutting concerns
└── infrastructure/   # External services
```

---

### Microservices Architecture

**Description**: Distributed system of independently deployable services.

**Key Features**:
- Independent deployment and scaling
- Technology diversity per service
- Fault isolation

**Use Cases**:
- Large teams needing autonomy
- Complex domains with clear boundaries
- High scalability requirements

**Key Components**:
| Component | Purpose | Tools |
|-----------|---------|-------|
| API Gateway | Entry point, routing | Kong, AWS API Gateway |
| Service Discovery | Service registration | Consul, Kubernetes DNS |
| Config Management | Centralized config | Spring Cloud Config, Consul |
| Circuit Breaker | Fault tolerance | Resilience4j, Hystrix |

**Best Practices**:
1. Design around business capabilities
2. Decentralize data management
3. Design for failure
4. Automate deployment

---

### Event-Driven Architecture

**Description**: Systems communicating through events.

**Key Patterns**:

| Pattern | Description | Use Case |
|---------|-------------|----------|
| Event Sourcing | Store state as events | Audit trails, temporal queries |
| CQRS | Separate read/write models | High-read workloads |
| Saga | Distributed transactions | Cross-service workflows |

**Event Sourcing Example**:
```typescript
// Events are the source of truth
interface OrderEvent {
  id: string;
  type: 'OrderCreated' | 'ItemAdded' | 'OrderShipped';
  timestamp: Date;
  payload: unknown;
}

// Rebuild state from events
function rebuildOrder(events: OrderEvent[]): Order {
  return events.reduce((order, event) => {
    switch (event.type) {
      case 'OrderCreated': return { ...event.payload };
      case 'ItemAdded': return { ...order, items: [...order.items, event.payload] };
      case 'OrderShipped': return { ...order, status: 'shipped' };
    }
  }, {} as Order);
}
```

---

### Serverless Architecture

**Description**: Cloud-managed execution without server management.

**Key Features**:
- Pay-per-execution pricing
- Auto-scaling to zero
- Reduced operational overhead

**Considerations**:
| Aspect | Impact |
|--------|--------|
| Cold Start | 100ms-2s latency on first invocation |
| Timeout | Usually 15-30 min max execution |
| State | Must use external storage |
| Vendor Lock-in | Platform-specific features |

**Best Practices**:
1. Keep functions small and focused
2. Minimize dependencies
3. Use connection pooling for databases
4. Implement proper error handling

---

### Clean Architecture

**Description**: Dependency-inverted architecture with domain at center.

**Layer Structure**:
```
┌──────────────────────────────────────┐
│           Frameworks & Drivers       │  ← External (DB, Web, UI)
├──────────────────────────────────────┤
│           Interface Adapters         │  ← Controllers, Gateways
├──────────────────────────────────────┤
│           Application Business       │  ← Use Cases
├──────────────────────────────────────┤
│           Enterprise Business        │  ← Entities, Domain Rules
└──────────────────────────────────────┘
```

**Dependency Rule**: Dependencies point inward. Inner layers know nothing about outer layers.

---

### Domain-Driven Design (DDD)

**Description**: Architecture aligned with business domain.

**Strategic Patterns**:
| Pattern | Purpose |
|---------|---------|
| Bounded Context | Clear domain boundaries |
| Context Map | Relationships between contexts |
| Ubiquitous Language | Shared vocabulary |

**Tactical Patterns**:
| Pattern | Purpose |
|---------|---------|
| Entity | Objects with identity |
| Value Object | Immutable descriptors |
| Aggregate | Consistency boundary |
| Repository | Collection-like persistence |
| Domain Event | Something that happened |

---

## Decision Guide

```
START
  │
  ├─ Team size < 10? ──────────────────→ Monolith
  │
  ├─ Need independent deployments? ────→ Microservices
  │
  ├─ Audit trail required? ────────────→ Event Sourcing
  │
  ├─ Variable/unpredictable load? ─────→ Serverless
  │
  ├─ Complex business logic? ──────────→ Clean Architecture + DDD
  │
  └─ Default ──────────────────────────→ Modular Monolith
```

## Common Pitfalls

### 1. Premature Microservices
**Problem**: Starting with microservices for a simple application
**Solution**: Start monolithic, extract services when boundaries are clear

### 2. Distributed Monolith
**Problem**: Microservices that must deploy together
**Solution**: Ensure services are truly independent with clear API contracts

### 3. Ignoring Data Boundaries
**Problem**: Shared database across services
**Solution**: Each service owns its data, use events for synchronization

---

### Hexagonal Architecture (Ports & Adapters)

**Description**: Application core isolated from external concerns through ports (interfaces) and adapters (implementations).

**Structure**:
```
┌─────────────────────────────────────────────────────────────┐
│                      Driving Adapters                       │
│    (REST API, CLI, GraphQL, Message Consumer)               │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    Input Ports                              │
│              (Use Case Interfaces)                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                   APPLICATION CORE                          │
│              (Domain Logic, Entities)                       │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                   Output Ports                              │
│           (Repository, Gateway Interfaces)                  │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                     Driven Adapters                         │
│    (Database, External APIs, Message Publisher)             │
└─────────────────────────────────────────────────────────────┘
```

**TypeScript Example**:
```typescript
// Port (Interface)
interface OrderRepository {
  save(order: Order): Promise<void>;
  findById(id: string): Promise<Order | null>;
}

// Adapter (Implementation)
class PostgresOrderRepository implements OrderRepository {
  constructor(private db: Database) {}

  async save(order: Order): Promise<void> {
    await this.db.query('INSERT INTO orders...', [order]);
  }

  async findById(id: string): Promise<Order | null> {
    const row = await this.db.query('SELECT * FROM orders WHERE id = $1', [id]);
    return row ? this.toDomain(row) : null;
  }
}

// Use Case (Application Core)
class CreateOrderUseCase {
  constructor(private orderRepo: OrderRepository) {} // Depends on Port, not Adapter

  async execute(input: CreateOrderInput): Promise<Order> {
    const order = new Order(input);
    await this.orderRepo.save(order);
    return order;
  }
}
```

**Benefits**:
- Easy to swap implementations (DB, external services)
- Highly testable (mock ports)
- Framework-agnostic domain logic

---

### Modular Monolith

**Description**: Monolith with strict module boundaries, preparing for potential microservices extraction.

**Key Features**:
- Modules communicate via defined interfaces
- Each module owns its data
- Can be deployed as single unit or extracted

**Structure**:
```
src/
├── modules/
│   ├── users/
│   │   ├── api/           # Public API of module
│   │   │   └── UserService.ts
│   │   ├── internal/      # Private implementation
│   │   │   ├── UserRepository.ts
│   │   │   └── UserEntity.ts
│   │   └── index.ts       # Only exports public API
│   ├── orders/
│   │   ├── api/
│   │   │   └── OrderService.ts
│   │   ├── internal/
│   │   └── index.ts
│   └── shared/            # Cross-cutting utilities
├── infrastructure/
│   ├── database/
│   ├── messaging/
│   └── http/
└── main.ts
```

**Module Communication Rules**:
```typescript
// ✅ Good: Use public API
import { UserService } from '@modules/users';
const user = await userService.getById(id);

// ❌ Bad: Direct access to internal
import { UserRepository } from '@modules/users/internal/UserRepository';
```

**Enforcement**:
```json
// eslint rules or ts-paths to prevent internal imports
{
  "rules": {
    "no-restricted-imports": ["error", {
      "patterns": ["@modules/*/internal/*"]
    }]
  }
}
```

---

### Strangler Fig Pattern

**Description**: Gradually replace legacy system by routing traffic to new implementation.

**Migration Process**:
```
Phase 1: Facade
┌─────────┐     ┌─────────┐     ┌─────────────┐
│ Client  │────→│ Facade  │────→│ Legacy      │
└─────────┘     └─────────┘     │ System      │
                                └─────────────┘

Phase 2: Partial Migration
┌─────────┐     ┌─────────┐     ┌─────────────┐
│ Client  │────→│ Facade  │──┬─→│ Legacy      │
└─────────┘     └─────────┘  │  └─────────────┘
                             │  ┌─────────────┐
                             └─→│ New System  │
                                └─────────────┘

Phase 3: Complete Migration
┌─────────┐     ┌─────────┐     ┌─────────────┐
│ Client  │────→│ Facade  │────→│ New System  │
└─────────┘     └─────────┘     └─────────────┘
```

**Implementation**:
```typescript
class PaymentFacade {
  constructor(
    private legacyPayment: LegacyPaymentService,
    private newPayment: NewPaymentService,
    private featureFlags: FeatureFlags
  ) {}

  async processPayment(payment: Payment): Promise<Result> {
    // Gradually migrate traffic
    if (this.featureFlags.isEnabled('new-payment-system', payment.userId)) {
      return this.newPayment.process(payment);
    }
    return this.legacyPayment.process(payment);
  }
}
```

---

### Backend for Frontend (BFF)

**Description**: Dedicated backend for each frontend type (web, mobile, etc.).

**Structure**:
```
                    ┌─────────────┐
                    │ Web Client  │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Web BFF    │
                    └──────┬──────┘
                           │
       ┌───────────────────┼───────────────────┐
       │                   │                   │
┌──────▼──────┐    ┌──────▼──────┐    ┌──────▼──────┐
│ User Service│    │Order Service│    │Product Svc  │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                    ┌──────▼──────┐
                    │ Mobile BFF  │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │Mobile Client│
                    └─────────────┘
```

**Benefits**:
- Optimized payload for each client
- Client-specific authentication
- Independent deployment per frontend
- Reduces over-fetching

**When to Use**:
| Scenario | Recommendation |
|----------|----------------|
| Single client type | Skip BFF |
| Web + Mobile with same needs | Single API Gateway |
| Different UX per platform | Separate BFFs |
| Multiple teams per frontend | Dedicated BFFs |

---

## Architecture Patterns Comparison

| Pattern | Complexity | Scalability | Team Size | Best For |
|---------|------------|-------------|-----------|----------|
| Monolith | Low | Vertical | Small (2-10) | MVPs, Simple apps |
| Modular Monolith | Medium | Vertical | Medium (5-20) | Growing apps |
| Microservices | High | Horizontal | Large (20+) | Complex domains |
| Serverless | Medium | Auto | Any | Event-driven, Variable load |
| Event-Driven | High | Horizontal | Medium-Large | Async workflows |

---

## Architecture Decision Record (ADR) Template

When choosing an architecture, document decisions:

```markdown
# ADR-001: Choose Modular Monolith

## Status
Accepted

## Context
- Team of 8 developers
- MVP deadline in 3 months
- Uncertain about domain boundaries
- Limited DevOps resources

## Decision
Adopt Modular Monolith with strict boundaries

## Consequences
### Positive
- Faster initial development
- Simpler deployment
- Can extract services later

### Negative
- Single point of failure
- Scaling limited to vertical
- Need discipline for module boundaries

## Alternatives Considered
1. Microservices - Too complex for team size
2. Traditional Monolith - No path to scale
```

---

## Evolution Path

```
┌─────────────────────────────────────────────────────────────────┐
│                    Architecture Evolution                        │
│                                                                 │
│   Monolith ──→ Modular Monolith ──→ Microservices              │
│      │              │                     │                     │
│      │              │                     ▼                     │
│      │              │            Event-Driven / CQRS            │
│      │              │                     │                     │
│      ▼              ▼                     ▼                     │
│  [Simple]     [Growing]            [Complex/Scale]              │
│                                                                 │
│   Tip: Don't skip steps. Each stage teaches domain boundaries. │
└─────────────────────────────────────────────────────────────────┘
```

---

## Anti-Patterns to Avoid

### 1. Big Ball of Mud
**Symptom**: No clear structure, everything depends on everything
**Fix**: Introduce module boundaries, apply Clean Architecture principles

### 2. Golden Hammer
**Symptom**: Using same architecture for every project
**Fix**: Evaluate requirements, use decision guide

### 3. Accidental Complexity
**Symptom**: Architecture more complex than domain requires
**Fix**: Start simple, add complexity only when needed

### 4. Resume-Driven Development
**Symptom**: Choosing tech for learning, not solving problems
**Fix**: Align architecture with team skills and project needs

### 5. Vendor Lock-In
**Symptom**: Core logic tightly coupled to cloud provider
**Fix**: Use Hexagonal Architecture, abstract vendor-specific code

---

## Performance Considerations by Pattern

| Pattern | Latency | Throughput | Cold Start |
|---------|---------|------------|------------|
| Monolith | Low | High | N/A |
| Microservices | Medium (network) | High (distributed) | N/A |
| Serverless | Variable | Auto-scale | 100ms-2s |
| Event-Driven | Higher (async) | Very High | Depends |

---

## Testing Strategies by Pattern

### Monolith
```
Unit Tests → Integration Tests → E2E Tests
    70%           20%              10%
```

### Microservices
```
Unit Tests → Contract Tests → Integration → E2E
    60%           20%           15%         5%

// Contract Test Example (Pact)
const provider = new Pact({ consumer: 'OrderService', provider: 'UserService' });
await provider.addInteraction({
  state: 'user exists',
  uponReceiving: 'get user request',
  withRequest: { method: 'GET', path: '/users/123' },
  willRespondWith: { status: 200, body: { id: '123', name: 'John' } }
});
```

### Event-Driven
- Test event producers and consumers independently
- Use event schema validation
- Test saga/workflow orchestration

---

## Related Skills

- [[api-design]] - API design for service communication
- [[system-design]] - Large-scale system considerations
- [[devops-cicd]] - Deployment strategies for each pattern
- [[data-design]] - Database patterns for each architecture
