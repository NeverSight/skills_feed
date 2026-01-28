---
name: jest-react-testing
description: Comprehensive React component testing with Jest and React Testing Library covering configuration, mocking strategies, async testing patterns, hooks testing, and integration testing best practices
---

# Jest React Testing

A comprehensive skill for testing React applications using Jest and React Testing Library. This skill covers everything from basic component testing to advanced patterns including mocking, async testing, custom hooks testing, and integration testing strategies.

## When to Use This Skill

Use this skill when:

- Testing React components with Jest and React Testing Library
- Setting up Jest configuration for React projects
- Writing unit tests for components, hooks, and utilities
- Testing user interactions and component behavior
- Mocking modules, functions, API calls, and external dependencies
- Testing asynchronous operations (API calls, timers, promises)
- Testing custom React hooks
- Writing integration tests for complex component trees
- Debugging failing tests or improving test coverage
- Following testing best practices and patterns

## Core Concepts

### Testing Philosophy

React Testing Library follows these guiding principles:

- **Test User Behavior, Not Implementation**: Write tests that resemble how users interact with your app
- **Accessibility First**: Use queries that promote accessible components (getByRole, getByLabelText)
- **Avoid Testing Implementation Details**: Don't test state, props, or internal methods directly
- **Maintainable Tests**: Tests should break when behavior changes, not when code refactors
- **Confidence Over Coverage**: Focus on tests that give confidence, not 100% coverage

### Key Testing Concepts

1. **Queries**: Methods to find elements (getBy, queryBy, findBy)
2. **User Events**: Simulating user interactions (click, type, select)
3. **Async Testing**: Testing components with asynchronous operations
4. **Mocking**: Replacing dependencies with controlled test doubles
5. **Assertions**: Verifying expected outcomes with matchers

## Jest Configuration

### Basic Jest Configuration

**jest.config.js** (JavaScript projects):
```javascript
/** @type {import('jest').Config} */
const config = {
  // Test environment for DOM testing
  testEnvironment: 'jsdom',

  // Setup files after environment
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.js'],

  // Module paths
  moduleDirectories: ['node_modules', 'src'],

  // Transform files with babel-jest
  transform: {
    '^.+\\.(js|jsx)$': 'babel-jest',
  },

  // Module name mapper for static assets and CSS
  moduleNameMapper: {
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
    '\\.(jpg|jpeg|png|gif|svg)$': '<rootDir>/__mocks__/fileMock.js',
  },

  // Coverage configuration
  collectCoverageFrom: [
    'src/**/*.{js,jsx}',
    '!src/index.js',
    '!src/**/*.test.{js,jsx}',
    '!src/**/__tests__/**',
  ],

  // Coverage thresholds
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
};

module.exports = config;
```

**jest.config.js** (TypeScript projects):
```typescript
import type {Config} from 'jest';

const config: Config = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.ts'],

  moduleDirectories: ['node_modules', 'src'],

  transform: {
    '^.+\\.tsx?$': 'ts-jest',
  },

  moduleNameMapper: {
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
    '\\.(jpg|jpeg|png|gif|svg)$': '<rootDir>/__mocks__/fileMock.ts',
    '^@/(.*)$': '<rootDir>/src/$1',
  },

  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/index.tsx',
    '!src/**/*.test.{ts,tsx}',
    '!src/**/__tests__/**',
    '!src/**/*.d.ts',
  ],

  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
};

export default config;
```

### Setup Files

**src/setupTests.js**:
```javascript
// Add custom jest matchers from jest-dom
import '@testing-library/jest-dom';

// Extend expect with jest-extended matchers (optional)
import * as matchers from 'jest-extended';
expect.extend(matchers);

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(),
    removeListener: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

// Mock IntersectionObserver
global.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  takeRecords() {
    return [];
  }
  unobserve() {}
};

// Suppress console errors in tests (optional)
const originalError = console.error;
beforeAll(() => {
  console.error = (...args) => {
    if (
      typeof args[0] === 'string' &&
      args[0].includes('Warning: ReactDOM.render')
    ) {
      return;
    }
    originalError.call(console, ...args);
  };
});

afterAll(() => {
  console.error = originalError;
});

// Reset mocks after each test
afterEach(() => {
  jest.clearAllMocks();
});
```

### File Mocks

