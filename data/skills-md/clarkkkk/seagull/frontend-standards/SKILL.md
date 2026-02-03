---
name: frontend-standards
description: Use when implementing or refactoring frontend UI and business logic in apps/expo. Enforce business/UI layering, feature-based business folders, effect hooks, store usage rules, and Tailwind/NativeWind + clsx styling conventions.
---

# Frontend Standards (Seagull)

## When to use
- Building or refactoring React Native screens/components in `apps/expo`.
- Moving logic into `apps/expo/src/business` modules.
- Deciding where logic/state/style belongs (business vs UI).

## Core rules
- **Business logic lives in `apps/expo/src/business/<module>/<feature>`**.
  - Files: `hooks.ts`, `effect.ts` (side effects only), `store.ts` (Zustand shared state), `types.ts`, `utils.ts`.
  - Business modules must not contain UI details (className/layout/components).
- **UI layer is pure**: no `trpc`, `queryClient`, `authClient`, `useQuery/useMutation`.
- **Hook contract**:
  - UI events call business methods; UI does not assemble payloads.
  - Derived data computed in hooks.
  - Side effects only in `effect.ts`, mounted once by page-level aggregate hook.
- **Store access**: UI may read store via selector only. No side effects in UI.
- **Styling**: TailwindCSS + NativeWind with `className`.
  - `className` composition must use `clsx`.
  - Use semantic tokens (`text-foreground`, `bg-primary`, `border-border`), avoid hardcoded colors.

## React Query / tRPC (TanStack Query) rules
- **Only business layer uses Query/Mutation**: keep `useQuery/useMutation`, `queryClient.invalidateQueries(...)` inside `apps/expo/src/business/**`.
- **Never put the whole `useMutation(...)` result object into `useEffect` deps** (it is not stable and can cause effect re-run loops).
  - Prefer destructuring: `const { mutate, mutateAsync, isPending } = useMutation(...)`, then depend on `mutateAsync`/`mutate` only if needed.
  - If you must reference mutation from async callbacks/timers/cleanup, prefer `useRef` or `store.getState()` over closures.
- **Query drives state; mutations only invalidate**:
  - Prefer “server truth → store flags” to be driven from query result (single source of truth).
  - Mutations should generally `invalidate`/`refetch` queries in `onSuccess/onSettled`, not directly flip multiple store flags.
- **Guard query/mutation with `enabled` and stable inputs**:
  - All query inputs must be stable and non-empty; use `enabled: isAuthed && !!id && !sessionLoading` style gating.
  - Avoid calling mutation in render; trigger from event or a guarded effect.
- **Avoid infinite loops**:
  - If an effect calls a mutation that invalidates a query, ensure the effect does not re-trigger solely because the query updated.
  - Use “attempt once per `id`” refs for auto-acquire patterns; never spam retries on every re-render.
- **TTL/lock heartbeats**:
  - `refetchInterval` refreshes query data, but does **not** extend TTL unless backend explicitly does so.
  - If backend has a `refresh` mutation, keep it and run it on an interval while owner; then invalidate `get` to sync `expiresAt`.
- **Cleanup must read latest state**:
  - For unmount releases, do not trust closed-over `hasLock`; use `useTripEditStore.getState()` (or a ref) to check latest ownership before calling `release`.

## Refactoring checklist
- Page contains only UI logic and view state.
- Repeated logic extracted to business hooks/utils/components.
- Files > 500 lines are split by feature.
- Lists handle empty states.

## Canonical reference
- See `skills/frontend-standards/references/frontend-standards.md` for the full policy text and examples.
