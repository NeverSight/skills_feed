---
name: react-router-7-framework
description: Apply React Router 7 framework mode best practices including server-first data fetching, type-safe loaders/actions, proper hydration strategies, middleware authentication, handle metadata, useMatches/useRouteLoaderData hooks, and maximum type safety. Use when working with React Router 7 framework mode, implementing loaders, actions, route protection, breadcrumbs, streaming with Suspense/Await, URL search params, form validation, optimistic UI, resource routes (API endpoints), route configuration, or building SSR applications.
license: MIT
metadata:
  author: kota
  version: "1.2.0"
---

# React Router 7 Framework Mode Best Practices

## Version Compatibility

This skill targets **React Router 7.9.0+** in framework mode. Key features by version:

| Version | Features |
|---------|----------|
| v7.0 | Framework mode, type generation, loaders/actions, `Route.*` types |
| v7.5 | `href()` utility for type-safe links |
| v7.9+ | Stable middleware and context APIs, v8 future flags |

### Future Flags

Enable v8 features in `react-router.config.ts`:

```typescript
import type { Config } from "@react-router/dev/config";

export default {
  future: {
    v8_middleware: true,        // Middleware support
    v8_splitRouteModules: true, // Route module splitting for performance
  },
} satisfies Config;
```

These will become the default in v8.

## Core Principles

1. **Server-First**: Fetch and process data on the server whenever possible. Only use client-side data fetching when absolutely necessary.
2. **Maximum Type Safety**: Always use React Router 7's generated types (`Route.LoaderArgs`, `Route.ComponentProps`, etc.). Access loader/action data from props or use `typeof loader`/`typeof action` with hooks.
3. **Proper Hydration**: Understand when to use `clientLoader.hydrate = true` and when to skip it
4. **Declarative Data**: Colocate data requirements with routes using loaders
5. **Progressive Enhancement**: Use actions for mutations with automatic revalidation

## Route Configuration

Define routes in `app/routes.ts` using helper functions:

```typescript
import type { RouteConfig } from "@react-router/dev/routes";
import { route, index, layout, prefix } from "@react-router/dev/routes";

export default [
  index("./home.tsx"),
  route("about", "./about.tsx"),
  layout("./auth-layout.tsx", [
    route("login", "./login.tsx"),
    route("register", "./register.tsx"),
  ]),
  ...prefix("api", [
    route("users", "./api/users.tsx"),
  ]),
  route("*", "./not-found.tsx"), // Catch-all 404
] satisfies RouteConfig;
```

**See [references/routes-config.md](references/routes-config.md) for layout routes, Outlet, splat routes, custom IDs, and nested route patterns.**

## Type Safety

### Generated Types

React Router 7 generates route-specific types in `.react-router/types/+types/<route-file>.d.ts` for each route. Always import and use these types:

```typescript
import type { Route } from "./+types/product";

export async function loader({ params }: Route.LoaderArgs) {
  // params is typed based on your route definition
  const product = await db.getProduct(params.id);
  return { product };
}

export default function Product({ loaderData }: Route.ComponentProps) {
  // loaderData is inferred from loader return type
  return <h1>{loaderData.product.name}</h1>;
}
```

### Available Route Types

- `Route.LoaderArgs` - Types for loader parameters (params, request, context)
- `Route.ActionArgs` - Types for action parameters
- `Route.ClientLoaderArgs` - Types for clientLoader parameters (includes serverLoader)
- `Route.ClientActionArgs` - Types for clientAction parameters (includes serverAction)
- `Route.ComponentProps` - Types for component props (includes loaderData, actionData, matches, etc.)

### Accessing Loader/Action Data

**In route module default exports, always use props** — they provide the best type safety and are the recommended approach in framework mode:

```typescript
import type { Route } from "./+types/product";

export async function loader() {
  return { product: await db.getProduct() };
}

export async function action() {
  return { success: true };
}

// ✅ Props are auto-typed for this specific route
export default function Product({
  loaderData,
  actionData,
}: Route.ComponentProps) {
  return <div>{loaderData.product.name}</div>;
}
```

**When to use hooks instead:**

Hooks (`useLoaderData`, `useActionData`) are for **non-route-module contexts** — deep child components, shared UI, or when testing:

```typescript
// In a child component that doesn't have direct access to route props
import { useLoaderData } from "react-router";

function ProductDetails() {
  // Use typeof for type inference
  const { product } = useLoaderData<typeof import("./route").loader>();
  return <span>{product.description}</span>;
}
```

