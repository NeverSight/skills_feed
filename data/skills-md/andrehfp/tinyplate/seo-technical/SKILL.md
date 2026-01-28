---
name: seo-technical
description: Implement technical SEO infrastructure for Next.js apps. Use this skill when setting up sitemaps, robots.txt, meta tags, OpenGraph, structured data (JSON-LD), canonical URLs, and other technical SEO elements. Covers Next.js 15/16 App Router patterns and 2025 best practices.
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, WebSearch
---

# Technical SEO Implementation (Next.js 2025)

## Skill Files

This skill includes multiple reference files:
- **SKILL.md** (this file): Core technical SEO implementation guide
- **nextjs-implementation.md**: Next.js-specific code templates and patterns
- **checklist.md**: Pre-launch technical SEO checklist
- **structured-data.md**: JSON-LD schema markup templates

## What This Skill Covers

1. **Sitemaps** → `app/sitemap.ts` for dynamic sitemap generation
2. **Robots.txt** → `app/robots.ts` for crawler directives
3. **Meta Tags** → OpenGraph, Twitter Cards, keywords, descriptions
4. **Structured Data** → JSON-LD for rich snippets
5. **Canonical URLs** → Prevent duplicate content issues
6. **Performance SEO** → Core Web Vitals considerations

---

# Part 1: Sitemap Implementation

## Next.js App Router Sitemap (app/sitemap.ts)

Next.js automatically serves `/sitemap.xml` when you create `app/sitemap.ts`:

```typescript
import type { MetadataRoute } from "next";

const BASE_URL = process.env.NEXT_PUBLIC_SITE_URL || "https://example.com";

export default function sitemap(): MetadataRoute.Sitemap {
  const currentDate = new Date().toISOString();

  // Static pages
  const staticPages: MetadataRoute.Sitemap = [
    {
      url: BASE_URL,
      lastModified: currentDate,
      changeFrequency: "weekly",
      priority: 1.0,
    },
    {
      url: `${BASE_URL}/pricing`,
      lastModified: currentDate,
      changeFrequency: "monthly",
      priority: 0.8,
    },
    {
      url: `${BASE_URL}/about`,
      lastModified: currentDate,
      changeFrequency: "monthly",
      priority: 0.7,
    },
    {
      url: `${BASE_URL}/privacy`,
      lastModified: currentDate,
      changeFrequency: "yearly",
      priority: 0.3,
    },
    {
      url: `${BASE_URL}/terms`,
      lastModified: currentDate,
      changeFrequency: "yearly",
      priority: 0.3,
    },
  ];

  return staticPages;
}
```

### Dynamic Sitemap with Database Content

```typescript
import type { MetadataRoute } from "next";
import { db } from "@/lib/db";
import { blogPosts, products } from "@/lib/db/schema";

const BASE_URL = process.env.NEXT_PUBLIC_SITE_URL || "https://example.com";

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  // Fetch dynamic content
  const posts = await db.select().from(blogPosts).where(eq(blogPosts.published, true));
  const allProducts = await db.select().from(products);

  const staticPages: MetadataRoute.Sitemap = [
    { url: BASE_URL, lastModified: new Date(), changeFrequency: "weekly", priority: 1.0 },
  ];

  const blogPages: MetadataRoute.Sitemap = posts.map((post) => ({
    url: `${BASE_URL}/blog/${post.slug}`,
    lastModified: post.updatedAt || post.createdAt,
    changeFrequency: "weekly" as const,
    priority: 0.7,
  }));

  const productPages: MetadataRoute.Sitemap = allProducts.map((product) => ({
    url: `${BASE_URL}/products/${product.slug}`,
    lastModified: product.updatedAt,
    changeFrequency: "daily" as const,
    priority: 0.8,
  }));

  return [...staticPages, ...blogPages, ...productPages];
}
```

### Large Sitemaps (50,000+ URLs)

Use `generateSitemaps()` for sitemap index:

```typescript
import type { MetadataRoute } from "next";

const URLS_PER_SITEMAP = 50000;

export async function generateSitemaps() {
  const totalProducts = await getProductCount();
  const sitemapCount = Math.ceil(totalProducts / URLS_PER_SITEMAP);

  return Array.from({ length: sitemapCount }, (_, i) => ({ id: i }));
}

export default async function sitemap({ id }: { id: number }): Promise<MetadataRoute.Sitemap> {
  const start = id * URLS_PER_SITEMAP;
  const products = await getProducts({ start, limit: URLS_PER_SITEMAP });

  return products.map((product) => ({
    url: `${BASE_URL}/products/${product.slug}`,
    lastModified: product.updatedAt,
  }));
}
```

