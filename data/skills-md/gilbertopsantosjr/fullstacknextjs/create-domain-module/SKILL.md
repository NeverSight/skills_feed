---
description: Creates complete, production-ready feature modules following the 10 architectural principles, with emphasis on state isolation, service layer patterns, and runtime-agnostic design for deployment flexibility. Adapted for Next.js 15+, DynamoDB/OneTable, ZSA, and Vitest.
name: create-domain-module
---

# Feature Module Generator (Next.js + DynamoDB)

You are an expert in creating feature modules that comply with the 10 architectural principles, emphasizing state isolation, well-defined boundaries, and deployment independence. This skill is adapted for the modern stack: Next.js 15+, DynamoDB with OneTable, ZSA server actions, and Vitest.

## Technology Stack

| Component | Technology |
|-----------|------------|
| Framework | Next.js 15+ / React 19+ |
| Database | DynamoDB (single-table design) |
| ORM | OneTable |
| Server Actions | ZSA (Zod Server Actions) |
| Validation | Zod schemas |
| Testing | Vitest |
| ID Generation | ULID |
| Deployment | SST (Serverless Stack) |

## Core Principles Applied

This skill enforces these critical architectural principles:

| # | Principle | How Applied |
|---|-----------|-------------|
| 1 | **Well-Defined Boundaries** | Clear feature exports, internal data hidden via service layer |
| 3 | **Independence** | No cross-feature DAL imports, autonomous operation |
| 5 | **Explicit Communication** | Service layer defines public API contracts |
| 7 | **Deployment Independence** | Runtime-agnostic DAL works in Next.js, Lambda, or queues |
| 8 | **State Isolation** | Feature-prefixed DynamoDB keys (pk/sk patterns) |

**CRITICAL**: State Isolation (Principle 8) is the most frequently violated principle. Feature-prefixed DynamoDB key patterns are MANDATORY.

## When to Use This Skill

Use this skill when:

- Creating a new feature module from scratch
- User asks to "create a feature", "scaffold a feature", or "generate a module"
- User mentions needing a new business domain (accounts, billing, notifications, etc.)
- Starting a new bounded context that needs its own data and logic

## Requirements Gathering

Before generating any code, ask the user these questions using the AskQuestion tool:

