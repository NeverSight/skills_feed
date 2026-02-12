---
name: hummingbird
description: 'Expert guidance on Hummingbird 2 web framework. Use when developers mention: (1) Hummingbird, HB, or Hummingbird 2, (2) Swift web server or HTTP server, (3) server-side Swift routing or middleware, (4) building REST APIs in Swift, (5) RequestContext or ChildRequestContext, (6) HummingbirdAuth or authentication middleware, (7) HummingbirdWebSocket, (8) HummingbirdFluent or database integration, (9) ResponseGenerator or EditedResponse.'
---

# Hummingbird 2

Hummingbird is a lightweight, flexible HTTP server framework for Swift, built on SwiftNIO with full Swift Concurrency support. It's an SSWG (Swift Server Work Group) incubated project.

## Quick Start

### Installation

Add to `Package.swift`:

```swift
dependencies: [
    .package(url: "https://github.com/hummingbird-project/hummingbird.git", from: "2.0.0")
]
```

Add to your target:

```swift
.target(
    name: "App",
    dependencies: [
        .product(name: "Hummingbird", package: "hummingbird")
    ]
)
```

### Minimal Application

```swift
import Hummingbird

@main
struct App {
    static func main() async throws {
        let router = Router()

        router.get("/") { _, _ in
            "Hello, World!"
        }

        router.get("/health") { _, _ -> HTTPResponse.Status in
            .ok
        }

        let app = Application(
            router: router,
            configuration: .init(address: .hostname("0.0.0.0", port: 8080))
        )

        try await app.runService()
    }
}
```

## Core Concepts

### Router

The router directs requests to handlers based on path and HTTP method:

```swift
let router = Router()

// Basic routes
router.get("/users") { request, context in
    // Return all users
}

router.post("/users") { request, context in
    // Create user
}

router.get("/users/{id}") { request, context in
    let id = context.parameters.get("id")!
    // Return user by ID
}

router.put("/users/{id}") { request, context in
    // Update user
}

router.delete("/users/{id}") { request, context in
    // Delete user
}
```

### Route Groups

Organize routes with common prefixes:

```swift
let router = Router()

router.group("api/v1") { api in
    api.group("users") { users in
        users.get { _, _ in /* list users */ }
        users.post { _, _ in /* create user */ }
        users.get("{id}") { _, context in /* get user */ }
    }

    api.group("posts") { posts in
        posts.get { _, _ in /* list posts */ }
    }
}
```

### Request Context

Each request gets a context instance. Use `BasicRequestContext` or create custom contexts:

```swift
// Using basic context
let router = Router(context: BasicRequestContext.self)

// Custom context for additional properties
struct AppRequestContext: RequestContext {
    var coreContext: CoreRequestContextStorage
    var requestId: String?
    var authenticatedUser: User?

    init(source: Source) {
        self.coreContext = .init(source: source)
    }
}

let router = Router(context: AppRequestContext.self)
```

### Child Request Context

Use `ChildRequestContext` to transform contexts and guarantee properties exist:

```swift
import HummingbirdAuth

// Parent context with optional authentication
struct AppRequestContext: AuthRequestContext {
    var coreContext: CoreRequestContextStorage
    var auth: LoginCache

    init(source: Source) {
        self.coreContext = .init(source: source)
        self.auth = .init()
    }
}

// Child context guarantees authenticated user
struct AuthenticatedContext: ChildRequestContext {
    typealias ParentContext = AppRequestContext

    var coreContext: CoreRequestContextStorage
    var user: User  // Non-optional, guaranteed to exist

    init(context: AppRequestContext) throws {
        self.coreContext = context.coreContext
        self.user = try context.auth.require(User.self)
    }
}

// Use in routes
let router = Router(context: AppRequestContext.self)

router.group("api")
    .add(middleware: BearerAuthenticator())
    .group(context: AuthenticatedContext.self) { protected in
        // All routes here have guaranteed user
        protected.get("/me") { _, context -> User in
            context.user  // Non-optional access
        }
    }
```

See `references/request-context.md` for detailed patterns including multi-level child contexts and protocol composition.

### Route Handlers

Handlers receive `Request` and `Context`, returning any `ResponseGenerator`:

```swift
// Return String
router.get("/hello") { _, _ in
    "Hello, World!"
}

// Return HTTP status
router.get("/health") { _, _ -> HTTPResponse.Status in
    .ok
}

// Return Codable (auto-encoded to JSON)
router.get("/user") { _, _ -> User in
    User(id: 1, name: "Alice")
}

// Return full Response
router.get("/custom") { _, _ -> Response in
    Response(
        status: .ok,
        headers: [.contentType: "text/plain"],
        body: .init(byteBuffer: ByteBuffer(string: "Custom response"))
    )
}
```

## Request Handling

### Path Parameters

```swift
router.get("/users/{id}") { request, context in
    let id = context.parameters.get("id")!
    return "User ID: \(id)"
}

router.get("/posts/{postId}/comments/{commentId}") { request, context in
    let postId = context.parameters.get("postId")!
    let commentId = context.parameters.get("commentId")!
    return "Post \(postId), Comment \(commentId)"
}
```

### Query Parameters

```swift
router.get("/search") { request, context in
    let query = request.uri.queryParameters.get("q") ?? ""
    let page = request.uri.queryParameters.get("page").flatMap(Int.init) ?? 1
    return "Searching for '\(query)' on page \(page)"
}
```

### Request Body (JSON)

```swift
struct CreateUserRequest: Decodable {
    let name: String
    let email: String
}

router.post("/users") { request, context in
    let input = try await request.decode(as: CreateUserRequest.self, context: context)
    // Create user with input.name, input.email
    return HTTPResponse.Status.created
}
```

### Headers

```swift
router.get("/protected") { request, context in
    guard let auth = request.headers[.authorization] else {
        throw HTTPError(.unauthorized)
    }
    // Process authorization header
    return "Authorized"
}
```

## Response Handling

### ResponseCodable

Types conforming to `ResponseCodable` auto-encode to JSON:

```swift
struct User: ResponseCodable {
    let id: Int
    let name: String
    let email: String
}

router.get("/users/{id}") { request, context -> User in
    return User(id: 1, name: "Alice", email: "alice@example.com")
}
```

### EditedResponse

Control status code and headers with response body:

```swift
router.post("/users") { request, context -> EditedResponse<User> in
    let user = User(id: 1, name: "Alice", email: "alice@example.com")
    return EditedResponse(
        status: .created,
        headers: [.location: "/users/1"],
        response: user
    )
}
```

### HTTPError

Throw errors for HTTP error responses:

```swift
router.get("/users/{id}") { request, context in
    guard let user = findUser(id: context.parameters.get("id")!) else {
        throw HTTPError(.notFound, message: "User not found")
    }
    return user
}
```

## Middleware

Middleware processes requests before handlers and responses after:

```swift
struct LoggingMiddleware<Context: RequestContext>: RouterMiddleware {
    func handle(
        _ request: Request,
        context: Context,
        next: (Request, Context) async throws -> Response
    ) async throws -> Response {
        let start = ContinuousClock.now
        let response = try await next(request, context)
        let duration = ContinuousClock.now - start
        print("\(request.method) \(request.uri.path) - \(response.status) (\(duration))")
        return response
    }
}

// Apply to router
router.middlewares.add(LoggingMiddleware())

// Apply to route group
router.group("api") { api in
    api.middlewares.add(AuthMiddleware())
    api.get("/protected") { _, _ in "Secret data" }
}
```

### Built-in Middleware

```swift
import Hummingbird

// CORS
router.middlewares.add(CORSMiddleware(
    allowOrigin: .originBased,
    allowHeaders: [.contentType, .authorization],
    allowMethods: [.get, .post, .put, .delete]
))

// File serving
router.middlewares.add(FileMiddleware(rootFolder: "public"))

// Metrics (with swift-metrics)
router.middlewares.add(MetricsMiddleware())

// Tracing (with swift-distributed-tracing)
router.middlewares.add(TracingMiddleware())
```

## Application Configuration

```swift
let app = Application(
    router: router,
    configuration: .init(
        address: .hostname("0.0.0.0", port: 8080),
        serverName: "MyApp"
    )
)

try await app.runService()
```

### With ServiceLifecycle

```swift
import Hummingbird
import ServiceLifecycle

@main
struct App {
    static func main() async throws {
        let router = Router()
        // ... configure routes

        let app = Application(
            router: router,
            configuration: .init(address: .hostname("0.0.0.0", port: 8080))
        )

        let serviceGroup = ServiceGroup(
            services: [app],
            gracefulShutdownSignals: [.sigterm, .sigint],
            logger: Logger(label: "app")
        )

        try await serviceGroup.run()
    }
}
```

