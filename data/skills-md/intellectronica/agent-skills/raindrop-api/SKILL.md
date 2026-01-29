---
name: raindrop-api
description: >
  This skill provides comprehensive instructions for interacting with the Raindrop.io bookmarks service
  via its REST API using curl and jq. It covers authentication, CRUD operations for collections, raindrops
  (bookmarks), tags, highlights, filters, import/export, and backups. Use this skill whenever the user asks
  to work with their bookmarks from Raindrop.io, including reading, creating, updating, deleting, searching,
  or organising bookmarks and collections.
---

# Raindrop.io API Skill

This skill enables interaction with the Raindrop.io bookmarks service through its REST API. Use `curl` and `jq` for direct REST calls.

**Official API documentation**: https://developer.raindrop.io/

## Authentication

### Token Resolution

Resolve the API token in this order:

1. Check environment variable `RAINDROP_TOKEN`
2. Check if the user has provided a token in the conversation context
3. If neither is available, use AskUserQuestion to request the token from the user

To verify a token exists in the environment:

```bash
[ -n "$RAINDROP_TOKEN" ] && echo "Token available" || echo "Token not set"
```

**Quick setup**: For personal use or development, generate a test token at https://app.raindrop.io/settings/integrations — open your app and copy the "Test token". Test tokens do not expire.