1. **Feature name** (kebab-case, e.g., "accounts", "billing", "notifications")
2. **Initial entities** (comma-separated list, e.g., "Account, Transaction, Balance")
3. **External integrations** (any third-party services? e.g., "Stripe, SendGrid")
4. **Cross-feature access needed?** (will other features need to access this feature's data?)
5. **Key access patterns** (how will data be queried? e.g., "by userId", "by date range")

## Folder Structure Generation

Generate this structure for feature modules:

```
src/features/<feature-name>/
├── actions/                     # Server actions (ZSA pattern)
│   ├── create-<entity>.ts       # kebab-case files
│   ├── update-<entity>.ts
│   ├── delete-<entity>.ts
│   ├── get-<entity>.ts
│   └── index.ts                 # Public action exports
├── dal/                         # Data Access Layer (runtime-agnostic)
│   ├── create_<entity>.ts       # snake_case files
│   ├── find_<entity>_by_id.ts
│   ├── find_<entity>s_by_user.ts
│   ├── update_<entity>.ts
│   ├── delete_<entity>.ts
│   ├── <entity>.test.ts         # Co-located tests
│   └── index.ts                 # DAL exports
├── service/                     # Public API for cross-feature access
│   └── <feature>-service.ts
├── model/                       # Zod schemas and types
│   ├── <feature>-schemas.ts     # Input/output schemas
│   ├── <feature>-types.ts       # TypeScript types
│   └── <feature>-constants.ts   # Feature constants
├── components/                  # UI components (if needed)
│   ├── <entity>-form.tsx
│   ├── <entity>-list.tsx
│   └── index.ts
├── hooks/                       # React hooks (if needed)
│   └── use-<entity>.ts
└── index.ts                     # Public feature exports
```

## Component Generation Instructions

### 1. DynamoDB Schema (in `src/features/database/db-schema.ts`)

Add the entity model to the shared schema:

```typescript
// Add to existing db-schema.ts
export const schema = {
  // ... existing models

  {EntityName}: {
    pk: { type: String, value: 'USER#${userId}' },
    sk: { type: String, value: '{FEATURE}#{entityName}#${id}' },
    id: { type: String, required: true, generate: 'ulid' },
    userId: { type: String, required: true },
    // Add entity-specific fields
    name: { type: String, required: true },
    description: { type: String },
    status: { type: String, enum: ['{EntityName}Status'], default: 'active' },
    metadata: { type: Object },

    // Standard timestamps
    createdAt: { type: String },
    updatedAt: { type: String },

    // GSI for queries
    gs1pk: { type: String, value: '{FEATURE}#${status}' },
    gs1sk: { type: String, value: '${createdAt}' },
  },
} as const
```

**Key Pattern Rules**:
- **pk**: Always starts with entity type (e.g., `USER#`, `ACCOUNT#`)
- **sk**: Feature prefix + entity type + ID (e.g., `ACCOUNTS#account#01HXYZ...`)
- **GSI patterns**: For alternate access patterns (by status, by date, etc.)

### 2. Zod Schemas (model/<feature>-schemas.ts)

```typescript
import { z } from 'zod'

// Base entity schema (what comes from DB)
export const {EntityName}Schema = z.object({
  id: z.string().ulid(),
  userId: z.string().ulid(),
  name: z.string().min(1).max(255),
  description: z.string().max(1000).optional(),
  status: z.enum(['active', 'inactive', 'archived']).default('active'),
  metadata: z.record(z.unknown()).optional(),
  createdAt: z.string().datetime(),
  updatedAt: z.string().datetime(),
})

export type {EntityName}Entity = z.infer<typeof {EntityName}Schema>

// Create input schema (what client sends)
export const Create{EntityName}Schema = z.object({
  name: z.string().min(1).max(255),
  description: z.string().max(1000).optional(),
  metadata: z.record(z.unknown()).optional(),
})

export type Create{EntityName}Input = z.infer<typeof Create{EntityName}Schema>

// Update input schema
export const Update{EntityName}Schema = z.object({
  name: z.string().min(1).max(255).optional(),
  description: z.string().max(1000).optional(),
  status: z.enum(['active', 'inactive', 'archived']).optional(),
  metadata: z.record(z.unknown()).optional(),
})

export type Update{EntityName}Input = z.infer<typeof Update{EntityName}Schema>

// Query params schema
export const {EntityName}QuerySchema = z.object({
  status: z.enum(['active', 'inactive', 'archived']).optional(),
  limit: z.coerce.number().min(1).max(100).default(20),
  cursor: z.string().optional(),
})

export type {EntityName}QueryParams = z.infer<typeof {EntityName}QuerySchema>
```

### 3. DAL Functions (dal/create_<entity>.ts)

**CRITICAL**: DAL files must be runtime-agnostic (NO `'server-only'` import).

```typescript
// dal/create_account.ts
import { getDynamoDbTable } from '@/features/database/db-config'
import { Create{EntityName}Schema, type Create{EntityName}Input, type {EntityName}Entity } from '../model/{feature}-schemas'
import type { RepositoryResult } from '@/types'
import { ZodError } from 'zod'
import { log } from '@/lib/logger'

export const create{EntityName} = async (
  input: Create{EntityName}Input & { userId: string }
): Promise<RepositoryResult<{EntityName}Entity>> => {
  const startTime = Date.now()

  try {
    // Validate input
    const validatedInput = Create{EntityName}Schema.extend({
      userId: z.string().ulid(),
    }).parse(input)

    // Get the model from OneTable
    const {EntityName}Model = getDynamoDbTable().getModel('{EntityName}')

    // Create the entity
    const entity = await {EntityName}Model.create({
      userId: validatedInput.userId,
      name: validatedInput.name,
      description: validatedInput.description,
      metadata: validatedInput.metadata,
      status: 'active',
    })

    log.debug('[{EntityName}.create] Success', {
      id: entity.id,
      userId: entity.userId,
      duration: Date.now() - startTime,
    })

    return { success: true, data: entity as {EntityName}Entity }
  } catch (error) {
    log.error('[{EntityName}.create] Failed', { error, duration: Date.now() - startTime })

    if (error instanceof ZodError) {
      return {
        success: false,
        error: error.errors,
        code: 'VALIDATION_ERROR'
      }
    }

    return {
      success: false,
      error: 'Failed to create {entityName}',
      code: 'CREATE_{ENTITY_NAME}_ERROR'
    }
  }
}
```

**DAL Pattern Rules**:
- Files use **snake_case**: `create_account.ts`, `find_account_by_id.ts`
- Functions use **camelCase**: `createAccount()`, `findAccountById()`
- Return `RepositoryResult<T>` for consistent error handling
- NO `'server-only'` import - DAL must work in Lambda
- Include logging with timing
- Handle Zod validation errors explicitly

### 4. DAL Query Functions (dal/find_<entity>_by_id.ts)

```typescript
// dal/find_account_by_id.ts
import { getDynamoDbTable } from '@/features/database/db-config'
import type { {EntityName}Entity } from '../model/{feature}-schemas'
import type { RepositoryResult } from '@/types'
import { log } from '@/lib/logger'

export const find{EntityName}ById = async (
  id: string,
  userId: string
): Promise<RepositoryResult<{EntityName}Entity | null>> => {
  const startTime = Date.now()

  try {
    const {EntityName}Model = getDynamoDbTable().getModel('{EntityName}')

    const entity = await {EntityName}Model.get({
      pk: `USER#${userId}`,
      sk: `{FEATURE}#{entityName}#${id}`,
    })

    log.debug('[{EntityName}.findById] Complete', {
      id,
      found: !!entity,
      duration: Date.now() - startTime,
    })

    return { success: true, data: entity as {EntityName}Entity | null }
  } catch (error) {
    log.error('[{EntityName}.findById] Failed', { error, id, duration: Date.now() - startTime })

    return {
      success: false,
      error: 'Failed to find {entityName}',
      code: 'FIND_{ENTITY_NAME}_ERROR'
    }
  }
}
```

### 5. DAL List Functions (dal/find_<entity>s_by_user.ts)

```typescript
// dal/find_accounts_by_user.ts
import { getDynamoDbTable } from '@/features/database/db-config'
import { {EntityName}QuerySchema, type {EntityName}QueryParams, type {EntityName}Entity } from '../model/{feature}-schemas'
import type { RepositoryResult, PaginatedResult } from '@/types'
import { log } from '@/lib/logger'