**__mocks__/fileMock.js**:
```javascript
module.exports = 'test-file-stub';
```

**__mocks__/styleMock.js**:
```javascript
module.exports = {};
```

## React Testing Library Queries

### Query Types

React Testing Library provides three types of queries:

1. **getBy**: Returns element or throws error (use for elements that should exist)
2. **queryBy**: Returns element or null (use for elements that may not exist)
3. **findBy**: Returns promise that resolves to element (use for async elements)

### Query Priority

**Recommended Query Order** (accessibility-focused):

1. **getByRole**: Most accessible query
   ```javascript
   getByRole('button', { name: /submit/i })
   getByRole('heading', { level: 1 })
   getByRole('textbox', { name: /username/i })
   ```

2. **getByLabelText**: For form fields with labels
   ```javascript
   getByLabelText(/email address/i)
   getByLabelText('Password')
   ```

3. **getByPlaceholderText**: For inputs with placeholders
   ```javascript
   getByPlaceholderText(/search/i)
   ```

4. **getByText**: For non-interactive elements with text
   ```javascript
   getByText(/welcome/i)
   getByText('Error: Invalid credentials')
   ```

5. **getByDisplayValue**: For form elements with values
   ```javascript
   getByDisplayValue('John Doe')
   ```

6. **getByAltText**: For images with alt text
   ```javascript
   getByAltText(/profile picture/i)
   ```

7. **getByTitle**: For elements with title attribute
   ```javascript
   getByTitle(/close/i)
   ```

8. **getByTestId**: Last resort when other queries don't work
   ```javascript
   getByTestId('custom-element')
   ```

### Query Variants

```javascript
// Single element queries
screen.getByRole('button')      // Throws if not found or multiple found
screen.queryByRole('button')    // Returns null if not found
await screen.findByRole('button') // Async, waits up to 1000ms

// Multiple element queries
screen.getAllByRole('listitem')      // Throws if none found
screen.queryAllByRole('listitem')    // Returns [] if none found
await screen.findAllByRole('listitem') // Async version
```

## Component Testing Strategies

### Basic Component Test

```javascript
import { render, screen } from '@testing-library/react';
import { Greeting } from './Greeting';

describe('Greeting Component', () => {
  it('renders greeting message', () => {
    render(<Greeting name="Alice" />);

    expect(screen.getByText(/hello, alice/i)).toBeInTheDocument();
  });

  it('renders default greeting when no name provided', () => {
    render(<Greeting />);

    expect(screen.getByText(/hello, guest/i)).toBeInTheDocument();
  });
});
```

### Testing User Interactions

```javascript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Counter } from './Counter';

describe('Counter Component', () => {
  it('increments counter on button click', async () => {
    const user = userEvent.setup();
    render(<Counter />);

    const button = screen.getByRole('button', { name: /increment/i });
    const count = screen.getByText(/count: 0/i);

    expect(count).toBeInTheDocument();

    await user.click(button);

    expect(screen.getByText(/count: 1/i)).toBeInTheDocument();
  });

  it('decrements counter on button click', async () => {
    const user = userEvent.setup();
    render(<Counter initialCount={5} />);

    const decrementBtn = screen.getByRole('button', { name: /decrement/i });

    await user.click(decrementBtn);

    expect(screen.getByText(/count: 4/i)).toBeInTheDocument();
  });
});
```

### Testing Forms

```javascript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { LoginForm } from './LoginForm';

describe('LoginForm Component', () => {
  it('submits form with username and password', async () => {
    const user = userEvent.setup();
    const handleSubmit = jest.fn();

    render(<LoginForm onSubmit={handleSubmit} />);

    const usernameInput = screen.getByLabelText(/username/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /submit/i });

    await user.type(usernameInput, 'testuser');
    await user.type(passwordInput, 'password123');
    await user.click(submitButton);

    expect(handleSubmit).toHaveBeenCalledTimes(1);
    expect(handleSubmit).toHaveBeenCalledWith({
      username: 'testuser',
      password: 'password123',
    });
  });

  it('shows validation errors for empty fields', async () => {
    const user = userEvent.setup();
    render(<LoginForm onSubmit={jest.fn()} />);

    const submitButton = screen.getByRole('button', { name: /submit/i });

    await user.click(submitButton);

    expect(screen.getByText(/username is required/i)).toBeInTheDocument();
    expect(screen.getByText(/password is required/i)).toBeInTheDocument();
  });
});
```

