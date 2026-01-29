---
name: busirocket-validation
description:
  Validation strategy using Zod for schemas and guard helpers for runtime
  checks. Use when validating API responses, request inputs, or external data at
  boundaries.
metadata:
  author: cristiandeluxe
  version: "1.0.0"
---

# Validation (Zod + Guards)

Consistent validation at boundaries: Zod for complex schemas, small guards for
simple runtime checks.

## When to Use

Use this skill when:

- Validating API responses or external data in services
- Validating request/input shapes at boundaries (e.g. route handlers, SDK)
- Adding or refactoring `utils/validation/` helpers
- Defining Zod schemas alongside types in `types/<area>/`

## Non-Negotiables (MUST)

- **Services**: validate API/external data with Zod schemas (e.g.
  `.safeParse()`).
- **Utils**: keep small coercion/guard helpers under `utils/validation/` (one
  function per file).
- **Types**: Zod schemas can live in `types/<area>/`; infer types with
  `z.infer<typeof Schema>`.
- Prefer `unknown` inputs at boundaries + explicit narrowing.
- No inline validation logic inside components/hooks.

## Rules

### Boundaries & Placement

- `validation-boundaries` - Where validation lives (services, utils, types)

### Zod Schemas (Complex Validation)

- `validation-zod-schemas` - Using Zod for complex validation with
  `.safeParse()`
- `validation-zod-types` - Inferring types from Zod schemas with `z.infer`

### Guard Helpers (Simple Runtime Checks)

- `validation-guard-helpers` - Creating simple guard functions with type
  predicates
- `validation-guard-examples` - Recommended guard helpers (isRecord,
  isNonEmptyString, etc.)

### Anti-Patterns

- `validation-no-inline` - No inline validation logic in components/hooks

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/validation-boundaries.md
rules/validation-zod-schemas.md
rules/validation-guard-helpers.md
```

Each rule file contains:

- Brief explanation of why it matters
- Code examples (correct and incorrect patterns)
- Additional context and best practices