export const find{EntityName}sByUser = async (
  userId: string,
  params: {EntityName}QueryParams = {}
): Promise<RepositoryResult<PaginatedResult<{EntityName}Entity>>> => {
  const startTime = Date.now()

  try {
    const validatedParams = {EntityName}QuerySchema.parse(params)
    const {EntityName}Model = getDynamoDbTable().getModel('{EntityName}')

    const queryOptions: any = {
      pk: `USER#${userId}`,
      sk: { begins: '{FEATURE}#{entityName}#' },
      limit: validatedParams.limit,
    }

    if (validatedParams.cursor) {
      queryOptions.start = JSON.parse(Buffer.from(validatedParams.cursor, 'base64').toString())
    }

    const result = await {EntityName}Model.find(queryOptions)

    const nextCursor = result.next
      ? Buffer.from(JSON.stringify(result.next)).toString('base64')
      : undefined

    log.debug('[{EntityName}.findByUser] Complete', {
      userId,
      count: result.length,
      hasMore: !!nextCursor,
      duration: Date.now() - startTime,
    })

    return {
      success: true,
      data: {
        items: result as {EntityName}Entity[],
        nextCursor,
        hasMore: !!nextCursor,
      }
    }
  } catch (error) {
    log.error('[{EntityName}.findByUser] Failed', { error, userId, duration: Date.now() - startTime })

    return {
      success: false,
      error: 'Failed to find {entityName}s',
      code: 'FIND_{ENTITY_NAME}S_ERROR'
    }
  }
}
```

### 6. DAL Index (dal/index.ts)

```typescript
// dal/index.ts
export { create{EntityName} } from './create_{entity_name}'
export { find{EntityName}ById } from './find_{entity_name}_by_id'
export { find{EntityName}sByUser } from './find_{entity_name}s_by_user'
export { update{EntityName} } from './update_{entity_name}'
export { delete{EntityName} } from './delete_{entity_name}'
```

### 7. Server Actions (actions/create-<entity>.ts)

**Server actions MUST be lean (<20 lines in handler).**

```typescript
// actions/create-account.ts
'use server'
import 'server-only'
import { authedProcedure } from '@/lib/zsa'
import { Create{EntityName}Schema } from '../model/{feature}-schemas'
import { create{EntityName} } from '../dal'

