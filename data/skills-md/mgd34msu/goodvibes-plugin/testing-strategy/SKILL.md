---
name: testing-strategy
description: "Load PROACTIVELY when task involves writing tests, improving coverage, or test infrastructure. Use when user says \"add tests\", \"write unit tests\", \"set up E2E testing\", \"improve coverage\", or \"add mocks\". Covers Vitest/Jest unit tests, React Testing Library component tests, Playwright E2E tests, MSW API mocking, test organization and naming, fixture management, coverage targets and thresholds, snapshot testing, and CI integration."
metadata:
  version: "1.0.0"
  category: outcome
  tags: [testing, vitest, jest, playwright, coverage, tdd]
---

## Resources
```
scripts/
  validate-tests.sh
references/
  testing-patterns.md
```

# Testing Strategy

This skill guides you through implementing comprehensive testing strategies using modern testing frameworks and GoodVibes precision tools. Use this workflow when adding tests to existing code, setting up test infrastructure, or achieving coverage goals.

## When to Use This Skill

- Setting up test infrastructure (Vitest, Jest, Playwright)
- Writing unit tests for functions, hooks, and utilities
- Creating component tests with React Testing Library
- Implementing E2E tests with Playwright
- Adding API mocking with MSW
- Improving test coverage
- Configuring CI test pipelines
- Debugging flaky tests
- Creating test fixtures and factories

## Test Organization

### File Naming Conventions

Follow consistent naming patterns:

```typescript
// Co-located pattern (recommended)
src/
  components/
    Button.tsx
    Button.test.tsx          // Component tests
  utils/
    formatDate.ts
    formatDate.test.ts       // Unit tests
  api/
    users.ts
    users.integration.test.ts // Integration tests

// Centralized pattern (alternative)
__tests__/
  components/
    Button.test.tsx
  utils/
    formatDate.test.ts
```

### Test Suite Structure

Organize tests with clear describe blocks:

```typescript
import { describe, it, expect, beforeEach } from 'vitest';
import { formatDate } from './formatDate';

describe('formatDate', () => {
  describe('with valid dates', () => {
    it('formats ISO dates to MM/DD/YYYY', () => {
      expect(formatDate('2024-01-15')).toBe('01/15/2024');
    });

    it('handles Date objects', () => {
      const date = new Date('2024-01-15');
      expect(formatDate(date)).toBe('01/15/2024');
    });
  });

  describe('with invalid dates', () => {
    it('throws for invalid strings', () => {
      expect(() => formatDate('invalid')).toThrow('Invalid date');
    });

    it('throws for null', () => {
      expect(() => formatDate(null)).toThrow('Invalid date');
    });
  });
});
```

### Discovery: Finding Test Files

Use precision tools to discover existing test patterns:

```yaml
# Find all test files and analyze patterns
discover:
  queries:
    - id: test-files
      type: glob
      patterns:
        - "**/*.test.{ts,tsx,js,jsx}"
        - "**/*.spec.{ts,tsx,js,jsx}"
        - "e2e/**/*.spec.ts"
      exclude:
        - "**/node_modules/**"
        - "**/dist/**"
    - id: test-config
      type: glob
      patterns:
        - "vitest.config.ts"
        - "jest.config.js"
        - "playwright.config.ts"
    - id: skipped-tests
      type: grep
      pattern: "\\.skip|it\\.only|describe\\.only"
      glob: "**/*.test.{ts,tsx}"
  output_mode: files_only
```

## Unit Testing

### Vitest Setup (Recommended)

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'src/test/',
        '**/*.d.ts',
        '**/*.config.*',
        '**/dist/**',
      ],
      all: true,
      lines: 80,
      functions: 80,
      branches: 80,
      statements: 80,
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

### Testing Pure Functions

