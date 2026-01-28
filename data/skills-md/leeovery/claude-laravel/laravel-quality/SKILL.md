---
name: laravel-quality
description: Code quality tooling with PHPStan, Pint, and strict types. Use when working with code quality, static analysis, formatting, or when user mentions PHPStan, Pint, quality, static analysis, type safety, code style, linting.
---

# Laravel Quality

Testing, static analysis, and code quality enforcement.

**Related guides:**
- [code-style.md](references/code-style.md) - Laravel Pint configuration and coding style
- [type-safety.md](references/type-safety.md) - Strict types and type hints
- [Testing](../laravel-testing/SKILL.md) - Comprehensive testing guide

## Quality Stack

```bash
# composer.json scripts
{
    "test": "pest",
    "analyse": "phpstan analyse",
    "format": "pint",
    "quality": [
        "@analyse",
        "@test"
    ]
}
```

All files must have `declare(strict_types=1)` at top. Run quality checks before every commit.

## Architecture Tests (Pest)

### Setup

`tests/Pest.php`
```php
pest()->extend(Tests\TestCase::class)->in('Feature', 'Unit');
```

### Core Architecture Tests

`tests/Architecture/ActionsTest.php`
```php
<?php

declare(strict_types=1);

arch('actions are invokable')
    ->expect('App\Actions')
    ->toHaveMethod('__invoke');

arch('actions live in Actions namespace')
    ->expect('App\Actions')
    ->toBeClasses()
    ->toOnlyBeUsedIn('App\Actions', 'App\Http', 'App\Jobs', 'App\Listeners');

arch('actions do not use models directly')
    ->expect('App\Actions')
    ->not->toUse('Illuminate\Database\Eloquent\Model');
```

`tests/Architecture/DataTest.php`
```php
<?php

declare(strict_types=1);

arch('data objects extend base Data class')
    ->expect('App\Data')
    ->toExtend('App\Data\Data')
    ->ignoring('App\Data\Data');

arch('data objects use constructor property promotion')
    ->expect('App\Data')
    ->toHaveConstructor();
```

`tests/Architecture/StrictTypesTest.php`
```php
<?php

declare(strict_types=1);

arch('app files declare strict types')
    ->expect('App')
    ->toUseStrictTypes();

arch('test files declare strict types')
    ->expect('Tests')
    ->toUseStrictTypes();
```

`tests/Architecture/ControllersTest.php`
```php
<?php

declare(strict_types=1);

arch('controllers do not use DB facade')
    ->expect('App\Http')
    ->not->toUse('Illuminate\Support\Facades\DB');

arch('controllers do not use models directly')
    ->expect('App\Http\Web\Controllers')
    ->not->toUse('App\Models');
```

`tests/Architecture/NamingTest.php`
```php
<?php

declare(strict_types=1);

arch('actions end with Action suffix')
    ->expect('App\Actions')
    ->toHaveSuffix('Action');

arch('data objects end with Data suffix')
    ->expect('App\Data')
    ->toHaveSuffix('Data')
    ->ignoring('App\Data\Data', 'App\Data\Concerns');

arch('exceptions end with Exception suffix')
    ->expect('App\Exceptions')
    ->toHaveSuffix('Exception')
    ->ignoring('App\Exceptions\Concerns');
```

`tests/Architecture/ModelsTest.php`
```php
<?php

declare(strict_types=1);

arch('models use custom query builders')
    ->expect('App\Models')
    ->toHaveMethod('newEloquentBuilder');

arch('models do not use local scopes')
    ->expect('App\Models')
    ->not->toHaveMethod('scope*');
```

## Static Analysis (PHPStan)

### Installation
```bash
composer require phpstan/phpstan --dev
composer require phpstan/phpstan-strict-rules --dev
composer require larastan/larastan --dev
```

### Configuration

`phpstan.neon`
```neon
includes:
    - vendor/larastan/larastan/extension.neon
    - vendor/phpstan/phpstan-strict-rules/rules.neon

parameters:
    level: 8
    paths:
        - app
        - tests
    excludePaths:
        - app/Providers/TelescopeServiceProvider.php
    checkMissingIterableValueType: true
    checkGenericClassInNonGenericObjectType: true
    reportUnmatchedIgnoredErrors: false
```

### Run
```bash
./vendor/bin/phpstan analyse
```

## Code Style (Laravel Pint)

### Installation
```bash
composer require laravel/pint --dev
```

### Configuration

`pint.json`
```json
{
    "preset": "laravel",
    "rules": {
        "simplified_null_return": true,
        "no_unused_imports": true,
        "ordered_imports": {
            "sort_algorithm": "alpha"
        }
    }
}
```

### Run
```bash
./vendor/bin/pint
./vendor/bin/pint --test  # Check only
```

## Test Coverage

### Enable Coverage (Pest)

`phpunit.xml`
```xml
<coverage>
    <report>
        <html outputDirectory="coverage"/>
        <text outputFile="php://stdout"/>
    </report>
</coverage>
```

### Run with Coverage
```bash
./vendor/bin/pest --coverage
./vendor/bin/pest --coverage --min=80  # Enforce minimum
```

## CI/CD Checks

### GitHub Actions Example

`.github/workflows/tests.yml`
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: 8.4
          extensions: dom, curl, libxml, mbstring, zip, pcntl, pdo, sqlite, pdo_sqlite
          coverage: xdebug

      - name: Install Dependencies
        run: composer install --prefer-dist --no-interaction

      - name: Code Style
        run: ./vendor/bin/pint --test

      - name: Static Analysis
        run: ./vendor/bin/phpstan analyse

      - name: Run Tests
        run: ./vendor/bin/pest --coverage --min=80
```

## Pre-commit Hooks

### Installation
```bash
composer require brainmaestro/composer-git-hooks --dev
```

### Configuration

`composer.json`
```json
{
    "extra": {
        "hooks": {
            "pre-commit": [
                "./vendor/bin/pint",
                "./vendor/bin/phpstan analyse",
                "./vendor/bin/pest"
            ]
        }
    },
    "scripts": {
        "post-install-cmd": "vendor/bin/cghooks add --ignore-lock",
        "post-update-cmd": "vendor/bin/cghooks update"
    }
}
```

## Quality Metrics

### What to Track

- **Test coverage** - Aim for 80%+
- **PHPStan level** - Level 8 (max)
- **Architecture test pass rate** - 100%
- **Code style violations** - 0

### Regular Reviews

- **Weekly** - Check test coverage trends
- **Per PR** - Run all quality checks
- **Monthly** - Review architecture compliance
- **Release** - Full quality audit

## Common Issues to Watch

### Anti-patterns
- Domain logic in controllers
- Using scopes instead of builders
- Missing strict types declaration
- Passing primitives instead of DTOs
- Jobs/Listeners with domain logic

### Type Safety
- Missing return types
- Missing parameter types
- Missing property types
- Untyped arrays/collections

### Testing
- Missing feature tests for endpoints
- Missing unit tests for actions
- Low coverage on critical paths
- Brittle tests (too many mocks)

## Enforcement Strategy

1. **Architecture tests** - Automated checks
2. **PR reviews** - Manual verification
3. **CI/CD gates** - Block failing builds
4. **Team standards** - Document + training
5. **Pair programming** - Share knowledge
