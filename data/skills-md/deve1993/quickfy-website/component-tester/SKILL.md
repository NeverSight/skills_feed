---
name: component-tester
description: Write, run, and analyze component tests using Vitest 4 and React Testing Library with coverage analysis, visual regression, and accessibility validation
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# Component Tester

Expert skill for testing UI component libraries with Vitest 4 and React Testing Library. Specializes in Browser Mode, visual regression testing, comprehensive coverage analysis, and accessibility validation.

## Technology Stack (2025)

### Testing Framework
- **Vitest 4.0** - Browser Mode stable, visual regression built-in
- **@testing-library/react 16** - React 19 support
- **@testing-library/user-event 14** - Realistic user interactions
- **@vitest/browser-playwright** - Browser provider for visual testing
- **@axe-core/react 5** - Accessibility testing

### Coverage & Reporting
- **@vitest/coverage-v8** - Fast V8-based coverage
- **Playwright Traces** - Debug failed tests with traces
- **HTML Reporter** - Visual test reports

## Core Capabilities

### 1. Test Writing
- Unit tests for individual components
- Integration tests for component interactions
- Visual regression tests (Vitest 4 Browser Mode)
- Accessibility tests (a11y)
- User interaction tests
- Async behavior testing
- Server Component testing

### 2. Vitest 4.0 Features
- **Browser Mode Stable** - Real browser testing
- **Visual Regression** - Built-in screenshot comparison
- **Playwright Traces** - Debugging with traces
- **Improved TypeScript** - Better type inference

### 3. Test Patterns
- Arrange-Act-Assert (AAA) pattern
- Test fixtures and factories
- Custom render functions
- Mock management
- React 19 `use` API testing

## Configuration

### Vitest 4 Config
```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
    css: true,
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'lcov'],
      exclude: [
        'node_modules/',
        'src/test/',
        '**/*.d.ts',
        '**/*.config.*',
        'dist/',
      ],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80,
      },
    },
    // Browser Mode (Vitest 4)
    browser: {
      enabled: true,
      provider: 'playwright',
      name: 'chromium',
      headless: true,
    },
  },
})
```

### Browser Mode Setup
```typescript
// vitest.workspace.ts
import { defineWorkspace } from 'vitest/config'

export default defineWorkspace([
  {
    extends: './vitest.config.ts',
    test: {
      name: 'unit',
      environment: 'jsdom',
      include: ['src/**/*.test.{ts,tsx}'],
    },
  },
  {
    extends: './vitest.config.ts',
    test: {
      name: 'browser',
      browser: {
        enabled: true,
        provider: 'playwright',
        instances: [{ browser: 'chromium' }],
      },
      include: ['src/**/*.browser.test.{ts,tsx}'],
    },
  },
])
```

### Setup File
```typescript
// src/test/setup.ts
import '@testing-library/jest-dom/vitest'
import { cleanup } from '@testing-library/react'
import { afterEach, vi } from 'vitest'

afterEach(() => {
  cleanup()
})

// Mock matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
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

// Mock IntersectionObserver
global.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  takeRecords() { return [] }
  unobserve() {}
} as any
```

## Test Examples

### Basic Component Test
```typescript
// Button.test.tsx
import { render, screen } from '@testing-library/react'
import { userEvent } from '@testing-library/user-event'
import { describe, it, expect, vi } from 'vitest'
import { Button } from './Button'

describe('Button', () => {
  it('renders with text', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument()
  })

  it('calls onClick when clicked', async () => {
    const handleClick = vi.fn()
    const user = userEvent.setup()

    render(<Button onClick={handleClick}>Click me</Button>)
    await user.click(screen.getByRole('button'))

    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>)
    expect(screen.getByRole('button')).toBeDisabled()
  })

  it('applies variant styles', () => {
    const { rerender } = render(<Button variant="primary">Primary</Button>)
    expect(screen.getByRole('button')).toHaveClass('bg-primary')

    rerender(<Button variant="secondary">Secondary</Button>)
    expect(screen.getByRole('button')).toHaveClass('bg-secondary')
  })
})
```

### Visual Regression Test (Vitest 4)
```typescript
// Button.visual.test.tsx
import { page } from '@vitest/browser/context'
import { describe, it, expect } from 'vitest'
import { render } from '@testing-library/react'
import { Button } from './Button'

describe('Button visual', () => {
  it('matches default screenshot', async () => {
    render(<Button>Click me</Button>)

    await expect(page.screenshot()).toMatchFileSnapshot(
      './__snapshots__/button-default.png'
    )
  })

  it('matches hover state screenshot', async () => {
    render(<Button>Hover me</Button>)

    const button = page.getByRole('button')
    await button.hover()

    await expect(page.screenshot()).toMatchFileSnapshot(
      './__snapshots__/button-hover.png'
    )
  })

  it('matches all variants', async () => {
    const variants = ['primary', 'secondary', 'outline', 'ghost'] as const

    for (const variant of variants) {
      render(<Button variant={variant}>{variant}</Button>)

      await expect(page.screenshot()).toMatchFileSnapshot(
        `./__snapshots__/button-${variant}.png`
      )
    }
  })
})
```

