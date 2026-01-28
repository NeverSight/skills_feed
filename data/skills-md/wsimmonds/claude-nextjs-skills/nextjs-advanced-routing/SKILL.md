---
name: nextjs-advanced-routing
description: Guide for advanced Next.js App Router patterns including Route Handlers, Parallel Routes, Intercepting Routes, Server Actions, error boundaries, draft mode, and streaming with Suspense. CRITICAL for server actions (action.ts, actions.ts files, 'use server' directive), setting cookies from client components, and form handling. Use when requirements involve server actions, form submissions, cookies, mutations, API routes, `route.ts`, parallel routes, intercepting routes, or streaming. Essential for separating server actions from client components.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Next.js Advanced Routing

## Overview

Provide comprehensive guidance for advanced Next.js App Router features including Route Handlers (API routes), Parallel Routes, Intercepting Routes, Server Actions, error handling, draft mode, and streaming with Suspense.

## TypeScript: NEVER Use `any` Type

**CRITICAL RULE:** This codebase has `@typescript-eslint/no-explicit-any` enabled. Using `any` will cause build failures.

**❌ WRONG:**
```typescript
function handleSubmit(e: any) { ... }
const data: any[] = [];
```

**✅ CORRECT:**
```typescript
function handleSubmit(e: React.FormEvent<HTMLFormElement>) { ... }
const data: string[] = [];
```

### Common Next.js Type Patterns

```typescript
// Page props
function Page({ params }: { params: { slug: string } }) { ... }
function Page({ searchParams }: { searchParams: { [key: string]: string | string[] | undefined } }) { ... }

// Form events
const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => { ... }
const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => { ... }

// Server actions
async function myAction(formData: FormData) { ... }
```

## When to Use This Skill

Use this skill when:
- Creating API endpoints with Route Handlers
- Implementing parallel or intercepting routes
- Building forms with Server Actions
- Setting cookies or handling mutations
- Creating error boundaries
- Implementing draft mode for CMS previews
- Setting up streaming and Suspense boundaries
- Building complex routing patterns (modals, drawers)

## ⚠️ CRITICAL: Server Action File Naming and Location

When work requirements mention a specific filename, follow that instruction exactly. If no name is given, pick the option that best matches the project conventions—`app/actions.ts` is a safe default for collections of actions, while `app/action.ts` works for a single form handler.

### Choosing between `action.ts` and `actions.ts`

- **Match existing patterns:** Check whether the project already has an actions file and extend it if appropriate.
- **Single vs multiple exports:** Prefer `action.ts` for a single action, and `actions.ts` for a group of related actions.
- **Explicit requirement:** If stakeholders call out a specific name, do not change it.

**Location guidelines**
- Server actions belong under the `app/` directory so they can participate in the App Router tree.
- Keep the file alongside the UI that invokes it unless shared across multiple routes.
- Avoid placing actions in `lib/` or `utils/` unless they are triggered from multiple distant routes and remain server-only utilities.

**Example placement**
```
app/
├── actions.ts       ← Shared actions that support multiple routes
└── dashboard/
    └── action.ts    ← Route-specific action colocated with a single page
```

### Example: Creating action.ts

```typescript
// app/action.ts (single-action example)
'use server';

export async function submitForm(formData: FormData) {
  const name = formData.get('name') as string;
  // Process the form
  console.log('Submitted:', name);
}
```

### Example: Creating actions.ts

```typescript
// app/actions.ts (multiple related actions)
'use server';

export async function createPost(formData: FormData) {
  // ...
}

export async function deletePost(id: string) {
  // ...
}
```

**Remember:** When a project requirement spells out an exact filename, mirror it precisely.

## ⚠️ CRITICAL: Server Actions Return Types - Form Actions MUST Return Void

**This is a TypeScript requirement, not optional. Even if you see code that returns data from form actions, that code is WRONG.**

When using form action attribute: `<form action={serverAction}>`
- The function **MUST have no return statement** (implicitly returns void)
- TypeScript will **REJECT any return value**, even `return undefined` or `return null`
- **IMPORTANT:** If you see example code in the codebase that returns data from a form action, ignore it - it's an anti-pattern. Fix it by removing the return statement.

