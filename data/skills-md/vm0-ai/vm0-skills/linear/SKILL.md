---
name: linear
description: Linear issue tracking API via curl. Use this skill to create, update, and query issues, projects, and teams using GraphQL.
vm0_secrets:
  - LINEAR_API_KEY
---

# Linear API

Use the Linear API via direct `curl` calls to manage **issues, projects, and teams** with GraphQL queries and mutations.

> Official docs: `https://linear.app/developers`

---

## When to Use

Use this skill when you need to:

- **Query issues** from Linear workspaces
- **Create new issues** with title, description, and assignments
- **Update issue status** and properties
- **List teams and projects** in an organization
- **Add comments** to issues
- **Search issues** with filters

---

## Prerequisites

1. Log in to [Linear](https://linear.app/) and go to Settings
2. Navigate to **Security & access** → **Personal API keys**
3. Create a new API key with appropriate permissions

```bash
export LINEAR_API_KEY="lin_api_..."
```

### Rate Limits

Linear's API is rate-limited to ensure fair usage. Limits may vary based on your plan.

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"'
> ```

## How to Use

All examples below assume you have `LINEAR_API_KEY` set.

Base URL: `https://api.linear.app/graphql`

Linear uses **GraphQL** for all API operations. Queries retrieve data, mutations modify data.

---

### 1. List Teams

Get all teams in your workspace:

Write to `/tmp/linear_request.json`:

```json
{
  "query": "{ teams { nodes { id name key } } }"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.linear.app/graphql" -H "Content-Type: application/json" -H "Authorization: ${LINEAR_API_KEY}" -d @/tmp/linear_request.json' | jq '.data.teams.nodes'
```

Save a team ID for subsequent queries.

---

### 2. List Issues for a Team

Get issues from a specific team. Replace `<your-team-id>` with the actual team ID:

Write to `/tmp/linear_request.json`:

```json
{
  "query": "{ team(id: \"<your-team-id>\") { issues { nodes { id identifier title state { name } assignee { name } } } } }"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.linear.app/graphql" -H "Content-Type: application/json" -H "Authorization: ${LINEAR_API_KEY}" -d @/tmp/linear_request.json' | jq '.data.team.issues.nodes'
```

---

### 3. Get Issue by Identifier

Fetch a specific issue by its identifier (e.g., `ENG-123`):

Write to `/tmp/linear_request.json`:

```json
{
  "query": "{ issue(id: \"ENG-123\") { id identifier title description state { name } priority assignee { name } createdAt } }"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.linear.app/graphql" -H "Content-Type: application/json" -H "Authorization: ${LINEAR_API_KEY}" -d @/tmp/linear_request.json' | jq '.data.issue'
```

---

### 4. Search Issues

Search issues with filters:

Write to `/tmp/linear_request.json`:

```json
{
  "query": "{ issues(filter: { state: { name: { eq: \"In Progress\" } } }, first: 10) { nodes { id identifier title assignee { name } } } }"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.linear.app/graphql" -H "Content-Type: application/json" -H "Authorization: ${LINEAR_API_KEY}" -d @/tmp/linear_request.json' | jq '.data.issues.nodes'
```

---

### 5. Create Issue

Create a new issue in a team. Replace `<your-team-id>` with the actual team ID:

Write to `/tmp/linear_request.json`:

```json
{
  "query": "mutation { issueCreate(input: { title: \"Bug: Login button not working\", description: \"Users report the login button is unresponsive on mobile.\", teamId: \"<your-team-id>\" }) { success issue { id identifier title url } } }"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.linear.app/graphql" -H "Content-Type: application/json" -H "Authorization: ${LINEAR_API_KEY}" -d @/tmp/linear_request.json' | jq '.data.issueCreate'
```

---

### 6. Create Issue with Priority and Labels

Create an issue with additional properties. Replace `<your-team-id>` and `<your-label-id>` with actual IDs:

Write to `/tmp/linear_request.json`:

```json
{
  "query": "mutation { issueCreate(input: { title: \"High priority task\", teamId: \"<your-team-id>\", priority: 1, labelIds: [\"<your-label-id>\"] }) { success issue { id identifier title priority } } }"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.linear.app/graphql" -H "Content-Type: application/json" -H "Authorization: ${LINEAR_API_KEY}" -d @/tmp/linear_request.json' | jq '.data.issueCreate'
```

**Priority values:** 0 (No priority), 1 (Urgent), 2 (High), 3 (Medium), 4 (Low)

---

### 7. Update Issue

Update an existing issue. Replace `<your-issue-id>` with the actual issue ID:

Write to `/tmp/linear_request.json`:

```json
{
  "query": "mutation { issueUpdate(id: \"<your-issue-id>\", input: { title: \"Updated title\", priority: 2 }) { success issue { id identifier title priority } } }"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.linear.app/graphql" -H "Content-Type: application/json" -H "Authorization: ${LINEAR_API_KEY}" -d @/tmp/linear_request.json' | jq '.data.issueUpdate'
```

---

### 8. Change Issue State

Move an issue to a different state (e.g., "Done"). Replace `<your-issue-id>` and `<your-state-id>` with actual IDs:

Write to `/tmp/linear_request.json`:

```json
{
  "query": "mutation { issueUpdate(id: \"<your-issue-id>\", input: { stateId: \"<your-state-id>\" }) { success issue { id identifier state { name } } } }"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.linear.app/graphql" -H "Content-Type: application/json" -H "Authorization: ${LINEAR_API_KEY}" -d @/tmp/linear_request.json' | jq '.data.issueUpdate'
```

---

### 9. List Workflow States

Get available states for a team. Replace `<your-team-id>` with the actual team ID:

Write to `/tmp/linear_request.json`:

```json
{
  "query": "{ team(id: \"<your-team-id>\") { states { nodes { id name type } } } }"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.linear.app/graphql" -H "Content-Type: application/json" -H "Authorization: ${LINEAR_API_KEY}" -d @/tmp/linear_request.json' | jq '.data.team.states.nodes'
```

---

### 10. Add Comment to Issue

Add a comment to an existing issue. Replace `<your-issue-id>` with the actual issue ID:

Write to `/tmp/linear_request.json`:

```json
{
  "query": "mutation { commentCreate(input: { issueId: \"<your-issue-id>\", body: \"This is a comment from the API.\" }) { success comment { id body createdAt } } }"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.linear.app/graphql" -H "Content-Type: application/json" -H "Authorization: ${LINEAR_API_KEY}" -d @/tmp/linear_request.json' | jq '.data.commentCreate'
```

---

### 11. List Projects

Get all projects in the workspace:

Write to `/tmp/linear_request.json`:

```json
{
  "query": "{ projects { nodes { id name state progress targetDate } } }"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.linear.app/graphql" -H "Content-Type: application/json" -H "Authorization: ${LINEAR_API_KEY}" -d @/tmp/linear_request.json' | jq '.data.projects.nodes'
```

---

### 12. Get Current User

Get information about the authenticated user:

Write to `/tmp/linear_request.json`:

```json
{
  "query": "{ viewer { id name email admin } }"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.linear.app/graphql" -H "Content-Type: application/json" -H "Authorization: ${LINEAR_API_KEY}" -d @/tmp/linear_request.json' | jq '.data.viewer'
```

---

### 13. List Labels

Get available labels for a team. Replace `<your-team-id>` with the actual team ID:

Write to `/tmp/linear_request.json`:

```json
{
  "query": "{ team(id: \"<your-team-id>\") { labels { nodes { id name color } } } }"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.linear.app/graphql" -H "Content-Type: application/json" -H "Authorization: ${LINEAR_API_KEY}" -d @/tmp/linear_request.json' | jq '.data.team.labels.nodes'
```

---

## Finding IDs

To find IDs for teams, issues, projects, etc.:

1. Open Linear app
2. Press `Cmd/Ctrl + K` to open command menu
3. Type "Copy model UUID"
4. Select the entity to copy its ID

Or use the queries above to list entities and extract their IDs.

---

## Guidelines

1. **Use GraphQL variables**: For production, use variables instead of string interpolation for better security
2. **Handle pagination**: Use `first`, `after`, `last`, `before` for paginated results
3. **Check for errors**: GraphQL returns 200 even with errors; always check the `errors` array
4. **Rate limiting**: Implement backoff if you receive rate limit errors
5. **Batch operations**: Combine multiple queries in one request when possible
6. **Issue identifiers**: You can use either UUID or readable identifier (e.g., `ENG-123`) for most queries
