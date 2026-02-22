---
name: rust-expert
description: Rust programming expert including ownership, borrowing, lifetimes, async Tokio patterns, error handling, trait system, performance optimization, testing, and production systems development
version: 2.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash, Grep, Glob]
verified: true
lastVerifiedAt: 2026-02-19T00:00:00.000Z
---

# Rust Expert

Apply idiomatic Rust patterns with strong safety, performance, and maintainability guarantees.

## Core Principles

- Model correctness through the type system; make invalid states unrepresentable.
- Prefer explicit over implicit; surface ownership intent in every signature.
- Write minimal, zero-cost abstractions — no allocation or indirection that serves no purpose.
- Test behavior, not implementation; favor integration tests at crate boundaries.

---

## 1. Ownership, Borrowing, and Lifetimes

### Ownership Patterns

```rust
// Prefer moves when value is consumed; prefer borrows when value is shared.
fn process(data: Vec<u8>) -> Vec<u8> { /* consumes */ }
fn inspect(data: &[u8]) -> usize { data.len() /* borrows */ }

// Clone only when necessary and explicitly documented.
// Anti-pattern: clone() to silence borrow checker errors — fix the design instead.
```

### Borrowing Rules (enforce at design time)

- Only one mutable reference OR any number of immutable references at a time.
- References must not outlive the value they point to.
- Use `Cow<'a, T>` when you need borrow-or-own semantics without forcing allocation.

```rust
use std::borrow::Cow;

fn normalize(s: &str) -> Cow<str> {
    if s.contains(' ') {
        Cow::Owned(s.replace(' ', "_"))
    } else {
        Cow::Borrowed(s)
    }
}
```

### Lifetime Patterns

```rust
// Explicit lifetime annotation: only when compiler cannot infer.
struct Parser<'input> {
    source: &'input str,
    pos: usize,
}

impl<'input> Parser<'input> {
    fn next_token(&mut self) -> &'input str {
        // Returns a slice of the original input — lifetime ties result to source.
        &self.source[self.pos..]
    }
}

// RPIT (Return Position Impl Trait) avoids lifetime noise in many cases.
fn words(s: &str) -> impl Iterator<Item = &str> {
    s.split_whitespace()
}
```

### Anti-Patterns to Avoid

- `clone()` inside hot loops to avoid borrow checker.
- `unsafe` to bypass lifetime checks — redesign instead.
- `'static` bounds that force heap allocation when borrowing suffices.
- Storing `&mut T` in structs — prefer owned data or `RefCell<T>`.

---

## 2. Error Handling

### Decision Matrix

| Scenario                    | Tool                              |
| --------------------------- | --------------------------------- |
| Library crate errors        | `thiserror` — typed, composable   |
| Application / binary errors | `anyhow` — ergonomic `?` chaining |
| Domain-specific context     | Custom enum via `thiserror`       |
| Infallible conversions      | `From` / `Into` — zero overhead   |

### thiserror (Library Crates)

```rust
use thiserror::Error;

#[derive(Debug, Error)]
pub enum ConfigError {
    #[error("missing required field: {field}")]
    MissingField { field: &'static str },
    #[error("invalid value for {field}: {source}")]
    ParseError { field: &'static str, #[source] source: std::num::ParseIntError },
    #[error(transparent)]
    Io(#[from] std::io::Error),
}
```

### anyhow (Application / Binary)

```rust
use anyhow::{Context, Result};

fn load_config(path: &str) -> Result<Config> {
    let raw = std::fs::read_to_string(path)
        .with_context(|| format!("reading config from {path}"))?;
    toml::from_str(&raw).context("parsing config TOML")
}
```

### Error Propagation Rules

- Never use `.unwrap()` in library code; use `.expect()` only in tests and `main()` where the invariant is self-evident.
- Add `.context()` / `.with_context()` at every error boundary to preserve the call chain.
- Map errors at crate boundaries — do not leak internal error types in public APIs.

---

## 3. Trait System

### Generics vs Trait Objects

```rust
// Prefer generics (monomorphized, zero-cost) when types are known at compile time.
fn serialize<S: Serialize>(value: &S) -> Vec<u8> { /* ... */ }

// Use dyn Trait only when you need heterogeneous collections or runtime dispatch.
fn handlers() -> Vec<Box<dyn EventHandler>> { /* ... */ }
```

### Where Clauses

