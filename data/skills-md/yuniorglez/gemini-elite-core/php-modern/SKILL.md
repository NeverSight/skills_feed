---
name: php-modern
id: php-modern
version: 1.1.0
description: "Master of Modern PHP (8.4-8.6+), specialized in Property Hooks, Partial Function Application, and High-Performance Engine optimization."
last_updated: "2026-01-22"
---

# Skill: PHP Modern (Standard 2026)

**Role:** The Modern PHP Specialist is responsible for architecting robust, high-performance backends using the latest language features. In 2026, PHP has shed its legacy reputation, offering first-class syntax like Property Hooks, Pipe Operators, and Native URI handling. This skill focuses on leveraging these for "Clean Code" that executes with near-native efficiency.

## 🎯 Primary Objectives
1.  **Syntactic Excellence:** Mastery of PHP 8.4 Property Hooks and PHP 8.5/8.6 Pipe Operators (`|>`) and Partial Function Application.
2.  **Type Safety:** Utilizing Intersection Types, Disjunctive Normal Form (DNF) types, and `#[NoDiscard]` for bulletproof APIs.
3.  **Engine Mastery:** Optimizing JIT (Just-In-Time) compilation and persistent handle sharing for high-scale applications.
4.  **Security First:** Implementing modern cryptography (Sodium) and secure data encoding natively.

---

## 🏗️ The 2026 Toolbelt

### 1. Language Features
- **Property Hooks:** Logic-embedded properties (no more boilerplate getters/setters).
- **Pipe Operator (`|>`):** Left-to-right functional composition.
- **Clone With:** Immutable state updates in a single expression.
- **Partial Function Application:** Creating closures with placeholders (`?`).

### 2. Static Analysis & Tooling
- **PHPStan / Psalm (Level 9+):** Mandatory for all Squaads codebases.
- **Rector:** Automated migrations and code quality refactors.
- **Pest 3.x:** Functional and architectural testing.

---

## 🛠️ Implementation Patterns

### 1. Property Hooks (PHP 8.4+)
Eliminating getters/setters for clean, reactive-like properties.

```php
class User {
    public string $name {
        set => trim($value);
        get => ucfirst($this->name);
    }

    public string $fullName {
        get => "{$this->firstName} {$this->lastName}";
    }
}
```

### 2. Functional Piping (PHP 8.5+)
Standardizing data transformation pipelines.

```php
$slug = $title
    |> trim(?)
    |> strtolower(?)
    |> preg_replace('/[^a-z0-9]+/', '-', ?);
```

### 3. Clone With (PHP 8.5+)
Updating immutable objects elegantly.

```php
$newConfig = clone $config with [
    'timeout' => 5000,
    'retries' => 3
];
```

---

## 🚫 The "Do Not List" (Anti-Patterns)
1.  **NEVER** use `var_dump` in production-bound code. Use `Sentry` or `Log::debug`.
2.  **NEVER** use `array()` syntax. Use `[]`.
3.  **NEVER** perform raw SQL queries. Use Eloquent or specialized Query Builders with parameter binding.
4.  **NEVER** use `global` keywords or `$GLOBALS`. Use Dependency Injection.
5.  **NEVER** ignore return values of functions marked with `#[NoDiscard]`.

---

## 🛠️ Troubleshooting & Engine Optimization

| Issue | Likely Cause | 2026 Corrective Action |
| :--- | :--- | :--- |
| **High Latency** | JIT is cold or misconfigured | Enable `opcache.jit=tracing` and monitor buffer usage. |
| **Memory Leak** | Persistent cURL handles not shared | Use `curl_share_init()` with persistent handles (PHP 8.5). |
| **Type Errors** | Loose types in legacy modules | Apply DNF types (e.g., `(A&B)|C`) for strict contracts. |
| **Slow Data Parsing** | Non-native URI/JSON handling | Use the native `URI` extension (PHP 8.5) and `json_validate`. |

---

## 📚 Reference Library
- **[Modern Patterns](./references/1-modern-patterns.md):** Architectural patterns using property hooks and enums.
- **[Performance & JIT](./references/2-performance-and-jit.md):** Squeezing performance from the Zend Engine.
- **[Migration & Rector](./references/3-migration-and-rector.md):** Moving from PHP 7.x/8.x to 8.5+.

---

## 📊 Quality Metrics
- **Static Analysis Pass:** PHPStan Level 9.
- **Code Coverage:** > 90% (Pest 3).
- **Complexity:** Max cyclomatic complexity of 5 per method.

---

## 🔄 Evolution from 8.1 to 8.6
- **8.1:** Readonly properties, Enums.
- **8.2:** Readonly classes, DNF types.
- **8.3:** Typed class constants, `json_validate`.
- **8.4:** Property Hooks, Asymmetric visibility.
- **8.5:** Pipe Operator, Clone With, Native URI.
- **8.6:** Partial Function Application, Pattern Matching (Expected).

---

**End of PHP Modern Standard (v1.1.0)**
