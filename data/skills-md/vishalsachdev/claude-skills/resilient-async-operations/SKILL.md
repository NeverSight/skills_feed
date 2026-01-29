---
name: resilient-async-operations
description: A comprehensive pattern for handling asynchronous operations in JavaScript/TypeScript applications with automatic cleanup, graceful error handling, and memory leak prevention. Use when building async operations that need timeout control, cancellation support, retry logic, or graceful error handling.
---

# Resilient Async Operations

A comprehensive pattern for handling asynchronous operations in JavaScript/TypeScript applications with automatic cleanup, graceful error handling, and memory leak prevention.

## When to use this skill

- Building React applications with API calls and async operations
- Preventing memory leaks from abandoned promises
- Managing multiple concurrent requests with proper cleanup
- Implementing background operations that shouldn't crash the UI
- Handling timeouts and AbortController lifecycle
- Go-style error handling without try-catch blocks

## Core Patterns

This skill provides 4 complementary utilities:

1. **AbortManager** - Centralized abort controller management with automatic cleanup
2. **safePromise** - Go-style `[data, error]` tuple error handling
3. **backgroundOperation** - Non-blocking operations that log errors without crashing
4. **withTimeout** - Timeout-wrapped promises with abort support

## Implementation

### Step 1: Create Promise Utilities

Create `lib/promise-utils.ts`:

```typescript
/**
 * Utility functions for handling promises and background operations
 */

/**
 * Wraps a promise to handle errors gracefully without crashing
 * Returns a tuple of [data, error] similar to Go error handling
 */
export async function safePromise<T>(
  promise: Promise<T>
): Promise<[T | null, Error | null]> {
  try {
    const data = await promise;
    return [data, null];
  } catch (error) {
    return [null, error instanceof Error ? error : new Error(String(error))];
  }
}

/**
 * Executes a background operation with proper error handling
 * Logs errors but doesn't throw them to prevent crashes
 */
export async function backgroundOperation<T>(
  name: string,
  operation: () => Promise<T>,
  onError?: (error: Error) => void
): Promise<T | null> {
  try {
    return await operation();
  } catch (error) {
    const err = error instanceof Error ? error : new Error(String(error));
    console.error(`Background operation '${name}' failed:`, err);
    onError?.(err);
    return null;
  }
}

/**
 * Creates a timeout-wrapped promise with AbortController support
 */
export function withTimeout<T>(
  promise: Promise<T>,
  timeoutMs: number,
  controller?: AbortController
): Promise<T> {
  return new Promise((resolve, reject) => {
    const timeoutId = setTimeout(() => {
      controller?.abort();
      reject(new Error(`Operation timed out after ${timeoutMs}ms`));
    }, timeoutMs);

    promise
      .then((result) => {
        clearTimeout(timeoutId);
        resolve(result);
      })
      .catch((error) => {
        clearTimeout(timeoutId);
        reject(error);
      });
  });
}

/**
 * Manages multiple AbortControllers with cleanup
 */
export class AbortManager {
  private controllers = new Map<string, AbortController>();
  private timeouts = new Map<string, NodeJS.Timeout>();

  createController(key: string, timeoutMs?: number): AbortController {
    // Cleanup existing controller if any
    this.cleanup(key);

    const controller = new AbortController();
    this.controllers.set(key, controller);

    if (timeoutMs) {
      const timeoutId = setTimeout(() => {
        controller.abort();
        this.controllers.delete(key);
        this.timeouts.delete(key);
      }, timeoutMs);
      this.timeouts.set(key, timeoutId);
    }

    return controller;
  }

  cleanup(key?: string) {
    if (key) {
      const controller = this.controllers.get(key);
      if (controller && !controller.signal.aborted) {
        controller.abort();
      }
      this.controllers.delete(key);

      const timeoutId = this.timeouts.get(key);
      if (timeoutId) {
        clearTimeout(timeoutId);
        this.timeouts.delete(key);
      }
    } else {
      // Cleanup all
      for (const [k] of this.controllers) {
        this.cleanup(k);
      }
    }
  }

  getSignal(key: string): AbortSignal | undefined {
    return this.controllers.get(key)?.signal;
  }
}
```

