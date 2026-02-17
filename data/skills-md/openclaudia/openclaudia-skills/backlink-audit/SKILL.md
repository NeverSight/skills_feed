---
name: backlink-audit
description: Audit a domain's backlink profile using the SemRush API. Use when the user says "audit backlinks", "check my backlinks", "backlink analysis", "link profile", "toxic links", "disavow", "link building opportunities", "referring domains", "anchor text", or asks about a site's link authority.
---

# Backlink Audit Skill

You are an expert link building strategist and backlink auditor. Use the SemRush API to analyze a domain's backlink profile, identify toxic links, and find link building opportunities.

## Prerequisites

This skill requires either `SEMRUSH_API_KEY` or `AHREFS_API_KEY` (or both). Check for them in environment variables or in `~/.claude/.env.global`. Prefer whichever is available; if both are present, use SemRush as primary and Ahrefs to cross-reference. If neither is found, inform the user:

```
This skill requires a SemRush or Ahrefs API key. Set one via:
  export SEMRUSH_API_KEY=your_key_here
  export AHREFS_API_KEY=your_key_here
Or add them to ~/.claude/.env.global
```

## SemRush Backlink API Endpoints

Use `curl` via the Bash tool. Base URL: `https://api.semrush.com/analytics/v1/`

### Core Endpoints

**1. Backlinks Overview**
```
https://api.semrush.com/analytics/v1/?key={KEY}&type=backlinks_overview&target={domain}&target_type=root_domain&export_columns=total,domains_num,urls_num,ips_num,ipclassc_num,follows_num,nofollows_num,texts_num,images_num,forms_num,frames_num
```

**2. Backlinks List (individual links)**
```
https://api.semrush.com/analytics/v1/?key={KEY}&type=backlinks&target={domain}&target_type=root_domain&export_columns=source_url,source_title,target_url,anchor,external_num,internal_num,redirect,nofollow,image,first_seen,last_seen&display_limit=100&display_offset=0
```

**3. Referring Domains**
```
https://api.semrush.com/analytics/v1/?key={KEY}&type=backlinks_refdomains&target={domain}&target_type=root_domain&export_columns=domain,domain_ascore,backlinks_num,ip,country,first_seen,last_seen&display_limit=100&display_sort=domain_ascore_desc
```

**4. Anchor Text Distribution**
```
https://api.semrush.com/analytics/v1/?key={KEY}&type=backlinks_anchors&target={domain}&target_type=root_domain&export_columns=anchor,domains_num,backlinks_num&display_limit=50&display_sort=backlinks_num_desc
```

**5. Indexed Pages (pages receiving links)**
```
https://api.semrush.com/analytics/v1/?key={KEY}&type=backlinks_pages&target={domain}&target_type=root_domain&export_columns=target_url,backlinks_num,domains_num&display_limit=50&display_sort=backlinks_num_desc
```

**6. Competitor Backlinks (for comparison)**
```
# Reuse endpoints above with competitor domain as target
```

**7. Referring Domain Authority Score**
Domain Authority Score (domain_ascore) is returned with referring domains and ranges 0-100.

## Alternative: Ahrefs API

If `AHREFS_API_KEY` is available (and SemRush is not), use the Ahrefs API v3 endpoints below. All endpoints require the Bearer token header.

### Ahrefs Core Endpoints

**1. Backlinks Overview (Stats)**
```bash
# Ahrefs backlinks overview
curl -s "https://api.ahrefs.com/v3/site-explorer/backlinks-stats?target={domain}&output=json" \
  -H "Authorization: Bearer ${AHREFS_API_KEY}"
```
Returns: `live_backlinks`, `all_time_backlinks`, `live_refdomains`, `all_time_refdomains`, `live_refpages`, `dofollow_backlinks`, `nofollow_backlinks`.

**2. Referring Domains**
```bash
# Ahrefs referring domains
curl -s "https://api.ahrefs.com/v3/site-explorer/refdomains?target={domain}&output=json&limit=100" \
  -H "Authorization: Bearer ${AHREFS_API_KEY}"
```
Returns: Array of referring domains with `domain`, `domain_rating`, `backlinks`, `first_seen`, `last_seen`, `dofollow`, `nofollow`. Sort by `domain_rating` to see highest-authority referrers first.

**3. Backlinks List**
```bash
curl -s "https://api.ahrefs.com/v3/site-explorer/backlinks?target={domain}&output=json&limit=100&mode=subdomains" \
  -H "Authorization: Bearer ${AHREFS_API_KEY}"
```
Returns: Individual backlinks with `url_from`, `url_to`, `anchor`, `domain_rating`, `first_seen`, `last_seen`, `nofollow`, `redirect`, `edu`, `gov`.

**4. Anchors**
```bash
curl -s "https://api.ahrefs.com/v3/site-explorer/anchors?target={domain}&output=json&limit=50&mode=subdomains" \
  -H "Authorization: Bearer ${AHREFS_API_KEY}"
```
Returns: Anchor text distribution with `anchor`, `backlinks`, `refdomains`.

