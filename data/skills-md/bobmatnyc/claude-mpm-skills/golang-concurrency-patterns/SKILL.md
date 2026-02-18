---
name: golang-concurrency-patterns
description: "Go concurrency patterns for production services: context cancellation, errgroup, worker pools, bounded parallelism, fan-in/fan-out, and common race/deadlock pitfalls"
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Write race-free, cancellation-aware Go using context, errgroup, channels, and bounded concurrency patterns"
    when_to_use: "When implementing concurrent pipelines, background workers, fan-out/fan-in, or fixing goroutine leaks, deadlocks, and data races in Go services"
    quick_start: "1. Thread context everywhere 2. Use errgroup.WithContext for fan-out 3. Bound concurrency with a semaphore 4. Make goroutine lifetimes explicit 5. Test with -race and timeouts"
  token_estimate:
    entry: 150
    full: 5000
context_limit: 800
tags:
  - golang
  - concurrency
  - context
  - errgroup
  - channels
  - mutex
  - race-detector
  - worker-pool
requires_tools: []
---

# Go Concurrency Patterns (Production)

## Overview

Go concurrency scales when goroutine lifetimes are explicit, cancellation is propagated with `context.Context`, and shared state is protected (channels or locks). Apply these patterns to build reliable services and avoid common failure modes: goroutine leaks, deadlocks, and data races.

## Quick Start

**Default building blocks**
- Use `context` to drive cancellation and deadlines.
- Use `errgroup.WithContext` for fan-out/fan-in with early abort.
- Bound concurrency (avoid unbounded goroutines) with a semaphore or worker pool.
- Prefer immutable data; otherwise protect shared state with a mutex or make a single goroutine the owner.

**Avoid**
- Fire-and-forget goroutines in request handlers.
- `time.After` inside hot loops.
- Closing channels from the receiver side.
- Sharing mutable variables across goroutines without synchronization.

## Core Concepts

### Goroutine lifecycle

Treat goroutines as resources with a clear owner and shutdown condition.

✅ **Correct: stop goroutines via context**
```go
ctx, cancel := context.WithCancel(context.Background())
defer cancel()

go func() {
    ticker := time.NewTicker(250 * time.Millisecond)
    defer ticker.Stop()

    for {
        select {
        case <-ctx.Done():
            return
        case <-ticker.C:
            // do work
        }
    }
}()
```

❌ **Wrong: goroutine without a stop condition**
```go
go func() {
    for {
        doWork() // leaks forever
    }
}()
```

### Channels vs mutexes (choose intentionally)

- Use **channels** to model ownership/serialization of state or to pipeline work.
- Use **mutexes** to protect shared in-memory state with simple read/write patterns.

✅ **Correct: one goroutine owns the map**
```go
type req struct {
    key   string
    reply chan<- int
}

func mapOwner(ctx context.Context, in <-chan req) {
    m := map[string]int{}
    for {
        select {
        case <-ctx.Done():
            return
        case r := <-in:
            r.reply <- m[r.key]
        }
    }
}
```

✅ **Correct: mutex protects shared map**
```go
type SafeMap struct {
    mu sync.RWMutex
    m  map[string]int
}

func (s *SafeMap) Get(k string) (int, bool) {
    s.mu.RLock()
    defer s.mu.RUnlock()
    v, ok := s.m[k]
    return v, ok
}
```

## Patterns

### 1) Fan-out/fan-in with cancellation (`errgroup`)

Use `errgroup.WithContext` to run concurrent tasks, cancel siblings on error, and wait for completion.

✅ **Correct: cancel on first error**
```go
g, ctx := errgroup.WithContext(ctx)

for _, id := range ids {
    id := id // capture
    g.Go(func() error {
        return process(ctx, id)
    })
}

if err := g.Wait(); err != nil {
    return err
}
```

❌ **Wrong: WaitGroup loses the first error and does not propagate cancellation**
```go
var wg sync.WaitGroup
for _, id := range ids {
    wg.Add(1)
    go func() {
        defer wg.Done()
        _ = process(context.Background(), id) // ignores caller ctx + captures id
    }()
}
wg.Wait()
```

### 2) Bounded concurrency (semaphore pattern)

Bound parallelism to prevent CPU/memory exhaustion and downstream overload.