### Sitemap Best Practices

| Practice | Why |
|----------|-----|
| Keep `lastModified` accurate | Google uses it when consistently accurate |
| Only include canonical URLs | Duplicates waste crawl budget |
| Priority: 1.0 homepage, 0.8-0.9 key pages, 0.6-0.7 others | Guides crawler importance |
| `changeFrequency` is ignored by Google | Include for other search engines |
| Max 50,000 URLs per sitemap | Use sitemap index for more |

---

# Part 2: Robots.txt Implementation

## Next.js App Router Robots (app/robots.ts)

```typescript
import type { MetadataRoute } from "next";

const BASE_URL = process.env.NEXT_PUBLIC_SITE_URL || "https://example.com";

export default function robots(): MetadataRoute.Robots {
  const isProduction = process.env.NODE_ENV === "production";

  // Block everything in non-production
  if (!isProduction) {
    return {
      rules: { userAgent: "*", disallow: "/" },
    };
  }

  return {
    rules: [
      {
        userAgent: "*",
        allow: "/",
        disallow: [
          "/api/",
          "/dashboard/",
          "/admin/",
          "/private/",
          "/_next/",
          "/sign-in/",
          "/sign-up/",
        ],
      },
      // Block AI training bots (optional)
      { userAgent: "GPTBot", disallow: "/" },
      { userAgent: "ChatGPT-User", disallow: "/" },
      { userAgent: "CCBot", disallow: "/" },
      { userAgent: "anthropic-ai", disallow: "/" },
      { userAgent: "Google-Extended", disallow: "/" },
    ],
    sitemap: `${BASE_URL}/sitemap.xml`,
  };
}
```

### Robots.txt Rules

| Directive | Usage |
|-----------|-------|
| `User-agent: *` | Applies to all crawlers |
| `Allow: /` | Allow crawling of path |
| `Disallow: /private/` | Block crawling of path |
| `Sitemap:` | Advertise sitemap location |
| `Crawl-delay:` | Slow down crawling (not respected by Google) |

### Common AI Bots to Block/Allow

```typescript
// Block AI training (keeps content out of training data)
{ userAgent: "GPTBot", disallow: "/" },           // OpenAI
{ userAgent: "ChatGPT-User", disallow: "/" },     // ChatGPT browsing
{ userAgent: "CCBot", disallow: "/" },            // Common Crawl
{ userAgent: "anthropic-ai", disallow: "/" },     // Anthropic
{ userAgent: "Google-Extended", disallow: "/" },  // Google AI training
{ userAgent: "Bytespider", disallow: "/" },       // ByteDance

// Allow AI search (keeps content in AI search results)
// Comment out the above to allow AI indexing
```

### What NOT to Block

- Don't block `/sitemap.xml`
- Don't block CSS/JS files (`/_next/static/`)
- Don't block images you want indexed
- Don't block your homepage

---

# Part 3: Metadata Implementation

## Root Layout Metadata (app/layout.tsx)

```typescript
import type { Metadata, Viewport } from "next";

const BASE_URL = process.env.NEXT_PUBLIC_SITE_URL || "https://example.com";

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  themeColor: "#6366f1",
};

export const metadata: Metadata = {
  metadataBase: new URL(BASE_URL),

  // Title template for child pages
  title: {
    default: "Brand Name — Tagline",
    template: "%s | Brand Name",
  },

  // Description (150-160 chars ideal)
  description: "Your compelling meta description that includes primary keywords and encourages clicks.",

  // Keywords (less important now, but include)
  keywords: ["primary keyword", "secondary keyword", "brand name"],

  // Author info
  authors: [{ name: "Brand Name" }],
  creator: "Brand Name",
  publisher: "Brand Name",

  // Robots directives
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },

  // OpenGraph (Facebook, LinkedIn, etc.)
  openGraph: {
    type: "website",
    locale: "en_US",
    url: BASE_URL,
    siteName: "Brand Name",
    title: "Brand Name — Tagline",
    description: "Your compelling description for social sharing.",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Brand Name - Description",
      },
    ],
  },

  // Twitter Card
  twitter: {
    card: "summary_large_image",
    title: "Brand Name — Tagline",
    description: "Your compelling description for Twitter.",
    images: ["/og-image.png"],
    creator: "@twitterhandle",
    site: "@twitterhandle",
  },

  // Canonical URL
  alternates: {
    canonical: BASE_URL,
  },

  // App categorization
  category: "Technology",

  // Verification codes
  verification: {
    google: "google-site-verification-code",
    // yandex: "yandex-verification-code",
    // bing: "bing-verification-code",
  },
};
```

