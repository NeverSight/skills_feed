---
name: agent-conventions
description: >
  Enforce code conventions that make codebases agent-friendly and self-healing.
  Inspired by Factory AI's "agent-native development" philosophy where lint rules
  and conventions act as guardrails for AI coding agents. Use this skill whenever
  generating, reviewing, or refactoring code in any language or framework. Triggers
  on: code generation, file creation, refactoring, code review, new features,
  bug fixes, migrations, or any task that produces source code. Covers file
  organization, naming, searchability, testing, error handling, logging, security,
  and architectural boundaries. Stack-specific references available for React,
  Vue, Angular, Laravel, .NET, Python, Go, Rust, and more.
---

# Agent Conventions

Conventions that make codebases searchable, predictable, and agent-friendly.
The core principle: **agents write the code; conventions write the law.**

## Core Philosophy

Every convention serves one or more of these goals:
- **Grep-ability**: Code is easy to find via text search (named exports, consistent naming)
- **Glob-ability**: File structure is predictable (agents can place and find files deterministically)
- **Self-healing**: Conventions prevent drift and regressions automatically

## Universal Rules (All Languages)

### 1. File Organization

Use a predictable layout so agents can place and find files deterministically.

**Scope**: The folder structures below are organized by **project type**. Universal rules (naming, exports, testing, errors, logging, security) apply to all project types. Folder structures are type-specific — don't force web app folders onto a game or CLI.

---

#### Web Applications (Frontend)

Choose by project size:

##### Option A: Concern-first (small/medium projects)

Group by concern at the top level, then by domain inside each:

```
src/
  components/
    layout/              # Structural shell (Header, Footer, Sidebar)
    ui/                  # Reusable primitives (Button, Modal, Input, Toast)
    users/               # User-specific components
    products/            # Product-specific components
  hooks/                 # React hooks / Vue composables (aka composables/)
    useUsers.ts
  services/              # Business logic, orchestration (non-HTTP)
    users.ts
    products.ts
  stores/                # Shared state containers (Pinia/Zustand/Redux)
    auth.ts
    cart.ts
  api/                   # HTTP clients (+ client interceptors/middleware)
    users.ts
    products.ts
  validators/            # Form/input validation schemas (Zod/Yup)
    user.ts
    login.ts
  types/
    user.ts
    product.ts
  enums/
    user.ts
  errors/
    user.ts
  constants/
  utils/
tests/
```

**When to use**: Project has < 10 domain areas, or features rarely have more than 2-3 concerns each. Simple, flat, easy to navigate.

##### Option B: Feature-first (large projects)

Group by feature, then by concern inside each:

```
src/
  components/
    layout/              # Structural shell (Header, Footer, Sidebar)
    ui/                  # Reusable primitives (Button, Modal, Input, Toast)
  features/
    users/
      components/        # User-specific UI components
      composables/       # Vue composables / React hooks (aka hooks/)
      stores/            # User-specific shared state
      services/          # Business logic, orchestration (non-HTTP)
      api/               # HTTP clients / DTO mappers
      validators/        # Form/input validation schemas
      types/
      enums/
      errors/
      constants/
      utils/
      index.{ext}        # Public surface
  shared/                # Truly cross-feature code (same concern buckets)
tests/                   # If the ecosystem requires a separate test tree
```

**When to use**: Project has 10+ domain areas, features have 3+ concerns each, or multiple teams work on separate features. Scales well — deleting a feature means deleting one folder.

#### When to graduate from A to B

Move a domain from concern-first to a feature folder when it accumulates 3+ concern files (components + service + types + ...). You don't need to migrate the entire project at once.

#### Shared rules (both approaches)

**Decision rule (where to save a new file):**
- Used only by one domain/feature → inside that domain's folder
- Used by multiple features and stable → `src/shared/` (feature-first) or top-level concern folder (concern-first)
- Shared UI (layout, primitives) → `src/components/layout/` or `src/components/ui/`
- Boundary code (HTTP, DB, queues) → `api/`, `controllers/`, `endpoints/`, `repositories/` (framework idioms)

