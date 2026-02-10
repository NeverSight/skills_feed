---
name: laravel:runner-selection
description: Choose Sail automatically when available, fall back cleanly to host PHP/Composer/Node; paired command map for both environments
---

# Runner Selection for Laravel Commands

Use Sail when present for environment consistency. Fall back to host tools when Sail is unavailable. Detect once, then stick to the choice for the session.

## Detecting Sail

```
# Best-effort alias; safe in any repo
alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'

# Is Sail usable?
[ -f ./sail ] || [ -x ./vendor/bin/sail ] && echo "Sail available" || echo "Sail not found"
```

If Sail is unavailable, use host `php`, `composer`, and your local Node (pnpm/npm/yarn). Keep versions aligned with your project.

## Command Pairs

Use the left command if Sail is available; otherwise use the right.

- `sail artisan about`   | `php artisan about`
- `sail artisan test`    | `php artisan test`
- `sail artisan migrate` | `php artisan migrate`
- `sail composer install`| `composer install`
- `sail composer require vendor/package` | `composer require vendor/package`
- `sail pnpm install`    | `pnpm install`
- `sail pnpm run dev`    | `pnpm run dev`
- `sail mysql`           | `mysql` (with matching DSN/env)
- `sail redis`           | `redis-cli`

## Safety Notes

- Never mix hosts: don’t install PHP deps with Composer on host and then run them inside Sail (or vice versa). Pick one runtime per session.
- Prefer non-interactive commands in automations/agents; provide flags instead of prompts.
- Treat DB-destructive commands (`migrate:fresh`, `down -v`) with care.

