---
name: podchaser
description: Podchaser GraphQL API for podcast data, discovery, episodes, creators, and sponsorship information.
vm0_secrets:
  - PODCHASER_CLIENT_SECRET
vm0_vars:
  - PODCHASER_CLIENT_ID
---

# Podchaser API

Access comprehensive podcast data including shows, episodes, creators, networks, charts, and sponsorship information via GraphQL.

> Official docs: `https://api-docs.podchaser.com/docs/overview`

---

## When to Use

Use this skill when you need to:

- Search and discover podcasts by topic, category, or keywords
- Get detailed podcast and episode metadata
- Access Apple Podcasts and Spotify chart rankings
- Find sponsorship and advertising data
- Retrieve episode transcripts
- Look up podcast creators and networks

---

## Prerequisites

1. Create an account at https://www.podchaser.com/
2. Go to Account Settings > API Settings to get your Client ID and Secret
3. Use Development credentials during integration (Production works identically)

Set environment variables:

```bash
export PODCHASER_CLIENT_ID="your-client-id"
export PODCHASER_CLIENT_SECRET="your-client-secret"
```

---

> **Important:** Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly. Wrap the command containing `$VAR` in `bash -c '...'`, keep `jq` outside.

## How to Use

### 1. Get Access Token

Request an access token (valid for 1 year) and save to a temp file:

Write to `/tmp/podchaser_request.json`:

```json
{
  "query": "mutation { requestAccessToken(input: { grant_type: CLIENT_CREDENTIALS, client_id: \"<your-client-id>\", client_secret: \"<your-client-secret>\" }) { access_token token_type expires_in } }"
}
```

Replace `<your-client-id>` and `<your-client-secret>` with your actual credentials from the Prerequisites section.

Then run:

```bash
bash -c 'curl -s -X POST "https://api.podchaser.com/graphql" --header "Content-Type: application/json" -d @/tmp/podchaser_request.json' | jq -r '.data.requestAccessToken.access_token' > /tmp/podchaser_token.txt
```

Store the token for use in subsequent requests.

Verify the token was saved:

```bash
cat /tmp/podchaser_token.txt | head -c 50
```

### 2. Search Podcasts

Search for podcasts by keyword:

Write to `/tmp/podchaser_request.json`:

```json
{
  "query": "{ podcasts(searchTerm: \"technology\", first: 5) { paginatorInfo { count } data { id title description author { name } } } }"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.podchaser.com/graphql" --header "Content-Type: application/json" --header "Authorization: Bearer $(cat /tmp/podchaser_token.txt)" -d @/tmp/podchaser_request.json'
```

### 3. Get Podcast Details

Get detailed information about a specific podcast by ID:

> **Note:** The `type` field is required in the identifier. Use `PODCHASER` for Podchaser IDs, `APPLE_PODCASTS` for Apple IDs, or `SPOTIFY` for Spotify IDs.

Write to `/tmp/podchaser_request.json`:

```json
{
  "query": "{ podcast(identifier: { id: \"717178\", type: PODCHASER }) { id title description url imageUrl language ratingAverage ratingCount author { name } categories { title } } }"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.podchaser.com/graphql" --header "Content-Type: application/json" --header "Authorization: Bearer $(cat /tmp/podchaser_token.txt)" -d @/tmp/podchaser_request.json'
```

### 4. Search Episodes

Search for episodes across all podcasts:

Write to `/tmp/podchaser_request.json`:

```json
{
  "query": "{ episodes(searchTerm: \"AI\", first: 5) { paginatorInfo { count } data { id title description airDate length podcast { title } } } }"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.podchaser.com/graphql" --header "Content-Type: application/json" --header "Authorization: Bearer $(cat /tmp/podchaser_token.txt)" -d @/tmp/podchaser_request.json'
```

### 5. Get Podcast Episodes

Get episodes for a specific podcast:

Write to `/tmp/podchaser_request.json`:

```json
{
  "query": "{ podcast(identifier: { id: \"717178\", type: PODCHASER }) { id title episodes(first: 10) { data { id title description airDate length } } } }"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.podchaser.com/graphql" --header "Content-Type: application/json" --header "Authorization: Bearer $(cat /tmp/podchaser_token.txt)" -d @/tmp/podchaser_request.json'
```

### 6. Get Episode Details

Get detailed information about a specific episode:

Write to `/tmp/podchaser_request.json`:

```json
{
  "query": "{ episode(identifier: { id: \"789012\", type: PODCHASER }) { id title description airDate length url imageUrl podcast { id title } } }"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.podchaser.com/graphql" --header "Content-Type: application/json" --header "Authorization: Bearer $(cat /tmp/podchaser_token.txt)" -d @/tmp/podchaser_request.json'
```

### 7. Get Podcast Categories

Categories are available as a field on podcast objects. Get categories for a specific podcast:

Write to `/tmp/podchaser_request.json`:

```json
{
  "query": "{ podcast(identifier: { id: \"717178\", type: PODCHASER }) { title categories { title slug } } }"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.podchaser.com/graphql" --header "Content-Type: application/json" --header "Authorization: Bearer $(cat /tmp/podchaser_token.txt)" -d @/tmp/podchaser_request.json'
```

### 8. Filter Podcasts by Category

Get podcasts in a specific category:

Write to `/tmp/podchaser_request.json`:

