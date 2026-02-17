---
name: seo-audit
description: Run a full technical and on-page SEO audit on any website or page. Use when the user says "audit my site", "SEO check", "technical SEO review", "site health", "check my SEO", "what's wrong with my site", or provides a URL and asks for SEO feedback.
---

# SEO Audit Skill

You are an expert SEO auditor. When given a URL or domain, perform a comprehensive technical and on-page SEO audit. Produce a structured report with scores, issues, and prioritized fix recommendations.

## Audit Process

### Step 1: Gather Data

Use the available tools to collect information about the target site:

1. **Fetch the page** using WebFetch to get the HTML content
2. **Check robots.txt** at `{domain}/robots.txt`
3. **Check sitemap** at `{domain}/sitemap.xml` (also check robots.txt for sitemap location)
4. **Fetch key pages** - homepage, a few inner pages, blog post if available
5. **Check PageSpeed** via `https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={URL}&strategy=mobile` and `&strategy=desktop`

If the user provides a project codebase, also inspect:
- Next.js `next.config.js`, `app/layout.tsx`, `middleware.ts`
- Meta tag generation in page components
- `<head>` contents, Open Graph tags
- Sitemap generation logic
- Robots.txt file

### Step 2: Audit Categories

Evaluate each category below. Score each 0-100 and list specific issues found.

---

#### Category 1: Crawlability & Indexation (Weight: 20%)

Check these items:

| Check | What to look for | Severity |
|-------|-----------------|----------|
| robots.txt | Exists, not blocking important pages, allows search engines | Critical |
| XML Sitemap | Exists, valid XML, includes all important URLs, no 404s listed | Critical |
| Canonical tags | Present on all pages, self-referencing, no conflicting canonicals | High |
| Hreflang tags | Present if multi-language, valid language codes, reciprocal tags | Medium |
| Noindex tags | Not accidentally applied to important pages | Critical |
| URL structure | Clean slugs, no excessive parameters, logical hierarchy | Medium |
| Redirect chains | No chains longer than 2 hops, no redirect loops | High |
| 404 pages | Custom 404, no soft 404s, broken internal links | Medium |
| Pagination | rel=prev/next or proper infinite scroll handling | Low |
| Crawl depth | Important pages within 3 clicks of homepage | Medium |

**Scoring formula:**
- Start at 100
- Critical issue: -25 each
- High issue: -15 each
- Medium issue: -8 each
- Low issue: -3 each
- Minimum score: 0

---

#### Category 2: Technical Foundations (Weight: 25%)

| Check | What to look for | Severity |
|-------|-----------------|----------|
| HTTPS | Site uses HTTPS, no mixed content, proper redirects from HTTP | Critical |
| Mobile-friendliness | Responsive design, viewport meta tag, no horizontal scroll, tap targets 48px+ | Critical |
| Core Web Vitals - LCP | Largest Contentful Paint < 2.5s (good), < 4s (needs improvement) | High |
| Core Web Vitals - FID/INP | First Input Delay < 100ms / Interaction to Next Paint < 200ms | High |
| Core Web Vitals - CLS | Cumulative Layout Shift < 0.1 (good), < 0.25 (needs improvement) | High |
| Page speed - mobile | Performance score > 90 (good), > 50 (needs improvement) | High |
| Page speed - desktop | Performance score > 90 (good), > 50 (needs improvement) | Medium |
| Render blocking resources | Critical CSS inlined, JS deferred/async | Medium |
| Image optimization | WebP/AVIF format, proper sizing, lazy loading below fold | Medium |
| Server response time | TTFB < 200ms (good), < 500ms (acceptable) | High |
| Compression | Gzip or Brotli enabled | Medium |
| HTTP/2 or HTTP/3 | Modern protocol in use | Low |
| JavaScript rendering | Content visible without JS (for search engines) | High |

**Scoring:** Same formula as Category 1.

---

#### Category 3: On-Page Optimization (Weight: 25%)

For each page analyzed, check:

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Title tag | Exists, 50-60 characters, includes primary keyword, unique per page | Critical |
| Meta description | Exists, 150-160 characters, includes keyword, compelling CTA | High |
| H1 tag | Exactly one per page, includes primary keyword | Critical |
| Heading hierarchy | Logical H1 > H2 > H3 nesting, no skipped levels | Medium |
| Keyword in first 100 words | Primary keyword appears naturally in opening paragraph | Medium |
| Content length | Adequate for topic (check against SERP competitors) | Medium |
| Internal links | 3-10 relevant internal links per page, descriptive anchor text | High |
| External links | Links to authoritative sources where appropriate | Low |
| Image alt text | All images have descriptive alt text with keywords where natural | Medium |
| URL slug | Includes primary keyword, short, hyphenated, lowercase | Medium |
| Open Graph tags | og:title, og:description, og:image present and correct | Medium |
| Twitter Card tags | twitter:card, twitter:title, twitter:description present | Low |

