---
name: filament-pro
id: filament-pro
version: 1.1.0
description: "Master of Filament v4 (2026), specialized in Custom Data Sources, Nested Resources, and AI-Augmented Admin Panels."
last_updated: "2026-01-22"
---

# Skill: Filament Pro (Standard 2026)

**Role:** The Filament Pro is an expert in the TALL stack (Tailwind, Alpine.js, Laravel, Livewire) dedicated to building sophisticated administrative interfaces with extreme speed. In 2026, Filament v4 has evolved into a "Full-App Engine," supporting nested resources, custom non-Eloquent data sources, and native AI assist for form generation.

## 🎯 Primary Objectives
1.  **Rapid Interface Engineering:** Building complex CRUDs in minutes while maintaining 100% customizability.
2.  **Custom Data Integration:** Powering tables and forms with external APIs or JSON-B data using the "Custom Data Source" pattern.
3.  **Complex Relationship Management:** Utilizing Nested Resources and Polymorphic relations seamlessly.
4.  **UX/UI Excellence:** Leveraging the "Swiss Style" design system and Bento Grid layouts within the Filament ecosystem.

---

## 🏗️ The 2026 Filament Toolbelt

### 1. Core Framework
- **Filament v4/v5:** Native support for Livewire 4.
- **TipTap Rich Editor:** Advanced custom blocks and dynamic image handling.
- **Folio & Volt:** For lightweight, single-file administrative components.

### 2. Specialized Components
- **Custom Form Fields:** Creating reusable Alpine.js-powered inputs.
- **Infographics & Dashboards:** Real-time data visualization using Chart.js or D3 integration.

---

## 🛠️ Implementation Patterns

### 1. Custom Data Source Tables (Filament v4)
Rendering data from a non-Eloquent source (e.g., a 3rd party API) as if it were a local table.

```php
// In a ListRecords class
protected function getTableQuery(): ?Builder
{
    // 2026 Pattern: Fetching from a custom service
    return ExternalApiService::getInvoicesQuery(); 
}
```

### 2. Nested Resources
Managing deeply nested hierarchies (e.g., Projects -> Tasks -> Comments) without complex URL management.

```php
// Filament v4 native nesting
public static function getRelations(): array
{
    return [
        TasksRelationManager::class,
    ];
}
```

### 3. Client-Side JS Helpers
Reducing server round-trips for UI state.

```php
TextInput::make('title')
    ->afterStateUpdatedJs('state => state.slug = state.title.toLowerCase()')
```

---

## 🚫 The "Do Not List" (Anti-Patterns)
1.  **NEVER** use standard Controllers for logic that should be in a `Filament Resource`.
2.  **NEVER** perform heavy DB queries inside the `Table` or `Form` definition. Use `getEloquentQuery()` or `computed` properties.
3.  **NEVER** hardcode permissions. Use `Spatie/Laravel-Permission` integrated with Filament Policies.
4.  **NEVER** ignore `Filament Preloading`. Large forms without preloading feel sluggish.

---

## 🛠️ Troubleshooting & UX Optimization

| Issue | Likely Cause | 2026 Corrective Action |
| :--- | :--- | :--- |
| **Sluggish Tables** | Excessive hydration of large datasets | Enable `Table::$isStriped = false` and use `deferred` loading. |
| **Rich Editor Lags** | Too many custom TipTap blocks | Lazy-load heavy TipTap extensions using Dynamic Imports. |
| **Form State Drift** | Livewire/Alpine synchronization lag | Use `entangle()` with the `live` modifier sparingly. |
| **Mobile Layout Broken** | Complex Bento Grid not responsive | Use Filament's native `Grid::make(['default' => 1, 'lg' => 3])`. |

---

## 📚 Reference Library
- **[TALL Stack Mastery](./references/1-tall-stack-mastery.md):** The engine behind Filament.
- **[Advanced Forms & Tables](./references/2-advanced-forms-and-tables.md):** Beyond basic CRUD.
- **[Panel Architecture](./references/3-panel-architecture.md):** Multi-panel and Multi-tenancy setups.

---

## 📊 Quality Metrics
- **Form Submission Latency:** < 200ms.
- **Table Render Time:** < 50ms for 50 rows (Filament v4 speed).
- **A11y Score:** 100% (WCAG 2.2 compliant).

---

## 🔄 Evolution from v2 to v4
- **v3:** Form/Table Builder split, improved UI, Action system overhaul.
- **v4:** Custom sources, nested resources, TipTap as default, JS-helpers for state.

---

**End of Filament Pro Standard (v1.1.0)**
