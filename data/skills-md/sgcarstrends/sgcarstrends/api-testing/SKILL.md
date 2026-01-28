---
name: api-testing
description: Write and run API tests with Vitest for endpoints, middleware, and integrations. Use when testing API functionality, request/response validation, error handling.
allowed-tools: Read, Edit, Write, Bash, Grep, Glob
---

# API Testing Skill

This skill helps you write comprehensive API tests using Vitest for the Hono-based API service.

## When to Use This Skill

- Testing API endpoints and routes
- Validating request/response payloads
- Testing middleware and error handling
- Integration testing with database
- Testing workflows and background jobs
- Authentication and authorization testing
- Rate limiting and caching tests

## Testing Framework

The project uses **Vitest** for API testing:
- Fast execution with native ESM support
- Compatible with Jest API
- TypeScript support out of the box
- V8 coverage reporting
- Watch mode for development

## Project Configuration

### Vitest Config

```typescript
// apps/api/vitest.config.ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    environment: "node",
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
      exclude: [
        "node_modules/",
        "__tests__/",
        "dist/",
        "*.config.ts",
      ],
    },
    setupFiles: ["__tests__/setup.ts"],
  },
});
```

### Test Setup

```typescript
// apps/api/__tests__/setup.ts
import { beforeAll, afterAll, beforeEach } from "vitest";
import { db } from "../src/config/database";

beforeAll(async () => {
  // Connect to test database
  console.log("Setting up test database...");
});

afterAll(async () => {
  // Clean up connections
  console.log("Cleaning up test database...");
});

beforeEach(async () => {
  // Clear test data before each test
  // await db.delete(testTable);
});
```

## Test Structure

### File Organization

```
apps/api/
├── __tests__/
│   ├── setup.ts                    # Test setup
│   ├── helpers.ts                  # Test utilities
│   ├── routes/
│   │   ├── cars.test.ts           # Cars endpoints
│   │   ├── coe.test.ts            # COE endpoints
│   │   └── health.test.ts         # Health check
│   ├── workflows/
│   │   ├── update-car-data.test.ts
│   │   └── social-media.test.ts
│   └── middleware/
│       ├── auth.test.ts           # Auth middleware
│       └── error.test.ts          # Error handling
```

## Testing Hono Endpoints

### Basic Endpoint Test

```typescript
// apps/api/__tests__/routes/health.test.ts
import { describe, it, expect } from "vitest";
import app from "../../src/index";

describe("Health Check", () => {
  it("should return 200 OK", async () => {
    const res = await app.request("/health");

    expect(res.status).toBe(200);
    expect(await res.json()).toEqual({ status: "ok" });
  });

  it("should include timestamp", async () => {
    const res = await app.request("/health");
    const data = await res.json();

    expect(data).toHaveProperty("timestamp");
    expect(typeof data.timestamp).toBe("string");
  });
});
```

### Testing GET Endpoints

```typescript
// apps/api/__tests__/routes/cars.test.ts
import { describe, it, expect, beforeEach } from "vitest";
import app from "../../src/index";
import { db } from "../../src/config/database";
import { cars } from "@sgcarstrends/database/schema";

describe("GET /api/v1/cars/makes", () => {
  beforeEach(async () => {
    // Seed test data
    await db.insert(cars).values([
      { make: "Toyota", model: "Corolla", month: "2024-01", number: 100 },
      { make: "Honda", model: "Civic", month: "2024-01", number: 80 },
    ]);
  });

  it("should return list of car makes", async () => {
    const res = await app.request("/api/v1/cars/makes");

    expect(res.status).toBe(200);

    const data = await res.json();
    expect(data).toHaveLength(2);
    expect(data[0]).toHaveProperty("make");
    expect(data[0]).toHaveProperty("count");
  });

  it("should filter by month", async () => {
    const res = await app.request("/api/v1/cars/makes?month=2024-01");

    expect(res.status).toBe(200);

    const data = await res.json();
    expect(data).toHaveLength(2);
  });

  it("should return 400 for invalid month format", async () => {
    const res = await app.request("/api/v1/cars/makes?month=invalid");

    expect(res.status).toBe(400);
    expect(await res.json()).toHaveProperty("error");
  });
});
```

