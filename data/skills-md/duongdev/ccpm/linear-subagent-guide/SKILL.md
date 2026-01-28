---
name: linear-subagent-guide
description: Guides optimal Linear operations usage with caching, performance patterns, and error handling. Auto-activates when implementing CCPM commands that interact with Linear. Prevents usage of non-existent Linear MCP tools.
allowed-tools: [Task]
---

# Linear Subagent Guide

## ⛔ EXACT LINEAR MCP PARAMETERS (VERIFIED)

**These are the EXACT parameter names from `get_server_tools`. Copy exactly.**

### Most Common Operations

```javascript
// GET ISSUE - uses "id"
mcp__agent-mcp-gateway__execute_tool({
  server: "linear",
  tool: "get_issue",
  args: { id: "WORK-26" }  // ✅ CORRECT - "id" not "issueId"
})

// UPDATE ISSUE - uses "id"
mcp__agent-mcp-gateway__execute_tool({
  server: "linear",
  tool: "update_issue",
  args: {
    id: "WORK-26",        // ✅ CORRECT - "id" not "issueId"
    description: "...",
    state: "In Progress"
  }
})

// CREATE COMMENT - uses "issueId"
mcp__agent-mcp-gateway__execute_tool({
  server: "linear",
  tool: "create_comment",
  args: {
    issueId: "WORK-26",   // ✅ CORRECT - "issueId" for comments
    body: "Comment text"
  }
})

// LIST COMMENTS - uses "issueId"
mcp__agent-mcp-gateway__execute_tool({
  server: "linear",
  tool: "list_comments",
  args: { issueId: "WORK-26" }  // ✅ CORRECT
})
```

### Parameter Reference Table

| Tool | Required Parameter | Example Args |
|------|-------------------|--------------|
| `get_issue` | `id` | `{ id: "WORK-26" }` |
| `update_issue` | `id` | `{ id: "WORK-26", ... }` |
| `create_comment` | `issueId`, `body` | `{ issueId: "WORK-26", body: "..." }` |
| `list_comments` | `issueId` | `{ issueId: "WORK-26" }` |
| `create_issue` | `title`, `team` | `{ title: "...", team: "..." }` |
| `get_project` | `query` | `{ query: "ProjectName" }` |
| `get_team` | `query` | `{ query: "TeamName" }` |
| `get_user` | `query` | `{ query: "me" }` |

---

## Overview

The **Linear subagent** (`ccpm:linear-operations`) is a dedicated MCP handler that optimizes all Linear API operations in CCPM. Rather than making direct Linear MCP calls, commands should delegate to this subagent, which provides:

- **50-60% token reduction** (15k-25k → 8k-12k per workflow)
- **Session-level caching** with 85-95% hit rates
- **Performance**: <50ms for cached operations (vs 400-600ms direct)
- **Structured error handling** with actionable suggestions
- **Centralized logic** for Linear operations consistency

## When to Use the Linear Subagent

**Use the subagent for:**
- Reading issues, projects, teams, statuses
- Creating or updating issues, projects
- Managing labels and comments
- Fetching documents and cycles
- Searching Linear documentation

**Never use the subagent for:**
- Local file operations
- Git commands
- External API calls (except Linear)

---

## ⚠️ CRITICAL: Parameter Name Gotcha

**Different Linear MCP tools use different parameter names for issue IDs:**

| Tool | Parameter | WRONG | CORRECT |
|------|-----------|-------|---------|
| `get_issue` | `id` | `{ issueId: "X" }` ❌ | `{ id: "X" }` ✅ |
| `update_issue` | `id` | `{ issueId: "X" }` ❌ | `{ id: "X" }` ✅ |
| `create_comment` | `issueId` | `{ id: "X" }` ❌ | `{ issueId: "X" }` ✅ |
| `list_comments` | `issueId` | `{ id: "X" }` ❌ | `{ issueId: "X" }` ✅ |

**First-call failures** are often caused by using `issueId` instead of `id` for `get_issue`/`update_issue`.

---

## Available Linear MCP Tools (Complete Reference)

Linear MCP provides **23 tools** for interacting with Linear. This is the complete, validated list.

---

### 1. Comments (2 tools)

