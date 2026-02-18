---
name: encore-testing
description: Test APIs and services with Vitest in Encore.ts.
---

# Testing Encore.ts Applications

## Instructions

Encore.ts uses standard TypeScript testing tools. The recommended setup is Vitest.

### Setup Vitest

```bash
npm install -D vitest
```

Add to `package.json`:

```json
{
  "scripts": {
    "test": "vitest"
  }
}
```

### Test an API Endpoint

```typescript
// api.test.ts
import { describe, it, expect } from "vitest";
import { hello } from "./api";

describe("hello endpoint", () => {
  it("returns a greeting", async () => {
    const response = await hello();
    expect(response.message).toBe("Hello, World!");
  });
});
```

### Run Tests

```bash
# Run with Encore (recommended - sets up infrastructure)
encore test

# Or run directly with npm
npm test
```

Using `encore test` is recommended because it:
- Sets up test databases automatically
- Provides isolated infrastructure per test
- Handles service dependencies

### Test with Request Parameters

```typescript
// api.test.ts
import { describe, it, expect } from "vitest";
import { getUser } from "./api";

describe("getUser endpoint", () => {
  it("returns the user by ID", async () => {
    const user = await getUser({ id: "123" });
    expect(user.id).toBe("123");
    expect(user.name).toBeDefined();
  });
});
```

### Test Database Operations

Encore provides isolated test databases:

```typescript
// user.test.ts
import { describe, it, expect, beforeEach } from "vitest";
import { createUser, getUser, db } from "./user";

describe("user operations", () => {
  beforeEach(async () => {
    // Clean up before each test
    await db.exec`DELETE FROM users`;
  });

  it("creates and retrieves a user", async () => {
    const created = await createUser({ email: "test@example.com", name: "Test" });
    const retrieved = await getUser({ id: created.id });
    
    expect(retrieved.email).toBe("test@example.com");
  });
});
```

### Test Service-to-Service Calls

```typescript
// order.test.ts
import { describe, it, expect } from "vitest";
import { createOrder } from "./order";

describe("order service", () => {
  it("creates an order and notifies user service", async () => {
    // Service calls work normally in tests
    const order = await createOrder({
      userId: "user-123",
      items: [{ productId: "prod-1", quantity: 2 }],
    });
    
    expect(order.id).toBeDefined();
    expect(order.status).toBe("pending");
  });
});
```

### Test Error Cases

```typescript
import { describe, it, expect } from "vitest";
import { getUser } from "./api";
import { APIError } from "encore.dev/api";

describe("error handling", () => {
  it("throws NotFound for missing user", async () => {
    await expect(getUser({ id: "nonexistent" }))
      .rejects
      .toThrow("user not found");
  });

  it("throws with correct error code", async () => {
    try {
      await getUser({ id: "nonexistent" });
    } catch (error) {
      expect(error).toBeInstanceOf(APIError);
      expect((error as APIError).code).toBe("not_found");
    }
  });
});
```

### Test Pub/Sub

```typescript
// notifications.test.ts
import { describe, it, expect, vi } from "vitest";
import { orderCreated } from "./events";

describe("pub/sub", () => {
  it("publishes order created event", async () => {
    const messageId = await orderCreated.publish({
      orderId: "order-123",
      userId: "user-456",
      total: 9999,
    });
    
    expect(messageId).toBeDefined();
  });
});
```

### Test Cron Jobs

Test the underlying function, not the cron schedule:

```typescript
// cleanup.test.ts
import { describe, it, expect } from "vitest";
import { cleanupExpiredSessions } from "./cleanup";

describe("cleanup job", () => {
  it("removes expired sessions", async () => {
    // Create some expired sessions first
    await createExpiredSession();
    
    // Call the endpoint directly
    await cleanupExpiredSessions();
    
    // Verify cleanup happened
    const remaining = await countSessions();
    expect(remaining).toBe(0);
  });
});
```

### Mocking External Services

```typescript
import { describe, it, expect, vi, beforeEach } from "vitest";
import { sendWelcomeEmail } from "./email";

// Mock external API
vi.mock("./external-email-client", () => ({
  send: vi.fn().mockResolvedValue({ success: true }),
}));

describe("email service", () => {
  it("sends welcome email", async () => {
    const result = await sendWelcomeEmail({ userId: "123" });
    expect(result.sent).toBe(true);
  });
});
```

### Test Configuration

Create `vitest.config.ts`:

```typescript
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    environment: "node",
    include: ["**/*.test.ts"],
    coverage: {
      reporter: ["text", "json", "html"],
    },
  },
});
```

### Guidelines

- Use `encore test` to run tests with infrastructure setup
- Each test file gets an isolated database transaction (rolled back after)
- Test API endpoints by calling them directly as functions
- Service-to-service calls work normally in tests
- Mock external dependencies (third-party APIs, email services, etc.)
- Don't mock Encore infrastructure (databases, Pub/Sub) - use the real thing
