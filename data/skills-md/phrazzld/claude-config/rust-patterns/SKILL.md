---
name: rust-patterns
description: |
  Idiomatic Rust patterns for ownership, errors, traits, and configuration. Use when:
  - Writing or reviewing Rust code
  - Designing error handling with Result and thiserror
  - Implementing traits and composition patterns
  - Working with ownership and borrowing
  - Configuring Cargo features
  Keywords: Rust, ownership, borrowing, Result, thiserror, anyhow, trait,
  lifetimes, Cargo features, unsafe
---

# Rust Patterns

Ownership-first, zero-cost abstractions, no hidden complexity.

## Error Handling

**Always use `Result<T, E>`. Never panic for expected failures:**
```rust
// Use thiserror for library error types
#[derive(Debug, thiserror::Error)]
pub enum UserError {
    #[error("user not found: {0}")]
    NotFound(String),
    #[error("invalid email format")]
    InvalidEmail,
    #[error("database error: {0}")]
    Database(#[from] sqlx::Error),
}

// Use anyhow for applications (context chaining)
fn fetch_user(id: &str) -> anyhow::Result<User> {
    let user = db.get(id)
        .context("fetching user from database")?;
    Ok(user)
}
```

**Propagate with `?`, add context at boundaries.**

## Ownership Patterns

**Borrowing > Cloning:**
```rust
// Good: Borrow for read-only
fn process(items: &[Item]) -> usize { ... }

// Good: Take ownership when storing/transforming
fn consume(items: Vec<Item>) -> Output { ... }

// Avoid: Excessive cloning
fn bad(items: &Vec<Item>) {
    let copy = items.clone(); // Usually unnecessary
}
```

**Fight the borrow checker → redesign, don't circumvent.**

## Trait Design

**Small, focused traits (1-3 methods):**
```rust
trait Readable {
    type Item;
    fn read(&self) -> Self::Item;
}

trait Writable {
    type Item;
    fn write(&mut self, item: Self::Item);
}

// Compose through bounds
fn copy<R, W>(src: &R, dst: &mut W)
where
    R: Readable<Item = Vec<u8>>,
    W: Writable<Item = Vec<u8>>,
{ ... }
```

**Consumer-side interfaces. Static dispatch by default.**

## Configuration

**Cargo features for compile-time options:**
```toml
[features]
default = ["json"]
json = ["serde_json"]
database = ["sqlx"]
full = ["json", "database"]
```

```rust
#[cfg(feature = "json")]
pub mod json_support { ... }
```

## Unsafe

**Minimize. Document with `// SAFETY:` comments:**
```rust
// SAFETY: We verified ptr is non-null and properly aligned
// in the caller's bounds check above
unsafe { *ptr }
```

Abstract behind safe interfaces.

## Anti-Patterns

- `unwrap()` / `expect()` for recoverable errors
- `Result<T, String>` (use typed errors)
- Excessive `Rc<RefCell<T>>` (redesign ownership)
- Monolithic traits (10+ methods)
- Reflection instead of generics
- Fighting borrow checker with unsafe
