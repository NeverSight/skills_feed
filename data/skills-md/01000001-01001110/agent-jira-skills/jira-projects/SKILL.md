---
name: jira-projects
description: Manage Jira projects. Use when listing projects, getting project configuration, retrieving issue types, or managing components and versions.
---

# Jira Projects Skill

## Purpose
Manage Jira projects - list, get details, retrieve issue types, components, and versions.

## When to Use
- Listing available projects
- Getting project configuration
- Retrieving issue types for a project
- Managing project components and versions

## Prerequisites
- Authenticated JiraClient (see jira-auth skill)
- Project browse permissions

## Implementation Pattern

### Step 1: List All Projects

```typescript
interface JiraProject {
  id: string;
  key: string;
  name: string;
  projectTypeKey: string;
  simplified: boolean;
  style: string;
  avatarUrls: Record<string, string>;
  description?: string;
  lead?: {
    accountId: string;
    displayName: string;
  };
}

interface ProjectsResponse {
  values: JiraProject[];
  startAt: number;
  maxResults: number;
  total: number;
  isLast: boolean;
}

async function listProjects(
  client: JiraClient,
  options: {
    status?: 'LIVE' | 'ARCHIVED' | 'DELETED';
    expand?: string[];
    maxResults?: number;
    startAt?: number;
  } = {}
): Promise<JiraProject[]> {
  const params = new URLSearchParams();
  if (options.status) params.set('status', options.status);
  if (options.expand) params.set('expand', options.expand.join(','));
  if (options.maxResults) params.set('maxResults', String(options.maxResults));
  if (options.startAt) params.set('startAt', String(options.startAt));

  const response = await client.request<ProjectsResponse>(
    `/projects?${params.toString()}`
  );
  return response.values;
}
```

### Step 2: Get Project Details

```typescript
async function getProject(
  client: JiraClient,
  projectKeyOrId: string,
  expand?: string[]
): Promise<JiraProject> {
  const params = expand ? `?expand=${expand.join(',')}` : '';
  return client.request<JiraProject>(`/projects/${projectKeyOrId}${params}`);
}
```

### Step 3: Get Project Issue Types

```typescript
interface IssueType {
  id: string;
  name: string;
  description: string;
  iconUrl: string;
  subtask: boolean;
  hierarchyLevel: number;
}

async function getProjectIssueTypes(
  client: JiraClient,
  projectKeyOrId: string
): Promise<IssueType[]> {
  const response = await client.request<{ values: IssueType[] }>(
    `/projects/${projectKeyOrId}/issuetypes`
  );
  return response.values;
}
```

### Step 4: Get Project Components

```typescript
interface Component {
  id: string;
  name: string;
  description?: string;
  lead?: {
    accountId: string;
    displayName: string;
  };
  project: string;
  projectId: number;
}

async function getProjectComponents(
  client: JiraClient,
  projectKeyOrId: string
): Promise<Component[]> {
  const response = await client.request<{ values: Component[] }>(
    `/projects/${projectKeyOrId}/components`
  );
  return response.values;
}
```

### Step 5: Get Project Versions

```typescript
interface Version {
  id: string;
  name: string;
  description?: string;
  archived: boolean;
  released: boolean;
  releaseDate?: string;
  startDate?: string;
  overdue: boolean;
}

async function getProjectVersions(
  client: JiraClient,
  projectKeyOrId: string,
  options: {
    status?: 'UNRELEASED' | 'RELEASED' | 'ARCHIVED';
    expand?: string[];
  } = {}
): Promise<Version[]> {
  const params = new URLSearchParams();
  if (options.status) params.set('status', options.status);
  if (options.expand) params.set('expand', options.expand.join(','));

  const response = await client.request<{ values: Version[] }>(
    `/projects/${projectKeyOrId}/versions?${params.toString()}`
  );
  return response.values;
}
```

## curl Examples

### List Projects
```bash
curl -X GET "https://mycompany.atlassian.net/rest/api/3/projects?expand=description,issueTypes&status=LIVE" \
  -H "Authorization: Basic $(echo -n 'email:token' | base64)" \
  -H "Accept: application/json"
```

### Get Project Details
```bash
curl -X GET "https://mycompany.atlassian.net/rest/api/3/projects/PROJECT?expand=issueTypes,permissions" \
  -H "Authorization: Basic $(echo -n 'email:token' | base64)" \
  -H "Accept: application/json"
```

### Get Issue Types
```bash
curl -X GET "https://mycompany.atlassian.net/rest/api/3/projects/PROJECT/issuetypes" \
  -H "Authorization: Basic $(echo -n 'email:token' | base64)" \
  -H "Accept: application/json"
```

## API Endpoints Summary

| Operation | Method | Path |
|-----------|--------|------|
| List projects | GET | `/projects` |
| Get project | GET | `/projects/{projectIdOrKey}` |
| Get issue types | GET | `/projects/{projectIdOrKey}/issuetypes` |
| Get components | GET | `/projects/{projectIdOrKey}/components` |
| Get versions | GET | `/projects/{projectIdOrKey}/versions` |

## Expand Options
- `description` - Project description
- `lead` - Project lead user details
- `issueTypes` - Available issue types
- `url` - Project URL
- `permissions` - Current user permissions
- `projectKeys` - All project keys

## Common Mistakes
- Using project name instead of key/ID
- Forgetting pagination for large project lists
- Not handling archived projects

## References
- [Projects API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-projects/)

## Version History
- 2025-12-10: Created
