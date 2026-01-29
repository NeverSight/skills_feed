---
name: setup-sdk-testing
description: Use when setting up SDK testing, configuring contract tests, writing Arazzo test workflows, or running integration tests. Triggers on "SDK testing", "test SDK", "contract testing", "Arazzo tests", "integration tests", "speakeasy test", "mock server", "test generation", "ResponseValidationError"
license: Apache-2.0
---

# setup-sdk-testing

Set up and run tests for Speakeasy-generated SDKs using contract testing, custom Arazzo workflows, or integration tests against live APIs.

## When to Use

- Setting up automated testing for a generated SDK
- Enabling contract test generation via `gen.yaml`
- Writing custom multi-step API workflow tests with Arazzo
- Configuring integration tests against a live API
- Debugging `ResponseValidationError` or test failures
- User says: "test SDK", "contract testing", "Arazzo tests", "speakeasy test", "mock server", "test generation"

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `gen.yaml` | Yes | Generation config; contract testing is enabled here |
| OpenAPI spec | Yes | The API spec the SDK is generated from |
| Target language | Yes | `typescript`, `python`, `go`, or `java` (contract test support) |
| `.speakeasy/tests.arazzo.yaml` | No | Custom Arazzo test definitions |
| Live API credentials | No | Required only for integration testing |

## Outputs

| Output | Location |
|--------|----------|
| Generated contract tests | `tests/` directory in SDK output |
| Mock server config | Auto-generated alongside contract tests |
| Arazzo test results | Terminal output from `speakeasy test` |
| CI workflow | `.github/workflows/` (if integration testing configured) |

## Prerequisites

- Speakeasy CLI installed and authenticated (`speakeasy auth login`)
- A working SDK generation setup (`gen.yaml` + OpenAPI spec)
- For integration tests: API credentials as environment variables

## Decision Framework

Pick the right testing approach based on what you need:

| Need | Approach | Effort |
|------|----------|--------|
| Verify SDK types and methods match the API contract | Contract testing | Low (auto-generated) |
| Test multi-step API workflows (create then verify) | Custom Arazzo tests | Medium |
| Validate against a live API with real data | Integration testing | High |
| Catch regressions on every SDK regeneration | Contract testing + CI | Low |
| Test authentication flows end-to-end | Integration testing | High |
| Verify chained operations with data dependencies | Custom Arazzo tests | Medium |

**Start with contract testing.** It is auto-generated and catches the most common issues. Add custom Arazzo tests for workflow coverage, and integration tests only when live API validation is required.

## Command

### Enable Contract Testing

Add to `gen.yaml`:

```yaml
generation:
  tests:
    generateTests: true
```

Then regenerate the SDK:

```bash
speakeasy run --output console
```

### Run Tests

```bash
# Run all Arazzo-defined tests (contract + custom)
speakeasy test

# Run tests for a specific target
speakeasy test --target my-typescript-sdk

# Run with verbose output for debugging
speakeasy test --verbose
```

### Run via CI

Contract tests run automatically in the Speakeasy GitHub Actions workflow when test generation is enabled. No additional CI configuration is needed for contract tests.

## Example

### 1. Contract Testing (Quick Start)

Enable test generation in `gen.yaml`:

```yaml
generation:
  tests:
    generateTests: true
```

Regenerate the SDK:

```bash
speakeasy run --output console
```

Run the generated tests:

```bash
speakeasy test
```

The CLI generates tests from your OpenAPI spec, creates a mock server that returns spec-compliant responses, and validates that the SDK correctly handles requests and responses.

### 2. Custom Arazzo Tests

Create or edit `.speakeasy/tests.arazzo.yaml`:

```yaml
arazzo: 1.0.0
info:
  title: Custom SDK Tests
  version: 1.0.0

sourceDescriptions:
  - name: my-api
    type: openapi
    url: ./openapi.yaml

workflows:
  - workflowId: create-and-verify-resource
    steps:
      - stepId: create-resource
        operationId: createResource
        requestBody:
          payload:
            name: "test-resource"
            type: "example"
        successCriteria:
          - condition: $statusCode == 201
        outputs:
          resourceId: $response.body#/id

      - stepId: get-resource
        operationId: getResource
        parameters:
          - name: id
            in: path
            value: $steps.create-resource.outputs.resourceId
        successCriteria:
          - condition: $statusCode == 200
          - condition: $response.body#/name == "test-resource"

  - workflowId: list-and-filter
    steps:
      - stepId: list-resources
        operationId: listResources
        parameters:
          - name: limit
            in: query
            value: 10
        successCriteria:
          - condition: $statusCode == 200
```

Run the custom tests:

```bash
speakeasy test
```

#### Using Environment Variables in Arazzo Tests

Reference environment variables for sensitive values:

