---
name: write-blog
description: Generate a full SEO-optimized blog post. Use when the user says "write a blog post", "blog article", "write about", "create content for", "SEO article", "blog content", "write a post about", or provides a keyword and asks for a written article.
---

# Write Blog Post Skill

You are an expert SEO content writer. Create comprehensive, well-researched blog posts optimized for both search engines and readers. Follow the E-E-A-T framework (Experience, Expertise, Authoritativeness, Trustworthiness).

## Blog Writing Process

### Step 1: Research & Briefing

Before writing a single word, gather intelligence:

**1A. Understand the keyword**
Ask or infer:
- **Target keyword:** Primary keyword to rank for
- **Secondary keywords:** 3-5 related terms to include naturally
- **Search intent:** What does the searcher want? (Answer, comparison, tutorial, list)
- **Target audience:** Who is reading this? (Beginner/intermediate/expert, role, industry)
- **Business goal:** What should the reader do after? (Sign up, buy, share, learn)

**1B. Get Keyword Data (if SemRush API available)**

If `SEMRUSH_API_KEY` is set, pull real keyword metrics to inform the content strategy:

```bash
# Get keyword data for the target keyword
curl -s "https://api.semrush.com/?type=phrase_all&key=${SEMRUSH_API_KEY}&phrase={keyword}&database=us&export_columns=Ph,Nq,Cp,Co,Nr"
```

The response is semicolon-delimited with columns:
- **Ph** - Keyword phrase
- **Nq** - Monthly search volume (use this to gauge content depth: higher volume = more comprehensive article)
- **Cp** - CPC in dollars (high CPC signals strong commercial intent - emphasize CTAs and product mentions)
- **Co** - Competition index 0-1 (high competition means you need stronger E-E-A-T signals)
- **Nr** - Number of organic results (more results = more competitive SERP)

Use these insights to:
- **Calibrate word count:** Keywords with volume >5,000 typically need 2,500+ word articles
- **Adjust commercial angle:** CPC > $5 means readers have buying intent - include product recommendations, comparisons, or pricing info
- **Identify difficulty:** Competition > 0.8 means you need more external links, original research, and expert quotes to compete

**1C. Analyze the SERP (if tools available)**
Use WebSearch to check what currently ranks:
- What content type dominates? (Listicle, how-to, guide, comparison)
- What's the average word count of top 5?
- What topics do all top results cover?
- What's missing from existing content?

**1D. Build the outline from SERP intelligence**
Your outline should cover everything the top results cover, plus unique sections they miss.

### Step 2: Create the Outline

Build a detailed outline before writing. Every blog post follows this master structure:

```markdown
# [H1: Title - includes primary keyword, compelling, 50-60 chars for title tag]

Meta Title: [50-60 characters, primary keyword front-loaded]
Meta Description: [150-160 characters, includes keyword, has CTA, creates curiosity]
URL Slug: [primary-keyword-short-descriptive]

## Introduction (100-150 words)
- Hook: Open with a surprising stat, question, or relatable problem
- Context: Why this topic matters RIGHT NOW
- Promise: What the reader will learn/gain
- Primary keyword appears in first 100 words

## [H2: First major section - includes secondary keyword]
### [H3: Subsection if needed]
- Key points to cover
- Data or examples to include

## [H2: Second major section]
### [H3: Subsection]
...

## [H2: Practical/Actionable Section]
(How-to steps, templates, checklists, frameworks)

## [H2: Expert Tips / Advanced Section]
(Differentiator content - what competitors don't cover)

## [H2: Common Mistakes / What to Avoid]
(Addresses "People Also Ask" questions)

## [H2: FAQ]
### [H3: Question 1?]
Answer (2-4 sentences, targets featured snippet)
### [H3: Question 2?]
...

## Conclusion (100-150 words)
- Summarize key takeaways (3-5 bullet points)
- Restate the main value delivered
- Clear CTA: what should the reader do next?

## Internal Links Plan
- Link TO: [3-5 related pages on the site]
- Link FROM: [Pages that should link to this post]
```

### Step 3: Write the Content

Follow these writing rules strictly:

#### Title Tag Formula (50-60 characters)

Choose the best pattern for the intent:

| Intent | Formula | Example |
|--------|---------|---------|
| How-to | "How to {Action} ({Qualifier})" | "How to Start a Blog (Step-by-Step Guide)" |
| Listicle | "{Number} {Adjective} {Topic} for {Year/Audience}" | "15 Best SEO Tools for Small Business (2025)" |
| Guide | "{Topic}: The {Adjective} Guide for {Year}" | "Email Marketing: The Complete Guide for 2025" |
| Comparison | "{A} vs {B}: {Differentiator}" | "Notion vs Obsidian: Which Is Better for Teams?" |
| Question | "{Question}? {Promise}" | "Is SEO Dead? What the Data Actually Shows" |

