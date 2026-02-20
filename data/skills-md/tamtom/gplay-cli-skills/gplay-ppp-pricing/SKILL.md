---
name: gplay-ppp-pricing
description: Set region-specific pricing for subscriptions and in-app purchases using purchasing power parity (PPP). Use when adjusting prices by country or implementing localized pricing strategies on Google Play.
---

# PPP Pricing (Per-Region Pricing)

Use this skill to set different prices for different countries based on purchasing power parity or custom pricing strategies.

## Preconditions
- Ensure credentials are set (`gplay auth login --service-account` or `GPLAY_SERVICE_ACCOUNT` env var).
- Use `GPLAY_PACKAGE` or pass `--package` explicitly.
- Know your base region (usually US) and base price.

## PPP Multiplier Table

Apply these multipliers to the base USD price. Round all results to `.99` endings (e.g., $4.73 → $4.99, ₹249.37 → ₹249.99).

### Tier 1 — Full Price (1.0x–1.1x)
| Region | Code | Multiplier | Currency |
|--------|------|-----------|----------|
| United States | US | 1.0x | USD |
| United Kingdom | GB | 1.0x | GBP |
| Germany | DE | 1.0x | EUR |
| Australia | AU | 1.0x | AUD |
| Switzerland | CH | 1.1x | CHF |
| Canada | CA | 1.0x | CAD |
| Netherlands | NL | 1.0x | EUR |
| Sweden | SE | 1.0x | SEK |
| Norway | NO | 1.05x | NOK |
| Denmark | DK | 1.0x | DKK |

### Tier 2 — Medium (0.6x–0.8x)
| Region | Code | Multiplier | Currency |
|--------|------|-----------|----------|
| France | FR | 0.8x | EUR |
| Spain | ES | 0.7x | EUR |
| Italy | IT | 0.7x | EUR |
| Japan | JP | 0.8x | JPY |
| South Korea | KR | 0.7x | KRW |
| Poland | PL | 0.6x | PLN |
| Portugal | PT | 0.7x | EUR |
| Czech Republic | CZ | 0.6x | CZK |
| Greece | GR | 0.65x | EUR |
| Chile | CL | 0.6x | CLP |
| Saudi Arabia | SA | 0.8x | SAR |
| UAE | AE | 0.8x | AED |

### Tier 3 — Low (0.3x–0.5x)
| Region | Code | Multiplier | Currency |
|--------|------|-----------|----------|
| India | IN | 0.3x | INR |
| Brazil | BR | 0.5x | BRL |
| Mexico | MX | 0.45x | MXN |
| Indonesia | ID | 0.3x | IDR |
| Turkey | TR | 0.35x | TRY |
| Vietnam | VN | 0.3x | VND |
| Philippines | PH | 0.35x | PHP |
| Egypt | EG | 0.3x | EGP |
| Colombia | CO | 0.4x | COP |
| Argentina | AR | 0.3x | ARS |
| Nigeria | NG | 0.3x | NGN |
| Pakistan | PK | 0.25x | PKR |
| Thailand | TH | 0.4x | THB |
| Malaysia | MY | 0.45x | MYR |
| South Africa | ZA | 0.4x | ZAR |
| Ukraine | UA | 0.3x | UAH |

## Workflow: Set PPP-Based IAP Pricing

### 1. List in-app products
```bash
gplay iap list --package "PACKAGE"
```

### 2. Get current product details
```bash
gplay iap get --package "PACKAGE" --sku "SKU"
```
Note the current `defaultPrice` as your base price.

### 3. Build PPP-adjusted prices JSON
Using the base USD price and the multiplier table, compute per-region prices. Round all values to `.99` endings.

Example: Base price $9.99 USD → India (0.3x) = ₹249.99, Brazil (0.5x) = R$24.99

```json
{
  "sku": "premium_upgrade",
  "defaultPrice": {
    "priceMicros": "9990000",
    "currency": "USD"
  },
  "prices": {
    "US": { "priceMicros": "9990000", "currency": "USD" },
    "IN": { "priceMicros": "2499900", "currency": "INR" },
    "BR": { "priceMicros": "24990000", "currency": "BRL" },
    "MX": { "priceMicros": "4490000", "currency": "MXN" },
    "TR": { "priceMicros": "3490000", "currency": "TRY" },
    "ID": { "priceMicros": "2990000", "currency": "IDR" },
    "JP": { "priceMicros": "7990000", "currency": "JPY" },
    "KR": { "priceMicros": "6990000", "currency": "KRW" },
    "GB": { "priceMicros": "9990000", "currency": "GBP" },
    "DE": { "priceMicros": "9990000", "currency": "EUR" }
  }
}
```

### 4. Update the product
```bash
gplay iap update \
  --package "PACKAGE" \
  --sku "SKU" \
  --json @ppp-prices.json
```

### 5. Verify prices
```bash
gplay iap get --package "PACKAGE" --sku "SKU"
```
Review the `prices` map to confirm all regions are set correctly.

## Workflow: Set PPP-Based Subscription Pricing

