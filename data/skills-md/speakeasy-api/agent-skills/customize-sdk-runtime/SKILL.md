---
name: customize-sdk-runtime
description: Use when configuring SDK runtime behavior such as retries, timeouts, pagination, server selection, custom code hooks, or error handling. Triggers on "SDK retries", "timeout configuration", "x-speakeasy-retries", "x-speakeasy-timeout", "pagination config", "x-speakeasy-pagination", "server selection", "custom HTTP client", "SDK runtime", "error handling", "custom code", "preserve code"
license: Apache-2.0
---

# customize-sdk-runtime

Configure runtime behavior for Speakeasy-generated SDKs including retries, timeouts, pagination, server selection, custom code preservation, and error handling.

## When to Use

- Configuring retry logic for SDK operations
- Setting global or per-operation timeouts
- Adding pagination support to list endpoints
- Selecting between multiple server environments
- Preserving custom code across SDK regeneration
- Customizing error handling and typed error responses
- User says: "SDK retries", "timeout configuration", "server selection", "pagination config", "custom code", "error handling"

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| OpenAPI spec | Yes | Path to the OpenAPI spec to configure |
| gen.yaml | Sometimes | Generation config for error handling customization |
| Target language | Helpful | TypeScript, Python, or Go (defaults vary) |

## Outputs

| Output | Description |
|--------|-------------|
| Updated OpenAPI spec | Spec with runtime extensions applied |
| SDK configuration | Runtime behavior configured in generated SDK |
| Custom code files | Hook files preserved across regeneration |

## Prerequisites

- Speakeasy CLI installed and authenticated
- An existing OpenAPI spec
- An existing SDK project (for runtime override examples)

## Command

Runtime configuration is primarily done through OpenAPI extensions, not CLI commands. After modifying the spec, regenerate:

```bash
speakeasy run --output console
```

---

## Retry Configuration

### Global Retries (OpenAPI Spec)

Add `x-speakeasy-retries` at the root of your OpenAPI document:

```yaml
openapi: 3.1.0
info:
  title: My API
  version: 1.0.0
x-speakeasy-retries:
  strategy: backoff
  backoff:
    initialInterval: 500        # milliseconds
    maxInterval: 60000           # milliseconds
    maxElapsedTime: 3600000      # milliseconds (1 hour)
    exponent: 1.5
  statusCodes:
    - 5XX
    - 408
    - 429
  retryConnectionErrors: true
```

### Per-Operation Retries

Override retries on a specific operation by adding `x-speakeasy-retries` at the operation level with the same schema as above.

### Retry Options Reference

| Option | Type | Description |
|--------|------|-------------|
| `strategy` | string | Must be `backoff` |
| `backoff.initialInterval` | integer | First retry delay in ms |
| `backoff.maxInterval` | integer | Maximum delay between retries in ms |
| `backoff.maxElapsedTime` | integer | Total time limit for all retries in ms |
| `backoff.exponent` | number | Backoff multiplier (e.g., 1.5, 2.0) |
| `statusCodes` | string[] | HTTP status codes to retry (supports `5XX` patterns) |
| `retryConnectionErrors` | boolean | Retry on connection failures |

### Runtime Override (TypeScript)

```typescript
const res = await sdk.payments.create(
  { amount: 1000 },
  {
    retries: {
      strategy: "backoff",
      backoff: {
        initialInterval: 1000,
        maxInterval: 30000,
        maxElapsedTime: 300000,
        exponent: 2.0,
      },
      retryConnectionErrors: true,
    },
  }
);
```

### Runtime Override (Python)

```python
from sdk.utils import BackoffStrategy, RetryConfig

res = sdk.payments.create(
    amount=1000,
    retries=RetryConfig("backoff",
        backoff=BackoffStrategy(1000, 30000, 300000, 2.0),
        retry_connection_errors=True),
)
```

### Runtime Override (Go)

```go
res, err := sdk.Payments.Create(ctx, req, operations.WithRetries(retry.Config{
    Strategy: "backoff",
    Backoff: &retry.BackoffStrategy{
        InitialInterval: 1000, MaxInterval: 30000,
        MaxElapsedTime: 300000, Exponent: 2.0,
    },
    RetryConnectionErrors: true,
}))
```

---

## Timeout Configuration

### Global Timeout (OpenAPI Spec)

Set a default timeout in milliseconds at the document root:

```yaml
x-speakeasy-timeout: 30000   # 30 seconds
```

### Per-Operation Timeout

Override timeout on specific operations:

```yaml
paths:
  /reports/generate:
    post:
      operationId: generateReport
      x-speakeasy-timeout: 120000   # 2 minutes for long-running ops
```

### Runtime Override

**TypeScript:**
```typescript
const sdk = new SDK({ timeoutMs: 30000 });                          // global
const res = await sdk.reports.generate({ type: "annual" }, { timeoutMs: 120000 }); // per-call
```

**Python:**
```python
sdk = SDK(timeout_ms=30000)                                          # global
res = sdk.reports.generate(type="annual", timeout_ms=120000)         # per-call
```

**Go:**
```go
sdk := SDK.New(SDK.WithTimeoutMs(30000))                             // global
res, err := sdk.Reports.Generate(ctx, req, operations.WithTimeoutMs(120000)) // per-call
```

---

## Pagination Configuration

Add `x-speakeasy-pagination` to list endpoints:

```yaml
paths:
  /users:
    get:
      operationId: listUsers
      x-speakeasy-pagination:
        type: offsetLimit
        inputs:
          - name: offset
            in: parameters
            type: offset
          - name: limit
            in: parameters
            type: limit
        outputs:
          results: $.data
```

### Pagination Types

