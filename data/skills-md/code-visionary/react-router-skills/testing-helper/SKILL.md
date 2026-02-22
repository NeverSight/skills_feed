---
name: testing-helper
description: Testing patterns for React and React Router v7 - Vitest, React Testing Library, route testing, mocking loaders/actions
tags: [testing, vitest, react-testing-library, react-router]
version: 1.0.0
author: Code Visionary
---

# Testing Helper

Master testing for React and React Router v7 applications. Learn how to write effective tests using Vitest and React Testing Library.

## Quick Reference

### Basic Component Test

```typescript
import { render, screen } from "@testing-library/react";
import { expect, test } from "vitest";

test("renders button", () => {
  render(<Button>Click me</Button>);
  expect(screen.getByText("Click me")).toBeInTheDocument();
});
```

### Test User Interactions

```typescript
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

test("handles click", async () => {
  const user = userEvent.setup();
  const handleClick = vi.fn();
  
  render(<Button onClick={handleClick}>Click</Button>);
  await user.click(screen.getByRole("button"));
  
  expect(handleClick).toHaveBeenCalledOnce();
});
```

### Test Loaders

```typescript
import { loader } from "./route";

test("loader fetches user", async () {
  const result = await loader({
    params: { userId: "123" },
    request: new Request("http://localhost"),
    context: {},
  });
  
  expect(result.user).toBeDefined();
});
```

## When to Use This Skill

- Setting up testing infrastructure
- Writing component tests
- Testing loaders and actions
- Mocking API calls
- Testing user interactions
- Testing forms and validation
- Integration testing routes

## Setup

### Install Dependencies

```bash
npm install -D vitest @testing-library/react @testing-library/user-event @testing-library/jest-dom jsdom
```

### Configure Vitest

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    setupFiles: ["./test/setup.ts"],
    globals: true,
  },
});
```

### Test Setup File

```typescript
// test/setup.ts
import "@testing-library/jest-dom";
import { expect, afterEach } from "vitest";
import { cleanup } from "@testing-library/react";

// Cleanup after each test
afterEach(() => {
  cleanup();
});
```

## Component Testing

### 1. Basic Rendering

```typescript
import { render, screen } from "@testing-library/react";
import { describe, test, expect } from "vitest";
import { UserCard } from "./UserCard";

describe("UserCard", () => {
  test("renders user information", () => {
    const user = {
      id: "1",
      name: "John Doe",
      email: "john@example.com",
    };
    
    render(<UserCard user={user} />);
    
    expect(screen.getByText("John Doe")).toBeInTheDocument();
    expect(screen.getByText("john@example.com")).toBeInTheDocument();
  });
  
  test("displays avatar when provided", () => {
    const user = {
      id: "1",
      name: "John Doe",
      email: "john@example.com",
      avatar: "https://example.com/avatar.jpg",
    };
    
    render(<UserCard user={user} />);
    
    const avatar = screen.getByRole("img", { name: "John Doe" });
    expect(avatar).toHaveAttribute("src", user.avatar);
  });
});
```

### 2. User Interactions

```typescript
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { vi } from "vitest";

test("calls onClick when button is clicked", async () => {
  const user = userEvent.setup();
  const handleClick = vi.fn();
  
  render(<Button onClick={handleClick}>Click me</Button>);
  
  await user.click(screen.getByRole("button", { name: "Click me" }));
  
  expect(handleClick).toHaveBeenCalledOnce();
});

test("types in input field", async () => {
  const user = userEvent.setup();
  const handleChange = vi.fn();
  
  render(<input onChange={handleChange} />);
  
  await user.type(screen.getByRole("textbox"), "Hello");
  
  expect(screen.getByRole("textbox")).toHaveValue("Hello");
  expect(handleChange).toHaveBeenCalledTimes(5); // Once per character
});
```

### 3. Async Operations

```typescript
import { render, screen, waitFor } from "@testing-library/react";

