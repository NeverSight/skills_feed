---
name: typescript-unit-testing
description: |
  Complete unit testing skill for TypeScript/NestJS projects using Jest, @golevelup/ts-jest, and in-memory databases.

  ALWAYS use this skill when user needs to:

  **SETUP** - Initialize or configure unit testing:
  - Set up Jest for a new project
  - Configure test infrastructure (jest.config.ts)
  - Install testing dependencies (@nestjs/testing, @golevelup/ts-jest)
  - Create mock helpers or test utilities
  - Set up coverage configuration

  **WRITE** - Create or add unit tests:
  - Write, create, add, or generate unit tests
  - Test a service, usecase, controller, guard, interceptor, pipe, or filter
  - Add tests for new code or features
  - Improve test coverage or add missing tests
  - Mock dependencies or set up test fixtures
  - Working on any file ending in .spec.ts

  **REVIEW** - Audit or evaluate unit tests:
  - Review existing tests for quality
  - Check test coverage and gaps
  - Audit testing patterns and conventions
  - Evaluate assertion quality

  **RUN** - Execute or analyze test results:
  - Run unit tests
  - Analyze test results or coverage reports
  - Understand test failures or successes
  - Check which tests are passing/failing

  **DEBUG** - Fix failing or broken tests:
  - Fix failing unit tests
  - Debug test errors or exceptions
  - Resolve mock issues or setup problems
  - Troubleshoot test timeouts or flaky tests
  - Diagnose "undefined" or unexpected results

  **OPTIMIZE** - Improve test performance and maintainability:
  - Speed up slow tests
  - Fix open handles preventing clean exit
  - Improve test organization
  - Reduce test execution time
  - Clean up test code

  Keywords: unit test, spec, jest, typescript, nestjs, mock, DeepMocked, createMock, AAA, test coverage, TDD, .spec.ts, testing, write test, add test, create test, fix test, debug test, run test, review test, optimize test, test setup, jest config
---

# Unit Testing Skill

Unit testing validates individual functions, methods, and classes in isolation by mocking all external dependencies.

---

## Workflows

For guided, step-by-step execution of unit testing tasks, use the appropriate workflow:

| Workflow | Purpose | When to Use |
|----------|---------|-------------|
| [Setup](workflows/setup-unit-test.md) | Initialize test infrastructure | New project or missing test setup |
| [Writing](workflows/writing-unit-test.md) | Write new unit tests | Creating tests for components |
| [Reviewing](workflows/reviewing-unit-test.md) | Review existing tests | Code review, quality audit |
| [Running](workflows/running-unit-test.md) | Execute tests | Running tests, analyzing results |
| [Debugging](workflows/debugging-unit-test.md) | Fix failing tests | Tests failing, need diagnosis |
| [Optimizing](workflows/optimizing-unit-test.md) | Improve test performance | Slow tests, maintainability |

## Workflow Selection Guide

**IMPORTANT**: Before starting any testing task, identify the user's intent and load the appropriate workflow.

### Detect User Intent → Select Workflow

| User Says / Wants | Workflow to Load | File |
|-------------------|------------------|------|
| "Set up tests", "configure Jest", "add testing to project", "install test dependencies" | **Setup** | `workflows/setup-unit-test.md` |
| "Write tests", "add tests", "create tests", "test this service/controller" | **Writing** | `workflows/writing-unit-test.md` |
| "Review tests", "check test quality", "audit tests", "are these tests good?" | **Reviewing** | `workflows/reviewing-unit-test.md` |
| "Run tests", "execute tests", "check if tests pass", "show test results" | **Running** | `workflows/running-unit-test.md` |
| "Fix tests", "debug tests", "tests are failing", "why is this test broken?" | **Debugging** | `workflows/debugging-unit-test.md` |
| "Speed up tests", "optimize tests", "tests are slow", "fix open handles" | **Optimizing** | `workflows/optimizing-unit-test.md` |

### Workflow Execution Protocol