```typescript
import { describe, it, expect } from 'vitest';
import { calculateTotal, discountPrice } from './pricing';

describe('pricing utilities', () => {
  describe('calculateTotal', () => {
    it('sums item prices', () => {
      const items = [
        { price: 10.00, quantity: 2 },
        { price: 5.50, quantity: 1 },
      ];
      expect(calculateTotal(items)).toBe(25.50);
    });

    it('returns 0 for empty array', () => {
      expect(calculateTotal([])).toBe(0);
    });

    it('handles quantity multipliers', () => {
      const items = [{ price: 10, quantity: 3 }];
      expect(calculateTotal(items)).toBe(30);
    });
  });

  describe('discountPrice', () => {
    it('applies percentage discount', () => {
      expect(discountPrice(100, 0.2)).toBe(80);
    });

    it('rounds to 2 decimal places', () => {
      expect(discountPrice(10.99, 0.15)).toBe(9.34);
    });

    it('throws for invalid discounts', () => {
      expect(() => discountPrice(100, -0.1)).toThrow('Invalid discount');
      expect(() => discountPrice(100, 1.5)).toThrow('Invalid discount');
    });
  });
});
```

### Testing React Hooks

```typescript
import { renderHook, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useAuth } from './useAuth';

// Mock the auth context
vi.mock('@/contexts/AuthContext', () => ({
  useAuthContext: vi.fn(),
}));

describe('useAuth', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('returns user when authenticated', () => {
    vi.mocked(useAuthContext).mockReturnValue({
      user: { id: '1', email: 'test@example.com' },
      isLoading: false,
    });

    const { result } = renderHook(() => useAuth());
    
    expect(result.current.user).toEqual({
      id: '1',
      email: 'test@example.com',
    });
    expect(result.current.isAuthenticated).toBe(true);
  });

  it('handles loading state', () => {
    vi.mocked(useAuthContext).mockReturnValue({
      user: null,
      isLoading: true,
    });

    const { result } = renderHook(() => useAuth());
    
    expect(result.current.isLoading).toBe(true);
    expect(result.current.isAuthenticated).toBe(false);
  });

  it('refetches user on login', async () => {
    const refetch = vi.fn().mockResolvedValue({ id: '1' });
    vi.mocked(useAuthContext).mockReturnValue({
      user: null,
      refetch,
    });

    const { result } = renderHook(() => useAuth());
    
    await result.current.login('test@example.com', 'password');
    
    expect(refetch).toHaveBeenCalledOnce();
  });
});
```

## Component Testing

### React Testing Library Patterns

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import { Button } from './Button';
import { SearchInput } from './SearchInput';

describe('Button', () => {
  it('renders with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
  });

  it('calls onClick when clicked', async () => {
    const handleClick = vi.fn();
    const user = userEvent.setup();
    
    render(<Button onClick={handleClick}>Click</Button>);
    await user.click(screen.getByRole('button'));
    
    expect(handleClick).toHaveBeenCalledOnce();
  });

  it('disables button when loading', () => {
    render(<Button isLoading>Submit</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });

  it('shows spinner when loading', () => {
    render(<Button isLoading>Submit</Button>);
    expect(screen.getByRole('button')).toHaveAttribute('aria-busy', 'true');
  });

  it('applies variant styles', () => {
    const { container } = render(<Button variant="primary">Primary</Button>);
    expect(container.firstChild).toHaveClass('bg-blue-600');
  });
});

describe('SearchInput', () => {
  it('debounces search input', async () => {
    const onSearch = vi.fn();
    const user = userEvent.setup();
    
    render(<SearchInput onSearch={onSearch} debounce={300} />);
    const input = screen.getByRole('searchbox');
    
    await user.type(input, 'test query');
    
    // Should not call immediately
    expect(onSearch).not.toHaveBeenCalled();
    
    // Should call after debounce
    await waitFor(
      () => expect(onSearch).toHaveBeenCalledWith('test query'),
      { timeout: 500 }
    );
  });

  it('clears input on clear button click', async () => {
    const user = userEvent.setup();
    
    render(<SearchInput />);
    const input = screen.getByRole('searchbox') as HTMLInputElement;
    
    await user.type(input, 'test');
    expect(input.value).toBe('test');
    
    await user.click(screen.getByRole('button', { name: /clear/i }));
    expect(input.value).toBe('');
  });
});
```

### Testing Async Components

```typescript
import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { UserProfile } from './UserProfile';
import * as api from '@/api/users';

vi.mock('@/api/users');

