---
name: data-export-formats
description: Use when exporting data for ad platforms (Google Ads, Meta) or working with project datasets. Documents exact CSV formats for Enhanced Conversions, Customer Match, and project data schemas.
---

# Data Export Formats

Use this skill when creating CSV exports for ad platforms or when you need to understand the project's data schemas.

## Google Ads Export Formats

### Enhanced Conversions CSV

For uploading offline conversion data to improve Smart Bidding.

**Required columns:**
```
Email,Phone,Conversion Name,Conversion Time,Conversion Value,Conversion Currency
```

**Format requirements:**
- **Email**: SHA256 hash (32 hex chars, lowercase)
- **Phone**: SHA256 hash (32 hex chars, lowercase)
- **Conversion Name**: String matching your Google Ads conversion action
- **Conversion Time**: ISO 8601 UTC format (`2024-11-15T14:32:00Z`)
- **Conversion Value**: Numeric, no currency symbol
- **Conversion Currency**: 3-letter code (`USD`, `EUR`, etc.)

**Example:**
```csv
Email,Phone,Conversion Name,Conversion Time,Conversion Value,Conversion Currency
ed8e83c2f4cb7b9f43cdc75c148b0b09,628923b3c489bda7dd9ebba89cb5b46c,paid_subscription,2025-11-03T00:00:00Z,2388.0,USD
1bffb899c9248b28e37cda02dbd59444,0dd03c9dc463ab5efcd15f3343035ffa,paid_subscription,2025-10-31T00:00:00Z,2189.0,USD
```

**Google Ads upload path:**
`Tools & Settings → Conversions → Upload conversions → Import`

---

### Customer Match CSV (Retargeting Audiences)

For uploading audience lists to Google Ads.

**Minimal columns (email only):**
```
Email
```

**Extended columns (better match rate):**
```
Email,Phone,First Name,Last Name,Country,Zip
```

**Format requirements:**
- **Email**: SHA256 hash (32 hex chars, lowercase) OR plaintext (Google hashes it)
- **Phone**: SHA256 hash OR E.164 format (`+14155551234`)
- **First Name / Last Name**: Plaintext, lowercase, trimmed
- **Country**: 2-letter ISO code (`US`, `GB`, etc.)
- **Zip**: 5-digit US or local format

**Example (hashed):**
```csv
Email,Phone
ed8e83c2f4cb7b9f43cdc75c148b0b09,628923b3c489bda7dd9ebba89cb5b46c
1bffb899c9248b28e37cda02dbd59444,0dd03c9dc463ab5efcd15f3343035ffa
```

**Google Ads upload path:**
`Tools & Settings → Audience Manager → Customer Match → Email list`

---

### Meta Custom Audiences CSV

For uploading to Meta Ads Manager.

**Columns:**
```
email,phone,fn,ln,country,zip
```

**Format requirements:**
- **email**: SHA256 hash (lowercase hex) OR plaintext lowercase
- **phone**: Digits only, no formatting (`14155551234`)
- **fn / ln**: Lowercase, trimmed
- **country**: 2-letter ISO lowercase (`us`)
- **zip**: 5-digit

**Example:**
```csv
email,phone,fn,ln,country,zip
ed8e83c2f4cb7b9f43cdc75c148b0b09,14155551234,john,doe,us,94105
```

---

## Project Data Schemas

### users.csv (~5,000 records)

User master file with acquisition data.

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| user_id | UUID | Unique identifier | `208763df-9843-4c82-b4f1-bc6382a44acf` |
| email | String | SHA256 hash (32 chars) | `0f9f75d98cacdbd135ccbf18f1aa2e54` |
| phone | String | SHA256 hash (32 chars) | `eb18808fce984c7887799fe9e45f3d66` |
| signup_date | Date | Registration date | `2024-11-15` |
| traffic_source | String | Acquisition channel | `organic`, `paid_search`, `paid_social`, `direct`, `referral` |
| utm_source | String | UTM source | `google`, `facebook`, `linkedin` |
| utm_medium | String | UTM medium | `cpc`, `organic`, `social`, `referral` |
| utm_campaign | String | Campaign ID | `google_ads_q4`, `fb_retargeting` |

---

### events.csv (~57,000 records)

Event stream with funnel progression.

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| event_id | UUID | Unique event ID | `22794184-df27-4329-86b1-acccd60b79b2` |
| user_id | UUID | FK to users | `a0505dd5-4327-4f86-82cc-bf39ba62c92e` |
| event_name | String | Event type | `page_view`, `pricing_view`, `checkout_start`, `form_submit`, `conversion` |
| page_url | String | Page path | `/`, `/pricing`, `/checkout`, `/success` |
| timestamp | DateTime | ISO 8601 UTC | `2024-11-15T14:32:00Z` |
| session_id | UUID | Groups session events | `80ea1bd9-d628-4ef6-bf26-64d928490205` |
| conversion_value | Numeric | USD (conversions only) | `150.00` or empty |