#### `list_comments`
List comments for a specific Linear issue.

**Parameters:**
- `issueId` (string, required) - The issue ID

**Example:**
```javascript
mcp__linear__list_comments({ issueId: "PSN-41" })
```

#### `create_comment`
Create a comment on a specific Linear issue.

**Parameters:**
- `issueId` (string, required) - The issue ID
- `body` (string, required) - The content of the comment as Markdown
- `parentId` (string, optional) - A parent comment ID to reply to

**Linear's Native Collapsible Syntax:**
Use `+++` to create collapsible sections (starts collapsed, native Linear feature):
```
+++ Section Title
Content here (multi-line markdown supported)
+++
```

**Example (simple):**
```javascript
mcp__linear__create_comment({
  issueId: "PSN-41",
  body: "## Progress Update\n\nCompleted first phase."
})
```

**Example (with collapsible section):**
```javascript
mcp__linear__create_comment({
  issueId: "PSN-41",
  body: `🔄 **Progress Update**

Completed first phase, all tests passing

+++ 📋 Detailed Context
**Changed Files:**
- src/auth.ts
- src/tests/auth.test.ts

**Next Steps:**
- Implement phase 2
- Update documentation
+++`
})
```

---

### 2. Cycles (1 tool)

#### `list_cycles`
Retrieve cycles for a specific Linear team.

**Parameters:**
- `teamId` (string, required) - The team ID
- `type` (string, optional) - "current", "previous", or "next"

**Example:**
```javascript
mcp__linear__list_cycles({ teamId: "team-123", type: "current" })
```

---

### 3. Documents (2 tools)

#### `get_document`
Retrieve a Linear document by ID or slug.

**Parameters:**
- `id` (string, required) - The document ID or slug

**Example:**
```javascript
mcp__linear__get_document({ id: "doc-abc-123" })
```

#### `list_documents`
List documents in the user's Linear workspace.

**Parameters:**
- `limit` (number, optional, max 250, default 50)
- `before` (string, optional) - An ID to end at
- `after` (string, optional) - An ID to start from
- `orderBy` (string, optional) - "createdAt" or "updatedAt" (default: "updatedAt")
- `query` (string, optional) - Search query
- `projectId` (string, optional) - Filter by project ID
- `initiativeId` (string, optional) - Filter by initiative ID
- `creatorId` (string, optional) - Filter by creator ID
- `createdAt` (string, optional) - ISO-8601 date-time or duration (e.g., "-P1D")
- `updatedAt` (string, optional) - ISO-8601 date-time or duration
- `includeArchived` (boolean, optional, default false)

**Example:**
```javascript
mcp__linear__list_documents({ projectId: "proj-123", limit: 20 })
```

---

### 4. Issues (4 tools)

#### `get_issue`
Retrieve detailed information about an issue by ID.

**Parameters:**
- `id` (string, required) - The issue ID (e.g., "PSN-41")

**Example:**
```javascript
mcp__linear__get_issue({ id: "PSN-41" })
```

#### `list_issues`
List issues in the user's Linear workspace. Use "me" for assignee to get your issues.

**Parameters:**
- `limit` (number, optional, max 250, default 50)
- `before` (string, optional)
- `after` (string, optional)
- `orderBy` (string, optional) - "createdAt" or "updatedAt"
- `query` (string, optional) - Search title or description
- `team` (string, optional) - Team name or ID
- `state` (string, optional) - State name or ID
- `cycle` (string, optional) - Cycle name or ID
- `label` (string, optional) - Label name or ID
- `assignee` (string, optional) - User ID, name, email, or "me"
- `delegate` (string, optional) - Agent name or ID
- `project` (string, optional) - Project name or ID
- `parentId` (string, optional) - Parent issue ID
- `createdAt` (string, optional) - ISO-8601 date-time or duration
- `updatedAt` (string, optional) - ISO-8601 date-time or duration
- `includeArchived` (boolean, optional, default true)

**Example:**
```javascript
mcp__linear__list_issues({ assignee: "me", state: "In Progress" })
```

#### `create_issue`
Create a new Linear issue.

