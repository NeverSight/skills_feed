---
name: api-designer
description: REST and GraphQL API architect for designing robust, scalable APIs. Use when designing new APIs or improving existing ones.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebFetch, WebSearch
metadata:
  hooks:
    after_complete:
      - trigger: self-improving-agent
        mode: background
        reason: "Learn from API design patterns"
      - trigger: session-logger
        mode: auto
        reason: "Log API design activity"
---

# API Designer

Expert in designing REST and GraphQL APIs that are robust, scalable, and maintainable.

## When This Skill Activates

Activates when you:
- Design a new API
- Review API design
- Improve existing API
- Create API specifications

## REST API Design Principles

### 1. Resource-Oriented Design

**Good:**
```
GET    /users          # List users
POST   /users          # Create user
GET    /users/{id}     # Get specific user
PATCH  /users/{id}     # Update user
DELETE /users/{id}     # Delete user
```

**Avoid:**
```
POST   /getUsers       # Should be GET
POST   /users/create  # Redundant
GET    /users/get/{id} # Redundant
```

### 2. HTTP Methods

| Method | Safe | Idempotent | Purpose |
|--------|------|------------|---------|
| GET | ✓ | ✓ | Read resource |
| POST | ✗ | ✗ | Create resource |
| PUT | ✗ | ✓ | Replace resource |
| PATCH | ✗ | ✗ | Update resource |
| DELETE | ✗ | ✓ | Delete resource |

### 3. Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful GET, PATCH, DELETE |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE with no body |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Missing or invalid auth |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Resource already exists |
| 422 | Unprocessable | Valid syntax but semantic errors |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |

### 4. Naming Conventions

- **URLs**: kebab-case (`/user-preferences`)
- **JSON**: camelCase (`{"userId": "123"}`)
- **Query params**: snake_case or camelCase (`?page_size=10`)

### 5. Pagination

```http
GET /users?page=1&page_size=20

Response:
{
  "data": [...],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

### 6. Filtering and Sorting

```http
GET /users?status=active&sort=-created_at,name

# -created_at = descending
# name = ascending
```

## GraphQL API Design

### Schema Design

```graphql
type Query {
  user(id: ID!): User
  users(limit: Int, offset: Int): UserConnection!
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
}

type User {
  id: ID!
  email: String!
  profile: Profile
  posts(first: Int, after: String): PostConnection!
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
}

type UserEdge {
  node: User!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
```

### Best Practices

- **Nullability**: Default to non-null, nullable only when appropriate
- **Connections**: Use cursor-based pagination for lists
- **Payloads**: Use mutation payloads for consistent error handling
- **Descriptions**: Document all types and fields

## API Versioning

### Approaches

**URL Versioning** (Recommended):
```
/api/v1/users
/api/v2/users
```

**Header Versioning**:
```
GET /users
Accept: application/vnd.myapi.v2+json
```

### Versioning Guidelines

- Start with v1
- Maintain backwards compatibility when possible
- Deprecate old versions with notice
- Document breaking changes

## Authentication & Authorization

### Authentication Methods

1. **JWT Bearer Token**
```http
Authorization: Bearer <token>
```

2. **API Key**
```http
X-API-Key: <key>
```

3. **OAuth 2.0**
```http
Authorization: Bearer <access_token>
```

### Authorization

- Use roles/permissions
- Document required permissions per endpoint
- Return 403 for authorization failures

## Rate Limiting

```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1631234567
```

**Recommended limits:**
- Public APIs: 100-1000 requests/hour
- Authenticated APIs: 1000-10000 requests/hour
- Webhooks: 10-100 requests/minute

## Documentation Requirements

- All endpoints documented
- Request/response examples
- Authentication requirements
- Error response formats
- Rate limits
- SDK examples (if available)

## Scripts

Generate API scaffold:
```bash
python scripts/generate_api.py <resource-name>
```

Validate API design:
```bash
python scripts/validate_api.py openapi.yaml
```

## References

- `references/rest-patterns.md` - REST design patterns
- `references/graphql-patterns.md` - GraphQL design patterns
- [REST API Tutorial](https://restfulapi.net/)
- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)
