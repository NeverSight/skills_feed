---
name: adonisjs-best-practices
description: Use when building AdonisJS v6 applications, implementing features in AdonisJS, or reviewing AdonisJS code. Covers routing, controllers, validation, authentication, database patterns, testing, and error handling.
tags: [framework, adonisjs]
---

# AdonisJS v6 Best Practices

## Overview

AdonisJS v6 is a TypeScript-first MVC framework with batteries included. Core principle: **type safety, dependency injection, and convention over configuration**.

## When to Use

- Building new AdonisJS v6 features
- Implementing routes, controllers, middleware
- Setting up authentication or authorization
- Writing Lucid ORM models and queries
- Creating validators with VineJS
- Writing tests for AdonisJS apps

## Quick Reference

| Task                 | Pattern                                                                 |
| -------------------- | ----------------------------------------------------------------------- |
| Route to controller  | `router.get('/users', [UsersController, 'index'])`                      |
| Lazy-load controller | `const UsersController = () => import('#controllers/users_controller')` |
| Validate request     | `const payload = await request.validateUsing(createUserValidator)`      |
| Auth check           | `await auth.authenticate()` or `auth.use('guard').authenticate()`       |
| Authorize action     | `await bouncer.authorize('editPost', post)`                             |
| Query with relations | `await User.query().preload('posts')`                                   |

## Project Structure

```
app/
  controllers/     # HTTP handlers (thin, delegate to services)
  models/          # Lucid ORM models
  services/        # Business logic
  middleware/      # Request interceptors
  validators/      # VineJS validation schemas
  exceptions/      # Custom exceptions
  policies/        # Bouncer authorization
start/
  routes.ts        # Route definitions
  kernel.ts        # Middleware registration
config/            # Configuration files
database/          # Migrations, seeders, factories
tests/             # Test suites
```

## Routing

**Lazy-load controllers** for HMR support and faster boot:

```typescript
// start/routes.ts
const UsersController = () => import('#controllers/users_controller')

router.get('/users', [UsersController, 'index'])
router.post('/users', [UsersController, 'store'])
```

**Order matters**: Define specific routes before dynamic ones:

```typescript
// CORRECT
router.get('/users/me', [UsersController, 'me'])
router.get('/users/:id', [UsersController, 'show'])

// WRONG - /users/me will never match
router.get('/users/:id', [UsersController, 'show'])
router.get('/users/me', [UsersController, 'me'])
```

**Use route groups** for organization and bulk middleware:

```typescript
router
  .group(() => {
    router.resource('posts', PostsController)
    router.resource('comments', CommentsController)
  })
  .prefix('/api/v1')
  .middleware(middleware.auth())
```

**Resource controllers** for RESTful CRUD:

```typescript
router.resource('posts', PostsController)
// Creates: index, create, store, show, edit, update, destroy
```

**Name routes** for URL generation:

```typescript
router.get('/posts/:id', [PostsController, 'show']).as('posts.show')
// Use: route('posts.show', { id: 1 })
```

## Controllers

**Single responsibility**: One controller per resource, thin handlers:

```typescript
// app/controllers/posts_controller.ts
export default class PostsController {
  async index({ request, response }: HttpContext) {
    const posts = await Post.query().preload('author')
    return response.json(posts)
  }

  async store({ request, response }: HttpContext) {
    const payload = await request.validateUsing(createPostValidator)
    const post = await Post.create(payload)
    return response.created(post)
  }
}
```

**Method injection** for services:

```typescript
import { inject } from '@adonisjs/core'
import PostService from '#services/post_service'

export default class PostsController {
  @inject()
  async store({ request }: HttpContext, postService: PostService) {
    const payload = await request.validateUsing(createPostValidator)
    return postService.create(payload)
  }
}
```

## Validation

**Validate immediately** in controller, before any business logic:

```typescript
// app/validators/post_validator.ts
import vine from '@vinejs/vine'

export const createPostValidator = vine.compile(
  vine.object({
    title: vine.string().trim().minLength(3).maxLength(255),
    content: vine.string().trim(),
    published: vine.boolean().optional(),
  })
)

// In controller
async store({ request }: HttpContext) {
  const payload = await request.validateUsing(createPostValidator)
  // payload is now typed and validated
}
```

**Database rules** for unique/exists checks:

```typescript
import vine from '@vinejs/vine'
import { uniqueRule } from '#validators/rules/unique'

export const createUserValidator = vine.compile(
  vine.object({
    email: vine
      .string()
      .email()
      .use(uniqueRule({ table: 'users', column: 'email' })),
  })
)
```

## Middleware

**Three stacks** with distinct purposes:

```typescript
// start/kernel.ts

// Server middleware: ALL requests (static files, health checks)
server.use([() => import('#middleware/container_bindings_middleware')])

// Router middleware: matched routes only (auth, logging)
router.use([() => import('@adonisjs/cors/cors_middleware')])

// Named middleware: explicit assignment
export const middleware = router.named({
  auth: () => import('#middleware/auth_middleware'),
  guest: () => import('#middleware/guest_middleware'),
})
```

**Apply per-route**:

```typescript
router.get('/dashboard', [DashboardController, 'index']).middleware(middleware.auth())
```

## Authentication

**Choose guard by client type**:

- **Session guard**: Server-rendered apps (web)
- **Access tokens**: SPA/mobile clients (api)

