---
name: sirv-api
description: Sirv REST API integration for image and file management. Use when working with Sirv CDN, uploading/downloading files to Sirv, managing image metadata, searching files, creating 360 spins, converting videos, or any Sirv API operations. Covers authentication, file operations, metadata, search queries, async jobs, and account management.
---

# Sirv REST API

Base URL: `https://api.sirv.com`

## Authentication

All requests require a Bearer token from `/v2/token`:

```bash
curl -X POST https://api.sirv.com/v2/token \
  -H "Content-Type: application/json" \
  -d '{"clientId": "YOUR_CLIENT_ID", "clientSecret": "YOUR_CLIENT_SECRET"}'
```

Response:
```json
{"token": "eyJhbG...", "expiresIn": 1200, "scope": ["account:read", ...]}
```

Use token in subsequent requests:
```bash
curl https://api.sirv.com/v2/account \
  -H "Authorization: Bearer eyJhbG..."
```

Tokens expire in 20 minutes. Request a new one before expiry.

## Quick Reference

### File Operations

| Operation | Method | Endpoint | Key Params |
|-----------|--------|----------|------------|
| Upload | POST | `/v2/files/upload` | `?filename=/path/file.jpg` + binary body |
| Download | GET | `/v2/files/download` | `?filename=/path/file.jpg` |
| Delete | POST | `/v2/files/delete` | `?filename=/path/file.jpg` |
| Copy | POST | `/v2/files/copy` | `?from=/a.jpg&to=/b.jpg` |
| Rename/Move | POST | `/v2/files/rename` | `?from=/a.jpg&to=/b.jpg` |
| Create folder | POST | `/v2/files/mkdir` | `?dirname=/new-folder` |
| List directory | GET | `/v2/files/readdir` | `?dirname=/folder` |

### Metadata Operations

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Get all meta | GET | `/v2/files/meta?filename=/path` |
| Set meta | POST | `/v2/files/meta?filename=/path` |
| Get/Set title | GET/POST | `/v2/files/meta/title?filename=/path` |
| Get/Set description | GET/POST | `/v2/files/meta/description?filename=/path` |
| Get/Add/Delete tags | GET/POST/DELETE | `/v2/files/meta/tags?filename=/path` |
| Get/Set product | GET/POST | `/v2/files/meta/product?filename=/path` |

### Async Jobs (return job ID, poll for progress)

| Operation | Start | Poll |
|-----------|-------|------|
| Spin to video | POST `/v2/files/spin2video` | Returns filename directly |
| Video to spin | POST `/v2/files/video2spin` | Returns filename directly |
| Create ZIP | POST `/v2/files/zip` | GET `/v2/files/zip?id=` |
| Batch delete | POST `/v2/files/batch/delete` | GET `/v2/files/batch/delete?id=` |
| 3D to GLB | POST `/v2/files/3d/model2GLB` | GET `/v2/files/3d/model2GLB?id=` |

## When to Read Reference Files

- **File operations** (upload, download, copy, delete, directory listing): See [files.md](references/files.md)
- **Metadata & search** (meta fields, search query syntax, product data): See [metadata.md](references/metadata.md)
- **Async jobs** (video conversion, ZIP, batch ops): See [jobs.md](references/jobs.md)
- **Account & stats** (usage, billing, events, settings): See [account.md](references/account.md)

## Common Patterns

### Upload an image
```javascript
const token = await getToken();
await fetch('https://api.sirv.com/v2/files/upload?filename=/images/photo.jpg', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'image/jpeg'
  },
  body: imageBuffer
});
```

### Search for recent images
```javascript
await fetch('https://api.sirv.com/v2/files/search', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    query: 'extension:.jpg AND mtime:[now-7d TO now]',
    size: 50
  })
});
```

### Create ZIP archive (async)
```javascript
// Start job
const { id } = await fetch('https://api.sirv.com/v2/files/zip', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
  body: JSON.stringify({
    filenames: ['/images/photo1.jpg', '/images/photo2.jpg'],
    zipFilename: '/downloads/photos.zip'
  })
}).then(r => r.json());

// Poll until complete
let progress = 0;
while (progress < 100) {
  const status = await fetch(`https://api.sirv.com/v2/files/zip?id=${id}`, {
    headers: { 'Authorization': `Bearer ${token}` }
  }).then(r => r.json());
  progress = status.progress;
  await new Promise(r => setTimeout(r, 1000));
}
```
