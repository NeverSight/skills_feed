---
name: organizing-project-files
description: Provides file organization conventions for React and Next.js projects. Use when creating new files, components, hooks, utilities, or services. Triggers on questions like "where should this go?", "where do I put this?", or when deciding between colocating vs grouping files.
---

# Organizing Project Files

Colocate by feature when possible. Group by type only for truly shared code.

## Standard Layout

```
src/
├── app/                    # Next.js App Router (or pages/)
├── components/
│   ├── ui/                 # Reusable primitives (Button, Modal)
│   └── [feature]/          # Feature-specific (auth/, dashboard/)
├── hooks/                  # Custom React hooks
├── lib/                    # Core utilities, clients, constants
├── services/               # API calls, external integrations
├── stores/                 # State management
└── types/                  # TypeScript definitions
```

## Placement Quick Reference

| "I need..." | Location |
|-------------|----------|
| A button | `components/ui/Button.tsx` |
| A login form | `components/auth/LoginForm.tsx` |
| User data fetching | `services/user.ts` or `hooks/queries/useUser.ts` |
| Date formatter | `lib/utils.ts` |
| Auth state | `stores/auth.ts` |
| Supabase types | `types/supabase.ts` (generated) |
| Custom type | `types/index.ts` or colocate |

## Naming

- Components: `PascalCase.tsx`
- Hooks: `useCamelCase.ts`
- Utilities: `camelCase.ts`
- Types: `camelCase.ts`

## Colocation Pattern

For complex features, keep related files together:

```
components/auth/
├── LoginForm.tsx
├── LoginForm.test.tsx
├── useLoginForm.ts
└── login-schema.ts
```

## Advanced Patterns

For App Router specifics, barrel files, and monorepo structures, see [PATTERNS.md](PATTERNS.md).
