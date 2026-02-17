---
name: google-analytics
description: >
  Pull GA4 reports, traffic data, and insights from the Google Analytics Data API.
  Use when asked about website traffic, user behavior, acquisition channels,
  conversions, or audience segments. Trigger phrases: "google analytics", "GA4",
  "traffic report", "analytics data", "user acquisition", "engagement metrics",
  "conversion tracking", "audience segments", "page views", "sessions".
---

# Google Analytics (GA4)

Pull reports and insights from GA4 using the Google Analytics Data API.

## Prerequisites

Requires Google OAuth credentials:
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- A valid OAuth access token (refreshed as needed)

Set credentials in `.env`, `.env.local`, or `~/.claude/.env.global`.

### Getting an Access Token

```bash
# Step 1: Get authorization code (user must visit this URL in browser)
echo "https://accounts.google.com/o/oauth2/v2/auth?client_id=${GOOGLE_CLIENT_ID}&redirect_uri=urn:ietf:wg:oauth:2.0:oob&scope=https://www.googleapis.com/auth/analytics.readonly&response_type=code&access_type=offline"

# Step 2: Exchange code for tokens
curl -s -X POST "https://oauth2.googleapis.com/token" \
  -d "code={AUTH_CODE}" \
  -d "client_id=${GOOGLE_CLIENT_ID}" \
  -d "client_secret=${GOOGLE_CLIENT_SECRET}" \
  -d "redirect_uri=urn:ietf:wg:oauth:2.0:oob" \
  -d "grant_type=authorization_code"

# Step 3: Refresh an expired token
curl -s -X POST "https://oauth2.googleapis.com/token" \
  -d "refresh_token={REFRESH_TOKEN}" \
  -d "client_id=${GOOGLE_CLIENT_ID}" \
  -d "client_secret=${GOOGLE_CLIENT_SECRET}" \
  -d "grant_type=refresh_token"
```

Store the refresh token securely. The access token expires after 1 hour.

### Finding Your GA4 Property ID

```bash
curl -s -H "Authorization: Bearer ${GA_ACCESS_TOKEN}" \
  "https://analyticsadmin.googleapis.com/v1beta/accountSummaries" \
  | python3 -c "
import json, sys
data = json.load(sys.stdin)
for acct in data.get('accountSummaries', []):
    for prop in acct.get('propertySummaries', []):
        print(f\"{prop['property']}  |  {prop.get('displayName','')}  |  Account: {acct.get('displayName','')}\")
"
```

The property ID format is `properties/XXXXXXXXX`.

---

## API Base

```
POST https://analyticsdata.googleapis.com/v1beta/{property_id}:runReport
```

All report requests use POST with a JSON body. Always include `Authorization: Bearer {ACCESS_TOKEN}`.

---

## 1. Traffic Overview Report

Get sessions, users, page views, and engagement rate over a date range.

### Example curl

```bash
curl -s -X POST \
  "https://analyticsdata.googleapis.com/v1beta/properties/{PROPERTY_ID}:runReport" \
  -H "Authorization: Bearer ${GA_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
    "metrics": [
      {"name": "sessions"},
      {"name": "totalUsers"},
      {"name": "newUsers"},
      {"name": "screenPageViews"},
      {"name": "engagementRate"},
      {"name": "averageSessionDuration"},
      {"name": "bounceRate"}
    ]
  }'
```

### Date Range Shortcuts

- `today`, `yesterday`
- `7daysAgo`, `14daysAgo`, `28daysAgo`, `30daysAgo`, `90daysAgo`
- Specific dates: `2024-01-01`
- Compare periods by passing two dateRanges

---

## 2. User Acquisition Report

See where users come from (channels, sources, campaigns).

```bash
curl -s -X POST \
  "https://analyticsdata.googleapis.com/v1beta/properties/{PROPERTY_ID}:runReport" \
  -H "Authorization: Bearer ${GA_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
    "dimensions": [
      {"name": "sessionDefaultChannelGroup"}
    ],
    "metrics": [
      {"name": "sessions"},
      {"name": "totalUsers"},
      {"name": "engagementRate"},
      {"name": "conversions"}
    ],
    "orderBys": [{"metric": {"metricName": "sessions"}, "desc": true}],
    "limit": 20
  }'
```

### Useful Acquisition Dimensions

| Dimension | Description |
|-----------|-------------|
| `sessionDefaultChannelGroup` | Channel grouping (Organic, Paid, Social, etc.) |
| `sessionSource` | Traffic source (google, facebook, etc.) |
| `sessionMedium` | Medium (organic, cpc, referral, etc.) |
| `sessionCampaignName` | UTM campaign name |
| `firstUserSource` | First-touch attribution source |

---

## 3. Top Pages Report

Find the highest-traffic pages on the site.

```bash
curl -s -X POST \
  "https://analyticsdata.googleapis.com/v1beta/properties/{PROPERTY_ID}:runReport" \
  -H "Authorization: Bearer ${GA_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
    "dimensions": [
      {"name": "pagePath"}
    ],
    "metrics": [
      {"name": "screenPageViews"},
      {"name": "totalUsers"},
      {"name": "engagementRate"},
      {"name": "averageSessionDuration"}
    ],
    "orderBys": [{"metric": {"metricName": "screenPageViews"}, "desc": true}],
    "limit": 25
  }'
```

---

## 4. Engagement Metrics

Understand how users interact with your content.