❌ WRONG (causes build error):
```typescript
export async function saveForm(formData: FormData) {
  'use server';

  const name = formData.get('name') as string;
  if (!name) throw new Error('Name required');

  await db.save(name);
  return { success: true }; // ❌ BUILD ERROR: Type mismatch
}

// In component:
<form action={saveForm}>  {/* ❌ Expects void function */}
  <input name="name" />
</form>
```

✅ CORRECT - Option 1 (Simple form action, no response):
```typescript
export async function saveForm(formData: FormData) {
  'use server';

  const name = formData.get('name') as string;

  // Validate - throw errors instead of returning them
  if (!name) throw new Error('Name required');

  await db.save(name);
  revalidatePath('/'); // Trigger UI update
  // No return statement - returns void implicitly
}

// In component:
<form action={saveForm}>
  <input name="name" required />
  <button type="submit">Save</button>
</form>
```

✅ CORRECT - Option 2 (With useActionState for feedback):
```typescript
export async function saveForm(prevState: any, formData: FormData) {
  'use server';

  const name = formData.get('name') as string;
  if (!name) return { error: 'Name required' };

  await db.save(name);
  return { success: true, message: 'Saved!' }; // ✅ OK with useActionState
}

// In component:
'use client';
const [state, action] = useActionState(saveForm, null);

return (
  <form action={action}>
    <input name="name" required />
    <button type="submit">Save</button>
    {state?.error && <p>{state.error}</p>}
    {state?.success && <p>{state.message}</p>}
  </form>
);
```

**The key rule:** `<form action={...}>` expects `void`. If you need to return data, use `useActionState`.

## Route Handlers (API Routes)

### Basic Route Handler

Route Handlers replace API Routes from the Pages Router. Create them in `route.ts` or `route.js` files.

```typescript
// app/api/hello/route.ts
export async function GET(request: Request) {
  return Response.json({ message: 'Hello World' });
}

export async function POST(request: Request) {
  const body = await request.json();

  return Response.json({
    message: 'Data received',
    data: body
  });
}
```

### Supported HTTP Methods

```typescript
// app/api/items/route.ts
export async function GET(request: Request) { }
export async function POST(request: Request) { }
export async function PUT(request: Request) { }
export async function PATCH(request: Request) { }
export async function DELETE(request: Request) { }
export async function HEAD(request: Request) { }
export async function OPTIONS(request: Request) { }
```

### Dynamic Route Handlers

```typescript
// app/api/posts/[id]/route.ts
export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  const id = params.id;
  const post = await db.posts.findUnique({ where: { id } });

  return Response.json(post);
}

export async function DELETE(
  request: Request,
  { params }: { params: { id: string } }
) {
  await db.posts.delete({ where: { id: params.id } });

  return Response.json({ success: true });
}
```

### Request Headers and Cookies

```typescript
// app/api/profile/route.ts
import { cookies, headers } from 'next/headers';

export async function GET(request: Request) {
  // Access headers
  const headersList = await headers();
  const authorization = headersList.get('authorization');

  // Access cookies
  const cookieStore = await cookies();
  const sessionToken = cookieStore.get('session-token');

  if (!sessionToken) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const user = await fetchUser(sessionToken.value);

  return Response.json(user);
}
```

### Setting Cookies in Route Handlers

```typescript
// app/api/login/route.ts
import { cookies } from 'next/headers';

export async function POST(request: Request) {
  const { email, password } = await request.json();

  const token = await authenticate(email, password);

  if (!token) {
    return Response.json({ error: 'Invalid credentials' }, { status: 401 });
  }

  // Set cookie
  const cookieStore = await cookies();
  cookieStore.set('session-token', token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    maxAge: 60 * 60 * 24 * 7, // 1 week
    path: '/',
  });

  return Response.json({ success: true });
}
```

### CORS Configuration

```typescript
// app/api/public/route.ts
export async function GET(request: Request) {
  const data = await fetchData();

  return Response.json(data, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  });
}

export async function OPTIONS(request: Request) {
  return new Response(null, {
    status: 204,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  });
}
```

