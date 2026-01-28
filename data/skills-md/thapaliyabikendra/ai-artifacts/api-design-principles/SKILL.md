---
name: api-design-principles
description: "Master REST API design principles to build intuitive, scalable, and maintainable APIs. Use when designing new APIs, reviewing API specifications, or establishing API design standards."
layer: 2
tech_stack: [agnostic]
topics: [rest-api, versioning, pagination, http-methods, status-codes, api-design]
depends_on: []
complements: [technical-design-patterns, abp-api-implementation]
keywords: [REST, API, Endpoint, GET, POST, PUT, DELETE, OpenAPI, Swagger, HTTP]
---

# API Design Principles

Master REST API design principles to build intuitive, scalable, and maintainable APIs. This skill focuses on **design theory** - for implementation patterns, see `abp-api-implementation` or `abp-service-patterns`.

## When to Use This Skill

- Designing new REST API contracts
- Reviewing API specifications before implementation
- Establishing API design standards for your team
- Planning API versioning and evolution strategy
- Creating developer-friendly API documentation

## Audience

- **Backend Architects** - API contract design
- **Tech Leads** - Standards and review
- **Business Analysts** - Understanding API capabilities

> **For Implementation**: Use `abp-service-patterns` for AppService code, `api-response-patterns` for response wrappers, `fluentvalidation-patterns` for validation.

---

## Core Principles

### 1. Resource-Oriented Design

APIs expose **resources** (nouns), not **actions** (verbs).

| Concept | Good | Bad |
|---------|------|-----|
| Resource naming | `/patients`, `/appointments` | `/getPatients`, `/createAppointment` |
| Actions via HTTP methods | `POST /patients` | `POST /createPatient` |
| Plural for collections | `/patients` | `/patient` |
| Consistent casing | `kebab-case` or `camelCase` | Mixed styles |

**Resource Hierarchy**:
```
/api/v1/patients                    # Collection
/api/v1/patients/{id}               # Single resource
/api/v1/patients/{id}/appointments  # Nested collection
/api/v1/appointments/{id}           # Direct access to nested resource
```

**Avoid Deep Nesting** (max 2 levels):
```
# Good - Shallow
GET /api/v1/patients/{id}/appointments
GET /api/v1/appointments/{id}

# Bad - Too deep
GET /api/v1/clinics/{id}/doctors/{id}/patients/{id}/appointments/{id}
```

### 2. HTTP Methods Semantics

| Method | Purpose | Idempotent | Safe | Request Body |
|--------|---------|------------|------|--------------|
| `GET` | Retrieve resource(s) | Yes | Yes | No |
| `POST` | Create resource | No | No | Yes |
| `PUT` | Replace entire resource | Yes | No | Yes |
| `PATCH` | Partial update | Yes* | No | Yes |
| `DELETE` | Remove resource | Yes | No | No |

**Idempotent**: Multiple identical requests produce same result.
**Safe**: Does not modify server state.

### 3. HTTP Status Codes

**Success (2xx)**:
| Code | Meaning | Use When |
|------|---------|----------|
| `200 OK` | Success | GET, PUT, PATCH succeeded |
| `201 Created` | Resource created | POST succeeded |
| `204 No Content` | Success, no body | DELETE succeeded |

**Client Errors (4xx)**:
| Code | Meaning | Use When |
|------|---------|----------|
| `400 Bad Request` | Malformed request | Invalid JSON, missing required headers |
| `401 Unauthorized` | Not authenticated | Missing or invalid token |
| `403 Forbidden` | Not authorized | Valid token, insufficient permissions |
| `404 Not Found` | Resource doesn't exist | ID not found |
| `409 Conflict` | State conflict | Duplicate email, version mismatch |
| `422 Unprocessable Entity` | Validation failed | Business rule violations |
| `429 Too Many Requests` | Rate limited | Exceeded request quota |

**Server Errors (5xx)**:
| Code | Meaning | Use When |
|------|---------|----------|
| `500 Internal Server Error` | Unexpected error | Unhandled exception |
| `503 Service Unavailable` | Temporarily down | Maintenance, overload |

---

## Design Patterns

### Pattern 1: Pagination

**Always paginate collections** - Never return unbounded lists.

**Offset-Based** (simple, good for small datasets):
```
GET /api/v1/patients?page=2&pageSize=20

Response:
{
  "items": [...],
  "totalCount": 150,
  "pageNumber": 2,
  "pageSize": 20,
  "totalPages": 8
}
```

**Cursor-Based** (efficient for large datasets, real-time data):
```
GET /api/v1/patients?cursor=eyJpZCI6MTIzfQ&limit=20

Response:
{
  "items": [...],
  "nextCursor": "eyJpZCI6MTQzfQ",
  "hasMore": true
}
```

