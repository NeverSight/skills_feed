---
name: app-store-price-index
description: >
  Price localization intelligence for iOS/macOS apps using purchasing power parity
  analysis. Use this skill when working with App Store pricing for any of these tasks:
  (1) Building a "Price Index" by analyzing reference app prices across territories,
  (2) Comparing your app's pricing against PPP-adjusted benchmarks,
  (3) Generating localized price recommendations based on economic data,
  (4) Automating price updates via App Store Connect API,
  (5) Analyzing competitor pricing strategies across markets,
  (6) Identifying overpriced/underpriced territories hurting conversions or revenue,
  (7) Creating pricing health reports with actionable recommendations.
---

# App Store Price Index

Optimize your App Store pricing using purchasing power parity analysis—like the
Big Mac Index or Spotify Premium Index, but for your iOS/macOS apps.

## Concept

Different countries have vastly different purchasing power. A $9.99/month subscription
that feels reasonable in the US may be unaffordable in India or Turkey. This skill helps
you set data-driven, localized prices that maximize both conversions and revenue.

### The Premium Index Approach

1. **Collect reference prices** — Fetch prices of popular apps (Spotify, Netflix, etc.)
   across all 175 App Store territories
2. **Calculate index** — Compare each territory's price to the US baseline
3. **Cross-reference PPP** — Validate against World Bank purchasing power parity data
4. **Generate recommendations** — Suggest optimal prices per territory
5. **Automate updates** — Apply prices via App Store Connect API

## API Access Tiers

| Tier | Auth | Scope | Use Case |
|------|------|-------|----------|
| **Public** | None | Any app's price via iTunes Lookup | Build Premium Index, competitor analysis |
| **Private** | JWT | Your apps' price points + write access | Get equalizations, apply price changes |

## Workflow 1 — Build Premium Index

Create a price index by analyzing reference apps across territories.

### Step 1: Select Reference Apps

Choose 3-5 popular subscription apps as benchmarks:

```
Suggested references by category:
- General: Spotify (id: 324684580), Netflix (id: 363590051)
- Productivity: Notion (id: 1232780281), Todoist (id: 585829637)
- Fitness: Strava (id: 426826309), MyFitnessPal (id: 341232718)
- News: NYTimes (id: 284862083), The Athletic (id: 1135216317)
```

### Step 2: Fetch Prices Across Territories

For each reference app, fetch prices from all territories:

```
GET https://itunes.apple.com/lookup?id={app_id}&country={territory_code}
```

Response fields:
- `price` — Numeric price value
- `currency` — Currency code (USD, EUR, GBP, etc.)
- `formattedPrice` — Localized string ("$9.99", "€9,99", "Free")

**Rate limiting:** ~20 requests/minute. Cache results aggressively.

### Step 3: Calculate Index Values

For each territory, calculate:

```
price_index = local_price_in_usd / us_price
```

Where `local_price_in_usd` = local_price × exchange_rate_to_usd

### Step 4: Generate Index Table

Output format:

```markdown
| Territory | Currency | Spotify | Netflix | Avg Index | PPP Factor | Status |
|-----------|----------|---------|---------|-----------|------------|--------|
| USA       | USD      | $11.99  | $15.49  | 1.00      | 1.00       | Baseline |
| GBR       | GBP      | £11.99  | £10.99  | 0.92      | 0.69       | High |
| IND       | INR      | ₹119    | ₹199    | 0.14      | 0.28       | Optimized |
| TUR       | TRY      | ₺57.99  | ₺63.99  | 0.16      | 0.19       | Good |
| BRA       | BRL      | R$21.90 | R$39.90 | 0.35      | 0.41       | Low |
```

Status interpretation:
- **Baseline** — Reference territory (usually USA)
- **Optimized** — Index aligns well with PPP (within ±20%)
- **High** — Price higher than PPP suggests (may hurt conversions)
- **Low** — Price lower than PPP suggests (leaving money on table)
- **Good** — Reasonable alignment

See [index-methodology.md](references/index-methodology.md) for calculation details.

---

## Workflow 2 — Analyze Your Current Pricing

Compare your app's pricing against the Premium Index to identify optimization opportunities.

### Step 1: Fetch Your Current Prices

**Option A: Via iTunes Lookup (public)**
```
GET https://itunes.apple.com/lookup?id={your_app_id}&country={territory}
```

