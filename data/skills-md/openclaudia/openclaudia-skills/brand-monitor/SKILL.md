---
name: brand-monitor
description: >
  Brand monitoring and mention tracking via the Brand.dev API. Use when asked to
  monitor brand mentions, track sentiment, find PR opportunities, detect logo
  usage, or analyze brand presence online. Trigger phrases: "brand monitoring",
  "mention tracking", "brand sentiment", "PR opportunities", "logo detection",
  "brand.dev", "brand mentions", "media monitoring".
---

# Brand Monitor

Track brand mentions, analyze sentiment, and discover PR opportunities using the Brand.dev API.

## Prerequisites

Requires `BRANDDEV_API_KEY` set in `.env`, `.env.local`, or `~/.claude/.env.global`.

```bash
echo "BRANDDEV_API_KEY is ${BRANDDEV_API_KEY:+set}"
```

If the key is not set, instruct the user:
> You need a Brand.dev API key. Get one at https://brand.dev/
> Then add `BRANDDEV_API_KEY=your_key` to your `.env` file.

## API Base

All requests go to `https://api.brand.dev/v1/` with the header `Authorization: Bearer {BRANDDEV_API_KEY}`.

---

## 1. Brand Search

Search for mentions of a brand name across the web.

### Endpoint

```
GET https://api.brand.dev/v1/brand/search
```

### Parameters

| Param | Type | Description |
|-------|------|-------------|
| `query` | string | Brand name or phrase to search |
| `limit` | int | Number of results (default 20, max 100) |
| `offset` | int | Pagination offset |
| `sort` | string | `relevance` or `date` |
| `from_date` | string | Start date (YYYY-MM-DD) |
| `to_date` | string | End date (YYYY-MM-DD) |

### Example curl

```bash
curl -s -H "Authorization: Bearer ${BRANDDEV_API_KEY}" \
  "https://api.brand.dev/v1/brand/search?query=YourBrand&limit=20&sort=date"
```

### Response Parsing

```bash
curl -s -H "Authorization: Bearer ${BRANDDEV_API_KEY}" \
  "https://api.brand.dev/v1/brand/search?query=YourBrand&limit=20" \
  | python3 -c "
import json, sys
data = json.load(sys.stdin)
for m in data.get('results', []):
    print(f\"Source: {m.get('source','')}  |  Title: {m.get('title','')}  |  Sentiment: {m.get('sentiment','n/a')}  |  Date: {m.get('published_at','')}\")
    print(f\"  URL: {m.get('url','')}\")
    print()
"
```

---

## 2. Brand Info Lookup

Get structured brand information for any company or product.

### Endpoint

```
GET https://api.brand.dev/v1/brand/info
```

### Parameters

| Param | Type | Description |
|-------|------|-------------|
| `domain` | string | Company domain (e.g., `stripe.com`) |
| `name` | string | Brand name (alternative to domain) |

### Example curl

```bash
curl -s -H "Authorization: Bearer ${BRANDDEV_API_KEY}" \
  "https://api.brand.dev/v1/brand/info?domain=stripe.com"
```

### Response Fields

- `name`: Official brand name
- `domain`: Primary domain
- `description`: Brand description
- `industry`: Industry classification
- `founded`: Year founded
- `headquarters`: Location
- `social_profiles`: Links to social media
- `logos`: Brand logo URLs
- `colors`: Brand color palette
- `employees_range`: Company size estimate

---

## 3. Logo Detection

Detect brand logos in images across the web.

### Endpoint

```
GET https://api.brand.dev/v1/logo/search
```

### Parameters

| Param | Type | Description |
|-------|------|-------------|
| `brand` | string | Brand name to search for |
| `domain` | string | Filter to specific domain |
| `limit` | int | Number of results |

### Example curl

```bash
curl -s -H "Authorization: Bearer ${BRANDDEV_API_KEY}" \
  "https://api.brand.dev/v1/logo/search?brand=YourBrand&limit=20"
```

Use logo detection to find:
- Unauthorized logo usage
- Partner and sponsor visibility
- Event coverage and media placements
- Counterfeit product listings

---

## 4. Mention Tracking

Set up ongoing tracking for brand mentions.

### Create a Monitor

```
POST https://api.brand.dev/v1/monitors
```

### Body

```json
{
  "name": "My Brand Monitor",
  "keywords": ["YourBrand", "Your Brand", "yourbrand.com"],
  "exclude_keywords": ["unrelated term"],
  "sources": ["news", "blogs", "social", "forums", "reviews"],
  "languages": ["en"],
  "notify_email": "alerts@yourdomain.com"
}
```

### Example curl

