---
name: qa-engineer
description: Expert guidance for software testing and quality assurance. Use when the user asks to write tests, create test plans, review code for bugs, perform code reviews, write test cases, set up testing frameworks, debug issues, validate requirements, create bug reports, perform regression testing, or improve test coverage. Triggers on testing, QA, quality assurance, test cases, bug reports, test automation, unit tests, integration tests, E2E tests, test coverage, debugging, code review.
---

# QA Engineer & Software Testing Expert

Expert guidance for comprehensive software testing, quality assurance, and bug detection.

## Testing Philosophy

### Core Principles
1. **Shift left** — Find bugs early; prevention over detection
2. **Risk-based testing** — Prioritize high-impact, high-probability failure areas
3. **Test pyramid** — Many unit tests, fewer integration tests, minimal E2E tests
4. **Automation first** — Automate repetitive tests; manual for exploratory
5. **Clean test code** — Tests are production code; maintain them accordingly

### Test Pyramid Distribution
```
        /\
       /  \      E2E (5-10%)
      /----\     - Critical user journeys
     /      \    
    /--------\   Integration (15-25%)
   /          \  - API contracts, DB interactions
  /------------\ 
 /              \ Unit (65-80%)
/________________\ - Functions, components, logic
```

## Test Case Design

### Structure (Arrange-Act-Assert)

```typescript
describe('ShoppingCart', () => {
  describe('addItem', () => {
    it('should increase quantity when adding existing item', () => {
      // Arrange
      const cart = new ShoppingCart();
      cart.addItem({ id: '1', name: 'Apple', quantity: 1 });
      
      // Act
      cart.addItem({ id: '1', name: 'Apple', quantity: 2 });
      
      // Assert
      expect(cart.getItem('1').quantity).toBe(3);
    });
  });
});
```

### Naming Convention
```
[Unit]_[Scenario]_[ExpectedResult]

Examples:
- calculateTotal_withEmptyCart_returnsZero
- login_withInvalidPassword_showsErrorMessage
- submitOrder_whenOutOfStock_preventsCheckout
```

### Test Case Categories

**Positive Tests** — Valid inputs produce expected outputs
```typescript
it('should create user with valid email and password', async () => {
  const user = await createUser('test@example.com', 'ValidPass123!');
  expect(user.id).toBeDefined();
  expect(user.email).toBe('test@example.com');
});
```

**Negative Tests** — Invalid inputs handled gracefully
```typescript
it('should reject user creation with invalid email', async () => {
  await expect(createUser('invalid-email', 'ValidPass123!'))
    .rejects.toThrow('Invalid email format');
});
```

**Boundary Tests** — Edge cases at limits
```typescript
it('should accept password with exactly 8 characters (minimum)', () => {
  expect(() => validatePassword('Pass123!')).not.toThrow();
});

it('should reject password with 7 characters (below minimum)', () => {
  expect(() => validatePassword('Pass12!')).toThrow();
});
```

**Error Handling Tests** — Failures fail gracefully
```typescript
it('should handle network timeout gracefully', async () => {
  mockApi.simulateTimeout();
  const result = await fetchUserData('123');
  expect(result.error).toBe('Request timed out. Please try again.');
  expect(result.data).toBeNull();
});
```

## Test Types & Frameworks

### Unit Testing

**JavaScript/TypeScript — Jest/Vitest**
```typescript
// Function to test
export function calculateDiscount(price: number, percentage: number): number {
  if (percentage < 0 || percentage > 100) {
    throw new Error('Invalid percentage');
  }
  return price * (1 - percentage / 100);
}

// Test file
import { calculateDiscount } from './pricing';

describe('calculateDiscount', () => {
  it('applies 20% discount correctly', () => {
    expect(calculateDiscount(100, 20)).toBe(80);
  });

  it('handles 0% discount', () => {
    expect(calculateDiscount(100, 0)).toBe(100);
  });

  it('handles 100% discount', () => {
    expect(calculateDiscount(100, 100)).toBe(0);
  });

  it('throws on negative percentage', () => {
    expect(() => calculateDiscount(100, -10)).toThrow('Invalid percentage');
  });

  it('handles decimal prices', () => {
    expect(calculateDiscount(99.99, 10)).toBeCloseTo(89.99, 2);
  });
});
```

