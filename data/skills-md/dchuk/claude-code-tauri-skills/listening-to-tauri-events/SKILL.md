---
name: listening-to-tauri-events
description: Teaches how to subscribe to and listen for Tauri events in the frontend using the events API, including typed event handlers and cleanup patterns.
---

# Listening to Tauri Events in the Frontend

This skill covers how to subscribe to events emitted from Rust in a Tauri v2 application using the `@tauri-apps/api/event` module.

## Core Concepts

Tauri provides two event scopes:

1. **Global events** - Broadcast to all listeners across all webviews
2. **Webview-specific events** - Targeted to specific webview windows

**Important:** Webview-specific events are NOT received by global listeners. Use the appropriate listener type based on how events are emitted from Rust.

## Installation

The event API is part of the core Tauri API package:

```bash
npm install @tauri-apps/api
# or
pnpm add @tauri-apps/api
# or
yarn add @tauri-apps/api
```

## Global Event Listening

### Basic Listen Pattern

```typescript
import { listen } from '@tauri-apps/api/event';

// Listen for a global event
const unlisten = await listen('download-started', (event) => {
  console.log('Event received:', event.payload);
});

// Clean up when done
unlisten();
```

### Typed Event Payloads

Define TypeScript interfaces matching your Rust payload structures:

```typescript
import { listen } from '@tauri-apps/api/event';

// Define the payload type (matches Rust struct with camelCase)
interface DownloadStarted {
  url: string;
  downloadId: number;
  contentLength: number;
}

// Use generic type parameter for type safety
const unlisten = await listen<DownloadStarted>('download-started', (event) => {
  console.log(`Downloading from ${event.payload.url}`);
  console.log(`Content length: ${event.payload.contentLength} bytes`);
  console.log(`Download ID: ${event.payload.downloadId}`);
});
```

### Event Object Structure

The event callback receives an `Event<T>` object:

```typescript
interface Event<T> {
  /** Event name */
  event: string;
  /** Event identifier */
  id: number;
  /** Event payload (your custom type) */
  payload: T;
}
```

## Webview-Specific Event Listening

For events emitted with `emit_to` or `emit_filter` targeting specific webviews:

```typescript
import { getCurrentWebviewWindow } from '@tauri-apps/api/webviewWindow';

const appWebview = getCurrentWebviewWindow();

// Listen for events targeted to this specific webview
const unlisten = await appWebview.listen<string>('login-result', (event) => {
  if (event.payload === 'loggedIn') {
    localStorage.setItem('authenticated', 'true');
  } else {
    console.error('Login failed:', event.payload);
  }
});
```

## One-Time Event Listeners

Use `once` for events that should only be handled a single time:

```typescript
import { once } from '@tauri-apps/api/event';
import { getCurrentWebviewWindow } from '@tauri-apps/api/webviewWindow';

// Global one-time listener
await once('app-ready', (event) => {
  console.log('Application is ready');
});

// Webview-specific one-time listener
const appWebview = getCurrentWebviewWindow();
await appWebview.once('initialized', (event) => {
  console.log('Webview initialized');
});
```

## Cleanup and Unsubscription

### Manual Cleanup

Always unsubscribe listeners when they are no longer needed:

```typescript
import { listen } from '@tauri-apps/api/event';

const unlisten = await listen('my-event', (event) => {
  // Handle event
});

// Later, when done listening
unlisten();
```

### React Component Cleanup

```typescript
import { useEffect } from 'react';
import { listen } from '@tauri-apps/api/event';

interface ProgressPayload {
  percent: number;
  message: string;
}

function DownloadProgress() {
  useEffect(() => {
    let unlisten: (() => void) | undefined;

    const setupListener = async () => {
      unlisten = await listen<ProgressPayload>('download-progress', (event) => {
        console.log(`Progress: ${event.payload.percent}%`);
      });
    };

    setupListener();

    // Cleanup when component unmounts
    return () => {
      if (unlisten) {
        unlisten();
      }
    };
  }, []);

  return <div>Listening for progress...</div>;
}
```

### Vue Composition API Cleanup

```typescript
import { onMounted, onUnmounted } from 'vue';
import { listen } from '@tauri-apps/api/event';

interface NotificationPayload {
  title: string;
  body: string;
}

export default {
  setup() {
    let unlisten: (() => void) | undefined;

    onMounted(async () => {
      unlisten = await listen<NotificationPayload>('notification', (event) => {
        console.log(`${event.payload.title}: ${event.payload.body}`);
      });
    });

    onUnmounted(() => {
      if (unlisten) {
        unlisten();
      }
    });
  }
};
```

### Svelte Cleanup

```svelte
<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { listen } from '@tauri-apps/api/event';

  interface StatusPayload {
    status: 'idle' | 'loading' | 'complete';
  }

  let unlisten: (() => void) | undefined;

  onMount(async () => {
    unlisten = await listen<StatusPayload>('status-change', (event) => {
      console.log('Status:', event.payload.status);
    });
  });

  onDestroy(() => {
    if (unlisten) {
      unlisten();
    }
  });
</script>
```

## Automatic Listener Cleanup

Tauri automatically clears listeners in these scenarios:

- **Page reload** - All listeners are cleared
- **URL navigation** - Listeners are cleared (except in SPA routers)

**Warning:** Single Page Application routers that do not trigger full page reloads will NOT automatically clean up listeners. You must manually unsubscribe.