> **Note**: Hook generics like `useLoaderData<typeof loader>()` exist largely for migration from Remix and are considered secondary to the props pattern. The `Route.*` types via props are the "most type-safe / least foot-gun" approach.

**❌ Never use**: `useLoaderData<Route.ComponentProps["loaderData"]>()` — this pattern is incorrect.

### Type-Safe Links

Use the `href` utility for type-safe route generation (v7.5+):

```typescript
import { href } from "react-router";
import { Link, NavLink } from "react-router";

// Basic usage with params
<Link to={href("/products/:id", { id: "123" })} />

// Optional params
<NavLink to={href("/:lang?/about", { lang: "en" })} />

// No params needed
<Link to={href("/contact")} />

// Programmatic use
const productLink = href("/products/:id", { id: productId });
navigate(productLink);

// Type errors caught at compile time:
href("/not/a/valid/path");         // ❌ Error: Invalid path
href("/blog/:slug", { oops: 1 });  // ❌ Error: Invalid param name
href("/blog/:slug", {});           // ❌ Error: Missing required param
```

**Benefits**:
- Compile-time validation of route paths
- Required params are enforced
- Refactoring routes updates all usages
- IDE autocomplete for available routes

## Data Loading Patterns

### 1. Server-Only Loading (Preferred)

Default pattern - load data on the server, hydrate automatically:

```typescript
import type { Route } from "./+types/products";

export async function loader({ params, request }: Route.LoaderArgs) {
  // Runs on server during SSR and on server during client navigations
  const product = await db.getProduct(params.id);
  return { product };
}

export default function Product({ loaderData }: Route.ComponentProps) {
  return <div>{loaderData.product.name}</div>;
}
```

**When to use**: This is the default and preferred pattern. Use unless you have specific client-side requirements.

### 2. Client-Only Loading

Load data exclusively on the client:

```typescript
import type { Route } from "./+types/products";

export async function clientLoader({ params }: Route.ClientLoaderArgs) {
  // Only runs in the browser
  const res = await fetch(`/api/products/${params.id}`);
  return await res.json();
}

// Required when clientLoader runs during hydration
export function HydrateFallback() {
  return <div>Loading...</div>;
}

export default function Product({ loaderData }: Route.ComponentProps) {
  return <div>{loaderData.name}</div>;
}
```

**When to use**:
- Accessing browser-only APIs (localStorage, IndexedDB)
- Client-side caching strategies
- No server environment available

**Important**: `clientLoader.hydrate = true` is implicit when no server `loader` exists.

### 3. Combined Server + Client Loading

Augment server data with client data:

```typescript
import type { Route } from "./+types/products";

export async function loader({ params }: Route.LoaderArgs) {
  // Server data (e.g., from database)
  return await db.getProduct(params.id);
}

export async function clientLoader({
  params,
  serverLoader,
}: Route.ClientLoaderArgs) {
  // Get server data + add client data
  const [serverData, clientData] = await Promise.all([
    serverLoader(),
    getClientOnlyData(params.id),
  ]);
  return { ...serverData, ...clientData };
}
clientLoader.hydrate = true as const; // Use 'as const' for proper type inference

export function HydrateFallback() {
  return <div>Loading...</div>;
}

export default function Product({ loaderData }: Route.ComponentProps) {
  return <div>{loaderData.name}</div>;
}
```

**When to use**:
- Combining server data with client-only data (user preferences, client state)
- Augmenting server data with cached data

**Important**: Set `clientLoader.hydrate = true as const` to call clientLoader during initial hydration.

### 4. Skip Server Hop (BFF Pattern)

Load server data on initial request, then call client API directly:

```typescript
import type { Route } from "./+types/products";

export async function loader({ params }: Route.LoaderArgs) {
  // Server loads data on initial document request
  const product = await db.getProduct(params.id);
  return { product };
}

export async function clientLoader({ params }: Route.ClientLoaderArgs) {
  // Subsequent navigations fetch from API directly (skip server hop)
  const res = await fetch(`/api/products/${params.id}`);
  return await res.json();
}
// clientLoader.hydrate is false (default) - only runs on subsequent navigations

export default function Product({ loaderData }: Route.ComponentProps) {
  return <div>{loaderData.product.name}</div>;
}
```

**When to use**:
- Backend-For-Frontend pattern
- Initial SSR data load, then direct API calls
- Authentication/cookies work for both server and client

**Important**: Do NOT set `clientLoader.hydrate = true` for this pattern. You want clientLoader to skip during hydration.

