---
name: typescript-e2e-testing
description: |
  Complete E2E (end-to-end) and integration testing skill for TypeScript/NestJS projects using Jest, real infrastructure via Docker, and GWT pattern.

  ALWAYS use this skill when user needs to:

  **SETUP** - Initialize or configure E2E testing infrastructure:
  - Set up E2E testing for a new project
  - Configure docker-compose for testing (Kafka, PostgreSQL, MongoDB, Redis)
  - Create jest-e2e.config.ts or E2E Jest configuration
  - Set up test helpers for database, Kafka, or Redis
  - Configure .env.e2e environment variables
  - Create test/e2e directory structure

  **WRITE** - Create or add E2E/integration tests:
  - Write, create, add, or generate e2e tests or integration tests
  - Test API endpoints, workflows, or complete features end-to-end
  - Test with real databases, message brokers, or external services
  - Test Kafka consumers/producers, event-driven workflows
  - Working on any file ending in .e2e-spec.ts or in test/e2e/ directory
  - Use GWT (Given-When-Then) pattern for tests

  **REVIEW** - Audit or evaluate E2E tests:
  - Review existing E2E tests for quality
  - Check test isolation and cleanup patterns
  - Audit GWT pattern compliance
  - Evaluate assertion quality and specificity
  - Check for anti-patterns (multiple WHEN actions, conditional assertions)

  **RUN** - Execute or analyze E2E test results:
  - Run E2E tests
  - Start/stop Docker infrastructure for testing
  - Analyze E2E test results
  - Verify Docker services are healthy
  - Interpret test output and failures

  **DEBUG** - Fix failing or flaky E2E tests:
  - Fix failing E2E tests
  - Debug flaky tests or test isolation issues
  - Troubleshoot connection errors (database, Kafka, Redis)
  - Fix timeout issues or async operation failures
  - Diagnose race conditions or state leakage
  - Debug Kafka message consumption issues

  **OPTIMIZE** - Improve E2E test performance:
  - Speed up slow E2E tests
  - Optimize Docker infrastructure startup
  - Replace fixed waits with smart polling
  - Reduce beforeEach cleanup time
  - Improve test parallelization where safe

  Keywords: e2e, end-to-end, integration test, e2e-spec.ts, test/e2e, Jest, supertest, NestJS, Kafka, Redpanda, PostgreSQL, MongoDB, Redis, docker-compose, GWT pattern, Given-When-Then, real infrastructure, test isolation, flaky test, MSW, nock, waitForMessages, fix e2e, debug e2e, run e2e, review e2e, optimize e2e, setup e2e
---

# E2E Testing Skill

E2E testing validates complete workflows from user perspective, using real infrastructure via Docker.

---

## Workflows

For comprehensive step-by-step guidance, use the appropriate workflow:

| Workflow | When to Use |
|----------|-------------|
| [Setup E2E Test](workflows/setup-e2e-test.md) | Setting up E2E infrastructure for a new or existing project |
| [Writing E2E Test](workflows/writing-e2e-test.md) | Creating new E2E test cases with proper GWT pattern |
| [Review E2E Test](workflows/review-e2e-test.md) | Reviewing existing tests for quality and correctness |
| [Running E2E Test](workflows/running-e2e-test.md) | Executing tests with proper verification |
| [Debugging E2E Test](workflows/debugging-e2e-test.md) | Systematically fixing failing tests |
| [Optimize E2E Test](workflows/optimize-e2e-test.md) | Improving test suite performance |

## Workflow Selection Guide

**IMPORTANT**: Before starting any E2E testing task, identify the user's intent and load the appropriate workflow.

### Detect User Intent → Select Workflow

| User Says / Wants | Workflow to Load | File |
|-------------------|------------------|------|
| "Set up E2E tests", "configure docker-compose", "add E2E to project", "create test helpers" | **Setup** | `workflows/setup-e2e-test.md` |
| "Write E2E tests", "add integration tests", "test this endpoint", "create e2e-spec" | **Writing** | `workflows/writing-e2e-test.md` |
| "Review E2E tests", "check test quality", "audit tests", "is this test correct?" | **Reviewing** | `workflows/review-e2e-test.md` |
| "Run E2E tests", "execute tests", "start docker and test", "check if tests pass" | **Running** | `workflows/running-e2e-test.md` |
| "Fix E2E tests", "debug tests", "tests are failing", "flaky test", "connection error" | **Debugging** | `workflows/debugging-e2e-test.md` |
| "Speed up E2E tests", "optimize tests", "tests are slow", "reduce test time" | **Optimizing** | `workflows/optimize-e2e-test.md` |

