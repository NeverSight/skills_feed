---
name: fullstack-developer
description: End-to-end feature expert specializing in frontend-backend integration, system architecture, and complete application development
---

# Fullstack Developer Skill

## Purpose

Provides end-to-end full-stack development expertise spanning frontend and backend technologies with focus on seamless integration, complete feature ownership, and system-level architecture. Specializes in building complete applications from database to UI with modern web technologies.

## When to Use

- Building complete features end-to-end (database → API → frontend)
- Integrating frontend and backend systems (REST/GraphQL APIs, WebSockets)
- Implementing authentication and authorization across the stack
- Designing and implementing full-stack architectures (monoliths, microservices)
- Optimizing performance across frontend-backend boundaries
- Debugging complex issues spanning multiple layers of the stack
- Building full-stack applications with React/Vue + Node.js/Python/Go

## Core Capabilities

### Frontend Development
- Building React, Vue, or other modern frontend applications
- Implementing component architectures and design patterns
- Managing state with Redux, Context, or other solutions
- Creating responsive and accessible user interfaces

### Backend Development
- Developing APIs with Node.js, Python, Go, or other backends
- Managing database design and ORM usage
- Implementing authentication and authorization systems
- Handling file uploads, streaming, and server-side processing

### Full-Stack Integration
- Connecting frontend and backend systems seamlessly
- Managing API contracts and version compatibility
- Implementing real-time features (WebSockets, Server-Sent Events)
- Optimizing performance across the full stack

### DevOps and Deployment
- Setting up CI/CD pipelines for full-stack applications
- Managing containerization with Docker and Kubernetes
- Configuring cloud infrastructure and deployment strategies
- Monitoring and troubleshooting production issues

## Quick Start

### Invoke When
- User needs complete feature implementation from database to UI
- Task involves frontend-backend communication or integration
- Building or debugging full-stack applications
- Need architecture decisions spanning multiple layers

### Don't Invoke When
- Task is purely frontend (use react-specialist or vue-expert)
- Task is purely backend API (use backend-developer)
- Task is infrastructure-focused (use devops-engineer)
- Task is database-specific (use database-optimizer)

## Decision Framework

### Architecture Patterns

```
Building new application?
│
├─ Team size < 5 developers?
│  │
│  ├─ YES → **Monolith** ✓
│  │        (simpler deployment, faster development)
│  │
│  └─ NO → Clear service boundaries exist?
│           │
│           ├─ YES → **Microservices** ✓
│           │        (team autonomy, independent scaling)
│           │
│           └─ NO → **Modular Monolith** ✓
│                    (monolith benefits + future flexibility)
│
└─ Integrating with existing system?
    │
    └─ Use **API Gateway Pattern** for consistent interface
```

### Frontend-Backend Communication

| Pattern | Use When | Avoid When |
|---------|----------|------------|
| **REST API** | CRUD operations, simple data fetching | Complex nested data, real-time needs |
| **GraphQL** | Complex data requirements, mobile apps | Simple APIs, caching is critical |
| **WebSockets** | Real-time updates, chat, live feeds | One-time data fetches |
| **Server-Sent Events** | Server-to-client streaming only | Bidirectional communication needed |

### State Management Decision

```
Application complexity?
│
├─ Simple (< 5 components sharing state)
│  └─ **React Context / Vue provide/inject** ✓
│
├─ Medium (multiple feature modules)
│  └─ **Zustand / Pinia** ✓
│
└─ Complex (large team, strict requirements)
   └─ **Redux Toolkit / Vuex** ✓
```

## Architecture Patterns and Methodologies

### Fullstack Integration Patterns
- **API-First Development**: Design contracts before implementation
- **Component-Driven Architecture**: Reusable UI and backend components
- **Service Layer Pattern**: Business logic separation
- **Repository Pattern**: Data access abstraction
- **State Management**: Frontend state consistency strategies

### Frontend Architecture
- **Component Architecture**: Atomic design, feature-based organization
- **State Management**: Redux, MobX, Context API, Vuex
- **Routing Patterns**: Client-side routing and navigation guards
- **Form Handling**: Validation, submission, and error management
- **Performance Optimization**: Code splitting, lazy loading, caching

### Backend Architecture
- **RESTful API Design**: Resource-oriented endpoints
- **GraphQL Integration**: Flexible data fetching
- **Authentication & Authorization**: JWT, OAuth2, session management
- **Data Validation**: Request validation and sanitization
- **Error Handling**: Consistent error responses and logging

## Best Practices

### Fullstack Development

- **API Design**: RESTful conventions with OpenAPI documentation
- **State Management**: Centralized state with proper data flow
- **Error Handling**: Consistent error responses, proper HTTP status codes
- **Security**: Input validation, SQL injection prevention, XSS protection
- **Performance**: Caching strategies, query optimization, code splitting

### Frontend Excellence

- **Component Design**: Reusable, composable components with clear interfaces
- **State Management**: Predictable state updates, proper data flow
- **Accessibility**: WCAG 2.1 compliance, keyboard navigation, screen reader support
- **Testing**: Unit tests, integration tests, E2E tests with good coverage
- **Performance**: Optimized bundle size, lazy loading, image optimization

### Backend Excellence

- **API Design**: Consistent patterns, proper versioning, deprecation strategies
- **Database**: Proper indexing, query optimization, connection pooling
- **Security**: Authentication, authorization, input validation, rate limiting
- **Monitoring**: Logging, metrics, tracing, alerting
- **Scalability**: Horizontal scaling, load balancing, caching strategies

### DevOps Integration

- **CI/CD**: Automated testing, building, and deployment pipelines
- **Infrastructure as Code**: Terraform or CloudFormation for infrastructure
- **Containerization**: Docker for consistent environments
- **Monitoring**: Prometheus, Grafana for metrics and alerting
- **Documentation**: API docs, runbooks, architecture diagrams

### Collaboration and Workflow

- **Code Review**: Meaningful reviews, constructive feedback
- **Documentation**: Clear README, contributing guide, code comments
- **Version Control**: Meaningful commits, branch strategy, PR workflow
- **Testing Strategy**: Test pyramid with appropriate coverage
- **Communication**: Clear requirements, regular syncs, async updates

## Additional Resources

- **Detailed Technical Reference**: See [REFERENCE.md](REFERENCE.md)
- **Code Examples & Patterns**: See [EXAMPLES.md](EXAMPLES.md)
