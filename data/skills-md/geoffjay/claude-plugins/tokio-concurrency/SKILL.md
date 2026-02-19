---
name: tokio-concurrency
description: Advanced concurrency patterns for Tokio including fan-out/fan-in, pipeline processing, rate limiting, and coordinated shutdown. Use when building high-concurrency async systems.
---

# Tokio Concurrency Patterns

This skill provides advanced concurrency patterns for building scalable async applications with Tokio.

## Fan-Out/Fan-In Pattern

Distribute work across multiple workers and collect results:

```rust
use futures::stream::{self, StreamExt};

pub async fn fan_out_fan_in<T, R>(
    items: Vec<T>,
    concurrency: usize,
    process: impl Fn(T) -> Pin<Box<dyn Future<Output = R> + Send>> + Send + Sync + 'static,
) -> Vec<R>
where
    T: Send + 'static,
    R: Send + 'static,
{
    stream::iter(items)
        .map(|item| process(item))
        .buffer_unordered(concurrency)
        .collect()
        .await
}

// Usage
let results = fan_out_fan_in(
    items,
    10,
    |item| Box::pin(async move { process_item(item).await })
).await;
```

## Pipeline Processing

Chain async processing stages:

```rust
use tokio::sync::mpsc;

pub struct Pipeline<T> {
    stages: Vec<Box<dyn Stage<T>>>,
}

#[async_trait::async_trait]
pub trait Stage<T>: Send {
    async fn process(&self, item: T) -> T;
}

impl<T: Send + 'static> Pipeline<T> {
    pub fn new() -> Self {
        Self { stages: Vec::new() }
    }

    pub fn add_stage<S: Stage<T> + 'static>(mut self, stage: S) -> Self {
        self.stages.push(Box::new(stage));
        self
    }

    pub async fn run(self, mut input: mpsc::Receiver<T>) -> mpsc::Receiver<T> {
        let (tx, rx) = mpsc::channel(100);

        tokio::spawn(async move {
            while let Some(mut item) = input.recv().await {
                // Process through all stages
                for stage in &self.stages {
                    item = stage.process(item).await;
                }

                if tx.send(item).await.is_err() {
                    break;
                }
            }
        });

        rx
    }
}

// Usage
let pipeline = Pipeline::new()
    .add_stage(ValidationStage)
    .add_stage(TransformStage)
    .add_stage(EnrichmentStage);

let output = pipeline.run(input_channel).await;
```

## Rate Limiting

Control operation rate using token bucket or leaky bucket:

```rust
use tokio::time::{interval, Duration, Instant};
use tokio::sync::Semaphore;
use std::sync::Arc;

pub struct RateLimiter {
    semaphore: Arc<Semaphore>,
    rate: usize,
    period: Duration,
}

impl RateLimiter {
    pub fn new(rate: usize, period: Duration) -> Self {
        let limiter = Self {
            semaphore: Arc::new(Semaphore::new(rate)),
            rate,
            period,
        };

        // Refill tokens
        let semaphore = limiter.semaphore.clone();
        let rate = limiter.rate;
        let period = limiter.period;

        tokio::spawn(async move {
            let mut interval = interval(period);
            loop {
                interval.tick().await;
                // Add permits up to max
                for _ in 0..rate {
                    if semaphore.available_permits() < rate {
                        semaphore.add_permits(1);
                    }
                }
            }
        });

        limiter
    }

    pub async fn acquire(&self) {
        self.semaphore.acquire().await.unwrap().forget();
    }
}

// Usage
let limiter = RateLimiter::new(100, Duration::from_secs(1));

for _ in 0..1000 {
    limiter.acquire().await;
    make_request().await;
}
```

## Parallel Task Execution with Join

Execute multiple tasks in parallel and wait for all:

```rust
use tokio::try_join;

pub async fn parallel_operations() -> Result<(String, Vec<User>, Config), Error> {
    try_join!(
        fetch_data(),
        fetch_users(),
        load_config()
    )
}

// With manual spawning for CPU-bound work
pub async fn parallel_cpu_work(items: Vec<Item>) -> Vec<Result<Processed, Error>> {
    let handles: Vec<_> = items
        .into_iter()
        .map(|item| {
            tokio::task::spawn_blocking(move || {
                expensive_cpu_work(item)
            })
        })
        .collect();

    let mut results = Vec::new();
    for handle in handles {
        results.push(handle.await.unwrap());
    }
    results
}
```

