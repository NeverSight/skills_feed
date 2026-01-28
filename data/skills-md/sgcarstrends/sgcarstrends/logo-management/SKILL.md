---
name: logo-management
description: Manage car logo fetching, scraping, and Vercel Blob storage in the logos package. Use when updating logo sources, debugging brand name normalization, or managing logo cache.
allowed-tools: Read, Edit, Bash, Grep, Glob
---

# Logo Management Skill

This skill helps you manage car logos in `packages/logos/`.

## When to Use This Skill

- Adding new car brand logos
- Updating logo sources or URLs
- Debugging logo fetching failures
- Implementing brand name normalization
- Managing Vercel Blob storage
- Optimizing logo caching with Redis
- Scraping logos from external sources

## Logo Package Architecture

```
packages/logos/
├── src/
│   ├── services/
│   │   └── logo/
│   │       ├── fetch.ts        # Logo fetching logic
│   │       ├── list.ts         # List available logos
│   │       └── download.ts     # Download logos to Blob
│   ├── infra/
│   │   └── storage/
│   │       └── blob.ts         # Vercel Blob service
│   ├── utils/
│   │   └── normalize.ts        # Brand name normalization
│   └── index.ts                # Package exports
├── scripts/
│   ├── fetch-logos.ts          # Fetch all logos
│   └── upload-to-blob.ts       # Upload to Vercel Blob
└── package.json
```

## Core Functionality

### Brand Name Normalization

```typescript
// packages/logos/src/utils/normalize.ts

/**
 * Normalize brand names to match logo file names
 */
export function normalizeBrandName(brand: string): string {
  return brand
    .toLowerCase()
    .trim()
    .replace(/\s+/g, "-")           // Replace spaces with hyphens
    .replace(/[^a-z0-9-]/g, "")     // Remove special characters
    .replace(/-+/g, "-")             // Remove duplicate hyphens
    .replace(/^-|-$/g, "");          // Remove leading/trailing hyphens
}

// Examples
normalizeBrandName("Mercedes-Benz");  // "mercedes-benz"
normalizeBrandName("BMW");            // "bmw"
normalizeBrandName("Land Rover");     // "land-rover"
normalizeBrandName("Alfa Romeo");     // "alfa-romeo"

/**
 * Handle special cases and aliases
 */
const BRAND_ALIASES: Record<string, string> = {
  "mercedes": "mercedes-benz",
  "merc": "mercedes-benz",
  "benz": "mercedes-benz",
  "vw": "volkswagen",
  "bmw": "bmw",
  "landrover": "land-rover",
  "alfa": "alfa-romeo",
};

export function resolveBrandAlias(brand: string): string {
  const normalized = normalizeBrandName(brand);
  return BRAND_ALIASES[normalized] || normalized;
}
```

### Logo Fetching

```typescript
// packages/logos/src/services/logo/fetch.ts
import { redis } from "@sgcarstrends/utils";
import { normalizeBrandName } from "../../utils/normalize";

const LOGO_CDN_BASE = "https://cdn.example.com/logos";
const CACHE_TTL = 7 * 24 * 60 * 60; // 7 days

export async function getLogoUrl(brand: string): Promise<string | null> {
  const normalizedBrand = normalizeBrandName(brand);
  const cacheKey = `logo:url:${normalizedBrand}`;

  // Check cache
  const cached = await redis.get<string>(cacheKey);
  if (cached) {
    console.log(`Logo cache hit: ${normalizedBrand}`);
    return cached;
  }

  // Fetch logo URL
  const logoUrl = await fetchLogoUrl(normalizedBrand);

  if (logoUrl) {
    // Cache the URL
    await redis.set(cacheKey, logoUrl, { ex: CACHE_TTL });
  }

  return logoUrl;
}

async function fetchLogoUrl(brand: string): Promise<string | null> {
  const possibleExtensions = ["svg", "png", "jpg"];

  for (const ext of possibleExtensions) {
    const url = `${LOGO_CDN_BASE}/${brand}.${ext}`;

    try {
      const response = await fetch(url, { method: "HEAD" });

      if (response.ok) {
        console.log(`Found logo: ${url}`);
        return url;
      }
    } catch (error) {
      console.error(`Failed to fetch ${url}:`, error);
    }
  }

  console.warn(`No logo found for: ${brand}`);
  return null;
}
```

### Vercel Blob Storage

