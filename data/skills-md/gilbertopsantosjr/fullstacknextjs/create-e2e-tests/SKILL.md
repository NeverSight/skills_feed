---
name: create-e2e-tests
description: Creates e2e and integration tests following project patterns and conventions with emphasis on test independence, state isolation verification, and proper cross-feature mocking. Adapted for Vitest, DynamoDB Local, and ZSA server actions.
---

# Create E2E Tests (Next.js + DynamoDB + Vitest)

## Technology Stack

| Component | Technology |
|-----------|------------|
| Test Runner | Vitest |
| Database | DynamoDB Local |
| HTTP Testing | SuperTest (for API routes) |
| Mocking | Vitest mocks, MSW (for HTTP) |
| Test Data | @faker-js/faker |
| Assertions | Vitest expect |

## Core Testing Principles

This skill enforces these critical testing principles aligned with modular architecture:

| Principle | How Applied in Tests |
|-----------|---------------------|
| **Test Independence** | Each feature's tests run in complete isolation |
| **State Isolation** | Never import from another feature's DAL in tests |
| **Explicit Communication** | Mock cross-feature interactions via service layer, not DAL |
| **Replaceability** | Tests don't depend on other features' internal implementations |

**CRITICAL**: Cross-feature DAL imports in test files are violations, even for test setup.

## Quick Start

When creating tests, follow this workflow:

1. Determine the feature and test type (unit/integration/e2e)
2. **Verify test isolation** (no cross-feature DAL imports)
3. Create test file co-located with source (`<function>.test.ts`)
4. Set up DynamoDB Local test helpers
5. Configure lifecycle hooks (beforeAll, afterAll, beforeEach)
6. Write tests following Arrange-Act-Assert pattern
7. **Mock cross-feature dependencies** via service layer
8. Use @faker-js/faker for test data
9. Clean up DynamoDB tables after each test
10. **Run state isolation verification** before committing

## File Location Pattern

Tests are **co-located** with source files:

```
src/features/<feature>/
├── dal/
│   ├── create_account.ts
│   ├── create_account.test.ts      # Co-located DAL test
│   ├── find_account_by_id.ts
│   └── find_account_by_id.test.ts  # Co-located DAL test
├── actions/
│   ├── create-account.ts
│   └── create-account.test.ts      # Co-located action test
└── service/
    ├── accounts-service.ts
    └── accounts-service.test.ts    # Co-located service test
```

**Key Points**:
- Test files use `.test.ts` suffix
- Tests live next to the code they test
- NO separate `__test__` folder pattern

## Required Imports Template

### DAL Tests (Integration with DynamoDB Local)

```typescript
import { describe, it, expect, beforeAll, afterAll, beforeEach } from 'vitest'
import { faker } from '@faker-js/faker'
import { setupTestDb, cleanupTestDb, clearTestData } from '@/test/db-helpers'
import { createAccount } from './create_account'
import { findAccountById } from './find_account_by_id'
```

### Action Tests

```typescript
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { faker } from '@faker-js/faker'
import { createAccountAction } from './create-account'
```

### Service Layer Tests

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { faker } from '@faker-js/faker'
import { accountsService } from './accounts-service'
import * as dalModule from '../dal'
```

## DynamoDB Local Setup

### Test Database Helpers (`src/test/db-helpers.ts`)

```typescript
import { DynamoDBClient } from '@aws-sdk/client-dynamodb'
import { Table } from 'dynamodb-onetable'
import { schema } from '@/features/database/db-schema'

// Use DynamoDB Local for tests
const testClient = new DynamoDBClient({
  endpoint: process.env.DYNAMODB_LOCAL_ENDPOINT || 'http://localhost:8000',
  region: 'local',
  credentials: {
    accessKeyId: 'local',
    secretAccessKey: 'local',
  },
})

let testTable: Table

