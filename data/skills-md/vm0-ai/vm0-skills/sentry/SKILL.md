---
name: sentry
description: Sentry API via curl. Use this skill to manage error tracking, list issues, resolve errors, and monitor releases in Sentry.
vm0_secrets:
  - SENTRY_TOKEN
vm0_vars:
  - SENTRY_HOST
  - SENTRY_ORG
---

# Sentry API

Use the Sentry API via direct `curl` calls to manage **error tracking, issues, projects, and releases**.

> Official docs: `https://docs.sentry.io/api/`

---

## When to Use

Use this skill when you need to:

- **List and search issues** - find errors and exceptions
- **Resolve or ignore issues** - manage issue status
- **View issue details** - get stack traces and event data
- **Manage projects** - list and configure projects
- **Track releases** - create and monitor releases
- **View events** - get detailed error events

---

## Prerequisites

1. Go to Sentry → Settings → Developer Settings → Internal Integrations
2. Create a new Internal Integration with required scopes (see below)
3. Copy the generated token

```bash
export SENTRY_HOST="sentry.io" # Or your self-hosted Sentry domain
export SENTRY_TOKEN="sntrys_..." # Auth token from Internal Integration
export SENTRY_ORG="your-org-slug" # Your organization slug
```

### Required Scopes

- `project:read` - List and view projects
- `event:read` - View issues and events
- `event:write` - Update issues (resolve, ignore, assign)
- `release:read` - View releases
- `release:write` - Create releases

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"'
> ```

## How to Use

All examples below assume `SENTRY_HOST`, `SENTRY_TOKEN`, and `SENTRY_ORG` are set.

Base URL: `https://${SENTRY_HOST}/api/0`

---

### 1. List Your Projects

Get all projects you have access to:

```bash
bash -c 'curl -s "https://${SENTRY_HOST}/api/0/projects/" --header "Authorization: Bearer ${SENTRY_TOKEN}"' | jq '.[] | {slug, name, platform, dateCreated}'
```

---

### 2. Get Project Details

Get details for a specific project:

> **Note:** Replace `my-project` with your actual project slug from the "List Your Projects" output above.

```bash
PROJECT_SLUG="my-project"

bash -c 'curl -s "https://${SENTRY_HOST}/api/0/projects/${SENTRY_ORG}/${PROJECT_SLUG}/" --header "Authorization: Bearer ${SENTRY_TOKEN}"' | jq '{slug, name, platform, status, dateCreated}'
```

---

### 3. List Organization Issues

Get all issues across the organization:

```bash
bash -c 'curl -s "https://${SENTRY_HOST}/api/0/organizations/${SENTRY_ORG}/issues/" --header "Authorization: Bearer ${SENTRY_TOKEN}"' | jq '.[] | {id, shortId, title, culprit, status, count, userCount, firstSeen, lastSeen}
```

Query parameters:
- `query=is:unresolved` - Filter by status
- `query=error.type:TypeError` - Filter by error type
- `sort=date` - Sort by last seen (default)
- `sort=new` - Sort by first seen
- `sort=freq` - Sort by event count

---

### 4. List Project Issues

Get issues for a specific project:

> **Note:** Replace `my-project` with your actual project slug from the "List Your Projects" output.

```bash
PROJECT_SLUG="my-project"

bash -c 'curl -s "https://${SENTRY_HOST}/api/0/projects/${SENTRY_ORG}/${PROJECT_SLUG}/issues/" --header "Authorization: Bearer ${SENTRY_TOKEN}"' | jq '.[] | {id, shortId, title, status, count, lastSeen}
```

---

### 5. Search Issues

Search issues with query:

Write to `/tmp/sentry_query.txt`:

```
is:unresolved level:error
```

```bash
bash -c 'curl -s -G "https://${SENTRY_HOST}/api/0/organizations/${SENTRY_ORG}/issues/" --header "Authorization: Bearer ${SENTRY_TOKEN}" --data-urlencode "query@/tmp/sentry_query.txt"' | jq '.[] | {shortId, title, level, count}
```

Common query filters:
- `is:unresolved` / `is:resolved` / `is:ignored` - By status
- `level:error` / `level:warning` / `level:info` - By level
- `assigned:me` / `assigned:none` - By assignee
- `browser:Chrome` - By browser
- `os:Windows` - By OS
- `release:1.0.0` - By release version

---

### 6. Get Issue Details

Get details for a specific issue:

> **Note:** Replace `123456789` with an actual issue ID from the "List Issues" or "List Project Issues" output (use the `id` field, not `shortId`).

```bash
ISSUE_ID="123456789"

bash -c 'curl -s "https://${SENTRY_HOST}/api/0/organizations/${SENTRY_ORG}/issues/${ISSUE_ID}/" --header "Authorization: Bearer ${SENTRY_TOKEN}"' | jq '{id, shortId, title, culprit, status, level, count, userCount, firstSeen, lastSeen, assignedTo}'
```