**React Components — React Testing Library**
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { Counter } from './Counter';

describe('Counter', () => {
  it('renders initial count', () => {
    render(<Counter initialCount={5} />);
    expect(screen.getByText('Count: 5')).toBeInTheDocument();
  });

  it('increments count on button click', () => {
    render(<Counter initialCount={0} />);
    fireEvent.click(screen.getByRole('button', { name: /increment/i }));
    expect(screen.getByText('Count: 1')).toBeInTheDocument();
  });

  it('calls onChange callback when count changes', () => {
    const handleChange = jest.fn();
    render(<Counter initialCount={0} onChange={handleChange} />);
    fireEvent.click(screen.getByRole('button', { name: /increment/i }));
    expect(handleChange).toHaveBeenCalledWith(1);
  });
});
```

### Integration Testing

**API Integration — Supertest**
```typescript
import request from 'supertest';
import { app } from '../app';
import { db } from '../db';

describe('POST /api/users', () => {
  beforeEach(async () => {
    await db.clear('users');
  });

  it('creates user and returns 201', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com', password: 'SecurePass123!' })
      .expect(201);

    expect(response.body.user.email).toBe('test@example.com');
    expect(response.body.user.password).toBeUndefined(); // Not exposed
    
    // Verify database state
    const dbUser = await db.users.findByEmail('test@example.com');
    expect(dbUser).toBeDefined();
  });

  it('returns 409 for duplicate email', async () => {
    await db.users.create({ email: 'test@example.com', password: 'hash' });
    
    await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com', password: 'SecurePass123!' })
      .expect(409);
  });
});
```

**Database Integration**
```typescript
describe('UserRepository', () => {
  let repo: UserRepository;

  beforeAll(async () => {
    await setupTestDatabase();
    repo = new UserRepository(testDb);
  });

  afterEach(async () => {
    await testDb.clear('users');
  });

  afterAll(async () => {
    await teardownTestDatabase();
  });

  it('persists and retrieves user correctly', async () => {
    const created = await repo.create({ name: 'John', email: 'john@test.com' });
    const retrieved = await repo.findById(created.id);
    
    expect(retrieved).toMatchObject({
      name: 'John',
      email: 'john@test.com',
    });
  });
});
```

### E2E Testing

**Playwright**
```typescript
import { test, expect } from '@playwright/test';

test.describe('User Authentication', () => {
  test('complete login flow', async ({ page }) => {
    await page.goto('/login');
    
    await page.fill('[data-testid="email-input"]', 'user@example.com');
    await page.fill('[data-testid="password-input"]', 'password123');
    await page.click('[data-testid="login-button"]');
    
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('[data-testid="welcome-message"]'))
      .toContainText('Welcome back');
  });

  test('shows error for invalid credentials', async ({ page }) => {
    await page.goto('/login');
    
    await page.fill('[data-testid="email-input"]', 'user@example.com');
    await page.fill('[data-testid="password-input"]', 'wrongpassword');
    await page.click('[data-testid="login-button"]');
    
    await expect(page.locator('[data-testid="error-message"]'))
      .toContainText('Invalid credentials');
    await expect(page).toHaveURL('/login');
  });
});
```

**Mobile E2E — Detox (React Native)**
```typescript
describe('Shopping List', () => {
  beforeAll(async () => {
    await device.launchApp({ newInstance: true });
  });

  it('should add item to shopping list', async () => {
    await element(by.id('add-item-button')).tap();
    await element(by.id('item-name-input')).typeText('Milk');
    await element(by.id('item-quantity-input')).typeText('2');
    await element(by.id('save-button')).tap();
    
    await expect(element(by.text('Milk'))).toBeVisible();
    await expect(element(by.text('2'))).toBeVisible();
  });

  it('should mark item as bought', async () => {
    await element(by.id('item-checkbox-milk')).tap();
    await expect(element(by.id('item-milk'))).toHaveToggleValue(true);
  });
});
```

## Mocking Strategies

### Function Mocks
```typescript
// Mock external service
jest.mock('../services/emailService', () => ({
  sendEmail: jest.fn().mockResolvedValue({ success: true }),
}));

