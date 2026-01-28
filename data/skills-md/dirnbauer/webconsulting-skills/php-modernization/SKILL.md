---
name: php-modernization
description: PHP 8.x modernization patterns. Use when upgrading to PHP 8.2/8.3/8.4, implementing type safety, or achieving PHPStan level 10.
version: 1.0.0
triggers:
  - php
  - modernization
  - phpstan
  - rector
  - type safety
  - dto
  - enum
---

# PHP Modernization Skill

Modernize PHP applications to PHP 8.x with type safety, PSR compliance, and static analysis.

## Expertise Areas

- **PHP 8.x**: Constructor promotion, readonly, enums, match, attributes, union types
- **PSR/PER Compliance**: Active PHP-FIG standards
- **Static Analysis**: PHPStan (level 9+), PHPat, Rector, PHP-CS-Fixer
- **Type Safety**: DTOs/VOs over arrays, generics via PHPDoc

## PHP 8.x Features

### Constructor Property Promotion (PHP 8.0+)

```php
// ❌ OLD
class UserService
{
    private UserRepository $userRepository;
    private LoggerInterface $logger;

    public function __construct(
        UserRepository $userRepository,
        LoggerInterface $logger
    ) {
        $this->userRepository = $userRepository;
        $this->logger = $logger;
    }
}

// ✅ NEW
final class UserService
{
    public function __construct(
        private readonly UserRepository $userRepository,
        private readonly LoggerInterface $logger,
    ) {}
}
```

### Readonly Classes (PHP 8.2+)

```php
// ✅ All properties are implicitly readonly
final readonly class UserDTO
{
    public function __construct(
        public int $id,
        public string $name,
        public string $email,
    ) {}
}
```

### Enums (PHP 8.1+)

```php
// ❌ OLD - String constants
class Status
{
    public const DRAFT = 'draft';
    public const PUBLISHED = 'published';
    public const ARCHIVED = 'archived';
}

// ✅ NEW - Backed enum
enum Status: string
{
    case Draft = 'draft';
    case Published = 'published';
    case Archived = 'archived';

    public function label(): string
    {
        return match($this) {
            self::Draft => 'Draft',
            self::Published => 'Published',
            self::Archived => 'Archived',
        };
    }
}

// Usage
public function setStatus(Status $status): void
{
    $this->status = $status;
}

$item->setStatus(Status::Published);
```

### Match Expression (PHP 8.0+)

```php
// ❌ OLD - Switch
switch ($type) {
    case 'a':
        $result = 'Type A';
        break;
    case 'b':
        $result = 'Type B';
        break;
    default:
        $result = 'Unknown';
}

// ✅ NEW - Match
$result = match($type) {
    'a' => 'Type A',
    'b' => 'Type B',
    default => 'Unknown',
};
```

### Named Arguments (PHP 8.0+)

```php
// ✅ Clearer and order-independent
$this->doSomething(
    name: 'value',
    options: ['key' => 'value'],
    enabled: true,
);
```

### Null Safe Operator (PHP 8.0+)

```php
// ❌ OLD
$country = null;
if ($user !== null && $user->getAddress() !== null) {
    $country = $user->getAddress()->getCountry();
}

// ✅ NEW
$country = $user?->getAddress()?->getCountry();
```

### Union Types (PHP 8.0+)

```php
public function process(string|int $value): string|null
{
    // ...
}
```

### Intersection Types (PHP 8.1+)

```php
public function handle(Countable&Iterator $collection): void
{
    // $collection must implement both interfaces
}
```

### Attributes (PHP 8.0+)

```php
use TYPO3\CMS\Core\Attribute\AsEventListener;

#[AsEventListener(identifier: 'myext/my-listener')]
final class MyListener
{
    public function __invoke(SomeEvent $event): void
    {
        // Handle event
    }
}
```

## DTOs and Value Objects

### Never Use Arrays for Structured Data

```php
// ❌ BAD - Array passing
public function createUser(array $data): array
{
    // What fields are expected? What types?
}

// ✅ GOOD - DTO pattern
public function createUser(CreateUserDTO $dto): UserDTO
{
    // Type-safe, documented, IDE-friendly
}
```

### Data Transfer Object

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\DTO;

final readonly class CreateUserDTO
{
    public function __construct(
        public string $name,
        public string $email,
        public ?string $phone = null,
    ) {}

    public static function fromArray(array $data): self
    {
        return new self(
            name: $data['name'] ?? throw new \InvalidArgumentException('Name required'),
            email: $data['email'] ?? throw new \InvalidArgumentException('Email required'),
            phone: $data['phone'] ?? null,
        );
    }
}
```

### Value Object

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\ValueObject;

final readonly class EmailAddress
{
    private function __construct(
        public string $value,
    ) {}

    public static function fromString(string $email): self
    {
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            throw new \InvalidArgumentException('Invalid email address');
        }

        return new self($email);
    }

    public function equals(self $other): bool
    {
        return $this->value === $other->value;
    }

    public function __toString(): string
    {
        return $this->value;
    }
}
```

## PSR/PER Compliance

### Active Standards

| Standard | Purpose | Status |
|----------|---------|--------|
| PSR-1 | Basic Coding | Required |
| PSR-4 | Autoloading | Required |
| PER CS | Coding Style | Required (supersedes PSR-12) |
| PSR-3 | Logger Interface | Use for logging |
| PSR-6/16 | Cache | Use for caching |
| PSR-7/17/18 | HTTP | Use for HTTP clients |
| PSR-11 | Container | Use for DI |
| PSR-14 | Events | Use for event dispatching |
| PSR-15 | Middleware | Use for HTTP middleware |
| PSR-20 | Clock | Use for time-dependent code |

