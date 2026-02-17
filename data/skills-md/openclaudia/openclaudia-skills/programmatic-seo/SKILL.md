---
name: programmatic-seo
description: Create SEO-optimized pages at scale using programmatic/template-based approaches. Use when the user says "programmatic SEO", "pSEO", "pages at scale", "template pages", "dynamic SEO pages", "auto-generate pages", "landing pages at scale", "city pages", "comparison pages", or wants to create many similar pages targeting different keywords.
---

# Programmatic SEO Skill

You are an expert in programmatic SEO (pSEO) -- the strategy of creating large numbers of targeted pages using templates and data. Help users identify page patterns, build templates, and deploy at scale while avoiding thin content penalties.

## What is Programmatic SEO?

Programmatic SEO creates pages at scale by combining:
- A **page template** (layout + structure)
- A **data source** (database, API, CSV)
- **Dynamic content** (unique per page, not just variable substitution)
- **SEO optimization** (meta tags, internal links, schema)

**Examples of successful pSEO:**
- Zapier: "How to connect {App A} to {App B}" (150K+ pages)
- Nomad List: "{City} for digital nomads" (1000+ city pages)
- Wise: "{Currency A} to {Currency B} exchange rate" (10K+ pages)
- G2: "{Software} reviews" (100K+ product pages)
- Tripadvisor: "Best {type} in {city}" (millions of pages)

## Process

### Step 1: Identify the Page Pattern

Help the user find their pSEO opportunity. Look for patterns where:

**Pattern formula:** `{Modifier} + {Head Term} + {Qualifier}`

| Pattern Type | Formula | Example | Volume Potential |
|-------------|---------|---------|-----------------|
| Location + Service | "{service} in {city}" | "plumber in Austin" | Cities x Services |
| Comparison | "{product A} vs {product B}" | "Notion vs Asana" | nC2 combinations |
| Integration | "{tool A} + {tool B} integration" | "Slack Salesforce integration" | Tools x Tools |
| Template/Example | "{type} template" | "invoice template" | Types count |
| Stats/Data | "{topic} statistics {year}" | "remote work statistics 2025" | Topics x Years |
| Glossary | "What is {term}" | "What is APR" | Terms count |
| Best/Top | "Best {product} for {use case}" | "Best CRM for startups" | Products x Uses |
| Review | "{product} review" | "Airtable review" | Products count |
| Alternative | "{product} alternatives" | "Slack alternatives" | Products count |
| Cost/Pricing | "How much does {service} cost" | "How much does a website cost" | Services count |

**Qualification criteria for a good pSEO opportunity:**
- [ ] Pattern has 100+ possible pages minimum
- [ ] Each combination has measurable search volume (even 10-50/mo is fine at scale)
- [ ] You can generate genuinely useful, unique content for each page
- [ ] The data is available (API, database, web scraping)
- [ ] Competitors aren't already dominating with better data
- [ ] Pages serve real user intent (not just keyword stuffing)

### Step 2: Build the Data Source

Define the data model that powers the pages:

```typescript
// Example: City + Service pages
interface PageData {
  // URL parameters
  slug: string;           // "plumber-in-austin-tx"
  city: string;           // "Austin"
  state: string;          // "TX"
  service: string;        // "plumber"

  // SEO fields
  title: string;          // "Best Plumber in Austin, TX | Top 10 for 2025"
  metaDescription: string; // "Find the best plumber in Austin, TX..."
  h1: string;             // "Best Plumber in Austin, TX"

  // Dynamic content
  providers: Provider[];  // Local providers data
  avgCost: number;        // Average cost in this market
  reviewCount: number;    // Total reviews aggregated
  faqs: FAQ[];            // Location-specific FAQs

  // Related pages (internal linking)
  nearbyPages: string[];  // Nearby cities
  relatedServices: string[]; // Related services
}
```

**Data sources to consider:**
- Public APIs (government data, Wikipedia, industry databases)
- Web scraping (with permission/robots.txt compliance)
- User-generated content (reviews, contributions)
- AI-generated unique analysis per entity
- Licensed data (paid data providers)
- Internal product data (for SaaS/e-commerce)

### Step 3: Create the Page Template

