---
name: laravel:task-scheduling
description: Schedule tasks with safety; use withoutOverlapping, onOneServer, and visibility settings for reliable cron execution
---

# Task Scheduling

Run scheduled tasks predictably across environments.

## Commands

```
// app/Console/Kernel.php
protected function schedule(Schedule $schedule): void
{
    $schedule->command('reports:daily')
        ->dailyAt('01:00')
        ->withoutOverlapping()
        ->onOneServer()
        ->runInBackground()
        ->evenInMaintenanceMode();
}

# Run the scheduler from cron
* * * * * cd /var/www/app && php artisan schedule:run >> /dev/null 2>&1
```

## Patterns

- Guard long-running commands with `withoutOverlapping()`
- Use `onOneServer()` when running on multiple nodes
- Emit logs/metrics for visibility; consider notifications on failure
- Feature-flag risky jobs via config/env