### Workflow Execution Protocol

1. **ALWAYS load the workflow file first** - Read the full workflow before taking action
2. **Follow each step in order** - Complete checkpoints before proceeding
3. **Load knowledge files as directed** - Each workflow specifies which `references/` files to read
4. **Verify compliance after completion** - Re-read relevant reference files to ensure quality

**Important**: Each workflow includes instructions to load relevant knowledge from the `references/` folder before and after completing tasks.

---

## Knowledge Base Structure

```
references/
├── common/              # Shared testing fundamentals
│   ├── knowledge.md     # Core E2E concepts and test pyramid
│   ├── rules.md         # Mandatory testing rules (GWT, timeouts, logging)
│   ├── best-practices.md # Test design and cleanup patterns
│   ├── test-case-creation-guide.md # GWT templates for all scenarios
│   ├── nestjs-setup.md  # NestJS app bootstrap and Jest config
│   ├── debugging.md     # VS Code config and log analysis
│   └── examples.md      # Comprehensive examples by category
│
├── kafka/               # Kafka-specific testing
│   ├── knowledge.md     # Why common approaches fail, architecture
│   ├── rules.md         # Kafka-specific testing rules
│   ├── test-helper.md   # KafkaTestHelper implementation
│   ├── docker-setup.md  # Redpanda/Kafka Docker configs
│   ├── performance.md   # Optimization techniques
│   ├── isolation.md     # Pre-subscription pattern details
│   └── examples.md      # Kafka test examples
│
├── postgres/            # PostgreSQL-specific testing
│   ├── knowledge.md     # PostgreSQL testing concepts
│   ├── rules.md         # Cleanup, transaction, assertion rules
│   ├── test-helper.md   # PostgresTestHelper implementation
│   └── examples.md      # CRUD, transaction, constraint examples
│
├── mongodb/             # MongoDB-specific testing
│   ├── knowledge.md     # MongoDB testing concepts
│   ├── rules.md         # Document cleanup and assertion rules
│   ├── test-helper.md   # MongoDbTestHelper implementation
│   ├── docker-setup.md  # Docker and Memory Server setup
│   └── examples.md      # Document and aggregation examples
│
├── redis/               # Redis-specific testing
│   ├── knowledge.md     # Redis testing concepts
│   ├── rules.md         # TTL and pub/sub rules
│   ├── test-helper.md   # RedisTestHelper implementation
│   ├── docker-setup.md  # Docker configuration
│   └── examples.md      # Cache, session, rate limit examples
│
└── api/                 # API testing (REST, GraphQL, gRPC)
    ├── knowledge.md     # API testing concepts
    ├── rules.md         # Request/response assertion rules
    ├── test-helper.md   # Auth and Supertest helpers
    ├── examples.md      # REST, GraphQL, validation examples
    └── mocking.md       # MSW and Nock external API mocking
```

## Quick Reference by Task

