---
name: react-router-v7-app
description: Implements React Router v7 app structure, routing patterns, and component templates. Use when creating or modifying React Router v7 applications to ensure consistent folder structure, data loading patterns, and component architecture.
---

# React Router v7 App Implementation

## 1. Route Structure
- Use file-based routing in `app/routes/`.
- Route files: `route.tsx` for route components.
- Use underscore prefix for route groups: `_app`, `_landing`.
- Use dot notation for nested routes: `users.$id.tsx`.

## 2. Data Loading Patterns
- Use `loader` functions for server-side data fetching.
- Use `action` functions for form submissions and mutations.
- Leverage `useLoaderData()` and `useActionData()` hooks.
- Handle loading states with `useNavigation()`.

## 3. Route Component Structure
Use arrow functions for all exports.

```typescript
import type { Route } from './+types/route';

export const loader = async ({ request, params, context }: Route.LoaderArgs) => {
  // Server-side data loading
  // Return an object
  return { ... };
};

export const action = async ({ request, params, context }: Route.ActionArgs) => {
  // Handle form submissions and mutations
  // Return an object
  return { ... };
};

const Page = ({ loaderData, actionData }: Route.ComponentProps) => {
  // Component implementation with typed props
  return (
    <div>
      {/* Content */}
    </div>
  );
};

export default Page;
```

## 4. Error Handling
- Use `ErrorBoundary` components for route-level error handling.
- Implement proper error responses in loaders/actions.
- Use `isRouteErrorResponse()` for typed error handling.

## 5. Meta and Headers
- Export `meta` function for dynamic page metadata.
- Export `headers` function for custom HTTP headers.
- Use proper SEO practices with meta tags.

## 6. Project Structure

The `app` folder should follow this structure:

```sh
public                # Static files (images, fonts, etc.)
|
app
|
+-- components        # Shared components
|
+-- config            # Global configuration and environment variables
|
+-- constants         # Global constants
|
+-- hooks             # Shared hooks
|
+-- lib               # Pre-configured reusable libraries
|
+-- routes            # React Router routing directory
|
+-- stores            # Global state stores
|
+-- testing           # Test utilities and mock servers
|
+-- types             # Base types used across the application
|
+-- utils             # Shared utility functions
|
```

### app/components

```sh
app/components
|
+-- shadcn
|   |
|   +-- ui              # shadcn/ui components
|       |
|       +-- button.tsx
|       ...
|
```

### routes

Use collocation to group files related to layouts and pages.

```sh
app/routes/_app._index
|
+-- assets      # Feature-specific static files
|
+-- components  # Feature-scoped components
|
+-- constants   # Feature-specific constants
|
+-- hooks       # Feature-scoped hooks
|
+-- services    # Feature services (business logic)
|
+-- stores      # Feature state stores
|
+-- types       # Feature-specific TypeScript types
|
+-- utils       # Feature-specific utility functions
```

Example structure:

```sh
app/routes
|
+-- _app                # App-wide layout & shared files
|   |
|   +-- route.tsx       # Layout file
|   
+-- _app.index          # App top page
|   |
|   +-- route.tsx       # Page file
|   
+-- _app.todos          # (Example) todos layout & shared files
|   |
|   +-- components      # Components used in layout
|   |
|   +-- types           # Types common to todos
|   |
|   +-- route.tsx       # Layout file
|
+-- _app.todos._index   # (Example) todos top page
|   |
|   +-- components      # Components used in page
|   |
|   +-- route.tsx       # Page file
|
+-- _app.todos.$todoId.edit._index  # (Example) todos edit page
|   |
|   +-- components      # Components used in page
|   |
|   +-- hooks           # Hooks used in page
|   |
|   +-- stores          # Stores used in page
|   |
|   +-- route.tsx       # Page file
|
+-- _app.todos.$todoId_.delete      # (Example) todos delete resource route
    |
    +-- route.tsx       # Resource route file
```

## 7. Advanced Routing Patterns

### Nested Routes for UI Segmentation
Use nested routes to split complex pages (e.g., tabs) into independent route modules.
- Parent route renders shared UI and `<Outlet />`.
- Child routes handle their own data loading (`loader`) and mutations (`action`).
- Reduces prop drilling and isolates logic.

Example (Tabs):
- `routes/user.tsx`: Renders tabs navigation and `<Outlet />`.
- `routes/user.profile.tsx`: Renders profile tab content.
- `routes/user.account.tsx`: Renders account tab content.

### Route-based Modals
Manage modal state via URLs instead of `useState`.
- Define the modal as a child route.
- Parent route renders the background UI and `<Outlet />`.
- Modal component renders inside the `<Outlet />` (often using a Dialog component).
- Closing the modal is a navigation action (e.g., `<Link to="..">`).

Example:
- `routes/users.tsx`: Lists users and contains `<Outlet />`.
- `routes/users.new.tsx`: Renders the "Create User" modal.

