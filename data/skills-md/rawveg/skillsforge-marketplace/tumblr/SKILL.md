---
name: tumblr
description: Tumblr API Development and Integration
---

# Tumblr API Skill

Comprehensive assistance with Tumblr API development, authentication, and integration. This skill provides practical guidance for building applications that interact with Tumblr's platform.

## When to Use This Skill

This skill should be triggered when:
- Integrating with the Tumblr API (any version)
- Implementing OAuth 1.0a or OAuth 2.0 authentication for Tumblr
- Working with Tumblr blog data, posts, likes, or followers
- Building Tumblr clients, dashboard tools, or analytics applications
- Debugging Tumblr API requests or responses
- Understanding Tumblr's Neue Post Format (NPF) or legacy post types
- Managing rate limits or API quotas
- Handling Tumblr webhooks or real-time updates

## Quick Reference

### 1. Fetch Blog Information

Retrieve basic blog metadata including title, description, and post count:

```bash
curl -H 'User-Agent: MyApp/1.0' \
  'https://api.tumblr.com/v2/blog/staff.tumblr.com/info?api_key=YOUR_API_KEY'
```

**Response includes:** Blog title, URL, post count, description, avatar, theme settings.

### 2. Get Recent Posts

Retrieve the 5 most recent posts from a blog:

```bash
curl -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  'https://api.tumblr.com/v2/blog/staff.tumblr.com/posts?limit=5'
```

**Query parameters:**
- `limit`: 1-20 posts per request
- `offset`: Pagination offset
- `tag`: Filter by tag
- `npf=true`: Request Neue Post Format

### 3. OAuth 2.0 Token Exchange

Exchange authorization code for access token:

```bash
curl -X POST https://api.tumblr.com/v2/oauth2/token \
  -F grant_type=authorization_code \
  -F code=YOUR_AUTH_CODE \
  -F client_id=YOUR_CONSUMER_KEY \
  -F client_secret=YOUR_CONSUMER_SECRET
```

**Scopes:** `basic`, `write`, `offline_access`

### 4. Get Blog Avatar

Fetch blog avatar image URL:

```bash
curl 'https://api.tumblr.com/v2/blog/staff.tumblr.com/avatar/128'
```

**Available sizes:** 16, 24, 30, 40, 48, 64, 96, 128, 512 (default: 64)

### 5. Retrieve Liked Posts

Get posts liked by a blog:

```bash
curl -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  'https://api.tumblr.com/v2/blog/staff.tumblr.com/likes?limit=20&offset=0'
```

**Parameters:** `limit`, `offset`, `before` (timestamp), `after` (timestamp)

### 6. Queue Management

Retrieve queued posts:

```bash
curl -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  'https://api.tumblr.com/v2/blog/myblog.tumblr.com/posts/queue'
```

Reorder queue:

```bash
curl -X POST https://api.tumblr.com/v2/blog/myblog.tumblr.com/posts/queue/reorder \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -d 'post_id=123456789'
```

### 7. Get Followers

Retrieve blog followers:

```bash
curl -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  'https://api.tumblr.com/v2/blog/myblog.tumblr.com/followers'
```

**Response includes:** Total follower count, follower blog objects with names and URLs.

### 8. Filter Posts by Tag

Retrieve posts with specific tag:

```bash
curl -H 'User-Agent: MyApp/1.0' \
  'https://api.tumblr.com/v2/blog/staff.tumblr.com/posts?api_key=YOUR_KEY&tag=photography&limit=10'
```

### 9. Standard API Response Format

All Tumblr API responses follow this structure:

```json
{
  "meta": {
    "status": 200,
    "msg": "OK"
  },
  "response": {
    "blog": { },
    "posts": [ ]
  }
}
```

### 10. Working with Blog Identifiers

Three interchangeable identifier formats:

```bash
# Blog name
/v2/blog/staff/info

# Hostname
/v2/blog/staff.tumblr.com/info

# UUID (stable, persistent)
/v2/blog/t:0aY0xL2Fi1OFJg4YxpmegQ/info
```

**Recommendation:** Use UUID for long-term stability (survives blog renames).

## Key Concepts

### Authentication Levels

1. **None** - Public endpoints (blog info, public posts) require no authentication
2. **API Key** - Use OAuth Consumer Key as `api_key` query parameter
3. **OAuth** - Signed requests using OAuth 1.0a or OAuth 2.0 for user-specific data

### Rate Limits

**Per IP Address:**
- 300 calls/minute
- 18,000 calls/hour
- 432,000 calls/day

**Per Consumer Key:**
- 1,000 calls/hour
- 5,000 calls/day

**Action Limits:**
- 250 posts/day
- 200 follows/day
- 1,000 likes/day

### Post Formats

**Legacy Post Types:**
- Text, Photo, Quote, Link, Chat, Audio, Video, Answer

**Neue Post Format (NPF):**
- Modern block-based format
- Posts with `type: blocks` or `is_blocks_post_format: true`
- Request with `npf=true` parameter
- Contains `content` (blocks), `layout` (specifications), `trail` (reblog chain)

### Post IDs

Post IDs are 64-bit integers. **Important:** Use `id_string` field for JavaScript or languages with unsafe integer handling.

### Required Headers

**User-Agent:** Mandatory for all requests. Must be consistent. Format: `AppName/Version`