### PER Coding Style

```php
<?php

declare(strict_types=1);

namespace Vendor\Package;

use Vendor\Package\SomeClass;

final class MyClass
{
    public function __construct(
        private readonly SomeClass $dependency,
    ) {}

    public function doSomething(
        string $param1,
        int $param2,
    ): string {
        return match ($param2) {
            1 => $param1,
            2 => $param1 . $param1,
            default => '',
        };
    }
}
```

## Static Analysis Tools

### PHPStan (Level 9+)

```neon
# phpstan.neon
includes:
    - vendor/phpstan/phpstan-strict-rules/rules.neon
    - vendor/saschaegerer/phpstan-typo3/extension.neon

parameters:
    level: 10
    paths:
        - Classes
        - Tests
    excludePaths:
        - Classes/Domain/Model/*
```

**Level Guide:**
- Level 0-5: Basic checks
- Level 6-8: Type checking
- Level 9: Strict mixed handling
- Level 10: Maximum strictness (recommended)

### PHP-CS-Fixer

```php
<?php
// .php-cs-fixer.dist.php
$config = new PhpCsFixer\Config();

return $config
    ->setRules([
        '@PER-CS' => true,
        '@PER-CS:risky' => true,
        'declare_strict_types' => true,
        'no_unused_imports' => true,
        'ordered_imports' => ['sort_algorithm' => 'alpha'],
        'single_line_empty_body' => true,
        'trailing_comma_in_multiline' => [
            'elements' => ['arguments', 'arrays', 'match', 'parameters'],
        ],
    ])
    ->setRiskyAllowed(true)
    ->setFinder(
        PhpCsFixer\Finder::create()
            ->in(__DIR__ . '/Classes')
            ->in(__DIR__ . '/Tests')
    );
```

### Rector

```php
<?php
// rector.php
declare(strict_types=1);

use Rector\Config\RectorConfig;
use Rector\Set\ValueObject\LevelSetList;
use Rector\Set\ValueObject\SetList;

return RectorConfig::configure()
    ->withPaths([
        __DIR__ . '/Classes',
        __DIR__ . '/Tests',
    ])
    ->withSets([
        LevelSetList::UP_TO_PHP_83,
        SetList::CODE_QUALITY,
        SetList::TYPE_DECLARATION,
        SetList::DEAD_CODE,
    ]);
```

### PHPat (Architecture Testing)

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Tests\Architecture;

use PHPat\Selector\Selector;
use PHPat\Test\Builder\Rule;
use PHPat\Test\PHPat;

final class ArchitectureTest
{
    public function testDomainDoesNotDependOnInfrastructure(): Rule
    {
        return PHPat::rule()
            ->classes(Selector::inNamespace('Vendor\MyExtension\Domain'))
            ->shouldNotDependOn()
            ->classes(Selector::inNamespace('Vendor\MyExtension\Infrastructure'));
    }
}
```

## Type Safety Patterns

### Typed Arrays with PHPDoc Generics

```php
/**
 * @return array<int, User>
 */
public function getUsers(): array
{
    return $this->users;
}

/**
 * @param array<string, mixed> $config
 */
public function configure(array $config): void
{
    // ...
}

/**
 * @return \Generator<int, Item, mixed, void>
 */
public function iterateItems(): \Generator
{
    foreach ($this->items as $item) {
        yield $item;
    }
}
```

### Strict Comparison

```php
// ❌ Loose comparison
if ($value == '1') {}

// ✅ Strict comparison
if ($value === '1') {}
if ($value === 1) {}
```

### Early Returns

```php
// ❌ Nested conditions
public function process(?User $user): ?Result
{
    if ($user !== null) {
        if ($user->isActive()) {
            return $this->doProcess($user);
        }
    }
    return null;
}

// ✅ Early returns
public function process(?User $user): ?Result
{
    if ($user === null) {
        return null;
    }

    if (!$user->isActive()) {
        return null;
    }

    return $this->doProcess($user);
}
```

## Migration Checklist

- [ ] `declare(strict_types=1)` in all files
- [ ] PSR-4 autoloading in composer.json
- [ ] PER Coding Style enforced via PHP-CS-Fixer
- [ ] PHPStan level 9+ (level 10 for new projects)
- [ ] All methods have return types
- [ ] All parameters have type declarations
- [ ] All properties have type declarations
- [ ] **DTOs for data transfer**, Value Objects for domain concepts
- [ ] **Enums** for fixed sets of values (not string constants)
- [ ] Constructor property promotion used
- [ ] `final` on classes not designed for inheritance
- [ ] `readonly` on immutable classes
- [ ] No `@var` annotations when type is declared
- [ ] PHPat architecture tests for layer dependencies

## Resources

- **PHP-FIG**: https://www.php-fig.org/
- **PHPStan**: https://phpstan.org/
- **Rector**: https://getrector.com/
- **PHP-CS-Fixer**: https://cs.symfony.com/
- **PHPat**: https://www.phpat.dev/

---

## Credits & Attribution

This skill is based on the excellent work by
**[Netresearch DTT GmbH](https://www.netresearch.de/)**.

Original repository: https://github.com/netresearch/php-modernization-skill

**Copyright (c) Netresearch DTT GmbH** - Methodology and best practices  
Adapted by webconsulting.at for this skill collection
