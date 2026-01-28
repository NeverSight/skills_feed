---
name: api-development
description: FastAPI, REST APIs, GraphQL, data service design, and API best practices
sasmp_version: "1.3.0"
bonded_agent: 02-backend-developer
bond_type: PRIMARY_BOND
skill_version: "2.0.0"
last_updated: "2025-01"
complexity: intermediate
estimated_mastery_hours: 100
prerequisites: [python-programming, sql-databases]
unlocks: [containerization, monitoring-observability]
---

# API Development

Production-grade API development with FastAPI, REST best practices, and data service patterns.

## Quick Start

```python
from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uvicorn

app = FastAPI(title="Data API", version="1.0.0")

# Pydantic models for validation
class DataRecord(BaseModel):
    id: str = Field(..., description="Unique identifier")
    value: float = Field(..., ge=0, description="Non-negative value")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[dict] = None

    class Config:
        json_schema_extra = {
            "example": {"id": "rec-001", "value": 42.5, "metadata": {"source": "sensor-1"}}
        }

class DataResponse(BaseModel):
    data: list[DataRecord]
    total: int
    page: int
    page_size: int

@app.get("/data", response_model=DataResponse)
async def get_data(
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=1000),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """Retrieve paginated data records with optional date filtering."""
    # Query data with pagination
    records = query_database(page, page_size, start_date, end_date)
    total = count_records(start_date, end_date)

    return DataResponse(data=records, total=total, page=page, page_size=page_size)

@app.post("/data", status_code=201)
async def create_data(record: DataRecord):
    """Create a new data record."""
    try:
        save_to_database(record)
        return {"status": "created", "id": record.id}
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Record already exists")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Core Concepts

### 1. Dependency Injection

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

security = HTTPBearer()

# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication dependency
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Rate limiting dependency
class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute

    async def __call__(self, request: Request):
        client_ip = request.client.host
        if is_rate_limited(client_ip, self.requests_per_minute):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")

# Usage
@app.get("/protected")
async def protected_endpoint(
    user: dict = Depends(verify_token),
    db: Session = Depends(get_db),
    _: None = Depends(RateLimiter(100))
):
    return {"user": user["sub"]}
```

### 2. Error Handling

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError

app = FastAPI()

class APIError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code

@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message}}
    )

@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": {"code": "VALIDATION_ERROR", "details": exc.errors()}}
    )

@app.exception_handler(Exception)
async def generic_error_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": {"code": "INTERNAL_ERROR", "message": "An unexpected error occurred"}}
    )
```

### 3. Background Tasks

```python
from fastapi import BackgroundTasks
from celery import Celery

# Simple background tasks
@app.post("/reports")
async def generate_report(background_tasks: BackgroundTasks, report_id: str):
    background_tasks.add_task(process_report, report_id)
    return {"status": "processing", "report_id": report_id}

def process_report(report_id: str):
    # Long-running task
    time.sleep(60)
    save_report(report_id)

# Celery for distributed tasks
celery_app = Celery('tasks', broker='redis://localhost:6379')

@celery_app.task
def async_etl_job(job_id: str):
    run_etl_pipeline(job_id)

@app.post("/jobs")
async def start_job(job_id: str):
    task = async_etl_job.delay(job_id)
    return {"task_id": task.id, "status": "queued"}
```

## Tools & Technologies

| Tool | Purpose | Version (2025) |
|------|---------|----------------|
| **FastAPI** | Modern API framework | 0.109+ |
| **Pydantic** | Data validation | 2.5+ |
| **SQLAlchemy** | Database ORM | 2.0+ |
| **Celery** | Task queue | 5.3+ |
| **httpx** | Async HTTP client | 0.27+ |
| **pytest** | Testing | 8.0+ |

## Troubleshooting Guide

| Issue | Symptoms | Root Cause | Fix |
|-------|----------|------------|-----|
| **422 Error** | Validation failed | Invalid request data | Check request schema |
| **Slow Response** | High latency | Blocking I/O | Use async, background tasks |
| **Connection Pool** | DB timeouts | Pool exhausted | Increase pool, use limits |
| **Memory Leak** | Growing memory | Unclosed connections | Use context managers |

## Best Practices

```python
# ✅ DO: Use Pydantic for validation
class CreateUser(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)

# ✅ DO: Version your API
app = FastAPI()
v1 = APIRouter(prefix="/v1")

# ✅ DO: Use proper HTTP status codes
# 201 Created, 204 No Content, 404 Not Found

# ✅ DO: Document with OpenAPI
@app.get("/users/{user_id}", summary="Get user by ID", tags=["users"])

# ❌ DON'T: Return 200 for errors
# ❌ DON'T: Expose internal errors to clients
# ❌ DON'T: Skip input validation
```

## Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [REST API Design Guide](https://restfulapi.net/)
- [Pydantic Docs](https://docs.pydantic.dev/)

---

**Skill Certification Checklist:**
- [ ] Can build REST APIs with FastAPI
- [ ] Can implement authentication and authorization
- [ ] Can handle errors gracefully
- [ ] Can use background tasks
- [ ] Can write API tests
