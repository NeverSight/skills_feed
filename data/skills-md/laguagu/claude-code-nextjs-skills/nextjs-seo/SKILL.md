---
name: nextjs-seo
description: Next.js SEO optimization guide. Use when building Next.js apps, optimizing for search engines, fixing Google indexing issues, implementing metadata, sitemaps, robots.txt, JSON-LD, or auditing SEO.
---

# Next.js SEO Optimization

Comprehensive SEO guide for Next.js 16+ applications using App Router.

> **Version:** Updated for Next.js 16.1.3 (January 2026)

## Quick SEO Audit

Run this checklist for any Next.js project:

1. **Check robots.txt**: `curl https://your-site.com/robots.txt`
2. **Check sitemap**: `curl https://your-site.com/sitemap.xml`
3. **Check metadata**: View page source, search for `<title>` and `<meta name="description">`
4. **Check JSON-LD**: View page source, search for `application/ld+json`
5. **Check Core Web Vitals**: Run Lighthouse in Chrome DevTools

## Essential Files

### app/layout.tsx - Root Metadata

```typescript
import type { Metadata, Viewport } from 'next';

// Viewport (separate export required in Next.js 14+)
export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
  userScalable: true,
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#ffffff' },
    { media: '(prefers-color-scheme: dark)', color: '#0a0a0a' },
  ],
};

export const metadata: Metadata = {
  metadataBase: new URL('https://your-site.com'),
  title: {
    default: 'Site Title - Main Keyword',
    template: '%s | Site Name',
  },
  description: 'Compelling description with keywords (150-160 chars)',
  keywords: ['keyword1', 'keyword2', 'keyword3'],
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://your-site.com',
    siteName: 'Site Name',
    title: 'Site Title',
    description: 'Description for social sharing',
    images: [{ url: '/og-image.png', width: 1200, height: 630, alt: 'Site preview' }],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Site Title',
    description: 'Description for Twitter',
    images: ['/og-image.png'],
  },
  alternates: {
    canonical: '/',
  },
  robots: {
    index: true,
    follow: true,
  },
};
```

### app/sitemap.ts - Dynamic Sitemap

```typescript
import type { MetadataRoute } from 'next';

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = 'https://your-site.com';

  return [
    {
      url: baseUrl,
      lastModified: new Date(),
      changeFrequency: 'weekly',
      priority: 1,
      images: [`${baseUrl}/og-image.png`], // Next.js 16 Image Sitemap
    },
    {
      url: `${baseUrl}/about`,
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.8,
    },
  ];
}
```

### app/robots.ts - Robots Configuration

```typescript
import type { MetadataRoute } from 'next';

export default function robots(): MetadataRoute.Robots {
  const baseUrl = 'https://your-site.com';

  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: ['/api/', '/_next/', '/admin/'],
      },
    ],
    sitemap: `${baseUrl}/sitemap.xml`,
    host: baseUrl,
  };
}
```

## Key Principles

### Rendering Strategy for SEO

| Strategy | Use When | SEO Impact |
|----------|----------|------------|
| SSG (Static) | Content rarely changes | Best - pre-rendered HTML |
| SSR | Dynamic content per request | Great - server-rendered |
| ISR | Large sites, periodic updates | Great - cached + fresh |
| CSR | Dashboards, authenticated areas | Poor - avoid for SEO pages |

### Core Web Vitals Targets

| Metric | Target | Impact |
|--------|--------|--------|
| LCP (Largest Contentful Paint) | < 2.5s | Loading speed |
| INP (Interaction to Next Paint) | < 200ms | Interactivity |
| CLS (Cumulative Layout Shift) | < 0.1 | Visual stability |

## References

- **Metadata API**: See [references/metadata-api.md](references/metadata-api.md)
- **Sitemap & Robots**: See [references/sitemap-robots.md](references/sitemap-robots.md)
- **JSON-LD Structured Data**: See [references/json-ld.md](references/json-ld.md)
- **SEO Audit Checklist**: See [references/checklist.md](references/checklist.md)
- **Troubleshooting**: See [references/troubleshooting.md](references/troubleshooting.md)

## Common Mistakes to Avoid

1. **Mixing next-seo with Metadata API** - Use only Metadata API in App Router
2. **Missing canonical URLs** - Always set `alternates.canonical`
3. **Using CSR for SEO pages** - Use SSG/SSR for indexable content
4. **Blocking assets in robots.txt** - Don't block CSS/JS needed for rendering
5. **Missing metadataBase** - Required for relative URLs in metadata
6. **Viewport in metadata** - Must be separate export in Next.js 14+
7. **Mixing metadata object and generateMetadata** - Use one or the other, not both

## Quick Fixes

### Add noindex to a page

```typescript
export const metadata: Metadata = {
  robots: {
    index: false,
    follow: false,
  },
};
```

### Dynamic metadata per page

```typescript
export async function generateMetadata({ params }): Promise<Metadata> {
  const product = await getProduct(params.id);
  return {
    title: product.name,
    description: product.description,
  };
}
```

### Canonical for dynamic routes

```typescript
export async function generateMetadata({ params }): Promise<Metadata> {
  return {
    alternates: {
      canonical: `/products/${params.slug}`,
    },
  };
}
```
