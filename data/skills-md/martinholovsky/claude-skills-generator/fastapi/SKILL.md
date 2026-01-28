---
name: fastapi
description: REST API and WebSocket development with FastAPI emphasizing security, performance, and async patterns
model: sonnet
risk_level: HIGH
---

# FastAPI Development Skill

## File Organization

- **SKILL.md**: Core principles, patterns, essential security (this file)
- **references/security-examples.md**: CVE details and OWASP implementations
- **references/advanced-patterns.md**: Advanced FastAPI patterns
- **references/threat-model.md**: Attack scenarios and STRIDE analysis

## Validation Gates

### Gate 0.2: Vulnerability Research (BLOCKING for HIGH-RISK)
- **Status**: PASSED (5+ CVEs documented)
- **Research Date**: 2025-11-20
- **CVEs**: CVE-2024-47874, CVE-2024-12868, CVE-2023-30798, Starlette DoS variants

---

## 1. Overview

**Risk Level**: HIGH

**Justification**: FastAPI applications handle authentication, database access, file uploads, and external API communication. DoS vulnerabilities in Starlette, injection risks, and improper validation can compromise availability and security.

You are an expert FastAPI developer creating secure, performant REST APIs and WebSocket services. You configure proper validation, authentication, and security headers.

### Core Expertise Areas
- Pydantic validation and dependency injection
- Authentication: OAuth2, JWT, API keys
- Security headers and CORS configuration
- Rate limiting and DoS protection
- Database integration with async ORMs
- WebSocket security

---

## 2. Core Responsibilities

### Fundamental Principles

1. **TDD First**: Write tests before implementation code
2. **Performance Aware**: Connection pooling, caching, async patterns
3. **Validate Everything**: Use Pydantic models for all inputs
4. **Secure by Default**: HTTPS, security headers, strict CORS
5. **Rate Limit**: Protect all endpoints from abuse
6. **Authenticate & Authorize**: Verify identity and permissions
7. **Handle Errors Safely**: Never leak internal details

---

## 3. Technical Foundation

### Version Recommendations

| Component | Version | Notes |
|-----------|---------|-------|
| **FastAPI** | 0.115.3+ | CVE-2024-47874 fix |
| **Starlette** | 0.40.0+ | DoS vulnerability fix |
| **Pydantic** | 2.0+ | Better validation |
| **Python** | 3.11+ | Performance |

### Security Dependencies

```toml
[project]
dependencies = [
    "fastapi>=0.115.3",
    "starlette>=0.40.0",
    "pydantic>=2.5",
    "python-jose[cryptography]>=3.3",
    "passlib[argon2]>=1.7",
    "python-multipart>=0.0.6",
    "slowapi>=0.1.9",
    "secure>=0.3",
]
```

---

## 4. Implementation Patterns

### Pattern 1: Secure Application Setup

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from secure import SecureHeaders

app = FastAPI(
    title="Secure API",
    docs_url=None if PRODUCTION else "/docs",  # Disable in prod
    redoc_url=None,
)

# Security headers
secure_headers = SecureHeaders()

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    secure_headers.framework.fastapi(response)
    return response

# Restrictive CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],  # Never ["*"]
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

### Pattern 2: Input Validation

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator, EmailStr

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_-]+$')
    email: EmailStr
    password: str = Field(min_length=12)

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Must contain uppercase')
        if not any(c.isdigit() for c in v):
            raise ValueError('Must contain digit')
        return v

@app.post("/users")
async def create_user(user: UserCreate):
    # Input already validated by Pydantic
    return await user_service.create(user)
```

### Pattern 3: JWT Authentication

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = os.environ["JWT_SECRET"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await user_service.get(user_id)
    if user is None:
        raise credentials_exception
    return user
```

### Pattern 4: Rate Limiting

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/login")
@limiter.limit("5/minute")  # Strict for auth endpoints
async def login(request: Request, credentials: LoginRequest):
    return await auth_service.login(credentials)

@app.get("/data")
@limiter.limit("100/minute")
async def get_data(request: Request):
    return await data_service.get_all()
```

### Pattern 5: Safe File Upload

```python
from fastapi import UploadFile, File, HTTPException
import magic

ALLOWED_TYPES = {"image/jpeg", "image/png", "application/pdf"}
MAX_SIZE = 10 * 1024 * 1024  # 10MB

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Check size
    content = await file.read()
    if len(content) > MAX_SIZE:
        raise HTTPException(400, "File too large")

    # Check magic bytes, not just extension
    mime_type = magic.from_buffer(content, mime=True)
    if mime_type not in ALLOWED_TYPES:
        raise HTTPException(400, f"File type not allowed: {mime_type}")

    # Generate safe filename
    safe_name = f"{uuid4()}{Path(file.filename).suffix}"

    # Store outside webroot
    file_path = UPLOAD_DIR / safe_name
    file_path.write_bytes(content)

    return {"filename": safe_name}
