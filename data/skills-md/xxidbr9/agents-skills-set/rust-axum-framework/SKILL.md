---
name: rust-axum-framework
description: Complete guide for Axum web framework including routing, extractors, middleware, state management, error handling, and production deployment
tags: [axum, rust, web-framework, tokio, tower, async, rest-api]
tier: tier-1
---

# Rust Axum Framework

A comprehensive skill for building production-ready web applications and APIs using Axum, the ergonomic and modular Rust web framework built on Tokio and Tower. Master routing, extractors, middleware, state management, error handling, and deployment patterns.

## When to Use This Skill

Use this skill when:

- Building REST APIs with Rust and async/await
- Creating high-performance web services with type safety
- Developing microservices with Tokio ecosystem integration
- Implementing WebSocket servers or Server-Sent Events (SSE)
- Building GraphQL APIs with Rust backend
- Creating middleware-heavy applications requiring Tower integration
- Developing production-ready web applications requiring robust error handling
- Building systems requiring fine-grained control over HTTP request/response handling
- Implementing authentication, authorization, and security middleware
- Creating real-time web applications with async Rust
- Developing APIs requiring request validation and transformation
- Building web services with complex routing and nested routers
- Implementing rate limiting, timeout, and backpressure handling
- Creating web applications requiring custom extractors and response types

## Core Concepts

### Axum Architecture Philosophy

Axum is built on three fundamental pillars:

1. **Tower Services**: Everything in Axum is built on Tower's `Service` trait, providing composability and middleware integration
2. **Type-Safe Extractors**: Request data extraction is compile-time checked, eliminating runtime parsing errors
3. **Minimal Boilerplate**: Ergonomic APIs that reduce ceremony while maintaining explicitness

### The Router

The `Router` is the central building block in Axum. It maps HTTP requests to handlers based on path and method.

**Key Properties:**
- Routes are matched in the order they're defined
- Routers can be nested for modular organization
- Middleware can be applied at router, route, or method level
- Generic over state type for flexible state management
- Implements Tower's `Service` trait for composability

**Router Creation:**
```rust
use axum::{Router, routing::get};

let app = Router::new()
    .route("/", get(handler))
    .route("/users/{id}", get(get_user))
    .route("/posts", get(list_posts).post(create_post));
```

### Handlers

Handlers are async functions that process requests and return responses. Axum supports multiple handler signatures through its powerful type system.

**Handler Requirements:**
- Must be async functions
- Can extract data from requests using extractors
- Must return types implementing `IntoResponse`
- Can have up to 16 parameters (all must be extractors)

**Common Handler Patterns:**
```rust
// Simple handler
async fn handler() -> &'static str {
    "Hello, World!"
}

// Handler with path parameter
async fn get_user(Path(user_id): Path<u32>) -> String {
    format!("User ID: {}", user_id)
}

// Handler with multiple extractors
async fn create_user(
    State(state): State<AppState>,
    Json(payload): Json<CreateUser>,
) -> Result<Json<User>, StatusCode> {
    // Implementation
}
```

### Extractors

Extractors are types that implement `FromRequest` or `FromRequestParts`, allowing type-safe extraction of data from requests.

**Built-in Extractors:**

1. **Path** - Extract path parameters
2. **Query** - Extract query string parameters
3. **Json** - Parse JSON request body
4. **Form** - Parse form-encoded request body
5. **State** - Access shared application state
6. **Extension** - Access request extensions
7. **Headers** - Access request headers
8. **Method** - Get HTTP method
9. **Uri** - Get request URI
10. **Request** - Get full request
11. **Bytes** - Raw request body as bytes
12. **String** - Request body as UTF-8 string
13. **Multipart** - Handle multipart/form-data

**Extractor Ordering:**
- Extractors that consume the request body must come last
- Multiple body extractors in one handler will cause compilation errors
- `State` and other non-body extractors can be in any order

### Responses

Any type implementing `IntoResponse` can be returned from handlers. Axum provides many built-in implementations.

**Built-in Response Types:**
- `String`, `&'static str` - Text responses
- `Json<T>` - JSON responses
- `Html<String>` - HTML responses
- `StatusCode` - Status-only responses
- `(StatusCode, T)` - Status with body
- `(Parts, T)` - Custom headers with body
- `Response` - Full control over response
- `Result<T, E>` - Error handling (where E: IntoResponse)

### State Management

Axum uses the `State` extractor to share data across handlers. State must implement `Clone` and is typically wrapped in `Arc` for shared ownership.

**State Patterns:**

1. **Simple State:**
```rust
#[derive(Clone)]
struct AppState {
    api_key: String,
}

let app = Router::new()
    .route("/", get(handler))
    .with_state(AppState {
        api_key: "secret".to_string(),
    });
```

2. **Shared State with Arc:**
```rust
#[derive(Clone)]
struct AppState {
    db_pool: Arc<DatabasePool>,
    cache: Arc<RwLock<Cache>>,
}
```

3. **Multiple State Types:**
```rust
// Define separate state types for different router sections
let api_router: Router<ApiState> = Router::new()
    .route("/api/data", get(api_handler));

let app_router: Router<AppState> = Router::new()
    .route("/app", get(app_handler));

// Combine with final state
let app = Router::new()
    .nest("/", app_router.with_state(app_state))
    .nest("/", api_router.with_state(api_state));
```

### Middleware

Middleware in Axum comes from Tower and provides request/response transformation, logging, authentication, and more.

**Middleware Categories:**

1. **Tower Middleware** - From `tower` and `tower-http` crates
2. **Custom Middleware** - Using `middleware::from_fn`
3. **Service Middleware** - Implementing Tower's `Service` trait
4. **Layer Pattern** - Using Tower's `Layer` for composability

**Middleware Application Order:**
- Applied with `.layer()` executes bottom-to-top (wrapping previous layers)
- Applied with `ServiceBuilder` executes top-to-bottom (more intuitive)
- Middleware on `Router::layer` runs after routing
- Middleware around `Router` (using `Layer::layer`) runs before routing

