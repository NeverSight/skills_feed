---
name: jest-generator
description: Generate Jest-based unit tests for JavaScript/TypeScript code. Creates
  test files following Jest conventions with proper mocking, describe blocks, and
  coverage.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Jest Generator Skill

## Purpose

This skill generates Jest-based unit tests for JavaScript and TypeScript code, following Jest conventions, best practices, and project standards. It creates comprehensive test suites with proper mocking, describe blocks, and code organization.

## When to Use

- Generate Jest tests for JavaScript/TypeScript modules
- Create test files for React components
- Add missing test coverage to existing JS/TS code
- Need Jest-specific patterns (mocks, spies, snapshots)

## Test File Naming Convention

**Source to Test Mapping:**
- Source: `src/components/Feature.tsx`
- Test: `src/components/Feature.test.tsx`
- Pattern: `<source_filename>.test.ts` or `<source_filename>.test.js`

**Examples:**
- `src/utils/validator.ts` → `src/utils/validator.test.ts`
- `src/models/User.ts` → `src/models/User.test.ts`
- `src/services/api.js` → `src/services/api.test.js`
- `src/components/Button.tsx` → `src/components/Button.test.tsx`

---

## Jest Test Generation Workflow

### 1. Analyze JavaScript/TypeScript Source Code

**Read the source file:**
```bash
# Read the source to understand structure
cat src/components/Feature.tsx
```

**Identify test targets:**
- Exported functions to test
- Classes and methods
- React components (if applicable)
- Error conditions
- Edge cases
- Dependencies and imports

**Output:** List of functions/classes/components requiring tests

---

### 2. Generate Test File Structure

**Create test file with proper naming:**

