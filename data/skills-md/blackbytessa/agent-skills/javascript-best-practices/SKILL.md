---
name: javascript-best-practices
description: Modern JavaScript best practices and performance optimization guidelines. Use when writing, reviewing, or refactoring JavaScript code to ensure optimal performance, maintainability, and modern patterns.
license: MIT
metadata:
  author: your-name
  version: "1.0.0"
---

# JavaScript Best Practices

Comprehensive guide for modern JavaScript development covering performance, code quality, and best practices.

## When to Apply

Reference these guidelines when:
- Writing new JavaScript code
- Reviewing code for performance or quality issues
- Refactoring existing JavaScript code
- Optimizing application performance
- Ensuring code maintainability

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Performance | CRITICAL | `perf-` |
| 2 | Async Patterns | HIGH | `async-` |
| 3 | Error Handling | HIGH | `error-` |
| 4 | Code Quality | HIGH | `quality-` |
| 5 | Modern Syntax | MEDIUM | `modern-` |
| 6 | Arrays | MEDIUM | `array-` |

## Quick Reference

### 1. Performance (CRITICAL)

- `perf-avoid-memory-leaks` - Always cleanup event listeners, timers, intervals, subscriptions, and observers

### 2. Async Patterns (HIGH)

- `async-promise-chains` - Prefer async/await over .then()/.catch() chains for better readability

### 3. Error Handling (HIGH)

- `error-defensive-programming` - Use guard clauses and validate input at system boundaries
- `error-explicit-validation` - Don't hide data errors with optional chaining - validate explicitly

### 4. Code Quality (HIGH)

- `quality-strict-equality` - Use === instead of == (except for null checks)
- `quality-explicit-boolean-checks` - Don't rely on truthy/falsy for non-boolean values
- `quality-small-functions` - Keep functions focused on one task (5-15 lines ideal)
- `quality-no-magic-numbers` - Extract numbers to named constants
- `quality-immutability` - Prefer creating new objects/arrays over mutating existing ones
- `quality-pure-functions` - Write functions with no side effects when possible
- `quality-naming-conventions` - Use meaningful, consistent names (camelCase, PascalCase, UPPER_SNAKE_CASE)
- `quality-commenting` - Comments explain "why", not "what" - code should be self-documenting
- `quality-avoid-console-log` - Use structured logging with levels in production

### 5. Modern Syntax (MEDIUM)

- `modern-const-let-no-var` - Never use var; prefer const, use let only when reassignment is needed

### 6. Arrays (MEDIUM)

- `array-mutation-safety` - Avoid in-place mutations (push, sort, reverse) on shared arrays

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/perf-avoid-memory-leaks.md
rules/async-promise-chains.md
rules/error-defensive-programming.md
rules/quality-strict-equality.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
