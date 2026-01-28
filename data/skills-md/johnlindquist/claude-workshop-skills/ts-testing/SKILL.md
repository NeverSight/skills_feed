---
name: ts-testing
description: Design, implement, and maintain high‑value TypeScript test suites using popular JS/TS testing libraries. Use this skill whenever the user is adding tests, debugging failing tests, or refactoring code that should be covered by tests.
license: Complete terms in LICENSE.txt
---

This skill guides you to build pragmatic, maintainable test suites for TypeScript code. Focus on behavioral coverage, fast feedback, and alignment with the project's existing tooling.

The user is a TypeScript‑focused developer. They likely care about correctness, refactoring safety, and not drowning in flaky or brittle tests.

## When to use this skill

Use this skill when:

- The user is adding or updating unit, integration, or end‑to‑end tests
- The user reports a bug and wants a regression test
- The user is refactoring and wants confidence they didn’t break behavior
- The repo has test tooling configured (or clearly needs one) and you’re asked to “add tests” or “improve tests”

Do **not** invent a new test stack if the repo already has one. First detect and follow the existing setup.

## Library preferences

Always align with the repo first (check `package.json`, `devDependencies`, config files):

- If the repo already uses a framework (Jest, Vitest, Playwright, Cypress, etc.), **stick with it**.
- Only suggest new libraries if there is no obvious testing stack yet.

When you **must choose**, prefer:

- **Unit / integration tests**
  - Node / backend / shared libraries:  
    - Prefer **Vitest** (`vitest`) or **Jest** (`jest`)  
    - If `vitest` is present, use it. Else if `jest` is present, use that.
- **React / UI component tests**
  - Use **Testing Library** with the existing runner:
    - `@testing-library/react` with Vitest or Jest
- **End‑to‑end browser tests**
  - Prefer **Playwright** if installed or if starting from scratch
  - Use **Cypress** if the repo already uses it or the user asks for it explicitly

If the repo uses a less common stack (Mocha, Ava, Node’s built‑in test runner), respect that choice and adapt.

## Core testing philosophy

Follow these principles:

- **Test behavior, not implementation details**
  - For React/UI: test what the user sees and does (DOM, events, ARIA), not internal state or private methods
  - For services: test public APIs, not private helpers
- **Keep tests fast and focused**
  - Prefer small, deterministic tests that run quickly
  - Avoid unnecessary network, filesystem, or database calls unless you are explicitly writing integration tests
- **Make failures obvious**
  - Clear naming and assertions that explain *why* a test failed
  - Use descriptive test names following “given/when/then” style where helpful
- **Minimize mocking, but use it where it makes sense**
  - Mock external services, network calls, and slow dependencies
  - Avoid mocking your own business logic unless there’s a strong reason

## Standard workflow

When asked to add or improve tests, follow this workflow:

1. **Detect the existing stack**
   - Inspect `package.json` for `jest`, `vitest`, `@playwright/test`, `cypress`, `@testing-library/*`
   - Look for config files: `jest.config.*`, `vitest.config.*`, `playwright.config.*`, `cypress.config.*`
   - Check `test`, `unit`, or `e2e` scripts in `package.json`

2. **Locate the right place for the test**
   - Mirror existing patterns:
     - If tests live in `__tests__` directories, follow that
     - If they use `*.test.ts` or `*.spec.ts`, do the same
   - For UI: place tests near the component (e.g. `Component.test.tsx`) if that’s the existing convention

3. **Write the test in a TS‑friendly way**
   - Use `.test.ts` / `.test.tsx` (or `.spec`) as per repo convention
   - Avoid `any` in tests when possible; use real types or minimal interfaces to keep tests robust
   - For async code: use `await` with async test functions, avoid dangling promises

4. **Follow library‑specific best practices**

   **Vitest / Jest**
   - Use `describe` / `it` or `test` with clear names
   - Prefer `vi.fn()` / `jest.fn()` for spies and mocks
   - For modules: use `vi.mock()` / `jest.mock()` and keep mocks at the top of the file
   - For timers: use fake timers only when necessary (`vi.useFakeTimers()` / `jest.useFakeTimers()`)

   **React Testing Library**
   - Use `render`, `screen`, and user interactions (`userEvent`)
   - Query by role, label, text as a user would (prefer `getByRole`, `getByLabelText`)
   - Avoid querying by test IDs unless there’s no good semantic alternative

   **Playwright / Cypress**
   - Use existing fixtures and helpers (e.g. authenticated sessions, base URL) instead of re‑inventing them
   - Keep tests independent; don’t rely on order
   - Use `data-testid` or semantics consistently as locators

5. **Add regression tests for reported bugs**
   - Reproduce the bug in a failing test first
   - Only then change the implementation to make the test pass
   - Name regression tests clearly (e.g. `it("does not crash when X is null (regression #123)")`)

6. **Running tests**
   - Use existing scripts, e.g. `npm test`, `pnpm test`, `npx vitest`, `npx jest`, `npx playwright test`
   - If adding a new test command, wire it into `package.json` scripts following existing style

## Patterns to prefer

- **One behavior per test**: Don’t cram multiple unrelated assertions into a single test unless they’re part of the same scenario.
- **Helper factories**: Use small factory functions for building test data (`makeUser`, `makeOrder`) instead of duplicating setup.
- **Explicit async handling**: Always `await` promises; avoid passing async callbacks to APIs that don’t expect them.

## Anti‑patterns to avoid

- Overuse of snapshots for complex objects or DOM – use targeted assertions instead
- Testing private methods directly
- Heavy mocking that makes tests mirror implementation wiring
- Flaky tests that depend on real time, network, or global state without control

## TypeScript‑specific guidance

- Use the project’s `tsconfig` for tests when possible (`tsconfig.test.json` if present)
- Avoid silencing type errors just to “get tests compiling”
- When stubbing data, create minimal typed helpers rather than using `as any`

If the user asks you to generate tests, prefer **fewer, high‑value tests** that mirror real usage over large, mechanical test suites.
