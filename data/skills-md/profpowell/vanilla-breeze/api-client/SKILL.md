---
name: api-client
description: Fetch API patterns with error handling, retry logic, and caching. Use when building API integrations, handling network failures, or implementing offline-first data fetching.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# API Client Skill

Patterns for fetch-based API communication with robust error handling, retry logic, and response caching.

## Philosophy

1. **Native `fetch()` only** - No axios or other libraries
2. **Errors should be explicit** - No swallowed promises
3. **Requests should be cancellable** - Use AbortController
4. **Fail gracefully** - Handle network issues elegantly

---

## Base Fetch Wrapper

A typed wrapper around fetch with consistent error handling:

```javascript
/**
 * @typedef {Object} ApiError
 * @property {number} status - HTTP status code
 * @property {string} statusText - HTTP status text
 * @property {Object} [body] - Parsed error response body
 * @property {string} message - Error message
 */

/**
 * Custom error class for API failures
 */
class ApiError extends Error {
  /**
   * @param {Response} response
   * @param {Object} [body]
   */
  constructor(response, body = null) {
    super(`API Error: ${response.status} ${response.statusText}`);
    this.name = 'ApiError';
    this.status = response.status;
    this.statusText = response.statusText;
    this.body = body;
  }
}

/**
 * Base fetch wrapper with consistent error handling
 * @template T
 * @param {string} endpoint
 * @param {RequestInit} [options={}]
 * @returns {Promise<T>}
 * @throws {ApiError}
 */
async function api(endpoint, options = {}) {
  const response = await fetch(endpoint, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers
    },
    ...options
  });

  if (!response.ok) {
    let body = null;
    try {
      body = await response.json();
    } catch {
      // Response may not be JSON
    }
    throw new ApiError(response, body);
  }

  // Handle empty responses (204 No Content)
  if (response.status === 204) {
    return /** @type {T} */ (null);
  }

  return response.json();
}
```

### Usage

```javascript
// GET request
const user = await api('/api/users/123');

// POST request
const newUser = await api('/api/users', {
  method: 'POST',
  body: JSON.stringify({ name: 'Alice', email: 'alice@example.com' })
});

// With error handling
try {
  const data = await api('/api/protected');
} catch (error) {
  if (error instanceof ApiError) {
    if (error.status === 401) {
      // Redirect to login
    } else if (error.status === 404) {
      // Show not found
    }
  }
  throw error;
}
```

---

## Error Handling Patterns

### Typed Error Responses

```javascript
/**
 * @typedef {'validation' | 'auth' | 'not_found' | 'server'} ErrorType
 */

/**
 * @typedef {Object} ValidationError
 * @property {'validation'} type
 * @property {Object<string, string[]>} errors - Field-level errors
 */

/**
 * Check error type and handle appropriately
 * @param {ApiError} error
 */
function handleApiError(error) {
  const body = error.body;

  if (error.status === 400 && body?.type === 'validation') {
    // Show field-level errors
    Object.entries(body.errors).forEach(([field, messages]) => {
      console.error(`${field}: ${messages.join(', ')}`);
    });
    return;
  }

  if (error.status === 401) {
    // Redirect to login
    window.location.href = '/login';
    return;
  }

  if (error.status === 403) {
    // Show permission denied
    showNotification('You do not have permission for this action');
    return;
  }

  if (error.status >= 500) {
    // Show generic server error
    showNotification('Something went wrong. Please try again later.');
    return;
  }

  // Unknown error - log and show generic message
  console.error('Unexpected API error:', error);
  showNotification('An unexpected error occurred');
}
```

### Error Boundary Integration

```javascript
/**
 * Report error to monitoring service
 * @param {Error} error
 * @param {Object} [context]
 */
function reportError(error, context = {}) {
  // Use sendBeacon for reliability
  navigator.sendBeacon('/api/errors', JSON.stringify({
    message: error.message,
    stack: error.stack,
    status: error instanceof ApiError ? error.status : undefined,
    url: window.location.href,
    timestamp: Date.now(),
    ...context
  }));
}
```

---

## Retry with Exponential Backoff

```javascript
/**
 * @typedef {Object} RetryOptions
 * @property {number} [retries=3] - Maximum retry attempts
 * @property {number} [delay=1000] - Initial delay in ms
 * @property {(status: number) => boolean} [retryOn] - Function to determine if status should retry
 */

/**
 * Fetch with automatic retry on failure
 * @template T
 * @param {string} url
 * @param {RequestInit} [options={}]
 * @param {RetryOptions} [retryOptions={}]
 * @returns {Promise<T>}
 */
async function fetchWithRetry(url, options = {}, retryOptions = {}) {
  const {
    retries = 3,
    delay = 1000,
    retryOn = (status) => status >= 500 && status <= 504
  } = retryOptions;

  let lastError;

  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      return await api(url, options);
    } catch (error) {
      lastError = error;

      // Don't retry on client errors or if not a retryable status
      if (error instanceof ApiError && !retryOn(error.status)) {
        throw error;
      }

      // Don't retry if we've exhausted attempts
      if (attempt === retries) {
        throw error;
      }

      // Exponential backoff: 1s, 2s, 4s, 8s...
      const backoff = delay * Math.pow(2, attempt);
      await new Promise(resolve => setTimeout(resolve, backoff));
    }
  }

  throw lastError;
}
```

