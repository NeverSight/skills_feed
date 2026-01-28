---
name: fastapi-patterns
description: Comprehensive FastAPI best practices, patterns, and conventions for building production-ready Python web APIs. Covers application structure, async patterns, Pydantic models, dependency injection, database integration, authentication, error handling, testing, OpenAPI documentation, performance optimization, and common anti-patterns. Essential reference for FastAPI code reviews and development.
allowed-tools: Read, Write, Grep, Glob, Bash
---

# FastAPI Patterns and Best Practices

## Purpose

This skill provides comprehensive guidance for building production-ready FastAPI applications. Reference this skill when:
- Reviewing FastAPI code
- Designing API endpoints and structures
- Implementing authentication and authorization
- Integrating databases with async patterns
- Writing tests for FastAPI applications
- Optimizing API performance
- Setting up dependency injection
- Validating request/response models

## Context

FastAPI is a modern, high-performance Python web framework built on Starlette and Pydantic. It leverages Python 3.6+ type hints to provide automatic request validation, serialization, and OpenAPI documentation generation. FastAPI is designed for async-first development, making it ideal for I/O-bound operations.

### Core Principles

1. **Type hints everywhere**: Enable automatic validation and documentation
2. **Async by default**: Use async/await for I/O operations
3. **Dependency injection**: Share resources and enforce dependencies
4. **Pydantic models**: Validate and serialize data
5. **Automatic documentation**: OpenAPI/Swagger generated from code

## Prerequisites

- Python 3.7+ (3.10+ recommended for best type hint support)
- Understanding of async/await patterns
- Familiarity with type hints (see `python-type-hints-guide` skill)
- Knowledge of Pydantic basics

## FastAPI Application Structure

### Recommended Project Layout

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration management
│   ├── dependencies.py      # Shared dependencies
│   ├── models/              # Pydantic models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/             # Database models (if using ORM)
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routers/             # API routes
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── items.py
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   └── user_service.py
│   ├── repositories/        # Data access layer
│   │   ├── __init__.py
│   │   └── user_repository.py
│   └── utils/               # Utility functions
│       ├── __init__.py
│       └── security.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_users.py
│   └── test_items.py
├── alembic/                 # Database migrations (if using SQLAlchemy)
├── .env
├── requirements.txt
└── pyproject.toml
```

### Main Application (main.py)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routers import users, items
from app.config import settings
from app.database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(items.router, prefix=f"{settings.API_V1_STR}/items", tags=["items"])

@app.get("/")
async def root():
    return {"message": "Welcome to the API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### Configuration Management (config.py)

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Application"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # Redis (optional)
    REDIS_URL: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )

settings = Settings()
```

## Path Operations

### Decorator Usage

```python
from fastapi import APIRouter, status
from app.models.user import UserCreate, UserResponse

router = APIRouter()

@router.get(
    "/",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="List all users",
    description="Retrieve a paginated list of all users",
    response_description="List of users successfully retrieved"
)
async def list_users(
    skip: int = 0,
    limit: int = 100
) -> list[UserResponse]:
    """Retrieve all users with pagination."""
    # Implementation
    pass

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new user"
)
async def create_user(user: UserCreate) -> UserResponse:
    """Create a new user."""
    # Implementation
    pass

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    responses={
        404: {"description": "User not found"},
        200: {"description": "User successfully retrieved"}
    }
)
async def get_user(user_id: int) -> UserResponse:
    """Get a specific user by ID."""
    # Implementation
    pass
```

### Path Parameters

```python
from fastapi import Path

@router.get("/users/{user_id}")
async def get_user(
    user_id: int = Path(..., title="User ID", ge=1, description="The ID of the user to retrieve")
):
    """Path parameters with validation."""
    return {"user_id": user_id}

# Multiple path parameters
@router.get("/users/{user_id}/items/{item_id}")
async def get_user_item(
    user_id: int = Path(..., ge=1),
    item_id: int = Path(..., ge=1)
):
    return {"user_id": user_id, "item_id": item_id}
```

### Query Parameters

```python
from fastapi import Query
from typing import List

@router.get("/items/")
async def list_items(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Max records to return"),
    search: str | None = Query(None, min_length=3, max_length=50),
    tags: List[str] = Query([], description="Filter by tags")
):
    """Query parameters with validation and defaults."""
    # Implementation
    pass
```