```typescript
// Session-based (web)
router.post('/login', async ({ auth, request, response }) => {
  const { email, password } = await request.validateUsing(loginValidator)
  const user = await User.verifyCredentials(email, password)
  await auth.use('web').login(user)
  return response.redirect('/dashboard')
})

// Token-based (API)
router.post('/api/login', async ({ request }) => {
  const { email, password } = await request.validateUsing(loginValidator)
  const user = await User.verifyCredentials(email, password)
  const token = await User.accessTokens.create(user)
  return { token: token.value!.release() }
})
```

**Protect routes**:

```typescript
router
  .group(() => {
    router.get('/profile', [ProfileController, 'show'])
  })
  .middleware(middleware.auth({ guards: ['web'] }))
```

## Authorization (Bouncer)

**Abilities** for simple checks:

```typescript
// app/abilities/main.ts
import { Bouncer } from '@adonisjs/bouncer'
import User from '#models/user'
import Post from '#models/post'

export const editPost = Bouncer.ability((user: User, post: Post) => {
  return user.id === post.userId
})
```

**Policies** for resource-based authorization:

```typescript
// app/policies/post_policy.ts
import { BasePolicy } from '@adonisjs/bouncer'
import User from '#models/user'
import Post from '#models/post'

export default class PostPolicy extends BasePolicy {
  edit(user: User, post: Post) {
    return user.id === post.userId
  }

  delete(user: User, post: Post) {
    return user.id === post.userId || user.isAdmin
  }
}
```

**Use in controllers**:

```typescript
async update({ bouncer, params, request }: HttpContext) {
  const post = await Post.findOrFail(params.id)
  await bouncer.authorize('editPost', post)  // Throws if unauthorized
  // or: if (await bouncer.allows('editPost', post)) { ... }
}
```

## Database (Lucid ORM)

**Prevent N+1** with eager loading:

```typescript
// BAD - N+1 queries
const posts = await Post.all()
for (const post of posts) {
  console.log(post.author.name) // Query per post
}

// GOOD - 2 queries total
const posts = await Post.query().preload('author')
```

**Model hooks** for business logic:

```typescript
// app/models/user.ts
import { beforeSave, column } from '@adonisjs/lucid/orm'
import hash from '@adonisjs/core/services/hash'

export default class User extends BaseModel {
  @column()
  declare password: string

  @beforeSave()
  static async hashPassword(user: User) {
    if (user.$dirty.password) {
      user.password = await hash.make(user.password)
    }
  }
}
```

**Transactions** for atomic operations:

```typescript
import db from '@adonisjs/lucid/services/db'

await db.transaction(async (trx) => {
  const user = await User.create({ email }, { client: trx })
  await Profile.create({ userId: user.id }, { client: trx })
})
```

## Error Handling

**Custom exceptions**:

```typescript
// app/exceptions/not_found_exception.ts
import { Exception } from '@adonisjs/core/exceptions'

export default class NotFoundException extends Exception {
  static status = 404
  static code = 'E_NOT_FOUND'
}

// Usage
throw new NotFoundException('Post not found')
```

**Global exception handler**:

```typescript
// app/exceptions/handler.ts
import { ExceptionHandler, HttpContext } from '@adonisjs/core/http'

export default class HttpExceptionHandler extends ExceptionHandler {
  async handle(error: unknown, ctx: HttpContext) {
    if (error instanceof NotFoundException) {
      return ctx.response.status(404).json({ error: error.message })
    }
    return super.handle(error, ctx)
  }
}
```

## Testing

**HTTP tests** via test client:

```typescript
import { test } from '@japa/runner'

test.group('Posts', () => {
  test('can list posts', async ({ client }) => {
    const response = await client.get('/api/posts')
    response.assertStatus(200)
    response.assertBodyContains({ data: [] })
  })

  test('requires auth to create post', async ({ client }) => {
    const response = await client.post('/api/posts').json({ title: 'Test' })
    response.assertStatus(401)
  })

  test('authenticated user can create post', async ({ client }) => {
    const user = await UserFactory.create()
    const response = await client
      .post('/api/posts')
      .loginAs(user)
      .json({ title: 'Test', content: 'Content' })
    response.assertStatus(201)
  })
})
```

**Database isolation** with transactions:

```typescript
import { test } from '@japa/runner'
import testUtils from '@adonisjs/core/services/test_utils'

test.group('Posts', (group) => {
  group.each.setup(() => testUtils.db().withGlobalTransaction())

  test('creates post in database', async ({ client, assert }) => {
    const user = await UserFactory.create()
    await client.post('/api/posts').loginAs(user).json({ title: 'Test' })

    const post = await Post.findBy('title', 'Test')
    assert.isNotNull(post)
  })
})
```

## Common Mistakes

| Mistake                        | Fix                                                  |
| ------------------------------ | ---------------------------------------------------- |
| Raw controller imports         | Use lazy-loading: `() => import('#controllers/...')` |
| Validating in services         | Validate in controller before business logic         |
| N+1 queries                    | Use `.preload()` for eager loading                   |
| Dynamic route before specific  | Order specific routes first                          |
| Skipping authorization         | Always check permissions with Bouncer                |
| Not using transactions         | Wrap related operations in `db.transaction()`        |
| Testing directly, not via HTTP | Use `client.get()` for integration tests             |
