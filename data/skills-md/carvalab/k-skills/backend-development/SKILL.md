---
name: backend-development
description: PROACTIVELY build backend APIs with Node.js/TypeScript and Go. Use when designing APIs, implementing auth, or building microservices. Applies Clean Architecture, SOLID, DRY, YAGNI, KISS principles.
tools: Read, Edit, Bash, Grep, Glob
model: opus
---

# Backend Development

Node.js/TypeScript and Go. PostgreSQL, Redis. REST APIs.

> **Related Skills:**
>
> - `test-driven-development` - **USE PROACTIVELY** for new features and bug fixes (Red-Green-Refactor)
> - Check `.claude/CLAUDE.md` or `.cursor/rules/*` for project-specific conventions

## Core Principles

**Architecture:** Clean Architecture (4-layer) for new projects → `references/architecture.md`

**Design Principles:**

- **SOLID** - Single Responsibility, Open/Closed, Liskov, Interface Segregation, Dependency Inversion
- **DRY** - Don't Repeat Yourself (extract reusable code)
- **YAGNI** - You Aren't Gonna Need It (don't build unused features)
- **KISS** - Keep It Simple, Stupid (simplest solution that works)

**Comments Rule:** Code should be self-documenting. Only add comments when:

- Logic is complex/non-obvious (explain "why", not "what")
- Workarounds or edge cases need context
- Public API documentation (JSDoc/GoDoc)

```typescript
// ❌ BAD: Obvious comment
const age = user.age; // Get user age

// ✅ GOOD: Explains WHY
// Add 1 day buffer for timezone edge cases in billing cycle
const billingDate = addDays(cycleEnd, 1);
```

See `references/code-quality.md` for detailed examples.

## ⚠️ Existing Projects Rule

**ALWAYS respect existing project structure and patterns:**

1. **Read first** - Explore the codebase before making changes
2. **Follow existing patterns** - If project uses a pattern, continue using it
3. **Don't force architecture** - Don't refactor to Clean Architecture unless asked
4. **Incremental improvement** - Apply good practices to NEW code you write
5. **Ask if unclear** - When patterns conflict, ask the user

```
Existing project has flat structure? → Keep flat structure
Existing project has no interfaces? → Don't add interfaces everywhere
Existing project uses callbacks? → Use callbacks (unless migrating)
```

**Only apply Clean Architecture patterns to:**

- New greenfield projects
- New modules/features in existing projects (when it fits)
- When explicitly asked to refactor

## Quick Start

| Language | Test            | Lint                |
| -------- | --------------- | ------------------- |
| Node/TS  | `npm test`      | `npm run lint`      |
| Go       | `go test ./...` | `golangci-lint run` |

## Technology Selection

| Need               | Choose                             |
| ------------------ | ---------------------------------- |
| TypeScript API     | NestJS                             |
| High concurrency   | Go + Chi                           |
| Go database        | pgx/v5 + sqlc                      |
| Node database      | Drizzle (new), keep existing       |
| Go Redis           | rueidis (new), keep existing       |
| Go job queue       | River (PostgreSQL-backed)          |
| Node job queue     | **pg-boss** (PostgreSQL-backed)    |
| **Events (Kavak)** | **kbroker** (Kafka-by-REST)        |
| **Rate limiting**  | pg-boss throttle / River snooze    |
| Testing            | Vitest (new Node), Jest (existing) |
| Tracing            | OpenTelemetry + dd-trace           |

> **Note:** Use kbroker for events between services. Use pg-boss (Node) or River (Go) for job queues.

## Common Workflows

### New API Endpoint (TDD Approach)

> **Use `test-driven-development` skill** for Red-Green-Refactor cycle

1. **Write failing test first** → `test-driven-development` skill
2. Design endpoint → `references/api-design.md`
3. Set up handler → `references/go/http-handlers.md` or `references/node/frameworks.md`
4. Add database access → `references/go/database.md` or `references/node/database.md`
5. Implement auth → `references/authentication.md`
6. Refactor with tests passing → `references/code-quality.md`

### Fix Slow Query

1. Profile query → `references/debugging.md` (EXPLAIN ANALYZE)
2. Add indexes → `references/performance.md`
3. Add caching → `references/go/redis-queues.md` or `references/node/database.md`

### Deploy New Service

1. Write Dockerfile → `references/devops/docker.md`
2. Set up CI/CD → `references/devops/ci-cd.md`

### Debug Production Issue

1. Check logs/traces → `references/debugging.md`
2. Profile if slow → `references/debugging.md` (pprof/clinic.js)
3. Check DB queries → `references/debugging.md` (pg_stat_statements)

## References

| Reference                        | When to Use                                                |
| -------------------------------- | ---------------------------------------------------------- |
| **Go**                           |                                                            |
| `references/go/http-handlers.md` | Set up Chi routes, handlers, middleware                    |
| `references/go/database.md`      | Implement pgx/v5, sqlc queries                             |
| `references/go/patterns.md`      | Apply error handling, validation, testing                  |
| `references/go/redis-queues.md`  | Add rueidis caching, River job queue                       |
| **Node.js**                      |                                                            |
| `references/node/frameworks.md`  | Set up NestJS, Express, Fastify                            |
| `references/node/database.md`    | Implement Drizzle, Prisma, caching                         |
| `references/node/patterns.md`    | Apply validation, errors, testing                          |
| **DevOps**                       |                                                            |
| `references/devops/docker.md`    | Write Dockerfiles, compose, health checks, DataDog metrics |
| `references/devops/ci-cd.md`     | Configure GitLab CI pipelines                              |
| **Cross-Cutting**                |                                                            |
| `references/architecture.md`     | **Clean Architecture (4-layer)**, microservices, events    |
| `references/code-quality.md`     | **SOLID, DRY, YAGNI, KISS**, design patterns               |
| `references/api-design.md`       | Design REST endpoints, versioning                          |
| `references/authentication.md`   | Implement OAuth 2.1, JWT, RBAC                             |
| `references/security.md`         | Apply OWASP Top 10, input validation                       |
| `references/performance.md`      | Optimize caching, queries, pooling                         |
| `references/testing.md`          | Write unit, integration, E2E tests                         |
| `references/debugging.md`        | Debug with logs, profilers, tracing                        |

## Kavak-Only References

Use when working on Kavak projects.

| Reference                               | When to Use                                      |
| --------------------------------------- | ------------------------------------------------ |
| `references/kavak/kbroker.md`           | **Publish/subscribe events** between services    |
| `references/kavak/queues-ratelimit.md`  | **Job queues, rate limiting** with River/pg-boss |
| `references/kavak/microservice-auth.md` | Authenticate between services (STS)              |
| `references/kavak/gitlab-ci.md`         | Set up kavak-it/ci-jobs v3 pipelines             |
| `references/kavak/docker-images.md`     | Build with docker-debian base                    |
| `references/kavak/workload-config.md`   | Configure `.kavak/` dir, cron jobs               |
| `references/kavak/logging-metrics.md`   | Use kvklog, kvkmetric SDKs                       |