### Streaming Responses

```typescript
// app/api/stream/route.ts
export async function GET() {
  const encoder = new TextEncoder();

  const stream = new ReadableStream({
    async start(controller) {
      for (let i = 0; i < 10; i++) {
        controller.enqueue(encoder.encode(`data: ${i}\n\n`));
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
      controller.close();
    },
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  });
}
```

## Server Actions

Server Actions enable server-side mutations without creating API endpoints.

### Basic Server Action (Without Return)

```typescript
// app/actions.ts
'use server';

import { revalidatePath } from 'next/cache';

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;
  const content = formData.get('content') as string;

  const post = await db.posts.create({
    data: { title, content },
  });

  revalidatePath('/posts');
  // No return statement - Server Actions with forms should return void
}
```

**Note:** See "Using Server Actions in Forms" section below for patterns that return data vs. those that don't.

### ⚠️ CRITICAL: Server Actions File Organization

**File Naming Precision:**
- When stakeholders specify a filename (e.g., “create a server action in a file called `action.ts`”), mirror it exactly.
- Common filenames: `action.ts` (singular) or `actions.ts` (plural)—choose the one that matches the brief or existing code.
- Place the file in the appropriate directory: typically `app/action.ts` or `app/actions.ts`.

**Two Patterns for 'use server' Directive:**

**Pattern 1: File-level (recommended for multiple actions):**
```typescript
// app/actions.ts
'use server';  // At the top - ALL exports are server actions

export async function createPost(formData: FormData) { ... }
export async function updatePost(formData: FormData) { ... }
export async function deletePost(postId: string) { ... }
```

**Pattern 2: Function-level (for single action or mixed file):**
```typescript
// app/action.ts or any file
export async function createPost(formData: FormData) {
  'use server';  // Inside the function - ONLY this function is a server action

  const title = formData.get('title') as string;
  await db.posts.create({ data: { title } });
}
```

**Client Component Calling Server Action:**

When a client component needs to call a server action (e.g., onClick, form submission):
1. Create the server action in a SEPARATE file with 'use server' directive
2. Import and use it in the client component

**✅ CORRECT Pattern:**
```typescript
// app/actions.ts - Server Actions file
'use server';

import { cookies } from 'next/headers';

export async function updateUserPreference(key: string, value: string) {
  const cookieStore = await cookies();
  cookieStore.set(key, value);

  // Or perform other server-side operations
  await db.userSettings.update({ [key]: value });
}

// app/InteractiveButton.tsx - Client Component
'use client';

import { updateUserPreference } from './actions';

export default function InteractiveButton() {
  const handleClick = () => {
    updateUserPreference('theme', 'dark');
  };

  return (
    <button onClick={handleClick}>
      Update Preference
    </button>
  );
}
```

**❌ WRONG - Mixing 'use server' and 'use client' in same file:**
```typescript
// app/CookieButton.tsx
'use client';  // This file is a client component

export async function setCookie() {
  'use server';  // ERROR! Can't have server actions in client component file
  // ...
}
```

### Using Server Actions in Forms - Two Patterns

#### Pattern 1: Simple Form Action (Returns void / Throws Errors)

**CRITICAL:** When using form `action` attribute directly, the Server Action **MUST return void** (nothing). Do NOT return `{ success: true }` or any object.

**VALIDATION RULE:** Check all inputs and throw errors if validation fails. Do NOT return error objects.

