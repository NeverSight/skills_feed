---
name: tokio-troubleshooting
description: Debugging and troubleshooting Tokio applications using tokio-console, detecting deadlocks, memory leaks, and performance issues. Use when diagnosing async runtime problems.
---

# Tokio Troubleshooting

This skill provides techniques for debugging and troubleshooting async applications built with Tokio.

## Using tokio-console for Runtime Inspection

Monitor async runtime in real-time:

```rust
// In Cargo.toml
[dependencies]
console-subscriber = "0.2"

// In main.rs
fn main() {
    console_subscriber::init();

    tokio::runtime::Builder::new_multi_thread()
        .enable_all()
        .build()
        .unwrap()
        .block_on(async {
            run_application().await
        });
}
```

**Run console in separate terminal:**
```bash
tokio-console
```

**Key metrics to monitor:**
- Task spawn rate and total tasks
- Poll duration per task
- Idle vs. busy time
- Waker operations
- Resource utilization

**Identifying issues:**
- Long poll durations: CPU-intensive work in async context
- Many wakers: Potential contention or inefficient polling
- Growing task count: Task leak or unbounded spawning
- High idle time: Not enough work or blocking operations

## Debugging Deadlocks and Hangs

Detect and resolve deadlock situations:

### Common Deadlock Pattern

```rust
// BAD: Potential deadlock
async fn deadlock_example() {
    let mutex1 = Arc::new(Mutex::new(()));
    let mutex2 = Arc::new(Mutex::new(()));

    let m1 = mutex1.clone();
    let m2 = mutex2.clone();
    tokio::spawn(async move {
        let _g1 = m1.lock().await;
        tokio::time::sleep(Duration::from_millis(10)).await;
        let _g2 = m2.lock().await; // May deadlock
    });

    let _g2 = mutex2.lock().await;
    tokio::time::sleep(Duration::from_millis(10)).await;
    let _g1 = mutex1.lock().await; // May deadlock
}

// GOOD: Consistent lock ordering
async fn no_deadlock_example() {
    let mutex1 = Arc::new(Mutex::new(()));
    let mutex2 = Arc::new(Mutex::new(()));

    // Always acquire locks in same order
    let _g1 = mutex1.lock().await;
    let _g2 = mutex2.lock().await;
}

// BETTER: Avoid nested locks
async fn best_example() {
    // Use message passing instead
    let (tx, mut rx) = mpsc::channel(10);

    tokio::spawn(async move {
        while let Some(msg) = rx.recv().await {
            process_message(msg).await;
        }
    });

    tx.send(message).await.unwrap();
}
```

### Detecting Hangs with Timeouts

```rust
use tokio::time::{timeout, Duration};

async fn detect_hang() {
    match timeout(Duration::from_secs(5), potentially_hanging_operation()).await {
        Ok(result) => println!("Completed: {:?}", result),
        Err(_) => {
            eprintln!("Operation timed out - potential hang detected");
            // Log stack traces, metrics, etc.
        }
    }
}
```

### Deadlock Detection with try_lock

```rust
use tokio::sync::Mutex;

async fn try_with_timeout(mutex: &Mutex<State>) -> Option<State> {
    for _ in 0..10 {
        if let Ok(guard) = mutex.try_lock() {
            return Some(guard.clone());
        }
        tokio::time::sleep(Duration::from_millis(10)).await;
    }
    eprintln!("Failed to acquire lock - possible deadlock");
    None
}
```

## Memory Leak Detection

Identify and fix memory leaks:

### Task Leaks

```rust
// BAD: Tasks never complete
async fn leaking_tasks() {
    loop {
        tokio::spawn(async {
            loop {
                // Never exits
                tokio::time::sleep(Duration::from_secs(1)).await;
            }
        });
    }
}

// GOOD: Tasks have exit condition
async fn proper_tasks(shutdown: broadcast::Receiver<()>) {
    loop {
        let mut shutdown_rx = shutdown.resubscribe();
        tokio::spawn(async move {
            loop {
                tokio::select! {
                    _ = shutdown_rx.recv() => break,
                    _ = tokio::time::sleep(Duration::from_secs(1)) => {
                        // Work
                    }
                }
            }
        });
    }
}
```

