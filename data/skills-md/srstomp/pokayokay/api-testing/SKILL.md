---
name: api-testing
description: Test APIs with integration tests, contract tests, and E2E validation. Covers Jest, Vitest, and Supertest for Node.js/TypeScript APIs. Includes test data management, fixtures, factories, environment configuration, CI/CD integration, mocking external services, and contract testing with OpenAPI validation. Use this skill when building test suites for REST APIs, validating API contracts, or setting up API testing infrastructure.
---

# API Integration Testing

Build robust test suites for your APIs.

## Testing Pyramid for APIs

```
                    ▲
                   ▲▲▲  E2E Tests
                  ▲▲▲▲▲  (Full stack, real DB, slow)
                 ▲▲▲▲▲▲▲
                ▲▲▲▲▲▲▲▲▲  Contract Tests
               ▲▲▲▲▲▲▲▲▲▲▲  (API shape validation)
              ▲▲▲▲▲▲▲▲▲▲▲▲▲
             ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲  Integration Tests
            ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲  (API + DB, services)
           ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲
          ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲  Unit Tests
         ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲  (Handlers, validators, utils)
```

| Level | What It Tests | Speed | Isolation |
|-------|---------------|-------|-----------|
| **Unit** | Individual functions, validators | Fast | High |
| **Integration** | API + database, services together | Medium | Medium |
| **Contract** | API shape matches spec | Fast | High |
| **E2E** | Full request flow, real environment | Slow | Low |

## Test Types Overview

### Integration Tests

Test your API endpoints with real (or test) database.

```typescript
describe('POST /users', () => {
  it('creates a user with valid input', async () => {
    const response = await request(app)
      .post('/users')
      .send({ email: 'test@example.com', name: 'Test User' })
      .expect(201);

    expect(response.body).toMatchObject({
      id: expect.any(String),
      email: 'test@example.com',
      name: 'Test User',
    });
  });
});
```

### Contract Tests

Validate API responses match your OpenAPI spec.

```typescript
it('matches OpenAPI schema', async () => {
  const response = await request(app).get('/users/1');
  
  expect(response.body).toMatchSchema('User');
});
```

### E2E Tests

Test complete flows across multiple endpoints.

```typescript
describe('User registration flow', () => {
  it('registers, verifies email, and logs in', async () => {
    // 1. Register
    const registerRes = await request(app)
      .post('/auth/register')
      .send({ email: 'new@example.com', password: 'secure123' });
    
    // 2. Verify email (simulate)
    const token = await getVerificationToken('new@example.com');
    await request(app)
      .post('/auth/verify')
      .send({ token });
    
    // 3. Login
    const loginRes = await request(app)
      .post('/auth/login')
      .send({ email: 'new@example.com', password: 'secure123' })
      .expect(200);
    
    expect(loginRes.body.accessToken).toBeDefined();
  });
});
```

## Core Principles

### 1. Test Behavior, Not Implementation

```typescript
// ❌ Testing implementation
it('calls userRepository.save', async () => {
  await request(app).post('/users').send(userData);
  expect(mockRepository.save).toHaveBeenCalled();
});

// ✅ Testing behavior
it('creates user and returns 201', async () => {
  const response = await request(app)
    .post('/users')
    .send(userData)
    .expect(201);
  
  expect(response.body.email).toBe(userData.email);
});
```

### 2. Isolate Tests

```typescript
// ✅ Each test sets up its own data
beforeEach(async () => {
  await db.clear();
});

it('test 1', async () => {
  const user = await createUser({ email: 'test1@example.com' });
  // Test with user...
});

it('test 2', async () => {
  const user = await createUser({ email: 'test2@example.com' });
  // Test with user...
});
```

### 3. Test Error Paths

```typescript
describe('POST /users', () => {
  it('returns 400 for invalid email', async () => {
    const response = await request(app)
      .post('/users')
      .send({ email: 'invalid', name: 'Test' })
      .expect(400);
    
    expect(response.body.errors).toContainEqual(
      expect.objectContaining({ field: 'email' })
    );
  });

  it('returns 409 for duplicate email', async () => {
    await createUser({ email: 'exists@example.com' });
    
    await request(app)
      .post('/users')
      .send({ email: 'exists@example.com', name: 'Test' })
      .expect(409);
  });

  it('returns 401 without authentication', async () => {
    await request(app)
      .get('/users/me')
      .expect(401);
  });
});
```

### 4. Use Realistic Test Data

```typescript
// ❌ Lazy test data
const user = { email: 'a@b.c', name: 'x' };

// ✅ Realistic test data
const user = {
  email: 'john.smith@company.com',
  name: 'John Smith',
  role: 'admin',
};

// ✅ Or use factories
const user = createUser({ role: 'admin' });
```

### 5. Assert Precisely

```typescript
// ❌ Vague assertion
expect(response.body).toBeDefined();

// ❌ Over-specific (brittle)
expect(response.body).toEqual({
  id: '123e4567-e89b-12d3-a456-426614174000',
  email: 'test@example.com',
  createdAt: '2024-01-15T10:30:00.000Z',
  // ... every field
});

// ✅ Assert what matters
expect(response.body).toMatchObject({
  email: 'test@example.com',
  name: 'Test User',
});
expect(response.body.id).toMatch(/^[0-9a-f-]{36}$/);
```

