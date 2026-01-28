---
name: api-design-patterns
description: RESTful API design, error handling, versioning, and best practices. Use when designing APIs, reviewing endpoints, implementing error responses, or setting up API structure. Triggers on "design API", "review API", "REST best practices", or "API patterns".
license: MIT
metadata:
  author: api-design-patterns
  version: "1.0.0"
---

# API Design Patterns

RESTful API design principles, error handling, pagination, versioning, and security best practices. Guidelines for building consistent, developer-friendly APIs.

## When to Apply

Reference these guidelines when:
- Designing new API endpoints
- Reviewing existing API structure
- Implementing error handling
- Setting up pagination/filtering
- Planning API versioning

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Resource Design | CRITICAL | `rest-` |
| 2 | Error Handling | CRITICAL | `error-` |
| 3 | Security | CRITICAL | `sec-` |
| 4 | Pagination & Filtering | HIGH | `page-` |
| 5 | Versioning | HIGH | `ver-` |
| 6 | Response Format | MEDIUM | `resp-` |
| 7 | Documentation | MEDIUM | `doc-` |

## Quick Reference

### 1. Resource Design (CRITICAL)

- `rest-nouns-not-verbs` - Use nouns for endpoints
- `rest-plural-resources` - Use plural resource names
- `rest-http-methods` - Correct HTTP method usage
- `rest-nested-resources` - Proper resource nesting
- `rest-status-codes` - Appropriate status codes
- `rest-idempotency` - Idempotent operations
- `rest-hateoas` - Hypermedia links

### 2. Error Handling (CRITICAL)

- `error-consistent-format` - Consistent error structure
- `error-meaningful-messages` - Helpful error messages
- `error-validation-details` - Field-level validation errors
- `error-codes` - Machine-readable error codes
- `error-stack-traces` - Never expose in production

### 3. Security (CRITICAL)

- `sec-authentication` - Proper auth implementation
- `sec-authorization` - Resource-level permissions
- `sec-rate-limiting` - Prevent abuse
- `sec-input-validation` - Validate all input
- `sec-cors` - CORS configuration
- `sec-sensitive-data` - Protect sensitive data

### 4. Pagination & Filtering (HIGH)

- `page-cursor-based` - Cursor pagination for large datasets
- `page-offset-based` - Offset pagination for simple cases
- `page-consistent-params` - Consistent parameter names
- `page-metadata` - Include pagination metadata
- `filter-query-params` - Filter via query parameters
- `sort-flexible` - Flexible sorting options

### 5. Versioning (HIGH)

- `ver-url-path` - Version in URL path
- `ver-header-based` - Version in headers
- `ver-backward-compatible` - Maintain compatibility
- `ver-deprecation` - Deprecation strategy

### 6. Response Format (MEDIUM)

- `resp-consistent-structure` - Consistent response envelope
- `resp-json-conventions` - JSON naming conventions
- `resp-partial-responses` - Field selection
- `resp-compression` - Response compression

### 7. Documentation (MEDIUM)

- `doc-openapi` - OpenAPI/Swagger spec
- `doc-examples` - Request/response examples
- `doc-changelog` - API changelog

## Essential Guidelines

### Resource Naming

```
# ❌ Verbs in URLs - RPC style
GET    /getUsers
POST   /createUser
PUT    /updateUser/123
DELETE /deleteUser/123

# ✅ Nouns with HTTP methods - REST style
GET    /users          # List users
POST   /users          # Create user
GET    /users/123      # Get user
PUT    /users/123      # Update user (full)
PATCH  /users/123      # Update user (partial)
DELETE /users/123      # Delete user
```

### Nested Resources

```
# ✅ Logical nesting (max 2 levels)
GET    /users/123/orders              # User's orders
GET    /users/123/orders/456          # Specific order
POST   /users/123/orders              # Create order for user

# ❌ Too deeply nested
GET    /users/123/orders/456/items/789/reviews

# ✅ Flatten when appropriate
GET    /order-items/789/reviews       # Direct access
```

### HTTP Methods & Status Codes

```
# GET - Retrieve resource(s)
GET /users              → 200 OK + array
GET /users/123          → 200 OK + object
GET /users/999          → 404 Not Found

# POST - Create resource
POST /users             → 201 Created + object + Location header
POST /users (invalid)   → 400 Bad Request + errors

# PUT - Full update (replace)
PUT /users/123          → 200 OK + updated object
PUT /users/999          → 404 Not Found

# PATCH - Partial update
PATCH /users/123        → 200 OK + updated object

# DELETE - Remove resource
DELETE /users/123       → 204 No Content
DELETE /users/999       → 404 Not Found

# Other common status codes
401 Unauthorized        # Not authenticated
403 Forbidden           # Authenticated but not authorized
409 Conflict            # Resource state conflict
422 Unprocessable       # Validation failed
429 Too Many Requests   # Rate limited
500 Internal Error      # Server error
503 Service Unavailable # Maintenance/overload
```

### Error Response Format

```json
// ❌ Inconsistent error formats
{ "error": "Not found" }
{ "message": "Invalid email" }
{ "errors": ["Error 1", "Error 2"] }

// ✅ Consistent error envelope
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request contains invalid data",
    "details": [
      {
        "field": "email",
        "code": "INVALID_FORMAT",
        "message": "Please provide a valid email address"
      },
      {
        "field": "password",
        "code": "TOO_SHORT",
        "message": "Password must be at least 8 characters"
      }
    ],
    "request_id": "req_abc123"
  }
}

// ✅ Not found error
{
  "error": {
    "code": "NOT_FOUND",
    "message": "User with ID 123 not found",
    "request_id": "req_def456"
  }
}

// ✅ Server error (no sensitive details)
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An unexpected error occurred. Please try again.",
    "request_id": "req_ghi789"
  }
}
```

