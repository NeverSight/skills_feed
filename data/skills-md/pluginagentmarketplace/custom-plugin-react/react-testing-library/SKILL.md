---
name: react-testing-library
description: Write production-grade React tests with Testing Library, MSW, and comprehensive coverage patterns
sasmp_version: "2.0.0"
bonded_agent: 07-testing-deployment
bond_type: PRIMARY_BOND
input_validation:
  required_packages:
    - "@testing-library/react": ">=14.0.0"
    - "@testing-library/user-event": ">=14.0.0"
    - "msw": ">=2.0.0"
output_format:
  code_examples: jsx
  coverage_target: 80
error_handling:
  patterns:
    - retry_flaky
    - async_waitfor
    - mock_error_states
observability:
  logging: jest_console
  metrics: ["test_duration", "coverage"]
---

# React Testing Library Skill

## Overview
Master React Testing Library for writing maintainable tests that focus on user behavior rather than implementation details.

## Learning Objectives
- Write component tests with RTL
- Test user interactions
- Handle async operations
- Test hooks and context
- Follow testing best practices

## Quick Start

### Installation
```bash
npm install --save-dev @testing-library/react @testing-library/jest-dom @testing-library/user-event
```

### Setup
```javascript
// setupTests.js
import '@testing-library/jest-dom';
```

## Basic Component Testing

```jsx
// Button.test.jsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Button from './Button';

describe('Button', () => {
  it('renders button text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
  });

  it('calls onClick when clicked', async () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);

    await userEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

## Queries

### Priority Order
```jsx
// 1. Accessible queries (preferred)
screen.getByRole('button', { name: /submit/i });
screen.getByLabelText('Email');
screen.getByPlaceholderText('Enter email');
screen.getByText('Welcome');

// 2. Semantic queries
screen.getByAltText('Profile picture');
screen.getByTitle('Close');

// 3. Test IDs (last resort)
screen.getByTestId('custom-element');
```

### Query Variants
```jsx
// getBy - throws error if not found
screen.getByText('Hello');

// queryBy - returns null if not found
screen.queryByText('Hello'); // Use for asserting non-existence

// findBy - async, waits for element
await screen.findByText('Hello'); // Use for async content
```

## Testing Forms

```jsx
// LoginForm.test.jsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import LoginForm from './LoginForm';

describe('LoginForm', () => {
  it('submits form with correct data', async () => {
    const handleSubmit = jest.fn();
    render(<LoginForm onSubmit={handleSubmit} />);

    await userEvent.type(screen.getByLabelText(/email/i), 'test@example.com');
    await userEvent.type(screen.getByLabelText(/password/i), 'password123');
    await userEvent.click(screen.getByRole('button', { name: /login/i }));

    expect(handleSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123'
    });
  });

  it('shows validation errors', async () => {
    render(<LoginForm onSubmit={jest.fn()} />);

    await userEvent.click(screen.getByRole('button', { name: /login/i }));

    expect(await screen.findByText(/email is required/i)).toBeInTheDocument();
  });
});
```

## Testing Async Operations

```jsx
// UserProfile.test.jsx
import { render, screen, waitFor } from '@testing-library/react';
import { rest } from 'msw';
import { setupServer } from 'msw/node';
import UserProfile from './UserProfile';

