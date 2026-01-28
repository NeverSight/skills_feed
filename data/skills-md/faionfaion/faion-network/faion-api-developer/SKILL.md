---
name: faion-api-developer
description: "API development: REST, GraphQL, OpenAPI, versioning, auth, rate limiting."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite, Skill
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# API Developer Skill

API design and development covering REST, GraphQL, OpenAPI specifications, authentication, and API best practices.

## Purpose

Handles API design, documentation, authentication, rate limiting, versioning, and API-specific patterns.

## When to Use

- REST API design and implementation
- GraphQL API design
- OpenAPI/Swagger specifications
- API authentication (OAuth, JWT, API keys)
- API versioning strategies
- API rate limiting and throttling
- API error handling
- API testing
- API gateways
- API monitoring
- WebSocket APIs

## Methodologies

| Category | Methodology | File |
|----------|-------------|------|
| **REST APIs** |
| REST API design | RESTful principles, resource design | api-rest-design.md |
| REST API design alt | REST patterns and best practices | rest-api-design.md |
| **GraphQL** |
| GraphQL API basics | Schema, queries, mutations | api-graphql.md |
| GraphQL API design | Schema design, resolvers, federation | graphql-api-design.md |
| GraphQL API alt | GraphQL patterns | graphql-api.md |
| **OpenAPI** |
| OpenAPI spec | OpenAPI 3.x specification | api-openapi-spec.md |
| OpenAPI specification | Spec writing, code generation | openapi-specification.md |
| **API Patterns** |
| Contract-first API | Schema-first development | api-contract-first.md |
| Contract-first development | API-first approach | contract-first-development.md |
| API versioning | Version strategies (URL, header, media type) | api-versioning.md |
| API error handling | Error codes, error responses | api-error-handling.md |
| API authentication | OAuth 2.0, JWT, API keys | api-authentication.md |
| API rate limiting | Rate limiting strategies | api-rate-limiting.md |
| Rate limiting | Throttling patterns | rate-limiting.md |
| API gateway patterns | Gateway design, BFF pattern | api-gateway-patterns.md |
| API monitoring | Metrics, logging, tracing | api-monitoring.md |
| **Testing & Docs** |
| API testing | Integration testing, contract testing | api-testing.md |
| API documentation | API docs, Swagger UI | api-documentation.md |
| **Real-time** |
| WebSocket design | WebSocket patterns, real-time APIs | websocket-design.md |

## Tools

- **REST:** OpenAPI 3.x, Swagger, Postman
- **GraphQL:** Apollo Server, GraphQL Yoga, Hasura
- **Auth:** OAuth 2.0, JWT, Passport.js, Auth0
- **Testing:** Postman, REST Client, Hoppscotch
- **Documentation:** Swagger UI, Redoc, Stoplight
- **Gateways:** Kong, Tyk, API Gateway (AWS)

## Related Sub-Skills

| Sub-skill | Relationship |
|-----------|--------------|
| faion-python-developer | Django REST Framework, FastAPI |
| faion-javascript-developer | Express, Fastify, GraphQL |
| faion-backend-developer | API implementation in Go, Java, etc. |
| faion-testing-developer | API testing strategies |

## Integration

Invoked by parent skill `faion-software-developer` for API design and implementation work.

---

*faion-api-developer v1.0 | 19 methodologies*
