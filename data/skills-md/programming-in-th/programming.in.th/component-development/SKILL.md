---
name: component-development
description: Use when creating or modifying React components. Ensures proper Server/Client component patterns, performance optimization, and accessibility.
allowed-tools: Read, Edit, Write, Glob, Grep
---

See [React patterns](../../docs/react-patterns.md) for full reference.

**Quick rules**:
- Default to Server Components (no directive)
- Use `'use client'` only for: `onClick`, `useState`, `useEffect`, browser APIs
- Push client boundary to smallest component
- Tailwind only, use `dark:` variants

**Example**:
```tsx
// Server Component (default)
export function TaskCard({ task }: { task: Task }) {
  return <div className="p-4 dark:bg-gray-800">{task.title}</div>
}
```

**Checklist**: Minimal client components, `dark:` variants, accessible inputs.