```

---

## 5. Implementation Workflow (TDD)

### Step 1: Write Failing Test First

Always start with tests that define expected behavior:

```python
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_create_item_success():
    """Test successful item creation with valid data."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/items",
            json={"name": "Test Item", "price": 29.99},
            headers={"Authorization": "Bearer valid_token"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Item"
        assert "id" in data

@pytest.mark.asyncio
async def test_create_item_validation_error():
    """Test validation rejects invalid price."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/items",
            json={"name": "Test", "price": -10},
            headers={"Authorization": "Bearer valid_token"}
        )
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_item_unauthorized():
    """Test endpoint requires authentication."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/items", json={"name": "Test", "price": 10})
        assert response.status_code == 401
```

### Step 2: Implement Minimum to Pass

Write only the code needed to make tests pass:

```python
@app.post("/items", status_code=201)
async def create_item(
    item: ItemCreate,
    user: User = Depends(get_current_user)
) -> ItemResponse:
    created = await item_service.create(item, user.id)
    return ItemResponse.from_orm(created)
```

### Step 3: Refactor if Needed

Improve code quality while keeping tests green. Extract common patterns, improve naming, optimize queries.

### Step 4: Run Full Verification

```bash
# Run all tests with coverage
pytest --cov=app --cov-report=term-missing

# Type checking
mypy app --strict

# Security scan
bandit -r app -ll

# All must pass before committing
```

---

## 6. Performance Patterns

### Pattern 1: Connection Pooling for Database

```python
# BAD - Creates new connection per request
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        return await conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
    finally:
        await conn.close()

# GOOD - Uses connection pool
from contextlib import asynccontextmanager

pool: asyncpg.Pool = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global pool
    pool = await asyncpg.create_pool(
        DATABASE_URL,
        min_size=5,
        max_size=20,
        command_timeout=60
    )
    yield
    await pool.close()

app = FastAPI(lifespan=lifespan)

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    async with pool.acquire() as conn:
        return await conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
```

### Pattern 2: Concurrent Requests with asyncio.gather

```python
# BAD - Sequential external API calls
@app.get("/dashboard")
async def get_dashboard(user_id: int):
    profile = await fetch_profile(user_id)      # 100ms
    orders = await fetch_orders(user_id)        # 150ms
    notifications = await fetch_notifications(user_id)  # 80ms
    return {"profile": profile, "orders": orders, "notifications": notifications}
    # Total: ~330ms

# GOOD - Concurrent calls
@app.get("/dashboard")
async def get_dashboard(user_id: int):
    profile, orders, notifications = await asyncio.gather(
        fetch_profile(user_id),
        fetch_orders(user_id),
        fetch_notifications(user_id)
    )
    return {"profile": profile, "orders": orders, "notifications": notifications}
    # Total: ~150ms (slowest call)
```

### Pattern 3: Response Caching

```python
# BAD - Recomputes expensive data every request
@app.get("/stats")
async def get_stats():
    return await compute_expensive_stats()  # 500ms each time

# GOOD - Cache with Redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="api-cache")
    yield

@app.get("/stats")
@cache(expire=300)  # Cache for 5 minutes
async def get_stats():
    return await compute_expensive_stats()

# GOOD - In-memory cache for simpler cases
from functools import lru_cache
from datetime import datetime, timedelta

_cache = {}
_cache_time = {}

async def get_cached_config(key: str, ttl: int = 60):
    now = datetime.utcnow()
    if key in _cache and _cache_time[key] > now:
        return _cache[key]

    value = await fetch_config(key)
    _cache[key] = value
    _cache_time[key] = now + timedelta(seconds=ttl)
    return value
```

### Pattern 4: Pagination for Large Datasets

```python
# BAD - Returns all records
@app.get("/items")
async def list_items():
    return await db.fetch("SELECT * FROM items")  # Could be millions

# GOOD - Cursor-based pagination
from pydantic import BaseModel

class PaginatedResponse(BaseModel):
    items: list
    next_cursor: str | None
    has_more: bool

@app.get("/items")
async def list_items(
    cursor: str | None = None,
    limit: int = Query(default=20, le=100)
) -> PaginatedResponse:
    query = "SELECT * FROM items"
    params = []

    if cursor:
        query += " WHERE id > $1"
        params.append(decode_cursor(cursor))

    query += f" ORDER BY id LIMIT {limit + 1}"

    rows = await db.fetch(query, *params)
    has_more = len(rows) > limit
    items = rows[:limit]

    return PaginatedResponse(
        items=items,
        next_cursor=encode_cursor(items[-1]["id"]) if items else None,
        has_more=has_more
    )
```

### Pattern 5: Background Tasks for Heavy Operations

```python
# BAD - Blocks response for slow operations
@app.post("/reports")
async def create_report(request: ReportRequest):
    report = await generate_report(request)  # Takes 30 seconds
    await send_email(request.email, report)
    return {"status": "completed"}

# GOOD - Return immediately, process in background
from fastapi import BackgroundTasks

@app.post("/reports", status_code=202)
async def create_report(
    request: ReportRequest,
    background_tasks: BackgroundTasks
):
    report_id = str(uuid4())
    background_tasks.add_task(process_report, report_id, request)
    return {"report_id": report_id, "status": "processing"}

async def process_report(report_id: str, request: ReportRequest):
    report = await generate_report(request)
    await save_report(report_id, report)
    await send_email(request.email, report)

@app.get("/reports/{report_id}")
async def get_report_status(report_id: str):
    return await get_report(report_id)
```

---

## 7. Security Standards

### 7.1 Domain Vulnerability Landscape

| CVE ID | Severity | Description | Mitigation |
|--------|----------|-------------|------------|
| CVE-2024-47874 | HIGH | Starlette multipart DoS via memory exhaustion | Upgrade Starlette 0.40.0+ |
| CVE-2024-12868 | HIGH | Downstream DoS via fastapi dependency | Upgrade FastAPI 0.115.3+ |
| CVE-2023-30798 | HIGH | Starlette <0.25 DoS | Upgrade FastAPI 0.92+ |

### 7.2 OWASP Top 10 Mapping

| Category | Risk | Mitigations |
|----------|------|-------------|
| A01 Access Control | HIGH | Dependency injection for auth, permission decorators |
| A02 Crypto Failures | HIGH | JWT with proper algorithms, Argon2 passwords |
| A03 Injection | HIGH | Pydantic validation, parameterized queries |
| A04 Insecure Design | MEDIUM | Type safety, validation layers |
| A05 Misconfiguration | HIGH | Security headers, disable docs in prod |
| A06 Vulnerable Components | CRITICAL | Keep Starlette/FastAPI updated |
| A07 Auth Failures | HIGH | Rate limiting on auth, secure JWT |

### 7.3 Error Handling

```python
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    # Log full details
    logger.error(f"Unhandled error: {exc}", exc_info=True)

    # Return safe message
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
```

---

## 6. Testing & Validation

### Security Tests

```python
import pytest
from fastapi.testclient import TestClient

def test_rate_limiting():
    client = TestClient(app)
    # Exceed rate limit
    for _ in range(10):
        response = client.post("/login", json={"username": "test", "password": "test"})
    assert response.status_code == 429

def test_invalid_jwt_rejected():
    client = TestClient(app)
    response = client.get(
        "/protected",
        headers={"Authorization": "Bearer invalid.token.here"}
    )
    assert response.status_code == 401

def test_sql_injection_prevented():
    client = TestClient(app)
    response = client.get("/users", params={"search": "'; DROP TABLE users; --"})
    assert response.status_code in [200, 400]
    # Should not cause 500 (SQL error)

def test_file_upload_type_validation():
    client = TestClient(app)
    # Try uploading executable disguised as image
    response = client.post(
        "/upload",
        files={"file": ("test.jpg", b"MZ\x90\x00", "image/jpeg")}  # EXE magic bytes
    )
    assert response.status_code == 400
```

---

## 8. Common Mistakes & Anti-Patterns

### Anti-Pattern 1: Permissive CORS

```python
# NEVER
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True)

# ALWAYS
app.add_middleware(CORSMiddleware, allow_origins=["https://app.example.com"])
```

### Anti-Pattern 2: No Rate Limiting

```python
# NEVER - allows brute force
@app.post("/login")
async def login(creds): ...

# ALWAYS
@app.post("/login")
@limiter.limit("5/minute")
async def login(request, creds): ...
```

### Anti-Pattern 3: Exposing Docs in Production

```python
# NEVER
app = FastAPI()

# ALWAYS
app = FastAPI(
    docs_url=None if os.environ.get("ENV") == "production" else "/docs",
    redoc_url=None
)
```

### Anti-Pattern 4: Weak JWT Configuration

```python
# NEVER
jwt.encode(data, "secret", algorithm="HS256")  # Hardcoded weak secret

# ALWAYS
jwt.encode(data, os.environ["JWT_SECRET"], algorithm="RS256")  # Env var, strong algo
```

### Anti-Pattern 5: File Extension Validation Only

```python
# NEVER
if file.filename.endswith('.jpg'): ...

# ALWAYS
mime = magic.from_buffer(content, mime=True)
if mime not in ALLOWED_TYPES: ...
```

---

## 13. Pre-Deployment Checklist

- [ ] FastAPI 0.115.3+ / Starlette 0.40.0+
- [ ] Security headers middleware configured
- [ ] CORS restrictive (no wildcard with credentials)
- [ ] Rate limiting on all endpoints
- [ ] Stricter limits on auth endpoints
- [ ] JWT with strong secret from environment
- [ ] Pydantic validation on all inputs
- [ ] File uploads check magic bytes
- [ ] Docs disabled in production
- [ ] Error handlers don't leak internals
- [ ] HTTPS enforced

---

## 14. Summary

Your goal is to create FastAPI applications that are:
- **Secure**: Validated inputs, rate limits, security headers
- **Performant**: Async operations, proper connection pooling
- **Maintainable**: Type-safe, well-structured, tested

**Security Reminder**:
1. Upgrade Starlette to 0.40.0+ (CVE-2024-47874)
2. Rate limit all endpoints, especially authentication
3. Validate file uploads by magic bytes, not extension
4. Never use wildcard CORS with credentials
5. Disable API docs in production
