---
name: django-dev-ninja
description: |
  This skill should be used when the user asks to "create api endpoint", "django ninja",
  "django api", "add endpoint", "rest api django", "ninja router", "api schemas", or mentions
  API development, endpoint organization, or Pydantic schemas in Django projects. Provides
  Django Ninja patterns with 1-endpoint-per-file organization.
---

# Django Ninja API Development

Opinionated Django Ninja patterns with single-endpoint-per-file organization.

## Core Principles

1. **One endpoint = one file** - Each endpoint lives in its own file
2. **Logical grouping** - Endpoints grouped in subpackages by domain
3. **Router per group** - Each group has its own router
4. **Schemas in separate package** - Pydantic models in `schemas/`
5. **Services for logic** - Business logic in services, not endpoints

## API Structure

```
myapp/
├── api/
│   ├── __init__.py           # Main NinjaAPI instance
│   ├── users/
│   │   ├── __init__.py       # Router: users_router
│   │   ├── list.py           # GET /users/
│   │   ├── detail.py         # GET /users/{id}
│   │   ├── create.py         # POST /users/
│   │   ├── update.py         # PUT /users/{id}
│   │   └── delete.py         # DELETE /users/{id}
│   ├── products/
│   │   ├── __init__.py
│   │   ├── list.py
│   │   ├── detail.py
│   │   └── search.py
│   └── auth/
│       ├── __init__.py
│       ├── login.py
│       ├── logout.py
│       └── refresh.py
└── schemas/
    ├── __init__.py
    ├── user.py               # UserIn, UserOut, UserPatch
    ├── product.py
    └── common.py             # Pagination, errors
```

## Main API Setup

In `api/__init__.py`:

```python
from ninja import NinjaAPI
from ninja.security import HttpBearer

from .users import router as users_router
from .products import router as products_router
from .auth import router as auth_router


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        # Token validation logic
        from ..services.auth import AuthService
        return AuthService.validate_token(token)


api = NinjaAPI(
    title="My API",
    version="1.0.0",
    description="API documentation",
    auth=AuthBearer(),
)

# Register routers
api.add_router("/users", users_router, tags=["Users"])
api.add_router("/products", products_router, tags=["Products"])
api.add_router("/auth", auth_router, tags=["Authentication"], auth=None)
```

## Router Setup

Each group has a router in `__init__.py`:

```python
# api/users/__init__.py
from ninja import Router

from .list import router as list_router
from .detail import router as detail_router
from .create import router as create_router
from .update import router as update_router
from .delete import router as delete_router

router = Router()

# Merge endpoint routers
router.add_router("", list_router)
router.add_router("", detail_router)
router.add_router("", create_router)
router.add_router("", update_router)
router.add_router("", delete_router)
```

## Endpoint File Template

Each endpoint in its own file:

```python
# api/users/create.py
from ninja import Router
from django.http import HttpRequest

from ...schemas.user import UserIn, UserOut
from ...services.user import UserService

router = Router()


@router.post("/", response={201: UserOut})
def create_user(request: HttpRequest, payload: UserIn) -> UserOut:
    """Create a new user."""
    user = UserService.create(payload)
    return user
```

## Schema Organization

Pydantic schemas in `schemas/` package:

```python
# schemas/user.py
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Shared user fields."""
    email: EmailStr
    name: str = Field(max_length=255)


class UserIn(UserBase):
    """Input schema for creating users."""
    password: str = Field(min_length=8)


class UserPatch(BaseModel):
    """Partial update schema."""
    email: EmailStr | None = None
    name: str | None = Field(None, max_length=255)


class UserOut(UserBase):
    """Output schema for users."""
    id: UUID
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
```

## Common Patterns

### Pagination

```python
# schemas/common.py
from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    per_page: int
    pages: int
```

```python
# api/users/list.py
from ninja import Router, Query
from ...schemas.user import UserOut
from ...schemas.common import PaginatedResponse

router = Router()


@router.get("/", response=PaginatedResponse[UserOut])
def list_users(
    request,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
):
    """List users with pagination."""
    from ...services.user import UserService
    return UserService.list_paginated(page, per_page)
```

### Error Handling

```python
# schemas/common.py
class ErrorResponse(BaseModel):
    detail: str
    code: str | None = None


class ValidationErrorResponse(BaseModel):
    detail: list[dict]
```

```python
# api/users/detail.py
from ninja import Router
from django.http import Http404
from ...schemas.user import UserOut
from ...schemas.common import ErrorResponse

router = Router()


@router.get("/{user_id}", response={200: UserOut, 404: ErrorResponse})
def get_user(request, user_id: UUID):
    """Get user by ID."""
    from ...services.user import UserService

    user = UserService.get_by_id(user_id)
    if not user:
        return 404, {"detail": "User not found", "code": "USER_NOT_FOUND"}
    return user
```

### File Upload

```python
# api/files/upload.py
from ninja import Router, File, UploadedFile
from ...schemas.file import FileOut

router = Router()


@router.post("/upload", response=FileOut)
def upload_file(request, file: UploadedFile = File(...)):
    """Upload a file."""
    from ...services.file import FileService
    return FileService.save(file)
```

## URL Configuration

Register API in `urls.py`:

```python
# config/urls.py
from django.urls import path
from apps.myapp.api import api

urlpatterns = [
    path("api/", api.urls),
]
```

## Authentication Patterns

See `references/endpoints.md` for detailed authentication patterns including:
- JWT authentication
- API key authentication
- Session authentication
- Permission decorators

## Additional Resources

### Reference Files

- **`references/endpoints.md`** - Detailed endpoint patterns, authentication, permissions
- **`references/routers.md`** - Router organization, versioning, OpenAPI customization

### Related Skills

- **django-dev** - Core Django patterns and model organization
- **django-dev-test** - Testing API endpoints with pytest
