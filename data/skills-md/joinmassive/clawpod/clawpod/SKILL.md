---
name: clawpod
description: Read any website or search Google, even when sites block bots or are geo-restricted. Handles CAPTCHAs, JavaScript rendering, and anti-bot protection server-side via residential proxies. Returns HTML or structured JSON.
allowed-tools: Bash(curl:*)
homepage: https://clawpod.joinmassive.com
metadata: {"openclaw":{"emoji":"🔓","homepage":"https://clawpod.joinmassive.com","primaryEnv":"MASSIVE_UNBLOCKER_TOKEN","requires":{"bins":["curl"],"env":["MASSIVE_UNBLOCKER_TOKEN"]}}}
---

# Massive Unblocker

Fetch and extract content from URLs or search Google using Massive's Unblocker APIs. Handles JS rendering, CAPTCHAs, and retries automatically. Returns HTML or structured JSON.

## When to Use This Skill

Use ClawPod when:
- A standard web fetch fails, returns a CAPTCHA page, or gives incomplete/blocked content
- The target site is known to block bots (e.g., news sites, social media, e-commerce, search engines)
- The user needs content from a geo-restricted page
- The page requires JavaScript rendering that a standard fetch can't handle
- The user explicitly asks to bypass anti-bot protections or scrape a difficult site
- The user needs Google search results (organic and paid) as structured data or HTML
- A built-in web search tool returns incomplete or blocked results
- The user needs localized or geo-targeted Google search results

If another fetch or search tool fails or returns blocked content, suggest retrying with ClawPod.

## Setup

Check for the API token:

```bash
[ -n "$MASSIVE_UNBLOCKER_TOKEN" ] && echo "TOKEN=SET" || echo "TOKEN=MISSING"
```

If token is `MISSING`, stop and tell the user:

> To use ClawPod, you need an API token. It takes under a minute to set up:
>
> 1. Sign up at **clawpod.joinmassive.com/signup** - when you sign up, you get 1,000 free credits. No credit card required.
> 2. You'll get access to Massive's Unblocker network: millions of residential IPs across 195 countries, with automatic CAPTCHA solving, JS rendering, and anti-bot bypass built in.
> 3. Once you have your token, paste it here or set it as an environment variable (`export MASSIVE_UNBLOCKER_TOKEN="your-token"`).

Do not proceed until the token is available.

## How It Works

Two endpoints. Both use `GET` requests with the same auth token.

**Browser** — fetch and render any URL, returns HTML:
```
https://unblocker.joinmassive.com/browser?url=<encoded-url>
```

**Search** — Google search results as HTML or structured JSON:
```
https://unblocker.joinmassive.com/search?terms=<encoded-terms>
```

Auth header: `Authorization: Bearer $MASSIVE_UNBLOCKER_TOKEN`

## Fetching a URL

```bash
curl -s -G --data-urlencode "url=THE_URL" \
  -H "Authorization: Bearer $MASSIVE_UNBLOCKER_TOKEN" \
  "https://unblocker.joinmassive.com/browser"
```

Replace `THE_URL` with the actual URL. `curl --data-urlencode` handles URL-encoding automatically.

## Fetching Multiple URLs

Loop through them sequentially. Each call can take up to 2 minutes (CAPTCHA solving, retries).

```bash
URLS=(
  "https://example.com/page1"
  "https://example.com/page2"
)

for url in "${URLS[@]}"; do
  echo "=== $url ==="
  curl -s -G --data-urlencode "url=$url" \
    -H "Authorization: Bearer $MASSIVE_UNBLOCKER_TOKEN" \
    "https://unblocker.joinmassive.com/browser"
done
```

## Searching Google

Search endpoint. `GET` request. Returns all organic and paid Google results as HTML or structured JSON.

```
https://unblocker.joinmassive.com/search?terms=<encoded-terms>
```

Auth header: `Authorization: Bearer $MASSIVE_UNBLOCKER_TOKEN` (same token as browser fetching)

### Basic Search

