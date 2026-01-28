---
name: imgur
description: Upload images to Imgur for free hosting. Use this skill when you need to upload images and get public URLs for sharing or embedding in articles.
vm0_secrets:
  - IMGUR_CLIENT_ID
---

# Imgur Image Hosting

Imgur is a free image hosting service. Upload images and get URLs for sharing, embedding in articles, or using in documentation.

## When to Use

- Upload images to get shareable URLs
- Host images for blog posts or documentation
- Get image URLs for use in Markdown content
- Anonymous image uploads (no account needed)

## Prerequisites

Set the following environment variable:

```bash
export IMGUR_CLIENT_ID=your_client_id
```

Get your Client ID from: https://api.imgur.com/oauth2/addclient

When registering:
- Authorization type: "OAuth 2 authorization without a callback URL"
- You only need the Client ID for anonymous uploads


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"'
> ```

## How to Use

### Upload Local Image

```bash
curl -X POST https://api.imgur.com/3/image -H "Authorization: Client-ID ${IMGUR_CLIENT_ID}" -F "image=@/path/to/image.png"
```

### Upload from URL

```bash
curl -X POST https://api.imgur.com/3/image -H "Authorization: Client-ID ${IMGUR_CLIENT_ID}" -F "image=https://example.com/image.png" -F "type=url"
```

### Upload Base64

```bash
curl -X POST https://api.imgur.com/3/image -H "Authorization: Client-ID ${IMGUR_CLIENT_ID}" -F "image=$(base64 -i /path/to/image.png)" -F "type=base64"
```

### Optional Parameters

| Parameter | Description |
|-----------|-------------|
| title | Image title |
| description | Image description |
| name | Filename |

```bash
curl -X POST https://api.imgur.com/3/image -H "Authorization: Client-ID ${IMGUR_CLIENT_ID}" -F "image=@screenshot.png" -F "title=My Screenshot" -F "description=Screenshot from my app"
```

## Response

```json
{
  "data": {
  "id": "abc123",
  "link": "https://i.imgur.com/abc123.png",
  "deletehash": "xyz789"
  },
  "success": true,
  "status": 200
}
```

Key fields:
- `data.link` - Public URL to use in Markdown: `![img](https://i.imgur.com/abc123.png)`
- `data.deletehash` - Save this to delete the image later

## Delete Image

Replace `<your-deletehash>` with the deletehash from the upload response:

```bash
curl -X DELETE https://api.imgur.com/3/image/<your-deletehash> -H "Authorization: Client-ID ${IMGUR_CLIENT_ID}"
```

## Rate Limits

- ~12,500 requests/day
- ~1,250 uploads/day (uploads cost 10 credits)
- Headers show remaining: `X-RateLimit-ClientRemaining`

## Guidelines

1. **Save deletehash**: Store it if you need to delete images later
2. **Anonymous uploads**: Images are not tied to any account
3. **Supported formats**: JPEG, PNG, GIF, APNG, TIFF, BMP, PDF, XCF, WebP
4. **Max file size**: 20MB for images, 200MB for GIFs

## API Reference

- Documentation: https://apidocs.imgur.com/
- Register App: https://api.imgur.com/oauth2/addclient