export const setupTestDb = async () => {
  testTable = new Table({
    client: testClient,
    name: process.env.TEST_TABLE_NAME || 'test-table',
    schema,
    partial: true,
  })

  // Create table if it doesn't exist
  try {
    await testTable.createTable()
  } catch (error: any) {
    if (error.name !== 'ResourceInUseException') {
      throw error
    }
  }

  return testTable
}

export const cleanupTestDb = async () => {
  // Table cleanup is handled per-test
}

export const clearTestData = async (modelName: string) => {
  const Model = testTable.getModel(modelName)
  const items = await Model.scan({})

  for (const item of items) {
    await Model.remove(item)
  }
}

export const getTestTable = () => testTable
```

### Vitest Config for DynamoDB Local (`vitest.config.ts`)

```typescript
import { defineConfig } from 'vitest/config'
import path from 'path'

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    setupFiles: ['./src/test/setup.ts'],
    include: ['**/*.test.ts'],
    exclude: ['node_modules', 'dist'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: ['**/*.test.ts', '**/test/**'],
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
```

### Test Setup File (`src/test/setup.ts`)

```typescript
import { beforeAll, afterAll } from 'vitest'
import { setupTestDb, cleanupTestDb } from './db-helpers'

beforeAll(async () => {
  await setupTestDb()
})

afterAll(async () => {
  await cleanupTestDb()
})
```

## DAL Test Pattern

```typescript
// dal/account.test.ts
import { describe, it, expect, beforeEach } from 'vitest'
import { faker } from '@faker-js/faker'
import { clearTestData } from '@/test/db-helpers'
import { createAccount } from './create_account'
import { findAccountById } from './find_account_by_id'
import { findAccountsByUser } from './find_accounts_by_user'
import { updateAccount } from './update_account'
import { deleteAccount } from './delete_account'

describe('Account DAL', () => {
  const testUserId = faker.string.ulid()

  beforeEach(async () => {
    await clearTestData('Account')
  })

  describe('createAccount', () => {
    it('creates a new account successfully', async () => {
      // Arrange
      const input = {
        userId: testUserId,
        name: faker.company.name(),
        description: faker.lorem.sentence(),
      }

      // Act
      const result = await createAccount(input)

      // Assert
      expect(result.success).toBe(true)
      expect(result.data).toMatchObject({
        name: input.name,
        description: input.description,
        userId: testUserId,
        status: 'active',
      })
      expect(result.data?.id).toBeDefined()
      expect(result.data?.createdAt).toBeDefined()
    })

    it('returns validation error for invalid input', async () => {
      // Arrange
      const input = {
        userId: testUserId,
        name: '', // Invalid: empty name
      }

      // Act
      const result = await createAccount(input)

      // Assert
      expect(result.success).toBe(false)
      expect(result.code).toBe('VALIDATION_ERROR')
    })

    it('returns validation error for missing userId', async () => {
      // Arrange
      const input = {
        name: faker.company.name(),
      }

      // Act
      const result = await createAccount(input as any)

      // Assert
      expect(result.success).toBe(false)
      expect(result.code).toBe('VALIDATION_ERROR')
    })
  })

  describe('findAccountById', () => {
    it('finds an existing account', async () => {
      // Arrange
      const createResult = await createAccount({
        userId: testUserId,
        name: faker.company.name(),
      })
      const accountId = createResult.data!.id

      // Act
      const result = await findAccountById(accountId, testUserId)

      // Assert
      expect(result.success).toBe(true)
      expect(result.data?.id).toBe(accountId)
      expect(result.data?.userId).toBe(testUserId)
    })

    it('returns null for non-existent account', async () => {
      // Act
      const result = await findAccountById(faker.string.ulid(), testUserId)

      // Assert
      expect(result.success).toBe(true)
      expect(result.data).toBeNull()
    })

    it('returns null when userId does not match', async () => {
      // Arrange
      const createResult = await createAccount({
        userId: testUserId,
        name: faker.company.name(),
      })
      const accountId = createResult.data!.id
      const differentUserId = faker.string.ulid()

      // Act
      const result = await findAccountById(accountId, differentUserId)

      // Assert
      expect(result.success).toBe(true)
      expect(result.data).toBeNull()
    })
  })

  describe('findAccountsByUser', () => {
    it('returns empty array when no accounts exist', async () => {
      // Act
      const result = await findAccountsByUser(testUserId)

      // Assert
      expect(result.success).toBe(true)
      expect(result.data?.items).toEqual([])
      expect(result.data?.hasMore).toBe(false)
    })

    it('returns all accounts for user', async () => {
      // Arrange
      await createAccount({ userId: testUserId, name: 'Account 1' })
      await createAccount({ userId: testUserId, name: 'Account 2' })
      await createAccount({ userId: testUserId, name: 'Account 3' })

      // Act
      const result = await findAccountsByUser(testUserId)

      // Assert
      expect(result.success).toBe(true)
      expect(result.data?.items).toHaveLength(3)
    })

    it('returns paginated results', async () => {
      // Arrange
      await createAccount({ userId: testUserId, name: 'Account 1' })
      await createAccount({ userId: testUserId, name: 'Account 2' })
      await createAccount({ userId: testUserId, name: 'Account 3' })

      // Act - First page
      const page1 = await findAccountsByUser(testUserId, { limit: 2 })

      // Assert
      expect(page1.success).toBe(true)
      expect(page1.data?.items).toHaveLength(2)
      expect(page1.data?.hasMore).toBe(true)
      expect(page1.data?.nextCursor).toBeDefined()

      // Act - Second page
      const page2 = await findAccountsByUser(testUserId, {
        limit: 2,
        cursor: page1.data!.nextCursor,
      })

      // Assert
      expect(page2.success).toBe(true)
      expect(page2.data?.items).toHaveLength(1)
      expect(page2.data?.hasMore).toBe(false)
    })

    it('does not return accounts from other users', async () => {
      // Arrange
      const otherUserId = faker.string.ulid()
      await createAccount({ userId: testUserId, name: 'My Account' })
      await createAccount({ userId: otherUserId, name: 'Other Account' })

      // Act
      const result = await findAccountsByUser(testUserId)

      // Assert
      expect(result.success).toBe(true)
      expect(result.data?.items).toHaveLength(1)
      expect(result.data?.items[0].name).toBe('My Account')
    })
  })

  describe('updateAccount', () => {
    it('updates an existing account', async () => {
      // Arrange
      const createResult = await createAccount({
        userId: testUserId,
        name: 'Original Name',
      })
      const accountId = createResult.data!.id

      // Act
      const result = await updateAccount(accountId, testUserId, {
        name: 'Updated Name',
        status: 'inactive',
      })

      // Assert
      expect(result.success).toBe(true)
      expect(result.data?.name).toBe('Updated Name')
      expect(result.data?.status).toBe('inactive')
    })

    it('returns error for non-existent account', async () => {
      // Act
      const result = await updateAccount(
        faker.string.ulid(),
        testUserId,
        { name: 'Updated' }
      )

      // Assert
      expect(result.success).toBe(false)
      expect(result.code).toBe('ACCOUNT_NOT_FOUND')
    })
  })

  describe('deleteAccount', () => {
    it('deletes an existing account', async () => {
      // Arrange
      const createResult = await createAccount({
        userId: testUserId,
        name: faker.company.name(),
      })
      const accountId = createResult.data!.id

      // Act
      const result = await deleteAccount(accountId, testUserId)

      // Assert
      expect(result.success).toBe(true)

      // Verify deleted
      const findResult = await findAccountById(accountId, testUserId)
      expect(findResult.data).toBeNull()
    })
  })
})
```

## Server Action Test Pattern

```typescript
// actions/create-account.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { faker } from '@faker-js/faker'
import { createAccountAction } from './create-account'
import * as dalModule from '../dal'

// Mock the DAL module
vi.mock('../dal', () => ({
  createAccount: vi.fn(),
}))

describe('createAccountAction', () => {
  const mockUserId = faker.string.ulid()
  const mockCtx = {
    user: { id: mockUserId },
  }

  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('creates account successfully', async () => {
    // Arrange
    const input = {
      name: faker.company.name(),
      description: faker.lorem.sentence(),
    }

    const mockAccount = {
      id: faker.string.ulid(),
      ...input,
      userId: mockUserId,
      status: 'active',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    }

    vi.mocked(dalModule.createAccount).mockResolvedValue({
      success: true,
      data: mockAccount,
    })

    // Act
    const result = await createAccountAction.handler({
      input,
      ctx: mockCtx,
    })

    // Assert
    expect(dalModule.createAccount).toHaveBeenCalledWith({
      ...input,
      userId: mockUserId,
    })
    expect(result).toEqual(mockAccount)
  })

  it('throws error when DAL returns failure', async () => {
    // Arrange
    const input = { name: faker.company.name() }

    vi.mocked(dalModule.createAccount).mockResolvedValue({
      success: false,
      error: 'Database error',
      code: 'CREATE_ACCOUNT_ERROR',
    })

    // Act & Assert
    await expect(
      createAccountAction.handler({ input, ctx: mockCtx })
    ).rejects.toThrow('Database error')
  })

  it('validates input with Zod schema', async () => {
    // Arrange
    const invalidInput = { name: '' } // Empty name should fail

    // Act & Assert
    await expect(
      createAccountAction.handler({ input: invalidInput, ctx: mockCtx })
    ).rejects.toThrow()
  })
})
```

## Service Layer Test Pattern

```typescript
// service/accounts-service.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { faker } from '@faker-js/faker'
import { accountsService } from './accounts-service'
import * as dalModule from '../dal'

// Mock the DAL module
vi.mock('../dal', () => ({
  findAccountById: vi.fn(),
  findAccountsByUser: vi.fn(),
}))

describe('accountsService', () => {
  const testUserId = faker.string.ulid()

  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('getAccountById', () => {
    it('returns account summary when found', async () => {
      // Arrange
      const mockAccount = {
        id: faker.string.ulid(),
        name: faker.company.name(),
        status: 'active',
        description: faker.lorem.sentence(),
        userId: testUserId,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      }

      vi.mocked(dalModule.findAccountById).mockResolvedValue({
        success: true,
        data: mockAccount,
      })

      // Act
      const result = await accountsService.getAccountById(mockAccount.id, testUserId)

      // Assert
      expect(result).toEqual({
        id: mockAccount.id,
        name: mockAccount.name,
        status: mockAccount.status,
      })
      // Verify only necessary fields are exposed
      expect(result).not.toHaveProperty('description')
      expect(result).not.toHaveProperty('userId')
    })

    it('returns null when account not found', async () => {
      // Arrange
      vi.mocked(dalModule.findAccountById).mockResolvedValue({
        success: true,
        data: null,
      })

      // Act
      const result = await accountsService.getAccountById(
        faker.string.ulid(),
        testUserId
      )

      // Assert
      expect(result).toBeNull()
    })

    it('returns null when DAL returns error', async () => {
      // Arrange
      vi.mocked(dalModule.findAccountById).mockResolvedValue({
        success: false,
        error: 'Database error',
        code: 'FIND_ERROR',
      })

      // Act
      const result = await accountsService.getAccountById(
        faker.string.ulid(),
        testUserId
      )

      // Assert
      expect(result).toBeNull()
    })
  })

  describe('accountExists', () => {
    it('returns true when account exists', async () => {
      // Arrange
      vi.mocked(dalModule.findAccountById).mockResolvedValue({
        success: true,
        data: { id: faker.string.ulid() } as any,
      })

      // Act
      const result = await accountsService.accountExists(
        faker.string.ulid(),
        testUserId
      )

      // Assert
      expect(result).toBe(true)
    })

    it('returns false when account does not exist', async () => {
      // Arrange
      vi.mocked(dalModule.findAccountById).mockResolvedValue({
        success: true,
        data: null,
      })

      // Act
      const result = await accountsService.accountExists(
        faker.string.ulid(),
        testUserId
      )

      // Assert
      expect(result).toBe(false)
    })
  })
})
```

## Cross-Feature Mocking Pattern

**CRITICAL**: Never import from another feature's DAL. Mock the service layer instead.

### When Feature A Tests Need Feature B Data

**BAD**:
```typescript
// In billing feature test
import { createAccount } from '@/features/accounts/dal' // VIOLATION!

it('creates invoice for account', async () => {
  await createAccount({ ... }) // Direct DAL access
})
```

**GOOD**:
```typescript
// In billing feature test
import { accountsService } from '@/features/accounts'
import { vi } from 'vitest'

vi.mock('@/features/accounts', () => ({
  accountsService: {
    getAccountById: vi.fn(),
    accountExists: vi.fn(),
  },
}))

it('creates invoice for account', async () => {
  // Mock the service layer response
  vi.mocked(accountsService.accountExists).mockResolvedValue(true)
  vi.mocked(accountsService.getAccountById).mockResolvedValue({
    id: 'account-123',
    name: 'Test Account',
    status: 'active',
  })

  // Now test billing logic
  const result = await createInvoice({ accountId: 'account-123', ... })
  expect(result.success).toBe(true)
})
```

## HTTP Mocking with MSW (for External APIs)

```typescript
// test/mocks/handlers.ts
import { http, HttpResponse } from 'msw'

export const handlers = [
  // Mock Stripe API
  http.post('https://api.stripe.com/v1/customers', () => {
    return HttpResponse.json({
      id: 'cus_test123',
      email: 'test@example.com',
    })
  }),

  // Mock SendGrid API
  http.post('https://api.sendgrid.com/v3/mail/send', () => {
    return HttpResponse.json({ message: 'success' })
  }),
]
```

```typescript
// test/setup.ts
import { setupServer } from 'msw/node'
import { handlers } from './mocks/handlers'
import { beforeAll, afterAll, afterEach } from 'vitest'

const server = setupServer(...handlers)

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }))
afterAll(() => server.close())
afterEach(() => server.resetHandlers())
```

## Test Lifecycle Hooks

### beforeAll - Setup Database

```typescript
beforeAll(async () => {
  await setupTestDb()
})
```

### afterAll - Cleanup Database

```typescript
afterAll(async () => {
  await cleanupTestDb()
})
```

### beforeEach - Clear Test Data

```typescript
beforeEach(async () => {
  await clearTestData('Account')
  vi.clearAllMocks()
})
```

### afterEach - Reset Mocks

```typescript
afterEach(() => {
  vi.restoreAllMocks()
})
```

## Test Data Factory Pattern

```typescript
// test/factories/account-factory.ts
import { faker } from '@faker-js/faker'
import type { AccountEntity, CreateAccountInput } from '@/features/accounts/model/account-schemas'

