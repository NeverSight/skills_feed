---
name: setup-vitest
description: Configure Vitest for unit and integration testing. Use when setting up a test framework, when no test runner is detected, or when the user asks to configure testing.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Setup Vitest

Configure Vitest as the unit and integration test framework with Testing Library integration.

## When to Use This Skill

- No test framework is configured in the project
- User requests to set up unit testing
- Migrating from Jest to Vitest
- Setting up a new project that needs testing

## Installation

Use `ni` to auto-detect the package manager:

```bash
# Core Vitest packages
ni -D vitest @vitest/ui @vitest/coverage-v8

# For React projects
ni -D @testing-library/react @testing-library/dom @testing-library/user-event @testing-library/jest-dom

# For Vue projects
ni -D @testing-library/vue @testing-library/dom @testing-library/user-event @testing-library/jest-dom

# For Svelte projects
ni -D @testing-library/svelte @testing-library/dom @testing-library/user-event @testing-library/jest-dom
```

## Configuration

### vitest.config.ts

Create or update `vitest.config.ts` at the project root:

```typescript
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react' // For React projects

export default defineConfig({
  plugins: [react()], // Add framework plugin as needed
  test: {
    // Test file patterns
    include: ['**/*.{test,spec}.{js,ts,jsx,tsx}'],
    exclude: ['**/node_modules/**', '**/dist/**', '**/e2e/**'],

    // Environment - use 'jsdom' or 'happy-dom' for DOM testing
    environment: 'jsdom',

    // Enable global test APIs (describe, it, expect)
    globals: true,

    // Setup files run before each test file
    setupFiles: ['./tests/setup.ts'],

    // Mock behavior
    clearMocks: true,
    restoreMocks: true,

    // Coverage configuration
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'lcov'],
      reportsDirectory: './coverage',
      include: ['src/**/*.{ts,tsx}'],
      exclude: [
        '**/*.test.{ts,tsx}',
        '**/*.spec.{ts,tsx}',
        '**/*.d.ts',
        '**/types/**',
      ],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80,
      },
    },

    // Timeouts
    testTimeout: 5000,
    hookTimeout: 10000,
  },
})
```

### TypeScript Configuration

Add Vitest types to `tsconfig.json`:

```json
{
  "compilerOptions": {
    "types": ["vitest/globals"]
  }
}
```

### Setup File

Create `tests/setup.ts` for global test configuration:

```typescript
import '@testing-library/jest-dom/vitest'
import { cleanup } from '@testing-library/react'
import { afterEach, vi } from 'vitest'

// Cleanup after each test
afterEach(() => {
  cleanup()
})

// Mock window.matchMedia (common requirement)
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
})
```

### Package.json Scripts

Add test scripts to the **workspace** package.json (where the code lives):

```json
{
  "scripts": {
    "test": "vitest",
    "test:run": "vitest run",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest run --coverage"
  }
}
```

## Monorepo Configuration

For monorepo projects (Turborepo, Nx, Lerna, etc.), additional setup is required.

### 1. Check Project State

Read `.claude/marathon-ralph.json` to get the project configuration:
- `project.monorepo.type` - The monorepo type (turbo, nx, lerna, etc.)
- `project.packageManager` - The package manager (bun, pnpm, yarn, npm)

### 2. Turborepo Setup

If using Turborepo (`turbo.json` exists), add the test task to the pipeline:

**turbo.json:**
```json
{
  "$schema": "https://turbo.build/schema.json",
  "pipeline": {
    "test": {
      "dependsOn": ["^build"],
      "outputs": [],
      "cache": false
    },
    "test:run": {
      "dependsOn": ["^build"],
      "outputs": [],
      "cache": false
    }
  }
}
```

**Root package.json - add script to run tests across all workspaces:**
```json
{
  "scripts": {
    "test": "turbo run test",
    "test:run": "turbo run test:run"
  }
}
```