```rust
// Prefer where clauses for readability when bounds are complex.
fn merge<K, V>(a: HashMap<K, V>, b: HashMap<K, V>) -> HashMap<K, V>
where
    K: Eq + Hash,
    V: Clone,
{ /* ... */ }
```

### Blanket Implementations and Orphan Rules

- Implement standard traits (`Display`, `From`, `Iterator`) for your types.
- Respect the orphan rule: you may only implement a foreign trait for a local type.
- Use the newtype pattern to work around orphan restrictions.

```rust
struct Wrapper(Vec<u8>);

impl fmt::Display for Wrapper {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{:?}", self.0)
    }
}
```

### Rust 1.75+ Async in Traits (RPITIT)

```rust
// Stable as of Rust 1.75 — no more async-trait macro needed.
trait DataSource {
    async fn fetch(&self, id: u64) -> anyhow::Result<Record>;
}

// Return-Position Impl Trait in Traits (RPITIT) — also stable in 1.75.
trait Transformer {
    fn transform(&self, input: &str) -> impl Iterator<Item = String>;
}
```

---

## 4. Async / Await with Tokio

### Tokio Runtime Setup

```rust
#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // Default: multi-thread runtime (all CPU cores).
    Ok(())
}

// Single-thread runtime for I/O-only workloads.
#[tokio::main(flavor = "current_thread")]
async fn main() -> anyhow::Result<()> { Ok(()) }
```

### Task Spawning

```rust
use tokio::task;

// Spawn a non-blocking async task.
let handle = task::spawn(async move {
    fetch_data(url).await
});
let result = handle.await?; // propagate JoinError

// CPU-bound work must go to the blocking thread pool — never block the async runtime.
let result = task::spawn_blocking(|| {
    expensive_cpu_computation()
}).await?;
```

### Channels

```rust
use tokio::sync::{mpsc, oneshot, broadcast, watch};

// mpsc: producer → consumer pipeline.
let (tx, mut rx) = mpsc::channel::<Bytes>(1024);

// oneshot: request / response pattern.
let (resp_tx, resp_rx) = oneshot::channel::<Result<Record>>();

// broadcast: fan-out to multiple subscribers.
let (tx, _rx) = broadcast::channel::<Event>(16);

// watch: latest-value semantics (config reload, health state).
let (tx, rx) = watch::channel(Config::default());
```

### select! and Cancellation

```rust
use tokio::select;
use tokio_util::sync::CancellationToken;

async fn worker(token: CancellationToken) {
    select! {
        _ = token.cancelled() => {
            // Structured cancellation — always handle shutdown path.
        }
        result = do_work() => {
            // Normal completion.
        }
    }
}
```

### Structured Concurrency

```rust
use tokio::task::JoinSet;

async fn fetch_all(urls: Vec<String>) -> Vec<anyhow::Result<Bytes>> {
    let mut set = JoinSet::new();
    for url in urls {
        set.spawn(fetch(url));
    }
    let mut results = Vec::new();
    while let Some(res) = set.join_next().await {
        results.push(res.expect("task panicked"));
    }
    results
}
```

### Async Anti-Patterns

- `std::thread::sleep` inside async context — use `tokio::time::sleep`.
- Holding `MutexGuard` across `.await` — use `tokio::sync::Mutex` instead.
- Blocking I/O (file read, DNS) on async thread — use `spawn_blocking` or `tokio::fs`.
- Unbounded channels — always set a capacity bound.

---

## 5. Common Crates

### serde — Serialization

```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct User {
    pub id: u64,
    pub display_name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub email: Option<String>,
}
```

### axum — HTTP Servers

```rust
use axum::{extract::{Path, State}, routing::get, Json, Router};

async fn get_user(
    State(db): State<DbPool>,
    Path(id): Path<u64>,
) -> Result<Json<User>, AppError> {
    let user = db.find_user(id).await?;
    Ok(Json(user))
}

let app = Router::new()
    .route("/users/:id", get(get_user))
    .with_state(db_pool);
```

### sqlx — Async Database

```rust
use sqlx::PgPool;

async fn insert_user(pool: &PgPool, name: &str) -> sqlx::Result<i64> {
    let row = sqlx::query!("INSERT INTO users (name) VALUES ($1) RETURNING id", name)
        .fetch_one(pool)
        .await?;
    Ok(row.id)
}
```

### reqwest — HTTP Client

```rust
use reqwest::Client;

async fn fetch_json<T: for<'de> serde::Deserialize<'de>>(
    client: &Client,
    url: &str,
) -> anyhow::Result<T> {
    Ok(client.get(url).send().await?.error_for_status()?.json().await?)
}
```

