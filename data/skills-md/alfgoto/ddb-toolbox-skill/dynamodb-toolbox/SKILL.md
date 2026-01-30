---
name: dynamodb-toolbox
description: Guide for using DynamoDB-Toolbox v2 - the lightweight TypeScript library for DynamoDB with type-safe query building and schema validation. Use when implementing DynamoDB operations with the .build() pattern, defining Tables/Entities/Schemas, or working with commands like GetItem, PutItem, UpdateItem, DeleteItem, Query, Scan, BatchGet, BatchWrite, or Transactions. Triggers on DynamoDB-Toolbox imports, Entity/Table definitions, or .build() command patterns.
metadata:
  short-description: DynamoDB-Toolbox v2 type-safe query builder guidance
---

# DynamoDB-Toolbox v2

Type-safe query builder for DynamoDB with schema validation and the `.build()` pattern.

## Installation

```bash
npm install dynamodb-toolbox @aws-sdk/client-dynamodb @aws-sdk/lib-dynamodb
```

TypeScript 5+ with `"strict": true` in tsconfig.json is recommended.

## Core Concepts

### Import Pattern

Import directly from the main package:

```typescript
import {
  Table,
  Entity,
  item, string, number, boolean, binary, list, map, set, record, anyOf, any,
  GetItemCommand,
  PutItemCommand,
  UpdateItemCommand,
  DeleteItemCommand,
  QueryCommand,
  ScanCommand
} from 'dynamodb-toolbox'
```

### Table Definition

```typescript
import { DynamoDBClient } from '@aws-sdk/client-dynamodb'
import { DynamoDBDocumentClient } from '@aws-sdk/lib-dynamodb'
import { Table } from 'dynamodb-toolbox'

const client = new DynamoDBClient({})
const documentClient = DynamoDBDocumentClient.from(client)

const MyTable = new Table({
  documentClient,
  name: 'my-table',
  partitionKey: { name: 'PK', type: 'string' },
  sortKey: { name: 'SK', type: 'string' },  // optional
  indexes: {  // optional
    GSI1: {
      type: 'global',
      partitionKey: { name: 'GSI1PK', type: 'string' },
      sortKey: { name: 'GSI1SK', type: 'string' }
    },
    LSI1: {
      type: 'local',
      sortKey: { name: 'LSI1SK', type: 'number' }
    }
  },
  entityAttributeSavedAs: '_et'  // optional, defaults to 'entity'
})
```

### Entity Definition

```typescript
import { Entity, item, string, number, boolean, list, map } from 'dynamodb-toolbox'

const UserEntity = new Entity({
  name: 'User',
  table: MyTable,
  schema: item({
    // Key attributes
    PK: string().key().savedAs('PK'),
    SK: string().key().savedAs('SK'),

    // Regular attributes
    userId: string(),
    email: string(),
    name: string().optional(),
    age: number().optional(),
    isActive: boolean().default(true),
    tags: list(string()).optional(),
    profile: map({
      bio: string().optional(),
      avatar: string().optional()
    }).optional()
  }),
  computeKey: ({ userId }) => ({
    PK: `USER#${userId}`,
    SK: `PROFILE`
  }),
  timestamps: true  // adds created/modified timestamps
})
```

## Schema Types

### Primitives

```typescript
string()              // String
number()              // Number (use .big() for BigInt)
boolean()             // Boolean
binary()              // Binary (Uint8Array)
any()                 // Any type (no validation)
```

### Collections

```typescript
list(string())                    // List of strings
set(number())                     // Number set (also string/binary sets)
map({ name: string() })           // Map with known keys
record(string(), number())        // Map with dynamic keys
```

### Union Types

```typescript
anyOf(
  map({ type: string().const('dog'), breed: string() }),
  map({ type: string().const('cat'), lives: number() })
)
```

### Attribute Modifiers

```typescript
string()
  .required()           // Required (default: 'atLeastOnce')
  .optional()           // Same as .required('never')
  .hidden()             // Omit from formatted output
  .key()                // Mark as primary key attribute
  .savedAs('attr_name') // Rename in DynamoDB
  .enum('a', 'b', 'c')  // Restrict to specific values
  .default('value')     // Default value
  .default(() => uuid()) // Default with getter
  .transform(...)       // Transform during parse/format
  .validate(v => v.length > 0) // Custom validation
  .link<Schema>(({ name }) => name.toUpperCase()) // Derive from other attrs
