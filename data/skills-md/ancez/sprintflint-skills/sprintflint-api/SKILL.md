---
name: sprintflint-api
description: Manage SprintFlint projects, sprints, issues, and comments via REST API. Use when you need to create tickets, update status, or track sprint progress.
---

# SprintFlint API Skill

Interact with SprintFlint sprint ticketing platform through the REST API. Use this skill to manage projects, sprints, issues/tickets, and comments.

## When to Use

Use this skill when you need to:

- List, create, or update projects
- List, create, update, or manage sprints
- List, create, update, or delete issues/tickets
- Add comments to issues
- Track sprint progress and velocity

## Authentication

All requests require the `X-API-Token` header. Use the `SPRINTFLINT_API_TOKEN` environment variable:

```bash
curl -H "X-API-Token: $SPRINTFLINT_API_TOKEN" https://sprintflint.com/api/v1/projects
```

**Important:** The user must have `SPRINTFLINT_API_TOKEN` set in their environment. If it's not set, ask them to:

1. Go to SprintFlint → Profile → API Token
2. Generate a token
3. Add `export SPRINTFLINT_API_TOKEN="token"` to their shell profile

## Base URL

All endpoints use: `https://sprintflint.com/api/v1`

## API Reference

### Projects

**List all projects:**

```bash
GET /api/v1/projects
```

**Get a project:**

```bash
GET /api/v1/projects/{id}
```

**Create a project:**

```bash
POST /api/v1/projects
Content-Type: application/json

{
  "project": {
    "name": "My Project",
    "prefix": "MP",
    "description": "Optional description"
  }
}
```

**Update a project:**

```bash
PATCH /api/v1/projects/{id}
Content-Type: application/json

{
  "project": {
    "name": "Updated Name"
  }
}
```

**Delete a project:** (admin only)

```bash
DELETE /api/v1/projects/{id}
```

### Sprints

**List sprints in a project:**

```bash
GET /api/v1/projects/{project_id}/sprints
```

**Get a sprint:**

```bash
GET /api/v1/projects/{project_id}/sprints/{id}
```

**Create a sprint:**

```bash
POST /api/v1/projects/{project_id}/sprints
Content-Type: application/json

{
  "sprint": {
    "name": "Sprint 1",
    "start_date": "2026-02-01",
    "end_date": "2026-02-14",
    "description": "Optional description"
  }
}
```

**Update a sprint:**

```bash
PATCH /api/v1/projects/{project_id}/sprints/{id}
Content-Type: application/json

{
  "sprint": {
    "name": "Updated Sprint Name"
  }
}
```

**Activate a sprint:**

```bash
POST /api/v1/projects/{project_id}/sprints/{id}/activate
```

**Complete a sprint:**

```bash
POST /api/v1/projects/{project_id}/sprints/{id}/complete
```

**Delete a sprint:** (admin only)

```bash
DELETE /api/v1/projects/{project_id}/sprints/{id}
```

### Issues (Tickets)

**List issues in a sprint:**

```bash
GET /api/v1/projects/{project_id}/sprints/{sprint_id}/issues
```

**Get an issue:**

```bash
GET /api/v1/projects/{project_id}/sprints/{sprint_id}/issues/{id}
```

**Create an issue:**

```bash
POST /api/v1/projects/{project_id}/sprints/{sprint_id}/issues
Content-Type: application/json

{
  "issue": {
    "title": "Implement feature X",
    "description": "Detailed description",
    "status": "backlog",
    "story_points": 3,
    "assignee_id": 123
  }
}
```

Valid statuses: `backlog`, `todo`, `in_progress`, `done`, `cancelled`

**Update an issue:**

```bash
PATCH /api/v1/projects/{project_id}/sprints/{sprint_id}/issues/{id}
Content-Type: application/json

{
  "issue": {
    "status": "in_progress",
    "story_points": 5
  }
}
```

**Delete an issue:**

