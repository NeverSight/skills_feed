---
name: async-programming
description: Master Rust async/await with Tokio
sasmp_version: "1.3.0"
bonded_agent: rust-async-agent
bond_type: PRIMARY_BOND
version: "1.0.0"
---

# Async Programming Skill

Master Rust's asynchronous programming with async/await and Tokio.

## Quick Start

### Basic Setup

```toml
# Cargo.toml
[dependencies]
tokio = { version = "1", features = ["full"] }
```

```rust
use tokio;

#[tokio::main]
async fn main() {
    let result = fetch_data().await;
    println!("{:?}", result);
}

async fn fetch_data() -> String {
    // Async operation
    tokio::time::sleep(tokio::time::Duration::from_secs(1)).await;
    "Data fetched".to_string()
}
```

### Spawning Tasks

```rust
use tokio;

#[tokio::main]
async fn main() {
    // Spawn concurrent task
    let handle = tokio::spawn(async {
        expensive_operation().await
    });

    // Do other work...

    // Wait for result
    let result = handle.await.unwrap();
}
```

### Concurrent Execution

```rust
// Run multiple futures concurrently
let (r1, r2, r3) = tokio::join!(
    fetch_user(1),
    fetch_user(2),
    fetch_user(3),
);

// Race futures - first to complete wins
tokio::select! {
    result = operation_a() => println!("A: {:?}", result),
    result = operation_b() => println!("B: {:?}", result),
}
```

## Common Patterns

### Timeout

```rust
use tokio::time::{timeout, Duration};

match timeout(Duration::from_secs(5), slow_operation()).await {
    Ok(result) => println!("Completed: {:?}", result),
    Err(_) => println!("Timed out"),
}
```

### Channels

```rust
use tokio::sync::mpsc;

let (tx, mut rx) = mpsc::channel(32);

tokio::spawn(async move {
    tx.send("message").await.unwrap();
});

while let Some(msg) = rx.recv().await {
    println!("Got: {}", msg);
}
```

### Mutex

```rust
use std::sync::Arc;
use tokio::sync::Mutex;

let data = Arc::new(Mutex::new(0));
let data_clone = Arc::clone(&data);

tokio::spawn(async move {
    let mut lock = data_clone.lock().await;
    *lock += 1;
});
```

## HTTP Client Example

```rust
use reqwest;

#[tokio::main]
async fn main() -> Result<(), reqwest::Error> {
    let response = reqwest::get("https://api.example.com/data")
        .await?
        .json::<serde_json::Value>()
        .await?;

    println!("{:?}", response);
    Ok(())
}
```

## Resources

- [Tokio Tutorial](https://tokio.rs/tokio/tutorial)
- [Async Book](https://rust-lang.github.io/async-book/)
