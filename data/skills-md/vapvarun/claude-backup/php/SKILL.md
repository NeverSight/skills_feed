---
name: php
description: Modern PHP development best practices including PHP 8.x features, OOP patterns, error handling, security, testing, and performance optimization. Use when writing PHP code, reviewing PHP projects, debugging PHP issues, or implementing PHP features outside of WordPress/Laravel specific contexts.
---

# PHP Development

Modern PHP 8.x development patterns and best practices.

## PHP 8.x Features

### Constructor Property Promotion

```php
// Before PHP 8
class User {
    private string $name;
    private int $age;

    public function __construct(string $name, int $age) {
        $this->name = $name;
        $this->age = $age;
    }
}

// PHP 8+
class User {
    public function __construct(
        private string $name,
        private int $age,
        private bool $active = true
    ) {}
}
```

### Named Arguments

```php
function createUser(string $name, string $email, bool $admin = false): User {
    // ...
}

// Named arguments (order doesn't matter)
createUser(email: 'john@example.com', name: 'John', admin: true);
```

### Match Expression

```php
// BAD: Switch with many breaks
switch ($status) {
    case 'pending':
        $color = 'yellow';
        break;
    case 'approved':
        $color = 'green';
        break;
    default:
        $color = 'gray';
}

// GOOD: Match expression
$color = match($status) {
    'pending' => 'yellow',
    'approved', 'published' => 'green',
    'rejected' => 'red',
    default => 'gray',
};
```

### Null Safe Operator

```php
// Before
$country = null;
if ($user !== null && $user->getAddress() !== null) {
    $country = $user->getAddress()->getCountry();
}

// PHP 8+
$country = $user?->getAddress()?->getCountry();
```

### Union Types & Intersection Types

```php
// Union types
function process(int|float|string $value): int|float {
    return is_string($value) ? strlen($value) : $value * 2;
}

// Intersection types (PHP 8.1+)
function save(Countable&Iterator $items): void {
    foreach ($items as $item) {
        // ...
    }
}
```

### Enums (PHP 8.1+)

```php
enum Status: string {
    case Draft = 'draft';
    case Published = 'published';
    case Archived = 'archived';

    public function label(): string {
        return match($this) {
            self::Draft => 'Draft',
            self::Published => 'Published',
            self::Archived => 'Archived',
        };
    }

    public function color(): string {
        return match($this) {
            self::Draft => 'gray',
            self::Published => 'green',
            self::Archived => 'red',
        };
    }
}

// Usage
$post->status = Status::Published;
echo $post->status->label(); // "Published"
```

### Readonly Properties (PHP 8.1+)

```php
class User {
    public function __construct(
        public readonly int $id,
        public readonly string $email,
        private string $password
    ) {}
}

$user = new User(1, 'john@example.com', 'hashed');
$user->id = 2; // Error: Cannot modify readonly property
```

## Type Safety

### Strict Types

```php
<?php
declare(strict_types=1);

function add(int $a, int $b): int {
    return $a + $b;
}

add(1, 2);     // OK
add('1', '2'); // TypeError
```

### Return Types

```php
class UserRepository {
    public function find(int $id): ?User {
        // Returns User or null
    }

    public function findOrFail(int $id): User {
        return $this->find($id) ?? throw new NotFoundException();
    }

    public function all(): array {
        // Returns array of Users
    }

    public function save(User $user): void {
        // Returns nothing
    }

    public function delete(User $user): never {
        // Never returns (throws or exits)
        throw new NotImplementedException();
    }
}
```

## OOP Patterns

### Dependency Injection

```php
// BAD: Hard dependency
class OrderService {
    private $mailer;

    public function __construct() {
        $this->mailer = new SmtpMailer(); // Hard to test
    }
}

// GOOD: Dependency injection
interface MailerInterface {
    public function send(string $to, string $subject, string $body): void;
}

class OrderService {
    public function __construct(
        private MailerInterface $mailer,
        private LoggerInterface $logger
    ) {}

    public function complete(Order $order): void {
        $this->mailer->send($order->email, 'Order Complete', '...');
        $this->logger->info('Order completed', ['id' => $order->id]);
    }
}
```

### Value Objects

```php
final class Email {
    private function __construct(
        private readonly string $value
    ) {}

    public static function fromString(string $email): self {
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            throw new InvalidArgumentException('Invalid email');
        }
        return new self(strtolower($email));
    }

    public function toString(): string {
        return $this->value;
    }

    public function equals(self $other): bool {
        return $this->value === $other->value;
    }
}

// Usage
$email = Email::fromString('John@Example.com');
echo $email->toString(); // "john@example.com"
```

### Repository Pattern

```php
interface UserRepositoryInterface {
    public function find(int $id): ?User;
    public function findByEmail(string $email): ?User;
    public function save(User $user): void;
    public function delete(User $user): void;
}

class DatabaseUserRepository implements UserRepositoryInterface {
    public function __construct(
        private PDO $pdo
    ) {}

    public function find(int $id): ?User {
        $stmt = $this->pdo->prepare('SELECT * FROM users WHERE id = ?');
        $stmt->execute([$id]);
        $row = $stmt->fetch(PDO::FETCH_ASSOC);
        return $row ? $this->hydrate($row) : null;
    }

    private function hydrate(array $data): User {
        return new User(
            id: $data['id'],
            email: $data['email'],
            name: $data['name']
        );
    }
}
```