1. **ALWAYS load the workflow file first** - Read the full workflow before taking action
2. **Follow each step in order** - Complete checkpoints before proceeding
3. **Load knowledge files as directed** - Each workflow specifies which `references/` files to read
4. **Verify compliance after completion** - Re-read relevant reference files to ensure quality

---

## Knowledge Base Structure

```
references/
├── common/              # Core testing fundamentals
│   ├── knowledge.md     # Testing philosophy and test pyramid
│   ├── rules.md         # Mandatory testing rules (AAA, naming, coverage)
│   ├── assertions.md    # Assertion patterns and matchers
│   ├── examples.md      # Comprehensive examples by category
│   ├── detect-open-handles.md   # Open handle detection and cleanup
│   └── performance-optimization.md  # Jest runtime optimization
│
├── nestjs/              # NestJS component testing
│   ├── services.md      # Service/usecase testing patterns
│   ├── controllers.md   # Controller testing patterns
│   ├── guards.md        # Guard testing patterns
│   ├── interceptors.md  # Interceptor testing patterns
│   └── pipes-filters.md # Pipe and filter testing
│
├── mocking/             # Mock patterns and strategies
│   ├── deep-mocked.md   # @golevelup/ts-jest patterns
│   ├── jest-native.md   # Jest.fn, spyOn, mock patterns
│   └── factories.md     # Test data factory patterns
│
├── repository/          # Repository testing
│   ├── mongodb.md       # mongodb-memory-server patterns
│   └── postgres.md      # pg-mem patterns
│
├── kafka/               # NestJS Kafka microservices testing
│   └── kafka.md         # ClientKafka, @MessagePattern, @EventPattern handlers
│
└── redis/               # Redis cache testing
    └── redis.md         # Cache operations, health checks, graceful degradation
```

## Quick Reference by Task

### Write Unit Tests
1. **MANDATORY**: Read `references/common/rules.md` - AAA pattern, naming, coverage
2. Read `references/common/assertions.md` - Assertion best practices
3. Read component-specific files:
   - **Services**: `references/nestjs/services.md`
   - **Controllers**: `references/nestjs/controllers.md`
   - **Guards**: `references/nestjs/guards.md`
   - **Interceptors**: `references/nestjs/interceptors.md`
   - **Pipes/Filters**: `references/nestjs/pipes-filters.md`

### Setup Mocking
1. Read `references/mocking/deep-mocked.md` - DeepMocked patterns
2. Read `references/mocking/jest-native.md` - Native Jest patterns
3. Read `references/mocking/factories.md` - Test data factories

### Test Repositories
1. **MongoDB**: `references/repository/mongodb.md`
2. **PostgreSQL**: `references/repository/postgres.md`

### Test Kafka (NestJS Microservices)
- Read `references/kafka/kafka.md` - ClientKafka mocking, @MessagePattern/@EventPattern handlers, emit/send testing

### Test Redis
- Read `references/redis/redis.md` - Cache operations, health checks, graceful degradation

### Examples
- Read `references/common/examples.md` for comprehensive patterns

### Optimize Test Performance
1. Read `references/common/performance-optimization.md` - Worker config, caching, CI optimization
2. Read `references/common/detect-open-handles.md` - Fix open handles preventing clean exit

### Debug Open Handles
- Read `references/common/detect-open-handles.md` - Detection commands, common handle types, cleanup patterns

---

## Core Principles

### 0. Context Efficiency (Temp File Output)
**ALWAYS redirect unit test output to temp files, NOT console**. Test output can be verbose and bloats agent context.

**IMPORTANT**: Use unique session ID in filenames to prevent conflicts when multiple agents run.