## Quick Start

### Project Structure

```
src/
├── routes/
├── services/
└── app.ts

tests/
├── setup.ts              # Global setup
├── helpers/
│   ├── request.ts        # Supertest wrapper
│   ├── factories.ts      # Test data factories
│   └── auth.ts           # Auth helpers
├── integration/
│   ├── users.test.ts
│   └── orders.test.ts
├── contracts/
│   └── openapi.test.ts
└── e2e/
    └── checkout.test.ts
```

### Basic Test File

```typescript
// tests/integration/users.test.ts
import { describe, it, expect, beforeEach, afterAll } from 'vitest';
import request from 'supertest';
import { app } from '../../src/app';
import { db } from '../helpers/db';
import { createUser } from '../helpers/factories';

describe('Users API', () => {
  beforeEach(async () => {
    await db.clear('users');
  });

  afterAll(async () => {
    await db.close();
  });

  describe('GET /users/:id', () => {
    it('returns user by id', async () => {
      const user = await createUser({ name: 'John' });

      const response = await request(app)
        .get(`/users/${user.id}`)
        .expect(200);

      expect(response.body.name).toBe('John');
    });

    it('returns 404 for non-existent user', async () => {
      await request(app)
        .get('/users/non-existent-id')
        .expect(404);
    });
  });
});
```

## What to Test

### Always Test

- ✅ Success cases (200, 201, 204)
- ✅ Validation errors (400, 422)
- ✅ Authentication (401)
- ✅ Authorization (403)
- ✅ Not found (404)
- ✅ Conflict (409)
- ✅ Server errors (500) - verify graceful handling

### Test When Relevant

- Pagination (limit, offset, cursors)
- Filtering and sorting
- Rate limiting
- Caching headers
- CORS headers
- Content negotiation

### Skip or Minimize

- Framework internals
- Third-party library behavior
- Database driver behavior

## Anti-Patterns

### ❌ Shared Mutable State

```typescript
// BAD: Tests depend on each other
let userId: string;

it('creates user', async () => {
  const res = await request(app).post('/users').send(data);
  userId = res.body.id; // Other tests depend on this
});

it('gets user', async () => {
  await request(app).get(`/users/${userId}`); // Fails if run alone
});
```

### ❌ Testing Against Production

```typescript
// BAD: Never test against production
const API_URL = process.env.NODE_ENV === 'test' 
  ? 'https://api.production.com'  // NO!
  : 'http://localhost:3000';
```

### ❌ Ignoring Cleanup

```typescript
// BAD: Data leaks between tests
it('creates user', async () => {
  await request(app).post('/users').send({ email: 'test@example.com' });
  // Never cleaned up
});

it('creates another user', async () => {
  // May fail due to duplicate email from previous test
  await request(app).post('/users').send({ email: 'test@example.com' });
});
```

### ❌ Overly Broad Tests

```typescript
// BAD: Testing everything in one test
it('user CRUD', async () => {
  // Create
  const createRes = await request(app).post('/users').send(data);
  // Read
  const getRes = await request(app).get(`/users/${createRes.body.id}`);
  // Update
  const updateRes = await request(app).put(`/users/${createRes.body.id}`).send(newData);
  // Delete
  await request(app).delete(`/users/${createRes.body.id}`);
  // Too many assertions, hard to debug failures
});
```

### ❌ Sleeping Instead of Waiting

```typescript
// BAD: Arbitrary sleep
it('processes async job', async () => {
  await request(app).post('/jobs').send(data);
  await sleep(5000); // Flaky and slow
  const result = await request(app).get('/jobs/1');
});

// GOOD: Poll or use callbacks
it('processes async job', async () => {
  const { body } = await request(app).post('/jobs').send(data);
  await waitForJobCompletion(body.id, { timeout: 10000 });
  const result = await request(app).get(`/jobs/${body.id}`);
});
```

## Checklist

### Test Suite Setup
- [ ] Test framework configured (Jest or Vitest)
- [ ] Supertest installed and configured
- [ ] Test database configured
- [ ] Cleanup between tests
- [ ] Factories for test data
- [ ] Auth helpers for protected routes
- [ ] Environment variables for test config

### Per-Endpoint Coverage
- [ ] Success case (happy path)
- [ ] Validation errors
- [ ] Authentication required
- [ ] Authorization (role-based)
- [ ] Not found handling
- [ ] Edge cases (empty, large data)

### CI/CD Integration
- [ ] Tests run on every PR
- [ ] Test database provisioned in CI
- [ ] Environment secrets configured
- [ ] Test reports generated
- [ ] Coverage thresholds set

---

**References:**
- [references/test-frameworks.md](references/test-frameworks.md) — Jest and Vitest setup with Supertest
- [references/test-patterns.md](references/test-patterns.md) — Integration, E2E, and authentication testing patterns
- [references/test-data.md](references/test-data.md) — Fixtures, factories, database setup and cleanup
- [references/contract-testing.md](references/contract-testing.md) — OpenAPI validation, schema testing
- [references/ci-cd.md](references/ci-cd.md) — Pipeline integration, environments, reporting
