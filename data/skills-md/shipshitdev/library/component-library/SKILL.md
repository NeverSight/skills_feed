---
name: component-library
description: Expert React/Next.js component architect specializing in creating consistent, reusable, and maintainable components for monorepo projects
version: 1.0.0
tags:
  - react
  - nextjs
  - components
  - design-system
  - typescript
  - performance
  - patterns
---

# Component Library Standards Skill

Expert React/Next.js component architect specializing in creating consistent, reusable, and maintainable components.

## When to Use This Skill

Use when you're:

- Creating new UI components
- Refactoring existing components for reusability
- Reviewing component architecture
- Setting up shared component patterns
- Optimizing component performance

## Quick Reference

### Naming

- Files: PascalCase (`Button.tsx`)
- Props: `ComponentNameProps` interface
- Hooks: `use-` prefix (`use-auth.ts`)

### Structure

```typescript
'use client'; // Only if needed
// Imports: types → hooks → utils → components
export interface MyComponentProps { ... }
export default function MyComponent({ ... }: MyComponentProps) { ... }
```

### Patterns

- Composition over configuration
- Compound components for complex UI
- Controlled components for forms
- Generic components for type safety

### Performance

- `React.memo` for pure components
- `useMemo` / `useCallback` for expensive operations
- `lazy` + `Suspense` for code splitting
- `react-window` for virtualization

### Accessibility

- Semantic HTML (`button`, `nav`, not `div`)
- ARIA labels for icons
- Keyboard navigation support
- Focus states visible

## References

- [Full guide: Patterns, styling, TypeScript, testing, documentation](references/full-guide.md)
