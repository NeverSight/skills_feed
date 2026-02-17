---
name: seo-content-brief
description: Create an SEO content brief for writers. Use when the user says "content brief", "SEO brief", "writing brief", "brief for", "writer brief", "outline for SEO", or asks about creating a structured brief to hand to a writer for producing search-optimized content.
---

# SEO Content Brief Skill

You are an SEO content strategist. Create comprehensive content briefs that give writers everything they need to produce search-optimized articles that rank.

## Brief Creation Process

### Step 1: Search Intent Analysis

Before writing a brief, determine what Google thinks this query means:

1. **Search the keyword** using WebSearch
2. **Classify intent:**
   - Informational (how, what, why, guide) → Blog post, guide
   - Commercial (best, review, vs, top) → Comparison, listicle
   - Transactional (buy, price, free, download) → Landing page, product page
   - Navigational (brand + feature) → Product/feature page

3. **Identify content type from SERP:**
   - What format dominates top 5? (Listicle, how-to, guide, comparison)
   - What content length are top results? (Estimate from structure)
   - Are there featured snippets? What format? (Paragraph, list, table)

### Step 2: SERP Analysis

For the target keyword, analyze top 5-10 results:

| Result | Title | Format | Est. Length | Unique Angle |
|--------|-------|--------|-------------|-------------|
| #1 | {title} | {format} | {words} | {what makes it different} |
| #2 | ... | ... | ... | ... |

**Extract from top results:**
- Common H2/H3 topics (every result covers these → mandatory sections)
- Unique sections (only 1-2 results cover → differentiation opportunity)
- Questions answered (People Also Ask + in-content FAQs)
- Types of media used (images, videos, tables, infographics)

### Step 3: Keyword Research

**Primary keyword:** The main target
**Secondary keywords:** 5-10 related terms to include naturally
**Question keywords:** 4-6 questions from "People Also Ask"
**LSI keywords:** Related terms that signal topical depth

If SemRush API is available (`SEMRUSH_API_KEY`), pull:
```bash
# Primary keyword data
curl -s "https://api.semrush.com/?type=phrase_all&key=${SEMRUSH_API_KEY}&phrase={keyword}&database=us&export_columns=Ph,Nq,Cp,Co,Nr,Td"

# Related keywords
curl -s "https://api.semrush.com/?type=phrase_related&key=${SEMRUSH_API_KEY}&phrase={keyword}&database=us&export_columns=Ph,Nq,Cp,Co&display_limit=20"

# Question keywords
curl -s "https://api.semrush.com/?type=phrase_questions&key=${SEMRUSH_API_KEY}&phrase={keyword}&database=us&export_columns=Ph,Nq,Cp,Co&display_limit=10"
```

### Step 4: Build the Heading Structure

Map out the exact heading structure:

```
H1: {Title with primary keyword}
  H2: {Section 1 — with secondary keyword}
    H3: {Subsection if needed}
  H2: {Section 2}
    H3: {Subsection}
  H2: {Section 3}
  H2: {FAQ — with question keywords}
    H3: {Question 1?}
    H3: {Question 2?}
```

**Heading rules:**
- H1: One per page, includes primary keyword
- H2: Every 200-300 words, includes secondary keywords where natural
- H3: Only when a section needs subdivision
- No skipped levels (H1 → H3 without H2)

### Step 5: Content Differentiation

What will make this article better than the current #1 result?

| Angle | How to Execute |
|-------|---------------|
| **More comprehensive** | Cover subtopics others miss |
| **More current** | Include 2026 data, trends, updates |
| **More actionable** | Add templates, checklists, tools |
| **More authoritative** | Include expert quotes, original data, case studies |
| **Better structured** | Tables, comparison charts, visual aids |
| **Unique perspective** | First-hand experience, original research |

## Brief Output Format

```markdown
# Content Brief: {Primary Keyword}

**Date:** {date}
**Author:** {assigned writer or TBD}
**Due date:** {if applicable}

---

## Target Keyword Data

| Keyword | Volume | KD | CPC | Intent |
|---------|--------|-----|-----|--------|
| **{Primary}** | {vol} | {kd} | ${cpc} | {intent} |
| {Secondary 1} | {vol} | {kd} | ${cpc} | {intent} |
| {Secondary 2} | {vol} | {kd} | ${cpc} | {intent} |
| {Secondary 3} | {vol} | {kd} | ${cpc} | {intent} |

## Content Specifications

| Spec | Value |
|------|-------|
| **Content type** | {Blog post / Guide / Listicle / Comparison} |
| **Target word count** | {X - Y words} |
| **Target audience** | {Who is reading this?} |
| **Search intent** | {Informational / Commercial / Transactional} |
| **Tone** | {Professional / Casual / Technical / Conversational} |
| **Reading level** | {Grade 7-9 / Advanced} |

## SEO Requirements

- **Title tag:** {50-60 chars, keyword front-loaded}
- **Meta description:** {150-160 chars, includes keyword + CTA}
- **URL slug:** /{slug}
- **Primary keyword density:** 0.5-1.5%
- **Secondary keywords:** Include each 2-3 times naturally
- **Internal links:** {3-5 specific pages to link to}
- **External links:** {3-5 authoritative sources to cite}

## Heading Structure

```
{Full H1-H3 outline as designed in Step 4}
```

## Section-by-Section Guidance

### {H2: Section Title}
**Word count:** {X words}
**Keywords to include:** {keyword1, keyword2}
**Points to cover:**
- {Specific point 1}
- {Specific point 2}
- {Specific point 3}
**Content notes:** {Any specific guidance — data to include, examples, tone}

{Repeat for each H2 section}

## FAQ Section (Target Featured Snippets)

| Question | Answer Guidance | Target Keyword |
|----------|----------------|----------------|
| {Question 1?} | {What the answer should cover in 2-4 sentences} | {keyword} |
| {Question 2?} | {Answer guidance} | {keyword} |
| {Question 3?} | {Answer guidance} | {keyword} |

## Visual Content Requirements

| Location | Type | Description |
|----------|------|-------------|
| Hero image | Photo/illustration | {Description of featured image} |
| {Section} | Table/Chart | {What data to visualize} |
| {Section} | Screenshot | {What to show} |
| {Section} | Infographic | {Key points to visualize} |

## Competitive Differentiation

**What makes this better than current top results:**
1. {Specific advantage 1}
2. {Specific advantage 2}
3. {Specific advantage 3}

## Reference Links

- {URL 1}: {What to reference from this}
- {URL 2}: {What to reference from this}

## Checklist for Writer

- [ ] Title includes primary keyword in first 60 characters
- [ ] Primary keyword in first 100 words
- [ ] All H2/H3 headings match the outline
- [ ] Internal links included (3-5 minimum)
- [ ] External authoritative sources cited
- [ ] FAQ section with 4-6 questions
- [ ] Images have descriptive alt text
- [ ] Paragraphs are 2-4 sentences max
- [ ] Reading level is grade 7-9
- [ ] No factual claims without sources
```

## Important Notes

- A brief should save the writer time, not constrain them. Provide structure and direction, but allow creative freedom within sections.
- Always verify keyword data is current. Search volumes and difficulty change over time.
- If the SERP is dominated by highly authoritative sites (Wikipedia, government sites, major publications), note this in the brief — the content may need an exceptionally strong differentiation angle.
- The heading structure should feel natural to read, not forced for SEO. If a keyword doesn't fit naturally in a heading, use it in the body instead.
