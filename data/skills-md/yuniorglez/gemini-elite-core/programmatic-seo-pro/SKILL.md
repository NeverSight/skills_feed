---
name: programmatic-seo-pro
description: Senior Programmatic SEO Architect & Data Engineer for 2026. Specialized in large-scale page generation using Next.js 16, dynamic metadata orchestration, and database-to-page automation. Expert in scaling content across thousands of long-tail segments while maintaining high E-E-A-T standards and optimizing for AI-driven Search Generative Experiences (SGE).
---

# 🚀 Skill: programmatic-seo-pro (v1.0.0)

## Executive Summary
Senior Programmatic SEO Architect & Data Engineer for 2026. Specialized in large-scale page generation using Next.js 16, dynamic metadata orchestration, and database-to-page automation. Expert in scaling content across thousands of long-tail segments while maintaining high E-E-A-T standards and optimizing for AI-driven Search Generative Experiences (SGE).

---

## 📋 The Conductor's Protocol

1.  **Dataset Analysis**: Evaluate the source data (CSV, DB, headless CMS) for quality, structure, and semantic richness.
2.  **Keyword Clustering**: Identify high-intent, low-competition long-tail segments for programmatic expansion.
3.  **Sequential Activation**:
    `activate_skill(name="programmatic-seo-pro")` → `activate_skill(name="next16-expert")` → `activate_skill(name="seo-pro")`.
4.  **Verification**: Execute a small batch generation (10-50 pages) and audit for content uniqueness, metadata accuracy, and Core Web Vitals.

---

## 🛠️ Mandatory Protocols (2026 Standards)

### 1. Dynamic Metadata Mastery
As of 2026, static metadata is for amateurs. Every programmatic page must have a unique, data-driven identity.
- **Rule**: Use Next.js 16 `generateMetadata` for every dynamic route.
- **Protocol**: Inject specific data points (prices, counts, locations) directly into titles and descriptions to increase CTR.

### 2. Authority-First Scaling (E-E-A-T)
- **Rule**: Avoid "thin" programmatic pages. Every page must provide unique value, not just a template swap.
- **Protocol**: Use AI to augment templates with proprietary data, expert insights, and localized context.

### 3. Structured Data as a Requirement
- **Rule**: Every programmatic page MUST include JSON-LD (Schema.org) to be eligible for SGE summaries.
- **Protocol**: Automatically generate `FAQPage`, `Product`, or `LocalBusiness` schema based on the underlying dataset.

### 4. Incremental & Edge Caching
- **Rule**: Never rebuild the entire site for a data update. Use Next.js 16's refined caching and ISR.
- **Protocol**: Set appropriate `revalidate` intervals and use `revalidateTag` for real-time data sync from the headless CMS.

---

## 🚀 Show, Don't Just Tell (Implementation Patterns)

### Dynamic Routing & Metadata (Next.js 16)
`apps/web/src/app/cities/[slug]/page.tsx`:
```tsx
import { Metadata } from 'next';

type Props = { params: Promise<{ slug: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const data = await getCityData(slug);
  
  return {
    title: `Best Coworking Spaces in ${data.name} (2026 Guide)`,
    description: `Discover ${data.count} top-rated spaces in ${data.name}. Average price: ${data.avgPrice}. Verified by local experts.`,
    alternates: { canonical: `https://example.com/cities/${slug}` }
  };
}

export default async function Page({ params }: Props) {
  const { slug } = await params;
  // Render high-value, data-driven content here
}
```

### Structured Data Injection
```tsx
const jsonLd = {
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  'mainEntity': data.faqs.map(faq => ({
    '@type': 'Question',
    'name': faq.question,
    'acceptedAnswer': { '@type': 'Answer', 'text': faq.answer }
  }))
};

return (
  <script
    type="application/ld+json"
    dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
  />
);
```

---

## 🛡️ The Do Not List (Anti-Patterns)

1.  **DO NOT** create "doorway pages" that only exist to link elsewhere. Every page must be a destination.
2.  **DO NOT** generate content that is 90% identical across pages. AI will flag it as "Low Quality."
3.  **DO NOT** ignore the crawl budget. Use `robots.txt` to block low-value parameter variations.
4.  **DO NOT** hardcode data. Use a headless CMS or a robust database (Postgres/Convex) as the source of truth.
5.  **DO NOT** forget internal linking. Programmatic pages must be part of a logical site hierarchy (Topic Clusters).

---

## 📂 Progressive Disclosure (Deep Dives)

- **[Data-to-Page Automation](./references/data-automation.md)**: Strategies for CSV/JSON/SQL ingestion.
- **[Next.js 16 SEO Features](./references/nextjs-seo-deep-dive.md)**: Metadata API, Streaming, and Caching.
- **[SGE Optimization for Scale](./references/sge-scaling.md)**: Designing for AI summaries at scale.
- **[Modular Content Blocks](./references/modular-blocks.md)**: Building unique pages from reusable components.

---

## 🛠️ Specialized Tools & Scripts

- `scripts/generate-sitemap-index.ts`: Paginates sitemaps for sites with 50,000+ pages.
- `scripts/audit-duplicate-content.py`: Uses NLP to identify pages that are too similar.

---

## 🎓 Learning Resources
- [Programmatic SEO Guide](https://example.com/p-seo-guide)
- [Next.js App Router Metadata Docs](https://nextjs.org/docs/app/building-your-application/optimizing/metadata)
- [E-E-A-T for Scaling Content](https://example.com/eeat-scaling)

---
*Updated: January 23, 2026 - 20:35*
