---
name: schema-markup
description: Generate Schema.org structured data (JSON-LD) for any page type. Use when the user says "schema markup", "structured data", "JSON-LD", "rich snippets", "rich results", "FAQ schema", "product schema", "article schema", "breadcrumb schema", "organization schema", "how-to schema", "review schema", or asks about structured data for SEO.
---

# Schema Markup Generator Skill

You are an expert in Schema.org structured data and Google's rich results requirements. Generate valid, complete JSON-LD markup that maximizes eligibility for Google rich results.

## Supported Schema Types

This skill supports the following schema types. When the user asks for schema, determine which type(s) are appropriate based on the page content.

### 1. Article / BlogPosting / NewsArticle

**Use for:** Blog posts, news articles, editorial content
**Rich result:** Article carousel, headline in search

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Your Article Title (max 110 characters)",
  "description": "Brief description of the article (max 160 characters)",
  "image": [
    "https://example.com/image-16x9.jpg",
    "https://example.com/image-4x3.jpg",
    "https://example.com/image-1x1.jpg"
  ],
  "datePublished": "2025-01-15T08:00:00+00:00",
  "dateModified": "2025-01-20T10:30:00+00:00",
  "author": [{
    "@type": "Person",
    "name": "Author Name",
    "url": "https://example.com/author/name",
    "jobTitle": "Senior Editor",
    "sameAs": [
      "https://twitter.com/authorhandle",
      "https://linkedin.com/in/authorname"
    ]
  }],
  "publisher": {
    "@type": "Organization",
    "name": "Publisher Name",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png",
      "width": 600,
      "height": 60
    }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://example.com/article-url"
  },
  "wordCount": 2500,
  "articleSection": "Technology",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "isAccessibleForFree": true
}
```

**Google requirements:**
- `headline` is required (max 110 characters)
- `image` is required (provide 3 aspect ratios: 16:9, 4:3, 1:1; each > 696px wide)
- `datePublished` is required (ISO 8601 format)
- `author.name` is required
- For `NewsArticle`, also add `dateline` if applicable
- For `BlogPosting`, `@type` changes to `"BlogPosting"`

---

### 2. Product

**Use for:** Product pages, e-commerce listings
**Rich result:** Product snippet with price, availability, reviews

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Name",
  "description": "Product description",
  "image": [
    "https://example.com/product-1.jpg",
    "https://example.com/product-2.jpg"
  ],
  "sku": "SKU-12345",
  "mpn": "MPN-67890",
  "gtin13": "0123456789012",
  "brand": {
    "@type": "Brand",
    "name": "Brand Name"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/product",
    "priceCurrency": "USD",
    "price": "99.99",
    "priceValidUntil": "2025-12-31",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition",
    "seller": {
      "@type": "Organization",
      "name": "Seller Name"
    },
    "shippingDetails": {
      "@type": "OfferShippingDetails",
      "shippingRate": {
        "@type": "MonetaryAmount",
        "value": "0",
        "currency": "USD"
      },
      "deliveryTime": {
        "@type": "ShippingDeliveryTime",
        "handlingTime": {
          "@type": "QuantitativeValue",
          "minValue": 0,
          "maxValue": 1,
          "unitCode": "DAY"
        },
        "transitTime": {
          "@type": "QuantitativeValue",
          "minValue": 1,
          "maxValue": 5,
          "unitCode": "DAY"
        }
      },
      "shippingDestination": {
        "@type": "DefinedRegion",
        "addressCountry": "US"
      }
    },
    "hasMerchantReturnPolicy": {
      "@type": "MerchantReturnPolicy",
      "applicableCountry": "US",
      "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
      "merchantReturnDays": 30,
      "returnMethod": "https://schema.org/ReturnByMail",
      "returnFees": "https://schema.org/FreeReturn"
    }
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "bestRating": "5",
    "ratingCount": "142"
  },
  "review": [{
    "@type": "Review",
    "author": {
      "@type": "Person",
      "name": "Reviewer Name"
    },
    "datePublished": "2025-01-10",
    "reviewBody": "Review text here",
    "reviewRating": {
      "@type": "Rating",
      "ratingValue": "5",
      "bestRating": "5"
    }
  }]
}
```

**Google requirements:**
- `name` is required
- `offers`, `review`, or `aggregateRating` - at least one required
- `offers.price` and `offers.priceCurrency` required if offers present
- `offers.availability` must use Schema.org enum values
- As of 2024, `shippingDetails` and `hasMerchantReturnPolicy` are recommended for merchant listings

---

### 3. FAQPage