```typescript
// packages/logos/src/infra/storage/blob.ts
import { put, list, del } from "@vercel/blob";
import { redis } from "@sgcarstrends/utils";

const BLOB_PREFIX = "logos";

export class LogoBlobService {
  /**
   * Upload logo to Vercel Blob
   */
  async upload(brand: string, file: Buffer | File): Promise<string> {
    const normalizedBrand = normalizeBrandName(brand);
    const fileName = `${BLOB_PREFIX}/${normalizedBrand}.png`;

    const blob = await put(fileName, file, {
      access: "public",
      addRandomSuffix: false,
    });

    // Cache blob URL
    await redis.set(
      `logo:blob:${normalizedBrand}`,
      blob.url,
      { ex: 7 * 24 * 60 * 60 } // 7 days
    );

    console.log(`Uploaded logo to: ${blob.url}`);
    return blob.url;
  }

  /**
   * List all logos in Blob storage
   */
  async list(): Promise<string[]> {
    const { blobs } = await list({ prefix: BLOB_PREFIX });

    return blobs.map(blob => blob.url);
  }

  /**
   * Delete logo from Blob storage
   */
  async delete(brand: string): Promise<void> {
    const normalizedBrand = normalizeBrandName(brand);
    const fileName = `${BLOB_PREFIX}/${normalizedBrand}.png`;

    await del(fileName);

    // Invalidate cache
    await redis.del(`logo:blob:${normalizedBrand}`);

    console.log(`Deleted logo: ${fileName}`);
  }

  /**
   * Get logo URL from Blob storage
   */
  async getUrl(brand: string): Promise<string | null> {
    const normalizedBrand = normalizeBrandName(brand);
    const cacheKey = `logo:blob:${normalizedBrand}`;

    // Check cache
    const cached = await redis.get<string>(cacheKey);
    if (cached) {
      return cached;
    }

    // List and find
    const logos = await this.list();
    const logoUrl = logos.find(url => url.includes(normalizedBrand));

    if (logoUrl) {
      // Cache the result
      await redis.set(cacheKey, logoUrl, { ex: 7 * 24 * 60 * 60 });
    }

    return logoUrl || null;
  }
}

export const logoBlobService = new LogoBlobService();
```

### Logo Scraping

```typescript
// packages/logos/src/services/logo/scrape.ts
import * as cheerio from "cheerio";

interface ScrapedLogo {
  brand: string;
  url: string;
  source: string;
}

/**
 * Scrape logos from car manufacturer websites
 */
export async function scrapeLogos(): Promise<ScrapedLogo[]> {
  const sources = [
    {
      name: "CarLogos.org",
      url: "https://www.carlogos.org/car-brands/",
      selector: ".car-brand-logo img",
    },
    // Add more sources as needed
  ];

  const logos: ScrapedLogo[] = [];

  for (const source of sources) {
    try {
      const html = await fetch(source.url).then(res => res.text());
      const $ = cheerio.load(html);

      $(source.selector).each((_, element) => {
        const $el = $(element);
        const brand = $el.attr("alt") || "";
        const url = $el.attr("src") || "";

        if (brand && url) {
          logos.push({
            brand: normalizeBrandName(brand),
            url: url.startsWith("http") ? url : new URL(url, source.url).href,
            source: source.name,
          });
        }
      });

      console.log(`Scraped ${logos.length} logos from ${source.name}`);
    } catch (error) {
      console.error(`Failed to scrape ${source.name}:`, error);
    }
  }

  return logos;
}

/**
 * Download and upload scraped logos to Blob
 */
export async function processScrape dLogos(logos: ScrapedLogo[]) {
  for (const logo of logos) {
    try {
      // Download logo
      const response = await fetch(logo.url);
      const buffer = Buffer.from(await response.arrayBuffer());

      // Upload to Blob
      await logoBlobService.upload(logo.brand, buffer);

      console.log(`Processed logo: ${logo.brand}`);
    } catch (error) {
      console.error(`Failed to process ${logo.brand}:`, error);
    }
  }
}
```

## Public API

```typescript
// packages/logos/src/index.ts
export { getLogoUrl } from "./services/logo/fetch";
export { logoBlobService } from "./infra/storage/blob";
export { normalizeBrandName, resolveBrandAlias } from "./utils/normalize";
export { scrapeLogos, processScrapedLogos } from "./services/logo/scrape";
```

## Usage in Applications

### In API Routes

