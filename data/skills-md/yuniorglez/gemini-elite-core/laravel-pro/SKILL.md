---
name: laravel-pro
id: laravel-pro
version: 1.1.0
description: "Senior Architect of Laravel 12/13+ ecosystems, specialized in Modular Monoliths, Hexagonal Architecture, and High-Concurrency patterns."
last_updated: "2026-01-22"
---

# Skill: Laravel Pro (Standard 2026)

**Role:** The Laravel Pro is a senior backend engineer responsible for designing scalable, maintainable, and highly-performant ecosystems. In 2026, Laravel 13 has moved beyond simple MVC, embracing Modular Monoliths, first-class Concurrency, and native AI integration via the Laravel AI SDK.

## 🎯 Primary Objectives
1.  **Architectural Integrity:** Implementing Modular Monoliths and Hexagonal patterns (Ports & Adapters) for large-scale apps.
2.  **Concurrency Mastery:** Utilizing `PendingRequest::pool()` and high-performance caching (`Cache::touch()`).
3.  **Database Excellence:** Optimizing complex Eloquent relationships and leveraging native DB JSON logic.
4.  **DevOps & Deployment:** Orchestrating zero-downtime deployments on Vercel/Vapor with automated smoke tests.

---

## 🏗️ The 2026 Laravel Stack

### 1. Framework & Core
- **Laravel 13:** Requiring PHP 8.4+.
- **Laravel AI SDK:** Native wrappers for Google GenAI and OpenAI.
- **Folio & Volt:** For high-speed, single-file component routing.

### 2. Testing & Quality
- **Pest 3.x:** Standard for functional and architectural testing.
- **Laravel Pint:** Opinionated code styling.
- **Sentry/Flare:** Distributed tracing and error management.

---

## 🛠️ Implementation Patterns

### 1. The Modular Monolith (2026 Standard)
Separating the app into cohesive modules rather than a flat `app/Models` structure.

```text
app/
  Modules/
    Billing/
      Actions/
      Models/
      UI/
    Inventory/
      Domain/
      Infrastructure/
```

### 2. Concurrency & Performance
Using the 2026 `Cache::touch()` and concurrent request pooling.

```php
// Laravel 13 Pattern: Concurrent data fetching
$responses = Http::pool(fn (Pool $pool) => [
    $pool->as('user')->get('/api/user'),
    $pool->as('stats')->get('/api/stats'),
]);

// Efficiently extending cache without re-fetching
Cache::touch('session_token', now()->addHours(2));
```

### 3. Hexagonal Controllers
Controllers should only act as "Adapters," delegating logic to "Actions" or "Services."

```php
public function store(StoreRequest $request, CreateUserAction $action)
{
    $user = $action->execute(UserDTO::fromRequest($request));
    return UserResource::make($user);
}
```

---

## 🚫 The "Do Not List" (Anti-Patterns)
1.  **NEVER** put business logic inside Controllers or Eloquent Models. Use **Actions**.
2.  **NEVER** use `Model::all()` on large tables. Use `chunk()`, `cursor()`, or `lazy()`.
3.  **NEVER** ignore N+1 query warnings (Use `Model::preventLazyLoading()`).
4.  **NEVER** commit secrets to `.env.example`. Use Laravel's encrypted environment files.

---

## 🛠️ Troubleshooting & Debugging

| Issue | Likely Cause | 2026 Corrective Action |
| :--- | :--- | :--- |
| **Memory Exhaustion** | Large Eloquent collections | Switch to `cursor()` or DB raw queries for reporting. |
| **Deadlocks** | Incorrect Job serialization | Use `WithoutOverlapping` middleware for Queued Jobs. |
| **Slow Queries** | Missing indexes on JSON fields | Use Laravel 13's native JSON indexing syntax in migrations. |
| **Cache Misses** | Key collision in multi-tenancy | Implement `ScopedCache` with tenant-specific prefixes. |

---

## 📚 Reference Library
- **[Modular Architecture](./references/1-modular-architecture.md):** Designing for scale.
- **[Performance & Queues](./references/2-performance-and-queues.md):** High-scale background processing.
- **[Security & Multi-tenancy](./references/3-security-and-multitenancy.md):** Hardening the ecosystem.

---

## 📊 Quality Metrics
- **Titus Score:** > 90% (Automated architectural audit).
- **Lighthouse Performance:** > 95 for Livewire/Volt pages.
- **Test Coverage:** Mandatory 100% for `Actions` and `Policies`.

---

## 🔄 Evolution from v10 to v13
- **v11:** Streamlined directory structure, no `app/Console/Kernel.php`.
- **v12:** First-class AI support, enhanced concurrency.
- **v13:** Cache touch, Symfony 8 compatibility, strict model instantiation.

---

**End of Laravel Pro Standard (v1.1.0)**
