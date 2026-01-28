---
name: typo3-extension-upgrade
description: Systematic TYPO3 extension upgrades to newer LTS versions. Covers Extension Scanner, Rector, Fractor, PHPStan, and testing.
version: 1.0.0
typo3_compatibility: "13.0 - 14.x"
triggers:
  - extension
  - upgrade
  - fractor
  - rector
  - migration
---

# TYPO3 Extension Upgrade Skill

Systematic framework for upgrading TYPO3 extensions to newer LTS versions.

> **Scope**: Extension code upgrades only. NOT for TYPO3 project/core upgrades.

## Upgrade Toolkit

| Tool | Purpose | Files |
|------|---------|-------|
| Extension Scanner | Diagnose deprecated APIs | TYPO3 Backend |
| Rector | Automated PHP migrations | `.php` |
| Fractor | Non-PHP migrations | FlexForms, TypoScript, YAML, Fluid |
| PHPStan | Static analysis | `.php` |

## Planning Phase (Required)

Before ANY code changes for major upgrades:

1. **List all files with hardcoded versions** (composer.json, CI, Docker, Rector)
2. **Document scope** - how many places need changes?
3. **Present plan to user** for approval
4. **Track progress** with todo list

### Pre-Upgrade Checklist

- [ ] Extension key and current TYPO3 version documented
- [ ] Target TYPO3 version(s) identified (v13, v14, or both)
- [ ] Current PHP version and target PHP version noted
- [ ] All deprecation warnings from logs collected
- [ ] Extension Scanner report reviewed
- [ ] Dependencies checked for target version compatibility

## Upgrade Workflow

### 1. Prepare Environment

```bash
# Create backup/snapshot
ddev snapshot --name=before-upgrade

# Verify git is clean
git status

# Create feature branch
git checkout -b feature/typo3-14-upgrade
```

### 2. Update Version Constraints

```json
// composer.json
{
    "require": {
        "php": "^8.2",
        "typo3/cms-core": "^13.0 || ^14.0"
    }
}
```

```php
// ext_emconf.php
$EM_CONF[$_EXTKEY] = [
    'constraints' => [
        'depends' => [
            'typo3' => '13.0.0-14.99.99',
            'php' => '8.2.0-8.4.99',
        ],
    ],
];
```

### 3. Run Rector

Rector handles PHP code migrations automatically.

#### Configuration

```php
<?php
// rector.php
declare(strict_types=1);

use Rector\Config\RectorConfig;
use Rector\Set\ValueObject\LevelSetList;
use Ssch\TYPO3Rector\Set\Typo3LevelSetList;
use Ssch\TYPO3Rector\Set\Typo3SetList;

return RectorConfig::configure()
    ->withPaths([
        __DIR__ . '/Classes',
        __DIR__ . '/Configuration',
        __DIR__ . '/Tests',
    ])
    ->withSkip([
        __DIR__ . '/Resources',
    ])
    ->withSets([
        // PHP version upgrades
        LevelSetList::UP_TO_PHP_82,
        
        // TYPO3 upgrades
        Typo3LevelSetList::UP_TO_TYPO3_13,
        Typo3SetList::TYPO3_13,
    ])
    ->withImportNames();
```

#### Run Rector

```bash
# Dry run first
vendor/bin/rector process --dry-run

# Review changes, then apply
vendor/bin/rector process

# Review git diff
git diff
```

### 4. Run Fractor

Fractor handles non-PHP file migrations (FlexForms, TypoScript, YAML).

#### Configuration

```php
<?php
// fractor.php
declare(strict_types=1);

use a]9r\Fractor\Configuration\FractorConfiguration;
use a9f\Typo3Fractor\Set\Typo3LevelSetList;

return FractorConfiguration::configure()
    ->withPaths([
        __DIR__ . '/Configuration',
        __DIR__ . '/Resources',
    ])
    ->withSets([
        Typo3LevelSetList::UP_TO_TYPO3_13,
    ]);
```

#### Run Fractor

```bash
# Dry run first
vendor/bin/fractor process --dry-run

# Review changes, then apply
vendor/bin/fractor process
```

### 5. Fix Code Style

```bash
# Run PHP-CS-Fixer
vendor/bin/php-cs-fixer fix

# Verify no issues remain
vendor/bin/php-cs-fixer fix --dry-run
```

### 6. Run PHPStan

```bash
# Analyze codebase
vendor/bin/phpstan analyse

# Fix any reported issues
# Then re-run until clean
```

### 7. Run Tests

```bash
# Unit tests
vendor/bin/phpunit -c Tests/UnitTests.xml

# Functional tests
vendor/bin/phpunit -c Tests/FunctionalTests.xml

# Fix failing tests
```

### 8. Manual Testing

```bash
# Test in target TYPO3 version
ddev composer require "typo3/cms-core:^14.0" --no-update
ddev composer update
ddev typo3 cache:flush

# Test all extension functionality:
# - Backend modules
# - Frontend plugins
# - CLI commands
# - Scheduler tasks
```

## Common Migration Patterns

### ViewFactory (Replaces StandaloneView)

