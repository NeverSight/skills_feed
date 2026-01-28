---
name: seo
description: Optimize content for search engines and AI answer engines. Use when writing or auditing SEO for any Lightfast page.
allowed-tools: Read, Grep, Glob, Write, Edit
---

# SEO Skill

Comprehensive SEO and AEO (Answer Engine Optimization) guidelines for Lightfast pages.

## Core Principle: Citability Over Rankings

Traditional SEO optimizes for position #1-10. AEO optimizes for **AI citation frequency**. Modern SEO requires both.

> "AEO is about becoming the definitive source that AI trusts and cites, not just ranking for keywords."

## When to Use This Skill

- Writing new Lightfast pages
- Auditing existing pages for SEO/AEO compliance
- Adding structured data (JSON-LD schema)
- Reviewing meta tags and OpenGraph

## Quick Reference

### Content Structure Requirements

| Element | Requirement |
|---------|-------------|
| TL;DR | 40-100 words, first position |
| Meta description | 150-160 chars |
| FAQ section | 3-5 Q&A pairs |
| Answer-first | Key answer in first 200 words |
| Question headings | H2/H3 as questions |
| Internal links | 3-5 per page |

### Schema Priority

| Priority | Schema Type | Use Case |
|----------|-------------|----------|
| 1 | FAQPage | Any page with Q&A content |
| 2 | HowTo | Step-by-step instructions |
| 3 | Article | Content with dates and authors |
| 4 | WebPage | General pages, landing pages |
| 5 | Product | Features with pricing |
| 6 | Organization | Site-wide identity |

## The 5-Step AEO Framework

1. **Analyze**: What are users asking AI about this topic?
2. **Create**: Structure content for citability (tables, lists, FAQs)
3. **Distribute**: Link from high-authority pages
4. **Measure**: Track AI visibility (citations, mentions)
5. **Iterate**: Refresh content every 90 days for recency signals

## Resources

- **[Core Requirements](resources/core-requirements.md)**: Universal SEO/AEO standards
- **[Schema Patterns](resources/schema-patterns.md)**: JSON-LD templates
- **[URL Guidelines](resources/url-guidelines.md)**: URL structure best practices
- **[Meta Templates](resources/meta-templates.md)**: Meta tag patterns
- **[SEO Checklist](resources/checklist.md)**: Pre-publish validation

## Do

- Lead with direct answers (first 100-200 words)
- Use question-format headings for discoverability
- Include comparison tables with specific values
- Add FAQ sections with self-contained answers
- Cite 5+ external authoritative sources (E-E-A-T)
- Update content regularly (90-day freshness signal)

## Don't

- Keyword stuff (AI detects this)
- Use generic headings ("Overview", "Introduction")
- Skip schema markup
- Write walls of text without structure
- Use creative prose over clarity
- Neglect internal linking

## AI Engine Optimization Matrix

| Engine | Priority Signal | Content Focus |
|--------|-----------------|---------------|
| ChatGPT | Comprehensiveness | Encyclopedic coverage |
| Perplexity | Recency (90 days) | Fresh, updated content |
| Google AI | E-E-A-T + Rankings | Authority signals |
| Gemini | Entity clarity | Consistent terminology |

## Lightfast-Specific Notes

- Use `@vendor/seo/metadata` for `createMetadata` utility
- Use `@vendor/seo/json-ld` for `<JsonLd>` component
- Canonical URLs: `https://lightfast.ai/{path}`
- Twitter handle: `@lightfastai`
- OG images: 1200x630px, stored in `/public/og/`
