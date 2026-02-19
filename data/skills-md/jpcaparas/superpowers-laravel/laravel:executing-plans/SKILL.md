---
name: laravel:executing-plans
description: Execute Laravel plans in small batches with checkpoints—TDD first, migrations safe, queues verified, and quality gates enforced
---

# Executing Plans (Laravel)

Work in small batches. After each batch: tests green, quality clean, checkpoints recorded.

## Loop

1) Pick next small task
2) Write failing test (feature or unit)
3) Minimal implementation; commit
4) Verify queues/events/IO if applicable
5) Run Pint, static analysis, tests (parallel)
6) Update docs/notes; checkpoint

## Checkpoints

- Tests pass locally; no errors/warnings
- Pint clean; static analysis passes
- Migrations safe and idempotent; no breaking edits to merged migrations
- Queues healthy; Horizon metrics reasonable if used
- Feature branch notes updated (what changed, why)

Repeat until plan complete, then run `laravel:quality-checks` and request review.

