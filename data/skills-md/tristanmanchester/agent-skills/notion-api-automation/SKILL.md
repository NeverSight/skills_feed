---
name: notion-api-automation
description: >-
  Automates Notion workspaces via the official Notion REST API and SDKs:
  authenticate an integration, search for pages/databases, query data sources,
  create/update pages and blocks, move pages, apply templates, and handle
  pagination + rate limits.
  Use when the user mentions the Notion API, Notion integrations, Notion databases/data sources,
  syncing content with Notion, or making HTTP requests to api.notion.com.
allowed-tools: Read,Write,Bash(curl:*),Bash(node:*),Bash(npm:*),Bash(python:*)
---

# Notion API Automation

## Why this exists

Notion API work is easy to get “mostly right” and still fail in production due to:
- **Versioning**: `Notion-Version` is required and features differ by version.
- **Database vs data source split**: modern integrations must work with `data_source_id` for “rows”.
- **Properties vs content**: page properties are not the same as page block content.
- **Pagination + throttling**: most listing endpoints are paginated; rate limits are tight.
- **Validation schema**: property values must match the data source schema exactly.

This skill provides reliable, repeatable workflows and drop-in request patterns.

---

## Quick start

### Required environment variables (defaults are safe)
- `NOTION_TOKEN` (preferred) or `NOTION_API_KEY` / `NOTION_API_TOKEN`
- `NOTION_VERSION` (default: `2025-09-03`)
- Optional: `NOTION_BASE_URL` (default: `https://api.notion.com`)

### Smoke test (HTTP)
Use the “bot user” endpoint to verify the token + headers:
```bash
curl https://api.notion.com/v1/users/me \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: ${NOTION_VERSION:-2025-09-03}"
```

### Smoke test (Python script)
```bash
python scripts/notion_request.py GET /v1/users/me
```

### JS/TS (preferred when you’re already in Node)
```bash
npm i @notionhq/client
```

```js
import { Client } from "@notionhq/client"

const notion = new Client({
  auth: process.env.NOTION_TOKEN,
  notionVersion: process.env.NOTION_VERSION ?? "2025-09-03",
})

// 1) Search for a page/database by title fragment
const search = await notion.search({
  query: "Project Alpha",
  page_size: 5,
})

// 2) Retrieve a page (properties only)
const page = await notion.pages.retrieve({ page_id: search.results[0].id })
console.log(page.id)
```

If the SDK lacks a newer endpoint, use raw HTTP (fetch/axios) with the same headers.

---

## Operating rules (do these every time)

1. **Always send these headers**
   - `Authorization: Bearer <token>`
   - `Notion-Version: 2025-09-03` (or whatever the integration is pinned to)
   - `Content-Type: application/json` for JSON bodies

2. **Respect the “database vs data source” model**
   - A **database** is a container; it has one or more **data sources**.
   - Use `data_source_id` to query rows and to move pages into a database.

3. **Know what you’re reading**
   - `GET /v1/pages/{page_id}` returns **properties**, not the page body.
   - Page body is in **blocks**: `GET /v1/blocks/{block_id}/children` (use `page_id` as `block_id`).

4. **No empty strings**
   - To clear strings and similar fields, set them to `null`, not `""`.

5. **Pagination is mandatory for “list/query/search”**
   - Loop on `has_more` + `next_cursor`
   - Send `start_cursor` and `page_size` (often 1–100)

6. **Throttle + retry**
   - Handle HTTP `429 rate_limited`; honour `Retry-After`.
   - Prefer sequential writes unless you have a proper rate limiter.

7. **Validate after writing**
   - Retrieve the updated resource and confirm the expected fields changed.

---

## Core workflows (copy + tick)

### A) Identify IDs (page/database/data_source/block)
- [ ] If you have a Notion URL: extract the 32-char/UUID id (script: `scripts/notion_extract_id.py`)
- [ ] If you only have a title: use `POST /v1/search` to find candidate pages/databases
- [ ] If you have a `database_id` and need rows: call `GET /v1/databases/{database_id}` and choose a `data_source_id`

See: `references/versioning-data-sources.md` and `references/endpoints.md`.

### B) Read data
- [ ] Page properties: `GET /v1/pages/{page_id}`
- [ ] Page content: `GET /v1/blocks/{page_id}/children` (+ recurse if `has_children`)
- [ ] Data source rows: `POST /v1/data_sources/{data_source_id}/query`