## Usage Examples

### Example 1: React Component with AbortManager

**Problem**: Prevent memory leaks when component unmounts during async operations.

```typescript
'use client';

import { useEffect, useRef, useState } from 'react';
import { AbortManager } from '@/lib/promise-utils';

export function VideoAnalysis() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const abortManager = useRef(new AbortManager());

  useEffect(() => {
    const fetchData = async () => {
      // Create abort controller with 30s timeout
      const controller = abortManager.current.createController('fetch-video', 30000);

      try {
        const response = await fetch('/api/analyze', {
          signal: controller.signal
        });
        const result = await response.json();
        setData(result);
      } catch (err) {
        if (err.name !== 'AbortError') {
          setError(err.message);
        }
      }
    };

    fetchData();

    // Cleanup on unmount - automatically aborts all pending requests
    return () => {
      abortManager.current.cleanup();
    };
  }, []);

  return <div>{data ? <Results data={data} /> : <Loading />}</div>;
}
```

**Benefits**:
- ✅ Automatic cleanup on unmount
- ✅ No memory leaks from abandoned promises
- ✅ Built-in timeout handling
- ✅ Multiple requests managed centrally

---

### Example 2: Go-Style Error Handling with safePromise

**Problem**: Try-catch blocks add nesting and complexity.

```typescript
import { safePromise } from '@/lib/promise-utils';

// ❌ Old way - nested try-catch
async function fetchUserOld(id: string) {
  try {
    const response = await fetch(`/api/users/${id}`);
    try {
      const data = await response.json();
      return { success: true, data };
    } catch (parseError) {
      return { success: false, error: 'Failed to parse response' };
    }
  } catch (fetchError) {
    return { success: false, error: 'Failed to fetch user' };
  }
}

// ✅ New way - clean and predictable
async function fetchUser(id: string) {
  const [response, fetchError] = await safePromise(
    fetch(`/api/users/${id}`)
  );

  if (fetchError) {
    return { success: false, error: 'Failed to fetch user' };
  }

  const [data, parseError] = await safePromise(response.json());

  if (parseError) {
    return { success: false, error: 'Failed to parse response' };
  }

  return { success: true, data };
}
```

**Benefits**:
- ✅ No try-catch nesting
- ✅ Explicit error handling at each step
- ✅ Type-safe error objects
- ✅ Linear code flow

---

### Example 3: Background Operations

**Problem**: Non-critical operations (analytics, logging, DB saves) shouldn't crash the UI if they fail.

```typescript
import { backgroundOperation } from '@/lib/promise-utils';

async function handleVideoAnalysis(videoId: string) {
  // Critical operation - let errors bubble up
  const analysis = await generateAnalysis(videoId);

  // Show results to user immediately
  displayResults(analysis);

  // Non-critical background operations - fire and forget
  backgroundOperation('save-to-db', async () => {
    await saveToDatabase(analysis);
  });

  backgroundOperation('generate-suggestions', async () => {
    const questions = await generateQuestions(analysis);
    updateUI(questions); // Update UI when ready, but don't block
  });

  backgroundOperation('track-analytics', async () => {
    await trackEvent('video-analyzed', { videoId });
  });

  // User sees results immediately, background tasks run without blocking
}
```

**Benefits**:
- ✅ UI doesn't wait for non-critical operations
- ✅ Errors logged but don't crash app
- ✅ Optional error callbacks for monitoring
- ✅ Better perceived performance

---

### Example 4: Timeout Handling

**Problem**: Prevent requests from hanging forever.

