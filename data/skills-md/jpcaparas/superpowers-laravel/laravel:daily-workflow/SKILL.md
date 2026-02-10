---
name: laravel:daily-workflow
description: Practical daily checklist for Laravel projects; bring services up, run migrations, queues, quality gates, and tests
---

# Daily Workflow (Laravel)

Run through this checklist at the start of a session or before handoff.

```
# Start services
sail up -d && sail ps                     # Sail
# or (non‑Sail): ensure PHP/DB are running locally

# Schema as needed
sail artisan migrate                      # or: php artisan migrate

# Queue worker if required
sail artisan queue:work --tries=3         # or: php artisan queue:work --tries=3

# Quality gates
sail pint --test && sail pint             # or: vendor/bin/pint --test && vendor/bin/pint
sail artisan test --parallel              # or: php artisan test --parallel

# Frontend (if present)
sail pnpm run lint && sail pnpm run types # or: pnpm run lint && pnpm run types
```