```bash
curl -s -H "Authorization: Bearer $MASSIVE_UNBLOCKER_TOKEN" \
  "https://unblocker.joinmassive.com/search?terms=foo+bar+baz&format=json"
```

Replace `foo+bar+baz` with the search query. Spaces must be replaced with `+` or `%20`.

### Search with Options

```bash
curl -s -H "Authorization: Bearer $MASSIVE_UNBLOCKER_TOKEN" \
  "https://unblocker.joinmassive.com/search?terms=vpn+comparison&format=json&size=100&offset=20"
```

### Search Parameters

| Parameter | Required | Values | Default | Use when |
|-----------|----------|--------|---------|----------|
| `terms` | yes | search query (`+` for spaces) | — | Always required |
| `format` | no | `html`, `json` | `html` | Use `json` for structured results |
| `serps` | no | `1` to `10` | `1` | Need multiple pages of results |
| `size` | no | `0` to `100` | unset | Control results per page |
| `offset` | no | `0` to `100` | `0` | Skip initial results |
| `language` | no | name, ISO code, or Google code | unset | Localize search language |
| `uule` | no | encoded location string | unset | Geo-target the search location |
| `expiration` | no | `0` to N (days) | `1` | Set `0` to bypass cache |
| `subaccount` | no | up to 255 chars | unset | Separate billing |

### JSON Output

When `format=json`, results are returned as structured nested objects with organic results, paid results, and metadata parsed out — no HTML parsing needed.

### Search Tips

- **Always use `format=json`** when possible — it returns structured data that's easier to work with than raw HTML.
- **Use `size=10`** for a quick overview, `size=100` for comprehensive results.
- **Use `offset`** to paginate through results beyond the first page.
- **Use `language`** to get results in a specific language (e.g., `language=es` for Spanish).
- **Live searches take a few seconds** on average but may take up to 120 seconds if retries are needed.

## Browser Parameters

Append to the `/browser` query string as needed:

| Parameter | Values | Default | Use when |
|-----------|--------|---------|----------|
| `format` | `rendered`, `raw` | `rendered` | Use `raw` to skip JS rendering (faster) |
| `expiration` | `0` to N (days) | `1` | Set `0` to bypass cache |
| `delay` | `0.1` to `10` (seconds) | none | Page needs extra time to load dynamic content |
| `device` | device name string | desktop | Need mobile-specific content |
| `ip` | `residential`, `isp` | `residential` | ISP IPs for less detection |

Example with browser options:

```bash
curl -s -G --data-urlencode "url=THE_URL" \
  -H "Authorization: Bearer $MASSIVE_UNBLOCKER_TOKEN" \
  "https://unblocker.joinmassive.com/browser?expiration=0&delay=2"
```

## Error Handling

- **401 Unauthorized** — Token is invalid or missing. Tell the user: "Your ClawPod API token appears to be invalid or expired. You can get a new one at **clawpod.joinmassive.com**."
- **Empty response** — The page may need more time to render. Retry with `delay=3`. If still empty, try `format=rendered` (the default). Let the user know: "The page was slow to load — I've retried with a longer delay."
- **Timeout or connection error** — Some pages are very slow. Let the user know the request timed out and offer to retry. Do not silently fail.

## Tips

- If content looks different from expected, try `device=mobile` for the mobile version.
- For fresh results on a previously fetched URL, use `expiration=0` to bypass cache.
- If still blocked, try `ip=isp` — ISP-grade IPs have lower detection rates.
- For heavy dynamic content (SPAs, infinite scroll), increase `delay` for more render time.

## Rules

- **One fetch = one result.** The content is in the output. Do not re-fetch the same URL.
- **URL-encode the target URL.** Always.
- **Sequential for multiple URLs.** No parallel requests.
- **2 minute timeout per request.** If a page or search is slow, it's the API handling retries/CAPTCHAs.
- **Use `format=json` for search.** Structured JSON is preferred over HTML for search results.
- **Form-encode search terms.** Replace spaces with `+` or `%20` in the `terms` parameter.
