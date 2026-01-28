---
name: php-testing
version: "2.0.0"
description: PHP testing mastery - PHPUnit 11, Pest 3, TDD, mocking, and CI/CD integration
sasmp_version: "1.3.0"
bonded_agent: 06-php-testing
bond_type: PRIMARY_BOND
atomic: true
category: quality
---

# PHP Testing Skill

> Atomic skill for mastering PHP testing strategies

## Overview

Comprehensive skill for PHP testing covering PHPUnit 11, Pest 3, TDD methodology, mocking strategies, and CI/CD integration.

## Skill Parameters

### Input Validation
```typescript
interface SkillParams {
  topic:
    | "phpunit"          // PHPUnit framework
    | "pest"             // Pest framework
    | "mocking"          // Mockery, Prophecy
    | "tdd"              // Test-driven development
    | "integration"      // Database, API testing
    | "ci-cd";           // GitHub Actions, GitLab CI

  level: "beginner" | "intermediate" | "advanced";
  framework?: "laravel" | "symfony" | "none";
  coverage_goal?: number;
}
```

### Validation Rules
```yaml
validation:
  topic:
    required: true
    allowed: [phpunit, pest, mocking, tdd, integration, ci-cd]
  level:
    required: true
  framework:
    default: "none"
```

## Learning Modules

### Module 1: PHPUnit Fundamentals
```yaml
beginner:
  - Test case structure
  - Basic assertions
  - Running tests

intermediate:
  - Data providers
  - Fixtures (setUp/tearDown)
  - Test doubles

advanced:
  - Attributes (#[Test], #[DataProvider])
  - Code coverage
  - Parallel execution
```

### Module 2: Pest Framework
```yaml
beginner:
  - Expectations syntax
  - Test organization
  - Groups and filtering

intermediate:
  - Higher-order tests
  - Datasets
  - Hooks

advanced:
  - Mutation testing (--mutate)
  - Architecture testing
  - Custom expectations
```

### Module 3: Mocking Strategies
```yaml
beginner:
  - Mock basics
  - Stubs vs mocks
  - Simple expectations

intermediate:
  - Partial mocks
  - Spies
  - Argument matching

advanced:
  - Mock chains
  - Return callbacks
  - Exception testing
```

## Error Handling & Retry Logic

```yaml
errors:
  TEST_FAILURE:
    code: "TEST_001"
    recovery: "Compare expected vs actual, check setup"

  MOCK_ERROR:
    code: "TEST_002"
    recovery: "Verify mock expectations and injection"

  FLAKY_TEST:
    code: "TEST_003"
    recovery: "Check isolation, fix race conditions"

retry:
  max_attempts: 2
  backoff:
    type: linear
    delay_ms: 100
```

## Code Examples

### PHPUnit Test (PHP 8.2+)
```php
<?php
declare(strict_types=1);

namespace Tests\Unit;

use App\Services\Calculator;
use PHPUnit\Framework\TestCase;
use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\Attributes\DataProvider;

final class CalculatorTest extends TestCase
{
    private Calculator $calculator;

    protected function setUp(): void
    {
        $this->calculator = new Calculator();
    }

    #[Test]
    public function it_adds_two_numbers(): void
    {
        $result = $this->calculator->add(2, 3);

        $this->assertSame(5, $result);
    }

    #[Test]
    #[DataProvider('divisionProvider')]
    public function it_divides_correctly(int $a, int $b, float $expected): void
    {
        $result = $this->calculator->divide($a, $b);

        $this->assertEqualsWithDelta($expected, $result, 0.0001);
    }

    public static function divisionProvider(): array
    {
        return [
            'whole' => [10, 2, 5.0],
            'decimal' => [7, 2, 3.5],
        ];
    }

    #[Test]
    public function it_throws_on_division_by_zero(): void
    {
        $this->expectException(\DivisionByZeroError::class);

        $this->calculator->divide(10, 0);
    }
}
```

### Pest Test
```php
<?php
use App\Models\User;
use function Pest\Laravel\{actingAs, post, assertDatabaseHas};

describe('User Registration', function () {
    it('allows new user registration', function () {
        post('/register', [
            'name' => 'John',
            'email' => 'john@example.com',
            'password' => 'password',
            'password_confirmation' => 'password',
        ])
        ->assertRedirect('/dashboard');

        assertDatabaseHas('users', ['email' => 'john@example.com']);
    });

    it('requires valid email', function () {
        post('/register', ['email' => 'invalid'])
            ->assertSessionHasErrors('email');
    });
})->group('auth');
```

### Mocking with Mockery
```php
<?php
declare(strict_types=1);

namespace Tests\Unit;

use App\Services\UserService;
use App\Repositories\UserRepository;
use Mockery;
use PHPUnit\Framework\TestCase;

final class UserServiceTest extends TestCase
{
    public function test_creates_user(): void
    {
        // Arrange
        $repository = Mockery::mock(UserRepository::class);
        $repository
            ->shouldReceive('create')
            ->once()
            ->with(['name' => 'John', 'email' => 'john@test.com'])
            ->andReturn(new User(['id' => 1]));

        $service = new UserService($repository);

        // Act
        $user = $service->createUser([
            'name' => 'John',
            'email' => 'john@test.com',
        ]);

        // Assert
        $this->assertEquals(1, $user->id);
    }

    protected function tearDown(): void
    {
        Mockery::close();
    }
}
```

### CI/CD Configuration (GitHub Actions)
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: '8.3'
          coverage: xdebug

      - name: Install dependencies
        run: composer install --no-progress

      - name: Run tests
        run: vendor/bin/phpunit --coverage-clover coverage.xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Tests pass locally, fail in CI | Environment differences | Check PHP version, database state |
| Mock not called | Not injected | Verify DI, don't instantiate inside class |
| Database pollution | Shared state | Use RefreshDatabase trait |
| Slow tests | Too many DB operations | Use mocks, run parallel |

## Quality Metrics

| Metric | Target |
|--------|--------|
| Code coverage | ≥80% |
| Test speed | <5 min full suite |
| Flaky rate | 0% |
| Test isolation | 100% |

## Usage

```
Skill("php-testing", {topic: "mocking", level: "intermediate"})
```
