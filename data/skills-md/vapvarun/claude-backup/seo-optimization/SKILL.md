---
name: seo-optimization
description: Optimize websites for search engines including on-page SEO, technical SEO, meta tags, schema markup, Core Web Vitals, and keyword optimization. Use when improving search rankings, auditing SEO, or optimizing content for Google.
---

# SEO Optimization Skill

## Instructions

When optimizing for SEO:

### 1. On-Page SEO

**Title Tags:**
- 50-60 characters max
- Primary keyword near the beginning
- Include brand name at end
- Make it compelling and clickable

```html
<title>Primary Keyword - Secondary Keyword | Brand Name</title>
```

**Meta Descriptions:**
- 150-160 characters
- Include primary keyword
- Call-to-action
- Unique for each page

```html
<meta name="description" content="Compelling description with keyword that encourages clicks. Learn more about X today!">
```

**Heading Structure:**
```html
<h1>One H1 per page with primary keyword</h1>
<h2>Section headings with secondary keywords</h2>
<h3>Subsections for organization</h3>
```

### 2. Technical SEO

**Essential Meta Tags:**
```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://example.com/page/">
```

**Open Graph (Social Sharing):**
```html
<meta property="og:title" content="Page Title">
<meta property="og:description" content="Description">
<meta property="og:image" content="https://example.com/image.jpg">
<meta property="og:url" content="https://example.com/page/">
<meta property="og:type" content="website">
```

**Twitter Cards:**
```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Page Title">
<meta name="twitter:description" content="Description">
<meta name="twitter:image" content="https://example.com/image.jpg">
```

### 3. Schema Markup (JSON-LD)

**Organization:**
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Company Name",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+1-xxx-xxx-xxxx",
    "contactType": "customer service"
  },
  "sameAs": [
    "https://facebook.com/company",
    "https://twitter.com/company"
  ]
}
```

**Product:**
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Name",
  "image": "https://example.com/product.jpg",
  "description": "Product description",
  "brand": {"@type": "Brand", "name": "Brand"},
  "offers": {
    "@type": "Offer",
    "price": "49.99",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "reviewCount": "124"
  }
}
```

**Article/Blog Post:**
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title",
  "author": {"@type": "Person", "name": "Author Name"},
  "datePublished": "2025-01-15",
  "dateModified": "2025-01-20",
  "image": "https://example.com/article-image.jpg"
}
```

**FAQ:**
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "Question text?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Answer text."
    }
  }]
}
```

### 4. Core Web Vitals

**LCP (Largest Contentful Paint) < 2.5s:**
- Optimize images (WebP, lazy loading)
- Preload critical assets
- Use CDN

**FID (First Input Delay) < 100ms:**
- Minimize JavaScript
- Break up long tasks
- Use web workers

**CLS (Cumulative Layout Shift) < 0.1:**
- Set image dimensions
- Reserve space for ads/embeds
- Avoid inserting content above existing content

### 5. Image SEO

```html
<img
  src="image.webp"
  alt="Descriptive alt text with keyword"
  width="800"
  height="600"
  loading="lazy"
  decoding="async"
>
```

### 6. URL Structure

**Good:**
- `example.com/category/product-name`
- `example.com/blog/how-to-do-something`

**Avoid:**
- `example.com/p?id=123`
- `example.com/category/sub/sub/page`

### 7. Internal Linking

- Use descriptive anchor text
- Link to related content
- Create topic clusters
- Maintain reasonable link depth (3 clicks max)

### 8. SEO Checklist

- [ ] Unique title tag with keyword
- [ ] Meta description with CTA
- [ ] One H1 with primary keyword
- [ ] Schema markup implemented
- [ ] Images optimized with alt text
- [ ] Internal links added
- [ ] Mobile-friendly
- [ ] Page speed optimized
- [ ] Canonical URL set
- [ ] XML sitemap updated
