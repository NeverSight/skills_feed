---
name: python-backend-expert
description: >-
  Python backend implementation patterns for FastAPI applications with SQLAlchemy 2.0,
  Pydantic v2, and async patterns. Use during the implementation phase when creating
  or modifying FastAPI endpoints, Pydantic models, SQLAlchemy models, service layers,
  or repository classes. Covers async session management, dependency injection via
  Depends(), layered error handling, and Alembic migrations. Does NOT cover testing
  (use pytest-patterns), deployment (use deployment-pipeline), or FastAPI framework
  mechanics like middleware and WebSockets (use fastapi-patterns).
license: MIT
compatibility: 'Python 3.12+, FastAPI 0.115+, SQLAlchemy 2.0+, Pydantic v2, Alembic 1.13+'
metadata:
  author: platform-team
  version: '1.0.0'
  sdlc-phase: implementation
allowed-tools: Read Edit Write Bash(python:*) Bash(pip:*) Bash(alembic:*)
context: fork
---

# Python Backend Expert

## When to Use

Activate this skill when:
- Creating or modifying FastAPI route handlers (endpoints)
- Defining or updating Pydantic v2 request/response schemas
- Writing SQLAlchemy 2.0 async models, queries, or relationships
- Implementing the repository pattern for data access
- Writing service layer business logic
- Creating or running Alembic migrations
- Setting up dependency injection chains with `Depends()`
- Handling errors across the route/service/repository layers

Do NOT use this skill for:
- Writing tests for backend code (use `pytest-patterns`)
- FastAPI framework mechanics — middleware, WebSockets, OpenAPI customization, CORS, lifespan (use `fastapi-patterns`)
- Deployment or CI/CD pipeline configuration (use `deployment-pipeline`)
- API contract design or endpoint planning (use `api-design-patterns`)
- Architecture decisions or layer design (use `system-architecture`)

## Instructions

### Project Structure

```
app/
├── main.py              # FastAPI application factory
├── core/
│   ├── config.py        # pydantic-settings configuration
│   ├── database.py      # Async engine, session factory
│   └── security.py      # Password hashing, JWT utilities
├── models/              # SQLAlchemy ORM models
│   ├── __init__.py
│   ├── base.py          # Declarative base
│   └── user.py
├── schemas/             # Pydantic v2 schemas
│   ├── __init__.py
│   └── user.py
├── repositories/        # Data access layer
│   ├── __init__.py
│   └── user_repo.py
├── services/            # Business logic layer
│   ├── __init__.py
│   └── user_service.py
├── routes/              # FastAPI routers
│   ├── __init__.py
│   └── users.py
├── dependencies/        # Reusable Depends() providers
│   ├── __init__.py
│   └── auth.py
└── exceptions.py        # Domain exception classes
```

### FastAPI Endpoint Pattern

Every endpoint follows this structure:

```python
router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    session: AsyncSession = Depends(get_async_session),
) -> UserResponse:
    service = UserService(session)
    try:
        user = await service.create_user(data)
        return UserResponse.model_validate(user)
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> UserResponse:
    service = UserService(session)
    try:
        user = await service.get_user(user_id)
        return UserResponse.model_validate(user)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
```

**Rules:**
- Routes handle HTTP concerns only: status codes, `HTTPException`, response formatting
- Routes call services, never repositories directly
- Use `response_model` for automatic response serialization and OpenAPI docs
- Use `status.HTTP_*` constants, not bare integers
- Use `Depends()` for session, auth, and service injection

### Repository Pattern

Repositories encapsulate all database access:

```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self._session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self._session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def list_with_posts(
        self, *, offset: int = 0, limit: int = 20
    ) -> list[User]:
        result = await self._session.execute(
            select(User)
            .options(selectinload(User.posts))
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def create(self, user: User) -> User:
        self._session.add(user)
        await self._session.flush()
        await self._session.refresh(user)
        return user

    async def update(self, user: User, **kwargs: object) -> User:
        for key, value in kwargs.items():
            setattr(user, key, value)
        await self._session.flush()
        await self._session.refresh(user)
        return user

    async def delete(self, user: User) -> None:
        await self._session.delete(user)
        await self._session.flush()
```

**Rules:**
- One repository per model (or aggregate root)
- Repositories return model instances or `None` — never HTTP responses
- No business logic in repositories
- Always `flush()` + `refresh()` after `add()` to get generated fields (id, timestamps)
- Use `selectinload()` for eager loading relationships in async context
- Never raise `HTTPException` from repositories

### Service Layer Pattern

Services contain business logic and orchestrate repositories:

```python
from app.exceptions import ConflictError, NotFoundError
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, UserPatch
from app.core.security import hash_password


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = UserRepository(session)

    async def create_user(self, data: UserCreate) -> User:
        # Business rule: email must be unique
        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise ConflictError(f"Email {data.email} already registered")

        # Business logic: hash password before storing
        user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
            display_name=data.display_name,
        )
        return await self.repo.create(user)

    async def get_user(self, user_id: int) -> User:
        user = await self.repo.get_by_id(user_id)
        if user is None:
            raise NotFoundError(f"User {user_id} not found")
        return user

    async def update_user(self, user_id: int, data: UserPatch) -> User:
        user = await self.get_user(user_id)
        update_fields = data.model_dump(exclude_unset=True)
        if "password" in update_fields:
            update_fields["hashed_password"] = hash_password(update_fields.pop("password"))
        return await self.repo.update(user, **update_fields)
```