### Testing Conditional Rendering

```javascript
import { render, screen } from '@testing-library/react';
import { UserProfile } from './UserProfile';

describe('UserProfile Component', () => {
  it('shows loading state when loading', () => {
    render(<UserProfile loading={true} />);

    expect(screen.getByText(/loading/i)).toBeInTheDocument();
    expect(screen.queryByRole('heading')).not.toBeInTheDocument();
  });

  it('shows user data when loaded', () => {
    const user = {
      name: 'John Doe',
      email: 'john@example.com',
    };

    render(<UserProfile loading={false} user={user} />);

    expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
    expect(screen.getByRole('heading', { name: /john doe/i })).toBeInTheDocument();
    expect(screen.getByText(/john@example.com/i)).toBeInTheDocument();
  });

  it('shows error message when error occurs', () => {
    render(<UserProfile loading={false} error="Failed to load user" />);

    expect(screen.getByText(/failed to load user/i)).toBeInTheDocument();
    expect(screen.queryByRole('heading')).not.toBeInTheDocument();
  });
});
```

## Mocking Patterns

### Mocking Modules

**Automatic Mock**:
```javascript
// __mocks__/axios.js
export default {
  get: jest.fn(),
  post: jest.fn(),
  put: jest.fn(),
  delete: jest.fn(),
};
```

**Usage in test**:
```javascript
import axios from 'axios';
import { UserService } from './UserService';

jest.mock('axios');

describe('UserService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('fetches users successfully', async () => {
    const mockUsers = [{ id: 1, name: 'Alice' }];
    axios.get.mockResolvedValue({ data: mockUsers });

    const users = await UserService.getUsers();

    expect(axios.get).toHaveBeenCalledWith('/api/users');
    expect(users).toEqual(mockUsers);
  });

  it('handles fetch error', async () => {
    axios.get.mockRejectedValue(new Error('Network Error'));

    await expect(UserService.getUsers()).rejects.toThrow('Network Error');
  });
});
```

### Mocking Functions

```javascript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Button } from './Button';

describe('Button Component', () => {
  it('calls onClick handler when clicked', async () => {
    const user = userEvent.setup();
    const handleClick = jest.fn();

    render(<Button onClick={handleClick}>Click Me</Button>);

    await user.click(screen.getByRole('button'));

    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('calls onClick with event object', async () => {
    const user = userEvent.setup();
    const handleClick = jest.fn();

    render(<Button onClick={handleClick}>Click Me</Button>);

    await user.click(screen.getByRole('button'));

    expect(handleClick).toHaveBeenCalledWith(
      expect.objectContaining({
        type: 'click',
      })
    );
  });
});
```

### Mocking API Calls with MSW (Mock Service Worker)

**Setup MSW**:
```javascript
// src/mocks/handlers.js
import { rest } from 'msw';

export const handlers = [
  rest.get('/api/users', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json([
        { id: 1, name: 'Alice' },
        { id: 2, name: 'Bob' },
      ])
    );
  }),

  rest.post('/api/users', async (req, res, ctx) => {
    const { name, email } = await req.json();

    return res(
      ctx.status(201),
      ctx.json({
        id: 3,
        name,
        email,
      })
    );
  }),
];
```

**Setup server**:
```javascript
// src/mocks/server.js
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);
```

**Configure in setupTests.js**:
```javascript
import { server } from './mocks/server';

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

**Usage in tests**:
```javascript
import { render, screen, waitFor } from '@testing-library/react';
import { server } from './mocks/server';
import { rest } from 'msw';
import { UserList } from './UserList';

describe('UserList Component', () => {
  it('fetches and displays users', async () => {
    render(<UserList />);

    expect(screen.getByText(/loading/i)).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText(/alice/i)).toBeInTheDocument();
      expect(screen.getByText(/bob/i)).toBeInTheDocument();
    });
  });

  it('handles server error', async () => {
    server.use(
      rest.get('/api/users', (req, res, ctx) => {
        return res(
          ctx.status(500),
          ctx.json({ message: 'Internal Server Error' })
        );
      })
    );

    render(<UserList />);

    await waitFor(() => {
      expect(screen.getByText(/error loading users/i)).toBeInTheDocument();
    });
  });
});
```

### Mocking Context

```javascript
import { render, screen } from '@testing-library/react';
import { AuthContext } from './AuthContext';
import { ProtectedComponent } from './ProtectedComponent';