### Request Body (Pydantic Models)

```python
from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str | None = None
    is_active: bool = True

@router.post("/users/")
async def create_user(user: UserCreate):
    """Request body automatically validated against Pydantic model."""
    return user

# Multiple body parameters
class Item(BaseModel):
    name: str
    description: str | None = None

class User(BaseModel):
    username: str
    email: EmailStr

@router.post("/users-items/")
async def create_user_item(user: User, item: Item):
    """Multiple body parameters."""
    return {"user": user, "item": item}
```

## Pydantic Models

### Request/Response Model Design

```python
from pydantic import BaseModel, Field, EmailStr, validator, field_validator
from datetime import datetime
from typing import Optional

# Base model with shared fields
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str | None = None

# Request model for creation
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v

# Request model for updates
class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    is_active: bool | None = None

# Response model (never includes password)
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,  # Allows ORM model conversion
        "json_schema_extra": {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "username": "johndoe",
                "full_name": "John Doe",
                "is_active": True,
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        }
    }

# Database model (for use with ORMs)
class UserInDB(UserResponse):
    hashed_password: str
```

### Field Validation

```python
from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime

class EventCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., max_length=500)
    start_date: datetime
    end_date: datetime
    max_attendees: int = Field(..., gt=0, le=1000)

    @field_validator('name')
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Name cannot be blank')
        return v.strip()

    @model_validator(mode='after')
    def check_dates(self):
        if self.end_date <= self.start_date:
            raise ValueError('end_date must be after start_date')
        return self
```

### Nested Models

```python
from pydantic import BaseModel
from typing import List

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str

class PhoneNumber(BaseModel):
    number: str
    type: str  # "mobile", "home", "work"

class UserProfile(BaseModel):
    username: str
    email: EmailStr
    addresses: List[Address] = []
    phone_numbers: List[PhoneNumber] = []

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "addresses": [
                    {
                        "street": "123 Main St",
                        "city": "Springfield",
                        "state": "IL",
                        "zip_code": "62701"
                    }
                ],
                "phone_numbers": [
                    {"number": "555-1234", "type": "mobile"}
                ]
            }
        }
```

### Model Inheritance

```python
from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class ItemCreate(ItemBase):
    """Inherits all fields from ItemBase."""
    pass

class ItemUpdate(ItemBase):
    """All fields optional for updates."""
    name: str | None = None
    price: float | None = None

class ItemInDB(ItemBase):
    id: int
    owner_id: int

    model_config = {"from_attributes": True}
```

## Dependency Injection

### Basic Dependencies

```python
from fastapi import Depends, HTTPException, status
from typing import Annotated

# Simple dependency
async def get_current_user_id(user_id: int) -> int:
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    return user_id

@router.get("/users/me")
async def read_current_user(
    user_id: Annotated[int, Depends(get_current_user_id)]
):
    return {"user_id": user_id}
```

### Database Session Dependencies

```python
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal

async def get_db() -> AsyncSession:
    """Dependency that provides database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

@router.get("/users/")
async def list_users(
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Use database session in endpoint."""
    # Use db session here
    pass
```

### Authentication Dependencies

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Annotated

from app.config import settings
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> User:
    """Dependency that validates token and returns current user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user_from_db(db, user_id=int(user_id))
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """Sub-dependency that checks if user is active."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user
```

### Shared Dependencies

```python
from fastapi import APIRouter, Depends

# Router-level dependencies (applied to all routes in router)
router = APIRouter(
    dependencies=[Depends(get_current_active_user)]
)

# All routes in this router require authentication
@router.get("/items/")
async def list_items():
    # Authentication already enforced by router dependency
    pass
```

### Yield Dependencies for Cleanup

```python
async def get_redis_client():
    """Dependency with cleanup using yield."""
    client = await aioredis.create_redis_pool('redis://localhost')
    try:
        yield client
    finally:
        client.close()
        await client.wait_closed()

@router.get("/cached-data/")
async def get_cached_data(
    redis: Annotated[aioredis.Redis, Depends(get_redis_client)]
):
    value = await redis.get('key')
    return {"value": value}
