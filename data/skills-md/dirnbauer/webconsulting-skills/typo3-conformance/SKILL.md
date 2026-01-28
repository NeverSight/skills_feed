---
name: typo3-conformance
description: Evaluate TYPO3 extensions for conformance to v13/v14 standards. Use when assessing quality, generating reports, or planning modernization.
version: 1.0.0
typo3_compatibility: "13.0 - 14.x"
file_triggers:
  - ext_emconf.php
  - ext_localconf.php
  - Configuration/TCA/**/*
  - "*.typoscript"
triggers:
  - conformance
  - standards
  - quality
  - assessment
---

# TYPO3 Extension Conformance Checker

Evaluate TYPO3 extensions for standards compliance, architecture patterns, and best practices.

## Skill Delegation

| Skill | Use For |
|-------|---------|
| **typo3-testing** | PHPUnit config, test patterns, coverage |
| **typo3-docs** | RST validation, documentation rendering |
| **php-modernization** | PHP 8.x patterns, PHPStan, type safety |

## Evaluation Workflow

1. **Initial Assessment** - Extension key, TYPO3 version, type
2. **File Structure** - composer.json, ext_emconf.php, required directories
3. **Coding Standards** - strict_types, types, PSR-12/PER
4. **Backend Module v13+** - ES6 modules, Modal API, CSRF
5. **PHP Architecture** - Services.yaml, DI, PSR-14 events
6. **Testing** - PHPUnit, Playwright E2E, coverage >70%
7. **Best Practices** - DDEV, runTests.sh, quality tools, CI/CD

## Scoring System

### Base Score (0-100 points)

| Category | Max Points | Requirements |
|----------|------------|--------------|
| Architecture | 20 | Directory structure, namespace, autoloading |
| Coding Guidelines | 20 | PSR-12/PER, strict_types, documentation |
| PHP Quality | 20 | Types, PHPStan level 9+, no deprecations |
| Testing | 20 | Unit tests, functional tests, 70%+ coverage |
| Best Practices | 20 | CI/CD, quality tools, documentation |

### Excellence Bonus (0-22 points)

| Feature | Points | Description |
|---------|--------|-------------|
| PHPat architecture tests | 5 | Layer constraints enforced |
| Mutation testing | 5 | Infection with 70%+ MSI |
| E2E tests | 4 | Playwright or Codeception |
| 90%+ code coverage | 4 | Exceptional test coverage |
| OpenSSF Scorecard | 4 | Security best practices |

## Required File Structure

```
my_extension/
├── Classes/
│   ├── Controller/
│   ├── Domain/
│   │   ├── Model/
│   │   └── Repository/
│   ├── Service/
│   └── EventListener/
├── Configuration/
│   ├── Backend/
│   │   └── Modules.php
│   ├── Icons.php
│   ├── Services.yaml
│   ├── TCA/
│   │   ├── Overrides/
│   │   └── tx_myext_*.php
│   └── TypoScript/
│       ├── setup.typoscript
│       └── constants.typoscript
├── Documentation/
│   ├── Index.rst
│   └── guides.xml
├── Resources/
│   ├── Private/
│   │   ├── Language/
│   │   ├── Layouts/
│   │   ├── Partials/
│   │   └── Templates/
│   └── Public/
│       ├── Css/
│       ├── Icons/
│       └── JavaScript/
├── Tests/
│   ├── Functional/
│   └── Unit/
├── composer.json
├── ext_emconf.php
├── ext_localconf.php
└── ext_tables.php
```

## Coding Standards Checklist

### PHP Files

- [ ] `declare(strict_types=1);` in every file
- [ ] PSR-4 namespace matching directory structure
- [ ] Full type declarations (parameters, returns, properties)
- [ ] `final` keyword on classes not designed for inheritance
- [ ] `readonly` on immutable classes (PHP 8.2+)
- [ ] Constructor property promotion used
- [ ] No `@var` annotations when type is declared

### Example: Conformant Service

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Service;

use Psr\Log\LoggerInterface;
use TYPO3\CMS\Core\Database\ConnectionPool;

final readonly class ItemService
{
    public function __construct(
        private ConnectionPool $connectionPool,
        private LoggerInterface $logger,
    ) {}

    /**
     * @return array<int, array<string, mixed>>
     */
    public function findActiveItems(): array
    {
        $queryBuilder = $this->connectionPool->getQueryBuilderForTable('tx_myext_items');
        
        return $queryBuilder
            ->select('*')
            ->from('tx_myext_items')
            ->where($queryBuilder->expr()->eq('active', 1))
            ->executeQuery()
            ->fetchAllAssociative();
    }
}
```

## Backend Module Standards (v13/v14)

### Required Patterns

```php
<?php
// Configuration/Backend/Modules.php
return [
    'web_myextension' => [
        'parent' => 'web',
        'position' => ['after' => 'web_info'],
        'access' => 'user,group',
        'iconIdentifier' => 'myextension-module',
        'path' => '/module/web/myextension',
        'labels' => 'LLL:EXT:my_extension/Resources/Private/Language/locallang_mod.xlf',
        'extensionName' => 'MyExtension',
        'controllerActions' => [
            \Vendor\MyExtension\Controller\BackendController::class => [
                'index',
                'list',
            ],
        ],
    ],
];
```

### ES6 Module Requirements

```javascript
// Resources/Public/JavaScript/MyModule.js
import Modal from '@typo3/backend/modal.js';
import Notification from '@typo3/backend/notification.js';

