---
name: debug:laravel
description: Debug Laravel applications systematically with this comprehensive troubleshooting skill. Covers class/namespace errors, database SQLSTATE issues, route problems (404/405), Blade template errors, middleware issues (CSRF/auth), queue job failures, and cache/session problems. Provides structured four-phase debugging methodology with Laravel Telescope, Debugbar, Artisan tinker, and logging best practices for development and production environments.
---

# Laravel Debugging Guide

## Overview

Debugging in Laravel requires understanding the framework's conventions, lifecycle, and tooling ecosystem. This guide provides a systematic approach to diagnosing and resolving Laravel issues, from simple configuration problems to complex runtime errors.

**Key Principles:**
- Always check logs first (`storage/logs/laravel.log`)
- Use appropriate tools for the environment (development vs production)
- Follow Laravel conventions - most errors stem from convention violations
- Isolate the problem layer (routing, middleware, controller, model, view)

## Common Error Patterns

### Class and Namespace Errors

**Class 'App\Http\Controllers\Controller' not found**
```php
// Problem: Missing base controller extension or incorrect namespace
// Solution: Ensure proper namespace and inheritance
namespace App\Http\Controllers;

use Illuminate\Routing\Controller as BaseController;

class YourController extends BaseController
{
    // ...
}
```

**Target class [ControllerName] does not exist**
```php
// Check routes/web.php or routes/api.php
// Laravel 8+ requires full namespace or route groups
use App\Http\Controllers\UserController;

Route::get('/users', [UserController::class, 'index']);

// Or use route group with namespace
Route::namespace('App\Http\Controllers')->group(function () {
    Route::get('/users', 'UserController@index');
});
```

### Database Errors (SQLSTATE)

**SQLSTATE[HY000] [1045] Access denied**
```bash
# Check .env database credentials
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=your_database
DB_USERNAME=your_username
DB_PASSWORD=your_password

# Clear config cache after changes
php artisan config:clear
```

**SQLSTATE[42S02] Table not found**
```bash
# Run migrations
php artisan migrate

# Check migration status
php artisan migrate:status

# Fresh database with seeders
php artisan migrate:fresh --seed
```

**QueryException with foreign key constraint**
```php
// Check migration order - parent tables must exist first
// Use Schema::disableForeignKeyConstraints() for fresh migrations
Schema::disableForeignKeyConstraints();
// ... your schema changes
Schema::enableForeignKeyConstraints();
```

### Route Errors

**404 Not Found - Route does not exist**
```bash
# List all registered routes
php artisan route:list

# Check specific route
php artisan route:list --name=users

# Clear route cache
php artisan route:clear
```

**MethodNotAllowedHttpException**
```php
// Wrong HTTP method for route
// Check route definition matches request method
Route::post('/submit', [FormController::class, 'store']);  // Expects POST
Route::put('/update/{id}', [FormController::class, 'update']);  // Expects PUT

// For HTML forms using PUT/PATCH/DELETE
<form method="POST" action="/update/1">
    @csrf
    @method('PUT')
</form>
```

### View Errors

**View [name] not found**
```bash
# Check view file exists at correct path
# resources/views/users/index.blade.php for view('users.index')

# Clear view cache
php artisan view:clear
```

**Undefined variable in view**
```php
// Ensure variable is passed from controller
return view('users.index', [
    'users' => $users,
    'total' => $total,
]);

// Or use compact()
return view('users.index', compact('users', 'total'));
```

### Middleware Issues

**TokenMismatchException (CSRF)**
```php
// Include @csrf in all POST/PUT/DELETE forms
<form method="POST" action="/submit">
    @csrf
    <!-- form fields -->
</form>

// For AJAX requests, include token in headers
$.ajaxSetup({
    headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
    }
});

// Exclude routes from CSRF if needed (VerifyCsrfToken middleware)
protected $except = [
    'stripe/*',
    'webhook/*',
];
```

**Unauthenticated / 403 Forbidden**
```bash
# Check middleware applied to route
php artisan route:list --columns=uri,middleware

# Verify auth guards in config/auth.php
# Check Gate/Policy definitions
```

### Queue and Job Failures

**Job failed without reason**
```bash
# Check failed jobs table
php artisan queue:failed

# Retry specific job
php artisan queue:retry <job-id>

# Retry all failed jobs
php artisan queue:retry all

# Clear failed jobs
php artisan queue:flush
```

**Jobs not processing**
```bash
# Ensure queue worker is running
php artisan queue:work

# Check queue connection in .env
QUEUE_CONNECTION=redis

# Restart queue after code changes
php artisan queue:restart
```

### Cache and Session Problems

**Session not persisting**
```bash
# Clear session files
php artisan session:clear

# Check session driver
SESSION_DRIVER=file  # or redis, database, etc.

# Verify storage permissions
chmod -R 775 storage/
chown -R www-data:www-data storage/
```