### rayon — Data Parallelism

```rust
use rayon::prelude::*;

fn parallel_sum(data: &[f64]) -> f64 {
    data.par_iter().sum()
}
```

### clap — CLI

```rust
use clap::Parser;

#[derive(Parser, Debug)]
#[command(version, about)]
struct Args {
    #[arg(short, long, default_value = "8080")]
    port: u16,

    #[arg(short, long, env = "CONFIG_PATH")]
    config: std::path::PathBuf,
}
```

---

## 6. Performance Optimization

### Zero-Cost Abstractions

- Prefer iterators over manual index loops — they compile to identical machine code.
- Use `#[inline]` for hot, small functions that cross crate boundaries.
- Prefer stack allocation; move to heap (`Box`, `Vec`, `Arc`) only when necessary.

### SIMD

```rust
// Use std::simd (nightly) or portable-simd crate for explicit vectorization.
// Profile first — LLVM auto-vectorizes most iterator chains.
use std::simd::{f32x8, SimdFloat};

fn dot_product_simd(a: &[f32], b: &[f32]) -> f32 {
    a.chunks_exact(8)
        .zip(b.chunks_exact(8))
        .map(|(a_chunk, b_chunk)| {
            let va = f32x8::from_slice(a_chunk);
            let vb = f32x8::from_slice(b_chunk);
            (va * vb).reduce_sum()
        })
        .sum()
}
```

### Profiling

```bash
# flamegraph (install: cargo install flamegraph)
cargo flamegraph --bin my-app

# perf stat for CPU counters (Linux)
perf stat cargo run --release

# heaptrack for heap allocation analysis (Linux)
heaptrack cargo run --release

# criterion for micro-benchmarks
cargo bench
```

### Allocation Awareness

```rust
// Preallocate when size is known.
let mut v = Vec::with_capacity(expected_len);

// String building: use write! into a pre-allocated String.
use std::fmt::Write;
let mut s = String::with_capacity(256);
write!(s, "id={}", id)?;

// Avoid format!() in hot paths — prefer direct write!() or push_str().
```

---

## 7. Testing

### Unit Tests

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parse_valid_config() {
        let cfg = Config::from_str("[server]\nport = 9000").unwrap();
        assert_eq!(cfg.port, 9000);
    }

    #[test]
    fn parse_invalid_port_returns_error() {
        let result = Config::from_str("[server]\nport = -1");
        assert!(result.is_err());
    }
}
```

### Integration Tests

```rust
// tests/integration/server.rs — tests the full public API.
#[tokio::test]
async fn health_endpoint_returns_200() {
    let addr = spawn_test_server().await;
    let resp = reqwest::get(format!("http://{addr}/health")).await.unwrap();
    assert_eq!(resp.status(), 200);
}
```

### Property-Based Testing (proptest)

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn encode_decode_roundtrip(data: Vec<u8>) {
        let encoded = encode(&data);
        prop_assert_eq!(decode(&encoded).unwrap(), data);
    }
}
```

### Async Tests

```rust
#[tokio::test]
async fn fetch_returns_data() {
    let mock = MockServer::start().await;
    Mock::given(method("GET")).respond_with(ResponseTemplate::new(200)).mount(&mock).await;
    let result = fetch(&mock.uri()).await;
    assert!(result.is_ok());
}
```

### Test Conventions

- Test one behavior per test function.
- Use descriptive names: `<function>_<scenario>_<expected>`.
- Mock only external I/O boundaries (HTTP, filesystem, database).
- Run `cargo test -- --nocapture` for diagnostic output during development.
- Run `cargo nextest run` for faster parallel test execution in CI.

---

## 8. Unsafe Rust

### When to Use

- FFI boundaries (calling C functions, exporting to C).
- Low-level memory mapping or SIMD intrinsics when safe abstractions cannot reach.
- Performance-critical code where the safe alternative has measurable overhead (proved by profiling).

### Guidelines

```rust
/// # Safety
///
/// - `ptr` must be non-null and properly aligned for `T`.
/// - The memory at `ptr` must be valid for `len` elements of type `T`.
/// - The caller must ensure no other mutable references to the memory exist.
pub unsafe fn from_raw_parts<T>(ptr: *const T, len: usize) -> &'static [T] {
    std::slice::from_raw_parts(ptr, len)
}
```