### Testing POST Endpoints

```typescript
// apps/api/__tests__/routes/blog.test.ts
import { describe, it, expect } from "vitest";
import app from "../../src/index";

describe("POST /api/v1/blog/posts", () => {
  it("should create a new post", async () => {
    const payload = {
      title: "Test Post",
      content: "Test content",
      slug: "test-post",
    };

    const res = await app.request("/api/v1/blog/posts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    expect(res.status).toBe(201);

    const data = await res.json();
    expect(data).toHaveProperty("id");
    expect(data.title).toBe(payload.title);
  });

  it("should validate required fields", async () => {
    const res = await app.request("/api/v1/blog/posts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: "Test" }), // Missing content
    });

    expect(res.status).toBe(400);
    expect(await res.json()).toHaveProperty("error");
  });

  it("should prevent duplicate slugs", async () => {
    const payload = {
      title: "Test Post",
      content: "Test content",
      slug: "duplicate",
    };

    // First insert
    await app.request("/api/v1/blog/posts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    // Duplicate insert
    const res = await app.request("/api/v1/blog/posts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    expect(res.status).toBe(409);
  });
});
```

## Testing Middleware

### Auth Middleware

```typescript
// apps/api/__tests__/middleware/auth.test.ts
import { describe, it, expect, vi } from "vitest";
import { Hono } from "hono";
import { authMiddleware } from "../../src/middleware/auth";

describe("Auth Middleware", () => {
  const app = new Hono();
  app.use("*", authMiddleware);
  app.get("/protected", (c) => c.json({ success: true }));

  it("should allow requests with valid token", async () => {
    const res = await app.request("/protected", {
      headers: {
        Authorization: "Bearer valid-token",
      },
    });

    expect(res.status).toBe(200);
  });

  it("should reject requests without token", async () => {
    const res = await app.request("/protected");

    expect(res.status).toBe(401);
    expect(await res.json()).toHaveProperty("error");
  });

  it("should reject requests with invalid token", async () => {
    const res = await app.request("/protected", {
      headers: {
        Authorization: "Bearer invalid-token",
      },
    });

    expect(res.status).toBe(401);
  });
});
```

### Error Handling Middleware

```typescript
// apps/api/__tests__/middleware/error.test.ts
import { describe, it, expect } from "vitest";
import { Hono } from "hono";
import { errorHandler } from "../../src/middleware/error";

describe("Error Handler", () => {
  const app = new Hono();
  app.onError(errorHandler);

  app.get("/error", () => {
    throw new Error("Test error");
  });

  it("should catch errors and return 500", async () => {
    const res = await app.request("/error");

    expect(res.status).toBe(500);

    const data = await res.json();
    expect(data).toHaveProperty("error");
  });

  it("should not expose stack traces in production", async () => {
    process.env.NODE_ENV = "production";

    const res = await app.request("/error");
    const data = await res.json();

    expect(data).not.toHaveProperty("stack");

    process.env.NODE_ENV = "test";
  });
});
```

## Testing Workflows

### QStash Workflow Testing

