---
name: gplay-subscription-localization
description: Bulk-localize subscription display names, descriptions, and offer tags across all Google Play locales using gplay. Use when you want to fill in subscription metadata for every language without clicking through Play Console manually.
---

# Google Play Subscription Localization

Use this skill to bulk-create or bulk-update localized display names, descriptions, and benefits for subscriptions across all Google Play supported locales. This eliminates the tedious manual process of editing each language in Play Console.

## Preconditions
- Auth configured (`gplay auth login` or `GPLAY_SERVICE_ACCOUNT` env var).
- Package name known (`--package` or `GPLAY_PACKAGE`).
- Subscription products already created (use `gplay subscriptions create` first).
- Service account has "Edit and manage your app" permission.

## Supported Google Play Locales

These are the locales supported by Google Play for subscription listings:

```
af, am, ar, hy-AM, az-AZ, eu-ES, be, bn-BD, bg, my-MM, ca,
zh-HK, zh-CN, zh-TW, hr, cs-CZ, da-DK, nl-NL, en-AU, en-CA,
en-GB, en-IN, en-SG, en-US, en-ZA, et, fil, fi-FI, fr-CA,
fr-FR, gl-ES, ka-GE, de-DE, el-GR, gu, he-IL, hi-IN, hu-HU,
is-IS, id, it-IT, ja-JP, kn-IN, kk, km-KH, ko-KR, ky-KG,
lo-LA, lv, lt, mk-MK, ms, ms-MY, ml-IN, mr-IN, mn-MN, ne-NP,
no-NO, fa, pl-PL, pt-BR, pt-PT, pa, ro, rm, ru-RU, sr, si-LK,
sk, sl, es-419, es-ES, es-US, sw, sv-SE, ta-IN, te-IN, th,
tr-TR, uk, ur, vi, zu
```

Verify which locales your app already supports:
```bash
EDIT_ID=$(gplay edits create --package com.example.app | jq -r '.id')
gplay listings list --package com.example.app --edit $EDIT_ID --output table
```

## Subscription Structure in Google Play

Google Play subscriptions have a hierarchical structure:
- **Subscription**: The product itself (e.g., "Premium")
  - **Listings**: Localized display name, description, benefits per locale
  - **Base Plan**: A pricing tier (e.g., "Monthly", "Yearly")
  - **Offer**: Promotional pricing on a base plan (trials, intro prices)

Listings are set at the subscription level and apply to all base plans under it.

## Workflow: Bulk-Localize a Subscription

### 1. List Existing Subscriptions

```bash
gplay subscriptions list --package com.example.app --paginate --output table
```

### 2. Get Current Subscription Details

```bash
gplay subscriptions get \
  --package com.example.app \
  --product-id premium_monthly \
  --output json --pretty
```

The response includes a `listings` object keyed by locale:
```json
{
  "productId": "premium_monthly",
  "listings": {
    "en-US": {
      "title": "Premium Monthly",
      "benefits": ["Unlimited access", "No ads"],
      "description": "Get premium access to all features"
    }
  }
}
```

### 3. Prepare Multi-locale Listings JSON

Create a JSON file with listings for all target locales:

`subscription-listings.json`:
```json
{
  "listings": {
    "en-US": {
      "title": "Premium Monthly",
      "benefits": ["Unlimited access", "No ads", "Priority support"],
      "description": "Get premium access to all features every month."
    },
    "de-DE": {
      "title": "Premium Monatlich",
      "benefits": ["Unbegrenzter Zugang", "Keine Werbung", "Prioritäts-Support"],
      "description": "Erhalten Sie jeden Monat Premium-Zugang zu allen Funktionen."
    },
    "fr-FR": {
      "title": "Premium Mensuel",
      "benefits": ["Accès illimité", "Sans publicité", "Support prioritaire"],
      "description": "Accédez à toutes les fonctionnalités premium chaque mois."
    },
    "es-ES": {
      "title": "Premium Mensual",
      "benefits": ["Acceso ilimitado", "Sin anuncios", "Soporte prioritario"],
      "description": "Obtén acceso premium a todas las funciones cada mes."
    },
    "ja-JP": {
      "title": "プレミアム月額",
      "benefits": ["無制限アクセス", "広告なし", "優先サポート"],
      "description": "毎月すべての機能にプレミアムアクセスできます。"
    },
    "ko-KR": {
      "title": "프리미엄 월간",
      "benefits": ["무제한 액세스", "광고 없음", "우선 지원"],
      "description": "매달 모든 기능에 프리미엄 액세스를 받으세요."
    },
    "pt-BR": {
      "title": "Premium Mensal",
      "benefits": ["Acesso ilimitado", "Sem anúncios", "Suporte prioritário"],
      "description": "Tenha acesso premium a todos os recursos todos os meses."
    },
    "zh-CN": {
      "title": "高级月度订阅",
      "benefits": ["无限访问", "无广告", "优先支持"],
      "description": "每月获得所有功能的高级访问权限。"
    }
  }
}
```

