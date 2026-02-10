---
name: laravel:horizon:metrics-and-dashboards
description: Operate Horizon with confidence—naming, tags, concurrency, failure handling, actionable metrics, and dashboards
---

# Horizon: Metrics and Dashboards

Make queues observable and actionable via Horizon.

## Naming & Tags

- Use named queues (e.g., `high`, `default`, `low`); route jobs intentionally
- Tag jobs with domain identifiers (user ID, aggregate ID) for tracing

## Workers & Concurrency

- Right‑size `--max-time`, `--tries`, `--backoff`
- Separate critical queues into dedicated supervisors

## Failures

- Use `failed()` method/logging with structured context
- Idempotency—ensure safe retries (unique keys, upserts, guards)

## Metrics & Dashboards

- Track: throughput, runtime distribution, retries, failure rate, time‑to‑handle
- Add health indicators for backlog and SLA thresholds
- Integrate with your APM where possible

## Testing

- Use `Bus::fake()` for dispatch assertions
- Integration tests to verify side‑effects and tags

