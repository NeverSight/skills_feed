---
name: busirocket-react-components-and-hooks
description:
  React component and hook structure rules. Use when writing or refactoring
  React components, extracting hooks, deciding client vs server components, and
  enforcing one-component/one-hook per file with no helpers or inline types.
metadata:
  author: cristiandeluxe
  version: "1.0.0"
---

# React Components and Hooks

Reusable patterns for scalable React codebases.

## When to Use

Use this skill when:

- Writing or refactoring `.tsx` components
- Extracting hooks into `hooks/<area>/useXxx.ts`
- Removing helpers from components/hooks into `utils/`
- Removing inline types into `types/`

## Non-Negotiables (MUST)

- Exactly **one exported component per `.tsx` file**.
- Exactly **one exported hook per hook file** (`hooks/<area>/useXxx.ts`).
- **No helper functions inside** components or hooks; extract helpers to
  `utils/`.
- **No inline types** inside components or hooks; import from `types/`.
- Prefer server-side rendering boundaries wisely (avoid `'use client'` for large
  subtrees).

## Rules

### Component Patterns

- `react-one-component-per-file` - One component per file (STRICT)
- `react-client-vs-server` - Client vs Server Components (App Router)
- `react-folder-namespacing` - Folder namespacing for complex components
- `react-performance` - Performance optimization (memo, useCallback)
- `react-accessibility` - Accessibility best practices

### Hooks Best Practices

- `react-one-hook-per-file` - One hook per file (STRICT)
- `react-no-helpers-in-hooks` - No helpers inside hooks (STRICT)
- `react-no-types-in-hooks` - No types inside hooks (STRICT)
- `react-stable-api` - Stable API for hooks
- `react-side-effects` - Side effects in hooks

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/react-one-component-per-file.md
rules/react-one-hook-per-file.md
rules/react-client-vs-server.md
```

Each rule file contains:

- Brief explanation of why it matters
- Code examples (correct and incorrect patterns)
- Additional context and best practices
