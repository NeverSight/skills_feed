---
name: react-router
description: React Router v7 Data Mode for Vite SPA with Convex backend. Triggers on routing, navigation, nested routes, protected routes, lazy loading. Use for client-side routing in Vite React apps.
---

# React Router v7 (Data Mode for Vite SPA + Convex)

Use **Data Mode** (`createBrowserRouter` + `RouterProvider`) for Vite SPAs with Convex.

> Attribution: [remix-run/react-router](https://github.com/remix-run/react-router)

## Key Principle

**Convex handles data, Router handles navigation.**

- **React Router**: routing, navigation, URL params, nested layouts, lazy loading
- **Convex**: data fetching (`useQuery`), mutations (`useMutation`), real-time updates

Don't use React Router loaders/actions with Convex.

## Installation

```bash
react-router-dom
```

_(Install with your project's package manager)_

## Basic Setup

```typescript
// main.tsx
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { ConvexProvider, ConvexReactClient } from "convex/react";

const convex = new ConvexReactClient(import.meta.env.VITE_CONVEX_URL);

const router = createBrowserRouter([
  {
    path: "/",
    Component: Layout,
    ErrorBoundary: RootError,
    children: [
      { index: true, Component: Home },
      { path: "projects", Component: Projects },
      { path: "projects/:projectId", Component: Project },
    ],
  },
]);

// HMR cleanup for Vite
if (import.meta.hot) {
  import.meta.hot.dispose(() => router.dispose());
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ConvexProvider client={convex}>
      <RouterProvider router={router} fallbackElement={<p>Loading...</p>} />
    </ConvexProvider>
  </StrictMode>
);
```

## Nested Routes & Outlet

```typescript
function Layout() {
  return (
    <div>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/projects">Projects</Link>
      </nav>
      <Outlet /> {/* Child routes render here */}
    </div>
  );
}
```

## URL Params + Convex Query

```typescript
function Project() {
  const { projectId } = useParams<{ projectId: string }>();
  
  const project = useQuery(
    api.projects.get,
    projectId ? { id: projectId as Id<"projects"> } : "skip"
  );

  if (project === undefined) return <p>Loading...</p>;
  if (project === null) return <p>Not found</p>;

  return <h1>{project.name}</h1>;
}
```

## Mutation + Navigate

```typescript
function CreateProject() {
  const navigate = useNavigate();
  const createProject = useMutation(api.projects.create);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const id = await createProject({ name: formData.get("name") as string });
    navigate(`/projects/${id}`);
  }

  return (
    <form onSubmit={handleSubmit}>
      <input name="name" required />
      <button type="submit">Create</button>
    </form>
  );
}
```

## Protected Routes

```typescript
function ProtectedRoute() {
  const { isAuthenticated, isLoading } = useConvexAuth();
  const location = useLocation();

  if (isLoading) return <p>Loading...</p>;
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }
  return <Outlet />;
}

// Usage in router
{
  Component: ProtectedRoute,
  children: [
    { path: "dashboard", Component: Dashboard },
  ],
}
```

## Quick Reference

| Task | API |
|------|-----|
| Navigate programmatically | `useNavigate()` |
| Get URL params | `useParams()` |
| Get/set search params | `useSearchParams()` |
| Get current location | `useLocation()` |
| Check navigation state | `useNavigation()` |
| Link with active state | `<NavLink>` |
| Render child routes | `<Outlet />` |
| Code split routes | `lazy: () => import()` |

## Critical Rules

1. **Use Convex hooks for data** - `useQuery`/`useMutation` provide real-time updates
2. **Don't use loaders/actions** - Convex handles data, Router handles navigation
3. **Handle loading states** - `useQuery` returns `undefined` while loading
4. **Dispose router in HMR** - Prevents memory leaks in Vite dev mode
5. **Wrap Router in ConvexProvider** - Convex context must be available

## Deep Dive References

- [examples.md](references/examples.md) - Complete CRUD, auth patterns, search params
- [api.md](references/api.md) - All hooks and components reference
