---
name: depot-services-review
description: Reviews Rust microservices in the depot/ directory with focus on Axum web framework, SQLx database patterns, Docker deployment, and WebSocket communication. Use when reviewing depot service changes (discovery, dispatch, map-api, gps-status, mapper), adding new endpoints, modifying database schemas, implementing WebSocket protocols, or debugging service integration issues. Covers Tokio async patterns, REST/WebSocket API design, PostgreSQL migrations, error handling, health checks, and Docker multi-stage builds.
allowed-tools: Read, Grep, Glob, Bash(cargo:check), Bash(cargo:test), Bash(docker:build)
---

# Depot Services Review Skill

Reviews Rust microservices in the `depot/` directory that provide base station infrastructure for rover fleet operations.

## Overview

The depot consists of 5 Rust-based microservices that handle rover discovery, mission dispatch, mapping, and GPS infrastructure:

### Services Covered

| Service | Port | Purpose | Database | WebSocket |
|---------|------|---------|----------|-----------|
| **discovery** | 4860 | Rover registration, heartbeat tracking, session API | No | Yes (operator updates) |
| **dispatch** | 4890 | Mission planning, task assignment, zone management | PostgreSQL | Yes (rover + console) |
| **map-api** | 4870 | Serve processed maps and sessions | No | No |
| **gps-status** | 4880 | RTK base station monitoring | No | Yes (console updates) |
| **mapper** | - | Map processing orchestrator (batch job) | No | No |

### Shared Technology Stack

All services use a consistent technology stack:

**Runtime & Async**:
- Rust Edition 2021
- Tokio 1.41+ (async runtime with `rt-multi-thread`, `macros`, `net`)
- Futures 0.3 (async utilities)

**Web Framework**:
- Axum 0.7-0.8 (web server, routing, WebSocket)
- Tower-HTTP 0.6 (middleware: CORS, compression, tracing)
- Hyper (underlying HTTP implementation)

**Database** (dispatch only):
- SQLx 0.8 (async PostgreSQL client)
- PostgreSQL 16+ (database server in Docker)
- JSON/JSONB for flexible schema fields

**Serialization**:
- Serde 1.0 (derive macros)
- serde_json 1.0 (JSON encoding/decoding)

**Error Handling**:
- thiserror 2.0 (library error types)
- anyhow (application-level error handling)

**Logging**:
- tracing 0.1 (structured logging)
- tracing-subscriber 0.3 (log formatting, env filtering)

**Other**:
- UUID 1.0 (unique identifiers with v4 generation)
- chrono 0.4 (timestamps with serde support)

### Architecture Pattern

All services follow a consistent structure:

```
depot/<service>/
├── Cargo.toml           # Dependencies and metadata
├── Dockerfile           # Multi-stage build (alpine-based)
├── src/
│   └── main.rs          # Single-file service (300-1200 LOC)
└── migrations/          # SQL migrations (dispatch only)
    └── 001_initial.sql
```

**Code Structure** (main.rs):
```rust
//! Service documentation

// Imports
use axum::{...};
use tokio::...;

// Type definitions
struct AppState { ... }
type SharedState = Arc<AppState>;

// Main function
#[tokio::main]
async fn main() {
    // 1. Initialize logging
    // 2. Load configuration from env vars
    // 3. Initialize state (DB connection, channels, etc.)
    // 4. Create router with routes
    // 5. Bind to port and serve
}

// Handler functions
async fn endpoint_handler(...) -> impl IntoResponse { ... }

// Helper functions
fn utility_function(...) { ... }
```

## Shared Patterns Review Checklist

### 1. Axum Web Server Setup

- [ ] **Tokio runtime is configured correctly**
  - Uses `#[tokio::main]` macro for async main
  - Runtime features include at least: `rt-multi-thread`, `macros`, `net`
  - No blocking operations in async contexts

❌ BAD:
```rust
fn main() {
    let rt = tokio::runtime::Runtime::new().unwrap();
    rt.block_on(async { ... });
}
```