// Test with mock
it('sends welcome email on registration', async () => {
  await registerUser({ email: 'test@example.com', password: 'Pass123!' });
  
  expect(emailService.sendEmail).toHaveBeenCalledWith({
    to: 'test@example.com',
    template: 'welcome',
  });
});
```

### API Mocks — MSW (Mock Service Worker)
```typescript
import { rest } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  rest.get('/api/users/:id', (req, res, ctx) => {
    return res(ctx.json({ id: req.params.id, name: 'Test User' }));
  }),
  rest.post('/api/users', (req, res, ctx) => {
    return res(ctx.status(201), ctx.json({ id: '123', ...req.body }));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

it('handles server error gracefully', async () => {
  server.use(
    rest.get('/api/users/:id', (req, res, ctx) => {
      return res(ctx.status(500));
    })
  );
  
  const result = await fetchUser('123');
  expect(result.error).toBe('Server error');
});
```

### Time Mocks
```typescript
beforeEach(() => {
  jest.useFakeTimers();
  jest.setSystemTime(new Date('2024-01-15T10:00:00Z'));
});

afterEach(() => {
  jest.useRealTimers();
});

it('expires session after 30 minutes', () => {
  const session = createSession();
  
  jest.advanceTimersByTime(31 * 60 * 1000); // 31 minutes
  
  expect(session.isExpired()).toBe(true);
});
```

## Bug Report Template

```markdown
## Bug Report: [Short descriptive title]

**Severity:** Critical | High | Medium | Low
**Priority:** P0 | P1 | P2 | P3
**Environment:** Production | Staging | Development
**Platform:** iOS 17.2 / Android 14 / Chrome 120 / etc.

### Summary
[One sentence description of the issue]

### Steps to Reproduce
1. Navigate to [page/screen]
2. Enter [specific data]
3. Click [button/action]
4. Observe [behavior]

### Expected Behavior
[What should happen]

### Actual Behavior
[What actually happens]

### Evidence
- Screenshots: [attached]
- Video: [link]
- Console logs: [attached]
- Network trace: [attached]

### Impact
[Who is affected and how severely]

### Workaround
[If any temporary solution exists]

### Additional Context
- First noticed: [date]
- Frequency: Always | Intermittent (X/10 attempts)
- Related issues: #123, #456
```

## Test Plan Template

```markdown
# Test Plan: [Feature/Release Name]

## Overview
**Objective:** [What we're testing]
**Scope:** [In scope / Out of scope]
**Timeline:** [Start date - End date]

## Test Strategy

### Test Levels
| Level       | Coverage | Automation |
|-------------|----------|------------|
| Unit        | 80%+     | 100%       |
| Integration | Critical paths | 90%   |
| E2E         | Happy paths | 70%      |
| Manual      | Edge cases | N/A       |

### Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Payment failures | Medium | Critical | Extra payment gateway tests |
| Data migration | Low | High | Rollback testing |

## Test Cases

### Functional Tests
- [ ] TC001: User can create account with valid data
- [ ] TC002: User cannot create account with duplicate email
- [ ] TC003: User receives verification email
...

### Non-Functional Tests
- [ ] Performance: Page load < 2s
- [ ] Security: SQL injection prevention
- [ ] Accessibility: WCAG 2.1 AA compliance

## Entry/Exit Criteria

**Entry:**
- [ ] Code complete and deployed to staging
- [ ] Test data prepared
- [ ] Test environment stable

**Exit:**
- [ ] All critical tests pass
- [ ] No P0/P1 bugs open
- [ ] Test coverage meets targets
- [ ] Sign-off from QA lead
```

## Code Review Checklist

### Functionality
- [ ] Code does what the ticket/PR describes
- [ ] Edge cases handled
- [ ] Error handling is appropriate
- [ ] No hardcoded values that should be configurable

### Security
- [ ] No sensitive data logged or exposed
- [ ] Input validation present
- [ ] SQL/NoSQL injection prevented
- [ ] Authentication/authorization checked

### Performance
- [ ] No N+1 queries
- [ ] Appropriate indexes used
- [ ] No memory leaks (event listeners cleaned up)
- [ ] Large lists virtualized

### Maintainability
- [ ] Code is readable and self-documenting
- [ ] Complex logic has comments
- [ ] No duplicate code
- [ ] Functions are single-purpose

### Testing
- [ ] Unit tests added for new logic
- [ ] Edge cases tested
- [ ] Tests are deterministic (no flaky tests)
- [ ] Mocks are appropriate

## Coverage Strategies

### Minimum Coverage Targets
```javascript
// jest.config.js
module.exports = {
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 80,
      lines: 80,
      statements: 80,
    },
    './src/critical/': {
      branches: 90,
      functions: 95,
      lines: 95,
    },
  },
};
```

### Coverage Commands
```bash
# Generate coverage report
npm test -- --coverage

# View HTML report
open coverage/lcov-report/index.html

# Check specific file
npm test -- --coverage --collectCoverageFrom="src/utils/pricing.ts"
```

## Debugging Techniques

### Systematic Debugging
1. **Reproduce** — Confirm the bug consistently
2. **Isolate** — Narrow down to smallest failing case
3. **Identify** — Find the root cause (not symptoms)
4. **Fix** — Apply minimal, targeted fix
5. **Verify** — Confirm fix and no regressions
6. **Document** — Add test to prevent recurrence

### Debug Logging
```typescript
// Temporary debug logging (remove before commit)
console.log('[DEBUG] Input:', JSON.stringify(input, null, 2));
console.log('[DEBUG] State before:', { ...state });
// ... operation
console.log('[DEBUG] State after:', { ...state });
```

### Binary Search Debugging
```typescript
// Comment out half the code to isolate issue
// If bug persists: problem in remaining half
// If bug disappears: problem in commented half
// Repeat until isolated
```

## Performance Testing

### Load Testing with k6
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 50 },   // Ramp up
    { duration: '3m', target: 50 },   // Steady state
    { duration: '1m', target: 100 },  // Peak
    { duration: '1m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% under 500ms
    http_req_failed: ['rate<0.01'],   // <1% errors
  },
};

export default function () {
  const res = http.get('https://api.example.com/products');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(1);
}
```

## Accessibility Testing

### Automated Checks
```typescript
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

it('should have no accessibility violations', async () => {
  const { container } = render(<LoginForm />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### Manual Checklist
- [ ] Keyboard navigation works (Tab, Enter, Escape)
- [ ] Focus indicators visible
- [ ] Screen reader announces content correctly
- [ ] Color contrast meets WCAG AA (4.5:1)
- [ ] Form inputs have associated labels
- [ ] Images have alt text
- [ ] Error messages are announced

## Common Anti-Patterns to Avoid

❌ **Testing implementation details**
```typescript
// Bad: Testing internal state
expect(component.state.isLoading).toBe(true);

// Good: Testing observable behavior
expect(screen.getByRole('progressbar')).toBeInTheDocument();
```

❌ **Flaky tests**
```typescript
// Bad: Time-dependent
expect(Date.now() - startTime).toBeLessThan(100);

// Good: Mock time
jest.useFakeTimers();
```

❌ **Test interdependence**
```typescript
// Bad: Tests share state
let counter = 0;
it('test 1', () => { counter++; });
it('test 2', () => { expect(counter).toBe(1); }); // Depends on test 1

// Good: Isolated tests
beforeEach(() => { counter = 0; });
```

❌ **Over-mocking**
```typescript
// Bad: Mock everything
jest.mock('../db');
jest.mock('../cache');
jest.mock('../utils');
// Test proves nothing

// Good: Mock boundaries only
jest.mock('../externalPaymentApi');
```

## CI/CD Integration

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm test -- --coverage
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info
```
