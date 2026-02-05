---
name: api-design-patterns
description: >-
  API contract design conventions for FastAPI projects with Pydantic v2. Use during
  the design phase when planning new API endpoints, defining request/response contracts,
  designing pagination or filtering, standardizing error responses, or planning API
  versioning. Covers RESTful naming, HTTP method semantics, Pydantic v2 schema naming
  conventions (XxxCreate/XxxUpdate/XxxResponse), cursor-based pagination, standard error
  format, and OpenAPI documentation. Does NOT cover implementation details (use
  python-backend-expert) or system-level architecture (use system-architecture).
license: MIT
compatibility: 'Python 3.12+, FastAPI 0.115+, Pydantic v2'
metadata:
  author: platform-team
  version: '1.0.0'
  sdlc-phase: architecture
allowed-tools: Read Grep Glob
context: fork
---

# API Design Patterns

## When to Use

Activate this skill when:
- Designing new API endpoints or modifying existing endpoint contracts
- Defining request/response schemas for a feature
- Standardizing pagination, filtering, or sorting across endpoints
- Designing a consistent error response format
- Planning API versioning or deprecation strategy
- Reviewing API contracts for consistency before implementation
- Documenting endpoint specifications for frontend/backend coordination

Do NOT use this skill for:
- Writing implementation code (use `python-backend-expert`)
- System-level architecture decisions (use `system-architecture`)
- Writing tests for endpoints (use `pytest-patterns`)
- Frontend data fetching implementation (use `react-frontend-expert`)

## Instructions

### URL Naming Conventions

#### Resource Naming Rules

1. **Plural nouns** for collections: `/users`, `/orders`, `/products`
2. **Kebab-case** for multi-word resources: `/order-items`, `/user-profiles`
3. **Singular resource by ID**: `/users/{user_id}`, `/orders/{order_id}`
4. **Maximum 2 nesting levels**: `/users/{user_id}/orders` (not `/users/{user_id}/orders/{order_id}/items/{item_id}`)
5. **No verbs in URLs**: use HTTP methods instead (`POST /orders` not `/orders/create`)
6. **Query parameters** for filtering, sorting, pagination: `/users?role=admin&sort=-created_at`

#### URL Structure Template

```
/{version}/{resource}                    → Collection (list, create)
/{version}/{resource}/{id}               → Single resource (get, update, delete)
/{version}/{resource}/{id}/{sub-resource} → Nested collection
/{version}/{resource}/actions/{action}   → Non-CRUD operations (rarely needed)
```

#### Naming Examples

| Good | Bad | Reason |
|------|-----|--------|
| `GET /v1/users` | `GET /v1/getUsers` | No verbs — HTTP method implies action |
| `POST /v1/users` | `POST /v1/user/create` | POST to collection = create |
| `GET /v1/order-items` | `GET /v1/orderItems` | Kebab-case, not camelCase |
| `GET /v1/users/{id}/orders` | `GET /v1/users/{id}/orders/{oid}/items` | Max 2 nesting levels |
| `POST /v1/orders/{id}/actions/cancel` | `POST /v1/cancelOrder/{id}` | Action sub-resource for non-CRUD |

### HTTP Method Semantics

| Method | Purpose | Request Body | Success Status | Idempotent |
|--------|---------|-------------|----------------|------------|
| `GET` | Retrieve resource(s) | None | `200 OK` | Yes |
| `POST` | Create new resource | Required | `201 Created` | No |
| `PUT` | Full replace | Required (full) | `200 OK` | Yes |
| `PATCH` | Partial update | Required (partial) | `200 OK` | No* |
| `DELETE` | Remove resource | None | `204 No Content` | Yes |

*PATCH is not inherently idempotent but can be made so with proper implementation.

**Response headers for creation:**
- `POST` returning `201` SHOULD include a `Location` header with the URL of the created resource

**Conditional requests:**
- Support `If-None-Match` / `ETag` for caching on GET endpoints with frequently-accessed resources

### Schema Naming Conventions (Pydantic v2)

Follow a consistent naming pattern for all Pydantic schemas:

| Pattern | Purpose | Fields |
|---------|---------|--------|
| `{Resource}Create` | POST request body | Writable fields, no id, no timestamps |
| `{Resource}Update` | PUT request body | All writable fields required |
| `{Resource}Patch` | PATCH request body | All fields Optional |
| `{Resource}Response` | Single resource response | All fields including id, timestamps |
| `{Resource}ListResponse` | Paginated list response | items + pagination metadata |
| `{Resource}Filter` | Query parameters | Optional filter fields |

