---
name: testing-strategies
description: Unit, integration, E2E testing and TDD practices
domain: software-engineering
version: 1.0.0
tags: [testing, unit-test, integration-test, e2e, tdd, mocking]
triggers:
  keywords:
    primary: [test, testing, unit test, integration test, e2e, tdd, jest, pytest]
    secondary: [mock, stub, fixture, coverage, assertion, cypress, playwright]
  context_boost: [quality, ci, automation, reliability]
  context_penalty: [design, architecture, frontend]
  priority: high
collaboration:
  prerequisites: []
  delegation_triggers:
    - trigger: Backend service to be tested
      delegate_to: backend
      context: Service architecture, dependencies
    - trigger: Frontend component to be tested
      delegate_to: frontend
      context: Component props, user interactions
    - trigger: API contract tests
      delegate_to: api-design
      context: API specifications, expected behaviors
    - trigger: Database fixtures and test data
      delegate_to: database
      context: Schema structure, seed data patterns
  receives_context_from:
    - skill: backend
      receives:
        - Service dependencies to mock
        - Integration test scenarios
        - Database transaction boundaries
    - skill: frontend
      receives:
        - Component structure
        - User interaction patterns
        - State management approach
    - skill: api-design
      receives:
        - API contract specifications
        - Expected response formats
    - skill: database
      receives:
        - Test database setup scripts
        - Seed data patterns
  provides_context_to:
    - skill: backend
      provides:
        - Test coverage requirements
        - Mocking best practices
    - skill: frontend
      provides:
        - Component testing patterns
        - E2E test scenarios
---

# Testing Strategies

## Overview

Testing pyramid, patterns, and practices for building reliable software.

---

## Testing Pyramid

```
           /\
          /  \
         / E2E\        Few, slow, expensive
        /──────\
       /        \
      /Integration\    Some, medium speed
     /──────────────\
    /                \
   /    Unit Tests    \  Many, fast, cheap
  /____________________\
```

| Level | Speed | Scope | Quantity |
|-------|-------|-------|----------|
| Unit | Fast (ms) | Single function/class | Many (70%) |
| Integration | Medium (s) | Multiple components | Some (20%) |
| E2E | Slow (min) | Full system | Few (10%) |

---

## Unit Testing

### Structure: Arrange-Act-Assert

```typescript
describe('calculateDiscount', () => {
  it('applies 10% discount for orders over $100', () => {
    // Arrange
    const order = { items: [{ price: 150 }] };
    const discountService = new DiscountService();

    // Act
    const result = discountService.calculateDiscount(order);

    // Assert
    expect(result).toBe(15);
  });

  it('returns 0 for orders under $100', () => {
    // Arrange
    const order = { items: [{ price: 50 }] };
    const discountService = new DiscountService();

    // Act
    const result = discountService.calculateDiscount(order);

    // Assert
    expect(result).toBe(0);
  });
});
```

### Mocking

```typescript
// Mock dependencies
const mockEmailService = {
  send: jest.fn().mockResolvedValue({ success: true })
};

const mockUserRepo = {
  findById: jest.fn().mockResolvedValue({ id: '1', email: 'test@example.com' })
};

describe('NotificationService', () => {
  let service: NotificationService;

  beforeEach(() => {
    jest.clearAllMocks();
    service = new NotificationService(mockEmailService, mockUserRepo);
  });

  it('sends email to user', async () => {
    await service.notifyUser('1', 'Hello!');

    expect(mockUserRepo.findById).toHaveBeenCalledWith('1');
    expect(mockEmailService.send).toHaveBeenCalledWith(
      'test@example.com',
      'Hello!'
    );
  });

  it('throws when user not found', async () => {
    mockUserRepo.findById.mockResolvedValue(null);

    await expect(service.notifyUser('999', 'Hello!'))
      .rejects.toThrow('User not found');
  });
});
```

### Testing Edge Cases

```typescript
describe('parseAge', () => {
  // Happy path
  it('parses valid age string', () => {
    expect(parseAge('25')).toBe(25);
  });

  // Edge cases
  it('handles zero', () => {
    expect(parseAge('0')).toBe(0);
  });

  it('handles boundary values', () => {
    expect(parseAge('1')).toBe(1);
    expect(parseAge('150')).toBe(150);
  });

  // Error cases
  it('throws on negative numbers', () => {
    expect(() => parseAge('-5')).toThrow('Age cannot be negative');
  });

  it('throws on non-numeric input', () => {
    expect(() => parseAge('abc')).toThrow('Invalid age format');
  });

  it('throws on empty string', () => {
    expect(() => parseAge('')).toThrow('Age is required');
  });

  // Null/undefined
  it('throws on null', () => {
    expect(() => parseAge(null as any)).toThrow();
  });
});
```