```typescript
/**
 * Unit tests for [module name]
 *
 * Tests cover:
 * - [Functionality 1]
 * - [Functionality 2]
 * - Error handling and edge cases
 */

import { functionToTest, ClassToTest, ComponentToTest } from './Feature';
import { mockDependency } from './__mocks__/dependency';

// Mock external dependencies
jest.mock('./dependency');
jest.mock('external-library');

// ============================================================================
// Test Setup
// ============================================================================

describe('ModuleName', () => {
  // Setup before each test
  beforeEach(() => {
    jest.clearAllMocks();
  });

  // Cleanup after each test
  afterEach(() => {
    jest.restoreAllMocks();
  });

  // ========================================================================
  // Class Tests
  // ========================================================================

  describe('ClassName', () => {
    let instance: ClassToTest;

    beforeEach(() => {
      instance = new ClassToTest();
    });

    describe('constructor', () => {
      it('should initialize with valid parameters', () => {
        // Arrange & Act
        const instance = new ClassToTest({ param: 'value' });

        // Assert
        expect(instance.param).toBe('value');
        expect(instance.initialized).toBe(true);
      });

      it('should throw error with invalid parameters', () => {
        // Arrange
        const invalidParams = null;

        // Act & Assert
        expect(() => new ClassToTest(invalidParams)).toThrow('Invalid parameters');
      });
    });

    describe('method', () => {
      it('should return expected result with valid input', () => {
        // Arrange
        const input = { name: 'test', value: 123 };

        // Act
        const result = instance.method(input);

        // Assert
        expect(result.processed).toBe(true);
        expect(result.name).toBe('test');
        expect(result.value).toBe(123);
      });

      it('should throw error with invalid input', () => {
        // Arrange
        const invalidInput = null;

        // Act & Assert
        expect(() => instance.method(invalidInput)).toThrow('Invalid input');
      });

      it('should handle edge case with empty input', () => {
        // Arrange
        const emptyInput = {};

        // Act
        const result = instance.method(emptyInput);

        // Assert
        expect(result).toEqual({});
      });
    });
  });

  // ========================================================================
  // Function Tests
  // ========================================================================

  describe('functionToTest', () => {
    it('should return expected result with valid input', () => {
      // Arrange
      const input = { key: 'value' };
      const expected = { processed: true, key: 'value' };

      // Act
      const result = functionToTest(input);

      // Assert
      expect(result).toEqual(expected);
    });

    it('should handle null input', () => {
      // Arrange
      const input = null;

      // Act & Assert
      expect(() => functionToTest(input)).toThrow('Input cannot be null');
    });

    it('should handle undefined input', () => {
      // Arrange
      const input = undefined;

      // Act
      const result = functionToTest(input);

      // Assert
      expect(result).toBeUndefined();
    });
  });

  // ========================================================================
  // Tests with Mocks
  // ========================================================================

  describe('functionWithDependency', () => {
    it('should call dependency with correct parameters', () => {
      // Arrange
      const input = { key: 'value' };
      const mockDep = jest.fn().mockReturnValue({ status: 'success' });

      // Act
      const result = functionWithDependency(input, mockDep);

      // Assert
      expect(mockDep).toHaveBeenCalledWith(input);
      expect(mockDep).toHaveBeenCalledTimes(1);
      expect(result.status).toBe('success');
    });

    it('should handle dependency error', () => {
      // Arrange
      const input = { key: 'value' };
      const mockDep = jest.fn().mockRejectedValue(new Error('API error'));

      // Act & Assert
      await expect(functionWithDependency(input, mockDep))
        .rejects.toThrow('API error');
    });
  });

  // ========================================================================
  // Async Tests
  // ========================================================================

  describe('asyncFunction', () => {
    it('should resolve with expected result', async () => {
      // Arrange
      const input = { key: 'value' };

      // Act
      const result = await asyncFunction(input);

      // Assert
      expect(result.success).toBe(true);
      expect(result.data).toEqual(input);
    });

    it('should reject with error on failure', async () => {
      // Arrange
      const invalidInput = null;

      // Act & Assert
      await expect(asyncFunction(invalidInput))
        .rejects.toThrow('Invalid input');
    });

    it('should handle timeout', async () => {
      // Arrange
      jest.useFakeTimers();
      const promise = asyncFunctionWithTimeout();

      // Act
      jest.advanceTimersByTime(5000);

      // Assert
      await expect(promise).rejects.toThrow('Timeout');
      jest.useRealTimers();
    });
  });

  // ========================================================================
  // Parametrized Tests (using test.each)
  // ========================================================================

  describe('validation', () => {
    it.each([
      ['valid@email.com', true],
      ['invalid.email', false],
      ['', false],
      [null, false],
      ['@no-user.com', false],
    ])('should validate email "%s" as %s', (email, expected) => {
      // Act
      const result = validateEmail(email);

      // Assert
      expect(result).toBe(expected);
    });
  });

  describe('permissions', () => {
    it.each([
      ['admin', 'all'],
      ['moderator', 'edit'],
      ['user', 'read'],
      ['guest', 'none'],
    ])('should return "%s" permission for %s user', (userType, expected) => {
      // Arrange
      const user = { type: userType };

      // Act
      const result = getPermissions(user);

      // Assert
      expect(result).toBe(expected);
    });
  });
});
```

**Deliverable:** Complete Jest test file

---

## Jest-Specific Patterns

### 1. Mocking

**Mock entire module:**
```typescript
jest.mock('./api', () => ({
  fetchData: jest.fn(),
  postData: jest.fn(),
}));
```

**Mock specific function:**
```typescript
import { fetchData } from './api';

jest.mock('./api');

describe('Component', () => {
  it('should fetch data', async () => {
    // Arrange
    (fetchData as jest.Mock).mockResolvedValue({ data: 'test' });

    // Act
    const result = await getData();

    // Assert
    expect(result.data).toBe('test');
  });
});
```

**Mock with implementation:**
```typescript
const mockFn = jest.fn((x: number) => x * 2);

// Use the mock
expect(mockFn(2)).toBe(4);
expect(mockFn).toHaveBeenCalledWith(2);
```