⚠️ **IMPORTANT:** Even if you see example code in the codebase that returns `{ success: true }` from a form action, **do NOT copy that pattern**. That code is an anti-pattern. Always:
1. Check/validate inputs
2. Throw errors if validation fails (don't return error objects)
3. Process the request
4. Don't return anything (return void)

Correct pattern for form actions:

```typescript
// app/actions.ts
'use server';

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;
  const content = formData.get('content') as string;

  // Validate
  if (!title || !content) {
    throw new Error('Title and content are required');
  }

  // Save to database
  await db.posts.create({ data: { title, content } });

  // Revalidate or redirect - no return needed
  revalidatePath('/posts');
}

// app/posts/new/page.tsx
import { createPost } from '@/app/actions';

export default function NewPost() {
  return (
    <form action={createPost}>
      <input name="title" placeholder="Title" required />
      <textarea name="content" placeholder="Content" required />
      <button type="submit">Create Post</button>
    </form>
  );
}
```

#### Pattern 2: Form with useActionState (Returns data)

When you need to display success/error messages, use `useActionState`:

```typescript
// app/actions.ts
'use server';

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;
  const content = formData.get('content') as string;

  if (!title || !content) {
    return { success: false, error: 'Title and content required' };
  }

  const post = await db.posts.create({ data: { title, content } });
  return { success: true, post };
}

// app/posts/new/page.tsx
'use client';

import { createPost } from '@/app/actions';
import { useActionState } from 'react';

export default function NewPost() {
  const [state, action, isPending] = useActionState(createPost, null);

  return (
    <form action={action}>
      <input name="title" placeholder="Title" required />
      <textarea name="content" placeholder="Content" required />
      <button type="submit" disabled={isPending}>
        {isPending ? 'Creating...' : 'Create Post'}
      </button>
      {state?.error && <p style={{ color: 'red' }}>{state.error}</p>}
      {state?.success && <p style={{ color: 'green' }}>Post created!</p>}
    </form>
  );
}
```

**Key difference:**
- **Pattern 1:** Form action only, Server Action returns void, use `revalidatePath`
- **Pattern 2:** With `useActionState`, Server Action returns data for display

### Form Validation Example - Multiple Fields

When validating multiple required fields, check them all together and throw if any are missing:

```typescript
'use server';

export async function saveContactMessage(formData: FormData) {
  const name = formData.get('name') as string;
  const email = formData.get('email') as string;
  const message = formData.get('message') as string;

  // Validate all fields - throw if any are missing
  if (!name || !email || !message) {
    throw new Error('All fields are required');
  }

  // Save to database
  console.log('Saving contact message:', { name, email, message });

  // No return - returns void implicitly
}
```

This will:
1. ✅ Pass TypeScript checks (returns void)
2. ✅ Validate all inputs before processing
3. ✅ Throw error if validation fails (prevents database save)
4. ✅ Not return an error object (which would break form action typing)

### Server Actions with Client Components

```typescript
// app/actions.ts
'use server';

export async function updateUsername(userId: string, username: string) {
  await db.users.update({
    where: { id: userId },
    data: { username },
  });

  return { success: true };
}

// app/components/UsernameForm.tsx
'use client';

import { updateUsername } from '@/app/actions';
import { useState } from 'react';

export default function UsernameForm({ userId }: { userId: string }) {
  const [username, setUsername] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    await updateUsername(userId, username);

    setLoading(false);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="New username"
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Updating...' : 'Update'}
      </button>
    </form>
  );
}
```

### Server Actions with Validation (Throw Errors)

When using form actions directly, throw errors for validation failures (don't return error objects):

```typescript
// app/actions.ts
'use server';

import { revalidatePath } from 'next/cache';

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;
  const content = formData.get('content') as string;

  // Validation - throw error if invalid
  if (!title || !content) {
    throw new Error('Title and content are required');
  }

  if (title.length > 100) {
    throw new Error('Title must be less than 100 characters');
  }

  if (content.length < 10) {
    throw new Error('Content must be at least 10 characters');
  }

  // Save to database
  const post = await db.posts.create({
    data: { title, content },
  });

  revalidatePath('/posts');
  // No return - form actions return void
}
```

**For returning validation state:** If you need to return validation errors or show them in the UI, use `useActionState` (Pattern 2 above) instead.

### Setting Cookies in Server Actions

```typescript
// app/actions.ts
'use server';

import { cookies } from 'next/headers';

export async function setTheme(theme: 'light' | 'dark') {
  const cookieStore = await cookies();

  cookieStore.set('theme', theme, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    maxAge: 60 * 60 * 24 * 365, // 1 year
    path: '/',
  });

  return { success: true };
}
```

### Revalidation and Redirection

```typescript
// app/actions.ts
'use server';

import { revalidatePath, revalidateTag } from 'next/cache';
import { redirect } from 'next/navigation';

export async function deletePost(postId: string) {
  await db.posts.delete({ where: { id: postId } });

  // Revalidate specific path
  revalidatePath('/posts');

  // Or revalidate by cache tag
  revalidateTag('posts');

  // Redirect after deletion
  redirect('/posts');
}
```

## Step 0: Determine Parallel Route Scope

Before implementing parallel routes, identify WHERE they should live in your route structure.

### Analyzing Route Context

**Key Question:** Is this feature for a specific page/section, or for the entire application?

- **Specific page/section** → Create under that route directory
- **Entire application** → Create at root level

### Route Scope Decision Process

**When the requirement mentions a specific feature or page:**
```
"Create a [feature-name] with parallel routes for X and Y"
→ Structure: app/[feature-name]/@x/ and app/[feature-name]/@y/
```

**When the requirement covers app-wide layout:**
```
"Create an app with parallel routes for X and Y"
→ Structure: app/@x/ and app/@y/
```

### Common Scope Mistake

❌ **WRONG - Parallel routes at incorrect scope:**
```
Request: "Create a [specific-feature] with sections for X and Y"

app/
├── @x/              # ❌ Created at root - affects entire app!
├── @y/              # ❌ Wrong scope
└── layout.tsx       # ❌ Root layout modified unnecessarily
```

This makes the parallel routes global when they should be feature-specific.

✅ **CORRECT - Parallel routes properly scoped:**
```
Request: "Create a [specific-feature] with sections for X and Y"

app/
├── [specific-feature]/
│   ├── @x/          # ✅ Scoped to this feature
│   ├── @y/          # ✅ Only affects this route
│   └── layout.tsx   # ✅ Feature-specific layout
└── layout.tsx       # Root layout unchanged
```

### Decision Criteria

1. **Analyze the requirements** - Look for specific feature/page names
   - Mentions a specific noun/feature? → Create under `app/[that-feature]/`
   - General app-level description? → Determine if root or new route

2. **Consider URL structure** - What URL should this live at?
   - `/feature` path → Use `app/feature/@slots/`
   - Root `/` path → Use `app/@slots/`
   - Nested `/parent/feature` → Use `app/parent/feature/@slots/`

3. **Think about scope impact** - How much of the app is affected?
   - One feature/page only? → Scope to feature directory
   - Multiple related pages? → Scope to parent directory
   - Entire application? → Use root level

### Practical Examples

**Example 1: Feature-specific parallel routes**
```
Scenario: a user profile page needs tabs for posts and activity

Analysis:
- "user profile page" = specific feature
- Should be at /profile URL
- Only affects profile page

Structure:
app/
├── profile/
│   ├── @posts/
│   │   └── page.tsx
│   ├── @activity/
│   │   └── page.tsx
│   └── layout.tsx        # Accepts posts, activity slots
```

**Example 2: App-wide parallel routes**
```
Scenario: the overall application layout must expose sidebar and main content slots

Analysis:
- "application layout" = root level
- Affects entire app
- Should be at root

Structure:
app/
├── @sidebar/
│   └── page.tsx
├── @main/
│   └── page.tsx
└── layout.tsx            # Root layout with slots
```

**Example 3: Nested section parallel routes**
```
Scenario: the admin area adds an analytics view with charts and tables

Analysis:
- "admin panel" = existing section
- "analytics view" = subsection
- Should be at /admin/analytics URL

Structure:
app/
├── admin/
│   ├── analytics/
│   │   ├── @charts/
│   │   │   └── page.tsx
│   │   ├── @tables/
│   │   │   └── page.tsx
│   │   └── layout.tsx    # Analytics-specific layout
│   └── layout.tsx        # Admin layout (unchanged)
```

### Quick Reference

| Requirement Pattern | Route Scope | Example Structure |
|---------------|-------------|-------------------|
| Feature-specific requirement | `app/[feature]/` | `app/profile/@tab/` |
| Section inside a parent area | `app/[parent]/[section]/` | `app/admin/analytics/@view/` |
| App-wide layout requirement | `app/` | `app/@sidebar/` |
| Page with multiple panels | `app/[page]/` | `app/settings/@panel/` |

**CRITICAL RULE:** Always analyze the requirement for scope indicators before defaulting to root-level parallel routes.

## Parallel Routes

Parallel Routes allow rendering multiple pages in the same layout simultaneously.

### ⚠️ IMPORTANT: Understand Route Scope First

Before creating parallel routes, **review "Step 0: Determine Parallel Route Scope" above** to identify the correct directory level.

Don't default to creating parallel routes at root level - scope them appropriately to the feature/page mentioned in the requirements.

### Creating Parallel Routes (Feature-Scoped)

For feature-specific parallel routes (most common):

```
app/
├── [feature-name]/
│   ├── @slot1/
│   │   └── page.tsx
│   ├── @slot2/
│   │   └── page.tsx
│   ├── layout.tsx       # Feature layout accepting slot props
│   └── page.tsx         # Feature main page
```

### Creating Parallel Routes (Root-Level)

For app-wide parallel routes (less common):

```
app/
├── @slot1/
│   └── page.tsx
├── @slot2/
│   └── page.tsx
├── layout.tsx           # Root layout with slots
└── page.tsx
```

### Layout with Parallel Routes (Feature-Scoped Example)

For a feature with parallel routes:

```typescript
// app/[feature]/layout.tsx
export default function FeatureLayout({
  children,
  slot1,
  slot2,
}: {
  children: React.ReactNode;
  slot1: React.ReactNode;
  slot2: React.ReactNode;
}) {
  return (
    <div>
      <h1>Feature Page</h1>
      <div className="main">{children}</div>
      <div className="slots">
        <div className="slot1">{slot1}</div>
        <div className="slot2">{slot2}</div>
      </div>
    </div>
  );
}
```

### Layout with Parallel Routes (Root-Level Example)

For app-wide parallel routes:

```typescript
// app/layout.tsx
export default function RootLayout({
  children,
  sidebar,
  main,
}: {
  children: React.ReactNode;
  sidebar: React.ReactNode;
  main: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <div className="app-layout">
          <aside>{sidebar}</aside>
          <main>{main}</main>
          {children}
        </div>
      </body>
    </html>
  );
}
```

### Default Parallel Route

Create a `default.tsx` to handle unmatched routes or provide fallback UI:

```typescript
// Feature-scoped: app/[feature]/@slot1/default.tsx
export default function Default() {
  return null; // Or a default UI
}

// Root-level: app/@sidebar/default.tsx
export default function Default() {
  return <div>Default sidebar content</div>;
}
```

### Conditional Parallel Routes

Parallel routes can be conditionally rendered based on runtime conditions:

```typescript
// app/[feature]/layout.tsx (or any layout with parallel routes)
export default function Layout({
  children,
  analytics,
}: {
  children: React.ReactNode;
  analytics: React.ReactNode;
}) {
  const showAnalytics = true; // Could be based on user permissions, feature flags, etc.

  return (
    <div>
      <main>{children}</main>
      {showAnalytics && <aside>{analytics}</aside>}
    </div>
  );
}
```

**Note:** This pattern works at any layout level (root or feature-scoped).

## Intercepting Routes

Intercepting Routes allow you to load a route within the current layout while keeping the context of the current page.

### Intercepting Route Conventions

- `(.)` - Match segments on the same level
- `(..)` - Match segments one level above
- `(..)(..)` - Match segments two levels above
- `(...)` - Match segments from the root

### Modal Pattern with Intercepting Routes

```
app/
├── photos/
│   ├── [id]/
│   │   └── page.tsx        # Full photo page
│   └── page.tsx            # Photo gallery
├── @modal/
│   └── (.)photos/
│       └── [id]/
│           └── page.tsx    # Modal photo view
└── layout.tsx
```

### Layout for Modal Pattern

```typescript
// app/layout.tsx
export default function Layout({
  children,
  modal,
}: {
  children: React.ReactNode;
  modal: React.ReactNode;
}) {
  return (
    <div>
      {children}
      {modal}
    </div>
  );
}
```

### Modal Component

```typescript
// app/@modal/(.)photos/[id]/page.tsx
import Modal from '@/components/Modal';
import PhotoView from '@/components/PhotoView';

export default async function PhotoModal({
  params,
}: {
  params: { id: string };
}) {
  const photo = await getPhoto(params.id);

  return (
    <Modal>
      <PhotoView photo={photo} />
    </Modal>
  );
}

// app/@modal/default.tsx
export default function Default() {
  return null;
}
```

### Client-Side Modal Component

```typescript
// components/Modal.tsx
'use client';

import { useRouter } from 'next/navigation';
import { useEffect, useRef } from 'react';

export default function Modal({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const dialogRef = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    dialogRef.current?.showModal();
  }, []);

  const handleClose = () => {
    router.back();
  };

  return (
    <dialog ref={dialogRef} onClose={handleClose}>
      <button onClick={handleClose}>Close</button>
      {children}
    </dialog>
  );
}
```

## Error Boundaries

### Basic Error Boundary

```typescript
// app/error.tsx
'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

### Nested Error Boundaries

```typescript
// app/dashboard/error.tsx
'use client';

export default function DashboardError({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div className="dashboard-error">
      <h2>Dashboard Error</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Retry</button>
    </div>
  );
}
```

### Global Error Boundary

```typescript
// app/global-error.tsx
'use client';

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <html>
      <body>
        <h2>Application Error</h2>
        <p>{error.message}</p>
        <button onClick={reset}>Try again</button>
      </body>
    </html>
  );
}
```

### Not Found Boundary

```typescript
// app/not-found.tsx
import Link from 'next/link';

