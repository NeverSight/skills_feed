---
name: apify-scraper-builder
description: Build Apify Actors (web scrapers) using Node.js and Crawlee. Use when creating new scrapers, defining input schemas, configuring Dockerfiles, or deploying to Apify. Triggers include apify, actor, scraper, crawlee, web scraping, data extraction.
---

# Apify Scraper Builder

Build production-ready Apify Actors using Node.js/TypeScript and Crawlee.

## Crawler Type Decision Tree

| Scenario | Crawler | Why |
|----------|---------|-----|
| Static HTML, no JavaScript | **CheerioCrawler** | Fastest, lowest memory |
| JavaScript-rendered content | **PlaywrightCrawler** | Modern, cross-browser |
| Legacy sites, specific Chrome behavior | **PuppeteerCrawler** | Chrome-specific features |
| Need to handle both static and JS | **PlaywrightCrawler** | More versatile |
| High-volume scraping (1000s pages) | **CheerioCrawler** | Best performance |

## Actor Creation Workflow

### Step 1: Initialize Project
```bash
python scripts/init_actor.py my-scraper --type cheerio
```
Or manually create structure:
```
my-scraper/
├── .actor/
│   ├── actor.json           # REQUIRED
│   ├── input_schema.json    # Recommended
│   └── Dockerfile           # REQUIRED
├── src/
│   └── main.ts              # Entry point
├── package.json
└── tsconfig.json
```

### Step 2: Configure actor.json
```json
{
    "actorSpecification": 1,
    "name": "my-scraper",
    "version": "0.0",
    "buildTag": "latest",
    "input": "./input_schema.json",
    "dockerfile": "./Dockerfile"
}
```

### Step 3: Define Input Schema
```bash
python scripts/generate_input_schema.py "Scrape product pages with URLs, max items limit, and proxy support"
```
Or use templates from `references/input-schema-guide.md`

### Step 4: Implement Crawler
Use patterns from `references/crawlee-patterns.md`

### Step 5: Validate Configuration
```bash
python scripts/validate_actor.py /path/to/actor
```

### Step 6: Deploy
```bash
apify login
apify push
```

## Project Structure

### Required Files

#### .actor/actor.json
```json
{
    "actorSpecification": 1,
    "name": "my-scraper",
    "version": "0.0",
    "buildTag": "latest",
    "minMemoryMbytes": 256,
    "maxMemoryMbytes": 4096,
    "dockerfile": "./Dockerfile",
    "input": "./input_schema.json",
    "storages": {
        "dataset": "./dataset_schema.json"
    }
}
```

#### .actor/Dockerfile (Node.js)
```dockerfile
FROM apify/actor-node:20

COPY package*.json ./
RUN npm --quiet set progress=false \
    && npm install --omit=dev --omit=optional \
    && echo "Installed NPM packages:" \
    && npm list || true \
    && echo "Node.js version:" \
    && node --version \
    && echo "NPM version:" \
    && npm --version

COPY . ./
CMD npm start
```

#### package.json
```json
{
    "name": "my-scraper",
    "version": "0.0.1",
    "type": "module",
    "main": "dist/main.js",
    "scripts": {
        "start": "node dist/main.js",
        "build": "tsc"
    },
    "dependencies": {
        "apify": "^3.0.0",
        "crawlee": "^3.0.0"
    },
    "devDependencies": {
        "typescript": "^5.0.0"
    }
}
```

## Input Schema Editors

| Editor | Use Case | Example |
|--------|----------|---------|
| `textfield` | Single-line text | Name, URL |
| `textarea` | Multi-line text | CSS selectors, notes |
| `requestListSources` | URL list with labels | Start URLs |
| `proxy` | Proxy configuration | Apify Proxy settings |
| `json` | JSON object/array | Custom configuration |
| `select` | Dropdown options | Country, category |
| `checkbox` | Boolean toggle | Debug mode |
| `number` | Integer/float | Max items, delay |
| `datepicker` | Date selection | Date range filter |

### Common Input Schema Pattern
```json
{
    "title": "Scraper Input",
    "type": "object",
    "schemaVersion": 1,
    "properties": {
        "startUrls": {
            "title": "Start URLs",
            "type": "array",
            "description": "URLs to start scraping from",
            "editor": "requestListSources",
            "prefill": [{"url": "https://example.com"}]
        },
        "maxItems": {
            "title": "Max Items",
            "type": "integer",
            "description": "Maximum number of items to scrape",
            "default": 100,
            "minimum": 1
        },
        "proxyConfig": {
            "title": "Proxy Configuration",
            "type": "object",
            "description": "Proxy settings for the scraper",
            "editor": "proxy",
            "default": {"useApifyProxy": true}
        }
    },
    "required": ["startUrls"]
}
```

## Crawlee Patterns