### 4. Update Subscription with All Listings

```bash
gplay subscriptions update \
  --package com.example.app \
  --product-id premium_monthly \
  --json @subscription-listings.json \
  --update-mask listings
```

The `--update-mask listings` ensures only the listings field is modified, leaving base plans and other configuration untouched.

### 5. Verify

```bash
gplay subscriptions get \
  --package com.example.app \
  --product-id premium_monthly \
  --output json --pretty
```

Check that all locales appear in the `listings` object.

## Workflow: Export, Translate, Import

### 1. Export current subscription data

```bash
gplay subscriptions get \
  --package com.example.app \
  --product-id premium_monthly \
  --output json --pretty > subscription-export.json
```

### 2. Extract listings for translation

Use `jq` to isolate the listings:
```bash
jq '.listings' subscription-export.json > listings-to-translate.json
```

### 3. Send for translation

Send `listings-to-translate.json` to your translation service or team. The structure is simple key-value pairs per locale.

### 4. Merge translated listings back

After receiving translations, build the update JSON:
```bash
jq -n --slurpfile translations translated-listings.json \
  '{ listings: $translations[0] }' > subscription-update.json
```

### 5. Import translated listings

```bash
gplay subscriptions update \
  --package com.example.app \
  --product-id premium_monthly \
  --json @subscription-update.json \
  --update-mask listings
```

## Workflow: Bulk-Localize All Subscriptions in an App

```bash
#!/bin/bash
# bulk-localize-subscriptions.sh

PACKAGE="com.example.app"
LISTINGS_FILE="subscription-listings.json"

# Get all subscription product IDs
PRODUCT_IDS=$(gplay subscriptions list \
  --package "$PACKAGE" \
  --paginate | jq -r '.[].productId')

for PRODUCT_ID in $PRODUCT_IDS; do
  echo "Updating listings for: $PRODUCT_ID"

  gplay subscriptions update \
    --package "$PACKAGE" \
    --product-id "$PRODUCT_ID" \
    --json "@$LISTINGS_FILE" \
    --update-mask listings

  echo "Done: $PRODUCT_ID"
done

echo "All subscriptions updated."
```

For subscriptions with different display names, use per-product JSON files:
```bash
for PRODUCT_ID in $PRODUCT_IDS; do
  LISTINGS_FILE="listings/${PRODUCT_ID}.json"
  if [ -f "$LISTINGS_FILE" ]; then
    gplay subscriptions update \
      --package "$PACKAGE" \
      --product-id "$PRODUCT_ID" \
      --json "@$LISTINGS_FILE" \
      --update-mask listings
  else
    echo "Warning: No listings file for $PRODUCT_ID, skipping."
  fi
done
```

## Workflow: Localize Subscription with Base Plans and Offers

When creating a new subscription with localized listings and base plans in one call:

```bash
gplay subscriptions create \
  --package com.example.app \
  --product-id premium_yearly \
  --json @full-subscription.json
```

`full-subscription.json`:
```json
{
  "productId": "premium_yearly",
  "listings": {
    "en-US": {
      "title": "Premium Yearly",
      "benefits": ["Unlimited access", "No ads", "2 months free"],
      "description": "Save with annual premium access."
    },
    "de-DE": {
      "title": "Premium Jährlich",
      "benefits": ["Unbegrenzter Zugang", "Keine Werbung", "2 Monate gratis"],
      "description": "Sparen Sie mit jährlichem Premium-Zugang."
    },
    "fr-FR": {
      "title": "Premium Annuel",
      "benefits": ["Accès illimité", "Sans publicité", "2 mois offerts"],
      "description": "Économisez avec l'accès premium annuel."
    },
    "ja-JP": {
      "title": "プレミアム年間",
      "benefits": ["無制限アクセス", "広告なし", "2ヶ月無料"],
      "description": "年間プレミアムアクセスでお得に。"
    }
  },
  "basePlans": [
    {
      "basePlanId": "yearly",
      "state": "ACTIVE",
      "autoRenewingBasePlanType": {
        "billingPeriodDuration": "P1Y",
        "gracePeriodDuration": "P7D",
        "resubscribeState": "RESUBSCRIBE_STATE_ACTIVE",
        "prorationMode": "CHARGE_ON_NEXT_BILLING_DATE"
      },
      "regionalConfigs": [
        {
          "regionCode": "US",
          "price": {
            "currencyCode": "USD",
            "units": "49",
            "nanos": 990000000
          }
        }
      ]
    }
  ]
}
```

## Workflow: Localize Offer Tags

Offers support localized `offerTags` which can be used for display in your app:

```bash
gplay offers update \
  --package com.example.app \
  --product-id premium_monthly \
  --base-plan-id monthly \
  --offer-id free_trial_7d \
  --json @offer-update.json
```

`offer-update.json`:
```json
{
  "offerTags": [
    {"tag": "free-trial"},
    {"tag": "7-days"}
  ]
}
```

