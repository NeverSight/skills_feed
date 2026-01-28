---
name: sqlalchemy-postgres
description: Expert guidance for SQLAlchemy 2.0 + Pydantic + PostgreSQL. Use when setting up database layers, defining models, creating migrations, or any database-related work. Automatically activated for DB tasks.
---

<essential_principles>
## SQLAlchemy 2.0 + Pydantic + PostgreSQL Best Practices

This skill provides expert guidance for building production-ready database layers.

### Stack
- **SQLAlchemy 2.0** with async support (asyncpg driver)
- **Pydantic v2** for validation and serialization
- **Alembic** for migrations
- **PostgreSQL** only

### Core Principles

**1. Separation of Concerns**
```
models/       # SQLAlchemy ORM models (database layer)
schemas/      # Pydantic schemas (API layer)
repositories/ # Data access patterns
services/     # Business logic
```

**2. Type Safety First**
Always use SQLAlchemy 2.0 style with `Mapped[]` type annotations:
```python
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
```

**3. Async by Default**
Use async engine and sessions for FastAPI:
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
engine = create_async_engine("postgresql+asyncpg://...")
```

**4. Pydantic-SQLAlchemy Bridge**
Keep models and schemas separate but mappable:
```python
# Schema reads from ORM
class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
```

**5. Repository Pattern**
Abstract database operations for testability and clean code.
</essential_principles>

<intake>
What do you need help with?

1. **Setup database layer** - Initialize SQLAlchemy + Pydantic + Alembic from scratch
2. **Define models** - Create SQLAlchemy models with Pydantic schemas
3. **Create migration** - Generate and manage Alembic migrations
4. **Query patterns** - Async CRUD, joins, eager loading, optimization
5. **Full implementation** - Complete database layer for a feature
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "setup", "initialize", "start" | workflows/setup-database.md |
| 2, "model", "define", "create model" | workflows/define-models.md |
| 3, "migration", "alembic", "schema change" | workflows/create-migration.md |
| 4, "query", "crud", "repository" | workflows/query-patterns.md |
| 5, "full", "complete", "feature" | Run setup → define-models → create-migration |

**Auto-detection triggers (use this skill when user mentions):**
- database, db, sqlalchemy, postgres, postgresql
- model, migration, alembic
- repository, crud, query
- async session, connection pool
</routing>

<reference_index>
## Domain Knowledge

| Reference | Purpose |
|-----------|---------|
| references/best-practices.md | Production patterns, security, performance |
| references/patterns.md | Repository, Unit of Work, common queries |
| references/async-patterns.md | Async session management, FastAPI integration |
</reference_index>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| workflows/setup-database.md | Initialize complete database layer |
| workflows/define-models.md | Create models + schemas + relationships |
| workflows/create-migration.md | Alembic migration workflow |
| workflows/query-patterns.md | CRUD operations and optimization |
</workflows_index>

<quick_reference>
## File Structure
```
src/
├── db/
│   ├── __init__.py
│   ├── base.py          # DeclarativeBase
│   ├── session.py       # Engine + async session factory
│   └── dependencies.py  # FastAPI dependency
├── models/
│   ├── __init__.py
│   └── user.py          # SQLAlchemy models
├── schemas/
│   ├── __init__.py
│   └── user.py          # Pydantic schemas
├── repositories/
│   ├── __init__.py
│   ├── base.py          # Generic repository
│   └── user.py          # User repository
└── alembic/
    ├── alembic.ini
    ├── env.py
    └── versions/
```

## Essential Imports
```python
# Models
from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

# Async
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# Pydantic
from pydantic import BaseModel, ConfigDict, Field
```

## Connection String
```python
# PostgreSQL async
DATABASE_URL = "postgresql+asyncpg://user:pass@localhost:5432/dbname"
```
</quick_reference>

<success_criteria>
Database layer is complete when:
- [ ] Async engine and session factory configured
- [ ] Base model with common fields (id, created_at, updated_at)
- [ ] Models use Mapped[] type annotations
- [ ] Pydantic schemas with from_attributes=True
- [ ] Alembic configured for async
- [ ] Repository pattern implemented
- [ ] FastAPI dependency for session injection
- [ ] Connection pooling configured for production
</success_criteria>
