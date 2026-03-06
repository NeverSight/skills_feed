---
name: backend
description: Design APIs, microservices, and database schemas. Use for server-side development, API design, or system architecture.
---

# Backend Architecture

Design scalable, reliable backend systems and APIs.

## When to Use

- Creating new APIs or services
- Database schema design
- Service architecture decisions
- Performance optimization
- API versioning and documentation

## Focus Areas

### API Design

- RESTful conventions
- Consistent error responses
- Proper HTTP methods and status codes
- Versioning strategy (URL or header)
- Rate limiting and throttling

### Service Boundaries

- Single responsibility per service
- Clear contracts between services
- Async communication where appropriate
- Circuit breakers for resilience

### Database Design

- Normalized schemas (3NF default)
- Appropriate indexes
- Migration strategy
- Connection pooling

### Security

- Authentication (JWT, OAuth2)
- Authorization (RBAC, ABAC)
- Input validation
- SQL injection prevention

## API Response Template

```json
{
  "data": { ... },
  "meta": {
    "page": 1,
    "total": 100
  },
  "errors": null
}
```

## Error Response Template

```json
{
  "data": null,
  "errors": [
    {
      "code": "VALIDATION_ERROR",
      "message": "Email is required",
      "field": "email"
    }
  ]
}
```

## Reliability Targets

- Uptime: 99.9%
- Error rate: <0.1%
- Response time: <200ms p95

## Examples

**Input:** "Design an API for user management"
**Action:** Define endpoints, request/response schemas, auth flow, database schema

**Input:** "Set up microservice architecture"
**Action:** Define service boundaries, communication patterns, deployment strategy