```bash
curl -s -X POST -H "Authorization: Bearer ${BRANDDEV_API_KEY}" \
  -H "Content-Type: application/json" \
  "https://api.brand.dev/v1/monitors" \
  -d '{
    "name": "Brand Alert",
    "keywords": ["YourBrand"],
    "sources": ["news", "blogs", "social"],
    "languages": ["en"]
  }'
```

### List Monitors

```bash
curl -s -H "Authorization: Bearer ${BRANDDEV_API_KEY}" \
  "https://api.brand.dev/v1/monitors"
```

### Get Monitor Results

```bash
curl -s -H "Authorization: Bearer ${BRANDDEV_API_KEY}" \
  "https://api.brand.dev/v1/monitors/{monitor_id}/mentions?limit=50&sort=date"
```

---

## 5. Sentiment Analysis

Analyze sentiment of brand mentions.

### Endpoint

```
GET https://api.brand.dev/v1/brand/sentiment
```

### Parameters

| Param | Type | Description |
|-------|------|-------------|
| `query` | string | Brand name |
| `from_date` | string | Start date |
| `to_date` | string | End date |
| `granularity` | string | `day`, `week`, or `month` |

### Example curl

```bash
curl -s -H "Authorization: Bearer ${BRANDDEV_API_KEY}" \
  "https://api.brand.dev/v1/brand/sentiment?query=YourBrand&from_date=2024-01-01&to_date=2024-03-31&granularity=week"
```

### Sentiment Scores

- **Positive** (> 0.3): Praise, recommendations, positive reviews
- **Neutral** (-0.3 to 0.3): Factual mentions, news coverage
- **Negative** (< -0.3): Complaints, criticism, negative reviews

---

## 6. Competitor Mention Comparison

Compare brand mention volume and sentiment against competitors.

### Workflow

1. Search mentions for your brand and each competitor
2. Compare mention counts over the same time period
3. Compare sentiment distributions
4. Identify sources where competitors get mentioned but you do not

```bash
# For each brand, get mention counts
for brand in "YourBrand" "Competitor1" "Competitor2"; do
  count=$(curl -s -H "Authorization: Bearer ${BRANDDEV_API_KEY}" \
    "https://api.brand.dev/v1/brand/search?query=${brand}&limit=1" \
    | python3 -c "import json,sys; print(json.load(sys.stdin).get('total',0))")
  echo "${brand}: ${count} mentions"
done
```

---

## Workflow: Full Brand Audit

When asked for a comprehensive brand monitoring report:

### Step 1: Brand Info

Pull structured brand data for context.

### Step 2: Mention Volume

Search for brand mentions over the last 30/90 days. Count total mentions and break down by source type.

### Step 3: Sentiment Analysis

Get sentiment trends. Flag any negative spikes and investigate root causes.

### Step 4: PR Opportunities

From mention data, identify:
- **High-authority sites** that mention competitors but not you
- **Journalists** who cover your industry
- **Trending topics** where your brand could contribute
- **Unanswered questions** about your brand on forums

### Step 5: Logo/Visual Presence

Search for logo appearances. Flag unauthorized usage.

### Step 6: Report

Present findings as:

```
## Brand Monitoring Report: {Brand}

### Overview
- Total mentions (last 30 days): X
- Sentiment breakdown: X% positive, X% neutral, X% negative
- Top sources: ...

### Sentiment Trend
[Weekly trend data]

### Top Positive Mentions
1. [Source] - [Title] - [URL]
2. ...

### Negative Mentions Requiring Attention
1. [Source] - [Title] - [URL] - [Issue summary]
2. ...

### PR Opportunities
1. [Publication] covers [topic] - pitch angle: ...
2. [Journalist] recently wrote about [topic] - pitch angle: ...

### Competitor Comparison
| Metric | Your Brand | Competitor A | Competitor B |
|--------|-----------|-------------|-------------|
| Mentions | ... | ... | ... |
| Positive % | ... | ... | ... |
| Top Source | ... | ... | ... |

### Action Items
- [ ] Respond to [negative mention]
- [ ] Pitch [publication] about [topic]
- [ ] Update brand listing on [platform]
```

---

## Error Handling

| Status | Meaning |
|--------|---------|
| 401 | Invalid or expired API key |
| 403 | Insufficient permissions for this endpoint |
| 404 | Resource not found (check monitor ID) |
| 429 | Rate limit exceeded - wait and retry |
| 500 | Server error - retry after a few seconds |

## Tips

- Use exact brand name + common misspellings as keywords
- Exclude your own domain to avoid self-mentions
- Set up monitors for competitor brands too
- Check mentions weekly at minimum; daily during launches or crises
- Export negative mentions to a spreadsheet for customer support follow-up
