---
name: api-designer
description: Design REST APIs or function contracts with clear request/response specifications,
  error handling patterns, authentication strategies, and comprehensive documentation.
allowed-tools: Read, Write, Edit
---

## Purpose

The api-designer skill provides comprehensive guidance for designing robust, RESTful APIs and function contracts that serve as clear interfaces for feature implementations. This skill helps the Architecture Designer agent create well-structured, documented, and maintainable API designs that follow industry best practices.

This skill emphasizes:
- **REST Principles:** Proper resource design, HTTP method usage, and status codes
- **Clear Contracts:** Well-defined request/response schemas
- **Error Handling:** Consistent error response formats
- **Authentication:** Security patterns and authorization strategies
- **Documentation:** Comprehensive API documentation for consumers

The api-designer skill ensures that APIs are intuitive, consistent, and provide excellent developer experience for both internal and external consumers.

## When to Use

This skill auto-activates when the agent describes:
- "Design API endpoints for..."
- "Create REST API for..."
- "Define function contract for..."
- "Specify request/response schemas..."
- "Design authentication for..."
- "Plan API structure with..."
- "Define error responses for..."
- "Create API documentation for..."

## Provided Capabilities

### 1. REST API Endpoint Design

**What it provides:**
- Resource identification and naming
- HTTP method selection (GET, POST, PUT, PATCH, DELETE)
- URL structure and path parameters
- Query parameter design
- Status code selection
- Idempotency considerations

**REST Principles:**
- Resources as nouns, not verbs
- HTTP methods for actions
- Stateless design
- Standard status codes
- HATEOAS (optional)

**Example:**
```python
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# ==================== RESOURCE: Users ====================

class UserCreate(BaseModel):
    """Request schema for creating user."""
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(...)
    full_name: str = Field(..., min_length=1, max_length=200)

class UserResponse(BaseModel):
    """Response schema for user."""
    id: int
    username: str
    email: str
    full_name: str
    is_active: bool
    created_at: datetime

class UserUpdate(BaseModel):
    """Request schema for updating user (all optional)."""
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

class UserList(BaseModel):
    """Response schema for user list with pagination."""
    items: List[UserResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

# API Endpoints
"""
POST   /api/v1/users              Create new user
GET    /api/v1/users              List users (with pagination)
GET    /api/v1/users/{user_id}    Get user by ID
PUT    /api/v1/users/{user_id}    Update user (full replace)
PATCH  /api/v1/users/{user_id}    Update user (partial)
DELETE /api/v1/users/{user_id}    Delete user

Query Parameters for GET /api/v1/users:
- page: int = 1          (pagination)
- page_size: int = 20    (items per page)
- search: str = None     (search filter)
- is_active: bool = None (status filter)
- sort_by: str = "created_at"
- sort_order: str = "desc"

Status Codes:
- 200 OK: Successful GET, PUT, PATCH
- 201 Created: Successful POST
- 204 No Content: Successful DELETE
- 400 Bad Request: Invalid input
- 401 Unauthorized: Authentication required
- 403 Forbidden: Insufficient permissions
- 404 Not Found: Resource not found
- 409 Conflict: Resource conflict (duplicate)
- 422 Unprocessable Entity: Validation error
- 500 Internal Server Error: Server error
"""
```

### 2. Request/Response Schema Design

**What it provides:**
- Input validation schemas
- Output serialization schemas
- Partial update schemas
- List/pagination schemas
- Error response schemas

**Schema Patterns:**

**Create Request (POST):**
```python
class ResourceCreate(BaseModel):
    """All fields required for creation."""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    category: str = Field(...)
```

**Update Request (PUT - Full Replace):**
```python
class ResourceUpdate(BaseModel):
    """All fields required for full update."""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    category: str = Field(...)
```

**Partial Update Request (PATCH):**
```python
class ResourcePatch(BaseModel):
    """All fields optional for partial update."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    category: Optional[str] = None
```

**Response Schema:**
```python
class ResourceResponse(BaseModel):
    """Response includes ID and audit fields."""
    id: int
    name: str
    description: Optional[str]
    category: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True  # Enable ORM integration
```