| Approach | Pros | Cons | Best For |
|----------|------|------|----------|
| Offset | Simple, supports jumping to page | Slow on large datasets, inconsistent with real-time data | Admin panels, reports |
| Cursor | Fast, consistent | Can't jump to arbitrary page | Infinite scroll, feeds |

### Pattern 2: Filtering and Sorting

**Query Parameters for Filtering**:
```
GET /api/v1/patients?status=active
GET /api/v1/patients?status=active&createdAfter=2025-01-01
GET /api/v1/patients?doctorId=abc-123
```

**Sorting**:
```
GET /api/v1/patients?sorting=name
GET /api/v1/patients?sorting=createdAt desc
GET /api/v1/patients?sorting=lastName,firstName
```

**Searching**:
```
GET /api/v1/patients?filter=john
GET /api/v1/patients?search=john doe
```

**Design Decisions**:
- Use `WhereIf` pattern - only apply filter if parameter provided
- Define allowed sort fields (security - don't expose internal fields)
- Set maximum page size (prevent abuse)

### Pattern 3: Error Response Design

**Consistent Structure**:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "One or more validation errors occurred.",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format."
      },
      {
        "field": "dateOfBirth",
        "message": "Date of birth cannot be in the future."
      }
    ],
    "traceId": "00-abc123-def456-00"
  }
}
```

**Error Codes** (for client handling):
| Code | HTTP Status | Meaning |
|------|-------------|---------|
| `VALIDATION_ERROR` | 422 | Input validation failed |
| `NOT_FOUND` | 404 | Resource doesn't exist |
| `UNAUTHORIZED` | 401 | Authentication required |
| `FORBIDDEN` | 403 | Permission denied |
| `CONFLICT` | 409 | State conflict |
| `RATE_LIMITED` | 429 | Too many requests |

### Pattern 4: Versioning Strategy

**URL Versioning** (Recommended for ABP):
```
/api/v1/patients
/api/v2/patients
```

| Strategy | Example | Pros | Cons |
|----------|---------|------|------|
| URL Path | `/api/v1/` | Clear, easy routing | Multiple URLs |
| Header | `Api-Version: 1` | Clean URLs | Hidden, harder to test |
| Query Param | `?version=1` | Easy testing | Can be forgotten |

**Versioning Policy**:
- Major version for breaking changes
- Support N-1 version minimum
- Deprecation notice 6+ months before removal
- Document migration path

### Pattern 5: Resource Relationships

**Embedding vs Linking**:

```json
// Embedded (fewer requests, larger payload)
{
  "id": "patient-123",
  "name": "John Doe",
  "doctor": {
    "id": "doctor-456",
    "name": "Dr. Smith"
  }
}

// Linked (smaller payload, more requests)
{
  "id": "patient-123",
  "name": "John Doe",
  "doctorId": "doctor-456"
}

// Hybrid (with expand parameter)
GET /api/v1/patients/123?expand=doctor,appointments
```

**Decision Criteria**:
| Use Embedding | Use Linking |
|---------------|-------------|
| Related data always needed | Related data rarely needed |
| Few relationships | Many relationships |
| Related data is small | Related data is large |

---

## API Contract Checklist

### Resource Design
- [ ] Resources are nouns, not verbs
- [ ] Plural names for collections
- [ ] Consistent naming convention
- [ ] Max 2 levels of nesting
- [ ] All CRUD mapped to correct HTTP methods

### Request/Response
- [ ] All collections paginated
- [ ] Default and max page size defined
- [ ] Filter parameters documented
- [ ] Sorting parameters documented
- [ ] Consistent error response format

### Security
- [ ] Authentication method defined
- [ ] Authorization on all mutating endpoints
- [ ] Rate limiting configured
- [ ] Sensitive data not in URLs
- [ ] CORS configured

### Documentation
- [ ] OpenAPI/Swagger spec
- [ ] All endpoints documented
- [ ] Request/response examples
- [ ] Error responses documented

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Verb endpoints | `POST /createPatient` | `POST /patients` |
| Ignoring HTTP methods | Using POST for everything | Use appropriate method |
| No pagination | Returning 10,000 items | Always paginate |
| Inconsistent errors | Different formats per endpoint | Standardize error structure |
| Exposing internals | Database columns in API | Design API contract separately |
| No versioning | Breaking changes break clients | Version from day one |
| Deep nesting | `/a/{id}/b/{id}/c/{id}/d` | Flatten, max 2 levels |

---

## Integration with Other Skills

| Need | Skill |
|------|-------|
| **AppService implementation** | `abp-service-patterns` |
| **Response wrappers** | `api-response-patterns` |
| **Input validation** | `fluentvalidation-patterns` |
| **Query optimization** | `linq-optimization-patterns` |
| **Technical design docs** | `technical-design-patterns` |

---

## References

- `references/rest-best-practices.md` - Detailed REST patterns
- `assets/api-design-checklist.md` - Pre-implementation checklist