```php
// ❌ OLD (deprecated in v13, removed in v14)
use TYPO3\CMS\Fluid\View\StandaloneView;

$view = GeneralUtility::makeInstance(StandaloneView::class);
$view->setTemplatePathAndFilename('...');

// ✅ NEW (v13/v14 compatible)
use TYPO3\CMS\Core\View\ViewFactoryInterface;
use TYPO3\CMS\Core\View\ViewFactoryData;

public function __construct(
    private readonly ViewFactoryInterface $viewFactory,
) {}

public function render(ServerRequestInterface $request): string
{
    $viewFactoryData = new ViewFactoryData(
        templateRootPaths: ['EXT:my_ext/Resources/Private/Templates'],
        request: $request,
    );
    $view = $this->viewFactory->create($viewFactoryData);
    $view->assign('data', $data);
    return $view->render('MyTemplate');
}
```

### Controller ResponseInterface

```php
// ❌ OLD (v12 and earlier)
public function listAction(): void
{
    $this->view->assign('items', $items);
}

// ✅ NEW (v13+ required)
public function listAction(): ResponseInterface
{
    $this->view->assign('items', $items);
    return $this->htmlResponse();
}
```

### PSR-14 Events (Replace Hooks)

```php
// ❌ OLD (hooks deprecated)
$GLOBALS['TYPO3_CONF_VARS']['SC_OPTIONS']['...']['hook'][] = MyHook::class;

// ✅ NEW (PSR-14 events)
// Configuration/Services.yaml
services:
  Vendor\MyExt\EventListener\MyListener:
    tags:
      - name: event.listener
        identifier: 'myext/my-listener'

// Or use PHP attribute
#[AsEventListener(identifier: 'myext/my-listener')]
final class MyListener
{
    public function __invoke(SomeEvent $event): void
    {
        // Handle event
    }
}
```

### Static TCA (No Runtime Modifications)

```php
// ❌ OLD (runtime TCA modification - forbidden in v14)
// ext_tables.php
$GLOBALS['TCA']['tt_content']['columns']['myfield'] = [...];

// ✅ NEW (static TCA files only)
// Configuration/TCA/Overrides/tt_content.php
$GLOBALS['TCA']['tt_content']['columns']['myfield'] = [...];
```

### Backend Module Registration

```php
// ❌ OLD (ext_tables.php registration)
ExtensionUtility::registerModule(...);

// ✅ NEW (Configuration/Backend/Modules.php)
return [
    'web_mymodule' => [
        'parent' => 'web',
        'access' => 'user,group',
        'iconIdentifier' => 'myext-module',
        'labels' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang_mod.xlf',
        'extensionName' => 'MyExt',
        'controllerActions' => [
            MyController::class => ['index', 'list'],
        ],
    ],
];
```

## API Changes Reference

### TYPO3 v13 Breaking Changes

| Removed/Changed | Replacement |
|-----------------|-------------|
| `StandaloneView` | `ViewFactoryInterface` |
| `ObjectManager` | Constructor injection |
| `TSFE->fe_user->user` | Request attribute |
| Various hooks | PSR-14 events |

### TYPO3 v14 Breaking Changes

| Removed/Changed | Replacement |
|-----------------|-------------|
| Runtime TCA changes | Static TCA only |
| Legacy backend modules | Modules.php |
| `$GLOBALS['TYPO3_DB']` | QueryBuilder |

## Troubleshooting

### Rector Fails

```bash
# Clear Rector cache
rm -rf .rector_cache/

# Run with verbose output
vendor/bin/rector process --dry-run -vvv

# Skip problematic rules
# Add to rector.php:
->withSkip([
    \Ssch\TYPO3Rector\SomeRule::class,
])
```

### PHPStan Errors

```bash
# Generate baseline for existing issues
vendor/bin/phpstan analyse --generate-baseline

# Add to phpstan.neon:
includes:
    - phpstan-baseline.neon
```

### Extension Not Found

```bash
# Regenerate autoload
ddev composer dump-autoload

# Clear all caches
ddev typo3 cache:flush
rm -rf var/cache/*

# Re-setup extension
ddev typo3 extension:setup
```

### Database Issues

```bash
# Check for schema differences
ddev typo3 database:updateschema --verbose

# Apply schema changes
ddev typo3 database:updateschema "*.add,*.change"
```

## Success Criteria

Before considering upgrade complete:

- [ ] `rector --dry-run` shows no changes
- [ ] `fractor --dry-run` shows no changes
- [ ] `phpstan analyse` passes
- [ ] `php-cs-fixer --dry-run` passes
- [ ] All unit tests pass
- [ ] All functional tests pass
- [ ] Manual testing in target version(s) complete
- [ ] No deprecation warnings in logs
- [ ] Extension works in TYPO3 v13
- [ ] Extension works in TYPO3 v14

## Resources

- **TYPO3 v13 Changelog**: https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog-13.html
- **TYPO3 v14 Changelog**: https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog-14.html
- **TYPO3 Rector**: https://github.com/sabbelasichon/typo3-rector
- **Fractor**: https://github.com/andreaswolf/fractor

---

## Credits & Attribution

This skill is based on the excellent work by
**[Netresearch DTT GmbH](https://www.netresearch.de/)**.

Original repository: https://github.com/netresearch/typo3-extension-upgrade-skill

**Copyright (c) Netresearch DTT GmbH** - Methodology and best practices  
Adapted by webconsulting.at for this skill collection
