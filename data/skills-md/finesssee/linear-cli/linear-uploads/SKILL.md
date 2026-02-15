---
name: linear-uploads
description: Download attachments and images from Linear issues. Use when fetching screenshots, images, or file attachments from Linear comments or descriptions.
allowed-tools: Bash Read
---

# Linear Uploads

Download attachments and images from Linear issues using `linear-cli`.

## Download to File

```bash
# Download image/attachment to file
linear-cli up fetch "https://uploads.linear.app/..." -f image.png

# Download to temp directory
linear-cli up fetch "https://uploads.linear.app/..." -f /tmp/screenshot.png
```

## Output to Stdout

```bash
# Pipe to other tools
linear-cli up fetch "https://uploads.linear.app/..." | base64

# Redirect to file
linear-cli up fetch "https://uploads.linear.app/..." > file.png
```

## Finding Upload URLs

Upload URLs are found in:
- Issue descriptions (`linear-cli i get LIN-123 --output json`)
- Comments (`linear-cli cm list LIN-123 --output json`)

URL pattern: `https://uploads.linear.app/{org}/{upload}/{filename}`

## View Images (AI Agents)

Since Claude is multimodal, download then read:

```bash
# 1. Download to temp file
linear-cli up fetch "https://uploads.linear.app/..." -f /tmp/screenshot.png

# 2. Use Read tool on the file
# Claude can view images directly
```

## Tips

- Requires valid LINEAR_API_KEY
- Use `-f` / `--file` to specify output filename
- Without `-f`, outputs raw bytes to stdout
- URLs must be from `uploads.linear.app`
