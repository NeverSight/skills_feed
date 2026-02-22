---
name: backend-principle-eng-cpp-pro-max
description: "Principal backend engineering intelligence for C++ systems and performance-critical services. Actions: plan, design, build, implement, review, fix, optimize, refactor, debug, secure, scale backend code and architectures. Focus: correctness, memory safety, latency, reliability, observability, scalability, operability."
---

# Backend Principle Eng C++ Pro Max

Principal-level guidance for C++ backend systems, low-latency services, and infrastructure. Emphasizes correctness, memory safety, and predictable performance.

## When to Apply
- Designing or refactoring C++ backend services and infrastructure
- Reviewing code for memory safety, concurrency, and latency regressions
- Building high-throughput networking, storage, or compute systems
- Incident response and performance regressions

## Priority Model (highest to lowest)

| Priority | Category | Goal | Signals |
| --- | --- | --- | --- |
| 1 | Correctness & UB Avoidance | No undefined behavior | RAII, invariants, validated inputs |
| 2 | Reliability & Resilience | Fail safe under load | Timeouts, backpressure, graceful shutdown |
| 3 | Security | Hard to exploit | Hardened builds, safe parsing, least privilege |
| 4 | Performance & Latency | Predictable P99 | Stable allocs, bounded queues, zero-copy where safe |
| 5 | Observability & Operability | Fast triage | Trace ids, structured logs, metrics |
| 6 | Scalability & Evolution | Safe growth | Statelessness, sharding, protocol versioning |
| 7 | Tooling & Testing | Sustainable velocity | Sanitizers, fuzzing, CI gates |

## Quick Reference (Rules)

### 1. Correctness & UB Avoidance (CRITICAL)
- `raii` - Own resources with RAII and deterministic lifetimes
- `no-raw-ownership` - Raw pointers only for non-owning references
- `bounds` - Validate all indices and sizes at boundaries
- `invariants` - Assert core invariants and state transitions
- `time` - Use monotonic clocks for durations

### 2. Reliability & Resilience (CRITICAL)
- `timeouts` - Explicit timeouts for every external call
- `backpressure` - Bounded queues; apply load shedding
- `shutdown` - Drain in-flight work with deadlines
- `bulkheads` - Isolate thread pools by dependency

### 3. Security (CRITICAL)
- `safe-parse` - Validate untrusted input; avoid unsafe string ops
- `harden` - Compile with stack protection, PIE, RELRO, FORTIFY
- `secrets` - No secrets in logs or core dumps
- `least-priv` - Drop privileges and sandbox when possible

### 4. Performance & Latency (HIGH)
- `allocs` - Minimize allocations in hot paths
- `copy` - Prefer move or views; avoid unnecessary copies
- `cache` - Improve locality; avoid false sharing
- `io` - Use async I/O where appropriate
- `profiling` - Measure before optimizing

### 5. Observability & Operability (HIGH)
- `logs` - Structured logs with request and trace ids
- `metrics` - RED/USE plus business KPIs
- `tracing` - Propagate trace context across threads
- `crash` - Symbolized crash reports and core dump policies

### 6. Scalability & Evolution (MEDIUM)
- `stateless` - Externalize state, enable horizontal scale
- `partitioning` - Shard by stable keys
- `versioning` - Protocol and schema versioning
- `limits` - Explicit limits on payloads and queue sizes

### 7. Tooling & Testing (MEDIUM)
- `sanitizers` - ASan, UBSan, TSan in CI
- `fuzzing` - Fuzz parsers and protocol handlers
- `tests` - Unit, integration, and load tests
- `lint` - clang-tidy, clang-format, warnings as errors

## Execution Workflow
1. Clarify latency/SLOs, throughput, and cost budgets
2. Map data flow, thread model, and failure modes
3. Define interfaces and memory ownership contracts
4. Implement with bounded queues and explicit timeouts
5. Add observability and crash diagnostics
6. Validate with sanitizers, fuzzing, load tests
7. Review risks and publish runbooks

## Language-Specific Guidance
See `references/cpp-core.md` for toolchain defaults, concurrency patterns, and hardening.
