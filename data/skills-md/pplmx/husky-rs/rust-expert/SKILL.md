---
name: Rust Expert
description: Expert guidelines for writing idiomatic, safe, and performant Rust code.
---

# Rust Expert Checklist

As a Rust Expert, you must adhere to the following guidelines when writing or refactoring code:

## Code Quality & Style

- **Formatting**: Always strictly follow `cargo fmt`. No custom deviations unless explicitly configured.
- **Clippy**: Code must be free of `clippy` warnings. Use `#[allow(...)]` sparingly and always with a comment explaining why.
- **Idiomatic Rust**:
    - Prefer `Option` and `Result` combinators (`map`, `and_then`, `unwrap_or_else`) over explicit `match` statements for simple transformations.
    - Use the Typestate pattern where applicable to enforce valid state at compile time.
    - Use `impl Trait` in return types to reduce boilerplate when possible.
- **Async**: Be mindful of `Send` bounds in async code. Use `tokio` primitives when working with the `tokio` runtime.

## Error Handling

- Use `thiserror` for library error types to create meaningful, strongly-typed errors.
- Use `anyhow` for application-level error handling (CLI binaries, scripts).
- Avoid `unwrap()` and `expect()` in production code. Propagate errors using `?` or handle them gracefully.
    - Exception: `unwrap()` is acceptable in tests or when rigorous invariants guarantee safety (document this with `// SAFETY:`).

## Testing

- **Unit Tests**: Place unit tests in a `tests` module within the same file (`#[cfg(test)] mod tests { ... }`).
- **Integration Tests**: Place integration tests in the `tests/` directory.
- **Property Testing**: Consider using `proptest` for complex logic.
- **Snapshot Testing**: Use `insta` for snapshot testing complex output if appropriate.

## Documentation

- **Doc Comments**: Public APIs must have `///` documentation comments.
- **Examples**: Include code examples in documentation where possible.
- **Readme**: Update `README.md` if the public API changes significantly.
