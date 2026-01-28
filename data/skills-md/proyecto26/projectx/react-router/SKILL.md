---
name: react-router
description: React Router v7 full-stack development. Use when working with routes, loaders, actions, SSR, or the web app in apps/web.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# React Router v7 Development

## Project Structure

The frontend app is in `apps/web/` using React Router v7 with SSR.

```
apps/web/
├── app/
│   ├── routes/           # File-based routing
│   ├── components/       # Shared components
│   ├── lib/              # Utilities and helpers
│   ├── root.tsx          # Root layout
│   └── entry.server.tsx  # Server entry
├── react-router.config.ts
└── vite.config.ts
```

## File-Based Routing

Routes are defined by file structure in `app/routes/`:

| File | Route |
|------|-------|
| `_index.tsx` | `/` |
| `about.tsx` | `/about` |
| `products.tsx` | `/products` |
| `products.$id.tsx` | `/products/:id` |
| `products._index.tsx` | `/products` (index) |
| `auth.login.tsx` | `/auth/login` |
| `$.tsx` | Catch-all (404) |

### Layout Routes

```
routes/
├── products.tsx          # Layout for /products/*
├── products._index.tsx   # /products
└── products.$id.tsx      # /products/:id
```

## Route Module Pattern

### Basic Route with Loader

```tsx
// app/routes/products.$id.tsx
import type { Route } from "./+types/products.$id";
import { useLoaderData } from "react-router";

export async function loader({ params }: Route.LoaderArgs) {
  const product = await fetchProduct(params.id);
  if (!product) {
    throw new Response("Not Found", { status: 404 });
  }
  return { product };
}

export function meta({ data }: Route.MetaArgs) {
  return [
    { title: data?.product.name ?? "Product" },
    { name: "description", content: data?.product.description },
  ];
}

export default function ProductPage({ loaderData }: Route.ComponentProps) {
  const { product } = loaderData;

  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <span>${product.price}</span>
    </div>
  );
}
```

### Route with Action (Form Handling)

```tsx
// app/routes/products.new.tsx
import type { Route } from "./+types/products.new";
import { Form, redirect, useActionData } from "react-router";

export async function action({ request }: Route.ActionArgs) {
  const formData = await request.formData();
  const name = formData.get("name") as string;
  const price = parseFloat(formData.get("price") as string);

  const errors: Record<string, string> = {};
  if (!name) errors.name = "Name is required";
  if (isNaN(price)) errors.price = "Valid price is required";

  if (Object.keys(errors).length) {
    return { errors };
  }

  const product = await createProduct({ name, price });
  return redirect(`/products/${product.id}`);
}

export default function NewProduct({ actionData }: Route.ComponentProps) {
  const errors = actionData?.errors;

  return (
    <Form method="post">
      <div>
        <label htmlFor="name">Name</label>
        <input type="text" name="name" id="name" />
        {errors?.name && <span className="error">{errors.name}</span>}
      </div>
      <div>
        <label htmlFor="price">Price</label>
        <input type="number" name="price" id="price" step="0.01" />
        {errors?.price && <span className="error">{errors.price}</span>}
      </div>
      <button type="submit">Create Product</button>
    </Form>
  );
}
```

## Data Fetching with TanStack Query

For client-side data fetching alongside loaders:

```tsx
import { useQuery } from "@tanstack/react-query";

export default function Dashboard() {
  const { data: stats, isLoading } = useQuery({
    queryKey: ["dashboard-stats"],
    queryFn: () => fetch("/api/stats").then((r) => r.json()),
    staleTime: 60_000, // 1 minute
  });

  if (isLoading) return <Skeleton />;

  return <StatsDisplay stats={stats} />;
}
```

## Component Library Integration

Use components from `@projectx/ui`:

```tsx
import { Button, Card, Input } from "@projectx/ui";

export default function ProductForm() {
  return (
    <Card>
      <form>
        <Input label="Product Name" name="name" required />
        <Button type="submit">Save</Button>
      </form>
    </Card>
  );
}
```

## Styling with Tailwind CSS v4

```tsx
export default function ProductCard({ product }: { product: Product }) {
  return (
    <div className="rounded-lg border border-gray-200 p-4 shadow-sm hover:shadow-md transition-shadow">
      <h3 className="text-lg font-semibold text-gray-900">{product.name}</h3>
      <p className="mt-2 text-gray-600">{product.description}</p>
      <span className="mt-4 block text-xl font-bold text-primary">
        ${product.price}
      </span>
    </div>
  );
}
```

## Error Handling

```tsx
// app/routes/products.$id.tsx
import { isRouteErrorResponse, useRouteError } from "react-router";

export function ErrorBoundary() {
  const error = useRouteError();

  if (isRouteErrorResponse(error)) {
    return (
      <div className="error-container">
        <h1>{error.status} {error.statusText}</h1>
        <p>{error.data}</p>
      </div>
    );
  }

  return (
    <div className="error-container">
      <h1>Something went wrong</h1>
      <p>{error instanceof Error ? error.message : "Unknown error"}</p>
    </div>
  );
}
```

## Navigation

```tsx
import { Link, NavLink, useNavigate } from "react-router";

function Navigation() {
  const navigate = useNavigate();

  return (
    <nav>
      {/* Basic link */}
      <Link to="/products">Products</Link>

      {/* Active state styling */}
      <NavLink
        to="/products"
        className={({ isActive }) =>
          isActive ? "text-primary font-bold" : "text-gray-600"
        }
      >
        Products
      </NavLink>

      {/* Programmatic navigation */}
      <button onClick={() => navigate("/checkout")}>
        Go to Checkout
      </button>
    </nav>
  );
}
```

## Running the Frontend

```bash
# Development with HMR
pnpm dev:web

# Build for production
pnpm build:web

# Type checking
pnpm --filter web typecheck
```

## Best Practices

1. **Use loaders** for server-side data fetching
2. **Use actions** for form submissions and mutations
3. **Handle errors** with ErrorBoundary components
4. **Type routes** using the generated `+types` files
5. **Co-locate** route-specific components with routes
6. **Use TanStack Query** for client-side caching when needed
7. **Leverage SSR** for SEO-critical pages
