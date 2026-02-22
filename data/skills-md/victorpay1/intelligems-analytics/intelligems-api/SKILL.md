---
name: intelligems-api
description: Load Intelligems External API context before building API integrations. Use when starting to build any API use case for Intelligems.
author: Victorpay1
version: 1.0.0
tags:
  - api
  - intelligems
  - ecommerce
  - ab-testing
---

# /intelligems-api

Load the Intelligems External API documentation before building integrations.

---

## When to Use This Skill

- Starting to build an API integration for Intelligems
- Creating a health check, monitoring, or reporting script
- Building any automation that uses Intelligems data

---

## Step 1: Read the Documentation (MANDATORY)

Read the bundled documentation file:

**`references/external-api.md`**

This contains:
- API overview and capabilities
- Authentication method (`intelligems-access-token` header)
- All endpoints: experiences-list, experiences/{id}, analytics
- Response structures and available metrics
- Python code examples
- Health check formulas and thresholds
- Slack integration tutorial

---

## Step 2: Check Live Docs (OPTIONAL)

If the bundled docs seem outdated or you need additional context, check the live documentation:

1. **Main API Docs:**
   https://docs.intelligems.io/developer-resources/external-api/default

2. **Slack Integration Tutorial:**
   https://docs.intelligems.io/developer-resources/external-api/build-an-automated-test-monitoring-integration-for-slack

Only do this if:
- The user asks to check for updates
- The bundled docs are missing information needed for the use case
- Building something not covered in the bundled docs

---

## Step 3: Confirm Ready

After reading the documentation, confirm you're ready:

> "Got it. I've loaded the Intelligems External API context:
> - Base URL: `https://api.intelligems.io/v25-10-beta`
> - Auth: `intelligems-access-token` header
> - Key endpoints: experiences-list, experiences/{id}, analytics/resource/{id}
>
> What are we building?"

---

## Quick Reference

**Base URL:** `https://api.intelligems.io/v25-10-beta`

**Authentication:**
```
intelligems-access-token: your_api_key_here
```

**Main Endpoints:**
| Endpoint | Purpose |
|----------|---------|
| GET /experiences-list | List all tests/experiences |
| GET /experiences/{id} | Get full test details |
| GET /analytics/resource/{id} | Get analytics data |

**Key Metrics (Intelligems Priority):**
- `net_revenue_per_visitor` - Revenue/visitor (**north star**)
- `gross_profit_per_visitor` - Profit/visitor (requires COGS)
- `conversion_rate` - Conversion rate
- `net_revenue_per_order` - AOV
- `n_visitors` - Visitors
- `n_orders` - Orders
- `pct_revenue_with_cogs` - Check if COGS data exists (0 = no COGS)

**Confidence:** `p2bb` = Probability to Beat Baseline (not `confidence`)

**Health Check Thresholds (Intelligems Philosophy):**
- MIN_RUNTIME_DAYS: 10
- MIN_VISITORS: 100
- MIN_ORDERS: 10
- MIN_CONFIDENCE: 80% ("we're not making cancer medicine")

---

## Common Use Cases

When the user wants to build...

| Use Case | What You Need |
|----------|---------------|
| Health check bot | experiences-list + analytics endpoints |
| Slack notifications | Add Slack webhook, format messages |
| Data export | Analytics endpoint with date ranges |
| Custom dashboard | All endpoints, audience segmentation |
| Test monitoring | experiences-list (status=started) + analytics |

---

## Notes

- API is in beta - contact support@intelligems.io for access
- Feature suggestions go to jerica@intelligems.io
- Python examples are in the bundled documentation
