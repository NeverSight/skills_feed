---
name: nest
description: NestJS framework for building efficient, scalable Node.js server-side applications. Use when working with NestJS apps, controllers, modules, providers, dependency injection, pipes, guards, interceptors, or building REST/GraphQL APIs.
metadata:
  author: Hairyf
  version: "2026.2.1"
  source: Generated from https://github.com/nestjs/docs.nestjs.com, scripts located at https://github.com/antfu/skills
---

NestJS is a progressive Node.js framework for building efficient and scalable server-side applications. It uses TypeScript by default, supports both Express and Fastify, and provides an out-of-the-box application architecture inspired by Angular. NestJS combines elements of OOP, FP, and FRP, making it ideal for building enterprise-grade applications.

> The skill is based on NestJS documentation, generated at 2026-02-01.

## CLI

| Topic | Description | Reference |
|-------|-------------|-----------|
| CLI Overview | Scaffolding, building, and running applications | [cli-overview](references/cli-overview.md) |
| Monorepo & Libraries | Workspaces, apps, shared libraries | [cli-monorepo](references/cli-monorepo.md) |

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Controllers | Route handlers, HTTP methods, request/response handling | [core-controllers](references/core-controllers.md) |
| Modules | Application structure, feature modules, shared modules, dynamic modules | [core-modules](references/core-modules.md) |
| Providers | Services, dependency injection, custom providers | [core-providers](references/core-providers.md) |
| Dependency Injection | DI fundamentals, custom providers, scopes | [core-dependency-injection](references/core-dependency-injection.md) |
| Middleware | Request/response middleware, functional middleware | [core-middleware](references/core-middleware.md) |

## Fundamentals

| Topic | Description | Reference |
|-------|-------------|-----------|
| Pipes | Data transformation and validation pipes | [fundamentals-pipes](references/fundamentals-pipes.md) |
| Guards | Authorization guards, role-based access control | [fundamentals-guards](references/fundamentals-guards.md) |
| Interceptors | Aspect-oriented programming, response transformation | [fundamentals-interceptors](references/fundamentals-interceptors.md) |
| Exception Filters | Error handling, custom exception filters | [fundamentals-exception-filters](references/fundamentals-exception-filters.md) |
| Custom Decorators | Creating custom parameter decorators | [fundamentals-custom-decorators](references/fundamentals-custom-decorators.md) |
| Dynamic Modules | Configurable modules, module configuration | [fundamentals-dynamic-modules](references/fundamentals-dynamic-modules.md) |
| Execution Context | Accessing request context, metadata reflection | [fundamentals-execution-context](references/fundamentals-execution-context.md) |
| Provider Scopes | Singleton, request-scoped, transient providers | [fundamentals-provider-scopes](references/fundamentals-provider-scopes.md) |
| Lifecycle Events | Application and provider lifecycle hooks | [fundamentals-lifecycle-events](references/fundamentals-lifecycle-events.md) |
| Lazy Loading | Loading modules on-demand for serverless | [fundamentals-lazy-loading](references/fundamentals-lazy-loading.md) |
| Circular Dependency | Resolving circular dependencies with forwardRef | [fundamentals-circular-dependency](references/fundamentals-circular-dependency.md) |
| Module Reference | Accessing providers dynamically with ModuleRef | [fundamentals-module-reference](references/fundamentals-module-reference.md) |
| Testing | Unit testing and e2e testing with @nestjs/testing | [fundamentals-testing](references/fundamentals-testing.md) |

## Techniques

