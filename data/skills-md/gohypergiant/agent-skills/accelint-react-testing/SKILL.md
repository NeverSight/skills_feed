---
name: accelint-react-testing
description: Use when writing, reviewing, or refactoring React component tests with Testing Library. Load when you see render(), screen, fireEvent, userEvent, waitFor, or *.test.tsx files. Covers query priority (getByRole > getByLabelText > getByText), user-centric testing patterns, async utilities, custom renders with providers, and accessibility-first assertions. Keywords include RTL, Testing Library, screen, getByRole, findBy, queryBy, userEvent, waitFor, toBeInTheDocument, testing-library/react, testing-library/user-event, jest-dom.
compatibility: Requires @testing-library/react, works with vitest or jest
license: Apache-2.0
metadata:
  author: gohypergiant
  version: "1.0"
---

# React Testing Best Practices

Expert guidance for writing maintainable, user-centric React component tests with Testing Library. Focused on query selection, accessibility-first testing, and avoiding implementation details.

## NEVER Do When Writing React Tests

- **NEVER query by test IDs before trying accessible queries** - Test IDs bypass accessibility verification: a button with `data-testid="submit"` but no accessible name works in tests but fails for screen reader users. When tests pass with test IDs, you ship inaccessible UIs. Query hierarchy: `getByRole` > `getByLabelText` > `getByText` > `getByTestId`. Each step down this list means less confidence your UI is usable.
- **NEVER use `fireEvent` for user interactions when `userEvent` is available** - `fireEvent` dispatches single DOM events, missing the event sequence real users trigger: `fireEvent.click()` fires one click event, but real users trigger focus → mousedown → mouseup → click. Components that work with fireEvent break in production when users interact normally. `userEvent.click()` simulates the full interaction sequence, catching bugs fireEvent misses.
- **NEVER test implementation details instead of user behavior** - Tests that verify "state variable X equals Y" or "function Z was called" create false failures: you refactor from useState to useReducer, all tests fail, yet the UI works identically. Testing implementation details punishes refactoring and provides zero confidence the user experience works. Test what users see and do (rendered output, interaction results), not how your component achieves it internally.
- **NEVER query from `container` or use destructured queries after initial render** - `const { getByText } = render(<Component />)` creates stale queries that miss updates: after state changes, destructured queries search the initial DOM snapshot, missing newly rendered elements. This causes "element not found" errors for elements that are actually present. Always use `screen.getByText()` which automatically queries the current DOM state. Using screen consistently also makes tests more maintainable - adding a new query doesn't require updating the destructuring.
- **NEVER add aria-label or role attributes solely for tests** - If you're adding `aria-label="submit-button"` or `role="button"` just so tests can find elements, you're working backwards. Tests should verify the component is already accessible, not make it accessible for tests. Adding test-only ARIA pollutes production code and masks real accessibility problems. Fix the component's semantic HTML and existing ARIA first.
- **NEVER snapshot entire component trees without specific assertions** - Massive snapshots with 500+ lines break on any change (updated classname, new prop, reordered elements), forcing reviewers to approve diffs they can't meaningfully evaluate. When test failures require "just update the snapshot" without understanding why, the test has zero value. Snapshot specific critical structures (error messages, data tables) with targeted assertions for everything else.
- **NEVER use `waitFor` for actions that return promises** - `waitFor(() => expect(element).toBeInTheDocument())` polls repeatedly until timeout when a promise-based `findBy` query solves it in one shot: `await screen.findByText('loaded')` waits for the element to appear without polling. Reserve waitFor for assertions that can't use findBy (checking element disappears, waiting for attribute changes).
- **NEVER perform side effects inside waitFor callback** - `waitFor(() => { fireEvent.click(button); expect(text).toBeInTheDocument(); })` runs the click multiple times as waitFor retries, causing unpredictable behavior. waitFor is for waiting on assertions, not triggering actions. Perform all actions outside waitFor, then use waitFor only for the assertion: `fireEvent.click(button); await waitFor(() => expect(text).toBeInTheDocument());` or better yet, `await userEvent.click(button); expect(await screen.findByText(text)).toBeInTheDocument();`.
- **NEVER create custom renders without documenting provider requirements** - A custom `renderWithRedux` function with undocumented required store shape breaks for every developer: they call `render(<Component />)` instead of `renderWithRedux()`, tests fail with cryptic "Cannot read property of undefined", wasting 15 minutes debugging. Centralize provider setup in test utils with TypeScript types that enforce correct usage, or document required wrappers prominently.
- **NEVER mix queries from different Testing Library imports** - Importing both `@testing-library/react` render and `@testing-library/dom` queries creates confusion: `screen` from react package doesn't work with `getByRole` from dom package, causing "screen.getByRole is not a function" errors. Import all queries from `@testing-library/react` for React components - it re-exports everything from dom with React-specific enhancements.