describe('UserProfile', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('shows loading state initially', () => {
    vi.mocked(api.getUser).mockReturnValue(new Promise(() => {}));
    
    render(<UserProfile userId="1" />);
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it('displays user data when loaded', async () => {
    vi.mocked(api.getUser).mockResolvedValue({
      id: '1',
      name: 'John Doe',
      email: 'john@example.com',
    });
    
    render(<UserProfile userId="1" />);
    
    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument();
    });
    
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
  });

  it('shows error message on fetch failure', async () => {
    vi.mocked(api.getUser).mockRejectedValue(new Error('Failed to fetch'));
    
    render(<UserProfile userId="1" />);
    
    await waitFor(() => {
      expect(screen.getByText(/failed to load/i)).toBeInTheDocument();
    });
  });
});
```

## Integration Testing

### API Route Testing

```typescript
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { createMocks } from 'node-mocks-http';
import { POST } from '@/app/api/posts/route';
import { prisma } from '@/lib/prisma';
import { createTestUser, cleanupDatabase } from '@/test/helpers';

describe('POST /api/posts', () => {
  let testUser: { id: string; email: string };

  beforeAll(async () => {
    testUser = await createTestUser();
  });

  afterAll(async () => {
    await cleanupDatabase();
  });

  it('creates a new post', async () => {
    const { req } = createMocks({
      method: 'POST',
      body: {
        title: 'Test Post',
        content: 'Test content',
      },
      headers: {
        authorization: `Bearer ${testUser.token}`,
      },
    });

    const response = await POST(req);
    const data = await response.json();

    expect(response.status).toBe(201);
    expect(data).toMatchObject({
      title: 'Test Post',
      content: 'Test content',
      authorId: testUser.id,
    });

    // Verify in database
    const post = await prisma.post.findUnique({
      where: { id: data.id },
    });
    expect(post).toBeTruthy();
  });

  it('validates required fields', async () => {
    const { req } = createMocks({
      method: 'POST',
      body: { title: '' }, // Missing content
      headers: { authorization: `Bearer ${testUser.token}` },
    });

    const response = await POST(req);
    const data = await response.json();

    expect(response.status).toBe(400);
    expect(data.error).toMatchObject({
      fieldErrors: {
        title: expect.arrayContaining([expect.any(String)]),
        content: expect.arrayContaining([expect.any(String)]),
      },
    });
  });

  it('requires authentication', async () => {
    const { req } = createMocks({
      method: 'POST',
      body: { title: 'Test', content: 'Test' },
      // No authorization header
    });

    const response = await POST(req);
    expect(response.status).toBe(401);
  });
});
```

### Database Testing with Fixtures

```typescript
// test/helpers.ts
import { PrismaClient } from '@prisma/client';
import { hash } from 'bcrypt';

export const prisma = new PrismaClient();

export async function createTestUser(overrides = {}) {
  const hashedPassword = await hash('password123', 10);
  
  return prisma.user.create({
    data: {
      email: `test-${Date.now()}@example.com`,
      name: 'Test User',
      password: hashedPassword,
      ...overrides,
    },
  });
}

export async function createTestPost(userId: string, overrides = {}) {
  return prisma.post.create({
    data: {
      title: 'Test Post',
      content: 'Test content',
      authorId: userId,
      published: false,
      ...overrides,
    },
  });
}

export async function cleanupDatabase() {
  // Delete in correct order to respect foreign keys
  await prisma.comment.deleteMany();
  await prisma.post.deleteMany();
  await prisma.user.deleteMany();
}
```

## E2E Testing

### Playwright Setup

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

### Page Object Pattern

```typescript
// e2e/pages/LoginPage.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel('Email');
    this.passwordInput = page.getByLabel('Password');
    this.submitButton = page.getByRole('button', { name: 'Sign in' });
    this.errorMessage = page.getByRole('alert');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async expectError(message: string) {
    // Note: expect is imported from @playwright/test
    await expect(this.errorMessage).toContainText(message);
  }
}

// e2e/auth.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from './pages/LoginPage';