> **Tip**: For detailed step-by-step guidance, use the [Workflows](#workflows) section above.

### Setup New E2E Structure
**Workflow**: [Setup E2E Test](workflows/setup-e2e-test.md)
1. Read `references/common/knowledge.md` - Understand E2E fundamentals
2. Read `references/common/nestjs-setup.md` - Project setup
3. Read technology-specific `docker-setup.md` files as needed

### Write Test Cases
**Workflow**: [Writing E2E Test](workflows/writing-e2e-test.md)
1. **MANDATORY**: Read `references/common/rules.md` - GWT pattern, timeouts
2. Read `references/common/test-case-creation-guide.md` - Templates
3. Read technology-specific files:
   - **Kafka**: `references/kafka/knowledge.md` → `test-helper.md` → `isolation.md`
   - **PostgreSQL**: `references/postgres/rules.md` → `test-helper.md`
   - **MongoDB**: `references/mongodb/rules.md` → `test-helper.md`
   - **Redis**: `references/redis/rules.md` → `test-helper.md`
   - **API**: `references/api/rules.md` → `test-helper.md`

### Review Test Quality
**Workflow**: [Review E2E Test](workflows/review-e2e-test.md)
1. Read `references/common/rules.md` - Check against mandatory patterns
2. Read `references/common/best-practices.md` - Quality standards
3. Read technology-specific `rules.md` files

### Run E2E Tests
**Workflow**: [Running E2E Test](workflows/running-e2e-test.md)
1. Verify Docker infrastructure is running
2. Run tests sequentially with `npm run test:e2e > /tmp/e2e-${E2E_SESSION}-output.log 2>&1`
3. Follow failure protocol if tests fail

### Debug Failing Tests
**Workflow**: [Debugging E2E Test](workflows/debugging-e2e-test.md)
1. Read `references/common/debugging.md`
2. Create `/tmp/e2e-${E2E_SESSION}-failures.md` tracking file
3. Fix ONE test at a time

### Optimize Test Performance
**Workflow**: [Optimize E2E Test](workflows/optimize-e2e-test.md)
1. Read `references/common/best-practices.md` - Performance patterns
2. Read `references/kafka/performance.md` for Kafka tests
3. Measure baseline before making changes

### Examples
- Read `references/common/examples.md` for general patterns
- Read technology-specific `examples.md` for detailed scenarios

---

## Core Principles

### 0. Context Efficiency (Temp File Output)
**ALWAYS redirect E2E test output to temp files, NOT console**. E2E output is verbose and bloats agent context.

**IMPORTANT**: Redirect output to temp files only (NO console output). Use unique session ID to prevent conflicts.

```bash
# Generate unique session ID at start of debugging session
export E2E_SESSION=$(date +%s)-$$

# Standard pattern - redirect to file only (no console output)
npm run test:e2e > /tmp/e2e-${E2E_SESSION}-output.log 2>&1

# Read summary only (last 50 lines)
tail -50 /tmp/e2e-${E2E_SESSION}-output.log

# Get failure details
grep -B 2 -A 15 "FAIL\|✕" /tmp/e2e-${E2E_SESSION}-output.log

# Cleanup when done
rm -f /tmp/e2e-${E2E_SESSION}-*.log /tmp/e2e-${E2E_SESSION}-*.md
```

**Temp Files** (with `${E2E_SESSION}` unique per agent):
- `/tmp/e2e-${E2E_SESSION}-output.log` - Full test output
- `/tmp/e2e-${E2E_SESSION}-failures.log` - Filtered failure output
- `/tmp/e2e-${E2E_SESSION}-failures.md` - Tracking file for one-by-one fixing
- `/tmp/e2e-${E2E_SESSION}-debug.log` - Debug runs
- `/tmp/e2e-${E2E_SESSION}-verify.log` - Verification runs

### 1. Real Infrastructure
Test against actual services via Docker. Never mock databases or message brokers for E2E tests.

### 2. GWT Pattern (Mandatory)
ALL E2E tests MUST follow Given-When-Then:
```typescript
it('should create user and return 201', async () => {
  // GIVEN: Valid user data
  const userData = { email: 'test@example.com', name: 'Test' };

  // WHEN: Creating user
  const response = await request(httpServer)
    .post('/users')
    .send(userData)
    .expect(201);

  // THEN: User created with correct data
  expect(response.body.data.email).toBe('test@example.com');
});
```

### 3. Test Isolation
Each test MUST be independent:
- Clean database state in `beforeEach`
- Use unique identifiers (consumer groups, topics)
- Wait for async operations to complete

### 4. Specific Assertions
Assert exact values, not just existence:
```typescript
// WRONG
expect(response.body.data).toBeDefined();

// CORRECT
expect(response.body).toMatchObject({
  code: 'SUCCESS',
  data: { email: 'test@example.com', name: 'Test' }
});
```

---

## Project Structure

```
project-root/
├── src/
├── test/
│   ├── e2e/
│   │   ├── feature.e2e-spec.ts
│   │   ├── setup.ts
│   │   └── helpers/
│   │       ├── test-app.helper.ts
│   │       ├── postgres.helper.ts
│   │       ├── mongodb.helper.ts
│   │       ├── redis.helper.ts
│   │       └── kafka.helper.ts
│   └── jest-e2e.config.ts
├── docker-compose.e2e.yml
├── .env.e2e
└── package.json
```

---

## Essential Jest Configuration

```typescript
// test/jest-e2e.config.ts
const config: Config = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testMatch: ['**/*.e2e-spec.ts'],
  testTimeout: 25000,
  maxWorkers: 1,           // CRITICAL: Sequential execution
  clearMocks: true,
  forceExit: true,
  detectOpenHandles: true,
};
```

---

## Technology-Specific Timeouts

| Technology | Wait Time | Strategy |
|------------|-----------|----------|
| Kafka | 10-20s max (polling) | Smart polling with 50ms intervals |
| PostgreSQL | <1s | Direct queries |
| MongoDB | <1s | Direct queries |
| Redis | <100ms | In-memory operations |
| External API | 1-5s | Network latency |

---

## Failure Resolution Protocol

**CRITICAL: Fix ONE test at a time. NEVER run full suite repeatedly while fixing.**

When E2E tests fail:

1. **Initialize session** (once at start):
   ```bash
   export E2E_SESSION=$(date +%s)-$$
   ```
2. **Create tracking file**: `/tmp/e2e-${E2E_SESSION}-failures.md` with all failing tests
3. **Select ONE failing test** - work on only this test
4. **Run ONLY that test** (never full suite):
   ```bash
   npm run test:e2e -- -t "test name" > /tmp/e2e-${E2E_SESSION}-debug.log 2>&1
   tail -50 /tmp/e2e-${E2E_SESSION}-debug.log
   ```
5. **Fix the issue** - analyze error, make targeted fix
6. **Verify fix** - run same test 3-5 times:
   ```bash
   for i in {1..5}; do npm run test:e2e -- -t "test name" > /tmp/e2e-${E2E_SESSION}-run$i.log 2>&1 && echo "Run $i: PASS" || echo "Run $i: FAIL"; done
   ```
7. **Mark as FIXED** in tracking file
8. **Move to next failing test** - repeat steps 3-7
9. **Run full suite ONLY ONCE** after ALL individual tests pass
10. **Cleanup**: `rm -f /tmp/e2e-${E2E_SESSION}-*.log /tmp/e2e-${E2E_SESSION}-*.md`

**WHY**: Running full suite wastes time and context. Each failing test pollutes output, making debugging harder.

---

## Common Patterns

### Database Cleanup (PostgreSQL/MongoDB)
```typescript
beforeEach(async () => {
  await new Promise(r => setTimeout(r, 500)); // Wait for in-flight
  await repository.clear();  // PostgreSQL
  // OR
  await model.deleteMany({}); // MongoDB
});
```

### Kafka Test Helper Pattern
```typescript
// Use pre-subscription + buffer clearing (NOT fromBeginning: true)
const kafkaHelper = new KafkaTestHelper();
await kafkaHelper.subscribeToTopic(outputTopic, false);
// In beforeEach: kafkaHelper.clearMessages(outputTopic);
```

### Redis Cleanup
```typescript
beforeEach(async () => {
  await redis.flushdb();
});
```

### External API Mock (MSW)
```typescript
mockServer.use(
  http.post('https://api.external.com/endpoint', () => {
    return HttpResponse.json({ status: 'success' });
  })
);
```

### Async Event Verification (Kafka)
```typescript
// Use smart polling instead of fixed waits
await kafkaHelper.publishEvent(inputTopic, event, event.id);
const messages = await kafkaHelper.waitForMessages(outputTopic, 1, 20000);
expect(messages[0].value).toMatchObject({ id: event.id });
```

---

## Debugging Commands

**All commands redirect output to temp files only (no console output).**

```bash
# Initialize session (once at start)
export E2E_SESSION=$(date +%s)-$$

# Run specific test (no console output)
npm run test:e2e -- -t "should create user" > /tmp/e2e-${E2E_SESSION}-output.log 2>&1 && tail -50 /tmp/e2e-${E2E_SESSION}-output.log

# Run specific file
npm run test:e2e -- test/e2e/user.e2e-spec.ts > /tmp/e2e-${E2E_SESSION}-output.log 2>&1 && tail -50 /tmp/e2e-${E2E_SESSION}-output.log

# Run full suite
npm run test:e2e > /tmp/e2e-${E2E_SESSION}-output.log 2>&1 && tail -50 /tmp/e2e-${E2E_SESSION}-output.log

# Get failure details from last run
grep -B 2 -A 15 "FAIL\|✕" /tmp/e2e-${E2E_SESSION}-output.log

# Debug with breakpoints (requires console for interactive debugging)
node --inspect-brk node_modules/.bin/jest --config test/jest-e2e.config.ts --runInBand

# View application logs (limited)
tail -100 logs/e2e-test.log
grep -i error logs/e2e-test.log | tail -50

# Cleanup session files
rm -f /tmp/e2e-${E2E_SESSION}-*.log /tmp/e2e-${E2E_SESSION}-*.md
```

---

## Anti-Patterns to Avoid

1. **Multiple WHEN actions** - Split into separate tests
2. **Conditional assertions** - Create deterministic test cases
3. **Shared state between tests** - Clean in beforeEach
4. **Mocking databases** - Use real connections
5. **Skipping cleanup** - Always clean before AND after
6. **Fixing multiple tests at once** - Fix one at a time
7. **Generic assertions** - Assert specific values
8. **fromBeginning: true for Kafka** - Use pre-subscription + buffer clearing
