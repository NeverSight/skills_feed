---
name: loader-action-optimizer
description: Best practices for React Router v7 loaders and actions - parallel fetching, deferred data, optimistic UI, and error handling patterns
tags: [react-router, performance, data-fetching, optimization]
version: 1.0.0
author: Code Visionary
---

# Loader & Action Optimizer

Master React Router v7's data loading and mutation patterns. Learn how to fetch data efficiently, handle errors gracefully, and create responsive user experiences.

## Quick Reference

### Basic Loader Pattern

```typescript
export async function loader({ request, params }: LoaderFunctionArgs) {
  const data = await fetchData(params.id);
  return { data };
}
```

### Basic Action Pattern

```typescript
export async function action({ request }: ActionFunctionArgs) {
  const formData = await request.formData();
  const result = await submitData(formData);
  return redirect(`/success`);
}
```

### Parallel Data Loading

```typescript
export async function loader() {
  const [users, posts, comments] = await Promise.all([
    fetchUsers(),
    fetchPosts(),
    fetchComments(),
  ]);
  return { users, posts, comments };
}
```

## When to Use This Skill

- Setting up data loading for routes
- Optimizing multiple API calls
- Implementing form submissions
- Handling server-side validation
- Creating optimistic UI updates
- Streaming data with deferred responses

## Core Concepts

### Loaders: Fetching Data

Loaders run **before** the route component renders, providing data to your page.

**Key principles:**
- Run on the server (SSR) and client
- Execute in parallel for all matching routes
- Block navigation until complete (unless deferred)
- Should be fast - optimize aggressively

### Actions: Mutating Data

Actions handle form submissions and data mutations.

**Key principles:**
- Only run on POST, PUT, PATCH, DELETE requests
- Execute before loaders
- Trigger revalidation of all loaders
- Return data or redirect

## Loader Patterns

### 1. Single Data Source

```typescript
import type { LoaderFunctionArgs } from "react-router";

export async function loader({ params }: LoaderFunctionArgs) {
  const user = await db.user.findUnique({
    where: { id: params.userId }
  });
  
  if (!user) {
    throw new Response("Not Found", { status: 404 });
  }
  
  return { user };
}
```

### 2. Parallel Data Loading (Recommended)

```typescript
export async function loader({ params }: LoaderFunctionArgs) {
  // ✅ All requests start simultaneously
  const [user, posts, followers] = await Promise.all([
    fetchUser(params.userId),
    fetchUserPosts(params.userId),
    fetchUserFollowers(params.userId),
  ]);
  
  return { user, posts, followers };
}
```

### 3. Sequential with Dependency

```typescript
export async function loader({ params }: LoaderFunctionArgs) {
  // First fetch required data
  const user = await fetchUser(params.userId);
  
  // Then fetch dependent data
  const recommendations = await fetchRecommendations(user.preferences);
  
  return { user, recommendations };
}
```

### 4. Deferred Data (Streaming)

Load critical data immediately, stream non-critical data later:

```typescript
import { defer } from "react-router";

export async function loader({ params }: LoaderFunctionArgs) {
  // Critical: Wait for this
  const user = await fetchUser(params.userId);
  
  // Non-critical: Don't wait
  const analyticsPromise = fetchAnalytics(params.userId);
  
  return defer({
    user,              // Available immediately
    analytics: analyticsPromise  // Resolves later
  });
}
```

**In your component:**

```tsx
import { Await, useLoaderData } from "react-router";
import { Suspense } from "react";

export default function UserProfile() {
  const { user, analytics } = useLoaderData<typeof loader>();
  
  return (
    <div>
      <h1>{user.name}</h1>  {/* Shows immediately */}
      
      <Suspense fallback={<Spinner />}>
        <Await resolve={analytics}>
          {(data) => <AnalyticsChart data={data} />}
        </Await>
      </Suspense>
    </div>
  );
}
```

### 5. Error Handling in Loaders

```typescript
export async function loader({ params }: LoaderFunctionArgs) {
  try {
    const data = await fetchData(params.id);
    return { data };
  } catch (error) {
    // Throw responses for expected errors
    if (error.status === 404) {
      throw new Response("Not Found", { status: 404 });
    }
    
    // Re-throw unexpected errors
    throw error;
  }
}
```

### 6. Authentication Check