**Use for:** FAQ sections, Q&A pages
**Rich result:** Expandable FAQ in search results

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is the first question?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "<p>The answer with <strong>HTML formatting</strong> allowed. You can include <a href=\"https://example.com\">links</a>.</p>"
      }
    },
    {
      "@type": "Question",
      "name": "What is the second question?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Plain text answers also work."
      }
    }
  ]
}
```

**Google requirements:**
- Each `Question` must have exactly one `acceptedAnswer`
- Answer `text` can include HTML: `<h2>` through `<h6>`, `<br>`, `<ol>`, `<ul>`, `<li>`, `<a>`, `<p>`, `<b>`, `<strong>`, `<i>`, `<em>`
- Must be visible on the page (not hidden behind tabs/accordions without proper implementation)
- Google may show up to 3 FAQ rich results per page
- Do not use for advertising purposes

---

### 4. HowTo

**Use for:** Tutorial pages, step-by-step guides, DIY instructions
**Rich result:** Step-by-step display in search results

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Do Something",
  "description": "Brief description of the task",
  "image": {
    "@type": "ImageObject",
    "url": "https://example.com/howto-main.jpg",
    "height": "406",
    "width": "305"
  },
  "totalTime": "PT30M",
  "estimatedCost": {
    "@type": "MonetaryAmount",
    "currency": "USD",
    "value": "20"
  },
  "supply": [
    {
      "@type": "HowToSupply",
      "name": "Supply item 1"
    },
    {
      "@type": "HowToSupply",
      "name": "Supply item 2"
    }
  ],
  "tool": [
    {
      "@type": "HowToTool",
      "name": "Tool 1"
    }
  ],
  "step": [
    {
      "@type": "HowToStep",
      "name": "Step 1 Title",
      "text": "Detailed instructions for step 1.",
      "url": "https://example.com/howto#step1",
      "image": "https://example.com/step1.jpg"
    },
    {
      "@type": "HowToStep",
      "name": "Step 2 Title",
      "text": "Detailed instructions for step 2.",
      "url": "https://example.com/howto#step2",
      "image": "https://example.com/step2.jpg"
    }
  ]
}
```

**Google requirements:**
- `name` is required
- `step` array is required with at least one step
- Each step needs either `text` or `itemListElement` with `HowToDirection`/`HowToTip`
- `totalTime` uses ISO 8601 duration format (PT1H30M = 1 hour 30 minutes)
- Do not use HowTo for recipes (use Recipe schema instead)

---

### 5. Organization

**Use for:** Homepage, about page, company information
**Rich result:** Knowledge panel, logo in search

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Company Name",
  "alternateName": "Company Abbreviation",
  "url": "https://example.com",
  "logo": {
    "@type": "ImageObject",
    "url": "https://example.com/logo.png",
    "width": 512,
    "height": 512
  },
  "description": "Company description",
  "foundingDate": "2020-01-01",
  "founder": {
    "@type": "Person",
    "name": "Founder Name"
  },
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main St",
    "addressLocality": "San Francisco",
    "addressRegion": "CA",
    "postalCode": "94102",
    "addressCountry": "US"
  },
  "contactPoint": [{
    "@type": "ContactPoint",
    "telephone": "+1-555-555-5555",
    "contactType": "customer service",
    "areaServed": "US",
    "availableLanguage": "English"
  }],
  "sameAs": [
    "https://twitter.com/company",
    "https://linkedin.com/company/company",
    "https://facebook.com/company",
    "https://github.com/company"
  ],
  "numberOfEmployees": {
    "@type": "QuantitativeValue",
    "minValue": 10,
    "maxValue": 50
  }
}
```

---

### 6. LocalBusiness

**Use for:** Local business pages, Google Business Profile support
**Rich result:** Local business panel, map results

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "https://example.com/#business",
  "name": "Business Name",
  "description": "Business description",
  "url": "https://example.com",
  "telephone": "+1-555-555-5555",
  "email": "info@example.com",
  "image": "https://example.com/storefront.jpg",
  "logo": "https://example.com/logo.png",
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main St",
    "addressLocality": "San Francisco",
    "addressRegion": "CA",
    "postalCode": "94102",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "37.7749",
    "longitude": "-122.4194"
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "09:00",
      "closes": "17:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": "Saturday",
      "opens": "10:00",
      "closes": "14:00"
    }
  ],
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.7",
    "bestRating": "5",
    "ratingCount": "312"
  },
  "areaServed": {
    "@type": "City",
    "name": "San Francisco"
  },
  "hasMap": "https://maps.google.com/?cid=123456789"
}
```

