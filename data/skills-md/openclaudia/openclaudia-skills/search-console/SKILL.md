---
name: search-console
description: >
  Pull Google Search Console data and perform search performance analysis.
  Use when asked about search rankings, clicks, impressions, CTR, index coverage,
  Core Web Vitals, or sitemap status. Trigger phrases: "search console", "GSC",
  "search performance", "clicks and impressions", "CTR analysis", "index coverage",
  "core web vitals", "URL inspection", "sitemap status", "ranking data",
  "search queries", "keyword positions".
---

# Google Search Console

Pull search performance data, index coverage, and Core Web Vitals from Google Search Console API.

## Prerequisites

Requires Google OAuth credentials:
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- A valid OAuth access token with `https://www.googleapis.com/auth/webmasters.readonly` scope

Set credentials in `.env`, `.env.local`, or `~/.claude/.env.global`.

### Getting an Access Token

```bash
# Step 1: Authorization URL (user visits in browser)
echo "https://accounts.google.com/o/oauth2/v2/auth?client_id=${GOOGLE_CLIENT_ID}&redirect_uri=urn:ietf:wg:oauth:2.0:oob&scope=https://www.googleapis.com/auth/webmasters.readonly&response_type=code&access_type=offline"

# Step 2: Exchange code for tokens
curl -s -X POST "https://oauth2.googleapis.com/token" \
  -d "code={AUTH_CODE}" \
  -d "client_id=${GOOGLE_CLIENT_ID}" \
  -d "client_secret=${GOOGLE_CLIENT_SECRET}" \
  -d "redirect_uri=urn:ietf:wg:oauth:2.0:oob" \
  -d "grant_type=authorization_code"

# Step 3: Refresh expired token
curl -s -X POST "https://oauth2.googleapis.com/token" \
  -d "refresh_token={REFRESH_TOKEN}" \
  -d "client_id=${GOOGLE_CLIENT_ID}" \
  -d "client_secret=${GOOGLE_CLIENT_SECRET}" \
  -d "grant_type=refresh_token"
```

### Listing Available Sites

```bash
curl -s -H "Authorization: Bearer ${GSC_ACCESS_TOKEN}" \
  "https://www.googleapis.com/webmasters/v3/sites" \
  | python3 -c "
import json, sys
data = json.load(sys.stdin)
for site in data.get('siteEntry', []):
    print(f\"{site['siteUrl']}  |  Permission: {site['permissionLevel']}\")
"
```

The site URL format is either `https://example.com/` (URL prefix) or `sc-domain:example.com` (domain property).

---

## 1. Search Performance Report

The core report: queries, pages, clicks, impressions, CTR, and average position.

### API Endpoint

```
POST https://www.googleapis.com/webmasters/v3/sites/{siteUrl}/searchAnalytics/query
```

Note: The `{siteUrl}` must be URL-encoded (e.g., `https%3A%2F%2Fexample.com%2F` or `sc-domain%3Aexample.com`).

### Top Queries

```bash
curl -s -X POST \
  "https://www.googleapis.com/webmasters/v3/sites/sc-domain%3Aexample.com/searchAnalytics/query" \
  -H "Authorization: Bearer ${GSC_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "startDate": "2024-01-01",
    "endDate": "2024-03-31",
    "dimensions": ["query"],
    "rowLimit": 50,
    "startRow": 0
  }'
```

### Top Pages

```bash
curl -s -X POST \
  "https://www.googleapis.com/webmasters/v3/sites/sc-domain%3Aexample.com/searchAnalytics/query" \
  -H "Authorization: Bearer ${GSC_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "startDate": "2024-01-01",
    "endDate": "2024-03-31",
    "dimensions": ["page"],
    "rowLimit": 50
  }'
```

### Query + Page Combination

```bash
curl -s -X POST \
  "https://www.googleapis.com/webmasters/v3/sites/sc-domain%3Aexample.com/searchAnalytics/query" \
  -H "Authorization: Bearer ${GSC_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "startDate": "2024-01-01",
    "endDate": "2024-03-31",
    "dimensions": ["query", "page"],
    "rowLimit": 100,
    "dimensionFilterGroups": [{
      "filters": [{
        "dimension": "page",
        "operator": "contains",
        "expression": "/blog/"
      }]
    }]
  }'
```

### Available Dimensions

| Dimension | Description |
|-----------|-------------|
| `query` | Search query |
| `page` | URL |
| `country` | Country code (ISO 3166-1 alpha-3) |
| `device` | `DESKTOP`, `MOBILE`, `TABLET` |
| `date` | Individual date |
| `searchAppearance` | Rich result type |

