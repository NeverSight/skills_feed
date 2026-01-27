---
name: microservices-architect
description: Distributed systems expert specializing in service decomposition, orchestration, and microservices architecture patterns. Use when designing microservices, defining service boundaries, implementing service mesh, or handling distributed system challenges. Triggers include "microservices", "service mesh", "service decomposition", "distributed systems", "API gateway", "event-driven".
---

# Microservices Architect

## Purpose
Provides expertise in designing and implementing microservices architectures. Specializes in service decomposition, inter-service communication patterns, service mesh implementation, and solving distributed systems challenges.

## When to Use
- Decomposing monoliths into microservices
- Defining service boundaries and APIs
- Implementing service mesh (Istio, Linkerd)
- Designing API gateway patterns
- Handling distributed transactions (Saga pattern)
- Implementing event-driven communication
- Setting up service discovery and load balancing
- Designing for resilience (circuit breakers, retries)

## Quick Start
**Invoke this skill when:**
- Designing microservices from scratch
- Decomposing existing monoliths
- Implementing service-to-service communication
- Setting up service mesh or API gateway
- Solving distributed system challenges

**Do NOT invoke when:**
- Migrating legacy systems incrementally → use `/legacy-modernizer`
- Event streaming architecture → use `/event-driven-architect`
- Kubernetes operations → use `/kubernetes-specialist`
- Single service API design → use `/api-designer`

## Decision Framework
```
Communication Pattern?
├── Synchronous
│   ├── Simple calls → REST/gRPC
│   └── Complex routing → API Gateway
├── Asynchronous
│   ├── Events → Kafka/RabbitMQ
│   └── Commands → Message queues
└── Distributed Transaction
    ├── Strong consistency → Saga (orchestration)
    └── Eventual consistency → Saga (choreography)
```

## Core Workflows

### 1. Service Decomposition
1. Identify bounded contexts from domain model
2. Define service responsibilities (single purpose)
3. Design APIs for each service
4. Determine data ownership per service
5. Plan inter-service communication
6. Define deployment strategy

### 2. Service Mesh Implementation
1. Select mesh (Istio, Linkerd, Consul)
2. Deploy sidecar proxies
3. Configure traffic management
4. Implement mTLS for security
5. Set up observability (tracing, metrics)
6. Define retry and circuit breaker policies

### 3. Saga Pattern Implementation
1. Identify distributed transaction boundaries
2. Choose orchestration vs choreography
3. Define compensating transactions
4. Implement saga coordinator (if orchestrated)
5. Handle failure scenarios
6. Add monitoring for saga status

## Best Practices
- Design services around business capabilities, not technical layers
- Own your data—each service manages its own database
- Use asynchronous communication for loose coupling
- Implement circuit breakers for fault tolerance
- Design for failure—everything will fail eventually
- Use correlation IDs for distributed tracing

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Distributed monolith | Coupled services, worst of both | True bounded contexts |
| Shared database | Tight coupling | Database per service |
| Synchronous chains | Cascading failures | Async where possible |
| No circuit breakers | Cascading failures | Implement Hystrix/Resilience4j |
| Nano-services | Operational overhead | Right-sized services |