**Option B: Via App Store Connect API (private, more accurate)**
```
GET /v1/apps/{id}/appPriceSchedule
GET /v1/subscriptions/{id}/pricePoints?filter[territory]={territory}
```

### Step 2: Compare Against Index

For each territory:

```
your_index = your_price_in_usd / your_us_price
deviation = (your_index - premium_index) / premium_index × 100
```

### Step 3: Generate Pricing Health Report

```markdown
## Pricing Health Report — {App Name}

### Summary
- Territories analyzed: 175
- Optimized: 42 (24%)
- Potentially overpriced: 58 (33%)
- Potentially underpriced: 75 (43%)

### Top Opportunities

#### Overpriced (may hurt conversions)
| Territory | Your Price | Recommended | Potential Impact |
|-----------|------------|-------------|------------------|
| Brazil    | $9.99      | $4.99       | +45% conversions |
| India     | $6.99      | $2.99       | +120% conversions |
| Turkey    | $7.99      | $1.99       | +85% conversions |

#### Underpriced (leaving revenue on table)
| Territory | Your Price | Recommended | Potential Impact |
|-----------|------------|-------------|------------------|
| Switzerland | $9.99    | $14.99      | +50% revenue |
| Norway      | $9.99    | $12.99      | +30% revenue |
| UAE         | $9.99    | $11.99      | +20% revenue |
```

---

## Workflow 3 — Generate Localized Price Recommendations

Create a complete price schedule optimized for each territory.

### Input Required

1. **Base price** — Your price in a reference territory (usually USA)
2. **Product type** — App, subscription, or in-app purchase
3. **Strategy** — Conservative, balanced, or aggressive localization

### Strategy Options

| Strategy | Description | Index Multiplier |
|----------|-------------|------------------|
| **Conservative** | Minimal variation, prioritize simplicity | 0.3× PPP adjustment |
| **Balanced** | Moderate localization (recommended) | 0.6× PPP adjustment |
| **Aggressive** | Full PPP alignment, maximize reach | 1.0× PPP adjustment |

### Step 1: Calculate Target Prices

```python
for territory in territories:
    ppp_factor = get_ppp_factor(territory)
    strategy_weight = get_strategy_weight(strategy)

    # Calculate adjustment
    adjustment = (1 - ppp_factor) * strategy_weight
    target_price = base_price * (1 - adjustment)

    # Ensure minimum viable price
    target_price = max(target_price, minimum_prices[territory])
```

### Step 2: Match to Apple Price Points

Apple has ~800 fixed price points. Match each target to the nearest available tier:

```
GET /v1/subscriptionPricePoints/{base_point_id}/equalizations
```

This returns equivalent price points across all territories.

### Step 3: Output Price Schedule

```markdown
## Recommended Price Schedule — {App Name}

Base: $9.99 USD (Monthly Subscription)
Strategy: Balanced

| Territory | Currency | Current | Recommended | Price Point ID | Change |
|-----------|----------|---------|-------------|----------------|--------|
| USA       | USD      | $9.99   | $9.99       | pp_usa_999     | —      |
| GBR       | GBP      | £9.99   | £7.99       | pp_gbr_799     | -20%   |
| EUR       | EUR      | €10.99  | €8.99       | pp_eur_899     | -18%   |
| IND       | INR      | ₹799    | ₹299        | pp_ind_299     | -63%   |
| BRA       | BRL      | R$54.90 | R$34.90     | pp_bra_3490    | -36%   |
| JPN       | JPY      | ¥1,500  | ¥1,200      | pp_jpn_1200    | -20%   |
```

---

## Workflow 4 — Apply Pricing via API

Automate price updates using App Store Connect API.

### Prerequisites

- App Store Connect API key with appropriate permissions
- JWT token generation capability
- See [apple-pricing-api.md](references/apple-pricing-api.md) for auth setup

### For Subscriptions

```
POST /v1/subscriptionPrices
{
  "data": {
    "type": "subscriptionPrices",
    "attributes": {
      "startDate": "2024-02-01"  // Optional: schedule future change
    },
    "relationships": {
      "subscription": {
        "data": { "type": "subscriptions", "id": "{subscription_id}" }
      },
      "subscriptionPricePoint": {
        "data": { "type": "subscriptionPricePoints", "id": "{price_point_id}" }
      }
    }
  }
}
```

Repeat for each territory.

### For In-App Purchases

