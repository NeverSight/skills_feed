---
name: backend-compression
description: Add response compression (gzip/deflate) to the backend for improved performance. Use when asked to "add compression", "enable gzip", or "optimize response size".
---

# Backend Response Compression

This skill adds response compression to a Koa backend using `koa-compress`.

## Overview

Response compression reduces payload size for text-based content (JSON, HTML, JS, CSS), improving network performance especially for mobile clients.

## Installation

```bash
npm install koa-compress
```

## Implementation

Add to `apps/backend/src/main.ts`:

```typescript
import compress from 'koa-compress';
import { constants as zlibConstants } from 'zlib';

// Add compression middleware (before routes)
app.use(
  compress({
    filter(content_type) {
      // Compress JSON, text, and other compressible types
      return /text|json|javascript|xml|svg/i.test(content_type);
    },
    threshold: 1024, // Only compress responses larger than 1KB
    gzip: {
      flush: zlibConstants.Z_SYNC_FLUSH,
    },
    deflate: {
      flush: zlibConstants.Z_SYNC_FLUSH,
    },
    br: false, // Disable brotli (CPU intensive, gzip is sufficient)
  })
);
```

## Configuration Options

### Filter

Only compress text-based content types:

```typescript
filter(content_type) {
  return /text|json|javascript|xml|svg/i.test(content_type);
}
```

**Why?** Binary content (images, videos, PDFs) is already compressed. Attempting to compress them wastes CPU and can actually increase size.

### Threshold

```typescript
threshold: 1024, // 1KB minimum
```

**Why?** Small responses have minimal benefit from compression, but still incur CPU cost. 1KB is a good balance.

### Brotli

```typescript
br: false,
```

**Why?** Brotli provides better compression but is significantly more CPU intensive. For most APIs, gzip provides sufficient compression with lower server load. Enable brotli only if:
- You have CPU headroom
- Your responses are large and benefit from higher compression ratios
- Your clients primarily support brotli

### Flush Mode

```typescript
gzip: {
  flush: zlibConstants.Z_SYNC_FLUSH,
},
```

**Why?** `Z_SYNC_FLUSH` ensures data is flushed immediately, important for streaming responses and keeping memory usage predictable.

## Middleware Order

Add compression early in the middleware chain, but after logging:

```typescript
// 1. Error handling
app.use(errorHandler);

// 2. Logging
app.use(requestLogger);

// 3. Compression (before routes)
app.use(compress({ ... }));

// 4. Body parsing
app.use(bodyParser());

// 5. Routes
app.use(mount('/api/resources', resourceRoutes.routes()));
```

## Testing Compression

Verify compression is working:

```bash
# Request with gzip support
curl -H "Accept-Encoding: gzip" -I http://localhost:3000/api/resources

# Should see: Content-Encoding: gzip
```

## Checklist

1. **Install** `koa-compress`: `npm install koa-compress`
2. **Add middleware** to `main.ts` before routes
3. **Verify** with curl that `Content-Encoding: gzip` header is present
