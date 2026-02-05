---
name: superdoc-react
description: React integration guidelines for SuperDoc document editor. Use when adding document editing capabilities to React or Next.js applications, working with DOCX files, or implementing collaboration features. Triggers on tasks involving document editors, DOCX handling, or SuperDoc integration.
license: MIT
metadata:
  author: superdoc-dev
  version: "1.0.0"
---

# SuperDoc React Integration

Official React wrapper for SuperDoc - the document editing and rendering library for the web. Provides component-based API with proper lifecycle management and React Strict Mode compatibility.

## When to Apply

Reference these guidelines when:
- Adding document editing to a React application
- Integrating SuperDoc with Next.js
- Implementing DOCX file upload/export
- Setting up real-time collaboration
- Building document viewers or editors

## Installation

```bash
npm install @superdoc-dev/react
```

> `superdoc` is included as a dependency - no separate installation needed.

## Quick Start

```tsx
import { SuperDocEditor } from '@superdoc-dev/react';
import '@superdoc-dev/react/style.css';

function App() {
  return (
    <SuperDocEditor
      document={file}
      documentMode="editing"
      onReady={() => console.log('Editor ready!')}
    />
  );
}
```

## Component API

### Document Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `document` | `File \| Blob \| string \| object` | required | Document to load |
| `documentMode` | `'editing' \| 'viewing' \| 'suggesting'` | `'editing'` | Editing mode |
| `role` | `'editor' \| 'viewer' \| 'suggester'` | `'editor'` | User permissions |

### User Props

| Prop | Type | Description |
|------|------|-------------|
| `user` | `{ name, email?, image? }` | Current user info |
| `users` | `Array<{ name, email, image? }>` | All users (for @-mentions) |

### UI Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `string` | auto-generated | Custom container ID |
| `hideToolbar` | `boolean` | `false` | Hide the toolbar |
| `rulers` | `boolean` | - | Show/hide rulers |
| `className` | `string` | - | CSS class for wrapper |
| `style` | `CSSProperties` | - | Inline styles |
| `renderLoading` | `() => ReactNode` | - | Custom loading UI |

### Event Callbacks

| Prop | Type | Description |
|------|------|-------------|
| `onReady` | `({ superdoc }) => void` | Editor initialized |
| `onEditorCreate` | `({ editor }) => void` | ProseMirror editor created |
| `onEditorDestroy` | `() => void` | Editor destroyed |
| `onEditorUpdate` | `({ editor }) => void` | Content changed |
| `onContentError` | `(event) => void` | Document parsing error |
| `onException` | `({ error }) => void` | Runtime error |

### Advanced Props

| Prop | Type | Description |
|------|------|-------------|
| `modules` | `object` | Configure collaboration, AI, comments |

## Ref API

Access SuperDoc methods via ref:

```tsx
import { useRef } from 'react';
import { SuperDocEditor, SuperDocRef } from '@superdoc-dev/react';

function Editor() {
  const editorRef = useRef<SuperDocRef>(null);

  const handleExport = async () => {
    await editorRef.current?.getInstance()?.export({ triggerDownload: true });
  };

  return <SuperDocEditor ref={editorRef} document={file} />;
}
```

### Available Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `getInstance()` | `SuperDoc \| null` | Access underlying instance |
| `setDocumentMode(mode)` | `void` | Change mode without rebuild |
| `export(options?)` | `Promise<Blob \| void>` | Export as DOCX |
| `getHTML(options?)` | `string[]` | Get document as HTML |
| `focus()` | `void` | Focus the editor |
| `search(text)` | `SearchResult[]` | Search document |
| `goToSearchResult(match)` | `void` | Navigate to result |
| `setLocked(locked)` | `void` | Lock/unlock editing |
| `toggleRuler()` | `void` | Toggle ruler visibility |

## Common Patterns

### Document Mode Switching

The component handles `documentMode` prop changes efficiently without rebuilding:

```tsx
function Editor() {
  const [mode, setMode] = useState<DocumentMode>('editing');

  return (
    <>
      <button onClick={() => setMode('viewing')}>View</button>
      <button onClick={() => setMode('editing')}>Edit</button>
      <SuperDocEditor document={file} documentMode={mode} />
    </>
  );
}
```

### File Upload

