---
name: schema-generator
description: Generate structured data and schema markup for content. Triggers on "schema", "structured data", "JSON-LD", "markup", "rich snippets", "generate schema".
---

# Schema Generator Skill

When generating schema markup:

## Schema Type Selection

| Content Type | Primary Schema | Additional Types |
|--------------|---------------|------------------|
| SaaS Product | SoftwareApplication | Offer, AggregateRating |
| Physical Product | Product | Offer, Brand, Review |
| Service | Service | Provider, AreaServed |
| Article | Article | Author, Organization |
| How-To | HowTo | Step, Tool |
| FAQ | FAQPage | Question, Answer |
| About Page | Organization | ContactPoint, Address |
| Person/Team | Person | Organization |
| Event | Event | Location, Offer |
| Course | Course | Organization |

## Output Format

```
┌─────────────────────────────────────────────────────────────┐
│  🏗️ SCHEMA MARKUP GENERATED                                 │
├─────────────────────────────────────────────────────────────┤
│  Type: [Schema Type]                                        │
│  Validation: ✓ Valid JSON-LD                                │
└─────────────────────────────────────────────────────────────┘

## JSON-LD (copy to <head>)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Product Name",
  "description": "GEO-optimized description",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "Web",
  "offers": {
    "@type": "Offer",
    "price": "99",
    "priceCurrency": "USD"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "[FILL: rating]",
    "reviewCount": "[FILL: review count]"
  }
}
</script>
```

## Implementation Checklist

- [ ] Add JSON-LD to page `<head>` section
- [ ] Fill in `[FILL: ...]` placeholders with real data
- [ ] Test with Google Rich Results Test
- [ ] Verify in Google Search Console
```

## Common Templates

### SaaS/Software
```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "",
  "description": "",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "Web",
  "offers": {
    "@type": "Offer",
    "price": "",
    "priceCurrency": "USD",
    "priceValidUntil": ""
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "",
    "reviewCount": ""
  },
  "author": {
    "@type": "Organization",
    "name": ""
  }
}
```

### B2B Service
```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "",
  "description": "",
  "serviceType": "",
  "provider": {
    "@type": "Organization",
    "name": "",
    "url": ""
  },
  "areaServed": {
    "@type": "Country",
    "name": ""
  },
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Services",
    "itemListElement": []
  }
}
```

### FAQ Page
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Question text?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Answer text."
      }
    }
  ]
}
```

## Rules
- Always output valid JSON-LD
- Mark fields needing human input as `[FILL: description]`
- Include implementation instructions
- Suggest additional schema types when relevant
