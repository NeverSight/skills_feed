---
name: jira-issues
description: Create, read, update, and delete Jira issues. Use when managing Stories, Tasks, Bugs, or Epics - includes field updates and metadata.
---

# Jira Issues Skill

## Purpose
Create, read, update, and delete issues in Jira Cloud. Manage issue fields, transitions, and metadata.

## When to Use
- Creating new issues (Story, Task, Bug, Epic)
- Updating issue fields (summary, description, assignee, etc.)
- Reading issue details
- Deleting issues

## Prerequisites
- Authenticated JiraClient (see jira-auth skill)
- Project access permissions
- Issue type IDs for the target project

## Implementation Pattern

### Step 1: Define Issue Types

```typescript
interface JiraIssue {
  id: string;
  key: string;
  self: string;
  fields: {
    summary: string;
    description?: {
      type: 'doc';
      version: 1;
      content: Array<{
        type: string;
        content?: Array<{
          type: string;
          text: string;
        }>;
      }>;
    };
    status: { name: string; id: string };
    assignee?: { accountId: string; displayName: string };
    reporter?: { accountId: string; displayName: string };
    priority?: { name: string; id: string };
    issuetype: { name: string; id: string };
    project: { key: string; id: string };
    created: string;
    updated: string;
    labels?: string[];
    components?: Array<{ id: string; name: string }>;
  };
}

interface CreateIssueInput {
  projectKey: string;
  summary: string;
  issueType: 'Story' | 'Task' | 'Bug' | 'Epic' | string;
  description?: string;
  assigneeAccountId?: string;
  labels?: string[];
  priority?: string;
}
```

### Step 2: Create Issue

```typescript
async function createIssue(
  client: JiraClient,
  input: CreateIssueInput
): Promise<{ id: string; key: string; self: string }> {
  const body: any = {
    fields: {
      project: { key: input.projectKey },
      summary: input.summary,
      issuetype: { name: input.issueType },
    },
  };

  // Add description in Atlassian Document Format (ADF)
  if (input.description) {
    body.fields.description = {
      type: 'doc',
      version: 1,
      content: [
        {
          type: 'paragraph',
          content: [
            {
              type: 'text',
              text: input.description,
            },
          ],
        },
      ],
    };
  }

  if (input.assigneeAccountId) {
    body.fields.assignee = { id: input.assigneeAccountId };
  }

  if (input.labels) {
    body.fields.labels = input.labels;
  }

  if (input.priority) {
    body.fields.priority = { name: input.priority };
  }

  return client.request<{ id: string; key: string; self: string }>('/issue', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}
```

### Step 3: Get Issue

```typescript
async function getIssue(
  client: JiraClient,
  issueKeyOrId: string,
  options: {
    fields?: string[];
    expand?: string[];
  } = {}
): Promise<JiraIssue> {
  const params = new URLSearchParams();
  if (options.fields) params.set('fields', options.fields.join(','));
  if (options.expand) params.set('expand', options.expand.join(','));

  const query = params.toString() ? `?${params.toString()}` : '';
  return client.request<JiraIssue>(`/issue/${issueKeyOrId}${query}`);
}
```

### Step 4: Update Issue

```typescript
interface UpdateIssueInput {
  summary?: string;
  description?: string;
  assigneeAccountId?: string | null;
  labels?: string[];
  priority?: string;
}

async function updateIssue(
  client: JiraClient,
  issueKeyOrId: string,
  input: UpdateIssueInput
): Promise<void> {
  const body: any = { fields: {} };

  if (input.summary) {
    body.fields.summary = input.summary;
  }

  if (input.description !== undefined) {
    body.fields.description = input.description
      ? {
          type: 'doc',
          version: 1,
          content: [
            {
              type: 'paragraph',
              content: [{ type: 'text', text: input.description }],
            },
          ],
        }
      : null;
  }

  if (input.assigneeAccountId !== undefined) {
    body.fields.assignee = input.assigneeAccountId
      ? { id: input.assigneeAccountId }
      : null;
  }

  if (input.labels) {
    body.fields.labels = input.labels;
  }

  if (input.priority) {
    body.fields.priority = { name: input.priority };
  }

  await client.request(`/issue/${issueKeyOrId}`, {
    method: 'PUT',
    body: JSON.stringify(body),
  });
}
```

