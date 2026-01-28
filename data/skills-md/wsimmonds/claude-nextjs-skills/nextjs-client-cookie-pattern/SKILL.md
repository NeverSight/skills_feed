---
name: nextjs-client-cookie-pattern
description: Pattern for client components calling server actions to set cookies in Next.js. Covers the two-file pattern of a client component with user interaction (onClick, form submission) that calls a server action to modify cookies. Use when building features like authentication, preferences, or session management where client-side triggers need to set/modify server-side cookies.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Next.js: Client Component + Server Action Cookie Pattern

## Pattern Overview

This pattern handles a common Next.js requirement: **client-side interaction (button click) that needs to set server-side cookies**.

**Why Two Files?**
- Client components (`'use client'`) can have onClick handlers
- Only server code can set cookies (security requirement)
- Solution: Client component calls a server action that sets cookies

## The Pattern

**Scenario:** A button that sets a cookie when clicked

**File 1: Client Component** (`app/CookieButton.tsx`)
- Has `'use client'` directive
- Has onClick handler
- Imports and calls server action

**File 2: Server Action** (`app/actions.ts`)
- Has `'use server'` directive
- Uses `cookies()` from `next/headers`
- Sets the cookie

## Complete Implementation

### File 1: Client Component

```typescript
// app/CookieButton.tsx
'use client';

import { setPreference } from './actions';

export default function CookieButton() {
  const handleClick = async () => {
    await setPreference('dark-mode', 'true');
  };

  return (
    <button onClick={handleClick}>
      Enable Dark Mode
    </button>
  );
}
```

### File 2: Server Action

```typescript
// app/actions.ts
'use server';

import { cookies } from 'next/headers';

export async function setPreference(key: string, value: string) {
  const cookieStore = await cookies();

  cookieStore.set(key, value, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    maxAge: 60 * 60 * 24 * 365, // 1 year
  });
}
```

## File Structure

```
app/
├── CookieButton.tsx    ← Client component
├── actions.ts          ← Server actions
└── page.tsx            ← Uses CookieButton
```

## TypeScript: NEVER Use `any` Type

This codebase has `@typescript-eslint/no-explicit-any` enabled.

```typescript
// ❌ WRONG
async function setCookie(key: any, value: any) { ... }

// ✅ CORRECT
async function setCookie(key: string, value: string) { ... }
```

## Real-World Examples

### Example 1: Theme Toggle

```typescript
// app/ThemeToggle.tsx
'use client';

import { useState } from 'react';
import { setTheme } from './actions';

export default function ThemeToggle() {
  const [theme, setLocalTheme] = useState('light');

  const toggle = async () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setLocalTheme(newTheme);
    await setTheme(newTheme);
  };

  return (
    <button onClick={toggle} className={theme}>
      {theme === 'light' ? '🌙' : '☀️'} Toggle Theme
    </button>
  );
}

// app/actions.ts
'use server';

import { cookies } from 'next/headers';

export async function setTheme(theme: 'light' | 'dark') {
  const cookieStore = await cookies();
  cookieStore.set('theme', theme, {
    httpOnly: false, // Allow client to read it
    maxAge: 60 * 60 * 24 * 365,
  });
}
```

### Example 2: Accept Cookies Banner

```typescript
// app/components/CookieBanner.tsx
'use client';

import { useState } from 'react';
import { acceptCookies } from '../actions';

export default function CookieBanner() {
  const [visible, setVisible] = useState(true);

  const handleAccept = async () => {
    await acceptCookies();
    setVisible(false);
  };

  if (!visible) return null;

  return (
    <div className="cookie-banner">
      <p>We use cookies to improve your experience.</p>
      <button onClick={handleAccept}>Accept</button>
    </div>
  );
}

// app/actions.ts
'use server';

import { cookies } from 'next/headers';

export async function acceptCookies() {
  const cookieStore = await cookies();
  cookieStore.set('cookies-accepted', 'true', {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    maxAge: 60 * 60 * 24 * 365,
  });
}
```

### Example 3: Language Preference

```typescript
// app/LanguageSelector.tsx
'use client';

import { setLanguage } from './actions';

export default function LanguageSelector() {
  const languages = ['en', 'es', 'fr', 'de'];

  return (
    <select onChange={(e) => setLanguage(e.target.value)}>
      {languages.map((lang) => (
        <option key={lang} value={lang}>
          {lang.toUpperCase()}
        </option>
      ))}
    </select>
  );
}

// app/actions.ts
'use server';

import { cookies } from 'next/headers';

export async function setLanguage(lang: string) {
  const cookieStore = await cookies();
  cookieStore.set('language', lang, {
    httpOnly: false,
    maxAge: 60 * 60 * 24 * 365,
  });
}
```