| Topic | Description | Reference |
|-------|-------------|-----------|
| Validation | ValidationPipe, class-validator, DTO validation | [techniques-validation](references/techniques-validation.md) |
| Configuration | Environment variables, ConfigModule, configuration management | [techniques-configuration](references/techniques-configuration.md) |
| Database | TypeORM, Prisma, MongoDB integration | [techniques-database](references/techniques-database.md) |
| Caching | Cache manager, Redis integration, auto-caching | [techniques-caching](references/techniques-caching.md) |
| Logging | Built-in logger, custom loggers, JSON logging | [techniques-logging](references/techniques-logging.md) |
| File Upload | File upload handling with multer, validation | [techniques-file-upload](references/techniques-file-upload.md) |
| Versioning | URI, header, and media type API versioning | [techniques-versioning](references/techniques-versioning.md) |
| Serialization | Response serialization with class-transformer | [techniques-serialization](references/techniques-serialization.md) |
| Queues | Background job processing with BullMQ | [techniques-queues](references/techniques-queues.md) |
| Task Scheduling | Cron jobs, intervals, and timeouts | [techniques-task-scheduling](references/techniques-task-scheduling.md) |
| Events | Event-driven architecture with EventEmitter | [techniques-events](references/techniques-events.md) |
| HTTP Module | Making HTTP requests with Axios | [techniques-http-module](references/techniques-http-module.md) |
| Fastify | Using Fastify for better performance | [techniques-fastify](references/techniques-fastify.md) |
| Sessions & Cookies | HTTP sessions and cookies for stateful apps | [techniques-sessions-cookies](references/techniques-sessions-cookies.md) |
| Streaming & SSE | Compression, file streaming, Server-Sent Events | [techniques-compression-streaming-sse](references/techniques-compression-streaming-sse.md) |
| MVC & Serve Static | Template rendering (Handlebars) and SPA static serving | [techniques-mvc-serve-static](references/techniques-mvc-serve-static.md) |

## Security

| Topic | Description | Reference |
|-------|-------------|-----------|
| Authentication | Passport integration, JWT authentication | [recipes-authentication](references/recipes-authentication.md) |
| Authorization | RBAC, claims-based, CASL integration | [security-authorization](references/security-authorization.md) |
| CORS & Rate Limiting | CORS, Helmet, ThrottlerModule | [security-cors-helmet-rate-limiting](references/security-cors-helmet-rate-limiting.md) |
| Encryption & Hashing | bcrypt, argon2, password hashing | [security-encryption-hashing](references/security-encryption-hashing.md) |

## OpenAPI

| Topic | Description | Reference |
|-------|-------------|-----------|
| Swagger | OpenAPI documentation generation | [openapi-swagger](references/openapi-swagger.md) |

## WebSockets

| Topic | Description | Reference |
|-------|-------------|-----------|
| Gateways | Real-time communication with Socket.IO/ws | [websockets-gateways](references/websockets-gateways.md) |
| Guards & Exception Filters | WsException, BaseWsExceptionFilter, interceptors, pipes | [websockets-advanced](references/websockets-advanced.md) |

## Microservices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Overview | Transport layers, message patterns, events | [microservices-overview](references/microservices-overview.md) |
| gRPC | Protocol Buffers, streaming, metadata, reflection | [microservices-grpc](references/microservices-grpc.md) |
| Transports | Redis, Kafka, NATS, RabbitMQ configuration | [microservices-transports](references/microservices-transports.md) |

## GraphQL

| Topic | Description | Reference |
|-------|-------------|-----------|
| Overview | Code-first and schema-first approaches | [graphql-overview](references/graphql-overview.md) |
| Resolvers & Mutations | Queries, mutations, field resolvers | [graphql-resolvers-mutations](references/graphql-resolvers-mutations.md) |
| Subscriptions | Real-time subscriptions with PubSub | [graphql-subscriptions](references/graphql-subscriptions.md) |
| Scalars, Unions & Enums | Interfaces, scalars, union types, enums | [graphql-scalars-unions-enums](references/graphql-scalars-unions-enums.md) |

## Recipes

| Topic | Description | Reference |
|-------|-------------|-----------|
| CRUD Generator | Nest CLI resource generator | [recipes-crud-generator](references/recipes-crud-generator.md) |
| Documentation | OpenAPI/Swagger integration | [recipes-documentation](references/recipes-documentation.md) |
| TypeORM | TypeORM integration and usage | [recipes-typeorm](references/recipes-typeorm.md) |
| Prisma | Prisma ORM integration | [recipes-prisma](references/recipes-prisma.md) |
| Mongoose | MongoDB with Mongoose ODM | [recipes-mongoose](references/recipes-mongoose.md) |
| CQRS | Command Query Responsibility Segregation | [recipes-cqrs](references/recipes-cqrs.md) |
| Terminus | Health checks and readiness/liveness probes | [recipes-terminus](references/recipes-terminus.md) |

## FAQ

| Topic | Description | Reference |
|-------|-------------|-----------|
| Raw Body & Hybrid | Webhook signature verification, HTTP + microservices | [faq-raw-body-hybrid](references/faq-raw-body-hybrid.md) |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Request Lifecycle | Understanding execution order and flow | [best-practices-request-lifecycle](references/best-practices-request-lifecycle.md) |
