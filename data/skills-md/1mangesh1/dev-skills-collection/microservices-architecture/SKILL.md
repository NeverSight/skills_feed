---
name: microservices-architecture
description: Microservices architecture patterns and design. Use when user asks to "design microservices", "service decomposition", "API gateway", "distributed transactions", "circuit breaker", "service mesh", "event-driven architecture", "saga pattern", "service discovery", or mentions microservices design patterns and distributed systems.
---

# Microservices Architecture

Patterns and best practices for designing and implementing microservices architectures.

## Core Patterns

### Service Decomposition
- Domain-driven design (bounded contexts)
- Business capability based
- Ownership clarity
- Technology diversity

### API Gateway Pattern
```
Client → API Gateway → Service 1
                    → Service 2
                    → Service 3
```
- Single entry point
- Authentication/authorization
- Request routing
- Rate limiting

### Database per Service
- Each service owns its database
- Data consistency challenges
- Enables technology diversity

### Event-Driven Communication
```
Service A → Event Bus → Service B
           → Service C
```
- Loose coupling
- Eventual consistency
- Event sourcing

## Reliability Patterns

### Circuit Breaker
```javascript
// Fails fast when service is unavailable
const breaker = new CircuitBreaker(async () => {
  return await serviceCall();
}, {
  threshold: 5,        // Fail after 5 errors
  timeout: 60000       // Check after 60s
});
```

### Retry Logic
```javascript
// Exponential backoff
const maxRetries = 3;
const baseDelay = 1000;
for (let i = 0; i < maxRetries; i++) {
  try {
    return await service.call();
  } catch (e) {
    if (i === maxRetries - 1) throw e;
    await sleep(baseDelay * Math.pow(2, i));
  }
}
```

### Timeout Management
- Set reasonable timeouts
- Cascading timeout calculation
- Fail fast strategy

## Consistency Patterns

### Two-Phase Commit (2PC)
- Synchronous, strong consistency
- Blocking, reduced availability
- Use sparingly

### Saga Pattern
```
Transaction 1: Service A
  ↓ success
Transaction 2: Service B
  ↓ success
Transaction 3: Service C
  ↓ failure → Compensating transactions
```
- Long-running transactions
- Eventual consistency
- Compensating actions on failure

### Event Sourcing
- Append-only event log
- Reconstible state
- Audit trail built-in

## Monitoring & Operations

### Distributed Tracing
- Correlate requests across services
- Identify latency bottlenecks
- Tools: Jaeger, Zipkin

### Logging
- Structured logging with correlation IDs
- Centralized log aggregation
- Tools: ELK, Splunk

### Metrics
- Per-service metrics
- Request latency, throughput
- Resource usage

## Service Mesh

### Istio/Linkerd
- Manages service-to-service communication
- Traffic management
- Security policies
- Observability

## Configuration Management

```yaml
# Environment-specific config
app:
  database:
    url: ${DB_URL}
    timeout: ${DB_TIMEOUT:-5000}
  cache:
    ttl: ${CACHE_TTL:-3600}
  security:
    jwtSecret: ${JWT_SECRET}
```

## Deployment Strategies

### Blue-Green Deployment
- Two identical environments
- Switch traffic instantly
- Quick rollback

### Canary Deployment
- Gradual rollout to subset of users
- Monitor metrics
- Expand if successful

### Rolling Deployment
- Gradual replacement of old instances
- No downtime
- Longer deploy time

## API Design for Microservices

- RESTful or gRPC
- Versioning strategy
- Backward compatibility
- Documentation (OpenAPI)

## Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| Distributed transactions | Saga pattern, event sourcing |
| Data consistency | Eventual consistency acceptance |
| Service discovery | Service registry (Consul, Eureka) |
| Latency | Caching, async communication |
| Debugging | Distributed tracing, correlation IDs |
| Complexity | API gateway, service mesh |

## Team Organization

- Cross-functional teams per service
- Clear API contracts
- Ownership and accountability
- Communication patterns

## References

- Sam Newman - Building Microservices
- Chris Richardson - Microservices Patterns
- Kubernetes in Action
- AWS Microservices Architecture
- Kong API Gateway Guide
