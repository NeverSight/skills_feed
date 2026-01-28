---
name: java-microservices
description: Build microservices - Spring Cloud, service mesh, event-driven, resilience patterns
sasmp_version: "1.3.0"
version: "3.0.0"
bonded_agent: 07-java-microservices
bond_type: PRIMARY_BOND
allowed-tools: Read, Write, Bash, Glob, Grep

# Parameter Validation
parameters:
  pattern:
    type: string
    enum: [saga, cqrs, event_sourcing, api_gateway]
    description: Architecture pattern
  messaging:
    type: string
    enum: [kafka, rabbitmq, redis]
    description: Messaging platform
---

# Java Microservices Skill

Build production microservices with Spring Cloud and distributed system patterns.

## Overview

This skill covers microservices architecture with Spring Cloud including service discovery, API gateway, circuit breakers, event-driven communication, and distributed tracing.

## When to Use This Skill

Use when you need to:
- Design microservices architecture
- Implement service-to-service communication
- Configure resilience patterns
- Set up event-driven messaging
- Add distributed tracing

## Topics Covered

### Spring Cloud Components
- Config Server (centralized config)
- Service Discovery (Eureka, Consul)
- API Gateway (Spring Cloud Gateway)
- Load Balancing (Spring Cloud LoadBalancer)

### Resilience Patterns
- Circuit Breaker (Resilience4j)
- Retry with backoff
- Bulkhead isolation
- Rate limiting

### Event-Driven Architecture
- Apache Kafka integration
- Spring Cloud Stream
- Saga pattern
- Event sourcing basics

### Observability
- Distributed tracing (Micrometer)
- Metrics (Prometheus)
- Log correlation

## Quick Reference

```java
// Saga with Choreography
@Component
public class OrderSagaListener {

    @KafkaListener(topics = "order.created")
    public void handleOrderCreated(OrderCreatedEvent event) {
        inventoryService.reserve(event.getItems());
    }

    @KafkaListener(topics = "payment.failed")
    public void handlePaymentFailed(PaymentFailedEvent event) {
        // Compensating transaction
        inventoryService.release(event.getOrderId());
        orderService.cancel(event.getOrderId());
    }
}

// Circuit Breaker Configuration
@Configuration
public class ResilienceConfig {

    @Bean
    public Customizer<Resilience4JCircuitBreakerFactory> cbCustomizer() {
        return factory -> factory.configureDefault(id ->
            new Resilience4JConfigBuilder(id)
                .circuitBreakerConfig(CircuitBreakerConfig.custom()
                    .failureRateThreshold(50)
                    .waitDurationInOpenState(Duration.ofSeconds(30))
                    .slidingWindowSize(10)
                    .build())
                .build());
    }
}

// API Gateway Routes
@Configuration
public class GatewayConfig {

    @Bean
    public RouteLocator routes(RouteLocatorBuilder builder) {
        return builder.routes()
            .route("orders", r -> r
                .path("/api/orders/**")
                .filters(f -> f
                    .stripPrefix(1)
                    .circuitBreaker(c -> c.setName("order-cb"))
                    .retry(retry -> retry.setRetries(3)))
                .uri("lb://order-service"))
            .build();
    }
}
```

## Observability Configuration

```yaml
management:
  tracing:
    sampling:
      probability: 1.0
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus

logging:
  pattern:
    level: "%5p [${spring.application.name:},%X{traceId:-},%X{spanId:-}]"
```

## Common Patterns

### Saga Pattern
```
Order → Inventory → Payment → (Success | Compensate)
```

### Circuit Breaker States
```
CLOSED → (failures exceed threshold) → OPEN
OPEN → (wait duration) → HALF_OPEN
HALF_OPEN → (success) → CLOSED
HALF_OPEN → (failure) → OPEN
```

## Troubleshooting

### Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| Cascade failure | No circuit breaker | Add Resilience4j |
| Message lost | No ack | Enable manual ack |
| Inconsistent data | No compensation | Implement saga |
| Service not found | Discovery delay | Tune heartbeat |

### Debug Checklist
```
□ Trace request (traceId)
□ Check circuit breaker state
□ Verify Kafka consumer lag
□ Review gateway routes
□ Monitor retry counts
```

## Usage

```
Skill("java-microservices")
```

## Related Skills
- `java-spring-boot` - Spring Cloud
- `java-docker` - Containerization
