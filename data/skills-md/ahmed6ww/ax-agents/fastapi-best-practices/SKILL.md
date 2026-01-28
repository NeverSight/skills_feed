---
name: fastapi-best-practices
description: FastAPI production-grade best practices and guidelines for building scalable, high-performance web APIs. Covers project structure, async concurrency, Pydantic validation, dependency injection, and database patterns.
license: MIT
metadata:
  author: zhanymkanov
  version: "1.0.0"
---

# FastAPI Best Practices

Comprehensive production-grade best practices for FastAPI applications. Contains rules across 7 categories to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Setting up a new FastAPI project structure
- Implementing async routes and handling blocking I/O
- Designing Pydantic models and validation logic
- Structuring dependencies for reusable validation and injection
- Integrating databases with SQLAlchemy and Alembic
- Writing tests and configuring CI/CD tooling

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Async & Concurrency | CRITICAL | `async-` |
| 2 | Project Structure | HIGH | `structure-` |
| 3 | Pydantic Patterns | HIGH | `pydantic-` |
| 4 | Dependency Injection | MEDIUM-HIGH | `dependency-` |
| 5 | Database & Storage | MEDIUM | `db-` |
| 6 | REST & API Design | MEDIUM | `api-` |
| 7 | Testing & Tooling | LOW-MEDIUM | `tooling-` |
| 8 | Code Maintenance | LOW | `maintenance-` |
| 9 | Performance Optimization | MEDIUM | `performance-` |
| 10 | TDD Strategy | HIGH | `tdd-` |

## Quick Reference

### 1. Async & Concurrency (CRITICAL)
- `async-io-intensive` - Use `async def` for awaitables, `def` for blocking I/O
- `async-cpu-intensive` - Offload CPU work to multiprocessing/Celery
- `async-sync-sdk` - Use `run_in_threadpool` for sync SDKs in async routes

### 2. Project Structure (HIGH)
- `structure-domain-driven` - Organize by domain (`src/{domain}`), not file type

### 3. Pydantic Patterns (HIGH)
- `pydantic-validation` - Use built-in regex, enums, etc.
- `pydantic-custom-base` - Use custom base model for global serialization
- `pydantic-config` - Split BaseSettings by domain
- `pydantic-value-error` - Raise ValueError for validation errors

### 4. Dependency Injection (MEDIUM-HIGH)
- `dependency-validation` - Use Depends for DB-backed validation
- `dependency-chaining` - Chain dependencies for reuse
- `dependency-decoupling` - Decouple into small reusable units
- `dependency-async` - Prefer async dependencies

### 5. Database & Storage (MEDIUM)
- `db-naming-conventions` - Strict naming (snake_case, singular, etc.)
- `db-index-naming` - Explicit index naming conventions
- `db-sql-first` - Prefer SQL for complex data logic
- `db-migrations` - Static, descriptive, reversible migrations

### 6. REST & API Design (MEDIUM)
- `api-path-naming` - Consistent path vars for dependency reuse
- `api-response-serialization` - Minimize serialization overhead
- `api-docs-hiding` - Hide docs in production
- `api-docs-customization` - Detailed OpenAPI metadata

### 7. Testing & Tooling (LOW-MEDIUM)
- `tooling-test-client` - Use AsyncClient/httpx for tests
- `tooling-linter` - Use Ruff for all linting

### 8. New Capabilities (Merged)
- **Scripts**: Helper scripts available in `scripts/` (e.g., `run_ruff.py`).
- **References**: Additional guides in `references/` (e.g., `quad_strategy.md`).
- **TDD**: Explicit testing strategies in `rules/tdd-strategy.md`.

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/async-io-intensive.md
rules/structure-domain-driven.md
```

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