**Config/cache showing old values**
```bash
# Clear all caches
php artisan optimize:clear

# Or individually
php artisan config:clear
php artisan cache:clear
php artisan route:clear
php artisan view:clear
```

## Debugging Tools

### Laravel Telescope

The most comprehensive debugging tool for Laravel development.

**Installation:**
```bash
composer require laravel/telescope --dev
php artisan telescope:install
php artisan migrate
```

**Access:** Navigate to `/telescope` in your browser

**Key Features:**
- **Requests**: View all HTTP requests with headers, parameters, response
- **Exceptions**: Stack traces and context for all errors
- **Queries**: All SQL queries with execution time and bindings
- **Jobs**: Queue job payloads, execution times, failures
- **Logs**: All log entries in real-time
- **Mail**: Preview sent emails with content
- **Cache**: Track cache hits, misses, and operations
- **Events**: All dispatched events and listeners

**Security:** Limit access in production via `TelescopeServiceProvider`:
```php
protected function gate()
{
    Gate::define('viewTelescope', function ($user) {
        return in_array($user->email, [
            'admin@example.com',
        ]);
    });
}
```

### Laravel Debugbar

Quick inline debugging for web pages.

**Installation:**
```bash
composer require barryvdh/laravel-debugbar --dev
```

**Features:**
- Query count and execution time
- Route information
- View rendering time
- Memory usage
- Timeline visualization

### Ray by Spatie

Desktop app for non-intrusive debugging.

**Installation:**
```bash
composer require spatie/laravel-ray --dev
```

**Usage:**
```php
ray($variable);                    // Send to Ray app
ray($var1, $var2)->green();        // Color coded
ray()->measure();                  // Start timer
ray()->pause();                    // Pause execution
ray()->showQueries();              // Show all queries
```

### Built-in Debugging Functions

```php
// Dump and Die - stops execution
dd($variable);
dd($user, $posts, $comments);

// Dump without dying
dump($variable);

// Dump, Die, Debug (with extra info)
ddd($variable);

// In Blade templates
@dd($variable)
@dump($variable)

// Log to file
Log::debug('Message', ['context' => $data]);
Log::info('User logged in', ['user_id' => $user->id]);
Log::error('Payment failed', ['order' => $order]);

// Log levels: emergency, alert, critical, error, warning, notice, info, debug
```

### Artisan Tinker

Interactive REPL for testing code:
```bash
php artisan tinker

# Test Eloquent queries
>>> User::where('active', true)->count()
=> 42

# Test relationships
>>> $user = User::find(1)
>>> $user->posts()->count()

# Test services
>>> app(UserService::class)->processUser($user)
```

## The Four Phases of Laravel Debugging

### Phase 1: Root Cause Investigation

**Check Logs First:**
```bash
# View latest errors
tail -f storage/logs/laravel.log

# Search for specific errors
grep -i "error\|exception" storage/logs/laravel.log | tail -50

# Check with specific date
cat storage/logs/laravel-2025-01-11.log
```

**Verify Configuration:**
```bash
# Check current environment
php artisan env

# Dump all config values
php artisan config:show

# Check specific config
php artisan config:show database
php artisan config:show queue

# Validate .env file
php artisan config:clear && php artisan config:cache
```

**Check Application State:**
```bash
# Check if app is in maintenance mode
php artisan up  # or down

# Check scheduled tasks
php artisan schedule:list

# Check registered routes
php artisan route:list

# Check registered events
php artisan event:list
```

### Phase 2: Pattern Analysis

**Compare with Laravel Conventions:**

| Component | Convention | Common Mistake |
|-----------|------------|----------------|
| Models | `App\Models\User` (singular) | Using plural names |
| Controllers | `UserController` | Missing `Controller` suffix |
| Migrations | `create_users_table` (plural) | Singular table names |
| Views | `resources/views/users/index.blade.php` | Wrong directory structure |
| Routes | RESTful naming | Non-standard HTTP methods |

**Check for Common Anti-patterns:**
```php
// BAD: N+1 query problem
$users = User::all();
foreach ($users as $user) {
    echo $user->profile->bio;  // Query per iteration!
}

// GOOD: Eager loading
$users = User::with('profile')->get();
foreach ($users as $user) {
    echo $user->profile->bio;  // No additional queries
}
```

**Verify Dependencies:**
```bash
# Check composer dependencies
composer show

# Check for package conflicts
composer diagnose

# Update autoloader
composer dump-autoload
```

### Phase 3: Hypothesis and Testing

**Create Focused Tests:**
```php
// tests/Feature/UserTest.php
use Tests\TestCase;
use Illuminate\Foundation\Testing\RefreshDatabase;

class UserTest extends TestCase
{
    use RefreshDatabase;

    public function test_user_can_be_created()
    {
        $response = $this->post('/users', [
            'name' => 'Test User',
            'email' => 'test@example.com',
        ]);

        $response->assertStatus(201);
        $this->assertDatabaseHas('users', [
            'email' => 'test@example.com',
        ]);
    }
}
```

