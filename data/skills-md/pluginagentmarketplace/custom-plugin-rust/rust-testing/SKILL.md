---
name: rust-testing
description: Master Rust testing - unit tests, integration tests, mocking, and TDD
sasmp_version: "1.3.0"
bonded_agent: rust-tooling-agent
bond_type: SECONDARY_BOND
version: "1.0.0"
---

# Rust Testing Skill

Master comprehensive testing in Rust: unit tests, integration tests, doc tests, property testing, and mocking.

## Quick Start

### Unit Tests

```rust
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add_positive() {
        assert_eq!(add(2, 3), 5);
    }

    #[test]
    fn test_add_negative() {
        assert_eq!(add(-1, -1), -2);
    }

    #[test]
    #[should_panic(expected = "overflow")]
    fn test_overflow() {
        panic!("overflow");
    }

    #[test]
    #[ignore]
    fn expensive_test() {
        // Run with: cargo test -- --ignored
    }
}
```

### Integration Tests

```rust
// tests/integration_test.rs
use my_crate::public_api;

#[test]
fn test_full_workflow() {
    let result = public_api::process("input");
    assert!(result.is_ok());
}

mod common;  // tests/common/mod.rs

#[test]
fn test_with_setup() {
    let ctx = common::setup();
    // test...
}
```

### Doc Tests

```rust
/// Adds two numbers.
///
/// # Examples
///
/// ```
/// let result = my_lib::add(2, 2);
/// assert_eq!(result, 4);
/// ```
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

## Test Commands

```bash
cargo test                      # All tests
cargo test test_name            # Specific test
cargo test -- --nocapture       # Show output
cargo test -- --ignored         # Ignored tests
cargo test --doc                # Doc tests only
cargo nextest run               # Fast parallel
```

## Common Patterns

### Async Tests

```rust
#[tokio::test]
async fn test_async_operation() {
    let result = async_function().await;
    assert!(result.is_ok());
}
```

### Property Testing

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn test_commutative(a in 0i32..1000, b in 0i32..1000) {
        assert_eq!(add(a, b), add(b, a));
    }
}
```

### Mocking

```rust
use mockall::automock;

#[automock]
trait Database {
    fn get(&self, id: u32) -> Option<String>;
}

#[test]
fn test_with_mock() {
    let mut mock = MockDatabase::new();
    mock.expect_get()
        .returning(|_| Some("data".to_string()));
}
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Test not found | Check module path |
| Async fails | Add `#[tokio::test]` |
| Random failures | Use `--test-threads=1` |

## Resources

- [Rust Book Ch.11](https://doc.rust-lang.org/book/ch11-00-testing.html)
- [proptest](https://docs.rs/proptest)
- [mockall](https://docs.rs/mockall)