### Error Handling

Axum's error handling is built on the `IntoResponse` trait, allowing custom error types to be converted to HTTP responses.

**Error Handling Strategies:**

1. **Result Types:**
```rust
async fn handler() -> Result<Json<Data>, StatusCode> {
    // Returns 200 OK or error status code
}
```

2. **Custom Error Types:**
```rust
enum AppError {
    Database(sqlx::Error),
    NotFound,
    Unauthorized,
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        // Convert to HTTP response
    }
}
```

3. **HandleErrorLayer:**
```rust
use axum::error_handling::HandleErrorLayer;

let app = Router::new()
    .layer(
        ServiceBuilder::new()
            .layer(HandleErrorLayer::new(handle_error))
            .layer(TimeoutLayer::new(Duration::from_secs(30)))
    );
```

### Tower Integration

Axum is built on Tower, enabling powerful middleware composition and service abstraction.

**Key Tower Concepts:**

1. **Service Trait** - Asynchronous request processing
2. **Layer Trait** - Middleware factory pattern
3. **ServiceBuilder** - Ergonomic middleware composition
4. **Timeout** - Request timeout handling
5. **RateLimit** - Request rate limiting
6. **LoadShed** - Backpressure management
7. **Buffer** - Request buffering

## Routing

### Basic Routing

Routes map HTTP methods and paths to handlers:

```rust
use axum::{
    Router,
    routing::{get, post, put, delete, patch},
};

let app = Router::new()
    .route("/", get(root))
    .route("/users", get(list_users).post(create_user))
    .route("/users/{id}", get(get_user).put(update_user).delete(delete_user))
    .route("/posts/{id}/comments", get(get_comments).post(add_comment));
```

### Path Parameters

Extract dynamic segments from paths:

```rust
use axum::extract::Path;
use serde::Deserialize;

// Single parameter
async fn get_user(Path(user_id): Path<u32>) -> String {
    format!("User {}", user_id)
}

// Multiple parameters
#[derive(Deserialize)]
struct PostPath {
    user_id: u32,
    post_id: u32,
}

async fn get_post(Path(params): Path<PostPath>) -> String {
    format!("User {} Post {}", params.user_id, params.post_id)
}

// Using tuple for multiple params
async fn get_comment(
    Path((post_id, comment_id)): Path<(u32, u32)>
) -> String {
    format!("Post {} Comment {}", post_id, comment_id)
}
```

### Wildcard Routes

Capture remaining path segments:

```rust
// Captures all remaining path
async fn handler(Path(path): Path<String>) -> String {
    format!("Captured path: {}", path)
}

let app = Router::new()
    .route("/{*key}", get(handler));

// GET /foo/bar/baz -> path = "foo/bar/baz"
```

**Important:** Nested routers strip matched prefixes, but wildcard routes retain the full URI.

### Nested Routers

Organize routes into modules using router nesting:

```rust
use axum::{Router, routing::get};

fn api_routes() -> Router {
    Router::new()
        .route("/users", get(list_users))
        .route("/users/{id}", get(get_user))
        .route("/posts", get(list_posts))
}

fn admin_routes() -> Router {
    Router::new()
        .route("/dashboard", get(dashboard))
        .route("/settings", get(settings))
}

let app = Router::new()
    .nest("/api", api_routes())
    .nest("/admin", admin_routes())
    .route("/", get(root));
```

**Important:** Merged routers can cause unexpected behavior as it collides with other routes.

### Merged Routers

Combining routes into modules using merge:

```rust
use axum::{Router, routing::get};

fn api_routes() -> Router {
    Router::new()
        .route("/users", get(list_users))
        .route("/users/{id}", get(get_user))
        .route("/posts", get(list_posts))
}

fn admin_routes() -> Router {
    Router::new()
        .route("/dashboard", get(dashboard))
        .route("/settings", get(settings))
}

let app = Router::new()
    .merge(api_routes())
    .merge(admin_routes())
    .route("/", get(root));
```

**Nesting Behavior:**
- Matched prefix is stripped from URI before passing to nested router
- Handlers in nested routers only see path relative to nest point
- Fallback handlers are inherited from parent if not defined in child
- Middleware can be applied before or after nesting

### Fallback Handlers

Handle unmatched routes:

```rust
use axum::{http::StatusCode, handler::Handler};

async fn fallback() -> (StatusCode, &'static str) {
    (StatusCode::NOT_FOUND, "Not Found")
}

let app = Router::new()
    .route("/", get(handler))
    .fallback(fallback);
```

**Fallback Inheritance:**
```rust
async fn api_fallback() -> (StatusCode, &'static str) {
    (StatusCode::NOT_FOUND, "API endpoint not found")
}

let api = Router::new()
    .route("/users", get(list_users))
    .fallback(api_fallback);

let app = Router::new()
    .nest("/api", api)
    .fallback(fallback); // Used for non-/api routes
```

### Method Routing

Handle multiple HTTP methods on the same route:

```rust
use axum::routing::{get, post, MethodRouter};

// Multiple methods on one route
let app = Router::new()
    .route("/users", get(list_users).post(create_user));

// Different handlers per method
let app = Router::new()
    .route("/resource",
        get(get_resource)
            .post(create_resource)
            .put(update_resource)
            .delete(delete_resource)
            .patch(patch_resource)
    );
```

## Extractors Deep Dive

### Path Extractor

Extract typed path parameters:

```rust
use axum::extract::Path;
use serde::Deserialize;

// Simple extraction
async fn user_by_id(Path(id): Path<u32>) -> String {
    format!("User {}", id)
}

// Complex extraction
#[derive(Deserialize)]
struct Params {
    org: String,
    repo: String,
    issue: u32,
}

async fn github_issue(Path(params): Path<Params>) -> String {
    format!("{}/{} issue #{}", params.org, params.repo, params.issue)
}

let app = Router::new()
    .route("/users/{id}", get(user_by_id))
    .route("/repos/:org/:repo/issues/:issue", get(github_issue));
```