export default function NotFound() {
  return (
    <div>
      <h2>Page Not Found</h2>
      <p>Could not find requested resource</p>
      <Link href="/">Return Home</Link>
    </div>
  );
}

// Trigger programmatically
import { notFound } from 'next/navigation';

export default async function Page({ params }: { params: { id: string } }) {
  const post = await getPost(params.id);

  if (!post) {
    notFound();
  }

  return <div>{post.title}</div>;
}
```

## Draft Mode

Draft Mode allows you to preview draft content from a headless CMS.

### Enabling Draft Mode

```typescript
// app/api/draft/route.ts
import { draftMode } from 'next/headers';
import { redirect } from 'next/navigation';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const secret = searchParams.get('secret');
  const slug = searchParams.get('slug');

  // Check secret
  if (secret !== process.env.DRAFT_SECRET) {
    return Response.json({ message: 'Invalid token' }, { status: 401 });
  }

  // Enable Draft Mode
  const draft = await draftMode();
  draft.enable();

  // Redirect to the path from the fetched post
  redirect(slug || '/');
}
```

### Disabling Draft Mode

```typescript
// app/api/draft/disable/route.ts
import { draftMode } from 'next/headers';
import { redirect } from 'next/navigation';

export async function GET() {
  const draft = await draftMode();
  draft.disable();
  redirect('/');
}
```

### Using Draft Mode in Pages

```typescript
// app/posts/[slug]/page.tsx
import { draftMode } from 'next/headers';

