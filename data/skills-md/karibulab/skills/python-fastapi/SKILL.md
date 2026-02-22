---
name: python-fastapi
description: FastAPI Secure Engineering
---

# python-fastapi

This skill defines how to build APIs using FastAPI following best
practices in architecture, security, maintainability, and performance.
This is the minimum acceptable standard.

## When to use

Use when you need to build APIs using FastAPI following best practices in architecture, security, maintainability, and performance.

## Instructions

## 1. Core Principles

1.  Secure by default.
2.  Strict typing and strong validation.
3.  Clear separation of concerns.
4.  No business logic inside routers.
5.  Zero hardcoded secrets.
6.  Fail closed, not fail open.

If it "works but is insecure", it does not work.

------------------------------------------------------------------------

## 2. Project Structure

Recommended minimum structure:

    app/
     ├── main.py
     ├── api/
     │    ├── deps.py
     │    └── v1/
     │         ├── routes_x.py
     ├── core/
     │    ├── config.py
     │    ├── security.py
     │    └── logging.py
     ├── services/
     ├── repositories/
     ├── models/
     └── schemas/

Rules:

-   `api/` → endpoints only.
-   `services/` → business logic.
-   `repositories/` → data access.
-   `schemas/` → Pydantic request/response models.
-   `core/` → configuration, security, cross-cutting concerns.

Everything inside `main.py` is not minimalism. It is chaos.

------------------------------------------------------------------------

## 3. Secure Configuration

### 3.1 Environment Variables

Use `pydantic-settings`.

``` python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str
    environment: str
    secret_key: str
    database_url: str
    access_token_expire_minutes: int = 15

    class Config:
        env_file = ".env"
```

Rules:

-   No default values for secrets.
-   No secrets in the repository.
-   `.env` files are forbidden in production.

------------------------------------------------------------------------

## 4. Authentication Security

### 4.1 Never Custom Authentication

Use: - OAuth2 + JWT - Or a trusted identity provider (Auth0, Cognito,
Keycloak, etc.)

### 4.2 Secure JWT

-   Signed with HS256 or RS256.
-   Short expiration time.
-   Validate:
    -   exp
    -   iss
    -   aud

Never trust the payload without verifying the signature.

------------------------------------------------------------------------

## 5. Endpoint Security

### 5.1 Dependency Injection for Security

``` python
from fastapi import Depends, HTTPException, status

def get_current_user(token: str = Depends(oauth2_scheme)):
    ...
```

Rules:

-   Every sensitive route must require authentication.
-   Separate authentication from authorization.
-   Implement explicit RBAC or ABAC.

------------------------------------------------------------------------

### 5.2 Strict Validation with Pydantic

Always use models:

``` python
class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=12)
```

Rules:

-   Never accept raw dicts.
-   Avoid `Any` unless absolutely necessary.
-   Limit string sizes.
-   Validate nested structures.

------------------------------------------------------------------------

## 6. OWASP Top 10 Protection

### 6.1 Injection

-   Never build SQL queries manually.
-   Use ORM or parameterized queries.
-   Enforce strict typing.

------------------------------------------------------------------------

### 6.2 Excessive Data Exposure

Never return:

-   Password hashes
-   Tokens
-   Internal fields
-   Stack traces

Use explicit response models:

``` python
@router.get("/", response_model=UserResponse)
```

------------------------------------------------------------------------

### 6.3 Error Handling

Do not expose internal errors.

``` python
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
```

Log internally. Do not leak details externally.

------------------------------------------------------------------------

## 7. Rate Limiting and Abuse Protection

Implement rate limiting:

-   SlowAPI or equivalent.
-   Or external gateway (NGINX, API Gateway).

Rules: - Never expose login without rate limiting. - Never expose public
endpoints without abuse control.

------------------------------------------------------------------------

## 8. Secure CORS

Never:

``` python
allow_origins=["*"]
allow_credentials=True
```

Explicitly configure allowed origins per environment.

------------------------------------------------------------------------

## 9. Secure Logging

-   Do not log passwords.
-   Do not log tokens.
-   Do not log sensitive data.
-   Use structured logging (JSON).
-   Include request_id.

If you feel the need to log the full request body, rethink your
architecture.

------------------------------------------------------------------------

## 10. File Upload Security

If uploads are allowed:

-   Enforce size limits.
-   Validate MIME type.
-   Do not trust file extensions.
-   Never execute uploaded content.
-   Store outside public root.

------------------------------------------------------------------------

## 11. Production Hardening

### 11.1 Server

Never use:

    uvicorn main:app --reload

Use:

-   Gunicorn + Uvicorn workers
-   Proper worker configuration
-   Reverse proxy in front

------------------------------------------------------------------------

### 11.2 Security Headers

Add:

-   X-Content-Type-Options
-   X-Frame-Options
-   Content-Security-Policy
-   Strict-Transport-Security

Preferably via middleware or reverse proxy.

------------------------------------------------------------------------

## 12. Mandatory Testing

At minimum:

-   Authentication tests.
-   Authorization tests.
-   Validation tests.
-   Error handling tests.

Testing only the happy path is self-deception.

------------------------------------------------------------------------

## 13. Code Quality Standards

-   Full typing.
-   `mypy` enabled.
-   `ruff` or `flake8`.
-   `black` mandatory.
-   No logic in decorators.
-   No side effects at import time.

------------------------------------------------------------------------

## 14. What NOT To Do

-   Do not expose `/docs` in production without authentication.
-   Do not use DEBUG=True.
-   Do not return raw exceptions.
-   Do not trust frontend input.
-   Do not mix sync and async blindly.
-   Never use `eval`.

------------------------------------------------------------------------

## 15. Pre-Deployment Checklist

-   [ ] Environment variables secured
-   [ ] Secrets outside repository
-   [ ] Rate limiting enabled
-   [ ] Restricted CORS
-   [ ] Logs free of sensitive data
-   [ ] JWT validates signature and expiration
-   [ ] Auth tests passing
-   [ ] Dependencies updated
-   [ ] /docs protected or disabled

If this checklist is not satisfied, it is not a deployment. It is a
gamble.