### Usage

```javascript
// Retry up to 3 times with exponential backoff
const data = await fetchWithRetry('/api/unstable-endpoint', {}, {
  retries: 3,
  delay: 1000,
  retryOn: (status) => status === 503 || status === 429
});
```

---

## Request Cancellation

### Timeout Pattern

```javascript
/**
 * Fetch with automatic timeout
 * @template T
 * @param {string} url
 * @param {RequestInit & {timeout?: number}} [options={}]
 * @returns {Promise<T>}
 */
async function fetchWithTimeout(url, options = {}) {
  const { timeout = 10000, ...fetchOptions } = options;

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    return await api(url, {
      ...fetchOptions,
      signal: controller.signal
    });
  } catch (error) {
    if (error.name === 'AbortError') {
      throw new Error(`Request timed out after ${timeout}ms`);
    }
    throw error;
  } finally {
    clearTimeout(timeoutId);
  }
}
```

### Component Cleanup

```javascript
class DataComponent extends HTMLElement {
  /** @type {AbortController | null} */
  #controller = null;

  async connectedCallback() {
    this.#controller = new AbortController();

    try {
      const data = await api('/api/data', {
        signal: this.#controller.signal
      });
      this.render(data);
    } catch (error) {
      if (error.name === 'AbortError') {
        // Component was disconnected - ignore
        return;
      }
      this.renderError(error);
    }
  }

  disconnectedCallback() {
    // Cancel any in-flight requests
    this.#controller?.abort();
  }
}
```

---

## Response Caching

### In-Memory Cache with TTL

```javascript
/**
 * @typedef {Object} CacheEntry
 * @property {*} data
 * @property {number} expires
 */

/**
 * Create a cached fetch function
 * @param {number} ttl - Time to live in milliseconds
 * @returns {<T>(url: string, options?: RequestInit) => Promise<T>}
 */
function createCachedFetch(ttl = 60000) {
  /** @type {Map<string, CacheEntry>} */
  const cache = new Map();

  return async function cachedFetch(url, options = {}) {
    // Only cache GET requests
    const method = options.method?.toUpperCase() || 'GET';
    if (method !== 'GET') {
      return api(url, options);
    }

    const cacheKey = url;
    const cached = cache.get(cacheKey);

    if (cached && cached.expires > Date.now()) {
      return cached.data;
    }

    const data = await api(url, options);

    cache.set(cacheKey, {
      data,
      expires: Date.now() + ttl
    });

    return data;
  };
}
```

### Cache Invalidation

```javascript
/**
 * Create a cache manager with invalidation
 */
function createCacheManager(ttl = 60000) {
  const cache = new Map();

  return {
    async fetch(url, options = {}) {
      // Same caching logic as above
    },

    /**
     * Invalidate specific URL
     * @param {string} url
     */
    invalidate(url) {
      cache.delete(url);
    },

    /**
     * Invalidate URLs matching pattern
     * @param {RegExp} pattern
     */
    invalidatePattern(pattern) {
      for (const key of cache.keys()) {
        if (pattern.test(key)) {
          cache.delete(key);
        }
      }
    },

    /**
     * Clear entire cache
     */
    clear() {
      cache.clear();
    }
  };
}
```

---

## Request Deduplication

Prevent duplicate in-flight requests:

```javascript
/**
 * Create a deduplicated fetch function
 * @returns {<T>(url: string, options?: RequestInit) => Promise<T>}
 */
function createDedupedFetch() {
  /** @type {Map<string, Promise<*>>} */
  const pending = new Map();

  return async function dedupedFetch(url, options = {}) {
    const method = options.method?.toUpperCase() || 'GET';

    // Only dedupe GET requests
    if (method !== 'GET') {
      return api(url, options);
    }

    const key = url;

    // Return existing promise if request is in-flight
    if (pending.has(key)) {
      return pending.get(key);
    }

    // Create new request
    const promise = api(url, options).finally(() => {
      pending.delete(key);
    });

    pending.set(key, promise);
    return promise;
  };
}
```

### Usage

```javascript
const dedupedFetch = createDedupedFetch();

// These will only make ONE network request
const [user1, user2, user3] = await Promise.all([
  dedupedFetch('/api/users/123'),
  dedupedFetch('/api/users/123'),
  dedupedFetch('/api/users/123')
]);
```

---

## Offline Queue

