---
name: tokio-networking
description: Network programming patterns with Hyper, Tonic, and Tower. Use when building HTTP services, gRPC applications, implementing middleware, connection pooling, or health checks.
---

# Tokio Networking Patterns

This skill provides network programming patterns for building production-grade services with the Tokio ecosystem.

## HTTP Service with Hyper and Axum

Build HTTP services with routing and middleware:

```rust
use axum::{
    Router,
    routing::{get, post},
    extract::{State, Path, Json},
    response::IntoResponse,
    middleware,
};
use std::sync::Arc;

#[derive(Clone)]
struct AppState {
    db: Arc<Database>,
    cache: Arc<Cache>,
}

async fn create_app() -> Router {
    let state = AppState {
        db: Arc::new(Database::new().await),
        cache: Arc::new(Cache::new()),
    };

    Router::new()
        .route("/health", get(health_check))
        .route("/api/v1/users", get(list_users).post(create_user))
        .route("/api/v1/users/:id", get(get_user).delete(delete_user))
        .layer(middleware::from_fn(logging_middleware))
        .layer(middleware::from_fn(auth_middleware))
        .with_state(state)
}

async fn health_check() -> impl IntoResponse {
    "OK"
}

async fn get_user(
    State(state): State<AppState>,
    Path(id): Path<u64>,
) -> Result<Json<User>, StatusCode> {
    state.db.get_user(id)
        .await
        .map(Json)
        .ok_or(StatusCode::NOT_FOUND)
}

async fn logging_middleware<B>(
    req: Request<B>,
    next: Next<B>,
) -> impl IntoResponse {
    let method = req.method().clone();
    let uri = req.uri().clone();

    let start = Instant::now();
    let response = next.run(req).await;
    let duration = start.elapsed();

    tracing::info!(
        method = %method,
        uri = %uri,
        status = %response.status(),
        duration_ms = duration.as_millis(),
        "request completed"
    );

    response
}
```

## gRPC Service with Tonic

Build type-safe gRPC services:

```rust
use tonic::{transport::Server, Request, Response, Status};

pub mod proto {
    tonic::include_proto!("myservice");
}

use proto::my_service_server::{MyService, MyServiceServer};

#[derive(Default)]
pub struct MyServiceImpl {
    db: Arc<Database>,
}

#[tonic::async_trait]
impl MyService for MyServiceImpl {
    async fn get_user(
        &self,
        request: Request<proto::GetUserRequest>,
    ) -> Result<Response<proto::User>, Status> {
        let req = request.into_inner();

        let user = self.db.get_user(req.id)
            .await
            .map_err(|e| Status::internal(e.to_string()))?
            .ok_or_else(|| Status::not_found("User not found"))?;

        Ok(Response::new(proto::User {
            id: user.id,
            name: user.name,
            email: user.email,
        }))
    }

    type ListUsersStream = ReceiverStream<Result<proto::User, Status>>;

    async fn list_users(
        &self,
        request: Request<proto::ListUsersRequest>,
    ) -> Result<Response<Self::ListUsersStream>, Status> {
        let (tx, rx) = mpsc::channel(100);

        let db = self.db.clone();
        tokio::spawn(async move {
            let mut users = db.list_users().await.unwrap();

            while let Some(user) = users.next().await {
                let proto_user = proto::User {
                    id: user.id,
                    name: user.name,
                    email: user.email,
                };

                if tx.send(Ok(proto_user)).await.is_err() {
                    break;
                }
            }
        });

        Ok(Response::new(ReceiverStream::new(rx)))
    }
}

async fn serve() -> Result<(), Box<dyn std::error::Error>> {
    let addr = "[::1]:50051".parse()?;
    let service = MyServiceImpl::default();

    Server::builder()
        .add_service(MyServiceServer::new(service))
        .serve(addr)
        .await?;

    Ok(())
}
```

## Tower Middleware Composition

Layer middleware for cross-cutting concerns:

```rust
use tower::{ServiceBuilder, Service};
use tower_http::{
    trace::TraceLayer,
    compression::CompressionLayer,
    timeout::TimeoutLayer,
    limit::RateLimitLayer,
};
use std::time::Duration;

fn create_middleware_stack<S>(service: S) -> impl Service
where
    S: Service + Clone,
{
    ServiceBuilder::new()
        // Outermost layer (executed first)
        .layer(TraceLayer::new_for_http())
        .layer(CompressionLayer::new())
        .layer(TimeoutLayer::new(Duration::from_secs(30)))
        .layer(RateLimitLayer::new(100, Duration::from_secs(1)))
        // Innermost layer (executed last)
        .service(service)
}

// Custom middleware
use tower::Layer;

#[derive(Clone)]
struct MetricsLayer {
    metrics: Arc<Metrics>,
}

impl<S> Layer<S> for MetricsLayer {
    type Service = MetricsService<S>;

    fn layer(&self, inner: S) -> Self::Service {
        MetricsService {
            inner,
            metrics: self.metrics.clone(),
        }
    }
}

#[derive(Clone)]
struct MetricsService<S> {
    inner: S,
    metrics: Arc<Metrics>,
}

impl<S, Req> Service<Req> for MetricsService<S>
where
    S: Service<Req>,
{
    type Response = S::Response;
    type Error = S::Error;
    type Future = /* ... */;

    fn poll_ready(&mut self, cx: &mut Context<'_>) -> Poll<Result<(), Self::Error>> {
        self.inner.poll_ready(cx)
    }

    fn call(&mut self, req: Req) -> Self::Future {
        self.metrics.requests_total.inc();
        let timer = self.metrics.request_duration.start_timer();

        let future = self.inner.call(req);
        let metrics = self.metrics.clone();

        Box::pin(async move {
            let result = future.await;
            timer.observe_duration();
            result
        })
    }
}
```

## Connection Pooling

Manage connection pools efficiently:

```rust
use deadpool_postgres::{Config, Pool, Runtime};
use tokio_postgres::NoTls;

pub struct DatabasePool {
    pool: Pool,
}

impl DatabasePool {
    pub async fn new(config: &DatabaseConfig) -> Result<Self, Error> {
        let mut cfg = Config::new();
        cfg.host = Some(config.host.clone());
        cfg.port = Some(config.port);
        cfg.dbname = Some(config.database.clone());
        cfg.user = Some(config.user.clone());
        cfg.password = Some(config.password.clone());

        let pool = cfg.create_pool(Some(Runtime::Tokio1), NoTls)?;

        Ok(Self { pool })
    }

    pub async fn get(&self) -> Result<Client, Error> {
        self.pool.get().await.map_err(Into::into)
    }

    pub async fn query<T>(&self, f: impl FnOnce(&Client) -> F) -> Result<T, Error>
    where
        F: Future<Output = Result<T, Error>>,
    {
        let client = self.get().await?;
        f(&client).await
    }
}

// Usage
let pool = DatabasePool::new(&config).await?;

let users = pool.query(|client| async move {
    client.query("SELECT * FROM users", &[])
        .await
        .map_err(Into::into)
}).await?;
```

## Health Checks and Readiness Probes

Implement comprehensive health checks:

```rust
use axum::{Router, routing::get, Json};
use serde::Serialize;

#[derive(Serialize)]
struct HealthResponse {
    status: String,
    version: String,
    dependencies: Vec<DependencyHealth>,
}

#[derive(Serialize)]
struct DependencyHealth {
    name: String,
    status: String,
    latency_ms: Option<u64>,
    message: Option<String>,
}

async fn health_check(State(state): State<Arc<AppState>>) -> Json<HealthResponse> {
    let mut dependencies = Vec::new();

    // Check database
    let db_start = Instant::now();
    let db_status = match state.db.ping().await {
        Ok(_) => DependencyHealth {
            name: "database".into(),
            status: "healthy".into(),
            latency_ms: Some(db_start.elapsed().as_millis() as u64),
            message: None,
        },
        Err(e) => DependencyHealth {
            name: "database".into(),
            status: "unhealthy".into(),
            latency_ms: None,
            message: Some(e.to_string()),
        },
    };
    dependencies.push(db_status);

    // Check cache
    let cache_start = Instant::now();
    let cache_status = match state.cache.ping().await {
        Ok(_) => DependencyHealth {
            name: "cache".into(),
            status: "healthy".into(),
            latency_ms: Some(cache_start.elapsed().as_millis() as u64),
            message: None,
        },
        Err(e) => DependencyHealth {
            name: "cache".into(),
            status: "unhealthy".into(),
            latency_ms: None,
            message: Some(e.to_string()),
        },
    };
    dependencies.push(cache_status);

    let all_healthy = dependencies.iter().all(|d| d.status == "healthy");

    Json(HealthResponse {
        status: if all_healthy { "healthy" } else { "unhealthy" }.into(),
        version: env!("CARGO_PKG_VERSION").into(),
        dependencies,
    })
}

async fn readiness_check(State(state): State<Arc<AppState>>) -> StatusCode {
    if state.is_ready().await {
        StatusCode::OK
    } else {
        StatusCode::SERVICE_UNAVAILABLE
    }
}

pub fn health_routes() -> Router<Arc<AppState>> {
    Router::new()
        .route("/health", get(health_check))
        .route("/ready", get(readiness_check))
        .route("/live", get(|| async { StatusCode::OK }))
}
```

