---
name: elysiajs-expert
description: Expert guidance for ElysiaJS web framework development. Use when building REST APIs, GraphQL services, or WebSocket applications with Elysia on Bun. Covers routing, lifecycle hooks, TypeBox validation, Eden type-safe clients, authentication with JWT/Bearer, all official plugins (OpenAPI, CORS, JWT, static, cron, GraphQL, tRPC), testing patterns, and production deployment. Assumes bun-expert skill is active for Bun runtime expertise.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# ElysiaJS Expert Skill

This skill provides comprehensive expertise for building high-performance, fully type-safe web applications with Elysia on the Bun runtime. It assumes the `bun-expert` skill is active for Bun-specific patterns (file I/O, SQLite, testing, builds).

## When to Use This Skill

- Building REST APIs with Elysia
- Implementing type-safe request/response validation with TypeBox
- Setting up authentication (JWT, Bearer tokens, sessions)
- Creating WebSocket servers
- Generating OpenAPI/Swagger documentation
- Building full-stack applications with Eden Treaty
- Configuring Elysia plugins (CORS, static files, cron, GraphQL, tRPC)
- Testing Elysia applications
- Production deployment optimization

## Quick Start

```typescript
import { Elysia, t } from 'elysia'

const app = new Elysia()
  .get('/', () => 'Hello Elysia')
  .get('/user/:id', ({ params }) => `User ${params.id}`)
  .post('/user', ({ body }) => body, {
    body: t.Object({
      name: t.String(),
      email: t.String({ format: 'email' })
    })
  })
  .listen(3000)

export type App = typeof app // Export for Eden client
```

## Core Concepts

### Elysia Constructor Options

```typescript
new Elysia({
  name: 'my-app',              // Plugin deduplication identifier
  prefix: '/api',              // Route prefix
  seed: config,                // Deduplication checksum seed
  websocket: {                 // WebSocket configuration
    idleTimeout: 30,
    maxPayloadLength: 16777216
  }
})
```

### HTTP Methods

```typescript
app
  .get('/path', handler)       // GET request
  .post('/path', handler)      // POST request
  .put('/path', handler)       // PUT request
  .delete('/path', handler)    // DELETE request
  .patch('/path', handler)     // PATCH request
  .options('/path', handler)   // OPTIONS request
  .all('/path', handler)       // All methods
  .route('CUSTOM', '/path', handler) // Custom HTTP verb
```

### Path Parameters

```typescript
.get('/user/:id', ({ params }) => params.id)           // Required param
.get('/user/:id?', ({ params }) => params.id ?? 'n/a') // Optional param
.get('/files/*', ({ params }) => params['*'])          // Wildcard
.get('/org/:org/repo/:repo', ({ params }) => params)   // Multiple params
```

### Context Object

Every handler receives a context object with:

```typescript
{
  body,        // Parsed request body
  query,       // Query string as object
  params,      // Path parameters
  headers,     // Request headers (lowercase keys)
  cookie,      // Cookie jar with get/set
  store,       // Global mutable state
  set,         // Response setters (status, headers)
  request,     // Raw Request object
  path,        // Request path
  server,      // Bun server instance
  redirect,    // Redirect function
  status,      // Status response function
  // + decorated/derived properties
}
```

### Response Patterns

```typescript
// String
.get('/', () => 'Hello')

// JSON (auto-serialized)
.get('/json', () => ({ hello: 'world' }))

// Status with response
.get('/error', ({ status }) => status(418, "I'm a teapot"))

// Custom headers
.get('/custom', ({ set }) => {
  set.headers['x-powered-by'] = 'Elysia'
  return 'Hello'
})

// Redirect
.get('/old', ({ redirect }) => redirect('/new'))

// File
import { file } from 'elysia'
.get('/image', () => file('image.png'))

// Streaming (generator)
.get('/stream', function* () {
  yield 'Hello '
  yield 'World'
})

// Async streaming
.get('/async', async function* () {
  for (let i = 0; i < 10; i++) {
    yield `Event ${i}\n`
    await Bun.sleep(100)
  }
})
```

## Lifecycle Hooks (Execution Order)

**Request → Parse → Transform → Validation → BeforeHandle → Handler → AfterHandle → MapResponse → AfterResponse**

### onRequest (Global, Before Routing)