- Every `unsafe` block must have a `// SAFETY:` comment explaining why it is sound.
- Minimize the scope of `unsafe` — wrap in a safe abstraction immediately.
- Prefer `unsafe` fn over `unsafe` block inside a safe fn when the entire function is unsafe.
- Use Miri (`cargo +nightly miri test`) to detect undefined behavior in unsafe code.

---

## 9. FFI and Interop

### Exporting to C

```rust
#[no_mangle]
pub extern "C" fn my_add(a: i32, b: i32) -> i32 {
    a + b
}
```

### Calling C from Rust

```rust
extern "C" {
    fn strlen(s: *const std::os::raw::c_char) -> usize;
}

fn rust_strlen(s: &str) -> usize {
    let cstr = std::ffi::CString::new(s).expect("no null bytes");
    // SAFETY: cstr is a valid, null-terminated C string.
    unsafe { strlen(cstr.as_ptr()) }
}
```

### cbindgen / bindgen

- Use `cbindgen` to generate C headers from Rust public API.
- Use `bindgen` to generate Rust bindings from C headers.
- Always run through CI to detect API drift.

---

## 10. Build System

### Cargo Workspaces

```toml
# Cargo.toml (workspace root)
[workspace]
members = ["crates/core", "crates/server", "crates/cli"]
resolver = "2"

[workspace.dependencies]
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }

# crates/core/Cargo.toml
[dependencies]
tokio.workspace = true
serde.workspace = true
```

### Feature Flags

```toml
[features]
default = ["std"]
std = []
async = ["dep:tokio"]
metrics = ["dep:prometheus"]

[dependencies]
tokio = { version = "1", optional = true }
prometheus = { version = "0.13", optional = true }
```

```rust
#[cfg(feature = "metrics")]
fn record_latency(ms: u64) { /* ... */ }

#[cfg(not(feature = "metrics"))]
fn record_latency(_ms: u64) {}
```

### Build Scripts

```rust
// build.rs — runs before crate compilation.
fn main() {
    // Rerun when proto files change.
    println!("cargo:rerun-if-changed=proto/");
    // Link a system library.
    println!("cargo:rustc-link-lib=ssl");
}
```

### Useful Cargo Commands

```bash
cargo build --release          # optimized build
cargo clippy -- -D warnings    # lint (treat warnings as errors)
cargo fmt --check              # format check (CI)
cargo doc --no-deps --open     # generate and open docs
cargo audit                    # check dependencies for CVEs
cargo deny check               # license + advisory checks
cargo expand                   # show macro expansion
```

---

## 11. Rust 1.75+ Features

### Async fn in Traits (Stable 1.75)

```rust
// No longer requires #[async_trait] crate.
trait Fetcher {
    async fn fetch(&self, url: &str) -> anyhow::Result<Bytes>;
}
```

### RPITIT — Return-Position Impl Trait in Traits (Stable 1.75)

```rust
trait Source {
    fn items(&self) -> impl Iterator<Item = &str>;
}
```

### let-else (Stable 1.65)

```rust
let Ok(value) = parse_value(raw) else {
    return Err(ConfigError::InvalidValue);
};
```

### std::io::ErrorKind — richer variants (ongoing)

```rust
use std::io::ErrorKind;
match err.kind() {
    ErrorKind::NotFound => { /* ... */ }
    ErrorKind::PermissionDenied => { /* ... */ }
    _ => { /* ... */ }
}
```

---

## 12. Code Quality Checklist

Before marking Rust work complete:

- [ ] `cargo clippy -- -D warnings` passes with zero warnings.
- [ ] `cargo fmt --check` produces no changes.
- [ ] `cargo test` (or `cargo nextest run`) passes — all tests green.
- [ ] All `unsafe` blocks have `// SAFETY:` comments.
- [ ] Public API items have `///` doc comments.
- [ ] No `.unwrap()` in library code except tests.
- [ ] Error types derive `Debug` + implement `std::error::Error`.
- [ ] Async code does not block the executor thread.
- [ ] Performance-critical paths benchmarked before and after changes.

---

## Assigned Agents

This skill is used by:

- `developer` — Rust feature implementation and bug fixes
- `code-reviewer` — Rust-specific code review patterns
- `qa` — Rust testing strategies (proptest, criterion, nextest)

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New Rust pattern discovered -> `.claude/context/memory/learnings.md`
- Rust-specific issue or gotcha -> `.claude/context/memory/issues.md`
- Architecture or crate selection decision -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
