---
name: laravel:queues-and-horizon
description: Operate and verify queues with or without Horizon; safe worker flags, failure handling, and test strategies
---

# Queues and Horizon

Run workers safely, verify execution, and test job behavior.

## Commands

```
# Start worker
sail artisan queue:work --queue=high,default --tries=3 --backoff=5   # or: php artisan queue:work --queue=high,default --tries=3 --backoff=5

# Horizon (if installed)
sail artisan horizon                                               # or: php artisan horizon

# Failed jobs
sail artisan queue:failed                                          # or: php artisan queue:failed
sail artisan queue:retry all                                       # or: php artisan queue:retry all
```

## Patterns

- Use named queues for prioritization; keep defaults sane
- Add actionable `Log::warning`/`::error` with context in jobs
- Idempotency: make jobs safe to retry
- Emit metrics where possible; observe in Horizon or your APM

## Testing Jobs

- Use `Bus::fake()` to assert dispatching in unit tests
- Use integration tests to verify side-effects (DB/IO)
