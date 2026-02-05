---
name: chatbot-seo
description: Optimize websites and content for AI chatbot retrieval and citation. Use when users want to improve how their content appears in AI-powered search (ChatGPT, Gemini, Claude, Perplexity), analyze chatbot retrieval patterns, optimize keywords for AI discovery, structure content for LLM parsing, or audit existing content for AI-friendliness. Triggers include requests about "chatbot SEO", "AI optimization", "LLM discoverability", "chatbot ranking", or analyzing how AI assistants find and cite web content.
---

# Chatbot SEO Optimization

Optimize content for discovery and citation by AI chatbots and LLM-powered search engines.

## Overview

As AI chatbots become primary discovery interfaces, traditional SEO is evolving. This skill helps optimize content for how LLMs retrieve, parse, and cite information - a practice sometimes called "AEO" (Answer Engine Optimization) or "GEO" (Generative Engine Optimization).

## Core Principles of Chatbot Optimization

### How Chatbots Discover Content

1. **Web Search Integration**: Most chatbots (ChatGPT Search, Gemini, Perplexity, Claude) use web search APIs that prioritize:
   - Recent, authoritative content
   - Clear, well-structured pages
   - Original sources over aggregators
   - High-quality domain reputation

2. **Content Parsing**: LLMs extract and synthesize information by:
   - Scanning for direct answers to questions
   - Identifying authoritative statements
   - Extracting structured data (tables, lists, statistics)
   - Recognizing expertise signals (credentials, citations, methodology)

3. **Citation Logic**: Chatbots tend to cite sources that:
   - Directly answer the query
   - Provide unique insights or data
   - Include specific facts, statistics, or quotes
   - Come from trusted domains
   - Are recent (for time-sensitive topics)

## Optimization Workflow

### Step 1: Content Audit

Analyze existing content for chatbot-friendliness:

```python
# Use the content audit script
python scripts/audit_content.py <url_or_file>
```

The script checks for:
- Clear headings and structure
- Answer-first formatting
- Citation-worthy data points
- Keyword density and placement
- Metadata completeness
- Schema markup presence

### Step 2: Keyword Research for AI

Unlike traditional SEO, optimize for natural language queries:

**Traditional SEO**: "best running shoes"
**Chatbot SEO**: "What are the best running shoes for flat feet?"

**Target query patterns:**
- Questions (who, what, when, where, why, how)
- Comparison queries ("X vs Y", "difference between")
- Recommendation requests ("best X for Y", "top X")
- Explanatory queries ("how does X work", "why does X")

**Tools and approach:**
1. Use references/query_patterns.md for common question frameworks
2. Identify information gaps your content fills uniquely
3. Focus on specific, answerable questions rather than broad topics

### Step 3: Content Structure Optimization

**Answer-First Architecture:**
```markdown
# [Clear, specific H1 with target question]

[Direct answer in first 1-2 sentences]

[Supporting details follow]

## Key Points
- Bullet point 1 with specific data
- Bullet point 2 with specific data

## Detailed Explanation
[Comprehensive context]
```

**Why this works:**
- LLMs can quickly extract the core answer
- Users get immediate value
- Supports various query intents (quick answer vs. deep dive)

### Step 4: Add Citation-Worthy Elements

Elements that increase citation likelihood:

**Data Points:**
- Original research and statistics
- Specific numbers, percentages, dates
- Survey results and methodology
- Case study outcomes

**Authoritative Signals:**
- Author credentials and bio
- Publication date (keep content fresh)
- References to primary sources
- Expert quotes with attribution

**Unique Value:**
- Original insights not found elsewhere
- Proprietary data or analysis
- Step-by-step methodologies
- Practical examples and templates

### Step 5: Technical Optimization

**Metadata:**
```html
<title>Specific, Question-Based Title - Brand</title>
<meta name="description" content="Direct answer in 150-160 chars">
<meta name="author" content="Expert Name, Credentials">
<meta property="og:type" content="article">
<meta property="article:published_time" content="2024-01-15">
```

**Schema Markup:**
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Your Title",
  "author": {"@type": "Person", "name": "Author"},
  "datePublished": "2024-01-15",
  "dateModified": "2024-02-01"
}
```

Use FAQ schema for Q&A content:
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "Question text",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Answer text"
    }
  }]
}
```

**Content Structure:**
- Use semantic HTML (article, section, aside)
- Clear heading hierarchy (H1 → H2 → H3)
- Tables for comparative data
- Lists for key points

### Step 6: Testing and Monitoring

**Manual Testing:**
1. Query ChatGPT Search, Perplexity, or Claude about your topic
2. Check if your content is cited
3. Evaluate position and context of citations

**Optimization Iterations:**
- If not cited: Add more specific data, improve answer clarity
- If cited but low prominence: Strengthen authority signals, update content
- If cited incorrectly: Improve structure, clarify key points

## Platform-Specific Considerations

### ChatGPT Search
- Relies heavily on Bing search results initially
- Favors very recent content for current topics
- Prefers clear, concise answers
- Often cites multiple sources for comprehensive answers

### Google Gemini
- Integrated with Google Search ranking signals
- Strong preference for authoritative domains
- Emphasizes E-E-A-T (Experience, Expertise, Authoritativeness, Trust)
- May show AI-generated overviews that synthesize multiple sources

### Perplexity
- Excellent at finding and citing specific data
- Shows multiple sources with inline citations
- Values primary sources and original research
- Good at finding niche, specialized content

### Claude (with search)
- Synthesizes information from multiple high-quality sources
- Explicitly cites specific claims with source attribution
- Prefers recent, authoritative content
- Follows up with additional searches for comprehensive answers

## Common Pitfalls to Avoid

1. **Keyword Stuffing**: Unnatural language hurts LLM parsing
2. **Thin Content**: Brief, generic answers won't get cited over comprehensive sources
3. **Outdated Information**: LLMs prioritize recent content for current topics
4. **Poor Structure**: Wall-of-text content is hard for LLMs to parse
5. **No Unique Value**: Regurgitating common knowledge won't earn citations
6. **Hidden Answers**: Burying key info deep in content reduces citation chances

## Quick Reference: Optimization Checklist

- [ ] Answer-first content structure
- [ ] Clear, descriptive headings
- [ ] Specific data points and statistics
- [ ] Author credentials visible
- [ ] Publication/update date prominent
- [ ] Schema markup implemented
- [ ] Mobile-friendly and fast-loading
- [ ] Primary source links included
- [ ] Unique insights or original research
- [ ] Natural language optimized for questions
- [ ] Key points in scannable format (bullets, tables)
- [ ] Comprehensive but concise answers

## Resources

This skill includes:

### scripts/
- `audit_content.py` - Analyze content for chatbot-friendliness
- `extract_queries.py` - Extract natural language queries from content
- `schema_generator.py` - Generate appropriate schema markup

### references/
- `query_patterns.md` - Common question frameworks and patterns
- `citation_triggers.md` - Elements that increase citation likelihood
- `platform_preferences.md` - Detailed platform-specific optimization tips
