---
name: cn-ecommerce-search
description: >
  Search products on Chinese e-commerce platforms including Taobao, Tmall, 1688, and AliExpress.
  Parse product links, get product details, compare prices across platforms.
  Use when the user asks to find products, get product info by URL, search Chinese suppliers, or compare prices.
license: MIT
metadata:
  author: shopme
  version: "1.0.0"
  mcp-server: "@shopme/cn-ecommerce-search-mcp"
---

# Chinese E-commerce Product Search

Search and retrieve product information from Taobao, Tmall, 1688, and AliExpress.

## When to Use

- User asks to find a product on Taobao, 1688, or AliExpress
- User shares a product link and wants details
- User needs to search Chinese suppliers for a product
- User asks about prices on Chinese platforms
- User provides a product URL that looks like it's from a Chinese e-commerce site

## MCP Server Setup

```json
{
  "mcpServers": {
    "cn-ecommerce-search": {
      "command": "npx",
      "args": ["-y", "@shopme/cn-ecommerce-search-mcp"],
      "env": {
        "TAOBAO_APP_KEY": "your-key",
        "TAOBAO_APP_SECRET": "your-secret",
        "TAOBAO_ACCESS_TOKEN": "your-token",
        "ALIEXPRESS_DS_KEY": "your-key",
        "ALIEXPRESS_DS_SECRET": "your-secret"
      }
    }
  }
}
```

## Available Tools

### search_products
Search products by keyword across platforms.
- `keyword`: Search term (Chinese or English)
- `platform`: "taobao", "aliexpress", or "all" (default)
- `sort`: PRICE_ASC, PRICE_DESC, SALE_QTY_DESC
- `pageNo`, `pageSize`: Pagination

### get_product_detail
Get detailed info about a specific product.
- `productId`: The product's ID
- `platform`: "taobao" or "aliexpress"

### parse_product_link
Parse a product URL to identify the platform and product ID.
- `url`: Any product URL or text containing one

### get_product_from_url
One-step: parse URL + fetch product details.
- `url`: Product URL from any supported platform

## Platform Guide

| Platform | Strengths | Price Range | Typical Buyer |
|----------|-----------|-------------|---------------|
| **Taobao** | Largest selection, consumer goods | ¥ Low-Mid | End consumers |
| **Tmall** | Brand flagship stores, higher quality | ¥ Mid-High | Quality-focused |
| **1688** | Wholesale/factory direct, bulk pricing | ¥ Lowest | Resellers, businesses |
| **AliExpress** | International shipping, buyer protection | $ Mid | International buyers |

## Supported URL Formats

- `item.taobao.com/item.htm?id=123456`
- `detail.tmall.com/item.htm?id=123456`
- `detail.1688.com/offer/123456.html`
- `aliexpress.com/item/123456.html`
- `aliexpress.com/i/123456.html`
- `mall.xiaohongshu.com/goods-detail/xxx`
- Short links: `e.tb.cn/xxx`, `m.tb.cn/xxx`

## Price Understanding Guide

- Taobao/Tmall prices are in CNY (¥). Rough conversion: 1 USD ≈ 7.2 CNY
- AliExpress shows prices in buyer's currency (usually USD)
- 1688 prices are factory/wholesale prices in CNY, often much lower
- Always consider shipping costs when comparing prices

## Search Tips

1. **Chinese keywords** get better results on Taobao/1688
2. **English keywords** work well on AliExpress
3. Sort by `SALE_QTY_DESC` to find popular/trusted products
4. Compare the same product across Taobao and AliExpress to find price gaps
5. 1688 often has the same product at 30-70% lower price than Taobao (wholesale)