const mockAuthContext = (overrides = {}) => ({
  user: { id: 1, name: 'Test User' },
  isAuthenticated: true,
  login: jest.fn(),
  logout: jest.fn(),
  ...overrides,
});

describe('ProtectedComponent', () => {
  it('renders content for authenticated user', () => {
    const contextValue = mockAuthContext();

    render(
      <AuthContext.Provider value={contextValue}>
        <ProtectedComponent />
      </AuthContext.Provider>
    );

    expect(screen.getByText(/welcome, test user/i)).toBeInTheDocument();
  });

  it('renders login prompt for unauthenticated user', () => {
    const contextValue = mockAuthContext({
      user: null,
      isAuthenticated: false,
    });

    render(
      <AuthContext.Provider value={contextValue}>
        <ProtectedComponent />
      </AuthContext.Provider>
    );

    expect(screen.getByText(/please log in/i)).toBeInTheDocument();
  });
});
```

### Mocking Child Components

```javascript
import { render, screen } from '@testing-library/react';
import { ParentComponent } from './ParentComponent';

// Mock the child component
jest.mock('./ChildComponent', () => ({
  ChildComponent: ({ title, onAction }) => (
    <div>
      <h2>{title}</h2>
      <button onClick={onAction}>Mocked Action</button>
    </div>
  ),
}));

describe('ParentComponent', () => {
  it('renders with mocked child', () => {
    render(<ParentComponent />);

    expect(screen.getByText(/mocked action/i)).toBeInTheDocument();
  });
});
```

## Async Testing Patterns

### Testing with waitFor

```javascript
import { render, screen, waitFor } from '@testing-library/react';
import { AsyncComponent } from './AsyncComponent';

describe('AsyncComponent', () => {
  it('loads and displays data', async () => {
    render(<AsyncComponent />);

    expect(screen.getByText(/loading/i)).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText(/data loaded/i)).toBeInTheDocument();
    });
  });

  it('waits for specific condition', async () => {
    render(<AsyncComponent />);

    await waitFor(
      () => {
        expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
      },
      { timeout: 3000 }
    );
  });
});
```

### Testing with findBy Queries

```javascript
import { render, screen } from '@testing-library/react';
import { DataFetcher } from './DataFetcher';

describe('DataFetcher Component', () => {
  it('displays fetched data', async () => {
    render(<DataFetcher />);

    // findBy automatically waits for element to appear
    const heading = await screen.findByRole('heading', { name: /data/i });
    expect(heading).toBeInTheDocument();
  });

  it('handles timeout for missing elements', async () => {
    render(<DataFetcher url="/api/missing" />);

    await expect(
      screen.findByText(/success/i, {}, { timeout: 500 })
    ).rejects.toThrow();
  });
});
```

### Testing Promises

```javascript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { AsyncForm } from './AsyncForm';

describe('AsyncForm Component', () => {
  it('submits form and shows success message', async () => {
    const user = userEvent.setup();
    render(<AsyncForm />);

    const input = screen.getByLabelText(/name/i);
    const submitBtn = screen.getByRole('button', { name: /submit/i });

    await user.type(input, 'John Doe');
    await user.click(submitBtn);

    const successMsg = await screen.findByText(/submitted successfully/i);
    expect(successMsg).toBeInTheDocument();
  });

  it('shows error message on failure', async () => {
    const user = userEvent.setup();
    render(<AsyncForm shouldFail={true} />);

    const submitBtn = screen.getByRole('button', { name: /submit/i });
    await user.click(submitBtn);

    const errorMsg = await screen.findByRole('alert');
    expect(errorMsg).toHaveTextContent(/submission failed/i);
  });
});
```

### Testing with Fake Timers

```javascript
import { render, screen, act } from '@testing-library/react';
import { Timer } from './Timer';

