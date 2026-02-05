---
name: testing
description: Comprehensive testing standards including unit, integration, security, and property-based testing with TDD methodology
---

# Testing Standards Skill

## Level 1: Quick Start (5 minutes)

### What You'll Learn

Implement effective testing strategies to ensure code quality, catch bugs early, and maintain confidence in changes.

### Core Principles

- **Test First**: Write tests before implementation (TDD)
- **Coverage**: Aim for >80% code coverage
- **Isolation**: Tests should be independent and repeatable
- **Speed**: Keep unit tests fast (<100ms each)

### Testing Pyramid

```
      /\
     /  \  E2E Tests (Few)
    /----\
   / Inte \
  / gration \ (Some)
 /  Tests   \
/------------\
/ Unit Tests  \ (Many)
/--------------\
```

### Quick Start Example

```typescript
// 1. Write the test first (RED)
describe("calculateDiscount", () => {
  it("should apply 10% discount for premium users", () => {
    const user = { tier: "premium" };
    const order = { total: 100 };

    const result = calculateDiscount(user, order);

    expect(result).toBe(90);
  });
});

// 2. Implement minimal code (GREEN)
function calculateDiscount(user, order) {
  if (user.tier === "premium") {
    return order.total * 0.9;
  }
  return order.total;
}

// 3. Refactor (REFACTOR)
function calculateDiscount(
  user: User,
  order: Order
): number {
  const PREMIUM_DISCOUNT = 0.1;
  return user.tier === "premium"
    ? order.total * (1 - PREMIUM_DISCOUNT)
    : order.total;
}
```

### Essential Checklist

- [ ] Unit tests for all business logic
- [ ] Integration tests for critical paths
- [ ] Tests run in CI/CD pipeline
- [ ] Coverage >80%
- [ ] Tests are maintainable and readable

### Common Pitfalls

- Testing implementation details instead of behavior
- Slow tests that discourage running them
- Flaky tests that fail intermittently
- Poor test isolation (shared state)

---

## Level 2: Implementation (30 minutes)

### Deep Dive Topics

#### 1. Test-Driven Development (TDD)

**Red-Green-Refactor Cycle:**

```typescript
// STEP 1: RED - Write failing test
describe("UserService", () => {
  describe("createUser", () => {
    it("should hash password before saving", async () => {
      const userData = {
        email: "test@example.com",
        password: "SecurePass123!",
      };

      const service = new UserService(mockRepository, mockHasher);
      await service.createUser(userData);

      expect(mockHasher.hash).toHaveBeenCalledWith("SecurePass123!");
      expect(mockRepository.save).toHaveBeenCalledWith(
        expect.objectContaining({
          email: "test@example.com",
          passwordHash: expect.any(String),
        })
      );
    });
  });
});

// STEP 2: GREEN - Minimal implementation
class UserService {
  constructor(
    private repository: UserRepository,
    private hasher: PasswordHasher
  ) {}

  async createUser(userData: UserData): Promise<User> {
    const passwordHash = await this.hasher.hash(userData.password);
    return this.repository.save({
      ...userData,
      passwordHash,
    });
  }
}

// STEP 3: REFACTOR - Improve design
class UserService {
  constructor(
    private repository: UserRepository,
    private hasher: PasswordHasher,
    private validator: UserValidator
  ) {}

  async createUser(userData: UserData): Promise<User> {
    await this.validator.validate(userData);
    const passwordHash = await this.hasher.hash(userData.password);

    const user = new User({
      email: userData.email,
      passwordHash,
      createdAt: new Date(),
    });

    return this.repository.save(user);
  }
}
```

**NIST Mapping:**

- @nist-controls: [si-10, si-11, au-2, au-3]

#### 2. Property-Based Testing

```typescript
import { fc } from "fast-check";

// Traditional example-based test
it("should reverse a reversed string back to original", () => {
  expect(reverse(reverse("hello"))).toBe("hello");
  expect(reverse(reverse("world"))).toBe("world");
  // Limited to specific examples
});

// Property-based test - tests thousands of cases
it("reversing twice should return original string", () => {
  fc.assert(
    fc.property(fc.string(), (str) => {
      expect(reverse(reverse(str))).toBe(str);
    })
  );
});

// Complex property testing
describe("calculateTotal", () => {
  it("should always return non-negative totals", () => {
    fc.assert(
      fc.property(
        fc.array(fc.record({ price: fc.nat(), quantity: fc.nat() })),
        (items) => {
          const total = calculateTotal(items);
          expect(total).toBeGreaterThanOrEqual(0);
        }
      )
    );
  });

  it("should be commutative (order doesn't matter)", () => {
    fc.assert(
      fc.property(fc.array(fc.record({ price: fc.nat(), quantity: fc.nat() })), (items) => {
        const total1 = calculateTotal(items);
        const total2 = calculateTotal([...items].reverse());
        expect(total1).toBe(total2);
      })
    );
  });
});
```

