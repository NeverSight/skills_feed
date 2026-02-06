---
name: debug:fastapi
description: Debug FastAPI applications systematically with this comprehensive troubleshooting skill. Covers async/await issues, Pydantic validation errors (422 responses), dependency injection failures, CORS configuration problems, database session management, and circular import resolution. Provides structured four-phase debugging methodology with FastAPI-specific tools including uvicorn logging, OpenAPI docs, and middleware debugging patterns.
---

# FastAPI Debugging Guide

## Overview

This skill provides a systematic approach to debugging FastAPI applications. FastAPI is built on Starlette and Pydantic, which means debugging often involves understanding async behavior, request validation, and dependency injection patterns.

**When to use this skill:**
- 422 Unprocessable Entity errors
- Pydantic ValidationError exceptions
- Async/await related issues
- Dependency injection failures
- CORS errors in browser
- 500 Internal Server Errors
- Database session/connection issues
- Circular import errors on startup

## Common Error Patterns

### 1. Pydantic ValidationError (422 Unprocessable Entity)

**Symptoms:**
- API returns 422 status code
- Response contains `detail` array with validation errors
- Client receives "field required" or "type error" messages

**Root Causes:**
- Missing required fields in request body
- Incorrect data types (string instead of int, etc.)
- Invalid enum values
- Nested model validation failures

**Debugging Steps:**
```python
# 1. Check the exact error response
{
    "detail": [
        {
            "loc": ["body", "field_name"],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]
}

# 2. Validate your Pydantic model directly
from pydantic import BaseModel, ValidationError

class UserCreate(BaseModel):
    name: str
    email: str
    age: int

try:
    user = UserCreate(**your_data)
except ValidationError as e:
    print(e.json())  # Detailed error info

# 3. Use Optional for non-required fields
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: str
    age: Optional[int] = None  # Now optional with default
```

### 2. 500 Internal Server Error

**Symptoms:**
- Generic "Internal Server Error" response
- No detailed error in API response
- Error details only in server logs

**Root Causes:**
- Unhandled exceptions in endpoint code
- Database connection failures
- Dependency injection failures
- Division by zero, null attribute access
- External service timeouts

**Debugging Steps:**
```python
# 1. Add exception logging middleware
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.middleware("http")
async def log_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.exception(f"Unhandled exception: {e}")
        raise

# 2. Add global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}  # Only in dev!
    )

# 3. Check dependency injection
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"DB error: {e}")
        raise
    finally:
        db.close()
```

### 3. Async/Await Issues

**Symptoms:**
- `RuntimeError: Event loop is already running`
- `RuntimeWarning: coroutine was never awaited`
- Blocking behavior in async endpoints
- `TypeError: object X can't be used in 'await' expression`

**Root Causes:**
- Mixing sync and async code incorrectly
- Using blocking I/O in async functions
- Missing await keywords
- Sync database calls in async context

**Debugging Steps:**
```python
# 1. Check for missing await
# Wrong
@app.get("/users")
async def get_users():
    users = db.get_users()  # If async, needs await!
    return users

# Correct
@app.get("/users")
async def get_users():
    users = await db.get_users()
    return users

# 2. Don't use blocking I/O in async functions
# Wrong - blocks event loop
@app.get("/data")
async def get_data():
    import time
    time.sleep(5)  # BLOCKS!
    return {"data": "done"}

# Correct - use asyncio.sleep or run_in_executor
import asyncio
@app.get("/data")
async def get_data():
    await asyncio.sleep(5)  # Non-blocking
    return {"data": "done"}

# 3. For sync database operations, use def instead of async def
@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    # FastAPI runs sync functions in threadpool
    return db.query(User).all()
```

### 4. Dependency Injection Errors

**Symptoms:**
- `TypeError: X() takes Y positional arguments but Z were given`
- Dependencies not being called
- `ValidationError` from dependency parameters

**Debugging Steps:**
```python
# 1. Ensure Depends() is used correctly
from fastapi import Depends

# Wrong - function is called immediately
@app.get("/items")
def get_items(db = get_db()):  # WRONG!
    pass

# Correct - FastAPI manages the dependency
@app.get("/items")
def get_items(db = Depends(get_db)):
    pass

# 2. Debug dependency chain
def get_settings():
    print("Loading settings...")  # Debug print
    return Settings()

def get_db(settings: Settings = Depends(get_settings)):
    print(f"Connecting to {settings.db_url}")  # Debug print
    return create_engine(settings.db_url)

# 3. Handle dependency failures gracefully
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        user = await verify_token(token)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user
    except Exception as e:
        logger.error(f"Auth failed: {e}")
        raise HTTPException(status_code=401, detail="Authentication failed")
```

### 5. CORS Problems

**Symptoms:**
- Browser console shows CORS errors
- API works in Postman but not browser
- Preflight OPTIONS requests failing