**5. Pages by Backlinks (Best by Links)**
```bash
curl -s "https://api.ahrefs.com/v3/site-explorer/best-by-links?target={domain}&output=json&limit=50" \
  -H "Authorization: Bearer ${AHREFS_API_KEY}"
```
Returns: Top linked pages with `url`, `backlinks`, `refdomains`, `dofollow`.

**6. Domain Rating**
```bash
curl -s "https://api.ahrefs.com/v3/site-explorer/domain-rating?target={domain}&output=json" \
  -H "Authorization: Bearer ${AHREFS_API_KEY}"
```
Returns: `domain_rating` (0-100) and `ahrefs_rank`.

### Ahrefs vs. SemRush Field Mapping

When using Ahrefs instead of SemRush, map the fields as follows:
| SemRush Field | Ahrefs Equivalent | Notes |
|---------------|-------------------|-------|
| `domain_ascore` | `domain_rating` | Both are 0-100 authority scores |
| `total` (backlinks) | `live_backlinks` | Ahrefs separates live vs. all-time |
| `domains_num` | `live_refdomains` | Referring domains count |
| `follows_num` | `dofollow_backlinks` | Dofollow link count |
| `nofollows_num` | `nofollow_backlinks` | Nofollow link count |
| `first_seen` / `last_seen` | `first_seen` / `last_seen` | Same concept, both available |

The audit process (Steps 1-7 below) works identically regardless of which API you use. Simply substitute the corresponding endpoints and field names.

## Audit Process

### Step 1: Pull Backlink Overview

Fetch the backlink overview and summarize:

```markdown
## Backlink Profile Summary: {domain}

| Metric | Value |
|--------|-------|
| Total Backlinks | {total} |
| Referring Domains | {domains_num} |
| Referring IPs | {ips_num} |
| Referring Subnets (Class C) | {ipclassc_num} |
| Follow Links | {follows_num} ({%}) |
| Nofollow Links | {nofollows_num} ({%}) |
| Text Links | {texts_num} ({%}) |
| Image Links | {images_num} ({%}) |
| Backlink-to-Domain Ratio | {total/domains_num} |
```

### Step 2: Analyze Referring Domains

Pull the top referring domains sorted by authority score. Evaluate:

**Domain Quality Tiers:**

| Tier | Authority Score | Quality | Action |
|------|----------------|---------|--------|
| Tier 1 | 80-100 | Excellent | Protect and nurture |
| Tier 2 | 60-79 | Good | Maintain relationship |
| Tier 3 | 40-59 | Average | Monitor |
| Tier 4 | 20-39 | Low quality | Review for relevance |
| Tier 5 | 0-19 | Suspicious | Investigate for toxicity |

**Domain Quality Distribution:**
Calculate the percentage of referring domains in each tier. A healthy profile should have:
- Tier 1-2: at least 10-15% of referring domains
- Tier 3: 30-40%
- Tier 4: 20-30%
- Tier 5: < 20% (flag if higher)

**Diversity Analysis:**
- Unique IPs vs. referring domains (ratio close to 1:1 is healthy)
- Unique Class C subnets (should be close to IP count)
- Country distribution (should match target market)
- TLD distribution (.com, .org, .edu, .gov diversity is positive)

### Step 3: Analyze Anchor Text Distribution

Pull anchor text data and classify each anchor:

| Anchor Type | Healthy Range | Description | Example |
|------------|---------------|-------------|---------|
| Branded | 30-50% | Brand name or domain | "Acme Corp", "acme.com" |
| Naked URL | 10-20% | Raw URL | "https://acme.com/product" |
| Generic | 10-15% | Non-descriptive text | "click here", "read more", "this website" |
| Topic/Keyword | 10-20% | Natural topic reference | "project management software" |
| Exact Match | 1-5% | Exact target keyword | "best project management tool" |
| Partial Match | 5-10% | Includes target keyword variation | "top tools for project management" |
| Compound | 5-10% | Brand + keyword | "Acme project management" |
| Image (no alt) | < 5% | Images without alt text | [image] |

**Red flags in anchor text:**
- Exact match > 10% = Over-optimized (Penguin risk)
- Single anchor > 15% of total = Unnatural concentration
- Money keyword anchors from low-quality sites = Likely spam
- Irrelevant anchors (casino, pharma, adult) = Toxic links
- Foreign language anchors unrelated to business = Likely spam

### Step 4: Identify Toxic Links

Score each backlink for toxicity based on these signals:

**Toxicity Signals (each adds to a toxicity score 0-100):**

| Signal | Weight | Detection Method |
|--------|--------|-----------------|
| Source domain AS < 10 | +15 | From referring domains data |
| Source is known link farm/PBN pattern | +30 | Domain name patterns: keyword-keyword-keyword.com, random strings |
| Anchor text is exact match keyword | +10 | From anchor text analysis |
| Source page has 100+ external links | +20 | From external_num column |
| Source is irrelevant niche | +15 | Compare source domain topic to target |
| Source has no organic traffic | +15 | Check via domain_organic if budget allows |
| Link from sitewide (footer/sidebar) | +10 | Same domain, many links to same target |
| Link from non-indexed page | +20 | Page not in Google (manual check) |
| Redirect chain to target | +10 | From redirect column |
| Foreign language + irrelevant | +15 | From anchor text + domain TLD |

