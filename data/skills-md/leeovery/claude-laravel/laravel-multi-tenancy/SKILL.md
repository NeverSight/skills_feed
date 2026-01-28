---
name: laravel-multi-tenancy
description: Multi-tenant application architecture patterns. Use when working with multi-tenant systems, tenant isolation, or when user mentions multi-tenancy, tenants, tenant scoping, tenant isolation, multi-tenant.
---

# Laravel Multi-Tenancy

Multi-tenancy separates application logic into **central** (non-tenant) and **tenanted** (tenant-specific) contexts.

**Related guides:**
- [tenancy-testing.md](references/tenancy-testing.md) - Testing multi-tenant features
- [Actions](../laravel-actions/SKILL.md) - Central vs Tenanted action organization
- [Models](../laravel-models/SKILL.md) - Model organization
- [structure.md](../laravel-architecture/references/structure.md) - Directory organization

## Philosophy

Multi-tenancy provides:
- **Clear separation** between central and tenant contexts
- **Database isolation** with separate databases per tenant
- **Automatic scoping** of queries to current tenant
- **Context awareness** through helper classes
- **Queue integration** with tenant context preservation

## When to Use

**Use multi-tenancy when:**
- Building SaaS applications with complete data isolation
- Each customer needs their own database
- Compliance requires strict data separation

**Don't use when:**
- Simple user segmentation is sufficient (use user_id scoping)
- All customers share the same schema
- Application complexity doesn't justify the overhead

## Directory Structure

```
app/
├── Actions/
│   ├── Central/          # Non-tenant actions
│   │   ├── Tenant/
│   │   │   ├── CreateTenantAction.php
│   │   │   └── DeleteTenantAction.php
│   │   └── User/
│   │       └── CreateCentralUserAction.php
│   └── Tenanted/         # Tenant-specific actions
│       ├── Order/
│       │   └── CreateOrderAction.php
│       └── Customer/
│           └── CreateCustomerAction.php
├── Data/
│   ├── Central/          # Central DTOs
│   └── Tenanted/         # Tenant DTOs
├── Http/
│   ├── Central/          # Central routes (tenant management)
│   ├── Web/              # Tenant application routes
│   └── Api/              # Public API (tenant-scoped)
├── Models/               # All models in standard location
│   ├── Tenant.php        # Central model
│   ├── Order.php         # Tenanted model
│   └── Customer.php
└── Support/
    └── TenantContext.php
```

## Central Actions

**Central actions** manage tenants and cross-tenant operations.

```php
<?php

declare(strict_types=1);

namespace App\Actions\Central\Tenant;

use App\Data\Central\CreateTenantData;
use App\Models\Tenant;
use Illuminate\Support\Facades\DB;

class CreateTenantAction
{
    public function __construct(
        private readonly CreateTenantDatabaseAction $createDatabase,
    ) {}

    public function __invoke(CreateTenantData $data): Tenant
    {
        return DB::transaction(function () use ($data): Tenant {
            $this->guard($data);
            $tenant = $this->createTenant($data);
            ($this->createDatabase)($tenant);
            return $tenant;
        });
    }

    private function guard(CreateTenantData $data): void
    {
        throw_if(
            Tenant::where('domain', $data->domain)->exists(),
            TenantDomainAlreadyExistsException::forDomain($data->domain)
        );
    }

    private function createTenant(CreateTenantData $data): Tenant
    {
        return Tenant::create([
            'id' => $data->tenantId,
            'name' => $data->name,
            'domain' => $data->domain,
        ]);
    }
}
```

## Tenanted Actions

**Tenanted actions** operate within a specific tenant's context. All queries automatically scoped.

```php
<?php

declare(strict_types=1);

namespace App\Actions\Tenanted\Order;

use App\Data\Tenanted\CreateOrderData;
use App\Models\Order;
use App\Models\User;
use Illuminate\Support\Facades\DB;

class CreateOrderAction
{
    public function __invoke(User $user, CreateOrderData $data): Order
    {
        return DB::transaction(function () use ($user, $data): Order {
            // Automatically scoped to current tenant
            $order = $user->orders()->create([
                'status' => $data->status,
                'total' => $data->total,
            ]);

            $this->createOrderItems($order, $data->items);
            return $order;
        });
    }

    private function createOrderItems(Order $order, array $items): void
    {
        foreach ($items as $item) {
            $order->items()->create([
                'product_id' => $item->productId,
                'quantity' => $item->quantity,
                'price' => $item->price,
            ]);
        }
    }
}
```

## Tenant Context Helper

```php
<?php

declare(strict_types=1);

namespace App\Support;

use App\Models\Tenant;
use Stancl\Tenancy\Facades\Tenancy;

class TenantContext
{
    public static function current(): ?Tenant
    {
        return Tenancy::tenant();
    }

    public static function id(): ?string
    {
        return Tenancy::tenant()?->getTenantKey();
    }

    public static function isActive(): bool
    {
        return Tenancy::tenant() !== null;
    }

    public static function run(Tenant $tenant, callable $callback): mixed
    {
        return tenancy()->runForMultiple([$tenant], $callback);
    }

    public static function runCentral(callable $callback): mixed
    {
        return tenancy()->runForMultiple([], $callback);
    }
}
```

