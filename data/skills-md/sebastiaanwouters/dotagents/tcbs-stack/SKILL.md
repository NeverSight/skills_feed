---
name: tcbs-stack
description: Builds full-stack apps with TanStack Start, Convex backend, Better-Auth authentication, and Shadcn UI. Use when creating React apps with real-time database, auth, or this specific stack.
---

# TCBS Stack

Build production-ready full-stack TypeScript applications with TanStack Start + Convex + Better-Auth + Shadcn UI.

## Stack Overview

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | TanStack Start | Full-stack React framework with SSR |
| **Backend** | Convex | Real-time database & serverless functions |
| **Auth** | Better-Auth | Flexible authentication with Convex adapter |
| **UI** | Shadcn UI | Accessible component library |

## Quick Start

```bash
# Create new TanStack Start project with Shadcn (recommended)
bun create @tanstack/start@latest --tailwind --add-ons shadcn
cd my-app

# Add Convex (requires v1.25.0+)
bun add convex@latest @convex-dev/react-query
bunx convex dev --once

# Add Better-Auth with Convex
bun add better-auth @convex-dev/better-auth
```

**Alternative manual setup:**
```bash
bun create @tanstack/start@latest
bun add tailwindcss @tailwindcss/vite
bunx shadcn@latest init
```

## Project Structure

```
project/
├── src/
│   ├── lib/
│   │   ├── auth-client.tsx      # Client auth setup
│   │   ├── auth-server.ts       # Server auth handler
│   │   └── utils.ts             # cn() helper
│   ├── routes/
│   │   ├── __root.tsx           # Root layout + providers
│   │   ├── _authed.tsx          # Protected route guard
│   │   ├── _authed/
│   │   │   └── index.tsx        # Dashboard
│   │   ├── sign-in.tsx
│   │   └── sign-up.tsx
│   ├── components/
│   │   └── ui/                  # Shadcn components
│   └── router.tsx
├── convex/
│   ├── auth.ts                  # Better-Auth instance
│   ├── auth.config.ts           # Auth providers config
│   ├── http.ts                  # HTTP routes
│   ├── schema.ts                # Database schema
│   └── convex.config.ts         # App config
├── components.json              # Shadcn config
└── vite.config.ts
```

## Core Setup Files

### 1. Convex Configuration

**convex/convex.config.ts**
```typescript
import { defineApp } from "convex/server";
import betterAuth from "@convex-dev/better-auth/convex.config";

const app = defineApp();
app.use(betterAuth);
export default app;
```

**convex/auth.config.ts**
```typescript
import { getAuthConfigProvider } from "@convex-dev/better-auth/auth-config";
import { AuthConfig } from "@auth/core";

export default {
  providers: [getAuthConfigProvider()],
} satisfies AuthConfig;
```

**convex/auth.ts**
```typescript
import { createClient, GenericCtx } from "@convex-dev/better-auth";
import { convex } from "@convex-dev/better-auth/plugins";
import { betterAuth } from "better-auth";
import { DataModel } from "./_generated/dataModel";
import { components, internal } from "./_generated/api";
import authConfig from "./auth.config";

const siteUrl = process.env.SITE_URL!;

export const authComponent = createClient<DataModel>(components.betterAuth, {
  authFunctions: internal.auth,
  triggers: {
    user: {
      onCreate: async (ctx, authUser) => {
        // Sync to your users table
        const userId = await ctx.db.insert("users", { email: authUser.email });
        await authComponent.setUserId(ctx, authUser._id, userId);
      },
    },
  },
});

export const createAuth = (ctx: GenericCtx<DataModel>) => {
  return betterAuth({
    baseURL: siteUrl,
    database: authComponent.adapter(ctx),
    emailAndPassword: { enabled: true },
    plugins: [convex({ authConfig })],
  });
};

// Auth helpers for queries/mutations
export const { getUser, safeGetUser } = authComponent.authHelpers(createAuth);
```

**convex/http.ts**
```typescript
import { httpRouter } from "convex/server";
import { authComponent, createAuth } from "./auth";

const http = httpRouter();
authComponent.registerRoutes(http, createAuth);
export default http;
```

**convex/schema.ts**
```typescript
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  users: defineTable({
    email: v.string(),
    authId: v.optional(v.string()),
  }).index("email", ["email"]),
});
```

### 2. Client Auth Setup

**src/lib/auth-client.tsx**
```typescript
import { createAuthClient } from "better-auth/react";
import { convexClient } from "@convex-dev/better-auth/client/plugins";

export const authClient = createAuthClient({
  plugins: [convexClient()],
});

export const { signIn, signUp, signOut, useSession } = authClient;
```

### 3. Server Auth Setup