### Response Parsing

```bash
curl -s -X POST "..." | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f\"{'Query':<50} {'Clicks':>8} {'Impr':>8} {'CTR':>8} {'Pos':>6}\")
print('-' * 82)
for row in data.get('rows', []):
    keys = ' + '.join(row.get('keys', []))
    print(f\"{keys:<50} {row['clicks']:>8} {row['impressions']:>8} {row['ctr']*100:>7.1f}% {row['position']:>6.1f}\")
"
```

---

## 2. Search Performance by Date

Track daily trends for queries and pages.

```bash
curl -s -X POST \
  "https://www.googleapis.com/webmasters/v3/sites/sc-domain%3Aexample.com/searchAnalytics/query" \
  -H "Authorization: Bearer ${GSC_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "startDate": "2024-01-01",
    "endDate": "2024-03-31",
    "dimensions": ["date"],
    "rowLimit": 1000
  }'
```

To track a specific query over time:

```bash
curl -s -X POST \
  "https://www.googleapis.com/webmasters/v3/sites/sc-domain%3Aexample.com/searchAnalytics/query" \
  -H "Authorization: Bearer ${GSC_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "startDate": "2024-01-01",
    "endDate": "2024-03-31",
    "dimensions": ["date"],
    "dimensionFilterGroups": [{
      "filters": [{
        "dimension": "query",
        "operator": "equals",
        "expression": "your target keyword"
      }]
    }]
  }'
```

---

## 3. Index Coverage (URL Inspection API)

Check if a specific URL is indexed.

### Endpoint

```
POST https://searchconsole.googleapis.com/v1/urlInspection/index:inspect
```

### Example curl

```bash
curl -s -X POST \
  "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect" \
  -H "Authorization: Bearer ${GSC_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "inspectionUrl": "https://example.com/page-to-check",
    "siteUrl": "sc-domain:example.com"
  }'
```

### Response Fields

| Field | Description |
|-------|-------------|
| `inspectionResult.indexStatusResult.coverageState` | `Submitted and indexed`, `Crawled - currently not indexed`, etc. |
| `inspectionResult.indexStatusResult.robotsTxtState` | `ALLOWED` or `DISALLOWED` |
| `inspectionResult.indexStatusResult.indexingState` | `INDEXING_ALLOWED` or `INDEXING_NOT_ALLOWED` |
| `inspectionResult.indexStatusResult.lastCrawlTime` | When Googlebot last crawled |
| `inspectionResult.indexStatusResult.crawledAs` | `DESKTOP` or `MOBILE` |
| `inspectionResult.mobileUsabilityResult.verdict` | `PASS`, `FAIL`, or `VERDICT_UNSPECIFIED` |

---

## 4. Sitemaps

List and check sitemap status.

### List Sitemaps

```bash
curl -s -H "Authorization: Bearer ${GSC_ACCESS_TOKEN}" \
  "https://www.googleapis.com/webmasters/v3/sites/sc-domain%3Aexample.com/sitemaps" \
  | python3 -c "
import json, sys
data = json.load(sys.stdin)
for sm in data.get('sitemap', []):
    print(f\"URL: {sm['path']}\")
    print(f\"  Type: {sm.get('type','')}  |  Submitted: {sm.get('lastSubmitted','')}\")
    print(f\"  URLs discovered: {sm.get('contents',[{}])[0].get('submitted','?')}  |  Indexed: {sm.get('contents',[{}])[0].get('indexed','?')}\")
    print()
"
```

### Submit a Sitemap

```bash
curl -s -X PUT -H "Authorization: Bearer ${GSC_ACCESS_TOKEN}" \
  "https://www.googleapis.com/webmasters/v3/sites/sc-domain%3Aexample.com/sitemaps/https%3A%2F%2Fexample.com%2Fsitemap.xml"
```

---

## 5. Opportunity Identification

Use Search Console data to find SEO opportunities.

### Low-Hanging Fruit: High Impressions, Low CTR

Queries with many impressions but low CTR suggest the title/description needs optimization.