```typescript
// apps/api/__tests__/workflows/update-car-data.test.ts
import { describe, it, expect, vi } from "vitest";
import { updateCarDataWorkflow } from "../../src/lib/workflows/update-car-data";

describe("Update Car Data Workflow", () => {
  it("should fetch and process car data", async () => {
    // Mock external API
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        records: [
          { make: "Toyota", model: "Corolla", number: 100 },
        ],
      }),
    });

    global.fetch = mockFetch;

    const result = await updateCarDataWorkflow.execute();

    expect(result.success).toBe(true);
    expect(mockFetch).toHaveBeenCalled();
  });

  it("should handle API errors", async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 500,
    });

    global.fetch = mockFetch;

    await expect(updateCarDataWorkflow.execute()).rejects.toThrow();
  });

  it("should save data to database", async () => {
    // Mock successful fetch
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        records: [{ make: "Toyota", model: "Corolla", number: 100 }],
      }),
    });

    global.fetch = mockFetch;

    await updateCarDataWorkflow.execute();

    // Verify database insert
    const cars = await db.query.cars.findMany({
      where: eq(cars.make, "Toyota"),
    });

    expect(cars.length).toBeGreaterThan(0);
  });
});
```

## Mocking

### Mock Database Queries

```typescript
// apps/api/__tests__/helpers.ts
import { vi } from "vitest";
import { db } from "../src/config/database";

export const mockDbQuery = (mockData: any) => {
  return vi.spyOn(db.query.cars, "findMany").mockResolvedValue(mockData);
};

// Use in tests
import { mockDbQuery } from "./helpers";

it("should return mocked data", async () => {
  mockDbQuery([
    { make: "Toyota", model: "Corolla", number: 100 },
  ]);

  const res = await app.request("/api/v1/cars/makes");
  const data = await res.json();

  expect(data[0].make).toBe("Toyota");
});
```

### Mock External APIs

```typescript
// Mock fetch
import { vi } from "vitest";

const mockFetch = vi.fn();
global.fetch = mockFetch;

it("should fetch data from LTA", async () => {
  mockFetch.mockResolvedValue({
    ok: true,
    json: async () => ({ records: [] }),
  });

  await fetchCarData();

  expect(mockFetch).toHaveBeenCalledWith(
    expect.stringContaining("lta.gov.sg"),
    expect.any(Object)
  );
});
```

### Mock Redis

```typescript
// Mock Redis client
import { vi } from "vitest";
import { redis } from "@sgcarstrends/utils";

vi.mock("@sgcarstrends/utils", () => ({
  redis: {
    get: vi.fn(),
    set: vi.fn(),
    del: vi.fn(),
  },
}));

it("should cache results", async () => {
  await cacheData("key", { data: "value" });

  expect(redis.set).toHaveBeenCalledWith(
    "key",
    JSON.stringify({ data: "value" }),
    expect.any(Object)
  );
});
```

## Integration Testing

### Test with Real Database

```typescript
// apps/api/__tests__/integration/cars.test.ts
import { describe, it, expect, beforeEach, afterEach } from "vitest";
import app from "../../src/index";
import { db } from "../../src/config/database";
import { cars } from "@sgcarstrends/database/schema";

describe("Cars API Integration", () => {
  beforeEach(async () => {
    // Clear database
    await db.delete(cars);

    // Seed data
    await db.insert(cars).values([
      { make: "Toyota", model: "Corolla", month: "2024-01", number: 100 },
    ]);
  });

  afterEach(async () => {
    // Clean up
    await db.delete(cars);
  });

  it("should perform full CRUD operations", async () => {
    // Read
    let res = await app.request("/api/v1/cars/makes");
    expect(res.status).toBe(200);

    // Update (if endpoint exists)
    // res = await app.request("/api/v1/cars/1", { method: "PUT", ... });

    // Delete (if endpoint exists)
    // res = await app.request("/api/v1/cars/1", { method: "DELETE" });
  });
});
```

## Running Tests

### Common Commands

```bash
# Run all API tests
pnpm -F @sgcarstrends/api test

# Run specific test file
pnpm -F @sgcarstrends/api test routes/cars.test.ts

# Run tests in watch mode
pnpm -F @sgcarstrends/api test:watch

# Run with coverage
pnpm -F @sgcarstrends/api test:coverage

# Run integration tests only
pnpm -F @sgcarstrends/api test integration/
```

### Package.json Scripts

```json
{
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "test:ui": "vitest --ui"
  }
}
```