### Arc Cycles

```rust
// BAD: Reference cycle
struct Node {
    next: Option<Arc<Mutex<Node>>>,
    prev: Option<Arc<Mutex<Node>>>, // Creates cycle!
}

// GOOD: Use weak references
use std::sync::Weak;

struct Node {
    next: Option<Arc<Mutex<Node>>>,
    prev: Option<Weak<Mutex<Node>>>, // Weak reference breaks cycle
}
```

### Monitoring Memory Usage

```rust
use sysinfo::{System, SystemExt};

pub async fn memory_monitor() {
    let mut system = System::new_all();
    let mut interval = tokio::time::interval(Duration::from_secs(60));

    loop {
        interval.tick().await;
        system.refresh_memory();

        let used = system.used_memory();
        let total = system.total_memory();
        let percent = (used as f64 / total as f64) * 100.0;

        tracing::info!(
            used_mb = used / 1024 / 1024,
            total_mb = total / 1024 / 1024,
            percent = %.2 percent,
            "Memory usage"
        );

        if percent > 80.0 {
            tracing::warn!("High memory usage detected");
        }
    }
}
```

## Performance Profiling with Tracing

Instrument code for performance analysis:

```rust
use tracing::{info, instrument, span, Level};

#[instrument]
async fn process_request(id: u64) -> Result<Response, Error> {
    let span = span!(Level::INFO, "database_query");
    let _enter = span.enter();

    let data = fetch_from_database(id).await?;

    drop(_enter);

    let span = span!(Level::INFO, "transformation");
    let _enter = span.enter();

    let result = transform_data(data).await?;

    Ok(Response { result })
}

// Configure subscriber for flame graphs
use tracing_subscriber::layer::SubscriberExt;

fn init_tracing() {
    let fmt_layer = tracing_subscriber::fmt::layer();
    let filter_layer = tracing_subscriber::EnvFilter::from_default_env();

    tracing_subscriber::registry()
        .with(filter_layer)
        .with(fmt_layer)
        .init();
}
```

## Understanding Panic Messages

Common async panic patterns:

### Panics in Spawned Tasks

```rust
// Panic is isolated to the task
tokio::spawn(async {
    panic!("This won't crash the program");
});

// To catch panics
let handle = tokio::spawn(async {
    // Work that might panic
});

match handle.await {
    Ok(result) => println!("Success: {:?}", result),
    Err(e) if e.is_panic() => {
        eprintln!("Task panicked: {:?}", e);
        // Handle panic
    }
    Err(e) => eprintln!("Task cancelled: {:?}", e),
}
```

### Send + 'static Errors

```rust
// ERROR: future cannot be sent between threads
async fn bad_example() {
    let rc = Rc::new(5); // Rc is !Send
    tokio::spawn(async move {
        println!("{}", rc); // Error!
    });
}

// FIX: Use Arc instead
async fn good_example() {
    let rc = Arc::new(5); // Arc is Send
    tokio::spawn(async move {
        println!("{}", rc); // OK
    });
}

// ERROR: borrowed value does not live long enough
async fn lifetime_error() {
    let data = String::from("hello");
    tokio::spawn(async {
        println!("{}", data); // Error: data might not live long enough
    });
}

// FIX: Move ownership
async fn lifetime_fixed() {
    let data = String::from("hello");
    tokio::spawn(async move {
        println!("{}", data); // OK: data is moved
    });
}
```

## Common Error Patterns and Solutions

### Blocking in Async Context

```rust
// PROBLEM: Detected with tokio-console (long poll time)
async fn blocking_example() {
    std::thread::sleep(Duration::from_secs(1)); // Blocks thread!
}

// SOLUTION
async fn non_blocking_example() {
    tokio::time::sleep(Duration::from_secs(1)).await; // Yields control
}

// For unavoidable blocking
async fn necessary_blocking() {
    tokio::task::spawn_blocking(|| {
        expensive_cpu_work()
    }).await.unwrap();
}
```