test("loads and displays data", async () => {
  render(<UserProfile userId="123" />);
  
  // Initially shows loading
  expect(screen.getByText("Loading...")).toBeInTheDocument();
  
  // Wait for data to load
  await waitFor(() => {
    expect(screen.getByText("John Doe")).toBeInTheDocument();
  });
  
  // Loading indicator is gone
  expect(screen.queryByText("Loading...")).not.toBeInTheDocument();
});
```

## Testing React Router

### 1. Test Loaders

```typescript
import { loader } from "./route";
import { vi } from "vitest";

// Mock fetch
global.fetch = vi.fn();

test("loader returns user data", async () => {
  const mockUser = { id: "123", name: "John" };
  
  (fetch as any).mockResolvedValueOnce({
    ok: true,
    json: async () => mockUser,
  });
  
  const result = await loader({
    params: { userId: "123" },
    request: new Request("http://localhost/users/123"),
    context: {},
  });
  
  expect(result).toEqual({ user: mockUser });
  expect(fetch).toHaveBeenCalledWith("/api/users/123");
});

test("loader throws on 404", async () => {
  (fetch as any).mockResolvedValueOnce({
    ok: false,
    status: 404,
  });
  
  await expect(loader({
    params: { userId: "999" },
    request: new Request("http://localhost/users/999"),
    context: {},
  })).rejects.toThrow();
});
```

### 2. Test Actions

```typescript
import { action } from "./route";

test("action creates user on valid data", async () => {
  const formData = new FormData();
  formData.set("name", "John Doe");
  formData.set("email", "john@example.com");
  
  const request = new Request("http://localhost/users", {
    method: "POST",
    body: formData,
  });
  
  const result = await action({
    request,
    params: {},
    context: {},
  });
  
  expect(result).toHaveProperty("user");
});

test("action returns errors on invalid data", async () => {
  const formData = new FormData();
  formData.set("name", "");
  formData.set("email", "invalid");
  
  const request = new Request("http://localhost/users", {
    method: "POST",
    body: formData,
  });
  
  const result = await action({
    request,
    params: {},
    context: {},
  });
  
  expect(result).toHaveProperty("errors");
  expect(result.errors).toHaveProperty("name");
  expect(result.errors).toHaveProperty("email");
});
```

### 3. Test Routes with RouterProvider

```typescript
import { render, screen } from "@testing-library/react";
import { createMemoryRouter, RouterProvider } from "react-router";

test("renders route component", async () => {
  const router = createMemoryRouter(
    [
      {
        path: "/users/:userId",
        element: <UserProfile />,
        loader: async () => ({ user: { id: "1", name: "John" } }),
      },
    ],
    {
      initialEntries: ["/users/1"],
    }
  );
  
  render(<RouterProvider router={router} />);
  
  await screen.findByText("John");
});
```

## Mocking

### 1. Mock API Calls

```typescript
import { vi } from "vitest";

// Mock fetch globally
global.fetch = vi.fn();

// Mock specific responses
(fetch as any).mockResolvedValue({
  ok: true,
  json: async () => ({ data: "mocked" }),
});

// Clean up after test
afterEach(() => {
  vi.clearAllMocks();
});
```

### 2. Mock Modules

```typescript
import { vi } from "vitest";

// Mock entire module
vi.mock("./api", () => ({
  fetchUser: vi.fn(),
  createUser: vi.fn(),
}));

// Import mocked module
import { fetchUser } from "./api";

test("uses mocked API", async () => {
  (fetchUser as any).mockResolvedValue({ id: "1", name: "John" });
  
  const user = await fetchUser("1");
  
  expect(user).toEqual({ id: "1", name: "John" });
});
```

### 3. Mock React Router Hooks

```typescript
import { vi } from "vitest";
import * as ReactRouter from "react-router";