#### 3. Integration Testing

```typescript
// API Integration Test
describe("POST /api/users", () => {
  let app: Express;
  let db: Database;

  beforeAll(async () => {
    // Setup test database
    db = await createTestDatabase();
    app = createApp({ database: db });
  });

  afterAll(async () => {
    await db.close();
  });

  beforeEach(async () => {
    // Clean state between tests
    await db.truncate("users");
  });

  it("should create a new user", async () => {
    const response = await request(app)
      .post("/api/users")
      .send({
        email: "test@example.com",
        password: "SecurePass123!",
        name: "Test User",
      })
      .expect(201);

    expect(response.body).toMatchObject({
      id: expect.any(String),
      email: "test@example.com",
      name: "Test User",
    });

    // Verify in database
    const user = await db.query("SELECT * FROM users WHERE email = ?", [
      "test@example.com",
    ]);
    expect(user).toBeDefined();
    expect(user.passwordHash).not.toBe("SecurePass123!"); // Should be hashed
  });

  it("should reject duplicate emails", async () => {
    // Create first user
    await request(app).post("/api/users").send({
      email: "test@example.com",
      password: "SecurePass123!",
    });

    // Attempt duplicate
    await request(app)
      .post("/api/users")
      .send({
        email: "test@example.com",
        password: "AnotherPass456!",
      })
      .expect(409);
  });
});
```

#### 4. Security Testing

```typescript
// Input validation tests
describe("Security: Input Validation", () => {
  it("should reject SQL injection attempts", async () => {
    const maliciousInput = "'; DROP TABLE users; --";

    await request(app)
      .get(`/api/users/search?name=${maliciousInput}`)
      .expect(400);
  });

  it("should sanitize XSS attempts", async () => {
    const xssPayload = '<script>alert("XSS")</script>';

    const response = await request(app)
      .post("/api/comments")
      .send({ content: xssPayload })
      .expect(201);

    expect(response.body.content).not.toContain("<script>");
  });

  it("should enforce rate limiting", async () => {
    const requests = Array(101)
      .fill(null)
      .map(() => request(app).get("/api/data"));

    const responses = await Promise.all(requests);
    const rateLimited = responses.filter((r) => r.status === 429);

    expect(rateLimited.length).toBeGreaterThan(0);
  });
});

// Authentication tests
describe("Security: Authentication", () => {
  it("should require authentication for protected routes", async () => {
    await request(app).get("/api/protected").expect(401);
  });

  it("should reject expired tokens", async () => {
    const expiredToken = generateExpiredToken();

    await request(app)
      .get("/api/protected")
      .set("Authorization", `Bearer ${expiredToken}`)
      .expect(401);
  });
});
```

#### 5. Performance Testing

```typescript
// Benchmark testing
describe("Performance: calculateComplexMetric", () => {
  it("should complete within 100ms for 1000 items", async () => {
    const items = generateTestData(1000);

    const start = performance.now();
    await calculateComplexMetric(items);
    const duration = performance.now() - start;

    expect(duration).toBeLessThan(100);
  });

  it("should scale linearly with input size", async () => {
    const sizes = [100, 200, 400, 800];
    const timings: number[] = [];

    for (const size of sizes) {
      const items = generateTestData(size);
      const start = performance.now();
      await calculateComplexMetric(items);
      timings.push(performance.now() - start);
    }

    // Check that doubling input approximately doubles time
    expect(timings[1] / timings[0]).toBeCloseTo(2, 0.5);
    expect(timings[2] / timings[1]).toBeCloseTo(2, 0.5);
  });
});

// Load testing with autocannon
import autocannon from "autocannon";

describe("Load Testing", () => {
  it("should handle 1000 req/s with <200ms p95 latency", async () => {
    const result = await autocannon({
      url: "http://localhost:3000/api/health",
      connections: 100,
      duration: 10,
      pipelining: 10,
    });

    expect(result.requests.average).toBeGreaterThan(1000);
    expect(result.latency.p95).toBeLessThan(200);
  });
});
```