```typescript
// apps/api/src/routes/logos.ts
import { Hono } from "hono";
import { getLogoUrl } from "@sgcarstrends/logos";

const app = new Hono();

app.get("/logos/:brand", async (c) => {
  const brand = c.req.param("brand");

  const logoUrl = await getLogoUrl(brand);

  if (!logoUrl) {
    return c.json({ error: "Logo not found" }, 404);
  }

  return c.json({ brand, logoUrl });
});

export default app;
```

### In Next.js Components

```tsx
// apps/web/src/components/car-logo.tsx
"use client";

import { useState, useEffect } from "react";
import Image from "next/image";

interface CarLogoProps {
  brand: string;
  size?: number;
}

export function CarLogo({ brand, size = 64 }: CarLogoProps) {
  const [logoUrl, setLogoUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/api/logos/${brand}`)
      .then(res => res.json())
      .then(data => {
        setLogoUrl(data.logoUrl);
        setLoading(false);
      })
      .catch(() => {
        setLoading(false);
      });
  }, [brand]);

  if (loading) {
    return <div className="animate-pulse bg-gray-200 rounded" style={{ width: size, height: size }} />;
  }

  if (!logoUrl) {
    return (
      <div
        className="flex items-center justify-center bg-gray-100 rounded text-gray-500"
        style={{ width: size, height: size }}
      >
        {brand[0].toUpperCase()}
      </div>
    );
  }

  return (
    <Image
      src={logoUrl}
      alt={`${brand} logo`}
      width={size}
      height={size}
      className="object-contain"
    />
  );
}
```

## Scripts

### Fetch All Logos

```typescript
// packages/logos/scripts/fetch-logos.ts
import { getLogoUrl } from "../src/services/logo/fetch";
import { logoBlobService } from "../src/infra/storage/blob";

const BRANDS = [
  "Toyota",
  "Honda",
  "BMW",
  "Mercedes-Benz",
  "Audi",
  "Volkswagen",
  "Nissan",
  "Mazda",
  "Hyundai",
  "Kia",
  "Ford",
  "Chevrolet",
  "Tesla",
  "Porsche",
  "Ferrari",
  "Lamborghini",
  "Lexus",
  "Volvo",
  "Jaguar",
  "Land Rover",
];

async function fetchAllLogos() {
  console.log(`Fetching logos for ${BRANDS.length} brands...\n`);

  for (const brand of BRANDS) {
    try {
      const logoUrl = await getLogoUrl(brand);

      if (logoUrl) {
        console.log(`✓ ${brand}: ${logoUrl}`);

        // Download and upload to Blob
        const response = await fetch(logoUrl);
        const buffer = Buffer.from(await response.arrayBuffer());

        await logoBlobService.upload(brand, buffer);
      } else {
        console.log(`✗ ${brand}: Not found`);
      }
    } catch (error) {
      console.error(`✗ ${brand}: Error -`, error);
    }
  }

  console.log("\n✅ Logo fetch complete!");
}

fetchAllLogos()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("Failed to fetch logos:", error);
    process.exit(1);
  });
```

Add to `package.json`:

```json
{
  "scripts": {
    "fetch-logos": "tsx scripts/fetch-logos.ts",
    "scrape-logos": "tsx scripts/scrape-logos.ts"
  }
}
```

Run scripts:

```bash
# Fetch logos from CDN
pnpm -F @sgcarstrends/logos fetch-logos

# Scrape logos from websites
pnpm -F @sgcarstrends/logos scrape-logos
```

### Scrape and Upload

```typescript
// packages/logos/scripts/scrape-logos.ts
import { scrapeLogos, processScrapedLogos } from "../src/services/logo/scrape";

async function main() {
  console.log("Scraping car logos...\n");

  const logos = await scrapeLogos();

  console.log(`\nFound ${logos.length} logos`);
  console.log("Uploading to Vercel Blob...\n");

  await processScrapedLogos(logos);

  console.log("\n✅ Scraping complete!");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("Failed to scrape logos:", error);
    process.exit(1);
  });
```

## Caching Strategy

### Multi-Layer Caching

```typescript
import { redis } from "@sgcarstrends/utils";
import { LRUCache } from "lru-cache";

// L1 Cache - In-memory
const memoryCache = new LRUCache<string, string>({
  max: 100,
  ttl: 5 * 60 * 1000, // 5 minutes
});

// L2 Cache - Redis
// L3 Cache - Vercel Blob

