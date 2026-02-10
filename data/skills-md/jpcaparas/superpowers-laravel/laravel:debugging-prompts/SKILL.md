---
name: laravel:debugging-prompts
description: Create effective debugging prompts—include error messages, stack traces, expected vs actual behavior, logs, and attempted solutions
---

# Debugging Prompts

Debugging with AI requires complete information. Missing context means generic suggestions that don't solve your specific problem.

## Error Messages and Stack Traces

### Incomplete
"Getting an error in the payment controller"

### Complete
"Getting error when processing payment:

**Error:**
```
Illuminate\Database\QueryException: SQLSTATE[23000]: 
Integrity constraint violation: 1452 Cannot add or update a child row: 
a foreign key constraint fails (`app`.`payments`, CONSTRAINT `payments_order_id_foreign` 
FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE)
```

**Stack trace:**
```
#0 app/Services/PaymentService.php(45): Payment::create()
#1 app/Http/Controllers/PaymentController.php(28): PaymentService->process()
#2 vendor/laravel/framework/src/Illuminate/Routing/Controller.php(54)
```

**Context:**
- Laravel 11.x, MySQL 8.0
- Happens when order_id doesn't exist in orders table
- Payment data: `['order_id' => 999, 'amount' => 5000, 'status' => 'pending']`
- Order 999 doesn't exist in database"

**Why it works:** Complete error, stack trace, context, and the specific data causing the issue.

## Expected vs Actual Behavior

### Vague
"The API isn't returning the right data"

### Specific
"Product API returning incorrect data:

**Expected behavior:**
```json
{
  "data": {
    "id": 1,
    "name": "Widget",
    "price": "29.99",
    "category": {
      "id": 5,
      "name": "Tools"
    }
  }
}
```

**Actual behavior:**
```json
{
  "data": {
    "id": 1,
    "name": "Widget",
    "price": 2999,
    "category": null
  }
}
```

**Issues:**
1. Price is in cents (2999) instead of formatted dollars ("29.99")
2. Category is null even though product has category_id = 5

**Code:**
```php
// ProductController@show
return new ProductResource($product);
```

Product has `category_id = 5` in database, but relationship not loading."

**Why it works:** Shows exact expected vs actual output, identifies specific issues, includes relevant code.

## Log Entries and State

### Insufficient
"Something's wrong with the queue"

### Sufficient
"Job failing in queue:

**Log entries:**
```
[2024-01-15 10:30:15] local.ERROR: Job failed: ProcessOrderJob
{"order_id":123,"exception":"Stripe\\Exception\\InvalidRequestException: 
No such customer: cus_invalid","attempts":3}

[2024-01-15 10:30:15] local.INFO: Order state before job
{"id":123,"status":"pending","stripe_customer_id":"cus_invalid"}
```

**Job code:**
```php
public function handle()
{
    $customer = $this->stripe->customers->retrieve(
        $this->order->stripe_customer_id
    );
    // ...
}
```

**State:**
- Order 123 has `stripe_customer_id = "cus_invalid"`
- Customer doesn't exist in Stripe
- Job has retried 3 times, now in failed_jobs table
- Using Laravel 11.x with Horizon"

**Why it works:** Includes logs, state information, relevant code, and context about retries.

## Hypotheses and Evidence

### Weak
"I think it's a caching issue"

### Strong
"Suspect Redis cache is stale:

**Hypothesis:** Product prices are cached but not invalidating on update.

**Evidence:**
1. Updated product price in database: `UPDATE products SET price = 3999 WHERE id = 1`
2. Database shows: `SELECT price FROM products WHERE id = 1` → `3999`
3. API returns old price: `GET /api/products/1` → `"price": "29.99"`
4. After `php artisan cache:clear`, API returns correct price: `"price": "39.99"`

**Caching code:**
```php
public function show(Product $product)
{
    $cached = Cache::remember("product.{$product->id}", 3600, function () use ($product) {
        return new ProductResource($product);
    });
    return $cached;
}
```

**Problem:** Cache key doesn't invalidate when product updates. Need cache invalidation in ProductObserver or remove caching from show method."

**Why it works:** Clear hypothesis, concrete evidence, relevant code, proposed solution.

## Attempted Solutions

### Unhelpful
"I tried some things but nothing worked"

### Helpful
"Attempted solutions and results:

**Attempt 1:** Added eager loading
```php
$products = Product::with('category')->get();
```
**Result:** Still getting N+1 queries. Debugbar shows 101 queries (1 for products, 100 for categories).

**Attempt 2:** Used `load()` after fetching
```php
$products = Product::all();
$products->load('category');
```
**Result:** Same issue, still 101 queries.

**Attempt 3:** Checked relationship definition
```php
// In Product model
public function category()
{
    return $this->belongsTo(Category::class);
}
```
**Result:** Relationship looks correct. Foreign key `category_id` exists in products table.

**Current state:** Eager loading syntax seems correct but not working. Using Laravel 11.x. What am I missing?"

**Why it works:** Shows what was tried, exact code used, results observed, helps avoid suggesting already-tried solutions.

## Debugging Templates

### Template: Error Report
```
**Error:** [Full error message]
**Stack trace:** [Complete stack trace]
**File/Line:** [Where error occurs]
**Context:** [Laravel version, packages, environment]
**Data:** [Input data causing error]
**Expected:** [What should happen]
```

### Template: Unexpected Behavior
```
**Expected:** [Describe expected behavior with example]
**Actual:** [Describe actual behavior with example]
**Code:** [Relevant code snippet]
**State:** [Database state, variable values]
**Environment:** [Laravel version, Sail/host, packages]
```

### Template: Performance Issue
```
**Problem:** [Describe slow operation]
**Metrics:** [Response time, query count, memory usage]
**Query log:** [Slow queries from Debugbar/Telescope]
**Code:** [Code causing performance issue]
**Dataset size:** [Number of records involved]
**Attempted:** [Optimizations already tried]
```

## Quick Reference

Debug effectively with AI:
- **Complete errors** - Full message, stack trace, file/line
- **Show both sides** - Expected vs actual behavior
- **Include logs** - Error logs, info logs, state dumps
- **Share evidence** - Database queries, API responses, variable dumps
- **Document attempts** - What you tried, exact code, results
- **Provide context** - Laravel version, environment, packages

More information = faster solutions. When debugging, over-communicate.
