---
name: error-handling
description: Master Rust's Result, Option, and error handling patterns
sasmp_version: "1.3.0"
bonded_agent: rust-fundamentals-agent
bond_type: SECONDARY_BOND
version: "1.0.0"
---

# Error Handling Skill

Master Rust's explicit, type-safe error handling with Result and Option.

## Quick Start

### Option<T> - For Absent Values

```rust
fn find_user(id: u32) -> Option<User> {
    if id == 0 {
        None
    } else {
        Some(User { id, name: "Alice".into() })
    }
}

// Handling Option
match find_user(1) {
    Some(user) => println!("Found: {}", user.name),
    None => println!("User not found"),
}

// Or with if let
if let Some(user) = find_user(1) {
    println!("Found: {}", user.name);
}
```

### Result<T, E> - For Recoverable Errors

```rust
use std::fs::File;
use std::io::{self, Read};

fn read_file(path: &str) -> Result<String, io::Error> {
    let mut file = File::open(path)?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    Ok(contents)
}

// Handling Result
match read_file("data.txt") {
    Ok(contents) => println!("{}", contents),
    Err(e) => eprintln!("Error: {}", e),
}
```

### The ? Operator

```rust
fn process_data(path: &str) -> Result<Data, Error> {
    let contents = read_file(path)?;  // Returns Err if fails
    let parsed = parse(&contents)?;    // Returns Err if fails
    let validated = validate(parsed)?; // Returns Err if fails
    Ok(validated)
}
```

## Common Patterns

### unwrap_or / unwrap_or_else

```rust
// Default value
let name = get_name().unwrap_or("Anonymous".to_string());

// Lazy default (computed only if needed)
let name = get_name().unwrap_or_else(|| generate_default_name());
```

### map / and_then

```rust
// Transform the inner value
let doubled = Some(5).map(|x| x * 2);  // Some(10)

// Chain operations that return Option/Result
let result = get_value()
    .and_then(|v| validate(v))
    .and_then(|v| process(v));
```

### ok_or / ok_or_else

```rust
// Convert Option to Result
let user = find_user(id).ok_or(Error::NotFound)?;

// Lazy error
let user = find_user(id).ok_or_else(|| Error::NotFound(id))?;
```

## Custom Errors with thiserror

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),

    #[error("Parse error at line {line}: {message}")]
    Parse { line: usize, message: String },

    #[error("Not found: {0}")]
    NotFound(String),
}
```

## Application Errors with anyhow

```rust
use anyhow::{Context, Result, bail, ensure};

fn process() -> Result<()> {
    let config = load_config()
        .context("Failed to load configuration")?;

    ensure!(config.is_valid(), "Configuration is invalid");

    if config.debug {
        bail!("Debug mode not allowed in production");
    }

    Ok(())
}
```

## Resources

- [Rust Book Ch.9](https://doc.rust-lang.org/book/ch09-00-error-handling.html)
- [thiserror docs](https://docs.rs/thiserror)
- [anyhow docs](https://docs.rs/anyhow)
