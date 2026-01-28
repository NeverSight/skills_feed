---
name: Vitest
description: Expert guidance for Vitest testing framework including unit tests, integration tests, mocking, coverage, React Testing Library integration, and TypeScript testing. Use this when writing tests for Vite-based applications.
---

# Vitest

Expert assistance with Vitest - Blazing fast unit test framework.

## Overview

Vitest is a Vite-native testing framework:
- **Fast**: Powered by Vite, instant HMR
- **Compatible**: Jest-compatible API
- **TypeScript**: First-class TypeScript support
- **Coverage**: Built-in coverage with v8/istanbul
- **UI**: Beautiful UI for test results

## Installation

```bash
npm install --save-dev vitest
npm install --save-dev @vitest/ui
npm install --save-dev @testing-library/react @testing-library/jest-dom
```

## Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'json'],
    },
  },
});
```

### Setup File

```typescript
// src/test/setup.ts
import { expect, afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';
import * as matchers from '@testing-library/jest-dom/matchers';

expect.extend(matchers);

afterEach(() => {
  cleanup();
});
```

## Basic Tests

```typescript
import { describe, it, expect } from 'vitest';

describe('Math functions', () => {
  it('adds numbers', () => {
    expect(1 + 1).toBe(2);
  });

  it('multiplies numbers', () => {
    const result = 2 * 3;
    expect(result).toEqual(6);
  });
});
```

## Testing React Components

```typescript
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { Button } from './Button';

describe('Button', () => {
  it('renders with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('handles click events', async () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click</Button>);

    await userEvent.click(screen.getByText('Click'));
    expect(handleClick).toHaveBeenCalledOnce();
  });
});
```

## Mocking

```typescript
import { vi } from 'vitest';

// Mock function
const mockFn = vi.fn();
mockFn('hello');
expect(mockFn).toHaveBeenCalledWith('hello');

// Mock return value
const mockFn = vi.fn().mockReturnValue(42);
expect(mockFn()).toBe(42);

// Mock async function
const mockFn = vi.fn().mockResolvedValue('data');
const result = await mockFn();
expect(result).toBe('data');

// Mock module
vi.mock('./api', () => ({
  fetchCertificate: vi.fn().mockResolvedValue({ id: '1', subject: 'CN=test' }),
}));
```

## Best Practices

1. **Describe Blocks**: Group related tests
2. **Clear Names**: Write descriptive test names
3. **AAA Pattern**: Arrange, Act, Assert
4. **One Assertion**: Test one thing at a time
5. **Mock External**: Mock external dependencies
6. **Coverage**: Aim for high coverage
7. **Fast Tests**: Keep tests fast
8. **Isolation**: Tests should be independent
9. **User Events**: Use userEvent over fireEvent
10. **Accessibility**: Test with accessible queries

## Resources

- Documentation: https://vitest.dev
- GitHub: https://github.com/vitest-dev/vitest
