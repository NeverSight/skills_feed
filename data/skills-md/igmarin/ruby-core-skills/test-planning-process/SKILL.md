---
name: test-planning-process
license: MIT
description: >
  Selects test boundaries, identifies test cases (happy path, edge case, error), picks the first
  failing test before writing any test code, tests at highest boundary directly expressing
  business goal (request for HTTP/JSON shape, service for domain invariants, unit for
  calculations), requires synthetic test data (never real production
  values), and runs the failing test skeleton to verify Red before proceeding to `tdd-process`.
  Use when the user needs to plan test coverage, determine test boundaries, or decide what tests
  to write before implementation. Trigger words: test plan, planning tests, test boundaries,
  test matrix, test strategy, first failing test.
metadata:
  version: 1.0.0
  user-invocable: "true"
  type: "process-discipline"
---
# Test Planning Process

## Quick Reference

| Dimension | Rule |
|-----------|------|
| **Test Boundary** | Test at the highest boundary that directly expresses the feature's business goal (e.g. integration/request vs unit) |
| **Coverage Goal** | Cover all primary paths, all input boundary values, and all expected error flows |
| **First Failing Test** | Select the single simplest assertion that will fail on the current code and prove the feature is missing |
| **Isolation** | Isolate tests from external networks, dates, and shared database states |

## HARD-GATE

```text
TEST PLANNING GATES:
1. DO NOT write test cases without defining a test plan first.
2. ALWAYS start testing at the most relevant boundary (don't write 10 unit tests for a feature that needs a request test, and vice versa).
3. The first failing test MUST be identified explicitly in the plan before writing it.
4. All test data must be synthetic; never use real production values or API payloads in test plans.
```

## Process Steps

### Step 1: Determine the Test Boundary
Identify where the behavior is observed:
- **Request / API Boundary:** Use when verifying HTTP statuses, headers, query parsing, or JSON payload structures.
- **Service / Business Boundary:** Use when validating domain invariants, complex calculations, or coordination between objects.
- **Unit Boundary:** Use when verifying low-level calculations, state changes on a single object, or formatting logic.

### Step 2: List the Test Cases
For the selected boundary, map out the test matrix:
1. **Happy Paths:** Standard expected execution flows.
2. **Boundary Values:** Zero, nil, empty strings, maximum lengths, negative values.
3. **Error Paths:** Invalid inputs, database failures, external service timeouts, auth failures.

### Step 3: Select the First Failing Test
- Choose the single simplest test case from the matrix that is expected to fail on the current code.
- This serves as the initial "Red" state to kick off the TDD loop.

### Step 4: Plan Test Isolation
- Identify any external dependencies (network APIs, system clocks, file systems).
- Plan mocks, stubs, or test doubles to isolate the tests and prevent flaky failures.

---

## Checkpoint Pattern

Align with the user:
1. **Test Plan Proposal:** Present the target boundary, the list of happy/edge/error cases, and specify which test will be the first failing test.
2. **Handoff:** Present the skeleton code for the first failing test before writing any implementation.

---

## Inline Example

### Feature: `POST /users` — create a new user account

**Selected Boundary:** Request / API (verifies HTTP status and JSON response shape)

| # | Type | Description | Expected Result | First Failing? |
|---|------|-------------|-----------------|----------------|
| 1 | Happy path | Valid email + password | `201 Created`, body contains `id` | ✅ Yes |
| 2 | Boundary | Password at minimum length (8 chars) | `201 Created` | |
| 3 | Error | Missing email field | `422 Unprocessable Entity` | |
| 4 | Error | Duplicate email already in database | `409 Conflict` | |

**First Failing Test — skeleton (Python / pytest + requests):**

```python
def test_create_user_returns_201_with_id(client):
    payload = {"email": "alice@example.test", "password": "s3cr3t!X"}
    response = client.post("/users", json=payload)
    assert response.status_code == 201
    assert "id" in response.json()
```

**First Failing Test — skeleton (JavaScript / Jest + supertest):**

```js
test('POST /users returns 201 with id for valid payload', async () => {
  const res = await request(app)
    .post('/users')
    .send({ email: 'alice@example.test', password: 's3cr3t!X' });
  expect(res.status).toBe(201);
  expect(res.body).toHaveProperty('id');
});
```

Run the skeleton as-is — it should fail (Red). Proceed to `tdd-process` to make it pass.

---

## Anti-Patterns

- **Coverage Blindness:** Happy-path-only tests with no error/edge cases.
- **Low-Value Testing:** Hundreds of unit tests for trivial methods with zero integration coverage.
- **Shared State Leaks:** Tests that write to a shared database or file without cleanup.

## Integration

| Context | Next Skill |
|---------|----------|
| Writing the failing test | **tdd-process** |
| General design modeling | **model-domain** |
