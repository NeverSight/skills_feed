---
name: seo-mastery
description: Comprehensive SEO optimization skill based on Google's official guidelines. Covers technical SEO, content SEO, structured data, Core Web Vitals, E-E-A-T strategies, practical code generation, and site audit workflows.
version: 1.0.0
author: pani
---

# SEO Mastery Agent Skills

Comprehensive SEO optimization skill based on Google's official documentation. Provides integrated support for technical SEO, content optimization, structured data, Core Web Vitals, and site audits.

## When to Use This Skill

### Technical SEO
- Debugging crawl and indexing issues
- Configuring robots.txt / sitemap.xml
- Implementing canonical URLs / hreflang
- JavaScript SEO optimization
- Mobile-first optimization
- Server-side rendering (SSR) setup

### Content SEO
- Meta tag optimization (title, description)
- Heading structure design (H1-H6)
- E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) strategies
- Search intent-aligned content design
- Internal linking strategy

### Structured Data
- JSON-LD schema.org implementation
- Rich results support (FAQ, How-to, Article, Product, etc.)
- VideoObject, BroadcastEvent implementation
- BreadcrumbList configuration
- LocalBusiness / Organization setup

### Core Web Vitals
- LCP (Largest Contentful Paint) optimization
- INP (Interaction to Next Paint) improvement
- CLS (Cumulative Layout Shift) fixes
- Performance monitoring and improvement

### Site Audit
- Comprehensive SEO audit workflow
- Automated checklist generation
- Issue prioritization
- Improvement report creation

## Quick Start

### Basic Usage

```
# Request meta tag optimization
"Optimize the meta tags for this page"

# Generate structured data
"Add Article structured data to this blog post"

# Run site audit
"Perform an SEO audit on this site"

# Improve Core Web Vitals
"How can I improve LCP?"
```

---

## Technical SEO Checklist

### Crawl Optimization
- [ ] robots.txt is properly configured
- [ ] XML sitemap exists and is submitted to Search Console
- [ ] Important pages are not set to noindex
- [ ] Crawl budget is not wasted
- [ ] No 404/5xx errors

### Index Optimization
- [ ] Canonical URLs are correctly set
- [ ] Duplicate content is properly handled
- [ ] hreflang (for multilingual sites) is correct
- [ ] Mobile and desktop versions have the same content

### Rendering Optimization
- [ ] JavaScript is properly rendered
- [ ] Critical content is included in HTML
- [ ] Lazy loading is properly implemented

---

## Structured Data Templates

### Article

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article title (max 110 characters recommended)",
  "description": "Article description",
  "image": [
    "https://example.com/photos/1x1/photo.jpg",
    "https://example.com/photos/4x3/photo.jpg",
    "https://example.com/photos/16x9/photo.jpg"
  ],
  "datePublished": "2025-01-01T08:00:00+00:00",
  "dateModified": "2025-01-15T10:30:00+00:00",
  "author": {
    "@type": "Person",
    "name": "Author Name",
    "url": "https://example.com/author/profile"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Site Name",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  }
}
```

### FAQ

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Question 1 text",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Answer 1 text"
      }
    },
    {
      "@type": "Question",
      "name": "Question 2 text",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Answer 2 text"
      }
    }
  ]
}
```

### BreadcrumbList

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://example.com/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Category",
      "item": "https://example.com/category/"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "Current Page"
    }
  ]
}
```

### Product

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Name",
  "image": "https://example.com/product.jpg",
  "description": "Product description",
  "brand": {
    "@type": "Brand",
    "name": "Brand Name"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/product",
    "priceCurrency": "USD",
    "price": "99.00",
    "availability": "https://schema.org/InStock",
    "seller": {
      "@type": "Organization",
      "name": "Seller Name"
    }
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "reviewCount": "128"
  }
}
```