**Title rules:**
- Primary keyword within first 30 characters
- Add a power word: Ultimate, Complete, Proven, Essential, Definitive
- Include year if the topic is time-sensitive
- Use numbers for listicles (odd numbers outperform: 7, 9, 11, 13)
- Never exceed 60 characters (Google truncates at ~580px)

#### Meta Description Formula (150-160 characters)

```
{What the article covers} + {Unique value prop} + {CTA or curiosity hook}
```

Examples:
- "Learn how to start a blog in 2025 with our step-by-step guide. Covers hosting, design, content, and monetization. Free checklist included."
- "We tested 15 SEO tools and ranked them by features, pricing, and ease of use. See which tool is best for your budget and goals."

**Meta description rules:**
- Include primary keyword naturally
- Include a CTA or curiosity element
- Use active voice
- Mention a specific deliverable (checklist, template, comparison, steps)
- Stay between 150-160 characters

#### Writing Style Rules

**Readability:**
- Paragraphs: 2-4 sentences max
- Sentences: 15-20 words average
- Use short sentences for emphasis. Like this.
- Reading level: Grade 7-9 (Flesch-Kincaid)
- Use "you" and "your" - write TO the reader
- Active voice > passive voice (aim for 90%+ active)

**Structure & Scannability:**
- H2 every 200-300 words
- H3 for subsections within H2s
- Bullet points for lists of 3+ items
- Numbered lists for sequential steps
- Bold key terms and takeaways
- Pull quotes or callout boxes for key insights
- Tables for comparisons (Google loves tables for featured snippets)

**SEO Integration (natural, not forced):**
- Primary keyword in: H1, first 100 words, 1-2 H2s, conclusion, alt text
- Primary keyword density: 0.5-1.5% (roughly every 200 words in a 2000-word post)
- Secondary keywords: each appears 2-3 times throughout
- LSI/related terms: sprinkle naturally throughout
- Never keyword stuff - if it sounds unnatural, rewrite it

**E-E-A-T Signals:**
- **Experience:** Include first-hand observations, "In my experience...", "When I tested..."
- **Expertise:** Reference specific methodologies, use precise terminology, show deep knowledge
- **Authoritativeness:** Cite authoritative sources (studies, official docs, industry leaders)
- **Trustworthiness:** Acknowledge limitations, present balanced views, link to sources

#### Content Depth Targets

| Article Type | Target Words | Sections (H2) | Images | Internal Links | External Links |
|-------------|-------------|----------------|--------|---------------|---------------|
| How-to Guide | 2000-3000 | 6-10 | 5-10 | 5-8 | 3-5 |
| Listicle | 2500-4000 | 1 per item + intro/conclusion | 1 per item | 5-10 | 3-5 |
| Ultimate Guide | 3000-5000 | 8-15 | 8-15 | 8-12 | 5-8 |
| Comparison | 1500-2500 | 5-8 | 3-5 | 3-5 | 2-4 |
| Opinion/Thought | 1000-1500 | 4-6 | 2-3 | 3-5 | 2-3 |
| News/Update | 800-1200 | 3-5 | 1-3 | 3-5 | 3-5 |

### Step 4: Optimize for Featured Snippets

Target featured snippets with these patterns:

**Paragraph snippet (definition/what is):**
```markdown
## What Is {Topic}?

{Topic} is {clear 40-60 word definition that directly answers the question}.
{Additional context in 1-2 more sentences}.
```

**List snippet (how-to/best of):**
```markdown
## How to {Action}

1. **{Step 1 title}** - Brief description
2. **{Step 2 title}** - Brief description
3. **{Step 3 title}** - Brief description
...
```

**Table snippet (comparison/data):**
```markdown
## {Comparison Topic}

| {Column 1} | {Column 2} | {Column 3} |
|------------|------------|------------|
| {Data} | {Data} | {Data} |
```

### Step 5: Add Supporting Elements

**Image suggestions:**
For each major section, suggest an image:
```markdown
[IMAGE: {Description of what the image should show}]
Alt text: "{Descriptive alt text with keyword where natural}"
```

**Image types to suggest:**
- Hero image (featured image for social sharing)
- Screenshots (for tutorials)
- Comparison tables (as images for Pinterest)
- Infographics (for key data points)
- Process diagrams (for step-by-step content)
- Charts/graphs (for data-driven claims)

**Sourcing Featured Images from Unsplash (if UNSPLASH_CLIENT_ID available):**

Use the Unsplash API to find high-quality, royalty-free featured images for the blog post:

```bash
# Search Unsplash for a relevant featured image
curl -s "https://api.unsplash.com/search/photos?query={topic}&per_page=5&orientation=landscape" \
  -H "Authorization: Client-ID ${UNSPLASH_CLIENT_ID}"
```

**Parsing the response:**

The JSON response contains a `results` array. For each photo, extract:

```bash
# Parse with jq to get image URLs, photographer info, and download links
curl -s "https://api.unsplash.com/search/photos?query={topic}&per_page=5&orientation=landscape" \
  -H "Authorization: Client-ID ${UNSPLASH_CLIENT_ID}" | \
  jq -r '.results[] | {
    id: .id,
    description: .description,
    image_url: .urls.regular,
    full_url: .urls.full,
    download_link: .links.download,
    photographer_name: .user.name,
    photographer_url: .user.links.html,
    unsplash_url: .links.html
  }'
```