**Funnel stages (event_name values):**
1. `page_view` - Landing page visit
2. `pricing_view` - Viewed pricing page
3. `checkout_start` - Started checkout
4. `form_submit` - Submitted form
5. `conversion` - Completed purchase

---

### daily_metrics.csv (~60 records)

Daily aggregated metrics with engineered anomalies.

| Field | Type | Description |
|-------|------|-------------|
| date | Date | Metric date |
| sessions | Integer | Daily sessions |
| users | Integer | Unique users |
| conversions | Integer | Daily conversions |
| revenue | Numeric | Daily revenue (USD) |
| conversion_rate | Numeric | Conversions / users |
| avg_order_value | Numeric | Revenue / conversions |

**Engineered anomalies:**
- Nov 15: -63% sessions (signup flow bug)
- Nov 21: +99% conversions (onboarding improvement)
- Nov 28-30: -72% conversion rate (activation issue)

---

### trial_users.csv (~500 records)

Trial user conversion data (Demo 4).

| Field | Type | Description |
|-------|------|-------------|
| user_id | UUID | Unique identifier |
| signup_date | Date | Trial start date |
| plan_type | String | Always `free_trial` |
| converted | Boolean | Whether converted to paid |
| conversion_date | Date | When converted (nullable) |
| days_to_convert | Integer | Days from signup to conversion |

---

### feature_usage.csv (~2,500 records)

Feature adoption events (Demo 4).

| Field | Type | Description |
|-------|------|-------------|
| user_id | UUID | FK to trial_users |
| feature_name | String | Feature used |
| first_used_date | Date | First usage date |
| usage_count | Integer | Total uses |
| days_since_signup_first_use | Integer | Days from signup to first use |

**Key features:**
- `create_form_onboarding` - Created first form
- `publish_form` - Published a form
- `embed_form` - Embedded form on site
- `configure_integration` - Set up integration (**aha moment**)
- `view_analytics` - Viewed form analytics

**Aha moment pattern:** Users who `configure_integration` within 3 days convert at 70% vs 19% baseline (3.7x lift).

---

### utm_data.csv (~12 records)

Campaign UTM data with intentional inconsistencies (Demo 5).

| Field | Type | Description |
|-------|------|-------------|
| url | String | Landing page URL |
| utm_source | String | Source parameter |
| utm_medium | String | Medium parameter |
| utm_campaign | String | Campaign parameter |
| session_count | Integer | Sessions with this UTM |

**Engineered issues:**
- Source fragmentation: `linkedin` vs `LinkedIn` vs `LINKEDIN`
- Typos: `product_upd_dec` instead of `product_update_dec`

---

## Common Export Patterns

### High-Value Converters (Enhanced Conversions)

```sql
SELECT
  u.email AS Email,
  u.phone AS Phone,
  'paid_subscription' AS "Conversion Name",
  e.timestamp AS "Conversion Time",
  e.conversion_value AS "Conversion Value",
  'USD' AS "Conversion Currency"
FROM users u
JOIN events e ON u.user_id = e.user_id
WHERE e.event_name = 'conversion'
  AND e.conversion_value > 100
ORDER BY e.conversion_value DESC
```

### Retargeting Audience (Customer Match)

```sql
WITH pricing_views AS (
  SELECT user_id, COUNT(*) as view_count
  FROM events
  WHERE event_name = 'pricing_view'
  GROUP BY user_id
  HAVING COUNT(*) >= 2
),
checkout_starters AS (
  SELECT DISTINCT user_id FROM events WHERE event_name = 'checkout_start'
),
converters AS (
  SELECT DISTINCT user_id FROM events WHERE event_name = 'conversion'
)
SELECT u.email AS Email, u.phone AS Phone
FROM users u
JOIN pricing_views pv ON u.user_id = pv.user_id
JOIN checkout_starters cs ON u.user_id = cs.user_id
LEFT JOIN converters c ON u.user_id = c.user_id
WHERE c.user_id IS NULL
```

---

## File Locations

| File | Location | Records |
|------|----------|---------|
| users.csv | `data/users.csv` | ~5,000 |
| events.csv | `data/events.csv` | ~57,000 |
| daily_metrics.csv | `data/daily_metrics.csv` | ~60 |
| trial_users.csv | `data/trial_users.csv` | ~500 |
| feature_usage.csv | `data/feature_usage.csv` | ~2,500 |
| utm_data.csv | `data/utm_data.csv` | ~12 |

## BigQuery Location

**Project:** `agents-webinar-2025`
**Dataset:** `webinar_demos`
**Tables:** `users`, `events`, `daily_metrics`, `trial_users`, `feature_usage`