## Test Helpers

### Create Test Utilities

```typescript
// apps/api/__tests__/helpers.ts
import { Hono } from "hono";

export const createTestApp = () => {
  const app = new Hono();
  // Add middleware and routes
  return app;
};

export const createAuthHeader = (token: string) => ({
  Authorization: `Bearer ${token}`,
});

export const seedDatabase = async (data: any[]) => {
  await db.insert(cars).values(data);
};

export const clearDatabase = async () => {
  await db.delete(cars);
};

export const expectJson = async (res: Response) => {
  expect(res.headers.get("Content-Type")).toContain("application/json");
  return await res.json();
};
```

## Best Practices

### 1. Isolate Tests

```typescript
// ❌ Tests depend on each other
it("create car", async () => {
  await createCar({ make: "Toyota" });
});

it("get car", async () => {
  // Assumes car from previous test exists
  const res = await app.request("/api/v1/cars/1");
});

// ✅ Independent tests
it("get car", async () => {
  // Create car in this test
  await db.insert(cars).values({ make: "Toyota" });

  const res = await app.request("/api/v1/cars/1");
});
```

### 2. Test Error Cases

```typescript
describe("GET /api/v1/cars/:id", () => {
  it("should return car when found", async () => {
    // Test happy path
  });

  it("should return 404 when not found", async () => {
    const res = await app.request("/api/v1/cars/999");
    expect(res.status).toBe(404);
  });

  it("should return 400 for invalid ID", async () => {
    const res = await app.request("/api/v1/cars/invalid");
    expect(res.status).toBe(400);
  });
});
```

### 3. Use Descriptive Names

```typescript
// ❌ Vague test names
it("works", async () => {});
it("returns data", async () => {});

// ✅ Descriptive test names
it("should return 200 OK with list of car makes", async () => {});
it("should validate month parameter format", async () => {});
it("should cache results for 1 hour", async () => {});
```

### 4. Clean Up After Tests

```typescript
import { afterEach } from "vitest";

afterEach(async () => {
  // Clear database
  await db.delete(cars);

  // Clear cache
  await redis.flushdb();

  // Reset mocks
  vi.clearAllMocks();
});
```

## Coverage

### Generate Coverage Reports

```bash
# Generate coverage
pnpm -F @sgcarstrends/api test:coverage

# View HTML report
open apps/api/coverage/index.html
```

### Coverage Configuration

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80,
      },
      exclude: [
        "__tests__/",
        "*.config.ts",
        "dist/",
      ],
    },
  },
});
```

## Troubleshooting

### Tests Failing Randomly

```typescript
// Issue: Database state from previous tests
// Solution: Clear database in beforeEach

beforeEach(async () => {
  await db.delete(cars);
  await db.delete(coe);
});
```

### Mock Not Working

```typescript
// Issue: Mock not applied
// Solution: Ensure mock is defined before import

vi.mock("@sgcarstrends/utils", () => ({
  redis: {
    get: vi.fn(),
  },
}));

// Import after mock
import { redis } from "@sgcarstrends/utils";
```

### Timeout Errors

```typescript
// Increase timeout for slow tests
it("slow test", async () => {
  // ...
}, 10000); // 10 second timeout
```

## References

- Vitest Documentation: https://vitest.dev
- Hono Testing: https://hono.dev/docs/guides/testing
- Related files:
  - `apps/api/vitest.config.ts` - Vitest configuration
  - Root CLAUDE.md - Testing guidelines

## Best Practices Summary

1. **Isolate Tests**: Each test should be independent
2. **Test Error Cases**: Test both happy and error paths
3. **Use Mocks**: Mock external dependencies
4. **Clean Up**: Reset state after tests
5. **Descriptive Names**: Clear test descriptions
6. **Coverage Goals**: Aim for 80%+ coverage
7. **Integration Tests**: Test real database interactions
8. **Fast Tests**: Keep unit tests fast, integration tests separate
