---
name: api-design
description: REST and GraphQL API design best practices including OpenAPI specs. Use when designing APIs, documenting endpoints, or reviewing API architecture.
---

# API Design Guide

Best practices for designing developer-friendly, maintainable APIs.

## REST API Principles

### Resource Naming

**Use nouns, not verbs**:

```
✓ GET /users
✓ GET /users/123
✓ GET /users/123/orders

✗ GET /getUsers
✗ GET /fetchUserById
✗ POST /createNewOrder
```

**Use plural nouns**:

```
✓ /users
✓ /orders
✓ /products

✗ /user
✗ /order
```

**Hierarchical relationships**:

```
/users/{userId}/orders           # User's orders
/users/{userId}/orders/{orderId} # Specific order
```

---

### HTTP Methods

| Method | Purpose                   | Idempotent | Request Body |
| ------ | ------------------------- | ---------- | ------------ |
| GET    | Retrieve resource(s)      | Yes        | No           |
| POST   | Create resource           | No         | Yes          |
| PUT    | Replace resource entirely | Yes        | Yes          |
| PATCH  | Update resource partially | No         | Yes          |
| DELETE | Remove resource           | Yes        | No           |

---

### Status Codes

**Success (2xx)**:

- `200 OK` - Request succeeded
- `201 Created` - Resource created (return Location header)
- `204 No Content` - Success with no response body

**Client Error (4xx)**:

- `400 Bad Request` - Malformed request
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - No permission
- `404 Not Found` - Resource doesn't exist
- `409 Conflict` - State conflict
- `422 Unprocessable Entity` - Validation failed
- `429 Too Many Requests` - Rate limited

**Server Error (5xx)**:

- `500 Internal Server Error` - Unexpected error
- `503 Service Unavailable` - Temporary outage

---

### Response Format

**Successful response**:

```json
{
  "data": {
    "id": "123",
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

**Collection response**:

```json
{
  "data": [
    { "id": "1", "name": "Item 1" },
    { "id": "2", "name": "Item 2" }
  ],
  "meta": {
    "page": 1,
    "perPage": 20,
    "total": 100,
    "totalPages": 5
  },
  "links": {
    "self": "/items?page=1",
    "next": "/items?page=2",
    "prev": null
  }
}
```

**Error response**:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "code": "INVALID_FORMAT",
        "message": "Must be a valid email address"
      }
    ]
  }
}
```

---

### Pagination

**Offset-based** (simple, but slow on large datasets):

```
GET /users?page=2&perPage=20
GET /users?offset=40&limit=20
```

**Cursor-based** (efficient, recommended):

```
GET /users?cursor=eyJpZCI6MTIzfQ&limit=20
```

Response includes next cursor:

```json
{
  "data": [...],
  "meta": {
    "nextCursor": "eyJpZCI6MTQzfQ",
    "hasMore": true
  }
}
```

---

### Filtering, Sorting, Fields

**Filtering**:

```
GET /users?status=active
GET /users?created_after=2024-01-01
GET /users?role=admin,moderator
```

**Sorting**:

```
GET /users?sort=name
GET /users?sort=-created_at         # Descending
GET /users?sort=status,-created_at  # Multiple fields
```

**Field selection**:

```
GET /users?fields=id,name,email
GET /users?include=orders,profile
```

---

### Versioning

**URL path** (recommended):

```
/api/v1/users
/api/v2/users
```

**Header**:

```
Accept: application/vnd.api+json;version=2
```

---

## OpenAPI Specification

```yaml
openapi: 3.0.3
info:
  title: My API
  version: 1.0.0
  description: API for managing users

servers:
  - url: https://api.example.com/v1

paths:
  /users:
    get:
      summary: List users
      tags: [Users]
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
      responses:
        "200":
          description: List of users
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: "#/components/schemas/User"

components:
  schemas:
    User:
      type: object
      required: [id, email]
      properties:
        id:
          type: string
        email:
          type: string
          format: email
        name:
          type: string
```

---

## Authentication

**API Keys** (simple, for server-to-server):

```
Authorization: Api-Key YOUR_API_KEY
```

**Bearer Tokens** (JWT, OAuth):

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

**Include in OpenAPI**:

```yaml
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []
```

---

## Rate Limiting

Include headers in responses:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

Return `429 Too Many Requests` when exceeded.

---

## Security Checklist

- [ ] HTTPS only
- [ ] Authentication on protected routes
- [ ] Input validation
- [ ] Output encoding
- [ ] Rate limiting
- [ ] CORS configuration
- [ ] No sensitive data in URLs
- [ ] Audit logging
