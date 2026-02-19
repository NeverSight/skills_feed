---
name: api-design
description: >-
  Guide API design for REST, GraphQL, gRPC, and CLI interfaces. Use this skill
  when designing new APIs, reviewing existing API contracts, or establishing
  API conventions for a project. Produces consistent, well-documented API
  specifications.
---

# API Design

Design consistent, well-documented APIs across REST, GraphQL, gRPC, and CLI interfaces.

## When to Use

- Designing new API endpoints or commands
- Reviewing existing API contracts for consistency
- Establishing API naming and versioning conventions
- Planning backward-compatible API changes
- Generating API documentation or OpenAPI specs

## Principles

1. **Consistency** - Same patterns everywhere (naming, error format, pagination)
2. **Discoverability** - A developer should guess the right endpoint/flag without reading docs
3. **Backward compatibility** - Additions are safe; removals and renames require versioning
4. **Minimal surface** - Expose only what consumers need; internal details stay internal
5. **Self-describing errors** - Error responses should tell the caller what went wrong and how to fix it

## REST API Checklist

### Naming

- Use plural nouns for resources: `/users`, `/tasks`
- Use kebab-case for multi-word paths: `/task-boards`
- Nest for ownership: `/users/{id}/tasks`
- Use verbs only for actions that don't map to CRUD: `/tasks/{id}/approve`

### HTTP Methods

| Method | Purpose | Idempotent |
|--------|---------|------------|
| GET | Read | Yes |
| POST | Create / action | No |
| PUT | Full replace | Yes |
| PATCH | Partial update | Yes |
| DELETE | Remove | Yes |

### Response Format

```json
{
  "data": { ... },
  "meta": { "page": 1, "total": 42 }
}
```

Error format:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable description",
    "details": [
      { "field": "email", "reason": "required" }
    ]
  }
}
```

### Status Codes

| Code | Use |
|------|-----|
| 200 | Success (with body) |
| 201 | Created |
| 204 | Success (no body) |
| 400 | Client error (validation) |
| 401 | Not authenticated |
| 403 | Not authorized |
| 404 | Not found |
| 409 | Conflict (duplicate, state mismatch) |
| 422 | Unprocessable (semantically invalid) |
| 500 | Server error |

### Pagination

Use cursor-based for large datasets, offset-based for simple cases:

```
GET /tasks?cursor=abc123&limit=20
GET /tasks?page=2&per_page=20
```

### Versioning

- Prefer URL prefix: `/v1/tasks`, `/v2/tasks`
- Use header-based only when URL versioning is impractical

## CLI API Checklist

### Command Structure

```
<tool> <noun> <verb> [args] [--flags]
```

Example: `synapse tasks create "Title" --priority 3`

### Flag Conventions

- Long form: `--output`, `--verbose`
- Short form for common flags: `-o`, `-v`
- Boolean flags: `--force`, `--no-color`
- Repeatable: `--attach file1 --attach file2`
- Mutually exclusive groups: `--response | --no-response`

### Output

- Default: human-readable
- `--json`: machine-readable JSON
- `--quiet` / `-q`: minimal output
- Exit codes: 0 = success, 1 = error, 2 = usage error

## Workflow

### Step 1: Define Resources / Commands

List the entities and actions the API must support.

### Step 2: Map to Endpoints / Subcommands

Apply naming conventions to produce the API surface.

### Step 3: Define Request / Response Schemas

Specify required and optional fields, types, and validation rules.

### Step 4: Document Error Cases

For each endpoint, list possible error responses and their meaning.

### Step 5: Review for Consistency

Cross-check naming, error format, and pagination across all endpoints.