**List Response with Pagination:**
```python
class PaginatedResponse(BaseModel):
    """Generic paginated response."""
    items: List[ResourceResponse]
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number", ge=1)
    page_size: int = Field(..., description="Items per page", ge=1, le=100)
    total_pages: int = Field(..., description="Total number of pages")

    @property
    def has_next(self) -> bool:
        """Check if there's a next page."""
        return self.page < self.total_pages

    @property
    def has_previous(self) -> bool:
        """Check if there's a previous page."""
        return self.page > 1
```

### 3. Error Response Formats

**What it provides:**
- Consistent error structure
- Error codes and types
- Detailed validation errors
- User-friendly messages
- Debug information (optional)

**Standard Error Response:**
```python
from typing import Optional, List, Dict, Any

class ValidationError(BaseModel):
    """Individual validation error."""
    field: str = Field(..., description="Field name with error")
    message: str = Field(..., description="Error message")
    code: str = Field(..., description="Error code")

class ErrorResponse(BaseModel):
    """Standard error response."""
    error: str = Field(..., description="Error type (e.g., 'validation_error')")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[List[ValidationError]] = Field(None, description="Validation errors")
    request_id: Optional[str] = Field(None, description="Request ID for tracking")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        schema_extra = {
            "example": {
                "error": "validation_error",
                "message": "Request validation failed",
                "details": [
                    {
                        "field": "email",
                        "message": "Invalid email format",
                        "code": "invalid_format"
                    }
                ],
                "request_id": "req_abc123",
                "timestamp": "2025-10-29T10:00:00Z"
            }
        }

# Error Types
"""
validation_error: Request validation failed (400)
authentication_error: Authentication failed (401)
authorization_error: Insufficient permissions (403)
not_found_error: Resource not found (404)
conflict_error: Resource conflict (409)
rate_limit_error: Rate limit exceeded (429)
internal_error: Internal server error (500)
"""
```

### 4. Authentication and Authorization

**What it provides:**
- Authentication patterns (JWT, OAuth2, API Key)
- Authorization strategies (RBAC, ABAC)
- Token validation
- Permission checking
- Security headers

**JWT Authentication Example:**
```python
from pydantic import BaseModel, Field
from typing import Optional, List

class LoginRequest(BaseModel):
    """Login request schema."""
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)

class TokenResponse(BaseModel):
    """Token response schema."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration in seconds")
    refresh_token: Optional[str] = Field(None, description="Refresh token")

class TokenPayload(BaseModel):
    """JWT token payload."""
    sub: int = Field(..., description="User ID (subject)")
    username: str = Field(..., description="Username")
    roles: List[str] = Field(default_factory=list, description="User roles")
    exp: int = Field(..., description="Expiration timestamp")

# API Endpoints
"""
POST /api/v1/auth/login          Login and get token
POST /api/v1/auth/refresh        Refresh access token
POST /api/v1/auth/logout         Logout (invalidate token)

Authentication Header:
Authorization: Bearer <access_token>

Example:
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
"""
```

**Role-Based Access Control (RBAC):**
```python
from enum import Enum

class UserRole(str, Enum):
    """User roles for RBAC."""
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"
    GUEST = "guest"

class Permission(str, Enum):
    """Permissions for resources."""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"

# Permission Matrix
"""
Resource: Users
- ADMIN: create, read, update, delete
- MANAGER: read, update
- USER: read (own profile only)
- GUEST: read (public profiles only)

Endpoint Protection:
POST   /api/v1/users              Requires: admin
GET    /api/v1/users              Requires: admin, manager
GET    /api/v1/users/{user_id}    Requires: authenticated
PUT    /api/v1/users/{user_id}    Requires: admin OR owner
DELETE /api/v1/users/{user_id}    Requires: admin
"""
```

### 5. Rate Limiting

**What it provides:**
- Rate limit strategies
- Rate limit headers
- Error responses for exceeded limits
- Quota management

