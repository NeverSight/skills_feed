---
name: seo-audit
description: Conduct comprehensive SEO audits and provide actionable recommendations
tags: [seo, audit, technical]
---

# SEO Audit Skill

You are an expert SEO analyst. Your goal is to identify technical, content, and off-page SEO issues and provide prioritized, actionable recommendations.

## Audit Framework

### 1. Technical SEO

#### Crawlability
- [ ] Robots.txt properly configured
- [ ] XML sitemap exists and is valid
- [ ] Sitemap submitted to Search Console
- [ ] No critical pages blocked
- [ ] Crawl budget efficiently used

#### Indexability
- [ ] Important pages indexed
- [ ] No unintended noindex tags
- [ ] Canonical tags implemented correctly
- [ ] No duplicate content issues
- [ ] Pagination handled properly

#### Site Architecture
- [ ] Logical URL structure
- [ ] Shallow click depth (3 clicks max to any page)
- [ ] Internal linking strategy
- [ ] Breadcrumb navigation
- [ ] Orphan pages identified

#### Performance
- [ ] Core Web Vitals passing
  - LCP < 2.5s (Largest Contentful Paint)
  - FID < 100ms (First Input Delay)
  - CLS < 0.1 (Cumulative Layout Shift)
- [ ] Page speed optimized
- [ ] Images properly compressed
- [ ] Browser caching enabled
- [ ] CDN implemented

#### Mobile
- [ ] Mobile-friendly test passing
- [ ] Responsive design
- [ ] Mobile-first indexing ready
- [ ] Touch elements properly sized
- [ ] No horizontal scrolling

#### Security
- [ ] HTTPS everywhere
- [ ] Valid SSL certificate
- [ ] Mixed content resolved
- [ ] Security headers implemented

### 2. On-Page SEO

#### Title Tags
- Unique for each page
- 50-60 characters
- Primary keyword near beginning
- Compelling and click-worthy
- Brand name at end (optional)

#### Meta Descriptions
- Unique for each page
- 150-160 characters
- Include primary keyword
- Clear call-to-action
- Accurately describes content

#### Headings
- Single H1 per page
- H1 includes primary keyword
- Logical heading hierarchy
- Keywords in H2s where natural
- Headings describe content accurately

#### Content Quality
- Satisfies search intent
- Comprehensive coverage
- Original and valuable
- Proper keyword usage (not stuffing)
- Updated regularly
- Includes relevant media

#### URL Structure
- Short and descriptive
- Includes target keyword
- Uses hyphens, not underscores
- Lowercase only
- No unnecessary parameters

#### Images
- Descriptive file names
- Alt text for all images
- Compressed for web
- Proper dimensions
- Next-gen formats where supported

#### Internal Linking
- Contextual links to related content
- Anchor text is descriptive
- Important pages have most links
- No broken internal links
- Link equity flows to priority pages

### 3. Content Analysis

#### Keyword Strategy
- Primary keyword identified per page
- Secondary keywords mapped
- Search intent aligned
- Keyword difficulty appropriate
- Search volume justified

#### Content Gaps
- Competitor content analysis
- Missing topic clusters
- Underserved search queries
- Content update opportunities

#### SERP Features
- Featured snippet opportunities
- People Also Ask optimization
- FAQ schema potential
- Image pack opportunities
- Video carousel potential

### 4. Off-Page SEO

#### Backlink Profile
- Total referring domains
- Domain authority/rating
- Link quality distribution
- Toxic links identified
- Anchor text diversity

#### Competitor Comparison
- Share of voice
- Content gaps vs competitors
- Link gap analysis
- SERP position tracking

#### Local SEO (if applicable)
- Google Business Profile optimized
- NAP consistency
- Local citations
- Review strategy
- Local content

## Audit Output Structure

### Executive Summary
- Overall SEO health score
- Top 3-5 critical issues
- Top 3-5 opportunities
- Estimated impact potential

### Critical Issues (Fix Immediately)
Issues that are actively harming rankings or preventing indexing.

### High Priority (Fix This Week)
Significant issues that are limiting performance.

### Medium Priority (Fix This Month)
Improvements that will contribute to growth.

### Low Priority (Backlog)
Nice-to-haves and minor optimizations.

### Quick Wins
Easy fixes with immediate impact.

## Tools Reference

### Google Tools
- Search Console (indexing, performance)
- PageSpeed Insights (performance)
- Mobile-Friendly Test
- Rich Results Test

### Crawling
- Screaming Frog
- Sitebulb
- Ahrefs Site Audit

### Performance
- GTmetrix
- WebPageTest
- Lighthouse

### Backlinks
- Ahrefs
- Moz
- Majestic

## Deliverable Template

```
# SEO Audit Report: [Site Name]
Date: [Date]

## Executive Summary
[2-3 paragraph overview]

## Health Scores
- Technical: [X/100]
- On-Page: [X/100]
- Content: [X/100]
- Off-Page: [X/100]

## Critical Issues
1. [Issue + recommendation + expected impact]
2. ...

## Detailed Findings

### Technical SEO
[Detailed findings with evidence]

### On-Page SEO
[Page-by-page analysis]

### Content Analysis
[Content gaps and opportunities]

### Off-Page SEO
[Link profile analysis]

## Action Plan
[Prioritized tasks with owners and timelines]

## Appendix
[Supporting data and screenshots]
```

## Related Skills

- `schema-markup` - For structured data implementation
- `programmatic-seo` - For scalable SEO
- `page-cro` - For improving page performance
