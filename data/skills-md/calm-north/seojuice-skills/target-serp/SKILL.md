---
name: target-serp
description: >
  Identify and capture SERP features for target keywords — featured snippets,
  People Also Ask boxes, knowledge panels, and rich results. Use when the user
  asks about featured snippets, position zero, PAA optimization, rich results,
  schema markup for SERP features, or how to get more SERP real estate.
metadata:
  version: 1.0.0
---

# Target SERP

Identify and capture featured snippets, People Also Ask boxes, knowledge panels,
and rich results for target keywords.

## SERP Feature Types

| Feature | Trigger | Content Format Needed |
|---------|---------|----------------------|
| Featured Snippet (paragraph) | "What is", "how does", definitional queries | 40-60 word direct answer under an H2/H3 matching the query |
| Featured Snippet (list) | "How to", "steps to", "best", "top" | Ordered or unordered list with H2/H3 heading |
| Featured Snippet (table) | Comparison, pricing, specs queries | HTML `<table>` with clear headers |
| People Also Ask | Most informational queries | Concise answer (2-3 sentences) under an H2 that matches the PAA question |
| Knowledge Panel | Brand/entity queries | Structured data (Organization, Person), Wikipedia presence, consistent NAP |
| Rich Results (FAQ) | Pages with FAQ content | FAQPage schema markup |
| Rich Results (How-To) | Tutorial/instructional pages | HowTo schema markup |
| Rich Results (Review) | Product/service review pages | Review/AggregateRating schema markup |
| Rich Results (Breadcrumb) | Any page with hierarchy | BreadcrumbList schema markup |
| Sitelinks | Brand queries | Clear site structure, descriptive navigation, internal linking |

## SERP Feature Prioritization Matrix

Not all SERP features are equally valuable. Use this to decide where to invest effort:

| SERP Feature | Traffic Impact | Effort to Win | Best For |
|-------------|--------------|--------------|---------|
| Featured Snippet | Very High | Medium | Informational content sites |
| AI Overview citation | High (growing) | Medium-High | Authority/expertise sites |
| People Also Ask | Medium-High | Low-Medium | FAQ-rich content |
| Video Carousel | High | High | Tutorial/how-to content |
| Local Pack | Very High (local) | Medium | Local businesses |
| Rich Results (Review) | Medium-High | Low-Medium | Product/service reviews |
| Image Pack | Medium | Low-Medium | Visual content creators |
| Shopping Results | Very High (ecommerce) | Medium | Product sellers |
| Knowledge Panel | Medium (brand) | High (long-term) | Established brands |

### Feature Combination Patterns

When multiple features appear together, optimize for the combination:

| Combination | Opportunity |
|------------|------------|
| AI Overview + Featured Snippet | Optimize for both — structured content with clear answers wins both slots |
| Video + PAA + Featured Snippet | Create a comprehensive guide with video and FAQ section |
| Shopping + Ads + Reviews | Product optimization + review schema + merchant feed |
| PAA only (no snippet) | Snippet opportunity — create snippet-optimized content to claim it |
| AI Overview only (no snippet) | Structured, authoritative content with cited data gets AI inclusion |

### AI Overview vs Traditional SERP Strategy

| Query Type | Traditional Strategy | AI-Era Strategy |
|-----------|---------------------|-----------------|
| Informational | Win featured snippet | Win AI Overview citation AND featured snippet |
| Comparison | Create comparison content | Create structured comparison tables with clear verdicts |
| Definition | Write clear definition for snippet | Write authoritative, citable definition with evidence |
| How-to | Create step-by-step list | Create steps with unique insights AI can synthesize |

Traditional features reward **format optimization**. AI Overviews reward **authority and uniqueness**.

## Step 1: Audit Current SERP Features

For each target keyword:

1. **Search the keyword** and document which SERP features appear
2. **Note who currently holds each feature** (which domain, what content format)
3. **Check if your site already appears** in any feature for this keyword
4. **Assess winnability** — can you match or beat the current holder's content format?

| Keyword | Feature Present | Current Holder | Your Page | Winnable? |
|---------|----------------|---------------|-----------|-----------|
| ... | Featured snippet (paragraph) | competitor.com | /blog/topic | Yes — need better answer |
| ... | PAA (3 questions) | various | No page | Yes — create FAQ section |
| ... | Knowledge panel | — | — | No — need Wikipedia presence |

## Step 2: Featured Snippet Optimization

Featured snippets pull content directly from pages. To win them:

### Paragraph Snippets
- Place a concise answer (40-60 words) directly under an H2 or H3 that matches the query
- Start with a definition or direct statement: "[Topic] is..."
- Follow the snippet-bait with expanded detail (Google wants the page to have depth, not just a snippet)