```typescript
.onRequest(({ request, ip, set, status }) => {
  // Rate limiting, CORS preflight, request logging
  if (rateLimiter.exceeded(ip)) return status(429)
})
```

### onParse (Body Parser)

```typescript
.onParse(({ request, contentType }) => {
  if (contentType === 'application/custom')
    return request.text()
})

// Or specify parser explicitly
.post('/', handler, { parse: 'json' }) // 'json' | 'text' | 'formdata' | 'urlencoded' | 'none'
```

### onTransform (Before Validation)

```typescript
.get('/id/:id', handler, {
  transform({ params }) {
    params.id = +params.id // Convert to number before validation
  }
})
```

### derive (Creates Context Properties - Before Validation)

```typescript
.derive(({ headers }) => ({
  bearer: headers.authorization?.startsWith('Bearer ')
    ? headers.authorization.slice(7)
    : null
}))
.get('/protected', ({ bearer }) => bearer)
```

### onBeforeHandle (After Validation)

```typescript
.onBeforeHandle(({ cookie, status }) => {
  if (!validateSession(cookie.session.value))
    return status(401, 'Unauthorized')
})

// Local hook
.get('/protected', handler, {
  beforeHandle({ headers, status }) {
    if (!headers.authorization) return status(401)
  }
})
```

### resolve (Creates Context Properties - After Validation, Type-Safe)

```typescript
.guard({
  headers: t.Object({ authorization: t.TemplateLiteral('Bearer ${string}') })
})
.resolve(({ headers }) => ({
  token: headers.authorization.split(' ')[1],
  userId: decodeToken(headers.authorization)
}))
.get('/me', ({ userId }) => userId)
```

### onAfterHandle (Transform Response)

```typescript
.onAfterHandle(({ responseValue, set }) => {
  if (isHtml(responseValue))
    set.headers['content-type'] = 'text/html'
})
```

### mapResponse (Custom Response Mapping)

```typescript
.mapResponse(({ responseValue, set }) => {
  set.headers['content-encoding'] = 'gzip'
  return new Response(Bun.gzipSync(JSON.stringify(responseValue)))
})
```

### onError (Error Handling)

```typescript
import { Elysia, NotFoundError } from 'elysia'

.onError(({ code, error, status }) => {
  switch(code) {
    case 'NOT_FOUND': return status(404, 'Not Found')
    case 'VALIDATION': return { errors: error.all }
    case 'PARSE': return status(400, 'Invalid body')
    case 'INTERNAL_SERVER_ERROR': return status(500)
    default: return new Response(error.toString())
  }
})
```

### onAfterResponse (Cleanup, Logging)

```typescript
.onAfterResponse(({ set, request }) => {
  console.log(`${request.method} ${request.url} - ${set.status}`)
})
```

### Hook Scoping

```typescript
// Hooks are LOCAL by default in Elysia 1.0+
.onBeforeHandle({ as: 'local' }, handler)   // Current instance only
.onBeforeHandle({ as: 'scoped' }, handler)  // Parent + current + descendants
.onBeforeHandle({ as: 'global' }, handler)  // All instances
```

## TypeBox Validation (Elysia.t)

### Basic Types

```typescript
import { Elysia, t } from 'elysia'

.post('/user', handler, {
  body: t.Object({
    name: t.String({ minLength: 2, maxLength: 100 }),
    email: t.String({ format: 'email' }),
    age: t.Number({ minimum: 0, maximum: 150 }),
    active: t.Boolean(),
    tags: t.Array(t.String()),
    role: t.Union([t.Literal('admin'), t.Literal('user')]),
    metadata: t.Optional(t.Object({ createdAt: t.String() }))
  })
})
```

### Schema Locations

```typescript
.post('/example', handler, {
  body: t.Object({ ... }),       // Request body
  query: t.Object({ ... }),      // Query string
  params: t.Object({ ... }),     // Path params
  headers: t.Object({ ... }),    // Headers (lowercase keys!)
  cookie: t.Cookie({ ... }),     // Cookies
  response: t.Object({ ... })    // Response validation
})

// Response per status code
.get('/user', handler, {
  response: {
    200: t.Object({ user: UserSchema }),
    400: t.Object({ error: t.String() }),
    404: t.Object({ message: t.String() })
  }
})
```

### Elysia-Specific Types

