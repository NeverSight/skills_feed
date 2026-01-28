---
name: readthedocs-redirects-manager
description: Manage Read the Docs redirects via the RTD API. Use when listing, creating, updating, or deleting custom redirects for a project.
---

# Read the Docs Redirects Manager

Use the Read the Docs API to manage custom redirects for a project.

## Required inputs

- RTD host in `RTD_HOST`
  - Community: `https://app.readthedocs.org`
  - Business: `https://app.readthedocs.com`
- API token available in `RTD_TOKEN` (preferred) or provided by the user
- Project slug

## Redirect model (API v3)

Fields commonly used in redirect requests/responses:

- `from_url`: source path (e.g., `/old-page/`)
- `to_url`: destination path or URL (e.g., `/new-page/`)
- `type`: redirect type (e.g., `page`, `exact`, `clean_url_to_html`, `html_to_clean_url`)
- `http_status`: HTTP status code (commonly `301` or `302`)
- `description`: optional note
- `enabled`: `true`/`false`
- `force`: apply even if the page exists (availability depends on plan)
- `position`: priority order (lower is higher priority)

## Common tasks

### 1) List redirects

```
GET /api/v3/projects/{slug}/redirects/
```

```bash
curl -s -H "Authorization: Token $RTD_TOKEN" \
  "${RTD_HOST}/api/v3/projects/project-slug/redirects/"
```

### 2) Create a redirect

```
POST /api/v3/projects/{slug}/redirects/
```

```bash
curl -s -X POST \
  -H "Authorization: Token $RTD_TOKEN" \
  -H "Content-Type: application/json" \
  "${RTD_HOST}/api/v3/projects/project-slug/redirects/" \
  -d '{
    "from_url": "/old-page/",
    "to_url": "/new-page/",
    "type": "page",
    "http_status": 301,
    "description": "Move old page to new location",
    "enabled": true
  }'
```

### 3) Update a redirect

```
PUT /api/v3/projects/{slug}/redirects/{id}/
```

```bash
curl -s -X PUT \
  -H "Authorization: Token $RTD_TOKEN" \
  -H "Content-Type: application/json" \
  "${RTD_HOST}/api/v3/projects/project-slug/redirects/123/" \
  -d '{
    "from_url": "/old-page/",
    "to_url": "/new-page/",
    "type": "page",
    "http_status": 302,
    "description": "Temporary redirect during migration",
    "enabled": true
  }'
```

### 4) Delete a redirect

```
DELETE /api/v3/projects/{slug}/redirects/{id}/
```

```bash
curl -s -X DELETE \
  -H "Authorization: Token $RTD_TOKEN" \
  "${RTD_HOST}/api/v3/projects/project-slug/redirects/123/"
```

## Notes

- Use `page` redirects for version-agnostic moves and `exact` for version/language-specific URLs.
- Order matters: earlier rules win when multiple redirects match.
- Do not print or log token values in responses.
