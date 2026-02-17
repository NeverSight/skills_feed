---
name: cross-border-price-compare
description: >
  Compare product prices across Taobao, 1688, AliExpress and other platforms with landed cost estimation.
  Calculate total cost including shipping, duties, and taxes for cross-border purchases.
  Use when the user asks to compare prices, estimate shipping costs, calculate import duties, or find the cheapest source.
license: MIT
metadata:
  author: shopme
  version: "1.0.0"
  mcp-server: "@shopme/cross-border-price-compare-mcp"
---

# Cross-border Price Comparison

Compare prices across Chinese e-commerce platforms and calculate total landed cost including shipping, duties, and taxes.

## When to Use

- User asks "which platform is cheapest for X?"
- User wants to know total cost of importing a product
- User needs shipping cost estimates from China
- User asks about import duties or taxes
- User wants to compare 1688 wholesale vs Taobao retail vs AliExpress prices
- User asks to convert between CNY and other currencies

## MCP Server Setup

```json
{
  "mcpServers": {
    "cross-border-price-compare": {
      "command": "npx",
      "args": ["-y", "@shopme/cross-border-price-compare-mcp"]
    }
  }
}
```

No API keys required! This MCP uses built-in calculation logic.

## Available Tools

### compare_price
Compare prices from multiple sources with full landed cost breakdown.
- `sources`: Array of products (platform, name, price in CNY or USD, weight)
- `category`: Product category for duty estimation
- `destination`: Country code
- `shippingMethod`: economy/standard/express/premium
- Returns: ranked results with savings calculation

### calculate_landed_cost
Get detailed cost breakdown for a single product.
- `priceCny` or `priceUsd`: Product price
- `weightKg`: Package weight
- `category`: For duty rate lookup
- `destination`: Country code
- `shippingMethod`: Shipping speed tier
- Returns: full breakdown (product + shipping + duty + tax = total)

### estimate_shipping
Compare shipping options and costs.
- `weightKg`: Package weight
- `destination`: Country code
- Returns: all shipping tier options with cost and delivery time

### convert_currency
Quick currency conversion between major currencies.
- `amount`: Amount to convert
- `from`/`to`: Currency codes (CNY, USD, HKD, EUR, GBP, JPY, KRW, etc.)

## Price Comparison Strategies

### Quick Price Check
1. Search for the product on each platform
2. Note the price and currency (Taobao=CNY, AliExpress=USD)
3. Use `compare_price` with all sources to get ranked results

### Full Cost Analysis
1. Identify product on multiple platforms
2. Estimate weight (check product specs or estimate)
3. Use `calculate_landed_cost` for each
4. Compare total costs, not just product prices

### Key Insight: Don't Compare Unit Prices Alone!
A ¥50 product on Taobao ≠ $7 on AliExpress because:
- Taobao: ¥50 product + ¥30 international shipping = $11.10 total
- AliExpress: $7 product + $0 shipping (free) = $7 total
- In this case, AliExpress is cheaper despite higher unit price!

## Shipping Tiers

| Method | Cost/kg | Delivery | Best For |
|--------|---------|----------|----------|
| Economy | ~$5 | 15-30 days | Low value, not urgent |
| Standard | ~$10 | 10-20 days | Most purchases |
| Express | ~$20 | 5-10 days | Moderate urgency |
| Premium | ~$35 | 3-7 days | High value, urgent |

## Import Duty Quick Reference (US)

- **$800 de minimis**: No duty on orders under $800 (US only)
- Electronics: 0% duty
- Clothing: ~12% duty
- Shoes: ~20% duty
- Cosmetics: ~6.5% duty
- Bags: ~20% duty
- Toys: 0% duty

## Common Cross-border Routes

| From → To | Typical Time | Customs Risk |
|-----------|-------------|--------------|
| China → US | 10-20 days | Low (<$800 duty-free) |
| China → UK | 15-25 days | Medium (20% VAT from £135) |
| China → EU | 15-30 days | Medium (VAT from €22) |
| China → HK | 3-5 days | Very Low (duty-free port) |
| China → JP | 5-10 days | Medium (10% consumption tax) |
