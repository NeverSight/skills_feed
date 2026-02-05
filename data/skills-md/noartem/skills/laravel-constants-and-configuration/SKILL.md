---
name: laravel-constants-and-configuration
description: Replace hardcoded values with constants, enums, and configuration for maintainability; use PHP 8.1+ enums and config files
---

# Constants and Configuration Values

Avoid hardcoded values throughout your codebase. Use constants, configuration files, and enums to make your application more maintainable, refactorable, and debuggable.

## The Problem with Hardcoded Values

```php
// BAD: Magic numbers and strings scattered everywhere
if ($user->role === 'admin') { // What other roles exist?
    $cacheTime = 3600; // What does 3600 mean?
}

if ($order->status === 1) { // What does 1 represent?
    $discount = 0.15; // Why 15%?
}

Cache::remember('users_list', 600, fn() => ...); // 600 what?
```

## Solution 1: PHP Constants and Enums

### Class Constants

```php
// app/Constants/UserRole.php
class UserRole
{
    public const ADMIN = 'admin';
    public const EDITOR = 'editor';
    public const VIEWER = 'viewer';
    public const GUEST = 'guest';

    public const ALL = [
        self::ADMIN,
        self::EDITOR,
        self::VIEWER,
        self::GUEST,
    ];

    public static function hasPermission(string $role, string $action): bool
    {
        return match($role) {
            self::ADMIN => true,
            self::EDITOR => in_array($action, ['read', 'write', 'edit']),
            self::VIEWER => $action === 'read',
            self::GUEST => false,
            default => false,
        };
    }
}

// Usage
if ($user->role === UserRole::ADMIN) {
    // Clear intent
}
```

### PHP 8.1+ Enums

```php
// app/Enums/OrderStatus.php
enum OrderStatus: string
{
    case PENDING = 'pending';
    case PROCESSING = 'processing';
    case SHIPPED = 'shipped';
    case DELIVERED = 'delivered';
    case CANCELLED = 'cancelled';
    case REFUNDED = 'refunded';

    public function label(): string
    {
        return match($this) {
            self::PENDING => 'Pending Payment',
            self::PROCESSING => 'Processing',
            self::SHIPPED => 'Shipped',
            self::DELIVERED => 'Delivered',
            self::CANCELLED => 'Cancelled',
            self::REFUNDED => 'Refunded',
        };
    }

    public function color(): string
    {
        return match($this) {
            self::PENDING => 'yellow',
            self::PROCESSING => 'blue',
            self::SHIPPED => 'indigo',
            self::DELIVERED => 'green',
            self::CANCELLED => 'red',
            self::REFUNDED => 'gray',
        };
    }

    public function canTransitionTo(self $newStatus): bool
    {
        return match($this) {
            self::PENDING => in_array($newStatus, [
                self::PROCESSING,
                self::CANCELLED,
            ]),
            self::PROCESSING => in_array($newStatus, [
                self::SHIPPED,
                self::CANCELLED,
            ]),
            self::SHIPPED => $newStatus === self::DELIVERED,
            self::DELIVERED => $newStatus === self::REFUNDED,
            default => false,
        };
    }
}

// Model with enum casting
class Order extends Model
{
    protected $casts = [
        'status' => OrderStatus::class,
    ];

    public function transitionTo(OrderStatus $newStatus): void
    {
        if (!$this->status->canTransitionTo($newStatus)) {
            throw new InvalidStateTransition(
                "Cannot transition from {$this->status->value} to {$newStatus->value}"
            );
        }

        $this->update(['status' => $newStatus]);
    }
}

// Usage
$order->transitionTo(OrderStatus::PROCESSING);
```

## Solution 2: Configuration Files

### Application-Wide Settings

```php
// config/app.php
return [
    'cache_ttl' => [
        'short' => 60,      // 1 minute
        'medium' => 300,    // 5 minutes
        'long' => 3600,     // 1 hour
        'day' => 86400,     // 24 hours
    ],

    'pagination' => [
        'default' => 20,
        'max' => 100,
        'options' => [10, 20, 50, 100],
    ],

    'upload' => [
        'max_file_size' => 10 * 1024 * 1024, // 10MB
        'allowed_extensions' => ['jpg', 'jpeg', 'png', 'pdf', 'doc', 'docx'],
        'storage_path' => 'uploads',
    ],

    'business' => [
        'tax_rate' => 0.08,
        'shipping_threshold' => 50.00,
        'discount_tiers' => [
            'bronze' => 0.05,
            'silver' => 0.10,
            'gold' => 0.15,
            'platinum' => 0.20,
        ],
    ],
];

// Usage
Cache::remember(
    'products',
    config('app.cache_ttl.long'),
    fn() => Product::all()
);

$maxSize = config('app.upload.max_file_size');
```

### Feature-Specific Configuration