test.describe('Authentication', () => {
  test('successful login redirects to dashboard', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('test@example.com', 'password123');
    
    await expect(page).toHaveURL('/dashboard');
    await expect(page.getByText('Welcome back')).toBeVisible();
  });

  test('invalid credentials show error', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('invalid@example.com', 'wrong');
    
    await loginPage.expectError('Invalid email or password');
  });

  test('preserves redirect after login', async ({ page }) => {
    await page.goto('/dashboard');
    await expect(page).toHaveURL(/\/login\?redirect=%2Fdashboard/);
    
    const loginPage = new LoginPage(page);
    await loginPage.login('test@example.com', 'password123');
    
    await expect(page).toHaveURL('/dashboard');
  });
});
```

## Mocking Patterns

### MSW for API Mocking

```typescript
// src/test/mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/user', () => {
    return HttpResponse.json({
      id: '1',
      email: 'test@example.com',
      name: 'Test User',
    });
  }),

  http.post('/api/posts', async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json(
      {
        id: '1',
        ...body,
        createdAt: new Date().toISOString(),
      },
      { status: 201 }
    );
  }),

  http.get('/api/posts/:id', ({ params }) => {
    const { id } = params;
    
    if (id === '404') {
      return new HttpResponse(null, { status: 404 });
    }
    
    return HttpResponse.json({
      id,
      title: 'Test Post',
      content: 'Test content',
    });
  }),
];

// src/test/setup.ts
import { beforeAll, afterEach, afterAll } from 'vitest';
import { setupServer } from 'msw/node';
import { handlers } from './mocks/handlers';

const server = setupServer(...handlers);

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### Module Mocking

```typescript
import { vi } from 'vitest';
import type * as PrismaModule from '@/lib/prisma';

// Mock entire module
vi.mock('@/lib/prisma', () => ({
  prisma: {
    user: {
      findUnique: vi.fn(),
      create: vi.fn(),
      update: vi.fn(),
      delete: vi.fn(),
    },
    post: {
      findMany: vi.fn(),
      create: vi.fn(),
    },
  },
}));

// Mock with implementation
vi.mock('@/lib/auth', () => ({
  hashPassword: vi.fn((password: string) => `hashed_${password}`),
  verifyPassword: vi.fn((password: string, hash: string) => {
    return hash === `hashed_${password}`;
  }),
}));

// Partial mock
vi.mock('@/lib/email', async (importOriginal) => {
  const actual = await importOriginal<typeof import('@/lib/email')>();
  return {
    ...actual,
    sendEmail: vi.fn(), // Mock only sendEmail
  };
});
```

## Coverage Strategy

### Target Thresholds

Aim for high coverage on new code:

- **100% on new code** (enforced in CI)
- **80%+ on existing code** (gradual improvement)
- **100% on critical paths** (auth, payment, data integrity)

### Coverage Configuration

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json-summary', 'html'],
      exclude: [
        'node_modules/',
        'src/test/',
        '**/*.d.ts',
        '**/*.config.*',
        '**/dist/**',
        '**/*.stories.tsx', // Storybook
        '**/types/**',
      ],
      all: true,
      lines: 80,
      functions: 80,
      branches: 80,
      statements: 80,
      // Fail CI if coverage drops
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80,
      },
    },
  },
});
```

### Identifying Coverage Gaps

Use precision tools to find untested code:

```yaml
# Find files missing tests
precision_exec:
  commands:
    - cmd: "npm run test:coverage -- --reporter=json-summary"
      expect:
        exit_code: 0

# Parse coverage report
precision_read:
  files:
    - path: "coverage/coverage-summary.json"
  extract: content
  verbosity: minimal

# Find source files without corresponding tests
discover:
  queries:
    - id: source-files
      type: glob
      patterns: ["src/**/*.{ts,tsx}"]
      exclude: ["**/*.test.*", "**/*.spec.*"]
    - id: test-files
      type: glob
      patterns: ["**/*.test.{ts,tsx}"]
  output_mode: files_only
```

## CI Integration

### GitHub Actions Example

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

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
      
      - name: Run unit tests
        run: npm run test:coverage
      
      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage/coverage-final.json
      
      - name: Run E2E tests
        run: npx playwright test
      
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
```

### Parallel Test Execution

```typescript
// vitest.config.ts - parallel by default
export default defineConfig({
  test: {
    pool: 'threads',
    poolOptions: {
      threads: {
        singleThread: false,
        maxThreads: 8,
      },
    },
  },
});

// playwright.config.ts
export default defineConfig({
  workers: process.env.CI ? 1 : 4, // Limit parallelism in CI
  fullyParallel: true,
});
```

## Precision Tool Integration

### Running Tests with Expectations

```yaml
# Run tests and validate output
precision_exec:
  commands:
    - cmd: "npm run test -- --run"
      expect:
        exit_code: 0
    
    - cmd: "npm run typecheck"
      expect:
        exit_code: 0
    
    - cmd: "npm run test:coverage -- --run"
      expect:
        exit_code: 0
        stdout_contains: "All files"
  
  verbosity: minimal
```