### Query Extractor

Extract query string parameters:

```rust
use axum::extract::Query;
use serde::Deserialize;

#[derive(Deserialize)]
struct Pagination {
    page: Option<u32>,
    per_page: Option<u32>,
}

async fn list_users(Query(pagination): Query<Pagination>) -> String {
    let page = pagination.page.unwrap_or(1);
    let per_page = pagination.per_page.unwrap_or(20);
    format!("Page {} with {} items", page, per_page)
}

// GET /users?page=2&per_page=50
```

### Json Extractor

Parse JSON request bodies:

```rust
use axum::extract::Json;
use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
struct CreateUser {
    username: String,
    email: String,
}

#[derive(Serialize)]
struct User {
    id: u32,
    username: String,
    email: String,
}

async fn create_user(Json(payload): Json<CreateUser>) -> Json<User> {
    let user = User {
        id: 123,
        username: payload.username,
        email: payload.email,
    };
    Json(user)
}
```

**JSON Error Handling:**
```rust
use axum::extract::rejection::JsonRejection;
use axum::http::StatusCode;

async fn create_user(
    payload: Result<Json<CreateUser>, JsonRejection>
) -> Result<Json<User>, (StatusCode, String)> {
    match payload {
        Ok(Json(create_user)) => {
            // Valid JSON
            Ok(Json(User { /* ... */ }))
        }
        Err(JsonRejection::MissingJsonContentType(_)) => {
            Err((
                StatusCode::BAD_REQUEST,
                "Missing `Content-Type: application/json`".to_string(),
            ))
        }
        Err(JsonRejection::JsonDataError(err)) => {
            Err((
                StatusCode::BAD_REQUEST,
                format!("Invalid JSON: {}", err),
            ))
        }
        Err(JsonRejection::JsonSyntaxError(err)) => {
            Err((
                StatusCode::BAD_REQUEST,
                format!("JSON syntax error: {}", err),
            ))
        }
        Err(_) => {
            Err((
                StatusCode::INTERNAL_SERVER_ERROR,
                "Unknown error".to_string(),
            ))
        }
    }
}
```

### State Extractor

Access shared application state:

```rust
use axum::extract::State;
use std::sync::Arc;

#[derive(Clone)]
struct AppState {
    db_pool: Arc<DatabasePool>,
    api_key: String,
}

async fn handler(State(state): State<AppState>) -> String {
    format!("API Key: {}", state.api_key)
}

let state = AppState {
    db_pool: Arc::new(DatabasePool::new()),
    api_key: "secret".to_string(),
};

let app = Router::new()
    .route("/", get(handler))
    .with_state(state);
```

### Extension Extractor

Access request extensions (useful for middleware):

```rust
use axum::extract::Extension;

#[derive(Clone)]
struct CurrentUser {
    id: u32,
    username: String,
}

async fn handler(Extension(user): Extension<CurrentUser>) -> String {
    format!("Hello, {}", user.username)
}

// Set by middleware:
async fn auth_middleware(
    mut req: Request,
    next: Next,
) -> Result<Response, StatusCode> {
    let user = CurrentUser {
        id: 1,
        username: "alice".to_string(),
    };
    req.extensions_mut().insert(user);
    Ok(next.run(req).await)
}
```

### Form Extractor

Parse form-encoded request bodies:

```rust
use axum::extract::Form;
use serde::Deserialize;

#[derive(Deserialize)]
struct LoginForm {
    username: String,
    password: String,
}

async fn login(Form(form): Form<LoginForm>) -> String {
    format!("Logging in user: {}", form.username)
}
```

### Headers Extractor

Access request headers:

```rust
use axum::http::HeaderMap;

async fn handler(headers: HeaderMap) -> String {
    let user_agent = headers
        .get("user-agent")
        .and_then(|v| v.to_str().ok())
        .unwrap_or("unknown");
    format!("User-Agent: {}", user_agent)
}
```

### Custom Extractors

Create custom extractors by implementing `FromRequest` or `FromRequestParts`:

```rust
use axum::{
    extract::{FromRequest, Request},
    response::{IntoResponse, Response},
    http::StatusCode,
    async_trait,
};

struct AuthenticatedUser {
    id: u32,
    username: String,
}

#[async_trait]
impl<S> FromRequestParts<S> for AuthenticatedUser
where
    S: Send + Sync,
{
    type Rejection = Response;

    async fn from_request_parts(
        parts: &mut Parts,
        state: &S,
    ) -> Result<Self, Self::Rejection> {
        // Extract and validate auth token
        let auth_header = parts
            .headers
            .get("authorization")
            .and_then(|v| v.to_str().ok())
            .ok_or_else(|| {
                (StatusCode::UNAUTHORIZED, "Missing authorization header")
                    .into_response()
            })?;

        // Validate token and return user
        Ok(AuthenticatedUser {
            id: 1,
            username: "alice".to_string(),
        })
    }
}

async fn protected_route(user: AuthenticatedUser) -> String {
    format!("Hello, {}", user.username)
}
```

## Middleware

### Applying Middleware

**Three Ways to Apply Middleware:**

1. **Router-level** - Affects all routes
2. **Route-level** - Affects specific routes
3. **Method-level** - Affects specific methods on a route

```rust
use axum::{Router, routing::get, middleware};
use tower_http::trace::TraceLayer;

// 1. Router-level
let app = Router::new()
    .route("/", get(handler))
    .layer(TraceLayer::new_for_http());

// 2. Route-level
let app = Router::new()
    .route("/protected", get(handler))
    .route_layer(middleware::from_fn(auth_middleware));

// 3. Method-level
let app = Router::new()
    .route("/resource",
        get(handler)
            .route_layer(middleware::from_fn(read_only_auth))
            .post(create_handler)
            .route_layer(middleware::from_fn(write_auth))
    );
```

### Middleware Execution Order

