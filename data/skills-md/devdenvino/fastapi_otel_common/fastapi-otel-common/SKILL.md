---
name: fastapi-otel-common
description: Expert guidance for building FastAPI applications with OpenTelemetry, Loguru, and OIDC using the fastapi-otel-common library.
version: 0.1.0
---

# FastAPI OTEL Common Skill

This skill provides the AI agent with specialized knowledge and best practices for the `fastapi-otel-common` ecosystem.

## Core Principles

- **Observability First**: Always implement OpenTelemetry tracing and metrics. Use the built-in instrumentation.
- **Structured Logging**: Use `loguru` for all logging. Avoid `print()`. Use the library's logger initialization.
- **Security by Default**: Use `get_current_user` or role-based decorators (`RequireRoles`) for protected endpoints.
- **Production-Ready Health Checks**: Utilize the automatic `/healthz`, `/readyz`, and `/livez` endpoints.

## Common Tasks

### 1. Initialize the App
```python
from fastapi_otel_common import create_app

app = create_app(
    title="My Service",
    version="1.0.0",
    # All security headers and OTEL instrumentation are enabled by default
)
```

### 2. Add OIDC Protected Route
```python
from fastapi import Depends
from fastapi_otel_common.security import get_current_user
from fastapi_otel_common.core.models import UserBase

@app.get("/me")
async def get_me(user: UserBase = Depends(get_current_user)):
    return user
```

### 3. Implement Role-Based Access Control
```python
from fastapi_otel_common.security import RequireRoles

@app.post("/admin/action")
async def admin_action(
    user: UserBase = Depends(RequireRoles(["admin"]))
):
    return {"status": "success"}
```

### 4. Custom Tracing
```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

async def some_logic():
    with tracer.start_as_current_span("my-custom-operation"):
        # Logic here
        pass
```

## Troubleshooting

- **No Traces in Collector**: Check `OTEL_EXPORTER_OTLP_ENDPOINT` environment variable.
- **DB Connection Issues**: Ensure `DB_TYPE` and associated credentials (e.g., `POSTGRES_USER`, `SQLITE_DB_PATH`) are set.
- **Authentication Fails**: Verify `OIDC_ISSUER`, `OIDC_CLIENT_ID`, and `OIDC_JWKS_URI`.