## Coordinated Shutdown with CancellationToken

Manage hierarchical cancellation:

```rust
use tokio_util::sync::CancellationToken;
use tokio::select;

pub struct Coordinator {
    token: CancellationToken,
    tasks: Vec<tokio::task::JoinHandle<()>>,
}

impl Coordinator {
    pub fn new() -> Self {
        Self {
            token: CancellationToken::new(),
            tasks: Vec::new(),
        }
    }

    pub fn spawn<F>(&mut self, f: F)
    where
        F: Future<Output = ()> + Send + 'static,
    {
        let token = self.token.child_token();
        let handle = tokio::spawn(async move {
            select! {
                _ = token.cancelled() => {}
                _ = f => {}
            }
        });
        self.tasks.push(handle);
    }

    pub async fn shutdown(self) {
        self.token.cancel();

        for task in self.tasks {
            let _ = task.await;
        }
    }
}

// Usage
let mut coordinator = Coordinator::new();

coordinator.spawn(worker1());
coordinator.spawn(worker2());
coordinator.spawn(worker3());

// Later...
coordinator.shutdown().await;
```

## Async Trait Patterns

Work around async trait limitations:

```rust
use async_trait::async_trait;

#[async_trait]
pub trait AsyncService {
    async fn process(&self, input: String) -> Result<String, Error>;
}

// Alternative without async-trait
pub trait AsyncServiceManual {
    fn process<'a>(
        &'a self,
        input: String,
    ) -> Pin<Box<dyn Future<Output = Result<String, Error>> + Send + 'a>>;
}

// Implementation
struct MyService;

#[async_trait]
impl AsyncService for MyService {
    async fn process(&self, input: String) -> Result<String, Error> {
        // async implementation
        Ok(input.to_uppercase())
    }
}
```

## Shared State Management

Safe concurrent access to shared state:

```rust
use tokio::sync::RwLock;
use std::sync::Arc;

pub struct SharedState {
    data: Arc<RwLock<HashMap<String, String>>>,
}

impl SharedState {
    pub fn new() -> Self {
        Self {
            data: Arc::new(RwLock::new(HashMap::new())),
        }
    }

    pub async fn get(&self, key: &str) -> Option<String> {
        let data = self.data.read().await;
        data.get(key).cloned()
    }

    pub async fn set(&self, key: String, value: String) {
        let mut data = self.data.write().await;
        data.insert(key, value);
    }

    // Batch operations
    pub async fn get_many(&self, keys: &[String]) -> Vec<Option<String>> {
        let data = self.data.read().await;
        keys.iter()
            .map(|key| data.get(key).cloned())
            .collect()
    }
}

// Clone is cheap (Arc)
impl Clone for SharedState {
    fn clone(&self) -> Self {
        Self {
            data: self.data.clone(),
        }
    }
}
```

## Work Stealing Queue

Implement work stealing for load balancing:

```rust
use tokio::sync::mpsc;
use std::sync::Arc;

pub struct WorkQueue<T> {
    queues: Vec<mpsc::Sender<T>>,
    receivers: Vec<mpsc::Receiver<T>>,
    next: Arc<AtomicUsize>,
}

impl<T: Send + 'static> WorkQueue<T> {
    pub fn new(workers: usize, capacity: usize) -> Self {
        let mut queues = Vec::new();
        let mut receivers = Vec::new();

        for _ in 0..workers {
            let (tx, rx) = mpsc::channel(capacity);
            queues.push(tx);
            receivers.push(rx);
        }

        Self {
            queues,
            receivers,
            next: Arc::new(AtomicUsize::new(0)),
        }
    }

    pub async fn submit(&self, work: T) -> Result<(), mpsc::error::SendError<T>> {
        let idx = self.next.fetch_add(1, Ordering::Relaxed) % self.queues.len();
        self.queues[idx].send(work).await
    }

    pub fn spawn_workers<F>(mut self, process: F)
    where
        F: Fn(T) -> Pin<Box<dyn Future<Output = ()> + Send>> + Send + Sync + Clone + 'static,
    {
        for mut rx in self.receivers.drain(..) {
            let process = process.clone();
            tokio::spawn(async move {
                while let Some(work) = rx.recv().await {
                    process(work).await;
                }
            });
        }
    }
}
```