✅ **Correct: bounded fan-out**
```go
limit := make(chan struct{}, 8) // max 8 concurrent
g, ctx := errgroup.WithContext(ctx)

for _, id := range ids {
    id := id
    g.Go(func() error {
        select {
        case <-ctx.Done():
            return ctx.Err()
        case limit <- struct{}{}:
        }
        defer func() { <-limit }()

        return process(ctx, id)
    })
}

return g.Wait()
```

### 3) Worker pool (durable throughput)

Use a fixed number of workers for stable throughput and predictable resource usage.

✅ **Correct: worker pool with context stop**
```go
type Job struct{ ID string }

func runPool(ctx context.Context, jobs <-chan Job, workers int) error {
    g, ctx := errgroup.WithContext(ctx)

    for i := 0; i < workers; i++ {
        g.Go(func() error {
            for {
                select {
                case <-ctx.Done():
                    return ctx.Err()
                case j, ok := <-jobs:
                    if !ok {
                        return nil
                    }
                    if err := handleJob(ctx, j); err != nil {
                        return err
                    }
                }
            }
        })
    }

    return g.Wait()
}
```

### 4) Pipeline stages (fan-out between stages)

Prefer one-directional channels and close only from the sending side.

✅ **Correct: sender closes**
```go
func stageA(ctx context.Context, out chan<- int) {
    defer close(out)
    for i := 0; i < 10; i++ {
        select {
        case <-ctx.Done():
            return
        case out <- i:
        }
    }
}
```

❌ **Wrong: receiver closes**
```go
func stageB(in <-chan int) {
    close(in) // compile error in<-chan; also wrong ownership model
}
```

### 5) Periodic work without leaks (`time.Ticker` vs `time.After`)

Use `time.NewTicker` for loops; avoid `time.After` allocations in hot paths.

✅ **Correct: ticker**
```go
t := time.NewTicker(1 * time.Second)
defer t.Stop()

for {
    select {
    case <-ctx.Done():
        return
    case <-t.C:
        poll()
    }
}
```

❌ **Wrong: time.After in loop**
```go
for {
    select {
    case <-ctx.Done():
        return
    case <-time.After(1 * time.Second):
        poll()
    }
}
```

## Decision Trees

### Channel vs Mutex

- Need **ownership/serialization** (single writer, message passing) → use **channel + owner goroutine**
- Need **shared cache/map** with many readers and simple updates → use **RWMutex**
- Need **simple counter** with low contention → use **atomic**

### WaitGroup vs errgroup

- Need **error propagation + sibling cancellation** → use **`errgroup.WithContext`**
- Need **only wait** and errors are handled elsewhere → use **`sync.WaitGroup`**

### Buffered vs unbuffered channel

- Need **backpressure** and synchronous handoff → use **unbuffered**
- Need **burst absorption** up to a known size → use **buffered** (size with intent)
- Unsure → start unbuffered and measure; add buffer only to remove known bottleneck

## Testing & Verification

### Race detector and flake control

Run targeted tests with the race detector and disable caching during debugging:

```bash
go test -race ./...
go test -run TestName -race -count=1 ./...
```

### Timeouts to prevent hanging tests

✅ **Correct: test-level timeout via context**
```go
func TestSomething(t *testing.T) {
    ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
    defer cancel()

    if err := doThing(ctx); err != nil {
        t.Fatal(err)
    }
}
```

## Troubleshooting

### Symptom: deadlock (test hangs, goroutines blocked)

Actions:
- Add timeouts (`context.WithTimeout`) around blocking operations.
- Verify channel ownership: only the sender closes; receivers stop on `ok == false`.
- Check for missing `<-limit` release in semaphore patterns.

### Symptom: data race (`go test -race` reports)

Actions:
- Identify shared variables mutated by multiple goroutines.
- Add a mutex or convert to ownership model (single goroutine owns state).
- Avoid writing to captured loop variables.

### Symptom: goroutine leak (memory growth, slow shutdown)

Actions:
- Ensure every goroutine selects on `ctx.Done()`.
- Ensure `time.Ticker` is stopped and channels are closed by senders.
- Avoid `context.Background()` inside request paths; propagate caller context.

## Resources

- Go Blog: Concurrency patterns: https://go.dev/blog/pipelines
- `errgroup`: https://pkg.go.dev/golang.org/x/sync/errgroup
- Go memory model: https://go.dev/ref/mem
