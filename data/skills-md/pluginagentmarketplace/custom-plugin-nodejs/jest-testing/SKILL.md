---
name: jest-testing
description: Test Node.js applications with Jest including unit tests, integration tests, mocking, code coverage, and CI/CD integration
sasmp_version: "1.3.0"
bonded_agent: 01-nodejs-fundamentals
bond_type: PRIMARY_BOND
---

# Jest Testing Skill

Master testing Node.js applications with Jest - the delightful JavaScript testing framework.

## Quick Start

Test in 3 steps:
1. **Install** - `npm install --save-dev jest supertest`
2. **Write Test** - Create `*.test.js` files
3. **Run** - `npm test`

## Core Concepts

### Basic Test Structure
```javascript
// sum.test.js
const sum = require('./sum');

describe('sum function', () => {
  test('adds 1 + 2 to equal 3', () => {
    expect(sum(1, 2)).toBe(3);
  });

  test('adds negative numbers', () => {
    expect(sum(-1, -2)).toBe(-3);
  });
});
```

### Jest Configuration
```javascript
// package.json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  },
  "jest": {
    "testEnvironment": "node",
    "coverageThreshold": {
      "global": {
        "branches": 80,
        "functions": 80,
        "lines": 80
      }
    }
  }
}
```

### Unit Testing
```javascript
// userService.test.js
const UserService = require('./userService');
const User = require('./models/User');

jest.mock('./models/User');

describe('UserService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('createUser', () => {
    it('should create user successfully', async () => {
      const userData = {
        name: 'John',
        email: 'john@example.com'
      };

      User.create.mockResolvedValue({ id: 1, ...userData });

      const result = await UserService.createUser(userData);

      expect(User.create).toHaveBeenCalledWith(userData);
      expect(result.id).toBe(1);
    });

    it('should throw error for duplicate email', async () => {
      User.create.mockRejectedValue(new Error('Email exists'));

      await expect(UserService.createUser({}))
        .rejects
        .toThrow('Email exists');
    });
  });
});
```

## Learning Path

### Beginner (1-2 weeks)
- ✅ Setup Jest and write basic tests
- ✅ Understand test structure (describe/it/expect)
- ✅ Learn matchers (toBe, toEqual, etc.)
- ✅ Test synchronous functions

### Intermediate (3-4 weeks)
- ✅ Test async functions
- ✅ Mock modules and functions
- ✅ API testing with Supertest
- ✅ Code coverage reports

### Advanced (5-6 weeks)
- ✅ Integration testing
- ✅ Test database operations
- ✅ CI/CD integration
- ✅ Performance testing

## API Testing with Supertest
```javascript
const request = require('supertest');
const app = require('./app');

describe('User API', () => {
  describe('POST /api/users', () => {
    it('should create new user', async () => {
      const userData = {
        name: 'John',
        email: 'john@example.com',
        password: 'password123'
      };

      const response = await request(app)
        .post('/api/users')
        .send(userData)
        .expect('Content-Type', /json/)
        .expect(201);

      expect(response.body).toHaveProperty('id');
      expect(response.body.email).toBe(userData.email);
    });

    it('should return 400 for invalid email', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({ email: 'invalid' })
        .expect(400);

      expect(response.body).toHaveProperty('error');
    });
  });

  describe('GET /api/users/:id', () => {
    it('should return user by id', async () => {
      const response = await request(app)
        .get('/api/users/123')
        .expect(200);

      expect(response.body.id).toBe('123');
    });

    it('should return 404 for non-existent user', async () => {
      await request(app)
        .get('/api/users/999')
        .expect(404);
    });
  });
});
```

## Mocking Patterns
```javascript
// Mock entire module
jest.mock('axios');
const axios = require('axios');

test('fetches data from API', async () => {
  axios.get.mockResolvedValue({ data: { id: 1 } });

  const result = await fetchUser(1);

  expect(axios.get).toHaveBeenCalledWith('/api/users/1');
  expect(result.id).toBe(1);
});

// Spy on function
test('calls callback', () => {
  const callback = jest.fn();

  processData('test', callback);

  expect(callback).toHaveBeenCalledWith('test');
  expect(callback).toHaveBeenCalledTimes(1);
});

// Mock timers
jest.useFakeTimers();

test('delays execution', () => {
  const callback = jest.fn();

  setTimeout(callback, 1000);
  jest.advanceTimersByTime(1000);

  expect(callback).toHaveBeenCalled();
});
```

## Test Lifecycle Hooks
```javascript
describe('User Tests', () => {
  beforeAll(async () => {
    // Setup test database
    await connectTestDB();
  });

  afterAll(async () => {
    // Cleanup
    await disconnectTestDB();
  });

  beforeEach(async () => {
    // Clear data before each test
    await User.deleteMany({});
  });

  afterEach(() => {
    // Cleanup after each test
    jest.clearAllMocks();
  });

  test('...', () => {});
});
```

## Jest Matchers
```javascript
// Equality
expect(value).toBe(expected)        // Strict equality (===)
expect(value).toEqual(expected)     // Deep equality
expect(value).not.toBe(expected)    // Negation

// Truthiness
expect(value).toBeDefined()
expect(value).toBeNull()
expect(value).toBeTruthy()
expect(value).toBeFalsy()

// Numbers
expect(value).toBeGreaterThan(3)
expect(value).toBeGreaterThanOrEqual(3)
expect(value).toBeLessThan(5)
expect(value).toBeCloseTo(0.3)      // Floating point

// Strings
expect(string).toMatch(/pattern/)
expect(string).toContain('substring')

// Arrays
expect(array).toContain(item)
expect(array).toHaveLength(3)

// Objects
expect(obj).toHaveProperty('key')
expect(obj).toMatchObject({ key: 'value' })

// Exceptions
expect(() => fn()).toThrow()
expect(() => fn()).toThrow('error message')

// Async
await expect(promise).resolves.toBe(value)
await expect(promise).rejects.toThrow()
```

## Code Coverage
```bash
# Run with coverage
npm test -- --coverage

# Coverage report shows:
# - Statements: % of code executed
# - Branches: % of if/else paths
# - Functions: % of functions called
# - Lines: % of lines executed
```

## Testing Best Practices
- ✅ AAA pattern: Arrange, Act, Assert
- ✅ One assertion per test (ideally)
- ✅ Descriptive test names
- ✅ Test edge cases
- ✅ Mock external dependencies
- ✅ Clean up after tests
- ✅ Avoid test interdependence
- ✅ Aim for 80%+ coverage

## CI/CD Integration
```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - run: npm ci
      - run: npm test -- --coverage
      - uses: codecov/codecov-action@v3
```

## When to Use

Use Jest testing when:
- Building Node.js applications
- Need comprehensive test coverage
- Want fast, parallel test execution
- Require mocking and snapshot testing
- Implementing CI/CD pipelines

## Related Skills
- Express REST API (test API endpoints)
- Async Programming (test async code)
- Database Integration (test DB operations)
- JWT Authentication (test auth flows)

## Resources
- [Jest Documentation](https://jestjs.io)
- [Supertest Documentation](https://github.com/visionmedia/supertest)
- [Testing Best Practices](https://github.com/goldbergyoni/javascript-testing-best-practices)
