---
name: dynamodb-onetable
description: Guide for DynamoDB single-table design using OneTable ORM. Use when designing database schemas, writing DAL functions, creating queries, or handling schema evolution in DynamoDB.
---

# DynamoDB Single-Table Design with OneTable

## Key Design Patterns

| Access Pattern | pk | sk | Index |
|---------------|----|----|-------|
| User's items | `USER#${userId}` | `ITEM#${id}` | primary |
| Item by ID | `ITEM#${id}` | `USER#${userId}` | gsi1 |
| Hierarchical | `USER#${userId}` | `PARENT#${parentId}#${id}` | primary |
| By date | `USER#${userId}` | `DATE#${date}#${id}` | primary |

## Schema Definition

```typescript
// db-schema.ts
export const Schema = {
  format: 'onetable:1.1.0',
  version: '0.0.1',
  indexes: {
    primary: { hash: 'pk', sort: 'sk' },
    gsi1: { hash: 'gsi1pk', sort: 'gsi1sk', project: 'all' },
  },
  models: {
    Account: {
      pk: { type: String, value: 'USER#${userId}' },
      sk: { type: String, value: 'ACCOUNT#${id}' },
      gsi1pk: { type: String, value: 'ACCOUNT#${id}' },
      gsi1sk: { type: String, value: 'USER#${userId}' },
      id: { type: String, required: true, generate: 'ulid' },
      userId: { type: String, required: true },
      name: { type: String, required: true },
      balance: { type: Number, default: 0 },
      deleted: { type: Boolean, default: false },
    },
  },
}
```

## DAL Functions

**File naming:** `snake_case` (e.g., `create_account.ts`, `find_by_id.ts`)

**Location:** `features/<feature>/dal/`

**No 'server-only'** - DAL must work in Lambda and Next.js

### Create

```typescript
// dal/create_account.ts
import { ulid } from 'ulid'
import { log } from '@saas4dev/core'

export async function create_account(
  userId: string,
  input: { name: string }
): Promise<Result<Account>> {
  try {
    const entity = await AccountEntity.create({
      id: ulid(),
      userId,
      ...input,
    })
    return { success: true, data: entityToAccount(entity) }
  } catch (error) {
    log.error('[create_account]', { error, userId })
    return { success: false, error: 'Failed to create' }
  }
}
```

### Read

```typescript
// dal/find_account_by_id.ts
export async function find_account_by_id(id: string): Promise<Result<Account | null>> {
  try {
    const entity = await AccountEntity.get(
      { gsi1pk: `ACCOUNT#${id}` },
      { index: 'gsi1' }
    )
    if (!entity || entity.deleted) return { success: true, data: null }
    return { success: true, data: entityToAccount(entity) }
  } catch (error) {
    log.error('[find_account_by_id]', { error, id })
    return { success: false, error: 'Failed to find' }
  }
}
```

### List with Query

```typescript
// dal/list_accounts_by_user.ts
export async function list_accounts_by_user(userId: string): Promise<Result<Account[]>> {
  try {
    const entities = await AccountEntity.find(
      { pk: `USER#${userId}`, sk: { begins: 'ACCOUNT#' } },
      { where: '${deleted} <> {true}' }
    )
    return { success: true, data: entities.map(entityToAccount) }
  } catch (error) {
    log.error('[list_accounts_by_user]', { error, userId })
    return { success: false, error: 'Failed to list' }
  }
}
```

### Soft Delete

```typescript
// dal/delete_account.ts
export async function delete_account(id: string): Promise<Result<void>> {
  try {
    await AccountEntity.update(
      { gsi1pk: `ACCOUNT#${id}` },
      { set: { deleted: true, updatedAt: new Date() }, index: 'gsi1' }
    )
    return { success: true }
  } catch (error) {
    log.error('[delete_account]', { error, id })
    return { success: false, error: 'Failed to delete' }
  }
}
```

## Entity-to-Model Converter

Always convert entities to domain models:

```typescript
function entityToAccount(entity: any): Account {
  return {
    id: entity.id,
    userId: entity.userId,
    name: entity.name,
    balance: entity.balance ?? 0,        // Handle missing fields
    deleted: entity.deleted ?? false,
    createdAt: entity.createdAt ?? new Date(),
    updatedAt: entity.updatedAt ?? new Date(),
  }
}
```

## Schema Evolution

**Adding fields:** Always optional with defaults
```typescript
// GOOD
newField: { type: String, default: '' }

// BAD - breaks existing records
newField: { type: String, required: true }
```

**Process:**
1. Add field as optional with default
2. Update entity-to-model converter
3. Deploy
4. Backfill if needed

## Rules

- Use ULID for IDs (time-sortable)
- Always soft delete (`deleted: true`)
- Log errors with context
- Return `{ success, data?, error? }` format
- Handle missing fields in converters