## Extensions

### Authentication (HummingbirdAuth)

```swift
.product(name: "HummingbirdAuth", package: "hummingbird-auth")
```

```swift
import HummingbirdAuth

// Context with authentication
struct AppRequestContext: AuthRequestContext {
    var coreContext: CoreRequestContextStorage
    var auth: LoginCache

    init(source: Source) {
        self.coreContext = .init(source: source)
        self.auth = .init()
    }
}

// Bearer token authentication
router.group("api")
    .add(middleware: BearerAuthenticator())
    .get("/me") { request, context -> User in
        let user = try context.auth.require(User.self)
        return user
    }
```

### WebSockets (HummingbirdWebSocket)

```swift
.product(name: "HummingbirdWebSocket", package: "hummingbird-websocket")
```

```swift
import HummingbirdWebSocket

router.ws("/chat") { inbound, outbound, context in
    for try await message in inbound {
        switch message {
        case .text(let text):
            try await outbound.write(.text("Echo: \(text)"))
        case .binary(let data):
            try await outbound.write(.binary(data))
        }
    }
}
```

### Fluent ORM (HummingbirdFluent)

```swift
.product(name: "HummingbirdFluent", package: "hummingbird-fluent")
```

```swift
import HummingbirdFluent
import FluentPostgresDriver

// Add Fluent to application
let fluent = Fluent(logger: logger)
fluent.databases.use(.postgres(configuration: postgresConfig), as: .psql)

let app = Application(
    router: router,
    configuration: .init(address: .hostname("0.0.0.0", port: 8080))
)
app.addServices(fluent)
```

### HTTP/2 and TLS

```swift
.product(name: "HummingbirdHTTP2", package: "hummingbird")
.product(name: "HummingbirdTLS", package: "hummingbird")
```

## Testing

```swift
import HummingbirdTesting
import Testing

@Test func testHealthEndpoint() async throws {
    let router = Router()
    router.get("/health") { _, _ -> HTTPResponse.Status in .ok }

    let app = Application(router: router)

    try await app.test(.router) { client in
        try await client.execute(uri: "/health", method: .get) { response in
            #expect(response.status == .ok)
        }
    }
}

@Test func testCreateUser() async throws {
    let app = buildApplication()

    try await app.test(.router) { client in
        let user = CreateUserRequest(name: "Alice", email: "alice@example.com")

        try await client.execute(
            uri: "/users",
            method: .post,
            headers: [.contentType: "application/json"],
            body: JSONEncoder().encodeAsByteBuffer(user, allocator: .init())
        ) { response in
            #expect(response.status == .created)
        }
    }
}
```

## Best Practices

### 1. Use Custom Request Contexts

Extend contexts for type-safe access to authentication, database connections, etc:

```swift
struct AppRequestContext: AuthRequestContext {
    var coreContext: CoreRequestContextStorage
    var auth: LoginCache

    init(source: Source) {
        self.coreContext = .init(source: source)
        self.auth = .init()
    }
}
```

### 2. Organize Routes

Split routes into separate files/functions:

```swift
// UserRoutes.swift
func addUserRoutes(to router: Router<AppRequestContext>) {
    router.group("users") { users in
        users.get { _, _ in /* list */ }
        users.post { _, _ in /* create */ }
        users.get("{id}") { _, _ in /* get */ }
    }
}

// Application setup
let router = Router(context: AppRequestContext.self)
addUserRoutes(to: router)
addPostRoutes(to: router)
```

### 3. Use Middleware for Cross-Cutting Concerns

Apply authentication, logging, and metrics via middleware rather than in handlers.

### 4. Handle Errors Gracefully

```swift
router.get("/users/{id}") { request, context in
    guard let id = context.parameters.get("id"),
          let user = try await userService.find(id: id) else {
        throw HTTPError(.notFound, message: "User not found")
    }
    return user
}
```

## Reference Files

Load these files as needed for specific topics:

- **`references/request-context.md`** - RequestContext protocol, ChildRequestContext, protocol composition, AuthRequestContext, multi-level contexts
- **`references/routing.md`** - Advanced routing patterns, result builder router, wildcards
- **`references/middleware.md`** - Custom middleware, authentication, CORS, file serving
- **`references/testing.md`** - Testing strategies, mocking, integration tests
