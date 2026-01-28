---
name: testing
description: Write tests for JavaScript, React, PHP, and WordPress including unit tests, integration tests, and E2E tests. Use when writing tests, setting up testing frameworks, or debugging test failures.
---

# Testing Skill

## Instructions

When writing tests:

### 1. JavaScript Testing (Jest)

**Setup:**
```javascript
// jest.config.js
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  collectCoverageFrom: ['src/**/*.{js,jsx}'],
};
```

**Unit Test Example:**
```javascript
// utils.test.js
import { formatPrice, validateEmail } from './utils';

describe('formatPrice', () => {
  it('formats number as currency', () => {
    expect(formatPrice(1000)).toBe('$1,000.00');
  });

  it('handles zero', () => {
    expect(formatPrice(0)).toBe('$0.00');
  });

  it('handles negative numbers', () => {
    expect(formatPrice(-50)).toBe('-$50.00');
  });
});

describe('validateEmail', () => {
  it('returns true for valid email', () => {
    expect(validateEmail('user@example.com')).toBe(true);
  });

  it('returns false for invalid email', () => {
    expect(validateEmail('invalid')).toBe(false);
    expect(validateEmail('no@domain')).toBe(false);
  });
});
```

**Async Test:**
```javascript
describe('fetchUser', () => {
  it('fetches user data', async () => {
    const user = await fetchUser(1);
    expect(user).toHaveProperty('name');
    expect(user.id).toBe(1);
  });

  it('throws on invalid id', async () => {
    await expect(fetchUser(-1)).rejects.toThrow('Invalid ID');
  });
});
```

**Mocking:**
```javascript
// Mock module
jest.mock('./api');
import { fetchData } from './api';

fetchData.mockResolvedValue({ data: 'mocked' });

// Mock function
const mockCallback = jest.fn();
mockCallback.mockReturnValue(42);

// Verify calls
expect(mockCallback).toHaveBeenCalled();
expect(mockCallback).toHaveBeenCalledWith('arg1', 'arg2');
expect(mockCallback).toHaveBeenCalledTimes(2);
```

### 2. React Testing (React Testing Library)

**Component Test:**
```javascript
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Button from './Button';

describe('Button', () => {
  it('renders with label', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
  });

  it('calls onClick when clicked', async () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click</Button>);

    await userEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when loading', () => {
    render(<Button loading>Submit</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

**Form Test:**
```javascript
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import LoginForm from './LoginForm';

describe('LoginForm', () => {
  it('submits form with valid data', async () => {
    const onSubmit = jest.fn();
    render(<LoginForm onSubmit={onSubmit} />);

    await userEvent.type(screen.getByLabelText(/email/i), 'user@example.com');
    await userEvent.type(screen.getByLabelText(/password/i), 'password123');
    await userEvent.click(screen.getByRole('button', { name: /log in/i }));

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        email: 'user@example.com',
        password: 'password123',
      });
    });
  });

  it('shows error for invalid email', async () => {
    render(<LoginForm onSubmit={jest.fn()} />);

    await userEvent.type(screen.getByLabelText(/email/i), 'invalid');
    await userEvent.click(screen.getByRole('button', { name: /log in/i }));

    expect(await screen.findByText(/invalid email/i)).toBeInTheDocument();
  });
});
```

### 3. PHP Testing (PHPUnit)

**Setup:**
```xml
<!-- phpunit.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<phpunit bootstrap="tests/bootstrap.php" colors="true">
    <testsuites>
        <testsuite name="Unit">
            <directory>tests/Unit</directory>
        </testsuite>
    </testsuites>
</phpunit>
```

**Unit Test:**
```php
<?php
// tests/Unit/HelperTest.php
use PHPUnit\Framework\TestCase;

class HelperTest extends TestCase
{
    public function test_format_price_returns_formatted_string()
    {
        $result = format_price(1000);
        $this->assertEquals('$1,000.00', $result);
    }

    public function test_sanitize_title_removes_special_chars()
    {
        $result = sanitize_title('Hello World!');
        $this->assertEquals('hello-world', $result);
    }

    /**
     * @dataProvider emailProvider
     */
    public function test_validate_email($email, $expected)
    {
        $this->assertEquals($expected, validate_email($email));
    }

    public function emailProvider(): array
    {
        return [
            ['user@example.com', true],
            ['invalid', false],
            ['', false],
        ];
    }
}
```

### 4. WordPress Testing

**Setup:**
```php
<?php
// tests/bootstrap.php
$_tests_dir = getenv('WP_TESTS_DIR') ?: '/tmp/wordpress-tests-lib';
require_once $_tests_dir . '/includes/functions.php';

function _manually_load_plugin() {
    require dirname(__DIR__) . '/plugin-name.php';
}
tests_add_filter('muplugins_loaded', '_manually_load_plugin');

require $_tests_dir . '/includes/bootstrap.php';
```

**Plugin Test:**
```php
<?php
class PluginTest extends WP_UnitTestCase
{
    public function test_plugin_is_activated()
    {
        $this->assertTrue(is_plugin_active('plugin-name/plugin-name.php'));
    }

    public function test_custom_post_type_is_registered()
    {
        $this->assertTrue(post_type_exists('portfolio'));
    }

    public function test_shortcode_renders_content()
    {
        $output = do_shortcode('[my_shortcode]');
        $this->assertStringContainsString('expected-content', $output);
    }
}
```

### 5. E2E Testing (Playwright)

```javascript
// tests/e2e/login.spec.js
import { test, expect } from '@playwright/test';

test.describe('Login Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
  });

  test('successful login redirects to dashboard', async ({ page }) => {
    await page.fill('[name="email"]', 'user@example.com');
    await page.fill('[name="password"]', 'password123');
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('h1')).toContainText('Welcome');
  });

  test('invalid credentials show error', async ({ page }) => {
    await page.fill('[name="email"]', 'wrong@example.com');
    await page.fill('[name="password"]', 'wrongpassword');
    await page.click('button[type="submit"]');

    await expect(page.locator('.error')).toBeVisible();
    await expect(page.locator('.error')).toContainText('Invalid credentials');
  });
});
```

### 6. Test Structure

```
tests/
├── unit/           # Pure function tests
├── integration/    # Component interaction tests
├── e2e/           # Full user flow tests
├── fixtures/      # Test data
├── mocks/         # Mock implementations
└── helpers/       # Test utilities
```

### 7. Testing Best Practices

- Test behavior, not implementation
- One assertion per test (when practical)
- Use descriptive test names
- Arrange-Act-Assert pattern
- Don't test external libraries
- Keep tests fast and isolated
- Use factories for test data
- Mock external dependencies
- Aim for 80%+ coverage on critical paths
- Run tests in CI/CD

### 8. Common Matchers

```javascript
// Jest/Vitest
expect(value).toBe(exact);
expect(value).toEqual(deepEqual);
expect(value).toBeTruthy();
expect(value).toBeFalsy();
expect(value).toBeNull();
expect(value).toContain(item);
expect(value).toHaveLength(3);
expect(value).toMatch(/regex/);
expect(fn).toThrow(Error);
expect(fn).toHaveBeenCalled();
```
