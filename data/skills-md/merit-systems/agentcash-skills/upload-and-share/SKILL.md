---
name: upload-and-share
description: |
  Upload files to the cloud and get shareable public URLs using stableupload.dev (x402 micropayments).

  USE FOR:
  - Uploading files to get public URLs
  - Sharing files via download links
  - Hosting images, documents, or any file type
  - Making files publicly accessible for 6 months

  TRIGGERS:
  - "upload this", "share this file", "get me a link"
  - "host this file", "make this downloadable"
  - "public URL", "download link", "put online"
  - "share file", "file hosting", "upload file"

  ALWAYS use `npx agentcash fetch` for stableupload.dev endpoints — never curl or WebFetch for the purchase step.
---

# Upload and Share via StableUpload

Upload any local file to S3-backed cloud storage via x402 micropayments. Returns a public URL. No API keys needed.

## Setup

See [rules/getting-started.md](rules/getting-started.md) for installation and wallet setup.

## Quick Reference

| Tier | Max Size | Cost |
|------|----------|------|
| `10mb` | 10 MB | $0.02 |
| `100mb` | 100 MB | $0.20 |
| `1gb` | 1 GB | $2.00 |

All uploads expire after 6 months.

| Task | Endpoint | Price |
|------|----------|-------|
| Buy upload slot | `https://stableupload.dev/api/upload` | Tier-based |
| List uploads | `GET https://stableupload.dev/api/uploads` | Free (auth) |
| Get upload details | `GET https://stableupload.dev/api/download/:uploadId` | Free (auth) |

## Workflow

### 1. Check wallet balance

```bash
npx agentcash wallet info
```

Ensure sufficient USDC balance for the chosen tier. If balance is low, show the deposit link.

### 2. Determine the tier

Pick the smallest tier that fits the file. Check file size first with `ls -la` or `wc -c`.

| Tier | Max Size | Cost |
|------|----------|------|
| `10mb` | 10 MB | $0.02 |
| `100mb` | 100 MB | $0.20 |
| `1gb` | 1 GB | $2.00 |

### 3. Buy the upload slot

```bash
npx agentcash fetch https://stableupload.dev/api/upload -m POST -b '{"filename": "report.pdf", "contentType": "application/pdf", "tier": "10mb"}'
```

**Parameters:**
- `filename` — name for the uploaded file (required)
- `contentType` — MIME type (required, advisory for browser)
- `tier` — `"10mb"`, `"100mb"`, or `"1gb"` (required)

**Response:**
```json
{
  "uploadId": "k7gm3nqp2",
  "uploadUrl": "https://f.stableupload.dev/k7gm3nqp2/report.pdf?t=...",
  "publicUrl": "https://f.stableupload.dev/k7gm3nqp2/report.pdf",
  "expiresAt": "2026-08-19T00:00:00.000Z",
  "maxSize": 10485760
}
```

### 4. Upload the file via curl

Use Bash to PUT the file to the returned `uploadUrl`:

```bash
curl -s -X PUT "<uploadUrl>" -H "Content-Type: <mime>" --data-binary @/absolute/path/to/file
```

**Critical:** Use `--data-binary` (not `-d`) to preserve binary content. Use the absolute path.

### 5. Share the public URL

Present the `publicUrl` to the user. This URL is publicly accessible immediately and remains live for 6 months.

## Common MIME Types

| File Type | Content Type |
|-----------|-------------|
| PDF | `application/pdf` |
| PNG image | `image/png` |
| JPEG image | `image/jpeg` |
| CSV | `text/csv` |
| JSON | `application/json` |
| Plain text | `text/plain` |
| ZIP archive | `application/zip` |
| Excel | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` |
| Unknown | `application/octet-stream` |

## Listing Previous Uploads

To list uploads for the current wallet:

```bash
npx agentcash fetch https://stableupload.dev/api/uploads
```

## Get Upload Details

```bash
npx agentcash fetch https://stableupload.dev/api/download/k7gm3nqp2
```

## Key Details

- **No API keys required** — payment is the authentication
- **Upload URLs expire in 1 hour** — upload promptly after buying the slot
- **Public URLs last 6 months** from purchase date
- **Any file type accepted** — contentType is advisory for the browser, not a restriction
- **S3-backed** — files stored on AWS S3 with public read access
- **Discovery endpoint**: `npx agentcash discover https://stableupload.dev` if you need to verify endpoints

## Common Patterns

**Upload a file the user just created:**
Skip discovery, go straight to wallet check + buy slot + upload.

**Upload multiple files:**
Buy separate slots for each file. Slots can be purchased in parallel but uploads must use the correct uploadUrl for each.

**User asks to "share" or "send" a file:**
Upload it and present the public URL. The URL can be shared anywhere.

**Host images for emails:**
Upload the image, then reference the `publicUrl` in email HTML:
```html
<img src="https://f.stableupload.dev/abc/photo.png" alt="Photo" />
```

## Error Handling

- **Insufficient balance**: Show the deposit link from `npx agentcash wallet info`
- **File too large for tier**: Suggest the next tier up
- **Upload URL expired**: Buy a new slot (the previous payment is non-refundable)
- **curl fails**: Verify the file path exists and the uploadUrl is correctly quoted
