---
name: error-handling
description: >
  Python error handling patterns for FastAPI, Pydantic, and asyncio. Follows "Let it crash"
  philosophy - raise exceptions, catch at boundaries. Covers HTTPException, global exception
  handlers, validation errors, background task failures. Use when: (1) Designing API error
  responses, (2) Handling RequestValidationError, (3) Managing async exceptions,
  (4) Preventing stack trace leakage, (5) Designing custom exception hierarchies.
---

# Error Handling

Production-ready error handling for Python APIs using the **Let it crash** philosophy.

## Design Philosophy

**Let it crash** - Don't be defensive. Let exceptions propagate naturally and handle them at boundaries.

```python
# BAD - Too defensive, obscures errors
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    try:
        user = await user_service.get(user_id)
        if not user:
            raise HTTPException(404, "Not found")
        return user
    except DatabaseError as e:
        raise HTTPException(500, "Database error")
    except Exception as e:
        logger.exception("Unexpected error")
        raise HTTPException(500, "Internal error")

# GOOD - Let exceptions propagate, handle at boundary
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await user_service.get(user_id)
    if not user:
        raise UserNotFoundError(user_id)
    return user
```

## Core Principles

1. **Raise low, catch high** - Throw exceptions where errors occur, handle at API boundaries
2. **Domain exceptions** - Create semantic exceptions, not generic ones
3. **Global handlers** - Use `@app.exception_handler()` for centralized error formatting
4. **No bare except** - Always catch specific exceptions
5. **Preserve context** - Use `raise ... from error` to keep original traceback

## Quick Start

### 1. Define Domain Exceptions

```python
from enum import StrEnum

class ErrorCode(StrEnum):
    USER_NOT_FOUND = "user_not_found"
    INVALID_CREDENTIALS = "invalid_credentials"
    RATE_LIMITED = "rate_limited"

class DomainError(Exception):
    """Base exception for all domain errors."""
    def __init__(self, code: ErrorCode, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class UserNotFoundError(DomainError):
    def __init__(self, user_id: int):
        super().__init__(
            code=ErrorCode.USER_NOT_FOUND,
            message=f"User {user_id} not found",
            status_code=404
        )
```

### 2. Define Error Response Schema

```python
from pydantic import BaseModel

class ErrorDetail(BaseModel):
    code: str
    message: str
    request_id: str | None = None

class ErrorResponse(BaseModel):
    error: ErrorDetail
```

### 3. Register Global Handlers

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message}}
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": "http_error", "message": str(exc.detail)}}
    )

@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": {"code": "validation_error", "message": "Invalid request"}}
    )

@app.exception_handler(Exception)
async def generic_error_handler(request: Request, exc: Exception):
    # Log full error internally
    logger.exception("Unhandled error")
    # Return safe message to client
    return JSONResponse(
        status_code=500,
        content={"error": {"code": "internal_error", "message": "Internal server error"}}
    )
```

### 4. Use in Routes

```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await user_service.get(user_id)
    if not user:
        raise UserNotFoundError(user_id)
    return user
```

## When to Catch Exceptions

Only catch exceptions in these cases:

| Situation | Example |
|-----------|---------|
| **Need to retry** | `tenacity.retry()` for transient failures |
| **Need to transform** | Wrap third-party SDK errors as domain errors |
| **Need to clean up** | Use `finally` or context managers |
| **Need to add context** | `raise DomainError(...) from original` |

## Python + FastAPI Integration

| Layer | Responsibility |
|-------|---------------|
| **Service/Domain** | Raise domain exceptions (`UserNotFoundError`) |
| **Routes** | Let exceptions propagate (no try/except) |
| **Exception Handlers** | Transform to HTTP responses |
| **Middleware** | Add request context (request_id, timing) |

## Common Patterns

### Third-Party SDK Wrapping

```python
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

class ExternalServiceError(DomainError):
    def __init__(self, service: str, original: Exception):
        super().__init__(
            code=ErrorCode.EXTERNAL_SERVICE_ERROR,
            message=f"{service} unavailable",
            status_code=503
        )
        self.__cause__ = original

@retry(stop=stop_after_attempt(3), wait=wait_exponential())
async def call_payment_api(data: dict):
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post("https://api.payment.com/charge", json=data)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise ExternalServiceError("Payment API", e) from e
```

### Background Task Error Handling

```python
from fastapi import BackgroundTasks

async def safe_background_task(task_func, *args, **kwargs):
    try:
        await task_func(*args, **kwargs)
    except Exception as e:
        logger.exception(f"Background task failed: {e}")
        # Optional: send to dead letter queue or alerting

@app.post("/orders")
async def create_order(order: Order, background_tasks: BackgroundTasks):
    result = await order_service.create(order)
    background_tasks.add_task(safe_background_task, send_confirmation_email, result.id)
    return result
```

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Stack trace in response | No generic handler | Add `@app.exception_handler(Exception)` |
| Lost original error | Missing `from` | Use `raise NewError() from original` |
| Validation errors leak | Default handler | Override `RequestValidationError` handler |
| Silent failures | Swallowed exceptions | Let exceptions propagate, handle at boundary |

## References

- [Python Patterns](references/python.md) - Exception design, when to catch, SDK wrapping
- [FastAPI Patterns](references/fastapi.md) - HTTPException, global handlers, middleware
- [Pydantic Patterns](references/pydantic.md) - ValidationError, raise in validators
- [Asyncio Patterns](references/asyncio.md) - TaskGroup, timeout, background tasks
- [FastAPI Docs: Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/)
- [Pydantic Docs: Error Handling](https://docs.pydantic.dev/latest/errors/errors/)
