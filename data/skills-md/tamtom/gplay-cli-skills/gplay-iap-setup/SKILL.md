---
name: gplay-iap-setup
description: In-app products, subscriptions, base plans, and offers setup for Google Play monetization. Use when configuring in-app purchases or subscription products.
---

# In-App Purchase Setup for Google Play

Use this skill when you need to set up monetization for your Android app.

## Product Types

1. **In-App Products** - One-time or consumable purchases
2. **Subscriptions** - Recurring billing with base plans and offers

## In-App Products (IAP)

### List products
```bash
gplay iap list --package com.example.app
```

### Create product
```bash
gplay iap create \
  --package com.example.app \
  --sku premium_upgrade \
  --json @product.json
```

### product.json
```json
{
  "sku": "premium_upgrade",
  "status": "active",
  "purchaseType": "managedUser",
  "defaultPrice": {
    "priceMicros": "990000",
    "currency": "USD"
  },
  "prices": {
    "US": {
      "priceMicros": "990000",
      "currency": "USD"
    },
    "GB": {
      "priceMicros": "799000",
      "currency": "GBP"
    }
  },
  "listings": {
    "en-US": {
      "title": "Premium Upgrade",
      "description": "Unlock all premium features"
    },
    "es-ES": {
      "title": "Actualización Premium",
      "description": "Desbloquea todas las funciones premium"
    }
  }
}
```

### Update product
```bash
gplay iap update \
  --package com.example.app \
  --sku premium_upgrade \
  --json @product-updated.json
```

### Batch operations
```bash
# Update multiple products
gplay iap batch-update \
  --package com.example.app \
  --json @products.json

# Get multiple products
gplay iap batch-get \
  --package com.example.app \
  --skus "premium,coins_100,coins_500"
```

### Delete product
```bash
gplay iap delete \
  --package com.example.app \
  --sku premium_upgrade \
  --confirm
```

## Subscriptions

### List subscriptions
```bash
gplay subscriptions list --package com.example.app
```

### Create subscription
```bash
gplay subscriptions create \
  --package com.example.app \
  --json @subscription.json
```

### subscription.json
```json
{
  "productId": "premium_monthly",
  "basePlans": [
    {
      "basePlanId": "monthly",
      "state": "ACTIVE",
      "regionalConfigs": [
        {
          "regionCode": "US",
          "price": {
            "priceMicros": "4990000",
            "currency": "USD"
          }
        }
      ],
      "autoRenewingBasePlanType": {
        "billingPeriodDuration": "P1M"
      }
    },
    {
      "basePlanId": "yearly",
      "state": "ACTIVE",
      "regionalConfigs": [
        {
          "regionCode": "US",
          "price": {
            "priceMicros": "49990000",
            "currency": "USD"
          }
        }
      ],
      "autoRenewingBasePlanType": {
        "billingPeriodDuration": "P1Y"
      }
    }
  ],
  "listings": {
    "en-US": {
      "title": "Premium Subscription",
      "description": "Get all premium features"
    }
  }
}
```

## Base Plans

Base plans define the billing period and price for subscriptions.

### Activate base plan
```bash
gplay baseplans activate \
  --package com.example.app \
  --product-id premium_monthly \
  --base-plan monthly
```

### Deactivate base plan
```bash
gplay baseplans deactivate \
  --package com.example.app \
  --product-id premium_monthly \
  --base-plan monthly
```

### Migrate prices
```bash
gplay baseplans migrate-prices \
  --package com.example.app \
  --product-id premium_monthly \
  --base-plan monthly \
  --json @migration.json
```

## Subscription Offers

Offers provide discounts, free trials, or introductory pricing.

### List offers
```bash
gplay offers list \
  --package com.example.app \
  --product-id premium_monthly \
  --base-plan monthly
```

### Create offer
```bash
gplay offers create \
  --package com.example.app \
  --product-id premium_monthly \
  --base-plan monthly \
  --json @offer.json
```

### offer.json (Free trial)
```json
{
  "offerId": "trial_7day",
  "state": "ACTIVE",
  "phases": [
    {
      "duration": "P7D",
      "pricingType": "FREE_TRIAL"
    }
  ],
  "regionalConfigs": [
    {
      "regionCode": "US"
    }
  ]
}
```

### offer.json (Introductory price)
```json
{
  "offerId": "intro_50_off",
  "state": "ACTIVE",
  "phases": [
    {
      "duration": "P1M",
      "pricingType": "SINGLE_PAYMENT",
      "price": {
        "priceMicros": "2490000",
        "currency": "USD"
      }
    }
  ]
}
```

### Activate/Deactivate offer
```bash
# Activate
gplay offers activate \
  --package com.example.app \
  --product-id premium_monthly \
  --base-plan monthly \
  --offer-id trial_7day

# Deactivate
gplay offers deactivate \
  --package com.example.app \
  --product-id premium_monthly \
  --base-plan monthly \
  --offer-id trial_7day
```

## Regional Pricing

### Convert prices
```bash
gplay pricing convert \
  --package com.example.app \
  --json @price-request.json
```

### price-request.json
```json
{
  "basePriceMicros": "4990000",
  "baseCurrency": "USD",
  "targetCurrencies": ["GBP", "EUR", "JPY"]
}
```

## Common Monetization Patterns

### Pattern 1: Simple IAP
```bash
# One-time premium upgrade
gplay iap create \
  --package com.example.app \
  --sku premium_unlock \
  --json @premium.json
```

### Pattern 2: Consumable IAP
```bash
# Coins/gems that can be consumed
gplay iap create \
  --package com.example.app \
  --sku coins_100 \
  --json @coins.json
```

### Pattern 3: Subscription with Free Trial
```bash
# 1. Create subscription
gplay subscriptions create \
  --package com.example.app \
  --json @sub.json

# 2. Create free trial offer
gplay offers create \
  --package com.example.app \
  --product-id premium \
  --base-plan monthly \
  --json @trial.json
```

### Pattern 4: Multi-Tier Subscription
```json
{
  "productId": "premium",
  "basePlans": [
    {
      "basePlanId": "basic_monthly",
      "price": {"priceMicros": "2990000", "currency": "USD"},
      "billingPeriodDuration": "P1M"
    },
    {
      "basePlanId": "premium_monthly",
      "price": {"priceMicros": "4990000", "currency": "USD"},
      "billingPeriodDuration": "P1M"
    },
    {
      "basePlanId": "premium_yearly",
      "price": {"priceMicros": "49990000", "currency": "USD"},
      "billingPeriodDuration": "P1Y"
    }
  ]
}
```

## Testing

### Use test purchases
In your app code, use test product IDs:
- `android.test.purchased`
- `android.test.canceled`
- `android.test.refunded`
- `android.test.item_unavailable`

### License testing
Add test accounts in Play Console:
Settings → License Testing → Add license testers

## Best Practices

1. **Use clear product IDs** - e.g., `premium_monthly`, not `prod_001`
2. **Localize descriptions** - Provide listings for all supported languages
3. **Set up regional pricing** - Don't use same price everywhere
4. **Offer free trials** - Increase conversion rates
5. **Test thoroughly** - Use test accounts and test product IDs
6. **Monitor conversions** - Track which products/offers perform best
7. **Update prices carefully** - Price changes affect existing subscribers

## Billing Periods

- `P1W` - 1 week
- `P1M` - 1 month
- `P3M` - 3 months
- `P6M` - 6 months
- `P1Y` - 1 year
