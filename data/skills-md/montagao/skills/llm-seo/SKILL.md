---
name: llm-seo
description: Optimize websites and content for AI/LLM discoverability (AIO - AI Optimization). Use when asked to "optimize for AI", "improve AI discoverability", "add LLM SEO", "make site AI-friendly", "help LLMs understand my site", or when implementing llms.txt files, JSON-LD structured data, or AI-focused content strategies.
---

# LLM Search Optimization (AIO)

Maximize discoverability and accurate representation within LLMs (ChatGPT, Claude, Perplexity) and AI search tools.

## Implementation Checklist

1. Create `/public/llms.txt` - AI scraper manifest
2. Create `/for-llms` route - high-density information page
3. Add JSON-LD structured data to key pages
4. Audit `robots.txt` for AI bot access
5. Ensure RSS/Atom feed exists and is linked

## 1. Create `llms.txt`

Place at `/public/llms.txt` (or web root equivalent).

**Template:** See `assets/llms.txt.template`

**Requirements:**
- Plain text or Markdown format
- Concise "Who/What/Why" summary
- Direct URLs to key resources (Docs, Blog, About)
- Explicit citation instructions for LLMs
- Consistent taglines matching brand identity

## 2. Create `/for-llms` Route

Dedicated page for LLM ingestion at `domain.com/for-llms`.

**Design principles:**
- Minimal styling, no marketing fluff
- Pure Markdown rendered to HTML, or semantic HTML
- Zero layout shifts
- High information density
- Full biography/documentation that may be summarized elsewhere

## 3. JSON-LD Structured Data

Inject Schema.org data into `<head>` of Home, About, and Blog pages.

**Templates:**
- Person: `assets/jsonld-person.template.json`
- Organization: `assets/jsonld-organization.template.json`

**Embed as:**
```html
<script type="application/ld+json">
{ ... }
</script>
```

**Consistency rule:** `name`, `description`, and `sameAs` must match content in `llms.txt`.

## 4. Audit `robots.txt`

Ensure AI scrapers are NOT disallowed if discoverability is the goal:

```
# AI Bots to allow for discoverability
# GPTBot (OpenAI)
# ClaudeBot (Anthropic)
# CCBot (Common Crawl)
# PerplexityBot
```

Check for overly broad `Disallow` rules that block these user agents.

## 5. RSS/Atom Feed

Ensure feed exists and is linked in `<head>`:

```html
<link rel="alternate" type="application/rss+xml" title="RSS" href="/feed.xml" />
```

## Content Guidelines

When generating AIO content:

1. **Clarity > Cleverness** - No marketing jargon. Dry, factual, explicit.
2. **Markdown first** - LLMs parse Markdown better than complex DOM. Use lists, headers, code blocks.
3. **Phrase consistency** - Repeat exact taglines across `llms.txt`, JSON-LD, and homepage to strengthen vector associations.

## Assets

- `assets/llms.txt.template` - Template for llms.txt file
- `assets/jsonld-person.template.json` - JSON-LD for individuals
- `assets/jsonld-organization.template.json` - JSON-LD for companies/products