```php
// config/payment.php
return [
    'stripe' => [
        'key' => env('STRIPE_KEY'),
        'secret' => env('STRIPE_SECRET'),
        'webhook_secret' => env('STRIPE_WEBHOOK_SECRET'),
        'webhook_tolerance' => 300, // seconds
        'currency' => 'usd',
        'minimum_amount' => 50, // cents
    ],

    'retry' => [
        'max_attempts' => 3,
        'delay_seconds' => [5, 10, 30],
    ],

    'statuses' => [
        'pending' => 'pending',
        'processing' => 'processing',
        'succeeded' => 'succeeded',
        'failed' => 'failed',
    ],
];

// Usage in service
class PaymentService
{
    public function charge(int $amount): void
    {
        if ($amount < config('payment.stripe.minimum_amount')) {
            throw new InvalidAmountException('Amount below minimum');
        }

        // Process payment
    }
}
```

## Solution 3: Database-Driven Configuration

### Settings Model

```php
// app/Models/Setting.php
class Setting extends Model
{
    protected $fillable = ['key', 'value', 'type'];

    protected $casts = [
        'value' => 'json',
    ];

    public static function get(string $key, mixed $default = null): mixed
    {
        return Cache::remember(
            "settings.{$key}",
            config('app.cache_ttl.long'),
            fn() => static::where('key', $key)->first()?->value ?? $default
        );
    }

    public static function set(string $key, mixed $value): void
    {
        static::updateOrCreate(
            ['key' => $key],
            ['value' => $value]
        );

        Cache::forget("settings.{$key}");
    }

    protected static function booted(): void
    {
        static::saved(function ($setting) {
            Cache::forget("settings.{$setting->key}");
        });
    }
}

// Usage
$maintenanceMode = Setting::get('maintenance_mode', false);
$maxLoginAttempts = Setting::get('max_login_attempts', 5);
```

## Solution 4: Service Constants

```php
// app/Services/CacheService.php
class CacheService
{
    // Cache key patterns
    public const USER_KEY = 'user:%d';
    public const USER_POSTS_KEY = 'user:%d:posts';
    public const POST_KEY = 'post:%d';
    public const TRENDING_KEY = 'trending:%s:page:%d';

    // Cache tags
    public const TAG_USERS = 'users';
    public const TAG_POSTS = 'posts';
    public const TAG_COMMENTS = 'comments';

    public static function getUserKey(int $userId): string
    {
        return sprintf(self::USER_KEY, $userId);
    }

    public static function getUserPostsKey(int $userId): string
    {
        return sprintf(self::USER_POSTS_KEY, $userId);
    }

    public static function rememberUser(int $userId, Closure $callback)
    {
        return Cache::tags([self::TAG_USERS])->remember(
            self::getUserKey($userId),
            config('app.cache_ttl.medium'),
            $callback
        );
    }
}

// Usage
$user = CacheService::rememberUser($userId, fn() => User::find($userId));
```

## Solution 5: Validation Constants

```php
// app/Rules/ValidationRules.php
class ValidationRules
{
    public const NAME_REGEX = '/^[a-zA-Z\s\-\']+$/';
    public const PHONE_REGEX = '/^\+?[1-9]\d{1,14}$/';
    public const USERNAME_REGEX = '/^[a-zA-Z0-9_]{3,20}$/';
    public const SLUG_REGEX = '/^[a-z0-9\-]+$/';

    public const PASSWORD_MIN = 8;
    public const PASSWORD_MAX = 128;
    public const BIO_MAX = 500;
    public const COMMENT_MAX = 1000;

    public static function password(): array
    {
        return [
            'required',
            'string',
            'min:' . self::PASSWORD_MIN,
            'max:' . self::PASSWORD_MAX,
            Password::defaults(),
        ];
    }

    public static function username(): array
    {
        return [
            'required',
            'string',
            'regex:' . self::USERNAME_REGEX,
            'unique:users,username',
        ];
    }
}

// In FormRequest
public function rules(): array
{
    return [
        'username' => ValidationRules::username(),
        'password' => ValidationRules::password(),
        'bio' => ['nullable', 'string', 'max:' . ValidationRules::BIO_MAX],
    ];
}
```

## Solution 6: HTTP Status Constants

```php
// app/Http/Responses/ApiResponse.php
class ApiResponse
{
    // Standard HTTP codes as constants for clarity
    public const OK = 200;
    public const CREATED = 201;
    public const ACCEPTED = 202;
    public const NO_CONTENT = 204;
    public const BAD_REQUEST = 400;
    public const UNAUTHORIZED = 401;
    public const FORBIDDEN = 403;
    public const NOT_FOUND = 404;
    public const VALIDATION_ERROR = 422;
    public const SERVER_ERROR = 500;

    // Custom application codes
    public const CODE_SUCCESS = 1000;
    public const CODE_VALIDATION_FAILED = 2001;
    public const CODE_RESOURCE_NOT_FOUND = 2002;
    public const CODE_UNAUTHORIZED_ACTION = 2003;
    public const CODE_RATE_LIMITED = 2004;

    public static function success($data = null, string $message = 'Success'): JsonResponse
    {
        return response()->json([
            'success' => true,
            'code' => self::CODE_SUCCESS,
            'message' => $message,
            'data' => $data,
        ], self::OK);
    }

    public static function error(string $message, int $httpCode = self::BAD_REQUEST, int $appCode = null): JsonResponse
    {
        return response()->json([
            'success' => false,
            'code' => $appCode ?? $httpCode,
            'message' => $message,
        ], $httpCode);
    }
}

// Usage
return ApiResponse::success($user, 'User created successfully');
return ApiResponse::error('Resource not found', ApiResponse::NOT_FOUND);
```

