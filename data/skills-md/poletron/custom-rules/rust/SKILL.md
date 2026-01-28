---
name: rust
description: >
  Rust best practices, ownership, borrowing, and async patterns.
  Trigger: When writing Rust code with memory safety patterns.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with rust"

## When to Use

Use this skill when:
- Writing Rust applications
- Managing ownership and borrowing
- Implementing async patterns
- Handling errors with Result/Option

---

## Critical Patterns

### Error Handling (REQUIRED)

```rust
// ✅ ALWAYS: Use Result with ? operator
fn read_config(path: &str) -> Result<Config, ConfigError> {
    let content = std::fs::read_to_string(path)?;
    let config: Config = serde_json::from_str(&content)?;
    Ok(config)
}

// ❌ NEVER: Use unwrap in production
let config = std::fs::read_to_string(path).unwrap();
```

### Ownership Patterns (REQUIRED)

```rust
// ✅ ALWAYS: Prefer borrowing over ownership transfer
fn process(data: &[u8]) -> Result<(), Error> { ... }

// ✅ Use Clone only when necessary
fn take_ownership(data: Vec<u8>) -> Vec<u8> { ... }

// ❌ NEVER: Unnecessary cloning
process(data.clone());  // If borrow works, use it
```

### Option Handling (REQUIRED)

```rust
// ✅ ALWAYS: Pattern match or use combinators
let name = user.name.as_ref().unwrap_or(&default_name);

// ✅ Use if let for single variant
if let Some(name) = user.name {
    println!("Hello, {}", name);
}

// ❌ NEVER: Blind unwrap
let name = user.name.unwrap();
```

---

## Decision Tree

```
Need to modify data?       → Use &mut reference
Need to read data?         → Use & reference
Need to transfer?          → Move ownership
Need cleanup?              → Implement Drop trait
Need async?                → Use tokio or async-std
Need error context?        → Use anyhow or thiserror
```

---

## Code Examples

### Struct with Lifetimes

```rust
struct Parser<'a> {
    input: &'a str,
    position: usize,
}

impl<'a> Parser<'a> {
    fn new(input: &'a str) -> Self {
        Self { input, position: 0 }
    }
}
```

### Async with Tokio

```rust
use tokio;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let response = reqwest::get("https://api.example.com/data")
        .await?
        .json::<Response>()
        .await?;
    
    Ok(())
}
```

---

## Commands

```bash
cargo new myapp              # Create new project
cargo build --release        # Build optimized
cargo run                    # Build and run
cargo test                   # Run tests
cargo clippy                 # Linting
cargo fmt                    # Format code
```

---

## Resources

- **Ownership & Borrowing**: [ownership-borrowing.md](ownership-borrowing.md)
- **Async Programming**: [async-programming.md](async-programming.md)
- **Best Practices**: [best-practices.md](best-practices.md)
