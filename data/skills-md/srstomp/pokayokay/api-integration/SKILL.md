---
name: api-integration
description: Consume external APIs with type safety, robust error handling, and production-ready patterns. Handles OpenAPI/Swagger specs, GraphQL schemas, REST documentation, and example requests. Produces typed clients with authentication, retry logic, and comprehensive error handling. Primary focus on TypeScript with patterns applicable to other languages. Use this skill when integrating third-party APIs, generating API clients, or implementing authentication flows.
---

# API Integration

Build robust, type-safe API clients from specs and documentation.

## Integration Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                         INPUTS                              │
├──────────────┬──────────────┬──────────────┬────────────────┤
│ OpenAPI/     │ GraphQL      │ REST Docs    │ Example        │
│ Swagger      │ Schema       │ (informal)   │ Requests       │
└──────┬───────┴──────┬───────┴──────┬───────┴───────┬────────┘
       │              │              │               │
       └──────────────┴──────────────┴───────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │      ANALYSIS & DESIGN        │
              │  • Extract types/schemas      │
              │  • Identify auth requirements │
              │  • Map error responses        │
              │  • Plan client architecture   │
              └───────────────┬───────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │       IMPLEMENTATION          │
              │  • Generate/write types       │
              │  • Build client layer         │
              │  • Implement auth flow        │
              │  • Add error handling         │
              │  • Configure retry logic      │
              └───────────────┬───────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │         TESTING               │
              │  • Mock responses             │
              │  • Integration tests          │
              │  • Error scenario tests       │
              └───────────────────────────────┘
```

## Input Analysis

### OpenAPI/Swagger

**Best case**: Full spec with schemas, auth, error responses.

Extract:
- Base URL(s) and environments
- Authentication schemes
- Endpoint paths and methods
- Request/response schemas
- Error response formats
- Rate limit headers

### GraphQL

Extract:
- Schema types and operations
- Authentication headers
- Error format (errors array)
- Pagination patterns (cursor, offset)

### Informal REST Docs

When no formal spec exists:
1. Document observed endpoints
2. Infer types from examples
3. Test edge cases to discover error formats
4. Note undocumented behaviors

### Example Requests

From cURL, Postman, or code samples:
1. Extract base URL, headers, auth pattern
2. Infer request/response types
3. Note required vs optional fields
4. Identify query params vs body

## Client Architecture Decision

```
How complex is the integration?
│
├── Simple (1-5 endpoints, basic auth)
│   └── Typed fetch wrapper
│
├── Medium (5-20 endpoints, OAuth/multiple resources)
│   └── Service class with methods per endpoint
│
└── Complex (20+ endpoints, multiple auth schemes, heavy usage)
    └── Generated client + custom wrapper layer
```

### Architecture Quick Reference

| Complexity | Pattern | When to Use |
|------------|---------|-------------|
| Simple | Typed functions | Few endpoints, one-off integration |
| Medium | Service class | Core integration, team will maintain |
| Complex | Generated + wrapper | Large API, frequent updates, critical path |

## Core Principles

### 1. Type Everything

```typescript
// ❌ Untyped
const user = await api.get('/users/1');

// ✅ Typed
const user = await api.get<User>('/users/1');

// ✅ Even better: validated at runtime
const user = await api.get('/users/1', { schema: UserSchema });
```

### 2. Fail Explicitly

```typescript
// ❌ Silent failure
const data = response.data ?? {};

// ✅ Explicit error
if (!response.ok) {
  throw new ApiError(response.status, await response.json());
}
```

### 3. Auth is a First-Class Concern

```typescript
// ❌ Auth scattered everywhere
fetch(url, { headers: { Authorization: `Bearer ${token}` } });

// ✅ Auth handled by client
const client = createApiClient({ auth: tokenProvider });
```

### 4. Retry Intelligently

```typescript
// ❌ Retry everything
retry(request, { attempts: 3 });

// ✅ Retry only idempotent + transient failures
retry(request, {
  attempts: 3,
  when: (error) => error.status >= 500 || error.code === 'NETWORK_ERROR',
  methods: ['GET', 'PUT', 'DELETE'], // Not POST
});
```

### 5. Isolate the Integration

```typescript
// ❌ API details leak everywhere
const response = await fetch(`${API_URL}/users/${id}`);
const user = response.data.data.attributes;