✅ GOOD:
```rust
#[tokio::main]
async fn main() {
    // Tokio runtime handles everything
}
```

- [ ] **Router is created with all routes defined**
  - Uses `Router::new()` with chained `.route()` calls
  - Groups related routes together (RESTful patterns)
  - WebSocket routes use `get()` method with `ws.on_upgrade()`
  - State is attached with `.with_state()`

✅ GOOD:
```rust
let app = Router::new()
    // CRUD for zones
    .route("/zones", post(create_zone))
    .route("/zones", get(list_zones))
    .route("/zones/{id}", get(get_zone))
    .route("/zones/{id}", put(update_zone))
    .route("/zones/{id}", delete(delete_zone))
    // WebSocket
    .route("/ws", get(ws_handler))
    // Health check
    .route("/health", get(health))
    .layer(CorsLayer::permissive())
    .with_state(state);
```

- [ ] **CORS is configured appropriately**
  - Uses `CorsLayer::permissive()` for internal services
  - Applied as layer via `.layer(CorsLayer::permissive())`
  - Enables cross-origin requests from console

✅ GOOD:
```rust
use tower_http::cors::CorsLayer;

Router::new()
    .route("/endpoint", get(handler))
    .layer(CorsLayer::permissive())  // Allows all origins for internal services
```

- [ ] **Server binds to correct address**
  - Port loaded from `PORT` env var with sensible default
  - Binds to `0.0.0.0` (all interfaces) for Docker compatibility
  - Uses `tokio::net::TcpListener` for async binding

✅ GOOD:
```rust
let port: u16 = std::env::var("PORT")
    .ok()
    .and_then(|p| p.parse().ok())
    .unwrap_or(4860);  // Service-specific default

let addr = SocketAddr::from(([0, 0, 0, 0], port));
let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
axum::serve(listener, app).await.unwrap();
```

**Reference**: See [api-design-patterns.md](./api-design-patterns.md) for more Axum patterns.

### 2. State Management

- [ ] **AppState struct contains all shared state**
  - Database pool (dispatch only)
  - Broadcast channels for WebSocket updates
  - Configuration (directories, URLs, etc.)
  - Connected client tracking (if applicable)

✅ GOOD:
```rust
struct AppState {
    db: PgPool,  // Database connection pool
    rovers: RwLock<HashMap<String, ConnectedRover>>,  // Mutable state
    broadcast_tx: broadcast::Sender<BroadcastMessage>,  // Update channel
}
```

- [ ] **State is wrapped in Arc for sharing**
  - Uses `Arc<AppState>` for clone-on-share semantics
  - Type alias `SharedState = Arc<AppState>` for convenience
  - Handlers receive `State<SharedState>` extractor

✅ GOOD:
```rust
type SharedState = Arc<AppState>;

let state = Arc::new(AppState::new(pool));

async fn handler(State(state): State<SharedState>) -> impl IntoResponse {
    // Access state here
}
```

- [ ] **Concurrent state access uses appropriate synchronization**
  - Immutable state: direct access via `Arc`
  - Mutable state: `RwLock` for many readers, few writers
  - Channels: `broadcast` for fan-out, `mpsc` for point-to-point
  - Never use `Mutex` around async operations

❌ BAD:
```rust
let rovers = state.rovers.lock().await;  // Mutex in async = deadlock risk
tokio::time::sleep(Duration::from_secs(5)).await;  // Holding lock across await!
drop(rovers);
```

✅ GOOD:
```rust
// Read
let rovers = state.rovers.read().await;
let count = rovers.len();
drop(rovers);  // Release lock quickly

// Write
let mut rovers = state.rovers.write().await;
rovers.insert(id, rover);
drop(rovers);  // Release lock quickly
```

### 3. Database Patterns (Dispatch Service)