See: `references/blocks.md` and `references/pagination-rate-limits.md`.

### C) Write data (properties)
- [ ] Create page (row) under a data source: `POST /v1/pages` with `parent.type=data_source_id`
- [ ] Update page properties: `PATCH /v1/pages/{page_id}`
- [ ] Archive/restore page: set `archived` or `in_trash`

See: `references/property-values.md`.

### D) Write data (content / blocks)
- [ ] Append children blocks: `PATCH /v1/blocks/{block_id}/children`
- [ ] Insert not-at-end: use `"after": "<block_id>"` when appending
- [ ] Update a block (supported block types only): `PATCH /v1/blocks/{block_id}`
- [ ] Delete/trash a block: `DELETE /v1/blocks/{block_id}` (destructive)

See: `references/blocks.md`.

### E) Move pages (re-parent)
- [ ] Move under another page: `POST /v1/pages/{page_id}/move` with `parent.type=page_id`
- [ ] Move into a database: `POST /v1/pages/{page_id}/move` with `parent.type=data_source_id`
- [ ] When moving into a database: **use data source id**, not database id

See: `references/recipes.md`.

### F) Templates
- [ ] List templates: `GET /v1/data_sources/{data_source_id}/templates`
- [ ] Create page with a template (recommended for consistent scaffolding)
- [ ] If your integration must act after the template applies: wait/poll or use webhooks

See: `references/recipes.md`.

---

## Troubleshooting (fast diagnosis)

Use the response `"code"` + HTTP status:

- `400 missing_version` → you forgot `Notion-Version`
- `401 unauthorized` → token invalid / wrong env var
- `403 restricted_resource` → integration lacks access or capabilities for that endpoint
- `404 object_not_found` → wrong ID **or** page/database not shared with the integration
- `429 rate_limited` → throttle; retry after `Retry-After`
- `400 validation_error` → request body schema mismatch (often property values)
- `409 conflict_error` → retry; re-fetch latest ids/objects if necessary

For a full list, see `references/endpoints.md` and the official status codes docs.

---

## Safety tiers for write operations

| Tier | Auto-OK? | Examples |
|------|----------|----------|
| SAFE | Yes | Search, retrieve page, query data source |
| CAUTION | Yes (validate afterwards) | Update properties, append blocks |
| DANGEROUS | Only if explicitly requested | `erase_content`, delete blocks, bulk-archive/trash, bulk-move |

If a user asks for a bulk destructive operation but hasn’t specified scope (which pages? which data source?), do the read-only discovery steps first and present a plan + exact targets.

---

## THE EXACT PROMPT — Notion API execution plan

```text
You are operating on a Notion workspace via the public Notion API.

Goal:
- [state the user goal precisely]

Constraints:
- Use Notion-Version 2025-09-03 unless the user specifies otherwise.
- Respect pagination and the 3 rps average rate limit; handle 429 with Retry-After.
- Treat “database” vs “data source” correctly (query rows via data_sources).
- Avoid destructive actions unless the user explicitly asks; if destructive, enumerate targets first.
- Validate by retrieving the changed objects after writes.

Plan:
1) Identify required IDs (page_id, database_id, data_source_id, block_id).
2) Verify access (retrieve or search). If 404, explain how to share the resource with the integration.
3) Choose endpoints + request bodies.
4) Implement using @notionhq/client if available; otherwise raw HTTP with correct headers.
5) Run a validation loop: retrieve → compare expected fields → report results.
```

---

## References (load as-needed)

- `references/endpoints.md` — endpoint map + “what to call when”
- `references/versioning-data-sources.md` — versioning + database/data_source model
- `references/property-values.md` — property JSON patterns for create/update
- `references/blocks.md` — block JSON patterns for content
- `references/pagination-rate-limits.md` — pagination + retry patterns
- `references/recipes.md` — multi-step workflows (move pages, bulk ops, templates)

Quick grep:
```bash
grep -RIn "data_source_id" references/
grep -RIn "pages/{page_id}/move" references/
grep -RIn "Retry-After" references/
```

---

## Scripts

- `python scripts/notion_request.py METHOD PATH [--json JSON] [--json-file FILE] [--paginate]`
- `python scripts/notion_extract_id.py "<notion url or id>"`