**Run Tests:**
```bash
# Run all tests
php artisan test

# Run specific test file
php artisan test tests/Feature/UserTest.php

# Run specific test method
php artisan test --filter=test_user_can_be_created

# Run with coverage
php artisan test --coverage

# Use Pest (if installed)
./vendor/bin/pest
```

**Test in Isolation:**
```bash
# Test artisan commands
php artisan tinker
>>> User::factory()->create()
>>> $user->notify(new WelcomeNotification)

# Test queue jobs synchronously
QUEUE_CONNECTION=sync php artisan your:command

# Test with fresh database
php artisan migrate:fresh --seed && php artisan test
```

### Phase 4: Implementation and Verification

**Apply Fix:**
```bash
# Clear all caches after changes
php artisan optimize:clear

# Rebuild autoloader
composer dump-autoload

# Restart queue workers
php artisan queue:restart

# Re-cache for production
php artisan config:cache
php artisan route:cache
php artisan view:cache
```

**Verify Fix:**
```bash
# Run full test suite
php artisan test

# Check for new errors in logs
tail -f storage/logs/laravel.log

# Monitor queue processing
php artisan queue:work --verbose

# Check application health
php artisan about
```

## Quick Reference Commands

### Clearing and Caching

```bash
# Clear everything
php artisan optimize:clear

# Individual clears
php artisan config:clear      # Config cache
php artisan route:clear       # Route cache
php artisan view:clear        # Compiled views
php artisan cache:clear       # Application cache
php artisan event:clear       # Event cache

# Rebuild caches (production)
php artisan config:cache
php artisan route:cache
php artisan view:cache
php artisan event:cache
```

### Database Commands

```bash
# Migration status
php artisan migrate:status

# Run migrations
php artisan migrate

# Rollback last migration
php artisan migrate:rollback

# Fresh database with seeds
php artisan migrate:fresh --seed

# Show database info
php artisan db:show

# Open database CLI
php artisan db
```

### Queue Commands

```bash
# Check failed jobs
php artisan queue:failed

# Retry failed job
php artisan queue:retry <id>

# Retry all failed
php artisan queue:retry all

# Clear failed jobs
php artisan queue:flush

# Work queue
php artisan queue:work --verbose

# Restart workers (after code changes)
php artisan queue:restart
```

### Route Commands

```bash
# List all routes
php artisan route:list

# Filter by name
php artisan route:list --name=api

# Filter by path
php artisan route:list --path=users

# Show columns
php artisan route:list --columns=method,uri,name,action
```

### Debugging Commands

```bash
# Show app info
php artisan about

# Interactive shell
php artisan tinker

# Check environment
php artisan env

# Show config
php artisan config:show

# Schedule list
php artisan schedule:list
```

## Environment-Specific Debugging

### Development

```env
APP_DEBUG=true
APP_ENV=local
LOG_CHANNEL=stack
LOG_LEVEL=debug
```

Enable all debugging tools:
- Laravel Telescope
- Laravel Debugbar
- Ray

### Production

```env
APP_DEBUG=false
APP_ENV=production
LOG_CHANNEL=stack
LOG_LEVEL=error
```

Use:
- Error tracking services (Sentry, Bugsnag)
- Log aggregation (Papertrail, Loggly)
- APM tools (New Relic, Scout)

**Never expose detailed errors in production.**

## Logging Best Practices

### Structured Logging

```php
// Include context with every log
Log::info('Order processed', [
    'order_id' => $order->id,
    'user_id' => $order->user_id,
    'total' => $order->total,
    'items_count' => $order->items->count(),
]);

// Use appropriate log levels
Log::debug('Detailed debugging info');      // Development only
Log::info('Normal operational events');     // User actions, etc.
Log::warning('Unusual but not errors');     // Deprecated usage, etc.
Log::error('Runtime errors');               // Exceptions, failures
Log::critical('System is unusable');        // Database down, etc.
```

### Custom Log Channels

```php
// config/logging.php
'channels' => [
    'payments' => [
        'driver' => 'daily',
        'path' => storage_path('logs/payments.log'),
        'level' => 'info',
        'days' => 30,
    ],
],

// Usage
Log::channel('payments')->info('Payment processed', ['id' => $payment->id]);
```

## Additional Resources

- [Laravel Official Documentation](https://laravel.com/docs)
- [Laravel Telescope Documentation](https://laravel.com/docs/telescope)
- [Laravel Debugbar GitHub](https://github.com/barryvdh/laravel-debugbar)
- [Spatie Ray Documentation](https://spatie.be/docs/ray)
- [Laravel News - Debugging Articles](https://laravel-news.com/debugging-and-logging-in-laravel-applications)
- [Sentry Laravel Integration](https://docs.sentry.io/platforms/php/guides/laravel/)
