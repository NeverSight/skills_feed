---
name: busirocket-react-state-management-zustand
description:
  Zustand state management patterns for React applications. Use when
  implementing global state, modal visibility, cross-component communication, or
  avoiding prop drilling. This is an opinionated pattern recommendation.
disable-model-invocation: true
metadata:
  author: cristiandeluxe
  version: "1.0.0"
---

# React State Management (Zustand)

Opinionated guidance for using Zustand in React applications.

## When to Use

Use this skill when:

- Implementing global UI state (modals, progress indicators)
- Managing shared data across components
- Avoiding prop drilling
- Setting up cross-component communication

## Non-Negotiables (MUST)

- One store per domain (e.g., `uiStore`, `workspaceStore`, `statusLogStore`).
- Keep stores focused; split when they grow too large.
- Use selectors to minimize re-renders:
  `useStore((state) => state.specificValue)`.
- Actions should be defined in the store, not in components.
- Modals should read their visibility state from stores, not receive as props.

## Store Organization

- One store per domain: `uiStore`, `workspaceStore`, `statusLogStore`, etc.
- Keep stores focused; split when they grow too large.
- Use selectors to minimize re-renders:
  `useStore((state) => state.specificValue)`.
- Actions should be defined in the store, not in components.

## Rules

### Zustand Patterns

- `zustand-when-to-use` - When to use Zustand (modals, global UI state, shared
  data)
- `zustand-store-organization` - Store organization (one store per domain,
  selectors, actions)

### Modal Pattern

- `zustand-modal-pattern` - Modal pattern with Zustand (read visibility from
  store)

### Avoiding Prop Drilling

- `zustand-avoiding-prop-drilling` - Use Zustand stores instead of prop drilling

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/zustand-store-organization.md
rules/zustand-modal-pattern.md
rules/zustand-avoiding-prop-drilling.md
```

Each rule file contains:

- Brief explanation of why it matters
- Code examples (correct and incorrect patterns)
- Additional context and best practices
