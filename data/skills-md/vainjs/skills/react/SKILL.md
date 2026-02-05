---
name: react
description: TypeScript/React code standards. Use when writing or reviewing React components, hooks, or TypeScript code.
---

## Standards Detection

Search for ESLint config (`.eslintrc.*`, `eslint.config.*`, `package.json`). If found, merge with baseline (ESLint takes precedence). Otherwise use baseline only.

## Baseline Standards

### Types & Imports

- Use `type` (not `interface`)
- Use `import type` for type-only imports
- Naming: `ComponentNameProps`, `UseHookNameOptions`
- Order: types → libraries → components → utilities → styles

### Naming

| Element             | Convention       | Example           |
| ------------------- | ---------------- | ----------------- |
| Components          | PascalCase       | `UserProfile`     |
| Variables/functions | camelCase        | `getUserData`     |
| Constants           | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Event handlers      | on\*             | `onClick`         |
| Hooks               | use\*            | `useAuth`         |

### Components

- Functional components with arrow functions
- Destructure props with defaults
- Named exports preferred
- Set `displayName`
- Memoize: `useCallback` for callbacks, `useMemo` for computations
- Early returns for guards
- Conditional rendering with `&&`

### Custom Hooks

```typescript
export function useHookName(options: UseHookNameOptions) {}
```

### Code Style

- TypeScript strict mode
- Avoid `any` → use `unknown` or specific types
- Prefer `const` over `let`
- Single responsibility functions