**With sequential `.layer()` calls (bottom-to-top):**
```rust
let app = Router::new()
    .route("/", get(handler))
    .layer(layer_three)  // Executes third
    .layer(layer_two)    // Executes second
    .layer(layer_one);   // Executes first
```

**With `ServiceBuilder` (top-to-bottom):**
```rust
use tower::ServiceBuilder;

let app = Router::new()
    .route("/", get(handler))
    .layer(
        ServiceBuilder::new()
            .layer(layer_one)    // Executes first
            .layer(layer_two)    // Executes second
            .layer(layer_three)  // Executes third
    );
```

### Common Tower Middleware

**TraceLayer** - HTTP request tracing:
```rust
use tower_http::trace::TraceLayer;

let app = Router::new()
    .route("/", get(handler))
    .layer(TraceLayer::new_for_http());
```

**CompressionLayer** - Response compression:
```rust
use tower_http::compression::CompressionLayer;

let app = Router::new()
    .route("/", get(handler))
    .layer(CompressionLayer::new());
```

**CorsLayer** - CORS handling:
```rust
use tower_http::cors::{CorsLayer, Any};

let cors = CorsLayer::new()
    .allow_origin(Any)
    .allow_methods(Any)
    .allow_headers(Any);

let app = Router::new()
    .route("/api/data", get(handler))
    .layer(cors);
```

**TimeoutLayer** - Request timeouts:
```rust
use tower::timeout::TimeoutLayer;
use std::time::Duration;

let app = Router::new()
    .route("/", get(handler))
    .layer(TimeoutLayer::new(Duration::from_secs(30)));
```

### HandleErrorLayer

Convert middleware errors to HTTP responses:

```rust
use axum::{
    error_handling::HandleErrorLayer,
    http::{StatusCode, Method, Uri},
    BoxError,
};
use tower::ServiceBuilder;
use std::time::Duration;

async fn handle_timeout_error(
    method: Method,
    uri: Uri,
    err: BoxError,
) -> (StatusCode, String) {
    if err.is::<tower::timeout::error::Elapsed>() {
        (
            StatusCode::REQUEST_TIMEOUT,
            format!("`{} {}` request timed out", method, uri),
        )
    } else {
        (
            StatusCode::INTERNAL_SERVER_ERROR,
            format!("`{} {}` failed with {}", method, uri, err),
        )
    }
}

let app = Router::new()
    .route("/", get(handler))
    .layer(
        ServiceBuilder::new()
            .layer(HandleErrorLayer::new(handle_timeout_error))
            .layer(TimeoutLayer::new(Duration::from_secs(30)))
    );
```

### Custom Middleware with from_fn

Create custom middleware using async functions:

```rust
use axum::{
    middleware::{self, Next},
    extract::Request,
    response::Response,
    http::StatusCode,
};

async fn auth_middleware(
    req: Request,
    next: Next,
) -> Result<Response, StatusCode> {
    let auth_header = req.headers()
        .get("authorization")
        .and_then(|h| h.to_str().ok());

    if let Some(auth_header) = auth_header {
        if validate_token(auth_header).await {
            Ok(next.run(req).await)
        } else {
            Err(StatusCode::UNAUTHORIZED)
        }
    } else {
        Err(StatusCode::UNAUTHORIZED)
    }
}

let app = Router::new()
    .route("/protected", get(handler))
    .layer(middleware::from_fn(auth_middleware));
```

**Passing data from middleware to handler:**
```rust
use axum::extract::Extension;

#[derive(Clone)]
struct CurrentUser {
    id: u32,
    username: String,
}

async fn auth_middleware(
    mut req: Request,
    next: Next,
) -> Result<Response, StatusCode> {
    let auth_header = req.headers()
        .get("authorization")
        .and_then(|h| h.to_str().ok())
        .ok_or(StatusCode::UNAUTHORIZED)?;

    if let Some(user) = authorize_user(auth_header).await {
        req.extensions_mut().insert(user);
        Ok(next.run(req).await)
    } else {
        Err(StatusCode::UNAUTHORIZED)
    }
}

async fn handler(Extension(user): Extension<CurrentUser>) -> String {
    format!("Hello, {}", user.username)
}

let app = Router::new()
    .route("/", get(handler))
    .layer(middleware::from_fn(auth_middleware));
```

### Custom Tower Middleware

Implement Tower's `Service` and `Layer` traits for full control:

```rust
use tower::{Service, Layer};
use axum::{response::Response, extract::Request};
use std::task::{Context, Poll};
use futures_core::future::BoxFuture;

#[derive(Clone)]
struct MyLayer;

impl<S> Layer<S> for MyLayer {
    type Service = MyMiddleware<S>;

    fn layer(&self, inner: S) -> Self::Service {
        MyMiddleware { inner }
    }
}

#[derive(Clone)]
struct MyMiddleware<S> {
    inner: S,
}

impl<S> Service<Request> for MyMiddleware<S>
where
    S: Service<Request, Response = Response> + Send + 'static,
    S::Future: Send + 'static,
{
    type Response = S::Response;
    type Error = S::Error;
    type Future = BoxFuture<'static, Result<Self::Response, Self::Error>>;

    fn poll_ready(&mut self, cx: &mut Context<'_>) -> Poll<Result<(), Self::Error>> {
        self.inner.poll_ready(cx)
    }

    fn call(&mut self, request: Request) -> Self::Future {
        // Process request
        let future = self.inner.call(request);
        Box::pin(async move {
            let response: Response = future.await?;
            // Process response
            Ok(response)
        })
    }
}

let app = Router::new()
    .route("/", get(handler))
    .layer(MyLayer);
```

### Middleware with State Access

Create middleware that accesses application state:

```rust
use axum::extract::State;
use std::sync::Arc;

#[derive(Clone)]
struct AppState {
    db: Arc<Database>,
}

#[derive(Clone)]
struct MyLayer {
    state: AppState,
}

impl<S> Layer<S> for MyLayer {
    type Service = MyService<S>;

    fn layer(&self, inner: S) -> Self::Service {
        MyService {
            inner,
            state: self.state.clone(),
        }
    }
}

#[derive(Clone)]
struct MyService<S> {
    inner: S,
    state: AppState,
}

impl<S> Service<Request> for MyService<S>
where
    S: Service<Request>,
{
    type Response = S::Response;
    type Error = S::Error;
    type Future = S::Future;

    fn poll_ready(&mut self, cx: &mut Context<'_>) -> Poll<Result<(), Self::Error>> {
        self.inner.poll_ready(cx)
    }

    fn call(&mut self, req: Request) -> Self::Future {
        // Use self.state here
        self.inner.call(req)
    }
}

let state = AppState {
    db: Arc::new(Database::new()),
};

let app = Router::new()
    .route("/", get(handler))
    .layer(MyLayer { state: state.clone() })
    .with_state(state);
```

### Middleware Before Routing

Apply middleware before routing (e.g., for URI rewriting):

```rust
use tower::Layer;
use axum::ServiceExt;

fn rewrite_request_uri(req: Request) -> Request {
    // Modify request URI
    req
}

let middleware = tower::util::MapRequestLayer::new(rewrite_request_uri);

let app = Router::new()
    .route("/", get(handler));

// Apply layer around entire router
let app_with_middleware = middleware.layer(app);

let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await?;
axum::serve(listener, app_with_middleware.into_make_service()).await?;
```

## State Management

### Basic State

Simple state with cloneable types:

```rust
use axum::extract::State;

#[derive(Clone)]
struct AppState {
    config: Config,
    api_key: String,
}

async fn handler(State(state): State<AppState>) -> String {
    format!("Config: {:?}, Key: {}", state.config, state.api_key)
}

let state = AppState {
    config: Config::default(),
    api_key: "secret".to_string(),
};

let app = Router::new()
    .route("/", get(handler))
    .with_state(state);
```

### Shared State with Arc

Use `Arc` for shared ownership of expensive-to-clone types:

```rust
use std::sync::Arc;
use tokio::sync::RwLock;

#[derive(Clone)]
struct AppState {
    db_pool: Arc<DatabasePool>,
    cache: Arc<RwLock<HashMap<String, String>>>,
    config: Config, // Cheap to clone
}

async fn handler(State(state): State<AppState>) -> Result<String, StatusCode> {
    // Access database pool
    let conn = state.db_pool.get().await.map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;

    // Access cache (read)
    let cache = state.cache.read().await;
    let value = cache.get("key");

    // Access cache (write)
    drop(cache); // Release read lock
    let mut cache = state.cache.write().await;
    cache.insert("new_key".to_string(), "value".to_string());

    Ok("Success".to_string())
}
```

### Multiple State Types

Use different state types for different router sections:

```rust
#[derive(Clone)]
struct ApiState {
    api_key: String,
}

#[derive(Clone)]
struct AppState {
    db: Arc<Database>,
}

fn api_routes() -> Router<ApiState> {
    Router::new()
        .route("/data", get(|State(state): State<ApiState>| async move {
            format!("API Key: {}", state.api_key)
        }))
}

fn app_routes() -> Router<AppState> {
    Router::new()
        .route("/users", get(|State(state): State<AppState>| async move {
            "Users".to_string()
        }))
}

let api_state = ApiState { api_key: "secret".to_string() };
let app_state = AppState { db: Arc::new(Database::new()) };

let app = Router::new()
    .nest("/api", api_routes().with_state(api_state))
    .nest("/app", app_routes().with_state(app_state));
```

### Generic State in Functions

Return routers with generic state for flexibility:

```rust
fn routes<S>() -> Router<S>
where
    S: Clone + Send + Sync + 'static,
{
    Router::new()
        .route("/health", get(|| async { "OK" }))
        .route("/version", get(|| async { "1.0.0" }))
}

// Can be combined with any state type
let app = Router::new()
    .merge(routes())
    .route("/", get(handler))
    .with_state(AppState { /* ... */ });
```

### State Transitions

Chain routers with different state requirements:

```rust
#[derive(Clone)]
struct StateA {
    data_a: String,
}

#[derive(Clone)]
struct StateB {
    data_b: String,
}

let router_a: Router<StateA> = Router::new()
    .route("/a", get(|State(s): State<StateA>| async move { s.data_a }));

// Provide StateA, next missing state is StateB
let router_b: Router<StateB> = router_a.with_state(StateA {
    data_a: "A".to_string(),
});

// Add routes needing StateB
let router_b = router_b
    .route("/b", get(|State(s): State<StateB>| async move { s.data_b }));

// Provide StateB, now we have Router<()>
let app: Router<()> = router_b.with_state(StateB {
    data_b: "B".to_string(),
});
```

## Error Handling

### Basic Error Handling with Result

Use `Result` to handle errors in handlers:

```rust
use axum::http::StatusCode;

async fn handler() -> Result<String, StatusCode> {
    let result = some_operation().await;
    match result {
        Ok(data) => Ok(format!("Success: {}", data)),
        Err(_) => Err(StatusCode::INTERNAL_SERVER_ERROR),
    }
}
```

### Custom Error Types

Implement `IntoResponse` for custom errors:

```rust
use axum::{
    response::{IntoResponse, Response},
    http::StatusCode,
    Json,
};
use serde::Serialize;

#[derive(Debug)]
enum AppError {
    Database(sqlx::Error),
    NotFound,
    Unauthorized,
    ValidationError(String),
}

#[derive(Serialize)]
struct ErrorResponse {
    error: String,
    message: String,
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, error_message) = match self {
            AppError::Database(e) => {
                tracing::error!("Database error: {}", e);
                (StatusCode::INTERNAL_SERVER_ERROR, "Database error")
            }
            AppError::NotFound => (StatusCode::NOT_FOUND, "Resource not found"),
            AppError::Unauthorized => (StatusCode::UNAUTHORIZED, "Unauthorized"),
            AppError::ValidationError(msg) => (StatusCode::BAD_REQUEST, &msg),
        };

        let body = Json(ErrorResponse {
            error: status.to_string(),
            message: error_message.to_string(),
        });

        (status, body).into_response()
    }
}

// Use in handler
async fn get_user(Path(id): Path<u32>) -> Result<Json<User>, AppError> {
    let user = db.get_user(id).await.map_err(AppError::Database)?;
    user.ok_or(AppError::NotFound).map(Json)
}
```

