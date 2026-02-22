---
name: scrapling
description: CLI tool for web scraping - extract data from websites via terminal without programming. Powerful extract commands for HTTP requests and browser automation.
---

# scrapling

Scrapling is a powerful Python web scraping library with a comprehensive CLI for extracting data from websites directly from the terminal without writing code. The primary use case is the `extract` command group for quick data extraction.

## Installation

Install with the shell extras using uv:

```bash
uv tool install "scrapling[shell]"
```

Then install fetcher dependencies (browsers, system dependencies, fingerprint manipulation):

```bash
scrapling install
```

## Extract Commands (Primary Usage)

The `scrapling extract` command group allows you to download and extract content from websites without writing any code. Output format is determined by file extension:

- `.md` - Convert HTML to Markdown
- `.html` - Save raw HTML
- `.txt` - Extract clean text content

### Quick Start

```bash
# Basic website download as text
scrapling extract get "https://example.com" page_content.txt

# Download as markdown
scrapling extract get "https://blog.example.com" article.md

# Save raw HTML
scrapling extract get "https://example.com" page.html
```

### Decision Guide: Which Command to Use?

| Use Case                                      | Command                 |
| --------------------------------------------- | ----------------------- |
| Simple websites, blogs, news articles         | `get`                   |
| Modern web apps, dynamic content (JavaScript) | `fetch`                 |
| Protected sites, Cloudflare, anti-bot         | `stealthy-fetch`        |
| Form submissions, APIs                        | `post`, `put`, `delete` |

### HTTP Request Commands

#### GET Request

Most common command for downloading website content:

```bash
# Basic download
scrapling extract get "https://news.site.com" news.md

# Download with custom timeout
scrapling extract get "https://example.com" content.txt --timeout 60

# Extract specific content using CSS selectors
scrapling extract get "https://blog.example.com" articles.md --css-selector "article"

# Send request with cookies
scrapling extract get "https://scrapling.requestcatcher.com" content.md \
    --cookies "session=abc123; user=john"

# Add user agent
scrapling extract get "https://api.site.com" data.json \
    -H "User-Agent: MyBot 1.0"

# Add multiple headers
scrapling extract get "https://site.com" page.html \
    -H "Accept: text/html" \
    -H "Accept-Language: en-US"

# With query parameters
scrapling extract get "https://api.example.com" data.json \
    -p "page=1" -p "limit=10"
```

**GET options:**

```
-H, --headers TEXT              HTTP headers "Key: Value" (multiple allowed)
--cookies TEXT                  Cookies "name1=value1;name2=value2"
--timeout INTEGER               Request timeout in seconds (default: 30)
--proxy TEXT                    Proxy URL from $PROXY_URL env variable
-s, --css-selector TEXT         Extract specific content with CSS selector
-p, --params TEXT               Query parameters "key=value" (multiple)
--follow-redirects / --no-follow-redirects  (default: True)
--verify / --no-verify          SSL verification (default: True)
--impersonate TEXT              Browser to impersonate (chrome, firefox)
--stealthy-headers / --no-stealthy-headers  (default: True)
```

#### POST Request

```bash
# Submit form data
scrapling extract post "https://api.site.com/search" results.html \
    --data "query=python&type=tutorial"

# Send JSON data
scrapling extract post "https://api.site.com" response.json \
    --json '{"username": "test", "action": "search"}'
```

**POST options:** (same as GET plus)

```
-d, --data TEXT                 Form data "param1=value1&param2=value2"
-j, --json TEXT                 JSON data as string
```

#### PUT Request

```bash
# Send data
scrapling extract put "https://api.example.com" results.html \
    --data "update=info" \
    --impersonate "firefox"

# Send JSON data
scrapling extract put "https://api.example.com" response.json \
    --json '{"username": "test", "action": "search"}'
```

#### DELETE Request

```bash
scrapling extract delete "https://api.example.com/resource" response.txt

# With impersonation
scrapling extract delete "https://api.example.com/" response.txt \
    --impersonate "chrome"
```

### Browser Fetching Commands

Use browser-based fetching for JavaScript-heavy sites or when HTTP requests fail.

#### fetch - Handle Dynamic Content

For websites that load content dynamically or have slight protection:

```bash
# Wait for JavaScript to load and network activity to finish
scrapling extract fetch "https://example.com" content.md --network-idle

# Wait for specific element to appear
scrapling extract fetch "https://example.com" data.txt \
    --wait-selector ".content-loaded"

# Visible browser mode for debugging
scrapling extract fetch "https://example.com" page.html \
    --no-headless --disable-resources

# Use installed Chrome browser
scrapling extract fetch "https://example.com" content.md --real-chrome

# With CSS selector extraction
scrapling extract fetch "https://example.com" articles.md \
    --css-selector "article" \
    --network-idle
```

**fetch options:**

```
--headless / --no-headless      Run browser headless (default: True)
--disable-resources             Drop unnecessary resources for speed boost
--network-idle                  Wait for network idle
--timeout INTEGER               Timeout in milliseconds (default: 30000)
--wait INTEGER                  Additional wait time in ms (default: 0)
-s, --css-selector TEXT         Extract specific content
--wait-selector TEXT            Wait for selector before proceeding
--locale TEXT                   User locale (default: system)
--real-chrome                   Use installed Chrome browser
--proxy TEXT                    Proxy URL
-H, --extra-headers TEXT        Extra headers (multiple)
```

#### stealthy-fetch - Bypass Protection

For websites with anti-bot protection or Cloudflare:

```bash
# Bypass basic protection
scrapling extract stealthy-fetch "https://example.com" content.md

# Solve Cloudflare challenges
scrapling extract stealthy-fetch "https://nopecha.com/demo/cloudflare" data.txt \
    --solve-cloudflare \
    --css-selector "#padded_content a"

# Use proxy for anonymity (set PROXY_URL environment variable)
scrapling extract stealthy-fetch "https://site.com" content.md \
    --proxy "$PROXY_URL"

# Hide canvas fingerprint
scrapling extract stealthy-fetch "https://example.com" content.md \
    --hide-canvas \
    --block-webrtc
```

**stealthy-fetch options:** (same as fetch plus)

```
--block-webrtc                  Block WebRTC entirely
--solve-cloudflare              Solve Cloudflare challenges
--allow-webgl / --block-webgl   Allow WebGL (default: True)
--hide-canvas                   Add noise to canvas operations
```

### CSS Selector Examples

Extract specific content with the `-s` or `--css-selector` flag:

```bash
# Extract all articles
scrapling extract get "https://blog.example.com" articles.md -s "article"

# Extract specific class
scrapling extract get "https://example.com" titles.txt -s ".title"

# Extract by ID
scrapling extract get "https://example.com" content.md -s "#main-content"

# Extract links (href attributes)
scrapling extract get "https://example.com" links.txt -s "a::attr(href)"

# Extract text only
scrapling extract get "https://example.com" titles.txt -s "h1::text"

# Extract multiple elements with fetch
scrapling extract fetch "https://example.com" products.md \
    -s ".product-card" \
    --network-idle
```

## Help Commands

```bash
scrapling --help
scrapling extract --help
scrapling extract get --help
scrapling extract post --help
scrapling extract fetch --help
scrapling extract stealthy-fetch --help
```

## Resources

- Documentation: https://scrapling.readthedocs.io/
- GitHub: https://github.com/D4Vinci/Scrapling
