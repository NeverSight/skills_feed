---
name: react-testing-patterns
description: >-
  React component and hook testing patterns with Testing Library and Vitest. Use when
  writing tests for React components, custom hooks, or data fetching logic. Covers
  component rendering tests, user interaction simulation, async state testing, MSW for
  API mocking, hook testing with renderHook, accessibility assertions, and snapshot
  testing guidelines. Does NOT cover E2E tests (use e2e-testing) or TDD workflow
  enforcement (use tdd-workflow).
license: MIT
compatibility: 'React 18+, Testing Library 14+, MSW 2+, jest-axe, Vitest/Jest'
metadata:
  author: platform-team
  version: '1.0.0'
  sdlc-phase: testing
allowed-tools: Read Edit Write Bash(npm:*) Bash(npx:*)
context: fork
---

# React Testing Patterns

## When to Use

Activate this skill when:
- Writing tests for React components (rendering, interaction, accessibility)
- Testing custom hooks with `renderHook`
- Mocking API calls with MSW (Mock Service Worker)
- Testing async state changes (loading, error, success)
- Auditing component accessibility with jest-axe
- Setting up test infrastructure (providers, test utilities)

Do NOT use this skill for:
- E2E browser tests with Playwright (use `e2e-testing`)
- Backend Python tests (use `pytest-patterns`)
- TDD workflow enforcement (use `tdd-workflow`)
- Writing component implementation code (use `react-frontend-expert`)

## Instructions

### Testing Library Philosophy

**Core principle:** Test behavior, not implementation.

**Query priority** (prefer higher in the list):
1. `getByRole` — accessible role (button, heading, textbox)
2. `getByLabelText` — form elements with labels
3. `getByPlaceholderText` — input placeholders
4. `getByText` — visible text content
5. `getByDisplayValue` — current form input value
6. `getByAltText` — images
7. `getByTestId` — last resort (data-testid attribute)

**Interaction:** Always use `userEvent` over `fireEvent`:
```tsx
import userEvent from "@testing-library/user-event";

// Good — simulates real user behavior
const user = userEvent.setup();
await user.click(button);
await user.type(input, "hello");

// Bad — low-level event dispatch
fireEvent.click(button);
```