export const accountFactory = {
  build(overrides: Partial<AccountEntity> = {}): AccountEntity {
    return {
      id: faker.string.ulid(),
      userId: faker.string.ulid(),
      name: faker.company.name(),
      description: faker.lorem.sentence(),
      status: 'active',
      metadata: {},
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      ...overrides,
    }
  },

  buildCreateInput(overrides: Partial<CreateAccountInput> = {}): CreateAccountInput {
    return {
      name: faker.company.name(),
      description: faker.lorem.sentence(),
      ...overrides,
    }
  },
}
```

Usage:

```typescript
import { accountFactory } from '@/test/factories/account-factory'

it('creates account', async () => {
  const input = accountFactory.buildCreateInput({ name: 'Custom Name' })
  const result = await createAccount({ ...input, userId: testUserId })
  expect(result.success).toBe(true)
})
```

## Anti-Patterns to Avoid

### Cross-Feature DAL Imports in Tests (CRITICAL)

**BAD**:
```typescript
// In billing test
import { createAccount } from '@/features/accounts/dal'
```

**GOOD**:
```typescript
// Mock the service layer instead
vi.mock('@/features/accounts', () => ({
  accountsService: { getAccountById: vi.fn() },
}))
```

### Using Jest Instead of Vitest

**BAD**:
```typescript
import { jest } from '@jest/globals'
jest.mock(...)
```

**GOOD**:
```typescript
import { vi } from 'vitest'
vi.mock(...)
```

### Tests in `__test__` Folder

**BAD**:
```
src/features/accounts/__test__/create-account.test.ts
```

**GOOD**:
```
src/features/accounts/dal/create_account.test.ts
```

### Missing RepositoryResult Assertions

**BAD**:
```typescript
it('creates account', async () => {
  const result = await createAccount(input)
  expect(result.id).toBeDefined() // Assumes success
})
```

**GOOD**:
```typescript
it('creates account', async () => {
  const result = await createAccount(input)
  expect(result.success).toBe(true)
  expect(result.data?.id).toBeDefined()
})
```

## Test Isolation Verification

### Detection Command for Test Files

```bash
# Find cross-feature DAL imports in test files
grep -r "from '@/features/[^']*dal'" src/features/**/*.test.ts | \
  awk -F: '{
    match($1, /features\/([^/]+)/, feat);
    match($2, /features\/([^/]+)\/dal/, imported);
    if (feat[1] != imported[1] && imported[1] != "") {
      print "VIOLATION: " $1 " imports from " imported[1] "/dal"
    }
  }'
