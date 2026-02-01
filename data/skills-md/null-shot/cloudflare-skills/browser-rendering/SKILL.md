---
name: browser-rendering
description: Headless Chrome automation for web scraping, screenshots, PDFs, and testing at the edge. Load when capturing page screenshots, generating PDFs, scraping dynamic content, extracting structured data, or automating browser interactions. Supports REST API, Puppeteer, Playwright, and Stagehand.
---

# Browser Rendering

Cloudflare Browser Rendering provides headless Chrome instances on the global edge network for web scraping, screenshots, PDF generation, and automated testing. Choose from **REST API** for simple tasks or **Workers Bindings** (Puppeteer, Playwright, Stagehand) for advanced automation.

## Choosing an Integration Method

| Method | Use Case | Complexity |
|--------|----------|------------|
| **REST API** | Simple screenshots, PDFs, markdown extraction, structured data | Low - just HTTP requests |
| **Puppeteer** | Industry-standard Chrome automation, porting existing scripts | Medium - familiar API |
| **Playwright** | Modern cross-browser automation, AI agent integration (MCP) | Medium - developer-friendly |
| **Stagehand** | AI-native automation with natural language selectors | Low - resilient to site changes |

## REST API Method

For simple, stateless tasks like capturing screenshots or generating PDFs without writing complex scripts.

### Setup

Create an API token with `Browser Rendering - Edit` permission in the Cloudflare dashboard.

### Available Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/content` | Fetch fully-rendered HTML |
| `/screenshot` | Capture page screenshot |
| `/pdf` | Generate PDF document |
| `/snapshot` | Take webpage snapshot |
| `/scrape` | Extract HTML elements |
| `/json` | Capture structured data using AI |
| `/links` | Retrieve all links from page |
| `/markdown` | Extract markdown content |

### REST API Example

```bash
curl -X POST \
  https://api.cloudflare.com/client/v4/accounts/{account_id}/browser-rendering/screenshot \
  -H "Authorization: Bearer {api_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "fullPage": true,
    "type": "png"
  }' \
  --output screenshot.png
```

**Monitoring usage:** Check the `X-Browser-Ms-Used` header in responses to see browser time consumed (in milliseconds).

## Workers Bindings Method

For complex workflows, persistent sessions, and custom automation. Requires deploying a Cloudflare Worker.

### Configuration

Add browser binding to `wrangler.jsonc`:

```jsonc
{
  "name": "browser-automation",
  "main": "src/index.ts",
  "compatibility_date": "2025-09-17",
  "compatibility_flags": ["nodejs_compat"],
  "browser": {
    "binding": "BROWSER"
  }
}
```

### Option A: Puppeteer

Industry-standard Chrome automation API, ideal for porting existing scripts.

**Installation:**
```bash
npm install @cloudflare/puppeteer --save-dev
```

**Basic example:**

```typescript
import puppeteer from "@cloudflare/puppeteer";

interface Env {
  BROWSER: Fetcher;
}

export default {
  async fetch(request, env): Promise<Response> {
    const { searchParams } = new URL(request.url);
    const url = searchParams.get("url");

    if (!url) {
      return new Response("Missing ?url parameter", { status: 400 });
    }

    const browser = await puppeteer.launch(env.BROWSER);
    try {
      const page = await browser.newPage();
      await page.goto(url);
      const text = await page.$eval("body", (el) => el.textContent);

      return Response.json({ bodyText: text });
    } finally {
      await browser.close();
    }
  },
} satisfies ExportedHandler<Env>;
```

### Option B: Playwright (Recommended for New Projects)

Modern browser automation with developer-friendly API and AI agent integration.

**Installation:**
```bash
npm install @cloudflare/playwright --save-dev
```

**Current version:** v1.57.0

**Basic example:**

```typescript
import { launch } from "@cloudflare/playwright";

interface Env {
  BROWSER: Fetcher;
}

export default {
  async fetch(request, env): Promise<Response> {
    const browser = await launch(env.BROWSER);
    try {
      const page = await browser.newPage();
      await page.goto("https://example.com");
      
      const title = await page.title();
      const screenshot = await page.screenshot({ type: "png" });

      return new Response(screenshot, {
        headers: { "Content-Type": "image/png" },
      });
    } finally {
      await browser.close();
    }
  },
} satisfies ExportedHandler<Env>;
```

**Playwright advantages:**
- Built-in test assertions with `expect()` from `@cloudflare/playwright/test`
- Trace files for debugging (downloadable `trace.zip`)
- Storage state for persisting cookies/localStorage
- MCP integration for AI agents

### Option C: Stagehand (AI-Native)

Uses natural language selectors instead of brittle CSS selectors, making automation resilient to website changes.

**Example:**
```typescript
// Instead of: await page.click("#submit-button")
// Use natural language: await page.act("click the submit button")
```