**Debugging Steps:**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 1. Add CORS middleware (MUST be before routes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Or ["*"] for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Debug: Log all requests
@app.middleware("http")
async def log_requests(request, call_next):
    print(f"Origin: {request.headers.get('origin')}")
    print(f"Method: {request.method}")
    response = await call_next(request)
    print(f"CORS headers: {dict(response.headers)}")
    return response

# 3. Common issues:
# - allow_origins must match EXACTLY (including protocol and port)
# - allow_credentials=True requires specific origins (not "*")
# - Check if middleware order is correct
```

### 6. Database Session Issues

**Symptoms:**
- `sqlalchemy.exc.InvalidRequestError: This Session's transaction has been rolled back`
- Database connections exhausted
- Stale data being returned

**Debugging Steps:**
```python
from sqlalchemy.orm import Session
from contextlib import contextmanager

# 1. Proper session management
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()  # Commit on success
    except Exception:
        db.rollback()  # Rollback on error
        raise
    finally:
        db.close()  # Always close

# 2. Check connection pool settings
from sqlalchemy import create_engine

engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_pre_ping=True,  # Test connections before use
    echo=True,  # Log all SQL (debug only!)
)

# 3. Debug session state
@app.get("/debug-db")
def debug_db(db: Session = Depends(get_db)):
    print(f"Session active: {db.is_active}")
    print(f"Session dirty: {db.dirty}")
    print(f"Session new: {db.new}")
    return {"status": "ok"}
```

### 7. Circular Import Errors

**Symptoms:**
- `ImportError: cannot import name 'X' from partially initialized module`
- Application fails to start
- `AttributeError: module has no attribute`

**Debugging Steps:**
```python
# 1. Identify the circular dependency
# app/models.py
from app.schemas import UserSchema  # Imports schemas

# app/schemas.py
from app.models import User  # Imports models - CIRCULAR!

# 2. Solution: Use TYPE_CHECKING
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import User

# 3. Or use string annotations
class UserSchema(BaseModel):
    user: "User"  # Forward reference

# 4. Or restructure: Move shared code to separate module
# app/base.py - Contains shared Base class
# app/models.py - Imports from base
# app/schemas.py - Imports from base
```

## Debugging Tools

### 1. Python Debugger (pdb/breakpoint)

```python
# Insert breakpoint in your code
@app.get("/debug")
def debug_endpoint():
    data = fetch_data()
    breakpoint()  # Execution stops here
    return process(data)

# Run with: uvicorn main:app --reload
# When breakpoint hits, use pdb commands:
# n - next line
# s - step into
# c - continue
# p variable - print variable
# l - list code around current line
# q - quit debugger
```

### 2. Uvicorn with Reload

```bash
# Development server with auto-reload
uvicorn main:app --reload --log-level debug

# With specific host/port
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Show access logs
uvicorn main:app --reload --access-log
```

### 3. OpenAPI /docs Endpoint

```python
# FastAPI auto-generates interactive docs
# Access at: http://localhost:8000/docs (Swagger UI)
# Or: http://localhost:8000/redoc (ReDoc)

# Customize docs
app = FastAPI(
    title="My API",
    description="Debug info here",
    docs_url="/docs",  # Or None to disable
    redoc_url="/redoc",
)

# Test endpoints directly in browser!
```

### 4. Logging Module

```python
import logging
from fastapi import FastAPI

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.on_event("startup")
async def startup():
    logger.info("Application starting...")

@app.get("/")
def root():
    logger.debug("Root endpoint called")
    logger.info("Processing request")
    return {"status": "ok"}
```

### 5. httpx for Testing

```python
# tests/test_api.py
import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/users")
        assert response.status_code == 200
        print(response.json())  # Debug output

# Sync testing with TestClient
from fastapi.testclient import TestClient

def test_sync():
    client = TestClient(app)
    response = client.get("/users")
    assert response.status_code == 200
```

### 6. VS Code Debugging

```json
// .vscode/launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "FastAPI",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": ["main:app", "--reload"],
            "jinja": true,
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        }
    ]
}
```

### 7. Debug Middleware

```python
from starlette.middleware.base import BaseHTTPMiddleware
import time

class DebugMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Log request details
        print(f"Request: {request.method} {request.url}")
        print(f"Headers: {dict(request.headers)}")

        # Time the request
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start

        print(f"Response: {response.status_code} in {duration:.3f}s")
        return response

app.add_middleware(DebugMiddleware)
```

## The Four Phases of FastAPI Debugging

### Phase 1: Reproduce and Identify

1. **Reproduce the error consistently**
   ```bash
   # Use curl to reproduce
   curl -X POST http://localhost:8000/api/users \
     -H "Content-Type: application/json" \
     -d '{"name": "test"}'
   ```

2. **Check the error response**
   ```python
   # 422 = Validation error (check Pydantic model)
   # 401/403 = Auth issue (check dependencies)
   # 500 = Server error (check logs)
   # 404 = Route not found (check URL and method)
   ```

3. **Review server logs**
   ```bash
   # Check uvicorn output
   uvicorn main:app --log-level debug
   ```

### Phase 2: Isolate the Problem

1. **Simplify the endpoint**
   ```python
   @app.post("/api/users")
   async def create_user(user: UserCreate, db: Session = Depends(get_db)):
       # Comment out sections to isolate
       # return {"debug": "step 1"}

       # Check user data
       print(f"User data: {user.dict()}")

       # Check db connection
       print(f"DB connected: {db.is_active}")

       return create_user_in_db(db, user)
   ```

2. **Test dependencies individually**
   ```python
   # Test in Python shell
   from app.dependencies import get_db
   db = next(get_db())
   print(db.execute("SELECT 1").scalar())
   ```

3. **Validate request data**
   ```python
   @app.post("/api/users")
   async def create_user(request: Request):
       body = await request.json()
       print(f"Raw body: {body}")

       # Try manual validation
       from app.schemas import UserCreate
       user = UserCreate(**body)  # Will raise if invalid
       return {"validated": user.dict()}
   ```

### Phase 3: Fix and Verify

1. **Apply the fix**
   ```python
   # Before
   class UserCreate(BaseModel):
       name: str
       email: str

   # After (with proper validation)
   from pydantic import BaseModel, EmailStr, validator

   class UserCreate(BaseModel):
       name: str
       email: EmailStr

       @validator('name')
       def name_not_empty(cls, v):
           if not v.strip():
               raise ValueError('Name cannot be empty')
           return v
   ```

2. **Test the fix**
   ```bash
   # Test valid request
   curl -X POST http://localhost:8000/api/users \
     -H "Content-Type: application/json" \
     -d '{"name": "John", "email": "john@example.com"}'

   # Test edge cases
   curl -X POST http://localhost:8000/api/users \
     -H "Content-Type: application/json" \
     -d '{"name": "", "email": "invalid"}'
   ```

### Phase 4: Prevent Regression

1. **Add tests**
   ```python
   def test_create_user_valid():
       response = client.post("/api/users", json={
           "name": "John",
           "email": "john@example.com"
       })
       assert response.status_code == 200

   def test_create_user_invalid_email():
       response = client.post("/api/users", json={
           "name": "John",
           "email": "invalid"
       })
       assert response.status_code == 422
   ```

2. **Add error handling**
   ```python
   from fastapi import HTTPException

   @app.post("/api/users")
   async def create_user(user: UserCreate, db: Session = Depends(get_db)):
       try:
           return create_user_in_db(db, user)
       except IntegrityError:
           raise HTTPException(status_code=409, detail="User already exists")
       except Exception as e:
           logger.exception("Failed to create user")
           raise HTTPException(status_code=500, detail="Internal error")
   ```

## Quick Reference Commands

### Starting and Running

```bash
# Development server
uvicorn main:app --reload --log-level debug

# With custom host/port
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production (multiple workers)
uvicorn main:app --workers 4

# With gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Testing Endpoints

```bash
# GET request
curl http://localhost:8000/api/users

# POST with JSON
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "test", "email": "test@example.com"}'