```

## Commands (The .build() Pattern)

### GetItemCommand

```typescript
import { GetItemCommand } from 'dynamodb-toolbox'

const { Item } = await UserEntity.build(GetItemCommand)
  .key({ userId: '123' })
  .options({
    consistent: true,           // Strongly consistent read
    attributes: ['email', 'name'] // Project specific attributes
  })
  .send()
```

### PutItemCommand

```typescript
import { PutItemCommand } from 'dynamodb-toolbox'

const { Attributes } = await UserEntity.build(PutItemCommand)
  .item({
    userId: '123',
    email: 'user@example.com',
    name: 'John'
  })
  .options({
    returnValues: 'ALL_OLD',
    condition: { attr: 'userId', exists: false } // Only if not exists
  })
  .send()
```

### UpdateItemCommand

```typescript
import { UpdateItemCommand, $add, $remove, $append, $set } from 'dynamodb-toolbox'

// Basic update
await UserEntity.build(UpdateItemCommand)
  .item({
    userId: '123',
    name: 'Jane',
    age: 30
  })
  .send()

// Extended syntax
await UserEntity.build(UpdateItemCommand)
  .item({
    userId: '123',
    age: $add(1),                    // Increment
    oldField: $remove(),             // Remove attribute
    tags: $append(['new-tag']),      // Append to list
    profile: $set({ bio: 'Hello' })  // Replace entire nested object
  })
  .options({ returnValues: 'ALL_NEW' })
  .send()
```

**Update Operations:**
- `$add(n)` - Add to number or add elements to set
- `$remove()` - Remove attribute
- `$set(value)` - Override entire value (for deep attributes)
- `$append(items)` - Append to list
- `$prepend(items)` - Prepend to list
- `$get(path)` - Reference another attribute's value

### DeleteItemCommand

```typescript
import { DeleteItemCommand } from 'dynamodb-toolbox'

const { Attributes } = await UserEntity.build(DeleteItemCommand)
  .key({ userId: '123' })
  .options({
    returnValues: 'ALL_OLD',
    condition: { attr: 'isActive', eq: false }
  })
  .send()
```

### QueryCommand (Table-level)

```typescript
import { QueryCommand } from 'dynamodb-toolbox'

const { Items, LastEvaluatedKey } = await MyTable.build(QueryCommand)
  .query({
    partition: 'USER#123',
    range: { gte: 'ORDER#' }  // Range condition: eq, lt, lte, gt, gte, between, beginsWith
  })
  .entities(UserEntity, OrderEntity)  // Filter/format by entities
  .options({
    index: 'GSI1',           // Use secondary index
    consistent: true,
    reverse: true,           // Reverse order
    limit: 10,
    filters: { attr: 'status', eq: 'active' }
  })
  .send()

// Pagination
let lastKey
do {
  const result = await MyTable.build(QueryCommand)
    .query({ partition: 'USER#123' })
    .options({ exclusiveStartKey: lastKey })
    .send()
  // Process result.Items
  lastKey = result.LastEvaluatedKey
} while (lastKey)
```

### ScanCommand (Table-level)

```typescript
import { ScanCommand } from 'dynamodb-toolbox'

const { Items } = await MyTable.build(ScanCommand)
  .entities(UserEntity)
  .options({
    limit: 100,
    filters: { attr: 'isActive', eq: true }
  })
  .send()

