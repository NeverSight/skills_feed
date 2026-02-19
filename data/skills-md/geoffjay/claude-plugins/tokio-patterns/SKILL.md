---
name: tokio-patterns
description: Common Tokio patterns and idioms for async programming. Use when implementing worker pools, request-response patterns, pub/sub, timeouts, retries, or graceful shutdown.
---

# Tokio Patterns

This skill provides common patterns and idioms for building robust async applications with Tokio.

## Worker Pool Pattern

Limit concurrent task execution using a semaphore:

```rust
use tokio::sync::Semaphore;
use std::sync::Arc;

pub struct WorkerPool {
    semaphore: Arc<Semaphore>,
}

impl WorkerPool {
    pub fn new(size: usize) -> Self {
        Self {
            semaphore: Arc::new(Semaphore::new(size)),
        }
    }

    pub async fn execute<F, T>(&self, f: F) -> T
    where
        F: Future<Output = T>,
    {
        let _permit = self.semaphore.acquire().await.unwrap();
        f.await
    }
}

// Usage
let pool = WorkerPool::new(10);
let results = futures::future::join_all(
    (0..100).map(|i| pool.execute(process_item(i)))
).await;
```

## Request-Response Pattern

Use oneshot channels for request-response communication:

```rust
use tokio::sync::{mpsc, oneshot};

pub enum Command {
    Get { key: String, respond_to: oneshot::Sender<Option<String>> },
    Set { key: String, value: String },
}

pub async fn actor(mut rx: mpsc::Receiver<Command>) {
    let mut store = HashMap::new();

    while let Some(cmd) = rx.recv().await {
        match cmd {
            Command::Get { key, respond_to } => {
                let value = store.get(&key).cloned();
                let _ = respond_to.send(value);
            }
            Command::Set { key, value } => {
                store.insert(key, value);
            }
        }
    }
}

// Client usage
let (tx, rx) = mpsc::channel(32);
tokio::spawn(actor(rx));

let (respond_to, response) = oneshot::channel();
tx.send(Command::Get { key: "foo".into(), respond_to }).await.unwrap();
let value = response.await.unwrap();
```

## Pub/Sub with Channels

Use broadcast channels for pub/sub messaging:

```rust
use tokio::sync::broadcast;

pub struct PubSub<T: Clone> {
    tx: broadcast::Sender<T>,
}

impl<T: Clone> PubSub<T> {
    pub fn new(capacity: usize) -> Self {
        let (tx, _) = broadcast::channel(capacity);
        Self { tx }
    }

    pub fn subscribe(&self) -> broadcast::Receiver<T> {
        self.tx.subscribe()
    }

    pub fn publish(&self, message: T) -> Result<usize, broadcast::error::SendError<T>> {
        self.tx.send(message)
    }
}

// Usage
let pubsub = PubSub::new(100);

// Subscriber 1
let mut rx1 = pubsub.subscribe();
tokio::spawn(async move {
    while let Ok(msg) = rx1.recv().await {
        println!("Subscriber 1: {:?}", msg);
    }
});

// Subscriber 2
let mut rx2 = pubsub.subscribe();
tokio::spawn(async move {
    while let Ok(msg) = rx2.recv().await {
        println!("Subscriber 2: {:?}", msg);
    }
});

// Publisher
pubsub.publish("Hello".to_string()).unwrap();
```

## Timeout Pattern

Wrap operations with timeouts:

```rust
use tokio::time::{timeout, Duration};

pub async fn with_timeout<F, T>(duration: Duration, future: F) -> Result<T, TimeoutError>
where
    F: Future<Output = Result<T, Error>>,
{
    match timeout(duration, future).await {
        Ok(Ok(result)) => Ok(result),
        Ok(Err(e)) => Err(TimeoutError::Inner(e)),
        Err(_) => Err(TimeoutError::Elapsed),
    }
}

// Usage
let result = with_timeout(
    Duration::from_secs(5),
    fetch_data()
).await?;
```

## Retry with Exponential Backoff

Retry failed operations with backoff:

```rust
use tokio::time::{sleep, Duration};

pub async fn retry_with_backoff<F, T, E>(
    mut operation: F,
    max_retries: u32,
    initial_backoff: Duration,
) -> Result<T, E>
where
    F: FnMut() -> Pin<Box<dyn Future<Output = Result<T, E>>>>,
{
    let mut retries = 0;
    let mut backoff = initial_backoff;

    loop {
        match operation().await {
            Ok(result) => return Ok(result),
            Err(e) if retries < max_retries => {
                retries += 1;
                sleep(backoff).await;
                backoff *= 2; // Exponential backoff
            }
            Err(e) => return Err(e),
        }
    }
}

// Usage
let result = retry_with_backoff(
    || Box::pin(fetch_data()),
    3,
    Duration::from_millis(100)
).await?;
```