### Channel Closed Errors

```rust
// PROBLEM: SendError because receiver dropped
async fn send_error_example() {
    let (tx, rx) = mpsc::channel(10);
    drop(rx); // Receiver dropped

    match tx.send(42).await {
        Ok(_) => println!("Sent"),
        Err(e) => eprintln!("Send failed: {}", e), // Channel closed
    }
}

// SOLUTION: Check if receiver exists
async fn handle_closed_channel() {
    let (tx, rx) = mpsc::channel(10);

    tokio::spawn(async move {
        // Receiver keeps channel open
        while let Some(msg) = rx.recv().await {
            process(msg).await;
        }
    });

    // Or handle the error
    if let Err(e) = tx.send(42).await {
        tracing::warn!("Channel closed: {}", e);
        // Cleanup or alternative action
    }
}
```

### Task Cancellation

```rust
// PROBLEM: Task cancelled unexpectedly
let handle = tokio::spawn(async {
    // Long-running work
});

handle.abort(); // Cancels task

// SOLUTION: Handle cancellation gracefully
let handle = tokio::spawn(async {
    let result = tokio::select! {
        result = do_work() => result,
        _ = tokio::signal::ctrl_c() => {
            cleanup().await;
            return Err(Error::Cancelled);
        }
    };
    result
});
```

## Testing Async Code Effectively

Write reliable async tests:

```rust
#[tokio::test]
async fn test_with_timeout() {
    tokio::time::timeout(
        Duration::from_secs(5),
        async {
            let result = my_async_function().await;
            assert!(result.is_ok());
        }
    )
    .await
    .expect("Test timed out");
}

#[tokio::test]
async fn test_concurrent_access() {
    let shared = Arc::new(Mutex::new(0));

    let handles: Vec<_> = (0..10)
        .map(|_| {
            let shared = shared.clone();
            tokio::spawn(async move {
                let mut lock = shared.lock().await;
                *lock += 1;
            })
        })
        .collect();

    for handle in handles {
        handle.await.unwrap();
    }

    assert_eq!(*shared.lock().await, 10);
}

// Test with mocked time
#[tokio::test(start_paused = true)]
async fn test_with_time_control() {
    let start = tokio::time::Instant::now();

    tokio::time::sleep(Duration::from_secs(100)).await;

    // Time is mocked, so this completes instantly
    assert!(start.elapsed() < Duration::from_secs(1));
}
```

## Debugging Checklist

When troubleshooting async issues:

- [ ] Use tokio-console to monitor runtime behavior
- [ ] Check for blocking operations with tracing
- [ ] Verify all locks are released properly
- [ ] Look for task leaks (growing task count)
- [ ] Monitor memory usage over time
- [ ] Add timeouts to detect hangs
- [ ] Check for channel closure errors
- [ ] Verify Send + 'static bounds are satisfied
- [ ] Use try_lock to detect potential deadlocks
- [ ] Profile with tracing for performance bottlenecks
- [ ] Test with tokio-test for time-based code
- [ ] Check for Arc cycles with weak references

## Helpful Tools

- **tokio-console**: Real-time async runtime monitoring
- **tracing**: Structured logging and profiling
- **cargo-flamegraph**: Generate flame graphs
- **valgrind/heaptrack**: Memory profiling
- **perf**: CPU profiling on Linux
- **Instruments**: Profiling on macOS

## Best Practices

1. **Always use tokio-console** in development
2. **Add tracing spans** to critical code paths
3. **Use timeouts** liberally to detect hangs
4. **Monitor task count** for leaks
5. **Profile before optimizing** - measure first
6. **Test with real concurrency** - don't just test happy paths
7. **Handle cancellation** gracefully in all tasks
8. **Use structured logging** for debugging
9. **Avoid nested locks** - prefer message passing
10. **Document lock ordering** when necessary