Stagehand is ideal for AI agents that need to autonomously navigate websites without breaking when the DOM structure changes.

## FIRST: Installation (Workers Bindings)

Choose your library and install:

```bash
# Puppeteer (industry standard)
npm install @cloudflare/puppeteer --save-dev

# OR Playwright (modern, recommended)
npm install @cloudflare/playwright --save-dev

# OR Stagehand (AI-native)
npm install @cloudflare/stagehand --save-dev
```

## When to Use Browser Rendering

| Use Case | Recommended Method | Why |
|----------|-------------------|-----|
| Simple screenshots | REST API | No code required, just HTTP request |
| PDF generation | REST API or Puppeteer | REST for simple, Puppeteer for custom headers/auth |
| Web scraping | Puppeteer or Playwright | Full DOM access, complex navigation |
| Automated testing | Playwright | Built-in assertions, trace files |
| SEO analysis | REST API `/markdown` or `/json` | AI-powered structured extraction |
| AI agents | Playwright (MCP) or Stagehand | Natural language automation, resilient selectors |
| Page monitoring | REST API or Puppeteer | REST for periodic checks, Puppeteer for complex flows |

## Quick Reference

| Operation | API |
|-----------|-----|
| Launch browser | `await puppeteer.launch(env.BROWSER_RENDERING)` |
| Create new page | `await browser.newPage()` |
| Navigate to URL | `await page.goto(url)` |
| Get HTML content | `await page.content()` |
| Extract text | `await page.$eval("selector", el => el.textContent)` |
| Take screenshot | `await page.screenshot({ type: "png" })` |
| Generate PDF | `await page.pdf({ format: "A4" })` |
| Close browser | `await browser.close()` |

## Basic Page Scraping

```typescript
import puppeteer from "@cloudflare/puppeteer";

interface Env {
  BROWSER_RENDERING: Fetcher;
}

export default {
  async fetch(request, env): Promise<Response> {
    const { searchParams } = new URL(request.url);
    let url = searchParams.get("url");

    if (url) {
      url = new URL(url).toString(); // normalize
      const browser = await puppeteer.launch(env.BROWSER_RENDERING);
      const page = await browser.newPage();
      await page.goto(url);
      
      // Parse the page content
      const content = await page.content();
      
      // Find text within the page content
      const text = await page.$eval("body", (el) => el.textContent);
      
      // Do something with the text
      // e.g. log it to the console, write it to KV, or store it in a database.
      console.log(text);

      // Ensure we close the browser session
      await browser.close();

      return Response.json({
        bodyText: text,
      });
    } else {
      return Response.json({
        error: "Please add an ?url=https://example.com/ parameter"
      }, { status: 400 });
    }
  },
} satisfies ExportedHandler<Env>;
```

## Screenshot Capture

Capture screenshots of web pages as PNG or JPEG:

```typescript
import puppeteer from "@cloudflare/puppeteer";

interface Env {
  BROWSER_RENDERING: Fetcher;
}

export default {
  async fetch(request, env): Promise<Response> {
    const { searchParams } = new URL(request.url);
    const url = searchParams.get("url");

    if (!url) {
      return new Response("Missing ?url parameter", { status: 400 });
    }

    const browser = await puppeteer.launch(env.BROWSER_RENDERING);
    try {
      const page = await browser.newPage();
      
      // Set viewport size
      await page.setViewport({ width: 1920, height: 1080 });
      
      await page.goto(url, { waitUntil: "networkidle0" });
      
      // Capture screenshot
      const screenshot = await page.screenshot({
        type: "png",
        fullPage: true, // Capture entire page
      });

      return new Response(screenshot, {
        headers: { "Content-Type": "image/png" },
      });
    } finally {
      await browser.close();
    }
  },
} satisfies ExportedHandler<Env>;
```

## PDF Generation

Convert web pages to PDF documents:

```typescript
import puppeteer from "@cloudflare/puppeteer";

interface Env {
  BROWSER_RENDERING: Fetcher;
}

export default {
  async fetch(request, env): Promise<Response> {
    const { searchParams } = new URL(request.url);
    const url = searchParams.get("url");

    if (!url) {
      return new Response("Missing ?url parameter", { status: 400 });
    }

    const browser = await puppeteer.launch(env.BROWSER_RENDERING);
    try {
      const page = await browser.newPage();
      await page.goto(url, { waitUntil: "networkidle0" });
      
      // Generate PDF
      const pdf = await page.pdf({
        format: "A4",
        printBackground: true,
        margin: {
          top: "20px",
          right: "20px",
          bottom: "20px",
          left: "20px",
        },
      });

      return new Response(pdf, {
        headers: { "Content-Type": "application/pdf" },
      });
    } finally {
      await browser.close();
    }
  },
} satisfies ExportedHandler<Env>;
```

## Browser Lifecycle Management

**CRITICAL: Always close the browser after use** to prevent memory leaks and ensure resources are freed:

```typescript
const browser = await puppeteer.launch(env.BROWSER_RENDERING);
try {
  const page = await browser.newPage();
  // ... perform operations
} finally {
  // Always close, even if an error occurs
  await browser.close();
}
```

**Best practices:**

1. Use try/finally to ensure cleanup
2. Close browser even if operations fail
3. Each request should launch and close its own browser
4. Don't reuse browser instances across requests
5. Set reasonable timeouts to prevent hanging

## DOM Manipulation and Extraction

Extract structured data from pages:

```typescript
const browser = await puppeteer.launch(env.BROWSER_RENDERING);
try {
  const page = await browser.newPage();
  await page.goto(url);
  
  // Extract multiple elements
  const data = await page.evaluate(() => {
    return {
      title: document.querySelector("h1")?.textContent,
      links: Array.from(document.querySelectorAll("a")).map(a => ({
        text: a.textContent,
        href: a.href,
      })),
      images: Array.from(document.querySelectorAll("img")).map(img => img.src),
    };
  });

  return Response.json(data);
} finally {
  await browser.close();
}
```

## Wait Strategies

Wait for content to load before scraping:

```typescript
const page = await browser.newPage();
await page.goto(url);

// Wait for specific selector
await page.waitForSelector(".content-loaded");

// Wait for navigation with options
await page.goto(url, {
  waitUntil: "networkidle0", // Wait until network is idle
  timeout: 30000, // 30 second timeout
});

// Wait for custom condition
await page.waitForFunction(() => {
  return document.querySelector(".dynamic-content") !== null;
});
```

## Error Handling

Handle common browser automation errors:

```typescript
const browser = await puppeteer.launch(env.BROWSER_RENDERING);
try {
  const page = await browser.newPage();
  
  // Set timeout for navigation
  await page.goto(url, { timeout: 30000 });
  
} catch (error) {
  if (error.name === "TimeoutError") {
    return new Response("Page load timeout", { status: 504 });
  }
  
  console.error("Browser error:", error);
  return new Response("Browser automation failed", { status: 500 });
  
} finally {
  await browser.close();
}
```

## Puppeteer vs Playwright

| Feature | Puppeteer | Playwright |
|---------|-----------|------------|
| API Style | Chrome DevTools Protocol | Higher-level abstractions |
| Test Assertions | Manual | Built-in `expect()` |
| Debugging | Console logs | Trace files with GUI |
| Storage Persistence | Manual | Built-in storage state API |
| MCP Integration | No | Yes (for AI agents) |

**Choose Puppeteer if:** You have existing scripts or prefer Chrome DevTools Protocol.

**Choose Playwright if:** Starting new, need test assertions, want better debugging, or building AI agents.

See [references/puppeteer.md](references/puppeteer.md) for complete Playwright-specific features including test assertions, trace files, and storage state patterns

## Detailed References

- **[references/puppeteer.md](references/puppeteer.md)** - Complete Puppeteer API reference
- **[references/patterns.md](references/patterns.md)** - Advanced patterns (caching, rate limiting, authentication)
- **[references/limits.md](references/limits.md)** - Limits, quotas, pricing, and troubleshooting
- **[references/testing.md](references/testing.md)** - Mocking Puppeteer, testing browser logic

## Best Practices

### General

1. **Choose the right method**: REST API for simple tasks, Workers Bindings for complex automation
2. **Always close browsers**: Use try/finally to ensure `browser.close()` is called (Workers Bindings only)
3. **Monitor usage**: Check `X-Browser-Ms-Used` header (REST) or dashboard for browser time consumed
4. **Set timeouts**: Prevent hanging requests with reasonable timeout values
5. **Handle errors gracefully**: Catch TimeoutError and 429 rate limit errors
6. **Test locally first**: Use `wrangler dev` to iterate before deploying

### Workers Bindings Specific

7. **Reuse sessions**: Keep browsers open with `keep_alive` option (up to 10 minutes) for better performance
8. **Use waitUntil options**: Wait for appropriate page state (networkidle0, load, domcontentloaded)
9. **Consider caching**: Cache static screenshots/PDFs in R2 or KV
10. **Respect robots.txt**: Check site policies before automated scraping
11. **Check session history**: Use `playwright.history()` or `puppeteer.history()` to debug idle timeouts

### REST API Specific

12. **Spread requests evenly**: Rate limits are per-second, not burst (e.g., 6/min = 1 per 10 seconds)
13. **Handle 429 responses**: Read `Retry-After` header and retry appropriately
14. **Use AI endpoints**: `/json` and `/markdown` endpoints use AI for structured extraction

## Common Patterns

See [references/patterns.md](references/patterns.md) for complete examples including:
- Session reuse and keep-alive for performance
- Authentication with custom headers
- Custom user agents
- Caching screenshots in R2
- Rate limiting with Durable Objects
