---
name: laravel:brainstorming
description: Interactive design refinement tailored to Laravel projects; clarify domain, data, interfaces, testing, and quality gates while accounting for Sail/non‑Sail environments
---

# Brainstorming (Laravel)

Use this when shaping features or refactors. Keep answers concise, then propose a design and gather confirmation before planning.

## Ask (one at a time)

- Goal: What outcome should users achieve?
- Domain: Which bounded contexts or packages are involved?
- Data: New models/relations? Required queries and invariants?
- Interfaces: HTTP/API/CLI? Required inputs/outputs? Authz?
- Side‑effects: Email, storage, queues, external systems?
- Performance: Throughput, latency, pagination, N+1 risks?
- Observability: Logs, metrics, events, failure handling?
- Testing: TDD entry point, fixtures/factories, edge cases?
- Environment: Sail or host? DB/cache/mail/storage availability?

## Propose

Present a design of 200–300 words, covering:
- Routes/contracts, validation, DTOs/transformers
- Services (ports+adapters, strategies/pipelines)
- Data model changes and migrations
- Jobs/events/listeners where relevant
- Test strategy (feature/unit), factories and seeds
- Quality gates and rollout plan

## Prepare Next Steps

Suggest a short implementation plan; then use `laravel:writing-plans` to formalize it.