---

## Integration Testing

### API Testing

```typescript
import request from 'supertest';
import { app } from '../app';
import { db } from '../database';

describe('POST /api/users', () => {
  beforeEach(async () => {
    await db.users.deleteMany({});
  });

  afterAll(async () => {
    await db.disconnect();
  });

  it('creates a new user', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        email: 'test@example.com',
        name: 'Test User'
      })
      .expect(201);

    expect(response.body).toMatchObject({
      id: expect.any(String),
      email: 'test@example.com',
      name: 'Test User'
    });

    // Verify in database
    const user = await db.users.findOne({ email: 'test@example.com' });
    expect(user).not.toBeNull();
  });

  it('returns 400 for invalid email', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        email: 'invalid-email',
        name: 'Test User'
      })
      .expect(400);

    expect(response.body.error).toBe('Invalid email format');
  });

  it('returns 409 for duplicate email', async () => {
    // Create first user
    await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com', name: 'First' });

    // Try to create duplicate
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com', name: 'Second' })
      .expect(409);

    expect(response.body.error).toBe('Email already exists');
  });
});
```

### Database Testing with Testcontainers

```typescript
import { PostgreSqlContainer } from '@testcontainers/postgresql';
import { Pool } from 'pg';

describe('UserRepository', () => {
  let container: StartedPostgreSqlContainer;
  let pool: Pool;
  let repo: UserRepository;

  beforeAll(async () => {
    container = await new PostgreSqlContainer().start();
    pool = new Pool({ connectionString: container.getConnectionUri() });
    await runMigrations(pool);
    repo = new UserRepository(pool);
  }, 60000);

  afterAll(async () => {
    await pool.end();
    await container.stop();
  });

  beforeEach(async () => {
    await pool.query('TRUNCATE users CASCADE');
  });

  it('creates and retrieves user', async () => {
    const created = await repo.create({
      email: 'test@example.com',
      name: 'Test'
    });

    const found = await repo.findById(created.id);

    expect(found).toEqual(created);
  });
});
```

---

## E2E Testing

### Playwright

```typescript
import { test, expect } from '@playwright/test';

test.describe('User Authentication', () => {
  test('successful login flow', async ({ page }) => {
    await page.goto('/login');

    // Fill form
    await page.fill('[data-testid="email-input"]', 'user@example.com');
    await page.fill('[data-testid="password-input"]', 'password123');

    // Submit
    await page.click('[data-testid="login-button"]');

    // Verify redirect to dashboard
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('[data-testid="welcome-message"]'))
      .toContainText('Welcome, user@example.com');
  });

  test('shows error for invalid credentials', async ({ page }) => {
    await page.goto('/login');

    await page.fill('[data-testid="email-input"]', 'wrong@example.com');
    await page.fill('[data-testid="password-input"]', 'wrongpassword');
    await page.click('[data-testid="login-button"]');

    await expect(page.locator('[data-testid="error-message"]'))
      .toBeVisible()
      .toContainText('Invalid credentials');
  });
});

test.describe('Shopping Cart', () => {
  test('add item and checkout', async ({ page }) => {
    // Setup - login
    await page.goto('/login');
    await page.fill('[data-testid="email-input"]', 'buyer@example.com');
    await page.fill('[data-testid="password-input"]', 'password');
    await page.click('[data-testid="login-button"]');

    // Browse products
    await page.goto('/products');
    await page.click('[data-testid="product-1"] [data-testid="add-to-cart"]');

    // Verify cart
    await expect(page.locator('[data-testid="cart-count"]')).toHaveText('1');

    // Checkout
    await page.click('[data-testid="cart-icon"]');
    await page.click('[data-testid="checkout-button"]');

    // Fill shipping
    await page.fill('[data-testid="address"]', '123 Test St');
    await page.click('[data-testid="place-order"]');

    // Verify success
    await expect(page).toHaveURL(/\/orders\/\d+/);
    await expect(page.locator('[data-testid="order-status"]'))
      .toContainText('Order Confirmed');
  });
});
```

### Visual Regression Testing

```typescript
import { test, expect } from '@playwright/test';

test('homepage visual regression', async ({ page }) => {
  await page.goto('/');

  // Wait for dynamic content
  await page.waitForSelector('[data-testid="hero-section"]');

  // Take screenshot and compare
  await expect(page).toHaveScreenshot('homepage.png', {
    maxDiffPixels: 100,
    threshold: 0.2
  });
});

test('responsive design', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 }); // iPhone SE
  await page.goto('/');

  await expect(page).toHaveScreenshot('homepage-mobile.png');
});
```

