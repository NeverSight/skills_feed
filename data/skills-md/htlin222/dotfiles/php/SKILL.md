---
name: php
description: Write modern PHP with generators, SPL, and PHP 8+ features. Use for PHP development or optimization.
---

# PHP Development

Write modern, performant PHP code.

## When to use

- Writing PHP code
- PHP 8+ features
- Performance optimization
- Laravel/Symfony development

## Modern PHP patterns

### Type system (PHP 8+)

```php
// Union types
function process(int|string $id): array|false {
    // ...
}

// Constructor property promotion
class User {
    public function __construct(
        public readonly string $name,
        public readonly string $email,
        private ?int $age = null,
    ) {}
}

// Enums
enum Status: string {
    case Pending = 'pending';
    case Active = 'active';
    case Completed = 'completed';
}

// Match expression
$result = match($status) {
    Status::Pending => 'Waiting',
    Status::Active => 'In Progress',
    Status::Completed => 'Done',
};
```

### Generators

```php
// Memory-efficient iteration
function readLargeFile(string $path): Generator {
    $handle = fopen($path, 'r');
    while (($line = fgets($handle)) !== false) {
        yield trim($line);
    }
    fclose($handle);
}

// Usage
foreach (readLargeFile('huge.csv') as $line) {
    processLine($line);
}

// Generator with keys
function parseCSV(string $path): Generator {
    $handle = fopen($path, 'r');
    $headers = fgetcsv($handle);
    while (($row = fgetcsv($handle)) !== false) {
        yield array_combine($headers, $row);
    }
    fclose($handle);
}
```

### SPL data structures

```php
// Priority queue
$queue = new SplPriorityQueue();
$queue->insert('low', 1);
$queue->insert('high', 10);
$queue->insert('medium', 5);

while (!$queue->isEmpty()) {
    echo $queue->extract(); // high, medium, low
}

// Fixed array (memory efficient)
$arr = new SplFixedArray(1000);
$arr[0] = 'value';
```

### Error handling

```php
// Custom exceptions
class ValidationException extends Exception {
    public function __construct(
        public readonly string $field,
        string $message,
    ) {
        parent::__construct($message);
    }
}

// Try-catch with multiple types
try {
    process($data);
} catch (ValidationException $e) {
    log("Validation failed: {$e->field}");
} catch (RuntimeException $e) {
    log("Runtime error: {$e->getMessage()}");
} finally {
    cleanup();
}
```

### Attributes (PHP 8)

```php
#[Attribute(Attribute::TARGET_METHOD)]
class Route {
    public function __construct(
        public string $path,
        public string $method = 'GET',
    ) {}
}

class Controller {
    #[Route('/users', 'GET')]
    public function listUsers(): array {
        // ...
    }
}
```

## Best practices

- Use strict types: `declare(strict_types=1);`
- Follow PSR-12 coding standard
- Use Composer for autoloading
- Prefer built-in functions over custom
- Use generators for large datasets

## Examples

**Input:** "Optimize this PHP code"
**Action:** Profile with Xdebug, use generators, leverage SPL structures

**Input:** "Modernize to PHP 8"
**Action:** Add type hints, use match/enums, constructor promotion