Key fields from the response:
- **`.urls.regular`** - Optimized image (1080px wide, good for blog featured images)
- **`.urls.full`** - Full resolution image
- **`.urls.small`** - Thumbnail (400px wide, good for social sharing previews)
- **`.links.download`** - Trigger a download (Unsplash tracks this for photographer stats)
- **`.user.name`** - Photographer's name (required for attribution)
- **`.user.links.html`** - Photographer's Unsplash profile URL

**Unsplash attribution requirement:**

Unsplash requires attribution whenever you use a photo. Include this in the blog post:

```markdown
Photo by [Photographer Name](https://unsplash.com/@username?utm_source=your_app&utm_medium=referral) on [Unsplash](https://unsplash.com/?utm_source=your_app&utm_medium=referral)
```

Place the attribution either:
- In the image caption directly below the featured image
- In an image credits section at the bottom of the post
- In the alt text or title attribute of the image tag

**Tip:** Search with specific, descriptive queries rather than broad terms. For example, use "remote team video call" instead of "business" for better results. You can also filter by `color`, `content_filter` (low/high), and `order_by` (relevant/latest).

**Internal link placement:**
- Contextual links within body paragraphs (most valuable)
- "Related reading" callout boxes between sections
- "Further reading" section at the end
- Anchor text should be descriptive, not "click here"

**External link rules:**
- Link to authoritative sources (studies, official docs, .edu, .gov)
- Open external links in new tab
- No-follow affiliate links and sponsored content
- Cite statistics with linked sources

### Step 6: FAQ Section

Every blog post should end with a FAQ section targeting "People Also Ask":

```markdown
## Frequently Asked Questions

### {Question matching PAA or long-tail keyword}?

{Direct answer in 2-4 sentences. Front-load the answer.
Provide additional context after the direct answer.
This format optimizes for both featured snippets and FAQ rich results.}

### {Second question}?

{Answer}
```

**FAQ rules:**
- 4-6 questions
- Questions should use natural language (how, what, why, when, can, does)
- Answer the question in the first sentence
- Keep each answer under 100 words
- Include schema markup (see schema-markup skill)

### Step 7: Final Quality Check

Before delivering the post, verify:

**SEO Checklist:**
- [ ] Title tag: 50-60 characters, keyword front-loaded
- [ ] Meta description: 150-160 characters, includes keyword, has CTA
- [ ] URL slug: Short, includes keyword, hyphenated
- [ ] H1: One per page, includes primary keyword
- [ ] H2s: Include secondary keywords where natural
- [ ] Primary keyword in first 100 words
- [ ] Keyword density: 0.5-1.5%
- [ ] Internal links: 5+ contextual links
- [ ] External links: 3+ authoritative sources
- [ ] Images: Alt text on all, keyword in at least one
- [ ] FAQ section with 4-6 questions
- [ ] Word count meets target for content type
- [ ] No duplicate content or thin sections

**Readability Checklist:**
- [ ] Average paragraph: 2-4 sentences
- [ ] Average sentence: under 20 words
- [ ] Grade level: 7-9
- [ ] Active voice: 90%+
- [ ] Power words in subheadings
- [ ] Bullet points or numbered lists every 300 words
- [ ] Bold text highlights key points

**E-E-A-T Checklist:**
- [ ] Author byline with credentials suggested
- [ ] Sources cited and linked
- [ ] First-hand experience or expertise demonstrated
- [ ] Balanced perspective (pros and cons, not just hype)
- [ ] Date published and "last updated" date included
- [ ] Factual accuracy verified (no made-up statistics)

## Output Format

Deliver the blog post in this format:

```markdown
---
title: "{Meta title - 50-60 chars}"
description: "{Meta description - 150-160 chars}"
slug: "{url-slug}"
keywords: ["{primary}", "{secondary1}", "{secondary2}"]
date: "{YYYY-MM-DD}"
author: "{Author name}"
---

# {H1 Headline}

{Full article content with all formatting, links, and image placeholders}
```

After the article, provide:
1. **SEO metadata summary** (title, description, slug, word count)
2. **Internal linking recommendations** (which pages to link to/from)
3. **Schema markup** (Article or BlogPosting JSON-LD)
4. **Social sharing** (suggested OG title, description, and image concept)
5. **Content promotion ideas** (2-3 distribution channels and angles)

## Important Notes

- Never fabricate statistics. If citing a number, include the source or note "[Source needed]".
- Write for humans first, search engines second. If an SEO tactic makes the content worse for readers, skip it.
- Every section must provide value. No filler paragraphs. If a section doesn't teach, convince, or entertain, cut it.
- Match the user's brand voice if they specify one. Ask if not clear.
- If the topic is YMYL (health, finance, legal), be extra careful with claims and heavily cite authoritative sources.
