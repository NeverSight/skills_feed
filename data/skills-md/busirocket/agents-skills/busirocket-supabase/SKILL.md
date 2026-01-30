---
name: busirocket-supabase
description:
  Supabase access patterns and service boundaries. Use only when working with
  Supabase projects. Centralize Supabase access in services/ and never call
  Supabase directly from components/hooks/utils/route handlers.
disable-model-invocation: true
metadata:
  author: cristiandeluxe
  version: "1.0.0"
---

# Supabase Boundaries

Service boundary patterns for Supabase projects.

## When to Use

Use this skill only when:

- Working in a project that uses Supabase
- Creating or refactoring Supabase access code
- Enforcing service boundaries for database access

## Non-Negotiables (MUST)

- **Never call Supabase directly** from components, hooks, utils, or route
  handlers.
- **Centralize access** in dedicated Supabase service wrappers (e.g.
  `services/supabase/*`).
- Keep wrappers small, focused, and typed.
- Never import `@supabase/supabase-js` outside a single Supabase client module
  (e.g. `lib/supabase.ts`) or your Supabase service wrappers.

## Rules

### Supabase Access

- `supabase-access-rule` - Isolate Supabase access in service wrappers
- `supabase-services-usage` - Route handlers, hooks, utils, and components must
  NOT call Supabase directly

## Related Skills

- `busirocket-core-conventions` - Service boundaries and structure

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/supabase-access-rule.md
rules/supabase-services-usage.md
```

Each rule file contains:

- Brief explanation of why it matters
- Code examples (correct and incorrect patterns)
- Additional context and best practices
