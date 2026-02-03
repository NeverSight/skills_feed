---
name: website-to-vite-scraper
description: Multi-provider website scraper that converts any website (including CSR/SPA) to deployable static sites. Uses Playwright, Apify RAG Browser, Crawl4AI, and Firecrawl for comprehensive scraping. Triggers on requests to clone, reverse-engineer, or convert websites.
version: "2.0"
---

# Website-to-Vite Scraper V2

Multi-provider website scraper with AI-powered extraction for any website type.

## Scraping Methods

| Method | Best For | Anti-Bot | JS Rendering | Cost |
|--------|----------|----------|--------------|------|
| **Playwright** | General sites, Next.js/React apps | ❌ | ✅ Full | FREE |
| **Apify RAG Browser** | LLM/RAG-optimized content | ✅ | ✅ Adaptive | Credits |
| **Crawl4AI** | AI training data, clean extraction | ✅ | ✅ | Credits |
| **Firecrawl** | Protected sites, anti-bot bypass | ✅✅ | ✅ | $16/mo |

## Quick Start

### GitHub Actions (Recommended)

```bash
# Go to: Actions → Website Scraper V2 → Run workflow
# Options:
#   - URL: https://www.reventure.app/
#   - Project name: reventure-clone
#   - Method: all (tries all providers)
#   - Deploy: true
```

### API MEGA LIBRARY Integration

The following APIs from our library enhance this scraper:

| API | Purpose | Status |
|-----|---------|--------|
| `APIFY_API_TOKEN` | RAG Browser, Crawl4AI, Web Scraper | ✅ Configured |
| `FIRECRAWL_API_KEY` | Anti-bot bypass, stealth mode | ✅ Configured |
| `BROWSERLESS_API_KEY` | Alternative headless browser | 🔄 Available |

### MCP Server Integration

Connect Claude Desktop/Cursor to Apify MCP for AI-powered scraping:

```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": ["@apify/actors-mcp-server"],
      "env": {
        "APIFY_TOKEN": "your-apify-api-token"
      }
    }
  }
}
```

Or use hosted: `https://mcp.apify.com?token=YOUR_TOKEN`

## Apify Actors Used

### apify/rag-web-browser
- **Purpose:** LLM-optimized web content extraction
- **Output:** Markdown, HTML, text
- **Features:** 
  - Playwright adaptive (handles JS)
  - Clean content extraction
  - Link following
  - Metadata extraction

### raizen/ai-web-scraper (Crawl4AI)
- **Purpose:** AI training data collection
- **Output:** Cleaned markdown, structured links
- **Features:**
  - Excludes boilerplate (headers, footers, nav)
  - Word count thresholding
  - External link filtering

### Firecrawl
- **Purpose:** Anti-bot protected sites
- **Output:** Markdown, HTML, screenshots
- **Features:**
  - Anti-detection technology
  - JavaScript rendering
  - Main content extraction
  - 5-second wait for dynamic content

## Output Structure

```
project-name/
├── dist/
│   ├── index.html      # Best merged HTML
│   ├── screenshot.png  # Full page capture
│   ├── meta.json       # Scrape metadata
│   └── assets/
│       ├── images/     # Downloaded images
│       ├── css/        # Stylesheets
│       └── js/         # Scripts
└── results/
    ├── playwright/     # Raw Playwright output
    ├── apify-rag/      # RAG Browser output
    ├── crawl4ai/       # Crawl4AI output
    └── firecrawl/      # Firecrawl output
```

## Handling CSR/SPA Sites

Sites like Next.js, React, Vue that render client-side require JavaScript execution:

1. **Playwright** waits for `networkidle` + 5 seconds
2. **Apify RAG** uses adaptive crawler (Playwright when needed)
3. **Firecrawl** has built-in JS rendering

For `__NEXT_DATA__` extraction (Next.js sites):
- Playwright automatically extracts and saves to `next_data.json`
- Can be parsed to reconstruct static pages

## Workflow Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | string | required | Website URL to scrape |
| `project_name` | string | required | Output folder/Cloudflare project name |
| `scrape_method` | choice | playwright | Method to use |
| `extract_assets` | boolean | true | Download images/CSS/JS |
| `deploy_cloudflare` | boolean | true | Deploy to Cloudflare Pages |

## Cost Optimization

| Scenario | Recommended Method |
|----------|-------------------|
| Simple static site | Playwright (FREE) |
| JS-heavy SPA | Playwright → Apify RAG fallback |
| Protected site (Cloudflare) | Firecrawl |
| AI/RAG pipeline | Apify RAG or Crawl4AI |
| Maximum coverage | `all` method |

## Security Assessment

Per API_MEGA_LIBRARY guidelines:

| API | Security Score | Recommendation |
|-----|----------------|----------------|
| Apify | 85/100 | ✅ ADOPT |
| Firecrawl | 82/100 | ✅ ADOPT |
| Playwright | 90/100 | ✅ ADOPT (local) |

## Troubleshooting

### Site returns blank page
1. Try `scrape_method: all` to use multiple providers
2. Increase wait time in Playwright
3. Check if site blocks datacenter IPs → use Firecrawl

### Assets not downloading
1. Some sites block direct asset requests
2. Use relative paths from original HTML
3. Check for CORS restrictions

### Cloudflare protection detected
1. Use Firecrawl (has anti-bot bypass)
2. Or use Apify with residential proxies

## Related Skills

- `auction-results` - Uses similar scraping for auction data
- `bcpao-scraper` - BCPAO property data extraction
- `youtube-transcript` - Video content extraction

## Changelog

### V2.0 (Dec 2025)
- Added multi-provider support (Playwright, Apify, Firecrawl)
- MCP server integration
- Automatic provider fallback
- Asset downloading
- Cloudflare Pages deployment

### V1.0 (Dec 2025)
- Initial Playwright-only scraper
- Basic HTML/CSS/JS extraction