### Extractor Rejection Handling

Handle extractor rejections for better error messages:

```rust
use axum::extract::rejection::JsonRejection;

async fn create_user(
    payload: Result<Json<CreateUser>, JsonRejection>,
) -> Result<Json<User>, AppError> {
    let Json(create_user) = payload.map_err(|err| match err {
        JsonRejection::MissingJsonContentType(_) => {
            AppError::ValidationError("Content-Type must be application/json".to_string())
        }
        JsonRejection::JsonDataError(e) => {
            AppError::ValidationError(format!("Invalid JSON: {}", e))
        }
        JsonRejection::JsonSyntaxError(e) => {
            AppError::ValidationError(format!("JSON syntax error: {}", e))
        }
        _ => AppError::ValidationError("Invalid request body".to_string()),
    })?;

    // Process create_user
    Ok(Json(user))
}
```

### Custom Extractors with Error Handling

Create extractors with custom rejection types:

```rust
use axum::{
    extract::{FromRequest, Request},
    response::{IntoResponse, Response},
    async_trait,
};

struct ValidatedJson<T>(T);

#[async_trait]
impl<S, T> FromRequest<S> for ValidatedJson<T>
where
    T: serde::de::DeserializeOwned + Validate,
    S: Send + Sync,
{
    type Rejection = Response;

    async fn from_request(req: Request, state: &S) -> Result<Self, Self::Rejection> {
        let Json(data) = Json::<T>::from_request(req, state)
            .await
            .map_err(|err| {
                (
                    StatusCode::BAD_REQUEST,
                    format!("Invalid JSON: {}", err),
                ).into_response()
            })?;

        data.validate().map_err(|err| {
            (
                StatusCode::BAD_REQUEST,
                format!("Validation error: {}", err),
            ).into_response()
        })?;

        Ok(ValidatedJson(data))
    }
}

async fn handler(ValidatedJson(data): ValidatedJson<MyData>) -> String {
    // data is validated
    format!("Received: {:?}", data)
}
```

### Middleware Error Handling

Handle errors from fallible middleware:

```rust
use axum::error_handling::HandleErrorLayer;
use tower::ServiceBuilder;

async fn handle_timeout_error(err: BoxError) -> (StatusCode, String) {
    if err.is::<tower::timeout::error::Elapsed>() {
        (
            StatusCode::REQUEST_TIMEOUT,
            "Request took too long".to_string(),
        )
    } else {
        (
            StatusCode::INTERNAL_SERVER_ERROR,
            format!("Unhandled error: {}", err),
        )
    }
}

let app = Router::new()
    .route("/", get(handler))
    .layer(
        ServiceBuilder::new()
            .layer(HandleErrorLayer::new(handle_timeout_error))
            .layer(TimeoutLayer::new(Duration::from_secs(30)))
    );
```

### Fallible Services

Route to services that can fail:

```rust
use axum::error_handling::HandleError;

async fn fallible_operation() -> Result<(), anyhow::Error> {
    // Operation that might fail
    Ok(())
}

let fallible_service = tower::service_fn(|_req| async {
    fallible_operation().await?;
    Ok::<_, anyhow::Error>(Response::new(Body::empty()))
});

async fn handle_error(err: anyhow::Error) -> (StatusCode, String) {
    (
        StatusCode::INTERNAL_SERVER_ERROR,
        format!("Something went wrong: {}", err),
    )
}

let app = Router::new().route_service(
    "/",
    HandleError::new(fallible_service, handle_error),
);
```

## Response Building

### JSON Responses

Return JSON with type safety:

```rust
use axum::Json;
use serde::Serialize;

#[derive(Serialize)]
struct ApiResponse {
    success: bool,
    data: String,
}

async fn handler() -> Json<ApiResponse> {
    Json(ApiResponse {
        success: true,
        data: "Hello".to_string(),
    })
}
```

### HTML Responses

Serve HTML content:

```rust
use axum::response::Html;

async fn handler() -> Html<&'static str> {
    Html("<h1>Hello, World!</h1>")
}

async fn dynamic_html(Path(name): Path<String>) -> Html<String> {
    Html(format!("<h1>Hello, {}</h1>", name))
}
```

### Status Code Responses

Return different status codes:

```rust
use axum::http::StatusCode;

async fn handler() -> StatusCode {
    StatusCode::NO_CONTENT
}

async fn with_body() -> (StatusCode, String) {
    (StatusCode::CREATED, "Resource created".to_string())
}

async fn json_with_status() -> (StatusCode, Json<ApiResponse>) {
    (StatusCode::CREATED, Json(ApiResponse { /* ... */ }))
}
```

### Custom Headers

Add custom headers to responses:

```rust
use axum::http::{HeaderMap, header};

async fn handler() -> (HeaderMap, String) {
    let mut headers = HeaderMap::new();
    headers.insert(header::CACHE_CONTROL, "max-age=3600".parse().unwrap());
    headers.insert("X-Custom-Header", "value".parse().unwrap());
    (headers, "Response body".to_string())
}
```

### Full Response Control

Build complete responses:

```rust
use axum::{
    response::Response,
    http::{StatusCode, header},
    body::Body,
};

async fn handler() -> Response {
    Response::builder()
        .status(StatusCode::OK)
        .header(header::CONTENT_TYPE, "application/json")
        .header("X-Custom", "value")
        .body(Body::from(r#"{"status":"ok"}"#))
        .unwrap()
}
```

### Streaming Responses

Stream data to clients:

```rust
use axum::response::sse::{Event, Sse};
use futures::stream::{self, Stream};
use std::convert::Infallible;

async fn sse_handler() -> Sse<impl Stream<Item = Result<Event, Infallible>>> {
    let stream = stream::iter(0..10).map(|i| {
        Ok(Event::default().data(format!("Event {}", i)))
    });
    Sse::new(stream)
}
```

### File Downloads

Serve files for download:

```rust
use axum::{
    response::{Response, IntoResponse},
    http::{header, StatusCode},
    body::Body,
};
use tokio::fs::File;

async fn download_file() -> Result<Response, StatusCode> {
    let file = File::open("path/to/file.pdf")
        .await
        .map_err(|_| StatusCode::NOT_FOUND)?;

    let body = Body::from_stream(tokio_util::io::ReaderStream::new(file));

    Ok(Response::builder()
        .status(StatusCode::OK)
        .header(header::CONTENT_TYPE, "application/pdf")
        .header(
            header::CONTENT_DISPOSITION,
            "attachment; filename=\"file.pdf\"",
        )
        .body(body)
        .unwrap())
}
```

## Production Patterns

### Database Integration

Integrate with database pools:

```rust
use sqlx::{PgPool, postgres::PgPoolOptions};
use std::sync::Arc;

#[derive(Clone)]
struct AppState {
    db: PgPool,
}

async fn get_user(
    State(state): State<AppState>,
    Path(id): Path<i64>,
) -> Result<Json<User>, AppError> {
    let user = sqlx::query_as!(User, "SELECT * FROM users WHERE id = $1", id)
        .fetch_optional(&state.db)
        .await
        .map_err(AppError::Database)?
        .ok_or(AppError::NotFound)?;

    Ok(Json(user))
}

#[tokio::main]
async fn main() {
    let db = PgPoolOptions::new()
        .max_connections(5)
        .connect(&env::var("DATABASE_URL").unwrap())
        .await
        .unwrap();

    let state = AppState { db };

    let app = Router::new()
        .route("/users/{id}", get(get_user))
        .with_state(state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

### Configuration Management

Use environment variables and configuration:

```rust
use serde::Deserialize;
use config::{Config, ConfigError, Environment};

#[derive(Debug, Deserialize, Clone)]
struct Settings {
    database_url: String,
    redis_url: String,
    jwt_secret: String,
    port: u16,
}

impl Settings {
    fn new() -> Result<Self, ConfigError> {
        Config::builder()
            .add_source(Environment::default())
            .build()?
            .try_deserialize()
    }
}

#[derive(Clone)]
struct AppState {
    settings: Settings,
    db: PgPool,
}

#[tokio::main]
async fn main() {
    let settings = Settings::new().expect("Failed to load configuration");

    let db = PgPoolOptions::new()
        .connect(&settings.database_url)
        .await
        .expect("Failed to connect to database");

    let state = AppState {
        settings: settings.clone(),
        db,
    };

    let app = Router::new()
        .route("/", get(handler))
        .with_state(state);

    let addr = format!("0.0.0.0:{}", settings.port);
    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

### Structured Logging

Implement comprehensive logging:

```rust
use tracing::{info, error, debug, instrument};
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

#[tokio::main]
async fn main() {
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "info".into()),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();

    info!("Starting server");

    let app = Router::new()
        .route("/", get(handler))
        .layer(TraceLayer::new_for_http());

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    info!("Listening on {}", listener.local_addr().unwrap());
    axum::serve(listener, app).await.unwrap();
}

#[instrument]
async fn handler(Path(id): Path<u32>) -> Result<String, AppError> {
    debug!("Handling request for user {}", id);

    match get_user_from_db(id).await {
        Ok(user) => {
            info!("Successfully retrieved user {}", id);
            Ok(format!("User: {}", user))
        }
        Err(e) => {
            error!("Failed to get user {}: {}", id, e);
            Err(AppError::Database(e))
        }
    }
}
```

### Graceful Shutdown

Implement graceful shutdown handling:

```rust
use tokio::signal;

async fn shutdown_signal() {
    let ctrl_c = async {
        signal::ctrl_c()
            .await
            .expect("failed to install Ctrl+C handler");
    };

    #[cfg(unix)]
    let terminate = async {
        signal::unix::signal(signal::unix::SignalKind::terminate())
            .expect("failed to install signal handler")
            .recv()
            .await;
    };

    #[cfg(not(unix))]
    let terminate = std::future::pending::<()>();

    tokio::select! {
        _ = ctrl_c => {},
        _ = terminate => {},
    }

    println!("Signal received, starting graceful shutdown");
}

#[tokio::main]
async fn main() {
    let app = Router::new().route("/", get(handler));

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, app)
        .with_graceful_shutdown(shutdown_signal())
        .await
        .unwrap();
}
```

### Health Checks

Implement health check endpoints:

```rust
use serde::Serialize;

#[derive(Serialize)]
struct HealthResponse {
    status: String,
    database: String,
    cache: String,
}

async fn health_check(State(state): State<AppState>) -> Json<HealthResponse> {
    let db_status = match sqlx::query("SELECT 1").fetch_one(&state.db).await {
        Ok(_) => "healthy",
        Err(_) => "unhealthy",
    };

    let cache_status = match state.redis.ping().await {
        Ok(_) => "healthy",
        Err(_) => "unhealthy",
    };

    Json(HealthResponse {
        status: if db_status == "healthy" && cache_status == "healthy" {
            "healthy".to_string()
        } else {
            "degraded".to_string()
        },
        database: db_status.to_string(),
        cache: cache_status.to_string(),
    })
}

let app = Router::new()
    .route("/health", get(health_check))
    .route("/ready", get(readiness_check))
    .with_state(state);
```

### Rate Limiting

Implement rate limiting:

```rust
use tower::limit::RateLimitLayer;
use std::time::Duration;

let app = Router::new()
    .route("/api/data", get(handler))
    .layer(RateLimitLayer::new(
        100, // max requests
        Duration::from_secs(60), // per minute
    ));
```

### Request Validation

Validate requests with custom extractors:

```rust
use validator::{Validate, ValidationError};

#[derive(Debug, Deserialize, Validate)]
struct CreateUserRequest {
    #[validate(length(min = 3, max = 50))]
    username: String,
    #[validate(email)]
    email: String,
    #[validate(length(min = 8))]
    password: String,
}

struct ValidatedJson<T>(T);

#[async_trait]
impl<S, T> FromRequest<S> for ValidatedJson<T>
where
    T: DeserializeOwned + Validate,
    S: Send + Sync,
{
    type Rejection = (StatusCode, String);

    async fn from_request(req: Request, state: &S) -> Result<Self, Self::Rejection> {
        let Json(data) = Json::<T>::from_request(req, state)
            .await
            .map_err(|e| (StatusCode::BAD_REQUEST, e.to_string()))?;

        data.validate()
            .map_err(|e| (StatusCode::BAD_REQUEST, e.to_string()))?;

        Ok(ValidatedJson(data))
    }
}

async fn create_user(
    ValidatedJson(user): ValidatedJson<CreateUserRequest>,
) -> Result<Json<User>, AppError> {
    // user is validated
    Ok(Json(User { /* ... */ }))
}
```

## Testing

### Unit Testing Handlers

Test handlers in isolation:

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use axum::body::Body;
    use axum::http::{Request, StatusCode};
    use tower::ServiceExt;

    #[tokio::test]
    async fn test_handler() {
        let app = Router::new().route("/", get(handler));

        let response = app
            .oneshot(Request::builder().uri("/").body(Body::empty()).unwrap())
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);
    }
}
```

### Integration Testing

Test full application:

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use axum::body::Body;
    use axum::http::{Request, StatusCode, Method};
    use tower::ServiceExt;
    use serde_json::json;

    #[tokio::test]
    async fn test_create_user() {
        let state = AppState::test();
        let app = create_app(state);

        let request_body = json!({
            "username": "testuser",
            "email": "test@example.com"
        });

        let response = app
            .oneshot(
                Request::builder()
                    .method(Method::POST)
                    .uri("/users")
                    .header("content-type", "application/json")
                    .body(Body::from(request_body.to_string()))
                    .unwrap()
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::CREATED);
    }
}
```

