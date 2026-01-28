---
name: browserless
description: Headless browser as a service for screenshots, PDFs, scraping, and automation
vm0_secrets:
  - BROWSERLESS_API_TOKEN
---

# Browserless

Headless Chrome browser as a service. Take screenshots, generate PDFs, scrape JS-rendered pages, and run Puppeteer/Playwright scripts without managing browser infrastructure.

> Official docs: https://docs.browserless.io/

---

## When to Use

Use this skill when you need to:

- Scrape JavaScript-heavy pages (React, Vue, Angular)
- Take full-page or element screenshots
- Generate PDFs from web pages
- Execute custom JavaScript in a browser context
- Bypass bot detection with stealth mode
- Run Puppeteer/Playwright scripts in the cloud

---

## Prerequisites

1. Create an account at https://www.browserless.io/
2. Get your API token from https://account.browserless.io/

Set environment variable:

```bash
export BROWSERLESS_API_TOKEN="your-api-token-here"
```

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"' | jq '.data[0]'
> ```

## How to Use

### 1. Scrape Data (CSS Selectors)

Extract structured JSON using CSS selectors:

Write to `/tmp/browserless_request.json`:

```json
{
  "url": "https://example.com",
  "elements": [
    {"selector": "h1"},
    {"selector": "p"}
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://production-sfo.browserless.io/scrape?token=${BROWSERLESS_API_TOKEN}" --header "Content-Type: application/json" -d @/tmp/browserless_request.json'
```

**With wait options:**

Write to `/tmp/browserless_request.json`:

```json
{
  "url": "https://news.ycombinator.com",
  "elements": [{"selector": ".titleline > a"}],
  "gotoOptions": {
    "waitUntil": "networkidle2",
    "timeout": 30000
  }
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://production-sfo.browserless.io/scrape?token=${BROWSERLESS_API_TOKEN}" --header "Content-Type: application/json" -d @/tmp/browserless_request.json' | jq '.data[0].results[:3]'
```

### 2. Take Screenshots

**Full page screenshot:**

Write to `/tmp/browserless_request.json`:

```json
{
  "url": "https://example.com",
  "options": {
    "fullPage": true,
    "type": "png"
  }
}
```

Then run:

```bash
curl -s -X POST "https://production-sfo.browserless.io/screenshot?token=${BROWSERLESS_API_TOKEN}" --header "Content-Type: application/json" -d @/tmp/browserless_request.json --output screenshot.png
```

**Element screenshot:**

Write to `/tmp/browserless_request.json`:

```json
{
  "url": "https://example.com",
  "options": {
    "type": "png"
  },
  "selector": "h1"
}
```

Then run:

```bash
curl -s -X POST "https://production-sfo.browserless.io/screenshot?token=${BROWSERLESS_API_TOKEN}" --header "Content-Type: application/json" -d @/tmp/browserless_request.json --output element.png
```

**With viewport size:**

Write to `/tmp/browserless_request.json`:

```json
{
  "url": "https://example.com",
  "viewport": {
    "width": 1920,
    "height": 1080
  },
  "options": {
    "type": "jpeg",
    "quality": 80
  }
}
```

Then run:

```bash
curl -s -X POST "https://production-sfo.browserless.io/screenshot?token=${BROWSERLESS_API_TOKEN}" --header "Content-Type: application/json" -d @/tmp/browserless_request.json --output screenshot.jpg
```

### 3. Generate PDF

Write to `/tmp/browserless_request.json`:

```json
{
  "url": "https://example.com",
  "options": {
    "format": "A4",
    "printBackground": true,
    "margin": {
      "top": "1cm",
      "bottom": "1cm"
    }
  }
}
```

Then run:

```bash
curl -s -X POST "https://production-sfo.browserless.io/pdf?token=${BROWSERLESS_API_TOKEN}" --header "Content-Type: application/json" -d @/tmp/browserless_request.json --output page.pdf
```

### 4. Get Rendered HTML

Get fully rendered HTML after JavaScript execution:

Write to `/tmp/browserless_request.json`:

```json
{
  "url": "https://example.com",
  "gotoOptions": {
    "waitUntil": "networkidle0"
  }
}
```

Then run:

```bash
curl -s -X POST "https://production-sfo.browserless.io/content?token=${BROWSERLESS_API_TOKEN}" --header "Content-Type: application/json" -d @/tmp/browserless_request.json
```

### 5. Execute Custom JavaScript (Click, Type, etc.)

Run Puppeteer code with full interaction support:

**Click element:**

Write to `/tmp/browserless_function.js`:

```javascript
export default async ({ page }) => {
  await page.goto("https://example.com");
  await page.click("a");
  return { data: { url: page.url() }, type: "application/json" };
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://production-sfo.browserless.io/function?token=${BROWSERLESS_API_TOKEN}" -H "Content-Type: application/javascript" -d @/tmp/browserless_function.js'
```

**Type into input:**

Write to `/tmp/browserless_function.js`:

```javascript
export default async ({ page }) => {
  await page.goto("https://duckduckgo.com");
  await page.waitForSelector("input[name=q]");
  await page.type("input[name=q]", "hello world");
  const val = await page.$eval("input[name=q]", e => e.value);
  return { data: { typed: val }, type: "application/json" };
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://production-sfo.browserless.io/function?token=${BROWSERLESS_API_TOKEN}" -H "Content-Type: application/javascript" -d @/tmp/browserless_function.js'
```

**Form submission:**

Write to `/tmp/browserless_function.js`:

```javascript
export default async ({ page }) => {
  await page.goto("https://duckduckgo.com");
  await page.type("input[name=q]", "test query");
  await page.keyboard.press("Enter");
  await page.waitForNavigation();
  return { data: { title: await page.title() }, type: "application/json" };
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://production-sfo.browserless.io/function?token=${BROWSERLESS_API_TOKEN}" -H "Content-Type: application/javascript" -d @/tmp/browserless_function.js'
```

**Extract data with custom script:**

Write to `/tmp/browserless_function.js`:

```javascript
export default async ({ page }) => {
  await page.goto("https://news.ycombinator.com");
  const links = await page.$$eval(".titleline > a", els => els.slice(0,5).map(a => ({title: a.innerText, url: a.href})));
  return { data: links, type: "application/json" };
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://production-sfo.browserless.io/function?token=${BROWSERLESS_API_TOKEN}" -H "Content-Type: application/javascript" -d @/tmp/browserless_function.js'
```

### 6. Unblock Protected Sites

Bypass bot detection:

Write to `/tmp/browserless_request.json`:

```json
{
  "url": "https://example.com",
  "browserWSEndpoint": false,
  "cookies": false,
  "content": true,
  "screenshot": false
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://production-sfo.browserless.io/unblock?token=${BROWSERLESS_API_TOKEN}" --header "Content-Type: application/json" -d @/tmp/browserless_request.json'
```

### 7. Stealth Mode

Enable stealth mode to avoid detection:

Write to `/tmp/browserless_request.json`:

```json
{
  "url": "https://example.com",
  "elements": [{"selector": "body"}]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://production-sfo.browserless.io/scrape?token=${BROWSERLESS_API_TOKEN}&stealth=true" --header "Content-Type: application/json" -d @/tmp/browserless_request.json'
```

### 8. Export Page with Resources

Fetch a URL and get content in native format. Can bundle all resources (CSS, JS, images) as zip:

**Basic export:**

Write to `/tmp/browserless_request.json`:

```json
{
  "url": "https://example.com"
}
```

Then run:

```bash
curl -s -X POST "https://production-sfo.browserless.io/export?token=${BROWSERLESS_API_TOKEN}" --header "Content-Type: application/json" -d @/tmp/browserless_request.json --output page.html
```

**Export with all resources as ZIP:**

Write to `/tmp/browserless_request.json`:

```json
{
  "url": "https://example.com",
  "includeResources": true
}
```

Then run:

```bash
curl -s -X POST "https://production-sfo.browserless.io/export?token=${BROWSERLESS_API_TOKEN}" --header "Content-Type: application/json" -d @/tmp/browserless_request.json --output webpage.zip
```

### 9. Performance Audit (Lighthouse)

Run Lighthouse audits for accessibility, performance, SEO, best practices:

**Full audit:**

Write to `/tmp/browserless_request.json`:

```json
{
  "url": "https://example.com"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://production-sfo.browserless.io/performance?token=${BROWSERLESS_API_TOKEN}" --header "Content-Type: application/json" -d @/tmp/browserless_request.json' | jq '.data.categories | to_entries[] | {category: .key, score: .value.score}'
```

**Specific category (accessibility, performance, seo, best-practices, pwa):**

Write to `/tmp/browserless_request.json`:

```json
{
  "url": "https://example.com",
  "config": {
    "extends": "lighthouse:default",
    "settings": {
      "onlyCategories": ["performance"]
    }
  }
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://production-sfo.browserless.io/performance?token=${BROWSERLESS_API_TOKEN}" --header "Content-Type: application/json" -d @/tmp/browserless_request.json' | jq '.data.audits | to_entries[:5][] | {audit: .key, score: .value.score, display: .value.displayValue}'
```

**Specific audit (e.g., unminified-css, first-contentful-paint):**

Write to `/tmp/browserless_request.json`:

```json
{
  "url": "https://example.com",
  "config": {
    "extends": "lighthouse:default",
    "settings": {
      "onlyAudits": ["first-contentful-paint", "largest-contentful-paint"]
    }
  }
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://production-sfo.browserless.io/performance?token=${BROWSERLESS_API_TOKEN}" --header "Content-Type: application/json" -d @/tmp/browserless_request.json' | jq '.data.audits'
```

### 10. Create Persistent Session

Create a persistent browser session that can be connected to via WebSocket:

Write to `/tmp/browserless_request.json`:

```json
{
  "ttl": 300000,
  "stealth": false,
  "headless": true
}
```

Then run:

```bash
curl -s -X POST "https://production-sfo.browserless.io/session?token=${BROWSERLESS_API_TOKEN}" --header "Content-Type: application/json" -d @/tmp/browserless_request.json
```

**Response includes:**
- `id` - Session ID for subsequent operations
- `connect` - WebSocket URL for Puppeteer/Playwright connection
- `stop` - Full URL to stop/delete the session (use this exact URL)
- `browserQL` - BrowserQL query endpoint
- `ttl` - Time-to-live in milliseconds (default: 300000 = 5 minutes)

**Use the session with Puppeteer:**

```javascript
const puppeteer = require('puppeteer-core');
const browser = await puppeteer.connect({
  browserWSEndpoint: '<connect-url-from-response>' // Use the 'connect' URL from response
});
```

### 11. Stop Persistent Session

Stop a running session before its timeout expires using the `stop` URL from the creation response:

```bash
curl -s -X DELETE "<stop-url-from-response>"
```

Example (replace `<stop-url-from-response>` with the actual `stop` URL from session creation):

```bash
curl -s -X DELETE "https://production-sfo.browserless.io/e/<encoded-path>/session/<session-id>?token=<your-token>"
```

**Response:**
```json
{
  "success": true,
  "message": "Session <session-id> was successfully removed",
  "sessionId": "<session-id>",
  "timestamp": "2026-01-01T07:41:36.933Z"
}
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/scrape` | POST | Extract data with CSS selectors |
| `/screenshot` | POST | Capture screenshots (PNG/JPEG) |
| `/pdf` | POST | Generate PDF documents |
| `/content` | POST | Get rendered HTML |
| `/function` | POST | Execute custom Puppeteer code |
| `/unblock` | POST | Bypass bot protection |
| `/export` | POST | Export page with resources as ZIP |
| `/performance` | POST | Lighthouse audits (a11y, perf, SEO) |
| `/session` | POST | Create persistent browser session |
| `/session/{id}` | DELETE | Stop persistent session |

---

## Common Options

### gotoOptions

Control page navigation:

```json
{
  "gotoOptions": {
  "waitUntil": "networkidle2",
  "timeout": 30000
  }
}
```

**waitUntil values:**
- `load` - Wait for load event
- `domcontentloaded` - Wait for DOMContentLoaded
- `networkidle0` - No network connections for 500ms
- `networkidle2` - Max 2 network connections for 500ms

### waitFor Options

```json
{
  "waitForTimeout": 1000,
  "waitForSelector": {"selector": ".loaded", "timeout": 5000},
  "waitForFunction": {"fn": "() => document.ready", "timeout": 5000}
}
```

### Viewport

```json
{
  "viewport": {
  "width": 1920,
  "height": 1080,
  "deviceScaleFactor": 2
  }
}
```

---

## Query Parameters

| Parameter | Description |
|-----------|-------------|
| `token` | API token (required) |
| `stealth` | Enable stealth mode (`true`/`false`) |
| `blockAds` | Block advertisements |
| `proxy` | Use proxy server |

---

## Response Format

**Scrape response:**

```json
{
  "data": [
  {
  "selector": "h1",
  "results": [
  {
  "text": "Example Domain",
  "html": "Example Domain",
  "attributes": [{"name": "class", "value": "title"}],
  "width": 400,
  "height": 50,
  "top": 100,
  "left": 50
  }
  ]
  }
  ]
}
```

---

## Guidelines

1. **waitUntil**: Use `networkidle2` for most pages, `networkidle0` for SPAs
2. **Timeouts**: Default is 30s; increase for slow pages
3. **Stealth Mode**: Enable for sites with bot detection
4. **Screenshots**: Use `jpeg` with quality 80 for smaller files
5. **Rate Limits**: Check your plan limits at https://account.browserless.io/
6. **Regions**: Use region-specific endpoints for better latency:
  - `production-sfo.browserless.io` (US West)
  - `production-lon.browserless.io` (Europe)
