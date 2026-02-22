---
name: typescript
description: TypeScript-specific coding conventions and type system patterns. Always load this skill when writing or reviewing TypeScript code.
---

# TypeScript

TypeScript-specific guidelines for type safety and code organization.

## Quick Reference

### Do

- Use `import type` for type-only imports
- Use `{ cause }` when re-throwing errors
- Let TypeScript infer types when obvious
- Create factory functions with `create*` prefix
- Prefer factory functions over classes
- Return `null` from handlers when request doesn't match
- Use a logger instead of `console.log`

### Don't

- Use default exports
- Use `any` type (use `unknown` and narrow)
- Use type assertions (`as Type`) - they indicate interface problems
- Over-type code with explicit annotations the compiler can infer
- Include file extensions in imports (unless required by runtime)

## Naming Conventions

### Files

| Type                | Convention                        | Example                         |
| ------------------- | --------------------------------- | ------------------------------- |
| Regular modules     | Lowercase, hyphens for multi-word | `token-payment.ts`, `server.ts` |
| Single-word modules | Lowercase                         | `cache.ts`, `common.ts`         |
| Test files          | `{name}.test.ts`                  | `cache.test.ts`                 |

### Types and Interfaces

| Pattern           | Use Case                 | Example                           |
| ----------------- | ------------------------ | --------------------------------- |
| `PascalCase`      | Interfaces, type aliases | `PaymentHandler`, `RequestConfig` |
| `*Args` / `*Opts` | Function arguments       | `CreateHandlerOpts`               |
| `*Response`       | API responses            | `SettleResponse`                  |
| `*Info`           | Data structures          | `ChainInfo`, `TokenInfo`          |
| `*Handler`        | Handler interfaces       | `PaymentHandler`                  |

### Functions

| Pattern     | Use Case                       | Example                             |
| ----------- | ------------------------------ | ----------------------------------- |
| `camelCase` | All functions                  | `handleRequest`                     |
| `create*`   | Factory functions              | `createHandler`, `createClient`     |
| `is*`       | Boolean predicates             | `isValidationError`, `isKnownType`  |
| `get*`      | Retrieval without side effects | `getBalance`, `getConfig`           |
| `lookup*`   | Search/lookup operations       | `lookupToken`, `lookupNetwork`      |
| `generate*` | Builder/generator functions    | `generateMatcher`, `generateConfig` |
| `handle*`   | Event/request handlers         | `handleSettle`, `handleVerify`      |

### Variables

| Pattern                | Use Case                    | Example                          |
| ---------------------- | --------------------------- | -------------------------------- |
| `camelCase`            | Regular variables           | `paymentResponse`, `blockNumber` |
| `SCREAMING_SNAKE_CASE` | Constants, environment vars | `API_BASE_URL`, `MAX_RETRIES`    |
| `_` prefix             | Unused parameters           | `_ctx`, `_unused`                |

### Acronyms in Names

Preserve acronym capitalization based on position:

```
// Good - acronyms stay capitalized when starting uppercase
getURLFromRequest
requestURL
parseHTTPHeaders

// Good - lowercase-starting acronyms stay lowercase
url
json

// Bad - don't mix case within acronyms
getUrlFromRequest  // Should be getURLFromRequest
requestUrl         // Should be requestURL
```

Common acronyms: URL, HTTP, HTTPS, JSON, API, RPC, HTML, XML

Note: "ID" is an abbreviation, so use standard camelCase: `userId`, `requestId`, `getId()`.

## Type System Patterns

### Runtime Validation

Use a validation library (e.g., arktype, zod) for runtime type validation. Define the validator and TypeScript type together:

```typescript
import { type } from "arktype";

// Define runtime validator
export const PaymentRequest = type({
  scheme: "string",
  network: "string",
  amount: "string.numeric",
  resource: "string.url",
});

// Derive TypeScript type from validator
export type PaymentRequest = typeof PaymentRequest.infer;
```

### Type Guards

Create type guards using validation functions:

```typescript
export function isAddress(maybe: unknown): maybe is Address {
  return !isValidationError(Address(maybe));
}

export function isKnownNetwork(n: string): n is KnownNetwork {
  return knownNetworks.includes(n as KnownNetwork);
}
```

### Interfaces vs Types

- **`type`**: Use for data structures, unions, and validator-derived types
- **`interface`**: Use for behavioral contracts (objects with methods)

