---
name: golang-mastery-skill
description: |
  Principal/Senior-level Go (Golang) playbook for architecture, idiomatic code, concurrency, testing, performance, reliability, security, observability, and production readiness.
  Use when: designing services/APIs/CLIs, doing large refactors, running code reviews, debugging races/leaks, tuning performance, hardening security, and shipping to production.
---

# Golang Mastery (Senior → Principal)

## Operate

- Start by confirming: goal, scope, constraints (Go version, platform, deps), non-functional requirements (latency/throughput/SLO), and “done”.
- Prefer small, end-to-end changes with tests; keep diffs easy to review (unless the user asks otherwise).
- Stdlib-first and “boring” solutions by default; add dependencies only when constraints justify them.
- Explain tradeoffs briefly; keep output actionable (commands, file paths, checklists).

> The goal is not “it works locally”, but “it survives production”: clear boundaries, observable behavior, secure defaults, and low ops cost.

## Default Go Standards

- Keep packages cohesive; avoid “util” grab-bags; name packages by responsibility, not type.
- Export only what must be used externally; keep APIs minimal and stable.
- Use `context.Context` for cancellation/timeouts at boundaries; pass `ctx` as first arg.
- Return errors, do not log-and-return the same error; wrap with `%w` for context.
- Avoid global state; prefer dependency injection via constructors and interfaces.
- Avoid premature interfaces; introduce interfaces at the consumer boundary.
- Concurrency: avoid shared mutable state; prefer channels for coordination, mutexes for invariants; always handle cancellation and shutdown.

## “Bad vs Good” (common production pitfalls)

```go
// ❌ BAD: log-and-return (double logging), no useful context
if err != nil {
    slog.Error("create user failed", "err", err)
    return err
}

// ✅ GOOD: log once at the boundary; wrap error with context
if err != nil {
    return fmt.Errorf("create user: %w", err)
}
```

## Workflow (Feature / Refactor / Bug)

1. Reproduce or specify behavior (tests first if feasible).
2. Sketch design: public API, package boundaries, data shapes, failure modes, concurrency model.
3. Implement smallest slice end-to-end.
4. Add/adjust tests and benchmarks (when performance-sensitive).
5. Validate: formatting, vet, tests, race (when relevant).
6. Review for production readiness: config, logging, metrics, timeouts, retries, shutdown.

## Validation Commands

- Run `gofmt -w (go list -f '{{.Dir}}' ./...)` (PowerShell: `gofmt -w @(go list -f '{{.Dir}}' ./...)`) and ensure no diffs remain.
- Run `go test ./...`.
- Run `go test -race ./...` for concurrent code or servers (where supported).
- Run `go test -run TestName -count=1 ./path` to avoid cached results when debugging.
- Run `go test -bench . -benchmem ./...` for hotspots.
- If available, run `golangci-lint run` (or `golangci-lint run --fast-only` during local iteration).
- If available, run `govulncheck ./...` (or `govulncheck -test ./...`) before release.

If you want PowerShell entrypoints:
- sanity: `scripts/go_sanity.ps1`
- security/vuln: `scripts/go_security.ps1`

## Project Structure & Dependencies

See [references/project-structure.md](references/project-structure.md) for pragmatic layouts by project size, dependency direction guidance, and package naming heuristics.

## Tooling (Up-to-date defaults)

See [references/tooling.md](references/tooling.md) for a safe baseline linter set, handling false positives, and configuration patterns.

## Advanced Topics (Production)

Use these when the project demands “senior+” rigor (many sections include ❌/✅ patterns):