```bash
# Initialize session (once at start of testing session)
export UT_SESSION=$(date +%s)-$$

# Standard pattern - redirect output to temp file (NO console output)
npm test > /tmp/ut-${UT_SESSION}-output.log 2>&1

# Read summary only (last 50 lines)
tail -50 /tmp/ut-${UT_SESSION}-output.log

# Get failure details
grep -B 2 -A 15 "FAIL\|✕" /tmp/ut-${UT_SESSION}-output.log

# Cleanup when done
rm -f /tmp/ut-${UT_SESSION}-*.log /tmp/ut-${UT_SESSION}-*.md
```

**Temp Files** (with `${UT_SESSION}` unique per agent):
- `/tmp/ut-${UT_SESSION}-output.log` - Full test output
- `/tmp/ut-${UT_SESSION}-failures.md` - Tracking file for one-by-one fixing
- `/tmp/ut-${UT_SESSION}-debug.log` - Debug runs
- `/tmp/ut-${UT_SESSION}-verify.log` - Verification runs
- `/tmp/ut-${UT_SESSION}-coverage.log` - Coverage output

### 1. AAA Pattern (Mandatory)
ALL unit tests MUST follow Arrange-Act-Assert:
```typescript
it('should return user when found', async () => {
  // Arrange
  const userId = 'user-123';
  mockRepository.findById.mockResolvedValue({
    id: userId,
    email: 'test@example.com',
    name: 'Test User',
  });

  // Act
  const result = await target.getUser(userId);

  // Assert
  expect(result).toEqual({
    id: userId,
    email: 'test@example.com',
    name: 'Test User',
  });
  expect(mockRepository.findById).toHaveBeenCalledWith(userId);
});
```

### 2. Use `target` for SUT
Always name the system under test as `target`:
```typescript
let target: UserService;
let mockRepository: DeepMocked<UserRepository>;
```

### 3. DeepMocked Pattern
Use `@golevelup/ts-jest` for type-safe mocks:
```typescript
import { createMock, DeepMocked } from '@golevelup/ts-jest';

let mockService: DeepMocked<UserService>;

beforeEach(() => {
  mockService = createMock<UserService>();
});
```

### 4. Specific Assertions
Assert exact values, not just existence:
```typescript
// WRONG
expect(result).toBeDefined();
expect(result.id).toBeDefined();

// CORRECT
expect(result).toEqual({
  id: 'user-123',
  email: 'test@example.com',
  name: 'Test User',
});
```

### 5. Mock All Dependencies
Mock external services, never real databases for unit tests:
```typescript
// Unit Test: Mock repository
{ provide: UserRepository, useValue: mockRepository }

// Repository Test: Use in-memory database
const mongoServer = await createMongoMemoryServer();
```

---

## Standard Test Template

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { createMock, DeepMocked } from '@golevelup/ts-jest';
import { MockLoggerService } from 'src/shared/logger/services/mock-logger.service';

