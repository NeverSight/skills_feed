---
name: writeas
description: Write.as API Documentation
---

# Write.as Skill

Comprehensive assistance with Write.as and WriteFreely API development, based on official API documentation. This skill provides practical guidance for building applications around the Write.as blogging platform and its open-source WriteFreely implementation.

## When to Use This Skill

This skill should be triggered when:
- Working with the Write.as REST API (`https://write.as/api/`)
- Building applications that interact with Write.as or WriteFreely
- Implementing blog post creation, updates, or management
- Setting up user authentication for Write.as accounts
- Creating or managing collections (blogs)
- Implementing crossposting to Twitter, Medium, or Tumblr
- Integrating Markdown rendering for blog posts
- Debugging Write.as API calls or authentication issues
- Working with anonymous posts and post claiming
- Building self-hosted WriteFreely instances

## Key Concepts

### Core Terminology

**Posts**: Markdown-based articles with metadata. Posts can be created anonymously or associated with a user account.

**Collections**: Known as "blogs" in the UI. Container for multiple posts with customizable settings. Creating collections requires a Pro account.

**Users**: Registered accounts with password, email, and resource access. Users can own multiple collections and posts.

**Tokens**: Used for authentication and post management. Anonymous posts return a `token` for later modifications, while user operations use access tokens via `Authorization: Token {access_token}` header.

### Authentication

- **Anonymous**: No authentication required. Store the returned `token` for later updates/deletions.
- **User-based**: Login via `/api/auth/login` to get an access token, then pass it in the `Authorization` header.

## Quick Reference

### Creating an Anonymous Post

```json
POST https://write.as/api/posts
Content-Type: application/json

{
  "body": "This is a post.",
  "title": "My First Post"
}
```

**Response:**
```json
{
  "code": 201,
  "data": {
    "id": "rf3t35fkax0aw",
    "token": "ozPEuJWYK8L1QsysBUcTUKy9za7yqQ4M",
    "title": "My First Post",
    "body": "This is a post."
  }
}
```

**Note**: Save the `token` to update or delete this post later.

### Updating a Post (Anonymous)

```json
POST https://write.as/api/posts/{POST_ID}
Content-Type: application/json

{
  "token": "ozPEuJWYK8L1QsysBUcTUKy9za7yqQ4M",
  "body": "This is an updated post."
}
```

### User Authentication

```json
POST https://write.as/api/auth/login
Content-Type: application/json

{
  "alias": "username",
  "pass": "password"
}
```

**Response:**
```json
{
  "code": 200,
  "data": {
    "access_token": "00000000-0000-0000-0000-000000000000",
    "user": {
      "username": "username"
    }
  }
}
```

### Creating a Post as Authenticated User

```json
POST https://write.as/api/posts
Authorization: Token 00000000-0000-0000-0000-000000000000
Content-Type: application/json

{
  "body": "# My authenticated post\n\nThis post is linked to my account.",
  "title": "Authenticated Post"
}
```

### Styling Posts with Fonts

```json
POST https://write.as/api/posts
Content-Type: application/json

{
  "body": "This is a monospace code post.",
  "font": "code"
}
```

**Available fonts:**
- `sans` - Sans-serif with word wrap
- `serif` or `norm` - Serif with word wrap
- `wrap` - Monospace with word wrap
- `mono` - Monospace without wrap
- `code` - Syntax-highlighted monospace

### Crossposting to Social Media

```json
POST https://write.as/api/posts
Authorization: Token 00000000-0000-0000-0000-000000000000
Content-Type: application/json

{
  "body": "Check out my new post!",
  "title": "My Post",
  "crosspost": [
    {"twitter": "yourusername"},
    {"medium": "yourusername"}
  ]
}
```

**Supported services**: Twitter, Tumblr, Medium

### Creating a Collection (Pro Feature)

```json
POST https://write.as/api/collections
Authorization: Token 00000000-0000-0000-0000-000000000000
Content-Type: application/json

{
  "alias": "my-blog",
  "title": "My Blog"
}
```

### Publishing to a Collection

```json
POST https://write.as/api/collections/{ALIAS}/posts
Authorization: Token 00000000-0000-0000-0000-000000000000
Content-Type: application/json

{
  "body": "# First blog post\n\nWelcome to my blog!",
  "title": "Hello World"
}
```

### Moving Anonymous Post to Collection

```json
POST https://write.as/api/collections/{ALIAS}/collect
Authorization: Token 00000000-0000-0000-0000-000000000000
Content-Type: application/json

[
  {
    "id": "rf3t35fkax0aw",
    "token": "ozPEuJWYK8L1QsysBUcTUKy9za7yqQ4M"
  }
]
```

### Rendering Markdown to HTML

```json
POST https://write.as/api/markdown
Content-Type: application/json

{
  "raw_body": "# Hello\n\nThis is **Markdown**."
}
```

