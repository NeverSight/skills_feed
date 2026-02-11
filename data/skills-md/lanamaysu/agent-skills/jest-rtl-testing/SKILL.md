---
name: jest-rtl-testing
description: Use when writing, reviewing, or debugging Jest + React Testing Library tests, before writing test code or when tests fail
---

# Jest + React Testing Library Best Practices

## Overview

Based on Testing Library's core principles and Kent C. Dodds' best practices guidance for writing user-centric tests.

**Core Principle:** Tests should interact with your application the same way users do, not test implementation details.

## 🔴 MANDATORY PRE-CHECK

**Before writing any test, you MUST:**

1. ✅ Check if project has `AGENTS.md` and read its Testing section
2. ✅ Follow `AGENTS.md` rules with highest priority when they exist
3. ✅ Use this skill's principles as baseline guidance and supplementary best practices

---

## When to Use

**Use this skill when:**
- Writing new tests, especially React component tests
- Reviewing or refactoring existing tests
- Debugging test failures to determine if API is misused
- Optimizing test readability and maintainability

**Don't use when:**
- Unit testing pure functions (no DOM or React)
- E2E testing (use Playwright, Cypress, etc.)
- Performance testing or visual regression testing

---

## Quick Reference

### Query Priority (Context-Aware)

⚠️ **Performance Warning**: `getByRole` can be slow on large views ([ref](https://github.com/testing-library/dom-testing-library/issues/820)). For complex UIs with many elements, prefer `getByLabelText` or `getByText` first.

**Priority Order:**
1. 🥇 **getByLabelText** - Form fields, best performance
2. 🥇 **getByText** - Non-interactive content
3. 🥇 **getByRole** - Small components only, great for a11y validation
4. 🥉 **getByPlaceholderText** / **getByDisplayValue**
5. 🚫 **getByTestId** - Last resort (document why in AGENTS.md)

**Query types:**
- `getBy*` - element must exist (throws if not found)
- `queryBy*` - expect absence (returns null)
- `findBy*` - async wait (returns Promise)

Details: [references/query-cheatsheet.md](./references/query-cheatsheet.md)

---

## Core Principles (Short)

1. **Project rules first** - Read `AGENTS.md` and follow testing rules with highest priority.
2. **User-centric behavior** - Assert what users see and do, not internal state.
3. **Async aware** - Use `findBy*` for appearance, `waitForElementToBeRemoved` for disappearance.
4. **Real interactions** - Prefer `@testing-library/user-event` over `fireEvent`.
5. **MSW first for HTTP** - Use MSW to mock network requests; avoid manual fetch/axios mocks.

Examples and patterns: [references/common-patterns.md](./references/common-patterns.md)

---

## Debugging (Short)

- Use `screen.debug()` to inspect the DOM.
- Check query choice (`getBy*` vs `queryBy*` vs `findBy*`).
- Use `screen.logTestingPlaygroundURL()` to discover better queries.

---

## Resources

- [Testing Library - Guiding Principles](https://testing-library.com/docs/guiding-principles)
- [Testing Library - Queries](https://testing-library.com/docs/queries/about)
- [Testing Library - Async](https://testing-library.com/docs/dom-testing-library/api-async)
- [MSW Documentation](https://mswjs.io/docs/)
- [Common mistakes with React Testing Library (Kent C. Dodds)](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)
- [getByRole Performance Issue](https://github.com/testing-library/dom-testing-library/issues/820)

---

**Last Updated**: 2026-02-10