```typescript
t.Numeric()                           // Coerces string to number (query/params)
t.File({ format: 'image/*' })         // Single file upload
t.Files()                             // Multiple files
t.Cookie({ session: t.String() }, {
  secure: true, httpOnly: true, sameSite: 'strict'
})
t.TemplateLiteral('Bearer ${string}') // Template literal validation
t.UnionEnum(['draft', 'published'])   // Enum-like union
```

### Custom Error Messages

```typescript
t.Object({
  email: t.String({
    format: 'email',
    error: 'Please provide a valid email'
  }),
  age: t.Number({
    minimum: 18,
    error({ value }) {
      return `Age must be 18+ (got ${value})`
    }
  })
})
```

### Standard Schema Support (Zod, Valibot)

```typescript
import { z } from 'zod'
import * as v from 'valibot'

.get('/user/:id', handler, {
  params: z.object({ id: z.coerce.number() }),
  query: v.object({ name: v.literal('test') })
})
```

## State Management

### state (Global Mutable Store)

```typescript
.state('counter', 0)
.state('users', new Map())
.get('/count', ({ store }) => store.counter++)
```

### decorate (Immutable Context Properties)

```typescript
.decorate('logger', new Logger())
.decorate('version', '1.0.0')
.decorate({ db: database, cache: redis })
.get('/', ({ logger, version }) => {
  logger.log('Request')
  return version
})
```

## Groups and Guards

### Groups (Route Prefixes)

```typescript
.group('/api/v1', app => app
  .get('/users', handler)
  .post('/users', handler)
)

// With guard configuration
.group('/admin', {
  headers: t.Object({ 'x-admin-key': t.String() })
}, app => app
  .get('/stats', handler)
)
```

### Guards (Shared Validation/Hooks)

```typescript
.guard({
  headers: t.Object({ authorization: t.String() }),
  beforeHandle: checkAuth
}, app => app
  .get('/protected1', handler1)
  .get('/protected2', handler2)
)
```

## Plugin Architecture

### Creating Plugins

```typescript
// As Elysia instance (recommended)
const userPlugin = new Elysia({ name: 'user' })
  .state('users', [])
  .decorate('userService', new UserService())
  .get('/users', ({ store }) => store.users)

// As function (access parent config)
const configPlugin = (config: Config) =>
  new Elysia({ name: 'config', seed: config })
    .decorate('config', config)

// Usage
new Elysia()
  .use(userPlugin)
  .use(configPlugin({ apiKey: '...' }))
```

### Plugin Scoping

```typescript
const authPlugin = new Elysia()
  .onBeforeHandle({ as: 'scoped' }, checkAuth) // Applies to parent too
  .derive({ as: 'global' }, getUser)           // Applies everywhere
  .as('scoped')                                 // Lift entire plugin
```

### Lazy Loading

```typescript
.use(import('./heavy-plugin'))
await app.modules // Wait for all async plugins
```

## WebSocket Support

### Basic WebSocket

```typescript
.ws('/ws', {
  message(ws, message) {
    ws.send('Received: ' + message)
  }
})
```

### Full WebSocket Handler

```typescript
.ws('/chat', {
  // Validation
  body: t.Object({ message: t.String() }),
  query: t.Object({ room: t.String() }),

  open(ws) {
    const { room } = ws.data.query
    ws.subscribe(room)
    ws.publish(room, 'User joined')
  },

  message(ws, { message }) {
    ws.publish(ws.data.query.room, message)
  },

  close(ws) {
    ws.publish(ws.data.query.room, 'User left')
  },

  // Authentication
  beforeHandle({ headers, status }) {
    if (!headers.authorization) return status(401)
  }
})
```

### WebSocket Methods

```typescript
ws.send(data)              // Send to connection
ws.publish(topic, data)    // Publish to topic
ws.subscribe(topic)        // Subscribe to topic
ws.unsubscribe(topic)      // Unsubscribe
ws.close()                 // Close connection
ws.data                    // Access context (query, params)
ws.id                      // Unique connection ID
```

## Macro Patterns

```typescript
const authPlugin = new Elysia({ name: 'auth' })
  .macro({
    isSignIn: {
      async resolve({ cookie, status }) {
        if (!cookie.session.value) return status(401)
        return { user: await getUser(cookie.session.value) }
      }
    }
  })

// Usage
.use(authPlugin)
.get('/profile', ({ user }) => user, { isSignIn: true })
```

## Official Plugins

### @elysiajs/openapi (API Documentation)