**Response:**
```json
{
  "code": 200,
  "data": {
    "body": "<h1>Hello</h1>\n<p>This is <strong>Markdown</strong>.</p>"
  }
}
```

## Error Handling

All API responses follow this structure:

```json
{
  "code": 200,
  "data": {}
}
```

**Common HTTP status codes:**
- `200` - Success
- `201` - Created successfully
- `400` - Bad request or malformed data
- `401` - Missing or invalid authentication
- `403` - Insufficient permissions (e.g., creating collection without Pro)
- `404` - Resource not found
- `410` - Post unpublished (may return later)
- `429` - Rate limited

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **api.md** - Complete Write.as API documentation including:
  - All available endpoints (posts, collections, users, formatting)
  - Request/response examples
  - Authentication methods
  - Crossposting configuration
  - Error codes and handling

Use `view` to read the API reference file when detailed information is needed.

## Working with This Skill

### For Beginners

1. **Start with anonymous posts**: No authentication required, perfect for testing
2. **Save the token**: Always store the `token` returned when creating anonymous posts
3. **Test with single posts**: Create, update, retrieve, and delete one post before scaling
4. **Read error responses**: The API provides clear error messages in the response body

### For Intermediate Users

1. **Implement user authentication**: Use `/api/auth/login` to get access tokens
2. **Work with collections**: Create blogs and organize posts into collections
3. **Enable crossposting**: Automatically share posts to Twitter, Medium, or Tumblr
4. **Claim anonymous posts**: Convert anonymous posts to user-owned posts with `/api/posts/claim`
5. **Use post styling**: Apply different fonts (`code`, `sans`, `mono`) for various content types

### For Advanced Users

1. **Build full applications**: Leverage all endpoints for complete blog management
2. **Self-host WriteFreely**: Deploy open-source WriteFreely instances
3. **Implement rate limiting**: Respect API limits and handle 429 responses
4. **Use client libraries**: Leverage official libraries (Go, Swift, Java) or community libraries (PHP, Python, JavaScript, .NET)
5. **Handle edge cases**: Implement retry logic, token refresh, and error recovery

### Navigation Tips

- **Authentication flow**: See `api.md` → "Users" section
- **Post management**: See `api.md` → "Posts" section
- **Collection setup**: See `api.md` → "Collections" section
- **Crossposting**: See `api.md` → "Crossposting" section
- **Error handling**: See `api.md` → "Error Handling" section

## API Best Practices

1. **Store tokens securely**: Never commit access tokens or post tokens to version control
2. **Handle anonymous posts**: Always save the `token` field when creating anonymous posts
3. **Respect rate limits**: Implement exponential backoff on 429 responses
4. **Use HTTPS**: All API endpoints require HTTPS
5. **Test with small datasets**: Verify your integration with a few posts before scaling
6. **Check Pro status**: Collection creation requires a Pro account
7. **Validate Markdown**: Test Markdown rendering with `/api/markdown` before posting
8. **Handle 410 gracefully**: Unpublished posts may return with 410 status

## Common Use Cases

### Building a Blog Publishing Tool
Use authenticated user endpoints to create collections, publish posts, and manage content.

### Creating a Markdown Editor Integration
Implement post creation with Markdown preview using `/api/markdown` endpoint.

### Social Media Cross-Poster
Leverage the `crosspost` parameter to automatically share posts to multiple platforms.

### Anonymous Blogging Platform
Build an app using anonymous post creation, storing tokens locally for later management.

### Content Migration Tool
Use `/api/posts/claim` to import anonymous posts into a user account.

## Client Libraries

**Official:**
- Go: https://github.com/writeas/go-writeas
- Swift: https://github.com/writeas/writefreely-swift
- Java: https://github.com/writeas/java-writeas

**Community:**
- PHP, Python, JavaScript, Vala, .NET Core (see Write.as documentation)

## Resources

### Official Documentation
- API Docs: https://developers.write.as/docs/api/
- WriteFreely: https://writefreely.org/ (open-source self-hosting)

### Key Features
- **Backwards compatibility**: Endpoints rarely removed; new features added alongside existing
- **Flexible authentication**: Works anonymously or with user tokens
- **Markdown-first**: All content uses Markdown formatting
- **Self-hosting ready**: WriteFreely powers Write.as and independent instances

## Notes

- All API requests must use HTTPS
- Anonymous posts can be claimed by authenticated users
- Collections (blogs) require a Pro subscription on Write.as
- Post IDs are permanent and unique
- Tokens are sensitive credentials - protect them like passwords
- The API maintains backwards compatibility - old integrations continue working

## Updating

This skill is based on the official Write.as API documentation. For the latest updates, refer to:
- https://developers.write.as/docs/api/