export async function getCachedLogoUrl(brand: string): Promise<string | null> {
  const normalizedBrand = normalizeBrandName(brand);

  // Check L1 (memory)
  const memCached = memoryCache.get(normalizedBrand);
  if (memCached) {
    console.log("L1 cache hit");
    return memCached;
  }

  // Check L2 (Redis)
  const redisCached = await redis.get<string>(`logo:${normalizedBrand}`);
  if (redisCached) {
    console.log("L2 cache hit");
    memoryCache.set(normalizedBrand, redisCached);
    return redisCached;
  }

  // Check L3 (Blob)
  const blobUrl = await logoBlobService.getUrl(normalizedBrand);
  if (blobUrl) {
    console.log("L3 cache hit");

    // Populate L1 and L2
    memoryCache.set(normalizedBrand, blobUrl);
    await redis.set(`logo:${normalizedBrand}`, blobUrl, { ex: 7 * 24 * 60 * 60 });

    return blobUrl;
  }

  console.log("Cache miss");
  return null;
}
```

## Fallback Strategy

```typescript
export async function getLogoWithFallback(brand: string): Promise<string> {
  const normalizedBrand = normalizeBrandName(brand);

  // Try 1: Get from cache/blob
  let logoUrl = await getCachedLogoUrl(normalizedBrand);

  if (logoUrl) {
    return logoUrl;
  }

  // Try 2: Fetch from CDN
  logoUrl = await getLogoUrl(normalizedBrand);

  if (logoUrl) {
    return logoUrl;
  }

  // Try 3: Scrape from web
  const scrapedLogos = await scrapeLogos();
  const scraped = scrapedLogos.find(l => l.brand === normalizedBrand);

  if (scraped) {
    return scraped.url;
  }

  // Fallback: Return placeholder
  return `/images/logo-placeholder.png`;
}
```

## Testing

```typescript
// packages/logos/src/utils/__tests__/normalize.test.ts
import { describe, it, expect } from "vitest";
import { normalizeBrandName, resolveBrandAlias } from "../normalize";

describe("Brand Name Normalization", () => {
  it("normalizes brand names correctly", () => {
    expect(normalizeBrandName("Mercedes-Benz")).toBe("mercedes-benz");
    expect(normalizeBrandName("BMW")).toBe("bmw");
    expect(normalizeBrandName("Land Rover")).toBe("land-rover");
    expect(normalizeBrandName("Alfa Romeo")).toBe("alfa-romeo");
  });

  it("handles special characters", () => {
    expect(normalizeBrandName("Audi (A4)")).toBe("audi-a4");
    expect(normalizeBrandName("Range Rover")).toBe("range-rover");
  });

  it("resolves aliases", () => {
    expect(resolveBrandAlias("VW")).toBe("volkswagen");
    expect(resolveBrandAlias("Merc")).toBe("mercedes-benz");
    expect(resolveBrandAlias("BMW")).toBe("bmw");
  });
});
```

Run tests:

```bash
pnpm -F @sgcarstrends/logos test
```

## Environment Variables

```env
# Vercel Blob
BLOB_READ_WRITE_TOKEN=vercel_blob_token_here
```

## Performance Optimization

### Batch Upload

```typescript
export async function batchUploadLogos(
  logos: Array<{ brand: string; file: Buffer }>
) {
  const results = await Promise.allSettled(
    logos.map(({ brand, file }) =>
      logoBlobService.upload(brand, file)
    )
  );

  const succeeded = results.filter(r => r.status === "fulfilled").length;
  const failed = results.filter(r => r.status === "rejected").length;

  console.log(`Uploaded: ${succeeded}, Failed: ${failed}`);

  return results;
}
```

### Pre-warming Cache

```typescript
export async function prewarmLogoCache() {
  const commonBrands = ["Toyota", "Honda", "BMW", "Mercedes-Benz"];

  for (const brand of commonBrands) {
    await getCachedLogoUrl(brand);
  }

  console.log("Logo cache prewarmed");
}
```

## References

- Vercel Blob: Use Context7 for latest docs
- Related files:
  - `packages/logos/src/` - Logo package source
  - `packages/logos/scripts/` - Utility scripts
  - Root CLAUDE.md - Project documentation

## Best Practices

1. **Normalize Names**: Always normalize brand names before lookup
2. **Cache Aggressively**: Use multi-layer caching
3. **Fallbacks**: Provide placeholder images for missing logos
4. **Lazy Loading**: Only fetch logos when needed
5. **Batch Operations**: Use batch uploads for multiple logos
6. **Error Handling**: Handle missing logos gracefully
7. **Testing**: Test normalization and caching logic
8. **Monitoring**: Track cache hit rates and missing logos
