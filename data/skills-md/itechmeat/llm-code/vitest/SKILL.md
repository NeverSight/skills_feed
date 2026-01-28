---
name: vitest
description: "Vitest testing framework: Vite-powered tests, Jest-compatible API, mocking, snapshots, coverage, browser mode, and TypeScript support."
version: "4.0.18"
release_date: "2026-01-21"
---

# Vitest

Next generation testing framework powered by Vite.

## Quick Navigation

- [Test API](references/api.md) - test, describe, hooks
- [Expect API](references/expect.md) - matchers and assertions
- [Mocking](references/mocking.md) - vi.fn, vi.mock, fake timers
- [Configuration](references/config.md) - vitest.config.ts options
- [CLI](references/cli.md) - command line reference
- [Browser Mode](references/browser.md) - real browser testing

## When to Use

- Testing Vite-based applications (shared config)
- Need Jest-compatible API with native ESM support
- Component testing in real browser
- Fast watch mode with HMR
- TypeScript testing without extra config
- Parallel test execution

## Installation

```bash
npm install -D vitest
```

**Requirements:** Vite >=v6.0.0, Node >=v20.0.0

## Quick Start

```js
// sum.js
export function sum(a, b) {
  return a + b;
}
```

```js
// sum.test.js
import { expect, test } from "vitest";
import { sum } from "./sum.js";

test("adds 1 + 2 to equal 3", () => {
  expect(sum(1, 2)).toBe(3);
});
```

```json
// package.json
{
  "scripts": {
    "test": "vitest",
    "test:run": "vitest run",
    "coverage": "vitest run --coverage"
  }
}
```

## Configuration

```ts
// vitest.config.ts (recommended)
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true, // Enable global test APIs
    environment: "jsdom", // Browser-like environment
    include: ["**/*.{test,spec}.{js,ts,jsx,tsx}"],
    coverage: {
      provider: "v8",
      reporter: ["text", "html"],
    },
  },
});
```

Or extend Vite config:

```ts
// vite.config.ts
/// <reference types="vitest/config" />
import { defineConfig } from "vite";

export default defineConfig({
  test: {
    // test options
  },
});
```

## Test File Naming

By default, tests must contain `.test.` or `.spec.` in filename:

- `sum.test.js`
- `sum.spec.ts`
- `__tests__/sum.js`

## Key Commands

```bash
# Watch mode (default)
vitest

# Single run
vitest run

# With coverage
vitest run --coverage

# Filter by file/test name
vitest sum
vitest -t "should add"

# UI mode
vitest --ui

# Browser tests
vitest --browser.enabled
```

## Common Patterns

### Basic Test

```ts
import { describe, it, expect, beforeEach } from "vitest";

describe("Calculator", () => {
  let calc: Calculator;

  beforeEach(() => {
    calc = new Calculator();
  });

  it("adds numbers", () => {
    expect(calc.add(1, 2)).toBe(3);
  });

  it("throws on invalid input", () => {
    expect(() => calc.add("a", 1)).toThrow();
  });
});
```

### Mocking

```ts
import { vi, expect, test } from "vitest";
import { fetchUser } from "./api";

vi.mock("./api", () => ({
  fetchUser: vi.fn(),
}));

test("uses mocked API", async () => {
  vi.mocked(fetchUser).mockResolvedValue({ name: "John" });

  const user = await fetchUser(1);

  expect(fetchUser).toHaveBeenCalledWith(1);
  expect(user.name).toBe("John");
});
```

### Snapshot Testing

```ts
import { expect, test } from "vitest";

test("matches snapshot", () => {
  const result = generateConfig();
  expect(result).toMatchSnapshot();
});

// Inline snapshot (auto-updates)
test("inline snapshot", () => {
  expect({ foo: "bar" }).toMatchInlineSnapshot();
});
```

### Async Testing

```ts
import { expect, test } from "vitest";

test("async/await", async () => {
  const result = await fetchData();
  expect(result).toBeDefined();
});

test("resolves", async () => {
  await expect(Promise.resolve("ok")).resolves.toBe("ok");
});

test("rejects", async () => {
  await expect(Promise.reject(new Error())).rejects.toThrow();
});
```

### Fake Timers

```ts
import { vi, expect, test, beforeEach, afterEach } from "vitest";

beforeEach(() => {
  vi.useFakeTimers();
});

afterEach(() => {
  vi.useRealTimers();
});

test("advances time", () => {
  const callback = vi.fn();
  setTimeout(callback, 1000);

  vi.advanceTimersByTime(1000);

  expect(callback).toHaveBeenCalled();
});
```

## Jest Migration

Most Jest code works with minimal changes:

```diff
- import { jest } from '@jest/globals'
+ import { vi } from 'vitest'

- jest.fn()
+ vi.fn()

- jest.mock('./module')
+ vi.mock('./module')

- jest.useFakeTimers()
+ vi.useFakeTimers()
```

**Key differences:**

- Use `vi` instead of `jest`
- Globals not enabled by default (add `globals: true`)
- `vi.mock` is hoisted (use `vi.doMock` for non-hoisted)
- No `jest.requireActual` (use `vi.importActual`)

## Environment Selection

```ts
// vitest.config.ts
{
  test: {
    environment: 'jsdom', // or 'happy-dom', 'node', 'edge-runtime'
  }
}

// Per-file (docblock at top)
/** @vitest-environment jsdom */
```

## TypeScript

```json
// tsconfig.json
{
  "compilerOptions": {
    "types": ["vitest/globals"]
  }
}
```

## References

See `references/` directory for detailed documentation on:

- Test API and hooks
- All expect matchers
- Mocking functions and modules
- Configuration options
- CLI commands
- Browser mode testing

## Links

- [Documentation](https://vitest.dev/)
- [API Reference](https://vitest.dev/api/)
- [GitHub](https://github.com/vitest-dev/vitest)
- [VS Code Extension](https://marketplace.visualstudio.com/items?itemName=vitest.explorer)
