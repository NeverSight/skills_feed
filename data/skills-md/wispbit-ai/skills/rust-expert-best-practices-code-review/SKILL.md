---
name: rust-expert-best-practices-code-review
description: Rust best practices and code quality guidelines for writing idiomatic, safe, and performant Rust code. This skill should be used when writing, reviewing, or refactoring Rust code. Triggers on tasks involving Rust programming, code review, error handling, type safety, or performance optimization.
license: MIT
metadata:
  author: wispbit
  version: "1.0.0"
---

# Rust Expert Best Practices

Simple, pragmatic, opinionated. Only what matters for writing production-grade Rust code.

## When to Apply

Reference these guidelines when:
- Writing Rust code (structs, functions, enums, traits)
- Implementing error handling and Result types
- Reviewing Rust code for safety or performance issues
- Refactoring existing Rust codebases
- Designing APIs and public interfaces
- Optimizing Rust code for performance or clarity

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Type Safety | CRITICAL | `use-typesafe-`, `use-enum-` |
| 2 | Error Handling | CRITICAL-HIGH | `result-`, `avoid-panic` |
| 3 | API Design | HIGH | `use-borrowed-`, `prefer-builder-` |
| 4 | Code Quality | MEDIUM-HIGH | `use-iterator-`, `prefer-format` |
| 5 | Readability | MEDIUM | `use-named-`, `avoid-boolean-` |
| 6 | Performance | MEDIUM | `avoid-rc`, `avoid-box` |

## Quick Reference

- `use-borrowed-argument-types` - Use &str, &[T], &Path instead of &String, &Vec<T>, &PathBuf
- `use-enum-deserialization` - Use exhaustive enum matching for safe deserialization
- `use-typesafe-index-wrappers` - Wrap index types to prevent mixing different indices
- `result-error-returns` - Use ? operator instead of unwrap/expect in Result functions
- `avoid-panic` - Use assert!, Result, or expect based on context instead of panic!
- `use-iterator-transforms` - Use iterator methods instead of explicit push loops
- `use-copied` - Use .copied() to avoid complex dereferencing patterns
- `prefer-format` - Use format! over manual string concatenation
- `prefer-builder-pattern-for-complex` - Use builder pattern for functions with 4+ parameters
- `use-named-placeholders` - Use named placeholders instead of bare _ in destructuring
- `decimal-comparison` - Use .is_sign_negative() instead of comparing to Decimal::ZERO
- `calculated-field-as-method` - Implement calculated fields as methods not struct fields
- `avoid-rc` - Avoid unnecessary Rc<T> when simpler ownership patterns work
- `avoid-box` - Don't use Box<T> for concrete types without legitimate reason
- `avoid-boolean-params` - Replace boolean parameters with enums or structs
- `match-statements-handle-all-cases` - Explicitly handle all enum variants without catch-all patterns

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/use-borrowed-argument-types.md
rules/use-enum-deserialization.md
rules/use-typesafe-index-wrappers.md
rules/result-error-returns.md
rules/avoid-panic.md
rules/use-iterator-transforms.md
rules/use-copied.md
rules/prefer-format.md
rules/prefer-builder-pattern-for-complex.md
rules/use-named-placeholders.md
rules/decimal-comparison.md
rules/calculated-field-as-method.md
rules/avoid-rc.md
rules/avoid-box.md
rules/avoid-boolean-params.md
rules/match-statements-handle-all-cases.md
```

Each rule file contains:
- Brief explanation of why it matters
- When to use and when not to use the pattern
- Implementation requirements
- BAD code examples with explanation
- GOOD code examples with explanation
- Additional context and best practices