#### 6. Mutation Testing

```typescript
// Original code
function isAdult(age: number): boolean {
  return age >= 18;
}

// Mutation 1: Change >= to >
// function isAdult(age: number): boolean {
//   return age > 18;
// }

// This test would catch mutation 1
it("should consider 18 as adult", () => {
  expect(isAdult(18)).toBe(true);
});

// Mutation 2: Change 18 to 17
// function isAdult(age: number): boolean {
//   return age >= 17;
// }

// This test would catch mutation 2
it("should not consider 17 as adult", () => {
  expect(isAdult(17)).toBe(false);
});

// Run mutation testing
// npm install --save-dev stryker
// npx stryker run
```

### Test Organization

```typescript
// Arrange-Act-Assert (AAA) Pattern
describe("OrderService", () => {
  describe("calculateTotal", () => {
    it("should apply discount to eligible orders", () => {
      // ARRANGE - Setup test data
      const order = {
        items: [
          { price: 100, quantity: 2 },
          { price: 50, quantity: 1 },
        ],
        discountCode: "SAVE10",
      };
      const service = new OrderService();

      // ACT - Execute the behavior
      const total = service.calculateTotal(order);

      // ASSERT - Verify the outcome
      expect(total).toBe(225); // (200 + 50) * 0.9
    });
  });
});
```

### Integration Points

- Links to [Coding Standards](../coding-standards/SKILL.md) for testable code design
- Links to [Security Practices](../security-practices/SKILL.md) for security testing
- Links to [NIST Compliance](../nist-compliance/SKILL.md) for SI-10, SI-11 controls

---

## Level 3: Mastery (Extended Learning)

### Advanced Topics

#### 1. Contract Testing

```typescript
// Provider contract (API server)
import { Pact } from "@pact-foundation/pact";

describe("User API Provider", () => {
  const provider = new Pact({
    consumer: "UserService",
    provider: "UserAPI",
  });

  beforeAll(() => provider.setup());
  afterAll(() => provider.finalize());

  it("should provide user by ID", async () => {
    await provider.addInteraction({
      state: "user 123 exists",
      uponReceiving: "a request for user 123",
      withRequest: {
        method: "GET",
        path: "/users/123",
      },
      willRespondWith: {
        status: 200,
        body: {
          id: "123",
          name: "John Doe",
          email: "john@example.com",
        },
      },
    });

    await provider.verify();
  });
});
```

#### 2. Chaos Engineering

```typescript
// Simulate failures to test resilience
class ChaosMonkey {
  private failureRate: number;

  constructor(failureRate: number = 0.1) {
    this.failureRate = failureRate;
  }

  async injectFailure<T>(operation: () => Promise<T>): Promise<T> {
    if (Math.random() < this.failureRate) {
      throw new Error("Simulated failure");
    }
    return operation();
  }
}

describe("Resilience Testing", () => {
  it("should retry failed operations", async () => {
    const chaos = new ChaosMonkey(0.5); // 50% failure rate
    let attempts = 0;

    const result = await retry(
      async () => {
        attempts++;
        return chaos.injectFailure(() => fetchData());
      },
      { maxAttempts: 3, delay: 100 }
    );

    expect(result).toBeDefined();
    expect(attempts).toBeGreaterThan(1);
  });
});
```

#### 3. Visual Regression Testing

```typescript
import { test, expect } from "@playwright/test";

test("homepage should match snapshot", async ({ page }) => {
  await page.goto("https://example.com");

  // Take screenshot and compare with baseline
  await expect(page).toHaveScreenshot("homepage.png", {
    maxDiffPixels: 100,
  });
});

test("button hover state", async ({ page }) => {
  await page.goto("https://example.com");
  await page.hover("button.primary");

  await expect(page.locator("button.primary")).toHaveScreenshot(
    "button-hover.png"
  );
});
```

### Resources

#### Essential Reading

