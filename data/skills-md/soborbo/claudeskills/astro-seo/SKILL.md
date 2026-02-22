---
name: astro-seo
description: SEO markup patterns for Astro lead generation sites. Meta tags, Open Graph, Schema.org, sitemap, robots. Use for all SEO implementation.
---

# Astro SEO Skill

## Purpose

Handles all SEO markup for Astro projects. Technical SEO patterns.

## Core Rules

1. **Every page needs unique title + description**
2. **Open Graph for social sharing**
3. **Schema.org for rich results**
4. **Canonical URLs always set**
5. **Sitemap auto-generated**

## Required Meta Tags

```astro
---
const { title, description, image, noindex = false } = Astro.props;
const canonicalURL = new URL(Astro.url.pathname, Astro.site);
---

<head>
  <title>{title}</title>
  <meta name="description" content={description} />
  <link rel="canonical" href={canonicalURL} />
  {noindex && <meta name="robots" content="noindex,nofollow" />}

  <!-- Open Graph -->
  <meta property="og:title" content={title} />
  <meta property="og:description" content={description} />
  <meta property="og:url" content={canonicalURL} />
  <meta property="og:image" content={image} />
  <meta property="og:type" content="website" />

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image" />
</head>
```

## Schema.org Patterns

### LocalBusiness (Homepage)

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Business Name",
  "address": { "@type": "PostalAddress", ... },
  "telephone": "+44...",
  "openingHours": "Mo-Fr 08:00-18:00"
}
```

### Service Pages

```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "Service Name",
  "provider": { "@type": "LocalBusiness", ... }
}
```

### FAQ

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [...]
}
```

## Sitemap

```javascript
// astro.config.mjs
import sitemap from '@astrojs/sitemap';

export default {
  site: 'https://yourdomain.com',
  integrations: [sitemap()]
}
```

## Noindex Pages

- Thank you pages
- 404/410 pages
- Admin/preview pages
- Duplicate content

## Related Skills

- `local-seo` — GBP, citations, area pages
- `heading-tree` — H1-H4 structure
- `keyword-research` — Keyword targeting

## Definition of Done

- [ ] Unique title + description per page
- [ ] Open Graph tags set
- [ ] LocalBusiness schema on homepage
- [ ] Service schema on service pages
- [ ] FAQ schema where applicable
- [ ] Sitemap configured
- [ ] Canonical URLs set
- [ ] Thank you pages noindexed