**Composables/hooks vs stores:**
- `composables/` (or `hooks/`) → reusable logic; usually **per-caller** state
- `stores/` → deliberate **shared** state container (feature-level global-ish)
- If you intentionally create a singleton composable/hook (module-scoped state), treat it like a store: put it in `stores/` (or name it accordingly)

**`api/` vs `services/` vs `hooks/`:**
- `api/` → raw HTTP calls (`getUsers()`, `createUser()`) — thin wrappers around fetch/axios
- `services/` → business logic, orchestration, transformations — no HTTP awareness
- `hooks/` (or `composables/`) → reactive wrappers that call `api/` functions (`useUsers()` via TanStack Query/SWR)

**`validators/` — form and input validation:**
- One schema file per domain concept (`validators/user.ts`, `validators/login.ts`)
- Use a schema library (Zod, Yup, Valibot) — never hand-roll validation
- Schemas can be shared between frontend forms and backend API validation

**Interceptors (HTTP/framework):**
- Keep interceptors/middleware **at the boundary** they intercept (HTTP client/server pipeline)
- Prefer explicit registration (order matters) over hidden global side effects
- Name by responsibility: `auth`, `retry`, `logging`, `error-mapping`, `tracing`

### 2. Splitting & Naming — One Domain Concept Per File

Agents should be able to infer file placement from *meaning*, not memory.

**Agent-friendly default**:
- **Behavior files** (components/services/controllers/handlers): filename matches the primary symbol  
  Examples: `UserService.ts`, `UserController.php`, `UserCard.tsx`
- **Definition buckets** (`types/`, `enums/`, `errors/`, `constants/`): one *domain concept* per file

Examples (TypeScript/Python):
- `types/user.ts` / `types/user.py` → user-only types/contracts
- `enums/user.ts` / `enums/user.py` → user-only enums
- `errors/user.ts` / `errors/user.py` → user-only errors