---

## Test-Driven Development (TDD)

### Red-Green-Refactor Cycle

```typescript
// 1. RED - Write failing test first
test('passwordValidator rejects passwords without numbers', () => {
  const result = validatePassword('NoNumbers!');
  expect(result.valid).toBe(false);
  expect(result.errors).toContain('Must contain at least one number');
});

// 2. GREEN - Write minimal code to pass
function validatePassword(password: string): ValidationResult {
  const errors: string[] = [];

  if (!/\d/.test(password)) {
    errors.push('Must contain at least one number');
  }

  return { valid: errors.length === 0, errors };
}

// 3. REFACTOR - Improve code quality
const VALIDATION_RULES = [
  { pattern: /\d/, message: 'Must contain at least one number' },
  { pattern: /[A-Z]/, message: 'Must contain at least one uppercase letter' },
  { pattern: /[a-z]/, message: 'Must contain at least one lowercase letter' },
  { pattern: /.{8,}/, message: 'Must be at least 8 characters' }
];

function validatePassword(password: string): ValidationResult {
  const errors = VALIDATION_RULES
    .filter(rule => !rule.pattern.test(password))
    .map(rule => rule.message);

  return { valid: errors.length === 0, errors };
}
```

---

## Testing Patterns

### Test Fixtures

```typescript
// fixtures/users.ts
export const validUser = {
  email: 'test@example.com',
  name: 'Test User',
  role: 'user'
};

export const adminUser = {
  ...validUser,
  role: 'admin',
  email: 'admin@example.com'
};

// In tests
import { validUser, adminUser } from '../fixtures/users';

describe('UserService', () => {
  it('creates user with valid data', async () => {
    const result = await service.create(validUser);
    expect(result.email).toBe(validUser.email);
  });
});
```

### Factory Functions

```typescript
// factories/user.factory.ts
import { faker } from '@faker-js/faker';

export function createUser(overrides: Partial<User> = {}): User {
  return {
    id: faker.string.uuid(),
    email: faker.internet.email(),
    name: faker.person.fullName(),
    createdAt: faker.date.past(),
    ...overrides
  };
}

// In tests
it('handles users with long names', () => {
  const user = createUser({ name: 'A'.repeat(100) });
  const result = formatUserCard(user);
  expect(result.displayName).toHaveLength(50); // Truncated
});
```

### Testing Async Code

```typescript
// Async/await
it('fetches user data', async () => {
  const user = await userService.getById('123');
  expect(user.name).toBe('John');
});

// Promises
it('fetches user data', () => {
  return userService.getById('123').then(user => {
    expect(user.name).toBe('John');
  });
});

// Testing rejected promises
it('throws on invalid id', async () => {
  await expect(userService.getById('invalid'))
    .rejects.toThrow('User not found');
});

// Waiting for side effects
it('debounces search input', async () => {
  const onSearch = jest.fn();
  render(<SearchBox onSearch={onSearch} debounceMs={300} />);

  await userEvent.type(screen.getByRole('textbox'), 'test');

  // Should not have called yet
  expect(onSearch).not.toHaveBeenCalled();

  // Wait for debounce
  await waitFor(() => {
    expect(onSearch).toHaveBeenCalledWith('test');
  }, { timeout: 500 });
});
```

---

## Code Coverage

### Coverage Metrics

| Metric | What It Measures |
|--------|------------------|
| Line | Percentage of lines executed |
| Branch | Percentage of if/else branches taken |
| Function | Percentage of functions called |
| Statement | Percentage of statements executed |

### Jest Configuration

```javascript
// jest.config.js
module.exports = {
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/*.stories.tsx',
    '!src/test/**'
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  }
};
```

---

## Related Skills

- [[code-quality]] - Writing testable code
- [[devops-cicd]] - CI integration
- [[performance-optimization]] - Performance testing

---

## Sharp Edges（常見陷阱）

> 這些是測試中最常見且代價最高的錯誤

### SE-1: 測試實作而非行為
- **嚴重度**: high
- **情境**: 測試過度耦合內部實作，重構時測試全部壞掉
- **原因**: 測試私有方法、mock 太細、驗證內部狀態
- **症狀**:
  - 改了一行程式碼，10 個測試失敗
  - 測試檔案比程式碼還長
  - 重構時花更多時間修測試
- **檢測**: `expect.*\.toHaveBeenCalledTimes\(\d{2,}\)|mock.*private|spy.*internal`
- **解法**: 測試公開 API/行為、使用 black-box testing、減少 mock 數量