## Cookie Options

```typescript
cookieStore.set('name', 'value', {
  httpOnly: true,    // Prevents JavaScript access (security)
  secure: true,      // Only send over HTTPS
  sameSite: 'lax',   // CSRF protection
  maxAge: 3600,      // Expires in 1 hour (seconds)
  path: '/',         // Available on all routes
});
```

## Common Variations

### With Form Submission

```typescript
// app/PreferencesForm.tsx
'use client';

import { savePreferences } from './actions';

export default function PreferencesForm() {
  return (
    <form action={savePreferences}>
      <label>
        <input type="checkbox" name="notifications" />
        Enable Notifications
      </label>
      <button type="submit">Save</button>
    </form>
  );
}

// app/actions.ts
'use server';

import { cookies } from 'next/headers';

export async function savePreferences(formData: FormData) {
  const cookieStore = await cookies();
  const notifications = formData.get('notifications') === 'on';

  cookieStore.set('notifications', String(notifications), {
    httpOnly: true,
    maxAge: 60 * 60 * 24 * 365,
  });
}
```

### With Redirect After Setting Cookie

```typescript
// app/actions.ts
'use server';

import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';

export async function login(email: string, password: string) {
  // Authenticate user
  const session = await authenticate(email, password);

  // Set session cookie
  const cookieStore = await cookies();
  cookieStore.set('session', session.token, {
    httpOnly: true,
    secure: true,
    sameSite: 'lax',
    maxAge: 60 * 60 * 24 * 7, // 1 week
  });

  // Redirect to dashboard
  redirect('/dashboard');
}
```

## Why This Pattern?

**Can't client components set cookies directly?**
No. Client components run in the browser, and modern browsers restrict cookie manipulation for security. Server actions run on the server where cookie-setting is allowed.

**Why not use a Route Handler (API route)?**
You can! But server actions are simpler and more integrated with the Next.js App Router pattern.

```typescript
// Alternative: Route Handler approach
// app/api/set-cookie/route.ts
export async function POST(request: Request) {
  const { name, value } = await request.json();

  return new Response(null, {
    status: 200,
    headers: {
      'Set-Cookie': `${name}=${value}; HttpOnly; Path=/; Max-Age=31536000`,
    },
  });
}

// Client component
async function setCookie() {
  await fetch('/api/set-cookie', {
    method: 'POST',
    body: JSON.stringify({ name: 'theme', value: 'dark' }),
  });
}
```

Server actions are preferred because they're:
- More type-safe
- Less boilerplate
- Better integrated with forms
- Easier to test

## Reading Cookies

**In Server Components:**
```typescript
// app/page.tsx
import { cookies } from 'next/headers';

export default async function Page() {
  const cookieStore = await cookies();
  const theme = cookieStore.get('theme')?.value || 'light';

  return <div className={theme}>Content</div>;
}
```

**In Client Components:**
```typescript
// Can't use next/headers in client components!
// Use document.cookie or a state management library
'use client';

import { useEffect, useState } from 'react';

export default function ThemeDisplay() {
  const [theme, setTheme] = useState('light');

  useEffect(() => {
    // Read from document.cookie
    const cookieTheme = document.cookie
      .split('; ')
      .find(row => row.startsWith('theme='))
      ?.split('=')[1];

    if (cookieTheme) setTheme(cookieTheme);
  }, []);

  return <div>Current theme: {theme}</div>;
}
```

## Quick Checklist

When you need to set cookies from a button click:

- [ ] Create client component with `'use client'`
- [ ] Add onClick handler or form submission
- [ ] Create server action file (e.g., `app/actions.ts`)
- [ ] Add `'use server'` directive
- [ ] Import `cookies` from `next/headers`
- [ ] Await `cookies()` (Next.js 15+)
- [ ] Call `cookieStore.set(name, value, options)`
- [ ] Import server action in client component
- [ ] Call server action from handler

## Summary

**Client-Server Cookie Pattern:**
- ✅ Client component handles user interaction
- ✅ Server action sets the cookie
- ✅ Two files: component + actions
- ✅ Type-safe with proper TypeScript
- ✅ Secure (httpOnly, secure, sameSite options)

This pattern is the recommended way to handle client-triggered cookie operations in Next.js App Router.
