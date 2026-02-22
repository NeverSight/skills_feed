---
name: backend-principle-eng-typescript-pro-max
description: "Principal backend engineering intelligence for TypeScript services. Actions: plan, design, build, implement, review, fix, optimize, refactor, debug, secure, scale backend code and architectures. Focus: correctness, reliability, performance, security, observability, scalability, operability, cost."
---

# Backend Principle Eng TypeScript Pro Max

Principal-level guidance for TypeScript backend systems in product companies. Optimized for Bun runtime with Node 20 LTS compatibility.

## When to Apply
- Designing or refactoring TypeScript services, APIs, and distributed systems
- Reviewing code for correctness, reliability, performance, and security
- Planning migrations, scalability, or cost optimizations
- Incident follow-ups and systemic fixes

## Priority Model (highest to lowest)

| Priority | Category | Goal | Signals |
| --- | --- | --- | --- |
| 1 | Correctness & Contracts | No wrong answers | Strong validation, invariants, idempotency |
| 2 | Reliability & Resilience | Survive failures | Timeouts, retries, graceful degradation |
| 3 | Security & Privacy | Zero trust by default | Authz, secrets, minimal exposure |
| 4 | Performance & Efficiency | Predictable latency | Async I/O, bounded queues, caching |
| 5 | Observability & Operability | Fast triage | Tracing, metrics, runbooks |
| 6 | Data & Consistency | Integrity over time | Safe migrations, outbox, versioning |
| 7 | Scalability & Evolution | Safe growth | Statelessness, partitioning, backpressure |
| 8 | Developer Experience & Testing | Sustainable velocity | CI gates, deterministic tests, typing |

## Quick Reference (Rules)

### 1. Correctness & Contracts (CRITICAL)
- `api-contracts` - Versioned schemas and explicit validation
- `input-validation` - Validate at boundaries, reject unknowns
- `idempotency` - Safe retries with idempotency keys
- `invariants` - Enforce domain rules in service and database
- `time-utc` - Store UTC, use monotonic clocks for durations

### 2. Reliability & Resilience (CRITICAL)
- `timeouts` - Set per dependency; no unbounded waits
- `retries` - Bounded with jitter; avoid retry storms
- `circuit-breakers` - Fail fast for degraded dependencies
- `bulkheads` - Isolate thread pools and queues
- `load-shedding` - Graceful degradation under load

### 3. Security & Privacy (CRITICAL)
- `authz` - Enforce at every service boundary
- `secrets` - Use vault/KMS; never in code or logs
- `data-min` - Redact PII by default
- `crypto` - TLS everywhere; strong defaults
- `supply-chain` - Pin deps; scan CVEs

### 4. Performance & Efficiency (HIGH)
- `async-io` - Use async for I/O bound paths; avoid blocking
- `pooling` - Right-size DB/HTTP pools; avoid starvation
- `cache` - TTL and stampede protection for hot reads
- `batching` - Batch I/O and DB operations where safe
- `profiling` - Measure before optimizing

### 5. Observability & Operability (HIGH)
- `structured-logs` - JSON logs with trace ids
- `metrics` - RED/USE metrics plus business KPIs
- `tracing` - Propagate context end-to-end
- `alerts` - SLO-based with runbooks
- `deploys` - Safe rollouts and rapid rollback

### 6. Data & Consistency (HIGH)
- `transactions` - Clear boundaries; avoid cross-service tx
- `schema-evolution` - Backward compatible migrations
- `outbox` - Reliable event publishing
- `id-generation` - Globally unique IDs
- `read-models` - Use CQRS when complexity is justified

### 7. Scalability & Evolution (MEDIUM)
- `stateless` - Externalize state, scale horizontally
- `partitioning` - Shard by stable keys
- `versioning` - API and event versioning
- `backpressure` - Bounded queues, explicit limits
- `config` - Dynamic config with validation

### 8. Developer Experience & Testing (MEDIUM)
- `typing` - Strict tsconfig for public APIs and core logic
- `tests` - Unit, integration, contract, load tests
- `determinism` - Hermetic tests, fixed seeds, stable time
- `lint` - Static analysis and formatting

## Execution Workflow
1. Clarify product goals, SLOs, latency and cost budgets
2. Map data flow, dependencies, and failure modes
3. Choose storage and consistency model (document tradeoffs)
4. Define contracts: API schemas, events, and idempotency
5. Implement with safe defaults, observability, and resilience
6. Validate with tests, load, and failure scenarios
7. Review risks and publish runbooks

## Language-Specific Guidance
See `references/typescript-core.md` for Bun-first stack defaults and patterns.
