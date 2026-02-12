---
name: happy-dom-tests
description: Generates React component render tests using happy-dom and Testing Library with the "given/should" prose format. Use when writing tests for display components, hooks, user interactions, or accessibility checks.
---

# Happy DOM Tests

Act as a top-tier software engineer with serious testing skills.

Write React component tests for: $ARGUMENTS

Each test must answer these 5 questions:

1. What is the component under test? (test should be in a named describe block)
2. What is the expected behavior? ($given and $should arguments are adequate)
3. What props or state trigger the behavior? (use a factory function with defaults)
4. What does the user see or interact with? (accessible queries, not implementation details)
5. How can we find the bug? (implicitly answered if the above questions are answered correctly)

## Rules

- Use Vitest with describe, expect, and test. Test files use the `.test.tsx` extension.
- Tests must use the "given: ..., should: ..." prose format.
- Colocate test files next to the component they test.
- Import `render`, `screen`, `userEvent`, and `createRoutesStub` from a shared `~/test/react-test-utils` module that wraps Testing Library with app providers (i18n, form context, etc.).
- Create a props factory function per component with sensible defaults. Each test overrides only what it needs.
- Use `createRoutesStub` from React Router to provide routing context. Pass `initialEntries` for specific routes.
- Use accessible queries as the primary locator strategy: `screen.getByRole`, `screen.getByLabel`, `screen.getByText`.
- Use `screen.queryByRole` (returns null) for negative assertions — never `getByRole` with `not.toBeInTheDocument`.
- Use regex with case-insensitive flag for text matching: `{ name: /submit/i }`.
- Use `userEvent.setup()` for user interactions — never `fireEvent`.
- Use `vi.fn()` for mock callbacks. Use `vi.spyOn` for global mocks.
- Use `renderHook` and `act` for testing custom hooks. Use `vi.useFakeTimers()` for timer-based hooks.
- Use `@faker-js/faker` and `cuid2` in factories for realistic test data.
- Use existing infrastructure factories (`*-factories.server.ts`) when props come from database entities.
- Wrap `RouterStub` in additional providers (e.g. `SidebarProvider`) when the component requires them.
- Pass `hydrationData` to `RouterStub` when the component reads loader data.
- Use `test.each` for parametrized tests when multiple inputs produce similar outcomes.
- Assert accessibility attributes: `toHaveAttribute("aria-selected", "true")`, `toHaveAttribute("aria-current", "page")`.
- Assert element state: `toBeDisabled()`, `toBeEnabled()`, `toHaveFocus()`.
- Assert structure: `toBeInTheDocument()`, `toHaveAttribute("href", "/path")`, `toHaveTextContent(/text/i)`.
- Capture `actual` and `expected` values in variables before asserting with `toEqual` for pure logic checks.

## When NOT to use this skill

- For pure function tests without React (`.test.ts`), use `/unit-tests` instead.
- For database or server action tests (`.spec.ts`), use `/integration-tests` instead.
- For browser-level user flow tests (`.e2e.ts`), use `/e2e-tests` instead.
- This skill is for React component and hook render tests (`.test.tsx`) only.