describe('UserService', () => {
  let target: UserService;
  let mockRepository: DeepMocked<UserRepository>;

  beforeEach(async () => {
    // Arrange: Create mocks
    mockRepository = createMock<UserRepository>();

    const module: TestingModule = await Test.createTestingModule({
      providers: [
        UserService,
        { provide: UserRepository, useValue: mockRepository },
      ],
    })
      .setLogger(new MockLoggerService())
      .compile();

    target = module.get<UserService>(UserService);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('getUser', () => {
    it('should return user when found', async () => {
      // Arrange
      mockRepository.findById.mockResolvedValue({
        id: 'user-123',
        email: 'test@example.com',
      });

      // Act
      const result = await target.getUser('user-123');

      // Assert
      expect(result).toEqual({ id: 'user-123', email: 'test@example.com' });
    });

    it('should throw NotFoundException when user not found', async () => {
      // Arrange
      mockRepository.findById.mockResolvedValue(null);

      // Act & Assert
      await expect(target.getUser('invalid')).rejects.toThrow(NotFoundException);
    });
  });
});
```

---

## Test Coverage Requirements

| Category | Priority | Description |
|----------|----------|-------------|
| Happy path | MANDATORY | Valid inputs producing expected outputs |
| Edge cases | MANDATORY | Empty arrays, null values, boundaries |
| Error cases | MANDATORY | Not found, validation failures |
| Exception behavior | MANDATORY | Correct type, error code, message |
| Business rules | MANDATORY | Domain logic, calculations |
| Input validation | MANDATORY | Invalid inputs, type mismatches |

**Coverage Target:** 80%+ for new code

---

## Failure Resolution Protocol

**CRITICAL: Fix ONE test at a time. NEVER run full suite repeatedly while fixing.**

When unit tests fail:

1. **Initialize session** (once at start):
   ```bash
   export UT_SESSION=$(date +%s)-$$
   ```
2. **Create tracking file**: `/tmp/ut-${UT_SESSION}-failures.md` with all failing tests
3. **Select ONE failing test** - work on only this test
4. **Run ONLY that test** (never full suite):
   ```bash
   npm test -- -t "test name" > /tmp/ut-${UT_SESSION}-debug.log 2>&1
   tail -50 /tmp/ut-${UT_SESSION}-debug.log
   ```
5. **Fix the issue** - analyze error, make targeted fix
6. **Verify fix** - run same test 3-5 times:
   ```bash
   for i in {1..5}; do npm test -- -t "test name" > /tmp/ut-${UT_SESSION}-run$i.log 2>&1 && echo "Run $i: PASS" || echo "Run $i: FAIL"; done
   ```
7. **Mark as FIXED** in tracking file
8. **Move to next failing test** - repeat steps 3-7
9. **Run full suite ONLY ONCE** after ALL individual tests pass
10. **Cleanup**: `rm -f /tmp/ut-${UT_SESSION}-*.log /tmp/ut-${UT_SESSION}-*.md`

**WHY**: Running full suite wastes time and context. Each failing test pollutes output, making debugging harder.

---

## Naming Conventions

### Test Files
- Pattern: `*.spec.ts`
- Location: Co-located with source file

### Test Structure
```typescript
describe('ClassName', () => {
  describe('methodName', () => {
    it('should [expected behavior] when [condition]', () => {});
  });
});
```

### Variable Names
| Variable | Convention |
|----------|------------|
| SUT | `target` |
| Mocks | `mock` prefix (`mockRepository`, `mockService`) |
| Mock Type | `DeepMocked<T>` |

---

## What NOT to Unit Test

Do NOT create unit tests for:
- **Interfaces** - Type definitions only, no runtime behavior
- **Enums** - Static value mappings, no logic to test
- **Constants** - Static values, no behavior
- **Type aliases** - Type definitions only
- **Plain DTOs** - Data structures without logic

Only test files containing **executable logic** (classes with methods, functions with behavior).

---

## Anti-Patterns to Avoid

| Don't | Why | Do Instead |
|-------|-----|------------|
| Assert only existence | Doesn't catch wrong values | Assert specific values |
| Conditional assertions | Non-deterministic | Separate test cases |
| Test private methods | Couples to implementation | Test via public interface |
| Share state between tests | Causes flaky tests | Fresh setup in beforeEach |
| Mock repositories in services | Tests implementation | Mock interfaces |
| Skip mock verification | Doesn't validate behavior | Verify mock calls |
| Test interfaces/enums/constants | No behavior to test | Skip these files |

---

## Checklist

**Setup:**
- [ ] Use `target` for system under test
- [ ] Use `mock` prefix for all mocks
- [ ] Use `DeepMocked<T>` type
- [ ] Include `.setLogger(new MockLoggerService())`
- [ ] Follow AAA pattern with comments
- [ ] Reset mocks in `afterEach`

**Coverage:**
- [ ] Happy path tests for all public methods
- [ ] Edge case tests (empty, null, boundaries)
- [ ] Error case tests (not found, validation failures)
- [ ] Exception type and error code verification
- [ ] Mock call verification (parameters + count)

**Quality:**
- [ ] 80%+ coverage on new code
- [ ] No assertions on log calls
- [ ] No test interdependence
- [ ] Tests fail when any field differs