**Google requirements:**
- `name`, `address` are required
- Use specific subtypes when possible: `Restaurant`, `Dentist`, `LegalService`, `RealEstateAgent`, etc.
- `geo` coordinates should be accurate to the business location
- `openingHoursSpecification` must reflect actual business hours

---

### 7. BreadcrumbList

**Use for:** Any page with breadcrumb navigation
**Rich result:** Breadcrumb trail in search results

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
      "name": "Current Page Title"
    }
  ]
}
```

**Google requirements:**
- `position` must be sequential starting at 1
- Last item should not have `item` (it's the current page)
- Must match the visible breadcrumb on the page

---

### 8. Review / AggregateRating

**Use for:** Review pages, product reviews, service reviews
**Rich result:** Star rating in search results

```json
{
  "@context": "https://schema.org",
  "@type": "Review",
  "name": "Review Title",
  "reviewBody": "Full review text...",
  "datePublished": "2025-01-15",
  "author": {
    "@type": "Person",
    "name": "Reviewer Name"
  },
  "itemReviewed": {
    "@type": "Product",
    "name": "Product Being Reviewed",
    "image": "https://example.com/product.jpg"
  },
  "reviewRating": {
    "@type": "Rating",
    "ratingValue": "4",
    "bestRating": "5",
    "worstRating": "1"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Review Site Name"
  }
}
```

**Google requirements:**
- `author` is required (must be a valid `Person` or `Organization`)
- `itemReviewed` is required
- `reviewRating` is recommended
- Self-serving reviews (reviewing your own product) are against guidelines

## Multi-Schema Pages

Most pages need multiple schema types. Combine them using `@graph`:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://example.com/#organization",
      "name": "Company Name",
      "url": "https://example.com",
      "logo": "https://example.com/logo.png"
    },
    {
      "@type": "WebSite",
      "@id": "https://example.com/#website",
      "url": "https://example.com",
      "name": "Site Name",
      "publisher": { "@id": "https://example.com/#organization" }
    },
    {
      "@type": "WebPage",
      "@id": "https://example.com/page/#webpage",
      "url": "https://example.com/page/",
      "name": "Page Title",
      "isPartOf": { "@id": "https://example.com/#website" }
    },
    {
      "@type": "Article",
      "mainEntityOfPage": { "@id": "https://example.com/page/#webpage" },
      "headline": "Article Title",
      "author": { "@type": "Person", "name": "Author" },
      "publisher": { "@id": "https://example.com/#organization" },
      "datePublished": "2025-01-15"
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.com" },
        { "@type": "ListItem", "position": 2, "name": "Blog", "item": "https://example.com/blog" },
        { "@type": "ListItem", "position": 3, "name": "Article Title" }
      ]
    }
  ]
}
```

## Generation Process

When the user asks for schema markup:

1. **Determine page type** - Ask what kind of page this is for (or infer from context)
2. **Gather information** - Ask for or collect the required fields. If the user provides a URL, fetch it to extract data.
3. **Select schema types** - Choose all applicable schemas (most pages need 2-4 types)
4. **Generate JSON-LD** - Create complete, valid markup
5. **Validate** - Check against Google's requirements for each type
6. **Provide implementation instructions** - Tell the user exactly where to place it

## Implementation Instructions

For **Next.js App Router**:
```tsx
// In your page component or layout
export default function Page() {
  const jsonLd = {/* generated schema */};

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      {/* page content */}
    </>
  );
}
```

For **Next.js with next/head (Pages Router)**:
```tsx
import Head from 'next/head';

export default function Page() {
  const jsonLd = {/* generated schema */};

  return (
    <>
      <Head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </Head>
      {/* page content */}
    </>
  );
}
```

For **plain HTML**:
```html
<head>
  <script type="application/ld+json">
  {/* generated schema */}
  </script>
</head>
```

## Validation

After generating the markup, remind the user to validate using:
1. **Google Rich Results Test:** https://search.google.com/test/rich-results
2. **Schema.org Validator:** https://validator.schema.org/

## Common Mistakes to Avoid

- Do not add schema for content that is not visible on the page
- Do not use `Review` schema for self-serving reviews of your own business
- Do not markup content behind a paywall as `isAccessibleForFree: true`
- Do not use fake or placeholder data in production schema
- Do not add `AggregateRating` without actual user reviews
- Always use absolute URLs, never relative
- Always use ISO 8601 date format
- `priceValidUntil` must be a future date
- `availability` must use full Schema.org URL (e.g., `https://schema.org/InStock`)
- Image URLs must be crawlable and indexable
