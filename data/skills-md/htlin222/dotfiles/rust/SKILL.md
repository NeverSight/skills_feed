---
name: rust
description: Write idiomatic Rust with ownership, lifetimes, and traits. Use for Rust development, memory safety, or systems programming.
---

# Rust Development

Write safe, performant Rust code.

## When to Use

- Writing Rust code
- Ownership and lifetime issues
- Trait implementations
- Async Rust
- FFI and unsafe code

## Ownership Patterns

### Borrowing

```rust
// Immutable borrow
fn print_length(s: &str) {
    println!("Length: {}", s.len());
}

// Mutable borrow
fn append_greeting(s: &mut String) {
    s.push_str(", world!");
}

// Ownership transfer
fn consume(s: String) -> String {
    format!("Consumed: {}", s)
}
```

### Lifetimes

```rust
// Explicit lifetime annotation
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// Struct with lifetime
struct Parser<'a> {
    input: &'a str,
    position: usize,
}
```

## Error Handling

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),

    #[error("Parse error at line {line}")]
    Parse { line: usize },

    #[error("Not found: {0}")]
    NotFound(String),
}

// Using Result
fn read_config(path: &Path) -> Result<Config, AppError> {
    let content = std::fs::read_to_string(path)?;
    parse_config(&content).map_err(|e| AppError::Parse { line: e.line })
}
```

## Traits

```rust
// Define trait
trait Summary {
    fn summarize(&self) -> String;

    // Default implementation
    fn preview(&self) -> String {
        format!("{}...", &self.summarize()[..50])
    }
}

// Implement for type
impl Summary for Article {
    fn summarize(&self) -> String {
        format!("{} by {}", self.title, self.author)
    }
}

// Generic with trait bounds
fn notify<T: Summary + Display>(item: &T) {
    println!("Breaking: {}", item.summarize());
}
```

## Async

```rust
use tokio;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let response = fetch_data().await?;
    process(response).await
}

async fn fetch_data() -> Result<Data, Error> {
    let client = reqwest::Client::new();
    let resp = client.get(URL).send().await?.json().await?;
    Ok(resp)
}
```

## Testing

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_valid() {
        let result = parse("valid input");
        assert!(result.is_ok());
        assert_eq!(result.unwrap(), expected);
    }

    #[test]
    #[should_panic(expected = "empty input")]
    fn test_parse_empty() {
        parse("");
    }
}
```

## Examples

**Input:** "Fix lifetime error"
**Action:** Analyze borrow checker message, adjust lifetimes or ownership

**Input:** "Make this async"
**Action:** Add async/await, use tokio runtime, handle async errors
