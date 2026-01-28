---
name: javascript-unit-testing
description: Writing high-quality unit tests for JavaScript and TypeScript using Jest. Covers test structure (AAA pattern, USE naming), breaking dependencies (stubs, mocks, dependency injection), testing async code (promises, callbacks, timers), avoiding flaky tests, and test-driven development. Use when writing tests, debugging test failures, refactoring tests for maintainability, or questions about Jest, TDD, mocks, stubs, or test best practices.
---

# JavaScript Unit Testing

Expert guidance for writing maintainable, trustworthy unit tests in JavaScript and TypeScript using Jest. Based on "The Art of Unit Testing, Third Edition" by Roy Osherove with Vladimir Khorikov (Manning, 2024).

## Instructions

When helping users with unit testing:

1. **Understand the context**: Identify if they're writing new tests, fixing existing ones, or learning concepts
2. **Apply core principles**: Focus on readability, maintainability, and trust in tests
3. **Use appropriate patterns**: Select the right testing pattern based on exit point type (return value, state change, or third-party call)
4. **Provide examples**: Show concrete code examples following best practices
5. **Reference supporting documentation**: Point to [REFERENCE.md](REFERENCE.md) for detailed concepts and [EXAMPLES.md](EXAMPLES.md) for more code samples

## Core Concepts

### Unit of Work

A **unit of work** is all actions between an **entry point** (function/method we trigger) and one or more **exit points** (observable results).

**Three types of exit points:**

1. **Return value** - Function returns a useful value
2. **State change** - Observable change in system state
3. **Third-party call** - Calling external dependency (logger, database, API)

### Good Unit Test Properties

**Must have:**

- Fast execution (milliseconds)
- Fully isolated from other tests
- Consistent results (no flakiness)
- Runs in memory (no filesystem, network, database)
- Clear intent and easy to read

**Avoid:**

- Logic in tests (if/else, loops, try/catch)
- Multiple concerns per test
- Shared state between tests
- Testing implementation details vs behavior

## Quick Start: Writing Your First Test

### Basic Test Structure (AAA Pattern)

```javascript
test('sum with two numbers returns their sum', () => {
  // Arrange - set up test data
  const input = '1,2';

  // Act - call the unit of work
  const result = sum(input);

  // Assert - verify the outcome
  expect(result).toBe(3);
});
```

### Test Naming (USE Pattern)

Format: **[U]**nit, **[S]**cenario, **[E]**xpectation

```javascript
// Good examples
test('sum, with two valid numbers, returns their sum', () => { ... });
test('verify, with no uppercase letter, returns false', () => { ... });
test('save, during maintenance window, throws exception', () => { ... });
```

### Organizing Tests

```javascript
describe('Password Verifier', () => {
  describe('one uppercase rule', () => {
    test('given no uppercase, returns false', () => {
      const verifier = makeVerifier([oneUpperCaseRule]);
      expect(verifier.verify('abc')).toBe(false);
    });

    test('given one uppercase, returns true', () => {
      const verifier = makeVerifier([oneUpperCaseRule]);
      expect(verifier.verify('Abc')).toBe(true);
    });
  });
});
```

**Use factory methods instead of beforeEach()** to avoid scroll fatigue and keep tests self-contained.

## Testing Different Exit Points

### Return Value Testing (Easiest)

```javascript
test('processes input and returns result', () => {
  const result = calculateTotal([10, 20, 30]);
  expect(result).toBe(60);
});
```

### State-Based Testing

```javascript
test('adds item to cart and updates count', () => {
  const cart = new ShoppingCart();

  cart.addItem('apple');

  expect(cart.itemCount()).toBe(1);
  expect(cart.contains('apple')).toBe(true);
});
```

### Interaction Testing (Use Sparingly)

Only for testing third-party calls (exit points):

```javascript
test('save calls logger with correct message', () => {
  const mockLogger = { info: jest.fn() };
  const repository = new Repository(mockLogger);

  repository.save({ id: 1, name: 'test' });

  expect(mockLogger.info).toHaveBeenCalledWith('Saved item 1');
});
```

**Important**: Use mocks only for exit points. Have **one mock per test maximum**. Most tests (95%+) should be return-value or state-based.

## Breaking Dependencies

### When to Break Dependencies

Break dependencies when code relies on:

- Time (Date.now(), moment())
- Random values (Math.random())
- Network calls (fetch, axios)
- Filesystem (fs.readFile)
- Databases
- External services

### Dependency Injection Patterns

**1. Parameter Injection (Simplest)**

```javascript
// Before - time dependency baked in
const verify = (input) => {
  const day = moment().day(); // Hard to test!
  if (day === 0 || day === 6) throw Error("Weekend!");
};

// After - time injected
const verify = (input, currentDay) => {
  if (currentDay === 0 || currentDay === 6) throw Error("Weekend!");
};

// Test with full control
test('on weekends, throws exception', () => {
  expect(() => verify('input', 0)).toThrow("Weekend!");
});
```

**2. Functional Injection**

```javascript
const verify = (logger) => (input) => {
  logger.info('Verifying');
  return input.length > 5;
};

// Test
test('verify logs attempt', () => {
  const stubLogger = { info: jest.fn() };
  const verifyFn = verify(stubLogger);
  verifyFn('password');
});
```

**3. Constructor Injection (OOP)**