describe('Timer Component', () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  it('updates timer every second', () => {
    render(<Timer />);

    expect(screen.getByText(/0 seconds/i)).toBeInTheDocument();

    act(() => {
      jest.advanceTimersByTime(1000);
    });

    expect(screen.getByText(/1 second/i)).toBeInTheDocument();

    act(() => {
      jest.advanceTimersByTime(3000);
    });

    expect(screen.getByText(/4 seconds/i)).toBeInTheDocument();
  });

  it('cleans up timer on unmount', () => {
    const { unmount } = render(<Timer />);

    const clearIntervalSpy = jest.spyOn(global, 'clearInterval');

    unmount();

    expect(clearIntervalSpy).toHaveBeenCalled();
  });
});
```

## Testing Custom Hooks

### Basic Hook Testing

```javascript
import { renderHook } from '@testing-library/react';
import { useCounter } from './useCounter';

describe('useCounter Hook', () => {
  it('initializes with default value', () => {
    const { result } = renderHook(() => useCounter());

    expect(result.current.count).toBe(0);
  });

  it('initializes with provided value', () => {
    const { result } = renderHook(() => useCounter(10));

    expect(result.current.count).toBe(10);
  });

  it('increments count', () => {
    const { result } = renderHook(() => useCounter());

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });

  it('decrements count', () => {
    const { result } = renderHook(() => useCounter(5));

    act(() => {
      result.current.decrement();
    });

    expect(result.current.count).toBe(4);
  });
});
```

### Testing Hooks with Props

```javascript
import { renderHook } from '@testing-library/react';
import { useFetch } from './useFetch';

describe('useFetch Hook', () => {
  it('fetches data for given URL', async () => {
    const { result } = renderHook(() => useFetch('/api/users'));

    expect(result.current.loading).toBe(true);

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.data).toBeDefined();
    expect(result.current.error).toBeNull();
  });

  it('refetches when URL changes', async () => {
    const { result, rerender } = renderHook(
      ({ url }) => useFetch(url),
      { initialProps: { url: '/api/users' } }
    );

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    const firstData = result.current.data;

    rerender({ url: '/api/posts' });

    await waitFor(() => {
      expect(result.current.data).not.toEqual(firstData);
    });
  });
});
```

### Testing Hooks with Context

```javascript
import { renderHook } from '@testing-library/react';
import { ThemeProvider } from './ThemeContext';
import { useTheme } from './useTheme';

describe('useTheme Hook', () => {
  const wrapper = ({ children }) => (
    <ThemeProvider initialTheme="light">
      {children}
    </ThemeProvider>
  );

  it('returns current theme', () => {
    const { result } = renderHook(() => useTheme(), { wrapper });

    expect(result.current.theme).toBe('light');
  });

  it('toggles theme', () => {
    const { result } = renderHook(() => useTheme(), { wrapper });

    act(() => {
      result.current.toggleTheme();
    });

    expect(result.current.theme).toBe('dark');
  });
});
```

### Testing Async Hooks

```javascript
import { renderHook, waitFor } from '@testing-library/react';
import { useAsyncData } from './useAsyncData';

describe('useAsyncData Hook', () => {
  it('loads data asynchronously', async () => {
    const { result } = renderHook(() => useAsyncData('/api/data'));

    expect(result.current.loading).toBe(true);
    expect(result.current.data).toBeNull();

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.data).toBeDefined();
  });

  it('handles errors', async () => {
    const { result } = renderHook(() => useAsyncData('/api/error'));

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.error).toBeDefined();
    expect(result.current.data).toBeNull();
  });
});
```

## Integration Testing Patterns

### Testing Component Integration

```javascript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { App } from './App';

describe('App Integration', () => {
  it('navigates between pages', async () => {
    const user = userEvent.setup();
    render(<App />);

    expect(screen.getByText(/home page/i)).toBeInTheDocument();

    const aboutLink = screen.getByRole('link', { name: /about/i });
    await user.click(aboutLink);

    expect(screen.getByText(/about page/i)).toBeInTheDocument();
  });

  it('completes full user flow', async () => {
    const user = userEvent.setup();
    render(<App />);

    // Navigate to signup
    await user.click(screen.getByRole('link', { name: /sign up/i }));

    // Fill out form
    await user.type(screen.getByLabelText(/email/i), 'user@example.com');
    await user.type(screen.getByLabelText(/password/i), 'password123');

    // Submit form
    await user.click(screen.getByRole('button', { name: /submit/i }));

    // Verify success
    expect(await screen.findByText(/welcome/i)).toBeInTheDocument();
  });
});
```

### Testing with Router

```javascript
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import userEvent from '@testing-library/user-event';
import { AppRoutes } from './AppRoutes';

