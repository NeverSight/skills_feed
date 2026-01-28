---
name: vitest-testing
description: Guide for writing unit tests with Vitest for Fastify plugins and routes. Use when creating or modifying tests in app/tests/.
---

# Vitest Testing Patterns

This skill provides patterns for writing unit tests with Vitest in this repository.

## Test Structure

- **Unit tests**: `app/tests/unit/**` (mirror `app/src/**` structure)
- **Integration tests**: `app/tests/integration/**`
- **Mocks**: `app/tests/mocks/**`
- **Helpers**: `app/tests/helpers/**`

## Plugin Test Template

```typescript
import Fastify from "fastify";
import { afterEach, describe, expect, it } from "vitest";
import pluginName from "../../../src/plugins/plugin-name.js";

describe("Plugin Name", () => {
  let fastify: ReturnType<typeof Fastify>;

  afterEach(async () => {
    if (fastify) await fastify.close();
  });

  it("should register plugin successfully", async () => {
    fastify = Fastify();
    await fastify.register(pluginName);
    await fastify.ready();

    // Test expectations
    expect(fastify.hasDecorator("decoratorName")).toBe(true);
  });
});
```

## Route Test Template

```typescript
import Fastify from "fastify";
import { afterEach, describe, expect, it } from "vitest";
import routeName from "../../../src/routes/route-name.js";

describe("GET /endpoint", () => {
  let fastify: ReturnType<typeof Fastify>;

  afterEach(async () => {
    if (fastify) await fastify.close();
  });

  it("should return expected response", async () => {
    fastify = Fastify();
    await fastify.register(routeName);

    const response = await fastify.inject({
      method: "GET",
      url: "/endpoint",
    });

    expect(response.statusCode).toBe(200);
    expect(response.json()).toEqual({ status: "healthy" });
  });

  it("should return 400 for invalid input", async () => {
    fastify = Fastify();
    await fastify.register(routeName);

    const response = await fastify.inject({
      method: "POST",
      url: "/endpoint",
      payload: { invalid: "data" },
    });

    expect(response.statusCode).toBe(400);
  });
});
```

## Key Patterns

### Fastify Instance

- Use `Fastify()` to create test instances
- Always call `await fastify.ready()` after registering plugins
- Always call `await fastify.close()` after tests (use afterEach hook)

### Request Simulation

Use `fastify.inject()` for HTTP request simulation:

```typescript
const response = await fastify.inject({
  method: "GET",
  url: "/endpoint",
  headers: { authorization: "Bearer token" },
  query: { param: "value" },
  payload: { data: "value" },
});
```

### Response Assertions

```typescript
expect(response.statusCode).toBe(200);
expect(response.headers["content-type"]).toContain("application/json");
expect(response.json()).toEqual({ expected: "data" });
```

### Testing Decorators

```typescript
it("should decorate fastify instance", async () => {
  const fastify = Fastify();
  await fastify.register(plugin);
  await fastify.ready();

  expect(fastify.hasDecorator("myDecorator")).toBe(true);
  expect(fastify.myDecorator).toBeDefined();

  await fastify.close();
});
```

## Coverage Requirements

- **Provider**: V8
- **Minimum thresholds**: 70% (lines, functions, branches, statements)
- **Target**: 90%+ overall, 100% for critical business logic
- **Scope**: Only `tests/unit/**` affects coverage metrics

## V8 Coverage Ignore

Use `/* v8 ignore next -- @preserve */` to exclude untestable code:

```typescript
// ignore single statement
/* v8 ignore next -- @preserve */
process.on("SIGTERM", () => gracefulShutdown());

// ignore block
/* v8 ignore start -- @preserve */
const handler = setupHandler();
process.on("SIGINT", handler);
/* v8 ignore stop -- @preserve */
```

The `-- @preserve` suffix prevents esbuild from stripping comments.

## Import Conventions

- Use `.js` extensions for relative imports
- Use `import type { ... } from "pkg"` for type-only imports
- Vitest globals are enabled but explicit imports are preferred for better IntelliSense, type checking, and refactoring support:
  ```typescript
  import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
  ```

## Commands

```bash
cd app
npm run test              # Run all tests
npm run test:watch        # Run tests in watch mode
npm run test:coverage     # Run tests with coverage report
```

## Boundaries

- No real network, filesystem, or database calls in unit tests
- Each source file should have a matching test file
- Do not skip tests without documenting the reason
- Do not add inline Vitest env comments