---

### 7. Get Latest Event for Issue

Get the most recent event for an issue:

> **Note:** Replace `123456789` with an actual issue ID from the "List Issues" output.

```bash
ISSUE_ID="123456789"

bash -c 'curl -s "https://${SENTRY_HOST}/api/0/organizations/${SENTRY_ORG}/issues/${ISSUE_ID}/events/latest/" --header "Authorization: Bearer ${SENTRY_TOKEN}"' | jq '{eventID, message, platform, dateCreated, tags, contexts}'
```

---

### 8. List Issue Events

Get all events for an issue:

> **Note:** Replace `123456789` with an actual issue ID from the "List Issues" output.

```bash
ISSUE_ID="123456789"

bash -c 'curl -s "https://${SENTRY_HOST}/api/0/organizations/${SENTRY_ORG}/issues/${ISSUE_ID}/events/" --header "Authorization: Bearer ${SENTRY_TOKEN}"' | jq '.[] | {eventID, message, dateCreated}
```

---

### 9. Resolve Issue

Mark an issue as resolved:

> **Note:** Replace `123456789` with an actual issue ID from the "List Issues" output.

```bash
ISSUE_ID="123456789"
```

Write to `/tmp/sentry_request.json`:

```json
{
  "status": "resolved"
}
```

Then run:

```bash
bash -c 'curl -s -X PUT "https://${SENTRY_HOST}/api/0/organizations/${SENTRY_ORG}/issues/${ISSUE_ID}/" --header "Authorization: Bearer ${SENTRY_TOKEN}" --header "Content-Type: application/json" -d @/tmp/sentry_request.json' | jq '{id, shortId, status}'
```

---

### 10. Resolve in Next Release

Mark issue as resolved in next release:

> **Note:** Replace `123456789` with an actual issue ID from the "List Issues" output.

```bash
ISSUE_ID="123456789"
```

Write to `/tmp/sentry_request.json`:

```json
{
  "status": "resolvedInNextRelease"
}
```

Then run:

```bash
bash -c 'curl -s -X PUT "https://${SENTRY_HOST}/api/0/organizations/${SENTRY_ORG}/issues/${ISSUE_ID}/" --header "Authorization: Bearer ${SENTRY_TOKEN}" --header "Content-Type: application/json" -d @/tmp/sentry_request.json' | jq '{id, shortId, status}'
```

---

### 11. Ignore Issue

Ignore an issue:

> **Note:** Replace `123456789` with an actual issue ID from the "List Issues" output.

```bash
ISSUE_ID="123456789"
```

Write to `/tmp/sentry_request.json`:

```json
{
  "status": "ignored"
}
```

Then run:

```bash
bash -c 'curl -s -X PUT "https://${SENTRY_HOST}/api/0/organizations/${SENTRY_ORG}/issues/${ISSUE_ID}/" --header "Authorization: Bearer ${SENTRY_TOKEN}" --header "Content-Type: application/json" -d @/tmp/sentry_request.json' | jq '{id, shortId, status}'
```

Ignore with duration (in minutes):

Write to `/tmp/sentry_request.json`:

```json
{
  "status": "ignored",
  "statusDetails": {
    "ignoreDuration": 60
  }
}
```

Then run:

```bash
bash -c 'curl -s -X PUT "https://${SENTRY_HOST}/api/0/organizations/${SENTRY_ORG}/issues/${ISSUE_ID}/" --header "Authorization: Bearer ${SENTRY_TOKEN}" --header "Content-Type: application/json" -d @/tmp/sentry_request.json' | jq '{id, shortId, status}'
```

---

### 12. Unresolve Issue

Reopen a resolved issue:

> **Note:** Replace `123456789` with an actual issue ID from the "List Issues" output.

```bash
ISSUE_ID="123456789"
```

Write to `/tmp/sentry_request.json`:

```json
{
  "status": "unresolved"
}
```

Then run:

```bash
bash -c 'curl -s -X PUT "https://${SENTRY_HOST}/api/0/organizations/${SENTRY_ORG}/issues/${ISSUE_ID}/" --header "Authorization: Bearer ${SENTRY_TOKEN}" --header "Content-Type: application/json" -d @/tmp/sentry_request.json' | jq '{id, shortId, status}'
```

---

### 13. Assign Issue

Assign an issue to a user:

> **Note:** Replace `123456789` with an actual issue ID from the "List Issues" output. Replace `<user-email>` with a valid user email from your Sentry organization members.

Write to `/tmp/sentry_request.json`:

```json
{
  "assignedTo": "<user-email>"
}
```

Then run:

```bash
bash -c 'curl -s -X PUT "https://${SENTRY_HOST}/api/0/organizations/${SENTRY_ORG}/issues/${ISSUE_ID}/" --header "Authorization: Bearer ${SENTRY_TOKEN}" --header "Content-Type: application/json" -d @/tmp/sentry_request.json' | jq '{id, shortId, assignedTo}'
```

> **Note:** Replace `123456789` in the URL with the actual issue ID from the "List Issues" output.

---

### 14. Bulk Update Issues

Update multiple issues at once:

> **Note:** Replace `123456789` and `987654321` with actual issue IDs from the "List Issues" output.

Write to `/tmp/sentry_request.json`:

```json
{
  "id": ["123456789", "987654321"],
  "status": "resolved"
}
```

Then run:

```bash
bash -c 'curl -s -X PUT "https://${SENTRY_HOST}/api/0/organizations/${SENTRY_ORG}/issues/" --header "Authorization: Bearer ${SENTRY_TOKEN}" --header "Content-Type: application/json" -d @/tmp/sentry_request.json'
```

---

### 15. Delete Issue

Delete an issue (requires admin permissions):

> **Note:** Replace `123456789` with an actual issue ID from the "List Issues" output.

```bash
ISSUE_ID="123456789"

bash -c 'curl -s -X DELETE "https://${SENTRY_HOST}/api/0/organizations/${SENTRY_ORG}/issues/${ISSUE_ID}/" --header "Authorization: Bearer ${SENTRY_TOKEN}" -w "\nHTTP Status: %{http_code}"'
```

---

### 16. List Releases

Get all releases for the organization:

```bash
bash -c 'curl -s "https://${SENTRY_HOST}/api/0/organizations/${SENTRY_ORG}/releases/" --header "Authorization: Bearer ${SENTRY_TOKEN}"' | jq '.[] | {version, dateCreated, newGroups, projects: [.projects[].slug]}'
```

---

### 17. Get Release Details

Get details for a specific release:

> **Note:** Replace `1.0.0` with an actual release version from the "List Releases" output.

```bash
RELEASE_VERSION="1.0.0"

bash -c 'curl -s "https://${SENTRY_HOST}/api/0/organizations/${SENTRY_ORG}/releases/${RELEASE_VERSION}/" --header "Authorization: Bearer ${SENTRY_TOKEN}"' | jq '{version, dateCreated, dateReleased, newGroups, lastEvent, projects}'
```

---

### 18. Create Release

Create a new release:

> **Note:** Replace `<your-project-slug>` with your actual project slug from the "List Your Projects" output.

Write to `/tmp/sentry_request.json`:

```json
{
  "version": "1.0.1",
  "projects": ["<your-project-slug>"]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://${SENTRY_HOST}/api/0/organizations/${SENTRY_ORG}/releases/" --header "Authorization: Bearer ${SENTRY_TOKEN}" --header "Content-Type: application/json" -d @/tmp/sentry_request.json' | jq '{version, dateCreated}'
```

---

### 19. Create Release with Commits

Create release with associated commits:

> **Note:** Replace `<your-project-slug>` with your actual project slug from the "List Your Projects" output.

Write to `/tmp/sentry_request.json`:

```json
{
  "version": "1.0.2",
  "projects": ["<your-project-slug>"],
  "refs": [
    {
      "repository": "owner/repo",
      "commit": "abc123def456"
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://${SENTRY_HOST}/api/0/organizations/${SENTRY_ORG}/releases/" --header "Authorization: Bearer ${SENTRY_TOKEN}" --header "Content-Type: application/json" -d @/tmp/sentry_request.json' | jq '{version, dateCreated}'
```

---

### 20. List Project Error Events

Get recent error events for a project:

> **Note:** Replace `my-project` with your actual project slug from the "List Your Projects" output.

```bash
PROJECT_SLUG="my-project"

bash -c 'curl -s "https://${SENTRY_HOST}/api/0/projects/${SENTRY_ORG}/${PROJECT_SLUG}/events/" --header "Authorization: Bearer ${SENTRY_TOKEN}"' | jq '.[] | {eventID, title, message, dateCreated}'
```

---

## Issue Status Values

| Status | Description |
|--------|-------------|
| `unresolved` | Active issue (default) |
| `resolved` | Manually resolved |
| `resolvedInNextRelease` | Auto-resolve on next release |
| `ignored` | Ignored (won't alert) |

---

## Guidelines

1. **Use organization slug**: Most endpoints use org slug, not ID
2. **Pagination**: Use `cursor` parameter for paginated results
3. **Query syntax**: Use Sentry's query language for powerful filtering
4. **Rate limits**: Sentry has rate limits; implement backoff for 429 responses
5. **Self-hosted**: For self-hosted Sentry, set `SENTRY_HOST` to your domain
6. **Scopes matter**: Ensure your token has required scopes for each operation
