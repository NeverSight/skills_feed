---
name: architecture-review
description: Review project architecture, identify structural issues, and plan refactoring. Analyzes directory structure, module boundaries, dependencies, and code organization. Provides systematic approaches for cleanup, restructuring, and migration. Primary focus on TypeScript/JavaScript projects with patterns applicable to other languages. Use this skill when auditing codebases, planning refactors, or improving project organization.
---

# Architecture Review

Analyze, audit, and improve project structure.

## Review Process

```
┌─────────────────────────────────────────────────────────────┐
│                    ARCHITECTURE REVIEW                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. DISCOVERY          2. ANALYSIS          3. PLANNING    │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐ │
│  │ Map structure│  →   │ Identify    │  →   │ Prioritize  │ │
│  │ List deps    │      │ issues      │      │ changes     │ │
│  │ Trace flows  │      │ Find smells │      │ Plan phases │ │
│  └─────────────┘      └─────────────┘      └─────────────┘ │
│                                                             │
│  4. EXECUTION          5. VALIDATION                        │
│  ┌─────────────┐      ┌─────────────┐                      │
│  │ Incremental │  →   │ Test        │                      │
│  │ refactoring │      │ Verify      │                      │
│  │ Safe moves  │      │ Document    │                      │
│  └─────────────┘      └─────────────┘                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Quick Assessment Checklist

### Structure Health
- [ ] Clear separation between layers (UI, business logic, data)
- [ ] Consistent directory naming conventions
- [ ] Logical grouping (by feature or by type)
- [ ] Reasonable file sizes (<500 lines typical)
- [ ] No deeply nested directories (>4 levels)

### Dependency Health
- [ ] No circular dependencies
- [ ] Clear dependency direction (UI → Logic → Data)
- [ ] External dependencies isolated
- [ ] Shared code properly extracted
- [ ] No god modules everything imports

### Code Organization
- [ ] Single responsibility per file/module
- [ ] Related code colocated
- [ ] Clear public API boundaries
- [ ] Consistent export patterns
- [ ] No barrel file explosion

### Maintainability
- [ ] Easy to find code for a feature
- [ ] Changes isolated to relevant areas
- [ ] New developers can navigate easily
- [ ] Tests colocated or clearly organized
- [ ] Configuration centralized

## Common Structural Patterns

### Feature-Based (Recommended for Apps)

```
src/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── api.ts
│   │   ├── types.ts
│   │   └── index.ts
│   ├── users/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── api.ts
│   │   ├── types.ts
│   │   └── index.ts
│   └── orders/
│       └── ...
├── shared/
│   ├── components/
│   ├── hooks/
│   ├── utils/
│   └── types/
├── lib/           # Third-party wrappers
├── config/        # App configuration
└── app.tsx        # Entry point
```

**Pros:** Colocation, feature isolation, clear ownership
**Cons:** May duplicate patterns, harder to share

### Layer-Based (Common for APIs)

```
src/
├── controllers/   # HTTP handlers
├── services/      # Business logic
├── repositories/  # Data access
├── models/        # Data structures
├── middleware/    # HTTP middleware
├── utils/         # Helpers
├── types/         # TypeScript types
├── config/        # Configuration
└── index.ts       # Entry point
```

**Pros:** Clear responsibilities, familiar pattern
**Cons:** Features spread across folders, harder to delete features

### Hybrid (Scales Well)

```
src/
├── modules/
│   ├── auth/
│   │   ├── auth.controller.ts
│   │   ├── auth.service.ts
│   │   ├── auth.repository.ts
│   │   ├── auth.types.ts
│   │   └── index.ts
│   ├── users/
│   └── orders/
├── shared/
│   ├── database/
│   ├── middleware/
│   └── utils/
├── config/
└── main.ts
```

**Pros:** Feature isolation + clear layers within
**Cons:** More boilerplate per feature

## Structural Anti-Patterns

### 🚨 God Module

```
// utils/helpers.ts - 2000+ lines
export function formatDate() { ... }
export function validateEmail() { ... }
export function calculateTax() { ... }
export function parseCSV() { ... }
export function sendNotification() { ... }
// ... 50 more unrelated functions
```

**Fix:** Split by domain (date-utils.ts, validation.ts, tax.ts, etc.)

### 🚨 Circular Dependencies

```
// users/service.ts
import { OrderService } from '../orders/service';