```typescript
class Verifier {
  constructor(private logger: ILogger) {}

  verify(input: string): boolean {
    this.logger.info('Verifying');
    return true;
  }
}

// Test
test('verify calls logger', () => {
  const mockLogger = { info: jest.fn() };
  const verifier = new Verifier(mockLogger);
  verifier.verify('input');
  expect(mockLogger.info).toHaveBeenCalled();
});
```

### Stubs vs Mocks

**Stubs** (incoming dependencies):

- Provide fake data/behavior INTO the unit
- Do NOT assert against them
- Can have many per test

**Mocks** (outgoing dependencies):

- Represent exit points
- DO assert they were called correctly
- Should have ONE per test

```javascript
// Stub - provides data IN
const stubDatabase = {
  getUser: () => ({ id: 1, name: 'John' })
};

// Mock - verifies calls OUT
const mockLogger = {
  info: jest.fn()
};

test('getUserName retrieves name from database and logs', () => {
  const service = new UserService(stubDatabase, mockLogger);

  const name = service.getUserName(1);

  expect(name).toBe('John'); // Return value assertion
  expect(mockLogger.info).toHaveBeenCalledWith('Retrieved user 1'); // Mock assertion
});
```

## Testing Asynchronous Code

### Extract Entry Point Pattern

Extract pure logic from async operations:

```javascript
// Before - everything mixed
const isWebsiteAlive = async () => {
  const resp = await fetch('http://example.com');
  if (!resp.ok) throw resp.statusText;
  const text = await resp.text();
  return text.includes('illustrative')
    ? { success: true }
    : { success: false, status: 'missing text' };
};

// After - extract testable logic
const processFetchContent = (text) => {
  return text.includes('illustrative')
    ? { success: true }
    : { success: false, status: 'missing text' };
};

// Fast, synchronous unit test
test('with good content, returns success', () => {
  const result = processFetchContent('illustrative');
  expect(result.success).toBe(true);
});
```

### Extract Adapter Pattern

Wrap async dependencies behind testable interfaces:

```javascript
// network-adapter.js - wrapper for fetch
const fetchUrlText = async (url) => {
  const resp = await fetch(url);
  return resp.ok
    ? { ok: true, text: await resp.text() }
    : { ok: false, text: resp.statusText };
};

// website-verifier.js - inject adapter
const isWebsiteAlive = async (network) => {
  const result = await network.fetchUrlText('http://example.com');
  if (!result.ok) throw result.text;
  return result.text.includes('illustrative');
};

// Test with fake adapter (synchronous!)
test('with good content, returns true', async () => {
  const fakeNetwork = {
    fetchUrlText: () => ({ ok: true, text: 'illustrative' })
  };
  const result = await isWebsiteAlive(fakeNetwork);
  expect(result).toBe(true);
});
```

### Testing Timers

```javascript
test('calls callback after delay', () => {
  jest.useFakeTimers();
  const callback = jest.fn();

  delayedGreeting(callback);

  expect(callback).not.toHaveBeenCalled();
  jest.advanceTimersByTime(1000);
  expect(callback).toHaveBeenCalledWith('hello');

  jest.useRealTimers();
});
```

## Common Antipatterns to Avoid

1. **Logic in tests** - No if/else, loops, or try/catch
2. **Multiple mocks per test** - One exit point per test
3. **Asserting against stubs** - Only assert against mocks
4. **beforeEach() overuse** - Use factory methods instead
5. **Testing private methods** - Test through public API
6. **Overspecification** - Don't test implementation details
7. **Flaky tests** - Inject all dependencies for consistency
8. **Shared state** - Keep tests fully isolated
9. **Integration tests as unit tests** - Use real dependencies sparingly
10. **No test naming convention** - Follow USE pattern

## Test Quality Checklist

Can you answer YES to all these?

- ✓ Tests run in under a few minutes (ideally seconds)?
- ✓ Any team member can run tests on any machine?
- ✓ Tests give same results every time (no flakiness)?
- ✓ Tests work without network, database, or filesystem?
- ✓ One test failure doesn't affect other tests?
- ✓ Test names clearly explain what they verify?
- ✓ Tests are easy to read and understand?
- ✓ When tests fail, you know exactly what broke?

If NO to any → Review the corresponding section in [REFERENCE.md](REFERENCE.md)

## Examples

For comprehensive code examples covering all patterns and scenarios, see [EXAMPLES.md](EXAMPLES.md).

## Best Practices

**Test Structure:**

- Use AAA pattern (Arrange-Act-Assert)
- Follow USE naming (Unit-Scenario-Expectation)
- One assertion per test (or multiple for same concern)
- Factory methods over beforeEach()

**Dependencies:**

- Inject all dependencies
- Use stubs for incoming data
- Use mocks only for exit points (one per test)
- Prefer return-value and state-based tests (95%+ of tests)

**Async Code:**

- Extract pure logic into separate functions
- Wrap async dependencies behind adapters
- Use fake timers for time-dependent code
- Keep most tests synchronous

**Maintainability:**

- No logic in tests
- Test behavior, not implementation
- Keep tests independent
- Refactor tests like production code
- Trust your tests - if they fail, there's a bug

## Resources

- Full reference documentation: [REFERENCE.md](REFERENCE.md)
- Code examples: [EXAMPLES.md](EXAMPLES.md)
- Book: "The Art of Unit Testing, Third Edition" by Roy Osherove (Manning, 2024)
- Code samples: <https://github.com/royosherove/aout3-samples>
- Jest documentation: <https://jestjs.io/>