**Schema design rules:**
- Never expose internal fields (hashed_password, internal_notes) in Response schemas
- Always include `id` and timestamps (`created_at`, `updated_at`) in Response schemas
- Use `model_validate(orm_instance)` to convert ORM models to response schemas
- Use `model_dump(exclude_unset=True)` for PATCH operations to distinguish "not provided" from "set to null"
- Reference `references/pydantic-schema-examples.md` for concrete examples

### Pagination

#### Cursor-Based Pagination (Default)

Use cursor-based pagination for all list endpoints. It is more performant than offset-based for large datasets and avoids the "shifting window" problem.

**Request parameters:**
```
GET /v1/users?cursor=eyJpZCI6MTAwfQ&limit=20
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `cursor` | `str \| None` | `None` | Opaque cursor from previous response |
| `limit` | `int` | `20` | Items per page (max 100) |

**Response format:**
```json
{
  "items": [...],
  "next_cursor": "eyJpZCI6MTIwfQ",
  "has_more": true
}
```

**Cursor implementation:**
- Encode the last item's sort key (usually `id`) as a base64 string
- The cursor is opaque to the client — they must not parse or construct it
- Use `WHERE id > :last_id ORDER BY id ASC LIMIT :limit + 1` — fetch one extra to determine `has_more`

#### Offset-Based Pagination (When Needed)

Use offset-based only when the client needs to jump to arbitrary pages (e.g., admin tables).

```json
{
  "items": [...],
  "total": 150,
  "page": 2,
  "page_size": 20,
  "total_pages": 8
}
```

### Filtering and Sorting

#### Filtering

Use query parameters with field names:

```
GET /v1/users?role=admin&is_active=true&created_after=2024-01-01
```

**Filtering conventions:**
- Exact match: `?field=value`
- Range: `?field_min=10&field_max=100` or `?created_after=...&created_before=...`
- Search: `?q=search+term` (for full-text search across multiple fields)
- Multiple values: `?status=active&status=pending` (OR semantics)

#### Sorting

Use a `sort` query parameter with field name and direction prefix:

```
GET /v1/users?sort=-created_at        → descending by created_at
GET /v1/users?sort=name               → ascending by name
GET /v1/users?sort=-created_at,name   → multi-field sort
```

**Convention:** `-` prefix means descending, no prefix means ascending.

### Error Response Format

All API errors follow a consistent format:

```json
{
  "detail": "Human-readable error message",
  "code": "MACHINE_READABLE_CODE",
  "field_errors": [
    {
      "field": "email",
      "message": "Invalid email format",
      "code": "INVALID_FORMAT"
    }
  ]
}
```

#### Standard Error Codes and Status Mapping

| HTTP Status | When to Use | Example `code` |
|-------------|-------------|----------------|
| `400` | Malformed request | `BAD_REQUEST` |
| `401` | Missing or invalid authentication | `UNAUTHORIZED` |
| `403` | Authenticated but not authorized | `FORBIDDEN` |
| `404` | Resource not found | `NOT_FOUND` |
| `409` | Conflict (duplicate, version mismatch) | `CONFLICT` |
| `422` | Validation error (Pydantic) | `VALIDATION_ERROR` |
| `429` | Rate limit exceeded | `RATE_LIMITED` |
| `500` | Unexpected server error | `INTERNAL_ERROR` |

**Error schema (Pydantic v2):**
```python
class FieldError(BaseModel):
    field: str
    message: str
    code: str

class ErrorResponse(BaseModel):
    detail: str
    code: str
    field_errors: list[FieldError] = []