## Multiple Event Listeners

### Listening to Multiple Events

```typescript
import { listen } from '@tauri-apps/api/event';

interface DownloadEvent {
  url: string;
}

interface ProgressEvent {
  percent: number;
}

interface CompleteEvent {
  path: string;
  size: number;
}

async function setupDownloadListeners() {
  const unlisteners: Array<() => void> = [];

  unlisteners.push(
    await listen<DownloadEvent>('download-started', (event) => {
      console.log(`Started downloading: ${event.payload.url}`);
    })
  );

  unlisteners.push(
    await listen<ProgressEvent>('download-progress', (event) => {
      console.log(`Progress: ${event.payload.percent}%`);
    })
  );

  unlisteners.push(
    await listen<CompleteEvent>('download-complete', (event) => {
      console.log(`Complete: ${event.payload.path} (${event.payload.size} bytes)`);
    })
  );

  // Return cleanup function
  return () => {
    unlisteners.forEach((unlisten) => unlisten());
  };
}

// Usage
const cleanup = await setupDownloadListeners();
// Later...
cleanup();
```

## Type Definitions Reference

### Creating Typed Event Helpers

```typescript
import { listen, once, Event } from '@tauri-apps/api/event';

// Define all your event types in one place
export interface AppEvents {
  'download-started': { url: string; downloadId: number };
  'download-progress': { downloadId: number; percent: number };
  'download-complete': { downloadId: number; path: string };
  'download-error': { downloadId: number; error: string };
  'notification': { title: string; body: string };
}

// Type-safe listen helper
export async function listenTyped<K extends keyof AppEvents>(
  eventName: K,
  handler: (event: Event<AppEvents[K]>) => void
): Promise<() => void> {
  return listen<AppEvents[K]>(eventName, handler);
}

// Usage
const unlisten = await listenTyped('download-started', (event) => {
  // event.payload is typed as { url: string; downloadId: number }
  console.log(event.payload.url);
});
```

## Corresponding Rust Emit Code

For reference, here is how events are emitted from Rust:

### Global Emit

```rust
use tauri::{AppHandle, Emitter};
use serde::Serialize;

#[derive(Clone, Serialize)]
#[serde(rename_all = "camelCase")]
struct DownloadStarted {
    url: String,
    download_id: usize,
    content_length: usize,
}

#[tauri::command]
fn start_download(app: AppHandle, url: String) {
    app.emit("download-started", DownloadStarted {
        url,
        download_id: 1,
        content_length: 1024,
    }).unwrap();
}
```

### Webview-Specific Emit

```rust
use tauri::{AppHandle, Emitter};

#[tauri::command]
fn notify_window(app: AppHandle, window_label: &str, message: String) {
    // Emit to a specific webview by label
    app.emit_to(window_label, "notification", message).unwrap();
}
```

### Filtered Emit

```rust
use tauri::{AppHandle, Emitter, EventTarget};

#[tauri::command]
fn broadcast_to_editors(app: AppHandle, content: String) {
    app.emit_filter("content-update", content, |target| {
        match target {
            EventTarget::WebviewWindow { label } => {
                label.starts_with("editor-")
            }
            _ => false,
        }
    }).unwrap();
}
```

## Best Practices

1. **Always define TypeScript interfaces** for event payloads to catch type mismatches at compile time

2. **Use `serde(rename_all = "camelCase")`** in Rust structs to match JavaScript naming conventions

3. **Store unlisten functions** and call them during cleanup to prevent memory leaks

4. **Use `once` for initialization events** that only fire a single time

5. **Match listener scope to emit scope** - use webview-specific listeners for `emit_to` events

6. **Centralize event type definitions** in a shared module for consistency

## Common Patterns

### Event Bus Pattern

```typescript
import { listen, Event } from '@tauri-apps/api/event';

type EventHandler<T> = (payload: T) => void;

class TauriEventBus {
  private unlisteners: Map<string, () => void> = new Map();

  async subscribe<T>(event: string, handler: EventHandler<T>): Promise<void> {
    if (this.unlisteners.has(event)) {
      this.unlisteners.get(event)!();
    }

    const unlisten = await listen<T>(event, (e: Event<T>) => {
      handler(e.payload);
    });

    this.unlisteners.set(event, unlisten);
  }

  unsubscribe(event: string): void {
    const unlisten = this.unlisteners.get(event);
    if (unlisten) {
      unlisten();
      this.unlisteners.delete(event);
    }
  }

  unsubscribeAll(): void {
    this.unlisteners.forEach((unlisten) => unlisten());
    this.unlisteners.clear();
  }
}

export const eventBus = new TauriEventBus();
```

### React Hook Pattern

```typescript
import { useEffect, useState } from 'react';
import { listen, Event } from '@tauri-apps/api/event';

export function useTauriEvent<T>(eventName: string, initialValue: T): T {
  const [value, setValue] = useState<T>(initialValue);

  useEffect(() => {
    let unlisten: (() => void) | undefined;

    listen<T>(eventName, (event: Event<T>) => {
      setValue(event.payload);
    }).then((fn) => {
      unlisten = fn;
    });

    return () => {
      if (unlisten) {
        unlisten();
      }
    };
  }, [eventName]);

  return value;
}

// Usage
function StatusDisplay() {
  const status = useTauriEvent<string>('app-status', 'initializing');
  return <div>Status: {status}</div>;
}
```
