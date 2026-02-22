---
name: api-tester
description: >-
  Test REST and GraphQL API endpoints with structured assertions and reporting.
  Use when a user asks to test an API, hit an endpoint, check if an API works,
  validate a response, debug an API call, test authentication flows, or verify
  API contracts. Supports GET, POST, PUT, PATCH, DELETE with headers, body,
  auth, and response validation.
license: Apache-2.0
compatibility: "Requires curl or Python 3.9+ with requests library"
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: development
  tags: ["api", "testing", "rest", "graphql", "http"]
---

# API Tester

## Overview

Test API endpoints by sending HTTP requests, validating responses, and reporting results. Supports REST and GraphQL APIs with authentication, custom headers, request bodies, and structured assertions on status codes, headers, and response payloads.

## Instructions

When a user asks you to test or debug an API endpoint, follow these steps:

### Step 1: Gather endpoint details

Determine from the user or codebase:
- **URL**: The full endpoint URL
- **Method**: GET, POST, PUT, PATCH, DELETE
- **Headers**: Content-Type, Authorization, custom headers
- **Body**: JSON payload, form data, or query parameters
- **Auth**: Bearer token, API key, basic auth
- **Expected response**: Status code, response shape, specific values

### Step 2: Send the request

**Using curl (preferred for quick tests):**

```bash
# GET request
curl -s -w "\nHTTP Status: %{http_code}\nTime: %{time_total}s\n" \
  -H "Authorization: Bearer $TOKEN" \
  "https://api.example.com/users?page=1"

# POST request with JSON
curl -s -w "\nHTTP Status: %{http_code}\nTime: %{time_total}s\n" \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "Jane", "email": "jane@example.com"}' \
  "https://api.example.com/users"
```

**Using Python (for complex flows):**

```python
import requests
import json
import time

def test_endpoint(method, url, headers=None, body=None, expected_status=200):
    start = time.time()
    response = requests.request(method, url, headers=headers, json=body, timeout=30)
    elapsed = time.time() - start

    result = {
        "status": response.status_code,
        "time_ms": round(elapsed * 1000),
        "headers": dict(response.headers),
        "body": response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text,
    }

    passed = response.status_code == expected_status
    print(f"{'PASS' if passed else 'FAIL'} | {method} {url} | {response.status_code} | {result['time_ms']}ms")
    return result, passed
```

### Step 3: Validate the response

Check these in order:
1. **Status code** matches expected (200, 201, 204, 400, 401, 404, etc.)
2. **Response time** is acceptable (flag if > 2 seconds)
3. **Content-Type** header matches expected format
4. **Response body** structure matches expected schema
5. **Specific values** match assertions

```python
def validate_response(result, assertions):
    failures = []
    body = result["body"]

    for field, expected in assertions.items():
        actual = body
        for key in field.split("."):
            if isinstance(actual, dict):
                actual = actual.get(key)
            elif isinstance(actual, list) and key.isdigit():
                actual = actual[int(key)]
            else:
                actual = None
                break

        if actual != expected:
            failures.append(f"  {field}: expected {expected!r}, got {actual!r}")

    return failures
```

### Step 4: Report results

Format as a clear test report:

```
API Test Results
================
Endpoint: POST /api/users
Status:   201 Created (expected 201) -- PASS
Time:     142ms
Body:     Valid JSON, 3 fields

Assertions:
  [PASS] body.id is present
  [PASS] body.name == "Jane"
  [PASS] body.email == "jane@example.com"
  [FAIL] body.role expected "admin", got "user"

Result: 3/4 assertions passed
```

## Examples

### Example 1: Test a CRUD flow

**User request:** "Test the users API -- create, read, update, delete"

**Output:**
```
API Test Suite: Users CRUD
==========================

1. POST /api/users
   Status: 201 Created -- PASS
   Time:   156ms
   Body:   {"id": 42, "name": "Test User", "email": "test@example.com"}

2. GET /api/users/42
   Status: 200 OK -- PASS
   Time:   38ms
   Body:   {"id": 42, "name": "Test User", "email": "test@example.com"}

3. PUT /api/users/42
   Status: 200 OK -- PASS
   Time:   89ms
   Body:   {"id": 42, "name": "Updated Name", "email": "test@example.com"}

4. DELETE /api/users/42
   Status: 204 No Content -- PASS
   Time:   45ms

5. GET /api/users/42 (verify deletion)
   Status: 404 Not Found -- PASS
   Time:   22ms

Result: 5/5 PASSED
```

### Example 2: Debug a failing request

**User request:** "I'm getting a 401 on POST /api/orders, can you figure out why?"

**Output:**
```
Debugging POST /api/orders
===========================

Test 1: No auth header
  Status: 401 -- Missing Authorization header (expected)

Test 2: With Bearer token
  Status: 401 -- Response: {"error": "Token expired"}
  Note: Token exp claim is 2024-01-15T00:00:00Z (expired)

Test 3: With refreshed token
  Status: 201 Created -- PASS

Root cause: Your Bearer token has expired.
Fix: Refresh the token using POST /api/auth/refresh
```

## Guidelines

- Never send requests to production APIs unless the user explicitly confirms. Ask first.
- Mask sensitive values (tokens, passwords, API keys) in output. Show only the last 4 characters.
- For sequences of dependent requests (create then read), use the response from the first request to build the second.
- Include response time in reports. Flag responses over 2 seconds as slow.
- When testing auth flows, test both the happy path and common failure modes (expired token, wrong credentials, missing permissions).
- For GraphQL, use POST with the query in the JSON body and validate the `data` field separately from `errors`.
- If an endpoint returns pagination, test the first page and mention the total count.
- Always set a timeout (30 seconds) to avoid hanging on unresponsive endpoints.
