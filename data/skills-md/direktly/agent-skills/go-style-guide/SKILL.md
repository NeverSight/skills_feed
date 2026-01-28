---
name: go-style-guide
description: Go programming best practices and style guide. This skill should be used when writing, reviewing, or refactoring Go code to ensure optimal performance patterns. Triggers on tasks involving Go code, data structures, concurrency, or performance improvements.
license: APACHE-2.0
metadata:
  author: Direkt, Inc.
  version: "1.0.0"
---

# Go Best Practices

Styles are the conventions that govern our code. The term style is a bit of
misnomer, since these conventions cover far more than just source file
formatting—gofmt handles that for us.

The goal of this guide is to manage this complexity by describing in detail the
Dos and Don'ts of writing Go code at Direkt. These rules exist to keep the code
base manageable while still allowing developers to use Go language features
productively. Created based on the Uber Go Style Guide.

## When to Apply

Reference these guidelines when:
- Writing new Go code
- Reviewing code for performance issues
- Refactoring existing Go code
- Optimizing performance, latency, or allocations

## Rule Categories by Priority

| Priority | Category | Impact | Examples |
|----------|----------|--------|----------|
| 1 | Correctness & Error Handling | CRITICAL | `panic.md`, `error-once.md`, `error-wrap.md`, `exit-once.md` |
| 2 | Concurrency | CRITICAL | `goroutine-forget.md`, `goroutine-exit.md`, `channel-size.md`, `atomic.md` |
| 3 | APIs & Types | HIGH | `interface-pointer.md`, `interface-compliance.md`, `functional-option.md`, `struct-tag.md` |
| 4 | Performance | HIGH | `performance.md`, `container-capacity.md`, `strconv.md`, `string-byte-slice.md` |
| 5 | Readability & Style | MEDIUM | `var-scope.md`, `nest-less.md`, `decl-group.md`, `function-order.md` |
| 6 | Testing | MEDIUM | `table-driven-tests.md`, `test-table.md` |
| 7 | Tooling | LOW | `lint.md`, `printf-name.md`, `struct-field-key.md` |

## Quick Reference

### 1. Correctness & Error Handling (CRITICAL)

- `panic.md` - Avoid panics in production; return errors.
- `error-type.md`, `error-wrap.md`, `error-once.md`, `error-name.md` - Use errors consistently; wrap with context; handle once.
- `exit-main.md`, `exit-once.md` - Exit in `main()`; keep exit logic in one place.

### 2. Concurrency (CRITICAL)

- `goroutine-forget.md` - Don’t fire-and-forget goroutines.
- `goroutine-exit.md` - Always provide a way to wait for goroutines to exit.
- `goroutine-init.md` - Don’t start goroutines in `init()`.
- `channel-size.md` - Channel size should be one or unbuffered.
- `mutex-zero-value.md` - Zero-value mutexes are valid (avoid pointers).
- `atomic.md` - Prefer typed atomics (`sync/atomic`, Go 1.19+).

### 3. APIs & Types (HIGH)

- `interface-pointer.md`, `interface-compliance.md`, `interface-receiver.md` - Interface and receiver best practices.
- `functional-option.md` - Prefer functional options for extensible APIs.
- `struct-tag.md` - Add tags for marshaled struct fields.
- `embed-public.md`, `struct-embed.md` - Be careful with embedding (especially in public structs).

### 4. Performance (HIGH)

- `performance.md` - Apply performance guidance on hot paths.
- `container-capacity.md` - Pre-size slices/maps where possible.
- `container-copy.md` - Copy slices/maps at boundaries to avoid aliasing bugs.
- `strconv.md` - Prefer `strconv` over `fmt` for primitives.
- `string-byte-slice.md` - Avoid repeated string-to-`[]byte` conversions.

### 5. Readability & Style (MEDIUM)

- `consistency.md`, `line-length.md` - Optimize for readability and consistency.
- `decl-group.md`, `import-group.md` - Group similar declarations and imports.
- `function-name.md`, `package-name.md`, `builtin-name.md` - Naming conventions.
- `function-order.md`, `nest-less.md`, `else-unnecessary.md`, `var-scope.md` - Reduce nesting and keep scope tight.
- `var-decl.md`, `slice-nil.md`, `map-init.md` - Prefer idiomatic declarations/initialization.
- `struct-field-key.md`, `struct-field-zero.md`, `struct-pointer.md`, `struct-zero.md` - Struct initialization conventions.

### 6. Testing (MEDIUM)

- `test-table.md`, `table-driven-tests.md` - Table tests, subtests, and when to avoid over-complicated tables.

### 7. Tooling (LOW)

- `lint.md` - Lint consistently across the codebase.
- `printf-name.md`, `printf-const.md` - Enable `go vet` format-string checking.

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/SUMMARY.md
AGENTS.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
