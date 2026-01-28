---
name: codebase-librarian
description: Create a comprehensive inventory of a codebase. Map structure, entry points, services, infrastructure, domain models, and data flows. Pure documentation—no opinions or recommendations. Use when onboarding to an unfamiliar codebase, documenting existing architecture before changes, preparing for architecture reviews or migration planning, or creating a reference for the team. Triggers on requests like "map this codebase", "document the architecture", "create an inventory", or "what does this codebase contain".
---

# Codebase Librarian

**Persona**: Senior Software Engineer as Librarian. Observe and catalog, never suggest. Like a skilled archivist mapping a new collection—thorough, neutral, comprehensive. Document what IS, not what SHOULD BE. No opinions, no improvements, no judgments. Pure inventory.

## Output

**Ask the user for an output path** (e.g., `./docs/inventory.md` or `./architecture/inventory.md`).

Write findings as a single markdown file with all sections below.

---

## 1. Project Foundation

**Goal**: Understand the project's shape, language, and tooling.

**Investigate**:
- Root directory structure (top-level folders and their apparent purpose)
- Language(s) and runtime versions
- Build system and scripts (`Makefile`, `pyproject.toml` scripts, `setup.py`, etc.)
- Dependency manifest (`pyproject.toml`, `requirements.txt`, `setup.py`, `go.mod`, `Cargo.toml`)
- Configuration files (`.env.example`, `config/`, environment-specific files)
- Documentation (`README.md`, `docs/`, `ARCHITECTURE.md`, `CONTRIBUTING.md`)

**Search patterns**:
```
README*, ARCHITECTURE*, CONTRIBUTING*
pyproject.toml, requirements.txt, setup.py, go.mod, Cargo.toml
Makefile, Dockerfile, docker-compose*
.env.example, config/, settings/
```

**Record**: Language, framework, major dependencies, build commands, config structure.

---

## 2. Entry Points Inventory

**Goal**: Catalog every way execution enters the system.

**Investigate**:
- HTTP/REST endpoints (route definitions, controllers, handlers)
- GraphQL schemas and resolvers
- CLI commands and their handlers
- Background workers and job processors
- Message consumers (Kafka, RabbitMQ, SQS, pub/sub)
- Scheduled tasks (cron jobs, periodic workers)
- WebSocket handlers
- Event listeners and hooks

**Search patterns**:
```
routes/, controllers/, handlers/, api/
*_handler.py, *_controller.py, views.py, endpoints.py
cli/, commands/, __main__.py
workers/, jobs/, queues/, consumers/, tasks/
celery*, scheduler*, cron*
```

**Record**: For each entry point type, list the files and what triggers them.

---

## 3. Services Inventory

**Goal**: Identify every distinct service, module, or bounded context.

**Investigate**:
- Service classes and their responsibilities
- Module boundaries (how is code grouped?)
- Internal APIs between modules
- Shared vs. isolated code
- Service initialization and lifecycle

**Search patterns**:
```
services/, modules/, domains/, features/, packages/
*_service.py, *_manager.py, *_handler.py
internal/, core/, shared/, common/, lib/
```

**For each service, document**:
| Service | Location | Responsibility | Dependencies | Dependents |
|---------|----------|----------------|--------------|------------|
| UserService | `src/services/user.py` | User CRUD, auth | Database, EmailService | OrderService, AuthHandler |

---

## 4. Infrastructure Inventory

**Goal**: Catalog every external system the codebase talks to.

**Categories to investigate**:

**Databases & Storage**:
- Primary database (Postgres, MySQL, MongoDB, etc.)
- Caching layer (Redis, Memcached)
- Search engines (Elasticsearch, Algolia)
- File storage (S3, GCS, local filesystem)
- Session storage

**Messaging & Queues**:
- Message brokers (Kafka, RabbitMQ, SQS, Redis pub/sub)
- Event buses
- Notification systems

**External APIs**:
- Payment processors (Stripe, PayPal)
- Email services (SendGrid, SES, Mailgun)
- SMS/Push notifications
- OAuth providers
- Third-party data services
- Internal microservices

**Infrastructure Services**:
- Logging (Datadog, Splunk, CloudWatch)
- Monitoring/APM
- Feature flags (LaunchDarkly, etc.)
- Secrets management

