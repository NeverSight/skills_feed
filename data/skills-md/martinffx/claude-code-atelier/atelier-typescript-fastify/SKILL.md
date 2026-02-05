---
name: atelier-typescript-fastify
description: Building REST APIs with Fastify in TypeScript. Use when creating routes, handling requests, implementing validation with TypeBox, structuring applications, or working with HTTP handlers and plugins.
user-invocable: false
---

# Fastify

Fast, low-overhead web framework for Node.js with TypeBox schema validation.

## Additional References

- [references/plugins.md](./references/plugins.md) - Plugin architecture and dependency injection
- [references/typeid.md](./references/typeid.md) - Type-safe prefixed identifiers

## Setup

```bash
npm i fastify @fastify/type-provider-typebox @sinclair/typebox
```

```typescript
import Fastify from 'fastify'
import { TypeBoxTypeProvider } from '@fastify/type-provider-typebox'

const app = Fastify({ logger: true }).withTypeProvider<TypeBoxTypeProvider>()
```

## Schema Definition

```typescript
import { Type, Static } from '@sinclair/typebox'

// Request/response schemas with $id for OpenAPI
export const UserSchema = Type.Object({
  id: Type.String({ format: 'uuid' }),
  name: Type.String({ minLength: 1, maxLength: 100 }),
  email: Type.String({ format: 'email' }),
  createdAt: Type.String({ format: 'date-time' }),
}, { $id: 'UserResponse' })

export type User = Static<typeof UserSchema>

// Input schemas (omit generated fields)
export const CreateUserSchema = Type.Object({
  name: Type.String({ minLength: 1, maxLength: 100 }),
  email: Type.String({ format: 'email' }),
}, { $id: 'CreateUserRequest' })

export type CreateUserInput = Static<typeof CreateUserSchema>
```

## Route with Full Schema

```typescript
const TAGS = ['Users']

app.post('/users', {
  schema: {
    operationId: 'createUser',
    tags: TAGS,
    summary: 'Create a new user',
    description: 'Create a new user account',
    body: CreateUserSchema,
    response: {
      201: UserSchema,
      400: BadRequestErrorResponse,
      401: UnauthorizedErrorResponse,
      500: InternalServerErrorResponse,
    },
  },
}, async (request, reply) => {
  const { name, email } = request.body // fully typed

  const user = await createUser({ name, email })
  return reply.status(201).send(user)
})
```

## Common Schema Patterns

```typescript
// Path parameters
const ParamsSchema = Type.Object({
  id: Type.String({ format: 'uuid' }),
})

// Query string with pagination
const QuerySchema = Type.Object({
  limit: Type.Optional(Type.Integer({ minimum: 1, maximum: 100, default: 20 })),
  cursor: Type.Optional(Type.String()),
  sort: Type.Optional(Type.Union([Type.Literal('asc'), Type.Literal('desc')])),
})

// Paginated response wrapper
const PaginatedResponse = <T extends TSchema>(itemSchema: T) =>
  Type.Object({
    items: Type.Array(itemSchema),
    nextCursor: Type.Optional(Type.String()),
    hasMore: Type.Boolean(),
  })

app.get('/users/:id', {
  schema: {
    operationId: 'getUser',
    tags: ['Users'],
    summary: 'Get user by ID',
    params: ParamsSchema,
    querystring: QuerySchema,
    response: {
      200: UserSchema,
      400: BadRequestErrorResponse,
      404: NotFoundErrorResponse,
      500: InternalServerErrorResponse,
    },
  },
}, async (request, reply) => {
  const { id } = request.params
  const { limit, cursor } = request.query
  // ...
})
```

## Modular Route Registration

```typescript
// types.ts - Export typed Fastify instance
import {
  FastifyInstance,
  FastifyBaseLogger,
  RawReplyDefaultExpression,
  RawRequestDefaultExpression,
  RawServerDefault,
} from 'fastify'
import { TypeBoxTypeProvider } from '@fastify/type-provider-typebox'

export type FastifyTypebox = FastifyInstance<
  RawServerDefault,
  RawRequestDefaultExpression<RawServerDefault>,
  RawReplyDefaultExpression<RawServerDefault>,
  FastifyBaseLogger,
  TypeBoxTypeProvider
>
```

```typescript
// routes/users.ts
import { Type } from '@sinclair/typebox'
import { FastifyTypebox } from '../types'

export async function userRoutes(app: FastifyTypebox) {
  app.get('/users', {
    schema: {
      response: {
        200: Type.Array(UserSchema),
      },
    },
  }, async () => {
    return await listUsers()
  })
}
```

```typescript
// index.ts
import { userRoutes } from './routes/users'

app.register(userRoutes, { prefix: '/api/v1' })
```

## Error Schemas (RFC 7807)

Use standardized error responses across all routes:

```typescript
import { Type } from '@sinclair/typebox'

// Base ProblemDetail schema (RFC 7807)
const ProblemDetail = Type.Object({
  type: Type.String(),
  status: Type.Number(),
  title: Type.String(),
  detail: Type.String(),
  instance: Type.String(),
  traceId: Type.String(),
})

// Specific error responses
export const BadRequestErrorResponse = Type.Composite([
  ProblemDetail,
  Type.Object({
    type: Type.Literal('BAD_REQUEST'),
    status: Type.Literal(400),
  }),
], { $id: 'BadRequestErrorResponse' })

export const UnauthorizedErrorResponse = Type.Composite([
  ProblemDetail,
  Type.Object({
    type: Type.Literal('UNAUTHORIZED'),
    status: Type.Literal(401),
  }),
], { $id: 'UnauthorizedErrorResponse' })

export const ForbiddenErrorResponse = Type.Composite([
  ProblemDetail,
  Type.Object({
    type: Type.Literal('FORBIDDEN'),
    status: Type.Literal(403),
  }),
], { $id: 'ForbiddenErrorResponse' })

export const NotFoundErrorResponse = Type.Composite([
  ProblemDetail,
  Type.Object({
    type: Type.Literal('NOT_FOUND'),
    status: Type.Literal(404),
  }),
], { $id: 'NotFoundErrorResponse' })

export const InternalServerErrorResponse = Type.Composite([
  ProblemDetail,
  Type.Object({
    type: Type.Literal('INTERNAL_SERVER_ERROR'),
    status: Type.Literal(500),
  }),
], { $id: 'InternalServerErrorResponse' })
```

