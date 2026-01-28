---
name: java-concurrency
description: Master Java concurrency - threads, executors, locks, CompletableFuture, virtual threads
sasmp_version: "1.3.0"
version: "3.0.0"
bonded_agent: 02-java-advanced
bond_type: PRIMARY_BOND
allowed-tools: Read, Write, Bash, Glob, Grep

# Parameter Validation
parameters:
  concurrency_model:
    type: string
    enum: [threads, executors, virtual_threads, reactive]
  java_version:
    type: string
    default: "21"
---

# Java Concurrency Skill

Master Java concurrency patterns for thread-safe applications.

## Overview

This skill covers concurrency from basic threads to virtual threads (Java 21+), including thread pools, synchronization, and CompletableFuture.

## When to Use This Skill

Use when you need to:
- Write thread-safe code
- Implement parallel processing
- Use async programming patterns
- Tune thread pools
- Debug concurrency issues

## Topics Covered

### Thread Management
- Thread lifecycle and states
- Daemon vs user threads
- Interrupt handling

### Synchronization
- synchronized, volatile
- Lock interfaces (ReentrantLock)
- Atomic operations

### Executors
- ThreadPoolExecutor configuration
- ForkJoinPool
- Virtual Threads (Java 21+)

### CompletableFuture
- Async execution
- Chaining and composition
- Exception handling

## Quick Reference

```java
// Virtual Threads (Java 21+)
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    IntStream.range(0, 10_000).forEach(i ->
        executor.submit(() -> processRequest(i)));
}

// CompletableFuture composition
CompletableFuture<Result> result = fetchUser(id)
    .thenCompose(user -> fetchOrders(user.id()))
    .thenApply(orders -> processOrders(orders))
    .exceptionally(ex -> handleError(ex))
    .orTimeout(5, TimeUnit.SECONDS);

// Thread pool configuration
ThreadPoolExecutor executor = new ThreadPoolExecutor(
    10, 50, 60L, TimeUnit.SECONDS,
    new ArrayBlockingQueue<>(1000),
    new ThreadPoolExecutor.CallerRunsPolicy()
);

// Lock with timeout
ReentrantLock lock = new ReentrantLock();
if (lock.tryLock(1, TimeUnit.SECONDS)) {
    try {
        // critical section
    } finally {
        lock.unlock();
    }
}
```

## Thread Pool Sizing

| Workload | Formula | Example |
|----------|---------|---------|
| CPU-bound | cores | 8 threads |
| I/O-bound | cores * (1 + wait/compute) | 80 threads |

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Deadlock | Circular lock | Lock ordering, tryLock |
| Race condition | Missing sync | Add locks/atomics |
| Thread starvation | Unfair scheduling | Fair locks |

### Debug Commands
```bash
jstack -l <pid> > threaddump.txt
jcmd <pid> Thread.print
```

## Usage

```
Skill("java-concurrency")
```
