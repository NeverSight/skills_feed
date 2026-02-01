---
name: laravel-best-practices
description: "Comprehensive Laravel development guidelines for writing clean, maintainable, and idiomatic code. This skill provides rules and examples for application architecture, database optimization, and code style. Use this when: (1) writing or refactoring Laravel code, (2) reviewing pull requests, (3) designing system architecture, or (4) optimizing performance."
---

# Laravel Best Practices

A comprehensive guide to writing high-quality Laravel applications, inspired by Vercel's React Best Practices and community standards. Adhere to these rules to ensure your code is idiomatic, scalable, and maintainable. Compatible with Laravel 10, 11, and 12.

## Core Categories

| Priority | Category | Impact | Rule Prefix |
|----------|----------|--------|-------------|
| 1 | Architecture & Logic | CRITICAL | `arch-` |
| 2 | Database & Performance | HIGH | `db-` |
| 3 | Code Quality & Style | MEDIUM | `style-` |

## 1. Architecture & Logic (CRITICAL)

- `arch-fat-models-skinny-controllers` - Move logic from controllers to models/services.
- `arch-validation-in-form-requests` - Extract validation rules to dedicated Request classes.
- `arch-business-logic-in-services` - Encapsulate complex logic in Service classes.
- `arch-dependency-injection` - Use IoC container for loose coupling.
- `arch-standard-tools` - Use established Laravel tools and community packages.

## 2. Database & Performance (HIGH)

- `db-prevent-n-plus-one` - Always eager load relationships (`with()`).
- `db-eloquent-over-raw-sql` - Use Eloquent ORM for readability and security.
- `db-mass-assignment` - Use fillable/guarded with `create()` or `update()`.
- `db-chunk-data` - Use `chunk()` or `cursor()` for large datasets.
- `db-eloquent-scopes` - Reuse query logic with Eloquent scopes.

## 3. Code Quality & Style (MEDIUM)

- `style-naming-conventions` - Follow standard Laravel naming (Singular/Plural).
- `style-no-env-directly` - Access environment variables via `config()` only.
- `style-date-handling` - Use UTC and Eloquent casts for date management.
- `style-descriptive-names` - Code should be self-documenting; comments explain "why".
- `style-separate-js-css` - Keep assets out of Blade templates.

## How to Use

Refer to the individual rule files in the `references/` directory for detailed explanations, "Bad" examples, and "Good" examples:

```bash
references/fat-models-skinny-controllers.md
references/prevent-n-plus-one.md
references/no-env-directly.md
```

## Review Checklist

When building or reviewing Laravel code, ensure:
1.  **Controllers** are minimal (Skinny).
2.  **Validation** is in Form Requests.
3.  **Queries** are optimized (Eager loading).
4.  **Logic** is testable and separated.
5.  **Environment** variables are accessed via Config.