export const create{EntityName}Action = authedProcedure
  .input(Create{EntityName}Schema)
  .handler(async ({ input, ctx }) => {
    const result = await create{EntityName}({
      ...input,
      userId: ctx.user.id,
    })

    if (!result.success) {
      throw new Error(result.error as string)
    }

    return result.data
  })
```

**Server Action Rules**:
- Files use **kebab-case**: `create-account.ts`
- Always include `'use server'` and `import 'server-only'`
- Use `authedProcedure` for authenticated actions
- Use `publicProcedure` for unauthenticated actions
- Handler should be <20 lines
- Delegate ALL business logic to DAL
- Transform `RepositoryResult` to action response

### 8. Server Actions for Queries (actions/get-<entity>.ts)

```typescript
// actions/get-account.ts
'use server'
import 'server-only'
import { authedProcedure } from '@/lib/zsa'
import { z } from 'zod'
import { find{EntityName}ById } from '../dal'

export const get{EntityName}Action = authedProcedure
  .input(z.object({ id: z.string().ulid() }))
  .handler(async ({ input, ctx }) => {
    const result = await find{EntityName}ById(input.id, ctx.user.id)

    if (!result.success) {
      throw new Error(result.error as string)
    }

    if (!result.data) {
      throw new Error('{EntityName} not found')
    }

    return result.data
  })
```

### 9. Service Layer (service/<feature>-service.ts)

**CRITICAL**: Create service layer if other features need access to this feature's data.

```typescript
// service/accounts-service.ts
import { find{EntityName}ById, find{EntityName}sByUser } from '../dal'
import type { {EntityName}Entity } from '../model/{feature}-schemas'

/**
 * Public API for cross-feature access.
 * Other features import this service, NEVER the DAL directly.
 *
 * @example
 * // In another feature:
 * import { {featureName}Service } from '@/features/{feature-name}'
 * const account = await {featureName}Service.get{EntityName}ById(id, userId)
 */
export const {featureName}Service = {
  /**
   * Get entity by ID (simplified return for external callers)
   * Returns null if not found instead of throwing
   */
  async get{EntityName}ById(id: string, userId: string): Promise<{EntityName}Summary | null> {
    const result = await find{EntityName}ById(id, userId)

    if (!result.success || !result.data) {
      return null
    }

    // Only expose necessary fields to other features
    return {
      id: result.data.id,
      name: result.data.name,
      status: result.data.status,
    }
  },

  /**
   * Check if entity exists (for validation from other features)
   */
  async {entityName}Exists(id: string, userId: string): Promise<boolean> {
    const result = await find{EntityName}ById(id, userId)
    return result.success && result.data !== null
  },

  /**
   * Get entities by user with pagination
   */
  async get{EntityName}sByUser(
    userId: string,
    options?: { limit?: number; cursor?: string }
  ): Promise<{EntityName}Summary[]> {
    const result = await find{EntityName}sByUser(userId, options)

    if (!result.success) {
      return []
    }

    return result.data.items.map(item => ({
      id: item.id,
      name: item.name,
      status: item.status,
    }))
  },
}

// Type for external consumption (limited fields)
export type {EntityName}Summary = {
  id: string
  name: string
  status: string
}
```

**Service Layer Rules**:
- Return simplified types (not full entities)
- Return `null` instead of throwing for not-found cases
- Only expose methods other features actually need
- Document each method with JSDoc
- Never expose DAL functions directly

### 10. Feature Index (index.ts)

```typescript
// index.ts - Public feature exports

// Actions (for use in components)
export {
  create{EntityName}Action,
  get{EntityName}Action,
  get{EntityName}sAction,
  update{EntityName}Action,
  delete{EntityName}Action,
} from './actions'

// Service layer (for cross-feature access)
export { {featureName}Service, type {EntityName}Summary } from './service/{feature}-service'