Build a template that generates high-quality, unique pages. Critical principle: **each page must provide standalone value.**

#### Template Structure

```markdown
## Page Template: {Pattern Name}

### Above the Fold
- H1: {dynamic title}
- Key stat or hook: {dynamic data point}
- Quick summary: 2-3 sentences with unique data
- CTA (if commercial intent)

### Main Content Section 1: Overview
- {Entity}-specific introduction (NOT generic)
- Unique data point 1: {dynamic}
- Unique data point 2: {dynamic}
- Contextual explanation

### Main Content Section 2: Detailed Analysis
- Comparison table or detailed breakdown
- {Entity}-specific insights
- Data visualizations if applicable

### Main Content Section 3: Practical Information
- How-to or action steps
- Costs, timing, or specifications
- Location-specific or entity-specific details

### Related Content
- Internal links to related pages (same cluster)
- Links to parent/pillar page
- Links to sibling pages

### FAQ Section
- 3-5 questions specific to this entity
- Answers with unique data points

### Schema Markup
- Appropriate structured data for page type
```

#### Avoiding Thin Content

**The #1 risk in pSEO is thin content.** Every page must pass this checklist:

| Check | Requirement | How |
|-------|------------|-----|
| Unique content | > 60% of visible text is unique to this page | Dynamic data, unique analysis, UGC |
| Sufficient depth | > 500 words of substantive content per page | Template sections + dynamic content |
| Unique data | At least 2 data points unique to this entity | API data, calculations, aggregations |
| Useful to visitor | Page answers the searcher's query fully | Match search intent |
| Not auto-generated feel | Reads naturally, not like a template | Varied sentence structures, context |
| Internal value | Links to and from other relevant pages | Related pages section, breadcrumbs |
| Visual content | At least 1 unique or relevant image | Maps, charts, entity images |

### Step 4: Next.js Implementation

#### Dynamic Routes (App Router)

```typescript
// app/[service]/[city]/page.tsx

import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { getPageData, getAllPages } from '@/lib/pseo-data';

interface Props {
  params: { service: string; city: string };
}

// Generate static paths at build time
export async function generateStaticParams() {
  const pages = await getAllPages();
  return pages.map((page) => ({
    service: page.serviceSlug,
    city: page.citySlug,
  }));
}

// Dynamic meta tags
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const data = await getPageData(params.service, params.city);
  if (!data) return {};

  return {
    title: data.title,
    description: data.metaDescription,
    alternates: {
      canonical: `https://example.com/${params.service}/${params.city}`,
    },
    openGraph: {
      title: data.ogTitle,
      description: data.ogDescription,
      url: `https://example.com/${params.service}/${params.city}`,
      type: 'website',
    },
  };
}

export default async function Page({ params }: Props) {
  const data = await getPageData(params.service, params.city);
  if (!data) notFound();

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'WebPage',
    name: data.title,
    description: data.metaDescription,
    // ... additional schema
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      {/* Page component tree */}
    </>
  );
}
```

#### Sitemap Generation

```typescript
// app/sitemap.ts
import { MetadataRoute } from 'next';
import { getAllPages } from '@/lib/pseo-data';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const pages = await getAllPages();

  return pages.map((page) => ({
    url: `https://example.com/${page.serviceSlug}/${page.citySlug}`,
    lastModified: page.updatedAt,
    changeFrequency: 'monthly',
    priority: 0.7,
  }));
}
```

For large sitemaps (50,000+ URLs), use sitemap index:

```typescript
// app/sitemap.xml/route.ts
import { getAllPageCount } from '@/lib/pseo-data';

export async function GET() {
  const totalPages = await getAllPageCount();
  const sitemapCount = Math.ceil(totalPages / 50000);

  const sitemaps = Array.from({ length: sitemapCount }, (_, i) =>
    `<sitemap><loc>https://example.com/sitemap-${i}.xml</loc></sitemap>`
  ).join('');

  return new Response(
    `<?xml version="1.0" encoding="UTF-8"?>
    <sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      ${sitemaps}
    </sitemapindex>`,
    { headers: { 'Content-Type': 'application/xml' } }
  );
}
```

#### Robots.txt Management

```typescript
// app/robots.ts
import { MetadataRoute } from 'next';

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: ['/api/', '/admin/'],
      },
    ],
    sitemap: 'https://example.com/sitemap.xml',
  };
}
```

### Step 5: Internal Linking Strategy

Internal linking is critical for pSEO. Implement these patterns:

**1. Hub-and-Spoke:**
```
Hub: /services/plumber/
  |- /plumber/austin-tx
  |- /plumber/dallas-tx
  |- /plumber/houston-tx
