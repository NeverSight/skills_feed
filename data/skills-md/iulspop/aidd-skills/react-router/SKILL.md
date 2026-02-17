---
name: react-router
description: React Router V7 patterns for loaders, actions, forms, routes, middleware, and error handling. Use when writing or reviewing React Router code.
---

# React Router

Act as a senior React Router engineer reviewing code for correctness, performance, and best practices.

Review: $ARGUMENTS

## Loaders

- Fetch all data in loaders, never in components with `useEffect`. Loaders run before render and eliminate loading spinners.
- Use `Promise.all` for independent data fetches within a loader to avoid sequential waterfalls.
- Use request-scoped caching (via context) so multiple loaders can call the same data function without duplicate requests.
- Control revalidation with `shouldRevalidate` to skip unnecessary refetches. Use `useRevalidator` for polling/focus patterns.
- Type loaders with `Route.LoaderArgs` and consume with `useLoaderData<typeof loader>()`.
- Validate URL params early with zod or invariant — don't trust `params` to be well-formed.
- Pass `request.signal` to fetch calls and database queries so they abort when the user navigates away.
- Colocate data queries in `queries.server.ts` next to the route file.

## Actions

- Validate all form data with zod schemas. Return validation errors with `data({ errors }, { status: 400 })` — don't throw for validation failures.
- Use `throw redirect("/path")` after successful mutations to prevent resubmission (Post/Redirect/Get).
- Use zod `.transform()` for input sanitization (trim, lowercase, parse numbers) during validation.
- Use `z.discriminatedUnion("intent", [...])` to handle multiple actions in one route with type-safe intent matching.
- Use `clientAction` for instant client-side validation before hitting the server.
- Re-throw redirects and unknown errors in catch blocks — only catch expected error types.

## Forms

- Use `useFetcher` for in-place mutations (likes, toggles, inline edits) that shouldn't trigger navigation. Use `<Form>` when the mutation should navigate.
- Show pending state with `fetcher.state !== "idle"` or `useNavigation().state`. Use `useSpinDelay` to avoid flicker.
- Reset uncontrolled forms on success with `formRef.current?.reset()` in an effect.
- Return field values from actions on validation error so inputs repopulate with `defaultValue={actionData?.fields?.email}`.
- Add `<HoneypotInputs />` to public-facing forms for bot protection.

## Routing

- Organize routes as folders with colocated `queries.server.ts`, `actions.server.ts`, `route.tsx`, and `components/`.
- Use resource routes (no default export) for API-like endpoints. Name them `api.<resource>.tsx`.
- Use dedicated action routes (`actions.<noun>-<verb>.ts`) for reusable mutations consumed by multiple pages via `useFetcher`.
- Name the default export `Component` in all route files.
- Never import from other route files — import shared modules instead. Exception: import `type { action }` for `useFetcher` type inference.
- Access parent route data with `useRouteLoaderData` in UI. In loaders, re-fetch (request-scoped caching prevents duplicate calls).

## Middleware

- Authenticate in middleware, authorize in each loader/action. Keep auth checks close to data access.
- Store session in middleware so loaders/actions get a single instance per request.
- Use `AsyncLocalStorage` for request-scoped context accessible without passing args through every function.
- Add `Server-Timing` headers in middleware for performance observability.
- Generate a request ID in middleware for log correlation across the request lifecycle.

## Security

- Protect mutations with CSRF tokens or verify `Sec-Fetch-Site` headers to reject cross-site requests.
- Sanitize user-driven redirect URLs with `safeRedirect(redirectTo, "/")` — never redirect to arbitrary user input.
- Apply CORS headers only to API resource routes that need cross-origin access. Use specific origins, not wildcards.
- Validate cookie payloads with schemas using typed cookies.
- Use `prefetch="intent"` on `<Link>` for faster navigation — preloads data on hover/focus.

## Error Handling

- Export `ErrorBoundary` from every route with data fetching. Use `isRouteErrorResponse` to distinguish HTTP errors from unexpected exceptions.
- In layout routes, make `ErrorBoundary` layout-aware so errors render within the app shell.
- Use `<Suspense>` with `<Await resolve={promise}>` for streamed loader data — return promises from `data()` and they auto-stream.
