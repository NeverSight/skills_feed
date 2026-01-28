---
name: react-router
description: Master React Router v6 for production routing with error boundaries, lazy loading, and navigation guards
sasmp_version: "2.0.0"
bonded_agent: 05-routing-navigation
bond_type: PRIMARY_BOND
input_validation:
  required_packages:
    - "react-router-dom": ">=6.0.0"
output_format:
  code_examples: jsx
  test_template: jest
error_handling:
  patterns:
    - error_boundary
    - lazy_retry
    - 404_fallback
observability:
  logging: structured
  metrics: ["navigation_count", "route_load_time"]
---

# React Router Skill

## Overview
Master React Router v6 for building single-page applications with client-side routing, including nested routes, protected routes, and navigation patterns.

## Learning Objectives
- Configure React Router
- Implement nested and dynamic routes
- Use navigation hooks and components
- Build protected routes
- Handle route parameters and search params

## Quick Start

### Installation
```bash
npm install react-router-dom
```

### Basic Setup
```jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/users/:userId" element={<UserProfile />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}
```

## Navigation

### Link Component
```jsx
import { Link, NavLink } from 'react-router-dom';

function Nav() {
  return (
    <nav>
      <Link to="/">Home</Link>
      <NavLink to="/about" className={({ isActive }) => isActive ? 'active' : ''}>
        About
      </NavLink>
    </nav>
  );
}
```

### Programmatic Navigation
```jsx
import { useNavigate } from 'react-router-dom';

function LoginForm() {
  const navigate = useNavigate();

  const handleSubmit = async (credentials) => {
    await login(credentials);
    navigate('/dashboard'); // Navigate after login
    // navigate(-1); // Go back
    // navigate('/home', { replace: true }); // Replace history
  };

  return <form onSubmit={handleSubmit}>...</form>;
}
```

## Route Parameters

```jsx
import { useParams } from 'react-router-dom';

// Route: /users/:userId
function UserProfile() {
  const { userId } = useParams();

  return <div>User ID: {userId}</div>;
}

// Multiple params: /posts/:postId/comments/:commentId
function Comment() {
  const { postId, commentId } = useParams();
  // ...
}
```

## Search Parameters

```jsx
import { useSearchParams } from 'react-router-dom';

function ProductList() {
  const [searchParams, setSearchParams] = useSearchParams();

  const category = searchParams.get('category') || 'all';
  const sort = searchParams.get('sort') || 'name';

  const updateCategory = (newCategory) => {
    setSearchParams({ category: newCategory, sort });
  };

  return (
    <div>
      {/* URL: /products?category=electronics&sort=price */}
      <select value={category} onChange={(e) => updateCategory(e.target.value)}>
        <option value="all">All</option>
        <option value="electronics">Electronics</option>
      </select>
    </div>
  );
}
```

## Nested Routes

```jsx
import { Outlet } from 'react-router-dom';

function DashboardLayout() {
  return (
    <div>
      <DashboardNav />
      <main>
        <Outlet /> {/* Child routes render here */}
      </main>
    </div>
  );
}

// Route configuration
<Route path="/dashboard" element={<DashboardLayout />}>
  <Route index element={<DashboardHome />} />
  <Route path="profile" element={<Profile />} />
  <Route path="settings" element={<Settings />} />
</Route>
```

## Protected Routes

```jsx
import { Navigate, useLocation } from 'react-router-dom';

function ProtectedRoute({ children }) {
  const { user } = useAuth();
  const location = useLocation();

  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
}

// Usage
<Route
  path="/dashboard"
  element={
    <ProtectedRoute>
      <Dashboard />
    </ProtectedRoute>
  }
/>
```

## Code Splitting

```jsx
import { lazy, Suspense } from 'react';

const Home = lazy(() => import('./pages/Home'));
const Dashboard = lazy(() => import('./pages/Dashboard'));

function App() {
  return (
    <Suspense fallback={<Spinner />}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Suspense>
  );
}
```

## Practice Exercises

1. Build multi-page app with navigation
2. Implement nested dashboard routes
3. Create protected authentication routes
4. Build dynamic product detail pages
5. Implement search with URL params
6. Create breadcrumb navigation
7. Build modal routes

## Resources

- [React Router Docs](https://reactrouter.com)
- [React Router Tutorial](https://reactrouter.com/en/main/start/tutorial)

---

## Error Boundary Pattern

```jsx
import { useRouteError, isRouteErrorResponse } from 'react-router-dom';

function RouteErrorBoundary() {
  const error = useRouteError();

  if (isRouteErrorResponse(error)) {
    if (error.status === 404) {
      return <NotFoundPage />;
    }
    return <ErrorPage status={error.status} message={error.statusText} />;
  }

  return <ErrorPage message="Something went wrong" />;
}

// Router configuration with error handling
const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    errorElement: <RouteErrorBoundary />,
    children: [/* routes */],
  },
]);
```

## Lazy Loading with Retry

```jsx
function lazyWithRetry(importFn, retries = 3) {
  return lazy(async () => {
    for (let i = 0; i < retries; i++) {
      try {
        return await importFn();
      } catch (err) {
        if (i === retries - 1) throw err;
        await new Promise(r => setTimeout(r, 1000 * Math.pow(2, i)));
      }
    }
  });
}

const Dashboard = lazyWithRetry(() => import('./Dashboard'));
```

## Unit Test Template

```jsx
import { render, screen } from '@testing-library/react';
import { MemoryRouter, Routes, Route } from 'react-router-dom';

describe('Routing', () => {
  it('renders correct route', () => {
    render(
      <MemoryRouter initialEntries={['/dashboard']}>
        <Routes>
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByText(/dashboard/i)).toBeInTheDocument();
  });
});
```

---

**Version**: 2.0.0
**Last Updated**: 2025-12-30
**SASMP Version**: 2.0.0
**Difficulty**: Intermediate
**Estimated Time**: 1-2 weeks
**Prerequisites**: React Fundamentals
**Changelog**: Added error boundaries, lazy retry, and test templates