```

**2. Sibling Links:**
Each city page links to 5-10 nearby city pages for the same service.

**3. Cross-Category Links:**
Each city page links to other services in the same city.

**4. Breadcrumb Navigation:**
```
Home > Services > Plumber > Austin, TX
```

**5. Footer/Sidebar Links:**
Popular pages and category indexes.

**Implementation pattern:**
```typescript
// Internal linking component
function RelatedPages({ currentSlug, relatedPages }) {
  return (
    <section>
      <h2>Related Pages</h2>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        {relatedPages.map((page) => (
          <Link
            key={page.slug}
            href={`/${page.slug}`}
            className="text-blue-600 hover:underline"
          >
            {page.title}
          </Link>
        ))}
      </div>
    </section>
  );
}
```

### Step 6: Indexation Management

When deploying thousands of pages, manage indexation carefully:

**Gradual rollout:**
1. Deploy 50-100 pages first
2. Monitor indexation in Google Search Console
3. Check for "Discovered - currently not indexed" and "Crawled - currently not indexed"
4. If indexation rate > 80%, continue deploying in batches of 500-1000
5. If indexation rate < 50%, improve page quality before deploying more

**Indexation signals:**
- Submit sitemap to Google Search Console
- Use IndexNow API (Bing, Yandex) for faster discovery
- Internal link from high-authority existing pages
- Share initial pages on social media for crawl signals

**Quality thresholds:**
- If Google indexes < 30% of pages, your template likely produces thin content
- If pages get indexed then dropped, content quality is borderline
- Monitor "Page experience" and "Core Web Vitals" in GSC for pSEO pages

### Step 7: Meta Tag Formulas

Use these formulas for generating meta tags at scale:

**Title tag formulas (50-60 chars):**
```
"{Primary Keyword} in {Location} | {Brand}"
"Best {Service} in {City}, {State} ({Year})"
"{Product A} vs {Product B}: {Differentiator}"
"{Number} Best {Category} for {Use Case} ({Year})"
"How Much Does {Service} Cost in {City}? ({Year} Pricing)"
```

**Meta description formulas (150-160 chars):**
```
"Find the best {service} in {city}. Compare {X} local providers, read {Y} reviews, and get free quotes. Average cost: ${Z}."
"Detailed comparison of {A} vs {B}. See features, pricing, pros/cons, and which is better for {use case}."
"{X} best {category} for {audience}. We analyzed {Y} options based on {criteria}. Updated for {year}."
```

**H1 formulas:**
```
"Best {Service} in {City}, {State}"
"{Product A} vs {Product B}: Complete Comparison"
"{Number} Best {Category} for {Use Case}"
```

## Output

When helping a user with programmatic SEO, deliver:

1. **Opportunity Analysis** - The pattern, estimated page count, volume potential
2. **Data Model** - TypeScript interface for the page data
3. **Page Template** - Complete template with all sections
4. **Sample Pages** - 2-3 fully rendered example pages
5. **Implementation Plan** - Next.js code for routes, sitemap, robots.txt
6. **Internal Linking Strategy** - How pages connect
7. **Indexation Plan** - Rollout schedule and monitoring metrics
8. **Quality Checklist** - Per-page quality criteria

## Common Pitfalls

- **Template stuffing:** Just swapping city names in identical text = thin content penalty
- **No unique data:** Pages without entity-specific data points add no value
- **Over-generation:** Creating pages for combinations with zero search volume wastes crawl budget
- **Ignoring cannibalization:** Overlapping pages compete with each other. Map one keyword per page.
- **No internal links:** Orphan pages won't get crawled or ranked
- **All at once:** Deploying 100K pages overnight looks unnatural. Batch them.
- **Ignoring noindex:** Some pages may not deserve indexing. Use `noindex` for low-quality or duplicate combinations.