// orders/service.ts
import { UserService } from '../users/service';  // Circular!
```

**Fix:** Extract shared logic, use dependency injection, or events

### 🚨 Leaky Abstractions

```
// components/UserList.tsx
import { prisma } from '../lib/prisma';  // Direct DB access in component!

const users = await prisma.user.findMany();
```

**Fix:** Add service layer, components only call APIs/hooks

### 🚨 Barrel File Explosion

```
// features/index.ts
export * from './auth';
export * from './users';
export * from './orders';
// ... 20 more

// This causes everything to load even if you need one thing
import { LoginButton } from '../features';  // Loads ALL features
```

**Fix:** Import directly from feature, use selective exports

### 🚨 Scattered Configuration

```
// Config in 10 different places
src/config.ts
src/lib/config.js
src/utils/env.ts
src/services/settings.ts
.env, .env.local, .env.production
```

**Fix:** Single config module that loads all env vars

### 🚨 Deep Nesting

```
src/features/users/components/forms/inputs/text/validation/rules/email.ts
```

**Fix:** Flatten structure, maximum 3-4 levels deep

## Issue Severity Classification

| Severity | Impact | Examples |
|----------|--------|----------|
| **Critical** | Blocks development, causes bugs | Circular deps, broken imports |
| **High** | Significant maintenance burden | God modules, no separation |
| **Medium** | Slows development | Inconsistent patterns, poor naming |
| **Low** | Minor friction | Style inconsistencies, extra files |

## Review Output Template

```markdown
# Architecture Review: [Project Name]

## Overview
- **Project Type:** [Web App / API / Library / Monorepo]
- **Primary Language:** [TypeScript / JavaScript / etc.]
- **Framework:** [React / Next.js / Express / NestJS / etc.]
- **Size:** [~X files, ~Y lines]

## Current Structure
[Directory tree or description]

## Findings

### Critical Issues
1. [Issue]: [Description]
   - **Location:** [file/folder]
   - **Impact:** [What problems it causes]
   - **Recommendation:** [How to fix]

### High Priority
1. ...

### Medium Priority
1. ...

### Low Priority
1. ...

## Recommendations

### Immediate Actions
- [ ] [Action 1]
- [ ] [Action 2]

### Short-term (1-2 weeks)
- [ ] [Action 1]

### Long-term (1+ month)
- [ ] [Action 1]

## Proposed Structure
[New directory tree if restructuring needed]

## Migration Plan
[Phased approach if significant changes]
```

## When to Restructure

**DO restructure when:**
- Developers can't find code
- Simple changes touch many files
- Circular dependencies are common
- Tests are hard to write due to coupling
- New features require copying boilerplate
- Team has grown and needs clearer boundaries

**DON'T restructure when:**
- "It doesn't feel right" (need concrete issues)
- Only for consistency with a blog post
- Major deadline approaching
- No tests to verify refactoring
- Team doesn't agree on target structure

---

**References:**
- [references/analysis-techniques.md](references/analysis-techniques.md) — Dependency graphs, complexity metrics, code analysis
- [references/refactoring-patterns.md](references/refactoring-patterns.md) — Safe refactoring techniques, migration strategies
- [references/structural-patterns.md](references/structural-patterns.md) — Directory structures for different project types
- [references/dependency-management.md](references/dependency-management.md) — Circular deps, coupling, module boundaries
- [references/cleanup-strategies.md](references/cleanup-strategies.md) — Dead code removal, consolidation, naming conventions
