---
name: producthunt
description: Search Product Hunt launches, products, and makers via the GraphQL V2 API. Use when the user asks about Product Hunt launches, trending products, or wants to research a product's reception. Requires a free developer token (~2 min setup).
---

# Product Hunt Search & Monitoring

Search for products, track launches, and monitor Product Hunt activity via the GraphQL V2 API.

## When to Use

- User asks about a product's Product Hunt launch or performance
- User wants to find trending products in a category
- User wants to monitor Product Hunt for competitors or similar products
- User asks "what launched on Product Hunt today/this week"
- User wants to research a product's reception on PH

## Requirements

**API Token Required.** The Product Hunt API requires authentication — but it's **free and takes ~2 minutes** to set up.

### Getting a Token

1. Go to [API Dashboard](https://www.producthunt.com/v2/oauth/applications)
2. Create an application (any name/URL works)
3. Use the **Developer Token** at the bottom of your app's page (no OAuth flow needed for read-only access)
4. Store the token in an environment variable: `PH_API_TOKEN`

If no token is available, fall back to using `web_search` with `site:producthunt.com` queries.

## Key Limitation: No Text Search

The Product Hunt API **does not support free-text search on posts**. You can browse by topic, date, or get a specific post by slug — but you cannot search "AI writing tool" and get matching products.

**To find a product by name**, use `web_search` first:
```
web_search: site:producthunt.com/posts "product name"
```
Then use the slug from the result to query the API for full details (votes, comments, makers, etc.).

## API Overview

- **Endpoint:** `https://api.producthunt.com/v2/api/graphql`
- **Method:** POST
- **Auth:** `Authorization: Bearer {token}`
- **Format:** GraphQL
- **Rate Limit:** ~900 requests per 15 minutes, complexity limit of 1000 per query

## How to Query

Use `exec` with `curl` to make GraphQL requests:

```bash
curl -s -X POST https://api.producthunt.com/v2/api/graphql \
  -H "Authorization: Bearer $PH_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "YOUR_GRAPHQL_QUERY"}'
```

## Common Queries

### Today's Top Posts

```graphql
query {
  posts(order: VOTES, first: 10) {
    edges {
      node {
        id
        name
        tagline
        votesCount
        commentsCount
        url
        website
        createdAt
        makers {
          name
          username
        }
        topics {
          edges {
            node {
              name
            }
          }
        }
      }
    }
  }
}
```

### Browse Posts by Topic

```graphql
query {
  posts(order: VOTES, first: 10, topic: "developer-tools") {
    edges {
      node {
        id
        name
        tagline
        votesCount
        url
        website
      }
    }
  }
}
```

**Remember:** This browses a topic — it's not a text search. To find a specific product by name, use `web_search` with `site:producthunt.com/posts "product name"`, then look up the post by slug via the API.

### Get a Specific Post

```graphql
query {
  post(slug: "chatgpt") {
    id
    name
    tagline
    description
    votesCount
    commentsCount
    reviewsCount
    reviewsRating
    url
    website
    createdAt
    featuredAt
    makers {
      name
      username
      headline
    }
    topics {
      edges {
        node {
          name
          slug
        }
      }
    }
    comments(first: 5) {
      edges {
        node {
          body
          votesCount
          createdAt
          user {
            name
            username
          }
        }
      }
    }
  }
}
```

### Get Posts by Topic

```graphql
query {
  topic(slug: "artificial-intelligence") {
    name
    postsCount
    posts(first: 10, order: VOTES) {
      edges {
        node {
          name
          tagline
          votesCount
          url
          createdAt
        }
      }
    }
  }
}
```

### Get Posts for a Specific Date

```graphql
query {
  posts(postedAfter: "2024-01-15T00:00:00Z", postedBefore: "2024-01-16T00:00:00Z", order: VOTES, first: 10) {
    edges {
      node {
        name
        tagline
        votesCount
        url
      }
    }
  }
}
```

### Look Up a User

```graphql
query {
  user(username: "rrhoover") {
    name
    username
    headline
    followersCount
    followingCount
    madePosts(first: 5) {
      edges {
        node {
          name
          tagline
          votesCount
          url
        }
      }
    }
  }
}
```

## Available Topics (Common Slugs)

- `artificial-intelligence`, `developer-tools`, `design-tools`
- `productivity`, `marketing`, `saas`, `fintech`
- `no-code`, `open-source`, `social-media`
- `web-app`, `iphone`, `android`, `mac`, `chrome-extensions`

For a full list, query:
```graphql
query { topics(first: 50, order: FOLLOWERS_COUNT) { edges { node { name slug followersCount } } } }
```

## Constructing Product Hunt Links

- **Product page:** `https://www.producthunt.com/posts/{slug}`
- **User profile:** `https://www.producthunt.com/@{username}`
- **Topic page:** `https://www.producthunt.com/topics/{slug}`

## Fallback: No API Token

If no `PH_API_TOKEN` is available:

1. Use `web_search` with queries like:
   - `site:producthunt.com/posts "product name"`
   - `site:producthunt.com "topic" launched`
2. Use `web_fetch` on specific Product Hunt URLs to get basic info
3. Inform the user that richer data (vote counts, comments, maker info) requires an API token

## Output Format

```
### Product Hunt Results

1. **Product Name** — Tagline
   🔼 votes · 💬 comments · ⭐ rating
   By @maker_username
   Topics: AI, Developer Tools
   🔗 product_url
   🏠 website_url
   📅 launched_date

2. ...
```

## Error Handling

- **401 Unauthorized:** Token is invalid or expired. Check `PH_API_TOKEN`.
- **429 Rate Limited:** Wait 15 minutes for rate limit reset.
- **Complexity limit exceeded:** Reduce the number of fields or nested queries. Remove `comments`, `topics`, or `makers` sub-queries.
- **Post not found:** The slug may be wrong. Try searching with `web_search` first to confirm the exact slug.
- **No results for topic:** Check the topic slug — use the topics query to find valid slugs.

## Examples

### Example 1: "What launched on Product Hunt today?"

Query today's posts sorted by votes, present top 10.

### Example 2: "How did Linear do on Product Hunt?"

1. Search: `web_search "site:producthunt.com/posts linear"`
2. Get the slug from results
3. Query: `post(slug: "linear-5")` with full details

### Example 3: "Show me top AI tools on Product Hunt this month"

1. Query posts by topic `artificial-intelligence` with date filters
2. Sort by votes, present top results

## Data Source

[Product Hunt API V2](https://api.producthunt.com/v2/docs) — GraphQL API, requires free developer token.
