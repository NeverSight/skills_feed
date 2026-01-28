---
name: readthedocs-project-manager
description: Manage Read the Docs projects via the RTD API. Use when creating projects, listing repos, triggering builds, syncing versions, or checking build status on Read the Docs.
---

# Read the Docs Project Manager

Use the Read the Docs API to create and manage projects. This skill covers the
core project lifecycle tasks that are commonly needed for setup and verification.

## Required inputs

- RTD host in `RTD_HOST`
  - Community: `https://app.readthedocs.org`
  - Business: `https://app.readthedocs.com`
- API token available in `RTD_TOKEN` (preferred) or provided by the user

## Quick workflow

1. Confirm host and token source.
2. Collect project inputs (name, slug, repo URL, repo type).
3. Create the project via API.
4. Trigger a build or sync versions if needed.
5. Poll the latest build status.

## API basics

Base URL:
```
${RTD_HOST}/api/v3/
```

All authenticated requests:
```
-H "Authorization: Token $RTD_TOKEN"
```

## Common tasks

### 1) List remote repositories (optional)

Use this when you need to verify repo access or pick a repo from integrations.
```
GET /api/v3/remote/repositories/
```

Example:
```bash
curl -s -H "Authorization: Token $RTD_TOKEN" \
  "${RTD_HOST}/api/v3/remote/repositories/"
```

### 2) Create a project

```
POST /api/v3/projects/
```

Minimal body:
```json
{
  "name": "Project Name",
  "slug": "project-slug",
  "repository": {
    "url": "https://github.com/org/repo",
    "type": "git"
  }
}
```

Example:
```bash
curl -s -X POST "${RTD_HOST}/api/v3/projects/" \
  -H "Authorization: Token $RTD_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Project Name","slug":"project-slug","repository":{"url":"https://github.com/org/repo","type":"git"}}'
```

### 3) Sync versions

```
POST /api/v3/projects/{slug}/sync-versions/
```

```bash
curl -s -X POST \
  -H "Authorization: Token $RTD_TOKEN" \
  "${RTD_HOST}/api/v3/projects/project-slug/sync-versions/"
```

### 4) Trigger a build

```
POST /api/v3/projects/{slug}/versions/{version}/builds/
```

```bash
curl -s -X POST \
  -H "Authorization: Token $RTD_TOKEN" \
  "${RTD_HOST}/api/v3/projects/project-slug/versions/latest/builds/"
```

### 5) Check latest build status

```
GET /api/v3/projects/{slug}/builds/?limit=1
```

```bash
curl -s -H "Authorization: Token $RTD_TOKEN" \
  "${RTD_HOST}/api/v3/projects/project-slug/builds/?limit=1"
```

## Notes

- Use the community host for public RTD, and your Business host for private instances.
- Do not print or log token values in responses.
- If project creation fails, confirm the slug is available and the repo URL is reachable.