### LocalBusiness

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Business Name",
  "image": "https://example.com/store.jpg",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main Street",
    "addressLocality": "New York",
    "addressRegion": "NY",
    "postalCode": "10001",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 40.7128,
    "longitude": -74.0060
  },
  "telephone": "+1-212-555-1234",
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "09:00",
      "closes": "18:00"
    }
  ],
  "priceRange": "$$"
}
```

### VideoObject

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "Video Title",
  "description": "Video description",
  "thumbnailUrl": [
    "https://example.com/thumb-1x1.jpg",
    "https://example.com/thumb-4x3.jpg",
    "https://example.com/thumb-16x9.jpg"
  ],
  "uploadDate": "2025-01-01T08:00:00+00:00",
  "duration": "PT5M30S",
  "contentUrl": "https://example.com/video.mp4",
  "embedUrl": "https://example.com/embed/video123",
  "interactionStatistic": {
    "@type": "InteractionCounter",
    "interactionType": { "@type": "WatchAction" },
    "userInteractionCount": 12345
  },
  "hasPart": [
    {
      "@type": "Clip",
      "name": "Introduction",
      "startOffset": 0,
      "endOffset": 30,
      "url": "https://example.com/video?t=0"
    },
    {
      "@type": "Clip",
      "name": "Main Content",
      "startOffset": 30,
      "endOffset": 300,
      "url": "https://example.com/video?t=30"
    }
  ]
}
```

---

## Core Web Vitals Optimization Guide

### LCP (Largest Contentful Paint) - Target: Under 2.5 seconds

**Common Causes and Solutions:**

| Cause | Solution |
|-------|----------|
| Slow server response | CDN implementation, cache optimization, server upgrades |
| Render-blocking resources | Defer CSS/JS loading, inline Critical CSS |
| Slow image loading | Use WebP/AVIF, specify proper sizes, preload settings |
| Client-side rendering | Implement SSR/SSG, pre-render critical content |

**Example: Image Preloading**
```html
<link rel="preload" as="image" href="hero-image.webp" fetchpriority="high">
```

### INP (Interaction to Next Paint) - Target: Under 200ms

**Common Causes and Solutions:**

| Cause | Solution |
|-------|----------|
| Heavy JavaScript | Code splitting, remove unnecessary JS, defer execution |
| Long tasks | Split tasks (yield to main thread) |
| Large DOM size | Reduce DOM elements, implement virtual scrolling |
| Third-party scripts | Lazy load, review necessity |

**Example: Splitting Long Tasks**
```javascript
async function processLargeArray(items) {
  for (const item of items) {
    processItem(item);
    // Yield to main thread
    await new Promise(resolve => setTimeout(resolve, 0));
  }
}
```

### CLS (Cumulative Layout Shift) - Target: Under 0.1

**Common Causes and Solutions:**

| Cause | Solution |
|-------|----------|
| Images/videos without dimensions | Specify width/height attributes, use aspect-ratio CSS |
| Dynamically inserted content | Reserve space in advance, use skeleton UI |
| Web fonts (FOUT/FOIT) | font-display: swap, preload fonts |
| Ads/embeds | Pre-position fixed-size containers |

**Example: Image Aspect Ratio**
```html
<img src="image.jpg" width="800" height="600" alt="Description"
     style="aspect-ratio: 4/3; width: 100%; height: auto;">
```

---

## E-E-A-T Optimization Checklist

### Experience
- [ ] Provide content based on first-hand experience
- [ ] Include actual product usage reviews/photos
- [ ] Present case studies and examples

### Expertise
- [ ] Author information page exists
- [ ] Author credentials/background are stated
- [ ] Content focuses on specialized field
- [ ] Provide accurate and up-to-date information

### Authoritativeness
- [ ] Backlinks from trusted external sites
- [ ] Citations from industry bodies/experts
- [ ] Brand mentions earned
- [ ] Expert review/supervision

### Trustworthiness
- [ ] HTTPS enabled
- [ ] Privacy policy exists
- [ ] Contact information is clear
- [ ] Company information/location is stated
- [ ] User reviews/ratings are displayed
- [ ] Sources are cited

---

## Site Audit Workflow

### Phase 1: Crawl Diagnosis

```bash
# Check robots.txt
curl -s https://example.com/robots.txt

# Check sitemap
curl -s https://example.com/sitemap.xml | head -50

# Index status (site: search)
# Search "site:example.com" on Google
```

