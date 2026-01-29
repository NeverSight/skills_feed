---
name: python-best-practices
description: Python >=3.11 performance optimization guidelines. This skill should be used when writing, reviewing, or refactoring Python code to ensure optimal performance patterns. Triggers on tasks involving asyncio, data structures, memory management, serialization, concurrency, or Python performance optimization.
---

# Python Community Python >=3.11 Best Practices

Comprehensive performance optimization guide for Python >=3.11 applications. Contains 45 rules across 9 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Writing new Python async/await code
- Processing large datasets or files
- Implementing caching and memoization
- Choosing data structures for performance
- Reviewing code for performance issues

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | I/O Patterns | CRITICAL | `io-` |
| 2 | Async Concurrency | CRITICAL | `async-` |
| 3 | Memory Management | HIGH | `mem-` |
| 4 | Data Structures | HIGH | `ds-` |
| 5 | Algorithm Efficiency | MEDIUM-HIGH | `algo-` |
| 6 | Concurrency Model | MEDIUM | `conc-` |
| 7 | Serialization | MEDIUM | `serial-` |
| 8 | Caching and Memoization | LOW-MEDIUM | `cache-` |
| 9 | Runtime Tuning | LOW | `runtime-` |

## Quick Reference

### 1. I/O Patterns (CRITICAL)

- `io-async-file-operations` - Use async file I/O for non-blocking operations
- `io-batch-database-operations` - Batch database operations to reduce round trips
- `io-connection-pooling` - Use connection pooling for database and HTTP clients
- `io-streaming-large-files` - Stream large files instead of loading into memory
- `io-use-buffered-io` - Use buffered I/O for frequent small writes

### 2. Async Concurrency (CRITICAL)

- `async-avoid-async-overhead` - Avoid async overhead for CPU-bound work
- `async-avoid-blocking-calls` - Avoid blocking calls in async code
- `async-create-task-fire-forget` - Store references to fire-and-forget tasks
- `async-gather-independent-operations` - Use asyncio.gather() for independent operations
- `async-semaphore-rate-limiting` - Use semaphores for concurrency limiting
- `async-taskgroup-structured-concurrency` - Use TaskGroup for structured concurrency

### 3. Memory Management (HIGH)

- `mem-avoid-intermediate-lists` - Avoid intermediate lists in pipelines
- `mem-generators-lazy-evaluation` - Use generators for lazy evaluation
- `mem-preallocate-lists` - Preallocate lists when size is known
- `mem-slots-dataclass` - Use __slots__ for memory-efficient classes
- `mem-string-interning` - Leverage string interning for repeated strings
- `mem-weak-references` - Use weak references for caches and observers

### 4. Data Structures (HIGH)

- `ds-counter-for-counting` - Use Counter for frequency counting
- `ds-deque-for-queues` - Use deque for O(1) queue operations
- `ds-dict-get-default` - Use dict.get() with default instead of KeyError handling
- `ds-namedtuple-immutable-records` - Use NamedTuple for immutable lightweight records
- `ds-set-for-membership` - Use Set for O(1) membership testing

### 5. Algorithm Efficiency (MEDIUM-HIGH)

- `algo-avoid-repeated-computation` - Cache expensive computations in loops
- `algo-builtin-functions` - Use built-in functions over manual implementation
- `algo-itertools-recipes` - Use itertools for efficient iteration patterns
- `algo-list-comprehension` - Use list comprehensions over manual loops
- `algo-local-variable-lookup` - Use local variables in hot loops
- `algo-string-join` - Use str.join() for string concatenation

### 6. Concurrency Model (MEDIUM)

- `conc-asyncio-queues` - Use asyncio.Queue for producer-consumer patterns
- `conc-avoid-lock-contention` - Minimize lock contention in threaded code
- `conc-choose-right-model` - Choose the right concurrency model
- `conc-process-pool-chunking` - Use chunking for ProcessPoolExecutor
- `conc-thread-safe-globals` - Use thread-safe data structures for shared state

### 7. Serialization (MEDIUM)

- `serial-avoid-pickle-security` - Avoid pickle for untrusted data
- `serial-msgpack-binary` - Use MessagePack for compact binary serialization
- `serial-orjson-over-json` - Use orjson for high-performance JSON
- `serial-pydantic-validation` - Use Pydantic for validated deserialization

### 8. Caching and Memoization (LOW-MEDIUM)

- `cache-avoid-over-caching` - Avoid over-caching low-value operations
- `cache-cached-property` - Use cached_property for expensive computed attributes
- `cache-lru-cache-decorator` - Use lru_cache for expensive pure functions
- `cache-ttl-expiration` - Implement TTL for time-sensitive caches

### 9. Runtime Tuning (LOW)

- `runtime-avoid-global-lookups` - Avoid repeated global and module lookups
- `runtime-exception-handling-cost` - Minimize exception handling in hot paths
- `runtime-profile-before-optimizing` - Profile before optimizing
- `runtime-use-python311-plus` - Upgrade to Python 3.11+ for free performance

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references

## Reference Files

| File | Description |
|------|-------------|
| [AGENTS.md](AGENTS.md) | Complete compiled guide with all rules |
| [references/_sections.md](references/_sections.md) | Category definitions and ordering |
| [assets/templates/_template.md](assets/templates/_template.md) | Template for new rules |
| [metadata.json](metadata.json) | Version and reference information |