export default async function Post({ params }: { params: { slug: string } }) {
  const draft = await draftMode();
  const isDraft = draft.isEnabled;

  // Fetch draft or published content
  const post = await getPost(params.slug, isDraft);

  return (
    <article>
      {isDraft && (
        <div className="draft-banner">
          <p>Draft Mode Active</p>
          <a href="/api/draft/disable">Exit Draft Mode</a>
        </div>
      )}
      <h1>{post.title}</h1>
      <div>{post.content}</div>
    </article>
  );
}
```

## Streaming and Suspense

### Basic Streaming with Suspense

```typescript
// app/dashboard/page.tsx
import { Suspense } from 'react';

export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>

      <Suspense fallback={<StatsSkeleton />}>
        <Stats />
      </Suspense>

      <Suspense fallback={<RecentActivitySkeleton />}>
        <RecentActivity />
      </Suspense>
    </div>
  );
}

async function Stats() {
  const stats = await fetchStats(); // Slow query
  return <div className="stats">{JSON.stringify(stats)}</div>;
}

async function RecentActivity() {
  const activity = await fetchRecentActivity();
  return (
    <ul>
      {activity.map((item) => (
        <li key={item.id}>{item.description}</li>
      ))}
    </ul>
  );
}
```

### Nested Suspense Boundaries

```typescript
// app/page.tsx
import { Suspense } from 'react';