```

## Async Best Practices

### When to Use async def vs def

```python
# ✅ Use async def for I/O operations
@router.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Database call - use async."""
    user = await db.get(User, user_id)
    return user

# ✅ Use async def for HTTP calls
@router.get("/external-api/")
async def call_external_api():
    """HTTP call - use async."""
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        return response.json()

# ✅ Use def for CPU-bound operations
@router.get("/compute/")
def compute_heavy_task(n: int):
    """CPU-bound calculation - use regular def."""
    result = sum(i ** 2 for i in range(n))
    return {"result": result}

# ❌ Don't use async def without await
@router.get("/bad-async/")
async def bad_async():
    """No await here - should be def."""
    return {"message": "No async operations"}
```

### Async Database Operations

See `templates/async-database-repository.py` for complete example.

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        result = await self.db.execute(
            select(User).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def create(self, user_data: UserCreate) -> User:
        user = User(**user_data.model_dump())
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user
```

### Background Tasks

```python
from fastapi import BackgroundTasks

def send_email(email: str, message: str):
    """Blocking operation run in background."""
    # Send email (blocking I/O)
    pass

@router.post("/send-notification/")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(send_email, email, "Welcome!")
    return {"message": "Notification will be sent"}
```

### Avoiding Blocking Operations

```python
# ❌ Bad: Blocking operation in async function
@router.get("/bad-blocking/")
async def bad_blocking():
    time.sleep(5)  # Blocks entire event loop!
    return {"status": "done"}

# ✅ Good: Use asyncio.sleep for async delay
@router.get("/good-async/")
async def good_async():
    await asyncio.sleep(5)  # Non-blocking
    return {"status": "done"}

# ✅ Good: Run blocking code in thread pool
import asyncio
from functools import partial

def blocking_operation(data: str) -> str:
    # CPU-intensive or blocking operation
    time.sleep(2)
    return data.upper()

@router.post("/blocking-task/")
async def run_blocking_task(data: str):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, blocking_operation, data)
    return {"result": result}
```

## Database Integration

### SQLAlchemy Async Setup

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/db"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    pool_size=20,
    max_overflow=0,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    pass
```

### Database Models

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    items = relationship("Item", back_populates="owner")
```

### Repository Pattern

See `templates/repository-pattern.py` for complete example.

```python
from typing import Generic, TypeVar, Type, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def get(self, id: int) -> ModelType | None:
        result = await self.db.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def list(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        result = await self.db.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        obj = self.model(**obj_in.model_dump())
        self.db.add(obj)
        await self.db.flush()
        await self.db.refresh(obj)
        return obj

    async def update(self, id: int, obj_in: UpdateSchemaType) -> ModelType | None:
        db_obj = await self.get(id)
        if not db_obj:
            return None

        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        await self.db.flush()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, id: int) -> bool:
        db_obj = await self.get(id)
        if not db_obj:
            return False
        await self.db.delete(db_obj)
        return True
```

## Authentication & Authorization

### OAuth2 with Password Flow

See `templates/auth-dependencies.py` for complete example.

```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
```

### Role-Based Authorization

```python
from enum import Enum
from fastapi import Depends, HTTPException, status

class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

def require_role(required_role: Role):
    """Dependency factory for role-based authorization."""
    async def check_role(
        current_user: Annotated[User, Depends(get_current_active_user)]
    ):
        if current_user.role != required_role and current_user.role != Role.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return check_role

# Usage
@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    admin: Annotated[User, Depends(require_role(Role.ADMIN))]
):
    """Only admins can delete users."""
    # Delete user
    pass
```

## Error Handling

### HTTPException Usage

```python
from fastapi import HTTPException, status

@router.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return user

@router.post("/users/")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    # Create user
    pass
```

### Custom Exception Handlers

```python
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

class UserNotFoundError(Exception):
    def __init__(self, user_id: int):
        self.user_id = user_id

class InsufficientCreditsError(Exception):
    def __init__(self, required: int, available: int):
        self.required = required
        self.available = available

@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "UserNotFound",
            "message": f"User {exc.user_id} not found",
            "user_id": exc.user_id
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "ValidationError",
            "message": "Request validation failed",
            "details": exc.errors()
        }
    )
```

### Validation Error Responses

```python
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

try:
    user = UserCreate(**data)
except ValidationError as e:
    # Pydantic validation errors are automatically handled by FastAPI
    # Custom handling example:
    errors = e.errors()
    formatted_errors = [
        {
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        }
        for error in errors
    ]
    raise HTTPException(
        status_code=422,
        detail=formatted_errors
    )
```

## Testing

### TestClient Usage

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the API"}

def test_create_user():
    response = client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "TestPass123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
```

### Testing Async Endpoints

```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_async_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/users/")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_create_user_async():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/users/",
            json={"email": "test@example.com", "username": "test", "password": "Test123"}
        )
    assert response.status_code == 201
```

### Dependency Overrides for Testing

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.dependencies import get_db
from app.database import Base

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()

def test_create_user(client):
    response = client.post("/users/", json={"email": "test@test.com", "username": "test"})
    assert response.status_code == 201
```

### Mock External Services

```python
from unittest.mock import AsyncMock, patch
import pytest

@pytest.mark.asyncio
@patch("app.services.external_api.fetch_data")
async def test_endpoint_with_external_call(mock_fetch):
    # Mock the external API call
    mock_fetch.return_value = {"data": "mocked"}

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/external-data/")

    assert response.status_code == 200
    assert response.json() == {"data": "mocked"}
    mock_fetch.assert_called_once()
```

## Performance Optimization

### Response Caching

```python
from functools import lru_cache
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

@router.get("/items/{item_id}")
@cache(expire=60)  # Cache for 60 seconds
async def get_item(item_id: int):
    # Expensive operation
    item = await fetch_item_from_db(item_id)
    return item

# In-memory caching for config
@lru_cache()
def get_settings():
    return Settings()
```

### Database Query Optimization

```python
from sqlalchemy.orm import selectinload, joinedload

# ❌ Bad: N+1 query problem
async def get_users_with_items_bad(db: AsyncSession):
    result = await db.execute(select(User))
    users = result.scalars().all()
    # This will trigger N additional queries
    for user in users:
        items = user.items  # Lazy loading
    return users

# ✅ Good: Eager loading with selectinload
async def get_users_with_items_good(db: AsyncSession):
    result = await db.execute(
        select(User).options(selectinload(User.items))
    )
    users = result.scalars().all()
    # All data loaded in 2 queries
    return users

# ✅ Good: Use joinedload for one-to-one relationships
async def get_users_with_profile(db: AsyncSession):
    result = await db.execute(
        select(User).options(joinedload(User.profile))
    )
    return result.unique().scalars().all()
```

### Connection Pooling

```python
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,           # Number of persistent connections
    max_overflow=0,          # Additional connections when pool full
    pool_timeout=30,         # Timeout for getting connection from pool
    pool_recycle=3600,       # Recycle connections after 1 hour
    pool_pre_ping=True,      # Test connections before using
)
```

### Async for I/O Operations

```python
import httpx

# ❌ Bad: Synchronous HTTP calls in async function
@router.get("/sync-external/")
async def sync_external():
    results = []
    for url in urls:
        response = requests.get(url)  # Blocking!
        results.append(response.json())
    return results

# ✅ Good: Async HTTP calls
@router.get("/async-external/")
async def async_external():
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return [r.json() for r in responses]
```

## Common Anti-Patterns

### 1. Not Using Async Properly

```python
# ❌ Bad: async without await
@router.get("/bad/")
async def bad_endpoint():
    return {"data": compute_something()}  # No async operation

# ✅ Good: Use def for synchronous operations
@router.get("/good/")
def good_endpoint():
    return {"data": compute_something()}

# ❌ Bad: Blocking operations in async
@router.get("/blocking/")
async def blocking():
    time.sleep(5)  # Blocks event loop!
    return {"done": True}

# ✅ Good: Use await for async operations
@router.get("/non-blocking/")
async def non_blocking():
    await asyncio.sleep(5)
    return {"done": True}
```

### 2. Missing Type Hints

```python
# ❌ Bad: No type hints
@router.get("/users/{user_id}")
async def get_user(user_id):
    return await fetch_user(user_id)

# ✅ Good: Complete type hints
@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> UserResponse:
    return await fetch_user(db, user_id)
```

### 3. Not Using Dependency Injection

```python
# ❌ Bad: Creating connections in endpoints
@router.get("/users/")
async def get_users():
    db = create_db_connection()  # Don't do this!
    try:
        users = await db.execute(select(User))
        return users.scalars().all()
    finally:
        await db.close()

# ✅ Good: Use dependency injection
@router.get("/users/")
async def get_users(db: Annotated[AsyncSession, Depends(get_db)]):
    users = await db.execute(select(User))
    return users.scalars().all()
```

### 4. Not Using Pydantic Models for Validation

```python
# ❌ Bad: Manual validation
@router.post("/users/")
async def create_user(data: dict):
    if "email" not in data:
        raise HTTPException(400, "Email required")
    if not validate_email(data["email"]):
        raise HTTPException(400, "Invalid email")
    # More manual validation...

# ✅ Good: Pydantic model handles validation
@router.post("/users/")
async def create_user(user: UserCreate):
    # All validation done automatically
    return user
```

### 5. Missing Error Handling

```python
# ❌ Bad: No error handling
@router.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    return user  # Returns None if not found!

# ✅ Good: Proper error handling
@router.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    return user
```

### 6. Poor Response Model Design

```python
# ❌ Bad: Exposing sensitive data
class UserResponse(BaseModel):
    id: int
    email: str
    password: str  # Never expose passwords!
    hashed_password: str  # Don't expose this either!

# ✅ Good: Only expose safe fields
class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool
    created_at: datetime

# ❌ Bad: Inconsistent response models
@router.get("/users/")
async def list_users():
    return [{"id": 1, "name": "John"}, {"id": 2, "email": "jane@example.com"}]

# ✅ Good: Consistent, typed responses
@router.get("/users/", response_model=List[UserResponse])
async def list_users() -> List[UserResponse]:
    # Returns consistent structure
    pass
```

### 7. Ignoring Status Codes

```python
# ❌ Bad: Always returns 200
@router.post("/users/")
async def create_user(user: UserCreate):
    created_user = await create_user_in_db(user)
    return created_user  # Returns 200, should be 201

# ✅ Good: Appropriate status codes
@router.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    created_user = await create_user_in_db(user)
    return created_user
```

## Best Practices Summary

### Application Structure
1. Use router organization for modular code
2. Separate models (Pydantic) from schemas (ORM)
3. Implement repository pattern for data access
4. Keep business logic in service layer
5. Use environment-based configuration

### Path Operations
1. Always use `response_model` for type safety
2. Specify appropriate `status_code`
3. Add `summary` and `description` for documentation
4. Use `tags` to organize endpoints
5. Document error responses with `responses` parameter

### Models
1. Separate Create, Update, and Response models
2. Use field validation and validators
3. Never expose sensitive data in response models
4. Use `model_config` for examples and ORM mode
5. Leverage model inheritance for DRY code

### Dependencies
1. Use dependency injection for shared resources
2. Implement authentication as dependencies
3. Use `Annotated` for clean dependency syntax
4. Create reusable dependency factories
5. Use yield dependencies for cleanup

### Async
1. Use `async def` for I/O-bound operations
2. Use `def` for CPU-bound operations
3. Always await async operations
4. Never use blocking operations in async functions
5. Use background tasks for long operations

### Database
1. Use async database drivers (asyncpg, aiomysql)
2. Implement proper session management
3. Use connection pooling
4. Avoid N+1 queries with eager loading
5. Implement repository pattern

### Security
1. Hash passwords with bcrypt
2. Use JWT tokens for authentication
3. Implement proper CORS settings
4. Validate all inputs with Pydantic
5. Use dependency-based authorization

### Testing
1. Use `TestClient` for synchronous tests
2. Use `AsyncClient` for async endpoint tests
3. Override dependencies for testing
4. Mock external services
5. Test both success and error cases

### Performance
1. Use caching for expensive operations
2. Optimize database queries
3. Configure connection pooling
4. Use async for concurrent I/O
5. Monitor and profile performance

## Related Skills

- **python-async-patterns**: Deep dive into async/await patterns
- **python-type-hints-guide**: Type hints best practices
- **python-testing-standards**: Comprehensive testing guidelines

## References

- [FastAPI Official Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [SQLAlchemy Async Documentation](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
- [PEP 492 - Coroutines with async and await](https://peps.python.org/pep-0492/)

---

**Version:** 1.0
**Last Updated:** 2025-12-24
**Maintainer:** Claude Code Skills Team
