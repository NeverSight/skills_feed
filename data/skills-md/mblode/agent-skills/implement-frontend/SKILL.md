---
name: implement-frontend
description: Implementation standards for React/TypeScript/Next.js. Use when writing or reviewing frontend code, especially forms, state, hooks/components, and type safety.
---

# Implement Frontend

Use this as the baseline for all frontend code. Fix violations.

## Core rules
- Keep a single source of truth for any data or state.
- Enforce type safety: no `any`, no `as` casting, no ts-ignore.
- Use React Hook Form for every form. No manual form state.
- Use proto types as the contract; do not duplicate API types.
- Components render; hooks own data fetching and business logic.

## Code quality (baseline)
- Use active verb names; use one word per concept.
- Keep functions small, do one thing, and stay at one abstraction level.
- Minimize arguments; avoid boolean flags; avoid negative conditionals.
- Use else-if for multi-way decisions.
- Replace magic numbers with named constants.
- Comment intent, warnings, examples, or TODOs; never contradict code.
- Remove commented-out or unused code.
- Guard against hidden side effects.

## Critical anti-patterns
- Duplicate state or syncing state via `useEffect`.
- API calls or business logic inside components.
- `zodResolver(schema as any)` or other type escapes.
- Form object in dependency arrays (use only formState fields).

## References
- See `typescript-patterns.md` for TypeScript and proto guidance.
- See `react-patterns.md` for forms, hooks, and state.

## Quick checks
- Remove `console.*`, `debugger`, commented code, unused imports.
- Use `useId` for IDs; avoid hardcoded IDs.
- Zod v4 + `createZodResolver`.
- React Query/Connect Query owns server state; RHF owns form state; `useState` only for UI.

## Reliability & data fetching (required)
- Optimistic updates must snapshot previous cache state and rollback on error.
- Only optimistic-update for operations with a safe rollback; avoid for destructive actions unless server supports undo.
- Retries are only for idempotent requests. Use exponential backoff with full jitter and cap attempts/time.
- Always use `AbortController` for in-flight requests to prevent race conditions on unmount or rapid input.

## Cache & invalidation (required)
- React Query/Connect Query is the source of truth for server state; never copy server data into `useState`.
- Mutations must invalidate or update only the affected queries; do not refetch everything.
- `setQueryData` is allowed only for optimistic updates or small, scoped edits.

## Performance & UX (required)
- Follow `audit-ui` for accessibility and UX checklist items; use `ui-animation` for motion.
- Lazy-load heavy UI (charts, editors, modals) with dynamic import and suspense fallback.
- Reserve image sizes to avoid layout shift; use `next/image` when applicable.
- Enforce bundle budgets in CI (document the budgets in the repo).

## Observability (required)
- Add error boundaries at route/layout level; report exceptions to Sentry (or project standard).
- Tag client errors with `userId`/`orgId` and `release` (commit/semantic version), scrub PII.

## Required structure (per feature)
```
components/<feature>/
  *.tsx
  hooks/                 # feature hooks only
  types/                 # schemas + UI types
  utils/
    proto-mappers.ts     # proto -> UI transforms
  constants.ts
```

## Naming
- Files: kebab-case. Components: PascalCase. Functions: camelCase. Constants: UPPER_SNAKE_CASE.

Every file should be ready to ship.