```typescript
export async function loader({ request }: LoaderFunctionArgs) {
  const user = await requireAuth(request);
  
  if (!user) {
    throw redirect("/login");
  }
  
  const data = await fetchPrivateData(user.id);
  return { user, data };
}
```

## Action Patterns

### 1. Form Submission with Validation

```typescript
import { redirect } from "react-router";
import { z } from "zod";

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

export async function action({ request }: ActionFunctionArgs) {
  const formData = await request.formData();
  
  // Validate
  const result = schema.safeParse({
    email: formData.get("email"),
    password: formData.get("password"),
  });
  
  if (!result.success) {
    return {
      errors: result.error.flatten().fieldErrors,
    };
  }
  
  // Process
  const user = await createUser(result.data);
  
  // Redirect on success
  return redirect(`/users/${user.id}`);
}
```

**In your component:**

```tsx
import { Form, useActionData } from "react-router";

export default function CreateUser() {
  const actionData = useActionData<typeof action>();
  
  return (
    <Form method="post">
      <input name="email" />
      {actionData?.errors?.email && (
        <span>{actionData.errors.email}</span>
      )}
      
      <input name="password" type="password" />
      {actionData?.errors?.password && (
        <span>{actionData.errors.password}</span>
      )}
      
      <button type="submit">Create User</button>
    </Form>
  );
}
```

### 2. Intent-Based Actions

Handle multiple actions in one route:

```typescript
export async function action({ request }: ActionFunctionArgs) {
  const formData = await request.formData();
  const intent = formData.get("intent");
  
  switch (intent) {
    case "delete":
      await deleteItem(formData.get("id"));
      return { success: true };
      
    case "archive":
      await archiveItem(formData.get("id"));
      return { success: true };
      
    case "update":
      await updateItem(formData.get("id"), formData);
      return redirect("/items");
      
    default:
      throw new Response("Invalid intent", { status: 400 });
  }
}
```

**In your component:**

```tsx
<Form method="post">
  <input type="hidden" name="intent" value="delete" />
  <button type="submit">Delete</button>
</Form>

<Form method="post">
  <input type="hidden" name="intent" value="archive" />
  <button type="submit">Archive</button>
</Form>
```

### 3. Optimistic UI Updates

```tsx
import { useFetcher } from "react-router";

function TodoItem({ todo }) {
  const fetcher = useFetcher();
  
  // Optimistic state
  const isCompleted = 
    fetcher.formData?.get("completed") === "true" 
      ? true 
      : todo.completed;
  
  return (
    <fetcher.Form method="post" action={`/todos/${todo.id}`}>
      <input
        type="checkbox"
        name="completed"
        value="true"
        checked={isCompleted}
        onChange={(e) => {
          fetcher.submit(e.currentTarget.form);
        }}
      />
      <span style={{ opacity: isCompleted ? 0.5 : 1 }}>
        {todo.text}
      </span>
    </fetcher.Form>
  );
}
```

### 4. File Upload

```typescript
export async function action({ request }: ActionFunctionArgs) {
  const formData = await request.formData();
  const file = formData.get("avatar") as File;
  
  if (!file || file.size === 0) {
    return { error: "No file provided" };
  }
  
  // Upload to storage
  const url = await uploadFile(file);
  
  // Update database
  await updateUserAvatar(formData.get("userId"), url);
  
  return { success: true, url };
}
```

## Performance Optimization

### 1. Cache Loader Results

```typescript
const cache = new Map();

export async function loader({ params }: LoaderFunctionArgs) {
  const cacheKey = `user-${params.userId}`;
  
  if (cache.has(cacheKey)) {
    return cache.get(cacheKey);
  }
  
  const user = await fetchUser(params.userId);
  cache.set(cacheKey, { user });
  
  return { user };
}
```

### 2. Abort Stale Requests

```typescript
export async function loader({ request, params }: LoaderFunctionArgs) {
  const { signal } = request;
  
  const data = await fetch(`/api/data/${params.id}`, { signal });
  
  return data.json();
}
```

### 3. Revalidation Control

```tsx
// Disable automatic revalidation
export function shouldRevalidate() {
  return false;
}

// Conditional revalidation
export function shouldRevalidate({ 
  currentUrl, 
  nextUrl, 
  formMethod,
  defaultShouldRevalidate 
}) {
  // Only revalidate after POST requests
  if (formMethod === "POST") return true;
  
  // Don't revalidate on same URL
  if (currentUrl.pathname === nextUrl.pathname) return false;
  
  return defaultShouldRevalidate;
}
```