### Batch Test Validation

```yaml
batch:
  id: validate-tests
  operations:
    query:
      - id: find-skipped
        type: grep
        pattern: "\\.skip|it\\.only|describe\\.only"
        glob: "**/*.test.ts"
        output:
          format: count_only
    
    exec:
      - id: run-tests
        type: command
        commands:
          - cmd: "npm run test -- --run"
            expect: { exit_code: 0 }
      
      - id: check-coverage
        type: command
        commands:
          - cmd: "npm run test:coverage -- --run"
            expect:
              exit_code: 0
              stdout_contains: "All files"
  
  config:
    execution:
      mode: sequential
```

## Debugging Flaky Tests

### Common Causes

1. **Race conditions**: Use `waitFor` for async operations
2. **Time-dependent tests**: Mock timers with `vi.useFakeTimers()`
3. **Test isolation**: Ensure tests don't share state
4. **Network requests**: Mock with MSW, don't rely on real APIs
5. **Random data**: Use deterministic test data or seed random generators

### Flaky Test Patterns

```typescript
import { vi, beforeEach, afterEach } from 'vitest';

// Mock timers for time-dependent code
beforeEach(() => {
  vi.useFakeTimers();
});

afterEach(() => {
  vi.restoreAllMocks();
});

it('debounces function calls', async () => {
  const callback = vi.fn();
  const debounced = debounce(callback, 1000);
  
  debounced('test');
  expect(callback).not.toHaveBeenCalled();
  
  vi.advanceTimersByTime(1000);
  expect(callback).toHaveBeenCalledWith('test');
});

// Ensure test isolation
beforeEach(async () => {
  await cleanupDatabase();
  vi.clearAllMocks();
});

// Use deterministic data
it('sorts users by creation date', () => {
  const users = [
    { id: '1', createdAt: new Date('2024-01-01') },
    { id: '2', createdAt: new Date('2024-01-02') },
  ];
  
  const sorted = sortByDate(users);
  expect(sorted[0].id).toBe('2');
});
```

## Best Practices

1. **Write tests first** (TDD) for new features
2. **Test behavior, not implementation** - focus on what, not how
3. **One assertion per test** when possible for clarity
4. **Use descriptive test names** - "it does X when Y"
5. **Avoid mocking everything** - integration tests need real collaborators
6. **Keep tests fast** - unit tests <100ms, integration <1s
7. **Test edge cases** - null, undefined, empty arrays, boundary values
8. **Don't test framework code** - test your logic, not React/Vue/etc.
9. **Maintain test fixtures** - keep test data realistic and up-to-date
10. **Review test coverage** - 100% coverage doesn't mean bug-free

## Common Anti-Patterns

### [X] Testing Implementation Details

```typescript
// BAD - tests internal state
it('sets loading to true', () => {
  const { result } = renderHook(() => useUsers());
  expect(result.current.loading).toBe(true);
});

// GOOD - tests user-visible behavior
it('shows loading spinner while fetching', () => {
  render(<UserList />);
  expect(screen.getByRole('status')).toBeInTheDocument();
});
```

### [X] Overmocking

```typescript
// BAD - mocks everything, tests nothing
vi.mock('./api');
vi.mock('./utils');
vi.mock('./hooks');

// GOOD - mock only external dependencies
vi.mock('axios'); // Mock HTTP client
// Let your code run for real
```

### [X] Brittle Selectors

```typescript
// BAD - breaks when styling changes
const button = container.querySelector('.btn-primary');

// GOOD - uses accessible queries
const button = screen.getByRole('button', { name: /submit/i });
```

## Summary

Effective testing requires:

- **Organized test files** co-located with source code
- **Comprehensive unit tests** for business logic and utilities
- **User-centric component tests** with React Testing Library
- **Realistic integration tests** for API routes and database operations
- **End-to-end tests** for critical user flows
- **API mocking** with MSW for deterministic tests
- **High coverage targets** (100% on new code, 80%+ overall)
- **CI integration** with parallel execution and coverage reporting
- **Flaky test prevention** through proper mocking and isolation

Use precision tools to discover test gaps, run tests efficiently, and validate implementation quality.