## Page-Level Metadata

```typescript
// app/pricing/page.tsx
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Pricing", // Becomes "Pricing | Brand Name" via template
  description: "Simple, transparent pricing. Start free, upgrade when you need more.",
  openGraph: {
    title: "Pricing | Brand Name",
    description: "Simple, transparent pricing. Start free, upgrade when you need more.",
  },
};

export default function PricingPage() {
  // ...
}
```

## Dynamic Metadata (generateMetadata)

```typescript
// app/blog/[slug]/page.tsx
import type { Metadata } from "next";

type Props = {
  params: Promise<{ slug: string }>;
};

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const post = await getPostBySlug(slug);

  if (!post) {
    return { title: "Post Not Found" };
  }

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      type: "article",
      publishedTime: post.publishedAt,
      modifiedTime: post.updatedAt,
      authors: [post.author.name],
      images: [
        {
          url: post.coverImage,
          width: 1200,
          height: 630,
          alt: post.title,
        },
      ],
    },
    twitter: {
      card: "summary_large_image",
      title: post.title,
      description: post.excerpt,
      images: [post.coverImage],
    },
    alternates: {
      canonical: `${BASE_URL}/blog/${slug}`,
    },
  };
}
```

---

# Part 4: Authentication Middleware Integration

When using auth (Clerk, NextAuth, etc.), add SEO routes to public matchers:

## Clerk (proxy.ts or middleware.ts)

```typescript
import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";

const isPublicRoute = createRouteMatcher([
  "/",
  "/sign-in(.*)",
  "/sign-up(.*)",
  "/pricing",
  "/about",
  "/blog(.*)",
  "/terms",
  "/privacy",
  // SEO files - IMPORTANT!
  "/robots.txt",
  "/sitemap.xml",
  "/sitemap(.*).xml",
  // Icons
  "/icon(.*)",
  "/apple-icon(.*)",
  "/favicon.ico",
]);

export const proxy = clerkMiddleware(async (auth, request) => {
  if (!isPublicRoute(request)) {
    await auth.protect();
  }
});

export const config = {
  matcher: [
    "/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)",
    "/(api|trpc)(.*)",
  ],
};
```

## NextAuth

```typescript
export { auth as middleware } from "@/auth";

export const config = {
  matcher: [
    // Exclude SEO files from auth
    "/((?!api|_next/static|_next/image|favicon.ico|robots.txt|sitemap.xml|sitemap.*\\.xml).*)",
  ],
};
```

---

# Part 5: Environment Variables

Required environment variables for SEO:

```bash
# .env.local (development)
NEXT_PUBLIC_SITE_URL=http://localhost:3000

# .env.production (production)
NEXT_PUBLIC_SITE_URL=https://yourdomain.com
```

---

# Quick Reference: File Locations

| File | Location | Purpose |
|------|----------|---------|
| Sitemap | `app/sitemap.ts` | Generates `/sitemap.xml` |
| Robots | `app/robots.ts` | Generates `/robots.txt` |
| Root Metadata | `app/layout.tsx` | Default meta tags |
| Page Metadata | `app/[route]/page.tsx` | Page-specific meta |
| OG Image | `public/og-image.png` | Social sharing image (1200x630) |
| Favicon | `app/icon.tsx` or `public/favicon.ico` | Browser tab icon |
| Apple Icon | `app/apple-icon.tsx` or `public/apple-icon.png` | iOS icon |

---

# Implementation Checklist

Before implementing, verify:

1. [ ] `NEXT_PUBLIC_SITE_URL` environment variable is set
2. [ ] Auth middleware allows `/robots.txt` and `/sitemap.xml`
3. [ ] OG image exists at `public/og-image.png` (1200x630px)
4. [ ] All public pages have unique titles and descriptions
5. [ ] Canonical URLs point to preferred versions

After implementing, verify:

1. [ ] Visit `/robots.txt` - should show rules
2. [ ] Visit `/sitemap.xml` - should show URLs
3. [ ] Test with [Google Rich Results Test](https://search.google.com/test/rich-results)
4. [ ] Test with [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)
5. [ ] Submit sitemap to Google Search Console