- [ ] **SQLx connection pool is created correctly**
  - Uses `PgPoolOptions::new()` to configure pool
  - Sets `max_connections` appropriately (10-20 for services)
  - Connection URL from `DATABASE_URL` env var
  - Handles connection errors gracefully

✅ GOOD:
```rust
let database_url = std::env::var("DATABASE_URL")
    .expect("DATABASE_URL must be set");

let pool = PgPoolOptions::new()
    .max_connections(10)
    .connect(&database_url)
    .await
    .expect("Failed to connect to database");
```

- [ ] **Migrations are applied on startup**
  - Migration SQL files in `migrations/` directory
  - Applied manually in `run_migrations()` function
  - Checks if migration already applied before running
  - Logs migration status

✅ GOOD:
```rust
async fn run_migrations(pool: &PgPool) {
    let migration = include_str!("../migrations/001_initial.sql");

    // Check if already migrated
    let table_exists: bool = sqlx::query_scalar(
        "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'zones')"
    )
    .fetch_one(pool)
    .await
    .unwrap_or(false);

    if !table_exists {
        info!("Running migration...");
        sqlx::raw_sql(migration).execute(pool).await.expect("Migration failed");
    }
}
```

- [ ] **Database queries use parameterized queries**
  - NEVER use string concatenation for SQL
  - Always use `.bind()` for parameters
  - Prevents SQL injection vulnerabilities

❌ BAD (SQL injection vulnerability):
```rust
let query = format!("SELECT * FROM zones WHERE id = '{}'", user_input);
sqlx::query(&query).fetch_one(&pool).await?;
```

✅ GOOD:
```rust
sqlx::query_as::<_, Zone>(
    "SELECT * FROM zones WHERE id = $1"
)
.bind(id)  // Parameterized - safe!
.fetch_one(&pool)
.await?
```

- [ ] **Query results use appropriate methods**
  - `.fetch_one()` - exactly one row expected, error if zero or multiple
  - `.fetch_optional()` - zero or one row, returns `Option<T>`
  - `.fetch_all()` - multiple rows, returns `Vec<T>`
  - `.execute()` - for INSERT/UPDATE/DELETE, returns rows affected

✅ GOOD:
```rust
// Get by ID - must exist
let zone: Zone = sqlx::query_as("SELECT ... WHERE id = $1")
    .bind(id)
    .fetch_one(&state.db)
    .await
    .map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()))?;

// Get by ID - may not exist
let zone: Option<Zone> = sqlx::query_as("SELECT ... WHERE id = $1")
    .bind(id)
    .fetch_optional(&state.db)
    .await?;
```

- [ ] **JSONB fields are handled correctly**
  - Use `#[sqlx(json)]` attribute on struct fields
  - Serialize/deserialize with serde
  - Type must be `serde_json::Value` in database model
  - Cast to concrete types when needed

✅ GOOD:
```rust
#[derive(FromRow, Serialize)]
struct Zone {
    pub id: Uuid,
    #[sqlx(json)]
    pub waypoints: serde_json::Value,  // Stored as JSONB
}

// When parsing
let waypoints: Vec<Waypoint> = serde_json::from_value(zone.waypoints)?;
```

**Reference**: See [database-patterns.md](./database-patterns.md) for comprehensive database guidance.

### 4. Error Handling

- [ ] **Handler errors use Result with IntoResponse**
  - Return type: `Result<impl IntoResponse, (StatusCode, String)>`
  - Errors map to HTTP status codes
  - Error messages are user-friendly (not debug strings)

✅ GOOD:
```rust
async fn get_zone(
    State(state): State<SharedState>,
    Path(id): Path<Uuid>,
) -> Result<impl IntoResponse, (StatusCode, String)> {
    let zone = sqlx::query_as("...")
        .bind(id)
        .fetch_optional(&state.db)
        .await
        .map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()))?
        .ok_or((StatusCode::NOT_FOUND, "Zone not found".to_string()))?;

    Ok(Json(zone))
}
```

