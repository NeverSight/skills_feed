---
name: busirocket-typescript-standards
description:
  TypeScript standards for maintainable codebases. Use when creating or
  refactoring TS/TSX to enforce one-thing-per-file, type conventions, and
  Next.js special-file export exceptions.
metadata:
  author: cristiandeluxe
  version: "1.0.0"
---

# TypeScript + React Standards

Strict, reusable standards for TypeScript/React projects.

## When to Use

Use this skill when:

- Writing or refactoring `.ts` / `.tsx`
- Moving inline types into `types/`
- Enforcing consistent type naming and result shapes
- Working in Next.js where special files allow extra exports

## Non-Negotiables (MUST)

- **One exported symbol per file** for your own modules.
- **No inline `interface`/`type`** in components/hooks/utils/services/route
  handlers.
- Put shared shapes under `types/<area>/...` (**one type per file**).
- Avoid barrel files (`index.ts`) that hide dependencies.
- After meaningful changes: run the project's standard checks (e.g.
  `yarn check:all`).

## Next.js Special-file Exceptions

- `app/**/page.tsx`, `app/**/layout.tsx`: allow `default export` +
  `metadata/generateMetadata/viewport` (etc.).
- `app/api/**/route.ts`: allow multiple HTTP method exports and route config
  exports.

## Rules

### TypeScript Standards

- `ts-language-style` - Language & style (interface vs type, const vs let,
  English-only)
- `ts-one-thing-per-file` - One thing per file (STRICT)
- `ts-nextjs-exceptions` - Next.js special-file exceptions
- `ts-types-strict` - Types (STRICT) - no inline types
- `ts-helpers-strict` - Helpers (STRICT) - no helpers in components/hooks
- `ts-nextjs-hygiene` - Next.js TS hygiene (docs-aligned)
- `ts-validation` - Validation (run checks after changes)

### Types Conventions

- `types-one-type-per-file` - One type per file (STRICT)
- `types-naming-patterns` - Naming patterns (Params, Result, Error, Props)
- `types-result-shape` - Result shape for boundaries that can fail
- `types-where-allowed` - Where types are allowed

## Related Skills

- `busirocket-core-conventions` - General file structure (one-thing-per-file,
  boundaries)
- `busirocket-react` - Component and hook structure
- `busirocket-refactor-workflow` - Refactoring workflow for TypeScript/React

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/ts-one-thing-per-file.md
rules/ts-types-strict.md
rules/types-one-type-per-file.md
```

Each rule file contains:

- Brief explanation of why it matters
- Code examples (correct and incorrect patterns)
- Additional context and best practices