For full OAuth2 flow details, see the [Authentication](#authentication-oauth2-flow) section below.

### Making Authenticated Requests

All requests require the Authorization header with Bearer token:

```bash
curl -s -H "Authorization: Bearer $RAINDROP_TOKEN" \
  "https://api.raindrop.io/rest/v1/ENDPOINT"
```

For POST/PUT requests with JSON body:

```bash
curl -s -X POST \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}' \
  "https://api.raindrop.io/rest/v1/ENDPOINT"
```

### Verifying Authentication

Test the token by retrieving the current user:

```bash
curl -s -H "Authorization: Bearer $RAINDROP_TOKEN" \
  "https://api.raindrop.io/rest/v1/user" | jq '.user.fullName'
```

## Base URL and Conventions

- **Base URL**: `https://api.raindrop.io/rest/v1/`
- **Data Format**: JSON for all request/response bodies
- **Timestamps**: ISO 8601 format
- **Rate Limit**: 120 requests per minute per authenticated user
- **CORS**: Supported for browser-based apps

## Confirmation Requirement

**Before executing any destructive action (DELETE, bulk update, move to trash), always ask the user for confirmation using AskUserQuestion.** A single confirmation suffices for a logical group of related actions.

Destructive actions include:
- Deleting raindrops, collections, or tags
- Bulk updating or moving raindrops
- Merging or removing tags
- Removing collaborators from shared collections
- Clearing trash

Read-only operations (GET requests) do not require confirmation.

## Endpoints Reference

### Raindrops (Bookmarks)

Docs: https://developer.raindrop.io/v1/raindrops

#### Single Raindrop Operations

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Get raindrop | GET | `/raindrop/{id}` |
| Create raindrop | POST | `/raindrop` |
| Update raindrop | PUT | `/raindrop/{id}` |
| Remove raindrop | DELETE | `/raindrop/{id}` |
| Upload file | PUT | `/raindrop/file` |
| Upload cover | PUT | `/raindrop/{id}/cover` |
| Get permanent copy | GET | `/raindrop/{id}/cache` |
| Suggest (new URL) | POST | `/raindrop/suggest` |
| Suggest (existing) | GET | `/raindrop/{id}/suggest` |

Docs: https://developer.raindrop.io/v1/raindrops/single

**Raindrop creation/update fields:**
- `link` (string, required for creation) - Bookmark URL
- `title` (string) - Bookmark title
- `excerpt` (string) - Short description
- `note` (string) - User notes (supports Markdown)
- `tags` (array of strings) - Tag names
- `collection` (object) - `{"$id": collectionId}`
- `type` (string) - `link`, `article`, `image`, `video`, `document`, `audio`
- `important` (boolean) - Mark as favourite
- `order` (number) - Sort order (ascending)
- `media` (array) - Media/thumbnail info
- `highlights` (array) - Text highlights
- `cover` (string) - Cover image URL, or `<screenshot>` for auto-capture
- `pleaseParse` (object) - `{}` to trigger background metadata parsing
- `created` (string) - ISO 8601 creation date
- `lastUpdate` (string) - ISO 8601 last update date
- `reminder` (object) - Reminder settings

**Deletion behaviour**: Removing a raindrop moves it to Trash (collection ID `-99`). Removing from Trash deletes permanently.

#### Multiple Raindrop Operations

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Get raindrops | GET | `/raindrops/{collectionId}` |
| Create multiple | POST | `/raindrops` |
| Update multiple | PUT | `/raindrops/{collectionId}` |
| Remove multiple | DELETE | `/raindrops/{collectionId}` |
| Export | GET | `/raindrops/{collectionId}/export.{format}` |

Docs: https://developer.raindrop.io/v1/raindrops/multiple

**collectionId values:**
- `0` - All raindrops
- `-1` - Unsorted
- `-99` - Trash
- Any positive integer - Specific collection

**Query parameters for GET /raindrops/{collectionId}:**
- `sort` - Sort order: `-created` (default), `created`, `score`, `-sort`, `title`, `-title`, `domain`, `-domain`
- `perpage` - Results per page (max 50)
- `page` - Page number (0-indexed)
- `search` - Search query (see `references/search-operators.md`)
- `nested` - Boolean, include child collection bookmarks

**Bulk update fields** (PUT with `ids` array or `search` query):
- `important` (boolean)
- `tags` (array) - Appends tags; empty array clears all
- `media` (array) - Appends; empty array clears
- `cover` (string) - URL or `<screenshot>`
- `collection` (object) - `{"$id": collectionId}` to move

**Export formats**: `csv`, `html`, `zip`

### Collections

Docs: https://developer.raindrop.io/v1/collections

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List root collections | GET | `/collections` |
| List child collections | GET | `/collections/childrens` |
| Get collection | GET | `/collection/{id}` |
| Create collection | POST | `/collection` |
| Update collection | PUT | `/collection/{id}` |
| Upload cover | PUT | `/collection/{id}/cover` |
| Delete collection | DELETE | `/collection/{id}` |
| Delete multiple | DELETE | `/collections` |
| Reorder/expand all | PUT | `/collections` |
| Merge collections | PUT | `/collections/merge` |
| Remove empty | PUT | `/collections/clean` |
| Empty trash | DELETE | `/collection/-99` |
| System collection counts | GET | `/user/stats` |
| Search covers/icons | GET | `/collections/covers/{text}` |
| Featured covers | GET | `/collections/covers` |

Docs: https://developer.raindrop.io/v1/collections/methods

**Collection fields:**
- `title` (string) - Collection name
- `view` (string) - Display style: `list`, `simple`, `grid`, `masonry`
- `public` (boolean) - Public accessibility
- `parent` (object) - `{"$id": parentCollectionId}` for nesting
- `sort` (number) - Sort position
- `cover` (array) - Cover image URLs
- `expanded` (boolean) - Whether subcollections are expanded
- `color` (string) - Collection colour

**System collections** (non-removable):
- ID `-1` - "Unsorted"
- ID `-99` - "Trash"

**Access levels** (`access.level`):
- `1` - Read only
- `2` - Collaborator (write)
- `3` - Collaborator (write + manage)
- `4` - Owner

For sharing/collaborators, see `references/collections-sharing.md`.

### Tags

Docs: https://developer.raindrop.io/v1/tags

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Get tags | GET | `/tags/{collectionId}` |
| Rename tag | PUT | `/tags/{collectionId}` |
| Merge tags | PUT | `/tags/{collectionId}` |
| Remove tag(s) | DELETE | `/tags/{collectionId}` |

**collectionId**: Omit or use `0` for tags from all collections.

**Get tags response:**

```json
{
  "result": true,
  "items": [{"_id": "tagname", "count": 42}]
}
```

**Rename tag:**

```bash
curl -s -X PUT \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"replace": "new-name", "tags": ["old-name"]}' \
  "https://api.raindrop.io/rest/v1/tags/0"
```

**Merge tags** (same endpoint, multiple tags in array):

```bash
curl -s -X PUT \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"replace": "merged-name", "tags": ["tag1", "tag2", "tag3"]}' \
  "https://api.raindrop.io/rest/v1/tags/0"
```

**Remove tags:**

```bash
curl -s -X DELETE \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tags": ["tag-to-remove"]}' \
  "https://api.raindrop.io/rest/v1/tags/0"
```

### Highlights

Docs: https://developer.raindrop.io/v1/highlights

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Get all highlights | GET | `/highlights` |
| Get collection highlights | GET | `/highlights/{collectionId}` |
| Get raindrop highlights | GET | `/raindrop/{id}` |
| Add highlight | PUT | `/raindrop/{id}` |
| Update highlight | PUT | `/raindrop/{id}` |
| Delete highlight | PUT | `/raindrop/{id}` |

For details, see `references/highlights.md`.

### Filters

Docs: https://developer.raindrop.io/v1/filters

```bash
curl -s -H "Authorization: Bearer $RAINDROP_TOKEN" \
  "https://api.raindrop.io/rest/v1/filters/{collectionId}" | jq '.'
```

Use `0` for all collections. Returns aggregated counts for broken links, duplicates, favourites, untagged items, tags, and content types.

**Query parameters:**
- `tagsSort` - `-count` (default) or `_id` (alphabetical)
- `search` - Additional search filter

### User

Docs: https://developer.raindrop.io/v1/user

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Get current user | GET | `/user` |
| Update user | PUT | `/user` |

### Import

Docs: https://developer.raindrop.io/v1/import

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Parse URL | GET | `/import/url/parse?url={url}` |
| Check URL existence | POST | `/import/url/exists` |
| Parse HTML bookmark file | POST | `/import/file` |

### Backups

Docs: https://developer.raindrop.io/v1/backups

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List backups | GET | `/backups` |
| Download backup | GET | `/backup/{id}.{format}` |
| Generate new backup | GET | `/backup` |

**Formats**: `html` or `csv`

## Authentication: OAuth2 Flow

Docs: https://developer.raindrop.io/v1/authentication/token

For apps accessing other users' data (not personal use), use the full OAuth2 flow:

### Step 1: Authorise

Direct users to:

```
https://raindrop.io/oauth/authorize?client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI&response_type=code
```

### Step 2: Exchange Code for Token

```bash
curl -s -X POST "https://raindrop.io/oauth/access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "AUTH_CODE",
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "redirect_uri": "YOUR_REDIRECT_URI",
    "grant_type": "authorization_code"
  }' | jq '.'
```

Response:

```json
{
  "access_token": "...",
  "refresh_token": "...",
  "expires_in": 1209599,
  "token_type": "Bearer"
}
```

### Step 3: Refresh Token

Access tokens expire after two weeks. Refresh with:

```bash
curl -s -X POST "https://raindrop.io/oauth/access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "refresh_token": "YOUR_REFRESH_TOKEN",
    "grant_type": "refresh_token"
  }' | jq '.'
```

## Error Handling

Check HTTP status codes:

- `200` - Success
- `204` - Success, no content
- `400` - Bad request
- `401` - Authentication failed (check token)
- `403` - Forbidden (insufficient permissions)
- `404` - Resource not found
- `429` - Rate limited (120 req/min exceeded)
- `5xx` - Server error

### Example with Error Handling

```bash
response=$(curl -s -w "\n%{http_code}" \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  "https://api.raindrop.io/rest/v1/raindrops/0")

http_code=$(echo "$response" | tail -1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
  echo "$body" | jq '.'
else
  echo "Error: HTTP $http_code"
  echo "$body"
fi
```

## Common Patterns

### List All Bookmarks in a Collection

```bash
curl -s -H "Authorization: Bearer $RAINDROP_TOKEN" \
  "https://api.raindrop.io/rest/v1/raindrops/COLLECTION_ID?perpage=50" | jq '.items[] | {title, link}'
```

### Create a Bookmark

```bash
curl -s -X POST \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "link": "https://example.com",
    "title": "Example Site",
    "tags": ["reference", "example"],
    "collection": {"$id": COLLECTION_ID},
    "pleaseParse": {}
  }' \
  "https://api.raindrop.io/rest/v1/raindrop" | jq '.'
```

### Search Bookmarks

```bash
# Search across all collections
curl -s -H "Authorization: Bearer $RAINDROP_TOKEN" \
  "https://api.raindrop.io/rest/v1/raindrops/0?search=YOUR_QUERY" | jq '.items[] | {title, link}'

# Search with tag filter
curl -s -H "Authorization: Bearer $RAINDROP_TOKEN" \
  "https://api.raindrop.io/rest/v1/raindrops/0?search=%23tagname" | jq '.items[] | {title, link}'
```

See `references/search-operators.md` for the complete search query syntax.

### Move Bookmark to a Collection

```bash
curl -s -X PUT \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"collection": {"$id": TARGET_COLLECTION_ID}}' \
  "https://api.raindrop.io/rest/v1/raindrop/RAINDROP_ID" | jq '.'
```

### Get All Tags

```bash
curl -s -H "Authorization: Bearer $RAINDROP_TOKEN" \
  "https://api.raindrop.io/rest/v1/tags/0" | jq '.items[] | {tag: ._id, count}'
```

### Create a Collection

```bash
curl -s -X POST \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Collection", "view": "list"}' \
  "https://api.raindrop.io/rest/v1/collection" | jq '.'
```

### List All Collections (Root + Children)

```bash
# Root collections
curl -s -H "Authorization: Bearer $RAINDROP_TOKEN" \
  "https://api.raindrop.io/rest/v1/collections" | jq '.items[] | {id: ._id, title}'

# Child collections
curl -s -H "Authorization: Bearer $RAINDROP_TOKEN" \
  "https://api.raindrop.io/rest/v1/collections/childrens" | jq '.items[] | {id: ._id, title, parent: .parent."$id"}'
```

### Paginate Through All Bookmarks

```bash
page=0
while true; do
  response=$(curl -s -H "Authorization: Bearer $RAINDROP_TOKEN" \
    "https://api.raindrop.io/rest/v1/raindrops/0?perpage=50&page=$page")

  count=$(echo "$response" | jq '.items | length')
  echo "$response" | jq '.items[] | {title, link}'

  if [ "$count" -lt 50 ]; then
    break
  fi
  page=$((page + 1))
done
```

### Export Bookmarks

```bash
# Export all bookmarks as CSV
curl -s -H "Authorization: Bearer $RAINDROP_TOKEN" \
  "https://api.raindrop.io/rest/v1/raindrops/0/export.csv" -o bookmarks.csv

# Export as HTML
curl -s -H "Authorization: Bearer $RAINDROP_TOKEN" \
  "https://api.raindrop.io/rest/v1/raindrops/0/export.html" -o bookmarks.html
```

### Check if URL Already Saved

```bash
curl -s -X POST \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://example.com"]}' \
  "https://api.raindrop.io/rest/v1/import/url/exists" | jq '.'
```

## Pagination

Raindrop uses page-based pagination (not cursor-based):

- `page` - Page number (0-indexed)
- `perpage` - Items per page (max 50, default 25 for highlights)

When the number of items returned is less than `perpage`, you have reached the last page.

## Nested Collection Structure

Collections are organised hierarchically. Reconstructing the full sidebar requires:

1. `GET /user` - Returns `groups` array with collection ordering
2. `GET /collections` - Root collections
3. `GET /collections/childrens` - Nested collections

Root collection sort order is persisted in the user's `groups[].collections` array. Child collection sort order is stored in the collection's `sort` field.

## Additional Reference

For detailed documentation on specific topics, consult:
- `references/search-operators.md` - Search query syntax and operators
- `references/collections-sharing.md` - Collection sharing and collaborators
- `references/highlights.md` - Highlight management

## Workflow Summary

1. **Resolve token** - Environment, context, or ask user
2. **Verify authentication** - Test with `GET /user`
3. **Read operations** - Execute directly without confirmation
4. **Write operations** - Ask for confirmation before executing
5. **Handle pagination** - Loop with page number until items < perpage
6. **Parse responses** - Use jq to extract and format data