# With authentication
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:8000/api/protected

# Verbose output for debugging
curl -v http://localhost:8000/api/users
```

### Python Debugging

```python
# Insert breakpoint
breakpoint()

# Or use pdb directly
import pdb; pdb.set_trace()

# Quick debug print
print(f"DEBUG: {variable=}")  # Python 3.8+ f-string debugging

# Log at debug level
import logging
logging.debug(f"Variable value: {variable}")
```

### Database Debugging

```python
# Enable SQLAlchemy echo
engine = create_engine(DATABASE_URL, echo=True)

# Check session state
print(f"Session: dirty={db.dirty}, new={db.new}, deleted={db.deleted}")

# Raw SQL for debugging
result = db.execute("SELECT * FROM users WHERE id = :id", {"id": 1})
print(result.fetchall())
```

### Async Debugging

```python
# Check if running in async context
import asyncio
try:
    loop = asyncio.get_running_loop()
    print(f"Running in event loop: {loop}")
except RuntimeError:
    print("No event loop running")

# Debug coroutines
import asyncio
asyncio.run(your_async_function())
```

### Environment and Configuration

```bash
# Check Python environment
python -c "import fastapi; print(fastapi.__version__)"
python -c "import pydantic; print(pydantic.__version__)"

# List installed packages
pip list | grep -E "(fastapi|pydantic|uvicorn|starlette)"

# Check environment variables
python -c "import os; print(os.environ.get('DATABASE_URL'))"
```

## Additional Resources

- [FastAPI Official Debugging Guide](https://fastapi.tiangolo.com/tutorial/debugging/)
- [FastAPI Error Handling Tutorial](https://fastapi.tiangolo.com/tutorial/handling-errors/)
- [Better Stack: FastAPI Error Handling Patterns](https://betterstack.com/community/guides/scaling-python/error-handling-fastapi/)
- [VS Code FastAPI Tutorial](https://code.visualstudio.com/docs/python/tutorial-fastapi)
- [Orchestra: FastAPI Debugging Guide](https://www.getorchestra.io/guides/fastapi-debugging-a-comprehensive-guide-with-examples)
- [Better Stack: Logging with FastAPI](https://betterstack.com/community/guides/logging/logging-with-fastapi/)
