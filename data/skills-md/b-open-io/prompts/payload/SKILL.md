---
name: payload
description: This skill should be used when the user asks to "create a post", "edit a post", "update post content", "list posts", "convert markdown to Lexical", "write article to Payload", or mentions Payload CMS content management. Handles both production and local Payload sites via REST API with authentication.
version: 0.4.0
---

# Payload CMS Operations

Manage Payload CMS content via REST API. Works with any Payload deployment (production or local).

## When to Use

- Creating or editing posts/pages in Payload CMS
- Converting markdown content to Lexical rich text format
- Listing and querying Payload collections
- Bulk content updates

## Workflow: REST API with Authentication

### Step 1: Determine the API Endpoint

Ask the user for their Payload site URL, or check common locations:

```bash
# Production site (ask user or check project config)
curl -s "https://your-site.com/api/posts?limit=1" | head -c 100

# Local development
curl -s "http://localhost:3000/api/posts?limit=1" 2>/dev/null | head -c 100
curl -s "http://localhost:3010/api/posts?limit=1" 2>/dev/null | head -c 100
```

### Step 2: Authenticate

For mutations (create/update/delete), authentication is required. Payload uses session-based auth.

**Option A: User provides credentials**
```bash
# Login to get auth token
curl -X POST "https://your-site.com/api/users/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "..."}' \
  -c cookies.txt

# Use the cookie file for authenticated requests
curl -X POST "https://your-site.com/api/posts" \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"title": "...", "content": {...}}'
```

**Option B: User logs in via admin UI**
Have the user log in at `/admin`, then extract the `payload-token` cookie from their browser for use in API calls.

### Step 3: Create/Update Content

```bash
# Create a post
curl -X POST "https://your-site.com/api/posts" \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "title": "Post Title",
    "slug": "post-slug",
    "content": { "root": { ... } },
    "_status": "published"
  }'

# Update a post
curl -X PATCH "https://your-site.com/api/posts/POST_ID" \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"content": { "root": { ... } }}'
```

### Step 4: Verify

```bash
# Check the post was created
curl -s "https://your-site.com/api/posts?where[slug][equals]=post-slug" | jq '.docs[0]'
```

## Lexical JSON Structure

Payload's Lexical editor stores content as JSON:

```json
{
  "root": {
    "type": "root",
    "format": "",
    "indent": 0,
    "version": 1,
    "direction": "ltr",
    "children": [
      {
        "type": "paragraph",
        "format": "",
        "indent": 0,
        "version": 1,
        "direction": "ltr",
        "children": [
          {"type": "text", "text": "Content here", "mode": "normal", "format": 0, "detail": 0, "version": 1, "style": ""}
        ]
      }
    ]
  }
}
```

### Supported Node Types

| Markdown | Lexical Node |
|----------|--------------|
| Paragraphs | `paragraph` |
| `# Heading` | `heading` with tag h1-h6 |
| `**bold**` | text with format: 1 |
| `*italic*` | text with format: 2 |
| `` `code` `` | text with format: 16 |
| Code blocks | `block` with blockType: "code" |
| Lists | `list` with `listitem` children |
| `> quotes` | `quote` |

### Text Format Bitmask

| Value | Format |
|-------|--------|
| 0 | Normal |
| 1 | Bold |
| 2 | Italic |
| 3 | Bold + Italic |
| 16 | Code |

## Markdown to Lexical Conversion

The skill includes a Python script for converting markdown to Lexical JSON:

```bash
python3 ${SKILL_DIR}/scripts/md_to_lexical.py article.md > /tmp/content.json
```

## Common Collections

| Collection | Slug | Purpose |
|------------|------|---------|
| Posts | `posts` | Blog posts |
| Pages | `pages` | Static pages |
| Media | `media` | Uploaded files |
| Users | `users` | User accounts |

## Local Development Alternative

If working locally and REST auth is problematic, write an inline script in the project:

```typescript
// scripts/create-post.ts
import { getPayload } from 'payload'
import config from '../src/payload.config'

const payload = await getPayload({ config })
await payload.create({
  collection: 'posts',
  data: { title: '...', content: {...}, _status: 'published' }
})
process.exit(0)
```

Run with: `source .env.local && bunx tsx scripts/create-post.ts`

**Note**: If Drizzle prompts for schema migration, answer 'n' and use REST API instead.

## Additional Resources

- **`references/lexical-format.md`** - Complete Lexical node type reference
- **`references/rest-api.md`** - Full REST API documentation
- **`scripts/md_to_lexical.py`** - Markdown to Lexical converter