**What NOT to test:**
- Internal component state (don't test `useState` values directly)
- CSS classes or styles
- Component instance methods
- Which hooks were called
- Snapshot tests for dynamic content
- Third-party library internals

### Component Test Structure

Every component test follows Arrange → Act → Assert:

```tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { axe } from "jest-axe";
import { UserCard } from "./UserCard";

describe("UserCard", () => {
  const defaultProps = {
    user: { id: 1, displayName: "Alice", email: "alice@example.com" },
    onEdit: vi.fn(),
  };

  it("renders user name", () => {
    // Arrange
    render(<UserCard {...defaultProps} />);
    // Assert
    expect(screen.getByText("Alice")).toBeInTheDocument();
  });

  it("calls onEdit when edit button is clicked", async () => {
    // Arrange
    const user = userEvent.setup();
    render(<UserCard {...defaultProps} />);
    // Act
    await user.click(screen.getByRole("button", { name: /edit/i }));
    // Assert
    expect(defaultProps.onEdit).toHaveBeenCalledWith(1);
  });

  it("has no accessibility violations", async () => {
    const { container } = render(<UserCard {...defaultProps} />);
    expect(await axe(container)).toHaveNoViolations();
  });
});
```

### Async Testing

#### waitFor (wait for state update)

```tsx
it("shows user data after loading", async () => {
  render(<UserProfile userId={1} />);

  // Loading state
  expect(screen.getByText(/loading/i)).toBeInTheDocument();

  // Wait for data to appear
  await waitFor(() => {
    expect(screen.getByText("Alice")).toBeInTheDocument();
  });

  // Loading state gone
  expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
});
```

#### findBy (built-in waitFor)

```tsx
it("shows user data after loading", async () => {
  render(<UserProfile userId={1} />);

  // findBy = getBy + waitFor — preferred for async appearance
  const heading = await screen.findByRole("heading", { name: "Alice" });
  expect(heading).toBeInTheDocument();
});
```

**Prefer `findBy*` over `waitFor` + `getBy*`** for elements that appear asynchronously.

#### Testing Error States

```tsx
it("shows error message on API failure", async () => {
  // Override MSW handler for this test
  server.use(
    http.get("/api/users/:id", () => {
      return HttpResponse.json(
        { detail: "User not found" },
        { status: 404 },
      );
    }),
  );

  render(<UserProfile userId={999} />);

  const error = await screen.findByRole("alert");
  expect(error).toHaveTextContent(/not found/i);
});
```

### MSW API Mocking

Setup a mock server for all API tests:

```tsx
// test/mocks/handlers.ts
import { http, HttpResponse } from "msw";

export const handlers = [
  http.get("/api/users", () => {
    return HttpResponse.json({
      items: [
        { id: 1, displayName: "Alice", email: "alice@example.com" },
        { id: 2, displayName: "Bob", email: "bob@example.com" },
      ],
      next_cursor: null,
      has_more: false,
    });
  }),

  http.get("/api/users/:id", ({ params }) => {
    return HttpResponse.json({
      id: Number(params.id),
      displayName: "Alice",
      email: "alice@example.com",
    });
  }),

  http.post("/api/users", async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json(
      { id: 3, ...body, created_at: new Date().toISOString() },
      { status: 201 },
    );
  }),
];
```

```tsx
// test/mocks/server.ts
import { setupServer } from "msw/node";
import { handlers } from "./handlers";

export const server = setupServer(...handlers);
```

```tsx
// test/setup.ts (Vitest setup file)
import { server } from "./mocks/server";

beforeAll(() => server.listen({ onUnhandledRequest: "error" }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

**Per-test handler override:**
```tsx
server.use(
  http.get("/api/users", () => {
    return HttpResponse.json({ items: [], next_cursor: null, has_more: false });
  }),
);
```

### Hook Testing

```tsx
import { renderHook, act } from "@testing-library/react";
import { useDebounce } from "./useDebounce";

describe("useDebounce", () => {
  beforeEach(() => { vi.useFakeTimers(); });
  afterEach(() => { vi.useRealTimers(); });

  it("returns initial value immediately", () => {
    const { result } = renderHook(() => useDebounce("hello", 300));
    expect(result.current).toBe("hello");
  });

  it("debounces value changes", () => {
    const { result, rerender } = renderHook(
      ({ value }) => useDebounce(value, 300),
      { initialProps: { value: "hello" } },
    );

    rerender({ value: "world" });
    expect(result.current).toBe("hello"); // Still old value

    act(() => { vi.advanceTimersByTime(300); });
    expect(result.current).toBe("world"); // Now updated
  });
});
```

**Testing hooks with TanStack Query:**
```tsx
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

function createWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return ({ children }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}

it("fetches users", async () => {
  const { result } = renderHook(() => useUsers(), { wrapper: createWrapper() });
  await waitFor(() => expect(result.current.isSuccess).toBe(true));
  expect(result.current.data).toHaveLength(2);
});
```

### Accessibility Testing

Add to every component test file:

```tsx
import { axe, toHaveNoViolations } from "jest-axe";

expect.extend(toHaveNoViolations);

it("has no accessibility violations", async () => {
  const { container } = render(<UserCard {...defaultProps} />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### Test Utility: Custom Render

Create a custom render that wraps components with required providers:

```tsx
// test/utils.tsx
import { render, RenderOptions } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { MemoryRouter } from "react-router-dom";
import { AuthProvider } from "@/contexts/AuthContext";

function AllProviders({ children }: { children: React.ReactNode }) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false, gcTime: 0 } },
  });
  return (
    <QueryClientProvider client={queryClient}>
      <MemoryRouter>
        <AuthProvider>{children}</AuthProvider>
      </MemoryRouter>
    </QueryClientProvider>
  );
}

export function renderWithProviders(ui: React.ReactElement, options?: RenderOptions) {
  return render(ui, { wrapper: AllProviders, ...options });
}
```

## Examples

### Testing a Form Component

```tsx
describe("CreateUserForm", () => {
  it("submits valid data", async () => {
    const onSubmit = vi.fn();
    const user = userEvent.setup();
    render(<CreateUserForm onSubmit={onSubmit} />);

    await user.type(screen.getByLabelText(/email/i), "test@example.com");
    await user.type(screen.getByLabelText(/name/i), "Test User");
    await user.click(screen.getByRole("button", { name: /create/i }));

    expect(onSubmit).toHaveBeenCalledWith({
      email: "test@example.com",
      displayName: "Test User",
      role: "member",
    });
  });

  it("shows validation errors for empty required fields", async () => {
    const user = userEvent.setup();
    render(<CreateUserForm onSubmit={vi.fn()} />);
    await user.click(screen.getByRole("button", { name: /create/i }));

    expect(await screen.findByText(/required/i)).toBeInTheDocument();
  });
});
```

## Edge Cases

- **Components with providers:** Always use a custom render function that wraps components with `QueryClientProvider`, `MemoryRouter`, and any context providers needed.

- **Components with router:** Use `<MemoryRouter initialEntries={["/users/1"]}>` for components that use `useParams` or `useNavigate`.

- **Flaky async tests:** Prefer `findBy*` over `waitFor` + `getBy*`. If using `waitFor`, increase timeout for CI: `waitFor(() => ..., { timeout: 5000 })`.

- **Testing modals/portals:** Use `screen` queries (they search the entire document), not `container` queries.

- **Cleanup:** Testing Library auto-cleans after each test. Don't call `cleanup()` manually unless using a custom setup.

See `references/component-test-template.tsx` for an annotated test file template.
See `references/msw-handler-examples.ts` for MSW handler patterns.
See `references/hook-test-template.tsx` for hook testing patterns.
