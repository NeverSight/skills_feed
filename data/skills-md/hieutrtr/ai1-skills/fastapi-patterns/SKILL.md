---
name: fastapi-patterns
description: >-
  FastAPI framework mechanics and advanced patterns. Use when configuring middleware,
  creating dependency injection chains, implementing WebSocket endpoints, customizing
  OpenAPI documentation, setting up CORS, building authentication dependencies (JWT
  validation, role-based access), implementing background tasks, or managing application
  lifespan (startup/shutdown). Does NOT cover basic endpoint CRUD or repository/service
  patterns (use python-backend-expert) or testing (use pytest-patterns).
license: MIT
compatibility: 'Python 3.12+, FastAPI 0.115+, Starlette'
metadata:
  author: platform-team
  version: '1.0.0'
  sdlc-phase: implementation
allowed-tools: Read Edit Write Bash(python:*) Bash(uvicorn:*)
context: fork
---

# FastAPI Patterns

## When to Use

Activate this skill when:
- Configuring FastAPI middleware (CORS, logging, timing, error handling)
- Creating complex dependency injection chains
- Implementing WebSocket endpoints with connection management
- Customizing OpenAPI documentation (tags, examples, deprecation)
- Setting up JWT authentication and role-based access dependencies
- Implementing background tasks (lightweight or distributed)
- Managing application lifecycle (startup/shutdown via lifespan)
- Setting up rate limiting or request throttling

Do NOT use this skill for:
- Basic endpoint CRUD, repository, or service patterns (use `python-backend-expert`)
- Writing tests for FastAPI endpoints (use `pytest-patterns`)
- API contract design or schema planning (use `api-design-patterns`)
- Architecture decisions (use `system-architecture`)

## Instructions

### Middleware Stack

Middleware executes in LIFO (Last In, First Out) order. The last middleware added is the outermost layer.

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Order matters: added last = executed first (outermost)
app.add_middleware(TimingMiddleware)          # 3rd added = runs 1st
app.add_middleware(RequestLoggingMiddleware)  # 2nd added = runs 2nd
app.add_middleware(                           # 1st added = runs 3rd (innermost)
    CORSMiddleware,
    allow_origins=["https://app.example.com"],  # NEVER use "*" in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

#### ASGI Middleware (Preferred)

Use pure ASGI middleware for performance-critical paths:

```python
from starlette.types import ASGIApp, Receive, Scope, Send
import time

class TimingMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start = time.perf_counter()
        await self.app(scope, receive, send)
        duration = time.perf_counter() - start
        # Log or record the duration
```

#### BaseHTTPMiddleware (Simpler but Slower)

Use only for middleware that needs to read/modify the request body or response:

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
```

**When to use which:**
- **ASGI middleware:** Performance-critical, no need to read request/response body
- **BaseHTTPMiddleware:** Need access to `Request`/`Response` objects, simpler API

### Authentication Dependencies

#### JWT Token Validation

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session),
) -> User:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await session.get(User, user_id)
    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    return user
```

#### Role-Based Access (Factory Pattern)

```python
def require_role(*roles: str):
    """Factory that creates a dependency requiring specific roles."""
    async def check_role(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(
                status_code=403,
                detail=f"Requires one of: {', '.join(roles)}",
            )
        return user
    return check_role

# Usage in routes
@router.delete("/users/{user_id}", dependencies=[Depends(require_role("admin"))])
async def delete_user(user_id: int, ...) -> None:
    ...

@router.patch("/posts/{post_id}")
async def update_post(
    post_id: int,
    user: User = Depends(require_role("admin", "editor")),
) -> PostResponse:
    ...
```

### Dependency Injection Chains

#### Caching Behavior

FastAPI caches dependency results within a single request. The same dependency called multiple times returns the same instance:

```python
# get_async_session is called once per request, even if used by multiple deps
async def get_user_service(session: AsyncSession = Depends(get_async_session)) -> UserService:
    return UserService(session)

async def get_post_service(session: AsyncSession = Depends(get_async_session)) -> PostService:
    return PostService(session)  # Same session instance as user_service
```

To disable caching (get a new instance each time), use `use_cache=False`:
```python
session: AsyncSession = Depends(get_async_session, use_cache=False)
```

#### Yield Dependencies (Resource Cleanup)

```python
async def get_http_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient(timeout=30.0) as client:
        yield client
    # Client is automatically closed after the request
```

#### Overriding Dependencies in Tests

```python
# In tests
from app.main import app
from app.dependencies.auth import get_current_user

async def mock_current_user() -> User:
    return User(id=1, email="test@example.com", role="admin")

app.dependency_overrides[get_current_user] = mock_current_user
```

### Background Tasks

#### FastAPI BackgroundTasks (Lightweight)

For tasks that don't need to survive server restarts:

```python
from fastapi import BackgroundTasks

@router.post("/users", status_code=201)
async def create_user(
    data: UserCreate,
    background_tasks: BackgroundTasks,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    user = await service.create_user(data)
    background_tasks.add_task(send_welcome_email, user.email)
    return UserResponse.model_validate(user)

async def send_welcome_email(email: str) -> None:
    """Runs after the response is sent. Creates its own session."""
    async with async_session_factory() as session:
        async with session.begin():
            # Send email, log activity, etc.
            ...
```

**Rules:**
- Never reuse the request session in background tasks — create a new one
- Background tasks run in the same process — no retry, no persistence
- Use Celery or similar for tasks that need reliability, retry, or distribution

### WebSocket Pattern

```python
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self) -> None:
        self.active: dict[int, list[WebSocket]] = {}

    async def connect(self, user_id: int, ws: WebSocket) -> None:
        await ws.accept()
        self.active.setdefault(user_id, []).append(ws)

    def disconnect(self, user_id: int, ws: WebSocket) -> None:
        if user_id in self.active:
            self.active[user_id].remove(ws)
            if not self.active[user_id]:
                del self.active[user_id]

    async def send_to_user(self, user_id: int, message: dict) -> None:
        for ws in self.active.get(user_id, []):
            await ws.send_json(message)

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket, token: str) -> None:
    # Auth via query parameter: /ws?token=xxx
    user = await verify_ws_token(token)
    if not user:
        await ws.close(code=4001)
        return

    await manager.connect(user.id, ws)
    try:
        while True:
            data = await ws.receive_json()
            # Process incoming messages
            await handle_message(user.id, data)
    except WebSocketDisconnect:
        manager.disconnect(user.id, ws)
```

**WebSocket auth approaches:**
1. Query parameter: `ws://host/ws?token=xxx` (simplest, token visible in logs)
2. First message: Connect, then send token as first message (more secure)
3. Cookie: Use existing session cookie (requires same domain)

### Application Lifespan

Use the `lifespan` context manager (not deprecated `on_event`):

```python
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Startup: initialize resources
    await init_database()
    redis = await aioredis.from_url(settings.redis_url)
    app.state.redis = redis

    yield  # Application runs here

    # Shutdown: cleanup resources
    await redis.close()
    await dispose_engine()

app = FastAPI(lifespan=lifespan)
```

**Lifespan responsibilities:**
- Database connection pool initialization and disposal
- Redis/cache connection setup and teardown
- HTTP client pool creation
- Background scheduler startup/shutdown
- Cache warmup on startup

### Exception Handlers

Register global exception handlers for consistent error responses:

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "code": "VALIDATION_ERROR",
            "field_errors": [
                {"field": e["loc"][-1], "message": e["msg"], "code": e["type"]}
                for e in exc.errors()
            ],
        },
    )
