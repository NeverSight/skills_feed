---
name: image-compression
description: "Client-side image compression before upload using Squoosh with Canvas fallback and server-side Sharp validation. Use for web apps needing max width 1920px, max size 512KB, transparent UX, and consistent compression stats."
---

# Image Compression

Seamless image compression prior to upload with a hybrid approach:
- **Client primary:** Squoosh (WASM)
- **Client fallback:** Canvas API
- **Server safety net:** Sharp

**Defaults:** max width $1920$px, max size $512$ KB, quality $75$ (adjust down to hit size).

## When to Use

✅ Web apps that upload user images and must reduce bandwidth
✅ Need transparent UX (no user action)
✅ Want modern codecs but must support older browsers

## When Not to Use

❌ Server-only batch pipelines (use Sharp directly)
❌ Large-scale media processing with complex transforms (use ImageMagick/FFmpeg)

## Core Rules

1. Maintain aspect ratio; never upscale.
2. Target max width $1920$px and max size $512$ KB.
3. Start at quality $75$; reduce in steps to meet size.
4. Prefer JPEG for compatibility; try WebP if size remains too large.
5. Log compression stats (ratio, saved, processing time).

## Decision Flow

1. **Client attempt (Squoosh)**
   - Resize → compress → check size.
   - Decrease quality until size limit met.
   - If still too large, try WebP.
2. **Client fallback (Canvas)**
   - Resize → toBlob JPEG → reduce quality if needed.
3. **Server fallback (Sharp)**
   - Always validate size/dimensions server-side.
   - Re-compress if client output exceeds limits.

## Implementation Steps (High Level)

1. **Client compression service**
   - Expose `compressImage(file, options)`.
   - Use Squoosh with dynamic import.
   - Fallback to Canvas on error.
2. **Upload hook / handler**
   - Validate input is image.
   - Compress transparently.
   - Upload compressed blob.
3. **Server middleware**
   - Use Sharp to enforce limits.
   - Return 413 if still too large.
   - Attach compression stats to logs.

## Required Defaults

- `maxWidth`: 1920
- `maxHeight`: 1920
- `maxSize`: $512 * 1024$
- `quality`: 75
- `minDimensions`: 200x200 (server-side)

## Anti-Patterns

- ❌ Skipping server validation
- ❌ Uploading original file on failure without logging
- ❌ Enlarging images
- ❌ Using blocking UI (must be transparent to user)

## References (Load as Needed)

- Client implementation: references/client.md
- Client usage example: references/client-usage.md
- Server middleware + routes: references/server.md
- Storage adapters (S3/local): references/storage.md
- Security checks: references/security.md
- Monitoring & analytics: references/monitoring.md
- Performance targets: references/performance.md
- Quality examples: references/quality-metrics.md
- Environment variables: references/env.md
- Docker (Sharp): references/docker.md
- Implementation checklist: references/implementation-checklist.md

## Output Expectations

- Client compression completes in $100$–$500$ ms typical
- Server compression $50$–$200$ ms typical
- Bandwidth reduction $85$–$97\%$

## Checklist

- [ ] Client: Squoosh primary + Canvas fallback
- [ ] Client: size/dimension limits enforced
- [ ] Server: Sharp validation + compression
- [ ] Logging: compression stats & processing time
- [ ] Storage: image saved with metadata
- [ ] Tests: JPEG/PNG/WebP, large images, mobile