Queue failed mutations for retry when online:

```javascript
/**
 * @typedef {Object} QueuedRequest
 * @property {string} url
 * @property {RequestInit} options
 * @property {number} timestamp
 */

/**
 * Create an offline-capable mutation queue
 */
function createOfflineQueue() {
  const STORAGE_KEY = 'offline-queue';

  /**
   * Load queue from storage
   * @returns {QueuedRequest[]}
   */
  function loadQueue() {
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored ? JSON.parse(stored) : [];
  }

  /**
   * Save queue to storage
   * @param {QueuedRequest[]} queue
   */
  function saveQueue(queue) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(queue));
  }

  /**
   * Add request to queue
   * @param {string} url
   * @param {RequestInit} options
   */
  function enqueue(url, options) {
    const queue = loadQueue();
    queue.push({ url, options, timestamp: Date.now() });
    saveQueue(queue);
  }

  /**
   * Process all queued requests
   */
  async function flush() {
    const queue = loadQueue();
    const failed = [];

    for (const request of queue) {
      try {
        await api(request.url, request.options);
      } catch (error) {
        // Keep failed requests for next attempt
        failed.push(request);
      }
    }

    saveQueue(failed);
  }

  // Auto-flush when coming online
  window.addEventListener('online', flush);

  return {
    /**
     * Execute request, queue if offline
     * @template T
     * @param {string} url
     * @param {RequestInit} options
     * @returns {Promise<T>}
     */
    async execute(url, options) {
      if (!navigator.onLine) {
        enqueue(url, options);
        throw new Error('Request queued - you are offline');
      }

      try {
        return await api(url, options);
      } catch (error) {
        // Queue network errors for retry
        if (error.name === 'TypeError') {
          enqueue(url, options);
          throw new Error('Request queued - network error');
        }
        throw error;
      }
    },

    flush,
    getQueue: loadQueue
  };
}
```

---

## Complete API Client

Combining all patterns:

```javascript
/**
 * Create a full-featured API client
 * @param {Object} config
 * @param {string} config.baseUrl
 * @param {number} [config.timeout=10000]
 * @param {number} [config.cacheTtl=60000]
 * @param {number} [config.retries=3]
 */
function createApiClient(config) {
  const { baseUrl, timeout = 10000, cacheTtl = 60000, retries = 3 } = config;

  const cache = new Map();
  const pending = new Map();

  /**
   * @template T
   * @param {string} endpoint
   * @param {RequestInit & {skipCache?: boolean}} [options={}]
   * @returns {Promise<T>}
   */
  async function request(endpoint, options = {}) {
    const url = `${baseUrl}${endpoint}`;
    const method = options.method?.toUpperCase() || 'GET';
    const { skipCache = false, ...fetchOptions } = options;

    // Check cache for GET requests
    if (method === 'GET' && !skipCache) {
      const cached = cache.get(url);
      if (cached && cached.expires > Date.now()) {
        return cached.data;
      }
    }

    // Dedupe GET requests
    if (method === 'GET' && pending.has(url)) {
      return pending.get(url);
    }

    // Set up abort controller for timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    const promise = fetchWithRetry(url, {
      ...fetchOptions,
      signal: controller.signal
    }, { retries })
      .then(data => {
        // Cache GET responses
        if (method === 'GET') {
          cache.set(url, { data, expires: Date.now() + cacheTtl });
        }
        return data;
      })
      .finally(() => {
        clearTimeout(timeoutId);
        pending.delete(url);
      });

    if (method === 'GET') {
      pending.set(url, promise);
    }

    return promise;
  }

  return {
    get: (endpoint, options) => request(endpoint, options),
    post: (endpoint, body, options) => request(endpoint, {
      method: 'POST',
      body: JSON.stringify(body),
      ...options
    }),
    put: (endpoint, body, options) => request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(body),
      ...options
    }),
    delete: (endpoint, options) => request(endpoint, {
      method: 'DELETE',
      ...options
    }),
    invalidateCache: (pattern) => {
      for (const key of cache.keys()) {
        if (key.includes(pattern)) {
          cache.delete(key);
        }
      }
    }
  };
}
```

---

## API Client Checklist

When implementing API calls:

- [ ] All requests have a timeout
- [ ] AbortController used for cancellation
- [ ] Errors include status code and parsed body
- [ ] Retry only on safe/idempotent operations
- [ ] Cache keys include all relevant parameters
- [ ] Component cleanup aborts in-flight requests
- [ ] Consider offline queue for mutations
- [ ] Use JSDoc types for request/response shapes

## Related Skills

- **state-management** - Client-side state patterns for Web Components
- **authentication** - Implement secure authentication with JWT, sessions, OAuth...
- **rest-api** - Write REST API endpoints with HTTP methods, status codes,...
- **observability** - Implement error tracking, performance monitoring, and use...