```json
{
  "query": "{ podcasts(filters: { categories: [\"technology\"] }, first: 10) { data { id title description ratingAverage } } }"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.podchaser.com/graphql" --header "Content-Type: application/json" --header "Authorization: Bearer $(cat /tmp/podchaser_token.txt)" -d @/tmp/podchaser_request.json'
```

### 9. Get Chart Rankings

Get Apple Podcasts chart data:

Write to `/tmp/podchaser_request.json`:

```json
{
  "query": "{ podcasts(filters: { hasAppleChartRank: true }, sort: { sortBy: APPLE_CHART_RANK, direction: ASC }, first: 10) { data { id title appleChartRank } } }"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.podchaser.com/graphql" --header "Content-Type: application/json" --header "Authorization: Bearer $(cat /tmp/podchaser_token.txt)" -d @/tmp/podchaser_request.json'
```

### 10. Get Creator/Host Information

Search for podcast creators:

Write to `/tmp/podchaser_request.json`:

```json
{
  "query": "{ creators(searchTerm: \"Joe Rogan\", first: 5) { data { pcid name bio credits { data { podcast { title } } } } } }"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.podchaser.com/graphql" --header "Content-Type: application/json" --header "Authorization: Bearer $(cat /tmp/podchaser_token.txt)" -d @/tmp/podchaser_request.json'
```

### 11. Preview Query Cost

Check how many points a query will cost before executing:

Write to `/tmp/podchaser_request.json`:

```json
{
  "query": "{ podcasts(searchTerm: \"tech\", first: 10) { data { id title description episodes(first: 5) { data { id title } } } } }"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.podchaser.com/graphql/cost" --header "Content-Type: application/json" --header "Authorization: Bearer $(cat /tmp/podchaser_token.txt)" -d @/tmp/podchaser_request.json'
```

---

## GraphQL Schema Reference

### Main Queries

| Query | Description |
|-------|-------------|
| `podcast(identifier: {id: "...", type: PODCHASER})` | Get single podcast by ID |
| `podcasts(searchTerm: "...", first: N)` | Search podcasts |
| `episode(identifier: {id: "...", type: PODCHASER})` | Get single episode by ID |
| `episodes(searchTerm: "...", first: N)` | Search episodes |
| `creators(searchTerm: "...", first: N)` | Search creators/hosts |
| `networks(searchTerm: "...", first: N)` | Search podcast networks |
| `chartCategories(platform: APPLE_PODCASTS)` | List chart categories (requires paid plan) |

### Identifier Types

The `type` field is required when using `identifier` to fetch a podcast or episode:

| Type | Description |
|------|-------------|
| `PODCHASER` | Podchaser internal ID |
| `APPLE_PODCASTS` | Apple Podcasts ID |
| `SPOTIFY` | Spotify ID |

### Podcast Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | ID | Unique identifier |
| `title` | String | Podcast title |
| `description` | String | Podcast description |
| `url` | String | Podcast website URL |
| `imageUrl` | String | Cover art URL |
| `language` | String | Primary language |
| `ratingAverage` | Float | Average user rating |
| `ratingCount` | Int | Number of ratings |
| `author` | Creator | Podcast author/creator |
| `categories` | [Category] | Associated categories |
| `episodes(first: N)` | EpisodeList | Podcast episodes (paginated) |

### Episode Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | ID | Unique identifier |
| `title` | String | Episode title |
| `description` | String | Episode description |
| `airDate` | Date | Publication date |
| `length` | Int | Duration in seconds |
| `url` | String | Episode URL |
| `imageUrl` | String | Episode artwork URL |
| `podcast` | Podcast | Parent podcast |

### Creator Fields

| Field | Type | Description |
|-------|------|-------------|
| `pcid` | String | Unique identifier |
| `name` | String | Creator name |
| `bio` | String | Biography |
| `imageUrl` | String | Profile image URL |
| `credits` | CreditList | Podcast appearances |

### Filter Options

| Filter | Values |
|--------|--------|
| `categories` | Category slugs |
| `language` | ISO language codes |
| `hasAppleChartRank` | Boolean |
| `hasSpotifyChartRank` | Boolean |

### Sort Options

| sortBy | Description |
|--------|-------------|
| `RELEVANCE` | Search relevance |
| `POPULARITY` | Overall popularity |
| `RATING` | User rating |
| `APPLE_CHART_RANK` | Apple ranking |
| `SPOTIFY_CHART_RANK` | Spotify ranking |
| `LATEST_EPISODE` | Most recent episode |

---

## Rate Limits

- **Request Limit**: 50 requests per 10 seconds
- **Points System**: Query cost based on fields returned
- **Response Headers**:
  - `X-Podchaser-Points-Remaining`: Available points
  - `X-Podchaser-Query-Cost`: Points consumed

**Example costs:**
- Basic podcast metadata: ~9 points
- Search 10 podcasts with details: ~100 points

---

## Guidelines

1. **Store Access Token**: Tokens last 1 year, avoid requesting new tokens for each query
2. **Preview Costs**: Use `/graphql/cost` endpoint to estimate query cost before execution
3. **Use Limited Scope**: For client-side apps, request tokens with `limited_scope: true` (1 hour expiry)
4. **Optimize Queries**: Request only needed fields to minimize points consumption
5. **Handle Rate Limits**: Check `Retry-After` header on 429 responses
6. **Security**: Never expose regular access tokens in client-side code