const renderWithRouter = (ui, { initialEntries = ['/'] } = {}) => {
  return render(
    <MemoryRouter initialEntries={initialEntries}>
      {ui}
    </MemoryRouter>
  );
};

describe('AppRoutes Integration', () => {
  it('renders home page by default', () => {
    renderWithRouter(<AppRoutes />);

    expect(screen.getByText(/home/i)).toBeInTheDocument();
  });

  it('renders user page at /users/:id', () => {
    renderWithRouter(<AppRoutes />, { initialEntries: ['/users/123'] });

    expect(screen.getByText(/user profile/i)).toBeInTheDocument();
  });

  it('navigates programmatically', async () => {
    const user = userEvent.setup();
    renderWithRouter(<AppRoutes />);

    const navButton = screen.getByRole('button', { name: /go to profile/i });
    await user.click(navButton);

    expect(screen.getByText(/profile page/i)).toBeInTheDocument();
  });
});
```

### Testing with Redux

```javascript
import { render, screen } from '@testing-library/react';
import { Provider } from 'react-redux';
import { configureStore } from '@reduxjs/toolkit';
import userEvent from '@testing-library/user-event';
import { TodoList } from './TodoList';
import todosReducer from './todosSlice';

const createMockStore = (initialState = {}) => {
  return configureStore({
    reducer: {
      todos: todosReducer,
    },
    preloadedState: initialState,
  });
};

const renderWithStore = (ui, { store = createMockStore() } = {}) => {
  return render(<Provider store={store}>{ui}</Provider>);
};

describe('TodoList Integration', () => {
  it('adds new todo', async () => {
    const user = userEvent.setup();
    renderWithStore(<TodoList />);

    const input = screen.getByPlaceholderText(/new todo/i);
    const addButton = screen.getByRole('button', { name: /add/i });

    await user.type(input, 'Buy groceries');
    await user.click(addButton);

    expect(screen.getByText(/buy groceries/i)).toBeInTheDocument();
  });

  it('renders initial todos from store', () => {
    const initialState = {
      todos: {
        items: [
          { id: 1, text: 'Existing todo', completed: false },
        ],
      },
    };

    renderWithStore(<TodoList />, { store: createMockStore(initialState) });

    expect(screen.getByText(/existing todo/i)).toBeInTheDocument();
  });
});
```

## Jest DOM Matchers

### Common Matchers

```javascript
// Element presence
expect(element).toBeInTheDocument();
expect(element).not.toBeInTheDocument();

// Visibility
expect(element).toBeVisible();
expect(element).not.toBeVisible();

// Text content
expect(element).toHaveTextContent('Hello World');
expect(element).toHaveTextContent(/hello/i);

// Attributes
expect(element).toHaveAttribute('type', 'submit');
expect(element).toHaveAttribute('disabled');

// Classes
expect(element).toHaveClass('active');
expect(element).toHaveClass('btn', 'btn-primary');

// Styles
expect(element).toHaveStyle({ color: 'red' });
expect(element).toHaveStyle('display: none');

// Forms
expect(input).toHaveValue('test');
expect(input).toHaveDisplayValue('Test');
expect(checkbox).toBeChecked();
expect(checkbox).not.toBeChecked();
expect(input).toBeDisabled();
expect(input).toBeEnabled();
expect(input).toBeRequired();
expect(input).toBeInvalid();
expect(input).toBeValid();

// Focus
expect(element).toHaveFocus();

// Accessibility
expect(element).toHaveAccessibleName('Submit button');
expect(element).toHaveAccessibleDescription('Click to submit form');