- Arsitektur & boundaries: [references/architecture.md](references/architecture.md)
- Principal playbook (casebook + decision tree): [references/principal-playbook.md](references/principal-playbook.md)
- Coding standards (review-required): [references/coding-standards.md](references/coding-standards.md)
- Anti-patterns & bug traps: [references/anti-patterns.md](references/anti-patterns.md)
- Concurrency (race/leak/backpressure): [references/concurrency.md](references/concurrency.md)
- Errors & taxonomy: [references/errors.md](references/errors.md)
- HTTP API & status codes: [references/http-api.md](references/http-api.md)
- Frameworks (Gin/Fiber/Beego): [references/frameworks.md](references/frameworks.md)
- Database & queries: [references/database.md](references/database.md)
- Query engineering (Postgres/SQLC): [references/query-engineering.md](references/query-engineering.md)
- Auth (sessions/JWT/OAuth2): [references/auth.md](references/auth.md)
- Outbound HTTP & SSRF hardening: [references/outbound-http.md](references/outbound-http.md)
- Idempotency & outbox: [references/idempotency-outbox.md](references/idempotency-outbox.md)
- Security: [references/security.md](references/security.md)
- Reliability (timeouts, retries, backpressure): [references/reliability.md](references/reliability.md)
- Observability (OTel, correlation): [references/observability.md](references/observability.md)
- Log/trace correlation: [references/log-correlation.md](references/log-correlation.md)
- OTel bootstrap: [references/otel-bootstrap.md](references/otel-bootstrap.md)
- Performance (pprof/trace/allocs): [references/performance.md](references/performance.md)
- Testing advanced: [references/testing-advanced.md](references/testing-advanced.md)
- Distributed systems: [references/distributed-systems.md](references/distributed-systems.md)
- Examples (real-world skeleton): [references/examples.md](references/examples.md)
- Patterns (DI/options/circuit-breaker): [references/patterns.md](references/patterns.md)
- Snippets (copy/paste-safe): [references/snippets.md](references/snippets.md)

## Service/HTTP Defaults

- Set timeouts: server `ReadHeaderTimeout`, client `Timeout`/transport timeouts; avoid unbounded requests.
- Always implement graceful shutdown: close listeners, stop accepting, drain, cancel contexts, waitgroups.
- Prefer structured logs; include request IDs; avoid logging secrets/PII.
- Add health endpoints (`/healthz`, `/readyz`) and basic metrics hooks.

## Docker & Release Defaults

See [references/docker.md](references/docker.md) for secure, reproducible Docker patterns (multi-stage builds, non-root, no `latest`, health checks).

## Data & Persistence Defaults

- Validate inputs at the boundary; normalize early.
- Make error taxonomy explicit (not found, conflict, invalid, unavailable).
- Prefer migrations and explicit schemas; keep transactional boundaries clear.
- Keep domain logic independent of transport (HTTP/GRPC/CLI) where feasible.

## Debugging & Performance

- Use `pprof` and benchmarks for performance claims; measure before/after.
- Watch allocations; prefer `strings.Builder`, `bytes.Buffer`, preallocation when proven necessary.
- Avoid reflection-heavy paths in hot loops unless unavoidable.

## Security Checklist (Minimum)

- Validate and bound untrusted input (size, depth, time).
- Use `crypto/rand` for security tokens; never roll your own crypto.
- Store secrets in env/secret managers; never log secrets.
- Prefer least privilege and explicit allowlists for network/file operations.

## Library Selection (Practical)

See [references/libraries.md](references/libraries.md) for a conservative shortlist (stdlib-first) plus config/env decoding examples.

## Code Review Checklist

See [references/checklists.md](references/checklists.md) and [references/code-review.md](references/code-review.md) for PR checklists (API, concurrency, testing, ops).

## Snippets

See [references/snippets.md](references/snippets.md) for copy/paste-safe patterns (graceful shutdown, context plumbing, worker pools).

## Scripts

- `scripts/go_sanity.ps1` - runs `gofmt`, `go test`, `go vet`, optional `-race`, and `golangci-lint` if installed.
- `scripts/go_security.ps1` - runs `govulncheck` + quick hardening checks (and optional `gosec`/`staticcheck` if installed).
- `scripts/init_project.py` - bootstraps a clean Go project skeleton (optional).
