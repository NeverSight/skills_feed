---
name: google-search-console
description: Google Search Console API integration for search analytics, URL inspection, sitemap management, and site verification. Use when working with search performance data, checking indexing status, managing sitemaps, or analyzing SEO metrics.
allowed-tools: Read Write Edit Bash
---

# Google Search Console Skill

**Created by [Return Zero Inc.](https://github.com/rtzr)**

Comprehensive Google Search Console API skill for Claude Code providing search analytics, URL inspection, sitemap management, and site verification capabilities.

## When to Use

- User mentions "Google Search Console", "GSC", "search console"
- User asks about search performance, clicks, impressions, CTR
- User needs URL indexing status or inspection
- User wants to manage sitemaps
- User asks about search rankings or index status
- User needs SEO analytics data from Google

## Features

### 1. **Search Analytics** ⭐
- Query search performance data (clicks, impressions, CTR, position)
- Filter by date range, page, query, country, device
- Group by dimensions (query, page, country, device, date)
- Compare time periods
- Export to CSV/JSON

### 2. **URL Inspection**
- Check indexing status of specific URLs
- View crawl information
- Check mobile usability
- Identify indexing issues
- Request indexing for URLs

### 3. **Sitemap Management**
- List all sitemaps for a site
- Submit new sitemaps
- Delete sitemaps
- Check sitemap status and errors

### 4. **Site Management**
- List all verified sites
- Add new sites
- Remove sites
- Check verification status

## Environment Variables

This skill uses environment variables managed by `jelly-dotenv`. See `skills/jelly-dotenv/SKILL.md` for configuration details.

### Option 1: Service Account (Recommended)

```bash
# Service account JSON key file path
GOOGLE_SERVICE_ACCOUNT_KEY_FILE=/path/to/service-account.json

# Or inline JSON (for CI/CD environments)
GOOGLE_SERVICE_ACCOUNT_KEY_JSON='{"type":"service_account","project_id":"...","private_key":"..."}'
```

### Option 2: OAuth 2.0 Client Credentials

```bash
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REFRESH_TOKEN=your-refresh-token
```

### Common Settings

```bash
# Default site URL (optional, can be specified per request)
GOOGLE_SEARCH_CONSOLE_SITE_URL=https://your-site.com

# Alternative naming patterns (auto-detected)
GSC_SITE_URL=https://your-site.com
SEARCH_CONSOLE_SITE=sc-domain:your-site.com
```

Variables can be configured in either:
- `skills/jelly-dotenv/.env` (skill-common, highest priority)
- Project root `/.env` (project-specific, fallback)

## Configuration

### Setting Up Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable "Google Search Console API"
4. Create a Service Account:
   - Go to IAM & Admin → Service Accounts
   - Create service account
   - Download JSON key file
5. Add service account email to Search Console:
   - Go to [Search Console](https://search.google.com/search-console)
   - Settings → Users and permissions
   - Add user with service account email
   - Grant "Full" or "Restricted" access

### Setting Up OAuth 2.0

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create OAuth 2.0 credentials (Web application)
3. Set authorized redirect URI
4. Use OAuth playground or your app to get refresh token
5. Required scope: `https://www.googleapis.com/auth/webmasters.readonly`

## Usage Scenarios

### Scenario 1: Search Performance Overview

**User Request**: "Show me search performance for the last 7 days"

**Skill Actions**:
1. Load credentials from environment
2. Query Search Analytics API with date range
3. Aggregate clicks, impressions, CTR, position
4. Format as Markdown table with trends

**Output**:
```markdown
## Search Performance (Last 7 Days)

| Metric | Value | Change |
|--------|-------|--------|
| Clicks | 1,234 | +12% |
| Impressions | 45,678 | +8% |
| CTR | 2.7% | +0.3% |
| Avg Position | 15.2 | -2.1 |

### Top Queries
| Query | Clicks | Impressions | CTR | Position |
|-------|--------|-------------|-----|----------|
| keyword 1 | 234 | 5,678 | 4.1% | 8.5 |
| keyword 2 | 189 | 4,321 | 4.4% | 12.3 |
```

### Scenario 2: URL Inspection

**User Request**: "Check indexing status for https://example.com/page"

**Skill Actions**:
1. Call URL Inspection API
2. Parse indexing result
3. Check coverage status
4. Display mobile usability

**Output**:
```markdown
## URL Inspection: https://example.com/page

| Property | Status |
|----------|--------|
| Index Status | ✅ Indexed |
| Crawled | 2024-01-15 |
| Canonical | https://example.com/page |
| Mobile Usability | ✅ Mobile friendly |
| Rich Results | ⚠️ 2 warnings |
```

### Scenario 3: Sitemap Management

**User Request**: "Show all sitemaps and submit a new one"

**Skill Actions**:
1. List existing sitemaps
2. Show status and last submitted date
3. Submit new sitemap URL
4. Confirm submission

### Scenario 4: Top Pages Analysis

**User Request**: "What are my top performing pages?"

**Skill Actions**:
1. Query Search Analytics grouped by page
2. Sort by clicks
3. Include impressions, CTR, position
4. Highlight pages with high impressions but low CTR

## API Reference

### Search Analytics Query

```typescript
interface SearchAnalyticsRequest {
  startDate: string;      // YYYY-MM-DD
  endDate: string;        // YYYY-MM-DD
  dimensions?: ('query' | 'page' | 'country' | 'device' | 'date')[];
  searchType?: 'web' | 'image' | 'video' | 'news';
  dimensionFilterGroups?: FilterGroup[];
  aggregationType?: 'auto' | 'byPage' | 'byProperty';
  rowLimit?: number;      // Max 25000
  startRow?: number;
}
```

### URL Inspection

```typescript
interface UrlInspectionRequest {
  inspectionUrl: string;
  siteUrl: string;
  languageCode?: string;
}
```

### Sitemap Operations

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List | GET | `/webmasters/v3/sites/{siteUrl}/sitemaps` |
| Get | GET | `/webmasters/v3/sites/{siteUrl}/sitemaps/{feedpath}` |
| Submit | PUT | `/webmasters/v3/sites/{siteUrl}/sitemaps/{feedpath}` |
| Delete | DELETE | `/webmasters/v3/sites/{siteUrl}/sitemaps/{feedpath}` |

## Output Formats

### Markdown (Default)
- Formatted tables with metrics
- Trend indicators (↑↓)
- Status icons (✅⚠️❌)
- Summary insights

### JSON
- Raw API response
- Full data structure
- Programmatic access

### CSV
- Spreadsheet-compatible export
- All data rows
- For further analysis

## Error Handling

### Authentication Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid credentials | Check service account key or OAuth tokens |
| 403 Forbidden | No access to site | Add service account to Search Console |
| Invalid scope | Wrong OAuth scope | Use `webmasters.readonly` scope |

### API Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 404 Not Found | Site not in Search Console | Add site to Search Console first |
| 400 Bad Request | Invalid parameters | Check date format (YYYY-MM-DD) |
| 429 Rate Limit | Too many requests | Wait and retry with backoff |

### Common Issues

**"Configuration error: No Google credentials found"**
```bash
# Solution: Add credentials to .env
GOOGLE_SERVICE_ACCOUNT_KEY_FILE=/path/to/key.json
```

**"Site not found or no access"**
```bash
# Solution: Add service account email to Search Console
# Go to: Search Console → Settings → Users and permissions
```

**"Invalid date range"**
```bash
# Solution: Use YYYY-MM-DD format, max 16 months historical data
```

## Security Policy

### Authentication
- **Service Account**: Recommended for server-side usage
- **OAuth 2.0**: For user-authenticated requests
- **Credentials**: Loaded from environment variables only
- **Logging**: Private keys and tokens automatically redacted

### Data Access
- **Read-Only by Default**: Uses `webmasters.readonly` scope
- **Write Operations**: Sitemap submit/delete requires full scope
- **Site-Scoped**: Access limited to authorized sites only

### Rate Limiting
- **Automatic**: Respects Google API quotas
- **Retry**: Exponential backoff on 429 errors
- **Daily Quota**: 1,200 queries per day (default)

## Limitations

- **Historical Data**: Maximum 16 months of search data
- **Data Freshness**: 2-3 day delay for search analytics
- **URL Inspection**: 2,000 requests per day per site
- **Row Limit**: Maximum 25,000 rows per query
- **Dimensions**: Maximum 3 dimensions per query

## Integration with Claude Code

This skill activates automatically when users mention:
- "google search console", "gsc", "search console"
- "search performance", "search analytics"
- "url inspection", "index status"
- "sitemap", "sitemap management"
- "seo analytics", "seo data"

The skill will:
1. Load Google credentials from .env
2. Execute the requested query/operation
3. Format results as Markdown tables
4. Provide actionable insights and recommendations

## References

- [Google Search Console API Documentation](https://developers.google.com/webmaster-tools)
- [Search Analytics API Reference](https://developers.google.com/webmaster-tools/v1/searchanalytics/query)
- [URL Inspection API Reference](https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect)
- [OAuth 2.0 Setup](https://developers.google.com/webmaster-tools/v1/how-tos/authorizing)
- [API Quotas and Limits](https://developers.google.com/webmaster-tools/limits)