// Types (for TypeScript consumers)
export type {
  {EntityName}Entity,
  Create{EntityName}Input,
  Update{EntityName}Input,
} from './model/{feature}-schemas'

// Components (if any)
export { {EntityName}Form } from './components/{entity-name}-form'
export { {EntityName}List } from './components/{entity-name}-list'

// --------------------------------------------------------
// NEVER export: DAL functions, internal schemas, constants
// Other features MUST use the service layer for data access
// --------------------------------------------------------
```

### 11. Co-located Tests (dal/<entity>.test.ts)

```typescript
// dal/account.test.ts
import { describe, it, expect, beforeAll, afterAll, beforeEach } from 'vitest'
import { create{EntityName} } from './create_{entity_name}'
import { find{EntityName}ById } from './find_{entity_name}_by_id'
import { find{EntityName}sByUser } from './find_{entity_name}s_by_user'
import { setupTestDb, cleanupTestDb, clearTestData } from '@/test/db-helpers'

describe('{EntityName} DAL', () => {
  const testUserId = '01HXYZ123456789ABCDEFGHIJK'

  beforeAll(async () => {
    await setupTestDb()
  })

  afterAll(async () => {
    await cleanupTestDb()
  })

  beforeEach(async () => {
    await clearTestData('{EntityName}')
  })

  describe('create{EntityName}', () => {
    it('creates a new {entityName} successfully', async () => {
      const input = {
        userId: testUserId,
        name: 'Test {EntityName}',
        description: 'A test {entityName}',
      }

      const result = await create{EntityName}(input)

      expect(result.success).toBe(true)
      expect(result.data).toMatchObject({
        name: input.name,
        description: input.description,
        userId: testUserId,
        status: 'active',
      })
      expect(result.data?.id).toBeDefined()
    })

    it('returns validation error for invalid input', async () => {
      const input = {
        userId: testUserId,
        name: '', // Invalid: empty name
      }

      const result = await create{EntityName}(input)

      expect(result.success).toBe(false)
      expect(result.code).toBe('VALIDATION_ERROR')
    })
  })

  describe('find{EntityName}ById', () => {
    it('finds an existing {entityName}', async () => {
      // Arrange
      const createResult = await create{EntityName}({
        userId: testUserId,
        name: 'Test {EntityName}',
      })
      const entityId = createResult.data!.id

      // Act
      const result = await find{EntityName}ById(entityId, testUserId)

      // Assert
      expect(result.success).toBe(true)
      expect(result.data?.id).toBe(entityId)
    })

    it('returns null for non-existent {entityName}', async () => {
      const result = await find{EntityName}ById('nonexistent', testUserId)

      expect(result.success).toBe(true)
      expect(result.data).toBeNull()
    })
  })

  describe('find{EntityName}sByUser', () => {
    it('returns paginated results', async () => {
      // Arrange: Create multiple entities
      await Promise.all([
        create{EntityName}({ userId: testUserId, name: '{EntityName} 1' }),
        create{EntityName}({ userId: testUserId, name: '{EntityName} 2' }),
        create{EntityName}({ userId: testUserId, name: '{EntityName} 3' }),
      ])

      // Act
      const result = await find{EntityName}sByUser(testUserId, { limit: 2 })

      // Assert
      expect(result.success).toBe(true)
      expect(result.data?.items).toHaveLength(2)
      expect(result.data?.hasMore).toBe(true)
    })
  })
})
```

## Naming Conventions

### Files and Folders

| Type | Convention | Example |
|------|------------|---------|
| Feature folders | kebab-case | `src/features/user-accounts/` |
| Action files | kebab-case | `create-account.ts` |
| DAL files | snake_case | `create_account.ts` |
| Schema files | kebab-case | `account-schemas.ts` |
| Service files | kebab-case | `accounts-service.ts` |
| Test files | kebab-case | `account.test.ts` |
| Component files | kebab-case | `account-form.tsx` |

### Code

| Type | Convention | Example |
|------|------------|---------|
| DAL functions | camelCase | `createAccount()` |
| Action exports | camelCase + Action | `createAccountAction` |
| Service exports | camelCase + Service | `accountsService` |
| Zod schemas | PascalCase + Schema | `CreateAccountSchema` |
| Types | PascalCase | `AccountEntity`, `CreateAccountInput` |
| Constants | UPPER_SNAKE_CASE | `MAX_ACCOUNTS_PER_USER` |
| DynamoDB pk/sk | PREFIX#value | `USER#123`, `ACCOUNTS#account#456` |

