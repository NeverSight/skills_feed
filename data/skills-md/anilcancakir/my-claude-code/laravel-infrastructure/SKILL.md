---
name: laravel-infrastructure
description: "Laravel Horizon queues, Octane performance, Reverb WebSockets, Redis caching, PostgreSQL database. ALWAYS activate when: working with queue jobs, cache, sessions, broadcasting, database performance, supervisor, worker. Triggers on: job failed, queue stuck, cache not clearing, Redis connection, broadcast event, WebSocket, real-time, Horizon dashboard, Octane memory leak, slow query, N+1, database timeout, connection refused, kuyruk çalışmıyor, cache temizlenmiyor, job başarısız, worker durdu, broadcast çalışmıyor, real-time gelmiyor."
---

# Laravel Infrastructure

Horizon, Octane, Reverb, Redis, and PostgreSQL patterns for Laravel 12+.

## Horizon (Queue Management)

### Installation

```bash
composer require laravel/horizon
php artisan horizon:install
php artisan migrate
```

### Configuration

```php
// config/horizon.php
'environments' => [
    'production' => [
        'supervisor-1' => [
            'connection' => 'redis',
            'queue' => ['default', 'high', 'low'],
            'balance' => 'auto',
            'maxProcesses' => 10,
            'minProcesses' => 1,
            'memory' => 128,
            'tries' => 3,
            'timeout' => 60,
        ],
    ],
    'local' => [
        'supervisor-1' => [
            'connection' => 'redis',
            'queue' => ['default'],
            'balance' => 'simple',
            'processes' => 3,
            'tries' => 3,
        ],
    ],
],
```

### Running Horizon

```bash
# Development
php artisan horizon

# Production (with Supervisor)
# /etc/supervisor/conf.d/horizon.conf
[program:horizon]
process_name=%(program_name)s
command=php /var/www/app/artisan horizon
autostart=true
autorestart=true
user=www-data
redirect_stderr=true
stdout_logfile=/var/www/app/storage/logs/horizon.log
stopwaitsecs=3600
```

### Dispatching Jobs

```php
// Dispatch to specific queue
ProcessOrder::dispatch($order)->onQueue('high');

// Delayed dispatch
ProcessOrder::dispatch($order)->delay(now()->addMinutes(5));

// Chain jobs
Bus::chain([
    new ProcessOrder($order),
    new SendConfirmation($order),
    new NotifyWarehouse($order),
])->dispatch();
```

---

## Octane (High Performance)

### Installation

```bash
composer require laravel/octane
php artisan octane:install

# Choose: Swoole or RoadRunner
```

### Running

```bash
# Development
php artisan octane:start --watch

# Production
php artisan octane:start --workers=4 --task-workers=6
```

### Important: Memory Leaks

```php
// AVOID: Static properties accumulating data
class BadService
{
    private static array $cache = [];  // Memory leak!
}

// GOOD: Use request-scoped or proper cache
class GoodService
{
    public function __construct(
        private readonly Repository $cache
    ) {}
}
```

### Octane-Safe Patterns

```php
// Reset singletons between requests
// AppServiceProvider
public function register(): void
{
    $this->app->singleton(ShoppingCart::class, function ($app) {
        return new ShoppingCart();
    });
}

// In Octane config
'flush' => [
    ShoppingCart::class,
],
```

---

## Reverb (WebSockets)

### Installation

```bash
composer require laravel/reverb
php artisan reverb:install
```

### Configuration

```env
BROADCAST_DRIVER=reverb
REVERB_APP_ID=my-app
REVERB_APP_KEY=my-key
REVERB_APP_SECRET=my-secret
REVERB_HOST=localhost
REVERB_PORT=8080
```

### Running

```bash
php artisan reverb:start
```

### Broadcasting Events

```php
<?php

namespace App\Events;

use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Foundation\Events\Dispatchable;

class OrderStatusUpdated implements ShouldBroadcast
{
    use Dispatchable, InteractsWithSockets;

    public function __construct(
        public Order $order
    ) {}

    public function broadcastOn(): array
    {
        return [
            new Channel('orders.' . $this->order->id),
        ];
    }

    public function broadcastAs(): string
    {
        return 'status.updated';
    }
}
```

### Frontend (Laravel Echo)

```js
Echo.channel('orders.123')
    .listen('.status.updated', (event) => {
        console.log('Order status:', event.order.status);
    });
```

---

## Redis

### Caching

```php
use Illuminate\Support\Facades\Cache;

// Store
Cache::put('key', 'value', now()->addMinutes(10));
Cache::forever('key', 'value');

// Retrieve
$value = Cache::get('key', 'default');
$value = Cache::remember('key', 60, fn () => expensive());

// Remove
Cache::forget('key');
Cache::flush();

// Tags
Cache::tags(['users', 'orders'])->put('user:1:orders', $orders, 60);
Cache::tags(['users'])->flush();
```

### Sessions

```env
SESSION_DRIVER=redis
```

### Locks

```php
$lock = Cache::lock('processing-order-' . $orderId, 10);

if ($lock->get()) {
    try {
        // Process order
    } finally {
        $lock->release();
    }
}
```

---

## PostgreSQL

### Configuration

```env
DB_CONNECTION=pgsql
DB_HOST=127.0.0.1
DB_PORT=5432
DB_DATABASE=myapp
DB_USERNAME=postgres
DB_PASSWORD=secret
```

### PostgreSQL-Specific Features

```php
// JSONB columns
Schema::create('settings', function (Blueprint $table) {
    $table->id();
    $table->jsonb('data')->default('{}');
    $table->index('data', 'settings_data_gin')->using('gin');
});

// Query JSONB
$users = User::whereJsonContains('settings->notifications', 'email')->get();
$users = User::where('settings->theme', 'dark')->get();

// Full-text search
$products = Product::whereFullText('name', 'laptop')->get();
```

## References

| Topic | Reference | When to Load |
|-------|-----------|--------------|
| Horizon details | [references/horizon.md](references/horizon.md) | Supervisor, tags, batches |
| Octane caveats | [references/octane.md](references/octane.md) | Memory, concurrency |
| Reverb channels | [references/reverb.md](references/reverb.md) | Private/presence channels |

## Quick Commands

```bash
# Horizon
php artisan horizon
php artisan horizon:status
php artisan horizon:pause
php artisan horizon:continue
php artisan horizon:terminate

# Octane
php artisan octane:start
php artisan octane:reload
php artisan octane:stop

# Reverb
php artisan reverb:start

# Cache
php artisan cache:clear
php artisan config:cache
php artisan route:cache
```