// Parallel scan
const segment = 0
const totalSegments = 4
await MyTable.build(ScanCommand)
  .options({ segment, totalSegments })
  .send()
```

## Batch Operations

### BatchGet

```typescript
import { BatchGetRequest, BatchGetCommand, executeBatchGet } from 'dynamodb-toolbox'

const requests = [
  UserEntity.build(BatchGetRequest).key({ userId: '1' }),
  UserEntity.build(BatchGetRequest).key({ userId: '2' })
]

const command = MyTable.build(BatchGetCommand).requests(...requests)
const { Responses } = await executeBatchGet(command)
```

### BatchWrite

```typescript
import { BatchPutRequest, BatchDeleteRequest, BatchWriteCommand, executeBatchWrite } from 'dynamodb-toolbox'

const requests = [
  UserEntity.build(BatchPutRequest).item({ userId: '1', email: 'a@b.com' }),
  UserEntity.build(BatchDeleteRequest).key({ userId: '2' })
]

const command = MyTable.build(BatchWriteCommand).requests(...requests)
await executeBatchWrite(command)
```

## Transactions

### TransactGet

```typescript
import { GetTransaction, executeTransactGet } from 'dynamodb-toolbox'

const transactions = [
  UserEntity.build(GetTransaction).key({ userId: '1' }),
  OrderEntity.build(GetTransaction).key({ orderId: '100' })
]

const { Responses } = await executeTransactGet(...transactions)
```

### TransactWrite

```typescript
import { PutTransaction, UpdateTransaction, DeleteTransaction, ConditionCheck, executeTransactWrite } from 'dynamodb-toolbox'

await executeTransactWrite(
  UserEntity.build(PutTransaction).item({ userId: '1', email: 'new@email.com' }),
  OrderEntity.build(UpdateTransaction).item({ orderId: '100', status: 'shipped' }),
  UserEntity.build(ConditionCheck)
    .key({ userId: '2' })
    .options({ condition: { attr: 'balance', gte: 100 } })
)
```

## Conditions

Use in `.options({ condition: ... })` for conditional writes:

```typescript
// Simple conditions
{ attr: 'status', eq: 'active' }
{ attr: 'age', gt: 18 }
{ attr: 'email', exists: true }
{ attr: 'name', beginsWith: 'John' }
{ attr: 'tags', contains: 'premium' }
{ attr: 'score', between: [10, 100] }

// Logical operators
{ and: [{ attr: 'a', eq: 1 }, { attr: 'b', eq: 2 }] }
{ or: [{ attr: 'status', eq: 'a' }, { attr: 'status', eq: 'b' }] }
{ not: { attr: 'deleted', eq: true } }
```

## Common Patterns

### Single-Table Design

```typescript
// Base entity with shared key structure
const baseSchema = {
  PK: string().key(),
  SK: string().key()
}

const UserEntity = new Entity({
  name: 'User',
  table: MyTable,
  schema: item({
    ...baseSchema,
    userId: string(),
    email: string()
  }),
  computeKey: ({ userId }) => ({ PK: `USER#${userId}`, SK: 'PROFILE' })
})

const OrderEntity = new Entity({
  name: 'Order',
  table: MyTable,
  schema: item({
    ...baseSchema,
    userId: string(),
    orderId: string(),
    total: number()
  }),
  computeKey: ({ userId, orderId }) => ({ PK: `USER#${userId}`, SK: `ORDER#${orderId}` })
})
```

### Access Patterns

```typescript
import { EntityAccessPattern, item, string } from 'dynamodb-toolbox'

const getUserOrders = UserEntity.build(EntityAccessPattern)
  .schema(item({ userId: string() }))
  .pattern(({ userId }) => ({
    partition: `USER#${userId}`,
    range: { beginsWith: 'ORDER#' }
  }))

const { Items } = await getUserOrders.query({ userId: '123' }).send()
```

For detailed API reference, see [references/api.md](references/api.md).
