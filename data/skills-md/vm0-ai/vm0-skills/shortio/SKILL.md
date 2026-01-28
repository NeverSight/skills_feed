---
name: shortio
description: Short.io URL shortener API via curl. Use this skill to create, manage, and track short links on custom branded domains.
vm0_secrets:
  - SHORTIO_API_KEY
vm0_vars:
  - SHORTIO_DOMAIN
---

# Short.io

Use Short.io via direct `curl` calls to **create and manage short links** on your branded domain.

> Official docs: `https://developers.short.io/docs`

---

## When to Use

Use this skill when you need to:

- **Create short links** from long URLs
- **Customize link slugs** (paths) for branded URLs
- **Track link clicks** and analytics
- **Manage multiple links** (list, update, delete)
- **Set link expiration** using TTL (time-to-live)

---

## Prerequisites

1. Sign up at [Short.io](https://short.io/)
2. Add and configure your custom domain (or use the default short.io domain)
3. Go to [Integrations & API](https://app.short.io/settings/integrations/api-key) and create a **Secret API Key**
4. Get your domain ID from Domain Settings (visible in browser URL bar)

```bash
export SHORTIO_API_KEY="your-secret-api-key"
export SHORTIO_DOMAIN="your-domain.com"
export SHORTIO_DOMAIN_ID="123456" # Optional, needed for list/stats operations
```

### Pricing

- Free tier: 1,000 links, 50,000 tracked clicks/month
- API key is passed in the `Authorization` header

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"' | jq .
> ```

## How to Use

All examples below assume you have `SHORTIO_API_KEY` and `SHORTIO_DOMAIN` set.

Base URL: `https://api.short.io`

---

### 1. Create a Short Link

Create a new short link with auto-generated slug:

Write to `/tmp/shortio_request.json`:

```json
{
  "domain": "<your-domain-name>",
  "originalURL": "https://example.com/very/long/url/here"
}
```

Then run:

```bash
curl -s -X POST "https://api.short.io/links" --header "Authorization: ${SHORTIO_API_KEY}" --header "Content-Type: application/json" --header "Accept: application/json" -d @/tmp/shortio_request.json | jq '{shortURL, originalURL, path, idString}'
```

---

### 2. Create with Custom Slug

Create a short link with a custom path/slug:

Write to `/tmp/shortio_request.json`:

```json
{
  "domain": "<your-domain-name>",
  "originalURL": "https://example.com/product/12345",
  "path": "my-custom-slug"
}
```

Then run:

```bash
curl -s -X POST "https://api.short.io/links" --header "Authorization: ${SHORTIO_API_KEY}" --header "Content-Type: application/json" --header "Accept: application/json" -d @/tmp/shortio_request.json | jq '{shortURL, originalURL, path, idString}'
```

---

### 3. Create with TTL (Expiration)

Create a link that expires after a specified time (in ISO 8601 format):

Write to `/tmp/shortio_request.json`:

```json
{
  "domain": "<your-domain-name>",
  "originalURL": "https://example.com/temporary-offer",
  "ttl": "2026-12-31T23:59:59Z"
}
```

Then run:

```bash
curl -s -X POST "https://api.short.io/links" --header "Authorization: ${SHORTIO_API_KEY}" --header "Content-Type: application/json" --header "Accept: application/json" -d @/tmp/shortio_request.json | jq '{shortURL, originalURL, ttl}'
```

---

### 4. Get Link Info by Path

Get details of a short link using domain and path:

```bash
bash -c 'curl -s -X GET "https://api.short.io/links/expand?domain=${SHORTIO_DOMAIN}&path=my-custom-slug" --header "Authorization: ${SHORTIO_API_KEY}" --header "Accept: application/json"' | jq '{originalURL, shortURL, path, idString, createdAt, cloaking}
```

---

### 5. Get Link Info by ID

Get details of a short link using its ID:

```bash
LINK_ID="lnk_abc123xyz"

bash -c 'curl -s -X GET "https://api.short.io/links/${LINK_ID}" --header "Authorization: ${SHORTIO_API_KEY}" --header "Accept: application/json"' | jq '{originalURL, shortURL, path, idString, createdAt}
```

---

### 6. List All Links

Get a list of links for a domain (max 150 per request):

```bash
bash -c 'curl -s -X GET "https://api.short.io/api/links?domain_id=${SHORTIO_DOMAIN_ID}&limit=20" --header "Authorization: ${SHORTIO_API_KEY}" --header "Accept: application/json"' | jq '{count, links: [.links[] | {shortURL, originalURL, path, idString}]}'
```

---

### 7. Update a Link

Update an existing link's path, original URL, or other properties:

```bash
LINK_ID="lnk_abc123xyz"
```

Write to `/tmp/shortio_request.json`:

```json
{
  "path": "new-custom-slug",
  "originalURL": "https://example.com/new-destination"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.short.io/links/${LINK_ID}" --header "Authorization: ${SHORTIO_API_KEY}" --header "Content-Type: application/json" --header "Accept: application/json" -d @/tmp/shortio_request.json' | jq '{shortURL, originalURL, path, idString}'
```

---

### 8. Delete a Link

Delete a short link by ID:

```bash
LINK_ID="lnk_abc123xyz"

bash -c 'curl -s -X DELETE "https://api.short.io/links/${LINK_ID}" --header "Authorization: ${SHORTIO_API_KEY}" --header "Accept: application/json"' | jq '{success, idString}'
```

---

### 9. List Domains

Get all domains associated with your account:

```bash
bash -c 'curl -s -X GET "https://api.short.io/api/domains" --header "Authorization: ${SHORTIO_API_KEY}" --header "Accept: application/json"' | jq '.[] | {id, hostname, state, linkType}'
```

---

### 10. Get Link Click Statistics

Get click counts for specific links:

```bash
bash -c 'curl -s -X GET "https://api.short.io/domains/${SHORTIO_DOMAIN_ID}/link_clicks?link_ids=${LINK_ID}" --header "Authorization: ${SHORTIO_API_KEY}" --header "Accept: application/json"' | jq '{linkId: .linkId, clicks}'
```

---

## Create Link Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `domain` | string | Yes | Your branded domain |
| `originalURL` | string | Yes | The destination URL |
| `path` | string | No | Custom slug (auto-generated if not provided) |
| `title` | string | No | Link title for organization |
| `ttl` | string | No | Expiration date (ISO 8601 format) |
| `allowDuplicates` | boolean | No | Allow creating duplicate links (default: false) |
| `cloaking` | boolean | No | Enable URL cloaking |
| `password` | string | No | Password protect the link |
| `expiresAt` | string | No | Redirect URL when link expires |
| `tags` | array | No | Tags for categorization |

---

## Response Fields

| Field | Description |
|-------|-------------|
| `shortURL` | The generated short URL |
| `secureShortURL` | HTTPS version of short URL |
| `originalURL` | The destination URL |
| `path` | The slug/path of the short link |
| `idString` | Unique link ID (use for updates/deletes) |
| `DomainId` | Domain ID |
| `createdAt` | Creation timestamp |
| `cloaking` | Whether cloaking is enabled |
| `hasPassword` | Whether link is password protected |

---

## Guidelines

1. **Save the idString**: Always store the `idString` from the response - you'll need it to update or delete links
2. **Use TTL for temporary links**: Set expiration for promotional or time-sensitive links
3. **Limit parameter**: When listing links, max limit is 150 per request; use pagination for more
4. **Custom domains**: Configure DNS properly before using custom domains
5. **Avoid duplicates**: Set `allowDuplicates: false` to prevent creating multiple short links for the same URL
6. **Check rate limits**: API has rate limiting; implement retries with backoff for high-volume usage