### 3. pnpm Workspaces Setup

For pnpm workspaces without Turborepo:

**Root package.json:**
```json
{
  "scripts": {
    "test": "pnpm -r test",
    "test:run": "pnpm -r test:run"
  }
}
```

### 4. npm/yarn Workspaces Setup

For npm or yarn workspaces:

**Root package.json:**
```json
{
  "scripts": {
    "test": "npm run test --workspaces",
    "test:run": "npm run test:run --workspaces"
  }
}
```

### 5. Workspace-Specific Testing

To run tests for a specific workspace, use the package manager's filter:

```bash
# Turborepo + bun
bun run --filter=web test

# pnpm
pnpm --filter web test

# npm workspaces
npm run test --workspace=web
```

## Writing Tests

### Query Priority (Most Accessible First)

Follow Testing Library's query priority:

1. **`getByRole`** - Best choice, tests accessibility
2. **`getByLabelText`** - For form fields
3. **`getByPlaceholderText`** - If no label available
4. **`getByText`** - For non-interactive elements
5. **`getByDisplayValue`** - For filled form values
6. **`getByAltText`** - For images
7. **`getByTitle`** - Rarely needed
8. **`getByTestId`** - Last resort only

### Example Test

```typescript
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi } from 'vitest'
import { LoginForm } from './LoginForm'

describe('LoginForm', () => {
  it('submits with valid credentials', async () => {
    const user = userEvent.setup()
    const onSubmit = vi.fn()

    render(<LoginForm onSubmit={onSubmit} />)

    // Use accessible queries
    await user.type(screen.getByLabelText(/email/i), 'user@example.com')
    await user.type(screen.getByLabelText(/password/i), 'password123')
    await user.click(screen.getByRole('button', { name: /sign in/i }))

    expect(onSubmit).toHaveBeenCalledWith({
      email: 'user@example.com',
      password: 'password123',
    })
  })

  it('shows error for invalid email', async () => {
    const user = userEvent.setup()
    render(<LoginForm onSubmit={vi.fn()} />)

    await user.type(screen.getByLabelText(/email/i), 'invalid')
    await user.click(screen.getByRole('button', { name: /sign in/i }))

    expect(screen.getByRole('alert')).toHaveTextContent(/valid email/i)
  })
})
```

## Testing Philosophy

Follow Kent C. Dodds' testing principles:

### DO

- Test user behavior, not implementation details
- Use `screen` for all queries
- Prefer `getByRole` with accessible names
- Use `userEvent` over `fireEvent`
- Use `findBy*` for async elements
- Use `queryBy*` ONLY for asserting non-existence

### DON'T

- Test internal state or methods
- Use `container.querySelector`
- Use test IDs when better queries exist
- Add unnecessary accessibility attributes
- Mock everything (test real behavior where possible)

## Mocking

### Mock Functions

```typescript
import { vi } from 'vitest'

const mockFn = vi.fn()
mockFn.mockReturnValue('value')
mockFn.mockResolvedValue('async value')
```

### Mock Modules

```typescript
// Automatic mock
vi.mock('./api')

// Manual mock with factory
vi.mock('./api', () => ({
  fetchUser: vi.fn(() => ({ id: 1, name: 'Test' })),
}))

// Partial mock
vi.mock('./utils', async (importOriginal) => {
  const actual = await importOriginal()
  return {
    ...actual,
    specificFunction: vi.fn(),
  }
})
```

## Verification

After setup, verify with:

```bash
# Run tests
nr test

# Run with coverage
nr test:coverage

# Open UI mode
nr test:ui
```

## Directory Structure

```
project/
├── src/
│   ├── components/
│   │   ├── Button.tsx
│   │   └── Button.test.tsx    # Colocated tests
│   └── utils/
│       ├── helpers.ts
│       └── helpers.test.ts
├── tests/
│   └── setup.ts               # Global setup
├── vitest.config.ts
└── package.json
```