### Step 5: Delete Issue

```typescript
async function deleteIssue(
  client: JiraClient,
  issueKeyOrId: string,
  deleteSubtasks: boolean = false
): Promise<void> {
  const query = deleteSubtasks ? '?deleteSubtasks=true' : '';
  await client.request(`/issue/${issueKeyOrId}${query}`, {
    method: 'DELETE',
  });
}
```

### Step 6: Bulk Create Issues

```typescript
async function bulkCreateIssues(
  client: JiraClient,
  issues: CreateIssueInput[]
): Promise<Array<{ id: string; key: string; self: string }>> {
  const results: Array<{ id: string; key: string; self: string }> = [];

  // Jira doesn't have a native bulk create, so we batch with Promise.all
  const batches = [];
  const batchSize = 10;

  for (let i = 0; i < issues.length; i += batchSize) {
    batches.push(issues.slice(i, i + batchSize));
  }

  for (const batch of batches) {
    const batchResults = await Promise.all(
      batch.map((issue) => createIssue(client, issue))
    );
    results.push(...batchResults);
  }

  return results;
}
```

## curl Examples

### Create Issue
```bash
curl -X POST "$JIRA_BASE_URL/rest/api/3/issue" \
  -H "Authorization: Basic $(echo -n 'email:token' | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "project": { "key": "SCRUM" },
      "summary": "New feature implementation",
      "issuetype": { "name": "Story" },
      "description": {
        "type": "doc",
        "version": 1,
        "content": [
          {
            "type": "paragraph",
            "content": [{ "type": "text", "text": "Description here" }]
          }
        ]
      }
    }
  }'
```

### Get Issue
```bash
curl -X GET "$JIRA_BASE_URL/rest/api/3/issue/SCRUM-123" \
  -H "Authorization: Basic $(echo -n 'email:token' | base64)" \
  -H "Accept: application/json"
```

### Update Issue
```bash
curl -X PUT "$JIRA_BASE_URL/rest/api/3/issue/SCRUM-123" \
  -H "Authorization: Basic $(echo -n 'email:token' | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "summary": "Updated summary"
    }
  }'
```

### Delete Issue
```bash
curl -X DELETE "$JIRA_BASE_URL/rest/api/3/issue/SCRUM-123" \
  -H "Authorization: Basic $(echo -n 'email:token' | base64)"
```

## API Endpoints Summary

| Operation | Method | Path |
|-----------|--------|------|
| Create issue | POST | `/issue` |
| Get issue | GET | `/issue/{issueIdOrKey}` |
| Update issue | PUT | `/issue/{issueIdOrKey}` |
| Delete issue | DELETE | `/issue/{issueIdOrKey}` |

## Required Fields by Issue Type

### Story
- `project.key` (required)
- `summary` (required)
- `issuetype.name` = "Story" (required)

### Task
- `project.key` (required)
- `summary` (required)
- `issuetype.name` = "Task" (required)

### Bug
- `project.key` (required)
- `summary` (required)
- `issuetype.name` = "Bug" (required)
- `description` (recommended)

## Description Format (ADF)

Jira uses Atlassian Document Format for rich text:

```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "paragraph",
      "content": [
        { "type": "text", "text": "Normal text" }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Bold text",
          "marks": [{ "type": "strong" }]
        }
      ]
    }
  ]
}
```

## Common Mistakes
- Using plain text for description instead of ADF format
- Not using account ID for assignee (email doesn't work)
- Forgetting project key in create request
- Using issue type name that doesn't exist in project

## References
- [Issues API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/)
- [Atlassian Document Format](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/)

## Version History
- 2025-12-10: Created
