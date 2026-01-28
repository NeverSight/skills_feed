---
name: utoipa-axum
description: |
  OpenAPI documentation skill for Rust APIs using utoipa with Axum framework.
  Use when building REST APIs with automatic OpenAPI spec generation and Scalar UI.
  Covers: (1) ToSchema derive for request/response types, (2) #[utoipa::path] for endpoint documentation,
  (3) OpenApi derive for combining specs, (4) Security schemes (JWT, API keys), (5) IntoParams for query/path params,
  (6) Scalar UI integration, (7) Response and error handling patterns.
  Triggers: utoipa, openapi, scalar, axum api, ToSchema, IntoParams, rust api docs.
---

# OpenAPI with utoipa + Axum

utoipa provides compile-time OpenAPI documentation for Rust REST APIs. Code-first approach: annotate handlers and types, get OpenAPI 3.1 spec automatically.

## Core Concepts

1. **ToSchema** — Derive for request/response body types
2. **#[utoipa::path]** — Annotate handlers with path, method, params, responses
3. **OpenApi** — Combine all paths and schemas into spec
4. **Scalar** — Serve interactive API documentation

## Cargo.toml Setup

```toml
[dependencies]
axum = "0.8"
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
uuid = { version = "1", features = ["serde", "v4"] }
chrono = { version = "0.4", features = ["serde"] }

# utoipa with axum integration
utoipa = { version = "5", features = ["axum_extras", "uuid", "chrono"] }
utoipa-scalar = { version = "0.3", features = ["axum"] }
```

## ToSchema — Request/Response Types

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;
use uuid::Uuid;

#[derive(Debug, Deserialize, ToSchema)]
pub struct CreateUserRequest {
    /// User's email address
    pub email: String,
    /// Password (min 8 characters)
    #[schema(min_length = 8)]
    pub password: String,
}

#[derive(Debug, Serialize, ToSchema)]
pub struct UserResponse {
    pub id: Uuid,
    pub email: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub name: Option<String>,
}

#[derive(Debug, Serialize, ToSchema)]
pub struct ErrorResponse {
    pub error: String,
}
```

## #[utoipa::path] — Documenting Handlers

```rust
use axum::{extract::{Path, State}, http::StatusCode, Json};

#[utoipa::path(
    get,
    path = "/api/users/{id}",
    tag = "users",
    params(("id" = Uuid, Path, description = "User ID")),
    responses(
        (status = 200, description = "User found", body = UserResponse),
        (status = 404, description = "Not found", body = ErrorResponse)
    ),
    security(("bearer" = []))
)]
pub async fn get_user(
    State(state): State<AppState>,
    Path(id): Path<Uuid>,
) -> Result<Json<UserResponse>, (StatusCode, Json<ErrorResponse>)> {
    // handler logic
}

#[utoipa::path(
    post,
    path = "/api/users",
    tag = "users",
    request_body = CreateUserRequest,
    responses(
        (status = 201, description = "Created", body = UserResponse),
        (status = 400, description = "Bad request", body = ErrorResponse)
    )
)]
pub async fn create_user(
    State(state): State<AppState>,
    Json(req): Json<CreateUserRequest>,
) -> Result<(StatusCode, Json<UserResponse>), (StatusCode, Json<ErrorResponse>)> {
    // handler logic
}
```

## OpenApi — Combining Everything

```rust
use utoipa::openapi::security::{Http, HttpAuthScheme, SecurityScheme};
use utoipa::{Modify, OpenApi};

#[derive(OpenApi)]
#[openapi(
    info(
        title = "My API",
        version = "1.0.0",
        description = "API description"
    ),
    tags(
        (name = "users", description = "User management"),
        (name = "health", description = "Health checks")
    ),
    paths(
        get_user,
        create_user,
        health_check
    ),
    components(
        schemas(
            CreateUserRequest,
            UserResponse,
            ErrorResponse
        )
    ),
    modifiers(&SecurityAddon)
)]
pub struct ApiDoc;

struct SecurityAddon;

impl Modify for SecurityAddon {
    fn modify(&self, openapi: &mut utoipa::openapi::OpenApi) {
        if let Some(components) = openapi.components.as_mut() {
            components.add_security_scheme(
                "bearer",
                SecurityScheme::Http(Http::new(HttpAuthScheme::Bearer)),
            );
        }
    }
}
```

## Serving Scalar UI

```rust
use axum::{routing::get, Router};
use utoipa::OpenApi;
use utoipa_scalar::{Scalar, Servable};

pub fn create_router(state: AppState) -> Router {
    Router::new()
        .route("/health", get(health_check))
        .route("/api/users", get(list_users).post(create_user))
        .route("/api/users/{id}", get(get_user).put(update_user).delete(delete_user))
        // Scalar UI at /api/docs
        .merge(Scalar::with_url("/api/docs", ApiDoc::openapi()))
        .with_state(state)
}
```

## IntoParams — Query Parameters

```rust
use utoipa::IntoParams;

#[derive(Debug, Deserialize, IntoParams)]
pub struct PaginationParams {
    /// Page number (1-indexed)
    #[param(minimum = 1, default = 1)]
    pub page: Option<u32>,
    /// Items per page
    #[param(minimum = 1, maximum = 100, default = 20)]
    pub per_page: Option<u32>,
}

#[derive(Debug, Deserialize, IntoParams)]
pub struct UserFilters {
    /// Filter by email contains
    pub email: Option<String>,
    /// Filter by status
    pub status: Option<UserStatus>,
}

#[utoipa::path(
    get,
    path = "/api/users",
    tag = "users",
    params(PaginationParams, UserFilters),
    responses((status = 200, body = Vec<UserResponse>))
)]
pub async fn list_users(
    Query(pagination): Query<PaginationParams>,
    Query(filters): Query<UserFilters>,
) -> Json<Vec<UserResponse>> {
    // handler logic
}
```

## Enums in Schema

```rust
#[derive(Debug, Serialize, Deserialize, ToSchema)]
#[serde(rename_all = "snake_case")]
pub enum UserStatus {
    Active,
    Inactive,
    Pending,
}

#[derive(Debug, Serialize, Deserialize, ToSchema)]
#[serde(tag = "type", rename_all = "snake_case")]
pub enum Event {
    UserCreated { user_id: Uuid },
    UserDeleted { user_id: Uuid, reason: String },
}
```

## Common Patterns

See [references/patterns.md](references/patterns.md) for error handling, authentication middleware, and response types.

## API Reference

See [references/api_reference.md](references/api_reference.md) for complete ToSchema and path attribute options.
