---
name: azure-devops-skill
description: Comprehensive Azure DevOps REST API skill for work items, pipelines, repos, test plans, wikis, and search operations via MCP tools and direct API calls
version: 1.0.0
author: Claude Code
tags:
  - azure-devops
  - rest-api
  - devops
  - work-items
  - pipelines
  - git
  - testing
  - wikis
allowed-tools:
  - mcp__ado__*
  - Bash
  - WebFetch
  - Read
  - Write
---

# Azure DevOps REST API Skill

Comprehensive guide for Azure DevOps REST API v7.2 operations including work items, pipelines, repositories, test plans, wikis, and search functionality.

## Quick Reference

| Area | Base URL | MCP Tool Prefix |
|------|----------|-----------------|
| Core | `dev.azure.com/{org}/_apis/` | `mcp__ado__core_*` |
| Work Items | `dev.azure.com/{org}/{project}/_apis/wit/` | `mcp__ado__wit_*` |
| Pipelines | `dev.azure.com/{org}/{project}/_apis/pipelines/` | `mcp__ado__pipelines_*` |
| Git/Repos | `dev.azure.com/{org}/{project}/_apis/git/` | `mcp__ado__repo_*` |
| Test Plans | `dev.azure.com/{org}/{project}/_apis/testplan/` | `mcp__ado__testplan_*` |
| Wiki | `dev.azure.com/{org}/{project}/_apis/wiki/` | `mcp__ado__wiki_*` |
| Search | `almsearch.dev.azure.com/{org}/_apis/search/` | `mcp__ado__search_*` |

## Authentication Methods

### Personal Access Token (PAT)

```bash
# Base64 encode empty username with PAT
AUTH=$(echo -n ":${PAT}" | base64)
curl -H "Authorization: Basic ${AUTH}" https://dev.azure.com/{org}/_apis/projects
```

### OAuth 2.0 Scopes

| Scope | Access Level |
|-------|--------------|
| `vso.work` | Read work items |
| `vso.work_write` | Create/update work items |
| `vso.code` | Read source code |
| `vso.code_write` | Create branches, PRs |
| `vso.build_execute` | Run pipelines |
| `vso.test` | Read test plans |
| `vso.wiki` | Read wikis |

## API Versioning

Format: `{major}.{minor}[-{stage}[.{resource-version}]]`

- Current: `7.2-preview.3`
- Example: `api-version=7.2-preview.3`

---

## 1. Work Item Operations

### Available MCP Tools

```
mcp__ado__wit_get_work_item          - Get single work item
mcp__ado__wit_get_work_items_batch_by_ids - Get multiple work items
mcp__ado__wit_my_work_items          - Get items assigned to me
mcp__ado__wit_create_work_item       - Create new work item
mcp__ado__wit_update_work_item       - Update work item fields
mcp__ado__wit_update_work_items_batch - Bulk update work items
mcp__ado__wit_add_work_item_comment  - Add comment to work item
mcp__ado__wit_list_work_item_comments - List work item comments
mcp__ado__wit_add_child_work_items   - Create child work items
mcp__ado__wit_work_items_link        - Link work items together
mcp__ado__wit_work_item_unlink       - Remove work item links
mcp__ado__wit_link_work_item_to_pull_request - Link to PR
mcp__ado__wit_add_artifact_link      - Add artifact links (branch, commit, build)
mcp__ado__wit_get_work_item_type     - Get work item type definition
mcp__ado__wit_list_backlogs          - List team backlogs
mcp__ado__wit_list_backlog_work_items - Get backlog items
mcp__ado__wit_get_work_items_for_iteration - Get sprint items
mcp__ado__wit_get_query              - Get saved query
mcp__ado__wit_get_query_results_by_id - Execute saved query
```

### WIQL Query Syntax

#### Basic Structure

```sql
SELECT [Fields]
FROM workitems
WHERE [Conditions]
ORDER BY [Fields]
ASOF [DateTime]
```

#### Common Macros

