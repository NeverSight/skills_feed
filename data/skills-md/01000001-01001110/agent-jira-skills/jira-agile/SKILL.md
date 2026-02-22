---
name: jira-agile
description: Manage Jira Agile boards and sprints. Use when listing boards, creating sprints, or moving issues to/from sprints.
---

# Jira Agile Skill

## Purpose
Manage Jira Agile boards and sprints - list boards, manage sprints, move issues to sprints.

## When to Use
- Listing Scrum/Kanban boards
- Managing sprints (create, start, end)
- Moving issues to/from sprints
- Getting sprint issues

## Prerequisites
- Authenticated JiraClient (see jira-auth skill)
- Board/sprint management permissions
- Note: Uses `/rest/agile/1.0/` NOT `/rest/api/3/`

## Implementation Pattern

### Step 1: Create Agile Client Extension

```typescript
class JiraAgileClient extends JiraClient {
  async agileRequest<T>(path: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}/rest/agile/1.0${path}`;
    const response = await fetch(url, {
      ...options,
      headers: { ...this.headers, ...options.headers },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(`Jira Agile API error: ${response.status} - ${JSON.stringify(error)}`);
    }

    return response.json();
  }
}
```

### Step 2: List Boards

```typescript
interface Board {
  id: number;
  self: string;
  name: string;
  type: 'scrum' | 'kanban';
  projectKey?: string;
}

interface BoardsResponse {
  values: Board[];
  startAt: number;
  maxResults: number;
  total: number;
  isLast: boolean;
}

async function listBoards(
  client: JiraAgileClient,
  options: {
    type?: 'scrum' | 'kanban';
    projectKeyOrId?: string;
    maxResults?: number;
  } = {}
): Promise<Board[]> {
  const params = new URLSearchParams();
  if (options.type) params.set('type', options.type);
  if (options.projectKeyOrId) params.set('projectKeyOrId', options.projectKeyOrId);
  if (options.maxResults) params.set('maxResults', String(options.maxResults));

  const response = await client.agileRequest<BoardsResponse>(
    `/board?${params.toString()}`
  );
  return response.values;
}
```

### Step 3: Get Board Sprints

```typescript
interface Sprint {
  id: number;
  self: string;
  state: 'future' | 'active' | 'closed';
  name: string;
  startDate?: string;
  endDate?: string;
  goal?: string;
}

async function getBoardSprints(
  client: JiraAgileClient,
  boardId: number,
  state?: 'future' | 'active' | 'closed' | string
): Promise<Sprint[]> {
  const params = state ? `?state=${state}` : '';
  const response = await client.agileRequest<{ values: Sprint[] }>(
    `/board/${boardId}/sprint${params}`
  );
  return response.values;
}
```

### Step 4: Get Sprint Issues

```typescript
interface SprintIssue {
  id: string;
  key: string;
  self: string;
  fields: {
    summary: string;
    status: { name: string };
    assignee?: { displayName: string };
  };
}

async function getSprintIssues(
  client: JiraAgileClient,
  sprintId: number,
  options: {
    maxResults?: number;
    startAt?: number;
  } = {}
): Promise<SprintIssue[]> {
  const params = new URLSearchParams();
  if (options.maxResults) params.set('maxResults', String(options.maxResults));
  if (options.startAt) params.set('startAt', String(options.startAt));

  const response = await client.agileRequest<{ issues: SprintIssue[] }>(
    `/sprint/${sprintId}/issue?${params.toString()}`
  );
  return response.issues;
}
```

### Step 5: Move Issues to Sprint

```typescript
async function moveIssuesToSprint(
  client: JiraAgileClient,
  sprintId: number,
  issueKeys: string[],
  options: {
    rankBeforeIssue?: string;
    rankAfterIssue?: string;
  } = {}
): Promise<void> {
  await client.agileRequest(`/sprint/${sprintId}/issue`, {
    method: 'POST',
    body: JSON.stringify({
      issues: issueKeys,
      ...options,
    }),
  });
}
```

### Step 6: Create Sprint

```typescript
interface CreateSprintInput {
  name: string;
  boardId: number;
  startDate?: string;
  endDate?: string;
  goal?: string;
}

async function createSprint(
  client: JiraAgileClient,
  input: CreateSprintInput
): Promise<Sprint> {
  return client.agileRequest<Sprint>('/sprint', {
    method: 'POST',
    body: JSON.stringify({
      name: input.name,
      originBoardId: input.boardId,
      startDate: input.startDate,
      endDate: input.endDate,
      goal: input.goal,
    }),
  });
}
```

### Step 7: Start/End Sprint

```typescript
async function startSprint(
  client: JiraAgileClient,
  sprintId: number,
  startDate: string,
  endDate: string
): Promise<void> {
  await client.agileRequest(`/sprint/${sprintId}`, {
    method: 'POST',
    body: JSON.stringify({
      state: 'active',
      startDate,
      endDate,
    }),
  });
}

async function endSprint(
  client: JiraAgileClient,
  sprintId: number
): Promise<void> {
  await client.agileRequest(`/sprint/${sprintId}`, {
    method: 'POST',
    body: JSON.stringify({
      state: 'closed',
    }),
  });
}
```

## curl Examples

### List Boards
```bash
curl -X GET "https://mycompany.atlassian.net/rest/agile/1.0/board?type=scrum" \
  -H "Authorization: Basic $(echo -n 'email:token' | base64)" \
  -H "Accept: application/json"
```

### Get Board Sprints
```bash
curl -X GET "https://mycompany.atlassian.net/rest/agile/1.0/board/1/sprint?state=active,future" \
  -H "Authorization: Basic $(echo -n 'email:token' | base64)" \
  -H "Accept: application/json"
```

### Move Issues to Sprint
```bash
curl -X POST "https://mycompany.atlassian.net/rest/agile/1.0/sprint/1/issue" \
  -H "Authorization: Basic $(echo -n 'email:token' | base64)" \
  -H "Content-Type: application/json" \
  -d '{"issues": ["PROJ-123", "PROJ-124"]}'
```

### Create Sprint
```bash
curl -X POST "https://mycompany.atlassian.net/rest/agile/1.0/sprint" \
  -H "Authorization: Basic $(echo -n 'email:token' | base64)" \
  -H "Content-Type: application/json" \
  -d '{"name": "Sprint 1", "originBoardId": 1, "goal": "Complete MVP"}'
```

## API Endpoints Summary

| Operation | Method | Path |
|-----------|--------|------|
| List boards | GET | `/board` |
| Get board | GET | `/board/{boardId}` |
| Get board sprints | GET | `/board/{boardId}/sprint` |
| Get sprint | GET | `/sprint/{sprintId}` |
| Create sprint | POST | `/sprint` |
| Update sprint | PUT | `/sprint/{sprintId}` |
| Delete sprint | DELETE | `/sprint/{sprintId}` |
| Get sprint issues | GET | `/sprint/{sprintId}/issue` |
| Move issues to sprint | POST | `/sprint/{sprintId}/issue` |

## Common Mistakes
- Using `/rest/api/3/` instead of `/rest/agile/1.0/`
- Trying to add issues to closed sprints
- Kanban boards don't have sprints
- Sprint IDs are board-specific

## References
- [Jira Agile REST API](https://developer.atlassian.com/cloud/jira/software/rest/intro/)

## Version History
- 2025-12-10: Created