**src/lib/auth-server.ts**
```typescript
import { convexBetterAuthReactStart } from "@convex-dev/better-auth/react-start";

export const {
  handler,
  getToken,
  fetchAuthQuery,
  fetchAuthMutation,
  fetchAuthAction,
} = convexBetterAuthReactStart({
  convexUrl: process.env.VITE_CONVEX_URL!,
  convexSiteUrl: process.env.VITE_CONVEX_SITE_URL!,
});
```

### 3b. Mount Auth Route Handler

**src/routes/api/auth/$.ts**
```typescript
import { handler } from "~/lib/auth-server";

export const { GET, POST } = handler;
```

### 4. Root Route with Providers

**src/routes/__root.tsx**
```typescript
import { createRootRouteWithContext, Outlet } from "@tanstack/react-router";
import { createServerFn } from "@tanstack/react-start";
import { ConvexBetterAuthProvider } from "@convex-dev/better-auth/react";
import { QueryClient } from "@tanstack/react-query";
import { ConvexQueryClient } from "@convex-dev/react-query";
import { getToken } from "~/lib/auth-server";
import { authClient } from "~/lib/auth-client";

const getAuth = createServerFn({ method: "GET" }).handler(async () => {
  return await getToken();
});

export const Route = createRootRouteWithContext<{
  queryClient: QueryClient;
  convexQueryClient: ConvexQueryClient;
}>()({
  beforeLoad: async (ctx) => {
    const token = await getAuth();
    if (token) {
      ctx.context.convexQueryClient.serverHttpClient?.setAuth(token);
    }
    return { isAuthenticated: !!token, token };
  },
  component: RootComponent,
});

function RootComponent() {
  const { convexQueryClient, token } = Route.useRouteContext();
  return (
    <ConvexBetterAuthProvider
      client={convexQueryClient.convexClient}
      authClient={authClient}
      initialToken={token}
    >
      <Outlet />
    </ConvexBetterAuthProvider>
  );
}
```

### 5. Protected Route Guard

**src/routes/_authed.tsx**
```typescript
import { createFileRoute, Outlet, redirect } from "@tanstack/react-router";

export const Route = createFileRoute("/_authed")({
  beforeLoad: ({ context }) => {
    if (!context.isAuthenticated) {
      throw redirect({ to: "/sign-in" });
    }
  },
  component: () => <Outlet />,
});
```

### 6. Vite Configuration

**vite.config.ts**
```typescript
import { defineConfig } from "vite";
import { tanstackStart } from "@tanstack/react-start/plugin/vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import path from "path";

export default defineConfig({
  plugins: [tanstackStart(), react(), tailwindcss()],
  resolve: {
    alias: { "@": path.resolve(__dirname, "./src") },
  },
  ssr: {
    // Required: Bundle @convex-dev/better-auth during SSR
    noExternal: ["@convex-dev/better-auth"],
  },
});
```

### 7. Router Configuration

**src/router.tsx**
```typescript
import { createRouter } from "@tanstack/react-router";
import { routeTree } from "./routeTree.gen";
import { QueryClient } from "@tanstack/react-query";
import { ConvexQueryClient } from "@convex-dev/react-query";
import { ConvexReactClient } from "convex/react";

const convex = new ConvexReactClient(import.meta.env.VITE_CONVEX_URL);

export function createAppRouter() {
  const queryClient = new QueryClient();
  const convexQueryClient = new ConvexQueryClient(convex, { expectAuth: true });
  queryClient.setDefaultOptions({
    queries: { queryKeyHashFn: convexQueryClient.hashFn() },
  });
  convexQueryClient.connect(queryClient);

  return createRouter({
    routeTree,
    context: { queryClient, convexQueryClient },
    defaultPreload: "intent",
  });
}
```

## Environment Variables

**.env.local**
```bash
# Convex deployment (set by `npx convex dev`)
CONVEX_DEPLOYMENT=dev:your-deployment
VITE_CONVEX_URL=https://your-deployment.convex.cloud
VITE_CONVEX_SITE_URL=https://your-deployment.convex.site

# App URL
VITE_SITE_URL=http://localhost:3000
```

**Convex environment variables** (set via CLI):
```bash
# Generate and set secret
npx convex env set BETTER_AUTH_SECRET=$(openssl rand -base64 32)

# Set site URL
npx convex env set SITE_URL http://localhost:3000

# OAuth (optional)
npx convex env set GITHUB_CLIENT_ID your-id
npx convex env set GITHUB_CLIENT_SECRET your-secret
```

## Common Patterns

### Protected Queries

