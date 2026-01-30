---
name: busirocket-react
description:
  React component and hook structure rules plus Zustand state management. Use
  when writing or refactoring React components, extracting hooks, deciding
  client vs server components, implementing global state (Zustand), modals, or
  avoiding prop drilling.
metadata:
  author: cristiandeluxe
  version: "1.0.0"
---

# React (Components, Hooks, State)

Reusable patterns for scalable React codebases, including Zustand state
management.

## When to Use

Use this skill when:

- Writing or refactoring `.tsx` components
- Extracting hooks into `hooks/<area>/useXxx.ts`
- Removing helpers from components/hooks into `utils/`
- Removing inline types into `types/`
- Implementing global UI state (modals, progress indicators)
- Managing shared data across components or avoiding prop drilling
- Setting up cross-component communication with Zustand

## Non-Negotiables (MUST)

### Components and Hooks

- Exactly **one exported component per `.tsx` file**.
- Exactly **one exported hook per hook file** (`hooks/<area>/useXxx.ts`).
- **No helper functions inside** components or hooks; extract helpers to
  `utils/`.
- **No inline types** inside components or hooks; import from `types/`.
- Prefer server-side rendering boundaries wisely (avoid `'use client'` for large
  subtrees).

### State (Zustand)

- One store per domain (e.g., `uiStore`, `workspaceStore`, `statusLogStore`).
- Keep stores focused; split when they grow too large.
- Use selectors to minimize re-renders:
  `useStore((state) => state.specificValue)`.
- Actions should be defined in the store, not in components.
- Modals should read their visibility state from stores, not receive as props.

## Rules

### Component Patterns

- `react-one-component-per-file` - One component per file (STRICT)
- `react-client-vs-server` - Client vs Server Components (App Router)
- `react-folder-namespacing` - Folder namespacing for complex components
- `react-performance` - Performance optimization (memo, useCallback)
- `react-accessibility` - Accessibility best practices
- `react-component-testing` - Component tests in `__tests__`, React Testing Library

### Hooks Best Practices

- `react-one-hook-per-file` - One hook per file (STRICT)
- `react-no-helpers-in-hooks` - No helpers inside hooks (STRICT)
- `react-no-types-in-hooks` - No types inside hooks (STRICT)
- `react-stable-api` - Stable API for hooks
- `react-side-effects` - Side effects in hooks

### State (Zustand)

- `zustand-when-to-use` - When to use Zustand (modals, global UI state, shared
  data)
- `zustand-store-organization` - Store organization (one store per domain,
  selectors, actions)
- `zustand-modal-pattern` - Modal pattern with Zustand (read visibility from
  store)
- `zustand-avoiding-prop-drilling` - Use Zustand stores instead of prop drilling

## Related Skills

- `busirocket-core-conventions` - General file structure and boundaries
- `busirocket-typescript-standards` - TypeScript and type conventions
- `busirocket-nextjs` - Server vs Client Components (detailed)

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/react-one-component-per-file.md
rules/react-one-hook-per-file.md
rules/react-client-vs-server.md
rules/zustand-store-organization.md
rules/zustand-modal-pattern.md
```

Each rule file contains:

- Brief explanation of why it matters
- Code examples (correct and incorrect patterns)
- Additional context and best practices