For ecosystems with “one public type per file” norms (C#, Java, PHP), keep the same idea but split by type and group by folder/namespace:
- `Domain/Users/UserRole.cs`, `Domain/Users/UserStatus.cs`
- `app/Enums/UserRole.php`, `app/Exceptions/UserNotFoundException.php`

**Why**: Agents can create files without scanning, and humans can navigate by globbing folders.

### 3. Exports — Prefer Named Over Default (JS/TS)

```
// ✅ Good — grep-able
export function createUser() {}
export class UserService {}

// ❌ Bad — invisible to grep
export default function() {}
export default class {}
```

**Why**: `grep -r "export.*UserService"` finds it. Default exports are anonymous to search.

### 4. Imports — Prefer Absolute Over Deep Relative (When Supported)

```
// ✅ Good
import { UserService } from '@/services/UserService'
use App\Services\UserService;

// ❌ Bad
import { UserService } from '../../../services/UserService'
```

**Why**: Absolute paths tell agents the exact module provenance. Relative paths break on file moves.

### 5. Testing — Close to Source, Mirroring Structure

Prefer colocated tests when the ecosystem supports it (JS/TS, Go):

```
src/
  users/
    UserService.ts
    UserService.test.ts      ← colocated
    UserController.ts
    UserController.test.ts   ← colocated
```

If the framework/tooling expects a separate test tree (Laravel, many .NET setups), mirror the feature structure under `tests/`:

```
tests/
  features/
    users/
      UserServiceTest.php
```

**Why**: Either way, agents can answer “where is the test for this?” by following a deterministic path.

Testing principles (all languages):
- Test behavior through public interfaces (API, service contract, component props/events), not internal implementation details.
- Do not add tests for guarantees already enforced at compile-time by the language/type system.
- Add focused tests for runtime behavior the type system cannot guarantee (business rules, integration boundaries, side effects, failure handling).

### 6. Error Handling — Use Typed Errors

```
// ✅ Good — structured, grep-able
throw new UserNotFoundError(userId)
throw new ValidationError('email', 'Email is required')

// ❌ Bad — unstructured, hard to trace
throw new Error('something went wrong')
throw 'error'
```

**Why**: Typed errors create a searchable error taxonomy. Agents can find all error types and handle them consistently.

### 7. Logging — Structured, Never Bare

```
// ✅ Good — structured with context
logger.info('user.created', { userId, email })
Log::info('user.created', ['userId' => $userId])

// ❌ Bad — bare string, no context
console.log('user created')
echo "user created";
```

**Why**: Structured logs are parseable by machines and searchable by agents.

### 7b. Retry & Recovery — Standard Policy

Do not invent ad-hoc retry logic. Follow the standard retry policy in [retry.md](retry.md), which defines:

- **Classify** errors as retryable (transient) vs non-retryable (permanent) before retrying.
- **Max 3 attempts** with exponential backoff + jitter (capped at 30s, total deadline 60s).
- **Idempotency required** — only retry idempotent operations or those with a dedupe mechanism.
- **Observe** every attempt with structured logs (operation, attempt number, error class, elapsed time).
- **Circuit breaker** — stop calling a dependency after 5 consecutive failures, probe after 30s cooldown.

Full policy, including 409 classification, Retry-After handling, retry budgets, distributed concerns, and queue/dead-letter rules: [retry.md](retry.md).

### 8. Security Basics

- Never hardcode secrets, tokens, or API keys in source files
- Validate all external input at the boundary (route handlers, API endpoints)
- Use parameterized queries, never string interpolation for SQL
- Sanitize output to prevent XSS

### 9. Architectural Boundaries

- Feature folders should not reach into another feature's internals
- Use public module surfaces (index files, facades, service providers)
- Dependencies flow inward: UI → Application → Domain → Infrastructure

```
// ✅ Good — uses the public surface
import { createUser } from '@/features/users'

// ❌ Bad — reaches into internals
import { hashPassword } from '@/features/users/utils/crypto'
```

### 10. Documentation Signals

- Public APIs and exported functions should have docblocks/TSDoc
- Complex business logic should have inline comments explaining "why", not "what"
- Module-level comments for non-obvious architectural decisions

## Stack-Specific References

For detailed conventions per framework or language, read the relevant reference file:

### Frontend Frameworks
- **React**: See [frameworks/frontend/react.md](frameworks/frontend/react.md)
- **Next.js**: See [frameworks/frontend/nextjs.md](frameworks/frontend/nextjs.md)
- **Vue**: See [frameworks/frontend/vue.md](frameworks/frontend/vue.md)
- **Angular**: See [frameworks/frontend/angular.md](frameworks/frontend/angular.md)

### Backend Frameworks
- **Laravel**: See [frameworks/backend/laravel.md](frameworks/backend/laravel.md)
- **Symfony**: See [frameworks/backend/symfony.md](frameworks/backend/symfony.md)
- **Django**: See [frameworks/backend/django.md](frameworks/backend/django.md)
- **Spring Boot**: See [frameworks/backend/spring.md](frameworks/backend/spring.md)
- **NestJS**: See [frameworks/backend/nestjs.md](frameworks/backend/nestjs.md)
- **Ruby on Rails**: See [frameworks/backend/rails.md](frameworks/backend/rails.md)
- **.NET**: See [frameworks/backend/dotnet.md](frameworks/backend/dotnet.md)

### Languages
- **TypeScript**: See [languages/typescript.md](languages/typescript.md)
- **JavaScript**: See [languages/javascript.md](languages/javascript.md)
- **PHP**: See [languages/php.md](languages/php.md)
- **Python**: See [languages/python.md](languages/python.md)
- **Java**: See [languages/java.md](languages/java.md)
- **C#**: See [languages/csharp.md](languages/csharp.md)
- **Go**: See [languages/go.md](languages/go.md)
- **Rust**: See [languages/rust.md](languages/rust.md)

### General
- **API / HTTP**: See [api.md](api.md)
- **Retry & Error Recovery**: See [retry.md](retry.md)

Read the appropriate reference file based on the project's stack before generating code.

## Self-Healing Workflow

When generating or reviewing code, follow this loop:

1. **Generate** code following the conventions above
2. **Verify** by mentally checking each rule (file placement, naming, exports, tests)
3. **Fix** any violations before presenting the code
4. **Prevent** regressions by ensuring new patterns match existing codebase conventions

If the project has linters configured (ESLint, PHPStan, Pint, etc.), always run them after generating code and fix violations before presenting results.