## Circuit Breaker for Resilience

Prevent cascading failures:

```rust
use std::sync::atomic::{AtomicU64, Ordering};
use tokio::time::{Instant, Duration};

pub enum CircuitState {
    Closed,
    Open(Instant),
    HalfOpen,
}

pub struct CircuitBreaker {
    state: Arc<RwLock<CircuitState>>,
    failure_count: AtomicU64,
    threshold: u64,
    timeout: Duration,
}

impl CircuitBreaker {
    pub fn new(threshold: u64, timeout: Duration) -> Self {
        Self {
            state: Arc::new(RwLock::new(CircuitState::Closed)),
            failure_count: AtomicU64::new(0),
            threshold,
            timeout,
        }
    }

    pub async fn call<F, T, E>(&self, f: F) -> Result<T, CircuitBreakerError<E>>
    where
        F: Future<Output = Result<T, E>>,
    {
        // Check if circuit is open
        let state = self.state.read().await;
        match *state {
            CircuitState::Open(opened_at) => {
                if opened_at.elapsed() < self.timeout {
                    return Err(CircuitBreakerError::Open);
                }
                drop(state);
                *self.state.write().await = CircuitState::HalfOpen;
            }
            _ => {}
        }
        drop(state);

        // Execute request
        match f.await {
            Ok(result) => {
                self.on_success().await;
                Ok(result)
            }
            Err(e) => {
                self.on_failure().await;
                Err(CircuitBreakerError::Inner(e))
            }
        }
    }

    async fn on_success(&self) {
        self.failure_count.store(0, Ordering::SeqCst);
        let mut state = self.state.write().await;
        if matches!(*state, CircuitState::HalfOpen) {
            *state = CircuitState::Closed;
        }
    }

    async fn on_failure(&self) {
        let failures = self.failure_count.fetch_add(1, Ordering::SeqCst) + 1;
        if failures >= self.threshold {
            *self.state.write().await = CircuitState::Open(Instant::now());
        }
    }
}
```

## Batching Operations

Batch multiple operations for efficiency:

```rust
use tokio::time::{interval, Duration};

pub struct Batcher<T> {
    tx: mpsc::Sender<T>,
}

impl<T: Send + 'static> Batcher<T> {
    pub fn new<F>(
        batch_size: usize,
        batch_timeout: Duration,
        process: F,
    ) -> Self
    where
        F: Fn(Vec<T>) -> Pin<Box<dyn Future<Output = ()> + Send>> + Send + 'static,
    {
        let (tx, mut rx) = mpsc::channel(1000);

        tokio::spawn(async move {
            let mut batch = Vec::with_capacity(batch_size);
            let mut interval = interval(batch_timeout);

            loop {
                tokio::select! {
                    item = rx.recv() => {
                        match item {
                            Some(item) => {
                                batch.push(item);
                                if batch.len() >= batch_size {
                                    process(std::mem::replace(&mut batch, Vec::with_capacity(batch_size))).await;
                                }
                            }
                            None => break,
                        }
                    }
                    _ = interval.tick() => {
                        if !batch.is_empty() {
                            process(std::mem::replace(&mut batch, Vec::with_capacity(batch_size))).await;
                        }
                    }
                }
            }

            // Process remaining items
            if !batch.is_empty() {
                process(batch).await;
            }
        });

        Self { tx }
    }

    pub async fn submit(&self, item: T) -> Result<(), mpsc::error::SendError<T>> {
        self.tx.send(item).await
    }
}
```

## Best Practices

1. **Use appropriate concurrency limits** - Don't spawn unbounded tasks
2. **Implement backpressure** - Use bounded channels and semaphores
3. **Handle cancellation** - Support cooperative cancellation with tokens
4. **Avoid lock contention** - Minimize lock scope, prefer channels
5. **Use rate limiting** - Protect external services
6. **Implement circuit breakers** - Prevent cascading failures
7. **Batch operations** - Reduce overhead for small operations
8. **Profile concurrency** - Use tokio-console to understand behavior
9. **Use appropriate synchronization** - RwLock for read-heavy, Mutex for write-heavy
10. **Design for failure** - Always consider what happens when operations fail