export default function Page() {
  return (
    <div>
      <Header />

      <Suspense fallback={<PageSkeleton />}>
        <MainContent />
      </Suspense>
    </div>
  );
}

async function MainContent() {
  const data = await fetchMainData();

  return (
    <div>
      <h2>{data.title}</h2>

      <Suspense fallback={<CommentsSkeleton />}>
        <Comments postId={data.id} />
      </Suspense>
    </div>
  );
}

async function Comments({ postId }: { postId: string }) {
  const comments = await fetchComments(postId);
  return (
    <ul>
      {comments.map((c) => <li key={c.id}>{c.text}</li>)}
    </ul>
  );
}
```

### Loading States with loading.tsx

```typescript
// app/dashboard/loading.tsx
export default function Loading() {
  return (
    <div className="loading-skeleton">
      <div className="skeleton-header" />
      <div className="skeleton-body" />
    </div>
  );
}
```

### Streaming with Loading UI

```typescript
// app/posts/loading.tsx
export default function PostsLoading() {
  return (
    <div>
      {[1, 2, 3].map((i) => (
        <div key={i} className="post-skeleton">
          <div className="skeleton-title" />
          <div className="skeleton-excerpt" />
        </div>
      ))}
    </div>
  );
}
```

## Advanced Patterns

### Optimistic Updates with Server Actions

```typescript
// app/components/LikeButton.tsx
'use client';