**Parameters:**
- `title` (string, required)
- `team` (string, required) - Team name or ID
- `description` (string, optional) - Markdown description
- `cycle` (string, optional) - Cycle name, number, or ID
- `priority` (number, optional) - 0=None, 1=Urgent, 2=High, 3=Normal, 4=Low
- `project` (string, optional) - Project name or ID
- `state` (string, optional) - State type, name, or ID
- `assignee` (string, optional) - User ID, name, email, or "me"
- `delegate` (string, optional) - Agent name, displayName, or ID
- `labels` (array of strings, optional) - Label names or IDs
- `dueDate` (string, optional) - ISO format date
- `parentId` (string, optional) - Parent issue ID for sub-issues
- `links` (array of objects, optional) - Each object needs `url` and `title`

**Example:**
```javascript
mcp__linear__create_issue({
  title: "Fix authentication bug",
  team: "Engineering",
  description: "## Problem\n\nUsers cannot login",
  state: "Todo",
  labels: ["bug", "critical"],
  assignee: "me"
})
```

#### `update_issue`
Update an existing Linear issue.

**Parameters:**
- `id` (string, required) - The issue ID
- `title` (string, optional)
- `description` (string, optional) - Markdown
- `priority` (number, optional) - 0-4
- `project` (string, optional) - Project name or ID
- `state` (string, optional) - State type, name, or ID
- `cycle` (string, optional) - Cycle name, number, or ID
- `assignee` (string, optional) - User ID, name, email, or "me"
- `delegate` (string, optional) - Agent name, displayName, or ID
- `labels` (array of strings, optional) - Label names or IDs (replaces existing)
- `parentId` (string, optional)
- `dueDate` (string, optional) - ISO format
- `estimate` (number, optional) - Numerical estimate value
- `links` (array of objects, optional)

**Example:**
```javascript
mcp__linear__update_issue({
  id: "PSN-41",
  state: "In Progress",
  labels: ["planning", "implementation"]
})
```

---

### 5. Issue Statuses (2 tools)

#### `list_issue_statuses`
List available issue statuses in a Linear team.

**Parameters:**
- `team` (string, required) - Team name or ID

**Example:**
```javascript
mcp__linear__list_issue_statuses({ team: "Engineering" })
```

#### `get_issue_status`
Retrieve detailed information about an issue status by name or ID.

**Parameters:**
- `id` (string, required) - Status ID
- `name` (string, required) - Status name
- `team` (string, required) - Team name or ID

**Example:**
```javascript
mcp__linear__get_issue_status({ name: "In Progress", team: "Engineering" })
```

---

### 6. Labels (3 tools)

#### `list_issue_labels`
List available issue labels in a workspace or team.

**Parameters:**
- `limit` (number, optional, max 250, default 50)
- `before` (string, optional)
- `after` (string, optional)
- `orderBy` (string, optional) - "createdAt" or "updatedAt"
- `name` (string, optional) - Filter by label name
- `team` (string, optional) - Team name or ID

**Example:**
```javascript
mcp__linear__list_issue_labels({ team: "Engineering" })
```

#### `create_issue_label`
Create a new Linear issue label.

**Parameters:**
- `name` (string, required)
- `description` (string, optional)
- `color` (string, optional) - Hex color code
- `teamId` (string, optional) - Team UUID (workspace label if omitted)
- `parentId` (string, optional) - Parent label UUID for groups
- `isGroup` (boolean, optional, default false) - Whether this is a label group

**Example:**
```javascript
mcp__linear__create_issue_label({
  name: "feature-request",
  color: "#bb87fc",
  teamId: "team-123"
})
```

#### `list_project_labels`
List available project labels in the Linear workspace.

**Parameters:**
- `limit` (number, optional, max 250, default 50)
- `before` (string, optional)
- `after` (string, optional)
- `orderBy` (string, optional)
- `name` (string, optional)

**Example:**
```javascript
mcp__linear__list_project_labels({ limit: 100 })
```

---

### 7. Projects (4 tools)

#### `list_projects`
List projects in the user's Linear workspace.