```tsx
function FileEditor() {
  const [file, setFile] = useState<File | null>(null);

  return (
    <>
      <input
        type="file"
        accept=".docx"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />
      {file && <SuperDocEditor document={file} />}
    </>
  );
}
```

### Loading State

```tsx
<SuperDocEditor
  document={file}
  renderLoading={() => <div className="spinner">Loading...</div>}
  onReady={() => console.log('Ready!')}
/>
```

### View-Only Mode

```tsx
<SuperDocEditor
  document={file}
  documentMode="viewing"
  role="viewer"
  hideToolbar
/>
```

### With User Info

```tsx
<SuperDocEditor
  document={file}
  user={{
    name: 'John Doe',
    email: 'john@example.com',
    image: 'https://example.com/avatar.jpg'
  }}
  users={[
    { name: 'Jane Smith', email: 'jane@example.com' },
    { name: 'Bob Wilson', email: 'bob@example.com' },
  ]}
/>
```

## Next.js Integration

The React wrapper handles SSR automatically (renders `null` or `renderLoading()` on server, initializes after hydration).

### App Router (Next.js 13+)

```tsx
// app/editor/page.tsx
'use client';

import { SuperDocEditor } from '@superdoc-dev/react';
import '@superdoc-dev/react/style.css';

export default function EditorPage() {
  return (
    <SuperDocEditor
      document="/sample.docx"
      documentMode="editing"
      style={{ height: '100vh' }}
    />
  );
}
```

### Pages Router

```tsx
// pages/editor.tsx
import { SuperDocEditor } from '@superdoc-dev/react';
import '@superdoc-dev/react/style.css';

export default function EditorPage() {
  return (
    <SuperDocEditor
      document="/sample.docx"
      documentMode="editing"
      style={{ height: '100vh' }}
    />
  );
}
```

### With Dynamic Import (Optional)

For custom loading UI during SSR:

```tsx
'use client';

import dynamic from 'next/dynamic';

const SuperDocEditor = dynamic(
  () => import('@superdoc-dev/react').then(mod => mod.SuperDocEditor),
  {
    ssr: false,
    loading: () => <div>Loading editor...</div>
  }
);
```

### CSS Import in Layout

Import styles once in your layout:

```tsx
// app/layout.tsx
import '@superdoc-dev/react/style.css';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>{children}</body>
    </html>
  );
}
```

## Collaboration Setup

```tsx
import * as Y from 'yjs';
import { WebsocketProvider } from 'y-websocket';

function CollaborativeEditor() {
  const ydoc = useMemo(() => new Y.Doc(), []);
  const provider = useMemo(
    () => new WebsocketProvider('wss://your-server.com', 'doc-id', ydoc),
    [ydoc]
  );

  return (
    <SuperDocEditor
      document={file}
      modules={{
        collaboration: { ydoc, provider },
      }}
    />
  );
}
```

## Props That Trigger Rebuild

These props trigger a full instance rebuild when changed:

| Prop | Reason |
|------|--------|
| `document` | New document to load |
| `user` | User identity changed |
| `users` | Users list changed |
| `modules` | Module configuration changed |
| `role` | Permission level changed |
| `hideToolbar` | Toolbar DOM structure changed |

Other props like `documentMode` and callbacks are handled efficiently without rebuild.

## TypeScript

```tsx
import type {
  SuperDocEditorProps,
  SuperDocRef,
  DocumentMode,
  UserRole,
  SuperDocUser,
  SuperDocModules,
  SuperDocConfig,
  SuperDocInstance,
} from '@superdoc-dev/react';
```

Types are extracted from the `superdoc` package, ensuring they stay in sync.

## Requirements

| Requirement | Version |
|-------------|---------|
| React | 16.8.0+ |
| Node.js | 16+ |

## Examples

| Example | Description |
|---------|-------------|
| [React + TypeScript](https://github.com/superdoc-dev/superdoc/tree/main/examples/getting-started/react) | File upload, mode switching, export |
| [Next.js SSR](https://github.com/superdoc-dev/superdoc/tree/main/examples/integrations/nextjs-ssr) | App Router with SSR support |

## Links

- [Documentation](https://docs.superdoc.dev/getting-started/frameworks/react)
- [Next.js Guide](https://docs.superdoc.dev/getting-started/frameworks/nextjs)
- [GitHub](https://github.com/superdoc-dev/superdoc)
- [npm](https://www.npmjs.com/package/@superdoc-dev/react)