### CheerioCrawler (Fast HTML Parsing)
```typescript
import { Actor } from 'apify';
import { CheerioCrawler, Dataset } from 'crawlee';

await Actor.init();

const input = await Actor.getInput<{
    startUrls: { url: string }[];
    maxItems: number;
}>();

const crawler = new CheerioCrawler({
    maxRequestsPerCrawl: input?.maxItems || 100,
    async requestHandler({ request, $, enqueueLinks }) {
        const title = $('h1').text().trim();
        const price = $('.price').text().trim();

        await Dataset.pushData({
            url: request.url,
            title,
            price,
        });

        // Enqueue pagination links
        await enqueueLinks({
            selector: 'a.next-page',
        });
    },
});

await crawler.run(input?.startUrls?.map(u => u.url) || []);
await Actor.exit();
```

### PlaywrightCrawler (JavaScript Rendering)
```typescript
import { Actor } from 'apify';
import { PlaywrightCrawler, Dataset } from 'crawlee';

await Actor.init();

const input = await Actor.getInput<{
    startUrls: { url: string }[];
    maxItems: number;
}>();

const proxyConfiguration = await Actor.createProxyConfiguration(
    input?.proxyConfig
);

const crawler = new PlaywrightCrawler({
    proxyConfiguration,
    maxRequestsPerCrawl: input?.maxItems || 100,
    async requestHandler({ page, request, enqueueLinks }) {
        // Wait for dynamic content
        await page.waitForSelector('.product-list');

        const products = await page.$$eval('.product', items =>
            items.map(item => ({
                title: item.querySelector('h2')?.textContent?.trim(),
                price: item.querySelector('.price')?.textContent?.trim(),
            }))
        );

        for (const product of products) {
            await Dataset.pushData({
                url: request.url,
                ...product,
            });
        }

        await enqueueLinks({
            selector: 'a.pagination',
        });
    },
});

await crawler.run(input?.startUrls?.map(u => u.url) || []);
await Actor.exit();
```

### PuppeteerCrawler (Chrome-specific)
```typescript
import { Actor } from 'apify';
import { PuppeteerCrawler, Dataset } from 'crawlee';

await Actor.init();

const input = await Actor.getInput<{
    startUrls: { url: string }[];
}>();

const crawler = new PuppeteerCrawler({
    launchContext: {
        launchOptions: {
            headless: true,
        },
    },
    async requestHandler({ page, request }) {
        await page.waitForSelector('.content');

        const data = await page.evaluate(() => ({
            title: document.querySelector('h1')?.textContent,
            content: document.querySelector('.content')?.innerHTML,
        }));

        await Dataset.pushData({
            url: request.url,
            ...data,
        });
    },
});

await crawler.run(input?.startUrls?.map(u => u.url) || []);
await Actor.exit();
```

## Scripts

### Initialize New Actor
```bash
python scripts/init_actor.py <name> --type <cheerio|playwright|puppeteer> [--path <dir>]
```

### Validate Actor Configuration
```bash
python scripts/validate_actor.py <actor-path>
```

### Generate Input Schema
```bash
python scripts/generate_input_schema.py "<description>" [--output <path>]
```

## Deployment Commands

```bash
# Install Apify CLI
npm install -g @apify/cli

# Login to Apify
apify login

# Create new Actor from template (interactive)
apify create my-actor

# Run Actor locally
apify run --purge

# Push to Apify platform
apify push

# Build Actor remotely
apify actors build

# Call Actor remotely
apify actors call <actor-id>

# Pull Actor code from Apify
apify actors pull <actor-id>
```

## Validation Checklist

### Before Building
- [ ] Correct crawler type selected for target site
- [ ] Input schema defines all required parameters
- [ ] Dependencies in package.json are correct

### Configuration
- [ ] actor.json has actorSpecification: 1
- [ ] actor.json has valid name and version
- [ ] Dockerfile uses correct Node.js base image
- [ ] Input schema editors match field types

### Code Quality
- [ ] Error handling for network failures
- [ ] Proxy configuration used for production
- [ ] Rate limiting/delays configured
- [ ] Data validation before pushData

### Pre-Deployment
- [ ] `apify run --purge` succeeds locally
- [ ] Output data structure is correct
- [ ] Memory limits are appropriate

## References

| Topic | File |
|-------|------|
| actor.json Specification | `references/actor-json-spec.md` |
| Input Schema Editors | `references/input-schema-guide.md` |
| Crawlee Patterns | `references/crawlee-patterns.md` |

## Templates

| Template | Description | Path |
|----------|-------------|------|
| Cheerio | Fast HTML scraping | `templates/crawlee-cheerio/` |
| Playwright | JS-rendered content | `templates/crawlee-playwright/` |
| Puppeteer | Chrome-specific | `templates/crawlee-puppeteer/` |