### Pagination

```json
// ✅ Offset-based pagination
GET /users?page=2&per_page=20

{
  "data": [...],
  "meta": {
    "current_page": 2,
    "per_page": 20,
    "total_pages": 10,
    "total_count": 195
  },
  "links": {
    "first": "/users?page=1&per_page=20",
    "prev": "/users?page=1&per_page=20",
    "next": "/users?page=3&per_page=20",
    "last": "/users?page=10&per_page=20"
  }
}

// ✅ Cursor-based pagination (for large datasets)
GET /users?cursor=eyJpZCI6MTIzfQ&limit=20

{
  "data": [...],
  "meta": {
    "has_more": true,
    "next_cursor": "eyJpZCI6MTQzfQ"
  },
  "links": {
    "next": "/users?cursor=eyJpZCI6MTQzfQ&limit=20"
  }
}
```

### Filtering & Sorting

```
# ✅ Query parameter filtering
GET /users?status=active
GET /users?role=admin&status=active
GET /users?created_after=2024-01-01

# ✅ Sorting
GET /users?sort=created_at        # Ascending (default)
GET /users?sort=-created_at       # Descending (prefix with -)
GET /users?sort=last_name,-created_at  # Multiple fields

# ✅ Field selection (sparse fieldsets)
GET /users?fields=id,name,email
GET /users/123?fields=id,name,orders

# ✅ Search
GET /users?q=john
GET /users?search=john@example
```

### Consistent Response Structure

```json
// ✅ Single resource
GET /users/123
{
  "data": {
    "id": "123",
    "type": "user",
    "attributes": {
      "name": "John Doe",
      "email": "john@example.com",
      "created_at": "2024-01-15T10:30:00Z"
    },
    "relationships": {
      "orders": {
        "links": {
          "related": "/users/123/orders"
        }
      }
    }
  }
}

// ✅ Collection
GET /users
{
  "data": [
    { "id": "123", "type": "user", ... },
    { "id": "124", "type": "user", ... }
  ],
  "meta": {
    "total_count": 100
  },
  "links": {
    "self": "/users?page=1",
    "next": "/users?page=2"
  }
}

// ✅ Simpler envelope (also acceptable)
{
  "user": {
    "id": "123",
    "name": "John Doe"
  }
}

{
  "users": [...],
  "pagination": {...}
}
```

### Versioning

```
# ✅ URL path versioning (recommended - explicit)
GET /api/v1/users
GET /api/v2/users

# ✅ Header versioning
GET /api/users
Accept: application/vnd.myapi.v2+json

# ✅ Query parameter (simple, but less clean)
GET /api/users?version=2
```

### Rate Limiting

```
# ✅ Include rate limit headers
HTTP/1.1 200 OK
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 998
X-RateLimit-Reset: 1640995200

# ✅ Rate limited response
HTTP/1.1 429 Too Many Requests
Retry-After: 60

{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Too many requests. Please retry after 60 seconds.",
    "retry_after": 60
  }
}
```

### Actions on Resources

```
# For non-CRUD actions, use sub-resources or actions
# ✅ Sub-resource style
POST /users/123/activate
POST /orders/456/cancel
POST /posts/789/publish

# ✅ Or controller-style for complex operations
POST /auth/login
POST /auth/logout
POST /auth/refresh
POST /password/reset
POST /password/reset/confirm
```

### Request Validation

```json
// ✅ Validate and return all errors at once
POST /users
{
  "email": "invalid",
  "password": "short"
}

// Response: 422 Unprocessable Entity
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "code": "INVALID_FORMAT",
        "message": "Must be a valid email address"
      },
      {
        "field": "password",
        "code": "TOO_SHORT",
        "message": "Must be at least 8 characters",
        "meta": {
          "min_length": 8,
          "actual_length": 5
        }
      }
    ]
  }
}
```

### HATEOAS (Hypermedia)

```json
// ✅ Include links for discoverability
{
  "data": {
    "id": "123",
    "status": "pending",
    "total": 99.99
  },
  "links": {
    "self": "/orders/123",
    "cancel": "/orders/123/cancel",
    "pay": "/orders/123/pay",
    "items": "/orders/123/items"
  },
  "actions": {
    "cancel": {
      "method": "POST",
      "href": "/orders/123/cancel"
    },
    "pay": {
      "method": "POST",
      "href": "/orders/123/pay",
      "fields": [
        { "name": "payment_method", "type": "string", "required": true }
      ]
    }
  }
}
```

### Bulk Operations

```json
// ✅ Bulk create
POST /users/bulk
{
  "users": [
    { "name": "User 1", "email": "user1@example.com" },
    { "name": "User 2", "email": "user2@example.com" }
  ]
}

// Response with partial success
{
  "data": {
    "succeeded": [
      { "id": "123", "name": "User 1" }
    ],
    "failed": [
      {
        "index": 1,
        "error": {
          "code": "DUPLICATE_EMAIL",
          "message": "Email already exists"
        }
      }
    ]
  },
  "meta": {
    "total": 2,
    "succeeded": 1,
    "failed": 1
  }
}
```

## Output Format

When auditing APIs, output findings in this format:

```
endpoint - [category] Description of issue
```

Example:
```
GET /getUsers - [rest] Use noun '/users' instead of verb '/getUsers'
POST /users - [error] Missing validation error details in 400 response
GET /users - [page] Missing pagination metadata in list response
```

## How to Use

Read individual rule files for detailed explanations:

```
rules/rest-http-methods.md
rules/error-consistent-format.md
rules/page-cursor-based.md
```