### 5. Client-Side Caching

Cache server data on client for subsequent navigations:

```typescript
import type { Route } from "./+types/products";

let isInitialRequest = true;
const cache = new Map();

export async function loader({ params }: Route.LoaderArgs) {
  return await db.getProduct(params.id);
}

export async function clientLoader({
  params,
  serverLoader,
}: Route.ClientLoaderArgs) {
  const cacheKey = `product-${params.id}`;

  // First request: prime cache
  if (isInitialRequest) {
    isInitialRequest = false;
    const data = await serverLoader();
    cache.set(cacheKey, data);
    return data;
  }

  // Subsequent requests: use cache
  const cached = cache.get(cacheKey);
  if (cached) return cached;

  const data = await serverLoader();
  cache.set(cacheKey, data);
  return data;
}
clientLoader.hydrate = true as const;

export default function Product({ loaderData }: Route.ComponentProps) {
  return <div>{loaderData.name}</div>;
}
```

**When to use**:
- Optimizing for repeated visits to same routes
- Reducing server round-trips
- Offline-first strategies

## Actions and Mutations

### Server Actions (Preferred)

Handle mutations on the server with automatic revalidation:

```typescript
import type { Route } from "./+types/todos";
import { Form } from "react-router";

export async function loader() {
  // This runs after action completes
  const todos = await db.getTodos();
  return { todos };
}

export async function action({ request }: Route.ActionArgs) {
  const formData = await request.formData();
  const title = formData.get("title");
  await db.createTodo({ title });
  return { success: true };
}

export default function Todos({ loaderData }: Route.ComponentProps) {
  return (
    <div>
      <ul>
        {loaderData.todos.map((todo) => (
          <li key={todo.id}>{todo.title}</li>
        ))}
      </ul>
      <Form method="post">
        <input type="text" name="title" />
        <button type="submit">Add Todo</button>
      </Form>
    </div>
  );
}
```

**Key features**:
- Automatic revalidation of all loaders after action completes
- Type-safe with `Route.ActionArgs`
- Works with `<Form>`, `useFetcher`, and `useSubmit`

### Client Actions

Handle mutations in the browser, optionally calling server action:

```typescript
import type { Route } from "./+types/todos";

export async function action({ request }: Route.ActionArgs) {
  // Server mutation
  const formData = await request.formData();
  await db.createTodo({ title: formData.get("title") });
  return { success: true };
}

export async function clientAction({
  request,
  serverAction,
}: Route.ClientActionArgs) {
  // Invalidate client cache first
  clientCache.invalidate();

  // Optionally call server action
  const result = await serverAction();
  return result;
}

export default function Todos({ loaderData }: Route.ComponentProps) {
  return <Form method="post">{/* form fields */}</Form>;
}
```

**When to use**:
- Need to invalidate client caches before server mutation
- Optimistic UI updates
- Client-side validation before server call

### The `data()` Utility

Use `data()` to return responses with custom status codes and headers from loaders and actions:

```typescript
import { data } from "react-router";
import type { Route } from "./+types/item";

// Return with custom status and headers
export async function action({ request }: Route.ActionArgs) {
  const formData = await request.formData();
  const item = await createItem(formData);

  return data(item, {
    status: 201,
    headers: { "X-Custom-Header": "value" },
  });
}

// Throw 404 to trigger ErrorBoundary
export async function loader({ params }: Route.LoaderArgs) {
  const project = await db.getProject(params.id);

  if (!project) {
    throw data(null, { status: 404 });
  }

  return { project };
}
```

**Common status codes**:
- `201` - Resource created (after successful POST)
- `400` - Bad request (validation errors)
- `404` - Not found (missing resource)
- `403` - Forbidden (unauthorized access)

**Thrown vs returned**:
- `throw data(...)` - Triggers `ErrorBoundary`, stops execution
- `return data(...)` - Returns response, continues rendering

## Route Module Exports

Beyond `loader`, `action`, and the default component, route modules can export additional functions for metadata, headers, and revalidation control.

### meta

Export page metadata (title, description, og tags):

```typescript
import type { Route } from "./+types/product";

export function meta({ data }: Route.MetaArgs) {
  return [
    { title: data.product.name },
    { name: "description", content: data.product.description },
    { property: "og:title", content: data.product.name },
  ];
}
```

### links

Export link tags (stylesheets, preloads, favicons):

