---
name: detect-n-plus-one
description: Detects N+1 query problems in PHP code. Finds queries in loops, missing eager loading, lazy loading abuse, relationship traversal issues.
---

# N+1 Query Detection

Analyze PHP code for N+1 query problems that cause excessive database queries.

## Detection Patterns

### 1. Query Inside Loop

```php
// N+1: Query for each user
$users = $userRepository->findAll();
foreach ($users as $user) {
    $orders = $orderRepository->findByUser($user); // Query per iteration
    // ...
}

// N+1: Doctrine lazy loading in loop
foreach ($users as $user) {
    foreach ($user->getOrders() as $order) { // Lazy loads per user
        echo $order->getTotal();
    }
}
```

### 2. Missing Eager Loading

```php
// N+1: No JOIN/eager loading
$orders = $orderRepository->findAll();
foreach ($orders as $order) {
    echo $order->getCustomer()->getName(); // Lazy loads customer
    echo $order->getProduct()->getPrice(); // Lazy loads product
}

// FIXED: Eager load with DQL
$dql = "SELECT o, c, p FROM Order o
        JOIN o.customer c
        JOIN o.product p";
```

### 3. Relationship Traversal

```php
// N+1: Multiple levels of lazy loading
foreach ($departments as $department) {
    foreach ($department->getEmployees() as $employee) { // N queries
        foreach ($employee->getProjects() as $project) { // N*M queries
            echo $project->getName();
        }
    }
}
```

### 4. Collection Methods in Loop

```php
// N+1: count() triggers query each time
foreach ($categories as $category) {
    echo $category->getProducts()->count(); // Query per category
}

// N+1: filter() may not be optimized
foreach ($users as $user) {
    $activeOrders = $user->getOrders()->filter(
        fn($o) => $o->isActive()
    ); // May load all orders first
}
```

### 5. Eloquent N+1

```php
// N+1: Laravel Eloquent
$posts = Post::all();
foreach ($posts as $post) {
    echo $post->author->name; // Query per post
}

// FIXED: Eager loading
$posts = Post::with('author')->get();
$posts = Post::with(['author', 'comments.user'])->get();
```

### 6. API Calls in Loop

```php
// N+1: External API pattern
foreach ($products as $product) {
    $price = $pricingApi->getPrice($product->getSku()); // API call per product
}

// FIXED: Batch API call
$skus = array_map(fn($p) => $p->getSku(), $products);
$prices = $pricingApi->getPrices($skus);
```

## Grep Patterns

```bash
# Query methods inside foreach
Grep: "foreach.*\{[^}]*->find|foreach.*\{[^}]*->query|foreach.*\{[^}]*Repository" --glob "**/*.php"

# Getter calls that might lazy load
Grep: "foreach.*->get\w+\(\)" --glob "**/*.php"

# count() in loop
Grep: "foreach.*->count\(\)" --glob "**/*.php"

# Eloquent without with()
Grep: "::all\(\)|::get\(\)|::find\(" --glob "**/*.php"
```

## Detection in Doctrine

```php
// Check for LAZY fetch mode (default)
#[ManyToOne(fetch: 'LAZY')] // N+1 risk
private ?Customer $customer;

// Should use EAGER for frequently accessed
#[ManyToOne(fetch: 'EAGER')]
private ?Customer $customer;

// Or use DQL with JOIN
$qb->select('o', 'c')
   ->from(Order::class, 'o')
   ->join('o.customer', 'c');
```

## Solutions

### Eager Loading (Doctrine)

```php
// DQL JOIN
$query = $em->createQuery(
    'SELECT u, o, p
     FROM User u
     LEFT JOIN u.orders o
     LEFT JOIN o.products p'
);

// Query Builder
$qb = $em->createQueryBuilder()
    ->select('u', 'o', 'p')
    ->from(User::class, 'u')
    ->leftJoin('u.orders', 'o')
    ->leftJoin('o.products', 'p');
```

### Batch Loading

```php
// Load all related entities at once
$userIds = array_map(fn($u) => $u->getId(), $users);
$orders = $orderRepository->findByUserIds($userIds);
$ordersByUser = [];
foreach ($orders as $order) {
    $ordersByUser[$order->getUserId()][] = $order;
}

foreach ($users as $user) {
    $userOrders = $ordersByUser[$user->getId()] ?? [];
}
```

### Aggregation Instead of Counting

```php
// Instead of N count queries
// SELECT COUNT(*) FROM products WHERE category_id = 1
// SELECT COUNT(*) FROM products WHERE category_id = 2
// ...

// Use single aggregation query
$counts = $em->createQuery(
    'SELECT c.id, COUNT(p) as cnt
     FROM Category c
     LEFT JOIN c.products p
     GROUP BY c.id'
)->getResult();
```

## Severity Classification

| Pattern | Severity | Queries |
|---------|----------|---------|
| Query in loop (large dataset) | 🔴 Critical | O(n) |
| Nested relationship traversal | 🔴 Critical | O(n*m) |
| count() in loop | 🟠 Major | O(n) |
| Single lazy load | 🟡 Minor | +1 |

## Output Format

```markdown
### N+1 Query: [Description]

**Severity:** 🔴/🟠/🟡
**Location:** `file.php:line`
**Estimated Queries:** N + 1 (where N = number of items)

**Issue:**
[Description of the N+1 pattern]

**Code:**
```php
// Code with N+1 problem
```

**Fix:**
```php
// With eager loading
```

**Query Reduction:**
Before: 101 queries (1 + 100 items)
After: 1-2 queries
```

## When This Is Acceptable

- **Small fixed collections** — Iterating over <5 items with individual queries may be simpler than eager loading
- **CLI/worker context** — Background jobs where latency is less critical than memory
- **Cached results** — Queries inside loops that hit cache (Redis/in-memory) instead of database

### False Positive Indicators
- Loop iterates over a constant or config-defined small set
- Query result is wrapped in cache decorator
- Code is in a console command or queue worker
