---
name: fortify-ssc
description: "use this skill whenever the user wants to list and filter application security findings, discover applications and versions, and manage applications using Fortify Software Security Center (SSC). Triggers include: any mention of 'SSC', 'list vulnerabilities', 'list applications', and similar requests indicating interaction with Fortify SSC for application security tasks. OpenText Application Security is the new name for Fortify Software Security Center."
compatibility: Requires Fortify MCP configured for SSC, and authenticated session to SSC.
metadata:
  author: crance
  version: "0.0.1"
---

# Fortify Software Security Center (SSC) Skill
Fortify Software Security Center (SSC) integration via Model Context Protocol (MCP).

## When to Use This Skill
- List application and application version
- List security issues/vulnerabilities with filtering by severity, category, etc.
- Count issues grouped by severity, category, etc.

## Available MCP Tools
Only key MCP tools for SSC are listed here.
| Tool | Description | When to Use |
|-----------|-------------|-------------|
| `fcli_ssc_session_list` | List authentication sessions | Check authentication status |
| `fcli_ssc_app_list` | List applications | Discover available applications |
| `fcli_ssc_app_get` | Get details of a specific application | Retrieve detailed information about an application |
| `fcli_ssc_appversion_list` | List application versions | Discover available application versions |
| `fcli_ssc_appversion_get` | Get details of a specific application version | Retrieve detailed information about an application version |
| `fcli_ssc_issue_list` | List issues | Retrieve a list of security issues/vulnerabilities |
| `fcli_ssc_issue_list_filters` | Discover available filtering options for issues | Look for most appropriate filter to use |
| `fcli_ssc_issue_list_groups` | Discover available grouping options for issues | Look for most appropriate group to use |
| `fcli_ssc_issue_count` | Group and count issues | Count issues grouped by severity, category, etc. Always include `--by` parameter |
| `fcli_ssc_mcp_job` | Wait for background jobs to complete | When `pagination.jobToken` is present in responses |

## Parameter Formats
Common formats and examples for key parameters:
| Parameter | Format | Example |
|-----------|-------------|-------------|
| `appVersionNameOrId` or `--appversion` | `"<App>:<Version>"` - case-sensitive, colon-separated |  `"MyApp:MyRelease"` |
| `--filter` | `"<FilterType>:<Value>"` - preferred server-side filtering; discover via `issue_list_filters` first | `"Folder:Critical"` |
| `--filterset` | Filter set title or ID - predefined SSC filter combinations (e.g., "Security Auditor View", "Quick View"); distinct from `--filter` | `"Security Auditor View"` |
| `--embed` | Comma-separated values to include additional data (see reference files for specific options) | `"details,auditHistory"` |
| `--by` | Group name from `issue_list_groups` - **always include when using `issue_count`** | `"Folder"`, `"Category"` |

## Authentication
**All operations require authentication.** Always verify session before any  operation:
```tool
fcli_ssc_session_list with refresh-cache=true
```
- If `Expired` = `No` → proceed
- If expired → ask user to run locally: `fcli ssc session login --url "<URL>" -u "<user>" -p '<pass>'`
- When running any SSC tool, if authentication error occurs, prompt user to re-authenticate locally.

**Note:** Reference workflows assume authentication has been verified.

## Filtering: Prefer --filter; query Optional
- **Prefer `--filter`** for server-side filtering (fastest, smallest payloads)
- **Optionally use `query`** as a client-side post-filter when you need a simple match on returned fields
- Always discover available filters with `issue_list_filters` before applying them

## Pagination
- If `pagination.hasMore` = true → use `pagination-offset` for next page
- If `pagination.jobToken` present → background loading; wait with `fcli_ssc_mcp_job` (see [Background Job Handling](references/mcp-job-wait.md))
- Once `pagination.totalRecords` appears → all records collected

## Error Recovery
| Error | Recovery |
|-------|----------|
| "Session expired" | Refer to flow in `Authentication` section |
| "Application version not found" | Run `app_list` to discover correct names |
| "Unknown filter" | Run `issue_list_filters` to discover valid filters |

## Decision Tree: Choosing the Right Approach

| User Intent | Action |
|-------|----------|
| "list/show vulnerabilities" | `issue_list` with `--filter` + `--embed details` |
| "how many / count / summary" | `issue_count` with `--by` |
| "find app / which version" | `app_list` → `appversion_list` |

## Best Practices
**DO:**
- ✅ Use `--filter` for filtering
- ✅ Prioritize server-side filtering over client-side
- ✅ Prioritize use MCP tool over FCLI CLI directly

**Do NOT:**
- ❌ Guess application/version names - ask the user
- ❌ Prompt user for credentials - ask user to run `fcli ssc session login` locally
- ❌ Assume filter names exist - always run `issue_list_filters` first
- ❌ Make multiple API calls for details - use `--embed` parameter instead

## References
#### Example Workflows
| Workflow | Use When User Says... |
|----------|----------------------|
| [List and find Applications Versions](references/list-application-version.md) | "list applications", "show application versions", "what applications are available" |
| [List, Filter and Query Issues](references/list-filter-query-issues.md) | "list vulnerabilities", "show security issues", "filter issues by severity", "include suppressed issues" |
| [Summarise and Count Issues](references/issue-summary.md) | "count issues", "show summary", "breakdown by severity" |
| [Provide Recommendations](references/provide-recommendations.md) | "show recommendations", "provide remediation advice", "how to fix" |
| [Background Job Handling](references/mcp-job-wait.md) | When `pagination.jobToken` appears in responses, background data loading |
### External Resources
- [FCLI Documentation](https://fortify.github.io/fcli/)
- [SSC Documentation (version format: YY.Quarter.patch, e.g., 25.4.0)](https://www.microfocus.com/documentation/fortify-software-security-center/)
- [SSC User Guide](https://www.microfocus.com/documentation/fortify-software-security-center/2540/ssc-ugd-html-25.4.0/index.html)