## Best Practices

### Handler Organization

1. **Keep handlers thin** - Move business logic to service layer
2. **Use extractors** - Let type system handle extraction
3. **Return Result types** - Use custom error types
4. **Instrument handlers** - Add tracing for observability

### State Management

1. **Use Arc for expensive types** - Database pools, caches
2. **Keep state minimal** - Only what's truly shared
3. **Implement Clone** - Required for State extractor
4. **Avoid mutation** - Use interior mutability (RwLock, Mutex) when needed

### Error Handling

1. **Create custom error types** - Implement IntoResponse
2. **Provide context** - Include helpful error messages
3. **Log errors appropriately** - Use tracing
4. **Return proper status codes** - Match HTTP semantics

### Middleware

1. **Use ServiceBuilder** - More intuitive ordering
2. **Apply at right level** - Router vs route vs method
3. **Handle errors** - Use HandleErrorLayer for fallible middleware
4. **Keep middleware focused** - Single responsibility

### Performance

1. **Use connection pooling** - For databases and external services
2. **Enable compression** - CompressionLayer for responses
3. **Implement caching** - Reduce redundant operations
4. **Use backpressure** - LoadShedLayer, RateLimitLayer
5. **Optimize serialization** - Use efficient JSON libraries

### Security

1. **Validate inputs** - Use custom extractors with validation
2. **Implement authentication** - Use middleware for auth
3. **Use HTTPS** - In production environments
4. **Set security headers** - CORS, CSP, etc.
5. **Rate limit** - Prevent abuse

## Common Patterns

### Repository Pattern

```rust
trait UserRepository {
    async fn get(&self, id: u32) -> Result<User, AppError>;
    async fn create(&self, user: CreateUser) -> Result<User, AppError>;
    async fn update(&self, id: u32, user: UpdateUser) -> Result<User, AppError>;
    async fn delete(&self, id: u32) -> Result<(), AppError>;
}

struct PostgresUserRepository {
    pool: PgPool,
}

impl UserRepository for PostgresUserRepository {
    async fn get(&self, id: u32) -> Result<User, AppError> {
        // Implementation
    }
}

#[derive(Clone)]
struct AppState {
    user_repo: Arc<dyn UserRepository + Send + Sync>,
}

async fn get_user(
    State(state): State<AppState>,
    Path(id): Path<u32>,
) -> Result<Json<User>, AppError> {
    let user = state.user_repo.get(id).await?;
    Ok(Json(user))
}
```

### Service Layer Pattern

```rust
struct UserService {
    repo: Arc<dyn UserRepository + Send + Sync>,
    email_service: Arc<EmailService>,
}

impl UserService {
    async fn create_user(&self, data: CreateUser) -> Result<User, AppError> {
        let user = self.repo.create(data).await?;
        self.email_service.send_welcome_email(&user).await?;
        Ok(user)
    }
}

#[derive(Clone)]
struct AppState {
    user_service: Arc<UserService>,
}
```

### Versioned APIs

```rust
fn v1_routes() -> Router<AppState> {
    Router::new()
        .route("/users", get(v1::list_users))
        .route("/users/{id}", get(v1::get_user))
}

fn v2_routes() -> Router<AppState> {
    Router::new()
        .route("/users", get(v2::list_users))
        .route("/users/{id}", get(v2::get_user))
}

let app = Router::new()
    .nest("/api/v1", v1_routes())
    .nest("/api/v2", v2_routes())
    .with_state(state);
```

---

**Skill Version**: 1.0.0
**Last Updated**: January 2026
**Skill Category**: Web Development, REST APIs, Rust, Async Programming
**Compatible With**: Axum 0.8+, Tokio 1.0+, Tower 0.4+
