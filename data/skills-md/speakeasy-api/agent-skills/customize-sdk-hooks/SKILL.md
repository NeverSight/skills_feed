---
name: customize-sdk-hooks
description: |
  Guide for implementing SDK lifecycle hooks to customize request/response behavior.
  Covers hook types, registration patterns, and practical examples for adding
  custom headers, telemetry, security signatures, and error handling.

  Trigger phrases: "SDK hooks", "add hooks", "BeforeRequestHook", "custom user-agent",
  "telemetry hook", "SDK middleware", "intercept requests", "custom security hook",
  "HMAC authentication"
license: Apache-2.0
---

# Customize SDK Hooks

## When to Use

Use this skill when you need to:

- Add custom headers (User-Agent, correlation IDs) to every SDK request
- Implement telemetry, logging, or observability at the SDK level
- Add custom authentication logic (HMAC signatures, token refresh, API key injection)
- Transform responses or errors before they reach the caller
- Configure SDK defaults at initialization time
- Implement retry logic or custom error handling

## Inputs

- **Hook type**: Which lifecycle event to intercept (init, before request, after success, after error)
- **SDK language**: The target language of the generated SDK (TypeScript, Go, Python, Java, C#, Ruby, PHP, etc.)
- **Custom logic**: The behavior to inject at the hook point

## Outputs

- Hook implementation file(s) in `src/hooks/` (or language equivalent)
- Updated `src/hooks/registration.ts` to register the new hook
- The hook is preserved across SDK regenerations

## Prerequisites

- A Speakeasy-generated SDK (any supported language)
- Understanding of the SDK's request/response lifecycle
- The `src/hooks/` directory exists in the generated SDK (created by default)

## Hook Types

| Hook | When Called | Common Use Cases |
|------|-----------|-----------------|
| `SDKInitHook` | SDK client initialization | Configure defaults, validate config, set base URL |
| `BeforeCreateRequestHook` | Before the HTTP request object is created | Modify input parameters, inject defaults |
| `BeforeRequestHook` | Before the HTTP request is sent | Add headers, logging, telemetry, sign requests |
| `AfterSuccessHook` | After a successful HTTP response | Transform response, emit warnings, log metrics |
| `AfterErrorHook` | After an HTTP error response | Error transformation, retry logic, error logging |

### Hook Interfaces (TypeScript)

```typescript
// SDKInitHook
interface SDKInitHook {
  sdkInit(opts: SDKInitOptions): SDKInitOptions;
}

// BeforeCreateRequestHook
interface BeforeCreateRequestHook {
  beforeCreateRequest(hookCtx: BeforeCreateRequestHookContext, input: any): any;
}

// BeforeRequestHook
interface BeforeRequestHook {
  beforeRequest(
    hookCtx: BeforeRequestHookContext,
    request: Request
  ): Request;
}

// AfterSuccessHook
interface AfterSuccessHook {
  afterSuccess(
    hookCtx: AfterSuccessHookContext,
    response: Response
  ): Response;
}

// AfterErrorHook
interface AfterErrorHook {
  afterError(
    hookCtx: AfterErrorHookContext,
    response: Response | null,
    error: unknown
  ): { response: Response | null; error: unknown };
}
```

## Directory Structure

```
src/
  hooks/
    types.ts          # Generated - DO NOT EDIT (hook interfaces/types)
    registration.ts   # Custom - YOUR registrations (preserved on regen)
    custom_useragent.ts   # Custom - your hook implementations
    telemetry.ts          # Custom - your hook implementations
```

**Key rule**: `registration.ts` and any custom hook files you create are preserved
during SDK regeneration. The `types.ts` file is regenerated and should not be modified.

## Registration Pattern

All hooks are registered in `src/hooks/registration.ts`. This file is created once
by the generator and never overwritten. You add your hooks here:

```typescript
// src/hooks/registration.ts
import { Hooks } from "./types.js";
import { CustomUserAgentHook } from "./custom_useragent.js";
import { TelemetryHook } from "./telemetry.js";

/*
 * This file is only ever generated once on the first generation and then is free
 * to be modified. Any hooks you wish to add should be registered in the
 * initHooks function. Feel free to define them in this file or in separate files
 * in the hooks folder.
 */

export function initHooks(hooks: Hooks) {
  hooks.registerBeforeRequestHook(new CustomUserAgentHook());
  hooks.registerAfterSuccessHook(new TelemetryHook());
}
```

## Command

To add a hook to a Speakeasy-generated SDK:

1. Create your hook implementation file in `src/hooks/`
2. Implement the appropriate interface from `src/hooks/types.ts`
3. Register it in `src/hooks/registration.ts`
4. Regenerate the SDK -- your hooks are preserved

```bash
# After adding hooks, regenerate safely
speakeasy generate sdk -s openapi.yaml -o . -l typescript
# Your registration.ts and custom hook files are untouched
```

## Examples

### Example 1: Custom User-Agent Hook

Add a custom `User-Agent` header to every outgoing request.

```typescript
// src/hooks/custom_useragent.ts
import {
  BeforeRequestHook,
  BeforeRequestHookContext,
} from "./types.js";

export class CustomUserAgentHook implements BeforeRequestHook {
  private userAgent: string;

  constructor(appName: string, appVersion: string) {
    this.userAgent = `${appName}/${appVersion}`;
  }

  beforeRequest(
    hookCtx: BeforeRequestHookContext,
    request: Request
  ): Request {
    // Clone the request to add the custom header
    const newRequest = new Request(request, {
      headers: new Headers(request.headers),
    });
    newRequest.headers.set("User-Agent", this.userAgent);

    // Optionally append the existing User-Agent
    const existing = request.headers.get("User-Agent");
    if (existing) {
      newRequest.headers.set(
        "User-Agent",
        `${this.userAgent} ${existing}`
      );
    }

    return newRequest;
  }
}
```

Register it:

```typescript
// src/hooks/registration.ts
import { Hooks } from "./types.js";
import { CustomUserAgentHook } from "./custom_useragent.js";

export function initHooks(hooks: Hooks) {
  hooks.registerBeforeRequestHook(
    new CustomUserAgentHook("my-app", "1.0.0")
  );
}
```

### Example 2: Custom Security Hook (HMAC Signing)

For APIs requiring HMAC signatures or custom authentication that cannot be
expressed in the OpenAPI spec, combine an overlay with a `BeforeRequestHook`.

**Step 1**: Use an overlay to mark the security scheme so Speakeasy generates
the hook point:

```yaml
# overlay.yaml
overlay: 1.0.0
info:
  title: Add HMAC security
actions:
  - target: "$.components.securitySchemes"
    update:
      hmac_auth:
        type: http
        scheme: custom
        x-speakeasy-custom-security: true
```

**Step 2**: Implement the signing hook:

```typescript
// src/hooks/hmac_signing.ts
import {
  BeforeRequestHook,
  BeforeRequestHookContext,
} from "./types.js";
import { createHmac } from "crypto";

export class HmacSigningHook implements BeforeRequestHook {
  beforeRequest(
    hookCtx: BeforeRequestHookContext,
    request: Request
  ): Request {
    const timestamp = Date.now().toString();
    const secret = hookCtx.securitySource?.apiSecret;
    if (!secret) {
      throw new Error("API secret is required for HMAC signing");
    }

    const signature = createHmac("sha256", secret)
      .update(`${request.method}:${request.url}:${timestamp}`)
      .digest("hex");

    const newRequest = new Request(request, {
      headers: new Headers(request.headers),
    });
    newRequest.headers.set("X-Timestamp", timestamp);
    newRequest.headers.set("X-Signature", signature);

    return newRequest;
  }
}
```

Register it:

```typescript
// src/hooks/registration.ts
import { Hooks } from "./types.js";
import { HmacSigningHook } from "./hmac_signing.js";

export function initHooks(hooks: Hooks) {
  hooks.registerBeforeRequestHook(new HmacSigningHook());
}
```

## Best Practices

1. **Keep hooks focused**: Each hook should address a single concern. Use separate
   hooks for user-agent, telemetry, and auth rather than one monolithic hook.

2. **Clone responses before reading the body**: The `Response.body` stream can only
   be consumed once. Always clone before reading:

   ```typescript
   afterSuccess(hookCtx: AfterSuccessHookContext, response: Response): Response {
     // CORRECT: clone before reading
     const cloned = response.clone();
     cloned.json().then((data) => console.log("Response:", data));
     return response; // return the original, unconsumed
   }
   ```

3. **Fire-and-forget for telemetry**: Do not block the request pipeline for
   non-critical operations like logging or metrics:

   ```typescript
   beforeRequest(hookCtx: BeforeRequestHookContext, request: Request): Request {
     // Fire-and-forget: do not await
     void fetch("https://telemetry.example.com/events", {
       method: "POST",
       body: JSON.stringify({ operation: hookCtx.operationID }),
     });
     return request;
   }
   ```

4. **Test hooks independently**: Write unit tests for hooks in isolation by
   constructing mock `Request`/`Response` objects and hook contexts.

5. **Use `hookCtx.operationID`**: The hook context provides the current operation
   ID, which is useful for per-operation behavior, logging, and metrics.

## What NOT to Do

- **Do NOT edit `types.ts`**: This file is regenerated. Your changes will be lost.
- **Do NOT consume the response body without cloning**: This causes downstream
  failures because the body stream is exhausted.
- **Do NOT perform blocking I/O in hooks**: Long-running operations (network calls,
  file I/O) in hooks will degrade SDK performance. Use fire-and-forget patterns
  for non-critical work.
- **Do NOT throw errors in `AfterSuccessHook`** unless you intend to convert a
  success into a failure. Throwing in hooks disrupts the normal flow.
- **Do NOT store mutable shared state in hooks** without synchronization. Hooks may
  be called concurrently in multi-threaded environments.
- **Do NOT duplicate logic that belongs in an OpenAPI overlay**. If you need to
  modify the API spec (add security schemes, change parameters), use an overlay
  instead of a hook.

## Troubleshooting

### Hook is not being called

- Verify the hook is registered in `src/hooks/registration.ts`
- Confirm you are registering for the correct hook type (e.g., `registerBeforeRequestHook`
  vs `registerAfterSuccessHook`)
- Check that `initHooks` is exported and follows the expected signature

### Response body is empty or already consumed

- You are reading `response.body` or calling `response.json()` without cloning first
- Always use `response.clone()` before consuming the body, then return the original

### Hooks lost after regeneration

- Custom hook files in `src/hooks/` are preserved, but only if they are separate files
- `registration.ts` is never overwritten after initial generation
- `types.ts` IS overwritten -- never put custom code there

### TypeScript compilation errors after regeneration

- `types.ts` may have updated interfaces. Check for breaking changes in hook signatures
- Update your hook implementations to match the new interface definitions

### Hook causes request failures

- Ensure you are returning a valid `Request` or `Response` object
- Check that cloned requests preserve the original body and headers
- Verify any injected headers have valid values (no undefined or null)

## Other Languages

While the examples above are in TypeScript, Speakeasy SDK hooks are available
across all supported languages:

- **Go**: Hooks implement interfaces in `hooks/hooks.go` with registration in
  `hooks/registration.go`
- **Python**: Hooks are classes in `src/hooks/` implementing protocols from
  `src/hooks/types.py`
- **Java**: Hooks implement interfaces from `hooks/SDKHooks.java`
- **C#**: Hooks implement interfaces from `Hooks/SDKHooks.cs`
- **Ruby**: Hooks use Sorbet-typed classes with Faraday middleware patterns
- **PHP**: Hooks use PSR-7 request/response interfaces with Guzzle middleware

The hook types, lifecycle, and registration pattern are consistent across all
languages. Refer to the generated `types` file in your SDK for language-specific
interface definitions.