## Common Anti-Patterns to Avoid

### Cross-Feature DAL Imports (CRITICAL VIOLATION)

**BAD**:
```typescript
// In billing feature
import { findAccountById } from '@/features/accounts/dal' // VIOLATION!
```

**GOOD**:
```typescript
// In billing feature
import { accountsService } from '@/features/accounts'
const account = await accountsService.getAccountById(id, userId)
```

### `'server-only'` in DAL (Breaks Lambda)

**BAD**:
```typescript
// dal/create_account.ts
import 'server-only' // VIOLATION - breaks Lambda deployment
import { getDynamoDbTable } from '@/features/database/db-config'
```

**GOOD**:
```typescript
// dal/create_account.ts
// NO 'server-only' here - DAL is runtime-agnostic
import { getDynamoDbTable } from '@/features/database/db-config'
```

### Fat Server Actions (>20 lines)

**BAD**:
```typescript
export const createAccountAction = authedProcedure
  .input(CreateAccountSchema)
  .handler(async ({ input, ctx }) => {
    // Validation logic here...
    // Business rules here...
    // Database operations here...
    // More logic...
    // 50+ lines
  })
```

**GOOD**:
```typescript
export const createAccountAction = authedProcedure
  .input(CreateAccountSchema)
  .handler(async ({ input, ctx }) => {
    const result = await createAccount({ ...input, userId: ctx.user.id })
    if (!result.success) throw new Error(result.error as string)
    return result.data
  })
```

### Generic DynamoDB Keys

**BAD**:
```typescript
pk: `${userId}`,           // No type prefix
sk: `${id}`,               // No feature prefix
```

**GOOD**:
```typescript
pk: `USER#${userId}`,                    // Type prefix
sk: `ACCOUNTS#account#${id}`,            // Feature + entity prefix
```

### Missing Service Layer

**BAD**:
```typescript
// index.ts
export { findAccountById } from './dal'  // Exposing DAL directly
```

**GOOD**:
```typescript
// index.ts
export { accountsService } from './service/accounts-service'
// DAL is NEVER exported
```

### Missing RepositoryResult Pattern

**BAD**:
```typescript
export const createAccount = async (input) => {
  const entity = await Model.create(input)
  return entity  // Direct return, no error handling
}
```

**GOOD**:
```typescript
export const createAccount = async (input): Promise<RepositoryResult<AccountEntity>> => {
  try {
    const entity = await Model.create(input)
    return { success: true, data: entity }
  } catch (error) {
    return { success: false, error: 'Failed to create', code: 'CREATE_ERROR' }
  }
}
```

## Verification Commands

After generating the feature, run these verification commands. **All checks MUST pass before claiming compliance.**

### Critical Checks (P0 - Must Pass)

#### 1. Cross-Feature DAL Imports (MOST CRITICAL)

```bash
# Find cross-feature DAL imports
grep -r "from '@/features/[^']*dal'" src/features/ | \
  awk -F: '{
    match($1, /features\/([^/]+)/, feat);
    match($2, /features\/([^/]+)\/dal/, imported);
    if (feat[1] != imported[1] && imported[1] != "") {
      print "VIOLATION: " $1 " imports from " imported[1] "/dal"
    }
  }'