**Toxicity Rating:**
- 0-20: Clean - no action needed
- 21-40: Monitor - watch for changes
- 41-60: Suspicious - investigate further
- 61-80: Likely toxic - consider disavow
- 81-100: Toxic - add to disavow list

### Step 5: Link Velocity Analysis

Analyze the `first_seen` and `last_seen` dates to determine:

- **Monthly new links** over the past 12 months
- **Monthly lost links** (links where last_seen is in the past)
- **Net link growth rate**
- **Velocity spikes** (unnatural bursts of links)

**Healthy velocity patterns:**
- Steady, gradual growth = Natural
- Correlated with content publishing = Natural
- Sudden spike then flat = Likely campaign or mention (investigate)
- Massive spike from low-quality domains = Negative SEO attack (flag immediately)
- Declining trend = Losing links, need outreach

### Step 6: Competitor Comparison

Pull backlink overview for 2-3 competitors and compare:

```markdown
## Competitor Backlink Comparison

| Metric | {Your Domain} | {Competitor 1} | {Competitor 2} | {Competitor 3} |
|--------|--------------|----------------|----------------|----------------|
| Total Backlinks | | | | |
| Referring Domains | | | | |
| Avg. Domain AS | | | | |
| Follow % | | | | |
| Link Growth (6mo) | | | | |
```

**Link Gap Analysis:**
Find domains that link to competitors but not to the target:
1. Pull top 100 referring domains for each competitor
2. Filter out domains already linking to the target
3. Sort by authority score
4. These are outreach targets

### Step 7: Generate Disavow File

If toxic links are found, generate a Google Disavow file:

```
# Disavow file for {domain}
# Generated: {date}
# Total entries: {count}

# Individual URLs (confirmed toxic)
{url1}
{url2}

# Full domains (majority of links from domain are toxic)
domain:{domain1}
domain:{domain2}
```

**Disavow rules:**
- Only disavow domains where 80%+ of their links are toxic
- For mixed domains, disavow individual URLs
- Never disavow high-authority domains (AS > 60) without manual verification
- Always recommend the user review the list before submitting

## Output Report Format

```markdown
# Backlink Audit Report: {domain}
**Date:** {date}
**Total Backlinks:** {total}
**Referring Domains:** {count}
**Health Score:** {score}/100

## Executive Summary
{2-3 sentences summarizing the health of the backlink profile}

## Profile Overview
{Overview table from Step 1}

## Referring Domain Quality

### Distribution by Authority
| Tier | Range | Count | Percentage | Status |
|------|-------|-------|-----------|--------|
| Tier 1 | 80-100 | {} | {}% | {Good/Needs more} |
| ... | ... | ... | ... | ... |

### Top 20 Referring Domains
| Domain | Authority | Backlinks | First Seen | Status |
|--------|----------|-----------|-----------|--------|
| {} | {} | {} | {} | {} |

## Anchor Text Analysis

### Distribution
| Type | Percentage | Status |
|------|-----------|--------|
| Branded | {}% | {Healthy/Over/Under} |
| ... | ... | ... |

### Top 20 Anchors
| Anchor | Domains | Backlinks | Type |
|--------|---------|-----------|------|
| {} | {} | {} | {} |

## Toxic Link Analysis

### Summary
- **Total toxic links found:** {count}
- **Toxic referring domains:** {count}
- **Recommended for disavow:** {count}

### Toxic Links Detail
| Source URL | Anchor | Toxicity Score | Signals |
|-----------|--------|---------------|---------|
| {} | {} | {}/100 | {} |

## Link Velocity
{Monthly new/lost links chart description}
{Assessment of velocity health}

## Competitor Comparison
{Comparison table}

## Link Building Opportunities

### Domains Linking to Competitors (Not You)
| Domain | Authority | Links to Competitors | Outreach Strategy |
|--------|----------|---------------------|-------------------|
| {} | {} | {} | {} |

### Recommended Link Building Tactics
1. **{Tactic}** - {Description, estimated effort, expected results}
2. ...

## Action Items

### Immediate (This Week)
1. {Specific action}

### Short Term (This Month)
1. {Specific action}

### Ongoing
1. {Specific action}

## Disavow File
{If applicable, include the generated disavow file content}
```

## Notes

- SemRush API has rate limits. Space out calls if making many requests.
- Backlink data may be up to 30 days old. Note this in the report.
- Never recommend disavowing links from legitimately authoritative domains.
- For new sites (< 6 months), a small backlink profile is normal, not a problem.
- Always recommend manual review of the disavow list before submission to Google Search Console.
- If the user has Google Search Console access, recommend cross-referencing with GSC's link report for the most complete picture.
