---
name: backend-principle-eng-nodejs-pro-max
description: "Principal backend engineering intelligence for Node.js runtime systems. Actions: plan, design, build, implement, review, fix, optimize, refactor, debug, secure, scale backend code and architectures. Focus: correctness, reliability, performance, security, observability, scalability, operability, cost."
---

# Backend Principle Eng Node.js Pro Max

Principal-level guidance for Node.js backend systems and runtime behavior. Optimized for Bun runtime with Node 20 LTS compatibility.

## When to Apply
- Designing or refactoring Node.js services and platform components
- Reviewing runtime, event loop, and concurrency behavior
- Diagnosing latency spikes, memory leaks, and throughput regressions
- Planning scalability, cost, or reliability improvements

## Priority Model (highest to lowest)

| Priority | Category | Goal | Signals |
| --- | --- | --- | --- |
| 1 | Correctness & Contracts | No wrong answers | Validation, invariants, idempotency |
| 2 | Reliability & Resilience | Survive failures | Timeouts, retries, graceful degradation |
| 3 | Security & Privacy | Zero trust by default | Authz, secrets, minimal exposure |
| 4 | Performance & Efficiency | Predictable latency | Event loop health, bounded queues |
| 5 | Observability & Operability | Fast triage | Tracing, metrics, runbooks |
| 6 | Data & Consistency | Integrity over time | Safe migrations, outbox |
| 7 | Scalability & Evolution | Safe growth | Statelessness, partitioning |
| 8 | Developer Experience & Testing | Sustainable velocity | CI gates, deterministic tests |

## Quick Reference (Rules)

### 1. Correctness & Contracts (CRITICAL)
- `api-contracts` - Versioned schemas and explicit validation
- `input-validation` - Validate at boundaries, reject unknowns
- `idempotency` - Safe retries with idempotency keys
- `invariants` - Enforce domain rules in service and database

### 2. Reliability & Resilience (CRITICAL)
- `timeouts` - Set per dependency; no unbounded waits
- `retries` - Bounded with jitter; avoid retry storms
- `circuit-breakers` - Fail fast for degraded dependencies
- `bulkheads` - Isolate heavy dependencies and queues
- `load-shedding` - Graceful degradation under load

### 3. Security & Privacy (CRITICAL)
- `authz` - Enforce at every service boundary
- `secrets` - Use vault/KMS; never in code or logs
- `data-min` - Redact PII by default
- `crypto` - TLS everywhere; strong defaults

### 4. Performance & Efficiency (HIGH)
- `event-loop` - Monitor lag; avoid blocking sync work
- `streams` - Use backpressure-aware streams for large payloads
- `pooling` - Right-size DB/HTTP pools; avoid starvation
- `cache` - TTL and stampede protection for hot reads
- `profiling` - Measure before optimizing

### 5. Observability & Operability (HIGH)
- `structured-logs` - JSON logs with trace ids
- `metrics` - RED/USE metrics plus business KPIs
- `tracing` - Propagate context end-to-end
- `alerts` - SLO-based with runbooks

### 6. Data & Consistency (HIGH)
- `transactions` - Clear boundaries; avoid cross-service tx
- `schema-evolution` - Backward compatible migrations
- `outbox` - Reliable event publishing

### 7. Scalability & Evolution (MEDIUM)
- `stateless` - Externalize state, scale horizontally
- `partitioning` - Shard by stable keys
- `versioning` - API and event versioning
- `backpressure` - Bounded queues, explicit limits

### 8. Developer Experience & Testing (MEDIUM)
- `tests` - Unit, integration, contract, load tests
- `determinism` - Hermetic tests, fixed seeds, stable time
- `lint` - Static analysis and formatting

## Execution Workflow
1. Clarify product goals, SLOs, latency and cost budgets
2. Map data flow, dependencies, and event loop risks
3. Choose storage and consistency model (document tradeoffs)
4. Define contracts: API schemas, events, and idempotency
5. Implement with safe defaults, observability, and resilience
6. Validate with tests, load, and failure scenarios
7. Review risks and publish runbooks

## Runtime Guidance
See `references/node-core.md` for event loop, memory, and Bun-first runtime patterns.