### 1. List subscriptions
```bash
gplay subscriptions list --package "PACKAGE"
```

### 2. Get current subscription details
```bash
gplay subscriptions get --package "PACKAGE" --product-id "PRODUCT_ID"
```
Note the base plans and their current `regionalConfigs`.

### 3. Build PPP-adjusted subscription JSON
Apply PPP multipliers equally to ALL base plans. Round to `.99` endings.

Example: Monthly $4.99, Yearly $49.99 with PPP for India (0.3x) and Brazil (0.5x):

```json
{
  "productId": "premium_monthly",
  "basePlans": [
    {
      "basePlanId": "monthly",
      "regionalConfigs": [
        { "regionCode": "US", "price": { "priceMicros": "4990000", "currency": "USD" } },
        { "regionCode": "IN", "price": { "priceMicros": "1490000", "currency": "INR" } },
        { "regionCode": "BR", "price": { "priceMicros": "2490000", "currency": "BRL" } }
      ],
      "autoRenewingBasePlanType": { "billingPeriodDuration": "P1M" }
    },
    {
      "basePlanId": "yearly",
      "regionalConfigs": [
        { "regionCode": "US", "price": { "priceMicros": "49990000", "currency": "USD" } },
        { "regionCode": "IN", "price": { "priceMicros": "14990000", "currency": "INR" } },
        { "regionCode": "BR", "price": { "priceMicros": "24990000", "currency": "BRL" } }
      ],
      "autoRenewingBasePlanType": { "billingPeriodDuration": "P1Y" }
    }
  ]
}
```

### 4. Update the subscription
```bash
gplay subscriptions update \
  --package "PACKAGE" \
  --product-id "PRODUCT_ID" \
  --json @ppp-subscription.json
```

### 5. Verify prices
```bash
gplay subscriptions get --package "PACKAGE" --product-id "PRODUCT_ID"
```
Review all `regionalConfigs` across all base plans to confirm prices are correct.

## Workflow: Migrate Existing Subscriber Prices

When updating PPP prices on subscriptions with active subscribers, new prices only apply to new subscribers. To migrate existing subscribers:

### 1. Update prices (steps above)

### 2. Migrate existing subscribers to new prices
```bash
gplay baseplans migrate-prices \
  --package "PACKAGE" \
  --product-id "PRODUCT_ID" \
  --base-plan "BASE_PLAN_ID" \
  --json @migration.json
```

### 3. Repeat for each base plan
Apply migration to every base plan that had its prices changed:
```bash
# Monthly plan
gplay baseplans migrate-prices \
  --package "PACKAGE" \
  --product-id "PRODUCT_ID" \
  --base-plan monthly \
  --json @migration.json

# Yearly plan
gplay baseplans migrate-prices \
  --package "PACKAGE" \
  --product-id "PRODUCT_ID" \
  --base-plan yearly \
  --json @migration.json
```

### 4. Verify migration
```bash
gplay subscriptions get --package "PACKAGE" --product-id "PRODUCT_ID"
```

## Updating Existing PPP Prices

To change a region's price:
1. Get the current product/subscription to see existing prices.
2. Recompute the PPP-adjusted price with the new base price or new multiplier.
3. Update with the modified JSON (include all regions, not just the changed ones).
4. For subscriptions with active subscribers, run `migrate-prices` for each affected base plan.
5. Verify with a fetch + summary review.

## Batch PPP for Multiple Products

### Multiple IAPs
```bash
# Build a JSON file with PPP prices for each SKU
gplay iap batch-update \
  --package "PACKAGE" \
  --json @ppp-all-iaps.json
```

### Multiple subscriptions
Update each subscription individually:
```bash
gplay subscriptions update --package "PACKAGE" --product-id "sub_1" --json @ppp-sub1.json
gplay subscriptions update --package "PACKAGE" --product-id "sub_2" --json @ppp-sub2.json
```

## Common PPP Strategies

### BigMac Index Approach
Adjust prices based on relative purchasing power:
- USA: $9.99 (baseline)
- India: $2.99 (~70% discount)
- Brazil: $4.99 (~50% discount)
- UK: $9.99 (similar)
- Switzerland: $10.99 (premium)

### Tiered Regional Pricing
Group countries into pricing tiers:
- **Tier 1 (Full)**: USA, UK, Germany, Australia, Switzerland, Canada
- **Tier 2 (Medium)**: France, Spain, Italy, Japan, South Korea, Saudi Arabia
- **Tier 3 (Low)**: India, Brazil, Mexico, Indonesia, Turkey, Vietnam, Egypt

### Revenue Optimization
- Start with Tier 3 discounts to capture volume in price-sensitive markets.
- Monitor conversion rates per region after applying PPP.
- Adjust multipliers based on actual revenue data.

## Notes
- Price changes for subscriptions apply immediately to new subscribers.
- Existing subscribers require explicit price migration via `migrate-prices`.
- Use `gplay pricing convert` for currency conversion reference, but apply PPP multipliers on top.
- Always verify prices after updates by fetching the product and reviewing the summary.
- The PPP multiplier table provides starting points — adjust based on your market data and revenue goals.
