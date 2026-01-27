---
name: backend-developer
description: Comprehensive backend development for building production-ready server-side applications with multiple frameworks, databases, and deployment strategies. Use when building APIs, services, databases, or server infrastructure.
---

# Backend Developer Skill

## Purpose

Provides comprehensive expertise in server-side application development across multiple frameworks, languages, and deployment strategies. Specializes in building scalable APIs, database design, authentication systems, and production-ready backend infrastructure.

## When to Use

- Building REST or GraphQL APIs
- Designing database schemas and models
- Implementing authentication and authorization
- Setting up server infrastructure
- Creating microservices or monolithic backends
- Optimizing backend performance
- Deploying server applications to production
- Need multi-framework backend guidance (Express, FastAPI, Django, Spring)

## Quick Start

**Invoke this skill when:**
- Building server-side APIs (REST, GraphQL) in Node.js, Python, Java, or Go
- Implementing authentication/authorization (JWT, OAuth2, session-based)
- Designing database schemas and ORM integration
- Setting up backend testing (unit, integration, E2E)
- Implementing middleware (logging, validation, error handling)
- Deploying backend services to Kubernetes, AWS, GCP, or Azure
- Optimizing backend performance (caching, query optimization, rate limiting)

**Do NOT invoke when:**
- Only frontend development needed → Use frontend-developer or nextjs-developer
- Database-specific optimization required → Use database-optimizer or postgres-pro
- API design without implementation → Use api-designer
- GraphQL-specific architecture → Use graphql-architect
- DevOps/infrastructure only → Use devops-engineer or cloud-architect

## Framework Support

### Node.js/TypeScript
- Express.js, NestJS, Koa.js, Fastify

### Python
- FastAPI, Django, Flask, Tornado

### Java
- Spring Boot, Quarkus, Micronaut

### Go
- Gin, Echo, Fiber

## Decision Framework

### Backend Framework Selection

```
Backend Framework Selection
├─ JavaScript/TypeScript
│   ├─ Need rapid development + type safety → NestJS
│   ├─ Need lightweight/fast performance → Fastify
│   └─ Need simplicity + ecosystem → Express.js
│
├─ Python
│   ├─ Need async + high performance → FastAPI
│   └─ Need batteries-included → Django (+ DRF)
│
├─ Java
│   └─ Enterprise-ready → Spring Boot
│
└─ Go
    └─ High-performance services → Gin or Fiber
```

### Authentication Strategy Matrix

| Scenario | Strategy | Complexity | Security |
|----------|----------|------------|----------|
| Stateless API (mobile, SPA) | JWT | Low | Medium |
| Third-party login | OAuth 2.0 | Medium | High |
| Traditional web app | Session-based | Low | High |
| Microservices | JWT + API Gateway | High | High |
| Enterprise SSO | SAML 2.0 | High | Very High |

### Database & ORM Selection

```
Database & ORM Decision
├─ Relational (SQL)
│   ├─ Node.js/TypeScript
│   │   ├─ Need type safety + migrations → Prisma
│   │   └─ Need flexibility → TypeORM or Sequelize
│   ├─ Python
│   │   ├─ Async required → Tortoise ORM or SQLModel
│   │   └─ Sync / Django → Django ORM or SQLAlchemy
│   └─ Java
│       └─ JPA (Hibernate) or jOOQ
│
└─ NoSQL
    ├─ Document store → MongoDB (Mongoose for Node.js)
    └─ Key-value → Redis (caching, sessions)
```

## Best Practices

1. **Always validate input** - Use provided validation middleware
2. **Handle errors gracefully** - Use generated error handlers
3. **Write tests** - Use test templates for consistency
4. **Use environment variables** - Never hardcode secrets
5. **Implement logging** - Use provided logging configuration
6. **Monitor performance** - Set up metrics and alerts
7. **Security first** - Use provided authentication setup
8. **Version your API** - Follow versioning patterns
9. **Document your code** - Generate API docs automatically
10. **Deploy safely** - Use provided deployment scripts

## Common Patterns

### Repository Pattern
- Separation of concerns
- Easy testing
- Swappable implementations

### Service Layer
- Centralized business rules
- Transaction management
- Error handling

### Middleware Stack
- Authentication
- Authorization
- Validation
- Logging
- Error handling

## Troubleshooting

### Common Issues

**Database connection errors**
- Check connection string
- Verify database is running
- Check network connectivity
- Review connection pool settings

**Authentication failures**
- Verify JWT secret
- Check token expiration
- Validate token format
- Review middleware order

**Build failures**
- Check TypeScript configuration
- Verify dependencies are installed
- Review error messages
- Check for syntax errors

**Deployment issues**
- Verify Docker image builds
- Check Kubernetes pods
- Review logs
- Verify environment variables

## Quality Checklist

### Security
- [ ] Input validation on all endpoints (Zod/Joi)
- [ ] Password hashing (bcrypt cost 10+ or Argon2)
- [ ] SQL injection prevention (parameterized queries)
- [ ] Rate limiting on auth endpoints
- [ ] Security headers (Helmet.js)
- [ ] Environment variables for secrets

### Authentication & Authorization
- [ ] Strong JWT secret (256-bit)
- [ ] Short-lived access tokens (15min)
- [ ] Refresh token rotation
- [ ] Authorization checks on protected routes

### Error Handling
- [ ] Global error handler
- [ ] Async error handling (express-async-errors)
- [ ] Clear validation error messages
- [ ] 404 handling for unknown endpoints

### Performance
- [ ] Database connection pooling
- [ ] Query optimization (no N+1)
- [ ] Caching (Redis for sessions, rate limiting)
- [ ] Response compression (gzip/brotli)

### Testing
- [ ] Unit tests for services/repositories
- [ ] Integration tests for API endpoints
- [ ] >80% coverage for critical paths
- [ ] Separate test database

## Additional Resources

- **Detailed Technical Reference**: See [REFERENCE.md](REFERENCE.md)
- **Code Examples & Patterns**: See [EXAMPLES.md](EXAMPLES.md)