**Rate Limit Design:**
```python
class RateLimitInfo(BaseModel):
    """Rate limit information."""
    limit: int = Field(..., description="Requests allowed per window")
    remaining: int = Field(..., description="Requests remaining")
    reset: int = Field(..., description="Unix timestamp when limit resets")
    window: int = Field(..., description="Time window in seconds")

# Rate Limit Headers
"""
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1730203200
X-RateLimit-Window: 3600

Rate Limit Tiers:
- Anonymous: 10 requests/hour
- Authenticated: 100 requests/hour
- Premium: 1000 requests/hour
- Admin: Unlimited

Status Code: 429 Too Many Requests
Response:
{
  "error": "rate_limit_exceeded",
  "message": "Rate limit exceeded. Try again in 3600 seconds.",
  "limit": 100,
  "window": 3600,
  "reset": 1730203200
}
"""
```

### 6. API Versioning

**What it provides:**
- Versioning strategies
- Version migration paths
- Backward compatibility
- Deprecation notices

**Versioning Strategies:**

**URL Path Versioning (Recommended):**
```
/api/v1/users
/api/v2/users

Pros: Clear, explicit, easy to route
Cons: URLs change between versions
```

**Header Versioning:**
```
GET /api/users
Accept-Version: v1

GET /api/users
Accept-Version: v2

Pros: Clean URLs
Cons: Less visible, harder to test in browser
```

**Query Parameter Versioning:**
```
/api/users?version=1
/api/users?version=2

Pros: Flexible
Cons: Easy to forget, pollutes query params
```

**Deprecation Example:**
```python
class DeprecationWarning(BaseModel):
    """Deprecation warning in response header."""
    deprecated: bool = True
    sunset_date: str = "2026-01-01"
    replacement_url: str = "/api/v2/users"
    documentation: str = "https://api.example.com/docs/migration/v1-to-v2"

# Response Headers for Deprecated Endpoint
"""
X-API-Deprecated: true
X-API-Sunset: 2026-01-01
X-API-Replacement: /api/v2/users
Link: <https://api.example.com/docs/migration/v1-to-v2>; rel="deprecation"
"""
```

## Usage Guide

### Step 1: Identify Resources
```
Requirements → Identify nouns → Define resources → Name endpoints
```

### Step 2: Design Endpoints
```
Resources → HTTP methods → URL structure → Path/query params
```

### Step 3: Define Schemas
```
Create schemas → Update schemas → Response schemas → Error schemas
```

### Step 4: Plan Authentication
```
Identify auth needs → Choose strategy → Define tokens → Permission model
```

### Step 5: Error Handling
```
Identify error cases → Standard format → Status codes → Error messages
```

### Step 6: Rate Limiting
```
Define tiers → Set limits → Response headers → Exceeded handling
```

### Step 7: Documentation
```
OpenAPI spec → Examples → Authentication guide → Error reference
```

### Step 8: Versioning Strategy
```
Choose approach → Migration plan → Deprecation policy → Documentation
```

## Best Practices

1. **Use Proper HTTP Methods**
   - GET: Retrieve resources (idempotent, safe)
   - POST: Create resources (non-idempotent)
   - PUT: Full replace (idempotent)
   - PATCH: Partial update (idempotent)
   - DELETE: Remove resource (idempotent)

2. **Consistent Naming**
   - Use plural nouns: `/users`, `/posts`
   - Use kebab-case: `/user-profiles`
   - Avoid verbs: `/users` not `/getUsers`

3. **Status Codes**
   - 2xx: Success
   - 4xx: Client errors
   - 5xx: Server errors
   - Be specific: 201 for created, 204 for no content

4. **Pagination**
   - Always paginate lists
   - Provide total count
   - Include next/previous links (HATEOAS)

5. **Filtering and Sorting**
   - Use query params: `?status=active&sort=created_at`
   - Document available filters
   - Provide defaults

6. **Security**
   - Always use HTTPS
   - Validate all input
   - Rate limit requests
   - Use proper authentication

## Resources

