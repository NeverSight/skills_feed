---
name: htmlcsstoimage
description: HTMLCSStoImage API via curl. Use this skill to generate images from HTML/CSS or capture screenshots of web pages.
vm0_secrets:
  - HCTI_API_KEY
vm0_vars:
  - HCTI_USER_ID
---

# HTMLCSStoImage API

Use the HTMLCSStoImage API via direct `curl` calls to **generate images from HTML/CSS** or **capture screenshots of web pages**.

> Official docs: `https://docs.htmlcsstoimage.com/`

---

## When to Use

Use this skill when you need to:

- **Generate images from HTML/CSS** for social cards, thumbnails, certificates
- **Screenshot web pages** or specific elements on a page
- **Create dynamic images** with custom fonts and styling
- **Generate OG images** for social media sharing

---

## Prerequisites

1. Sign up at [HTMLCSStoImage](https://htmlcsstoimage.com/) and create an account
2. Go to your [Dashboard](https://htmlcsstoimage.com/dashboard) to get your User ID and API Key
3. Store credentials in environment variables

```bash
export HCTI_USER_ID="your-user-id"
export HCTI_API_KEY="your-api-key"
```

### Authentication

The API uses HTTP Basic Authentication:
- Username: Your User ID
- Password: Your API Key

### Pricing

- Free tier: 50 images/month
- Paid plans available for higher volume

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"'
> ```

## How to Use

All examples below assume you have `HCTI_USER_ID` and `HCTI_API_KEY` set.

The base URL for the API is:

- `https://hcti.io/v1/image`

---

### 1. Simple HTML to Image

Generate an image from basic HTML.

Write to `/tmp/hcti_html.txt`:

```html
<div style="padding:20px;background:blue;color:white;font-size:24px;">Hello World</div>
```

Then run:

```bash
bash -c 'curl -s "https://hcti.io/v1/image" -X POST -u "${HCTI_USER_ID}:${HCTI_API_KEY}" --data-urlencode "html@/tmp/hcti_html.txt"'
```

Response:
```json
{
  "url": "https://hcti.io/v1/image/abc123..."
}
```

The returned URL is permanent and served via Cloudflare CDN.

---

### 2. HTML with CSS Styling

Generate a styled card image.

Write to `/tmp/hcti_html.txt`:

```html
<div class="card"><h1>Welcome</h1><p>This is a styled card</p></div>
```

Write to `/tmp/hcti_css.txt`:

```css
.card { padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white; font-family: sans-serif; text-align: center; } h1 { margin: 0 0 10px 0; } p { margin: 0; opacity: 0.9; }
```

Then run:

```bash
bash -c 'curl -s "https://hcti.io/v1/image" -X POST -u "${HCTI_USER_ID}:${HCTI_API_KEY}" --data-urlencode "html@/tmp/hcti_html.txt" --data-urlencode "css@/tmp/hcti_css.txt"'
```

---

### 3. Use Google Fonts

Generate an image with custom fonts.

Write to `/tmp/hcti_html.txt`:

```html
<div class="title">Beautiful Typography</div>
```

Write to `/tmp/hcti_css.txt`:

```css
.title { font-family: Playfair Display; font-size: 48px; padding: 40px; background: #1a1a2e; color: #eee; }
```

Then run:

```bash
bash -c 'curl -s "https://hcti.io/v1/image" -X POST -u "${HCTI_USER_ID}:${HCTI_API_KEY}" --data-urlencode "html@/tmp/hcti_html.txt" --data-urlencode "css@/tmp/hcti_css.txt" -d "google_fonts=Playfair Display"'
```

Multiple fonts: `google_fonts=Playfair Display|Roboto|Open Sans`

---

### 4. Screenshot a Web Page (URL to Image)

Capture a screenshot of any public URL:

Write to `/tmp/hcti_url.txt`:

```
https://example.com
```

```bash
bash -c 'curl -s "https://hcti.io/v1/image" -X POST -u "${HCTI_USER_ID}:${HCTI_API_KEY}" --data-urlencode "url@/tmp/hcti_url.txt"'
```

---

### 5. Screenshot with Delay (for JavaScript)

Wait for JavaScript to render before capturing:

Write to `/tmp/hcti_url.txt`:

```
https://example.com
```

```bash
bash -c 'curl -s "https://hcti.io/v1/image" -X POST -u "${HCTI_USER_ID}:${HCTI_API_KEY}" --data-urlencode "url@/tmp/hcti_url.txt" -d "ms_delay=1500"'
```

`ms_delay` waits specified milliseconds before taking the screenshot.

---

### 6. Capture Specific Element (Selector)

Screenshot only a specific element on the page:

```bash
bash -c 'curl -s "https://hcti.io/v1/image" -X POST -u "${HCTI_USER_ID}:${HCTI_API_KEY}" --data-urlencode "url@/tmp/hcti_url.txt" -d "selector=h1"'
```

Use any CSS selector: `#id`, `.class`, `div > p`, etc.

---

### 7. High Resolution (Retina)

Generate 2x or 3x resolution images.

Write to `/tmp/hcti_html.txt`:

```html
<div style="padding:20px;font-size:18px;">High Resolution Image</div>
```

Then run:

```bash
bash -c 'curl -s "https://hcti.io/v1/image" -X POST -u "${HCTI_USER_ID}:${HCTI_API_KEY}" --data-urlencode "html@/tmp/hcti_html.txt" -d "device_scale=2"'
```

`device_scale` accepts values 1-3 (default: 1).

---

### 8. Custom Viewport Size

Set specific viewport dimensions:

```bash
bash -c 'curl -s "https://hcti.io/v1/image" -X POST -u "${HCTI_USER_ID}:${HCTI_API_KEY}" --data-urlencode "url@/tmp/hcti_url.txt" -d "viewport_width=1200" -d "viewport_height=630"'
```

Perfect for generating OG images (1200x630).

---

### 9. Full Page Screenshot

Capture the entire page height:

```bash
bash -c 'curl -s "https://hcti.io/v1/image" -X POST -u "${HCTI_USER_ID}:${HCTI_API_KEY}" --data-urlencode "url@/tmp/hcti_url.txt" -d "full_screen=true"'
```

---

### 10. Block Cookie Banners

Automatically hide consent/cookie popups:

```bash
bash -c 'curl -s "https://hcti.io/v1/image" -X POST -u "${HCTI_USER_ID}:${HCTI_API_KEY}" --data-urlencode "url@/tmp/hcti_url.txt" -d "block_consent_banners=true"'
```

---

### 11. Download Image Directly

Add `?dl=1` to the image URL to trigger download.

Write to `/tmp/hcti_html.txt`:

```html
<div style="padding:20px;background:green;color:white;">Download Me</div>
```

Then run:

```bash
bash -c 'curl -s "https://hcti.io/v1/image" -X POST -u "${HCTI_USER_ID}:${HCTI_API_KEY}" --data-urlencode "html@/tmp/hcti_html.txt"' | jq -r '.url'
```

This will output the image URL. Copy the URL and download with:

```bash
curl -s "https://hcti.io/v1/image/<your-image-id>?dl=1" --output image.png
```

---

### 12. Resize on the Fly

Add width/height query parameters to resize.

Write to `/tmp/hcti_html.txt`:

```html
<div style="padding:40px;background:purple;color:white;font-size:32px;">Resizable</div>
```

Then run:

```bash
bash -c 'curl -s "https://hcti.io/v1/image" -X POST -u "${HCTI_USER_ID}:${HCTI_API_KEY}" --data-urlencode "html@/tmp/hcti_html.txt"' | jq -r '.url'
```

This outputs the image URL. Add query parameters to resize:

```
Original: https://hcti.io/v1/image/<your-image-id>
Thumbnail: https://hcti.io/v1/image/<your-image-id>?width=200&height=200
```

---

## Response Format

**Success (200):**
```json
{
  "url": "https://hcti.io/v1/image/be4c5118-fe19-462b-a49e-48cf72697a9d"
}
```

**Error (400):**
```json
{
  "error": "Bad Request",
  "statusCode": 400,
  "message": "HTML is Required"
}
```

---

## Guidelines

1. **Use `--data-urlencode` for HTML/CSS**: Properly encodes special characters
2. **URLs must be public**: Pages requiring login cannot be screenshotted
3. **Use `ms_delay` for JS-heavy pages**: Give time for JavaScript to render
4. **Choose appropriate `device_scale`**: 2x for retina displays, 1x for standard
5. **Image URLs are permanent**: They're cached on Cloudflare CDN globally
6. **Use selectors for cropping**: More efficient than full page + manual crop