**Spy on method:**
```typescript
const obj = {
  method: () => 'original',
};

const spy = jest.spyOn(obj, 'method').mockReturnValue('mocked');

expect(obj.method()).toBe('mocked');
expect(spy).toHaveBeenCalled();

spy.mockRestore(); // Restore original implementation
```

### 2. Async Testing

**Testing promises:**
```typescript
it('should resolve with data', async () => {
  // Using async/await
  const result = await asyncFunction();
  expect(result).toBeDefined();
});

it('should reject with error', async () => {
  // Using async/await with expect
  await expect(asyncFunction()).rejects.toThrow('Error');
});

it('should handle promise chain', () => {
  // Using .then()
  return asyncFunction().then(result => {
    expect(result).toBeDefined();
  });
});
```

**Testing async with done callback:**
```typescript
it('should complete async operation', (done) => {
  asyncOperation((result) => {
    expect(result).toBe('complete');
    done();
  });
});
```

### 3. Timers

**Mock timers:**
```typescript
describe('with fake timers', () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  it('should execute after timeout', () => {
    const callback = jest.fn();

    setTimeout(callback, 1000);

    // Fast-forward time
    jest.advanceTimersByTime(1000);

    expect(callback).toHaveBeenCalled();
  });

  it('should run all timers', () => {
    const callback = jest.fn();

    setTimeout(callback, 1000);
    setTimeout(callback, 2000);

    jest.runAllTimers();

    expect(callback).toHaveBeenCalledTimes(2);
  });
});
```

### 4. Snapshots

**Snapshot testing:**
```typescript
it('should match snapshot', () => {
  const data = {
    name: 'test',
    value: 123,
    nested: {
      field: 'value',
    },
  };

  expect(data).toMatchSnapshot();
});

it('should match inline snapshot', () => {
  const result = formatData({ name: 'test' });

  expect(result).toMatchInlineSnapshot(`
    {
      "formatted": true,
      "name": "test",
    }
  `);
});
```

### 5. Setup and Teardown

**Test lifecycle hooks:**
```typescript
describe('TestSuite', () => {
  beforeAll(() => {
    // Runs once before all tests in this describe block
  });

  afterAll(() => {
    // Runs once after all tests in this describe block
  });

  beforeEach(() => {
    // Runs before each test in this describe block
  });

  afterEach(() => {
    // Runs after each test in this describe block
  });

  it('test 1', () => {});
  it('test 2', () => {});
});
```

### 6. Matchers

**Common Jest matchers:**
```typescript
// Equality
expect(value).toBe(expected);          // Strict equality (===)
expect(value).toEqual(expected);        // Deep equality
expect(value).toStrictEqual(expected);  // Strict deep equality

// Truthiness
expect(value).toBeTruthy();
expect(value).toBeFalsy();
expect(value).toBeNull();
expect(value).toBeUndefined();
expect(value).toBeDefined();

// Numbers
expect(value).toBeGreaterThan(3);
expect(value).toBeGreaterThanOrEqual(3);
expect(value).toBeLessThan(5);
expect(value).toBeLessThanOrEqual(5);
expect(value).toBeCloseTo(0.3, 5); // For floating point

// Strings
expect(string).toMatch(/pattern/);
expect(string).toContain('substring');

// Arrays and iterables
expect(array).toContain(item);
expect(array).toHaveLength(3);
expect(array).toContainEqual(item);

// Objects
expect(obj).toHaveProperty('key');
expect(obj).toHaveProperty('key', value);
expect(obj).toMatchObject({ key: value });

// Functions
expect(fn).toThrow();
expect(fn).toThrow('error message');
expect(fn).toThrow(ErrorClass);

// Promises
await expect(promise).resolves.toBe(value);
await expect(promise).rejects.toThrow();

// Mock functions
expect(mockFn).toHaveBeenCalled();
expect(mockFn).toHaveBeenCalledTimes(2);
expect(mockFn).toHaveBeenCalledWith(arg1, arg2);
expect(mockFn).toHaveBeenLastCalledWith(arg);
```

---

## React Component Testing

### Basic Component Test

