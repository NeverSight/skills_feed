---
name: laravel-packages
description: Package development and extraction of reusable code. Use when working with package development, code reusability, or when user mentions packages, composer packages, extract package, reusable code, package development.
---

# Laravel Packages

Package development: extracting reusable patterns for use across projects.

**Related guides:**
- [package-extraction.md](references/package-extraction.md) - Extracting code into packages
- [DTOs](../laravel-dtos/SKILL.md) - Using Spatie Laravel Data
- [Models](../laravel-models/SKILL.md) - Using Spatie Model States and Query Builder

## When to Extract

Extract to package when:
1. Pattern used in 3+ projects
2. Code is stable and well-tested
3. Pattern has clear boundaries
4. Maintenance cost justified

**[→ Complete extraction guide: package-extraction.md](references/package-extraction.md)**

## Package Structure

```
my-package/
├── src/
│   ├── PackageServiceProvider.php
│   ├── Actions/
│   ├── DTOs/
│   └── ...
├── tests/
├── composer.json
└── README.md
```

Use semantic versioning. Test packages independently. Document clearly.

## Core Packages (Always)

### Spatie Laravel Data
```bash
composer require spatie/laravel-data
```
- DTOs with casting, validation, transformers
- Test factory support

### Spatie Model States
```bash
composer require spatie/laravel-model-states
```
- State machine pattern
- State transitions with dedicated classes

### Spatie Query Builder
```bash
composer require spatie/laravel-query-builder
```
- Filter, sort, include relations via query strings
- API-friendly querying

### Saloon
```bash
composer require saloonphp/saloon saloonphp/laravel-plugin
```
- Elegant API client builder
- Testable external service integrations

### Pest
```bash
composer require pestphp/pest pestphp/pest-plugin-laravel --dev
```
- Expressive testing framework
- Architecture tests

## Optional Packages

### Laravel Sanctum
```bash
composer require laravel/sanctum
```
**When:** API authentication needed

### Stancl Tenancy
```bash
composer require stancl/tenancy
```
**When:** Multi-tenant application

### Spatie Settings
```bash
composer require spatie/laravel-settings
```
**When:** Application-level settings needed

## Installation Commands

### Full Install
```bash
composer require \
  spatie/laravel-data \
  spatie/laravel-model-states \
  spatie/laravel-query-builder \
  saloonphp/saloon \
  saloonphp/laravel-plugin

composer require \
  pestphp/pest \
  pestphp/pest-plugin-laravel \
  --dev

./vendor/bin/pest --init
```

### Minimal Install
```bash
composer require spatie/laravel-data
composer require pestphp/pest pestphp/pest-plugin-laravel --dev
./vendor/bin/pest --init
```