- [ ] **Custom error types implement IntoResponse**
  - Derive from `thiserror::Error` for libraries
  - Implement `IntoResponse` for Axum handlers
  - Map error variants to appropriate HTTP status codes

✅ GOOD:
```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ApiError {
    #[error("Not found: {0}")]
    NotFound(String),
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
}

impl IntoResponse for ApiError {
    fn into_response(self) -> axum::response::Response {
        let (status, message) = match &self {
            ApiError::NotFound(msg) => (StatusCode::NOT_FOUND, msg.clone()),
            ApiError::Io(e) => (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()),
        };
        (status, Json(serde_json::json!({ "error": message }))).into_response()
    }
}
```

- [ ] **Database errors are handled appropriately**
  - `.map_err()` converts SQLx errors to HTTP responses
  - Use `.ok_or()` to convert `Option` to `Result` with NOT_FOUND
  - Log errors before returning them

✅ GOOD:
```rust
let zone: Zone = sqlx::query_as("SELECT ... WHERE id = $1")
    .bind(id)
    .fetch_optional(&state.db)
    .await
    .map_err(|e| {
        warn!(error = %e, "Database query failed");
        (StatusCode::INTERNAL_SERVER_ERROR, "Database error".to_string())
    })?
    .ok_or_else(|| {
        warn!(zone_id = %id, "Zone not found");
        (StatusCode::NOT_FOUND, "Zone not found".to_string())
    })?;
```

### 5. WebSocket Communication

- [ ] **WebSocket upgrade is handled correctly**
  - Handler accepts `WebSocketUpgrade` extractor
  - Returns `ws.on_upgrade(|socket| handler_fn(socket, state))`
  - Handler function is `async fn` taking `WebSocket` and state

✅ GOOD:
```rust
async fn ws_handler(
    ws: WebSocketUpgrade,
    State(state): State<SharedState>,
) -> impl IntoResponse {
    ws.on_upgrade(|socket| handle_ws(socket, state))
}

async fn handle_ws(socket: WebSocket, state: SharedState) {
    let (mut sender, mut receiver) = socket.split();
    // ... WebSocket logic
}
```