**Parameters:**
- `limit` (number, optional, max 250, default 50)
- `before` (string, optional)
- `after` (string, optional)
- `orderBy` (string, optional)
- `query` (string, optional) - Search project name
- `state` (string, optional) - State name or ID
- `initiative` (string, optional) - Initiative name or ID
- `team` (string, optional) - Team name or ID
- `member` (string, optional) - User ID, name, email, or "me"
- `createdAt` (string, optional)
- `updatedAt` (string, optional)
- `includeArchived` (boolean, optional, default false)

**Example:**
```javascript
mcp__linear__list_projects({ team: "Engineering", state: "started" })
```

#### `get_project`
Retrieve details of a specific project.

**Parameters:**
- `query` (string, required) - Project ID or name

**Example:**
```javascript
mcp__linear__get_project({ query: "CCPM" })
```

#### `create_project`
Create a new project in Linear.

**Parameters:**
- `name` (string, required)
- `team` (string, required) - Team name or ID
- `summary` (string, optional) - Max 255 chars
- `description` (string, optional) - Markdown
- `state` (string, optional)
- `startDate` (string, optional) - ISO format
- `targetDate` (string, optional) - ISO format
- `priority` (integer, optional) - 0-4
- `labels` (array of strings, optional)
- `lead` (string, optional) - User ID, name, email, or "me"

**Example:**
```javascript
mcp__linear__create_project({
  name: "Q1 Authentication",
  team: "Engineering",
  description: "## Goals\n\n- OAuth integration\n- SSO support",
  lead: "me"
})
```

#### `update_project`
Update an existing Linear project.

**Parameters:**
- `id` (string, required)
- `name` (string, optional)
- `summary` (string, optional)
- `description` (string, optional)
- `state` (string, optional)
- `startDate` (string, optional)
- `targetDate` (string, optional)
- `priority` (integer, optional) - 0-4
- `labels` (array of strings, optional)
- `lead` (string, optional)

**Example:**
```javascript
mcp__linear__update_project({
  id: "proj-123",
  state: "completed"
})
```

---

### 8. Teams (2 tools)

#### `list_teams`
List teams in the user's Linear workspace.

**Parameters:**
- `limit` (number, optional, max 250, default 50)
- `before` (string, optional)
- `after` (string, optional)
- `orderBy` (string, optional)
- `query` (string, optional) - Search query
- `includeArchived` (boolean, optional, default false)
- `createdAt` (string, optional)
- `updatedAt` (string, optional)

**Example:**
```javascript
mcp__linear__list_teams({ includeArchived: false })
```

#### `get_team`
Retrieve details of a specific Linear team.

**Parameters:**
- `query` (string, required) - Team UUID, key, or name

**Example:**
```javascript
mcp__linear__get_team({ query: "Engineering" })
```

---

### 9. Users (2 tools)

#### `list_users`
Retrieve users in the Linear workspace.

**Parameters:**
- `query` (string, optional) - Filter by name or email

**Example:**
```javascript
mcp__linear__list_users({ query: "john" })
```

#### `get_user`
Retrieve details of a specific Linear user.

**Parameters:**
- `query` (string, required) - User ID, name, email, or "me"

**Example:**
```javascript
mcp__linear__get_user({ query: "me" })
```

---

### 10. Documentation (1 tool)

#### `search_documentation`
Search Linear's documentation to learn about features and usage.

**Parameters:**
- `query` (string, required) - Search query
- `page` (number, optional, default 0) - Page number

**Example:**
```javascript
mcp__linear__search_documentation({ query: "issue statuses", page: 0 })
```

---

## Summary: All 23 Tools

1. `list_comments` - List comments on issue
2. `create_comment` - Add comment to issue
3. `list_cycles` - Get team cycles
4. `get_document` - Fetch Linear document
5. `list_documents` - List documents
6. `get_issue` - Fetch single issue
7. `list_issues` - Search/list issues
8. `create_issue` - Create new issue
9. `update_issue` - Update existing issue
10. `list_issue_statuses` - List workflow states
11. `get_issue_status` - Get specific status
12. `list_issue_labels` - List labels
13. `create_issue_label` - Create new label
14. `list_project_labels` - List project labels
15. `list_projects` - List projects
16. `get_project` - Get specific project
17. `create_project` - Create new project
18. `update_project` - Update existing project
19. `list_teams` - List all teams
20. `get_team` - Get specific team
21. `list_users` - List workspace users
22. `get_user` - Get specific user
23. `search_documentation` - Search Linear docs

