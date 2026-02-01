---
name: checkout-directory
description: Discover merchants supporting agentic commerce protocols (UCP, ACP). Use when users want to buy products online, find merchants by category, check UCP/ACP protocol support, or get merchant API endpoints for programmatic checkout.
---

# Checkout Directory Skill

You can discover merchants that support agentic commerce protocols using the checkout.directory API.

## When to Use This Skill

Use this skill when:
- A user wants to buy something online
- You need to find merchants in a specific category
- You need to check if a merchant supports UCP/ACP
- You need a merchant's API endpoints to complete a purchase

## API Endpoints

Base URL: `https://checkout.directory`

### List/Search Merchants

```
GET /api/merchants
GET /api/merchants?q={search_term}
GET /api/merchants?category={category}
GET /api/merchants?protocol={ucp|acp}
```

Response:
```json
[
  {
    "domain": "allbirds.com",
    "name": "Allbirds",
    "category": "Footwear",
    "protocols": ["ucp"],
    "endpoints": {
      "ucp": "https://allbirds.com/.well-known/ucp"
    }
  }
]
```

### Get Merchant Details

```
GET /api/merchants/{domain}
```

Returns a single merchant object.

### Get Merchant Manifest

```
GET /api/merchants/{domain}/manifest
```

Returns the full UCP/ACP manifest from the merchant's endpoint. Use this to discover:
- Available capabilities (checkout, fulfillment, etc.)
- MCP endpoint for programmatic interaction
- Payment handlers supported

## Example Workflow

**User:** "I want to buy running shoes"

**Agent steps:**

1. Search for footwear merchants:
   ```
   GET https://checkout.directory/api/merchants?category=footwear
   ```

2. Pick a relevant merchant (e.g., Allbirds)

3. Get their manifest:
   ```
   GET https://checkout.directory/api/merchants/allbirds.com/manifest
   ```

4. Use the MCP endpoint from the manifest to:
   - Search products
   - Add to cart
   - Complete checkout

## Protocols

### UCP (Universal Checkout Protocol)

Merchants with UCP support expose endpoints at `/.well-known/ucp` with capabilities for:
- Product search and browsing
- Cart management
- Checkout flow
- Fulfillment tracking

### ACP (Agent Commerce Protocol)

Coming soon. Will enable more advanced agent-merchant interactions.

## Tips

- Always check the `protocols` array to confirm what a merchant supports
- Use the manifest's `capabilities` to understand what actions are available
- The MCP endpoint in the manifest is what you use for actual transactions
- Respect rate limits: don't poll the API excessively
