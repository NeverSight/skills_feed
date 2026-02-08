---
name: vitest
description: Writes and runs tests, configures test environments, mocks dependencies, and generates coverage reports. Use when setting up vitest.config.ts, writing test suites, mocking modules, or measuring code coverage.
---

# Vitest

Fast unit testing framework powered by Vite.

## Quick Start

### Setup

```json
{
  "scripts": {
    "test": "bun vitest run",
    "test:watch": "bun vitest",
    "coverage": "bun vitest run --coverage"
  }
}
```

### Config

```typescript
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "node", // 'jsdom', 'happy-dom'
    globals: true, // use global test functions
    setupFiles: ["./setup.ts"],
    include: ["**/*.test.ts", "**/*.spec.ts"],
    coverage: {
      reporter: ["text", "json", "html"],
      exclude: ["node_modules", "test"],
    },
  },
});
```

## Running Tests

```bash
# Run all tests
bun vitest run

# Watch mode (development)
bun vitest

# Run specific test file
bun vitest run src/utils.test.ts

# Run tests matching pattern
bun vitest run -t "should validate"

# With coverage
bun vitest run --coverage

# Verbose output
bun vitest run --reporter=verbose

# Run tests related to changed files
bun vitest related src/file.ts

# Run benchmarks
bun vitest bench

# Run type checking
bun vitest typecheck

# Stop on first failure
bun vitest run -x
```

## Test Pyramid & Best Practices

```
        /\
       /  \     E2E Tests (few)
      /----\    - Critical user journeys
     /      \   - Slow, expensive
    /--------\
   /          \ Integration Tests (some)
  /------------\- Component interactions
 /              \- Database, APIs
/----------------\
   Unit Tests (many)
   - Fast, isolated
   - Business logic
```

### What to Test

```
✅ TEST                              ❌ SKIP
─────────────────────────────────────────────────────
Business logic                       Framework code
Edge cases and boundaries            Trivial getters/setters
Error handling paths               Third-party libraries
Public API contracts               Private implementation details
Integration points                 UI layout (use visual tests)
Security-sensitive code           Configuration files
```

### Test Quality Checklist

- [ ] Tests are independent and isolated
- [ ] Tests are deterministic (no flakiness)
- [ ] Test names describe behavior being tested
- [ ] Each test has a single reason to fail
- [ ] Tests run fast (< 100ms for unit tests)
- [ ] Tests use meaningful assertions
- [ ] Setup/teardown is minimal and clear

### BDD Best Practices

```
✅ DO                                ❌ DON't
─────────────────────────────────────────────────────
Write from user's perspective        Use technical jargon
One behavior per scenario            Test multiple things
Use declarative style                Include implementation details
Keep scenarios independent           Share state between scenarios
Use meaningful data                  Use "test", "foo", "bar"
Focus on business outcomes           Focus on UI interactions
```

## BDD Test Structure

Write tests using Given-When-Then style with nested `describe` blocks:

```typescript
import { describe, it, expect, beforeEach } from "vitest";

describe("Calculator", () => {
  describe("given two positive numbers", () => {
    const a = 5;
    const b = 3;

    describe("when adding them", () => {
      it("then the result should be their sum", () => {
        expect(a + b).toBe(8);
      });
    });

    describe("when subtracting them", () => {
      it("then the result should be the difference", () => {
        expect(a - b).toBe(2);
      });
    });

    describe("when dividing them", () => {
      it("then the result should be the quotient", () => {
        expect(a / b).toBe(1.67);
      });
    });
  });

  describe("given a negative number and zero", () => {
    describe("when dividing", () => {
      it("then it should throw an error", () => {
        expect(() => a / 0).toThrow();
      });
    });
  });
});
```

## Mocking Dependencies

- [Module Mocking](./references/mocking-modules.md) - Mock external dependencies with `vi.mock()`
- [Filesystem Mocking](./references/filesystem-mocking.md) - In-memory filesystem with memfs
- [Request Mocking](./references/requests-mocking.md) - Mock HTTP requests

## Related Skills

- **typescript**: Type safety for tests
- **bun**: Package management and scripting
- **ast-grep**: Pattern matching for refactoring