---

## Tool Validation: Critical Rules

### Only Use Validated Tools

**RULE: Every Linear operation MUST use a tool from the validated list above.**

**Examples of INVALID tool names that will fail:**
- ❌ `get_issues` (correct: `list_issues`)
- ❌ `update_comment` (correct: create new comment instead)
- ❌ `delete_issue` (not supported)
- ❌ `list_issue_statuses` (correct tool, but check args)

### Before Using a Tool

1. Check the validated list above
2. Verify the exact tool name matches
3. If unsure, use `list_*` variants which are widely available
4. Never assume tool names—verify first

### Error Prevention Strategy

```javascript
// ✅ CORRECT: Use only validated tools
Task(ccpm:linear-operations): `
operation: get_issue
params:
  issueId: PSN-29
context:
  cache: true
`

// ❌ INCORRECT: Non-existent tool
Task(ccpm:linear-operations): `
operation: fetch_issue  // This tool doesn't exist!
params:
  issueId: PSN-29
`

// ❌ INCORRECT: Assuming delete exists
Task(ccpm:linear-operations): `
operation: delete_issue  // Linear MCP doesn't support deletion
params:
  issueId: PSN-29
`
```

---

## Using the Linear Subagent

### ⚠️ IMPORTANT: Command File Invocation Format

When writing **CCPM command files** (files in `commands/`), you MUST use explicit execution instructions, NOT the YAML template format shown in the examples below.

**Command files must use this format:**

```markdown
**Use the Task tool to fetch the issue from Linear:**

Invoke the `ccpm:linear-operations` subagent:
- **Tool**: Task
- **Subagent**: ccpm:linear-operations
- **Prompt**:
  ```
  operation: get_issue
  params:
    issueId: "{the issue ID from previous step}"
  context:
    cache: true
    command: "work"
  ```
```

**Why?** Claude Code interprets command markdown files as **executable prompts**, not documentation. YAML template syntax appears as an **example** rather than an instruction to execute. Explicit instructions (e.g., "Use the Task tool to...") are unambiguous execution directives that ensure Claude invokes the subagent correctly.

### Basic Syntax (For Documentation/Examples Only)

The examples below use YAML template format for readability. **Do NOT use this format in command files**—use the explicit format shown above instead.

```markdown
Task(ccpm:linear-operations): `
operation: <tool_name>
params:
  <param1>: <value1>
  <param2>: <value2>
context:
  cache: true
  command: "planning:plan"
`
```

### Enabling Caching (Recommended)

For **read operations**, always enable caching to achieve 85-95% hit rates:

```markdown
Task(ccpm:linear-operations): `
operation: get_issue
params:
  issueId: PSN-123
context:
  cache: true  # Enable session-level caching
  command: "planning:plan"
`
```

### Providing Context for Better Errors

Include context to improve error messages and debugging:

```markdown
Task(ccpm:linear-operations): `
operation: update_issue
params:
  issueId: PSN-29
  state: "In Progress"
context:
  cache: false  # Skip cache for writes
  command: "implementation:start"  # Which command triggered this
  purpose: "Marking task as started"  # Why we're doing this
`
```

---

## Shared Helpers

The `_shared-linear-helpers.md` file provides convenience functions that **delegate to the subagent**. Use these for common operations:

### getOrCreateLabel(teamId, labelName)
Smart label management with automatic creation if missing:

```markdown
// Use this instead of manual list + create
const label = await getOrCreateLabel(teamId, "feature-request");
```

**Benefits:**
- Deduplicates label creation logic
- Handles caching automatically
- Returns label ID or creates new one

### getValidStateId(teamId, stateNameOrId)
Fuzzy state matching with suggestions on errors:

```markdown
// Handles "In Progress" → actual state ID
const stateId = await getValidStateId(teamId, "In Progress");
```

**Benefits:**
- Case-insensitive matching
- Fuzzy matching for typos
- Suggests available states on error

### ensureLabelsExist(teamId, labelNames)
Batch create labels if missing:

```markdown
// Create multiple labels in one call
const labels = await ensureLabelsExist(teamId, [
  "planning",
  "implementation",
  "review"
]);
```

---

## Performance Optimization

### Caching Strategy

**Read Operations**: Always enable caching
- `get_issue`, `list_issues`, `list_projects`
- Cache hits: 85-95%
- Performance: <50ms

**Write Operations**: Disable caching
- `create_issue`, `update_issue`, `create_comment`
- Always fetch fresh data

```markdown
// READ: Cache enabled
Task(ccpm:linear-operations): `
operation: get_issue
params:
  issueId: PSN-29
context:
  cache: true  # ✅ Cached reads
`

// WRITE: Cache disabled
Task(ccpm:linear-operations): `
operation: update_issue
params:
  issueId: PSN-29
  state: "Done"
context:
  cache: false  # ❌ Never cache writes
`
```

### Batching Operations

When possible, batch related operations:

```markdown
// ✅ GOOD: Get all needed data in one context
Task(ccpm:linear-operations): `
operation: get_issue
params:
  issueId: PSN-29
context:
  cache: true
  batchId: "planning-workflow"
`

// Then use Team, Project, Status in sequence
// Subsequent calls reuse cached Team/Project data
```

### Token Reduction Comparison

| Operation | Direct MCP | Via Subagent | Savings |
|-----------|-----------|--------------|---------|
| Get issue | 400ms, 2.5k tokens | <50ms, 0.8k tokens | 68% |
| Update issue | 600ms, 3.2k tokens | <50ms, 1.2k tokens | 62% |
| Create comment | 500ms, 2.8k tokens | <50ms, 1.0k tokens | 64% |
| **Workflow average** | **500ms, 15k tokens** | **<50ms, 8k tokens** | **-47%** |

---

## Error Handling

The Linear subagent provides **structured errors** with actionable suggestions.

### Common Error Scenarios

#### STATE_NOT_FOUND
When updating an issue to a non-existent status:

```yaml
error:
  code: STATE_NOT_FOUND
  message: "State 'In Review' not found in team"
  params:
    requestedState: "In Review"
    teamId: "psn123"
  suggestions:
    - "Use 'In Progress' (exact match required)"
    - "Available states: Backlog, Todo, In Progress, Done, Blocked"
    - "Check team configuration in Linear"
```

**Fix**: Use exact state name or `getValidStateId()` helper

#### LABEL_NOT_FOUND
When assigning a non-existent label:

```yaml
error:
  code: LABEL_NOT_FOUND
  message: "Label 'feature' not found"
  params:
    requestedLabel: "feature"
    teamId: "psn123"
  suggestions:
    - "Label will be created automatically"
    - "Use 'ensureLabelsExist()' to batch create"
    - "Available labels: bug, feature-request, documentation"
```

**Fix**: Use `getOrCreateLabel()` or `ensureLabelsExist()` helpers

#### ISSUE_NOT_FOUND
When accessing a non-existent issue:

```yaml
error:
  code: ISSUE_NOT_FOUND
  message: "Issue PSN-9999 not found"
  params:
    issueId: "PSN-9999"
  suggestions:
    - "Verify issue ID is correct (use Linear UI)"
    - "Check team/project context"
    - "Issue may have been archived"
```

**Fix**: Validate issue ID before using

---

## Examples

### Example 1: Get Issue with Caching

```markdown
Task(ccpm:linear-operations): `
operation: get_issue
params:
  issueId: PSN-29
context:
  cache: true
  command: "planning:plan"
  purpose: "Fetch task details for planning"
`
```

**Performance**: <50ms (cached)
**Token cost**: ~0.8k
**Result**: Issue object with title, description, status, labels, assignee

### Example 2: Update Issue Status and Labels

```markdown
Task(ccpm:linear-operations): `
operation: update_issue
params:
  issueId: PSN-29
  state: "In Progress"
  labels: ["planning", "implementation"]
context:
  cache: false
  command: "implementation:start"
  purpose: "Mark task as started with relevant labels"
`
```

**Performance**: 100-200ms (no cache)
**Token cost**: ~1.2k
**Result**: Updated issue with new status and labels

### Example 3: Create Comment with Context