| Type | Description | Use Case |
|------|-------------|----------|
| `offsetLimit` | Offset + limit parameters | Traditional pagination |
| `cursor` | Cursor-based navigation | Large datasets, real-time data |
| `url` | Next-page URL in response | HATEOAS-style APIs |

For `cursor` type, use `type: cursor` in inputs and add `nextCursor: $.meta.next_cursor` to outputs.

### SDK Usage (TypeScript)

```typescript
// Auto-iterate through all pages
for await (const user of await sdk.users.list({ limit: 50 })) {
  console.log(user.name);
}

// Or manually page with next()
let page = await sdk.users.list({ limit: 50 });
while (page) {
  for (const user of page.data) { console.log(user.name); }
  page = await page.next();
}
```

---

## Server Configuration

### Multiple Servers in Spec

```yaml
servers:
  - url: https://api.example.com
    description: Production
    x-speakeasy-server-id: production
  - url: https://sandbox.example.com
    description: Sandbox
    x-speakeasy-server-id: sandbox
```

### Runtime Server Selection

**TypeScript:**
```typescript
const sdk = new SDK({ server: "sandbox" });
// or custom URL:
const sdk = new SDK({ serverURL: "https://custom.example.com" });
```

**Python:** `sdk = SDK(server="sandbox")` or `sdk = SDK(server_url="...")`

**Go:** `sdk := SDK.New(SDK.WithServer("sandbox"))` or `SDK.WithServerURL("...")`

---

## Custom Code Preservation

Files in `src/hooks/` (TypeScript) or the equivalent hooks directory are preserved during SDK regeneration.

### Key Rules

- `registration.ts` is generated on the first run, then never overwritten
- Any new files you add to `src/hooks/` are preserved across regeneration
- Register custom hooks in `registration.ts` to integrate them with the SDK lifecycle

### Example: Custom Hook Registration

```typescript
// src/hooks/registration.ts
import { Hooks } from "./types";
import { initLoggingHook } from "./logging";
import { initCustomAuthHook } from "./custom-auth";

export function initHooks(hooks: Hooks) {
  initLoggingHook(hooks);
  initCustomAuthHook(hooks);
}
```

---

## Error Handling

### Custom Error Schemas (gen.yaml)

```yaml
generation:
  errors:
    statusCodes:
      - statusCode: "4XX"
        schema: "#/components/schemas/ClientError"
      - statusCode: "5XX"
        schema: "#/components/schemas/ServerError"
```

Define typed error responses in your OpenAPI spec by adding response schemas for specific status codes (e.g., 404, 422). The SDK generates typed error classes for each.

### SDK Error Handling (TypeScript)

```typescript
import { NotFoundError, ValidationError } from "./sdk/models/errors";

try {
  const user = await sdk.users.get({ id: "123" });
} catch (err) {
  if (err instanceof NotFoundError) {
    console.log("User not found:", err.message);
  } else if (err instanceof ValidationError) {
    console.log("Validation failed:", err.errors);
  } else {
    throw err;
  }
}
```

### Error Transform Hooks

Add custom error transformation via hooks:

```typescript
// src/hooks/error-transform.ts
export function initErrorTransformHook(hooks: Hooks) {
  hooks.registerAfterError((_hookCtx, response, error) => {
    if (error) { console.error("API error:", error.message); }
    return { response, error };
  });
}
```

---

## Example

**Scenario**: Configure retries, a 30-second global timeout, and sandbox server selection.

1. Add extensions to your OpenAPI spec:

```yaml
openapi: 3.1.0
info:
  title: Payments API
  version: 1.0.0
x-speakeasy-retries:
  strategy: backoff
  backoff:
    initialInterval: 500
    maxInterval: 60000
    maxElapsedTime: 300000
    exponent: 1.5
  statusCodes: [5XX, 429]
  retryConnectionErrors: true
x-speakeasy-timeout: 30000
servers:
  - url: https://api.payments.com
    x-speakeasy-server-id: production
  - url: https://sandbox.payments.com
    x-speakeasy-server-id: sandbox
```

2. Regenerate: `speakeasy run --output console`

3. Use with runtime overrides:

```typescript
const sdk = new SDK({ server: "sandbox", timeoutMs: 30000 });

const payment = await sdk.payments.create(
  { amount: 5000, currency: "usd" },
  {
    retries: {
      strategy: "backoff",
      backoff: { initialInterval: 2000, maxInterval: 30000,
                 maxElapsedTime: 120000, exponent: 2.0 },
    },
    timeoutMs: 60000,
  }
);
```

## What NOT to Do

- **Do NOT** set excessively long `maxElapsedTime` values that could hang requests indefinitely
- **Do NOT** retry on 4XX status codes (except 408 and 429) as they indicate client errors
- **Do NOT** modify generated files outside of `src/hooks/` as they will be overwritten on regeneration
- **Do NOT** set timeouts to 0 expecting "no timeout" -- omit the extension instead
- **Do NOT** hardcode server URLs in application code -- use `x-speakeasy-server-id` and select at runtime

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Retries not working | Extension at wrong level | Ensure `x-speakeasy-retries` is at document root or operation level |
| Timeout not applying | Value not in milliseconds | `x-speakeasy-timeout` expects milliseconds, not seconds |
| Pagination `next()` undefined | Missing extension | Add `x-speakeasy-pagination` to the list operation |
| Custom hooks lost on regen | Files outside hooks dir | Move custom code to `src/hooks/` directory |
| Server ID not recognized | Missing extension | Add `x-speakeasy-server-id` to each server entry |
| Typed errors not generated | Missing error schemas | Define error response schemas per status code in OpenAPI spec |
| Hook not executing | Not registered | Register your hook in `registration.ts` |
