---
name: react-19
description: >
  React 19 patterns and breaking changes vs React 18.
  Trigger: When writing React 19 components/hooks in .tsx (ref as prop, new hooks, Actions, deprecations).
  If using Next.js App Router/Server Actions, also use nextjs-15.
license: MIT
metadata:
  author: noklip-io
  version: "1.0"
  scope: [root, ui]
  auto_invoke: "Writing React 19 components"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

# React 19 - Key Changes

This skill focuses on **what changed** in React 19. Not a complete React reference.

## Coming from React 16/17?

If upgrading from pre-18 versions, these changes accumulated and are **now mandatory**:

| Change | Introduced | React 19 Status |
|--------|------------|-----------------|
| `createRoot` / `hydrateRoot` | React 18 | **Required** (`ReactDOM.render` removed) |
| Concurrent rendering | React 18 | Foundation for all R19 features |
| Automatic batching | React 18 | Default behavior |
| `useId`, `useSyncExternalStore` | React 18 | Stable, commonly used |
| Hooks (no classes for new code) | React 16.8 | Only path for new features |
| `createContext` (not legacy) | React 16.3 | **Required** (legacy Context removed) |
| Error Boundaries | React 16 | Now with better error callbacks |

**Migration path:** Upgrade to React 18.3 first (shows deprecation warnings), then to 19.

## The React 19 Mindset

React 19 represents fundamental shifts in how to think about React:

| Old Thinking | New Thinking |
|--------------|--------------|
| Client-side by default | **Server-first** (RSC default) |
| Manual memoization | **Compiler handles it** |
| `useEffect` for data | **async Server Components** |
| `useState` for forms | **Form Actions** |
| Loading state booleans | **Suspense boundaries** |
| Optimize everything | **Write correct code, compiler optimizes** |

See [references/paradigm-shifts.md](./references/paradigm-shifts.md) for the mental model changes.

See [references/anti-patterns.md](./references/anti-patterns.md) for what to stop doing.

## Quick Reference: What's New

| Feature | React 18 | React 19+ |
|---------|----------|-----------|
| Memoization | Manual (`useMemo`, `useCallback`, `memo`) | React Compiler (automatic) or manual |
| Forward refs | `forwardRef()` wrapper | `ref` as regular prop |
| Context provider | `<Context.Provider value={}>` | `<Context value={}>` |
| Form state | Custom with `useState` | `useActionState` hook |
| Optimistic updates | Manual state management | `useOptimistic` hook |
| Read promises | Not possible in render | `use()` hook |
| Conditional context | Not possible | `use(Context)` after conditionals |
| Form pending state | Manual tracking | `useFormStatus` hook |
| Ref cleanup | Pass `null` on unmount | Return cleanup function |
| Document metadata | `react-helmet` or manual | Native `<title>`, `<meta>`, `<link>` |
| Hide/show UI with state | Unmount/remount (state lost) | `<Activity>` component (19.2+) |
| Non-reactive Effect logic | Add to deps or suppress lint | `useEffectEvent` hook (19.2+) |
| Custom Elements | Partial support | Full support (props as properties) |
| Hydration errors | Multiple vague errors | Single error with diff |

## React Compiler & Memoization

With React Compiler enabled, manual memoization is **optional, not forbidden**:

```tsx
// React Compiler handles this automatically
function Component({ items }) {
  const filtered = items.filter(x => x.active);
  const sorted = filtered.sort((a, b) => a.name.localeCompare(b.name));
  const handleClick = (id) => console.log(id);
  return <List items={sorted} onClick={handleClick} />;
}

// Manual memoization still works as escape hatch for fine-grained control
const filtered = useMemo(() => expensiveOperation(items), [items]);
const handleClick = useCallback((id) => onClick(id), [onClick]);
```