**Rules:**
- Services raise domain exceptions (`NotFoundError`, `ConflictError`), NEVER `HTTPException`
- Services are the only place for business logic
- Services call repositories for data access, never run raw queries
- Services receive `AsyncSession` via constructor and create their own repository instances
- Services validate business rules before calling repositories

### Domain Exceptions

Define a hierarchy of domain exceptions:

```python
class AppError(Exception):
    """Base application error."""

class NotFoundError(AppError):
    """Resource not found."""

class ConflictError(AppError):
    """Resource conflict (duplicate, version mismatch)."""

class ValidationError(AppError):
    """Business rule violation."""

class PermissionError(AppError):
    """Insufficient permissions."""
```

Register global exception handlers in the FastAPI app:

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc), "code": "NOT_FOUND"})

@app.exception_handler(ConflictError)
async def conflict_handler(request: Request, exc: ConflictError) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc), "code": "CONFLICT"})
```

This allows services to raise domain exceptions without knowing about HTTP, and routes don't need try/except blocks.

### Pydantic v2 Schema Conventions

```python
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """POST request body — writable fields only, no id/timestamps."""
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    display_name: str = Field(min_length=1, max_length=100)


class UserPatch(BaseModel):
    """PATCH request body — all fields Optional."""
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8, max_length=128)
    display_name: str | None = Field(default=None, min_length=1, max_length=100)


class UserResponse(BaseModel):
    """Response body — all fields including id and timestamps."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    display_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
```

**Key Pydantic v2 patterns:**
- Use `ConfigDict(from_attributes=True)` instead of `class Config: orm_mode = True`
- Use `model_validate()` instead of `from_orm()`
- Use `model_dump()` instead of `.dict()`
- Use `model_dump(exclude_unset=True)` for PATCH to distinguish "not sent" from "set to null"
- Use `Field()` for validation constraints
- Use `str | None` syntax (Python 3.12+), not `Optional[str]`

### Async Session Management

```python
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        async with session.begin():
            yield session
```

**Rules:**
- `expire_on_commit=False` prevents detached instance errors after commit
- `session.begin()` context manager auto-commits on success, rolls back on exception
- One session per request via `Depends(get_async_session)`
- Never share sessions across concurrent tasks
- For background tasks, create a new session — never reuse the request session

### SQLAlchemy 2.0 Model Pattern

```python
from datetime import datetime
from sqlalchemy import String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    display_name: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    # Relationships — ALWAYS use selectin or joined for async
    posts: Mapped[list["Post"]] = relationship(
        back_populates="author", lazy="selectin"
    )
```

**Rules:**
- Use `Mapped[type]` annotations (SQLAlchemy 2.0 style)
- Use `mapped_column()` instead of `Column()`
- Set `lazy="selectin"` on relationships for async compatibility
- Use `server_default` for database-generated defaults
- Always include `created_at` and `updated_at` timestamps

### Alembic Migration Workflow

```bash
# Generate migration from model changes
alembic revision --autogenerate -m "add_users_table"

# Review the generated migration file before applying

# Apply migration
alembic upgrade head

# Rollback one step
alembic downgrade -1

# Show current revision
alembic current

# Show migration history
alembic history
```

**Migration naming convention:**
```python
# alembic/env.py
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
```

**Rules:**
- Always review autogenerated migrations before applying
- Every migration must have a working `downgrade()` function
- One migration per logical schema change
- Test both upgrade and downgrade
- Use descriptive migration messages: `"add_users_table"`, `"add_email_index_to_users"`

### Dependency Injection Pattern

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.services.user_service import UserService


async def get_user_service(
    session: AsyncSession = Depends(get_async_session),
) -> UserService:
    return UserService(session)


# Chain dependencies for auth
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session),
) -> User:
    user_id = decode_token(token)
    service = UserService(session)
    return await service.get_user(user_id)


async def require_admin(
    user: User = Depends(get_current_user),
) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin required")
    return user
```

## Examples

### Complete Request Flow

A request to `POST /users` flows through all layers:
1. **Route** receives `UserCreate` (Pydantic validates the request body)
2. **Route** calls `UserService.create_user(data)` via `Depends()`
3. **Service** checks business rule (email uniqueness) via `UserRepository.get_by_email()`
4. **Service** hashes password, creates `User` model instance
5. **Service** calls `UserRepository.create(user)` to persist
6. **Repository** adds to session, flushes, refreshes to get generated fields
7. **Route** converts the ORM model to `UserResponse` via `model_validate()`

If the email is duplicate, the service raises `ConflictError`, the global exception handler returns `409 Conflict`. No `try/except` needed in the route.

## Edge Cases

- **Detached instance errors:** Always call `flush()` + `refresh()` after `session.add()`. Set `expire_on_commit=False` on the session factory.

- **Async session in background tasks:** Never reuse the request session. Create a new session:
  ```python
  async def background_job():
      async with async_session_factory() as session:
          async with session.begin():
              # do work
  ```

- **N+1 queries:** Use `selectinload()` in repository queries for relationships that will be accessed. Set `lazy="selectin"` as the default on model relationships.

- **Bulk operations:** Use `session.execute(insert(User).values(list_of_dicts))` for bulk inserts instead of adding one by one.

- **Transaction spanning multiple services:** Pass the same session to all services. The session's `begin()` context manager handles the transaction boundary.

- **Pydantic v2 computed fields:** Use `@computed_field` for derived values in response schemas. See `references/pydantic-v2-migration.md`.

See `references/sqlalchemy-patterns.md` for advanced query optimization patterns.