### SE-2: 假陽性測試 (False Positive)
- **嚴重度**: critical
- **情境**: 測試永遠通過，但實際上沒有驗證任何東西
- **原因**: 忘記 await、expect 沒有執行、條件判斷錯誤
- **症狀**:
  - 測試通過但 bug 仍然存在
  - 刪掉測試中的關鍵 assertion 測試還是通過
  - Coverage 高但信心低
- **檢測**: `it\(.*\{\s*\}\)|expect\(.*\)(?!\.)|\.resolves(?!\.)|\.rejects(?!\.)`
- **解法**: TDD（先寫失敗的測試）、review 測試程式碼、使用 ESLint no-floating-promises

### SE-3: Flaky Tests（不穩定測試）
- **嚴重度**: high
- **情境**: 測試有時通過有時失敗，沒有程式碼變更
- **原因**: 依賴時間、依賴外部服務、競態條件、共享狀態
- **症狀**:
  - CI 需要 retry 才能通過
  - 本地通過但 CI 失敗
  - 團隊開始忽略失敗的測試
- **檢測**: `new Date\(\)|Date\.now\(\)|setTimeout.*\d{4,}|sleep\(\d+\)`
- **解法**: 使用 fake timers、隔離測試狀態、避免 hard-coded delays、mock 外部依賴

### SE-4: 測試金字塔倒置
- **嚴重度**: medium
- **情境**: E2E 測試太多，單元測試太少，CI 超慢
- **原因**: 「E2E 測試更接近真實」的誤解、不想寫單元測試
- **症狀**:
  - CI 跑 30+ 分鐘
  - 測試失敗難以定位問題
  - E2E 測試經常 flaky
- **檢測**: `describe.*E2E|playwright.*test|cypress.*it` (數量遠超 unit test)
- **解法**: 遵循 70% unit / 20% integration / 10% E2E 比例、E2E 只測關鍵路徑

### SE-5: 過度 Mocking
- **嚴重度**: medium
- **情境**: Mock 太多導致測試失去意義，只是在測試 mock
- **原因**: 為了隔離而 mock 所有依賴、測試執行時間焦慮
- **症狀**:
  - 測試通過但整合時失敗
  - Mock 的行為與真實行為不符
  - 更新依賴後 mock 過時
- **檢測**: `jest\.mock.*jest\.mock.*jest\.mock|mock\(.*\).*mock\(.*\).*mock\(`
- **解法**: 只 mock 外部依賴（網路、檔案系統）、使用真實的 in-memory 實作、寫更多整合測試

---

## Validations

### V-1: 禁止空的測試
- **類型**: regex
- **嚴重度**: critical
- **模式**: `(it|test)\s*\([^)]+,\s*(async\s*)?\(\)\s*=>\s*\{\s*\}\s*\)`
- **訊息**: Empty test detected - test has no assertions
- **修復建議**: Add meaningful assertions with expect()
- **適用**: `*.test.ts`, `*.test.js`, `*.spec.ts`, `*.spec.js`

### V-2: 測試缺少 assertion
- **類型**: regex
- **嚴重度**: high
- **模式**: `(it|test)\s*\([^)]+,\s*(async\s*)?\(\)\s*=>\s*\{[^}]*\}(?![^}]*expect)`
- **訊息**: Test without expect() assertion may be a false positive
- **修復建議**: Add at least one expect() assertion
- **適用**: `*.test.ts`, `*.test.js`, `*.spec.ts`, `*.spec.js`

### V-3: 禁止 fit/fdescribe (focused tests)
- **類型**: regex
- **嚴重度**: critical
- **模式**: `\b(fit|fdescribe|it\.only|describe\.only|test\.only)\s*\(`
- **訊息**: Focused test will skip other tests in CI
- **修復建議**: Remove `f` prefix or `.only` before committing
- **適用**: `*.test.ts`, `*.test.js`, `*.spec.ts`, `*.spec.js`

### V-4: 禁止 skip tests 無說明
- **類型**: regex
- **嚴重度**: medium
- **模式**: `(xit|xdescribe|it\.skip|describe\.skip|test\.skip)\s*\([^)]+\)`
- **訊息**: Skipped test without documented reason
- **修復建議**: Add comment explaining why test is skipped and tracking issue
- **適用**: `*.test.ts`, `*.test.js`, `*.spec.ts`, `*.spec.js`

### V-5: 測試中使用 setTimeout
- **類型**: regex
- **嚴重度**: high
- **模式**: `setTimeout\s*\(\s*[^,]+,\s*\d{3,}\s*\)`
- **訊息**: Hard-coded delays in tests cause flakiness and slow tests
- **修復建議**: Use `jest.useFakeTimers()` or `waitFor()` from testing-library
- **適用**: `*.test.ts`, `*.test.js`, `*.spec.ts`, `*.spec.js`
