---
name: safe-golang
description: Enforce "safe-golang" coding principles in Go. Use when writing, reading, reviewing, or refactoring Go code to ensure maximum safety, predictable execution, and zero technical debt.
---

# Safe Golang

Build highly predictable, robust, and performant Go applications with a "zero technical debt" policy.

## Retrieval-First Development

**Always verify standards against the reference documentation before implementing.**

| Resource | URL / Path |
|----------|------------|
| Safety & Control Flow | `./references/safety.md` |
| Performance Patterns | `./references/performance.md` |
| Developer Experience | `./references/dx.md` |

Review the relevant documentation when writing new logic or performing code reviews.

## When to Use

- Writing new Go logic from scratch
- Refactoring existing Go code to improve safety or performance
- Reviewing Go PRs for code quality and standard adherence
- Optimizing memory allocations or hot paths
- Implementing strict error handling or boundary validation

## Reference Documentation

- `./references/safety.md` - Control flow limits, dynamic memory restrictions, assertions, errors
- `./references/performance.md` - In-place initialization, batching strategies
- `./references/dx.md` - Naming conventions, options structs, formatting limits, zero dependencies

Search: `no recursion`, `context cancellation`, `sync.Pool`, `golangci-lint`, `options struct`

## Core Principles

### Apply Safe Golang For

| Need | Example |
|------|---------|
| Predictable Execution | Bounded channels, bounded loops, timeout contexts |
| Memory Stability | Pre-allocating at startup, `sync.Pool`, value types over pointers |
| Operational Reliability | Explicitly wrapped errors, pair assertions |
| Maintainability | Maximum 70 lines per function, max 100 columns per line, options structs |

### Do NOT Use

- Unbounded loops or goroutines without a `context.Context`
- Dynamic memory allocations (`make()`, `new()`) in hot paths
- Deep indirection (`**` or pointers to interfaces)
- Third-party dependencies (unless explicitly approved, e.g., `godotenv`)

## Quick Reference

### Bounded Control Flow Pattern

```go
// Always bound asynchronous or repeated operations
const maxTasks = 1000
ch := make(chan Task, maxTasks)

for {
    select {
    case <-ctx.Done():
        // Always handle cancellation
        return ctx.Err()
    default:
        if checkStatus() == "done" {
            return nil
        }
        time.Sleep(10 * time.Millisecond)
    }
}
```

### Allocation-Free Hot Path

```go
type Server struct {
    bufferPool sync.Pool
}

func NewServer() *Server {
    return &Server{
        bufferPool: sync.Pool{
            New: func() any {
                b := make([]byte, 1024*1024)
                return &b
            },
        },
    }
}

func (s *Server) process(data []byte) {
    // Acquire from pool instead of allocating
    bufPtr := s.bufferPool.Get().(*[]byte)
    defer s.bufferPool.Put(bufPtr)
    
    // ...
}
```

## Critical Rules

1. **No Recursion or `goto`** - Keep control flow simple and execution bounds completely static.
2. **Fixed Upper Bounds** - All loops and channels must be bounded (e.g. by size or context timeouts).
3. **No Dynamic Memory After Init** - Allocate all significant memory at startup. Use `sync.Pool` for dynamic reuse.
4. **Short Functions** - Hard limit of 70 lines per function. Push `if`s up, push `for`s down.
5. **Check All Returns** - Never ignore errors with `_`. Handle or wrap every returned error.
6. **Explicit Panics Only** - Panic *only* for programmer errors/broken invariants. Use standard errors for operational issues.
7. **Limit Indirection** - Use at most one level of pointer indirection. Prefer value types.
8. **Options Structs** - Use explicit options structs for configuration instead of multiple boolean arguments.
9. **Zero Dependencies** - Strictly avoid third-party dependencies outside the standard library.
10. **Strict Naming** - Add units or qualifiers at the end of variables (e.g., `timeoutMs`, `latencyMaxMs`).

## Anti-Patterns (NEVER)

- Ignoring errors (`_ = ...`)
- Using `init()` for magic initialization or global mutable state
- Using `reflect` for runtime type manipulation
- Passing double pointers (e.g. `**Node`)
- Creating unbounded channels (`make(chan T)`) or unbound loops
- Making network requests without a timeout or context

## Credits

- [TIGER_STYLE.md](https://github.com/tigerbeetle/tigerbeetle/blob/main/docs/TIGER_STYLE.md)