```bash
curl -s -X POST \
  "https://analyticsdata.googleapis.com/v1beta/properties/{PROPERTY_ID}:runReport" \
  -H "Authorization: Bearer ${GA_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
    "dimensions": [
      {"name": "pagePath"}
    ],
    "metrics": [
      {"name": "engagedSessions"},
      {"name": "engagementRate"},
      {"name": "averageSessionDuration"},
      {"name": "screenPageViewsPerSession"},
      {"name": "eventCount"}
    ],
    "orderBys": [{"metric": {"metricName": "engagedSessions"}, "desc": true}],
    "limit": 20
  }'
```

### Key Engagement Metrics

| Metric | What It Measures |
|--------|-----------------|
| `engagementRate` | % of sessions that were engaged (>10s, 2+ pages, or conversion) |
| `averageSessionDuration` | Mean session length in seconds |
| `screenPageViewsPerSession` | Pages per session |
| `bounceRate` | % of sessions with no engagement |
| `eventCount` | Total events fired |

---

## 5. Conversion Tracking

Report on conversion events (purchases, signups, etc.).

```bash
curl -s -X POST \
  "https://analyticsdata.googleapis.com/v1beta/properties/{PROPERTY_ID}:runReport" \
  -H "Authorization: Bearer ${GA_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
    "dimensions": [
      {"name": "eventName"}
    ],
    "metrics": [
      {"name": "eventCount"},
      {"name": "totalUsers"},
      {"name": "eventValue"}
    ],
    "dimensionFilter": {
      "filter": {
        "fieldName": "eventName",
        "inListFilter": {
          "values": ["purchase", "sign_up", "generate_lead", "begin_checkout"]
        }
      }
    }
  }'
```

### Conversion by Channel

```bash
curl -s -X POST \
  "https://analyticsdata.googleapis.com/v1beta/properties/{PROPERTY_ID}:runReport" \
  -H "Authorization: Bearer ${GA_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
    "dimensions": [
      {"name": "sessionDefaultChannelGroup"}
    ],
    "metrics": [
      {"name": "sessions"},
      {"name": "conversions"},
      {"name": "totalRevenue"}
    ],
    "orderBys": [{"metric": {"metricName": "conversions"}, "desc": true}]
  }'
```

---

## 6. Audience Segments

Break down traffic by device, geography, and demographics.

### By Device Category

```bash
curl -s -X POST \
  "https://analyticsdata.googleapis.com/v1beta/properties/{PROPERTY_ID}:runReport" \
  -H "Authorization: Bearer ${GA_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
    "dimensions": [{"name": "deviceCategory"}],
    "metrics": [
      {"name": "sessions"},
      {"name": "totalUsers"},
      {"name": "engagementRate"},
      {"name": "conversions"}
    ]
  }'
```

### By Country

Replace `deviceCategory` with `country` in the dimensions.

### By Landing Page + Source

```bash
curl -s -X POST \
  "https://analyticsdata.googleapis.com/v1beta/properties/{PROPERTY_ID}:runReport" \
  -H "Authorization: Bearer ${GA_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
    "dimensions": [
      {"name": "landingPage"},
      {"name": "sessionSource"}
    ],
    "metrics": [
      {"name": "sessions"},
      {"name": "engagementRate"},
      {"name": "conversions"}
    ],
    "orderBys": [{"metric": {"metricName": "sessions"}, "desc": true}],
    "limit": 30
  }'
```

---

## 7. Period Comparison

Compare two time periods to identify trends.

```bash
curl -s -X POST \
  "https://analyticsdata.googleapis.com/v1beta/properties/{PROPERTY_ID}:runReport" \
  -H "Authorization: Bearer ${GA_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "dateRanges": [
      {"startDate": "30daysAgo", "endDate": "today", "name": "current"},
      {"startDate": "60daysAgo", "endDate": "31daysAgo", "name": "previous"}
    ],
    "metrics": [
      {"name": "sessions"},
      {"name": "totalUsers"},
      {"name": "conversions"},
      {"name": "engagementRate"}
    ]
  }'
```

---

## Response Parsing

GA4 API returns JSON. Parse with python3 or jq:

```bash
# Parse report into a table
curl -s -X POST "..." | python3 -c "
import json, sys
data = json.load(sys.stdin)
headers = [h['name'] for h in data.get('dimensionHeaders',[])] + [m['name'] for m in data.get('metricHeaders',[])]
print(' | '.join(headers))
print('-' * (len(headers) * 20))
for row in data.get('rows', []):
    dims = [d['value'] for d in row.get('dimensionValues',[])]
    mets = [m['value'] for m in row.get('metricValues',[])]
    print(' | '.join(dims + mets))
"
```

---

## Workflow: Monthly Analytics Report

When asked for a monthly report:

1. Pull traffic overview (sessions, users, page views) with period comparison
2. Pull acquisition breakdown by channel
3. Pull top 20 pages by page views
4. Pull conversion summary by channel
5. Pull device and country breakdown

Present as a structured report with tables, trends (up/down arrows), and recommendations:

```
## Monthly Analytics Report: {Property Name}
### Period: {date range} vs {previous period}

### Traffic Summary
| Metric | Current | Previous | Change |
|--------|---------|----------|--------|
| Sessions | X | Y | +Z% |
| ...

### Top Channels
...

### Top Pages
...

### Conversion Summary
...

### Recommendations
- [Based on data patterns]
```

## Common Issues

- **403 Forbidden**: User lacks access to the GA4 property
- **Empty rows**: No data for the requested date range or filters
- **Quota exceeded**: GA4 API has daily quotas; reduce date ranges or batch requests
- **Property not found**: Verify the property ID format (`properties/XXXXXXXXX`)
