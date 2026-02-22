---
name: jira-search
description: Search Jira issues using JQL queries. Use when filtering issues by project, status, assignee, date, or building reports.
---

# Jira Search Skill

## Purpose
Search for issues using JQL (Jira Query Language). Supports filtering, pagination, and field selection.

## When to Use
- Searching issues by project, status, assignee, date
- Building issue lists and reports
- Finding specific issues by criteria
- Bulk operations on filtered issues

## Prerequisites
- Authenticated JiraClient (see jira-auth skill)
- Project access permissions

## Implementation Pattern

### Step 1: Define Search Types

```typescript
interface SearchOptions {
  jql: string;
  startAt?: number;
  maxResults?: number;
  fields?: string[];
  expand?: string[];
}

interface SearchResponse {
  startAt: number;
  maxResults: number;
  total: number;
  issues: JiraIssue[];
}
```

### Step 2: Basic Search

```typescript
async function searchIssues(
  client: JiraClient,
  options: SearchOptions
): Promise<SearchResponse> {
  return client.request<SearchResponse>('/search', {
    method: 'POST',
    body: JSON.stringify({
      jql: options.jql,
      startAt: options.startAt ?? 0,
      maxResults: options.maxResults ?? 50,
      fields: options.fields ?? ['key', 'summary', 'status', 'assignee', 'created'],
      expand: options.expand,
    }),
  });
}
```

### Step 3: Search All (Paginated)

```typescript
async function searchAllIssues(
  client: JiraClient,
  jql: string,
  fields: string[] = ['key', 'summary', 'status']
): Promise<JiraIssue[]> {
  const allIssues: JiraIssue[] = [];
  let startAt = 0;
  const maxResults = 100;

  while (true) {
    const response = await searchIssues(client, {
      jql,
      startAt,
      maxResults,
      fields,
    });

    allIssues.push(...response.issues);

    if (startAt + response.issues.length >= response.total) {
      break;
    }

    startAt += maxResults;
  }

  return allIssues;
}
```

### Step 4: Common Search Builders

```typescript
// Search by project
function searchByProject(projectKey: string): string {
  return `project = ${projectKey}`;
}

// Search by status
function searchByStatus(status: string | string[]): string {
  if (Array.isArray(status)) {
    return `status IN (${status.map(s => `'${s}'`).join(', ')})`;
  }
  return `status = '${status}'`;
}

// Search by assignee
function searchByAssignee(accountId: string): string {
  return `assignee = '${accountId}'`;
}

// Search my issues
function searchMyIssues(): string {
  return `assignee = currentUser()`;
}

// Search by date range
function searchByCreatedDate(daysAgo: number): string {
  return `created >= -${daysAgo}d`;
}

// Combine conditions
function combineJql(...conditions: string[]): string {
  return conditions.join(' AND ');
}
```

### Step 5: Advanced Search Examples

```typescript
// Find all open issues in project
async function findOpenIssues(client: JiraClient, projectKey: string) {
  return searchAllIssues(
    client,
    combineJql(
      searchByProject(projectKey),
      `status NOT IN (Done, Closed)`
    )
  );
}

// Find my recent issues
async function findMyRecentIssues(client: JiraClient, daysAgo: number = 7) {
  return searchAllIssues(
    client,
    combineJql(
      searchMyIssues(),
      searchByCreatedDate(daysAgo)
    )
  );
}

// Find issues by label
async function findByLabel(client: JiraClient, projectKey: string, label: string) {
  return searchAllIssues(
    client,
    combineJql(
      searchByProject(projectKey),
      `labels = '${label}'`
    )
  );
}

// Find unassigned issues
async function findUnassigned(client: JiraClient, projectKey: string) {
  return searchAllIssues(
    client,
    combineJql(
      searchByProject(projectKey),
      `assignee IS EMPTY`
    )
  );
}
```

## JQL Quick Reference

### Operators
| Operator | Example | Description |
|----------|---------|-------------|
| `=` | `status = Done` | Equals |
| `!=` | `status != Done` | Not equals |
| `IN` | `status IN (Done, Closed)` | One of |
| `NOT IN` | `status NOT IN (Done)` | Not one of |
| `~` | `summary ~ "bug"` | Contains |
| `IS EMPTY` | `assignee IS EMPTY` | Is null |
| `IS NOT EMPTY` | `assignee IS NOT EMPTY` | Is not null |
| `>=` | `created >= -7d` | Greater/equal |
| `<=` | `created <= 2025-01-01` | Less/equal |

### Date Formats
| Format | Example | Description |
|--------|---------|-------------|
| Relative | `-7d` | 7 days ago |
| Relative | `-2w` | 2 weeks ago |
| Relative | `-1m` | 1 month ago |
| Absolute | `2025-01-15` | Specific date |
| Function | `startOfDay()` | Today midnight |
| Function | `startOfWeek()` | Monday |

### Common JQL Patterns

```jql
# All issues in project
project = SCRUM

# Open issues
project = SCRUM AND status != Done

# My issues
assignee = currentUser()

# High priority open issues
project = SCRUM AND priority = High AND status != Done

# Created this week
project = SCRUM AND created >= startOfWeek()

# Updated recently
project = SCRUM AND updated >= -7d

# Unassigned bugs
project = SCRUM AND issuetype = Bug AND assignee IS EMPTY

# Issues with specific label
project = SCRUM AND labels = "urgent"

# Text search in summary
project = SCRUM AND summary ~ "authentication"
```

## curl Examples

### Basic Search
```bash
curl -X POST "$JIRA_BASE_URL/rest/api/3/search" \
  -H "Authorization: Basic $(echo -n 'email:token' | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "jql": "project = SCRUM AND status != Done",
    "startAt": 0,
    "maxResults": 50,
    "fields": ["key", "summary", "status", "assignee"]
  }'
```

### Search with Pagination
```bash
curl -X POST "$JIRA_BASE_URL/rest/api/3/search" \
  -H "Authorization: Basic $(echo -n 'email:token' | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "jql": "project = SCRUM",
    "startAt": 50,
    "maxResults": 50,
    "fields": ["key", "summary"]
  }'
```

### Search with Changelog Expand
```bash
curl -X POST "$JIRA_BASE_URL/rest/api/3/search" \
  -H "Authorization: Basic $(echo -n 'email:token' | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "jql": "project = SCRUM AND updated >= -7d",
    "maxResults": 50,
    "fields": ["key", "summary", "status"],
    "expand": ["changelog"]
  }'
```

## Response Structure

```json
{
  "startAt": 0,
  "maxResults": 50,
  "total": 150,
  "issues": [
    {
      "id": "10001",
      "key": "SCRUM-1",
      "self": "$JIRA_BASE_URL/rest/api/3/issue/10001",
      "fields": {
        "summary": "Issue summary",
        "status": { "name": "To Do" },
        "assignee": { "displayName": "John Doe" }
      }
    }
  ]
}
```

## Pagination Formula

```
Total pages = ceil(total / maxResults)
Current page = floor(startAt / maxResults) + 1
Has more = (startAt + issues.length) < total
Next startAt = startAt + maxResults
```

## Common Mistakes
- Not quoting status values with spaces
- Using email instead of accountId for assignee
- Forgetting pagination for large result sets
- Not escaping special characters in search text

## References
- [Search API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/)
- [JQL Reference](https://support.atlassian.com/jira-software-cloud/docs/use-advanced-search-with-jira-query-language-jql/)

## Version History
- 2025-12-10: Created
