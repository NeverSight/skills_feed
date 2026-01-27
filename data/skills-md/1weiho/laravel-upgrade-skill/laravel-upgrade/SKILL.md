---
name: laravel-upgrade
description: Upgrade Laravel applications one major version at a time (9→10, 10→11, 11→12). Use when user wants to upgrade their Laravel framework version. Auto-detects current version from composer.json, identifies breaking changes, and applies necessary code fixes.
---

# Laravel Upgrade

Upgrade Laravel applications one major version at a time. Supports: 9→10, 10→11, 11→12.

## Workflow

### 1. Detect Current Version

Read `composer.json` and find the `laravel/framework` version constraint:

```php
// Example: "laravel/framework": "^10.0" means Laravel 10.x
```

Determine target version (current + 1). If already on Laravel 12, inform user they're on the latest supported version.

### 2. Load Upgrade Guide

Based on detected versions, read the appropriate reference file:

| Current | Target | Reference File |
|---------|--------|----------------|
| 9.x | 10.x | [references/from-9-to-10.md](references/from-9-to-10.md) |
| 10.x | 11.x | [references/from-10-to-11.md](references/from-10-to-11.md) |
| 11.x | 12.x | [references/from-11-to-12.md](references/from-11-to-12.md) |

### 3. Scan and Fix

For each breaking change in the guide, scan the codebase and apply fixes:

**High Impact** (always check):
- `composer.json` dependency versions
- PHP version requirements
- Database migrations using deprecated methods

**Medium Impact** (check relevant files):
- Model `$dates` property → `$casts` (9→10)
- Database expressions with `(string)` casting (9→10)
- Column modification migrations missing attributes (10→11)
- `HasUuids` trait behavior change (11→12)

**Low Impact** (check if patterns found):
- Deprecated method calls (`Bus::dispatchNow`, `Redirect::home`, etc.)
- Contract interface changes
- Configuration file updates

### 4. Update Dependencies

After code fixes, update `composer.json`:

```bash
# Update laravel/framework constraint to target version
# Update related packages per upgrade guide
composer update
```

### 5. Post-Upgrade Verification

- Run `php artisan` to verify framework boots
- Run test suite if available
- Check for deprecation warnings in logs

## Common Patterns

### Dependency Updates (all upgrades)

Search `composer.json` for outdated constraints and update per guide.

### Model $dates to $casts (9→10)

```php
// Before
protected $dates = ['deployed_at'];

// After
protected $casts = ['deployed_at' => 'datetime'];
```

Search pattern: `protected \$dates\s*=`

### Database Expression Casting (9→10)

```php
// Before
$string = (string) DB::raw('select 1');

// After
$string = DB::raw('select 1')->getValue(DB::connection()->getQueryGrammar());
```

### Column Modification (10→11)

Migrations using `->change()` must now include all modifiers:

```php
// Before (implicit retention)
$table->integer('votes')->nullable()->change();

// After (explicit)
$table->integer('votes')->unsigned()->default(1)->nullable()->change();
```

### HasUuids Trait (11→12)

```php
// Before (ordered UUIDv4)
use Illuminate\Database\Eloquent\Concerns\HasUuids;

// After (if you need UUIDv4 behavior)
use Illuminate\Database\Eloquent\Concerns\HasVersion4Uuids as HasUuids;
```