**When to use manual memoization with React Compiler:**
- Effect dependencies that need stable references
- Sharing expensive calculations across components (compiler doesn't share)
- Explicit control over when re-computation happens

See [references/react-compiler.md](./references/react-compiler.md) for details.

## ref as Prop (forwardRef Deprecated)

```tsx
// React 19: ref is just a prop
function Input({ placeholder, ref }) {
  return <input placeholder={placeholder} ref={ref} />;
}

// Usage - no change
const inputRef = useRef(null);
<Input ref={inputRef} placeholder="Enter text" />

// forwardRef still works but will be deprecated
// Codemod: npx codemod@latest react/19/replace-forward-ref
```

## Ref Cleanup Functions

```tsx
// React 19: Return cleanup function from ref callback
<input
  ref={(node) => {
    // Setup
    node?.focus();
    // Return cleanup (called on unmount or ref change)
    return () => {
      console.log('Cleanup');
    };
  }}
/>

// React 18: Received null on unmount (still works, but cleanup preferred)
<input ref={(node) => {
  if (node) { /* setup */ }
  else { /* cleanup */ }
}} />
```

## Context as Provider

```tsx
const ThemeContext = createContext('light');

// React 19: Use Context directly
function App({ children }) {
  return (
    <ThemeContext value="dark">
      {children}
    </ThemeContext>
  );
}

// React 18: Required .Provider (still works, will be deprecated)
<ThemeContext.Provider value="dark">
  {children}
</ThemeContext.Provider>
```

## New Hooks

### useActionState

```tsx
import { useActionState } from 'react';

function Form() {
  const [error, submitAction, isPending] = useActionState(
    async (prevState, formData) => {
      const result = await saveData(formData.get('name'));
      if (result.error) return result.error;
      redirect('/success');
      return null;
    },
    null // initial state
  );

  return (
    <form action={submitAction}>
      <input name="name" disabled={isPending} />
      <button disabled={isPending}>
        {isPending ? 'Saving...' : 'Save'}
      </button>
      {error && <p className="error">{error}</p>}
    </form>
  );
}
```

### useOptimistic

```tsx
import { useOptimistic } from 'react';

function Messages({ messages, sendMessage }) {
  const [optimisticMessages, addOptimistic] = useOptimistic(
    messages,
    (state, newMessage) => [...state, { ...newMessage, sending: true }]
  );

  async function handleSubmit(formData) {
    const message = { text: formData.get('text'), id: Date.now() };
    addOptimistic(message); // Show immediately
    await sendMessage(message); // Reverts on error
  }

  return (
    <form action={handleSubmit}>
      {optimisticMessages.map(m => (
        <div key={m.id} style={{ opacity: m.sending ? 0.5 : 1 }}>
          {m.text}
        </div>
      ))}
      <input name="text" />
    </form>
  );
}
```

### use() Hook

```tsx
import { use, Suspense } from 'react';

// Read promises (suspends until resolved)
function Comments({ commentsPromise }) {
  const comments = use(commentsPromise);
  return comments.map(c => <p key={c.id}>{c.text}</p>);
}

// Usage with Suspense
<Suspense fallback={<Spinner />}>
  <Comments commentsPromise={fetchComments()} />
</Suspense>

// Conditional context reading (not possible with useContext!)
function Theme({ showTheme }) {
  if (!showTheme) return <div>Plain</div>;

  const theme = use(ThemeContext); // Can be called conditionally!
  return <div style={{ color: theme.primary }}>Themed</div>;
}
```

### useFormStatus (react-dom)

```tsx
import { useFormStatus } from 'react-dom';

// Must be used inside a <form> - reads parent form status
function SubmitButton() {
  const { pending, data, method, action } = useFormStatus();
  return (
    <button disabled={pending}>
      {pending ? 'Submitting...' : 'Submit'}
    </button>
  );
}

function Form() {
  return (
    <form action={serverAction}>
      <input name="email" />
      <SubmitButton /> {/* Reads form status via context */}
    </form>
  );
}
```

See [references/new-hooks.md](./references/new-hooks.md) for complete API details.

## Form Actions

```tsx
// Pass function directly to form action
<form action={async (formData) => {
  'use server';
  await saveToDatabase(formData);
}}>
  <input name="email" type="email" />
  <button type="submit">Subscribe</button>
</form>

// Button-level actions
<form>
  <button formAction={saveAction}>Save</button>
  <button formAction={deleteAction}>Delete</button>
</form>

// Manual form reset
import { requestFormReset } from 'react-dom';
requestFormReset(formElement);
```

## Document Metadata

```tsx
// Automatically hoisted to <head> - works in any component
function BlogPost({ post }) {
  return (
    <article>
      <title>{post.title}</title>
      <meta name="description" content={post.excerpt} />
      <meta name="author" content={post.author} />
      <link rel="canonical" href={post.url} />
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </article>
  );
}
```

## Resource Preloading

```tsx
import { prefetchDNS, preconnect, preload, preinit } from 'react-dom';

function App() {
  // DNS prefetch
  prefetchDNS('https://api.example.com');

  // Establish connection early
  preconnect('https://fonts.googleapis.com');

  // Preload resources
  preload('https://example.com/font.woff2', { as: 'font' });
  preload('/hero.jpg', { as: 'image' });

  // Load and execute script eagerly
  preinit('https://example.com/analytics.js', { as: 'script' });

  return <main>...</main>;
}
```

## Stylesheet Support

```tsx
// precedence controls insertion order and deduplication
function Component() {
  return (
    <>
      <link rel="stylesheet" href="/base.css" precedence="default" />
      <link rel="stylesheet" href="/theme.css" precedence="high" />
      <div className="styled">Content</div>
    </>
  );
}

// React ensures stylesheets load before Suspense boundary reveals
<Suspense fallback={<Skeleton />}>
  <link rel="stylesheet" href="/feature.css" precedence="default" />
  <FeatureComponent />
</Suspense>
```

## Custom Elements Support

React 19 adds full support for Custom Elements (Web Components).

```tsx
// Props matching element properties are assigned as properties
// Others are assigned as attributes
<my-element
  stringAttr="hello"           // Attribute (string)
  complexProp={{ foo: 'bar' }} // Property (object)
  onCustomEvent={handleEvent}  // Property (function)
/>
```

**Client-side:** React checks if a property exists on the element instance. If yes, assigns as property; otherwise, as attribute.

**Server-side (SSR):** Primitive types (string, number) render as attributes. Objects, functions, symbols are omitted from HTML.

```tsx
// Define custom element
class MyElement extends HTMLElement {
  constructor() {
    super();
    this.data = undefined; // React will assign to this property
  }

  connectedCallback() {
    this.textContent = JSON.stringify(this.data);
  }
}
customElements.define('my-element', MyElement);

// Use in React
<my-element data={{ items: [1, 2, 3] }} />
```

## Hydration Improvements

### Better Error Messages

React 19 shows a single error with a diff instead of multiple vague errors:

```
Uncaught Error: Hydration failed because the server rendered HTML
didn't match the client.

<App>
  <span>
+   Client
-   Server
```

### Third-Party Script Compatibility

React 19 gracefully handles elements inserted by browser extensions or third-party scripts:

- Unexpected tags in `<head>` and `<body>` are skipped (no mismatch errors)
- Stylesheets from extensions are preserved during re-renders
- No need to add `suppressHydrationWarning` for extension-injected content

## Removed APIs (Breaking)

| Removed | Migration |
|---------|-----------|
| `ReactDOM.render()` | `createRoot().render()` |
| `ReactDOM.hydrate()` | `hydrateRoot()` |
| `unmountComponentAtNode()` | `root.unmount()` |
| `ReactDOM.findDOMNode()` | Use refs |
| `propTypes` | TypeScript or remove |
| `defaultProps` (functions) | ES6 default parameters |
| String refs | Callback refs or `useRef` |
| Legacy Context | `createContext` |
| `React.createFactory` | JSX |
| `react-dom/test-utils` | `act` from `'react'` |

See [references/deprecations.md](./references/deprecations.md) for migration guides.

## TypeScript Changes

```tsx
// useRef requires argument
const ref = useRef<HTMLDivElement>(null); // Required
const ref = useRef(); // Error in React 19

// Ref callbacks must not return values (except cleanup)
<div ref={(node) => { instance = node; }} /> // Correct
<div ref={(node) => (instance = node)} />    // Error - implicit return

// ReactElement props are now unknown (not any)
type Props = ReactElement['props']; // unknown in R19, any in R18

// JSX namespace - import explicitly
import type { JSX } from 'react';
```

See [references/typescript-changes.md](./references/typescript-changes.md) for codemods.

## Migration Codemods

```bash
# Run all React 19 codemods
npx codemod@latest react/19/migration-recipe

# Individual codemods
npx codemod@latest react/19/replace-reactdom-render
npx codemod@latest react/19/replace-string-ref
npx codemod@latest react/19/replace-act-import
npx codemod@latest react/19/replace-use-form-state
npx codemod@latest react/prop-types-typescript

# TypeScript types
npx types-react-codemod@latest preset-19 ./src
```

## Imports (Best Practice)

```tsx
// Named imports (recommended)
import { useState, useEffect, useRef, use } from 'react';
import { createRoot } from 'react-dom/client';
import { useFormStatus } from 'react-dom';

// Default import still works but named preferred
import React from 'react'; // Works but not recommended
```

## Error Handling Changes

```tsx
// React 19 error handling options
const root = createRoot(container, {
  onUncaughtError: (error, errorInfo) => {
    // Errors not caught by Error Boundary
    console.error('Uncaught:', error, errorInfo.componentStack);
  },
  onCaughtError: (error, errorInfo) => {
    // Errors caught by Error Boundary
    reportToAnalytics(error);
  },
  onRecoverableError: (error, errorInfo) => {
    // Errors React recovered from automatically
    console.warn('Recovered:', error);
  }
});
```

See [references/suspense-streaming.md](./references/suspense-streaming.md) for Suspense patterns and error boundaries.

## React 19.2+ Features

### Activity Component (19.2)

Hide/show UI while preserving state (like background tabs):

```tsx
import { Activity } from 'react';

// State preserved when hidden, Effects cleaned up
<Activity mode={isVisible ? 'visible' : 'hidden'}>
  <ExpensiveComponent />
</Activity>
```

### useEffectEvent Hook (19.2)

Extract non-reactive logic from Effects without adding dependencies:

```tsx
import { useEffect, useEffectEvent } from 'react';

function Chat({ roomId, theme }) {
  // Reads theme without making it a dependency
  const onConnected = useEffectEvent(() => {
    showNotification(`Connected!`, theme);
  });

  useEffect(() => {
    const conn = connect(roomId);
    conn.on('connected', onConnected);
    return () => conn.disconnect();
  }, [roomId]); // theme NOT in deps - won't reconnect on theme change
}
```

See [references/react-19-2-features.md](./references/react-19-2-features.md) for complete 19.1+ and 19.2 features.

## Reference Documentation

| Document | Content |
|----------|---------|
| [paradigm-shifts.md](./references/paradigm-shifts.md) | Mental model changes - how to *think* in React 19 |
| [anti-patterns.md](./references/anti-patterns.md) | What to stop doing - outdated patterns |
| [react-19-2-features.md](./references/react-19-2-features.md) | React 19.1+ and 19.2 features (Activity, useEffectEvent) |
| [new-hooks.md](./references/new-hooks.md) | Complete API for 19.0 hooks |
| [server-components.md](./references/server-components.md) | RSC, Server Actions, directives |
| [suspense-streaming.md](./references/suspense-streaming.md) | Suspense, streaming, error handling |
| [react-compiler.md](./references/react-compiler.md) | Automatic memoization details |
| [deprecations.md](./references/deprecations.md) | Removed APIs with migration guides |
| [typescript-changes.md](./references/typescript-changes.md) | Type changes and codemods |