### api-design-guide.md
Comprehensive API design guide including:
- REST principles and best practices
- GraphQL patterns (if applicable)
- Request/response schema design
- Error response formats
- Authentication/authorization patterns
- Rate limiting strategies
- API versioning approaches
- Documentation standards

### function-design-patterns.md
Function contract design patterns:
- Function signature design
- Parameter patterns (required, optional, defaults)
- Return type patterns
- Error handling in functions
- Async function patterns
- Type hints for functions
- Docstring standards

## Example Usage

### Input (from Architecture Designer agent):
```
"Design REST API for a task management system with tasks, projects, users, and comments."
```

### Output (api-designer skill provides):
```python
# Complete API design with endpoints and schemas

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

# ==================== ENUMS ====================

class TaskStatus(str, Enum):
    """Task status options."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class TaskPriority(str, Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

# ==================== REQUEST SCHEMAS ====================

class TaskCreate(BaseModel):
    """Create task request."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    project_id: int = Field(..., gt=0)
    assignee_id: Optional[int] = Field(None, gt=0)
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None

class TaskUpdate(BaseModel):
    """Update task request (partial)."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    assignee_id: Optional[int] = Field(None, gt=0)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None

class CommentCreate(BaseModel):
    """Create comment request."""
    content: str = Field(..., min_length=1, max_length=1000)

# ==================== RESPONSE SCHEMAS ====================

class TaskResponse(BaseModel):
    """Task response schema."""
    id: int
    title: str
    description: Optional[str]
    project_id: int
    assignee_id: Optional[int]
    status: TaskStatus
    priority: TaskPriority
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]
    created_by: int

    class Config:
        orm_mode = True

class TaskListResponse(BaseModel):
    """Paginated task list response."""
    items: List[TaskResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

# ==================== API ENDPOINTS ====================
"""
Base URL: /api/v1

Authentication: Bearer token
Rate Limit: 100 requests/hour per user

# Tasks
POST   /tasks                      Create new task
GET    /tasks                      List tasks (paginated, filtered)
GET    /tasks/{task_id}            Get task by ID
PATCH  /tasks/{task_id}            Update task
DELETE /tasks/{task_id}            Delete task

# Comments on Tasks
POST   /tasks/{task_id}/comments   Add comment to task
GET    /tasks/{task_id}/comments   List task comments
DELETE /comments/{comment_id}      Delete comment

# Query Parameters for GET /tasks:
- page: int = 1
- page_size: int = 20
- project_id: int (filter by project)
- assignee_id: int (filter by assignee)
- status: TaskStatus (filter by status)
- priority: TaskPriority (filter by priority)
- search: str (search in title/description)
- sort_by: str = "created_at" (sort field)
- sort_order: str = "desc" (asc or desc)

# Status Codes:
- 200 OK: Successful GET, PATCH
- 201 Created: Successful POST
- 204 No Content: Successful DELETE
- 400 Bad Request: Invalid input
- 401 Unauthorized: Not authenticated
- 403 Forbidden: Insufficient permissions
- 404 Not Found: Task not found
- 422 Unprocessable Entity: Validation error
- 429 Too Many Requests: Rate limit exceeded
- 500 Internal Server Error: Server error

# Permissions:
- Create task: Authenticated user
- List tasks: Authenticated user (filtered by access)
- Get task: Task assignee, project member, or admin
- Update task: Task assignee, project owner, or admin
- Delete task: Task creator, project owner, or admin
"""
```

## Integration

### Used By:
- **@architecture-designer** (Primary) - Phase 2 sub-agent for architecture design

### Integrates With:
- **architecture-planner** skill - API contracts defined after component structure
- **data-modeler** skill - Uses data models for request/response schemas

### Workflow Position:
1. Analysis Specialist completes requirements analysis
2. Architecture Designer receives analysis
3. architecture-planner skill designs component structure (Step 3)
4. data-modeler skill designs data models (Step 4)
5. **api-designer skill** designs API contracts (Step 5)
6. Results synthesized into PRP

---

**Version:** 2.0.0
**Auto-Activation:** Yes
**Phase:** 2 - Design & Planning
**Created:** 2025-10-29