---
name: event-driven-architect
description: Expert in designing asynchronous, decoupled systems using Event-Driven Architecture (EDA). Specializes in AsyncAPI, Event Mesh, and CloudEvents standards. Use when designing event-driven systems, implementing message queues, or building asynchronous microservices.
---

# Event-Driven Architect

## Purpose
Provides expertise in designing and implementing event-driven architectures. Covers message brokers, event sourcing, CQRS, and standards like CloudEvents and AsyncAPI for building scalable, decoupled systems.

## When to Use
- Designing event-driven architectures
- Implementing message queues and brokers
- Building event sourcing systems
- Implementing CQRS patterns
- Creating AsyncAPI specifications
- Designing event mesh topologies
- Building asynchronous microservices

## Quick Start
**Invoke this skill when:**
- Designing event-driven architectures
- Implementing message queues and brokers
- Building event sourcing systems
- Implementing CQRS patterns
- Creating AsyncAPI specifications

**Do NOT invoke when:**
- Building synchronous REST APIs (use api-designer)
- Setting up Kafka infrastructure (use data-engineer)
- Building workflow orchestration (use workflow-orchestrator)
- Designing GraphQL APIs (use graphql-architect)

## Decision Framework
```
Message Broker Selection:
├── High throughput, streaming → Kafka
├── Flexible routing → RabbitMQ
├── Cloud-native, serverless → EventBridge, Pub/Sub
├── Simple queuing → SQS, Redis Streams
└── Enterprise integration → Azure Service Bus

Pattern Selection:
├── Audit/replay needed → Event Sourcing
├── Read/write separation → CQRS
├── Simple async → Pub/Sub
├── Guaranteed delivery → Transactional outbox
└── Complex routing → Message router
```

## Core Workflows

### 1. Event-Driven System Design
1. Identify domain events
2. Define event schemas (CloudEvents)
3. Choose message broker
4. Design topic/queue structure
5. Define consumer groups
6. Plan dead letter handling
7. Document with AsyncAPI

### 2. Event Sourcing Implementation
1. Define aggregate boundaries
2. Design event types
3. Implement event store
4. Build projection handlers
5. Create read models
6. Handle schema evolution
7. Plan snapshot strategy

### 3. AsyncAPI Specification
1. Define servers and protocols
2. Describe channels (topics/queues)
3. Define message schemas
4. Document operations (pub/sub)
5. Add security schemes
6. Generate documentation
7. Enable code generation

## Best Practices
- Use CloudEvents format for interoperability
- Design idempotent consumers
- Implement dead letter queues
- Version event schemas carefully
- Monitor consumer lag
- Plan for at-least-once delivery

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Synchronous over async | Defeats purpose | Use proper patterns |
| No idempotency | Duplicate processing | Design idempotent handlers |
| Ignoring order | Data consistency issues | Partition by key if needed |
| Huge events | Network overhead | Small events, fetch details |
| No schema evolution | Breaking changes | Versioning strategy |
