---
name: cardtrader-api
description: Interact with CardTrader REST API for trading card management. Handles authentication, marketplace operations (search products, cart, purchase), inventory management (list/create/update/delete products), order management (list/update/ship orders), and wishlist operations. Use for trading card marketplace integration, inventory sync, order fulfillment automation.
license: MIT
---

# CardTrader API Integration

Comprehensive guide for working with CardTrader's REST API to manage trading card marketplace operations.

## When to Use This Skill

Use this skill when working with:
- **Trading card marketplace operations** - buying, selling, searching for cards
- **Inventory management systems** - syncing stock with CardTrader, bulk updates
- **E-commerce integrations** - building apps or services that connect to CardTrader
- **Order fulfillment automation** - processing purchases, shipping orders
- **Price comparison tools** - searching marketplace for best prices
- **Collection management** - wishlists, tracking cards

**Do not use** for general e-commerce APIs, non-CardTrader marketplaces, or other trading card platforms (TCGplayer, Card Market, etc.).

## Base Configuration

**Base URL**: `https://api.cardtrader.com/api/v2`

**Authentication**: All requests require Bearer token authentication

```bash
Authorization: Bearer [YOUR_AUTH_TOKEN]
```

**Rate Limits**:

- General: 200 requests per 10 seconds
- Marketplace products: 10 requests per second
- Jobs: 1 request per second

## Core Concepts

- **Game**: Trading card game (e.g., Magic: The Gathering, Pokemon)
- **Category**: Item grouping within a game (Single Cards, Booster Box, etc.)
- **Expansion**: Specific game expansion/set (e.g., "Core Set 2020")
- **Blueprint**: Sellable item template with properties (language, condition, etc.)
- **Product**: Physical item for sale with quantity and price (you own this)
- **Order**: Purchase transaction (you sold or purchased products)

## Quick Start

### Test Authentication

```bash
curl https://api.cardtrader.com/api/v2/info \
-H "Authorization: Bearer [YOUR_AUTH_TOKEN]"
```

### Common Workflow: Sell a Card

1. Get games: `GET /games`
2. Get expansions: `GET /expansions`
3. Find blueprint: `GET /blueprints/export?expansion_id={id}`
4. Create product: `POST /products` with blueprint_id, price, quantity

## Marketplace Operations

### Search Products

```bash
# By expansion
GET /marketplace/products?expansion_id={id}

# By blueprint (specific card)
GET /marketplace/products?blueprint_id={id}

# Filter by foil/language
GET /marketplace/products?blueprint_id={id}&foil=true&language=en
```

Response includes 25 cheapest products per blueprint with seller info, price, quantity.

**Response structure**: Keys are blueprint IDs, values are arrays of up to 25 products sorted by price.

**Example**: See [examples/marketplace-products.json](examples/marketplace-products.json)

### Cart & Purchase Flow

1. **Add to cart**: `POST /cart/add`

   ```json
   {
     "product_id": 105234025,
     "quantity": 1,
     "via_cardtrader_zero": true,
     "billing_address": {...},
     "shipping_address": {...}
   }
   ```

2. **Check cart**: `GET /cart`

3. **Remove from cart** (optional): `POST /cart/remove`

4. **Purchase**: `POST /cart/purchase`

### Wishlists

- List: `GET /wishlists?game_id={id}`
- Show: `GET /wishlists/{id}` - See [examples/wishlist.json](examples/wishlist.json) for response
- Create: `POST /wishlists`
- Delete: `DELETE /wishlists/{id}`

## Inventory Management

### List Your Products

```bash
# All products (may take 120-180s for large collections)
GET /products/export

# Filter by blueprint
GET /products/export?blueprint_id={id}

# Filter by expansion
GET /products/export?expansion_id={id}
```

### Single Product Operations

**Create**:

```bash
POST /products
{
  "blueprint_id": 16,
  "price": 62.58,
  "quantity": 1,
  "error_mode": "strict",  # optional: fail on invalid properties
  "user_data_field": "warehouse B, shelf 10C",  # optional
  "properties": {
    "condition": "Near Mint",
    "mtg_language": "en",
    "mtg_foil": false
  }
}
```

