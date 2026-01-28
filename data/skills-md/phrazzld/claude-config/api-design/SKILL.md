---
name: api-design
description: |
  REST API design principles, versioning, and documentation. Use when:
  - Designing new API endpoints
  - Choosing between REST, GraphQL, or gRPC
  - Implementing API versioning
  - Writing OpenAPI specifications
  - Handling API errors
  Keywords: REST, API, OpenAPI, Swagger, versioning, HTTP methods,
  status codes, pagination, error handling
---

# API Design

REST-first, OpenAPI-driven, backward-compatible by default.

## REST Principles

**Resources as nouns. HTTP methods as verbs:**
```
GET    /users          # List users
GET    /users/123      # Get user
POST   /users          # Create user
PUT    /users/123      # Replace user
PATCH  /users/123      # Update user
DELETE /users/123      # Delete user

# Relationships through URL hierarchy
GET /users/123/orders
```

**Never:** `/getUser`, `/createOrder`, `/api/processPayment`

## HTTP Status Codes

| Code | When |
|------|------|
| 200 | Successful GET, PUT, PATCH |
| 201 | Successful POST (created) |
| 204 | Successful DELETE (no body) |
| 400 | Invalid request format |
| 401 | Not authenticated |
| 403 | Not authorized |
| 404 | Resource not found |
| 409 | Business logic conflict |
| 422 | Validation failed |
| 500 | Server error |

## Error Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request data",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format",
        "value": "not-an-email"
      }
    ]
  }
}
```

## Pagination

```
GET /users?page=2&per_page=50&sort=created_at&order=desc

{
  "data": [...],
  "meta": {
    "page": 2,
    "per_page": 50,
    "total": 150,
    "total_pages": 3
  }
}
```

## Versioning

**URL versioning for public APIs:**
```
/v1/users
/v2/users
```

**Rules:**
- Major version for breaking changes only
- 6-month deprecation notice minimum
- Side-by-side version support during transition
- Additive changes don't require new version

## OpenAPI First

**Write spec before code:**
```yaml
openapi: 3.0.0
paths:
  /users/{id}:
    get:
      summary: Get user by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: User found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          description: User not found
```

## Anti-Patterns

- RPC-style endpoints (`/api/getUserById`)
- POST for everything
- Deep nesting (`/users/123/orders/456/items/789`)
- Inconsistent error formats
- Breaking changes without version bump
- Documentation that doesn't match implementation