```typescript
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { Button } from './Button';

describe('Button', () => {
  it('should render with text', () => {
    // Arrange & Act
    render(<Button>Click me</Button>);

    // Assert
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('should call onClick when clicked', () => {
    // Arrange
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);

    // Act
    fireEvent.click(screen.getByText('Click me'));

    // Assert
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('should be disabled when disabled prop is true', () => {
    // Arrange & Act
    render(<Button disabled>Click me</Button>);

    // Assert
    expect(screen.getByText('Click me')).toBeDisabled();
  });
});
```

### Component with Hooks

```typescript
import { renderHook, act } from '@testing-library/react';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('should initialize with default value', () => {
    // Arrange & Act
    const { result } = renderHook(() => useCounter());

    // Assert
    expect(result.current.count).toBe(0);
  });

  it('should increment count', () => {
    // Arrange
    const { result } = renderHook(() => useCounter());

    // Act
    act(() => {
      result.current.increment();
    });

    // Assert
    expect(result.current.count).toBe(1);
  });
});
```

---

## Running Jest

**Basic commands:**
```bash
# Run all tests
npm test
# or
jest

# Run specific file
jest src/components/Feature.test.ts

# Run tests matching pattern
jest Feature

# Run with coverage
jest --coverage

# Run in watch mode
jest --watch

# Run with verbose output
jest --verbose

# Update snapshots
jest --updateSnapshot
# or
jest -u
```

**Coverage commands:**
```bash
# Generate coverage report
jest --coverage

# View HTML report
open coverage/lcov-report/index.html

# Coverage with threshold
jest --coverage --coverageThreshold='{"global":{"branches":80,"functions":80,"lines":80,"statements":80}}'
```

---

## Best Practices

1. **Use descriptive test names:** `should <expected> when <condition>`
2. **Organize with describe blocks:** Group related tests
3. **Use beforeEach/afterEach:** Clean setup and teardown
4. **Mock external dependencies:** Isolate unit under test
5. **Test user behavior:** For components, test what users see/do
6. **Use test.each for similar tests:** Reduce duplication
7. **Keep tests independent:** No test depends on another
8. **Test edge cases:** Null, undefined, empty values
9. **Test error conditions:** Exceptions and rejections
10. **Use appropriate matchers:** Choose the most specific matcher

---

## TypeScript-Specific Considerations

**Type-safe mocks:**
```typescript
import { MockedFunction } from 'jest-mock';

const mockFn: MockedFunction<typeof realFunction> = jest.fn();
```

**Type assertions:**
```typescript
const mock = jest.fn() as jest.MockedFunction<typeof original>;
```

**Generic mocks:**
```typescript
interface ApiResponse<T> {
  data: T;
  status: number;
}

const mockApi = jest.fn<Promise<ApiResponse<User>>, [string]>();
```

---

## Quality Checklist

Before marking tests complete:

- [ ] Test file properly named (`<module>.test.ts`)
- [ ] All exported functions/classes/components tested
- [ ] Happy path tests included
- [ ] Edge case tests included (null, undefined, empty)
- [ ] Error condition tests included
- [ ] External dependencies mocked
- [ ] Tests organized with describe blocks
- [ ] beforeEach/afterEach used for setup/cleanup
- [ ] Test names are descriptive
- [ ] All tests pass
- [ ] Coverage ≥ 80%
- [ ] No snapshot tests without purpose
- [ ] Tests run quickly

---

## Integration with Testing Workflow

**Input:** JavaScript/TypeScript source file to test
**Process:** Analyze → Generate structure → Write tests → Run & verify
**Output:** Jest test file with ≥ 80% coverage
**Next Step:** Integration testing or code review

---

## Remember

- **Follow naming convention:** `<source_file>.test.ts`
- **Use describe blocks** for organization
- **Mock external dependencies** to isolate tests
- **Test behavior, not implementation**
- **Use appropriate matchers** for clarity
- **Aim for 80%+ coverage**
- **Keep tests fast and independent**
- **For React: test what users see and do**