// ✅ Transform at boundary
// In api client:
async getUser(id: string): Promise<User> {
  const response = await this.get(`/users/${id}`);
  return transformUser(response.data);
}
```

## Quick Patterns

### Typed Fetch Wrapper

```typescript
async function api<T>(
  path: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });

  if (!response.ok) {
    throw await ApiError.fromResponse(response);
  }

  return response.json();
}

// Usage
const user = await api<User>('/users/1');
```

### Service Class

```typescript
class UserService {
  constructor(private client: ApiClient) {}

  async getUser(id: string): Promise<User> {
    return this.client.get(`/users/${id}`);
  }

  async createUser(data: CreateUserInput): Promise<User> {
    return this.client.post('/users', data);
  }

  async updateUser(id: string, data: UpdateUserInput): Promise<User> {
    return this.client.put(`/users/${id}`, data);
  }

  async deleteUser(id: string): Promise<void> {
    return this.client.delete(`/users/${id}`);
  }
}
```

### Error Classification

```typescript
class ApiError extends Error {
  constructor(
    public status: number,
    public code: string,
    public details?: unknown
  ) {
    super(`API Error: ${code}`);
  }

  get isRetryable(): boolean {
    return this.status >= 500 || this.status === 429;
  }

  get isAuthError(): boolean {
    return this.status === 401 || this.status === 403;
  }

  get isValidationError(): boolean {
    return this.status === 400 || this.status === 422;
  }

  get isNotFound(): boolean {
    return this.status === 404;
  }
}
```

## Anti-Patterns

### ❌ Stringly-Typed APIs

```typescript
// Bad: No type safety
const user = await api.get('/users/' + id);
user.nmae; // Typo not caught
```

### ❌ Swallowing Errors

```typescript
// Bad: Errors disappear
try {
  return await api.getUser(id);
} catch {
  return null;
}
```

### ❌ Hardcoded Auth

```typescript
// Bad: Can't refresh, can't test
const headers = { Authorization: 'Bearer abc123' };
```

### ❌ Retry Without Backoff

```typescript
// Bad: Hammers failing server
while (attempts < 3) {
  try { return await request(); } catch { attempts++; }
}
```

### ❌ No Request/Response Logging

```typescript
// Bad: Can't debug production issues
// No logging at all
```

### ❌ Mixing API Shapes with Domain Models

```typescript
// Bad: API response shape leaks into app
function UserProfile({ user }: { user: ApiUserResponse }) {
  return <div>{user.data.attributes.name}</div>;
}
```

## Implementation Checklist

### Before Starting
- [ ] Obtained API credentials/keys
- [ ] Located API documentation (spec, docs, examples)
- [ ] Identified authentication method
- [ ] Understood rate limits
- [ ] Identified error response format

### Client Implementation
- [ ] Types generated/defined for all endpoints
- [ ] Base client with auth handling
- [ ] Error class with classification
- [ ] Retry logic for transient failures
- [ ] Request/response logging (redacted)
- [ ] Timeout configuration

### Error Handling
- [ ] All error responses typed
- [ ] Retry logic for 5xx and network errors
- [ ] Auth refresh on 401 (if applicable)
- [ ] Rate limit handling (429)
- [ ] Graceful degradation strategy

### Testing
- [ ] Mocks for all endpoints
- [ ] Error scenario tests
- [ ] Auth flow tests
- [ ] Retry logic tests
- [ ] Integration test with real API (CI)

---

**References:**
- [references/openapi-consumption.md](references/openapi-consumption.md) — Parsing specs, type generation, codegen tools
- [references/client-architecture.md](references/client-architecture.md) — Client patterns, service layers, request handling
- [references/error-handling.md](references/error-handling.md) — Error types, retry logic, circuit breakers
- [references/authentication.md](references/authentication.md) — OAuth, API keys, JWT, token refresh
- [references/testing.md](references/testing.md) — Mocking, integration tests, contract testing
