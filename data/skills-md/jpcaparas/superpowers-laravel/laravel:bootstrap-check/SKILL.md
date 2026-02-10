---
name: laravel:bootstrap-check
description: Detect Sail/non‑Sail and print the right command pairs for your environment; verify dependencies and key services are reachable
---

# Bootstrap Check (Laravel)

Quickly determine if the project should run with Sail or host tools, then list the correct commands for this session.

## Detect Runner

Run this snippet in your project root:

```bash
if [ -f sail ] || [ -x vendor/bin/sail ]; then
  echo "Sail detected. Use: sail artisan|composer|pnpm ...";
else
  echo "Sail not found. Use host tools: php artisan, composer, pnpm ...";
fi
```

Optional portable alias:

```bash
alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'
```

## Command Pairs

- `sail artisan about`    | `php artisan about`
- `sail artisan test`     | `php artisan test`
- `sail artisan migrate`  | `php artisan migrate`
- `sail composer install` | `composer install`
- `sail pnpm install`     | `pnpm install`
- `sail pnpm run dev`     | `pnpm run dev`

## Service Smoke Checks

- DB: `sail mysql -e 'select 1'` or `mysql -e 'select 1'`
- Cache: `sail redis ping` or `redis-cli ping`

