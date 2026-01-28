---
name: rust-code-quality-guide
description: "Code quality guide for Rust. USE WHEN: writing Rust code, reviewing code, or ensuring code quality."
license: MIT
metadata:
  author: masayuki-kono
  version: "1.0.0"
---

# Rust Code Quality Guide

## When to Use

- Writing new Rust code that requires type conversions or error handling
- Reviewing Rust code for quality issues
- Ensuring code follows best practices for error messages and Clippy compliance
- Fixing Clippy warnings or understanding why certain patterns are discouraged

## Quick Reference

- `as` casting → `try_from()` + `map_err()`
- `unwrap_or(default)` → `map_err()` with explicit error
- `format!` → use inline arguments `{var}`
- Error messages must include the causative value
- `#[allow(clippy::...)]` only allowed in test code

---

## Code Quality Rules

### No Fallback for Type Conversion

**CRITICAL**: Never use `unwrap_or(MAX_VALUE)` or similar fallback methods for type conversions.

```rust
// ❌ DANGEROUS - Silent failure with wrong value
let offset = u16::try_from(offset_value).unwrap_or(u16::MAX);

// ❌ DANGEROUS - Silent failure with wrong value (negative to zero)
let value_u8 = u8::try_from(value.max(0))
    .map_err(|_| "value exceeds u8::MAX")?;

// ❌ DANGEROUS - Silent failure with wrong value
let value = u8::try_from(negative_value).unwrap_or(0);

// ✅ SAFE - Explicit error handling
let offset = u16::try_from(offset_value)
    .map_err(|_| format!("offset {offset_value} exceeds u16::MAX"))?;

// ✅ SAFE - Explicit error handling (negative values cause error)
let value_u8 = u8::try_from(value)
    .map_err(|_| format!("value {value} must be between 0 and 255"))?;
```

**Reason**: Using `unwrap_or(MAX_VALUE)`, `max(0)`, `unwrap_or(0)`, or similar fallback methods can cause severe issues by silently mapping out-of-range or invalid values to default values, leading to incorrect calculations and potential system failures.

**Rule**: Always use proper error handling with `map_err` or explicit `match` statements for type conversions. Never silently convert invalid values (negative, out-of-range, etc.) to default values.

### Inline Format Arguments

**CRITICAL**: Always use inline format arguments in `format!` macro to avoid Clippy warnings.

```rust
// ❌ BAD - Causes clippy::uninlined_format_args warning
let message = format!("Error: {} occurred at line {}", error, line);

// ✅ GOOD - Use inline format arguments
let message = format!("Error: {error} occurred at line {line}");
```

**Reason**: Inline format arguments are more readable, performant, and avoid Clippy warnings.

**Rule**: Always use `{variable}` syntax instead of separate arguments in `format!` macro.

### Include Causative Values in Error Messages

**CRITICAL**: Always include the actual parameter values that caused the error in error messages.

```rust
// ❌ BAD - Generic error message without context
return Err("Invalid count".into());

// ✅ GOOD - Include the actual parameter value
return Err(format!("Invalid count: {count} (must be 1-474)").into());

// ✅ GOOD - Include multiple parameters for complex validation
return Err(format!("Range exceeds maximum: {start}-{end} (max 99)").into());
```

**Reason**: Including actual parameter values in error messages makes debugging significantly easier by providing immediate context about what went wrong.

**Rule**: Always include the actual parameter values that caused the error in error messages using inline format arguments.

### Use try_from() Instead of as

**CRITICAL**: Use `try_from()` instead of `as` casting for type conversions.

```rust
// ❌ BAD - Silent truncation with as casting
let value = large_number as u8;

// ✅ GOOD - Explicit error handling with try_from
let value = u8::try_from(large_number)
    .map_err(|_| format!("Value {large_number} exceeds u8::MAX"))?;
```

**Reason**: `as` casting can silently truncate values, while `try_from()` provides explicit error handling for out-of-range conversions.

**Rule**: Use `try_from()` instead of `as` casting and implement proper error handling for type conversions.

### No Clippy Suppression in Production Code

**CRITICAL**: Never use `#[allow(clippy::...)]` to suppress Clippy warnings in production code (non-test code).

```rust
// ❌ BAD - Suppressing warnings in production code
#[allow(clippy::too_many_lines)]
pub async fn process_request(...) {
    // 100+ lines of code
}

// ✅ GOOD - Refactor the function to be smaller
pub async fn process_request(...) {
    // Call smaller helper functions
    handle_validation(...).await?;
}

async fn handle_validation(...) {
    // Smaller, focused function
}
```

**Reason**: Suppressing Clippy warnings hides code quality issues. Instead, refactor the code to address the underlying problem (e.g., split large functions, fix type issues, etc.).

**Rule**: 
- In production code: Always fix the underlying issue instead of suppressing warnings
- In test code: `#[allow(...)]` is acceptable for test-specific patterns (e.g., `unwrap_used`, `significant_drop_tightening`)
- If a warning cannot be reasonably fixed, document why with a comment explaining the exception
