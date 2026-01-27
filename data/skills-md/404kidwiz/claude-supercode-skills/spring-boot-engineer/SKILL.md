---
name: spring-boot-engineer
description: Expert in Spring Boot 3+, Microservices, and Cloud-Native Java. Specializes in Virtual Threads, Spring Cloud, and Reactive Stack.
---

# Spring Boot Engineer

## Purpose
Provides expertise in building production-grade Java applications with Spring Boot 3+. Specializes in microservices architecture, cloud-native patterns, reactive programming, and leveraging modern Java features including virtual threads.

## When to Use
- Building Spring Boot applications and microservices
- Implementing REST APIs with Spring Web or WebFlux
- Configuring Spring Security for authentication/authorization
- Setting up Spring Data JPA, MongoDB, or R2DBC
- Implementing Spring Cloud patterns (Config, Gateway, Circuit Breaker)
- Using virtual threads with Spring Boot 3.2+
- Building reactive applications with Project Reactor
- Integrating messaging with Spring Kafka or RabbitMQ

## Quick Start
**Invoke this skill when:**
- Building Spring Boot applications and microservices
- Implementing REST APIs with Spring Web or WebFlux
- Configuring Spring Security for authentication/authorization
- Setting up Spring Data repositories
- Implementing Spring Cloud patterns

**Do NOT invoke when:**
- General Java questions without Spring → use java-architect
- Kubernetes deployment → use kubernetes-specialist
- Database design → use database-administrator
- Frontend development → use appropriate frontend skill

## Decision Framework
```
Spring Boot Task?
├── API Development → Spring Web (blocking) vs WebFlux (reactive)
├── Data Access → JPA (relational) vs MongoDB (document) vs R2DBC (reactive)
├── Security → OAuth2/OIDC vs JWT vs Basic Auth
├── Messaging → Kafka (high throughput) vs RabbitMQ (routing)
├── Service Communication → REST vs gRPC vs messaging
└── Configuration → Spring Cloud Config vs Kubernetes ConfigMaps
```

## Core Workflows

### 1. Microservice Development
1. Initialize project with Spring Initializr and required starters
2. Define domain model and DTOs
3. Implement repository layer with Spring Data
4. Create service layer with business logic
5. Build REST controllers with proper error handling
6. Add validation, security, and observability
7. Write tests at unit, integration, and contract levels
8. Configure for cloud deployment (health, metrics, config)

### 2. Spring Security Configuration
1. Add spring-boot-starter-security dependency
2. Define security filter chain configuration
3. Configure authentication provider (JWT, OAuth2, LDAP)
4. Set up authorization rules for endpoints
5. Implement custom UserDetailsService if needed
6. Add CORS and CSRF configuration
7. Test security configuration thoroughly

### 3. Reactive Application Development
1. Use WebFlux instead of Spring Web
2. Configure R2DBC for reactive database access
3. Return Mono/Flux from controllers and services
4. Use WebClient for non-blocking HTTP calls
5. Implement backpressure handling
6. Test with StepVerifier
7. Monitor with reactive-aware observability

## Best Practices
- Use constructor injection over field injection
- Externalize configuration with profiles and ConfigMaps
- Implement proper exception handling with @ControllerAdvice
- Enable Actuator endpoints for health and metrics
- Use Testcontainers for integration tests
- Leverage virtual threads for I/O-bound workloads (Spring Boot 3.2+)

## Anti-Patterns
- **Field injection** → Use constructor injection for testability
- **Blocking in reactive chains** → Keep reactive pipeline non-blocking
- **Catching generic exceptions** → Handle specific exceptions appropriately
- **Hardcoded configuration** → Externalize with environment variables
- **Missing health checks** → Always expose Actuator health endpoint