### List Snippets
- Use a proper HTML ordered or unordered list
- H2 heading should match the query: "How to [do thing]" or "Best [category]"
- 5-8 list items (Google rarely shows more)
- Each item should be a concise, scannable phrase

### Table Snippets
- Use semantic HTML `<table>` with `<thead>` and `<tbody>`
- Column headers should be descriptive
- Keep to 3-5 columns, 4-8 rows
- Include the query keyword in the table caption or preceding heading

### Snippet Optimization Checklist
- [ ] H2/H3 heading matches the target query exactly or closely
- [ ] Answer appears in the first paragraph after the heading
- [ ] Answer is self-contained (makes sense without surrounding context)
- [ ] Page already ranks on page 1 for the keyword (snippets almost always come from page 1 results)
- [ ] Content format matches what Google currently shows (paragraph, list, or table)

## Step 3: People Also Ask Optimization

PAA boxes appear on a large share of informational searches. To capture them:

1. **Collect PAA questions** for your target keywords
2. **Add an FAQ section** to relevant pages using the exact question as an H2 or H3
3. **Answer in 2-3 sentences** directly under the heading
4. **Mark up with FAQPage schema** for rich result eligibility

PAA answers should be:
- Direct and concise (no "great question!" preamble)
- Factually accurate
- Self-contained (answer stands alone)

## Step 4: Schema Markup

Add structured data for rich result eligibility.

**Important:** Google significantly restricted FAQ rich results in August 2023. FAQPage
schema now only generates rich results for well-known government and health authority
sites. For most sites, FAQ schema still helps AI systems extract Q&A content but will
not produce visible rich results in Google SERPs.

### FAQPage (AI extraction — not visual rich results for most sites)
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "What is [topic]?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Direct answer here."
    }
  }]
}
```

### HowTo
For step-by-step content. Include `name`, `step` array with `HowToStep`, `estimatedCost`, and `totalTime`:
```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to [do thing]",
  "totalTime": "PT30M",
  "step": [{
    "@type": "HowToStep",
    "name": "Step 1 title",
    "text": "Step 1 description",
    "image": "https://example.com/step1.jpg"
  }]
}
```

### Article
For blog posts and guides: include `headline`, `datePublished`, `dateModified`, `author`, `image`.

### BreadcrumbList
For every page with hierarchical navigation: define the path from home to current page.

### VideoObject
For pages with embedded videos — enables video rich results and video carousels:
```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "Video title",
  "description": "Video description",
  "thumbnailUrl": "https://example.com/thumb.jpg",
  "uploadDate": "2026-01-15",
  "duration": "PT5M30S",
  "contentUrl": "https://example.com/video.mp4"
}
```

### Dataset
For pages with original research or data — surfaces in Google Dataset Search:
```json
{
  "@context": "https://schema.org",
  "@type": "Dataset",
  "name": "Dataset title",
  "description": "What this dataset contains",
  "creator": { "@type": "Organization", "name": "Your Brand" },
  "datePublished": "2026-01-15",
  "license": "https://creativecommons.org/licenses/by/4.0/"
}
```

### SpeakableSpecification
Marks content sections suitable for text-to-speech and voice assistant extraction:
```json
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": [".article-summary", ".key-finding"]
  }
}
```

**Validation:** Always validate schema with Google's Rich Results Test before deploying.

## Step 5: Action Plan

For each target keyword and feature:

| Keyword | Target Feature | Current Status | Action Required | Page to Optimize | Priority |
|---------|---------------|---------------|-----------------|-----------------|----------|
| ... | Featured snippet | Competitor holds it | Add snippet-bait paragraph under matching H2 | /blog/guide | High |
| ... | PAA | Not present on our site | Add FAQ section with schema | /blog/guide | Medium |
| ... | Rich result (FAQ) | No schema | Add FAQPage JSON-LD | /faq | Low |

## Output Format

### SERP Feature Audit: [domain or keyword set]

**Current SERP Feature Presence**
- Features held: [count]
- Features available to win: [count]
- Keywords with SERP features: [count out of total]

**Feature Opportunities**
[Table from Step 1]

**Action Plan**
[Table from Step 5]

**Schema Implementation List**
For each page needing schema:
- Page URL
- Schema type to add
- Key fields to populate
- Validation status

---

> **Pro Tip:** Use the free [Schema Markup Generator](https://seojuice.com/tools/schema-markup-generator/)
> to build JSON-LD for any page type, and the [SERP Feature Landscape](https://seojuice.com/tools/serp-features/)
> tool to explore which features dominate your niche. SEOJuice MCP users can run
> `/seojuice:keyword-analysis` to find high-impression, low-click keywords where SERP features
> are stealing clicks.