```typescript
import { openapi } from '@elysiajs/openapi'

.use(openapi({
  provider: 'scalar',        // 'scalar' | 'swagger-ui' | null
  path: '/docs',
  documentation: {
    info: { title: 'My API', version: '1.0.0' },
    tags: [{ name: 'User', description: 'User endpoints' }],
    components: {
      securitySchemes: {
        bearerAuth: { type: 'http', scheme: 'bearer', bearerFormat: 'JWT' }
      }
    }
  },
  exclude: { methods: ['OPTIONS'], paths: ['/health'] }
}))
.get('/user', handler, {
  detail: {
    tags: ['User'],
    summary: 'Get user',
    security: [{ bearerAuth: [] }]
  }
})
```

### @elysiajs/jwt (JSON Web Token)

```typescript
import { jwt } from '@elysiajs/jwt'

.use(jwt({
  name: 'jwt',
  secret: process.env.JWT_SECRET!,
  exp: '7d'
}))
.post('/login', async ({ jwt, body, cookie: { auth } }) => {
  const token = await jwt.sign({ userId: body.id })
  auth.set({ value: token, httpOnly: true, maxAge: 7 * 86400 })
  return { token }
})
.get('/profile', async ({ jwt, bearer, status }) => {
  const profile = await jwt.verify(bearer)
  if (!profile) return status(401)
  return profile
})
```

### @elysiajs/bearer (Token Extraction)

```typescript
import { bearer } from '@elysiajs/bearer'

.use(bearer())
.get('/protected', ({ bearer, status }) => {
  if (!bearer) return status(401)
  return `Token: ${bearer}`
})
```

### @elysiajs/cors (Cross-Origin)

```typescript
import { cors } from '@elysiajs/cors'

.use(cors({
  origin: ['https://app.example.com'],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true,
  maxAge: 600
}))
```

### @elysiajs/static (Static Files)

```typescript
import { staticPlugin } from '@elysiajs/static'

.use(staticPlugin({
  assets: 'public',
  prefix: '/static',
  indexHTML: true
}))
```

### @elysiajs/html (HTML/JSX)

```typescript
import { html } from '@elysiajs/html'

.use(html())
.get('/', () => `
  <html>
    <body><h1>Hello</h1></body>
  </html>
`)
```

### @elysiajs/cron (Scheduled Tasks)

```typescript
import { cron } from '@elysiajs/cron'

.use(cron({
  name: 'heartbeat',
  pattern: '*/10 * * * * *', // Every 10 seconds
  run() { console.log('tick') }
}))
```

### @elysiajs/graphql-yoga (GraphQL)

```typescript
import { yoga } from '@elysiajs/graphql-yoga'

.use(yoga({
  typeDefs: `type Query { hello: String }`,
  resolvers: { Query: { hello: () => 'Hello' } },
  path: '/graphql'
}))
```

### @elysiajs/trpc (tRPC Integration)

```typescript
import { trpc, compile as c } from '@elysiajs/trpc'
import { initTRPC } from '@trpc/server'

const tr = initTRPC.create()
const router = tr.router({
  greet: tr.procedure
    .input(c(t.String()))
    .query(({ input }) => `Hello ${input}`)
})

.use(trpc(router, { endpoint: '/trpc' }))
```

### @elysiajs/server-timing (Performance Headers)

```typescript
import { serverTiming } from '@elysiajs/server-timing'

.use(serverTiming({
  enabled: process.env.NODE_ENV !== 'production'
}))
```

## Eden Treaty (Type-Safe Client)

### Setup

```typescript
// server.ts
const app = new Elysia()
  .get('/user/:id', ({ params }) => ({ id: params.id }))
  .post('/user', ({ body }) => body, {
    body: t.Object({ name: t.String() })
  })
  .listen(3000)

export type App = typeof app

// client.ts
import { treaty } from '@elysiajs/eden'
import type { App } from './server'

const api = treaty<App>('localhost:3000')
```

### Path Syntax

```typescript
api.index.get()                    // /
api.user({ id: '123' }).get()      // /user/123
api.deep.nested.path.get()         // /deep/nested/path
```

### Request Parameters

```typescript
// POST with body
const { data, error } = await api.user.post({ name: 'John' })

// With headers/query
await api.user.post({ name: 'John' }, {
  headers: { authorization: 'Bearer token' },
  query: { source: 'web' }
})

// GET with query
await api.users.get({ query: { page: 1, limit: 10 } })
```