const server = setupServer(
  rest.get('/api/users/:userId', (req, res, ctx) => {
    return res(ctx.json({ id: 1, name: 'John Doe' }));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('UserProfile', () => {
  it('loads and displays user data', async () => {
    render(<UserProfile userId={1} />);

    expect(screen.getByText(/loading/i)).toBeInTheDocument();

    expect(await screen.findByText('John Doe')).toBeInTheDocument();
    expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
  });

  it('handles API errors', async () => {
    server.use(
      rest.get('/api/users/:userId', (req, res, ctx) => {
        return res(ctx.status(500));
      })
    );

    render(<UserProfile userId={1} />);

    expect(await screen.findByText(/error/i)).toBeInTheDocument();
  });
});
```

## Testing Hooks

```jsx
// useCounter.test.js
import { renderHook, act } from '@testing-library/react';
import useCounter from './useCounter';

describe('useCounter', () => {
  it('increments counter', () => {
    const { result } = renderHook(() => useCounter());

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });

  it('resets to initial value', () => {
    const { result } = renderHook(() => useCounter(10));

    act(() => {
      result.current.increment();
      result.current.reset();
    });

    expect(result.current.count).toBe(10);
  });
});
```

## Testing Context

```jsx
// ThemeToggle.test.jsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ThemeProvider } from './ThemeContext';
import ThemeToggle from './ThemeToggle';

describe('ThemeToggle', () => {
  it('toggles theme', async () => {
    render(
      <ThemeProvider>
        <ThemeToggle />
      </ThemeProvider>
    );

    expect(screen.getByText(/current theme: light/i)).toBeInTheDocument();

    await userEvent.click(screen.getByRole('button'));

    expect(screen.getByText(/current theme: dark/i)).toBeInTheDocument();
  });
});
```

## Custom Render Utility

```jsx
// test-utils.jsx
import { render } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider } from './ThemeContext';

function AllProviders({ children }) {
  return (
    <BrowserRouter>
      <ThemeProvider>
        {children}
      </ThemeProvider>
    </BrowserRouter>
  );
}

function customRender(ui, options) {
  return render(ui, { wrapper: AllProviders, ...options });
}

export * from '@testing-library/react';
export { customRender as render };
```

## Best Practices

1. **Test user behavior, not implementation**
2. **Use accessible queries (role, label)**
3. **Avoid testing internal state**
4. **Use userEvent for realistic interactions**
5. **Mock external dependencies (API calls)**
6. **Test error states and edge cases**
7. **Keep tests simple and focused**

## Common Patterns

```jsx
// Wait for element to disappear
await waitFor(() => {
  expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
});

// Wait for multiple elements
await waitFor(() => {
  expect(screen.getAllByRole('listitem')).toHaveLength(3);
});

// Debugging
screen.debug(); // Print DOM
screen.logTestingPlaygroundURL(); // Get Testing Playground URL
```

## Practice Exercises

1. Test form validation
2. Test async data fetching
3. Test user authentication flow
4. Test routing navigation
5. Test modal interactions
6. Test list filtering
7. Test error boundaries

## Resources

- [React Testing Library Docs](https://testing-library.com/react)
- [Testing Library Queries](https://testing-library.com/docs/queries/about)
- [Common Mistakes](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)

---

## Flaky Test Prevention

```jsx
// Configure Jest retry for CI
// jest.config.js
module.exports = {
  testRetry: process.env.CI ? 2 : 0,
  testTimeout: 10000,
};

// Robust async pattern
it('handles async operations reliably', async () => {
  render(<AsyncComponent />);

  // Use findBy for async content
  expect(await screen.findByText(/loaded/i, {}, { timeout: 5000 }))
    .toBeInTheDocument();

  // Ensure loading is gone
  await waitFor(() => {
    expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
  });
});
```

## MSW 2.0 Setup

```jsx
// mocks/handlers.js
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/users', () => {
    return HttpResponse.json([{ id: 1, name: 'John' }]);
  }),

  http.post('/api/users', async ({ request }) => {
    const user = await request.json();
    return HttpResponse.json({ ...user, id: Date.now() }, { status: 201 });
  }),

  // Error simulation
  http.get('/api/error', () => {
    return HttpResponse.json({ message: 'Server Error' }, { status: 500 });
  }),
];
```

## Coverage Configuration

```javascript
// jest.config.js
module.exports = {
  collectCoverageFrom: ['src/**/*.{js,jsx,ts,tsx}', '!src/**/*.d.ts'],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
};
```

---

**Version**: 2.0.0
**Last Updated**: 2025-12-30
**SASMP Version**: 2.0.0
**Difficulty**: Intermediate
**Estimated Time**: 2-3 weeks
**Prerequisites**: React Fundamentals, Jest Basics
**Changelog**: Added MSW 2.0, flaky test prevention, and coverage config
