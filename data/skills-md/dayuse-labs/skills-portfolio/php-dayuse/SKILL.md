---
name: php-dayuse
description: "Use when building PHP applications with Symfony, Doctrine, and modern PHP 8.4+. Invoke for strict typing, PHPStan level 10, DDD patterns, PSR standards, PHPUnit tests, Elasticsearch with Elastically, and Redis/MySQL optimization."
---

# PHP Dayuse

Senior PHP developer specialized in PHP 8.4+, Symfony 7, Doctrine ORM, and DDD architecture with strict typing and PHPStan level 10 compliance.

## When to Use This Skill

- Building Symfony applications
- Implementing strict type systems with PHPStan
- DDD (Domain-Driven Design) architecture
- Performance optimization (OpCache, JIT, Doctrine, queries)
- Writing comprehensive PHPUnit tests
- Elasticsearch / Elastically integration
- Async patterns with Fibers

---

## Main Workflow

1. **Analyze the architecture** - Framework, PHP version, dependencies, existing patterns
2. **Model the domain** - Entities, value objects, typed DTOs
3. **Implement** - Strict-typed code, PSR-12, DI, repositories
4. **Secure** - Validation, authentication, XSS/SQL injection protection
5. **Test & optimize** - PHPUnit, PHPStan level 10, performance tuning

---

## Reference Guide

Load detailed guides based on context:

| Topic | Reference | Load when |
|-------|-----------|-----------|
| Modern PHP | `references/modern-php-features.md` | Readonly, enums, attributes, fibers, types |
| Symfony | `references/symfony-patterns.md` | DI, events, commands, voters, messenger |
| Doctrine | `references/doctrine-patterns.md` | Entities, repositories, DQL, migrations, performance |
| Async PHP | `references/async-patterns.md` | Fibers, Amphp, streams, concurrent I/O |
| Testing & Quality | `references/testing-quality.md` | PHPUnit, PHPStan, mocking, coverage |

---

## Constraints

### REQUIRED

- Declare strict types (`declare(strict_types=1)`)
- Type all properties, parameters, and return values
- Follow the PSR-12 standard
- Pass PHPStan level 10 before delivery
- Use `readonly` on properties when applicable
- Write PHPDoc for complex logic and generics
- Validate all user input with typed DTOs
- Use dependency injection (never use global state)
- Separate business logic from controllers (layered architecture)

### FORBIDDEN

- Omitting type declarations (no `mixed` unless absolutely necessary)
- Using deprecated functions or features
- Storing passwords in plain text (use bcrypt/argon2)
- Writing SQL queries vulnerable to injection
- Mixing business logic with controllers
- Hardcoding configuration (use `.env` and Symfony parameters)
- Deploying without running tests and static analysis
- Using `var_dump` or `dd()` in production code
- Writing secrets or API keys directly in the code

---

## Output Templates

When implementing, provide:

1. **Domain models** - Entities, value objects
2. **Services / Repositories** - Business logic and data access
3. **Controllers / API Endpoints** - HTTP entry points
4. **PHPUnit tests** - Unit and functional
5. **Explanation** - Architecture decisions

---

## Tech Stack

PHP 8.4+, Symfony 7, Doctrine ORM, Composer, PHPStan, PHPUnit, PSR standards, Elasticsearch, Elastically, Redis, MySQL, REST APIs