import { useOptimistic } from 'react';
import { likePost } from '@/app/actions';

export default function LikeButton({
  postId,
  initialLikes,
}: {
  postId: string;
  initialLikes: number;
}) {
  const [optimisticLikes, addOptimisticLike] = useOptimistic(
    initialLikes,
    (state, amount: number) => state + amount
  );

  const handleLike = async () => {
    addOptimisticLike(1);
    await likePost(postId);
  };

  return (
    <button onClick={handleLike}>
      Likes: {optimisticLikes}
    </button>
  );
}
```

### Progressive Enhancement with Forms

```typescript
// app/posts/new/page.tsx
'use client';

import { useFormState, useFormStatus } from 'react-dom';
import { createPost } from '@/app/actions';

function SubmitButton() {
  const { pending } = useFormStatus();

  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Creating...' : 'Create Post'}
    </button>
  );
}

export default function NewPost() {
  const [state, formAction] = useFormState(createPost, null);

  return (
    <form action={formAction}>
      <input name="title" placeholder="Title" required />
      <textarea name="content" placeholder="Content" required />

      {state?.errors && (
        <div className="errors">
          {Object.entries(state.errors).map(([field, messages]) => (
            <div key={field}>
              {messages.map((msg) => <p key={msg}>{msg}</p>)}
            </div>
          ))}
        </div>
      )}

      <SubmitButton />
    </form>
  );
}
```

## Summary

- **Route Handlers** - API endpoints in `route.ts` files with HTTP method exports
- **Server Actions** - Server-side mutations with 'use server' directive
- **Parallel Routes** - Multiple pages rendered simultaneously using `@folder` syntax
- **Intercepting Routes** - Load routes in context using `(.)` syntax for modals
- **Error Boundaries** - Handle errors with `error.tsx` and `global-error.tsx`
- **Draft Mode** - Preview draft content from CMS
- **Streaming** - Progressive rendering with Suspense boundaries
- **Cookies** - Access and set cookies in Route Handlers and Server Actions
- **Revalidation** - Invalidate cache with `revalidatePath` and `revalidateTag`
