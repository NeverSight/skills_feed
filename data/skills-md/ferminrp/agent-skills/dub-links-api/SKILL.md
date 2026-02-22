---
name: dub-links-api
description: >
  Integrates Dub Links API endpoints to create, update, delete,
  retrieve, list, count, and run bulk operations on short links.
  Use when the user asks for "dub links api", "create link dub",
  "upsert link dub", "list links", "count links", "bulk links",
  or lookups by linkId/domain+key/externalId.
---

# Dub Links API

Skill for integrating Dub Links API with strict scope limited to `/links*` endpoints.

## API Overview

- **Base URL**: `https://api.dub.co`
- **Auth**: Bearer token required
- **Header**: `Authorization: Bearer <DUB_API_KEY>`
- **Response format**: JSON
- **Scope**: Links endpoints only
- **Docs**: `https://dub.co/docs/api-reference/endpoint/create-a-link`
- **Token docs (onboarding)**: `https://dub.co/docs/api-reference/tokens`
- **Local snapshot**: `references/openapi-spec.json`

## API Key Onboarding

Use this flow when the user does not have an API key yet:

1. Create a Dub account/workspace (if needed).
2. Go to the dashboard token section (per docs):
   - `https://dub.co/docs/api-reference/tokens`
3. Generate an API key and export it in shell:
   - `export DUB_API_KEY="..."`
4. Validate credentials with a Links endpoint:
   - `curl -s -H "Authorization: Bearer $DUB_API_KEY" "https://api.dub.co/links/count" | jq '.'`

Useful onboarding note: if initial signup is needed, this referral can be used:
`https://refer.dub.co/agents`

## Links Endpoints

### 1) Create

- `POST /links`
- Creates a link in the authenticated workspace.
- Minimum recommended body: `url`.

```bash
curl -s -X POST "https://api.dub.co/links" \
  -H "Authorization: Bearer $DUB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}' | jq '.'
```

### 2) Update

- `PATCH /links/{linkId}`
- Updates an existing link by `linkId` (also accepts `externalId` prefixed with `ext_`).

```bash
curl -s -X PATCH "https://api.dub.co/links/{linkId}" \
  -H "Authorization: Bearer $DUB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/new"}' | jq '.'
```

### 3) Upsert

- `PUT /links/upsert`
- If a link with the same URL exists, returns/updates it; otherwise creates it.

```bash
curl -s -X PUT "https://api.dub.co/links/upsert" \
  -H "Authorization: Bearer $DUB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}' | jq '.'
```

### 4) Delete

- `DELETE /links/{linkId}`
- Deletes a link by `linkId` (also accepts `externalId` prefixed with `ext_`).
- Response: `{"id": "string"}`.

```bash
curl -s -X DELETE "https://api.dub.co/links/{linkId}" \
  -H "Authorization: Bearer $DUB_API_KEY" | jq '.'
```

### 5) Retrieve one

- `GET /links/info`
- Retrieves a link by one of these selectors:
  - `domain + key`
  - `linkId`
  - `externalId`

```bash
curl -s "https://api.dub.co/links/info?domain=acme.link&key=promo" \
  -H "Authorization: Bearer $DUB_API_KEY" | jq '.'
```

### 6) List

- `GET /links`
- Returns paginated list with filters.
- Common query params: `domain`, `search`, `tagIds`, `tagNames`, `folderId`, `userId`, `tenantId`, `showArchived`, `page`, `pageSize` (default: 100, max: 100), `sortBy` (`createdAt`|`clicks`|`saleAmount`|`lastClicked`), `sortOrder` (`asc`|`desc`).

```bash
curl -s "https://api.dub.co/links?page=1&pageSize=100&sortBy=createdAt&sortOrder=desc" \
  -H "Authorization: Bearer $DUB_API_KEY" | jq '.'
```

### 7) Count

- `GET /links/count`
- Returns number of links for the provided filters.
- Common query params: `domain`, `search`, `tagIds`, `tagNames`, `folderId`, `userId`, `tenantId`, `showArchived`, `groupBy` (`domain`|`tagId`|`userId`|`folderId`).

```bash
curl -s "https://api.dub.co/links/count?domain=acme.link" \
  -H "Authorization: Bearer $DUB_API_KEY" | jq '.'
```

### 8) Bulk create

- `POST /links/bulk`
- Creates up to 100 links.
- Body: array of objects (each item should include `url`).

```bash
curl -s -X POST "https://api.dub.co/links/bulk" \
  -H "Authorization: Bearer $DUB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '[{"url":"https://example.com/a"},{"url":"https://example.com/b"}]' | jq '.'
```

### 9) Bulk update

- `PATCH /links/bulk`
- Updates up to 100 links.
- Body requires `data`; target selection via `linkIds` or `externalIds`.

```bash
curl -s -X PATCH "https://api.dub.co/links/bulk" \
  -H "Authorization: Bearer $DUB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"linkIds":["lnk_123","lnk_456"],"data":{"archived":true}}' | jq '.'
```

### 10) Bulk delete

- `DELETE /links/bulk`
- Deletes up to 100 links. Non-existing IDs are ignored. **Irreversible.**
- Required query param: `linkIds` (comma-separated).
- Response: `{"deletedCount": number}`.

```bash
curl -s -X DELETE "https://api.dub.co/links/bulk?linkIds=lnk_123,lnk_456" \
  -H "Authorization: Bearer $DUB_API_KEY" | jq '.'
```

## Key Fields

Common response fields (from `LinkSchema`):

- `id`
- `domain`
- `key`
- `shortLink`
- `url`
- `createdAt`
- `updatedAt`
- `archived`
- `externalId`
- `tags`
- `folderId`

Result shapes by endpoint:

- `GET /links`: array of links
- `GET /links/count`: number
- Bulk endpoints: array/object depending on operation

## Recommended Workflow

1. Detect intent: create/update/upsert/delete/get/list/count/bulk.
2. Validate minimum inputs (`url`, `linkId`, filters, bulk ids).
3. Execute request with `curl -s` and Bearer header.
4. Parse with `jq` and verify logical operation result.
5. Respond first with a useful snapshot:
   - `id`, `shortLink`, `url`, and `archived` status when relevant.
6. For lists, provide a short table with relevant columns.
7. Keep strict scope on `/links*`.

## Error Handling

- **401/403**: missing, invalid, or unauthorized token.
- **404**: link not found for `linkId` or `GET /links/info` criteria.
- **422**: invalid payload (missing/invalid fields).
- **429**: rate limited; respect `Retry-After` if present.
- **Network/timeout**: retry up to 2 times with short delay.
- **Unexpected JSON**: return minimal raw output and warn about inconsistency.

## Presenting Results

Recommended output format:

- Executive summary (action + result).
- Short table for multiple links:
  - `id | domain | key | shortLink | url | createdAt`
- For bulk operations:
  - requested total, processed total, errors if any.
- Clarify data is scoped to the authenticated workspace.

## Out of Scope

This skill must not use:

- Analytics, events, conversions, partners, customers, commissions, payouts endpoints.
- Domains, folders, tags endpoints.
- `/tokens/*` endpoints (including `/tokens/embed/referrals`).

The tokens page is used only for API key onboarding, not as operational scope.

## OpenAPI Spec

Use `references/openapi-spec.json` as the stable local source for methods, paths, parameters, and schemas.