**Check Items:**
1. Are important pages blocked by robots.txt?
2. Does sitemap.xml exist and include main pages?
3. Does index count match expectations?

### Phase 2: Page-Level Diagnosis

**HTML Head Elements:**
```bash
# Extract meta information
curl -s https://example.com/ | grep -E '<title>|<meta name="description"|<link rel="canonical"'
```

**Check Items:**
1. Title tag (under 60 characters, includes keywords)
2. Meta description (under 160 characters)
3. Canonical URL
4. OGP / Twitter Card tags
5. Structured data presence

### Phase 3: Performance Diagnosis

**Lighthouse CLI:**
```bash
npx lighthouse https://example.com --output=json --output-path=./report.json
```

**Check Items:**
1. Core Web Vitals scores
2. Accessibility score
3. SEO score
4. Performance improvement suggestions

### Phase 4: Competitive Analysis

1. Content volume/structure of top-ranking sites
2. Backlink profiles
3. Structured data usage
4. Page speed comparison

### Phase 5: Improvement Priority Matrix

| Priority | Impact | Difficulty | Examples |
|----------|--------|------------|----------|
| Critical | High | Low | Remove noindex, fix 404s |
| High | High | Medium | Add structured data, optimize meta tags |
| Medium | Medium | Medium | Core Web Vitals improvements |
| Low | Low | High | Major site structure changes |

---

## Related Reference Files

This skill includes the following detailed documents:

| File | Content | Use Case |
|------|---------|----------|
| [technical-seo.md](technical-seo.md) | robots.txt, sitemap, canonical, hreflang, etc. | Technical SEO configuration |
| [content-seo.md](content-seo.md) | Meta tags, heading structure, content design | Content optimization |
| [structured-data.md](structured-data.md) | All structured data type details | Rich results implementation |
| [core-web-vitals.md](core-web-vitals.md) | Detailed LCP/INP/CLS optimization | Performance improvement |
| [audit-workflow.md](audit-workflow.md) | Audit procedures, tools, report formats | Site audit execution |

---

## Recommended Tools

### Google Official
- [Google Search Console](https://search.google.com/search-console) - Index status & search performance
- [PageSpeed Insights](https://pagespeed.web.dev/) - Core Web Vitals measurement
- [Rich Results Test](https://search.google.com/test/rich-results) - Structured data validation
- [Mobile-Friendly Test](https://search.google.com/test/mobile-friendly) - Mobile compatibility check

### CLI/Development Tools
- Lighthouse CLI - Performance auditing
- Screaming Frog - Large-scale site crawling
- ahrefs / SEMrush - Competitive & backlink analysis

---

## Common Mistakes and Solutions

### 1. Keyword Stuffing
- Avoid: "SEO SEO SEO optimization SEO tools SEO company"
- Better: Use keywords naturally in context

### 2. Duplicate Content
- Avoid: www vs non-www, http vs https as separate URLs
- Better: Canonical settings, 301 redirects

### 3. Slow Image Loading
- Avoid: Large PNG/JPG files used as-is
- Better: WebP conversion, proper sizing, lazy loading

### 4. Structured Data Errors
- Avoid: Missing required fields, invalid formats
- Better: Pre-validate with Rich Results Test

### 5. Not Mobile-Friendly
- Avoid: Desktop-only, no touch support
- Better: Responsive design, adequate tap targets

---

## Official Resources

- [Google Search Central](https://developers.google.com/search)
- [SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
- [Search Essentials](https://developers.google.com/search/docs/essentials)
- [Structured Data Documentation](https://developers.google.com/search/docs/appearance/structured-data)
- [Core Web Vitals](https://web.dev/vitals/)

---

## Changelog

- **v1.0.0** (2025-01) - Initial release
  - Created based on Google's official SEO guides
  - Comprehensive technical SEO, content SEO, structured data coverage
  - Core Web Vitals (2024 INP-compliant version)
  - E-E-A-T optimization checklist added
  - Site audit workflow added