**Usage:**

```php
use App\Support\TenantContext;

$tenant = TenantContext::current();
$tenantId = TenantContext::id();

if (TenantContext::isActive()) {
    // Tenant-specific logic
}

TenantContext::run($tenant, function () {
    Order::create([...]);
});

TenantContext::runCentral(function () {
    Tenant::create([...]);
});
```

## Tenant Identification Middleware

### Domain-Based

```php
use Stancl\Tenancy\Middleware\InitializeTenancyByDomain;

class IdentifyTenant extends InitializeTenancyByDomain
{
    // Tenant identified by domain (e.g., tenant1.myapp.com)
}
```

### Subdomain-Based

```php
use Stancl\Tenancy\Middleware\InitializeTenancyBySubdomain;

class IdentifyTenant extends InitializeTenancyBySubdomain
{
    // Tenant identified by subdomain
}
```

### Header-Based

```php
use Stancl\Tenancy\Middleware\InitializeTenancyByRequestData;

class IdentifyTenant extends InitializeTenancyByRequestData
{
    public static string $header = 'X-Tenant';
}
```

## Route Configuration

### Tenant Routes

```php
// routes/tenant.php
Route::middleware(['tenant'])->group(function () {
    Route::get('/orders', [OrderController::class, 'index']);
    Route::post('/orders', [OrderController::class, 'store']);
});
```

### Central Routes

```php
// routes/central.php
Route::middleware(['central'])->prefix('central')->group(function () {
    Route::get('/tenants', [TenantController::class, 'index']);
    Route::post('/tenants', [TenantController::class, 'store']);
});
```

### Bootstrap Configuration

```php
return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(function () {
        Route::middleware('web')
            ->prefix('central')
            ->name('central.')
            ->group(base_path('routes/central.php'));

        Route::middleware(['web', 'tenant'])
            ->group(base_path('routes/tenant.php'));
    })
    ->create();
```

## Models

All models live in `app/Models/`. Central vs tenanted distinguished by traits/interfaces, not subdirectories.

### Central Model

```php
<?php

declare(strict_types=1);

namespace App\Models;

use Stancl\Tenancy\Database\Models\Tenant as BaseTenant;

class Tenant extends BaseTenant
{
    public function users(): HasMany
    {
        return $this->hasMany(User::class);
    }
}
```

### Tenanted Model

```php
<?php

declare(strict_types=1);

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Order extends Model
{
    // Automatically scoped to current tenant
    // No tenant_id needed in queries

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
```

## Queue Jobs with Tenant Context

**Jobs must preserve tenant context** when queued.

```php
<?php

declare(strict_types=1);

namespace App\Jobs\Tenanted;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Stancl\Tenancy\Contracts\TenantWithDatabase;
use Stancl\Tenancy\Jobs\TenantAwareJob;

class ProcessOrderJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, TenantAwareJob;

    public function __construct(
        public TenantWithDatabase $tenant,
        public OrderData $orderData,
    ) {
        $this->onQueue('orders');
    }

    public function handle(ProcessOrderAction $action): void
    {
        // Runs in tenant context automatically
        $action($this->orderData);
    }
}
```

**Dispatching:**

```php
ProcessOrderJob::dispatch(TenantContext::current(), $orderData);
```

## Common Patterns

### Running Code in Multiple Tenants

```php
$tenants = Tenant::all();

foreach ($tenants as $tenant) {
    TenantContext::run($tenant, function () use ($tenant) {
        Order::where('status', 'pending')->update(['processed' => true]);
    });
}
```

### Accessing Central Data from Tenant Context

```php
TenantContext::runCentral(function () {
    $allTenants = Tenant::all();
});
```

### Conditional Logic Based on Tenant

```php
if (TenantContext::isActive()) {
    $orders = Order::all(); // Scoped to tenant
} else {
    $tenants = Tenant::all(); // Central
}
```

## Testing

**[→ Complete testing guide: tenancy-testing.md](references/tenancy-testing.md)**

Includes:
- Testing central and tenanted actions
- ManagesTenants and RefreshDatabaseWithTenant traits
- TenantTestCase setup
- Pest configuration for multi-tenancy
- Test directory structure

## Summary

**Multi-tenancy provides:**
1. **Clear separation** - Central vs Tenanted namespaces
2. **Database isolation** - Each tenant has dedicated database
3. **Automatic scoping** - Queries automatically tenant-scoped
4. **Context helpers** - Easy access to tenant context
5. **Queue integration** - Jobs preserve tenant context

**Best practices:**
- Use directory structure to separate central and tenanted actions/DTOs
- Keep models in `app/Models/` following Laravel convention
- Always use TenantContext helper for tenant access
- Test both central and tenant contexts separately
- Preserve tenant context in queued jobs