## Solution 7: Queue Priorities and Job Constants

```php
// app/Jobs/JobPriority.php
class JobPriority
{
    public const CRITICAL = 'critical';
    public const HIGH = 'high';
    public const NORMAL = 'default';
    public const LOW = 'low';

    public const MAX_TRIES = [
        self::CRITICAL => 5,
        self::HIGH => 3,
        self::NORMAL => 3,
        self::LOW => 1,
    ];

    public const TIMEOUT = [
        self::CRITICAL => 300,  // 5 minutes
        self::HIGH => 180,      // 3 minutes
        self::NORMAL => 120,    // 2 minutes
        self::LOW => 60,        // 1 minute
    ];
}

// app/Jobs/ProcessPayment.php
class ProcessPayment implements ShouldQueue
{
    public $tries = JobPriority::MAX_TRIES[JobPriority::HIGH];
    public $timeout = JobPriority::TIMEOUT[JobPriority::HIGH];

    public function __construct(
        public Payment $payment
    ) {}

    public function handle(): void
    {
        // Process payment
    }

    public function queue(): string
    {
        return JobPriority::HIGH;
    }
}
```

## Environment-Specific Constants

```php
// app/Providers/AppServiceProvider.php
class AppServiceProvider extends ServiceProvider
{
    public function boot(): void
    {
        // Define environment-specific constants
        if (app()->environment('local', 'testing')) {
            Config::set('app.debug_mode', true);
            Config::set('app.cache_ttl.short', 1); // Shorter cache in dev
        }

        if (app()->environment('production')) {
            Config::set('app.debug_mode', false);
            Config::set('app.rate_limit', 60); // Stricter in production
        }
    }
}
```

## Testing with Constants

```php
test('order status transitions work correctly', function () {
    $order = Order::factory()->create([
        'status' => OrderStatus::PENDING
    ]);

    // Valid transition
    $order->transitionTo(OrderStatus::PROCESSING);
    expect($order->status)->toBe(OrderStatus::PROCESSING);

    // Invalid transition
    expect(fn() => $order->transitionTo(OrderStatus::PENDING))
        ->toThrow(InvalidStateTransition::class);
});

test('cache keys are consistent', function () {
    $userId = 123;

    $key1 = CacheService::getUserKey($userId);
    $key2 = sprintf(CacheService::USER_KEY, $userId);

    expect($key1)->toBe($key2)
        ->and($key1)->toBe('user:123');
});

test('validation rules are applied correctly', function () {
    $data = ['username' => 'ab']; // Too short

    $validator = Validator::make($data, [
        'username' => ValidationRules::username()
    ]);

    expect($validator->fails())->toBeTrue();
});
```

## Best Practices

1. **Group related constants**

   ```php
   class OrderConstants
   {
       // Statuses
       public const STATUS_PENDING = 'pending';
       public const STATUS_PAID = 'paid';

       // Limits
       public const MAX_ITEMS = 100;
       public const MIN_TOTAL = 10.00;
   }
   ```

2. **Use descriptive names**

   ```php
   // BAD
   const TIMEOUT = 30;

   // GOOD
   const API_TIMEOUT_SECONDS = 30;
   ```

3. **Document units and meanings**

   ```php
   class RateLimits
   {
       /** Maximum requests per minute for anonymous users */
       public const ANONYMOUS_PER_MINUTE = 20;

       /** Maximum requests per minute for authenticated users */
       public const AUTHENTICATED_PER_MINUTE = 60;

       /** Lockout duration in minutes after max attempts */
       public const LOCKOUT_MINUTES = 15;
   }
   ```

4. **Validate against constants**

   ```php
   public function setRole(string $role): void
   {
       if (!in_array($role, UserRole::ALL)) {
           throw new InvalidArgumentException("Invalid role: {$role}");
       }

       $this->role = $role;
   }
   ```

5. **Use configuration for environment-specific values**

   ```php
   // Don't use constants for environment-specific values
   // BAD: const API_KEY = 'abc123';

   // GOOD: Use config
   'api_key' => env('EXTERNAL_API_KEY'),
   ```

6. **Create helper functions for complex constants**

   ```php
   class DateConstants
   {
       public static function secondsIn(string $unit): int
       {
           return match($unit) {
               'minute' => 60,
               'hour' => 3600,
               'day' => 86400,
               'week' => 604800,
               default => throw new InvalidArgumentException("Unknown unit: {$unit}")
           };
       }
   }

   // Usage
   $cacheTime = DateConstants::secondsIn('hour') * 2; // 2 hours
   ```

Remember: Constants make your code self-documenting, reduce bugs from typos, and make refactoring much safer!
