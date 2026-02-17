---
name: effect-http-server
description: Explains how to define http servers with effect. Use only when a top-level server is, or needs to be written in effect.
---

## Structure

```
HttpApi
├── HttpApiGroup
│   ├── HttpApiEndpoint
│   └── HttpApiEndpoint
```

## Defining Endpoints

```ts
import { HttpApiEndpoint, HttpApiSchema, HttpApiError } from "@effect/platform"
import { Schema } from "effect"

const User = Schema.Struct({
  id: Schema.Number,
  name: Schema.String,
  createdAt: Schema.DateTimeUtc
})

const idParam = HttpApiSchema.param("id", Schema.NumberFromString)

// GET with path param (template string syntax)
const getUser = HttpApiEndpoint.get("getUser")`/users/${idParam}`
  .addSuccess(User)
  .addError(HttpApiError.NotFound) // 404

// GET with URL params
const listUsers = HttpApiEndpoint.get("listUsers", "/users")
  .setUrlParams(Schema.Struct({
    page: Schema.NumberFromString,
    sort: Schema.String
  }))
  .addSuccess(Schema.Array(User))

// POST with payload
const createUser = HttpApiEndpoint.post("createUser", "/users")
  .setPayload(Schema.Struct({ name: Schema.String }))
  .addSuccess(User, { status: 201 })

// DELETE
const deleteUser = HttpApiEndpoint.del("deleteUser")`/users/${idParam}`

// PATCH
const updateUser = HttpApiEndpoint.patch("updateUser")`/users/${idParam}`
  .setPayload(Schema.Struct({ name: Schema.String }))
  .addSuccess(User)

// Headers (keys must be lowercase)
const withHeaders = HttpApiEndpoint.get("withHeaders", "/")
  .setHeaders(Schema.Struct({
    "x-api-key": Schema.String,
    "x-request-id": Schema.String
  }))
```

## Grouping & API Assembly

```ts
import { HttpApi, HttpApiGroup } from "@effect/platform"

class UserNotFound extends Schema.TaggedError<UserNotFound>()("UserNotFound", {}) {}
class Unauthorized extends Schema.TaggedError<Unauthorized>()("Unauthorized", {}) {}

const usersGroup = HttpApiGroup.make("users")
  .add(getUser)
  .add(listUsers)
  .add(createUser)
  .add(deleteUser)
  .add(updateUser)
  .addError(Unauthorized, { status: 401 }) // group-level error

const api = HttpApi.make("myApi")
  .add(usersGroup)
  .prefix("/api/v1") // optional prefix
```

## Implementation

```ts
import { HttpApiBuilder } from "@effect/platform"
import { Context, Effect, Layer, DateTime } from "effect"

// Service for handlers
class UsersRepo extends Context.Tag("UsersRepo")<UsersRepo, {
  findById: (id: number) => Effect.Effect<typeof User.Type>
}>() {}

// Implement group handlers
const usersGroupLive = HttpApiBuilder.group(api, "users", (handlers) =>
  Effect.gen(function* () {
    const repo = yield* UsersRepo
    return handlers
      .handle("getUser", ({ path: { id } }) => repo.findById(id))
      .handle("listUsers", ({ urlParams: { page, sort } }) =>
        Effect.succeed([{ id: 1, name: "John", createdAt: DateTime.unsafeNow() }])
      )
      .handle("createUser", ({ payload: { name } }) =>
        Effect.succeed({ id: 2, name, createdAt: DateTime.unsafeNow() })
      )
      .handle("deleteUser", ({ path: { id } }) => Effect.void)
      .handle("updateUser", ({ path: { id }, payload: { name } }) =>
        Effect.succeed({ id, name, createdAt: DateTime.unsafeNow() })
      )
      // Access raw request if needed
      .handle("withHeaders", ({ request, headers }) =>
        Effect.succeed(`method: ${request.method}, key: ${headers["x-api-key"]}`)
      )
  })
)

// Combine into API layer
const MyApiLive = HttpApiBuilder.api(api).pipe(Layer.provide(usersGroupLive))
```

## Serving

```ts
import { HttpApiSwagger, HttpMiddleware, HttpServer } from "@effect/platform"
import { NodeHttpServer, NodeRuntime } from "@effect/platform-node"
import { createServer } from "node:http"

const ServerLive = HttpApiBuilder.serve(HttpMiddleware.logger).pipe(
  Layer.provide(HttpApiSwagger.layer()),           // /docs
  Layer.provide(HttpApiBuilder.middlewareCors()),  // CORS
  Layer.provide(MyApiLive),
  HttpServer.withLogAddress,
  Layer.provide(NodeHttpServer.layer(createServer, { port: 3000 }))
)

Layer.launch(ServerLive).pipe(NodeRuntime.runMain)
```

## Client

```ts
import { HttpApiClient, FetchHttpClient } from "@effect/platform"

const program = Effect.gen(function* () {
  const client = yield* HttpApiClient.make(api, { baseUrl: "http://localhost:3000" })
  const user = yield* client.users.getUser({ path: { id: 1 } })
})

program.pipe(Effect.provide(FetchHttpClient.layer), Effect.runPromise)
```

## Custom Encoding

```ts
// URL-encoded request
const urlEncoded = HttpApiEndpoint.post("urlEncoded", "/form")
  .setPayload(
    Schema.Struct({ a: Schema.String })
      .pipe(HttpApiSchema.withEncoding({ kind: "UrlParams" }))
  )

// CSV response
const csv = HttpApiEndpoint.get("csv", "/export")
  .addSuccess(
    Schema.String.pipe(HttpApiSchema.withEncoding({
      kind: "Text",
      contentType: "text/csv"
    }))
  )
```

## Predefined Errors

| Error | Status |
|-------|--------|
| `HttpApiError.BadRequest` | 400 |
| `HttpApiError.Unauthorized` | 401 |
| `HttpApiError.Forbidden` | 403 |
| `HttpApiError.NotFound` | 404 |
| `HttpApiError.Conflict` | 409 |
| `HttpApiError.InternalServerError` | 500 |

## Additional Resources

[For deriving http clients](./effect-derive-http-client.md)
[For creating middlewares](./effect-http-middleware.md)
[For deriving swagger UIs](./effect-http-swagger.md)
[For multipart uploads](./effect-http-multipart.md)
[For streaming](./effect-http-streaming.md)