```typescript
// convex/todos.ts
import { query, mutation } from "./_generated/server";
import { v } from "convex/values";
import { getUser, safeGetUser } from "./auth";

export const get = query({
  handler: async (ctx) => {
    const user = await safeGetUser(ctx);
    if (!user) return [];
    return ctx.db.query("todos").withIndex("userId", (q) => q.eq("userId", user._id)).collect();
  },
});

export const create = mutation({
  args: { text: v.string() },
  handler: async (ctx, args) => {
    const user = await getUser(ctx); // Throws if unauthenticated
    await ctx.db.insert("todos", { text: args.text, userId: user._id, completed: false });
  },
});
```

### Sign In Component

```typescript
import { authClient } from "~/lib/auth-client";
import { Button } from "~/components/ui/button";
import { Input } from "~/components/ui/input";

export function SignIn() {
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = new FormData(e.currentTarget);
    await authClient.signIn.email({
      email: form.get("email") as string,
      password: form.get("password") as string,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input name="email" type="email" placeholder="Email" required />
      <Input name="password" type="password" placeholder="Password" required />
      <Button type="submit">Sign In</Button>
      <Button type="button" variant="outline" onClick={() => authClient.signIn.social({ provider: "github" })}>
        Sign in with GitHub
      </Button>
    </form>
  );
}
```

### Optimistic Updates

```typescript
import { useMutation } from "@convex-dev/react-query";
import { api } from "convex/_generated/api";

const createTodo = useMutation(api.todos.create).withOptimisticUpdate(
  (localStore, args) => {
    const todos = localStore.getQuery(api.todos.get);
    if (!todos) return;
    localStore.setQuery(api.todos.get, {}, [
      { _id: crypto.randomUUID(), text: args.text, completed: false },
      ...todos,
    ]);
  }
);
```

## Auth Methods

Better-Auth supports multiple authentication methods:

```typescript
// Email/Password
authClient.signIn.email({ email, password });
authClient.signUp.email({ email, password, name });

// OAuth
authClient.signIn.social({ provider: "github" });
authClient.signIn.social({ provider: "google" });

// Magic Link
authClient.signIn.magicLink({ email });

// Sign Out
authClient.signOut();

// Session
const { data: session } = authClient.useSession();
```

## Commands

```bash
# Development
bun dev               # Start frontend
bunx convex dev       # Start Convex (separate terminal)

# Add Shadcn components
bunx shadcn@latest add button input card form dialog

# Add all Shadcn components
bunx shadcn@latest add --all

# Build & Deploy
bun run build
bunx convex deploy
```

## SSR with TanStack Query

Use `ensureQueryData` and `useSuspenseQuery` for SSR:

```typescript
// src/routes/_authed/index.tsx
import { createFileRoute } from "@tanstack/react-router";
import { convexQuery } from "@convex-dev/react-query";
import { useSuspenseQuery } from "@tanstack/react-query";
import { api } from "convex/_generated/api";

export const Route = createFileRoute("/_authed/")({
  loader: async ({ context }) => {
    await context.queryClient.ensureQueryData(convexQuery(api.todos.get, {}));
  },
  component: Dashboard,
});

function Dashboard() {
  const { data: todos } = useSuspenseQuery(convexQuery(api.todos.get, {}));
  return <TodoList todos={todos} />;
}
```

## Sign Out (with expectAuth: true)

When using `expectAuth: true`, reload the page on sign out:

```typescript
import { authClient } from "~/lib/auth-client";

function SignOutButton() {
  const handleSignOut = async () => {
    await authClient.signOut();
    window.location.reload(); // Required with expectAuth: true
  };
  return <Button onClick={handleSignOut}>Sign Out</Button>;
}
```

## TanStack Server Functions vs Convex: When to Use What

| Use Case | Use This | Why |
|----------|----------|-----|
| Database CRUD | **Convex query/mutation** | Transactional, real-time |
| Real-time data | **Convex query** | Auto subscriptions |
| Third-party APIs | **Convex action** | Runs close to data |
| Auth handlers | **TanStack server route** | HTTP cookies/redirects |
| SSR preloading | **TanStack loader** | Pre-fetch for SSR |
| Webhooks | **TanStack server route** | HTTP endpoints |

**Core principle:** Convex = database & business logic. TanStack Start = HTTP & rendering.

See `reference/server-functions-vs-convex.md` for detailed guidelines.

## Key Integration Points

| Integration | Key File | Purpose |
|-------------|----------|---------|
| Auth Client | `src/lib/auth-client.tsx` | Client-side auth methods |
| Auth Server | `src/lib/auth-server.ts` | SSR token handling |
| Root Provider | `src/routes/__root.tsx` | Auth context + Convex client |
| Route Guard | `src/routes/_authed.tsx` | Redirect unauthenticated users |
| Backend Auth | `convex/auth.ts` | Better-Auth instance |
| HTTP Routes | `convex/http.ts` | Auth endpoint registration |
| Database | `convex/schema.ts` | Type-safe schema |