**Update**: `PUT /products/{id}` (same body as create)

**Delete**: `DELETE /products/{id}`

**Increment/Decrement**:

```bash
POST /products/{id}/increment
{"delta_quantity": 4}
```

**Images**:

- Add: `POST /products/{id}/upload_image` (multipart form-data)
- Remove: `DELETE /products/{id}/upload_image`

### Batch Operations (Recommended for Multiple Products)

All batch operations are **asynchronous** and return a `job` UUID for status checking.

**Create**: `POST /products/bulk_create`

```json
{
  "products": [
    {
      "blueprint_id": 13,
      "price": 3.5,
      "quantity": 4
    },
    {...}
  ]
}
```

**Update**: `POST /products/bulk_update`

```json
{
  "products": [
    { "id": 3936985, "quantity": 4 },
    { "id": 3936986, "price": 2.5 }
  ]
}
```

**Delete**: `POST /products/bulk_destroy`

```json
{
  "products": [{ "id": 3936985 }, { "id": 3936986 }]
}
```

**Check job status**: `GET /jobs/{uuid}`

Job states: `pending` → `running` → `completed` (or `unprocessable` on error)

### CSV Import/Export

**Upload CSV**:

```bash
POST /product_imports
-F csv=@path_to_csv.csv
-F game_id=1
-F replace_stock_or_add_to_stock=replace_stock  # or add_to_stock
-F column_names=expansion_code|_|name|quantity|language|condition|_|price_cents
```

Required column combinations (at least one):

- name + expansion_code/expansion_name/expansion_id
- collector_number + expansion_code/expansion_name/expansion_id
- mkm_id, tcgplayer_id, scryfall_id, or blueprint_id

**Check import status**: `GET /product_imports/{id}`

**Get skipped items**: `GET /product_imports/{id}/skipped`

## Order Management

### List Orders

```bash
GET /orders?page=1&limit=20&from=2019-01-01&to=2019-03-01&state=paid&order_as=seller
```

Parameters:

- `page`, `limit`: Pagination (default: page=1, limit=20)
- `from`, `to`: Date range (YYYY-MM-DD)
- `from_id`, `to_id`: ID range filtering
- `state`: Filter by order state
- `order_as`: Your role (`seller` or `buyer`)
- `sort`: `id.asc`, `id.desc`, `date.asc`, `date.desc`

### Order States & Lifecycle

**Standard Orders**:
`paid` → `sent` → `arrived` → `done`

**CardTrader Zero Orders**:
`hub_pending` → `paid` → `sent` → `arrived` → `done`

**Special States**: `request_for_cancel`, `canceled`, `lost`

### Order Operations

**Get order details**: `GET /orders/{id}`

**Set tracking code**:

```bash
PUT /orders/{id}/tracking_code
{"tracking_code": "ABC123"}
```

(Required BEFORE shipping CardTrader Zero orders)

**Mark as shipped**: `PUT /orders/{id}/ship`

**Request cancellation**:

```bash
PUT /orders/{id}/request-cancellation
{"cancel_explanation": "Reason (min 50 chars)", "relist_if_cancelled": true}
```

**Confirm cancellation**: `PUT /orders/{id}/confirm-cancellation`

### CardTrader Zero Inventory Decrementing

When to decrement stock for CardTrader Zero orders:

| State       | via_cardtrader_zero | Decrement? |
| ----------- | ------------------- | ---------- |
| hub_pending | true                | Yes\*      |
| paid        | true                | No         |
| paid        | false               | Yes        |

\*For pre-sale enabled accounts, also check: order `id` == order_item `hub_pending_order_id`

### CT0 Box Items

- List your CT0 Box: `GET /ct0_box_items`
- Get item details: `GET /ct0_box_items/{id}`

## Reference Data

### Games