### Error Handling

```typescript
const { data, error, status } = await api.user.post({ name })

if (error) {
  switch(error.status) {
    case 400: throw new ValidationError(error.value)
    case 401: throw new AuthError(error.value)
    default: throw error.value
  }
}

return data // Type-safe, non-null after error check
```

### WebSocket Client

```typescript
const chat = api.chat.subscribe()

chat.on('open', () => chat.send('hello'))
chat.subscribe(message => console.log(message))
chat.raw // Native WebSocket access
```

### Stream Handling

```typescript
const { data } = await api.stream.get()
for await (const chunk of data) {
  console.log(chunk)
}
```

### Eden Configuration

```typescript
const api = treaty<App>('localhost:3000', {
  fetch: { credentials: 'include' },
  headers: { authorization: 'Bearer token' },
  headers: (path) => ({ /* dynamic headers */ }),
  onRequest: (path, options) => { /* modify request */ },
  onResponse: (response) => { /* modify response */ }
})
```

### Unit Testing with Eden

```typescript
import { treaty } from '@elysiajs/eden'
import { app } from './server'

// Pass instance directly - no network calls
const api = treaty(app)

const { data } = await api.user.post({ name: 'Test' })
expect(data.name).toBe('Test')
```

## Testing Patterns

### Unit Testing with bun:test

```typescript
import { describe, expect, it } from 'bun:test'
import { Elysia } from 'elysia'

describe('API', () => {
  const app = new Elysia()
    .get('/hello', () => 'Hello')
    .post('/user', ({ body }) => body)

  it('returns hello', async () => {
    const res = await app.handle(new Request('http://localhost/hello'))
    expect(await res.text()).toBe('Hello')
  })

  it('creates user', async () => {
    const res = await app.handle(new Request('http://localhost/user', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: 'Test' })
    }))
    expect(await res.json()).toEqual({ name: 'Test' })
  })
})
```

### Testing with Eden

```typescript
import { treaty } from '@elysiajs/eden'
import { app } from './server'

const api = treaty(app)

it('should create user with type safety', async () => {
  const { data, error } = await api.users.post({
    name: 'John',
    email: 'john@example.com'
  })

  expect(error).toBeNull()
  expect(data?.name).toBe('John')
})
```

## Production Patterns

### Recommended Project Structure

```
src/
├── modules/
│   ├── auth/
│   │   ├── index.ts       # Routes
│   │   ├── service.ts     # Business logic
│   │   └── model.ts       # TypeBox schemas
│   ├── user/
│   └── product/
├── shared/
│   ├── middleware/
│   └── utils/
├── config/
│   └── env.ts
├── index.ts
└── server.ts
```

### Module Pattern

```typescript
// src/modules/user/index.ts
import { Elysia } from 'elysia'
import { UserService } from './service'
import { CreateUserSchema, UserSchema } from './model'

export const userRoutes = new Elysia({ prefix: '/users' })
  .post('/', ({ body }) => UserService.create(body), {
    body: CreateUserSchema,
    response: UserSchema
  })
  .get('/:id', ({ params }) => UserService.findById(params.id))
```

### Production Build

```bash
# Compile to binary
bun build --compile --minify-whitespace --minify-syntax \
  --target bun-linux-x64 --outfile server src/index.ts
```

### Cluster Mode

```typescript
import cluster from 'node:cluster'
import os from 'node:os'

if (cluster.isPrimary) {
  for (let i = 0; i < os.availableParallelism(); i++) {
    cluster.fork()
  }
} else {
  await import('./server')
}
```

## Best Practices

1. **Always use method chaining** - Maintains type inference
2. **Name plugins** - Enables deduplication
3. **Use resolve over derive** - When validation is needed first
4. **Export type App** - For Eden client type safety
5. **Use guards** - For shared validation across routes
6. **Local hooks by default** - Explicit `as: 'scoped'` or `as: 'global'`
7. **Extract services** - Outside Elysia for testability
8. **Use status() function** - For type-safe status responses

## References

See <reference/core-api.md> for complete API documentation.
See <reference/lifecycle-hooks.md> for hook execution details.
See <reference/plugins.md> for all plugin configurations.
See <patterns/authentication.md> for auth implementations.
See <patterns/testing.md> for testing strategies.
