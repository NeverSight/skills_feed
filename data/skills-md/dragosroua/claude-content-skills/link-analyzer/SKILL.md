---
name: link-analyzer
description: Comprehensive link analysis for static sites. Use when the user wants to analyze links, find broken links, identify orphan pages, detect under-linked or over-linked content, find link sinks, or understand their site's internal linking structure. Supports HTTP validation with false-positive filtering.
---

# Link Analyzer Skill

## Purpose

This skill provides comprehensive link analysis for static websites, including:
- Internal/external link extraction
- Broken link detection (HTTP validation)
- Link graph metrics (orphans, sinks, under/over-linked)
- False positive filtering (bot blockers, rate limits)
- SEO-focused recommendations

## When to Use This Skill

- User asks to "analyze links" or "check broken links"
- User wants to find "orphan pages" or "dead ends"
- User mentions "internal linking" or "link structure"
- User needs to "find under-linked content"
- User wants to identify "link sinks" or "pages with no outbound links"
- User asks about "link juice" distribution

## Link Analysis Types

### 1. Outbound Links Analysis
Extracts and categorizes all external links:
- Social media links
- E-commerce (Amazon, Gumroad)
- Email/Phone links
- App Store links
- General external websites

### 2. Internal Links Check
Validates all internal links point to existing pages:
- Handles path variations (with/without trailing slash)
- Checks for index.html alternatives
- Reports broken internal links

### 3. External Links Validation
HTTP checks on external links with smart filtering:
- Parallel requests for speed
- Retries for transient failures
- Filters false positives (bot blockers, rate limits)
- Categorizes by error type (404, timeout, SSL, etc.)

### 4. Link Graph Metrics (NEW)
Builds a complete link graph and calculates:
- **Orphan Pages**: Pages with zero inbound internal links
- **Under-linked Pages**: Pages below inbound link threshold
- **Over-linked Pages**: Pages above outbound link threshold
- **Link Sinks**: Pages that receive links but don't pass them (dead ends)
- **Link Flow Ratio**: Inbound vs outbound balance

## Configuration

Create a `config.json`:

```json
{
  "dist_path": "./dist",
  "site_domain": "example.com",
  "internal_domains": ["example.com", "www.example.com", "wp.example.com"],
  "excluded_paths": ["/tag/", "/category/", "/page/"],
  "http": {
    "timeout": 5,
    "max_workers": 20,
    "retry_count": 1,
    "user_agent": "LinkChecker/1.0"
  },
  "thresholds": {
    "underlinked_min_inbound": 3,
    "overlinked_max_outbound": 50,
    "link_sink_max_outbound": 2
  },
  "false_positive_domains": [
    "linkedin.com",
    "stackoverflow.com",
    "twitter.com",
    "facebook.com"
  ],
  "output": {
    "report_dir": "./reports",
    "data_dir": "./data"
  }
}
```

## Workflow

### Full Analysis
```bash
python scripts/analyze.py --dist ./dist --full
```

### Individual Analyses
```bash
# Outbound links only
python scripts/outbound_links.py --dist ./dist

# Internal links check
python scripts/internal_links.py --dist ./dist

# HTTP validation (requires outbound data)
python scripts/http_checker.py --input outbound_links_data.json

# Link graph metrics
python scripts/link_graph.py --dist ./dist
```

## Output Reports

### Link Graph Report
```
LINK GRAPH ANALYSIS
==================

ORPHAN PAGES (0 inbound links): 15 pages
- /old-page-nobody-links-to/
- /draft-accidentally-published/
...

UNDER-LINKED PAGES (<3 inbound): 47 pages
- /great-article-needs-promotion/ (1 inbound)
- /hidden-gem-content/ (2 inbound)
...

OVER-LINKED PAGES (>50 outbound): 3 pages
- /resources/ (127 outbound)
...

LINK SINKS (receive but don't pass): 23 pages
- /about/ (15 inbound, 0 outbound)
...
```

### Broken Links Report
```
ACTIONABLE BROKEN LINKS
======================

404 - Page Not Found: 25 links
- https://old-blog.com/post (5 occurrences)
...

Dead Domains: 8 links
- https://defunct-site.com (3 occurrences)
...

Timeouts: 4 links
- https://slow-affiliate.com (2 occurrences)
```

## Metrics Definitions

| Metric | Definition | SEO Impact |
|--------|------------|------------|
| **Orphan Page** | Page with 0 inbound internal links | Critical - page may not be indexed |
| **Under-linked** | Page with fewer than threshold inbound links | High - page lacks authority signals |
| **Over-linked** | Page with more than threshold outbound links | Medium - dilutes link equity |
| **Link Sink** | Page with high inbound but low/no outbound | Medium - doesn't distribute link equity |
| **Link Flow Ratio** | Inbound links / Outbound links | Ideal around 1.0 for most pages |

## Example Usage

User: "Analyze my site's internal linking and find pages that need more links"

Claude will:
1. Build complete link graph from static files
2. Calculate inbound/outbound counts for every page
3. Identify orphan pages (critical SEO issue)
4. Find under-linked pages (opportunity for improvement)
5. Detect link sinks (pages that don't pass equity)
6. Generate actionable report with recommendations