**Content-Type:** Required for POST/PUT with body. Accepted:
- `application/json`
- `application/x-www-form-urlencoded`
- `multipart/form-data`

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **api.md** - Complete Tumblr API documentation including:
  - All authentication methods (OAuth 1.0a, OAuth 2.0, API key)
  - Blog endpoints (info, posts, avatar, likes, following, followers)
  - User endpoints (dashboard, likes, following)
  - Post creation and management
  - Queue and draft management
  - Neue Post Format (NPF) specification
  - Legacy post type fields
  - Rate limits and best practices
  - Response format documentation

Use the `view` command to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners

1. **Start with public endpoints** - No authentication needed:
   - Fetch blog info: `/v2/blog/{blog}/info?api_key={key}`
   - Get public posts: `/v2/blog/{blog}/posts?api_key={key}`

2. **Register your application:**
   - Visit https://www.tumblr.com/oauth/apps
   - Get OAuth Consumer Key and Secret
   - Use Consumer Key as `api_key` for public endpoints

3. **Test with API Console:**
   - https://api.tumblr.com/console
   - Interactive testing environment

### For OAuth Implementation

1. **Choose OAuth version:**
   - OAuth 2.0: Modern, simpler, bearer tokens
   - OAuth 1.0a: Legacy, more complex, signed requests

2. **OAuth 2.0 flow:**
   - Redirect user to authorization URL with scopes
   - Exchange authorization code for access token
   - Use token in `Authorization: Bearer {token}` header

3. **OAuth 1.0a flow:**
   - Request temporary credentials
   - Redirect user to authorize
   - Exchange verifier for access token
   - Sign all requests with token

### For Advanced Features

1. **Neue Post Format (NPF):**
   - Add `npf=true` to any post-returning endpoint
   - Work with content blocks and layout objects
   - Access full reblog trail

2. **Pagination:**
   - Use `offset` for numeric pagination
   - Use `before`/`after` with timestamps for chronological navigation
   - Check `_links` object for next/previous URLs

3. **Partial responses:**
   - Use `fields` parameter to specify blog object fields
   - Reduces response size and improves performance

4. **JSONP support:**
   - Add `jsonp=callbackName` to GET requests
   - Useful for client-side JavaScript

## Common Patterns

### Authentication Flow (OAuth 2.0)

```bash
# Step 1: Redirect user to authorization URL
https://www.tumblr.com/oauth2/authorize?client_id={key}&response_type=code&scope=basic%20write&state={random}

# Step 2: User authorizes, Tumblr redirects back with code
# Your redirect URL receives: ?code={auth_code}

# Step 3: Exchange code for access token
curl -X POST https://api.tumblr.com/v2/oauth2/token \
  -F grant_type=authorization_code \
  -F code={auth_code} \
  -F client_id={consumer_key} \
  -F client_secret={consumer_secret}

# Step 4: Use access token in requests
curl -H 'Authorization: Bearer {access_token}' \
  'https://api.tumblr.com/v2/user/info'
```

### Error Handling

```json
{
  "meta": {
    "status": 401,
    "msg": "Unauthorized"
  },
  "response": [ ],
  "errors": [
    {
      "title": "Unauthorized",
      "code": 401,
      "detail": "OAuth authentication required"
    }
  ]
}
```

**Common status codes:**
- 200: Success
- 401: Unauthorized (missing/invalid credentials)
- 404: Not Found (blog or post doesn't exist)
- 429: Rate Limit Exceeded
- 503: Service Temporarily Unavailable

### Handling Large Post Counts

```bash
# Fetch all posts using pagination
offset=0
limit=20

while true; do
  curl "https://api.tumblr.com/v2/blog/staff.tumblr.com/posts?api_key={key}&limit=${limit}&offset=${offset}"
  offset=$((offset + limit))
  # Check if response contains fewer than 'limit' posts, then break
done
```

## Resources

### Official Links

- **API Console:** https://api.tumblr.com/console
- **Developer Portal:** https://www.tumblr.com/docs/api/v2
- **OAuth Apps:** https://www.tumblr.com/oauth/apps
- **Support:** https://www.tumblr.com/support

### Official Clients

- JavaScript: `tumblr.js`
- Ruby: `tumblr_client`
- PHP: `tumblr/tumblr`
- Python: `pytumblr`
- Java: `jumblr`
- Objective-C: `TMTumblrSDK`
- Go: `tumblr/tumblr.go`

### Best Practices

1. **Always include User-Agent header** - Inconsistent or missing User-Agent may result in suspension
2. **Respect rate limits** - Implement exponential backoff for 429 responses
3. **Use UUIDs for blog identifiers** - More stable than blog names (survive renames)
4. **Cache blog info** - Reduce API calls by caching static blog data
5. **Use NPF for new integrations** - Legacy formats may be deprecated
6. **Handle 64-bit integers carefully** - Use `id_string` for JavaScript
7. **Validate responses** - Check `meta.status` before processing `response`

## Notes

- This skill was generated from official Tumblr API documentation
- All endpoints use base URL: `https://api.tumblr.com`
- API version is included in path: `/v2/`
- HTTPS is required for all API requests
- Reference files preserve structure and examples from source docs
- Code examples include language detection for better syntax highlighting

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information from the official GitHub repository