```typescript
import type { Route } from "./+types/product";

export function links() {
  return [
    { rel: "stylesheet", href: "/styles/product.css" },
    { rel: "preload", href: "/fonts/brand.woff2", as: "font", type: "font/woff2" },
  ];
}
```

### headers

Control HTTP response headers:

```typescript
import type { Route } from "./+types/product";

export function headers({ loaderHeaders }: Route.HeadersArgs) {
  return {
    "Cache-Control": loaderHeaders.get("Cache-Control") ?? "max-age=300",
    "X-Custom-Header": "value",
  };
}
```

### shouldRevalidate

Control when loaders re-run (optimize performance):

```typescript
import type { Route } from "./+types/products";

export function shouldRevalidate({
  currentUrl,
  nextUrl,
  defaultShouldRevalidate,
}: Route.ShouldRevalidateArgs) {
  // Don't revalidate if only search params changed
  if (currentUrl.pathname === nextUrl.pathname) {
    return false;
  }

  return defaultShouldRevalidate;
}
```

**Use cases for `shouldRevalidate`**:
- Skip revalidation when navigating within the same route
- Prevent unnecessary refetches after certain actions
- Optimize performance for expensive loaders

### ErrorBoundary

Handle errors that occur during loading or rendering:

```typescript
import { isRouteErrorResponse, useRouteError } from "react-router";

export function ErrorBoundary() {
  const error = useRouteError();

  if (isRouteErrorResponse(error)) {
    return (
      <div>
        <h1>{error.status} {error.statusText}</h1>
        <p>{error.data}</p>
      </div>
    );
  }

  return <div>Something went wrong</div>;
}
```

## Server-Only Modules

Use `.server` and `.client` module conventions to prevent accidentally bundling server-only code (secrets, database clients) into the client bundle.

### .server Modules

Files ending in `.server.ts` or in a `.server/` directory are **never bundled into the client**:

```
app/
├── utils/
│   ├── db.server.ts      # Server-only: database client
│   ├── auth.server.ts    # Server-only: auth logic with secrets
│   └── format.ts         # Shared: safe for client and server
└── .server/
    └── secrets.ts        # Server-only: environment secrets
```

```typescript
// app/utils/db.server.ts
import { PrismaClient } from "@prisma/client";

// This code never reaches the client bundle
export const db = new PrismaClient();
```

```typescript
// app/routes/products.tsx
import { db } from "~/utils/db.server"; // Safe: only used in loader

export async function loader() {
  const products = await db.product.findMany();
  return { products };
}
```

### .client Modules

Files ending in `.client.ts` or in a `.client/` directory are **never bundled into the server**:

```typescript
// app/utils/analytics.client.ts
// Browser-only code (window, document, etc.)
export function trackPageView(path: string) {
  window.gtag?.("event", "page_view", { page_path: path });
}
```

### Why This Matters

- **Security**: Secrets and credentials stay on the server
- **Bundle size**: Server-only code doesn't bloat client bundles
- **Compatibility**: Browser-incompatible code (Node APIs, database clients) won't break the client build

> **Rule of thumb**: If a module imports secrets, database clients, or Node-only APIs, name it `.server.ts`.

## Useful Utilities and Hooks

### useFetcher

Submit forms and load data without navigation:

```typescript
import { useFetcher } from "react-router";

function TodoItem({ todo }) {
  const fetcher = useFetcher();
  const isDeleting = fetcher.state === "submitting";

  return (
    <div>
      <span>{todo.title}</span>
      <fetcher.Form method="post" action={`/todos/${todo.id}/delete`}>
        <button disabled={isDeleting}>
          {isDeleting ? "Deleting..." : "Delete"}
        </button>
      </fetcher.Form>
    </div>
  );
}
```

**States**: `"idle" | "submitting" | "loading"`
**Access data**: `fetcher.data` (from loader/action)
**Methods**: `fetcher.submit()`, `fetcher.load()`

### useNavigation

Track global navigation state:

```typescript
import { useNavigation } from "react-router";

function GlobalLoadingIndicator() {
  const navigation = useNavigation();
  const isNavigating = navigation.state !== "idle";

  return isNavigating ? <LoadingSpinner /> : null;
}
```

**States**: `"idle" | "loading" | "submitting"`

### useActionData

Access data returned from the most recent action. **In route modules, prefer `actionData` from props** (see "Accessing Loader/Action Data" above).

Use `useActionData` in **deep child components**:

```typescript
import { useActionData, Form } from "react-router";

function LoginForm() {
  const actionData = useActionData<typeof import("../route").action>();

  return (
    <Form method="post">
      {actionData?.error && <div>{actionData.error}</div>}
      <input type="email" name="email" />
      <button type="submit">Login</button>
    </Form>
  );
}
```

**Note**: `actionData` is undefined until an action has been called

### useLoaderData

Access the current route's loader data. **In route modules, prefer `loaderData` from props** (see "Accessing Loader/Action Data" above).

Use `useLoaderData` in **deep child components** that don't have direct access to route props:

```typescript
import { useLoaderData } from "react-router";

// In a child component, not the route module default export
function ProductCard() {
  const { products } = useLoaderData<typeof import("../route").loader>();
  return <div>{products[0].name}</div>;
}
```

**Important**:
- `useLoaderData` assumes the loader succeeded
- Cannot be used in `ErrorBoundary` or `Layout` components — use `useRouteLoaderData` for those cases
- Never use `useLoaderData<Route.ComponentProps["loaderData"]>()` — this is incorrect

### useRouteLoaderData

Access loader data from parent or sibling routes by route ID. Essential for `ErrorBoundary` and `Layout` components where `useLoaderData` is not allowed.

**Type-safe pattern with `typeof`**:

```typescript
import { useRouteLoaderData } from "react-router";
import type { loader as rootLoader } from "./root";

export function Layout({ children }) {
  // Type-safe: infers types from root loader
  const rootData = useRouteLoaderData<typeof rootLoader>("root");

  // Always check for undefined (loader may have thrown)
  if (rootData?.user) {
    return <div>Welcome, {rootData.user.name}</div>;
  }

  return <div>Not authenticated</div>;
}
```

**Basic usage (untyped)**:

```typescript
import { useRouteLoaderData } from "react-router";

export default function ChildComponent() {
  const rootData = useRouteLoaderData("root");

  if (rootData?.user) {
    return <div>Welcome, {rootData.user.name}</div>;
  }

  return <div>Not authenticated</div>;
}
```

**When to use**:
- Accessing parent route data (e.g., user auth from root loader)
- Sharing data across route hierarchy
- In `ErrorBoundary` or `Layout` components where `useLoaderData` is not allowed

**Route IDs**: Automatically generated from file paths:
- `app/root.tsx` → `"root"`
- `app/routes/products.tsx` → `"routes/products"`
- `app/routes/products.$id.tsx` → `"routes/products.$id"`

You can also specify custom IDs in `routes.ts`:

```typescript
import { route } from "@react-router/dev/routes";

export default [
  route("/products/:id", "./product.tsx", { id: "product-detail" }),
];
```

### useMatches

Access all matched routes and their data/handles:

```typescript
import { useMatches } from "react-router";

export function Layout({ children }) {
  const matches = useMatches();

  // Access all matched routes
  matches.forEach((match) => {
    console.log(match.id);           // Route ID
    console.log(match.pathname);     // URL pathname
    console.log(match.params);       // URL params
    console.log(match.loaderData);   // Loader data (may be undefined)
    console.log(match.handle);       // Custom handle metadata
  });

  return <div>{children}</div>;
}
```

> **Note**: Use `match.loaderData` instead of `match.data`. The `data` property is deprecated.

**Common use cases**:
- Building breadcrumbs from route hierarchy
- Creating dynamic navigation based on current route
- Accessing metadata from all matched routes

**Type safety with UIMatch**:

```typescript
import { useMatches, type UIMatch } from "react-router";

const matches = useMatches();
const rootMatch = matches[0] as UIMatch<{ user: User } | undefined>;

// Guard against undefined loaderData (loader may have thrown)
if (rootMatch.loaderData?.user) {
  const { user } = rootMatch.loaderData;
}
```

### Form Component

Use React Router's `Form` for enhanced form handling:

```typescript
import { Form } from "react-router";

<Form method="post" action="/todos">
  <input name="title" />
  <button type="submit">Create</button>
</Form>

// With navigate={false} to prevent navigation after action
<Form method="post" navigate={false}>
  {/* ... */}
</Form>
```

**See [references/forms.md](references/forms.md) for form validation patterns, optimistic UI, and pending states.**

### useParams

Access route parameters in components:

```typescript
import { useParams } from "react-router";

function ProductDetail() {
  const { productId } = useParams();
  return <div>Product: {productId}</div>;
}
```

**Note**: In route modules, prefer accessing params from `Route.ComponentProps` or `Route.LoaderArgs`.

### useRevalidator

Manually trigger data revalidation:

```typescript
import { useRevalidator } from "react-router";

function RefreshButton() {
  const revalidator = useRevalidator();

  return (
    <button
      onClick={() => revalidator.revalidate()}
      disabled={revalidator.state === "loading"}
    >
      {revalidator.state === "loading" ? "Refreshing..." : "Refresh"}
    </button>
  );
}
```

**Use cases**: Polling, window focus refresh, manual refresh buttons.

### useNavigate

Programmatic navigation without user interaction:

```typescript
import { useNavigate } from "react-router";

function LogoutButton() {
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate("/login", { replace: true });
  };

  return <button onClick={handleLogout}>Logout</button>;
}
```

**See [references/navigation.md](references/navigation.md) for navigation options, Outlet, and redirect patterns.**

## URL Search Params

For filters, pagination, search, and shareable UI state.

Quick example:

```typescript
import { useSearchParams } from "react-router";

export default function ProductList() {
  const [searchParams, setSearchParams] = useSearchParams();
  const category = searchParams.get("category") || "all";

  const handleCategoryChange = (newCategory: string) => {
    setSearchParams((prev) => {
      prev.set("category", newCategory);
      prev.set("page", "1"); // Reset page when filter changes
      return prev;
    });
  };

  return (/* ... */);
}
```

In loaders:

```typescript
export async function loader({ request }: Route.LoaderArgs) {
  const url = new URL(request.url);
  const category = url.searchParams.get("category") || "all";
  const products = await db.getProducts({ category });
  return { products, category };
}
```

**See [references/search-params.md](references/search-params.md) for pagination patterns, filtering with forms, type-safe parsing, and debounced search.**

## Route Metadata with handle

Export a `handle` object to attach custom metadata to routes. This metadata is accessible via `useMatches()` in ancestor components.

### Basic handle Export

```typescript
// app/routes/products.tsx
import { Link } from "react-router";

export const handle = {
  breadcrumb: () => <Link to="/products">Products</Link>,
  title: "Products",
  icon: "📦",
};
```

### Dynamic Breadcrumbs Pattern

Use `handle` with `useMatches` to build breadcrumbs:

```typescript
// app/routes/products.$id.tsx
import type { Route } from "./+types/products.$id";

export async function loader({ params }: Route.LoaderArgs) {
  const product = await db.getProduct(params.id);
  return { product };
}

export const handle = {
  breadcrumb: (match: any) => (
    <Link to={`/products/${match.params.id}`}>
      {match.loaderData?.product?.name || "Product"}
    </Link>
  ),
};

export default function Product({ loaderData }: Route.ComponentProps) {
  return <div>{loaderData.product.name}</div>;
}
```

### Rendering Breadcrumbs in Layout

```typescript
// app/root.tsx
import { useMatches, Outlet } from "react-router";

export function Layout({ children }) {
  const matches = useMatches();

  return (
    <html>
      <body>
        <nav>
          <ol>
            {matches
              .filter((match) => match.handle?.breadcrumb)
              .map((match, index) => (
                <li key={index}>
                  {match.handle.breadcrumb(match)}
                </li>
              ))}
          </ol>
        </nav>
        {children}
      </body>
    </html>
  );
}

export default function App() {
  return <Outlet />;
}
```

**Common handle use cases**:
- Breadcrumb navigation
- Page titles and metadata
- Icons for navigation items
- Role-based access control metadata
- Analytics tracking data

## Middleware (v7.9.0+)

Middleware runs code before/after route handlers for authentication, logging, context sharing.

Quick example:

```typescript
// app/middleware/auth.ts
import { redirect, createContext } from "react-router";

export const userContext = createContext<User>();

export async function authMiddleware({ request, context }) {
  const session = await getSession(request);
  if (!session.get("userId")) throw redirect("/login");

  const user = await getUserById(session.get("userId"));
  context.set(userContext, user);
}

// app/routes/dashboard.tsx
export const middleware = [authMiddleware] satisfies Route.MiddlewareFunction[];

export async function loader({ context }: Route.LoaderArgs) {
  const user = context.get(userContext);
  return { user };
}
```

Enable with `future.v8_middleware: true` in `react-router.config.ts`.

**See [references/middleware.md](references/middleware.md) for execution order, error handling, and role-based access patterns.**

## SSR and Pre-rendering

### Configure SSR

Enable server-side rendering in `react-router.config.ts`:

```typescript
import type { Config } from "@react-router/dev/config";

export default {
  ssr: true,
} satisfies Config;
```

