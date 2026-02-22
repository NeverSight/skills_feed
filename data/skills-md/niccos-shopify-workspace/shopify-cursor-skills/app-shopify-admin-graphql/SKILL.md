---
name: app-shopify-admin-graphql
description: Execute Shopify Admin API calls via GraphQL in Shopify Remix apps. Use when querying or mutating Shopify data (customers, orders, products, shop, segments, subscriptions), when writing GraphQL for the Admin API, or when handling throttling and retries.
---

# Shopify Admin GraphQL

Use this skill when adding or changing code that talks to the Shopify Admin API via GraphQL.

## When to Use

- Querying Shopify data (shop, customers, orders, products, inventory)
- Mutating Shopify data (creating/updating customers, orders, products)
- Implementing pagination for large datasets
- Handling API throttling and rate limits
- Working with metafields or other Shopify resources

## Getting the GraphQL Client

### In Remix Loaders/Actions (Recommended)

Use `authenticate.admin()` from `@shopify/shopify-app-remix`:

```typescript
import { authenticate } from "../shopify.server";

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const { admin } = await authenticate.admin(request);
  
  const response = await admin.graphql(`
    query GetShopDetails {
      shop {
        id
        name
        myshopifyDomain
        plan {
          displayName
        }
      }
    }
  `);
  
  const { data } = await response.json();
  return json({ shop: data.shop });
};
```

### With Variables

```typescript
export const action = async ({ request }: ActionFunctionArgs) => {
  const { admin } = await authenticate.admin(request);
  const formData = await request.formData();
  const email = formData.get("email") as string;
  
  // Validate email format to prevent query manipulation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!email || !emailRegex.test(email)) {
    return json({ error: "Invalid email format" }, { status: 400 });
  }
  
  // Escape quotes and wrap in quotes to treat as literal value
  const sanitizedEmail = email.replace(/"/g, '\\"');
  
  const response = await admin.graphql(`
    query FindCustomerByEmail($query: String!) {
      customers(first: 1, query: $query) {
        edges {
          node {
            id
            email
            phone
            firstName
            lastName
          }
        }
      }
    }
  `, {
    variables: { query: `email:"${sanitizedEmail}"` }
  });
  
  const { data } = await response.json();
  return json({ customer: data.customers.edges[0]?.node });
};
```

### Background Jobs / Webhooks (Offline Access)

When you don't have a request context, use offline session tokens:

```typescript
import { unauthenticated } from "../shopify.server";

export async function processWebhook(shop: string) {
  const { admin } = await unauthenticated.admin(shop);
  
  const response = await admin.graphql(`
    query GetShop {
      shop {
        name
      }
    }
  `);
  
  const { data } = await response.json();
  return data.shop;
}
```

## Common Query Patterns

### Shop Details

```graphql
query GetShopDetails {
  shop {
    id
    name
    email
    myshopifyDomain
    primaryDomain {
      url
    }
    plan {
      displayName
    }
    currencyCode
    timezoneAbbreviation
  }
}
```

### Products with Pagination

```graphql
query GetProducts($first: Int!, $after: String) {
  products(first: $first, after: $after) {
    pageInfo {
      hasNextPage
      endCursor
    }
    edges {
      node {
        id
        title
        handle
        status
        variants(first: 10) {
          edges {
            node {
              id
              title
              price
              sku
            }
          }
        }
      }
    }
  }
}
```

### Customer Lookup

```graphql
query FindCustomer($query: String!) {
  customers(first: 1, query: $query) {
    edges {
      node {
        id
        email
        phone
        firstName
        lastName
        ordersCount
        totalSpent
      }
    }
  }
}
```

### Order by ID

```graphql
query GetOrder($id: ID!) {
  order(id: $id) {
    id
    name
    email
    phone
    totalPriceSet {
      shopMoney {
        amount
        currencyCode
      }
    }
    lineItems(first: 50) {
      edges {
        node {
          title
          quantity
          variant {
            id
            sku
          }
        }
      }
    }
    shippingAddress {
      address1
      city
      country
    }
  }
}
```

## Handling Throttling

Shopify uses a leaky bucket algorithm for rate limiting. For bulk operations or background jobs, implement retry logic:

```typescript
interface RetryOptions {
  maxRetries?: number;
  initialDelay?: number;
  maxDelay?: number;
}

async function executeWithRetry<T>(
  admin: AdminApiContext,
  query: string,
  variables?: Record<string, unknown>,
  options: RetryOptions = {}
): Promise<T> {
  const { maxRetries = 3, initialDelay = 1000, maxDelay = 10000 } = options;
  
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      const response = await admin.graphql(query, { variables });
      const result = await response.json();
      
      if (result.errors?.some((e: any) => e.extensions?.code === "THROTTLED")) {
        throw new Error("THROTTLED");
      }
      
      return result.data as T;
    } catch (error) {
      if (attempt === maxRetries) throw error;
      
      const delay = Math.min(initialDelay * Math.pow(2, attempt), maxDelay);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  
  throw new Error("Max retries exceeded");
}
```

## Error Handling

```typescript
const response = await admin.graphql(query, { variables });
const { data, errors } = await response.json();

if (errors) {
  // Handle GraphQL errors
  console.error("GraphQL errors:", errors);
  
  // Check for specific error types
  const throttled = errors.some((e: any) => 
    e.extensions?.code === "THROTTLED"
  );
  
  const notFound = errors.some((e: any) => 
    e.message?.includes("not found")
  );
  
  if (throttled) {
    // Retry with backoff
  }
}
```

## Best Practices

1. **Use operation names** for debugging: `query GetShopDetails { ... }`
2. **Request only needed fields** to reduce response size and improve performance
3. **Use pagination** for lists - never request unbounded data
4. **Handle errors gracefully** - check for both `errors` array and HTTP errors
5. **Implement retries with exponential backoff** for background jobs
6. **Use fragments** for repeated field selections across queries
7. **Prefer GraphQL over REST** for complex queries with relationships

## References

- [Shopify Admin GraphQL API](https://shopify.dev/docs/api/admin-graphql)
- [GraphQL Basics](https://shopify.dev/docs/api/usage/graphql-basics)
- [Rate Limits](https://shopify.dev/docs/api/usage/rate-limits)
- [@shopify/shopify-app-remix](https://shopify.dev/docs/api/shopify-app-remix)