```typescript
import { withTimeout, AbortManager } from '@/lib/promise-utils';

async function fetchWithTimeout() {
  const abortManager = new AbortManager();
  const controller = abortManager.createController('fetch');

  try {
    // Fetch with 5 second timeout
    const response = await withTimeout(
      fetch('/api/slow-endpoint', { signal: controller.signal }),
      5000,
      controller
    );

    return await response.json();
  } catch (error) {
    if (error.message.includes('timeout')) {
      console.error('Request timed out after 5 seconds');
    }
    throw error;
  } finally {
    abortManager.cleanup();
  }
}
```

---

### Example 5: Complex Multi-Stage Loading

**Problem**: Manage multiple concurrent requests with different priorities and cleanup.

```typescript
import { AbortManager, backgroundOperation, safePromise } from '@/lib/promise-utils';

export function useVideoAnalysis(videoId: string) {
  const [state, setState] = useState('loading');
  const abortManager = useRef(new AbortManager());

  useEffect(() => {
    const analyze = async () => {
      // Stage 1: Critical data - wait for these
      const controller1 = abortManager.current.createController('transcript', 30000);
      const controller2 = abortManager.current.createController('metadata', 10000);

      const [transcript, transcriptError] = await safePromise(
        fetch('/api/transcript', { signal: controller1.signal })
          .then(r => r.json())
      );

      const [metadata, metadataError] = await safePromise(
        fetch('/api/metadata', { signal: controller2.signal })
          .then(r => r.json())
      );

      if (transcriptError || metadataError) {
        setState({ status: 'error', error: transcriptError || metadataError });
        return;
      }

      // Show data immediately
      setState({ status: 'ready', transcript, metadata });

      // Stage 2: Non-critical enhancements - background
      backgroundOperation('generate-summary', async () => {
        const controller3 = abortManager.current.createController('summary', 60000);
        const summary = await fetch('/api/summary', {
          signal: controller3.signal
        }).then(r => r.json());

        setState(prev => ({ ...prev, summary }));
      });

      backgroundOperation('suggested-questions', async () => {
        const controller4 = abortManager.current.createController('questions', 30000);
        const questions = await fetch('/api/questions', {
          signal: controller4.signal
        }).then(r => r.json());

        setState(prev => ({ ...prev, questions }));
      });
    };

    analyze();

    return () => {
      abortManager.current.cleanup(); // Abort all pending requests
    };
  }, [videoId]);

  return state;
}
```

**Benefits**:
- ✅ Fast initial load (critical data only)
- ✅ Progressive enhancement (background data)
- ✅ Automatic cleanup on navigation
- ✅ All requests have timeouts
- ✅ Proper error handling at each stage

---

## Advanced Patterns

### Pattern 1: Retry with Exponential Backoff

```typescript
import { safePromise } from '@/lib/promise-utils';

async function fetchWithRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3,
  baseDelay = 1000
): Promise<T> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    const [data, error] = await safePromise(fn());

    if (!error) return data;

    if (attempt < maxRetries - 1) {
      const delay = baseDelay * Math.pow(2, attempt);
      console.log(`Retry ${attempt + 1}/${maxRetries} after ${delay}ms`);
      await new Promise(resolve => setTimeout(resolve, delay));
    } else {
      throw error;
    }
  }

  throw new Error('All retries failed');
}

// Usage
const data = await fetchWithRetry(() => fetch('/api/data').then(r => r.json()));
```

---

### Pattern 2: Parallel Operations with AllSettled

```typescript
import { backgroundOperation } from '@/lib/promise-utils';

async function saveAnalysis(analysis) {
  // Run multiple save operations in parallel
  const results = await Promise.allSettled([
    saveToDatabase(analysis),
    saveToCache(analysis),
    notifyWebhooks(analysis)
  ]);

  // Log failures but don't crash
  results.forEach((result, index) => {
    if (result.status === 'rejected') {
      const operations = ['database', 'cache', 'webhooks'];
      console.error(`Failed to save to ${operations[index]}:`, result.reason);
    }
  });

  // Return success if at least database save succeeded
  return results[0].status === 'fulfilled';
}
```