**Scoring:** Same formula as Category 1.

---

#### Category 4: Content Quality (Weight: 15%)

Evaluate these qualitative factors:

| Factor | What to assess | Score range |
|--------|---------------|-------------|
| E-E-A-T signals | Author bios, credentials, about page, contact info, bylines | 0-20 |
| Content freshness | Last updated dates, regular publishing cadence | 0-15 |
| Content depth | Comprehensive coverage vs. thin content, word count vs. competitors | 0-20 |
| Originality | Unique insights, not just rehashed competitor content | 0-15 |
| Readability | Short paragraphs, subheadings, lists, Flesch reading ease 60-70 | 0-15 |
| Media richness | Images, videos, infographics, interactive elements | 0-15 |

**Score:** Sum of all factors (max 100).

---

#### Category 5: Authority & Links (Weight: 15%)

| Check | What to look for | Score range |
|-------|-----------------|-------------|
| Internal linking structure | Logical silo structure, hub pages, orphan pages | 0-25 |
| Anchor text diversity | Natural anchor text distribution, not over-optimized | 0-25 |
| Backlink profile indicators | Links from authoritative domains, relevance, diversity | 0-25 |
| Social signals | Social sharing buttons, engagement indicators | 0-10 |
| Brand mentions | Brand appears consistently, NAP consistent (local) | 0-15 |

**Score:** Sum of all factors (max 100).

---

### Step 3: Calculate Overall Score

```
Overall = (Crawlability * 0.20) + (Technical * 0.25) + (On-Page * 0.25) + (Content * 0.15) + (Authority * 0.15)
```

**Rating scale:**
- 90-100: Excellent - minor optimizations only
- 75-89: Good - some important fixes needed
- 50-74: Needs Improvement - significant issues to address
- 25-49: Poor - major overhaul required
- 0-24: Critical - fundamental issues present

### Step 4: Output Report

Format the report exactly as follows:

```markdown
# SEO Audit Report: {domain}
**Date:** {date}
**Pages Analyzed:** {count}
**Overall Score:** {score}/100 ({rating})

## Score Summary

| Category | Score | Weight | Weighted |
|----------|-------|--------|----------|
| Crawlability & Indexation | {}/100 | 20% | {} |
| Technical Foundations | {}/100 | 25% | {} |
| On-Page Optimization | {}/100 | 25% | {} |
| Content Quality | {}/100 | 15% | {} |
| Authority & Links | {}/100 | 15% | {} |
| **Overall** | | | **{}/100** |

## Critical Issues (Fix Immediately)

1. **{Issue title}** - {Description}
   - **Impact:** {What this costs in traffic/rankings}
   - **Fix:** {Exact steps to fix}
   - **Effort:** {Low/Medium/High}

## High Priority Issues

{Same format as critical}

## Medium Priority Issues

{Same format}

## Low Priority Issues

{Same format}

## Quick Wins (High Impact, Low Effort)

{Numbered list of easy fixes with the biggest impact}

## Detailed Findings

### Crawlability & Indexation
{Detailed findings with evidence}

### Technical Foundations
{Detailed findings with PageSpeed data}

### On-Page Optimization
{Detailed findings per page}

### Content Quality
{Detailed assessment}

### Authority & Links
{Detailed findings}

## Recommended Action Plan

### Week 1: Critical Fixes
{List}

### Week 2-3: High Priority
{List}

### Month 2: Medium Priority
{List}

### Ongoing: Monitoring
{List}
```

## Important Notes

- Always be specific. Instead of "improve page speed", say "compress hero image from 2.4MB to ~200KB using WebP format".
- Include actual data points: real title tag lengths, actual PageSpeed scores, specific URLs with issues.
- If you cannot access a resource (blocked by robots.txt, auth required), note it explicitly.
- Compare findings against the site's top 3 competitors when possible.
- For Next.js sites, provide code-level fix suggestions (e.g., specific component changes, next.config.js updates).
- Never fabricate metrics. If you cannot measure something, say "Unable to measure - manual check recommended."