```markdown
Task(ccpm:linear-operations): `
operation: create_comment
params:
  issueId: PSN-29
  body: |
    Progress update:
    - Implemented JWT authentication
    - 2 unit tests passing
    - Need to fix Redis integration

    Blockers:
    - Redis library compatibility
context:
  cache: false
  command: "implementation:sync"
  purpose: "Log implementation progress"
`
```

**Performance**: 150-300ms
**Token cost**: ~1.5k
**Result**: Comment added to issue with timestamp

### Example 4: Using Shared Helpers

```markdown
// Get or create label (delegates to subagent with caching)
const label = await getOrCreateLabel(teamId, "feature-request");

// Get valid state ID (fuzzy matching with suggestions)
const stateId = await getValidStateId(teamId, "In Progress");

// Ensure multiple labels exist
const labels = await ensureLabelsExist(teamId, [
  "planning",
  "implementation",
  "blocked"
]);

// Now use the results
Task(ccpm:linear-operations): `
operation: update_issue
params:
  issueId: PSN-29
  state: ${stateId}
  labels: ${labels.map(l => l.id)}
context:
  cache: false
  purpose: "Apply validated status and labels"
`
```

**Performance**: <100ms total (mostly cached lookups)
**Token cost**: ~1.8k
**Result**: Reliable label/status application with error prevention

### Example 5: Error Handling

```markdown
// PATTERN: Try operation, handle structured errors

Task(ccpm:linear-operations): `
operation: update_issue
params:
  issueId: PSN-29
  state: "Review"  // Might not exist
context:
  cache: false
  command: "implementation:sync"
`

// If error:
// {
//   code: "STATE_NOT_FOUND",
//   suggestions: ["Available states: Backlog, Todo, In Progress, Done"]
// }

// RECOVERY: Use helper or ask user
const stateId = await getValidStateId(teamId, "Review");
// Or ask user: "Which status should I use?"
```

**Pattern**: Structured errors guide user or helper selection

---

## Migration from Direct MCP

### Before: Direct MCP Call (Inefficient)

```markdown
// Direct call - no caching, higher token cost
Task(linear-operations): `
List issues in PSN project where status = "Todo"
`

// Result: ~2.5k tokens, 400ms, no future cache hits
```

### After: Via Subagent (Optimized)

```markdown
// Via subagent - automatic caching
Task(ccpm:linear-operations): `
operation: list_issues
params:
  projectId: "PSN"
  filter: {status: "Todo"}
context:
  cache: true
  command: "planning:plan"
`

// Result: ~0.9k tokens, <50ms, 85-95% cache hits next time
```

### Common Pitfalls to Avoid

```javascript
// ❌ DON'T: Forget caching
Task(ccpm:linear-operations): `
operation: get_issue
params:
  issueId: PSN-29
// Missing: context: cache: true
`

// ❌ DON'T: Use non-existent tools
Task(ccpm:linear-operations): `
operation: fetch_issue_details  // This doesn't exist
params:
  issueId: PSN-29
`

// ❌ DON'T: Cache writes
Task(ccpm:linear-operations): `
operation: update_issue
params:
  issueId: PSN-29
context:
  cache: true  // WRONG! Never cache writes
`

// ✅ DO: Follow patterns
Task(ccpm:linear-operations): `
operation: get_issue
params:
  issueId: PSN-29
context:
  cache: true  // ✅ Cache reads
  command: "planning:plan"
`
```

---

## Best Practices Summary

| Practice | Reason |
|----------|--------|
| Always use subagent for Linear ops | 50-60% token reduction |
| Enable caching on reads | 85-95% hit rate, <50ms performance |
| Disable caching on writes | Avoid stale data |
| Use shared helpers | Reduces duplication, better error handling |
| Validate tools against list | Prevent failures with non-existent tools |
| Provide context object | Better error messages and debugging |
| Handle structured errors | Graceful degradation and user guidance |

---

## References

- **Subagent Location**: `agents/linear-operations.md`
- **Shared Helpers**: `agents/_shared-linear-helpers.md`
- **Architecture Guide**: `docs/architecture/linear-subagent-architecture.md`
- **Linear MCP Docs**: Available via `search_documentation` tool