## Error Handling

```typescript
import { FastifyError, FastifyRequest, FastifyReply } from 'fastify'

// Custom error handler
const globalErrorHandler = (
  error: FastifyError,
  request: FastifyRequest,
  reply: FastifyReply
) => {
  // Handle Fastify validation errors
  if (error.code === 'FST_ERR_VALIDATION') {
    return reply.status(400).send({
      type: 'BAD_REQUEST',
      status: 400,
      title: 'Validation Error',
      detail: error.message,
      instance: request.url,
      traceId: request.id,
    })
  }

  // Handle domain errors (if using error classes)
  if (error instanceof AppError) {
    return reply.status(error.status).send(error.toResponse())
  }

  // Default to internal server error
  request.log.error(error)
  return reply.status(500).send({
    type: 'INTERNAL_SERVER_ERROR',
    status: 500,
    title: 'Internal Server Error',
    detail: 'Something went wrong',
    instance: request.url,
    traceId: request.id,
  })
}

app.setErrorHandler(globalErrorHandler)
```

## Reusable Schemas (Shared References)

```typescript
// Add schema to instance for $ref usage
app.addSchema({
  $id: 'User',
  ...UserSchema,
})

app.addSchema({
  $id: 'Error',
  ...ErrorSchema,
})

// Reference in routes
app.get('/me', {
  schema: {
    response: {
      200: Type.Ref('User'),
      401: Type.Ref('Error'),
    },
  },
}, handler)
```

## Headers and Auth

```typescript
const AuthHeadersSchema = Type.Object({
  authorization: Type.String({ pattern: '^Bearer .+$' }),
})

app.get('/protected', {
  schema: {
    headers: AuthHeadersSchema,
    response: {
      200: UserSchema,
      401: UnauthorizedErrorResponse,
    },
  },
  preValidation: async (request, reply) => {
    const token = request.headers.authorization?.replace('Bearer ', '')
    if (!token || !verifyToken(token)) {
      throw new UnauthorizedError('Invalid or missing token')
    }
  },
}, handler)
```

## Auth & Permissions

Role-based permission checks with decorators:

```typescript
import type { FastifyRequest, FastifyReply } from 'fastify'

// Permission constants
const Permissions = [
  'user:read',
  'user:write',
  'user:delete',
  'admin:access',
] as const

type Permission = typeof Permissions[number]

// Role-based permission sets
const RolePermissions = {
  admin: new Set<Permission>(['user:read', 'user:write', 'user:delete', 'admin:access']),
  user: new Set<Permission>(['user:read', 'user:write']),
  readonly: new Set<Permission>(['user:read']),
} as const

// Extend FastifyRequest with token data
declare module 'fastify' {
  interface FastifyRequest {
    token: {
      userId: string
      role: keyof typeof RolePermissions
      permissions: Permission[]
    }
  }
}

// Permission check decorator
app.decorate('hasPermissions', (requiredPermissions: Permission[]) => {
  return async (request: FastifyRequest, reply: FastifyReply): Promise<void> => {
    const userPermissions = request.token.permissions

    for (const permission of requiredPermissions) {
      if (!userPermissions.includes(permission)) {
        throw new ForbiddenError(`Missing permission: ${permission}`)
      }
    }
  }
})

// Usage in routes
app.delete('/users/:id', {
  schema: {
    operationId: 'deleteUser',
    tags: ['Users'],
    params: Type.Object({ id: Type.String() }),
    response: {
      204: Type.Null(),
      401: UnauthorizedErrorResponse,
      403: ForbiddenErrorResponse,
      404: NotFoundErrorResponse,
    },
  },
  preHandler: app.hasPermissions(['user:delete']),
}, async (request, reply) => {
  await deleteUser(request.params.id)
  return reply.status(204).send()
})
```

## Guidelines

1. Always define schemas with `Type.Object({ ... })` - full JSON Schema required in Fastify v5
2. Add `$id` to all schemas for OpenAPI generation and reusability
3. Add `operationId`, `tags`, and `summary` to all routes for documentation
4. Define response schemas for ALL status codes (200, 400, 401, 403, 404, 500)
5. Use RFC 7807 ProblemDetail format for errors with `Type.Composite`
6. Use `Static<typeof Schema>` to derive TypeScript types from schemas
7. Split input schemas (CreateX) from output schemas (X) - omit generated fields
8. Use `Type.Optional()` for optional fields, not `?` in the type
9. Export `FastifyTypebox` type for modular route files
10. Add format validators: `uuid`, `email`, `date-time`, `uri`
11. Use `Type.Union([Type.Literal(...)])` for string enums
12. Use Fastify plugins with `fp()` for dependency injection - see [references/plugins.md](./references/plugins.md)
13. Use `preHandler` with `hasPermissions()` decorator for protected routes
14. Use TypeID for type-safe prefixed identifiers - see [references/typeid.md](./references/typeid.md)