| Macro | Description |
|-------|-------------|
| `@Me` | Current user |
| `@project` | Current project |
| `@Today` | Today's date |
| `@Today - N` | N days ago |
| `@CurrentIteration` | Current sprint |
| `@StartOfMonth` | First of month |

#### Example Queries

```sql
-- Active tasks assigned to me
SELECT [System.Id], [System.Title], [System.State]
FROM workitems
WHERE [System.TeamProject] = @project
  AND [System.WorkItemType] = 'Task'
  AND [System.State] = 'Active'
  AND [System.AssignedTo] = @Me
ORDER BY [System.Priority] ASC

-- Bugs created in last 30 days
SELECT [System.Id], [System.Title], [System.CreatedDate]
FROM workitems
WHERE [System.TeamProject] = @project
  AND [System.WorkItemType] = 'Bug'
  AND [System.CreatedDate] >= @Today - 30

-- Parent-child hierarchy
SELECT [Source].[System.Id], [Target].[System.Id]
FROM workitemLinks
WHERE [Source].[System.TeamProject] = @project
  AND [System.Links.LinkType] = 'System.LinkTypes.Hierarchy-Forward'
MODE (Recursive)
```

### JSON Patch Operations

```json
[
  {"op": "add", "path": "/fields/System.Title", "value": "New Title"},
  {"op": "replace", "path": "/fields/System.State", "value": "Active"},
  {"op": "add", "path": "/relations/-", "value": {
    "rel": "System.LinkTypes.Related",
    "url": "https://dev.azure.com/{org}/_apis/wit/workItems/{id}"
  }}
]
```

### Link Types Reference

| Type | Rel Name |
|------|----------|
| Parent | `System.LinkTypes.Hierarchy-Reverse` |
| Child | `System.LinkTypes.Hierarchy-Forward` |
| Related | `System.LinkTypes.Related` |
| Predecessor | `System.LinkTypes.Dependency-Reverse` |
| Successor | `System.LinkTypes.Dependency-Forward` |

---

## 2. Pipeline Operations

### Available MCP Tools

```
mcp__ado__pipelines_get_build_definitions - List pipeline definitions
mcp__ado__pipelines_get_build_definition_revisions - Get definition history
mcp__ado__pipelines_get_builds         - List builds
mcp__ado__pipelines_get_build_status   - Get build status
mcp__ado__pipelines_get_build_log      - Get build logs
mcp__ado__pipelines_get_build_log_by_id - Get specific log
mcp__ado__pipelines_get_build_changes  - Get commits in build
mcp__ado__pipelines_run_pipeline       - Trigger pipeline run
mcp__ado__pipelines_get_run            - Get pipeline run details
mcp__ado__pipelines_list_runs          - List pipeline runs
mcp__ado__pipelines_update_build_stage - Retry/cancel stage
```

### Pipeline Trigger Example

```json
{
  "resources": {
    "repositories": {
      "self": {"refName": "refs/heads/feature-branch"}
    }
  },
  "templateParameters": {
    "environment": "staging"
  },
  "variables": {
    "customVar": {"value": "custom-value", "isSecret": false}
  }
}
```

### Build Status Values

| Status | Description |
|--------|-------------|
| `none` | Not started |
| `inProgress` | Running |
| `completed` | Finished |
| `cancelling` | Being cancelled |
| `postponed` | Delayed |
| `notStarted` | Queued |

### Build Result Values

| Result | Description |
|--------|-------------|
| `succeeded` | All tasks passed |
| `partiallySucceeded` | Some tasks failed |
| `failed` | Build failed |
| `canceled` | User cancelled |

---

## 3. Repository Operations

### Available MCP Tools

