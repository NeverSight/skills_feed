---
name: php-database
version: "2.0.0"
description: PHP database mastery - PDO, Eloquent, Doctrine, query optimization, and migrations
sasmp_version: "1.3.0"
bonded_agent: 05-php-database
bond_type: PRIMARY_BOND
atomic: true
category: data
---

# PHP Database Skill

> Atomic skill for mastering database operations in PHP

## Overview

Comprehensive skill for PHP database interactions covering PDO, ORM patterns, query optimization, schema design, and migrations.

## Skill Parameters

### Input Validation
```typescript
interface SkillParams {
  topic:
    | "pdo"              // Native PHP database
    | "eloquent"         // Laravel ORM
    | "doctrine"         // Symfony ORM
    | "optimization"     // Query tuning, indexing
    | "migrations"       // Schema versioning
    | "transactions";    // ACID, locking

  level: "beginner" | "intermediate" | "advanced";
  database?: "mysql" | "postgresql" | "sqlite";
  orm?: "eloquent" | "doctrine" | "none";
}
```

### Validation Rules
```yaml
validation:
  topic:
    required: true
    allowed: [pdo, eloquent, doctrine, optimization, migrations, transactions]
  level:
    required: true
  database:
    default: "mysql"
```

## Learning Modules

### Module 1: PDO Fundamentals
```yaml
beginner:
  - Connection and DSN
  - Prepared statements
  - Fetching results

intermediate:
  - Error handling modes
  - Transactions basics
  - Named placeholders

advanced:
  - Connection pooling
  - Stored procedures
  - Batch operations
```

### Module 2: Query Optimization
```yaml
beginner:
  - Basic indexing
  - EXPLAIN basics
  - WHERE clause optimization

intermediate:
  - Composite indexes
  - Join optimization
  - Query profiling

advanced:
  - Execution plan analysis
  - Partitioning
  - Query caching
```

### Module 3: ORM Patterns
```yaml
beginner:
  - Model basics
  - CRUD operations
  - Simple relationships

intermediate:
  - Eager loading (N+1 prevention)
  - Query scopes
  - Lifecycle hooks

advanced:
  - Custom repositories
  - Result caching
  - Batch processing
```

## Error Handling & Retry Logic

```yaml
errors:
  CONNECTION_ERROR:
    code: "DB_001"
    recovery: "Check connection string, retry with backoff"

  DEADLOCK_ERROR:
    code: "DB_002"
    recovery: "Retry transaction with exponential backoff"

  QUERY_ERROR:
    code: "DB_003"
    recovery: "Check SQL syntax, validate parameters"

retry:
  max_attempts: 3
  backoff:
    type: exponential
    initial_delay_ms: 100
    max_delay_ms: 2000
  retryable: [CONNECTION_ERROR, DEADLOCK_ERROR]
```

## Code Examples

### PDO with Prepared Statements
```php
<?php
declare(strict_types=1);

final class Database
{
    private \PDO $pdo;

    public function __construct(string $dsn, string $user, string $pass)
    {
        $this->pdo = new \PDO($dsn, $user, $pass, [
            \PDO::ATTR_ERRMODE => \PDO::ERRMODE_EXCEPTION,
            \PDO::ATTR_DEFAULT_FETCH_MODE => \PDO::FETCH_ASSOC,
            \PDO::ATTR_EMULATE_PREPARES => false,
        ]);
    }

    public function findById(int $id): ?array
    {
        $stmt = $this->pdo->prepare('SELECT * FROM users WHERE id = :id');
        $stmt->execute(['id' => $id]);
        return $stmt->fetch() ?: null;
    }

    public function insert(array $data): int
    {
        $stmt = $this->pdo->prepare(
            'INSERT INTO users (name, email) VALUES (:name, :email)'
        );
        $stmt->execute($data);
        return (int) $this->pdo->lastInsertId();
    }
}
```

### Transaction with Retry
```php
<?php
declare(strict_types=1);

final class TransactionService
{
    public function executeWithRetry(
        \PDO $pdo,
        callable $operation,
        int $maxRetries = 3
    ): mixed {
        $attempt = 0;

        while (true) {
            try {
                $pdo->beginTransaction();
                $result = $operation($pdo);
                $pdo->commit();
                return $result;
            } catch (\PDOException $e) {
                $pdo->rollBack();

                if (++$attempt >= $maxRetries || !$this->isRetryable($e)) {
                    throw $e;
                }

                usleep(100000 * pow(2, $attempt)); // Exponential backoff
            }
        }
    }

    private function isRetryable(\PDOException $e): bool
    {
        return str_contains($e->getMessage(), 'Deadlock');
    }
}
```

### N+1 Prevention (Eloquent)
```php
<?php
// BAD: N+1 problem
$posts = Post::all();
foreach ($posts as $post) {
    echo $post->author->name; // Query per post!
}

// GOOD: Eager loading
$posts = Post::with('author')->get();
foreach ($posts as $post) {
    echo $post->author->name; // No extra queries
}

// BETTER: Select specific columns
$posts = Post::with(['author:id,name'])->get(['id', 'title', 'author_id']);
```

### Query Optimization
```sql
-- Before: Full table scan
SELECT * FROM orders WHERE status = 'pending';

-- Step 1: Add index
CREATE INDEX idx_orders_status ON orders(status);

-- Step 2: Analyze with EXPLAIN
EXPLAIN SELECT * FROM orders WHERE status = 'pending';

-- Result: Index scan instead of full table scan
```

## Troubleshooting

| Problem | Detection | Solution |
|---------|-----------|----------|
| N+1 queries | Debugbar shows 100+ queries | Use eager loading with() |
| Slow queries | Query > 1 second | Add indexes, run EXPLAIN |
| Deadlocks | "Deadlock found" error | Implement retry logic |
| Memory exhaustion | Memory limit error | Use chunk() or cursor() |

### Memory-Efficient Processing
```php
<?php
// BAD: Loads all into memory
$users = User::all();

// GOOD: Chunk processing
User::chunk(1000, function ($users) {
    foreach ($users as $user) {
        // Process
    }
});

// BETTER: Cursor for minimal memory
foreach (User::cursor() as $user) {
    // Process one at a time
}
```

## Quality Metrics

| Metric | Target |
|--------|--------|
| Prepared statements | 100% |
| N+1 prevention | 100% |
| Index recommendations | ≥95% |
| Transaction safety | 100% |

## Usage

```
Skill("php-database", {topic: "optimization", level: "advanced"})
```