## Circuit Breaker Pattern

Protect against cascading failures:

```rust
use std::sync::atomic::{AtomicU64, Ordering};

pub struct ServiceClient {
    client: reqwest::Client,
    circuit_breaker: CircuitBreaker,
}

impl ServiceClient {
    pub async fn call(&self, req: Request) -> Result<Response, Error> {
        self.circuit_breaker.call(async {
            self.client
                .execute(req)
                .await
                .map_err(Into::into)
        }).await
    }
}
```

## Load Balancing

Distribute requests across multiple backends:

```rust
use tower::balance::p2c::Balance;
use tower::discover::ServiceList;

pub struct LoadBalancer {
    balancer: Balance<ServiceList<Vec<ServiceEndpoint>>, Request>,
}

impl LoadBalancer {
    pub fn new(endpoints: Vec<String>) -> Self {
        let services: Vec<_> = endpoints
            .into_iter()
            .map(|endpoint| create_client(endpoint))
            .collect();

        let balancer = Balance::new(ServiceList::new(services));

        Self { balancer }
    }

    pub async fn call(&mut self, req: Request) -> Result<Response, Error> {
        self.balancer.call(req).await
    }
}
```

## Request Deduplication

Deduplicate concurrent identical requests:

```rust
use tokio::sync::Mutex;
use std::collections::HashMap;

pub struct RequestDeduplicator<K, V> {
    in_flight: Arc<Mutex<HashMap<K, Arc<tokio::sync::Notify>>>>,
    cache: Arc<Mutex<HashMap<K, Arc<V>>>>,
}

impl<K: Eq + Hash + Clone, V> RequestDeduplicator<K, V> {
    pub fn new() -> Self {
        Self {
            in_flight: Arc::new(Mutex::new(HashMap::new())),
            cache: Arc::new(Mutex::new(HashMap::new())),
        }
    }

    pub async fn get_or_fetch<F, Fut>(
        &self,
        key: K,
        fetch: F,
    ) -> Result<Arc<V>, Error>
    where
        F: FnOnce() -> Fut,
        Fut: Future<Output = Result<V, Error>>,
    {
        // Check cache
        {
            let cache = self.cache.lock().await;
            if let Some(value) = cache.get(&key) {
                return Ok(value.clone());
            }
        }

        // Check if request is in flight
        let notify = {
            let mut in_flight = self.in_flight.lock().await;
            if let Some(notify) = in_flight.get(&key) {
                notify.clone()
            } else {
                let notify = Arc::new(tokio::sync::Notify::new());
                in_flight.insert(key.clone(), notify.clone());
                notify
            }
        };

        // Wait if another request is in progress
        notify.notified().await;

        // Check cache again
        {
            let cache = self.cache.lock().await;
            if let Some(value) = cache.get(&key) {
                return Ok(value.clone());
            }
        }

        // Fetch value
        let value = Arc::new(fetch().await?);

        // Update cache
        {
            let mut cache = self.cache.lock().await;
            cache.insert(key.clone(), value.clone());
        }

        // Remove from in-flight and notify
        {
            let mut in_flight = self.in_flight.lock().await;
            in_flight.remove(&key);
        }
        notify.notify_waiters();

        Ok(value)
    }
}
```

## Best Practices

1. **Use connection pooling** for database and HTTP connections
2. **Implement health checks** for all dependencies
3. **Add circuit breakers** for external service calls
4. **Use appropriate timeouts** for all network operations
5. **Implement retry logic** with exponential backoff
6. **Add comprehensive middleware** for logging, metrics, auth
7. **Use load balancing** for high availability
8. **Deduplicate requests** to reduce load
9. **Monitor latency** and error rates
10. **Design for graceful degradation** when services fail