```
mcp__ado__repo_list_repos_by_project   - List repositories
mcp__ado__repo_get_repo_by_name_or_id  - Get repository details
mcp__ado__repo_list_branches_by_repo   - List branches
mcp__ado__repo_list_my_branches_by_repo - List my branches
mcp__ado__repo_get_branch_by_name      - Get branch details
mcp__ado__repo_create_branch           - Create new branch
mcp__ado__repo_search_commits          - Search commit history
mcp__ado__repo_list_pull_requests_by_repo_or_project - List PRs
mcp__ado__repo_get_pull_request_by_id  - Get PR details
mcp__ado__repo_create_pull_request     - Create PR
mcp__ado__repo_update_pull_request     - Update PR (autocomplete, status)
mcp__ado__repo_update_pull_request_reviewers - Add/remove reviewers
mcp__ado__repo_list_pull_request_threads - List PR comments
mcp__ado__repo_list_pull_request_thread_comments - Get thread comments
mcp__ado__repo_create_pull_request_thread - Create comment thread
mcp__ado__repo_reply_to_comment        - Reply to comment
mcp__ado__repo_resolve_comment         - Resolve thread
mcp__ado__repo_list_pull_requests_by_commits - Find PR by commit
```

### PR Status Values

| Status | Description |
|--------|-------------|
| `active` | Open for review |
| `abandoned` | Closed without merge |
| `completed` | Merged |

### Merge Strategies

| Strategy | Description |
|----------|-------------|
| `noFastForward` | Merge commit (default) |
| `squash` | Squash commits |
| `rebase` | Rebase and fast-forward |
| `rebaseMerge` | Rebase with merge commit |

---

## 4. Test Plan Operations

### Available MCP Tools

```
mcp__ado__testplan_list_test_plans     - List test plans
mcp__ado__testplan_create_test_plan    - Create test plan
mcp__ado__testplan_create_test_suite   - Create test suite
mcp__ado__testplan_list_test_cases     - List test cases in suite
mcp__ado__testplan_create_test_case    - Create test case
mcp__ado__testplan_update_test_case_steps - Update test steps
mcp__ado__testplan_add_test_cases_to_suite - Add cases to suite
mcp__ado__testplan_show_test_results_from_build_id - Get test results
```

### Test Case Steps Format

```
1. Navigate to login page|Login page displayed
2. Enter username|Username field populated
3. Enter password|Password field populated
4. Click login button|User is logged in successfully
```

### Test Suite Types

| Type | Description |
|------|-------------|
| `staticTestSuite` | Manual hierarchy |
| `dynamicTestSuite` | Query-based |
| `requirementTestSuite` | Linked to requirement |

### Test Outcome Values

| Outcome | Description |
|---------|-------------|
| `Passed` | Test passed |
| `Failed` | Test failed |
| `Blocked` | Cannot execute |
| `NotExecuted` | Not run |
| `Inconclusive` | No clear result |

---

## 5. Wiki Operations

### Available MCP Tools

```
mcp__ado__wiki_list_wikis              - List wikis
mcp__ado__wiki_get_wiki                - Get wiki details
mcp__ado__wiki_list_pages              - List wiki pages
mcp__ado__wiki_get_page                - Get page metadata
mcp__ado__wiki_get_page_content        - Get page content
mcp__ado__wiki_create_or_update_page   - Create/update page
```

### Wiki Types

| Type | Description |
|------|-------------|
| `projectWiki` | Project-scoped wiki |
| `codeWiki` | Git-backed wiki |

### Page Path Format

- Root: `/`
- Subpage: `/Parent/Child`
- Spaces: `/My%20Page`

---

## 6. Search Operations

### Available MCP Tools

```
mcp__ado__search_code                  - Search source code
mcp__ado__search_workitem              - Search work items
mcp__ado__search_wiki                  - Search wiki pages
```

### Code Search Filters

```json
{
  "Project": ["project-name"],
  "Repository": ["repo-name"],
  "Path": ["/src"],
  "Branch": ["main"],
  "CodeElement": ["class", "def", "function"]
}
```

### Work Item Search Filters

```json
{
  "System.TeamProject": ["project-name"],
  "System.WorkItemType": ["Bug", "Task"],
  "System.State": ["Active", "New"],
  "System.AssignedTo": ["user@domain.com"]
}
```

---

## 7. Core Operations

### Available MCP Tools