```

**Expected**: Empty output (no cross-feature DAL imports)

#### 2. DAL Runtime-Agnostic (No 'server-only')

```bash
# Check for 'server-only' in DAL files
grep -l "server-only" src/features/*/dal/*.ts
```

**Expected**: Empty output (no 'server-only' in DAL)

#### 3. Lean Server Actions (<20 lines in handler)

```bash
# Check action file sizes
find src/features/{feature-name}/actions -name "*.ts" ! -name "index.ts" -exec wc -l {} \;
```

**Expected**: All files under 50 lines total

### High Priority Checks (P1)

#### 4. RepositoryResult Pattern

```bash
# Check DAL files return RepositoryResult
grep -L "RepositoryResult" src/features/{feature-name}/dal/*.ts | grep -v test | grep -v index
```

**Expected**: Empty output (all DAL functions return RepositoryResult)

#### 5. Service Layer Exists (if cross-feature access needed)

```bash
ls src/features/{feature-name}/service/*.ts
```

**Expected**: `{feature}-service.ts` exists

#### 6. DynamoDB Key Prefixes

```bash
# Check for proper key patterns in schema
grep -E "(pk|sk):" src/features/database/db-schema.ts | grep {FEATURE}
```

**Expected**: All pk/sk have proper prefixes

### Standard Checks (P2)

#### 7. Index Exports (No DAL)

```bash
# Check index.ts doesn't export dal
grep "from.*dal" src/features/{feature-name}/index.ts
```

**Expected**: Empty output (DAL never exported from index)

#### 8. Zod Schemas Exist

```bash
ls src/features/{feature-name}/model/*-schemas.ts
```

**Expected**: Schema file exists

#### 9. Tests Exist and Pass

```bash
# Run feature tests
npx vitest run src/features/{feature-name}
```

**Expected**: All tests pass

## Pre-Commit Verification Script

```bash
#!/bin/bash
# verify-feature.sh <feature-name>

FEATURE=$1
echo "Verifying feature: $FEATURE"

# P0: Cross-feature DAL imports
echo "Checking cross-feature DAL imports..."
VIOLATIONS=$(grep -r "from '@/features/" src/features/$FEATURE/ 2>/dev/null | grep "/dal'" | grep -v "@/features/$FEATURE")
if [ ! -z "$VIOLATIONS" ]; then
  echo "CRITICAL: Cross-feature DAL imports found:"
  echo "$VIOLATIONS"
  exit 1
fi

# P0: 'server-only' in DAL
echo "Checking DAL runtime-agnostic..."
SERVER_ONLY=$(grep -l "server-only" src/features/$FEATURE/dal/*.ts 2>/dev/null)
if [ ! -z "$SERVER_ONLY" ]; then
  echo "CRITICAL: 'server-only' found in DAL:"
  echo "$SERVER_ONLY"
  exit 1
fi

# P1: RepositoryResult pattern
echo "Checking RepositoryResult pattern..."
NO_RESULT=$(grep -L "RepositoryResult" src/features/$FEATURE/dal/*.ts 2>/dev/null | grep -v test | grep -v index)
if [ ! -z "$NO_RESULT" ]; then
  echo "WARNING: DAL files without RepositoryResult:"
  echo "$NO_RESULT"
fi

echo "Feature verification passed"
```

## Generation Process

Follow these steps in order:

1. **Gather requirements** using AskQuestion tool
2. **Create folder structure** with all necessary directories
3. **Add DynamoDB model** to db-schema.ts with proper key patterns
4. **Generate Zod schemas** for input validation and types
5. **Generate DAL functions** (snake_case files, RepositoryResult returns)
6. **Generate server actions** (kebab-case files, lean handlers)
7. **Generate service layer** if cross-feature access is needed
8. **Generate feature index** with public exports only
9. **Generate tests** co-located with DAL functions
10. **Run verification commands** to check compliance
11. **Report results** to user with next steps

## Success Criteria

A successfully generated feature should:

- Pass all verification commands (no violations)
- Have proper DynamoDB key patterns (pk/sk with prefixes)
- Have runtime-agnostic DAL (no `'server-only'`)
- Have lean server actions (<20 lines per handler)
- Return `RepositoryResult<T>` from all DAL functions
- Export only public APIs (no DAL in index.ts)
- Have service layer if other features need access
- Have passing tests for all DAL functions
- Follow all 10 architectural principles

## Next Steps After Generation

Inform the user to:

1. **Update db-schema.ts** with the new entity model
2. **Run tests** to verify DAL functions: `npx vitest run src/features/{feature-name}`
3. **Deploy schema changes** (if using SST): `npx sst deploy`
4. **Use in components**: Import from `@/features/{feature-name}`

## References

- Architecture Overview: `docs/ARCHITECTURE-OVERVIEW.md`
- State Isolation: `docs/STATE-ISOLATION.md`
- Coding Patterns: `docs/CODING-PATTERNS.md`
- DynamoDB Design: `docs/DYNAMODB-DESIGN.md`
- Testing Patterns: `docs/TESTING-PATTERNS.md`
