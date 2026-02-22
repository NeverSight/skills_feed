---
name: backend-principle-eng-java-pro-max
description: "Principal backend engineering intelligence for Java services and distributed systems. Actions: plan, design, build, implement, review, fix, optimize, refactor, debug, secure, scale backend code and architectures. Focus: correctness, reliability, performance, security, observability, scalability, operability, cost."
---

# Backend Principle Eng Java Pro Max

Senior principal-level guidance for Java backend systems in product companies. Emphasizes durable architecture, production readiness, and measurable outcomes.

## When to Apply
- Designing or refactoring Java services, APIs, data pipelines, or distributed systems
- Reviewing PRs for correctness, reliability, performance, and security
- Planning migrations, scalability, or cost optimizations
- Incident follow-ups and systemic fixes

## Priority Model (highest to lowest)

| Priority | Category | Goal | Signals |
| --- | --- | --- | --- |
| 1 | Correctness & Contracts | No wrong answers | Stable invariants, strong validation, idempotency |
| 2 | Reliability & Resilience | Survive failures | Timeouts, retries, circuit breakers, graceful degrade |
| 3 | Security & Privacy | Zero trust by default | Authz everywhere, secrets managed, minimal data exposure |
| 4 | Performance & Efficiency | Predictable latency | P95/P99 targets, bounded queues, efficient I/O |
| 5 | Observability & Operability | Fast detection and recovery | Tracing, actionable alerts, runbooks |
| 6 | Data & Consistency | Integrity over time | Safe migrations, transactional boundaries, outbox |
| 7 | Scalability & Evolution | Safe growth | Statelessness, partitioning, versioning |
| 8 | Developer Experience & Testing | Sustainable velocity | CI gates, deterministic tests, clear docs |

## Quick Reference (Rules)

### 1. Correctness & Contracts (CRITICAL)
- `api-contracts` - Versioned APIs, explicit schemas, backward compatibility
- `input-validation` - Validate at boundaries, normalize, reject unknowns
- `idempotency` - Safe retries for mutating calls with idempotency keys
- `invariants` - Enforce domain rules in service and database
- `time-utc` - Store UTC, handle clock skew, use monotonic time for durations

### 2. Reliability & Resilience (CRITICAL)
- `timeouts` - Set per dependency; no unbounded waits
- `retries` - Bounded with jitter; never retry non-idempotent without keys
- `circuit-breakers` - Fail fast when downstream degrades
- `bulkheads` - Isolate thread pools and queues per dependency
- `load-shedding` - Backpressure and graceful degradation under load

### 3. Security & Privacy (CRITICAL)
- `authz` - Enforce at every service boundary, deny by default
- `secrets` - Managed via vault/KMS; never in code or logs
- `data-min` - Log minimal PII, redact by default
- `crypto` - TLS everywhere, rotate keys, strong defaults
- `supply-chain` - Pin deps, scan CVEs, reproducible builds

### 4. Performance & Efficiency (HIGH)
- `pooling` - Right-size DB/HTTP pools; avoid blocking shared pools
- `serialization` - Avoid reflection in hot paths; prefer explicit schemas
- `allocation` - Minimize hot-path allocations and boxing
- `cache` - TTL and stampede protection for hot reads
- `batching` - Batch I/O and DB operations where safe

### 5. Observability & Operability (HIGH)
- `structured-logs` - JSON logs with trace/span ids and request ids
- `metrics` - RED/USE metrics plus business KPIs
- `tracing` - Propagate context end-to-end
- `alerts` - SLO-based, actionable, with runbooks
- `deploys` - Safe rollouts, health checks, rapid rollback

### 6. Data & Consistency (HIGH)
- `transactions` - Clear boundaries, short duration, avoid cross-service tx
- `schema-evolution` - Backward compatible migrations
- `outbox` - Reliable event publishing with transactional outbox
- `id-generation` - Globally unique IDs; avoid auto-increment for scale
- `read-models` - Use CQRS only when complexity is justified

### 7. Scalability & Evolution (MEDIUM)
- `stateless` - Externalize state, scale horizontally
- `partitioning` - Shard by stable keys, avoid hotspots
- `versioning` - API and event versioning with deprecation plans
- `backpressure` - Bounded queues, explicit limits
- `config` - Dynamic config with safe defaults and validation

### 8. Developer Experience & Testing (MEDIUM)
- `tests` - Unit, integration, contract, and load tests
- `determinism` - Hermetic tests, fixed seeds, stable time
- `lint` - Static analysis, formatting, build reproducibility
- `docs` - ADRs for major decisions, runbook ownership

## Execution Workflow
1. Clarify product goals, SLOs, latency and cost budgets
2. Map data flow, dependencies, and failure modes
3. Choose storage and consistency model (document tradeoffs)
4. Define contracts: API schemas, events, and idempotency
5. Implement with safe defaults, observability, and resilience
6. Validate with tests, load, and failure scenarios
7. Review risks and publish runbooks

## Language-Specific Guidance
See `references/java-core.md` for stack defaults, JVM tuning, libraries, and Java-specific patterns.
