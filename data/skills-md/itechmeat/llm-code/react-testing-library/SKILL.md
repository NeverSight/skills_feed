---
name: react-testing-library
description: "React Testing Library: user-centric component testing with queries, user-event simulation, async utilities, and accessibility-first API."
version: "16.3.2"
release_date: "2026-01-19"
---

# React Testing Library Skill

## Quick Navigation

| Topic       | Link                                                   |
| ----------- | ------------------------------------------------------ |
| Queries     | [references/queries.md](references/queries.md)         |
| User Events | [references/user-events.md](references/user-events.md) |
| API         | [references/api.md](references/api.md)                 |
| Async       | [references/async.md](references/async.md)             |
| Debugging   | [references/debugging.md](references/debugging.md)     |
| Config      | [references/config.md](references/config.md)           |

---

## Installation

```bash
# Core (v16+: @testing-library/dom is peer dependency)
npm install --save-dev @testing-library/react @testing-library/dom

# TypeScript support
npm install --save-dev @types/react @types/react-dom

# Recommended: user-event for interactions
npm install --save-dev @testing-library/user-event

# Recommended: jest-dom for matchers
npm install --save-dev @testing-library/jest-dom
```

**React 19 support**: Requires `@testing-library/react` v16.1.0+

## Core Philosophy

> "The more your tests resemble the way your software is used, the more confidence they can give you."

**Avoid testing**:

- Internal state of components
- Internal methods
- Lifecycle methods
- Child component implementation details

**Test instead**:

- What users see and interact with
- Behavior from user's perspective
- Accessibility (queries by role, label)

---

## Query Priority

Use queries in this order of preference:

### 1. Accessible to Everyone (Preferred)

```ts
// Best — by ARIA role
getByRole("button", { name: /submit/i });
getByRole("textbox", { name: /email/i });

// Form fields — by label
getByLabelText("Email");

// Non-interactive content — by text
getByText("Welcome back!");
```

### 2. Semantic Queries

```ts
// Images
getByAltText("Company logo");

// Title attribute (less reliable)
getByTitle("Close");
```

### 3. Test IDs (Escape Hatch)

```ts
// Only when other queries don't work
getByTestId("custom-element");
```

---

## Query Types

| Type            | No Match | 1 Match | >1 Match | Async |
| --------------- | -------- | ------- | -------- | ----- |
| `getBy...`      | throw    | return  | throw    | No    |
| `queryBy...`    | null     | return  | throw    | No    |
| `findBy...`     | throw    | return  | throw    | Yes   |
| `getAllBy...`   | throw    | array   | array    | No    |
| `queryAllBy...` | []       | array   | array    | No    |
| `findAllBy...`  | throw    | array   | array    | Yes   |

**When to use**:

- `getBy*` — element exists
- `queryBy*` — element may not exist (assertions like `expect(...).not.toBeInTheDocument()`)
- `findBy*` — element appears asynchronously

---

## Basic Test Pattern

```tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

test("shows greeting after login", async () => {
  const user = userEvent.setup();
  render(<App />);

  // Act — simulate user interactions
  await user.type(screen.getByLabelText(/username/i), "john");
  await user.click(screen.getByRole("button", { name: /login/i }));

  // Assert — verify outcome
  expect(await screen.findByText(/welcome, john/i)).toBeInTheDocument();
});
```

---

## User Events

Always use `@testing-library/user-event` over `fireEvent`:

```ts
import userEvent from "@testing-library/user-event";

test("user interactions", async () => {
  const user = userEvent.setup();

  // Click
  await user.click(element);
  await user.dblClick(element);
  await user.tripleClick(element);

  // Type
  await user.type(input, "Hello");
  await user.clear(input);

  // Select
  await user.selectOptions(select, ["option1", "option2"]);

  // Keyboard
  await user.keyboard("{Enter}");
  await user.keyboard("[ShiftLeft>]a[/ShiftLeft]"); // Shift+A

  // Clipboard
  await user.copy();
  await user.paste();

  // Pointer
  await user.hover(element);
  await user.unhover(element);
});
```

---

## Async Patterns

### waitFor — Retry Until Success

```ts
await waitFor(() => {
  expect(screen.getByText("Loaded")).toBeInTheDocument();
});

// With options
await waitFor(() => expect(callback).toHaveBeenCalled(), {
  timeout: 5000,
  interval: 100,
});
```

### findBy — Built-in waitFor

```ts
// Equivalent to: await waitFor(() => getByText('Loaded'))
const element = await screen.findByText("Loaded");
```

### waitForElementToBeRemoved

```ts
await waitForElementToBeRemoved(() => screen.queryByText("Loading..."));
```

---