export default class MyModule {
    constructor() {
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        document.querySelectorAll('[data-action="delete"]').forEach(element => {
            element.addEventListener('click', this.handleDelete.bind(this));
        });
    }

    handleDelete(event) {
        event.preventDefault();
        Modal.confirm(
            'Delete Item',
            'Are you sure?',
            Modal.severity.warning,
            [
                { text: 'Cancel', trigger: () => Modal.dismiss() },
                { text: 'Delete', trigger: () => this.performDelete(), btnClass: 'btn-danger' }
            ]
        );
    }
}
```

## PHP Architecture Requirements

### Services.yaml

```yaml
# Configuration/Services.yaml
services:
  _defaults:
    autowire: true
    autoconfigure: true
    public: false

  Vendor\MyExtension\:
    resource: '../Classes/*'
    exclude:
      - '../Classes/Domain/Model/*'

  # Explicit public services if needed
  Vendor\MyExtension\Service\PublicApiService:
    public: true
```

### PSR-14 Event Listeners

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\EventListener;

use TYPO3\CMS\Core\Attribute\AsEventListener;
use TYPO3\CMS\Core\DataHandling\Event\AfterRecordOperationEvent;

#[AsEventListener(identifier: 'myext/after-record-operation')]
final readonly class RecordOperationListener
{
    public function __invoke(AfterRecordOperationEvent $event): void
    {
        if ($event->getTable() !== 'tx_myext_items') {
            return;
        }
        
        // Handle event...
    }
}
```

## Testing Standards

### Required Tests

| Type | Requirement | Tool |
|------|-------------|------|
| Unit | Required, 70%+ coverage | PHPUnit |
| Functional | Required for DB operations | PHPUnit + TYPO3 Framework |
| Architecture | Required for full points | PHPat |
| E2E | Optional bonus | Playwright |

### PHPUnit Configuration

```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="vendor/phpunit/phpunit/phpunit.xsd"
         bootstrap="vendor/typo3/testing-framework/Resources/Core/Build/UnitTestsBootstrap.php"
         colors="true">
    <testsuites>
        <testsuite name="Unit">
            <directory>Tests/Unit</directory>
        </testsuite>
        <testsuite name="Functional">
            <directory>Tests/Functional</directory>
        </testsuite>
    </testsuites>
    <coverage>
        <report>
            <clover outputFile="var/log/coverage.xml"/>
            <html outputDirectory="var/log/coverage"/>
        </report>
    </coverage>
    <source>
        <include>
            <directory>Classes</directory>
        </include>
    </source>
</phpunit>
```

### PHPat Architecture Test

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Tests\Architecture;

use PHPat\Selector\Selector;
use PHPat\Test\Builder\Rule;
use PHPat\Test\PHPat;

final class ArchitectureTest
{
    public function testDomainModelIndependence(): Rule
    {
        return PHPat::rule()
            ->classes(Selector::inNamespace('Vendor\MyExtension\Domain\Model'))
            ->shouldNotDependOn()
            ->classes(Selector::inNamespace('Vendor\MyExtension\Controller'));
    }

    public function testServicesDoNotDependOnControllers(): Rule
    {
        return PHPat::rule()
            ->classes(Selector::inNamespace('Vendor\MyExtension\Service'))
            ->shouldNotDependOn()
            ->classes(Selector::inNamespace('Vendor\MyExtension\Controller'));
    }
}
```

## Quality Tools

### Required Configuration

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: '8.3'
          
      - name: Install dependencies
        run: composer install
        
      - name: PHPStan
        run: vendor/bin/phpstan analyse --level=9
        
      - name: PHP-CS-Fixer
        run: vendor/bin/php-cs-fixer fix --dry-run --diff
        
      - name: PHPUnit
        run: vendor/bin/phpunit --coverage-clover var/log/coverage.xml
```

### PHPStan Configuration

```neon
# phpstan.neon
includes:
    - vendor/phpstan/phpstan-strict-rules/rules.neon
    - vendor/saschaegerer/phpstan-typo3/extension.neon

parameters:
    level: 9
    paths:
        - Classes
        - Tests
    excludePaths:
        - Tests/Fixtures/*
```

## Scoring Interpretation

| Score | Grade | Status |
|-------|-------|--------|
| 90-122 | A+ | Excellent - Enterprise Ready |
| 80-89 | A | Production Ready |
| 70-79 | B | Development Ready |
| 60-69 | C | Basic - Needs Work |
| <60 | F | Not Conformant |

---

## Credits & Attribution

This skill is based on the excellent work by
**[Netresearch DTT GmbH](https://www.netresearch.de/)**.

Original repository: https://github.com/netresearch/typo3-conformance-skill

**Copyright (c) Netresearch DTT GmbH** - Methodology and best practices  
Adapted by webconsulting.at for this skill collection