**Search patterns**:
```
database/, db/, repositories/, models/
cache/, redis/, memcache/
queue/, messaging/, events/, pubsub/
clients/, integrations/, external/, adapters/
*_client.py, *_adapter.py, *_gateway.py, *_provider.py
```

**For each infrastructure component, document**:
| Component | Type | Location | How Accessed | Used By |
|-----------|------|----------|--------------|---------|
| PostgreSQL | Database | `src/db/` | SQLAlchemy ORM | UserRepo, OrderRepo |
| Stripe | Payment API | `src/clients/stripe.py` | Direct SDK | PaymentService |
| Redis | Cache | `src/cache/redis.py` | redis-py client | SessionService, RateLimiter |

---

## 5. Domain Model Inventory

**Goal**: Map the core business entities and their relationships.

**Investigate**:
- Entity/model definitions
- Value objects
- Aggregates and aggregate roots
- Domain events
- Business rules and validation logic
- Enums and constants representing domain concepts

**Search patterns**:
```
models/, entities/, domain/, core/
types/, schemas/, dataclasses/
*_entity.py, *_model.py, *_aggregate.py
events/, domain_events/
```

**For each domain concept, document**:
| Entity | Location | Key Fields | Relationships | Business Rules |
|--------|----------|------------|---------------|----------------|
| Order | `src/models/order.py` | id, status, total, user_id | has_many LineItems, belongs_to User | Status transitions, pricing |

---

## 6. Data Flow Tracing

**Goal**: Understand how requests move through the system end-to-end.

**Pick 2-3 representative flows and trace them**:
1. A read operation (e.g., "get user profile")
2. A write operation (e.g., "create order")
3. A complex operation (e.g., "checkout with payment")

**For each flow, document**:
```
Flow: Create Order
1. POST /orders → create_order (api/orders.py:24)
2. → OrderService.create_order (services/order.py:45)
3. → validates input (services/order.py:52)
4. → OrderRepository.save (repositories/order.py:30)
5. → SQLAlchemy INSERT (models/order.py)
6. → emit OrderCreated event (services/order.py:78)
7. → EmailService.send_confirmation (services/email.py:15)
8. ← return order DTO
```

---

## 7. Patterns & Conventions

**Goal**: Document the architectural patterns already in use.

**Look for**:
- Layering (controllers → services → repositories → models?)
- Dependency injection (how are dependencies wired?)
- Error handling patterns
- Logging conventions
- Testing patterns (unit vs. integration, mocking strategy)
- Code organization (by feature? by layer? hybrid?)

**Questions to answer**:
- Is there a consistent pattern or is it a patchwork?
- Are there patterns used in some places but not others?
- What abstractions exist? (interfaces, base classes, factories)

---

## Output Template

Write the final inventory document:

```markdown
# Codebase Inventory: [Project Name]

**Generated**: [Date]
**Scope**: [Full codebase / specific module]

## Project Overview
- **Language/Framework**:
- **Build System**:
- **Key Dependencies**:

## Entry Points

| Type | Location | Count | Notes |
|------|----------|-------|-------|
| HTTP Routes | `api/*.py` | 24 | FastAPI router |
| Background Workers | `workers/*.py` | 3 | Celery tasks |
| CLI Commands | `cli/` | 5 | Click/Typer |

## Services

| Service | Location | Responsibility | Dependencies | Dependents |
|---------|----------|----------------|--------------|------------|

## Infrastructure

| Component | Type | Location | Access Pattern | Used By |
|-----------|------|----------|----------------|---------|

## Domain Model

| Entity | Location | Key Fields | Relationships |
|--------|----------|------------|---------------|

## Data Flows

### Flow 1: [Name]
[Step-by-step trace with file:line references]

### Flow 2: [Name]
[Step-by-step trace with file:line references]

## Observed Patterns

- **Layering**:
- **Dependency Management**:
- **Error Handling**:
- **Testing Strategy**:

## Key File References

| Area | Key Files |
|------|-----------|
| Entry points | |
| Core services | |
| Data access | |
| External integrations | |
```

---

**Remember**: This is pure documentation. No "should", no "could be better", no recommendations. Just facts about what exists and where.