## Common Patterns

### Custom Render with Providers

```tsx
// test-utils.tsx
import { render } from "@testing-library/react";
import { ThemeProvider } from "./ThemeProvider";
import { AuthProvider } from "./AuthProvider";

function AllProviders({ children }) {
  return (
    <ThemeProvider>
      <AuthProvider>{children}</AuthProvider>
    </ThemeProvider>
  );
}

const customRender = (ui, options) => render(ui, { wrapper: AllProviders, ...options });

export * from "@testing-library/react";
export { customRender as render };
```

### Testing Hooks

```ts
import { renderHook, act } from "@testing-library/react";

test("useCounter increments", () => {
  const { result } = renderHook(() => useCounter());

  expect(result.current.count).toBe(0);

  act(() => {
    result.current.increment();
  });

  expect(result.current.count).toBe(1);
});
```

### Rerender with New Props

```ts
const { rerender } = render(<Counter count={1} />);
expect(screen.getByText("Count: 1")).toBeInTheDocument();

rerender(<Counter count={2} />);
expect(screen.getByText("Count: 2")).toBeInTheDocument();
```

### Query Within Container

```ts
import { within } from "@testing-library/react";

const modal = screen.getByRole("dialog");
const submitBtn = within(modal).getByRole("button", { name: /submit/i });
```

---

## Debugging

```ts
// Print entire DOM
screen.debug();

// Print specific element
screen.debug(screen.getByRole("button"));

// Log available roles
import { logRoles } from "@testing-library/react";
logRoles(container);

// With prettyDOM options
screen.debug(undefined, 10000); // max length
```

---

## jest-dom Matchers

```ts
import "@testing-library/jest-dom";

expect(element).toBeInTheDocument();
expect(element).toBeVisible();
expect(element).toBeEnabled();
expect(element).toBeDisabled();
expect(element).toHaveTextContent("Hello");
expect(element).toHaveValue("input value");
expect(element).toHaveAttribute("href", "/home");
expect(element).toHaveClass("active");
expect(element).toHaveFocus();
expect(element).toBeChecked();
```

---

## Configuration

```ts
import { configure } from "@testing-library/react";

configure({
  // Custom test ID attribute
  testIdAttribute: "data-my-test-id",

  // Async timeout
  asyncUtilTimeout: 5000,

  // Default hidden
  defaultHidden: true,

  // Throw suggestions (debugging)
  throwSuggestions: true,
});
```

---

## ❌ Prohibitions (Anti-patterns)

```ts
// ❌ Don't query by class/id
container.querySelector(".my-class");

// ❌ Don't use container.firstChild
const { container } = render(<Component />);
expect(container.firstChild).toHaveClass("active");

// ❌ Don't use fireEvent when userEvent works
fireEvent.click(button); // Use userEvent.click instead

// ❌ Don't test implementation details
expect(component.state.loading).toBe(false);

// ❌ Don't use waitFor with findBy
await waitFor(() => screen.findByText("x")); // findBy already waits

// ❌ Don't assert inside waitFor callback (unless necessary)
await waitFor(() => {
  expect(mockFn).toHaveBeenCalled(); // OK - need to wait for call
});
```

---

## ✅ Best Practices

```ts
// ✅ Use screen for all queries
import { render, screen } from "@testing-library/react";
render(<Component />);
screen.getByRole("button"); // Good

// ✅ Prefer userEvent over fireEvent
const user = userEvent.setup();
await user.click(button);

// ✅ Use findBy for async elements
const element = await screen.findByText("Loaded");

// ✅ Use queryBy for non-existence assertions
expect(screen.queryByText("Error")).not.toBeInTheDocument();

// ✅ Use within for scoped queries
const form = screen.getByRole("form");
within(form).getByLabelText("Email");

// ✅ Use accessible queries (role, label, text)
getByRole("button", { name: /submit/i });
```

---

## TextMatch Options

```ts
// Exact match (default)
getByText("Hello World");

// Substring match
getByText("llo Worl", { exact: false });

// Regex
getByText(/hello world/i);

// Custom function
getByText((content, element) => {
  return element.tagName === "SPAN" && content.startsWith("Hello");
});
```

---

## Quick Reference

| Import              | Usage                             |
| ------------------- | --------------------------------- |
| `render`            | Render component to DOM           |
| `screen`            | Query the rendered DOM            |
| `cleanup`           | Unmount components (auto in Jest) |
| `act`               | Wrap state updates                |
| `renderHook`        | Test custom hooks                 |
| `within`            | Scope queries to element          |
| `waitFor`           | Retry until assertion passes      |
| `configure`         | Set global options                |
| `userEvent.setup()` | Create user event instance        |