## Graceful Shutdown

Coordinate graceful shutdown across components:

```rust
use tokio::sync::broadcast;
use tokio::select;

pub struct ShutdownCoordinator {
    tx: broadcast::Sender<()>,
}

impl ShutdownCoordinator {
    pub fn new() -> Self {
        let (tx, _) = broadcast::channel(1);
        Self { tx }
    }

    pub fn subscribe(&self) -> broadcast::Receiver<()> {
        self.tx.subscribe()
    }

    pub fn shutdown(&self) {
        let _ = self.tx.send(());
    }
}

// Worker pattern
pub async fn worker(mut shutdown: broadcast::Receiver<()>) {
    loop {
        select! {
            _ = shutdown.recv() => {
                // Cleanup
                break;
            }
            result = do_work() => {
                // Process result
            }
        }
    }
}

// Main
let coordinator = ShutdownCoordinator::new();

let shutdown_rx1 = coordinator.subscribe();
let h1 = tokio::spawn(worker(shutdown_rx1));

let shutdown_rx2 = coordinator.subscribe();
let h2 = tokio::spawn(worker(shutdown_rx2));

// Wait for signal
tokio::signal::ctrl_c().await.unwrap();
coordinator.shutdown();

// Wait for workers
let _ = tokio::join!(h1, h2);
```

## Async Initialization

Lazy async initialization with `OnceCell`:

```rust
use tokio::sync::OnceCell;

pub struct Service {
    connection: OnceCell<Connection>,
}

impl Service {
    pub fn new() -> Self {
        Self {
            connection: OnceCell::new(),
        }
    }

    async fn get_connection(&self) -> &Connection {
        self.connection
            .get_or_init(|| async {
                Connection::connect().await.unwrap()
            })
            .await
    }

    pub async fn query(&self, sql: &str) -> Result<Vec<Row>> {
        let conn = self.get_connection().await;
        conn.query(sql).await
    }
}
```

## Resource Cleanup with Drop

Ensure cleanup even on task cancellation:

```rust
pub struct Resource {
    handle: SomeHandle,
}

impl Resource {
    pub async fn new() -> Self {
        Self {
            handle: acquire_resource().await,
        }
    }

    pub async fn use_resource(&self) -> Result<()> {
        // Use the resource
        Ok(())
    }
}

impl Drop for Resource {
    fn drop(&mut self) {
        // Synchronous cleanup
        // For async cleanup, use a separate shutdown method
        self.handle.close();
    }
}

// For async cleanup
impl Resource {
    pub async fn shutdown(self) {
        // Async cleanup
        self.handle.close_async().await;
    }
}
```

## Select Multiple Futures

Use `select!` to race multiple operations:

```rust
use tokio::select;

pub async fn select_example() {
    let mut rx1 = channel1();
    let mut rx2 = channel2();

    loop {
        select! {
            msg = rx1.recv() => {
                if let Some(msg) = msg {
                    handle_channel1(msg).await;
                } else {
                    break;
                }
            }
            msg = rx2.recv() => {
                if let Some(msg) = msg {
                    handle_channel2(msg).await;
                } else {
                    break;
                }
            }
            _ = tokio::time::sleep(Duration::from_secs(60)) => {
                check_timeout().await;
            }
        }
    }
}
```

## Cancellation Token Pattern

Use `tokio_util::sync::CancellationToken` for cooperative cancellation:

```rust
use tokio_util::sync::CancellationToken;

pub async fn worker(token: CancellationToken) {
    loop {
        tokio::select! {
            _ = token.cancelled() => {
                // Cleanup
                break;
            }
            _ = do_work() => {
                // Continue
            }
        }
    }
}

// Hierarchical cancellation
let parent_token = CancellationToken::new();
let child_token = parent_token.child_token();

tokio::spawn(worker(child_token));

// Cancel all
parent_token.cancel();
```

## Best Practices

1. **Use semaphores** for limiting concurrent operations
2. **Implement graceful shutdown** in all long-running tasks
3. **Add timeouts** to external operations
4. **Use channels** for inter-task communication
5. **Handle cancellation** properly in all tasks
6. **Clean up resources** in Drop or explicit shutdown methods
7. **Use appropriate channel types** for different patterns
8. **Implement retries** for transient failures
9. **Use select!** for coordinating multiple async operations
10. **Document lifetime** and ownership patterns clearly
