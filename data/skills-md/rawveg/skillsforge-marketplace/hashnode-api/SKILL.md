---
name: hashnode-api
description: Hashnode GraphQL API documentation for creating, managing, and querying blogs, posts, publications, and user data on the Hashnode platform
---

# Hashnode API Skill

Comprehensive assistance with the Hashnode GraphQL API for blog management, content creation, and user interaction on the Hashnode platform.

## When to Use This Skill

This skill should be triggered when:
- Building integrations with Hashnode blogs or publications
- Querying Hashnode posts, users, or publication data
- Creating, publishing, or managing blog posts via API
- Implementing authentication with Hashnode Personal Access Tokens
- Working with GraphQL queries or mutations for Hashnode
- Debugging Hashnode API responses or error codes
- Setting up pagination (cursor-based or offset-based) for Hashnode data
- Implementing newsletter subscriptions, comments, or user interactions
- Migrating from the legacy Hashnode API to the new GQL endpoint

## Key Concepts

### API Endpoint
All Hashnode API requests go through a single GraphQL endpoint:
- **Endpoint:** `https://gql.hashnode.com` (POST only)
- **Playground:** Visit the same URL in a browser to explore the API
- **Legacy API:** `https://api.hashnode.com` is discontinued - migrate to new endpoint

### Authentication
- Most queries work without authentication
- Sensitive fields (drafts, email, etc.) require authentication
- All mutations require authentication
- **Authentication method:** Add `Authorization` header with your Personal Access Token (PAT)
- **Get your PAT:** https://hashnode.com/settings/developer → "Generate New Token"

### Rate Limits
- **Queries:** 20,000 requests per minute
- **Mutations:** 500 requests per minute

### Caching
- Almost all query responses are cached on the Edge
- Cache is automatically purged when you mutate data
- Check cache status in playground (bottom right: HIT/MISS)
- **Important:** Always request the `id` field to avoid stale data

### Error Codes
Common GraphQL error codes:
- `GRAPHQL_VALIDATION_FAILED` - Invalid query structure
- `UNAUTHENTICATED` - Missing or invalid auth token
- `FORBIDDEN` - Insufficient permissions
- `BAD_USER_INPUT` - Invalid input data
- `NOT_FOUND` - Resource doesn't exist

## Quick Reference

### 1. Fetch Publication Details

```graphql
query Publication {
  publication(host: "blog.developerdao.com") {
    id
    isTeam
    title
    about {
      markdown
    }
  }
}
```

Get basic information about a publication by its hostname.

### 2. Fetch Recent Blog Posts

```graphql
query Publication {
  publication(host: "blog.developerdao.com") {
    id
    isTeam
    title
    posts(first: 10) {
      edges {
        node {
          id
          title
          brief
          url
        }
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
}
```

Retrieve the latest 10 posts from a publication with cursor-based pagination support.

### 3. Fetch a Single Article by Slug

```graphql
query Publication {
  publication(host: "blog.developerdao.com") {
    id
    post(slug: "the-developers-guide-to-chainlink-vrf-foundry-edition") {
      id
      title
      content {
        markdown
        html
      }
    }
  }
}
```

Get full content of a specific article using its slug and publication hostname.

### 4. Cursor-Based Pagination (Infinite Scroll)

```graphql
query Publication {
  publication(host: "blog.developerdao.com") {
    id
    posts(
      first: 10
      after: "NjQxZTc4NGY0M2NiMzc2YjAyNzNkMzU4XzIwMjMtMDMtMjVUMDQ6Mjc6NTkuNjQxWg=="
    ) {
      edges {
        node {
          id
          title
          brief
          url
        }
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
}
```

Use `endCursor` from previous response as `after` parameter to fetch next page.

### 5. Offset-Based Pagination (Traditional Pages)

```graphql
query Followers {
  user(username: "SandroVolpicella") {
    id
    followers(pageSize: 10, page: 1) {
      nodes {
        id
        username
      }
      pageInfo {
        hasNextPage
        hasPreviousPage
        previousPage
        nextPage
      }
    }
  }
}
```

Navigate between pages using explicit page numbers.

### 6. Get Entity Count (Series Count Example)

```graphql
query SeriesCount {
  publication(host: "engineering.hashnode.com") {
    id
    seriesList(first: 0) {
      totalDocuments
    }
  }
}
```

Result:
```json
{
  "data": {
    "publication": {
      "seriesList": {
        "totalDocuments": 3
      }
    }
  }
}
```

Use `totalDocuments` field to get counts without fetching all data.

### 7. Fetch Posts from a Series

```graphql
query Publication {
  publication(host: "lo-victoria.com") {
    id
    series(slug: "graphql") {
      id
      name
      posts(first: 10) {
        edges {
          node {
            id
            title
          }
        }
      }
    }
  }
}
```

Get all posts belonging to a specific series.

### 8. Fetch Static Pages

```graphql
query Publication {
  publication(host: "lo-victoria.com") {
    id
    staticPages(first: 10) {
      edges {
        node {
          id
          title
          slug
        }
      }
    }
  }
}
```

Retrieve custom static pages like "About", "Contact", etc.

### 9. Fetch Single Static Page