```
POST /v1/inAppPurchasePriceSchedules
{
  "data": {
    "type": "inAppPurchasePriceSchedules",
    "relationships": {
      "inAppPurchase": {
        "data": { "type": "inAppPurchases", "id": "{iap_id}" }
      },
      "manualPrices": {
        "data": [
          { "type": "inAppPurchasePrices", "id": "${placeholder-0}" },
          { "type": "inAppPurchasePrices", "id": "${placeholder-1}" }
        ]
      },
      "baseTerritory": {
        "data": { "type": "territories", "id": "USA" }
      }
    }
  },
  "included": [
    {
      "type": "inAppPurchasePrices",
      "id": "${placeholder-0}",
      "relationships": {
        "inAppPurchasePricePoint": {
          "data": { "type": "inAppPurchasePricePoints", "id": "{point_id}" }
        }
      }
    }
  ]
}
```

### Safety Checks

Before applying prices:
1. **Preview changes** — Show before/after comparison
2. **Require confirmation** — User must explicitly approve
3. **Validate price points** — Ensure all IDs are valid
4. **Check for scheduled changes** — Avoid conflicts with pending updates

---

## Workflow 5 — Competitor Price Intelligence

Analyze how competitors price across territories.

### Step 1: Identify Competitors

```
GET https://itunes.apple.com/search?term={category}&media=software&limit=50
```

Or user provides specific app IDs.

### Step 2: Fetch Competitor Prices

For each competitor, fetch prices across key territories:

```python
key_territories = ['USA', 'GBR', 'DEU', 'JPN', 'AUS', 'BRA', 'IND', 'KOR', 'TUR', 'MEX']

for competitor in competitors:
    for territory in key_territories:
        price = fetch_price(competitor.id, territory)
```

### Step 3: Generate Comparison Report

```markdown
## Competitor Pricing Analysis — {Category}

### Price Comparison (Monthly Subscription)

| App | USA | UK | Germany | Japan | India | Brazil | Turkey |
|-----|-----|-----|---------|-------|-------|--------|--------|
| Your App | $9.99 | £9.99 | €10.99 | ¥1,500 | ₹799 | R$54.90 | ₺149.99 |
| Competitor A | $7.99 | £6.99 | €7.99 | ¥1,000 | ₹349 | R$29.90 | ₺59.99 |
| Competitor B | $12.99 | £11.99 | €12.99 | ¥1,800 | ₹499 | R$44.90 | ₺99.99 |
| Market Avg | $10.32 | £9.66 | €10.66 | ¥1,433 | ₹549 | R$43.23 | ₺103.32 |

### Insights

- **India:** You're 45% above market average. Consider reducing to improve competitiveness.
- **Turkey:** You're 45% above market average. High-growth market, price sensitivity high.
- **Japan:** You're aligned with market. No immediate action needed.
- **USA:** You're 3% below market. Room to increase if value proposition is strong.
```

---

## Quick Reference — API Endpoints

| Task | Method | Endpoint | Auth |
|------|--------|----------|------|
| Lookup app price | GET | `itunes.apple.com/lookup?id={id}&country={cc}` | Public |
| Search apps | GET | `itunes.apple.com/search?term={q}&media=software` | Public |
| List subscription price points | GET | `/v1/subscriptions/{id}/pricePoints?filter[territory]={cc}` | JWT |
| Get price equalizations | GET | `/v1/subscriptionPricePoints/{id}/equalizations` | JWT |
| List IAP price points | GET | `/v2/inAppPurchases/{id}/pricePoints?filter[territory]={cc}` | JWT |
| Set subscription price | POST | `/v1/subscriptionPrices` | JWT |
| Set IAP price schedule | POST | `/v1/inAppPurchasePriceSchedules` | JWT |
| List territories | GET | `/v1/territories` | JWT |

---

## Caching Strategy

To avoid rate limits and improve performance:

| Data | Cache Duration | Storage |
|------|----------------|---------|
| iTunes Lookup prices | 24 hours | Local file |
| Premium Index | 7 days | Local file |
| PPP data | 30 days | Reference file |
| Territory codes | Permanent | Reference file |
| Price points | 24 hours | Local file |

---

## Reference Files

| File | Purpose |
|------|---------|
| [territory-codes.md](references/territory-codes.md) | All 175 territory codes, currencies, and regions |
| [ppp-data.md](references/ppp-data.md) | World Bank PPP conversion factors |
| [apple-pricing-api.md](references/apple-pricing-api.md) | API authentication and endpoint details |
| [index-methodology.md](references/index-methodology.md) | Premium Index calculation methodology |