### Accessibility Test
```typescript
// Button.a11y.test.tsx
import { render } from '@testing-library/react'
import { axe, toHaveNoViolations } from 'jest-axe'
import { describe, it, expect } from 'vitest'
import { Button } from './Button'

expect.extend(toHaveNoViolations)

describe('Button accessibility', () => {
  it('has no accessibility violations', async () => {
    const { container } = render(<Button>Click me</Button>)
    const results = await axe(container)
    expect(results).toHaveNoViolations()
  })

  it('has correct ARIA label when icon-only', async () => {
    const { container } = render(
      <Button aria-label="Close dialog" size="icon">
        <XIcon />
      </Button>
    )
    const results = await axe(container)
    expect(results).toHaveNoViolations()
  })
})
```

### Keyboard Navigation Test
```typescript
// Menu.test.tsx
import { render, screen } from '@testing-library/react'
import { userEvent } from '@testing-library/user-event'
import { describe, it, expect } from 'vitest'
import { Menu } from './Menu'

describe('Menu keyboard navigation', () => {
  it('opens menu with Enter key', async () => {
    const user = userEvent.setup()
    render(<Menu />)

    const trigger = screen.getByRole('button', { name: /open menu/i })
    await user.tab()
    await user.keyboard('{Enter}')

    expect(screen.getByRole('menu')).toBeInTheDocument()
  })

  it('navigates items with arrow keys', async () => {
    const user = userEvent.setup()
    render(<Menu defaultOpen />)

    const items = screen.getAllByRole('menuitem')

    await user.tab()
    expect(items[0]).toHaveFocus()

    await user.keyboard('{ArrowDown}')
    expect(items[1]).toHaveFocus()

    await user.keyboard('{ArrowUp}')
    expect(items[0]).toHaveFocus()
  })

  it('closes menu with Escape key', async () => {
    const user = userEvent.setup()
    render(<Menu defaultOpen />)

    expect(screen.getByRole('menu')).toBeInTheDocument()

    await user.keyboard('{Escape}')

    expect(screen.queryByRole('menu')).not.toBeInTheDocument()
  })
})
```

### React 19 Server Component Test
```typescript
// ProductList.test.tsx
import { render, screen } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'

// Mock the database
vi.mock('@/lib/db', () => ({
  db: {
    products: {
      findMany: vi.fn().mockResolvedValue([
        { id: '1', name: 'Product 1', price: 100 },
        { id: '2', name: 'Product 2', price: 200 },
      ]),
    },
  },
}))

describe('ProductList Server Component', () => {
  it('renders products from database', async () => {
    const ProductList = (await import('./ProductList')).default

    render(await ProductList())

    expect(screen.getByText('Product 1')).toBeInTheDocument()
    expect(screen.getByText('Product 2')).toBeInTheDocument()
  })
})
```

### Custom Hooks Test
```typescript
// useCounter.test.ts
import { renderHook, act } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import { useCounter } from './useCounter'

describe('useCounter', () => {
  it('increments counter', () => {
    const { result } = renderHook(() => useCounter())

    expect(result.current.count).toBe(0)

    act(() => {
      result.current.increment()
    })

    expect(result.current.count).toBe(1)
  })

  it('decrements counter', () => {
    const { result } = renderHook(() => useCounter(10))

    act(() => {
      result.current.decrement()
    })

    expect(result.current.count).toBe(9)
  })

  it('resets to initial value', () => {
    const { result } = renderHook(() => useCounter(5))

    act(() => {
      result.current.increment()
      result.current.increment()
      result.current.reset()
    })

    expect(result.current.count).toBe(5)
  })
})
```

## Testing Best Practices

### What to Test
- User-visible behavior
- Accessibility features
- User interactions
- Different prop combinations
- Edge cases and error states
- Loading and async states

### What NOT to Test
- Implementation details
- Internal state directly
- Styling (use visual regression)
- Third-party libraries
- Framework internals

### Query Priority Order
```typescript
// 1. Accessible to all (best)
getByRole('button', { name: /submit/i })
getByLabelText(/username/i)
getByPlaceholderText(/enter email/i)
getByText(/welcome/i)

// 2. Semantic (good)
getByAltText(/profile picture/i)
getByTitle(/tooltip/i)

// 3. Test IDs (last resort)
getByTestId('submit-button')
```

## Running Tests

### Commands
```bash
# Run all tests
npm test

# Watch mode
npm test -- --watch

# Run with coverage
npm test -- --coverage

# Run visual tests
npm test -- --project=browser

# Update visual snapshots
npm test -- --update-snapshots

# Run in UI mode
npm test -- --ui

# Run specific file
npm test Button.test.tsx
```

### CI/CD Integration
```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
      - run: npm ci
      - run: npx playwright install chromium
      - run: npm test -- --coverage
      - uses: codecov/codecov-action@v4
        with:
          file: ./coverage/lcov.info
```

## When to Use This Skill

Activate when you need to:
- Write unit tests for components
- Create visual regression tests
- Set up test infrastructure
- Analyze test coverage
- Add accessibility tests
- Test user interactions
- Mock API calls
- Configure Vitest 4
- Debug test issues

## Output Format

Provide:
1. **Complete Test Suite**: All test cases
2. **Coverage Report**: What's tested
3. **Setup Instructions**: Configuration needed
4. **Accessibility Notes**: A11y test results
5. **Visual Tests**: Screenshot comparison setup
