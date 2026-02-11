---
name: go-review
description: Checklists and anti-patterns for reviewing Go code. Covers API design, error handling, concurrency, interfaces, safety, performance, naming, testing, functional options, logging, and deterministic simulation testing.
---

# Go — Code Review

## Core Principles

- **Catch what the compiler can't.** Focus on design decisions — error strategies, goroutine lifecycles, API evolution safety.
- **Flag the irreversible.** Exported APIs, interface contracts, and error types ship forever. These deserve the most scrutiny.
- **Flag inconsistency.** Style violations compound. One embedded mutex today becomes ten next quarter.

## Reference Index

| Reference | Topics |
|-----------|--------|
| [api-design](references/api-design.md) | Export audit, signature evolution, parameter/result object usage |
| [errors](references/errors.md) | Log-and-return, missing `%w`, strategy consistency, sentinel/structured misuse |
| [interfaces](references/interfaces.md) | Compile-time checks, bloat detection, pointer-to-interface, driver pattern |
| [concurrency](references/concurrency.md) | Embedded mutexes, goroutine leaks, WaitGroup races, unbounded spawning |
| [safety](references/safety.md) | Bare type assertions, missing defer, panic in library, boundary copies |
| [performance](references/performance.md) | `fmt.Sprint` for conversions, missing pre-allocation, string concatenation |
| [code-style](references/code-style.md) | Naming, declarations, organization — combined style checks |
| [testing](references/testing.md) | Table-driven tests, assert vs require, bloated tables, goleak |
| [functional-options](references/functional-options.md) | Exposed options struct, missing defaults, missing WithX |
| [logging](references/logging.md) | fmt.Sprintf in logs, wrong level, raw structs, global logger in library |
| [deterministic-simulation-testing](references/deterministic-simulation-testing.md) | Direct time/rand/os calls, non-deterministic maps, missing seed logging, over-abstracted DST |

## When to Apply

Apply during:
- Code reviews of Go pull requests
- Auditing existing Go packages
- Pre-merge review of new public APIs

Do NOT apply to non-Go files.

## Quick Reference

**Errors**: Flag log-and-return. Flag missing `%w`. Flag capitalized messages. Flag `%s` where `%q` needed. Flag mixed strategies. Flag `==`/type-assertion checks.

**Interfaces**: Flag missing `var _ I = (*T)(nil)`. Flag `*Interface` params. Flag >3 methods. Flag embedded interfaces. Flag missing driver pattern.

**Concurrency**: Flag embedded mutexes. Flag channel size >1. Flag fire-and-forget goroutines. Flag missing `ctx.Done()`. Flag `wg.Add` inside goroutine.

**Safety**: Flag bare type assertions. Flag missing defer. Flag panic in library. Flag `os.Exit` outside main. Flag uncopied boundaries.

**Performance**: Flag `fmt.Sprint`. Flag `[]byte`→`string` in loops. Flag missing pre-allocation. Flag `+` concatenation in loops.

**Style**: Flag generic package names. Flag wrong import order. Flag deep nesting. Flag positional struct fields.

**Testing**: Flag non-table-driven tests. Flag `assert` for preconditions. Flag >10 case tables without split.

**Options**: Flag exported options struct. Flag missing defaults. Flag mixed options + param objects.

**Logging**: Flag `fmt.Sprintf` in log args. Flag `err.Error()` as message. Flag wrong log level. Flag raw structs without `LogValuer`. Flag global logger in library. Flag missing `*Context` variant.

**DST**: Flag direct `time.Now()`. Flag global `rand.*`. Flag direct `os.*` I/O. Flag non-deterministic map iteration. Flag missing seed logging. Flag over-abstracted Clock/FS interfaces where function types suffice.
