---
name: javascript-testing-patterns
description: "Implement comprehensive testing strategies using Jest, Vitest, and Testing Library for unit tests, integration tests, and end-to-end testing with mocking, fixtures, and test-driven development. Use when writing JavaScript/TypeScript tests, setting up test infrastructure, or implementing TDD/BDD workflows."
layer: 3
tech_stack: [typescript, javascript, jest, vitest]
topics: [jest, vitest, testing-library, mocking, tdd, react-testing]
depends_on: [modern-javascript-patterns]
complements: [e2e-testing-patterns]
keywords: [Jest, Vitest, describe, it, expect, mock, render, screen, fireEvent]
---

# JavaScript Testing Patterns

Comprehensive testing strategies for JavaScript/TypeScript applications.

## Framework Setup

### Jest Configuration

```typescript
// jest.config.ts
import type { Config } from 'jest';

const config: Config = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src'],
  testMatch: ['**/__tests__/**/*.ts', '**/?(*.)+(spec|test).ts'],
  collectCoverageFrom: ['src/**/*.ts', '!src/**/*.d.ts'],
  coverageThreshold: {
    global: { branches: 80, functions: 80, lines: 80, statements: 80 },
  },
  setupFilesAfterEnv: ['<rootDir>/src/test/setup.ts'],
};

export default config;
```

### Vitest Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
    },
    setupFiles: ['./src/test/setup.ts'],
  },
});
```

## Unit Testing Patterns

### Testing Pure Functions

```typescript
import { describe, it, expect } from 'vitest';

describe('Calculator', () => {
  describe('add', () => {
    it('should add two positive numbers', () => {
      expect(add(2, 3)).toBe(5);
    });

    it('should handle zero', () => {
      expect(add(0, 5)).toBe(5);
    });
  });

  describe('divide', () => {
    it('should throw error when dividing by zero', () => {
      expect(() => divide(10, 0)).toThrow('Division by zero');
    });
  });
});
```

### Testing Classes

```typescript
describe('UserService', () => {
  let service: UserService;

  beforeEach(() => {
    service = new UserService();
  });

  describe('create', () => {
    it('should create a new user', () => {
      const user = { id: '1', name: 'John', email: 'john@example.com' };
      const created = service.create(user);

      expect(created).toEqual(user);
      expect(service.findById('1')).toEqual(user);
    });

    it('should throw error if user already exists', () => {
      const user = { id: '1', name: 'John', email: 'john@example.com' };
      service.create(user);
      expect(() => service.create(user)).toThrow('User already exists');
    });
  });
});
```

### Testing Async Functions

```typescript
describe('ApiService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should fetch user successfully', async () => {
    const mockUser = { id: '1', name: 'John' };
    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => mockUser,
    });

    const user = await service.fetchUser('1');

    expect(user).toEqual(mockUser);
    expect(fetch).toHaveBeenCalledWith('https://api.example.com/users/1');
  });

  it('should throw error if user not found', async () => {
    global.fetch = vi.fn().mockResolvedValueOnce({ ok: false });
    await expect(service.fetchUser('999')).rejects.toThrow('User not found');
  });
});
```

## Mocking Patterns

### Mocking Modules

```typescript
vi.mock('nodemailer', () => ({
  default: {
    createTransport: vi.fn(() => ({
      sendMail: vi.fn().mockResolvedValue({ messageId: '123' }),
    })),
  },
}));
```

### Dependency Injection

```typescript
describe('UserService', () => {
  let service: UserService;
  let mockRepository: IUserRepository;

  beforeEach(() => {
    mockRepository = {
      findById: vi.fn(),
      create: vi.fn(),
    };
    service = new UserService(mockRepository);
  });

  it('should return user if found', async () => {
    const mockUser = { id: '1', name: 'John' };
    vi.mocked(mockRepository.findById).mockResolvedValue(mockUser);

    const user = await service.getUser('1');

    expect(user).toEqual(mockUser);
    expect(mockRepository.findById).toHaveBeenCalledWith('1');
  });
});
```

### Spying on Functions

```typescript
let loggerSpy: any;

beforeEach(() => {
  loggerSpy = vi.spyOn(logger, 'info');
});

afterEach(() => {
  loggerSpy.mockRestore();
});

it('should log order processing', async () => {
  await service.processOrder('123');
  expect(loggerSpy).toHaveBeenCalledWith('Processing order 123');
});
```

## React Component Testing

```typescript
import { render, screen, fireEvent } from '@testing-library/react';

describe('UserForm', () => {
  it('should render form inputs', () => {
    render(<UserForm onSubmit={vi.fn()} />);

    expect(screen.getByPlaceholderText('Name')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Submit' })).toBeInTheDocument();
  });

  it('should call onSubmit with form data', () => {
    const onSubmit = vi.fn();
    render(<UserForm onSubmit={onSubmit} />);

    fireEvent.change(screen.getByTestId('name-input'), {
      target: { value: 'John Doe' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Submit' }));

    expect(onSubmit).toHaveBeenCalledWith({ name: 'John Doe' });
  });
});
```

## Testing Hooks

```typescript
import { renderHook, act } from '@testing-library/react';

describe('useCounter', () => {
  it('should increment count', () => {
    const { result } = renderHook(() => useCounter());

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });
});
```

## Test Fixtures

```typescript
import { faker } from '@faker-js/faker';

export function createUserFixture(overrides?: Partial<User>): User {
  return {
    id: faker.string.uuid(),
    name: faker.person.fullName(),
    email: faker.internet.email(),
    ...overrides,
  };
}
```

## Best Practices

1. **AAA Pattern** - Arrange, Act, Assert
2. **One assertion per test** - Or logically related assertions
3. **Descriptive test names** - Describe what is being tested
4. **Use beforeEach/afterEach** - For setup and teardown
5. **Mock external dependencies** - Keep tests isolated
6. **Test edge cases** - Not just happy paths
7. **Avoid implementation details** - Test behavior
8. **Keep tests fast** - Mock slow operations
9. **Maintain 80%+ coverage** - Aim high
10. **Clean up after tests** - Prevent pollution

## Common Patterns

```typescript
// Testing promises
await expect(service.fetchUser('invalid')).rejects.toThrow('Not found');

// Testing timers
vi.useFakeTimers();
vi.advanceTimersByTime(1000);
vi.useRealTimers();

// Snapshot testing
expect(container.firstChild).toMatchSnapshot();
```

## Detailed References

For comprehensive patterns, see:
- [references/integration-testing.md](references/integration-testing.md)
- [references/react-testing-patterns.md](references/react-testing-patterns.md)
- [references/mocking-strategies.md](references/mocking-strategies.md)

## Resources

- **Jest**: https://jestjs.io/
- **Vitest**: https://vitest.dev/
- **Testing Library**: https://testing-library.com/
