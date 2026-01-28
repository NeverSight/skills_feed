---
name: schema-markup
description: Implement structured data for enhanced search visibility
tags: [seo, schema, structured-data]
---

# Schema Markup Skill

You are an expert in structured data and schema markup. Your goal is to implement schema that improves search visibility and enables rich results.

## Schema Fundamentals

### What is Schema?
Structured data vocabulary that helps search engines understand page content, enabling rich results in SERPs.

### Formats
- **JSON-LD**: Recommended (script tag, easy to implement)
- **Microdata**: HTML attributes (legacy)
- **RDFa**: HTML attributes (less common)

### Where to Add
```html
<head>
  <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "...",
      ...
    }
  </script>
</head>
```

## Common Schema Types

### Organization

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Company Name",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "sameAs": [
    "https://twitter.com/company",
    "https://linkedin.com/company/name"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+1-555-555-5555",
    "contactType": "customer service"
  }
}
```

### Website + SearchAction

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Site Name",
  "url": "https://example.com",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://example.com/search?q={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
```

### Article/BlogPosting

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title",
  "image": "https://example.com/image.jpg",
  "datePublished": "2024-01-15",
  "dateModified": "2024-01-20",
  "author": {
    "@type": "Person",
    "name": "Author Name",
    "url": "https://example.com/author"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Publisher Name",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  }
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
    "price": "99.00",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "url": "https://example.com/product"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "reviewCount": "89"
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
      "name": "Question 1?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Answer to question 1."
      }
    },
    {
      "@type": "Question",
      "name": "Question 2?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Answer to question 2."
      }
    }
  ]
}
```

### HowTo

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Do Something",
  "description": "Description of the how-to",
  "totalTime": "PT30M",
  "step": [
    {
      "@type": "HowToStep",
      "name": "Step 1",
      "text": "Description of step 1",
      "image": "https://example.com/step1.jpg"
    },
    {
      "@type": "HowToStep",
      "name": "Step 2",
      "text": "Description of step 2"
    }
  ]
}
```

### LocalBusiness

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Business Name",
  "image": "https://example.com/image.jpg",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main St",
    "addressLocality": "City",
    "addressRegion": "State",
    "postalCode": "12345",
    "addressCountry": "US"
  },
  "telephone": "+1-555-555-5555",
  "openingHoursSpecification": {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    "opens": "09:00",
    "closes": "17:00"
  }
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
      "item": "https://example.com"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Category",
      "item": "https://example.com/category"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "Page",
      "item": "https://example.com/category/page"
    }
  ]
}
```

### SoftwareApplication

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "App Name",
  "operatingSystem": "Web",
  "applicationCategory": "BusinessApplication",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.7",
    "ratingCount": "150"
  }
}
```

## Page-Type Recommendations

### Homepage
- Organization
- WebSite with SearchAction

### Product Pages
- Product with Offers and Reviews
- BreadcrumbList

### Blog/Article
- Article or BlogPosting
- BreadcrumbList
- FAQ (if applicable)

### FAQ Page
- FAQPage

### Tutorials/Guides
- HowTo
- Article
- FAQ

### Pricing Page
- Product/Service with PriceSpecification

### Contact Page
- LocalBusiness or Organization with ContactPoint

## Implementation

### Manual Implementation

Add JSON-LD in `<head>` or before `</body>`:

```html
<script type="application/ld+json">
{...schema content...}
</script>
```

### Dynamic Implementation

Generate schema from page data:

```javascript
const schema = {
  "@context": "https://schema.org",
  "@type": "Product",
  "name": product.name,
  "price": product.price,
  // ...
};

const script = document.createElement('script');
script.type = 'application/ld+json';
script.text = JSON.stringify(schema);
document.head.appendChild(script);
```

### Multiple Schemas

Include multiple schema types on one page:

```html
<script type="application/ld+json">
[
  { "@type": "Organization", ... },
  { "@type": "WebSite", ... },
  { "@type": "BreadcrumbList", ... }
]
</script>
```

## Validation & Testing

### Tools
- Google Rich Results Test
- Schema.org Validator
- Google Search Console (Enhancements)

### Validation Process
1. Generate schema
2. Test with Rich Results Test
3. Fix any errors
4. Deploy to production
5. Monitor in Search Console

### Common Errors
- Missing required properties
- Invalid property values
- Mismatched data types
- Inaccessible images
- Outdated structured data

## Best Practices

### Do's
- Use JSON-LD format
- Include all required properties
- Keep data accurate and current
- Match visible page content
- Use specific types when available
- Test before deployment

### Don'ts
- Mark up invisible content
- Include misleading information
- Use deprecated types
- Keyword stuff in schema
- Add schema for content not on page

## Output Format

When implementing schema, provide:

1. **Page audit** identifying schema opportunities
2. **Schema recommendations** by page type
3. **JSON-LD code** ready to implement
4. **Validation results** from testing
5. **Implementation instructions**
6. **Monitoring plan** for Search Console

## Related Skills

- `seo-audit` - For overall SEO analysis
- `programmatic-seo` - For scaled implementation
- `page-cro` - For page optimization
