---
name: forem-api
description: Forem API
---

# Forem API Skill

Comprehensive assistance with Forem API (v1) development. Forem is the platform that powers DEV.to and other online communities. This skill provides guidance on interacting with articles, users, comments, organizations, tags, and more through the Forem REST API.

## When to Use This Skill

This skill should be triggered when:
- **Building integrations with Forem-based platforms** (DEV.to, Forem communities)
- **Publishing or managing articles programmatically** via Forem API
- **Retrieving user data, comments, or organization information** from Forem
- **Implementing authentication** with Forem API keys
- **Working with tags, followers, reading lists, or reactions** on Forem
- **Debugging Forem API requests** or understanding response formats
- **Learning Forem API endpoints** and best practices
- **Managing display ads or podcast episodes** through the API

## Quick Reference

### Authentication Setup

Set up authentication headers for Forem API v1 requests:

```bash
# Required headers for authenticated requests
curl -X GET "https://dev.to/api/articles/me" \
  -H "api-key: YOUR_API_KEY" \
  -H "accept: application/vnd.forem.api-v1+json"
```

**Key points:**
- Generate API key at `dev.to/settings/extensions`
- Use `api-key` header (not `Authorization`)
- Include `accept: application/vnd.forem.api-v1+json` header

### Get Authenticated User Info

```bash
# Retrieve current user's profile information
curl -X GET "https://dev.to/api/users/me" \
  -H "api-key: YOUR_API_KEY" \
  -H "accept: application/vnd.forem.api-v1+json"
```

**Response:**
```json
{
  "type_of": "user",
  "id": 1431,
  "username": "username480",
  "name": "User Name",
  "twitter_username": "twitter_handle",
  "github_username": "github_handle",
  "joined_at": "Apr 14, 2023",
  "profile_image": "/uploads/user/profile_image/..."
}
```

### Publish a New Article

```javascript
// Create and publish an article with tags
const response = await fetch('https://dev.to/api/articles', {
  method: 'POST',
  headers: {
    'api-key': 'YOUR_API_KEY',
    'accept': 'application/vnd.forem.api-v1+json',
    'content-type': 'application/json'
  },
  body: JSON.stringify({
    article: {
      title: "Getting Started with Forem API",
      description: "Learn how to integrate with Forem",
      body_markdown: "## Introduction\n\n**Forem** is amazing!",
      published: true,
      tags: ["webdev", "api", "tutorial"]
    }
  })
});

const data = await response.json();
console.log(data.url); // https://dev.to/username/getting-started-...
```

**Returns:** Article object with `id`, `slug`, `path`, `url`, and `published_timestamp`

### Get Published Articles with Filters

```python
import requests

# Get JavaScript articles from the last 7 days
params = {
    'tag': 'javascript',
    'top': 7,
    'per_page': 10,
    'page': 1
}

response = requests.get(
    'https://dev.to/api/articles',
    params=params,
    headers={'accept': 'application/vnd.forem.api-v1+json'}
)

articles = response.json()
for article in articles:
    print(f"{article['title']} by {article['user']['name']}")
```

**Query parameters:**
- `tag` - Filter by single tag
- `tags` - Multiple tags (comma-separated)
- `username` - Filter by author
- `top` - Days since publication
- `per_page` - Results per page (30-1000)
- `page` - Page number for pagination

### Get User's Draft Articles

```bash
# Retrieve your unpublished articles
curl -X GET "https://dev.to/api/articles/me/unpublished" \
  -H "api-key: YOUR_API_KEY" \
  -H "accept: application/vnd.forem.api-v1+json"
```

**Other endpoints:**
- `/articles/me` - All your articles
- `/articles/me/published` - Published only
- `/articles/me/unpublished` - Drafts only
- `/articles/me/all` - Everything including hidden

### Update an Existing Article

```json
PUT /articles/{id}
Content-Type: application/json
Headers: api-key, accept

{
  "article": {
    "title": "Updated Title",
    "body_markdown": "Updated content with **bold** text",
    "published": true
  }
}
```

### Get Comments for an Article

```python
# Get comments by article ID
response = requests.get(
    'https://dev.to/api/comments',
    params={'a_id': 123456},
    headers={'accept': 'application/vnd.forem.api-v1+json'}
)

comments = response.json()
for comment in comments:
    print(f"{comment['user']['name']}: {comment['body_html']}")
```

**Query parameters:**
- `a_id` - Article ID
- `p_id` - Podcast episode ID

### Create a Reaction (Like)

```bash
# Add a "like" reaction to an article
curl -X POST "https://dev.to/api/reactions" \
  -H "api-key: YOUR_API_KEY" \
  -H "accept: application/vnd.forem.api-v1+json" \
  -H "content-type: application/json" \
  -d '{
    "category": "like",
    "reactable_id": 123456,
    "reactable_type": "Article"
  }'
```

**Categories:** `like`, `unicorn`, `readinglist`, `thinking`

### Get Organization Details

```bash
# Fetch organization information and articles
curl -X GET "https://dev.to/api/organizations/forem" \
  -H "accept: application/vnd.forem.api-v1+json"

# Get organization's published articles
curl -X GET "https://dev.to/api/organizations/forem/articles" \
  -H "accept: application/vnd.forem.api-v1+json"
```

