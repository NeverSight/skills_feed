---
name: prisma-patterns
description: Prisma ORM patterns - use for database access in Next.js, schema design, migrations, transactions, and relations
---

# Prisma ORM Patterns

## Schema Definition

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")

  environments Environment[]
  sessions     Session[]

  @@map("users")
}

model Environment {
  id          String            @id @default(cuid())
  name        String
  description String?
  status      EnvironmentStatus @default(PENDING)
  ownerId     String            @map("owner_id")
  createdAt   DateTime          @default(now()) @map("created_at")
  updatedAt   DateTime          @updatedAt @map("updated_at")

  owner User  @relation(fields: [ownerId], references: [id], onDelete: Cascade)
  tags  Tag[]

  @@unique([ownerId, name])
  @@index([status])
  @@index([createdAt(sort: Desc)])
  @@map("environments")
}

model Tag {
  id            String      @id @default(cuid())
  key           String
  value         String
  environmentId String      @map("environment_id")
  createdAt     DateTime    @default(now()) @map("created_at")

  environment Environment @relation(fields: [environmentId], references: [id], onDelete: Cascade)

  @@unique([environmentId, key])
  @@map("tags")
}

enum EnvironmentStatus {
  PENDING
  RUNNING
  STOPPED
  FAILED
}
```

## Prisma Client Setup

```typescript
// lib/prisma.ts
import { PrismaClient } from '@prisma/client'

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined
}

export const prisma = globalForPrisma.prisma ?? new PrismaClient({
  log: process.env.NODE_ENV === 'development'
    ? ['query', 'error', 'warn']
    : ['error'],
})

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma
}
```

## Basic CRUD Operations

```typescript
// Create
const environment = await prisma.environment.create({
  data: {
    name: 'dev-env',
    description: 'Development environment',
    ownerId: userId,
  },
})

// Read
const environment = await prisma.environment.findUnique({
  where: { id: envId },
})

const environments = await prisma.environment.findMany({
  where: { status: 'RUNNING' },
  orderBy: { createdAt: 'desc' },
  take: 10,
})

// Update
const updated = await prisma.environment.update({
  where: { id: envId },
  data: { status: 'STOPPED' },
})

// Delete
await prisma.environment.delete({
  where: { id: envId },
})

// Upsert
const env = await prisma.environment.upsert({
  where: { id: envId },
  update: { status: 'RUNNING' },
  create: {
    name: 'new-env',
    ownerId: userId,
  },
})
```

## Relations

```typescript
// Include relations
const envWithOwner = await prisma.environment.findUnique({
  where: { id: envId },
  include: {
    owner: true,
    tags: true,
  },
})

// Select specific fields
const envPartial = await prisma.environment.findUnique({
  where: { id: envId },
  select: {
    id: true,
    name: true,
    owner: {
      select: {
        name: true,
        email: true,
      },
    },
  },
})

// Nested create
const envWithTags = await prisma.environment.create({
  data: {
    name: 'tagged-env',
    ownerId: userId,
    tags: {
      create: [
        { key: 'team', value: 'platform' },
        { key: 'tier', value: 'production' },
      ],
    },
  },
  include: { tags: true },
})

// Connect existing relation
const env = await prisma.environment.create({
  data: {
    name: 'new-env',
    owner: {
      connect: { id: userId },
    },
  },
})
```

## Filtering

```typescript
// Complex filters
const environments = await prisma.environment.findMany({
  where: {
    AND: [
      { status: 'RUNNING' },
      {
        OR: [
          { name: { contains: 'prod', mode: 'insensitive' } },
          { tags: { some: { key: 'tier', value: 'production' } } },
        ],
      },
    ],
    createdAt: {
      gte: new Date('2024-01-01'),
    },
    owner: {
      email: { endsWith: '@jetbrains.com' },
    },
  },
})

// NOT filter
const nonFailedEnvs = await prisma.environment.findMany({
  where: {
    NOT: { status: 'FAILED' },
  },
})
```

## Pagination

```typescript
// Offset pagination
async function getEnvironmentsPage(page: number, pageSize: number) {
  const [items, total] = await Promise.all([
    prisma.environment.findMany({
      skip: (page - 1) * pageSize,
      take: pageSize,
      orderBy: { createdAt: 'desc' },
    }),
    prisma.environment.count(),
  ])

  return {
    items,
    total,
    page,
    pageSize,
    totalPages: Math.ceil(total / pageSize),
  }
}

// Cursor pagination
async function getEnvironmentsCursor(cursor?: string, take: number = 10) {
  const items = await prisma.environment.findMany({
    take: take + 1, // Fetch one extra to check if there's more
    ...(cursor && {
      cursor: { id: cursor },
      skip: 1, // Skip the cursor
    }),
    orderBy: { createdAt: 'desc' },
  })

  const hasMore = items.length > take
  const data = hasMore ? items.slice(0, -1) : items

  return {
    items: data,
    nextCursor: hasMore ? data[data.length - 1].id : null,
  }
}
```

## Transactions

```typescript
// Interactive transaction
const result = await prisma.$transaction(async (tx) => {
  // Create environment
  const env = await tx.environment.create({
    data: { name: 'new-env', ownerId: userId },
  })

  // Create associated tags
  await tx.tag.createMany({
    data: [
      { key: 'team', value: 'platform', environmentId: env.id },
      { key: 'cost-center', value: '12345', environmentId: env.id },
    ],
  })

  // Update user's environment count (if tracking)
  await tx.user.update({
    where: { id: userId },
    data: { environmentCount: { increment: 1 } },
  })

  return env
})

// Sequential transaction (batch)
const [deletedEnvs, deletedTags] = await prisma.$transaction([
  prisma.environment.deleteMany({ where: { status: 'FAILED' } }),
  prisma.tag.deleteMany({ where: { environment: { status: 'FAILED' } } }),
])
```

## Aggregations

```typescript
// Count by status
const statusCounts = await prisma.environment.groupBy({
  by: ['status'],
  _count: { status: true },
})

// Aggregate functions
const stats = await prisma.environment.aggregate({
  _count: { id: true },
  _min: { createdAt: true },
  _max: { createdAt: true },
})
```

## Raw Queries (When Needed)

```typescript
// Raw query
const result = await prisma.$queryRaw<Environment[]>`
  SELECT * FROM environments
  WHERE status = ${status}
  AND created_at > NOW() - INTERVAL '7 days'
`

// Raw execute
await prisma.$executeRaw`
  UPDATE environments
  SET status = 'STOPPED'
  WHERE status = 'RUNNING'
  AND updated_at < NOW() - INTERVAL '24 hours'
`
```

## Migrations

```bash
# Create migration
npx prisma migrate dev --name add_environment_type

# Apply migrations (production)
npx prisma migrate deploy

# Reset database (development)
npx prisma migrate reset

# Generate client
npx prisma generate
```