```

**Expected**: Empty output

### Verification Script

```bash
#!/bin/bash
# verify-test-isolation.sh <feature-name>

FEATURE=$1
echo "Verifying test isolation for: $FEATURE"

# Check for cross-feature DAL imports in tests
VIOLATIONS=$(grep -r "from '@/features/" src/features/$FEATURE/**/*.test.ts 2>/dev/null | \
  grep "/dal'" | \
  grep -v "@/features/$FEATURE")

if [ ! -z "$VIOLATIONS" ]; then
  echo "CRITICAL: Cross-feature DAL imports found in tests:"
  echo "$VIOLATIONS"
  exit 1
fi

echo "Test isolation verified"
```

## Coverage Requirements

| Metric | Minimum | Target |
|--------|---------|--------|
| Branches | 70% | 80% |
| Functions | 75% | 85% |
| Lines | 75% | 85% |
| Statements | 75% | 85% |

### Priority Order for Coverage

1. **DAL functions** (High) - Core data operations
2. **Service layer** (High) - Cross-feature contracts
3. **Server actions** (Medium) - Input validation
4. **Error handling** (Medium) - Edge cases

## CI/CD Integration

### GitHub Actions Workflow

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      dynamodb-local:
        image: amazon/dynamodb-local:latest
        ports:
          - 8000:8000

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Verify Test Isolation
        run: |
          VIOLATIONS=$(grep -r "from '@/features/" src/features/**/*.test.ts 2>/dev/null | \
            grep "/dal'" | \
            awk -F: '{
              match($1, /features\/([^/]+)/, feat);
              match($2, /features\/([^/]+)\/dal/, imported);
              if (feat[1] != imported[1] && imported[1] != "") {
                print "VIOLATION: " $1
              }
            }')
          if [ ! -z "$VIOLATIONS" ]; then
            echo "$VIOLATIONS"
            exit 1
          fi

      - name: Run Tests
        run: npm test
        env:
          DYNAMODB_LOCAL_ENDPOINT: http://localhost:8000
          TEST_TABLE_NAME: test-table

      - name: Upload Coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage/lcov.info
```

## Running Tests

```bash
# Run all tests
npx vitest

# Run tests for specific feature
npx vitest src/features/accounts

# Run tests in watch mode
npx vitest --watch

# Run with coverage
npx vitest --coverage

# Run specific test file
npx vitest src/features/accounts/dal/create_account.test.ts
```

## References

- Vitest Documentation: https://vitest.dev
- DynamoDB Local: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html
- MSW Documentation: https://mswjs.io
- Testing Patterns: `docs/TESTING-PATTERNS.md`
- State Isolation: `docs/STATE-ISOLATION.md`
