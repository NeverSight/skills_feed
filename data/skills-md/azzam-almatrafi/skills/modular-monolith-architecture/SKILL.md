---
name: modular-monolith-architecture
description: Scaffold and create a Modular Monolithic Architecture project. Use when the user wants to create a new modular monolith, restructure a monolith into modules, design module boundaries, or set up a project following modular monolith best practices. Supports multiple languages and frameworks.
argument-hint: "[language/framework] [project-name] [modules...]"
---

# Modular Monolithic Architecture — Project Scaffolder

Generate production-ready Modular Monolith projects with proper module boundaries, internal APIs, shared kernel, and infrastructure following industry best practices.

## Overview

A Modular Monolith is a single deployable application organized into loosely coupled, highly cohesive modules — each representing a bounded context. It combines monolithic simplicity (single deployment, ACID transactions, in-process calls) with microservices-style modularity (clear boundaries, team autonomy, independent development).

This skill scaffolds complete projects with:
- **Module isolation**: Each module owns its domain, data access, and API surface
- **Inter-module communication**: Via public contracts/interfaces, never internal details
- **Shared kernel**: Cross-cutting concerns (auth, logging, events) in a shared layer
- **Database-per-module schema**: Logical isolation within a single RDBMS
- **Migration-ready boundaries**: Modules can be extracted to microservices later

## Workflow

### Step 1: Gather Requirements

If the user hasn't specified, ask for:
1. **Language/Framework** (e.g., C#/ASP.NET Core, Java/Spring Boot, TypeScript/NestJS, Python/Django, Go)
2. **Project name**
3. **Business modules** (e.g., Product, Order, Payment, Shipping, Notification)
4. **Database** preference (PostgreSQL, MySQL, SQL Server, SQLite for dev)
5. **Additional features**: Event bus, API gateway, Docker, CI/CD

If the user provides `$ARGUMENTS`, parse them: `$ARGUMENTS[0]` = language/framework, `$ARGUMENTS[1]` = project name, remaining = module names.

### Step 2: Generate Project Structure

Read the architecture references for the chosen framework:
- For detailed structure patterns, see [references/project-structures.md](references/project-structures.md)
- For module design patterns, see [references/module-design.md](references/module-design.md)
- For comparison and decision guide, see [references/architecture-guide.md](references/architecture-guide.md)
- For event-driven patterns and event bus design, see [references/event-driven-patterns.md](references/event-driven-patterns.md)
- For inter-module communication and contract versioning, see [references/api-versioning-communication.md](references/api-versioning-communication.md)
- For concrete scaffold examples, see [examples/dotnet-scaffold.md](examples/dotnet-scaffold.md) and [examples/nestjs-scaffold.md](examples/nestjs-scaffold.md)

Generate the project following these **critical rules**:

#### Module Rules
1. Each module gets its own directory with internal layers (Domain/Application/Infrastructure/API)
2. Modules communicate ONLY through public contracts (interfaces/DTOs) — never reference another module's internal types
3. Each module has its own database schema or migration folder
4. Each module registers its own services/dependencies
5. No circular dependencies between modules

#### Shared Kernel Rules
1. Contains ONLY cross-cutting concerns: base entities, common value objects, event bus interfaces, auth abstractions
2. Must be thin — if it grows large, something belongs in a module
3. Never contains business logic specific to any module

#### Infrastructure Rules
1. Single entry point (Program.cs / main.ts / main.py / main.go)
2. Composition root wires all modules together
3. Database context/session is shared but schemas are isolated
4. Event bus for async inter-module communication (in-process, upgradeable to message broker)

### Step 3: Generate Code

For each module, generate:
- **Domain layer**: Entities, value objects, domain events, repository interfaces
- **Application layer**: Use cases/commands/queries, DTOs, validation
- **Infrastructure layer**: Repository implementations, database configuration, migrations
- **API layer**: Controllers/handlers, request/response models, module registration

Also generate:
- **Shared kernel**: Base classes, event bus, common abstractions
- **Host/entry point**: Composition root, middleware, configuration
- **Tests**: Module unit tests, integration tests, contract tests, and architecture boundary tests — see [references/testing-strategies.md](references/testing-strategies.md)
- **Observability**: Module-scoped logging, health checks, and tracing setup — see [references/observability.md](references/observability.md)
- **Docker** (if requested): Dockerfile + docker-compose with database
- **README.md**: Architecture overview, how to run, how to add modules (use [examples/README-template.md](examples/README-template.md))

### Step 4: Validate

After generation:
1. Verify no module directly references another module's internal types
2. Confirm each module has its own schema/migration folder
3. Check that the shared kernel contains no business logic
4. Ensure the project builds/compiles successfully
5. Run any generated tests

Validation scripts are available in [scripts/](scripts/) for CI integration:
- `scripts/validate-boundaries.sh <modules-dir>` — detects cross-module boundary violations
- `scripts/validate-shared-kernel.sh <shared-dir> <modules-dir>` — ensures shared kernel doesn't reference modules
- `scripts/check-circular-deps.sh <modules-dir>` — detects circular dependencies between modules

### Step 5: Migration Guidance

If the user asks about extracting modules to microservices, see [references/migration-to-microservices.md](references/migration-to-microservices.md) for a detailed step-by-step guide covering:
- When to extract (evidence-based signals)
- Pre-extraction checklist
- Creating the service, swapping the implementation, adding resilience
- Rollback strategy

## Key Principles to Enforce

| Principle | What It Means | How to Enforce |
|-----------|---------------|----------------|
| High Cohesion | Module contains everything for its domain | Domain + Application + Infrastructure + API per module |
| Low Coupling | Modules don't depend on each other's internals | Communication only via shared contracts/interfaces |
| Single Responsibility | Each module has one bounded context | One business domain per module directory |
| Encapsulated Data | Module owns its data | Separate DB schema per module, no cross-module queries |
| Explicit Dependencies | All module dependencies are visible | Module registration file listing required contracts |
| Domain-Driven Design | Modules align with business domains | Named after business capabilities, not technical layers |

## Example Invocations

```
/modular-monolith dotnet ECommerceApp Product Order Payment Shipping
/modular-monolith spring-boot MyShop catalog basket checkout
/modular-monolith nestjs SaasApp tenant billing notification
/modular-monolith go FinanceApp accounts transactions reporting
```

## When NOT to Use This

Suggest microservices instead if the user describes:
- Teams needing completely independent deployment cadences
- Requirements for polyglot tech stacks (Python ML + Go APIs + Java enterprise)
- Extreme per-service scaling requirements
- Already having Kubernetes infrastructure and DevOps maturity

Suggest a simple monolith if:
- Solo developer or very small team (1-3 devs)
- Prototype/MVP with unclear domain boundaries
- Application with fewer than 3 distinct business domains