## Before Writing Tests, Ask

Apply these thinking patterns before implementing React component tests:

### Query Selection Strategy
- **Which query matches how users find this element?** Real users don't look for test IDs or CSS classes - they look for labels, buttons, headings. If you can't query by role or label, your UI lacks accessibility. Query difficulty reveals UX problems before they reach production.
- **Does this element need to be found at all?** Not every element needs a query assertion. Users don't verify "loading spinner exists" - they verify "data appears after loading". Test outcomes, not intermediate states.
- **Should I use getBy, queryBy, or findBy?** Start with getBy for immediate presence - it gives the best error messages. Use queryBy only when asserting absence (.not.toBeInTheDocument()). Use findBy for async appearance. Never use queryBy + expect(...).toBeInTheDocument() - use getBy instead for better error messages when the element is missing.

### User vs Implementation Testing
- **What would a user do to verify this works?** Users click buttons and read text - they don't check state variables or mock function calls. If your test uses `rerender()` or accesses component internals, you're testing implementation. Refactor to test through user actions.
- **Will this test survive a refactoring that doesn't change behavior?** If renaming a function or switching from useState to useReducer breaks the test, you're testing implementation details. These tests waste time blocking safe changes while providing no confidence the UI actually works.

### Async and Timing
- **Is this query for something that loads asynchronously?** Use `findBy*` for anything loaded via useEffect, API calls, or setTimeout. `getBy*` throws immediately if element is missing; `findBy*` waits for it to appear. Using getBy for async content creates race conditions that only fail in CI.
- **Am I waiting for an element to appear or disappear?** Appearance = `findBy*` query. Disappearance = `waitForElementToBeRemoved`. State changes = `waitFor` with assertion. Each has different semantics; using the wrong one causes flaky tests or longer timeouts.

### Test Isolation and Setup
- **Does this component need context providers to render?** Components using useContext, Redux hooks, or React Router throw without providers. Create custom render utilities that wrap components in required providers automatically. Repeating provider setup in every test file is a maintenance disaster.
- **What's the minimal setup needed for this test case?** Tests with excessive setup (mocking 10 functions for a button test) are fragile and slow. Mock only external dependencies (APIs, localStorage), never your own functions. If setup is complex, the component design might be the problem.

## How to Use

This skill uses **progressive disclosure** to minimize context usage:

### 1. Start with the Overview (AGENTS.md)
Read [AGENTS.md](AGENTS.md) for a concise overview of all rules with one-line summaries.

### 2. Load Specific Rules as Needed
Use these explicit triggers to know when to load each reference file:

**MANDATORY Loading (load entire file):**
- **Writing any query (getBy*, findBy*, queryBy*)** → [query-priority.md](references/query-priority.md)
- **Simulating user interactions (clicks, typing, etc.)** → [user-events.md](references/user-events.md)

**Load When You See These Patterns:**
- **Confusion about getBy vs findBy vs queryBy** → [query-variants.md](references/query-variants.md)
- **waitFor, async queries, or "act" warnings** → [async-testing.md](references/async-testing.md)
- **Components using Context, Redux, Router** → [custom-render.md](references/custom-render.md)
- **Testing accessibility or ARIA attributes** → [accessibility-queries.md](references/accessibility-queries.md)
- **Using container, wrapper, or rerender extensively** → [anti-patterns.md](references/anti-patterns.md)
- **Queries failing or can't find right selector** → [query-variants.md](references/query-variants.md) for screen.debug() usage

**Do NOT Load Unless Specifically Needed:**
- Do NOT load [custom-render.md](references/custom-render.md) for simple components without providers
- Do NOT load [async-testing.md](references/async-testing.md) for synchronous tests
- Do NOT load [accessibility-queries.md](references/accessibility-queries.md) unless testing ARIA or a11y concerns

### 3. Apply the Pattern
Each reference file contains:
- ❌ Incorrect examples showing the anti-pattern
- ✅ Correct examples showing the optimal implementation
- Explanations of why the pattern matters