vi.spyOn(ReactRouter, "useNavigate").mockReturnValue(vi.fn());
vi.spyOn(ReactRouter, "useLoaderData").mockReturnValue({
  user: { id: "1", name: "John" },
});
```

## Form Testing

```typescript
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { createMemoryRouter, RouterProvider } from "react-router";

test("submits form with valid data", async () => {
  const user = userEvent.setup();
  const actionSpy = vi.fn().mockResolvedValue({ success: true });
  
  const router = createMemoryRouter(
    [
      {
        path: "/create",
        element: <CreateUserForm />,
        action: actionSpy,
      },
    ],
    {
      initialEntries: ["/create"],
    }
  );
  
  render(<RouterProvider router={router} />);
  
  // Fill form
  await user.type(screen.getByLabelText("Name"), "John Doe");
  await user.type(screen.getByLabelText("Email"), "john@example.com");
  
  // Submit
  await user.click(screen.getByRole("button", { name: "Submit" }));
  
  // Verify action was called
  expect(actionSpy).toHaveBeenCalled();
});

test("displays validation errors", async () => {
  const user = userEvent.setup();
  const actionSpy = vi.fn().mockResolvedValue({
    errors: { email: ["Invalid email"] },
  });
  
  const router = createMemoryRouter(
    [
      {
        path: "/create",
        element: <CreateUserForm />,
        action: actionSpy,
      },
    ],
    {
      initialEntries: ["/create"],
    }
  );
  
  render(<RouterProvider router={router} />);
  
  await user.type(screen.getByLabelText("Email"), "invalid");
  await user.click(screen.getByRole("button", { name: "Submit" }));
  
  await screen.findByText("Invalid email");
});
```

## Best Practices

- [ ] Use `screen` queries over destructured render result
- [ ] Prefer `getByRole` over other query methods
- [ ] Use `userEvent` instead of `fireEvent`
- [ ] Test user behavior, not implementation details
- [ ] Mock external dependencies (APIs, modules)
- [ ] Clean up after each test
- [ ] Use `waitFor` for async assertions
- [ ] Test accessibility with role queries
- [ ] Don't test third-party libraries
- [ ] Keep tests simple and focused

## Query Priority

Use queries in this order:

1. **`getByRole`** - Most accessible
2. **`getByLabelText`** - Good for forms
3. **`getByPlaceholderText`** - Form fallback
4. **`getByText`** - User-visible text
5. **`getByTestId`** - Last resort

```typescript
// ✅ Best - accessible
screen.getByRole("button", { name: "Submit" });
screen.getByRole("textbox", { name: "Email" });

// ✅ Good - form labels
screen.getByLabelText("Email");

// ⚠️  Okay - if no role/label
screen.getByPlaceholderText("Enter email");

// ⚠️  Fallback
screen.getByText("Submit");

// ❌ Last resort
screen.getByTestId("submit-button");
```

## Common Issues

### Issue 1: Act Warnings

**Symptoms**: "Warning: An update to Component was not wrapped in act()"
**Cause**: State updates not properly awaited
**Solution**: Use `waitFor` or `findBy` queries

```typescript
// ❌ Causes act warning
render(<AsyncComponent />);
expect(screen.getByText("Loaded")).toBeInTheDocument();

// ✅ Waits for update
render(<AsyncComponent />);
await screen.findByText("Loaded");
```

### Issue 2: Can't Find Element

**Symptoms**: "Unable to find an element"
**Cause**: Wrong query or timing issue
**Solution**: Use correct query method and wait for element

```typescript
// ❌ Element not visible yet
expect(screen.getByText("Success")).toBeInTheDocument();

// ✅ Wait for element to appear
await screen.findByText("Success");

// Or check if it doesn't exist
expect(screen.queryByText("Error")).not.toBeInTheDocument();
```

## References

- [Vitest Documentation](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)
- [Testing Library Queries](https://testing-library.com/docs/queries/about)
- [React Router Testing](https://reactrouter.com/start/framework/testing)
- [loader-action-optimizer skill](../loader-action-optimizer/)