```bash
DELETE /api/v1/projects/{project_id}/sprints/{sprint_id}/issues/{id}
```

### Comments

**List comments on an issue:**

```bash
GET /api/v1/projects/{project_id}/sprints/{sprint_id}/issues/{issue_id}/comments
```

**Get a comment:**

```bash
GET /api/v1/comments/{id}
```

**Create a comment:**

```bash
POST /api/v1/projects/{project_id}/sprints/{sprint_id}/issues/{issue_id}/comments
Content-Type: application/json

{
  "comment": {
    "body": "This is my comment"
  }
}
```

**Update a comment:** (author only)

```bash
PATCH /api/v1/comments/{id}
Content-Type: application/json

{
  "comment": {
    "body": "Updated comment text"
  }
}
```

**Delete a comment:** (author only)

```bash
DELETE /api/v1/comments/{id}
```

## Response Schemas

### Project

```json
{
  "id": 1,
  "name": "SprintFlint",
  "prefix": "SF-",
  "description": "Sprint ticketing platform",
  "sprints_count": 5,
  "created_at": "2026-01-01T00:00:00Z",
  "updated_at": "2026-01-15T00:00:00Z"
}
```

### Sprint

```json
{
  "id": 1,
  "name": "Sprint 1",
  "slug": "sprint-1",
  "status": "active",
  "start_date": "2026-01-19",
  "end_date": "2026-01-23",
  "issues_count": 7,
  "total_story_points": 21,
  "completed_story_points": 8,
  "project_id": 1,
  "created_at": "2026-01-19T00:00:00Z",
  "updated_at": "2026-01-20T00:00:00Z"
}
```

### Issue

```json
{
  "id": 1,
  "title": "Implement feature X",
  "description": "Detailed description",
  "status": "in_progress",
  "story_points": 3,
  "position": 1,
  "issue_number": "SF-1",
  "sprint_id": 1,
  "assignee_id": 123,
  "started_at": "2026-01-20T10:00:00Z",
  "completed_at": null,
  "created_at": "2026-01-19T00:00:00Z",
  "updated_at": "2026-01-20T00:00:00Z"
}
```

### Comment

```json
{
  "id": 1,
  "body": "This is my comment",
  "issue_id": 1,
  "author_id": 123,
  "author_name": "John Doe",
  "created_at": "2026-01-20T00:00:00Z",
  "updated_at": "2026-01-20T00:00:00Z"
}
```

## Error Handling

**401 Unauthorized** - Invalid or missing API token

```json
{ "error": "Unauthorized" }
```

**403 Forbidden** - Not authorized for this action

```json
{ "error": "Forbidden" }
```

**404 Not Found** - Resource not found

```json
{ "error": "Not found" }
```

**422 Unprocessable Entity** - Validation errors

```json
{ "errors": ["Title can't be blank", "Name is too short"] }
```

## Examples

### Create a complete workflow

```bash
# 1. Create a project
curl -X POST https://sprintflint.com/api/v1/projects \
  -H "X-API-Token: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"project": {"name": "New Project", "prefix": "NP"}}'

# 2. Create a sprint
curl -X POST https://sprintflint.com/api/v1/projects/1/sprints \
  -H "X-API-Token: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"sprint": {"name": "Sprint 1", "start_date": "2026-02-01", "end_date": "2026-02-14"}}'

# 3. Create issues
curl -X POST https://sprintflint.com/api/v1/projects/1/sprints/1/issues \
  -H "X-API-Token: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"issue": {"title": "Setup project", "story_points": 2}}'

# 4. Activate the sprint
curl -X POST https://sprintflint.com/api/v1/projects/1/sprints/1/activate \
  -H "X-API-Token: $TOKEN"

# 5. Update issue status
curl -X PATCH https://sprintflint.com/api/v1/projects/1/sprints/1/issues/1 \
  -H "X-API-Token: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"issue": {"status": "done"}}'
```
