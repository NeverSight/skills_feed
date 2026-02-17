---
name: google-ads-report
description: >
  Pull Google Ads performance data and generate reports. Use when asked about
  ad campaign performance, keyword costs, quality scores, ROAS, conversion
  tracking, or ad spend analysis. Trigger phrases: "google ads", "adwords",
  "campaign performance", "ad spend", "quality score", "CPC report",
  "ROAS", "ad conversion", "keyword performance", "google ads report".
---

# Google Ads Report

Pull campaign, keyword, and conversion data from the Google Ads API.

## Prerequisites

Requires:
- `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` (OAuth)
- `GOOGLE_ADS_DEVELOPER_TOKEN` (apply at https://ads.google.com/home/tools/manager-accounts/)
- `GOOGLE_ADS_CUSTOMER_ID` (the account ID, format: `XXX-XXX-XXXX`, passed without dashes)
- `GOOGLE_ADS_LOGIN_CUSTOMER_ID` (if using a manager account, the manager account ID)

Set in `.env`, `.env.local`, or `~/.claude/.env.global`.

### Getting an Access Token

```bash
# Same OAuth flow as other Google APIs
# Scope needed: https://www.googleapis.com/auth/adwords

echo "https://accounts.google.com/o/oauth2/v2/auth?client_id=${GOOGLE_CLIENT_ID}&redirect_uri=urn:ietf:wg:oauth:2.0:oob&scope=https://www.googleapis.com/auth/adwords&response_type=code&access_type=offline"

# Exchange code for tokens
curl -s -X POST "https://oauth2.googleapis.com/token" \
  -d "code={AUTH_CODE}" \
  -d "client_id=${GOOGLE_CLIENT_ID}" \
  -d "client_secret=${GOOGLE_CLIENT_SECRET}" \
  -d "redirect_uri=urn:ietf:wg:oauth:2.0:oob" \
  -d "grant_type=authorization_code"
```

---

## API Base

Google Ads API uses GAQL (Google Ads Query Language) via REST.

```
POST https://googleads.googleapis.com/v17/customers/{CUSTOMER_ID}/googleAds:searchStream
```

Headers:
```
Authorization: Bearer {ACCESS_TOKEN}
developer-token: {DEVELOPER_TOKEN}
login-customer-id: {LOGIN_CUSTOMER_ID}  # Only if using manager account
Content-Type: application/json
```

---

## 1. Campaign Performance Report

Overview of all campaigns with key metrics.

```bash
curl -s -X POST \
  "https://googleads.googleapis.com/v17/customers/${GOOGLE_ADS_CUSTOMER_ID}:searchStream" \
  -H "Authorization: Bearer ${GADS_ACCESS_TOKEN}" \
  -H "developer-token: ${GOOGLE_ADS_DEVELOPER_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "SELECT campaign.name, campaign.status, metrics.impressions, metrics.clicks, metrics.ctr, metrics.average_cpc, metrics.cost_micros, metrics.conversions, metrics.cost_per_conversion, metrics.conversions_value FROM campaign WHERE segments.date DURING LAST_30_DAYS AND campaign.status != REMOVED ORDER BY metrics.cost_micros DESC"
  }'
```

### Parsing Campaign Data

```bash
curl -s -X POST "..." | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f\"{'Campaign':<35} {'Status':<10} {'Impr':>8} {'Clicks':>7} {'CTR':>7} {'Avg CPC':>8} {'Cost':>10} {'Conv':>6} {'CPA':>8}\")
print('-' * 110)
for batch in data:
    for row in batch.get('results', []):
        c = row.get('campaign', {})
        m = row.get('metrics', {})
        cost = int(m.get('costMicros', 0)) / 1_000_000
        cpc = int(m.get('averageCpc', 0)) / 1_000_000
        cpa = float(m.get('costPerConversion', 0)) / 1_000_000 if m.get('costPerConversion') else 0
        print(f\"{c.get('name',''):<35} {c.get('status',''):<10} {int(m.get('impressions',0)):>8} {int(m.get('clicks',0)):>7} {float(m.get('ctr',0))*100:>6.2f}% \${cpc:>7.2f} \${cost:>9.2f} {float(m.get('conversions',0)):>6.1f} \${cpa:>7.2f}\")
"
```

### Important: Cost Micros

All cost values in Google Ads API are in **micros** (1/1,000,000 of the currency unit). Divide by 1,000,000 to get the actual amount.

---

## 2. Keyword Performance Report

See how individual keywords perform.

```bash
curl -s -X POST \
  "https://googleads.googleapis.com/v17/customers/${GOOGLE_ADS_CUSTOMER_ID}:searchStream" \
  -H "Authorization: Bearer ${GADS_ACCESS_TOKEN}" \
  -H "developer-token: ${GOOGLE_ADS_DEVELOPER_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.quality_info.quality_score, metrics.impressions, metrics.clicks, metrics.ctr, metrics.average_cpc, metrics.cost_micros, metrics.conversions, metrics.conversions_value FROM keyword_view WHERE segments.date DURING LAST_30_DAYS AND ad_group_criterion.status != REMOVED ORDER BY metrics.cost_micros DESC LIMIT 50"
  }'
```

### Quality Score Breakdown

```bash
curl -s -X POST \
  "https://googleads.googleapis.com/v17/customers/${GOOGLE_ADS_CUSTOMER_ID}:searchStream" \
  -H "Authorization: Bearer ${GADS_ACCESS_TOKEN}" \
  -H "developer-token: ${GOOGLE_ADS_DEVELOPER_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "SELECT ad_group_criterion.keyword.text, ad_group_criterion.quality_info.quality_score, ad_group_criterion.quality_info.creative_quality_score, ad_group_criterion.quality_info.post_click_quality_score, ad_group_criterion.quality_info.search_predicted_ctr, metrics.impressions, metrics.average_cpc FROM keyword_view WHERE ad_group_criterion.quality_info.quality_score IS NOT NULL AND segments.date DURING LAST_30_DAYS ORDER BY ad_group_criterion.quality_info.quality_score ASC LIMIT 50"
  }'
```

Quality Score Components:
- **quality_score**: Overall score (1-10)
- **creative_quality_score**: Ad relevance (BELOW_AVERAGE, AVERAGE, ABOVE_AVERAGE)
- **post_click_quality_score**: Landing page experience
- **search_predicted_ctr**: Expected click-through rate

---

## 3. Ad Group Performance

```bash
curl -s -X POST \
  "https://googleads.googleapis.com/v17/customers/${GOOGLE_ADS_CUSTOMER_ID}:searchStream" \
  -H "Authorization: Bearer ${GADS_ACCESS_TOKEN}" \
  -H "developer-token: ${GOOGLE_ADS_DEVELOPER_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "SELECT campaign.name, ad_group.name, ad_group.status, metrics.impressions, metrics.clicks, metrics.ctr, metrics.average_cpc, metrics.cost_micros, metrics.conversions FROM ad_group WHERE segments.date DURING LAST_30_DAYS AND ad_group.status != REMOVED ORDER BY metrics.cost_micros DESC LIMIT 50"
  }'
```

---

## 4. Search Terms Report

See what users actually searched for (vs. your keywords).

```bash
curl -s -X POST \
  "https://googleads.googleapis.com/v17/customers/${GOOGLE_ADS_CUSTOMER_ID}:searchStream" \
  -H "Authorization: Bearer ${GADS_ACCESS_TOKEN}" \
  -H "developer-token: ${GOOGLE_ADS_DEVELOPER_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "SELECT search_term_view.search_term, segments.keyword.info.text, segments.keyword.info.match_type, metrics.impressions, metrics.clicks, metrics.ctr, metrics.cost_micros, metrics.conversions FROM search_term_view WHERE segments.date DURING LAST_30_DAYS ORDER BY metrics.impressions DESC LIMIT 100"
  }'
```

Use this to:
- Find new keyword opportunities (high-converting search terms)
- Identify negative keyword candidates (irrelevant terms with spend)
- Discover match type issues (broad match pulling in junk traffic)

---

## 5. Conversion Tracking

```bash
curl -s -X POST \
  "https://googleads.googleapis.com/v17/customers/${GOOGLE_ADS_CUSTOMER_ID}:searchStream" \
  -H "Authorization: Bearer ${GADS_ACCESS_TOKEN}" \
  -H "developer-token: ${GOOGLE_ADS_DEVELOPER_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "SELECT campaign.name, metrics.conversions, metrics.conversions_value, metrics.cost_micros, metrics.conversions_from_interactions_rate, metrics.value_per_conversion FROM campaign WHERE segments.date DURING LAST_30_DAYS AND campaign.status = ENABLED ORDER BY metrics.conversions DESC"
  }'
```

### ROAS Calculation

```bash
# ROAS = conversions_value / (cost_micros / 1_000_000)
curl -s -X POST "..." | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f\"{'Campaign':<35} {'Cost':>10} {'Conv Value':>12} {'ROAS':>8}\")
for batch in data:
    for row in batch.get('results', []):
        c = row['campaign']['name']
        m = row['metrics']
        cost = int(m.get('costMicros', 0)) / 1_000_000
        value = float(m.get('conversionsValue', 0))
        roas = value / cost if cost > 0 else 0
        print(f\"{c:<35} \${cost:>9.2f} \${value:>11.2f} {roas:>7.2f}x\")
"
```

---

## 6. Daily Spend Trend

```bash
curl -s -X POST \
  "https://googleads.googleapis.com/v17/customers/${GOOGLE_ADS_CUSTOMER_ID}:searchStream" \
  -H "Authorization: Bearer ${GADS_ACCESS_TOKEN}" \
  -H "developer-token: ${GOOGLE_ADS_DEVELOPER_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "SELECT segments.date, metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions FROM customer WHERE segments.date DURING LAST_30_DAYS ORDER BY segments.date DESC"
  }'
```

---

## GAQL Date Ranges

Use these built-in date ranges in GAQL:
- `TODAY`, `YESTERDAY`
- `LAST_7_DAYS`, `LAST_14_DAYS`, `LAST_30_DAYS`
- `THIS_MONTH`, `LAST_MONTH`
- `THIS_QUARTER`, `LAST_QUARTER`
- Custom: `segments.date BETWEEN '2024-01-01' AND '2024-03-31'`

---

## Workflow: Monthly Google Ads Report

When asked for a full ads report:

1. **Account Overview**: Total spend, impressions, clicks, conversions, ROAS
2. **Campaign Performance**: All active campaigns ranked by spend
3. **Top Keywords**: Top 20 keywords by spend with quality scores
4. **Search Terms**: Top search terms and negative keyword candidates
5. **Quality Score Distribution**: How many keywords at each QS level
6. **Conversion Analysis**: Conversions and ROAS by campaign
7. **Daily Trend**: Spend and conversion trend over the period

### Report Format

```
## Google Ads Report: {Account Name}
### Period: {date range}

### Account Summary
| Metric | Value | vs Previous |
|--------|-------|-------------|
| Total Spend | $X | +Y% |
| Impressions | X | +Y% |
| Clicks | X | +Y% |
| CTR | X% | +Y pp |
| Avg CPC | $X | +Y% |
| Conversions | X | +Y% |
| ROAS | Xx | +Y% |

### Campaign Performance
| Campaign | Spend | Clicks | Conv | CPA | ROAS |
|----------|-------|--------|------|-----|------|
| ...      | ...   | ...    | ...  | ... | ...  |

### Top Keywords (by spend)
| Keyword | Match | QS | Spend | Clicks | Conv | CPC |
|---------|-------|-----|-------|--------|------|-----|
| ...     | ...   | ... | ...   | ...    | ...  | ... |

### Recommendations
- **Pause**: Keywords with high spend and zero conversions
- **Increase Bids**: Keywords with high conversion rate but limited budget
- **Negative Keywords**: Search terms wasting budget
- **Quality Score Fixes**: Keywords with QS < 5 and actions to improve
- **Budget Reallocation**: Shift budget from low-ROAS to high-ROAS campaigns
```

---

## Error Handling

| Error | Cause |
|-------|-------|
| `AUTHENTICATION_ERROR` | Invalid or expired access token |
| `AUTHORIZATION_ERROR` | Developer token issue or account access |
| `REQUEST_ERROR` | GAQL syntax error |
| `QUOTA_ERROR` | API quota exceeded |

### Common GAQL Mistakes

- Missing `WHERE segments.date DURING ...` (required for most metric queries)
- Using `REMOVED` status filter incorrectly
- Forgetting to handle `costMicros` division by 1,000,000
- Requesting incompatible resource + segment combinations

## Tips

- Always filter out REMOVED campaigns/ad groups/keywords
- Use `searchStream` instead of `search` for large result sets (no pagination needed)
- Cache results when building multi-section reports
- Quality Score of 0 means "not enough data" -- treat as null
