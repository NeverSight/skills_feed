---
name: restapi
description: REST API design, implementation, and best practices. Activate for API endpoints, HTTP methods, status codes, authentication, and API documentation.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# REST API Skill

Provides comprehensive REST API design and implementation capabilities for the Golden Armada AI Agent Fleet Platform.

## When to Use This Skill

Activate this skill when working with:
- API endpoint design
- HTTP request/response handling
- API authentication
- OpenAPI documentation
- API testing

## REST API Design Principles

### Resource Naming
\`\`\`
# Good - nouns, plural
GET    /agents
GET    /agents/{id}
POST   /agents
PUT    /agents/{id}
DELETE /agents/{id}

# Nested resources
GET    /agents/{id}/tasks
POST   /agents/{id}/tasks

# Bad - verbs, actions
GET    /getAgents
POST   /createAgent
\`\`\`

### HTTP Methods
| Method | Usage | Idempotent |
|--------|-------|------------|
| GET | Read resource | Yes |
| POST | Create resource | No |
| PUT | Replace resource | Yes |
| PATCH | Partial update | No |
| DELETE | Delete resource | Yes |

### Status Codes
\`\`\`
# Success
200 OK              - Successful GET, PUT, PATCH
201 Created         - Successful POST
204 No Content      - Successful DELETE

# Client Errors
400 Bad Request     - Validation error
401 Unauthorized    - Authentication required
403 Forbidden       - Not permitted
404 Not Found       - Resource not found
409 Conflict        - Duplicate/conflict
422 Unprocessable   - Semantic validation error

# Server Errors
500 Internal Error  - Server error
502 Bad Gateway     - Upstream error
503 Service Unavailable - Temporary overload
\`\`\`

## API Implementation (FastAPI)

\`\`\`python
from fastapi import FastAPI, HTTPException, Query, Path, Depends, status
from typing import List, Optional
from pydantic import BaseModel, Field

app = FastAPI(title="Golden Armada API", version="1.0.0")

# Models
class AgentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    type: str = Field(..., pattern="^(claude|gpt|gemini)$")

class AgentResponse(BaseModel):
    id: str
    name: str
    type: str
    status: str
    created_at: datetime

# Endpoints
@app.get("/agents", response_model=List[AgentResponse])
async def list_agents(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None)
):
    """List all agents with pagination and filtering."""
    return await agent_service.list(skip=skip, limit=limit, status=status)

@app.get("/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str = Path(..., description="Agent ID")):
    """Get a specific agent by ID."""
    agent = await agent_service.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@app.post("/agents", response_model=AgentResponse, status_code=201)
async def create_agent(agent: AgentCreate):
    """Create a new agent."""
    return await agent_service.create(agent)

@app.put("/agents/{agent_id}", response_model=AgentResponse)
async def update_agent(agent_id: str, agent: AgentCreate):
    """Replace an existing agent."""
    existing = await agent_service.get(agent_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Agent not found")
    return await agent_service.update(agent_id, agent)

@app.delete("/agents/{agent_id}", status_code=204)
async def delete_agent(agent_id: str):
    """Delete an agent."""
    deleted = await agent_service.delete(agent_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Agent not found")
\`\`\`

## Authentication

### JWT Authentication
\`\`\`python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
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
    return await get_user(user_id)

# Protected endpoint
@app.get("/protected")
async def protected_route(user: User = Depends(get_current_user)):
    return {"user": user.email}
\`\`\`

### API Key Authentication
\`\`\`python
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != VALID_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key
\`\`\`

## Error Handling

\`\`\`python
class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[dict] = None

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(
            error="validation_error",
            message=str(exc)
        ).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="internal_error",
            message="An unexpected error occurred"
        ).dict()
    )
\`\`\`

## API Testing with curl

\`\`\`bash
# GET
curl -X GET "http://localhost:8000/agents" \
  -H "Authorization: Bearer TOKEN"

# POST
curl -X POST "http://localhost:8000/agents" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"name": "agent-1", "type": "claude"}'

# PUT
curl -X PUT "http://localhost:8000/agents/123" \
  -H "Content-Type: application/json" \
  -d '{"name": "updated-agent", "type": "claude"}'

# DELETE
curl -X DELETE "http://localhost:8000/agents/123" \
  -H "Authorization: Bearer TOKEN"
\`\`\`

## OpenAPI Documentation

\`\`\`python
from fastapi import FastAPI

app = FastAPI(
    title="Golden Armada API",
    description="AI Agent Fleet Platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Access documentation at:
# - Swagger UI: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
# - OpenAPI JSON: http://localhost:8000/openapi.json
\`\`\`