```typescript
// Type for data structure
export type RequestContext = {
  request: RequestInfo | URL;
};

// Interface for behavioral contract
export interface PaymentHandler {
  getSupported?: () => Promise<SupportedKind>[];
  handleSettle: (requirements, payment) => Promise<SettleResponse | null>;
}
```

### Const Assertions for Exhaustive Types

Use `as const` for exhaustive literal types:

```typescript
const PaymentMode = {
  Direct: "direct",
  Deferred: "deferred",
} as const;

type PaymentMode = (typeof PaymentMode)[keyof typeof PaymentMode];

// TypeScript ensures all cases handled in switch
switch (mode) {
  case PaymentMode.Direct:
    // ...
    break;
  case PaymentMode.Deferred:
    // ...
    break;
}
```

### Type-Only Imports

Use `import type` for type-only imports:

```typescript
import type { PaymentRequest } from "./types";
import type { Hex, Account } from "viem";

// Mixed imports
import {
  type Transaction,
  createTransaction, // value import
} from "./transactions";
```

### Avoid Over-Typing

Let TypeScript infer types when obvious:

```typescript
// Good - return type is obvious
const createHandler = async (network: string) => {
  const config = { network, enabled: true };
  return {
    getConfig: () => config,
    isEnabled: () => config.enabled,
  };
};

// Unnecessary - the return type is obvious
const createHandler = async (network: string): Promise<{
  getConfig: () => { network: string; enabled: boolean };
  isEnabled: () => boolean;
}> => { ... };
```

**When to add explicit types:**

- Public API boundaries where the type serves as documentation
- When the inferred type would be too wide
- When TypeScript cannot infer the type correctly
- Complex return types that benefit from explicit documentation

**When NOT to add explicit types:**

- Variable assignments with obvious literal values
- Return types that match a simple expression
- Loop variables and intermediate calculations
- Arrow function parameters in callbacks where context provides types

### Avoiding `any` and Type Assertions

Use `unknown` instead of `any` when the type is truly unknown, then narrow with validation:

```typescript
// Bad
function processData(data: any) {
  return data.value;
}

// Good
function processData(data: unknown) {
  const validated = MyDataType(data);
  if (isValidationError(validated)) {
    throw new Error(`Invalid data: ${validated.summary}`);
  }
  return validated.value;
}
```

Type assertions (`as Type`) bypass type checking. They often indicate interface problems. Prefer runtime validation:

```typescript
// Bad
const data = (await response.json()) as UserData;

// Good
const raw = await response.json();
const data = UserData(raw);
if (isValidationError(data)) {
  throw new Error(`Invalid response: ${data.summary}`);
}
```

### Generic Constraints vs Index Signatures

Prefer generic type parameters with constraints over index signatures:

```typescript
// Bad - index signature (too permissive)
export interface LoggingBackend {
  configureApp(args: {
    level: LogLevel;
    [key: string]: unknown;
  }): Promise<void>;
}

// Good - generic with constraint (type-safe)
export type BaseConfigArgs = { level: LogLevel };

export interface LoggingBackend<TConfig extends BaseConfigArgs = BaseConfigArgs> {
  configureApp(args: TConfig): Promise<void>;
}
```

## Import/Export Patterns

### Barrel Exports

Use `index.ts` files to re-export from modules:

```typescript
// packages/types/src/index.ts

// Namespaced exports for grouped functionality
export * as payments from "./payments";
export * as client from "./client";

// Flat exports for utilities
export * from "./validation";
export * from "./helpers";
```

### Named Exports (Preferred)

```typescript
// Good
export function createMiddleware(args: CreateMiddlewareArgs) { ... }
export const MAX_RETRIES = 3;

// Avoid
export default function createMiddleware(args: CreateMiddlewareArgs) { ... }
```

### Import Ordering

Order imports by category:

1. External library imports
2. Internal package imports
3. Relative imports

```typescript
// External libraries
import { type } from "arktype";
import { Hono } from "hono";

// Internal packages
import { isValidationError } from "@myorg/types";
import type { Handler } from "@myorg/types/handler";

// Relative imports
import { isValidTransaction } from "./verify";
import { logger } from "./logger";
```

### Import Paths

Omit file extensions in import paths when the module resolver can infer them:

```typescript
// Good - no extension needed
import { createHandler } from "./handler";
import type { Config } from "../types";

// Bad - unnecessary extension
import { createHandler } from "./handler.ts";
import type { Config } from "../types.ts";
```

Note: Some environments (like Deno or Node.js with `"type": "module"`) require explicit extensions. Follow project conventions when extensions are mandated by the runtime.

## Async Patterns

### Factory Functions

Use async factory functions that return objects with async methods:

```typescript
const createHandler = async (network: string, rpc: RpcClient, config?: HandlerOptions) => {
  // Async initialization
  const networkInfo = await fetchNetworkInfo(rpc);

  // Return object with async methods
  return {
    getSupported,
    handleVerify,
    handleSettle,
  };
};
```

### Parallel Execution

Use `Promise.all` for independent parallel operations:

```typescript
const [tokenName, tokenVersion] = await Promise.all([
  client.readContract({ functionName: "name" }),
  client.readContract({ functionName: "version" }),
]);
```

### Timeouts

Use `Promise.race` for operations that need timeouts:

```typescript
function timeout(timeoutMs: number, msg?: string) {
  return new Promise((_, reject) =>
    setTimeout(() => reject(new Error(msg ?? "timed out")), timeoutMs),
  );
}

const result = await Promise.race([
  fetchData(),
  timeout(5000, "fetch timed out"),
]);
```

### Retry Logic

Implement retries with exponential backoff:

```typescript
let attempt = (options.retryCount ?? 2) + 1;
let backoff = options.initialRetryDelay ?? 100;
let response;

do {
  response = await makeRequest();

  if (response.ok) {
    return response;
  }

  await new Promise((resolve) => setTimeout(resolve, backoff));
  backoff *= 2;
} while (--attempt > 0);
```

## Error Handling

### Validation Errors

Check validation errors before proceeding:

```typescript
const payload = parsePayload(input);

if (isValidationError(payload)) {
  logger.debug(`couldn't validate payload: ${payload.summary}`);
  return sendBadRequest();
}

// payload is now typed correctly
```

### Local Error Response Factories

Create local helpers for consistent error responses:

```typescript
const handleSettle = async (requirements, payment) => {
  const errorResponse = (msg: string): SettleResponse => {
    logger.error(msg);
    return {
      success: false,
      error: msg,
      txHash: null,
    };
  };

  if (someConditionFails) {
    return errorResponse("Invalid transaction");
  }
  // ...
};
```

### Error Chaining

Use `{ cause }` when re-throwing errors:

```typescript
try {
  transaction = parseTransaction(input);
} catch (cause) {
  throw new Error("Failed to parse transaction", { cause });
}
```

### Return `null` for "Not My Responsibility"

Handlers should return `null` when a request doesn't match their criteria:

```typescript
const handleVerify = async (requirements, payment) => {
  if (!isMatchingRequirement(requirements)) {
    return null; // Let another handler try
  }
  // Handle the request...
};
```

## Testing

### Philosophy

Focus test coverage on logic specific to your codebase:

- Business logic and domain-specific validation
- Integration points between components
- Error handling paths and edge cases
- Custom algorithms and data transformations

Do not write tests that merely verify functionality provided by external libraries. Trust well-maintained libraries to do their job.

### Test Structure

```typescript
import t from "tap";

await t.test("descriptiveTestName", async (t) => {
  // Setup
  const cache = new Cache({ capacity: 3 });

  // Assertions
  t.equal(cache.size, 0);
  t.matchOnly(cache.get("key"), undefined);

  t.end();
});
```

### Time-Based Testing

Inject time functions for deterministic time-based tests:

```typescript
let theTime = 0;
const now = () => theTime;

const cache = new Cache({
  maxAge: 1000,
  now, // Inject time function
});

theTime += 500;
t.matchOnly(cache.get("key"), 42); // Still valid

theTime += 1000;
t.matchOnly(cache.get("key"), undefined); // Expired
```

## Documentation

### TSDoc Comments

Document public APIs with TSDoc:

```typescript
/**
 * Creates a handler for the payment scheme.
 *
 * @param network - The network identifier (e.g., "mainnet", "testnet")
 * @param rpc - RPC client
 * @param config - Optional configuration options
 * @returns Promise resolving to a Handler
 */
export const createHandler = async (
  network: string,
  rpc: RpcClient,
  config?: HandlerOptions,
): Promise<Handler> => { ... };
```
