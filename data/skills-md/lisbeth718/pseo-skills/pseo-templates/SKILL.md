---
name: pseo-templates
description: Create page templates with dynamic routing for programmatic SEO, including unique intent-matched content per page with differentiated titles, headings, descriptions, and FAQs. Use when building or refactoring pSEO page templates, setting up dynamic routes, or ensuring each generated page has unique, valuable content.
argument-hint: "[page-type]"
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# pSEO Page Templates

Build page templates that produce unique, intent-matched content at scale through dynamic routing and structured data rendering.

## Core Principles

1. **One template, many unique pages**: Templates are content-agnostic shells that render data
2. **No thin pages**: Every generated page must have substantial, differentiated content
3. **Intent matching**: Each page targets a specific search intent derived from its data
4. **Semantic HTML**: Use correct heading hierarchy, landmarks, and elements
5. **Progressive enhancement**: Pages work without JavaScript

## Implementation Steps

### 1. Set Up Dynamic Routes

Create dynamic route segments using the framework's routing system:

**Next.js App Router:**
```
app/
  [category]/
    page.tsx                    # category hub page
    [slug]/
      page.tsx                  # individual pSEO page
```

**Next.js Pages Router:**
```
pages/
  [category]/
    index.tsx
    [slug].tsx
```

Implement `generateStaticParams` (App Router) or `getStaticPaths` (Pages Router) using the data layer's `getAllSlugs()`.

### 2. Design the Page Template Structure

Every pSEO page template must include these content sections. **Value goes first** — the December 2025 core update devalues pages that bury useful content under filler intros, excessive ads, or boilerplate. The user's query should be answered within the first visible viewport.

```
┌─────────────────────────────┐
│ Breadcrumbs                 │
├─────────────────────────────┤
│ H1 (unique per page)        │
│ Key answer / value upfront  │  ← answer the search intent immediately
├─────────────────────────────┤
│ Primary content section     │
│ (unique body/data)          │
├─────────────────────────────┤
│ E-E-A-T signals             │  ← author, sources, data provenance
├─────────────────────────────┤
│ FAQ section (if applicable) │
├─────────────────────────────┤
│ Related pages / internal    │
│ links                       │
├─────────────────────────────┤
│ Category hub link           │
└─────────────────────────────┘
```

**"Needs Met" rule (Google Dec 2025):** If a user lands on this page from a search result, they should find the answer or primary value within the first screenful of content. No filler paragraphs, no "in today's world..." intros, no walls of generic text before the actual content. Get to the point immediately.

**LLM extraction rule:** Each section between headings should be a self-contained "answer capsule" of 134-167 words that makes sense if extracted without surrounding context. LLMs pull individual chunks, not full pages. A section heading should read as a question or topic, and the content below should fully answer it standalone. See pseo-llm-visibility for complete LLM optimization guidance.

### 3. Ensure Content Uniqueness

Each page MUST differentiate itself through:

- **Title**: Constructed from data fields, not a single template string with one variable swap
- **H1**: May differ from the title; should include the primary keyword naturally
- **Meta description**: Generated from page-specific data, not a boilerplate with token replacement
- **Body content**: Driven by page data — descriptions, stats, attributes, comparisons
- **FAQ section**: Questions and answers specific to the page's topic

Bad: `"Best {keyword} in {city}"` for every page.
Better: Titles that incorporate multiple data dimensions (type, location, attribute, use case).

### 4. Use Structured Content Blocks

Text variation alone is not enough to avoid thin content flags. Build reusable content components that render substantive, data-driven sections:

- **Data tables**: Render structured attributes as a comparison or specification table (e.g., features, specs, pricing tiers)
- **Stat highlights**: Pull numeric data into visual callouts (e.g., "4.8 rating", "500+ reviews", "Est. 2019")
- **Attribute breakdowns**: Render key-value pairs from the data model as descriptive sections (not just a list)
- **Comparison grids**: If the page relates to alternatives, render a side-by-side comparison
- **Contextual prose**: Generate intro and summary paragraphs from multiple data fields — not a single sentence template
- **FAQ accordion**: Render page-specific Q&A pairs (required: questions must be visible on page if using FAQPage schema)
- **Related content cards**: Previews of related pages with titles, descriptions, and images

The goal: if you remove the page title and URL, the remaining content should still be identifiably about *this specific topic* and not interchangeable with another page.

### 5. Implement the Page Component