- [ ] **WebSocket messages are properly parsed**
  - Use `serde_json::from_str()` to parse text messages
  - Handle parse errors gracefully (don't crash connection)
  - Implement message protocol with tagged enum

✅ GOOD:
```rust
#[derive(Deserialize)]
#[serde(tag = "type", rename_all = "lowercase")]
enum RoverMessage {
    Register { rover_id: String },
    Progress { task_id: Uuid, progress: i32 },
}

// In handler
while let Some(msg) = receiver.next().await {
    let msg = match msg {
        Ok(Message::Text(text)) => text,
        Ok(Message::Close(_)) => break,
        _ => continue,
    };

    match serde_json::from_str::<RoverMessage>(&msg) {
        Ok(RoverMessage::Register { rover_id }) => { ... },
        Ok(RoverMessage::Progress { task_id, progress }) => { ... },
        Err(e) => warn!(error = %e, "Failed to parse message"),
    }
}
```

- [ ] **Broadcast channels are used correctly**
  - Create channel with `broadcast::channel(capacity)`
  - Subscribe with `.subscribe()` in each WebSocket handler
  - Send updates with `.send()` (returns `Result`)
  - Handle lagged receivers (broadcast can drop messages)

✅ GOOD:
```rust
// In AppState
struct AppState {
    broadcast_tx: broadcast::Sender<BroadcastMessage>,
}

impl AppState {
    fn new() -> Self {
        let (broadcast_tx, _rx) = broadcast::channel(256);  // Drop receiver
        Self { broadcast_tx }
    }

    fn broadcast(&self, msg: BroadcastMessage) {
        let _ = self.broadcast_tx.send(msg);  // Ignore if no receivers
    }
}

// In WebSocket handler
let mut rx = state.broadcast_tx.subscribe();
loop {
    tokio::select! {
        Ok(msg) = rx.recv() => {
            // Send to client
        }
        msg = receiver.next() => {
            // Handle incoming message
        }
    }
}
```

- [ ] **WebSocket cleanup is handled on disconnect**
  - Remove client from tracking map
  - Abort spawned tasks
  - Broadcast disconnect event if needed
  - No panics in cleanup code

✅ GOOD:
```rust
async fn handle_ws(socket: WebSocket, state: SharedState) {
    let mut rover_id: Option<String> = None;

    // WebSocket loop
    while let Some(msg) = receiver.next().await {
        // ... handle messages
        if let RoverMessage::Register { rover_id: id } = parsed {
            rover_id = Some(id.clone());
            // Register rover
        }
    }

    // Cleanup on disconnect
    if let Some(id) = rover_id {
        info!(rover_id = %id, "Client disconnected");
        let mut rovers = state.rovers.write().await;
        rovers.remove(&id);
        drop(rovers);

        state.broadcast(BroadcastMessage::Disconnected { rover_id: id });
    }
}
```

**Reference**: See [websocket-patterns.md](./websocket-patterns.md) for detailed WebSocket guidance.

### 6. Logging and Observability

- [ ] **Tracing is initialized early**
  - Use `tracing_subscriber::fmt()` in `main()`
  - Set env filter with fallback: `RUST_LOG` env var or default level
  - Initialize before any other operations

✅ GOOD:
```rust
#[tokio::main]
async fn main() {
    tracing_subscriber::fmt()
        .with_env_filter(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "discovery=info,sqlx=warn".into())
        )
        .init();

    info!("Service starting...");
    // ... rest of main
}
```

- [ ] **Log statements use structured logging**
  - Use `info!`, `warn!`, `error!`, `debug!` macros
  - Include context with key-value pairs
  - Use `%` for Display, `?` for Debug formatting
  - Log important events: startup, requests, errors, shutdown

✅ GOOD:
```rust
info!(
    rover_id = %rover.id,
    address = %rover.address,
    "Rover registered"
);

warn!(
    task_id = %task_id,
    error = %error,
    "Task failed"
);
```

- [ ] **Health check endpoint exists**
  - Endpoint at `/health` returning JSON
  - Includes service status and metrics
  - Returns 200 OK if service is healthy
  - Used by Docker healthcheck

✅ GOOD:
```rust
async fn health(State(state): State<SharedState>) -> impl IntoResponse {
    let rover_count = state.rovers.read().await.len();
    Json(serde_json::json!({
        "status": "ok",
        "rovers": rover_count
    }))
}
```

### 7. Configuration and Environment

- [ ] **Configuration loaded from environment variables**
  - Use `std::env::var()` for required config
  - Provide sensible defaults for optional config
  - Validate configuration early (fail fast)
  - Log configuration values (except secrets)

✅ GOOD:
```rust
// Required
let database_url = std::env::var("DATABASE_URL")
    .expect("DATABASE_URL must be set");

// Optional with default
let port: u16 = std::env::var("PORT")
    .ok()
    .and_then(|p| p.parse().ok())
    .unwrap_or(4860);

let sessions_dir = std::env::var("SESSIONS_DIR")
    .map(PathBuf::from)
    .unwrap_or_else(|_| PathBuf::from("/data/sessions"));

info!(
    port = port,
    sessions_dir = %sessions_dir.display(),
    "Configuration loaded"
);
```

- [ ] **Paths use PathBuf for cross-platform compatibility**
  - Never hardcode paths with `/` or `\`
  - Use `PathBuf::from()` to convert from env vars
  - Use `.join()` to build paths
  - Use `.display()` for logging paths

✅ GOOD:
```rust
let base_dir = PathBuf::from(std::env::var("DATA_DIR").unwrap_or("/data".into()));
let sessions_path = base_dir.join("sessions").join(&rover_id);

info!(path = %sessions_path.display(), "Session path");
```

### 8. Docker Build and Deployment

- [ ] **Dockerfile uses multi-stage build**
  - Stage 1: `rust:1.83-alpine` for building
  - Stage 2: `alpine:3.21` for runtime
  - Minimizes final image size (typically 10-20 MB)

✅ GOOD:
```dockerfile
# Build stage
FROM rust:1.83-alpine AS builder
RUN apk add --no-cache musl-dev
WORKDIR /app
COPY Cargo.toml Cargo.lock* ./
# Dummy build for caching
RUN mkdir src && echo "fn main() {}" > src/main.rs
RUN cargo build --release 2>/dev/null || true
# Real build
COPY src ./src
RUN touch src/main.rs
RUN cargo build --release

# Runtime stage
FROM alpine:3.21
RUN apk add --no-cache ca-certificates
COPY --from=builder /app/target/release/[service] /usr/local/bin/[service]
ENV PORT=4860
EXPOSE 4860
CMD ["[service]"]
```

- [ ] **Release profile is optimized**
  - `lto = true` - Link-time optimization
  - `opt-level = "z"` - Optimize for size
  - `strip = true` - Remove debug symbols

✅ GOOD in Cargo.toml:
```toml
[profile.release]
lto = true
opt-level = "z"
strip = true
```

- [ ] **Docker Compose service is configured correctly**
  - Container name follows pattern: `depot-<service>`
  - Restart policy: `unless-stopped`
  - Ports mapped correctly (host:container)
  - Environment variables passed from `.env`
  - Healthcheck defined
  - Dependencies declared with `depends_on`

✅ GOOD in docker-compose.yml:
```yaml
discovery:
  build:
    context: ./discovery
    dockerfile: Dockerfile
  container_name: depot-discovery
  restart: unless-stopped
  ports:
    - "4860:4860"
  environment:
    - PORT=4860
    - RUST_LOG=discovery=info
  healthcheck:
    test: ["CMD", "wget", "-q", "-O-", "http://localhost:4860/health"]
    interval: 10s
    timeout: 3s
    retries: 3
```

**Reference**: See [docker-deployment.md](./docker-deployment.md) for comprehensive Docker patterns.

## Service-Specific Reviews

### Discovery Service (depot/discovery)

**Purpose**: Rover registration, heartbeat tracking, session file serving

**Key Files**:
- `src/main.rs` - Main service implementation (~600 LOC)
- `Dockerfile` - Multi-stage build

**Endpoints**:
- `POST /register` - Register rover with metadata
- `POST /heartbeat/{id}` - Update rover status with telemetry
- `GET /rovers` - List all registered rovers (HTTP fallback)
- `GET /ws` - WebSocket for live rover updates to operators
- `GET /api/sessions` - List recorded sessions
- `GET /api/sessions/{rover_id}/{session_dir}/session.rrd` - Serve session file
- `GET /health` - Health check

**Specific Concerns**:

- [ ] **Rover timeout is implemented correctly**
  - Constant `ROVER_TIMEOUT = Duration::from_secs(10)`
  - Background task checks for stale rovers every 2 seconds
  - Online status computed on-the-fly in `get_rovers()`

- [ ] **Session file serving is secure**
  - Path traversal attacks prevented (no `..` in paths)
  - Files served from configured `SESSIONS_DIR` only
  - Tries both direct and nested session structures
  - Returns 404 if file doesn't exist

- [ ] **WebSocket updates are efficient**
  - Initial rover list sent on connection
  - Updates only sent when state changes
  - Broadcast channel prevents blocking on slow clients

**Common Issues**:
- Forgetting to call `state.notify()` after state changes
- Not dropping read locks before broadcasting (potential deadlock)
- Not handling both session directory structures (direct vs nested)

### Dispatch Service (depot/dispatch)

**Purpose**: Mission planning, zone management, task assignment to rovers

**Key Files**:
- `src/main.rs` - Main service implementation (~1200 LOC)
- `migrations/001_initial.sql` - Database schema
- `Dockerfile` - Multi-stage build

**Database Tables**:
- `zones` - Geographic areas (routes, polygons, points)
- `missions` - Scheduled work definitions
- `tasks` - Execution instances with progress tracking

**Endpoints**:
- `POST/GET/PUT/DELETE /zones` - Zone CRUD
- `POST/GET/PUT/DELETE /missions` - Mission CRUD
- `POST /missions/{id}/start` - Start mission (creates task, assigns to rover)
- `POST /missions/{id}/stop` - Stop mission (cancels active task)
- `GET/POST /tasks` - Task management
- `GET /ws` - WebSocket for rover connections
- `GET /ws/console` - WebSocket for console updates
- `GET /health` - Health check

**Specific Concerns**:

- [ ] **Task lifecycle is managed correctly**
  - States: pending → assigned → active → done/failed/cancelled
  - `started_at` set on first progress update
  - `ended_at` set when task completes/fails/cancelled
  - Rover's `current_task` cleared when task ends

- [ ] **WebSocket protocol is implemented correctly**
  - Two WebSocket endpoints: `/ws` (rovers), `/ws/console` (operators)
  - Rover messages: `Register`, `Progress`, `Complete`, `Failed`
  - Dispatch messages: `Task`, `Cancel`
  - Broadcast messages: `TaskUpdate`, `RoverUpdate`, `ZoneUpdate`, `MissionUpdate`

- [ ] **Task assignment logic is correct**
  - Check if mission has preferred rover, verify connected
  - If no preference, find any available rover (no current task)
  - Create task in database with status=assigned
  - Update rover's current_task in memory
  - Send task to rover via WebSocket
  - Rollback if send fails

- [ ] **JSONB fields are validated**
  - `zones.waypoints` contains array of `{x, y, theta?}` objects
  - `missions.schedule` contains `{trigger, cron?, loop}` object
  - Validate structure before inserting (prevent invalid data)

**Common Issues**:
- Not clearing `rover.current_task` when task ends (rover stuck)
- Forgetting to broadcast updates to console clients
- Not rolling back database changes if WebSocket send fails
- Race condition between task creation and rover disconnect

### Map API Service (depot/map-api)

**Purpose**: Serve processed maps and 3D assets to console and other clients

**Key Files**:
- `src/main.rs` - Main service implementation (~450 LOC)
- `Dockerfile` - Multi-stage build

**Endpoints**:
- `GET /maps` - List all maps
- `GET /maps/{id}` - Get map manifest (metadata)
- `GET /maps/{id}/{asset}` - Download asset (splat.ply, pointcloud.laz, mesh.glb, thumbnail.jpg)
- `GET /sessions` - List all sessions
- `GET /sessions/{id}` - Get session metadata
- `GET /maps/{id}/sessions` - Get sessions used to build map
- `GET /health` - Health check

**Specific Concerns**:

- [ ] **Map manifest loading is efficient**
  - Reads `maps/index.json` for map list
  - Lazily loads manifests from `maps/{name}/manifest.json`
  - Caches manifests in `RwLock<HashMap<Uuid, MapManifest>>`
  - Reloads on each list/get request (eventual consistency)

- [ ] **Asset serving is correct**
  - Validates asset exists in manifest before serving
  - Sets correct Content-Type header for each asset type
  - Reads entire file into memory (acceptable for small assets)
  - Returns 404 if asset file missing

- [ ] **File paths are constructed safely**
  - Uses `PathBuf::join()` to build paths
  - Validates file exists before serving
  - No path traversal vulnerabilities

**Common Issues**:
- Serving assets not listed in manifest (security issue)
- Not setting Content-Type header (browser confusion)
- Not handling missing files gracefully

### GPS Status Service (depot/gps-status)

**Purpose**: Monitor RTK base station status and broadcast to console

**Key Files**:
- `src/main.rs` - Main service implementation (~400 LOC)
- `Dockerfile` - Multi-stage build

**Endpoints**:
- `GET /status` - Current RTK base station status
- `GET /ws` - WebSocket for live status updates to console
- `GET /health` - Health check

**Specific Concerns**:

- [ ] **RTK status is polled correctly**
  - Background task polls base station via serial/TCP
  - Parses RTCM3/NMEA messages for status
  - Broadcasts status updates via WebSocket
  - Handles base station disconnection gracefully

- [ ] **WebSocket updates are throttled**
  - Status sent at reasonable interval (1-5 seconds)
  - Prevents overwhelming clients with updates
  - Initial status sent on connection

**Common Issues**:
- Not handling base station disconnection
- Sending updates too frequently (CPU/bandwidth waste)
- Not validating RTCM3 message checksums

### Mapper Service (depot/mapper)

**Purpose**: Orchestrate map processing pipeline (batch job, not always running)

**Key Files**:
- `src/main.rs` - Main orchestrator (~1000 LOC)
- `Dockerfile` - Multi-stage build

**Operation**:
- Runs as batch job (not a long-running service)
- Scans sessions directory for new sessions
- Queues sessions for processing
- Invokes splat-worker for 3D reconstruction
- Generates map manifests and assets
- Updates index.json

**Specific Concerns**:

- [ ] **Session discovery is efficient**
  - Scans filesystem for new sessions
  - Reads metadata.json from each session
  - Filters by GPS bounds, frame counts, etc.
  - Deduplicates sessions already processed

- [ ] **Processing pipeline is fault-tolerant**
  - Tracks session status (pending, processing, processed, failed)
  - Retries failed sessions with exponential backoff
  - Logs errors for manual intervention
  - Doesn't block on failed sessions

- [ ] **Map manifest generation is correct**
  - Calculates GPS bounds from all sessions
  - Lists all available assets (splat, pointcloud, mesh, thumbnail)
  - Includes session references
  - Updates index.json atomically

**Common Issues**:
- Not handling concurrent mapper invocations (file conflicts)
- Not validating session metadata before processing
- Not cleaning up temporary files on failure

## Quick Commands

### Development

```bash
# Check code (no build)
cargo check -p discovery
cargo check -p dispatch

# Build service
cargo build -p discovery --release

# Run tests
cargo test -p dispatch

# Run service locally (requires dependencies)
cd depot/discovery
PORT=4860 cargo run

# Run with logging
RUST_LOG=discovery=debug cargo run
```

### Docker

```bash
# Build service image
cd depot/discovery
docker build -t depot-discovery .

# Run service container
docker run -p 4860:4860 -e RUST_LOG=info depot-discovery

# Build all services via Docker Compose
cd depot
docker compose build

# Start all services
docker compose up -d

# View logs
docker compose logs -f discovery

# Restart service
docker compose restart dispatch

# Stop all services
docker compose down
```

### Database (Dispatch Only)

```bash
# Connect to PostgreSQL
docker compose exec postgres psql -U postgres -d dispatch

# View tables
\dt

# Query zones
SELECT id, name, zone_type FROM zones;

# Query tasks
SELECT id, status, rover_id, progress FROM tasks ORDER BY created_at DESC LIMIT 10;

# Reset database (DESTRUCTIVE)
docker compose down -v  # Removes volumes
docker compose up -d postgres
docker compose restart dispatch  # Migrations run on startup
```

## References

- [database-patterns.md](./database-patterns.md) - SQLx, migrations, queries, transactions
- [api-design-patterns.md](./api-design-patterns.md) - Axum routing, middleware, error handling
- [websocket-patterns.md](./websocket-patterns.md) - WebSocket protocols, broadcast channels
- [docker-deployment.md](./docker-deployment.md) - Multi-stage builds, Docker Compose, healthchecks
- [CLAUDE.md](../../../CLAUDE.md) - Project-wide conventions
- [depot/README.md](../../../depot/README.md) - Depot architecture overview
