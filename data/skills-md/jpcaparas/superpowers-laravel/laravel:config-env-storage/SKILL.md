---
name: laravel:config-env-storage
description: Portable storage configuration across S3/R2/MinIO with optional CDN—env toggles, path-style endpoints, and URL generation
---

# Storage Config (S3/R2/MinIO/CDN)

Configure storage once; switch providers via env.

## Env

```
FILESYSTEM_DISK=s3
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_DEFAULT_REGION=auto
AWS_BUCKET=...
AWS_ENDPOINT=https://r2.example.com       # for R2/MinIO
AWS_USE_PATH_STYLE_ENDPOINT=true          # if required
MEDIA_CDN_URL=https://cdn.example.com     # optional CDN/base URL
```

## Tips

- Prefer pre‑signed URLs for uploads/downloads when possible
- For CDN, prefix public URLs with `MEDIA_CDN_URL` (app URL generation helper)
- Use path‑style only when necessary; some providers require it

## Testing

- Fake storage in unit tests (`Storage::fake('s3')`)
- Integration tests verify URL formats and ACLs