```bash
GET /games
# Returns: [{"id": 1, "name": "Magic", "display_name": "Magic: the Gathering"}]
```

### Categories

```bash
GET /categories?game_id={id}
# Returns categories with their properties
```

### Expansions

```bash
GET /expansions
```

**Example**: See [examples/expansions.json](examples/expansions.json)

Your expansions only:
```bash
GET /expansions/export
```

### Blueprints

```bash
GET /blueprints/export?expansion_id={id}
```

**Example**: See [examples/blueprints.json](examples/blueprints.json)

Key fields:

- `editable_properties`: Available properties for creating products (with type, default values, and possible values)
- `scryfall_id`, `card_market_ids`, `tcg_player_id`: External IDs

### Properties

Properties define item characteristics (condition, language, foil, etc.). Each property has:

- `name`: Identifier (e.g., "condition", "mtg_foil")
- `type`: "string" or "boolean"
- `possible_values`: Array of allowed values

Common Magic properties:

- `condition`: Mint, Near Mint, Slightly Played, Moderately Played, Played, Heavily Played, Poor
- `mtg_language`: en, it, fr, jp, etc.
- `mtg_foil`: true/false
- `signed`, `altered`: true/false

### Shipping Methods

```bash
GET /shipping_methods?username={seller_username}
```

Returns available shipping methods from a seller to you.

## Webhooks

CardTrader can POST to your endpoint when orders are created, updated, or deleted.

**Webhook payload**:

```json
{
  "id": "uuid",
  "time": 1632240962,
  "cause": "order.update",  // or order.create, order.destroy
  "object_class": "Order",
  "object_id": 733733,
  "mode": "live",  // or test
  "data": {...}  // Order object (empty for destroy)
}
```

**Verify authenticity**: Check `Signature` header = base64(HMAC-SHA256(body, shared_secret))

## Error Handling

**401 Unauthorized**: Invalid/missing Bearer token

```json
{ "error_code": "unauthorized", "errors": [], "extra": { "message": "..." } }
```

**404 Not Found**: Resource doesn't exist

```json
{ "error_code": "not_found", "errors": [], "extra": { "message": "..." } }
```

**422 Unprocessable Entity**: Missing/invalid parameters

```json
{
  "error_code": "missing_parameter",
  "errors": [],
  "extra": { "message": "..." }
}
```

**429 Rate Limit**:

```json
{ "error": "Too many requests: max 200 requests per 10 seconds" }
```

## Best Practices

1. **Use batch operations** for multiple products (more efficient than single operations)
2. **Set large timeouts** for `/products/export` (120-180s for large inventories)
3. **Use `error_mode: "strict"`** during development to catch property errors
4. **Check job status** after batch operations before assuming success
5. **Handle rate limits** with exponential backoff
6. **Use `user_data_field`** to store your internal IDs/references
7. **For CardTrader Zero**, set tracking code BEFORE shipping
8. **Cache reference data** (games, expansions, categories) - they change infrequently

## Common Patterns

### Sync External Inventory to CardTrader

1. Export your inventory: `GET /products/export`
2. Compare with your system
3. Use `POST /products/bulk_create` for new items
4. Use `POST /products/bulk_update` for changed items
5. Use `POST /products/bulk_destroy` for removed items
6. Check job status: `GET /jobs/{uuid}`

### Process New Orders

1. Poll for new orders: `GET /orders?state=paid&order_as=seller`
2. For each order:
   - Decrement local inventory
   - Prepare shipment
   - Set tracking: `PUT /orders/{id}/tracking_code`
   - Mark shipped: `PUT /orders/{id}/ship`

### Search Best Price for Card

1. Get blueprint_id (from expansion or by name)
2. `GET /marketplace/products?blueprint_id={id}`
3. Filter by condition/language in response
4. Take first item (sorted by price ascending)

## Additional Resources

- Postman Collection: Available at CardTrader API docs with pre-configured auth
- API Token: Obtain from CardTrader profile settings page: `https://www.cardtrader.com/en/docs/api/full/reference`