- [Test Driven Development by Kent Beck](https://www.oreilly.com/library/view/test-driven-development/0321146530/)
- [Growing Object-Oriented Software, Guided by Tests](http://www.growing-object-oriented-software.com/)
- [Unit Testing Principles, Practices, and Patterns by Vladimir Khorikov](https://www.manning.com/books/unit-testing)

#### Testing Frameworks

- **Unit Testing**: Jest, Vitest, pytest, JUnit
- **Integration Testing**: Supertest, TestContainers
- **E2E Testing**: Playwright, Cypress, Selenium
- **Property Testing**: fast-check, Hypothesis, QuickCheck
- **Mutation Testing**: Stryker, PIT, mutmut

#### Tools and Services

- **CI/CD**: GitHub Actions, GitLab CI, CircleCI
- **Coverage**: Istanbul, Coverage.py, JaCoCo
- **Load Testing**: k6, Artillery, Gatling
- **Contract Testing**: Pact, Spring Cloud Contract

### Templates

#### Test Suite Template

```typescript
describe("FeatureName", () => {
  // Setup and teardown
  beforeAll(async () => {
    // One-time setup
  });

  afterAll(async () => {
    // One-time cleanup
  });

  beforeEach(() => {
    // Reset state before each test
  });

  afterEach(() => {
    // Cleanup after each test
  });

  // Happy path tests
  describe("when conditions are normal", () => {
    it("should perform expected behavior", () => {
      // Test implementation
    });
  });

  // Edge cases
  describe("when edge conditions occur", () => {
    it("should handle edge case gracefully", () => {
      // Test implementation
    });
  });

  // Error cases
  describe("when errors occur", () => {
    it("should handle errors appropriately", () => {
      // Test implementation
    });
  });
});
```

### Scripts

See `./scripts/` for:

- Test coverage reporters
- Mutation testing runners
- Performance benchmark tools
- Test data generators

## Examples

### Basic Usage

```python
// TODO: Add basic example for testing
// This example demonstrates core functionality
```

### Advanced Usage

```python
// TODO: Add advanced example for testing
// This example shows production-ready patterns
```

### Integration Example

```python
// TODO: Add integration example showing how testing
// works with other systems and services
```

See `examples/testing/` for complete working examples.

## Integration Points

This skill integrates with:

### Upstream Dependencies

- **Tools**: Common development tools and frameworks
- **Prerequisites**: Basic understanding of general concepts

### Downstream Consumers

- **Applications**: Production systems requiring testing functionality
- **CI/CD Pipelines**: Automated testing and deployment workflows
- **Monitoring Systems**: Observability and logging platforms

### Related Skills

- See other skills in this category

### Common Integration Patterns

1. **Development Workflow**: How this skill fits into daily development
2. **Production Deployment**: Integration with production systems
3. **Monitoring & Alerting**: Observability integration points

## Common Pitfalls

### Pitfall 1: Insufficient Testing

**Problem:** Not testing edge cases and error conditions leads to production bugs

**Solution:** Implement comprehensive test coverage including:

- Happy path scenarios
- Error handling and edge cases
- Integration points with external systems

**Prevention:** Enforce minimum code coverage (80%+) in CI/CD pipeline

### Pitfall 2: Hardcoded Configuration

**Problem:** Hardcoding values makes applications inflexible and environment-dependent

**Solution:** Use environment variables and configuration management:

- Separate config from code
- Use environment-specific configuration files
- Never commit secrets to version control

**Prevention:** Use tools like dotenv, config validators, and secret scanners

### Pitfall 3: Ignoring Security Best Practices

**Problem:** Security vulnerabilities from not following established security patterns

**Solution:** Follow security guidelines:

- Input validation and sanitization
- Proper authentication and authorization
- Encrypted data transmission (TLS/SSL)
- Regular security audits and updates

**Prevention:** Use security linters, SAST tools, and regular dependency updates

**Best Practices:**

- Follow established patterns and conventions for testing
- Keep dependencies up to date and scan for vulnerabilities
- Write comprehensive documentation and inline comments
- Use linting and formatting tools consistently
- Implement proper error handling and logging
- Regular code reviews and pair programming
- Monitor production metrics and set up alerts

---

## Bundled Resources

- [Full TESTING_STANDARDS.md](../../docs/standards/TESTING_STANDARDS.md)
- [UNIFIED_STANDARDS.md](../../docs/standards/UNIFIED_STANDARDS.md)
- Test configuration templates in `./templates/`
- Testing utility scripts in `./scripts/`
- Example test suites in `./resources/`