```

### API Versioning

#### Strategy: URL Prefix Versioning

```
/v1/users    → Version 1
/v2/users    → Version 2
```

**Versioning rules:**
1. Start with `/v1/` for all new APIs
2. Increment major version only for breaking changes
3. Non-breaking changes (new optional fields, new endpoints) do NOT require a new version
4. Support at most 2 active versions simultaneously

**Breaking changes that require a new version:**
- Removing a field from a response
- Changing a field's type
- Making an optional request field required
- Changing the URL structure for existing endpoints
- Changing error response format

**Deprecation process:**
1. Add `Deprecation` header to the old version: `Deprecation: true`
2. Add `Sunset` header with the retirement date: `Sunset: Sat, 01 Mar 2026 00:00:00 GMT`
3. Add `Link` header pointing to the new version: `Link: </v2/users>; rel="successor-version"`
4. Log usage of deprecated endpoints for monitoring
5. Remove the old version after the sunset date

### OpenAPI Documentation

FastAPI generates OpenAPI schemas automatically. Enhance them with:

```python
@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="Retrieve a single user's details by their unique identifier.",
    responses={
        404: {"model": ErrorResponse, "description": "User not found"},
    },
    tags=["Users"],
)
async def get_user(user_id: int) -> UserResponse:
    ...
```

**Documentation conventions:**
- Every endpoint has a `summary` (short) and optional `description` (detailed)
- Document all non-200 responses with their schema
- Group endpoints by `tags` matching the resource name
- Use `response_model` for automatic response schema documentation

## Examples

### Designing a Products API Contract

**Objective:** Design the contract for a `/v1/products` CRUD endpoint with search and pagination.

**Endpoints:**

| Method | Path | Description | Request | Response | Status |
|--------|------|-------------|---------|----------|--------|
| GET | `/v1/products` | List products | Query: cursor, limit, q, category, sort | ProductListResponse | 200 |
| POST | `/v1/products` | Create product | Body: ProductCreate | ProductResponse | 201 |
| GET | `/v1/products/{id}` | Get product | — | ProductResponse | 200 |
| PATCH | `/v1/products/{id}` | Update product | Body: ProductPatch | ProductResponse | 200 |
| DELETE | `/v1/products/{id}` | Delete product | — | — | 204 |

**Schemas:**
```python
class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None
    price_cents: int = Field(gt=0)
    category: str
    sku: str = Field(pattern=r"^[A-Z0-9-]+$")

class ProductPatch(BaseModel):
    name: str | None = None
    description: str | None = None
    price_cents: int | None = Field(default=None, gt=0)
    category: str | None = None

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price_cents: int
    category: str
    sku: str
    created_at: datetime
    updated_at: datetime

class ProductListResponse(BaseModel):
    items: list[ProductResponse]
    next_cursor: str | None
    has_more: bool
```

**Search and filtering:**
```
GET /v1/products?q=laptop&category=electronics&sort=-price_cents&limit=20
```

See `references/endpoint-catalog-template.md` for the full documentation template.
See `references/pydantic-schema-examples.md` for additional schema examples.

## Edge Cases

### Bulk Operations

For operations on multiple resources at once:

```
POST /v1/users/bulk
```

**Request:**
```json
{
  "items": [
    {"email": "a@example.com", "name": "Alice"},
    {"email": "b@example.com", "name": "Bob"}
  ]
}
```

**Response (partial success — status 207):**
```json
{
  "results": [
    {"index": 0, "status": "created", "data": {...}},
    {"index": 1, "status": "error", "error": {"detail": "Email already exists", "code": "CONFLICT"}}
  ],
  "succeeded": 1,
  "failed": 1
}
```

Use HTTP `207 Multi-Status` when individual items can succeed or fail independently.

### File Upload Endpoints

File uploads use `multipart/form-data`, not JSON:

```python
@router.post("/v1/files", response_model=FileResponse, status_code=201)
async def upload_file(
    file: UploadFile,
    description: str = Form(default=""),
) -> FileResponse:
    ...
```

Validate file size and MIME type before processing. Return `413 Payload Too Large` for oversized files.

### Long-Running Operations

For operations that cannot complete within a normal request timeout:

1. Return `202 Accepted` with a status URL:
   ```json
   {"status_url": "/v1/jobs/abc123", "estimated_completion": "2024-01-15T10:30:00Z"}
   ```

2. Client polls the status URL:
   ```
   GET /v1/jobs/abc123 → {"status": "processing", "progress": 0.65}
   GET /v1/jobs/abc123 → {"status": "completed", "result_url": "/v1/reports/xyz"}
   ```

### Sub-Resource Design

When a resource logically belongs to a parent but nesting would exceed 2 levels, use a top-level resource with a filter:

```
# Instead of: GET /v1/users/{id}/orders/{oid}/items
# Use:        GET /v1/order-items?order_id=123
```

This keeps URLs flat while maintaining the relationship through filtering.