## Error Handling

### Custom Exceptions

```php
class DomainException extends Exception {}
class ValidationException extends DomainException {}
class NotFoundException extends DomainException {}

class InsufficientFundsException extends DomainException {
    public function __construct(
        public readonly float $balance,
        public readonly float $required
    ) {
        parent::__construct(
            "Insufficient funds: have {$balance}, need {$required}"
        );
    }
}

// Usage
throw new InsufficientFundsException(balance: 50.00, required: 100.00);
```

### Try-Catch Best Practices

```php
// BAD: Catching generic Exception
try {
    $result = $service->process($data);
} catch (Exception $e) {
    log($e->getMessage());
}

// GOOD: Specific exception handling
try {
    $result = $service->process($data);
} catch (ValidationException $e) {
    return response()->json(['errors' => $e->getErrors()], 422);
} catch (NotFoundException $e) {
    return response()->json(['error' => 'Not found'], 404);
} catch (Throwable $e) {
    $this->logger->error('Unexpected error', ['exception' => $e]);
    return response()->json(['error' => 'Server error'], 500);
}
```

## Security

### Input Validation

```php
// Always validate and sanitize input
$email = filter_input(INPUT_POST, 'email', FILTER_VALIDATE_EMAIL);
$age = filter_input(INPUT_POST, 'age', FILTER_VALIDATE_INT, [
    'options' => ['min_range' => 0, 'max_range' => 150]
]);

if ($email === false || $email === null) {
    throw new ValidationException('Invalid email');
}
```

### Password Hashing

```php
// Always use password_hash/password_verify
$hash = password_hash($password, PASSWORD_DEFAULT);

if (password_verify($inputPassword, $storedHash)) {
    // Password correct

    // Rehash if needed (algorithm upgrade)
    if (password_needs_rehash($storedHash, PASSWORD_DEFAULT)) {
        $newHash = password_hash($inputPassword, PASSWORD_DEFAULT);
        $user->updatePassword($newHash);
    }
}
```

### SQL Injection Prevention

```php
// BAD: Direct concatenation
$sql = "SELECT * FROM users WHERE email = '$email'"; // VULNERABLE

// GOOD: Prepared statements
$stmt = $pdo->prepare('SELECT * FROM users WHERE email = ?');
$stmt->execute([$email]);

// GOOD: Named parameters
$stmt = $pdo->prepare('SELECT * FROM users WHERE email = :email AND status = :status');
$stmt->execute(['email' => $email, 'status' => 'active']);
```

## Testing

### PHPUnit

```php
class UserServiceTest extends TestCase {
    private UserService $service;
    private MockObject $repository;

    protected function setUp(): void {
        $this->repository = $this->createMock(UserRepositoryInterface::class);
        $this->service = new UserService($this->repository);
    }

    public function testFindUserReturnsUser(): void {
        $expected = new User(1, 'john@example.com');
        $this->repository
            ->expects($this->once())
            ->method('find')
            ->with(1)
            ->willReturn($expected);

        $result = $this->service->find(1);

        $this->assertEquals($expected, $result);
    }

    public function testFindUserThrowsWhenNotFound(): void {
        $this->repository
            ->method('find')
            ->willReturn(null);

        $this->expectException(NotFoundException::class);

        $this->service->findOrFail(999);
    }
}
```

### Data Providers

```php
#[DataProvider('validEmailProvider')]
public function testValidEmails(string $email): void {
    $result = Email::fromString($email);
    $this->assertInstanceOf(Email::class, $result);
}

public static function validEmailProvider(): array {
    return [
        'simple' => ['test@example.com'],
        'with subdomain' => ['test@mail.example.com'],
        'with plus' => ['test+label@example.com'],
    ];
}
```

## Performance

### Opcache

```ini
; php.ini
opcache.enable=1
opcache.memory_consumption=256
opcache.max_accelerated_files=20000
opcache.validate_timestamps=0  ; Production only
```

### Array Functions

```php
// Use array functions instead of loops when possible
$names = array_map(fn($user) => $user->name, $users);
$adults = array_filter($users, fn($user) => $user->age >= 18);
$total = array_reduce($orders, fn($sum, $order) => $sum + $order->total, 0);

// Generators for large datasets
function readLargeFile(string $path): Generator {
    $handle = fopen($path, 'r');
    while (($line = fgets($handle)) !== false) {
        yield trim($line);
    }
    fclose($handle);
}

foreach (readLargeFile('huge.csv') as $line) {
    // Process one line at a time, low memory
}
```

## Composer Best Practices

```json
{
    "require": {
        "php": "^8.2",
        "monolog/monolog": "^3.0"
    },
    "require-dev": {
        "phpunit/phpunit": "^10.0",
        "phpstan/phpstan": "^1.0"
    },
    "autoload": {
        "psr-4": {
            "App\\": "src/"
        }
    },
    "config": {
        "sort-packages": true,
        "optimize-autoloader": true
    }
}
```

```bash
# Production deployment
composer install --no-dev --optimize-autoloader --classmap-authoritative
```
