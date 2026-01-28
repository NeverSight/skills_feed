---
name: deno-frontend
description: Use when building web UIs with Fresh framework, using Preact components, or adding Tailwind CSS styling in Deno
---

# Deno Frontend Development

## Overview

This skill covers frontend development in Deno using Fresh (Deno's web framework), Preact (a lightweight React alternative), and Tailwind CSS. Fresh uses "island architecture" where pages render on the server and only interactive parts ship JavaScript to the browser.

## When to Use This Skill

- Creating a new Fresh web application
- Building interactive UI components (islands)
- Adding server-rendered pages and routes
- Integrating Tailwind CSS for styling
- Choosing between islands (client-side) vs components (server-only)
- Working with Preact hooks and signals

Apply these practices when building web applications in Deno.

## Fresh Framework

Reference: https://fresh.deno.dev/docs

Fresh is Deno's web framework. It uses **island architecture** - pages are rendered on the server, and only interactive parts ("islands") get JavaScript on the client.

### Creating a Fresh Project

```bash
deno run -Ar jsr:@fresh/init
cd my-project
deno task dev    # Runs at http://127.0.0.1:5173/
```

### Project Structure

```
my-project/
├── deno.json           # Config and dependencies
├── main.ts             # Entry point
├── fresh.gen.ts        # Auto-generated manifest (don't edit)
├── routes/             # Pages and API routes
│   ├── _app.tsx        # App layout wrapper
│   ├── index.tsx       # Home page (/)
│   └── api/            # API routes
├── islands/            # Interactive components (hydrated on client)
│   └── Counter.tsx
├── components/         # Server-only components (no JS shipped)
│   └── Button.tsx
└── static/             # Static assets
```

### Key Concepts

**Routes (`routes/` folder)**
- File-based routing: `routes/about.tsx` → `/about`
- Dynamic routes: `routes/blog/[slug].tsx` → `/blog/my-post`
- API routes: `routes/api/users.ts` exports handlers

**Layouts (`_app.tsx`)**
```tsx
import { PageProps } from "jsr:@fresh/core";

export default function App({ Component }: PageProps) {
  return (
    <html>
      <head>
        <title>My App</title>
      </head>
      <body>
        <Component />
      </body>
    </html>
  );
}
```

**Async Server Components**
```tsx
export default async function Page() {
  const data = await fetchData(); // Runs on server only
  return <div>{data.title}</div>;
}
```

## Islands (Interactive Components)

Islands are components that get hydrated (made interactive) on the client. Place them in the `islands/` folder.

### When to Use Islands

- User interactions (clicks, form inputs)
- Client-side state (counters, toggles)
- Browser APIs (localStorage, geolocation)

### Island Example

```tsx
// islands/Counter.tsx
import { useSignal } from "@preact/signals";

export default function Counter() {
  const count = useSignal(0);

  return (
    <div>
      <p>Count: {count.value}</p>
      <button onClick={() => count.value++}>
        Increment
      </button>
    </div>
  );
}
```

### Island Rules

1. **Props must be serializable** - No functions, only JSON-compatible data
2. **Keep islands small** - Less JavaScript shipped to client
3. **Prefer server components** - Only use islands when you need interactivity

## Preact

Preact is a 3KB alternative to React. Fresh uses Preact instead of React.

### Preact vs React Differences

| Preact | React |
|--------|-------|
| `class` works | `className` required |
| `@preact/signals` | `useState` |
| 3KB bundle | ~40KB bundle |

### Hooks (Same as React)

```tsx
import { useState, useEffect, useRef } from "preact/hooks";

function MyComponent() {
  const [value, setValue] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    console.log("Component mounted");
  }, []);

  return <input ref={inputRef} value={value} />;
}
```

### Signals (Preact's Reactive State)

Signals are Preact's more efficient alternative to useState:

```tsx
import { signal, computed } from "@preact/signals";

const count = signal(0);
const doubled = computed(() => count.value * 2);

function Counter() {
  return (
    <div>
      <p>Count: {count}</p>
      <p>Doubled: {doubled}</p>
      <button onClick={() => count.value++}>+1</button>
    </div>
  );
}
```

Benefits of signals:
- More granular updates (only re-renders what changed)
- Can be defined outside components
- Cleaner code for shared state

## Tailwind CSS in Fresh

Fresh 2.0 uses Vite for builds, which means Tailwind integrates via the Vite plugin.

### Setup

In `deno.json`:
```json
{
  "imports": {
    "@tailwindcss/vite": "npm:@tailwindcss/vite"
  }
}
```

In `vite.config.ts`:
```typescript
import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [tailwindcss()],
});
```

### Usage

```tsx
export default function Button({ children }) {
  return (
    <button class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
      {children}
    </button>
  );
}
```

### Best Practices

1. **Prefer utility classes** over `@apply`
2. **Use `class` not `className`** (Preact supports both, but `class` is simpler)
3. **Dark mode**: Use `class` strategy in tailwind.config.js

```tsx
<div class="bg-white dark:bg-gray-900">
  <p class="text-gray-900 dark:text-white">Hello</p>
</div>
```

## Building and Deploying

### Development

```bash
deno task dev      # Start dev server with hot reload (http://127.0.0.1:5173/)
```

### Production Build

```bash
deno task build    # Build for production
deno task preview  # Preview production build locally
```

### Deploy to Deno Deploy

```bash
deno task build           # Build first
deno deploy --prod        # Deploy to production
```

## Quick Reference

| Task | Command/Pattern |
|------|-----------------|
| Create Fresh project | `deno run -Ar jsr:@fresh/init` |
| Start dev server | `deno task dev` (port 5173) |
| Build for production | `deno task build` |
| Add a page | Create `routes/pagename.tsx` |
| Add an API route | Create `routes/api/endpoint.ts` |
| Add interactive component | Create `islands/ComponentName.tsx` |
| Add static component | Create `components/ComponentName.tsx` |

## Common Mistakes

**Putting too much JavaScript in islands**
```tsx
// ❌ Wrong - entire page as an island (ships all JS to client)
// islands/HomePage.tsx
export default function HomePage() {
  return (
    <div>
      <Header />
      <MainContent />  {/* Most of this doesn't need interactivity */}
      <Footer />
    </div>
  );
}

// ✅ Correct - only interactive parts are islands
// routes/index.tsx (server component)
import Counter from "../islands/Counter.tsx";

export default function HomePage() {
  return (
    <div>
      <Header />
      <MainContent />
      <Counter />  {/* Only this needs to be an island */}
      <Footer />
    </div>
  );
}
```

**Passing non-serializable props to islands**
```tsx
// ❌ Wrong - functions can't be serialized
<Counter onUpdate={(val) => console.log(val)} />

// ✅ Correct - only pass JSON-serializable data
<Counter initialValue={5} label="Click count" />
```

**Using `className` instead of `class`**
```tsx
// ❌ Works but unnecessary in Preact
<div className="container">

// ✅ Preact supports native HTML attribute
<div class="container">
```

**Forgetting to build before deploying Fresh 2.0**
```bash
# ❌ Wrong - Fresh 2.0 requires a build step
deno deploy --prod

# ✅ Correct - build first, then deploy
deno task build
deno deploy --prod
```

**Creating islands for non-interactive content**
```tsx
// ❌ Wrong - this doesn't need to be an island (no interactivity)
// islands/StaticCard.tsx
export default function StaticCard({ title, body }) {
  return <div class="card"><h2>{title}</h2><p>{body}</p></div>;
}

// ✅ Correct - use a regular component (no JS shipped)
// components/StaticCard.tsx
export default function StaticCard({ title, body }) {
  return <div class="card"><h2>{title}</h2><p>{body}</p></div>;
}
```
