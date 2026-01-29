---
name: ogie
description: Extract OpenGraph, Twitter Cards, and metadata from URLs or HTML. Use when building link previews, SEO tools, or scraping webpage metadata.
license: MIT
metadata:
  author: dobroslavradosavljevic
  version: "1.0.1"
---

# OpenGraph & Metadata Extraction

Use this skill when helping users extract metadata from webpages, build link previews, create SEO tools, or parse OpenGraph/Twitter Card data.

## Quick Start

```typescript
import { extract } from "ogie";

const result = await extract("https://github.com");

if (result.success) {
  console.log(result.data.og.title);
  console.log(result.data.og.description);
  console.log(result.data.og.images[0]?.url);
}
```

## Core Functions

### `extract(url, options?)`

Fetch and extract metadata from a URL.

```typescript
import { extract } from "ogie";

const result = await extract("https://example.com", {
  timeout: 10000,
  maxRedirects: 5,
  userAgent: "MyBot/1.0",
  fetchOEmbed: true,
  convertCharset: true,
});

if (result.success) {
  console.log(result.data.og.title);
  console.log(result.data.twitter.card);
  console.log(result.data.basic.favicon);
}
```

### `extractFromHtml(html, options?)`

Extract metadata from an HTML string without network requests.

```typescript
import { extractFromHtml } from "ogie";

const html = `
  <html>
  <head>
    <meta property="og:title" content="My Page">
    <meta property="og:image" content="/images/hero.jpg">
  </head>
  </html>
`;

const result = extractFromHtml(html, {
  baseUrl: "https://example.com", // Required for relative URLs
});
```

### `extractBulk(urls, options?)`

Extract metadata from multiple URLs with rate limiting.

```typescript
import { extractBulk } from "ogie";

const result = await extractBulk(
  ["https://github.com", "https://twitter.com", "https://youtube.com"],
  {
    concurrency: 10,
    concurrencyPerDomain: 3,
    minDelayPerDomain: 200,
    onProgress: (p) => console.log(`${p.completed}/${p.total}`),
  }
);

for (const item of result.results) {
  if (item.result.success) {
    console.log(`${item.url}: ${item.result.data.og.title}`);
  }
}
```

### `createCache(options?)`

Create an LRU cache for extraction results.

```typescript
import { extract, createCache } from "ogie";

const cache = createCache({
  maxSize: 100,
  ttl: 300_000, // 5 minutes
});

// First call fetches, second returns cached
await extract("https://github.com", { cache });
await extract("https://github.com", { cache }); // Instant
```

## Extracted Metadata Types

Ogie extracts from 12 sources:

| Property               | Description                       |
| ---------------------- | --------------------------------- |
| `data.og`              | OpenGraph (title, images, etc.)   |
| `data.twitter`         | Twitter Cards                     |
| `data.basic`           | HTML meta tags, favicon, title    |
| `data.article`         | Article metadata (dates, author)  |
| `data.video`           | Video metadata (actors, duration) |
| `data.music`           | Music metadata (album, duration)  |
| `data.book`            | Book metadata (ISBN, authors)     |
| `data.profile`         | Profile metadata (name, gender)   |
| `data.jsonLd`          | JSON-LD structured data           |
| `data.dublinCore`      | Dublin Core metadata              |
| `data.appLinks`        | App Links for deep linking        |
| `data.oEmbed`          | oEmbed data (if enabled)          |
| `data.oEmbedDiscovery` | Discovered oEmbed endpoints       |

## Error Handling

```typescript
import { extract, isFetchError, isParseError } from "ogie";

const result = await extract(url);

if (!result.success) {
  switch (result.error.code) {
    case "INVALID_URL":
    case "FETCH_ERROR":
    case "TIMEOUT":
    case "PARSE_ERROR":
    case "NO_HTML":
    case "REDIRECT_LIMIT":
      console.error(result.error.message);
  }

  if (isFetchError(result.error)) {
    console.log(`HTTP Status: ${result.error.statusCode}`);
  }
}
```

## Options Reference

### ExtractOptions

| Option             | Type      | Default    | Description                 |
| ------------------ | --------- | ---------- | --------------------------- |
| `timeout`          | `number`  | `10000`    | Request timeout in ms       |
| `maxRedirects`     | `number`  | `5`        | Max redirects to follow     |
| `userAgent`        | `string`  | `ogie/1.0` | Custom User-Agent           |
| `baseUrl`          | `string`  | —          | Base URL for relative paths |
| `fetchOEmbed`      | `boolean` | `false`    | Fetch oEmbed endpoint       |
| `convertCharset`   | `boolean` | `false`    | Auto charset detection      |
| `allowPrivateUrls` | `boolean` | `false`    | Allow localhost/private IPs |
| `cache`            | `Cache`   | —          | Cache instance              |
| `bypassCache`      | `boolean` | `false`    | Force fresh fetch           |

### BulkOptions

| Option                 | Type      | Default | Description                    |
| ---------------------- | --------- | ------- | ------------------------------ |
| `concurrency`          | `number`  | `10`    | Max parallel requests          |
| `concurrencyPerDomain` | `number`  | `3`     | Max parallel per domain        |
| `minDelayPerDomain`    | `number`  | `200`   | Min ms between domain requests |
| `requestsPerMinute`    | `number`  | `600`   | Global rate limit              |
| `continueOnError`      | `boolean` | `true`  | Continue on failures           |

## Security

Ogie includes built-in protections:

- SSRF protection (blocks private IPs by default)
- URL validation (HTTP/HTTPS only)
- Redirect limits (default: 5)
- oEmbed endpoint validation

```typescript
// Allow private URLs for local development
await extract("http://localhost:3000", {
  allowPrivateUrls: true,
});
```

## Common Use Cases

### Link Preview

```typescript
const result = await extract(url);
if (result.success) {
  const preview = {
    title: result.data.og.title || result.data.basic.title,
    description: result.data.og.description || result.data.basic.description,
    image: result.data.og.images[0]?.url,
    siteName: result.data.og.siteName,
    favicon: result.data.basic.favicon,
  };
}
```

### SEO Audit

```typescript
const result = await extract(url);
if (result.success) {
  const issues = [];
  if (!result.data.og.title) issues.push("Missing og:title");
  if (!result.data.og.description) issues.push("Missing og:description");
  if (!result.data.og.images.length) issues.push("Missing og:image");
  if (!result.data.twitter.card) issues.push("Missing twitter:card");
}
```

### Batch Processing

```typescript
const urls = ["https://a.com", "https://b.com", "https://c.com"];
const result = await extractBulk(urls, {
  concurrency: 5,
  onProgress: (p) => console.log(`${p.succeeded}/${p.total} done`),
});
console.log(`Success rate: ${result.stats.succeeded}/${result.stats.total}`);
```