### Get Available Tags

```javascript
// Fetch popular tags from the platform
const response = await fetch('https://dev.to/api/tags', {
  headers: { 'accept': 'application/vnd.forem.api-v1+json' }
});

const tags = await response.json();
tags.forEach(tag => {
  console.log(`${tag.name} - ${tag.bg_color_hex}`);
});
```

## Key Concepts

### API Versions
- **API v1** - Current recommended version (`application/vnd.forem.api-v1+json`)
- **API v0** - Deprecated legacy version

### Authentication
- **API Key Authentication** - Required for most write operations
- **Public Endpoints** - Some GET endpoints work without authentication
- **CORS Policy** - Disabled on authenticated endpoints, open on public endpoints

### Response Formats
All responses use JSON format with consistent structure:
- `type_of` - Resource type (article, user, comment, etc.)
- `id` - Unique identifier
- Standard fields based on resource type

### Rate Limiting
Follow best practices to avoid rate limits:
- Use pagination for large datasets
- Cache responses when appropriate
- Implement exponential backoff for retries

### Pagination
Most list endpoints support pagination:
- `page` - Page number (starts at 1)
- `per_page` - Items per page (typically 30-1000, default 30)

### Common Status Codes
- `200` - Success (GET, PUT)
- `201` - Created (POST)
- `204` - No Content (DELETE, unpublish)
- `401` - Unauthorized (invalid API key)
- `404` - Not Found
- `422` - Unprocessable Entity (validation errors)

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **api.md** - Complete Forem API v1 reference documentation

Use `view` or read the reference file directly when you need:
- Detailed endpoint specifications
- Complete parameter lists
- Response schema details
- Additional code examples

## Working with This Skill

### For Beginners
1. **Start with authentication** - Generate your API key at `dev.to/settings/extensions`
2. **Try read-only endpoints first** - Use `GET /articles` or `GET /users/{username}` without auth
3. **Test with curl** - The examples above work directly in your terminal
4. **Use the Quick Reference** - Start with common patterns like getting articles or user info

### For Building Integrations
1. **Understand pagination** - Most lists require pagination for large datasets
2. **Handle errors gracefully** - Check status codes and response messages
3. **Use proper headers** - Always include both `api-key` and `accept` headers
4. **Test in development** - Use a test account before production deployment

### For Content Management
1. **Publishing workflow** - Create drafts (`published: false`), review, then update to publish
2. **Bulk operations** - Use pagination to process all articles
3. **Tag management** - Fetch available tags before creating articles
4. **Markdown support** - Use `body_markdown` field with full Markdown syntax

### For Advanced Users
1. **Admin operations** - Unpublish, suspend, invite (requires appropriate permissions)
2. **Display ads** - Create and manage promotional content
3. **Organization management** - Handle multi-author accounts
4. **Webhook integration** - Combine with webhooks for real-time updates

## Common Endpoints Summary

### Articles
- `POST /articles` - Publish new article
- `GET /articles` - Get published articles (paginated)
- `GET /articles/{id}` - Get specific article
- `PUT /articles/{id}` - Update article
- `GET /articles/me` - Your articles
- `PUT /articles/{id}/unpublish` - Unpublish article

### Users
- `GET /users/me` - Current user info
- `GET /users/{id}` - User by ID/username

### Comments
- `GET /comments` - Get comments by article/episode
- `GET /comments/{id}` - Specific comment with descendants

### Organizations
- `GET /organizations/{username}` - Organization details
- `GET /organizations/{username}/articles` - Organization's articles
- `GET /organizations/{username}/users` - Organization members

### Tags & Follows
- `GET /tags` - Available tags
- `GET /follows/tags` - User's followed tags
- `GET /followers/users` - User's followers

### Engagement
- `POST /reactions` - Create reaction
- `POST /reactions/toggle` - Toggle reaction
- `GET /readinglist` - User's reading list

## Resources

### Official Documentation
- **API Reference:** https://developers.forem.com/api/v1
- **OpenAPI Spec:** https://github.com/forem/forem-docs/blob/main/api_v1.json
- **Forem GitHub:** https://github.com/forem/forem

### Getting Help
- **Forem Creators Community:** https://forem.dev
- **DEV Community:** https://dev.to/t/forem
- **Issue Tracker:** https://github.com/forem/forem/issues

## Notes

- This skill covers Forem API v1 (current stable version)
- API keys are generated at `dev.to/settings/extensions` or your Forem instance settings
- Most endpoints require the `application/vnd.forem.api-v1+json` accept header
- Public endpoints (like listing articles) work without authentication
- Admin endpoints require appropriate user permissions
- Rate limits apply - implement proper pagination and caching

## Best Practices

1. **Always include both required headers** (`api-key` and `accept`)
2. **Use pagination for large result sets** (don't fetch 1000 articles at once)
3. **Handle errors gracefully** with proper status code checking
4. **Cache responses when appropriate** to reduce API calls
5. **Use Markdown formatting** in `body_markdown` for rich content
6. **Test with a development account** before production use
7. **Respect rate limits** and implement exponential backoff
8. **Keep API keys secure** - never commit them to version control