```graphql
query Publication {
  publication(host: "lo-victoria.com") {
    id
    staticPage(slug: "about") {
      id
      title
      content {
        markdown
      }
    }
  }
}
```

Get content of a specific static page by slug.

### 10. Authentication Example - Get Drafts (Requires Auth)

```graphql
query Publication($first: Int!, $host: String) {
  publication(host: $host) {
    id
    drafts(first: $first) {
      edges {
        node {
          id
          title
        }
      }
    }
  }
}
```

**Headers:**
```json
{
  "Authorization": "your-personal-access-token-here"
}
```

Variables:
```json
{
  "first": 10,
  "host": "your-blog-host.hashnode.dev"
}
```

Drafts can only be queried by the publication owner with valid authentication.

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **api.md** - Complete Hashnode GraphQL API documentation including:
  - GQL Playground overview
  - Caching behavior and best practices
  - Rate limits and authentication
  - Status codes and error handling
  - Pagination methods (cursor-based and offset-based)
  - Migration guide from legacy API
  - Query and mutation examples
  - Full list of available queries and mutations

Use the reference files for detailed information about specific API features, error handling patterns, and advanced query techniques.

## Working with This Skill

### For Beginners
Start by understanding the core concepts above, then explore:
1. **API Endpoint:** Test queries in the playground at https://gql.hashnode.com
2. **Authentication:** Generate your PAT at https://hashnode.com/settings/developer
3. **Basic Queries:** Try fetching publication details and blog posts first
4. **Pagination:** Start with cursor-based pagination for simple infinite scroll

### For Intermediate Users
Focus on:
1. **Authentication flows:** Implement PAT-based auth in your application
2. **Error handling:** Handle GraphQL error codes properly
3. **Pagination strategies:** Choose between cursor-based and offset-based based on your UI needs
4. **Caching considerations:** Always request `id` fields to avoid stale data
5. **Content extraction:** Work with both markdown and HTML content formats

### For Advanced Users
Explore:
1. **Mutations:** Publishing posts, managing drafts, updating content
2. **Complex queries:** Nested queries with multiple levels (publication → series → posts)
3. **Batch operations:** Optimize API calls with GraphQL field selection
4. **Webhook integration:** Handle Hashnode webhook events
5. **Rate limit optimization:** Implement efficient request batching

### Navigation Tips
- **Start broad → go deep:** Begin with publication queries, then drill into specific posts/series
- **Check authentication:** If you get `UNAUTHENTICATED` errors, verify your PAT is in the Authorization header
- **Test in playground:** Use https://gql.hashnode.com to test queries before implementing
- **Monitor cache:** Watch cache HIT/MISS status to optimize your queries
- **Read error messages:** GraphQL errors include helpful details in the `extensions.code` field

## Common Use Cases

### Building a Blog Frontend
1. Fetch publication metadata
2. Get post list with pagination
3. Display individual posts by slug
4. Implement series/category navigation
5. Show static pages (about, contact)

### Content Management Dashboard
1. Authenticate with PAT
2. List and manage drafts
3. Publish/update posts
4. Schedule content
5. Monitor analytics

### Newsletter Integration
1. Subscribe/unsubscribe users
2. Fetch subscriber counts
3. Manage email preferences
4. Track engagement metrics

### Migration from Legacy API
1. Update endpoint from `api.hashnode.com` to `gql.hashnode.com`
2. Convert REST calls to GraphQL queries
3. Update authentication mechanism (check docs)
4. Adjust pagination from old format to cursor/offset-based
5. Update error handling for new error codes

## Resources

### Official Documentation
- **API Docs:** https://apidocs.hashnode.com
- **Playground:** https://gql.hashnode.com
- **Discord:** Join for updates and community support
- **GraphQL Guide:** freeCodeCamp's beginner-friendly GraphQL guide

### references/
The `api.md` reference file contains:
- Complete API specification
- All available queries and mutations
- Detailed parameter descriptions
- Authentication requirements
- Code examples with proper syntax
- Links to original documentation
- Comprehensive error code reference

## Important Notes

- **Always request the `id` field** on objects to avoid stale cached data
- **Rate limits are generous** but respect them for production apps
- **Cache behavior:** Most responses are cached; mutations automatically purge related cache
- **Breaking changes are rare** and announced well in advance on Discord
- **Legacy API is shut down** - use `gql.hashnode.com` only

## Troubleshooting

### Getting UNAUTHENTICATED errors?
- Verify your Personal Access Token is valid
- Check the `Authorization` header is set correctly
- Ensure you're requesting fields that require auth (drafts, email, etc.)

### Not seeing latest data?
- Always request the `id` field to avoid stale cached data
- Check if response is HIT/MISS in playground

### Query validation failed?
- Verify your GraphQL syntax in the playground first
- Check required parameters are provided
- Ensure field names match the schema

### Rate limit reached?
- Queries: 20k/min is very generous - optimize your queries
- Mutations: 500/min limit - batch operations where possible
- Use caching on your end to reduce API calls

## Updating

This skill was automatically generated from official Hashnode documentation. To refresh with updated documentation, regenerate the skill using the latest docs from https://apidocs.hashnode.com.