---

### Pattern 3: Debounced Async Operations

```typescript
import { AbortManager } from '@/lib/promise-utils';

function useDebouncedSearch() {
  const abortManager = useRef(new AbortManager());
  const timeoutRef = useRef<NodeJS.Timeout>();

  const search = useCallback((query: string) => {
    // Clear previous timeout and abort previous request
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
    abortManager.current.cleanup('search');

    // Debounce 300ms
    timeoutRef.current = setTimeout(async () => {
      const controller = abortManager.current.createController('search', 10000);

      try {
        const response = await fetch(`/api/search?q=${query}`, {
          signal: controller.signal
        });
        const results = await response.json();
        setResults(results);
      } catch (error) {
        if (error.name !== 'AbortError') {
          console.error('Search failed:', error);
        }
      }
    }, 300);
  }, []);

  useEffect(() => {
    return () => {
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
      abortManager.current.cleanup();
    };
  }, []);

  return search;
}
```

---

## Best Practices

1. **Always cleanup AbortManager** in useEffect return or component unmount
2. **Use safePromise** for operations where you want explicit error handling
3. **Use backgroundOperation** for non-critical tasks (analytics, logging, cache updates)
4. **Set appropriate timeouts** - don't let requests hang forever
5. **Handle AbortError separately** - it's not a real error, just cancellation
6. **Combine patterns** - safePromise + backgroundOperation + AbortManager work great together

## Common Pitfalls

1. **Forgetting to cleanup AbortManager**: Always call `cleanup()` in unmount
2. **Not handling AbortError**: Check `error.name !== 'AbortError'` before showing errors
3. **Using backgroundOperation for critical operations**: Only use for non-critical tasks
4. **Creating new AbortManager in render**: Use `useRef` to persist across renders
5. **Not setting timeouts**: Always set reasonable timeouts to prevent hanging

## TypeScript Tips

```typescript
// Type-safe safePromise
interface User { id: string; name: string; }

const [user, error] = await safePromise<User>(fetchUser());
//     ^User | null      ^Error | null

if (error) {
  // error is Error
  console.error(error.message);
} else {
  // user is User
  console.log(user.name);
}

// Generic backgroundOperation
await backgroundOperation<void>('track', async () => {
  await trackEvent('click');
});

await backgroundOperation<AnalysisResult>('analyze', async () => {
  return await analyzeVideo();
});
```

## Testing

```typescript
// Mock AbortManager in tests
const mockAbortManager = {
  createController: jest.fn(() => new AbortController()),
  cleanup: jest.fn(),
  getSignal: jest.fn()
};

// Test cleanup
test('cleans up on unmount', () => {
  const { unmount } = render(<Component />);
  unmount();
  expect(mockAbortManager.cleanup).toHaveBeenCalled();
});

// Test timeout
test('aborts on timeout', async () => {
  jest.useFakeTimers();
  const promise = withTimeout(
    new Promise(resolve => setTimeout(resolve, 10000)),
    5000
  );

  jest.advanceTimersByTime(5000);

  await expect(promise).rejects.toThrow('timeout');
});
```

## Next Steps

After implementing this skill:

1. Audit existing code for memory leaks (unmounted components with pending promises)
2. Replace try-catch chains with safePromise
3. Move non-critical operations to backgroundOperation
4. Add timeouts to all fetch calls
5. Centralize abort controller management with AbortManager

## Related Skills

- **Secure Next.js API Routes** - Combine with rate limiting and security
- **Type-Safe Form Validation** - Use safePromise for form submissions
- **Complex State Management** - Manage loading states with AbortManager

---

Built from production patterns in [TLDW](https://github.com/vishalsachdev/tldw)
