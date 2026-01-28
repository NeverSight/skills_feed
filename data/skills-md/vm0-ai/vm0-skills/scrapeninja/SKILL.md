---
name: scrapeninja
description: High-performance web scraping API with Chrome TLS fingerprint and JS rendering
vm0_secrets:
  - SCRAPENINJA_API_KEY
---

# ScrapeNinja

High-performance web scraping API with Chrome TLS fingerprint, rotating proxies, smart retries, and optional JavaScript rendering.

> Official docs: https://scrapeninja.net/docs/

---

## When to Use

Use this skill when you need to:

- Scrape websites with anti-bot protection (Cloudflare, Datadome)
- Extract data without running a full browser (fast `/scrape` endpoint)
- Render JavaScript-heavy pages (`/scrape-js` endpoint)
- Use rotating proxies with geo selection (US, EU, Brazil, etc.)
- Extract structured data with Cheerio extractors
- Intercept AJAX requests
- Take screenshots of pages

---

## Prerequisites

1. Get an API key from RapidAPI or APIRoad:
  - RapidAPI: https://rapidapi.com/restyler/api/scrapeninja
  - APIRoad: https://apiroad.net/marketplace/apis/scrapeninja

Set environment variable:

```bash
# For RapidAPI
export SCRAPENINJA_API_KEY="your-rapidapi-key"

# For APIRoad (use X-Apiroad-Key header instead)
export SCRAPENINJA_API_KEY="your-apiroad-key"
```

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"'
> ```

## How to Use

### 1. Basic Scrape (Non-JS, Fast)

High-performance scraping with Chrome TLS fingerprint, no JavaScript:

Write to `/tmp/scrapeninja_request.json`:

```json
{
  "url": "https://example.com"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://scrapeninja.p.rapidapi.com/scrape" --header "Content-Type: application/json" --header "X-RapidAPI-Key: ${SCRAPENINJA_API_KEY}" -d @/tmp/scrapeninja_request.json' | jq '{status: .info.statusCode, url: .info.finalUrl, bodyLength: (.body | length)}'
```

**With custom headers and retries:**

Write to `/tmp/scrapeninja_request.json`:

```json
{
  "url": "https://example.com",
  "headers": ["Accept-Language: en-US"],
  "retryNum": 3,
  "timeout": 15
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://scrapeninja.p.rapidapi.com/scrape" --header "Content-Type: application/json" --header "X-RapidAPI-Key: ${SCRAPENINJA_API_KEY}" -d @/tmp/scrapeninja_request.json'
```

### 2. Scrape with JavaScript Rendering

For JavaScript-heavy sites (React, Vue, etc.):

Write to `/tmp/scrapeninja_request.json`:

```json
{
  "url": "https://example.com",
  "waitForSelector": "h1",
  "timeout": 20
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://scrapeninja.p.rapidapi.com/scrape-js" --header "Content-Type: application/json" --header "X-RapidAPI-Key: ${SCRAPENINJA_API_KEY}" -d @/tmp/scrapeninja_request.json' | jq '{status: .info.statusCode, bodyLength: (.body | length)}'
```

**With screenshot:**

Write to `/tmp/scrapeninja_request.json`:

```json
{
  "url": "https://example.com",
  "screenshot": true
}
```

Then run:

```bash
# Get screenshot URL from response
bash -c 'curl -s -X POST "https://scrapeninja.p.rapidapi.com/scrape-js" --header "Content-Type: application/json" --header "X-RapidAPI-Key: ${SCRAPENINJA_API_KEY}" -d @/tmp/scrapeninja_request.json' | jq -r '.info.screenshot'
```

### 3. Geo-Based Proxy Selection

Use proxies from specific regions:

Write to `/tmp/scrapeninja_request.json`:

```json
{
  "url": "https://example.com",
  "geo": "eu"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://scrapeninja.p.rapidapi.com/scrape" --header "Content-Type: application/json" --header "X-RapidAPI-Key: ${SCRAPENINJA_API_KEY}" -d @/tmp/scrapeninja_request.json' | jq .info
```

Available geos: `us`, `eu`, `br` (Brazil), `fr` (France), `de` (Germany), `4g-eu`

### 4. Smart Retries

Retry on specific HTTP status codes or text patterns:

Write to `/tmp/scrapeninja_request.json`:

```json
{
  "url": "https://example.com",
  "retryNum": 3,
  "statusNotExpected": [403, 429, 503],
  "textNotExpected": ["captcha", "Access Denied"]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://scrapeninja.p.rapidapi.com/scrape" --header "Content-Type: application/json" --header "X-RapidAPI-Key: ${SCRAPENINJA_API_KEY}" -d @/tmp/scrapeninja_request.json'
```

### 5. Extract Data with Cheerio

Extract structured JSON using Cheerio extractor functions:

Write to `/tmp/scrapeninja_request.json`:

```json
{
  "url": "https://news.ycombinator.com",
  "extractor": "function(input, cheerio) { let $ = cheerio.load(input); return $(\".titleline > a\").slice(0,5).map((i,el) => ({title: $(el).text(), url: $(el).attr(\"href\")})).get(); }"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://scrapeninja.p.rapidapi.com/scrape" --header "Content-Type: application/json" --header "X-RapidAPI-Key: ${SCRAPENINJA_API_KEY}" -d @/tmp/scrapeninja_request.json' | jq '.extractor'
```

### 6. Intercept AJAX Requests

Capture XHR/fetch responses:

Write to `/tmp/scrapeninja_request.json`:

```json
{
  "url": "https://example.com",
  "catchAjaxHeadersUrlMask": "api/data"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://scrapeninja.p.rapidapi.com/scrape-js" --header "Content-Type: application/json" --header "X-RapidAPI-Key: ${SCRAPENINJA_API_KEY}" -d @/tmp/scrapeninja_request.json' | jq '.info.catchedAjax'
```

### 7. Block Resources for Speed

Speed up JS rendering by blocking images and media:

Write to `/tmp/scrapeninja_request.json`:

```json
{
  "url": "https://example.com",
  "blockImages": true,
  "blockMedia": true
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://scrapeninja.p.rapidapi.com/scrape-js" --header "Content-Type: application/json" --header "X-RapidAPI-Key: ${SCRAPENINJA_API_KEY}" -d @/tmp/scrapeninja_request.json'
```

---

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/scrape` | Fast non-JS scraping with Chrome TLS fingerprint |
| `/scrape-js` | Full Chrome browser with JS rendering |
| `/v2/scrape-js` | Enhanced JS rendering for protected sites (APIRoad only) |

---

## Request Parameters

### Common Parameters (all endpoints)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | string | required | URL to scrape |
| `headers` | string[] | - | Custom HTTP headers |
| `retryNum` | int | 1 | Number of retry attempts |
| `geo` | string | `us` | Proxy geo: us, eu, br, fr, de, 4g-eu |
| `proxy` | string | - | Custom proxy URL (overrides geo) |
| `timeout` | int | 10/16 | Timeout per attempt in seconds |
| `textNotExpected` | string[] | - | Text patterns that trigger retry |
| `statusNotExpected` | int[] | [403, 502] | HTTP status codes that trigger retry |
| `extractor` | string | - | Cheerio extractor function |

### JS Rendering Parameters (`/scrape-js`, `/v2/scrape-js`)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `waitForSelector` | string | - | CSS selector to wait for |
| `postWaitTime` | int | - | Extra wait time after load (1-12s) |
| `screenshot` | bool | true | Take page screenshot |
| `blockImages` | bool | false | Block image loading |
| `blockMedia` | bool | false | Block CSS/fonts loading |
| `catchAjaxHeadersUrlMask` | string | - | URL pattern to intercept AJAX |
| `viewport` | object | 1920x1080 | Custom viewport size |

---

## Response Format

```json
{
  "info": {
  "statusCode": 200,
  "finalUrl": "https://example.com",
  "headers": ["content-type: text/html"],
  "screenshot": "base64-encoded-png",
  "catchedAjax": {
  "url": "https://example.com/api/data",
  "method": "GET",
  "body": "...",
  "status": 200
  }
  },
  "body": "<html>...</html>",
  "extractor": { "extracted": "data" }
}
```

---

## Guidelines

1. **Start with `/scrape`**: Use the fast non-JS endpoint first, only switch to `/scrape-js` if needed
2. **Retries**: Set `retryNum` to 2-3 for unreliable sites
3. **Geo Selection**: Use `eu` for European sites, `us` for American sites
4. **Extractors**: Test extractors at https://scrapeninja.net/cheerio-sandbox/
5. **Blocked Sites**: For Cloudflare/Datadome protected sites, use `/v2/scrape-js` via APIRoad
6. **Screenshots**: Set `screenshot: false` to speed up JS rendering
7. **Rate Limits**: Check your plan limits on RapidAPI/APIRoad dashboard

---

## Tools

- **Playground**: https://scrapeninja.net/scraper-sandbox
- **Cheerio Sandbox**: https://scrapeninja.net/cheerio-sandbox
- **cURL Converter**: https://scrapeninja.net/curl-to-scraper