Note: Offer tags are not locale-specific in the Google Play API. They are developer-defined identifiers used for filtering in your app. Localize the user-facing text for offer tags in your app code, not in Play Console.

## Validate Locale Codes

Check which locales your app already has store listings for:

```bash
EDIT_ID=$(gplay edits create --package com.example.app | jq -r '.id')
gplay listings list --package com.example.app --edit $EDIT_ID --output table
```

This lists all locales with store listings. Your subscription listings should cover at least these same locales.

To see the full list of locales a specific listing supports:
```bash
gplay listings list --package com.example.app --edit $EDIT_ID \
  | jq -r '.[].language'
```

## JSON Template: Minimal Multi-locale Subscription

Copy and customize this template for quick localization:

```json
{
  "listings": {
    "en-US": { "title": "TITLE_EN", "benefits": ["BENEFIT_1", "BENEFIT_2"], "description": "DESC_EN" },
    "de-DE": { "title": "TITLE_DE", "benefits": ["BENEFIT_1", "BENEFIT_2"], "description": "DESC_DE" },
    "fr-FR": { "title": "TITLE_FR", "benefits": ["BENEFIT_1", "BENEFIT_2"], "description": "DESC_FR" },
    "es-ES": { "title": "TITLE_ES", "benefits": ["BENEFIT_1", "BENEFIT_2"], "description": "DESC_ES" },
    "it-IT": { "title": "TITLE_IT", "benefits": ["BENEFIT_1", "BENEFIT_2"], "description": "DESC_IT" },
    "ja-JP": { "title": "TITLE_JA", "benefits": ["BENEFIT_1", "BENEFIT_2"], "description": "DESC_JA" },
    "ko-KR": { "title": "TITLE_KO", "benefits": ["BENEFIT_1", "BENEFIT_2"], "description": "DESC_KO" },
    "pt-BR": { "title": "TITLE_PT_BR", "benefits": ["BENEFIT_1", "BENEFIT_2"], "description": "DESC_PT_BR" },
    "ru-RU": { "title": "TITLE_RU", "benefits": ["BENEFIT_1", "BENEFIT_2"], "description": "DESC_RU" },
    "zh-CN": { "title": "TITLE_ZH_CN", "benefits": ["BENEFIT_1", "BENEFIT_2"], "description": "DESC_ZH_CN" },
    "zh-TW": { "title": "TITLE_ZH_TW", "benefits": ["BENEFIT_1", "BENEFIT_2"], "description": "DESC_ZH_TW" },
    "ar": { "title": "TITLE_AR", "benefits": ["BENEFIT_1", "BENEFIT_2"], "description": "DESC_AR" },
    "hi-IN": { "title": "TITLE_HI", "benefits": ["BENEFIT_1", "BENEFIT_2"], "description": "DESC_HI" },
    "tr-TR": { "title": "TITLE_TR", "benefits": ["BENEFIT_1", "BENEFIT_2"], "description": "DESC_TR" },
    "pl-PL": { "title": "TITLE_PL", "benefits": ["BENEFIT_1", "BENEFIT_2"], "description": "DESC_PL" },
    "nl-NL": { "title": "TITLE_NL", "benefits": ["BENEFIT_1", "BENEFIT_2"], "description": "DESC_NL" },
    "sv-SE": { "title": "TITLE_SV", "benefits": ["BENEFIT_1", "BENEFIT_2"], "description": "DESC_SV" },
    "th": { "title": "TITLE_TH", "benefits": ["BENEFIT_1", "BENEFIT_2"], "description": "DESC_TH" },
    "vi": { "title": "TITLE_VI", "benefits": ["BENEFIT_1", "BENEFIT_2"], "description": "DESC_VI" }
  }
}
```

## Agent Behavior
- Always list existing subscriptions and their current listings before making changes.
- Use `--update-mask listings` when updating only localized metadata to avoid overwriting base plans or pricing.
- When the user provides a single display name, use it for all locales (same name everywhere).
- When the user provides translated names per locale, use the locale-specific name for each.
- If benefits or description are provided, include them. Otherwise omit them from the JSON.
- Use `--output table` for verification steps so the user can visually confirm.
- Use default JSON output for intermediate automation steps.
- After bulk updates, always get the subscription to verify completeness.
- If an update fails, log the product ID and error, then continue with remaining subscriptions. Report all failures together at the end.
- Always confirm exact flags with `--help` before running commands.

## Notes
- Subscription listings are updated atomically per subscription: one `update` call sets all locales at once.
- Unlike App Store Connect, Google Play does not require separate create calls per locale. The listings object is a single JSON field.
- The `--update-mask` flag is critical: without it, an update call may overwrite base plans and pricing.
- Title max length: 55 characters. Benefits max: 4 items. Description max: 80 characters.
- Use `--paginate` on list commands to ensure all subscriptions are returned.
- Use `--pretty` when inspecting JSON output for human readability.
- Always use `--help` to verify flags for the exact command.