```

### OpenAPI Customization

```python
app = FastAPI(
    title="My API",
    version="1.0.0",
    description="API description with **markdown** support",
    openapi_tags=[
        {"name": "Users", "description": "User management operations"},
        {"name": "Auth", "description": "Authentication endpoints"},
    ],
    docs_url="/docs",        # Swagger UI
    redoc_url="/redoc",      # ReDoc
    openapi_url="/openapi.json",
)
```

## Examples

### JWT Auth Dependency Chain

Complete auth chain from token to authorized user:

```
Request with Authorization: Bearer <token>
    ↓
oauth2_scheme (extracts token from header)
    ↓
get_current_user (decodes JWT, loads user from DB)
    ↓
require_role("admin") (checks user.role)
    ↓
Route handler (receives verified admin user)
```

Each dependency in the chain is independently testable via `dependency_overrides`.

## Edge Cases

- **Middleware vs dependency:** Use middleware for cross-cutting concerns (logging, timing, CORS). Use dependencies for per-route logic (auth, pagination params, feature flags).

- **ASGI vs BaseHTTPMiddleware:** Prefer ASGI middleware for performance. `BaseHTTPMiddleware` reads the entire response body into memory, causing issues with streaming and large responses.

- **Lifespan vs on_event:** Always use the `lifespan` context manager. `@app.on_event("startup")` and `@app.on_event("shutdown")` are deprecated in FastAPI 0.109+.

- **Depends caching across sub-applications:** Dependency caching works per-request within a single app instance. If using `app.mount()` for sub-applications, each sub-app has its own dependency resolution scope.

- **WebSocket scaling:** A single server instance holds all WebSocket connections. For multi-instance deployments, use Redis pub/sub to broadcast messages across instances.

See `references/middleware-examples.md` for complete middleware implementations.
See `references/dependency-injection-patterns.md` for advanced DI patterns.