```yaml
steps:
  - stepId: authenticated-request
    operationId: getProtectedResource
    parameters:
      - name: Authorization
        in: header
        value: Bearer $env.API_TOKEN
    successCriteria:
      - condition: $statusCode == 200
```

#### Disabling a Specific Test

Use an overlay to disable a generated test without deleting it:

```yaml
overlay: 1.0.0
info:
  title: Disable flaky test
actions:
  - target: $["workflows"][?(@.workflowId=="flaky-test")]
    update:
      x-speakeasy-test:
        disabled: true
```

### 3. Integration Testing

For live API testing, use the SDK factory pattern:

**TypeScript example:**

```typescript
import { SDK } from "./src";

function createTestClient(): SDK {
  return new SDK({
    apiKey: process.env.TEST_API_KEY,
    serverURL: process.env.TEST_API_URL ?? "https://api.example.com",
  });
}

describe("Integration Tests", () => {
  const client = createTestClient();

  it("should list resources", async () => {
    const result = await client.resources.list({ limit: 5 });
    expect(result.statusCode).toBe(200);
    expect(result.data).toBeDefined();
  });

  it("should create and delete resource", async () => {
    // Create
    const created = await client.resources.create({ name: "integration-test" });
    expect(created.statusCode).toBe(201);

    // Cleanup
    const deleted = await client.resources.delete({ id: created.data.id });
    expect(deleted.statusCode).toBe(204);
  });
});
```

**Python example:**

```python
import os
import pytest
from my_sdk import SDK

@pytest.fixture
def client():
    return SDK(
        api_key=os.environ["TEST_API_KEY"],
        server_url=os.environ.get("TEST_API_URL", "https://api.example.com"),
    )

def test_list_resources(client):
    result = client.resources.list(limit=5)
    assert result.status_code == 200
    assert result.data is not None

@pytest.mark.cleanup
def test_create_and_delete(client):
    created = client.resources.create(name="integration-test")
    assert created.status_code == 201
    try:
        fetched = client.resources.get(id=created.data.id)
        assert fetched.data.name == "integration-test"
    finally:
        client.resources.delete(id=created.data.id)
```

**GitHub Actions CI for integration tests:**

```yaml
name: Integration Tests
on:
  schedule:
    - cron: "0 6 * * 1-5"
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: speakeasy-api/sdk-generation-action@v15
        with:
          speakeasy_version: latest
      - run: speakeasy test
        env:
          SPEAKEASY_API_KEY: ${{ secrets.SPEAKEASY_API_KEY }}
      - name: Run integration tests
        run: npm test -- --grep "integration"
        env:
          TEST_API_KEY: ${{ secrets.TEST_API_KEY }}
          TEST_API_URL: ${{ secrets.TEST_API_URL }}
```

## What NOT to Do

- **Do NOT** skip contract testing and jump straight to integration tests -- contract tests are free and catch most issues
- **Do NOT** hardcode API keys or secrets in Arazzo test files -- use `$env.VARIABLE_NAME` syntax
- **Do NOT** modify auto-generated test files directly -- they are overwritten on regeneration; use custom Arazzo tests instead
- **Do NOT** disable failing contract tests without investigating -- a `ResponseValidationError` usually means the spec and API are out of sync
- **Do NOT** run integration tests with destructive operations in production -- always use a test/staging environment
- **Do NOT** assume all languages support contract testing -- currently supported: TypeScript, Python, Go, Java

## Troubleshooting

### `ResponseValidationError` in contract tests

The SDK response does not match the OpenAPI spec. Common causes:

1. **Spec is outdated**: Regenerate from the latest API spec
2. **Missing required fields**: Check your spec's `required` arrays match actual API responses
3. **Type mismatches**: Verify `type` and `format` fields in schema definitions

```bash
# Regenerate with latest spec and re-run tests
speakeasy run --output console && speakeasy test --verbose
```

### Tests pass locally but fail in CI

1. Check that all environment variables are set in CI secrets
2. Verify the CI runner has network access to mock server ports
3. Ensure the Speakeasy CLI version matches between local and CI

### `speakeasy test` command not found

Update the Speakeasy CLI:

```bash
speakeasy update
```

### Mock server fails to start

1. Check for port conflicts on the default mock server port
2. Ensure the OpenAPI spec is valid: `speakeasy lint openapi -s spec.yaml`
3. Verify `generateTests: true` is set in `gen.yaml` and the SDK has been regenerated

### Custom Arazzo test not running

1. Verify the file is at `.speakeasy/tests.arazzo.yaml`
2. Check that `operationId` values match those in your OpenAPI spec exactly
3. Validate YAML syntax -- indentation errors are the most common cause

### Integration tests intermittently fail

1. Add retry logic for network-dependent tests
2. Use unique resource names with timestamps to avoid collisions
3. Ensure cleanup runs even on test failure (use `finally` or `afterEach`)