## Common Patterns

### Toast Notifications After Actions

```typescript
export async function action({ request }: ActionFunctionArgs) {
  await performAction();
  
  return {
    toast: {
      type: "success",
      message: "Action completed successfully!"
    }
  };
}
```

```tsx
export default function Component() {
  const actionData = useActionData<typeof action>();
  
  useEffect(() => {
    if (actionData?.toast) {
      toast[actionData.toast.type](actionData.toast.message);
    }
  }, [actionData]);
  
  return <div>...</div>;
}
```

### Search Params Handling

```typescript
export async function loader({ request }: LoaderFunctionArgs) {
  const url = new URL(request.url);
  const query = url.searchParams.get("q") || "";
  const page = Number(url.searchParams.get("page")) || 1;
  
  const results = await searchItems({ query, page });
  
  return { results, query, page };
}
```

## Common Issues

### Issue 1: Loaders Don't Rerun

**Symptoms**: Data doesn't refresh after navigation
**Cause**: React Router caches loader results
**Solution**: Use `revalidate()` or navigation options

```tsx
import { useRevalidator } from "react-router";

function Component() {
  const revalidator = useRevalidator();
  
  return (
    <button onClick={() => revalidator.revalidate()}>
      Refresh Data
    </button>
  );
}
```

### Issue 2: Race Conditions

**Symptoms**: Stale data appears when navigating quickly
**Cause**: Slower requests complete after faster ones
**Solution**: Use request.signal for automatic cancellation

```typescript
export async function loader({ request }: LoaderFunctionArgs) {
  const data = await fetch("/api/data", { 
    signal: request.signal  // Auto-cancels on navigation
  });
  return data.json();
}
```

### Issue 3: Slow Initial Load

**Symptoms**: Page takes too long to show
**Cause**: Loading too much data upfront
**Solution**: Use `defer()` for non-critical data

```typescript
import { defer } from "react-router";

export async function loader() {
  const critical = await fetchCritical();
  const nonCritical = fetchNonCritical(); // Don't await!
  
  return defer({ critical, nonCritical });
}
```

## Best Practices

- [ ] Run independent fetches in parallel with `Promise.all()`
- [ ] Use `defer()` for non-critical data to improve perceived performance
- [ ] Throw Response objects for expected errors (404, 401, etc.)
- [ ] Validate form data in actions before processing
- [ ] Use `redirect()` for successful mutations
- [ ] Pass `request.signal` to fetch calls for automatic cancellation
- [ ] Return validation errors from actions instead of throwing
- [ ] Use `shouldRevalidate()` to optimize when loaders rerun
- [ ] Handle loading states with useNavigation
- [ ] Use useFetcher for non-navigation mutations

## Anti-Patterns

Things to avoid:

- ❌ Sequential fetching when parallel is possible
- ❌ Fetching data in useEffect instead of loaders
- ❌ Not handling loading and error states
- ❌ Returning large payloads (serialize only what you need)
- ❌ Using actions for GET requests
- ❌ Ignoring validation in actions
- ❌ Not leveraging automatic revalidation
- ❌ Mixing client and server state management

## Testing

### Testing Loaders

```typescript
import { loader } from "./route";

describe("loader", () => {
  it("fetches user data", async () => {
    const request = new Request("http://localhost/users/123");
    const params = { userId: "123" };
    
    const result = await loader({ 
      request, 
      params, 
      context: {} 
    });
    
    expect(result.user).toBeDefined();
  });
});
```

### Testing Actions

```typescript
import { action } from "./route";

describe("action", () => {
  it("validates form data", async () => {
    const formData = new FormData();
    formData.set("email", "invalid");
    
    const request = new Request("http://localhost/users", {
      method: "POST",
      body: formData,
    });
    
    const result = await action({ request, params: {}, context: {} });
    
    expect(result.errors).toBeDefined();
  });
});
```

## References

- [React Router Loaders Documentation](https://reactrouter.com/start/framework/data-loading)
- [React Router Actions Documentation](https://reactrouter.com/start/framework/actions)
- [React Router Form Documentation](https://reactrouter.com/start/framework/forms)
- [Deferred Data Guide](https://reactrouter.com/start/framework/deferred-data)
- [route-error-handling skill](../route-error-handling/)
- [data-fetching-patterns skill](../data-fetching-patterns/)
