---
name: solo-seo-audit
description: SEO health check for any URL — analyzes meta tags, OG, JSON-LD, sitemap, robots.txt, SERP positions, and scores 0-100. Use when user says "check SEO", "audit this page", "SEO score", "check meta tags", or "SERP position". Do NOT use for generating landing content (use /landing-gen) or social media posts (use /content-gen).
license: MIT
metadata:
  author: fortunto2
  version: "1.1.1"
  openclaw:
    emoji: "📊"
allowed-tools: Read, Grep, Bash, Glob, Write, WebSearch, WebFetch, AskUserQuestion, mcp__solograph__web_search, mcp__solograph__project_info
argument-hint: "<url or project-name>"
---

# /seo-audit

SEO health check for any URL or project landing page. Fetches the page, analyzes meta tags, OG, JSON-LD, sitemap, robots.txt, checks SERP positions for target keywords, and outputs a scored report.

## MCP Tools (use if available)

- `web_search(query, engines, include_raw_content)` — SERP position check, competitor analysis
- `project_info(name)` — get project URL if auditing by project name

If MCP tools are not available, use Claude WebSearch/WebFetch as fallback.

## Steps

1. **Parse target** from `$ARGUMENTS`.
   - If URL (starts with `http`): use directly.
   - If project name: look up URL from project README, CLAUDE.md, or `docs/prd.md`.
   - If empty: ask via AskUserQuestion — "Which URL or project to audit?"

2. **Fetch the page** via WebFetch. Extract:
   - `<title>` tag (length check: 50-60 chars ideal)
   - `<meta name="description">` (length check: 150-160 chars ideal)
   - Open Graph tags: `og:title`, `og:description`, `og:image`, `og:url`, `og:type`
   - Twitter Card tags: `twitter:card`, `twitter:title`, `twitter:image`
   - JSON-LD structured data (`<script type="application/ld+json">`)
   - `<link rel="canonical">` — canonical URL
   - `<html lang="...">` — language tag
   - `<link rel="alternate" hreflang="...">` — i18n tags
   - Heading structure: H1 count (should be exactly 1), H2-H3 hierarchy

3. **Check infrastructure files:**
   - Fetch `{origin}/sitemap.xml` — exists? Valid XML? Page count?
   - Fetch `{origin}/robots.txt` — exists? Disallow rules? Sitemap reference?
   - Fetch `{origin}/favicon.ico` — exists?

4. **Forced reasoning — assess before scoring:**
   Write out before proceeding:
   - **What's present:** [list of found elements]
   - **What's missing:** [list of absent elements]
   - **Critical issues:** [anything that blocks indexing or sharing]

5. **SERP position check** — for 3-5 keywords:
   - Extract keywords from page title + meta description + H1.
   - For each keyword, search via MCP `web_search(query="{keyword}")` or WebSearch.
   - Record: position of target URL in results (1-10, or "not found").
   - Record: top 3 competitors for each keyword.

6. **Score calculation** (0-100):

   | Check | Max Points | Criteria |
   |-------|-----------|----------|
   | Title tag | 10 | Exists, 50-60 chars, contains primary keyword |
   | Meta description | 10 | Exists, 150-160 chars, compelling |
   | OG tags | 10 | og:title, og:description, og:image all present |
   | JSON-LD | 10 | Valid structured data present |
   | Canonical | 5 | Present and correct |
   | Sitemap | 10 | Exists, valid, referenced in robots.txt |
   | Robots.txt | 5 | Exists, no overly broad Disallow |
   | H1 structure | 5 | Exactly one H1, descriptive |
   | HTTPS | 5 | Site uses HTTPS |
   | Mobile meta | 5 | Viewport tag present |
   | Language | 5 | `lang` attribute on `<html>` |
   | Favicon | 5 | Exists |
   | SERP presence | 15 | Found in top 10 for target keywords |

7. **Write report** to `docs/seo-audit.md` (in project context) or print to console:

   ```markdown
   # SEO Audit: {URL}

   **Date:** {YYYY-MM-DD}
   **Score:** {N}/100

   ## Summary
   {2-3 sentence overview of SEO health}

   ## Checks

   | Check | Status | Score | Details |
   |-------|--------|-------|---------|
   | Title | pass/fail | X/10 | "{actual title}" (N chars) |
   | ... | ... | ... | ... |

   ## SERP Positions

   | Keyword | Position | Top Competitors |
   |---------|----------|----------------|
   | {kw} | #N or N/A | competitor1, competitor2, competitor3 |

   ## Critical Issues
   - {issue with fix recommendation}

   ## Recommendations (Top 3)
   1. {highest impact fix}
   2. {second priority}
   3. {third priority}
   ```

8. **Output summary** — print score and top 3 recommendations.

## Notes

- Score is relative — 80+ is good for a landing page, 90+ is excellent
- SERP checks are approximations (not real-time ranking data)
- Run periodically after content changes or before launch

## Common Issues

### Page fetch fails
**Cause:** URL is behind authentication, CORS, or returns non-HTML.
**Fix:** Ensure the URL is publicly accessible. For SPAs, check if content is server-rendered.

### SERP positions show "not found"
**Cause:** Site is new or not indexed by search engines.
**Fix:** This is expected for new sites. Submit sitemap to Google Search Console and re-audit in 2-4 weeks.

### Low score despite good content
**Cause:** Missing infrastructure files (sitemap.xml, robots.txt, JSON-LD).
**Fix:** These are the highest-impact fixes. Generate sitemap, add robots.txt with sitemap reference, and add JSON-LD structured data.