```typescript
// Pattern for a pSEO page component
export default async function Page({ params }) {
  const data = await getPageData(params.slug);

  if (!data) return notFound();

  return (
    <article>
      <Breadcrumbs category={data.category} current={data.h1} />
      <h1>{data.h1}</h1>
      <IntroSection data={data} />
      <MainContent data={data} />
      {data.faqs?.length > 0 && <FAQSection faqs={data.faqs} />}
      <RelatedPages slug={data.slug} category={data.category} />
    </article>
  );
}
```

### 6. Handle Edge Cases

- **Missing data**: Return `notFound()` for slugs without data — never render empty pages
- **Fallback rendering**: If using ISR with fallback, show a loading state, not empty content
- **Draft pages**: Add a mechanism to exclude draft/incomplete content from generation
- **Pagination**: If a page type has too much content, implement pagination with rel prev/next

### 7. Create Category Hub Pages

Hub pages aggregate and link to individual pages within a category:

- Display a categorized listing of all pages in the category
- Include an intro paragraph unique to the category
- Link to every child page (or paginate if >100)
- Include the category's own metadata and schema markup

### 8. Add E-E-A-T Signals

Google's 2025 updates heavily weight Experience, Expertise, Authoritativeness, and Trustworthiness — even on programmatic pages. Every pSEO template should include:

- **Data provenance**: Where the information comes from (cite sources, databases, official records)
- **Last updated date**: Visible on the page, not just in schema. Shows the content is maintained.
- **Author or organization attribution**: Who is responsible for this content. Can be an organization for pSEO.
- **Methodology note** (where applicable): "Prices updated daily from [source]" or "Rankings based on [criteria]"
- **First-party evidence**: If the business has proprietary data, surface it (original research, real user data, verified reviews)

For YMYL topics (health, finance, civic, legal), E-E-A-T requirements are stricter:
- Author credentials must be explicit
- Sources must be authoritative (government, medical, legal sources)
- Content must be reviewed by a qualified person

```typescript
// E-E-A-T component pattern
function ContentAttribution({ source, lastUpdated, methodology }: EEATProps) {
  return (
    <aside aria-label="Content information">
      <p>Data sourced from {source}</p>
      <p>Last updated: <time dateTime={lastUpdated}>{formatDate(lastUpdated)}</time></p>
      {methodology && <p>Methodology: {methodology}</p>}
    </aside>
  );
}
```

### 9. Image SEO at Scale

Images are often a key differentiator for pSEO pages (product photos, location images, comparison visuals). Every image rendered by a template must have:

- **Unique alt text**: Generated from data fields, not a generic template. Bad: `alt="product image"`. Good: `alt="{productName} - {color} {material}, {brand}"`.
- **Descriptive filenames**: Use slugified data fields in image URLs where possible (e.g., `blue-wool-sweater-brand.webp` not `IMG_4523.jpg`)
- **Explicit dimensions**: `width` and `height` attributes to prevent CLS
- **Lazy loading**: All below-fold images use `loading="lazy"`; the LCP image uses `loading="eager"` or `priority`
- **Image schema**: If images are a core part of the page value, include `ImageObject` in the page's JSON-LD (coordinate with pseo-schema)

For pages without unique images, consider:
- Category-level placeholder images (better than no image for OG tags)
- Data-driven visual elements (charts, comparison tables) that serve as the page's visual content
- Omitting `og:image` entirely rather than using a generic placeholder across thousands of pages

## Template Checklist

Before considering a template complete:
- [ ] Every generated page has a unique H1 that differs from other pages
- [ ] Body content varies substantially between pages (not just variable swaps)
- [ ] At least 2 structured content blocks are present (data table, stats, attributes, FAQ, etc.)
- [ ] FAQ section renders page-specific questions (if the data includes FAQs)
- [ ] Breadcrumbs render correctly with the page's category hierarchy
- [ ] `notFound()` is returned for invalid slugs
- [ ] Related pages section links to other pages in the same category
- [ ] Semantic HTML is used (article, section, nav, h1-h3 hierarchy)
- [ ] `generateStaticParams` produces the complete slug list
- [ ] E-E-A-T signals present: data source, last updated date, attribution
- [ ] Primary value/answer is visible in the first viewport (no filler intros)
- [ ] YMYL pages have elevated trust signals (author credentials, authoritative sources)

## Relationship to Other Skills

- **Depends on**: pseo-data (content models and fetching)
- **Consumed by**: pseo-metadata (template structure informs meta tag placement)
- **Works with**: pseo-linking (templates render link components), pseo-schema (templates include schema scripts)