### Configure Pre-rendering

Generate static HTML at build time:

```typescript
import type { Config } from "@react-router/dev/config";

export default {
  ssr: true, // Can be true or false
  async prerender() {
    return ["/", "/about", "/products", "/contact"];
  },
} satisfies Config;
```

**Static-only mode** (no runtime server):

```typescript
export default {
  ssr: false,
  prerender: true, // Pre-renders all static routes
} satisfies Config;
```

## Async Streaming with Promises

Stream non-critical data while rendering critical data immediately. `defer()` is deprecated - just return promises directly.

Quick example:

```typescript
export async function loader() {
  const user = await db.getUser(); // Critical - await
  const stats = db.getStats();     // Non-critical - don't await

  return { user, stats };
}

export default function Dashboard({ loaderData }: Route.ComponentProps) {
  const { user, stats } = loaderData;

  return (
    <div>
      <h1>Welcome, {user.name}!</h1>
      <Suspense fallback={<StatsSkeleton />}>
        <Await resolve={stats}>
          {(resolvedStats) => <StatsCard data={resolvedStats} />}
        </Await>
      </Suspense>
    </div>
  );
}
```

> **Important**: Promises must be wrapped in an object (`return { reviews }` not `return reviews`).

**See [references/streaming.md](references/streaming.md) for error handling, useAsyncValue patterns, and when to use streaming.**

## Common Patterns

### Loading States with HydrateFallback

Show loading UI during initial hydration when `clientLoader.hydrate = true`:

```typescript
export async function clientLoader({ serverLoader }: Route.ClientLoaderArgs) {
  const data = await serverLoader();
  return data;
}
clientLoader.hydrate = true as const;

export function HydrateFallback() {
  return <div>Loading...</div>;
}

export default function Component({ loaderData }: Route.ComponentProps) {
  return <div>{loaderData.content}</div>;
}
```

**Important**: `HydrateFallback` cannot render `<Outlet />` as child routes may not be ready.

### Error Handling

Use error boundaries for loader/action errors:

```typescript
import { isRouteErrorResponse, useRouteError } from "react-router";

export function ErrorBoundary() {
  const error = useRouteError();

  if (isRouteErrorResponse(error)) {
    return (
      <div>
        <h1>{error.status} {error.statusText}</h1>
        <p>{error.data}</p>
      </div>
    );
  }

  return <div>Something went wrong!</div>;
}
```

### Pending UI with useNavigation

Show pending states during navigation:

```typescript
import { useNavigation } from "react-router";

export default function Products({ loaderData }: Route.ComponentProps) {
  const navigation = useNavigation();
  const isLoading = navigation.state === "loading";

  return (
    <div className={isLoading ? "opacity-50" : ""}>
      {loaderData.products.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}
```

## Resource Routes (API Endpoints)

Resource routes serve non-UI responses (JSON, PDF, webhooks). A route is a resource route when it exports `loader`/`action` but **no default component**:

```typescript
// app/routes/api.users.tsx
export async function loader() {
  const users = await db.getUsers();
  return Response.json(users);
}

export async function action({ request }: Route.ActionArgs) {
  const data = await request.json();
  const user = await db.createUser(data);
  return Response.json(user, { status: 201 });
}
// No default export = resource route
```

Link with `reloadDocument` to prevent client-side routing:

```typescript
<Link reloadDocument to="/api/report.pdf">Download PDF</Link>
```

**See [references/resource-routes.md](references/resource-routes.md) for HTTP method handling, file serving, and webhook patterns.**

## Decision Tree

```
Do you need to access client-only APIs (localStorage, browser state)?
├─ YES → Use clientLoader (no server loader)
└─ NO  → Continue

Do you need to combine server and client data?
├─ YES → Use loader + clientLoader with hydrate = true
└─ NO  → Continue

Do you want to cache data on the client?
├─ YES → Use loader + clientLoader with caching logic + hydrate = true
└─ NO  → Continue

Do you want to skip server on subsequent navigations?
├─ YES → Use loader + clientLoader (BFF pattern, no hydrate)
└─ NO  → Continue

Do you have slow/non-critical data that blocks rendering?
├─ YES → Return promises without awaiting - wrap with Suspense/Await in component
└─ NO  → Use server-only loader (PREFERRED)
```

## Checklist

Before completing any React Router 7 implementation:

- [ ] All route modules use `Route.*` types from `./+types/<route>`
- [ ] Data fetching prioritizes server-side loaders
- [ ] `clientLoader.hydrate = true as const` is set correctly when needed
- [ ] `HydrateFallback` is exported when `clientLoader.hydrate = true`
- [ ] Actions use server-side mutations with automatic revalidation
- [ ] Forms use `<Form>` component from react-router, not native `<form>`
- [ ] Type-safe `href()` utility is used for route generation
- [ ] Error boundaries are implemented for route errors
- [ ] Loading states use `useNavigation` or fetcher states
- [ ] No client-side data fetching unless absolutely necessary
- [ ] Slow/non-critical data returned as promises (not awaited) for streaming
- [ ] Critical data is awaited, non-critical data is streamed
- [ ] `<Await>` wrapped in `<Suspense>` with fallback UI
- [ ] Error handling implemented for streaming promises (`errorElement` or `useAsyncError`)
- [ ] Search params used for shareable UI state (filters, pagination, search)
- [ ] Search params validated and parsed in loaders with proper defaults
- [ ] Search param values returned from loader and used as `defaultValue` in forms
- [ ] `<Form method="get">` used for filter forms (not POST)
- [ ] Use `useRouteLoaderData` instead of `useLoaderData` in ErrorBoundary/Layout components
- [ ] Parent route data accessed via `useRouteLoaderData("route-id")` with proper undefined checks
- [ ] `handle` exports used for route metadata (breadcrumbs, titles, etc.)
- [ ] Middleware used for authentication/authorization instead of loader-only patterns
- [ ] Context API (`context.set/get`) used for sharing data between middleware and loaders
- [ ] `data()` utility used for custom status codes (404, 201, etc.)
- [ ] Route IDs understood for `useRouteLoaderData` calls
- [ ] `meta`, `links`, `headers` exports used where appropriate
- [ ] `shouldRevalidate` considered for performance-critical loaders
- [ ] Server-only code uses `.server.ts` naming convention
- [ ] Secrets and database clients never imported in client-accessible modules
- [ ] Routes configured in `routes.ts` with appropriate helpers (`route`, `index`, `layout`, `prefix`)
- [ ] Resource routes (API endpoints) export no default component
- [ ] Form validation returns errors with `data({ errors }, { status: 400 })`
- [ ] Optimistic UI uses `fetcher.formData` for immediate feedback

## Bundled References

- [routes-config.md](references/routes-config.md) - Route configuration, helpers, Outlet, splats
- [navigation.md](references/navigation.md) - Redirects, useNavigate, Outlet context
- [forms.md](references/forms.md) - Validation, optimistic UI, pending states
- [resource-routes.md](references/resource-routes.md) - API endpoints, webhooks, file serving
- [middleware.md](references/middleware.md) - Authentication, context API, execution order
- [search-params.md](references/search-params.md) - Pagination, filtering, type-safe parsing
- [streaming.md](references/streaming.md) - Suspense, Await, deferred data

## External References

- [React Router Documentation](https://reactrouter.com/)
- [Routing Guide](https://reactrouter.com/start/framework/routing)
- [Type Safety Guide](https://reactrouter.com/explanation/type-safety)
- [Data Loading](https://reactrouter.com/start/framework/data-loading)
- [Actions](https://reactrouter.com/start/framework/actions)
- [Form Validation](https://reactrouter.com/how-to/form-validation)
- [Resource Routes](https://reactrouter.com/how-to/resource-routes)
- [Client Data Patterns](https://reactrouter.com/how-to/client-data)
- [Streaming & Suspense](https://reactrouter.com/how-to/suspense)
- [Middleware Guide](https://reactrouter.com/how-to/middleware)
- [Using handle](https://reactrouter.com/how-to/using-handle)
- [Pending UI](https://reactrouter.com/start/framework/pending-ui)

## Key Notes

- Always prefer server-side data loading over client-side
- In route modules, **use props** (`Route.ComponentProps`) — hooks are for deep child components
- Never use `useLoaderData<Route.ComponentProps["loaderData"]>()` — this is incorrect
- Use `as const` when setting `clientLoader.hydrate = true`
- `HydrateFallback` is required when `clientLoader.hydrate = true`
- Return promises without awaiting to stream slow/non-critical data
- Always wrap `<Await>` in `<Suspense>` with fallback UI
- `useLoaderData` cannot be used in `ErrorBoundary` or `Layout` — use `useRouteLoaderData`
- Use `.server.ts` naming for modules containing secrets or database clients
- Middleware requires `future.v8_middleware: true` flag (v7.9.0+)