// Contains
expect(container).toContainElement(child);
expect(container).toContainHTML('<span>Text</span>');
```

## Best Practices

### Test Organization

1. **Group Related Tests**: Use `describe` blocks to organize tests
   ```javascript
   describe('UserProfile', () => {
     describe('when loading', () => {
       it('shows loading spinner', () => {});
     });

     describe('when loaded', () => {
       it('displays user information', () => {});
       it('shows profile picture', () => {});
     });
   });
   ```

2. **Use Descriptive Test Names**: Test names should describe behavior
   ```javascript
   // Good
   it('displays error message when login fails', () => {});

   // Bad
   it('test login', () => {});
   ```

3. **Follow AAA Pattern**: Arrange, Act, Assert
   ```javascript
   it('increments counter', async () => {
     // Arrange
     const user = userEvent.setup();
     render(<Counter />);

     // Act
     await user.click(screen.getByRole('button', { name: /increment/i }));

     // Assert
     expect(screen.getByText(/count: 1/i)).toBeInTheDocument();
   });
   ```

### Query Best Practices

1. **Prefer Accessible Queries**: Use getByRole, getByLabelText
2. **Use Screen Queries**: Import from screen instead of destructuring render
3. **Avoid getByTestId**: Use it as last resort only
4. **Use Regular Expressions**: More flexible than exact strings

### Async Testing Best Practices

1. **Use findBy for Async**: Prefer findBy over getBy + waitFor
2. **Set Proper Timeouts**: Configure waitFor timeouts for slow operations
3. **Avoid act() Warnings**: Use userEvent, waitFor, findBy appropriately
4. **Clean Up Timers**: Use jest.useFakeTimers() and cleanup properly

### Mocking Best Practices

1. **Mock at Right Level**: Mock external dependencies, not internal logic
2. **Reset Mocks**: Clear mocks between tests
3. **Use MSW for API**: Prefer MSW over mocking axios/fetch directly
4. **Avoid Over-Mocking**: Don't mock what you're testing

### Coverage Best Practices

1. **Focus on Behavior**: Test user-facing behavior, not implementation
2. **Don't Chase 100%**: Focus on critical paths
3. **Test Error States**: Include error handling tests
4. **Test Edge Cases**: Include boundary conditions

## Common Testing Patterns

### Testing Lists and Iterations

```javascript
it('renders list of items', () => {
  const items = ['Apple', 'Banana', 'Cherry'];
  render(<ItemList items={items} />);

  items.forEach(item => {
    expect(screen.getByText(item)).toBeInTheDocument();
  });
});
```

### Testing Accessibility

```javascript
it('has accessible form', () => {
  render(<ContactForm />);

  const nameInput = screen.getByLabelText(/name/i);
  expect(nameInput).toHaveAccessibleName('Name');
  expect(nameInput).toBeRequired();

  const submitButton = screen.getByRole('button', { name: /submit/i });
  expect(submitButton).toHaveAttribute('type', 'submit');
});
```

### Testing Error Boundaries

```javascript
it('catches errors and displays fallback', () => {
  const ThrowError = () => {
    throw new Error('Test error');
  };

  // Suppress console.error for this test
  const spy = jest.spyOn(console, 'error').mockImplementation(() => {});

  render(
    <ErrorBoundary fallback={<div>Something went wrong</div>}>
      <ThrowError />
    </ErrorBoundary>
  );

  expect(screen.getByText(/something went wrong/i)).toBeInTheDocument();

  spy.mockRestore();
});
```

### Testing Portals

```javascript
it('renders modal in portal', () => {
  render(<Modal isOpen={true}>Modal Content</Modal>);

  const modal = screen.getByText(/modal content/i);
  expect(modal).toBeInTheDocument();

  // Modal should be in document.body, not in the component tree
  expect(modal.parentElement).toBe(document.body);
});
```

## Troubleshooting

### Common Issues

**Issue**: "Unable to find element"
- **Solution**: Use screen.debug() to see DOM, check query type, wait for async updates

**Issue**: "Act warnings"
- **Solution**: Use userEvent instead of fireEvent, wrap state updates in act(), use waitFor/findBy

**Issue**: "Jest timeout"
- **Solution**: Increase timeout, check for infinite loops, ensure async operations complete

**Issue**: "Cannot read property of undefined"
- **Solution**: Check mocks are set up correctly, ensure components receive required props

**Issue**: "Multiple elements found"
- **Solution**: Make queries more specific, use getAllBy for multiple elements

## Resources

- Jest Documentation: https://jestjs.io/
- React Testing Library: https://testing-library.com/react
- Testing Library Queries: https://testing-library.com/docs/queries/about
- Jest DOM Matchers: https://github.com/testing-library/jest-dom
- MSW Documentation: https://mswjs.io/
- Common Mistakes: https://kentcdodds.com/blog/common-mistakes-with-react-testing-library

---

**Skill Version**: 1.0.0
**Last Updated**: October 2025
**Skill Category**: Testing, React, Quality Assurance
**Compatible With**: Jest 29+, React Testing Library 13+, React 16.8+