```bash
# Pull queries, then filter for: impressions > 100 AND ctr < 0.03 AND position < 20
curl -s -X POST \
  "https://www.googleapis.com/webmasters/v3/sites/sc-domain%3Aexample.com/searchAnalytics/query" \
  -H "Authorization: Bearer ${GSC_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "startDate": "2024-01-01",
    "endDate": "2024-03-31",
    "dimensions": ["query", "page"],
    "rowLimit": 1000
  }' | python3 -c "
import json, sys
data = json.load(sys.stdin)
print('== Low CTR Opportunities (High impressions, low CTR, good position) ==')
print(f\"{'Query':<40} {'Page':<40} {'Impr':>6} {'CTR':>7} {'Pos':>5}\")
for row in data.get('rows', []):
    if row['impressions'] > 100 and row['ctr'] < 0.03 and row['position'] < 20:
        print(f\"{row['keys'][0]:<40} {row['keys'][1][-40:]:<40} {row['impressions']:>6} {row['ctr']*100:>6.1f}% {row['position']:>5.1f}\")
"
```

### Striking Distance: Position 5-20

Queries ranking on page 1-2 that could be pushed to top 5 with content optimization.

```bash
# Filter for position between 5 and 20 with decent impressions
curl -s -X POST "..." | python3 -c "
import json, sys
data = json.load(sys.stdin)
print('== Striking Distance Keywords (Position 5-20) ==')
opps = [r for r in data.get('rows',[]) if 5 <= r['position'] <= 20 and r['impressions'] > 50]
opps.sort(key=lambda x: x['impressions'], reverse=True)
for row in opps[:30]:
    print(f\"{row['keys'][0]:<50} Pos: {row['position']:>5.1f}  Impr: {row['impressions']:>6}  Clicks: {row['clicks']:>4}\")
"
```

### Cannibalization Detection

Find queries where multiple pages compete for the same keyword.

```bash
# Pull query+page data, then group by query to find duplicates
curl -s -X POST "..." | python3 -c "
import json, sys
from collections import defaultdict
data = json.load(sys.stdin)
query_pages = defaultdict(list)
for row in data.get('rows', []):
    query_pages[row['keys'][0]].append({
        'page': row['keys'][1],
        'clicks': row['clicks'],
        'impressions': row['impressions'],
        'position': row['position']
    })
print('== Keyword Cannibalization (multiple pages for same query) ==')
for query, pages in sorted(query_pages.items(), key=lambda x: -sum(p['impressions'] for p in x[1])):
    if len(pages) > 1:
        total_impr = sum(p['impressions'] for p in pages)
        if total_impr > 100:
            print(f\"\nQuery: {query} ({total_impr} total impressions)\")
            for p in sorted(pages, key=lambda x: -x['impressions']):
                print(f\"  {p['page'][-60:]}  Pos: {p['position']:.1f}  Impr: {p['impressions']}  Clicks: {p['clicks']}\")
"
```

---

## Workflow: Full Search Performance Audit

When asked for a complete GSC audit:

1. **Overall Metrics**: Total clicks, impressions, avg CTR, avg position for last 90 days vs previous 90 days
2. **Top 30 Queries**: By clicks, with CTR and position
3. **Top 20 Pages**: By clicks, with CTR and position
4. **Device Breakdown**: Desktop vs mobile performance
5. **Low-Hanging Fruit**: High impressions + low CTR opportunities
6. **Striking Distance**: Position 5-20 keywords with optimization potential
7. **Cannibalization**: Queries with multiple competing pages
8. **Index Coverage**: Spot-check important URLs
9. **Sitemap Health**: Verify sitemaps are submitted and indexed

### Report Format

```
## Search Console Audit: {domain}
### Period: {date range}

### Summary
| Metric | Current | Previous | Change |
|--------|---------|----------|--------|
| Clicks | X | Y | +Z% |
| Impressions | X | Y | +Z% |
| Avg CTR | X% | Y% | +Z pp |
| Avg Position | X | Y | +Z |

### Top Queries
| Query | Clicks | Impressions | CTR | Position |
|-------|--------|-------------|-----|----------|
| ...   | ...    | ...         | ... | ...      |

### Optimization Opportunities

#### Title/Description Optimization (High Impressions, Low CTR)
1. "{query}" - {impressions} impressions, {ctr}% CTR, position {pos}
   - Page: {url}
   - Recommendation: ...

#### Content Optimization (Striking Distance)
1. "{query}" - position {pos}, {impressions} impressions
   - Action: Add {query} to H2, expand section on {topic}

#### Cannibalization Fixes
1. "{query}" appears on {n} pages
   - Consolidate to: {best_url}
   - Redirect/noindex: {other_urls}
```

---

## Rate Limits

- Search Analytics API: 1,200 queries per minute
- URL Inspection API: 2,000 inspections per day per property
- Data freshness: Search data is typically 2-3 days behind

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| 403 | No access to this property | Verify ownership in GSC |
| 400 | Invalid date range | Dates must be within last 16 months |
| Empty rows | No data matching filters | Broaden date range or remove filters |