```
mcp__ado__core_list_projects           - List projects
mcp__ado__core_list_project_teams      - List teams
mcp__ado__core_get_identity_ids        - Get user identity
mcp__ado__work_list_team_iterations    - List iterations
mcp__ado__work_list_iterations         - List all iterations
mcp__ado__work_create_iterations       - Create iterations
mcp__ado__work_assign_iterations       - Assign to team
mcp__ado__work_get_team_capacity       - Get team capacity
mcp__ado__work_update_team_capacity    - Update capacity
mcp__ado__work_get_iteration_capacities - Get iteration capacity
```

---

## 8. Advanced Security Operations

### Available MCP Tools

```
mcp__ado__advsec_get_alerts            - Get security alerts
mcp__ado__advsec_get_alert_details     - Get alert details
```

### Alert Types

| Type | Description |
|------|-------------|
| `Dependency` | Vulnerable dependencies |
| `Secret` | Exposed secrets |
| `Code` | Code vulnerabilities |

---

## Rate Limiting

### TSTU (Throughput Unit) Limits

- **Anonymous**: 200 TSTUs/minute
- **Authenticated**: 1200 TSTUs/minute

### Response Headers

```
X-RateLimit-Resource: core
X-RateLimit-Delay: 500
X-RateLimit-Limit: 1200
X-RateLimit-Remaining: 847
X-RateLimit-Reset: 1609459200
Retry-After: 30
```

### Handling Rate Limits

```python
import time
import requests

def api_call_with_retry(url, headers, max_retries=3):
    for attempt in range(max_retries):
        response = requests.get(url, headers=headers)
        if response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 30))
            time.sleep(retry_after)
            continue
        return response
    raise Exception("Rate limit exceeded after retries")
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 204 | No Content (DELETE) |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict (version) |
| 429 | Rate Limited |
| 500 | Server Error |

### Error Response Format

```json
{
  "$id": "1",
  "innerException": null,
  "message": "Error description",
  "typeName": "Microsoft.VisualStudio.Services.WebApi.VssServiceException",
  "typeKey": "VssServiceException",
  "errorCode": 0
}
```

---

## Common Field Reference

### System Fields

| Field | Reference Name |
|-------|----------------|
| ID | `System.Id` |
| Title | `System.Title` |
| State | `System.State` |
| Assigned To | `System.AssignedTo` |
| Area Path | `System.AreaPath` |
| Iteration Path | `System.IterationPath` |
| Work Item Type | `System.WorkItemType` |
| Created Date | `System.CreatedDate` |
| Changed Date | `System.ChangedDate` |
| Tags | `System.Tags` |
| Description | `System.Description` |

### Scheduling Fields

| Field | Reference Name |
|-------|----------------|
| Story Points | `Microsoft.VSTS.Scheduling.Effort` |
| Remaining Work | `Microsoft.VSTS.Scheduling.RemainingWork` |
| Original Estimate | `Microsoft.VSTS.Scheduling.OriginalEstimate` |
| Completed Work | `Microsoft.VSTS.Scheduling.CompletedWork` |

---

## Best Practices

### 1. Use Batch Operations

- Use `mcp__ado__wit_get_work_items_batch_by_ids` instead of multiple single calls
- Max 200 items per batch request

### 2. Minimize Field Selection

- Only request fields you need: `fields=System.Id,System.Title,System.State`
- Reduces response size and API load

### 3. Handle Pagination

- Use `$top` and `$skip` for large result sets
- Follow continuation tokens when provided

### 4. Version Control

- Use `test` operation in JSON Patch for optimistic concurrency
- Always check `rev` field before updates

### 5. Error Recovery

- Implement exponential backoff for rate limits
- Log correlation IDs from response headers

---

## References

- [Azure DevOps REST API v7.2](https://learn.microsoft.com/en-us/rest/api/azure/devops/?view=azure-devops-rest-7.2)
- [WIQL Syntax Reference](https://learn.microsoft.com/en-us/azure/devops/boards/queries/wiql-syntax)
- [Authentication Guide](https://learn.microsoft.com/en-us/azure/devops/integrate/get-started/authentication/authentication-guidance)
- [Rate Limits](https://learn.microsoft.com/en-us/azure/devops/integrate/concepts/rate-limits)
