---
name: laravel:laravel-prompting-patterns
description: Use Laravel-specific vocabulary—Eloquent patterns, Form Requests, API resources, jobs/queues—to get idiomatic framework code
---

# Laravel Prompting Patterns

Use Laravel's vocabulary to get idiomatic code. Generic requests produce generic solutions that don't leverage the framework.

## Database Operations

### Generic
"Get all active users with their posts"

### Laravel-Specific
"Query active users with eager-loaded posts using Eloquent:
```php
User::where('active', true)
    ->with('posts')
    ->get();
```
Add a scope to User model: `scopeActive($query)`"

### Relationships
"Set up a many-to-many relationship between Posts and Tags:
- Create `post_tag` pivot table migration
- Add `belongsToMany` in Post model
- Add `belongsToMany` in Tag model
- Use `attach()`, `detach()`, `sync()` for management"

### Query Optimization
"Avoid N+1 on the posts index:
- Eager load `author` and `category` relationships
- Use `withCount('comments')` for comment totals
- Add database indexes on `published_at` and `category_id`"

## Validation

### Generic
"Validate the user input"

### Laravel-Specific
"Create UserStoreRequest with validation rules:
```php
public function rules(): array
{
    return [
        'email' => ['required', 'email', 'unique:users,email'],
        'password' => ['required', 'min:12', Password::defaults()],
        'name' => ['required', 'string', 'max:255'],
    ];
}
```
Add custom error messages in `messages()` method"

### Complex Validation
"Validate order creation:
- Use `Rule::exists('products', 'id')` for product IDs
- Validate nested items array: `items.*.quantity` must be integer, min 1
- Use `Rule::requiredIf()` for conditional shipping address
- Add custom rule for inventory check: `new HasSufficientStock`"

## API Endpoints

### Generic
"Create an API for products"

### Laravel-Specific
"Create RESTful product API:
- Resource controller: `ProductController` with apiResource routes
- Use `ProductResource` for response transformation
- Add `ProductCollection` for index endpoint with pagination
- Protect with Sanctum middleware: `auth:sanctum`
- Return 201 on create, 204 on delete
- Use `ProductStoreRequest` and `ProductUpdateRequest` for validation"

### Pagination
"Paginate products API:
- Use `Product::paginate(20)` in controller
- Return with `ProductResource::collection($products)`
- Include meta: `total`, `per_page`, `current_page`, `last_page`
- Support `?page=2` query parameter"

### Filtering
"Add filtering to products API:
- Accept `?category=electronics&min_price=100` query params
- Use `when()` for conditional queries
- Extract to `ProductFilters` class for reusability
- Document query params in API docs"

## Background Processing

### Generic
"Send email after user registers"

### Laravel-Specific
"Dispatch SendWelcomeEmail job after registration:
```php
SendWelcomeEmail::dispatch($user)
    ->onQueue('emails')
    ->delay(now()->addMinutes(5));
```
- Implement `ShouldQueue` interface
- Add `$tries = 3` and `$timeout = 30`
- Handle failure in `failed()` method
- Tag job for Horizon: `$tags = ['user:'.$user->id]`"

### Queue Configuration
"Configure queue for payment processing:
- Use `redis` connection for payments queue
- Set `queue:work --queue=payments,default`
- Add `retry_after` to 90 seconds in config
- Monitor with Horizon dashboard"

### Job Chaining
"Process order with job chain:
```php
Bus::chain([
    new ValidateInventory($order),
    new ChargePayment($order),
    new SendConfirmation($order),
])->dispatch();
```
If any job fails, chain stops. Handle in `catch()` callback."

## Referencing Documentation

### Effective References
"Implement according to Laravel's [Eloquent Relationships docs](https://laravel.com/docs/11.x/eloquent-relationships#many-to-many)"

"Follow Laravel's [Form Request Validation pattern](https://laravel.com/docs/11.x/validation#form-request-validation)"

"Use Laravel's [API Resource](https://laravel.com/docs/11.x/eloquent-resources) pattern for response transformation"

"Configure queues per [Laravel Queue docs](https://laravel.com/docs/11.x/queues)"

## Pattern Catalog

**Models & Eloquent:**
- Relationships: `hasMany`, `belongsTo`, `belongsToMany`, `morphMany`
- Scopes: `scopeActive`, `scopePublished`
- Accessors/Mutators: `get{Attribute}Attribute`, `set{Attribute}Attribute`
- Casts: `protected $casts = ['published_at' => 'datetime']`

**Validation:**
- Form Requests: `UserStoreRequest`, `ProductUpdateRequest`
- Rules: `required`, `unique:table,column`, `exists:table,column`
- Custom Rules: `new Uppercase`, `Rule::in(['admin', 'user'])`

**API:**
- Resources: `UserResource`, `ProductCollection`
- Pagination: `paginate()`, `simplePaginate()`, `cursorPaginate()`
- Rate Limiting: `throttle:60,1` middleware

**Jobs & Queues:**
- Jobs: `ShouldQueue`, `dispatch()`, `dispatchSync()`
- Chains: `Bus::chain()`, `Bus::batch()`
- Horizon: Tags, monitoring, failed job handling

Use Laravel's vocabulary. Get Laravel solutions.
