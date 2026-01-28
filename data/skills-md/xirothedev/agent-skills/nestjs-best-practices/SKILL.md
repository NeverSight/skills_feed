---
name: nestjs-best-practices
description: NestJS best practices and patterns for building scalable, maintainable backend applications. This skill should be used when writing, reviewing, or refactoring NestJS code to ensure proper architecture, security, performance, and code quality. Triggers on tasks involving NestJS modules, controllers, services, guards, pipes, middleware, Prisma database operations, authentication, or any NestJS-specific patterns.
license: MIT
metadata:
  author: xiro
  version: "1.0.0"
---

# NestJS Best Practices

Comprehensive guide for building production-ready NestJS applications. Contains 26 rules across 13 categories, covering security, architecture, performance, validation, database operations, authentication, and advanced patterns.

## When to Apply

Reference these guidelines when:
- Writing new NestJS modules, controllers, or services
- Implementing authentication and authorization
- Setting up Prisma database operations
- Creating DTOs and validation pipes
- Adding middleware or guards
- Implementing error handling and logging
- Reviewing NestJS code for best practices
- Refactoring existing NestJS applications

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Security | CRITICAL | `security-` |
| 2 | Performance | HIGH | `performance-` |
| 3 | Architecture | HIGH | `architecture-` |
| 4 | Error Handling | HIGH | `error-handling-` |
| 5 | Validation | CRITICAL | `validation-` |
| 6 | Database | CRITICAL | `database-` |
| 7 | Authentication | CRITICAL | `auth-` |
| 8 | API | MEDIUM | `api-` |
| 9 | Configuration | CRITICAL | `config-` |
| 10 | Testing | MEDIUM | `testing-` |
| 11 | Deployment | MEDIUM | `deployment-` |
| 12 | Middleware | MEDIUM | `middleware-` |
| 13 | Advanced | HIGH | `advanced-` |

## Quick Reference

### 1. Security (CRITICAL)

- `security-cors-whitelist` - Enable CORS with whitelist origins only
- `security-dependency-audit` - Regular dependency security audits with bun
- `security-helmet-headers` - Use Helmet middleware for security headers

### 2. Performance (HIGH)

- `performance-redis-caching` - Cache frequently used data with Redis

### 3. Architecture (HIGH)

- `architecture-short-functions` - Keep functions short and single purpose
- `architecture-feature-modules` - Organize code by feature modules
- `architecture-no-dead-code` - Remove unused code and dependencies
- `architecture-thin-controllers` - Single responsibility - separate controller and service
- `architecture-naming-conventions` - Use consistent naming conventions
- `architecture-event-driven` - Use event-driven architecture for loose coupling

### 4. Error Handling (HIGH)

- `error-handling-exception-filter` - Enable global exception filter
- `error-handling-structured-logging` - Implement proper logging strategy

### 5. Validation (CRITICAL)

- `validation-custom-pipes` - Create custom pipes for query parameter transformation
- `validation-dto-validation` - Validate all inputs with DTOs and ValidationPipe

### 6. Database (CRITICAL)

- `database-parameterized-queries` - Use parameterized queries to prevent SQL injection (Prisma v7)

### 7. Authentication (CRITICAL)

- `auth-password-hashing` - Use Bun's built-in Crypto for secure password hashing (argon2/bcrypt)
- `auth-route-guards` - Use guards for route protection

### 8. API (MEDIUM)

- `api-cursor-pagination` - Use cursor-based pagination for large datasets
- `api-swagger-docs` - Generate Swagger/OpenAPI documentation

### 9. Configuration (CRITICAL)

- `config-no-secrets` - Never hardcode secrets - use environment variables

### 10. Testing (MEDIUM)

- `testing-unit-tests` - Write comprehensive unit tests

### 11. Deployment (MEDIUM)

- `deployment-health-checks` - Implement health check endpoints

### 12. Middleware (MEDIUM)

- `middleware-compression` - Enable compression middleware for responses
- `middleware-rate-limiting` - Implement rate limiting for all routes

### 13. Advanced (HIGH)

- `advanced-lazy-loading` - Lazy load non-critical modules
- `advanced-scheduled-tasks` - Use @nestjs/schedule for cron jobs and scheduled tasks

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/security-cors-whitelist.md
rules/auth-route-guards.md
rules/validation-dto-validation.md
rules/_sections.md
```

Each rule file contains:
- "For AI Agents" section with step-by-step implementation instructions
- Quick Reference Checklist for code review
- ❌ WRONG vs ✅ CORRECT patterns with file locations
- Installation commands using `bun add`
- Comprehensive code examples for NestJS + Prisma
- Security and performance considerations

## Key Patterns

### Agent-Friendly Format

All rules are optimized for AI agents with:
- Explicit file locations (e.g., `src/users/users.service.ts`)
- Step-by-step "For AI Agents" sections
- ✅ CORRECT vs ❌ WRONG pattern comparisons
- Quick Reference Checklists
- Clear installation instructions

### Technology Stack

- **Framework**: NestJS with Express/Fastify adapter
- **Runtime**: Bun (native crypto, scheduling)
- **Database**: Prisma v7 (sql template tag, interactive transactions)
- **Validation**: class-validator + class-transformer
- **Security**: Helmet, CORS whitelisting, rate limiting
- **Scheduling**: @nestjs/schedule with cron/interval decorators
- **Events**: EventEmitter2 for loose coupling

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`

## Build Commands

```bash
cd packages/nestjs-best-practices-build
bun install
bun run build      # Generate AGENTS.md
bun run validate   # Validate rule files
bun run dev        # Build and validate
```

## Statistics

- **13 sections** covering all aspects of NestJS development
- **26 rules** prioritized by impact (CRITICAL, HIGH, MEDIUM)
- **Prisma v7** compatible database patterns
- **Bun runtime** native features (Crypto.hashPassword, @nestjs/schedule)
- **Agent-optimized** for automated code generation and review