### 4. Audit Existing Tests (Optional)
Use the provided scripts to audit existing test suites:
```bash
# Check query priority (testId usage, container.querySelector)
./scripts/check-query-priority.sh

# Find fireEvent that should be userEvent
./scripts/find-fire-event.sh

# Detect deprecated wrapper/container patterns
./scripts/detect-wrapper-queries.sh
```

### 5. Use the Report Template
When this skill is invoked for test code review, use the standardized report format:

**Template:** [`assets/output-report-template.md`](assets/output-report-template.md)

The report format provides:
- Executive Summary with accessibility confidence and user-centric coverage assessment
- Severity levels (Critical, High, Medium, Low) for prioritization
- Impact analysis (accessibility confidence, user-centric confidence, test reliability, refactor safety)
- Categorization (Query Priority, Query Variants, User Events, Async Testing, Custom Render, Accessibility, Anti-patterns)
- Pattern references linking to detailed guidance in references/
- Summary table for tracking all issues

**When to use the report template:**
- Skill invoked directly via `/accelint-react-testing <path>`
- User asks to "review test code" or "audit tests" across file(s), invoking skill implicitly

**When NOT to use the report template:**
- User asks to "write a test for this function" (direct implementation)
- User asks "what's wrong with this test?" (answer the question)
- User requests specific test fixes (apply fixes directly without formal report)

## What This Skill Covers

Expert guidance on React Testing Library patterns:

1. **Query Priority** - Accessible query hierarchy from getByRole to getByTestId
2. **Query Variants** - When to use getBy, findBy, queryBy for different scenarios
3. **User Events** - userEvent vs fireEvent for realistic interaction testing
4. **Async Testing** - Handling promises, waitFor, findBy queries, avoiding act warnings
5. **Custom Render** - Setting up providers (Context, Redux, Router) for complex components
6. **Accessibility Queries** - Testing with roles, labels, and ARIA attributes
7. **Anti-patterns** - Avoiding implementation details, container usage, excessive snapshots
9. **Audit Scripts** - Automated detection of suboptimal patterns in existing tests

## Query Selection Decision Tree

Use this hierarchy when selecting queries - try options from top to bottom:

```
1. getByRole          ← Preferred: Accessible, reflects how users & ATs interact
   ↓ Can't find role?
   
2. getByLabelText     ← For form fields: matches how users read forms
   ↓ No label?
   
3. getByPlaceholderText  ← For inputs: less accessible than labels
   ↓ No placeholder?
   
4. getByText          ← For non-interactive content: headings, paragraphs
   ↓ Text not unique?
   
5. getByDisplayValue  ← For form inputs: current value
   ↓ No display value?
   
6. getByAltText       ← For images: alt attribute
   ↓ No alt text?
   
7. getByTitle         ← For title attribute: less accessible
   ↓ No title?
   
8. getByTestId        ← Last resort: no accessibility verification
```

**Key principles:**
- Higher queries = more confidence in accessibility
- If you can't query by role/label, fix the component's accessibility first
- getByTestId means "I've verified accessibility is impossible here"

## Important Notes

- **The `screen` export is not magic** - It's just `getQueriesForElement(document.body)`. Using `screen.getByRole()` is identical to destructured `getByRole()` from render, but screen never goes stale after re-renders.
- **Testing Library encourages accessibility by making accessible elements easiest to query** - If queries are hard, your UI is hard to use. Query difficulty is a UX code smell.
- **Use screen.debug() or screen.logTestingPlaygroundURL() when queries fail** - When getByRole fails, run `screen.debug()` to see the current DOM or `screen.logTestingPlaygroundURL()` to get an interactive tool showing what queries work. Don't guess at selectors - let Testing Library show you what's available.
- **queryBy returns null silently - use getBy for better errors** - When an element should exist, `getBy*` throws with helpful suggestions about similar elements and available roles. `queryBy*` returns null, requiring you to add your own assertion with less helpful error output. Use queryBy only when asserting absence with .not.toBeInTheDocument().
- **Act warnings mean React state updates happened outside Testing Library's awareness** - Usually caused by promises resolving after test completion or missing `await` on async queries. Not caused by correct use of findBy or waitFor.
- **userEvent methods are async (return promises), fireEvent methods are sync** - Forgetting `await userEvent.click()` causes "act" warnings and flaky tests as state updates happen after assertions run.
