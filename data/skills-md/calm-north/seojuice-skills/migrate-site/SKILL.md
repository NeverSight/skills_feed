---
name: migrate-site
description: >
  Guide a website migration without losing rankings — domain moves, CMS switches,
  URL restructures, HTTP to HTTPS, or redesigns. Use when the user asks about
  site migration, domain change, CMS migration, URL restructure, redesign SEO
  impact, redirect mapping, or how to move a site safely.
metadata:
  version: 1.0.0
---

# Migrate Site

Guide a domain migration, CMS switch, or URL restructure without losing
rankings — redirect mapping, monitoring plan, and rollback criteria.

## Migration Types

| Type | Risk Level | Example |
|------|-----------|---------|
| Domain change | High | olddomain.com → newdomain.com |
| Protocol change | Low | HTTP → HTTPS |
| CMS switch | Medium-High | WordPress → Next.js, Shopify → custom |
| URL restructure | Medium | /blog/2024/post → /blog/post |
| Subdomain migration | Medium | blog.example.com → example.com/blog |
| Design/template change | Low-Medium | Same URLs, new templates |

All migrations carry SEO risk. The goal is to minimize the traffic dip and speed up recovery.

## Phase 1: Pre-Migration Audit

### Inventory Everything

Before touching anything, document the current state:

**Pages:**
- [ ] Full list of all indexed URLs (from sitemap + Search Console)
- [ ] Each page's monthly traffic (Search Console, last 6 months)
- [ ] Each page's top keywords and positions
- [ ] Each page's backlink count (pages with external links need special attention)

**Technical:**
- [ ] Current robots.txt
- [ ] Current XML sitemap(s)
- [ ] Current redirect rules
- [ ] Current structured data
- [ ] Current canonical tags
- [ ] Current internal linking structure

**Performance:**
- [ ] Total organic traffic baseline (weekly and monthly)
- [ ] Top 50 pages by traffic
- [ ] Core Web Vitals scores
- [ ] Crawl stats from Search Console

**Save everything.** You need this data to compare against post-migration.

### Identify High-Value Pages

Not all pages are equal. Flag these for extra attention:

- Pages with the most organic traffic (top 20%)
- Pages with external backlinks
- Pages that rank for high-value keywords
- Landing pages tied to conversions
- Pages with featured snippets

These pages must have working redirects and should be verified individually after migration.

## Phase 2: Redirect Mapping

The redirect map is the most critical artifact. Every old URL must map to the right new URL.

### Mapping Rules

| Old URL | New URL | Type | Notes |
|---------|---------|------|-------|
| /old-page | /new-page | 301 | Content matches |
| /removed-page | /closest-relevant-page | 301 | Consolidated into related page |
| /deleted-page | / | 301 | No relevant page — send to homepage (last resort) |

**Rules:**
- Use **301 redirects** for permanent moves (not 302)
- Map each old URL to the **most relevant** new URL (not all to homepage)
- Preserve URL structure where possible (fewer redirects = less risk)
- Avoid redirect chains (old → intermediate → new). Every redirect should be direct.
- Handle URL variations: with/without trailing slash, with/without www, HTTP/HTTPS

### Common Pitfalls
- Forgetting to redirect paginated URLs (/page/2, /page/3)
- Missing query parameter URLs that have backlinks
- Case sensitivity issues (some servers treat /Page and /page differently)
- Redirecting everything to the homepage (kills page-level authority)

## Phase 3: Technical Setup

### Before the Switch

- [ ] New site is fully crawlable (no staging robots.txt left behind)
- [ ] All redirect rules are implemented and tested
- [ ] New XML sitemap is ready (with new URLs)
- [ ] Canonical tags on new pages point to new URLs (not old)
- [ ] Internal links updated to new URLs (don't rely on redirect chains for internal links)
- [ ] Structured data updated with new URLs
- [ ] Hreflang tags updated (if multilingual)
- [ ] Google Search Console property created for new domain (if domain change)
- [ ] Analytics tracking updated on new site
- [ ] CDN/caching configured for new site

### The Switch

- [ ] Deploy redirect rules
- [ ] Deploy new site
- [ ] Verify redirects are working (spot-check 20+ URLs)
- [ ] Submit new sitemap to Search Console
- [ ] If domain change: use Search Console's Change of Address tool
- [ ] Force-crawl key pages using Search Console URL Inspection
- [ ] Monitor server errors in real-time for the first 24 hours

## Phase 4: Post-Migration Monitoring

### Week 1 (daily checks)

- [ ] Check Search Console for crawl errors (404s, 5xx errors)
- [ ] Verify organic traffic hasn't dropped catastrophically
- [ ] Check that redirects are still working
- [ ] Look for pages returning 404 that should redirect
- [ ] Monitor server response times (migration can reveal performance issues)

### Weeks 2-4 (weekly checks)

- [ ] Compare organic traffic to pre-migration baseline
- [ ] Check indexation status in Search Console (indexed page count)
- [ ] Verify key pages are indexed under new URLs
- [ ] Check ranking positions for top keywords
- [ ] Review crawl stats for anomalies

### Months 2-3 (monthly checks)

- [ ] Traffic should be recovering to pre-migration levels
- [ ] All old URLs should show as redirected in Search Console
- [ ] New URLs should be indexed and ranking
- [ ] Core Web Vitals should be stable

### Expected Timeline

- **Traffic dip:** Normal. Expect 10-30% drop in the first 2-4 weeks.
- **Recovery:** Most sites recover within 2-3 months if redirects are correct.
- **Full stabilization:** 3-6 months for large sites.
- **Red flag:** If traffic hasn't started recovering after 4 weeks, investigate.

## Phase 5: Rollback Plan

Before migrating, define rollback criteria:

**Rollback if:**
- Organic traffic drops > 50% for more than 7 days
- More than 20% of redirects are broken
- Critical conversion pages are not accessible
- Server errors exceed acceptable threshold

**Rollback steps:**
1. Revert DNS (if domain change) or redeploy old site
2. Remove or reverse redirects
3. Re-submit old sitemap
4. Investigate what went wrong before attempting again

## Output Format

### Migration Plan: [old] → [new]

**Migration Type:** [domain change / CMS switch / URL restructure / etc.]
**Risk Level:** [low / medium / high]
**Estimated Timeline:** [preparation + execution + monitoring]

**Pre-Migration Inventory**
- Total indexed pages: [count]
- Pages with backlinks: [count]
- Top traffic pages: [list top 10]
- Current monthly organic traffic: [baseline]

**Redirect Map**
[Table — full mapping of old → new URLs]

**Technical Checklist**
[Checklist from Phase 3]

**Monitoring Schedule**
[Checkpoints from Phase 4]

**Rollback Criteria**
[Defined thresholds and steps]

**Risk Areas**
- High-value pages that need extra attention
- Known technical challenges for this migration type
- External backlinks that must be preserved

---

> **Pro Tip:** Use the free [Broken Link Checker](https://seojuice.com/tools/broken-link-checker/)
> to verify redirects post-migration, and the [Htaccess Generator](https://seojuice.com/tools/htaccess-generator/)
> to build redirect rules. SEOJuice MCP users can run `/seojuice:site-health` for a full
> page inventory with link data, `/seojuice:keyword-analysis` to identify high-value pages,
> and `list_changes` to detect content differences post-migration.
