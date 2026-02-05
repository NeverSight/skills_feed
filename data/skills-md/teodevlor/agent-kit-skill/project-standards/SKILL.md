---
name: project-standards
description: Core coding standards, SOLID principles, Clean Code, and naming conventions. Use this skill for any coding task to ensure consistency.
---

# Project Standards

This skill provides the foundational coding standards that apply to ALL projects regardless of tech stack.

## When to Use
- Use this skill for ANY coding task
- This skill is the foundation that other stack-specific skills build upon
- Always read this skill FIRST before reading stack-specific skills

## Instructions

### 1. Analyze Environment First
Before applying any rules, READ the dependency files:
- `package.json` (Node/TS projects)
- `composer.json` (PHP/Laravel)
- `go.mod` (Go projects)
- `requirements.txt` / `pyproject.toml` (Python)

**Principle:** Respect legacy. If the project already uses a specific library, USE IT.

---

## SOLID Principles (Strict Enforcement)

### S - Single Responsibility
A class/function must have ONE and only ONE reason to change.
- *Violation:* A `UserService` that handles DB queries AND sends Emails.
- *Fix:* Split into `UserRepository` and `EmailNotificationService`.

### O - Open/Closed
Open for extension, closed for modification. Use Interfaces/Abstract classes.

### L - Liskov Substitution
Subtypes must be substitutable for their base types.

### I - Interface Segregation
Clients should not be forced to depend on interfaces they do not use. Split large interfaces.

### D - Dependency Inversion
Depend on abstractions, not concretions.
- *Rule:* Always inject dependencies via Constructor. Never use `new Class()` inside business logic.

---

## Clean Code Core

- **DRY (Don't Repeat Yourself):** Logic duplicated > 2 times must be extracted.
- **KISS (Keep It Simple, Stupid):** Simplest solution is usually best. Avoid Over-Engineering.
- **YAGNI (You Ain't Gonna Need It):** Do not implement features "just in case".

---

## Function/Method Rules

- **Max Lines:** < 30 lines ideally.
- **Max Params:** < 3 parameters. Use DTO/Object if more needed.
- **No Boolean Flags:** Split functions instead of `createUser(isSuperAdmin: boolean)`.

---

## Naming Conventions

### By Language
| Category | JS/TS | Python | Go | PHP |
|---|---|---|---|---|
| Files | `kebab-case` | `snake_case` | `snake_case` | `PascalCase` |
| Classes | `PascalCase` | `PascalCase` | `PascalCase` | `PascalCase` |
| Functions | `camelCase` | `snake_case` | `camelCase` | `camelCase` |
| Variables | `camelCase` | `snake_case` | `camelCase` | `$camelCase` |
| Constants | `SCREAMING_SNAKE` | `SCREAMING_SNAKE` | `PascalCase` | `SCREAMING_SNAKE` |

### Structural Naming
- **Helpers:** Module-specific support. Location: `modules/<name>/helpers/`
- **Common/Shared:** Generic reusable. Location: `src/common/` or `src/shared/`
- **Services:** Must end with `Service`, `Handler`, or `UseCase`.
- **DTOs/Types:** Must include suffix (e.g., `user.dto.ts`, `order_response.go`).

---

## Comments & Documentation

### Commenting Rules
- **Zero-Comment Policy:** Do not comment obvious code.
- **Complex Logic Only:** Only comment algorithms or counter-intuitive decisions.
- **NO ICONS/EMOJIS:** Absolutely NO decorations in comments. Raw text only.
  - Bad: `// Fast calculation function`
  - Good: `// Uses binary search for O(log n) complexity.`

### Function Documentation (JSDoc/GoDoc/Docstring)
- **Public API Only:** Only document exported functions.
- **Concise:** 1-2 sentences max. Do not restate parameter names.

```ts
// Bad: Redundant
/**
 * Adds two numbers.
 * @param a First number
 * @param b Second number
 * @returns The sum
 */
const add = (a: number, b: number) => a + b;

// Good: Necessary context only
/**
 * Calculates tax based on local VAT rules (2024 reform).
 */
const calculateTax = (price: number, region: string) => { ... }
```

---

## RESTful API Standards

### HTTP Verbs
- `GET` - Read (Idempotent, Safe)
- `POST` - Create
- `PUT` - Full Update
- `PATCH` - Partial Update
- `DELETE` - Remove

### Status Codes
- `200 OK` - Success (Read/Update)
- `201 Created` - Success (Create)
- `204 No Content` - Success (Delete)
- `400 Bad Request` - Validation Error
- `401 Unauthorized` - Auth missing
- `403 Forbidden` - No permission
- `404 Not Found` - Resource not exist
- `500 Internal Server Error` - App crash

### Response Envelope
```json
{
  "success": true,
  "data": {},
  "meta": { "page": 1, "limit": 10, "total": 100 },
  "error": { "code": "ERROR_CODE", "message": "...", "details": [] },
  "timestamp": "2024-01-20T10:00:00Z"
}
```

### URL Naming
- Collection: `/users` (Plural, kebab-case)
- Resource: `/users/123`
- Sub-resource: `/users/123/orders`

---

## Database Standards

- **Naming:** `snake_case` for tables/columns.
- **Primary Keys:** UUID (distributed) or BigInt.
- **Audit Fields:** `created_at`, `updated_at`, `deleted_at` mandatory.

---

## Folder Structure

### Option A: Feature-based (Recommended)
```
src/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── api/
│   │   └── index.ts
│   └── dashboard/
```

### Option B: Layer-based (Classic)
```
src/
├── components/
├── pages/
├── services/
├── utils/
└── hooks/
```
