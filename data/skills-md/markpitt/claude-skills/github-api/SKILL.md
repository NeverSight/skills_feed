---
name: github-api
description: Orchestrates comprehensive GitHub API access across all services. Intelligently routes API operations to specialized resource files covering authentication, repositories, issues/PRs, workflows, security, and more. Use when implementing GitHub integrations, automating operations, or building applications that interact with GitHub.
version: 2.0
---

# GitHub API Orchestration Skill

Comprehensive skill for working with the GitHub API across all services and operations. This skill provides intelligent routing to focused resource files covering both REST API v3 and GraphQL API v4.

## Quick Reference: When to Load Which Resource

| Use Case | Load Resource | Key Concepts |
|----------|---------------|--------------|
| Setting up authentication, checking rate limits, handling errors, pagination | `resources/rest-api-basics.md` | Auth methods, rate limits, error codes, ETags, conditional requests |
| Creating/managing repos, branches, commits, releases, tags, Git objects | `resources/repositories.md` | Repo CRUD, branch protection, file operations, releases, Git data |
| Working with issues, PRs, reviews, comments, labels, milestones | `resources/issues-pull-requests.md` | Issue tracking, code review, approvals, merging, reactions |
| Managing users, organizations, teams, permissions, membership | `resources/users-organizations-teams.md` | User profiles, org operations, team management, collaborators |
| Automating workflows, CI/CD runs, artifacts, secrets, runners | `resources/workflows-actions.md` | Workflow triggers, run management, artifacts, env secrets, runners |
| Searching repositories, code, issues, commits, users | `resources/search-content.md` | Repository discovery, code search, issue search, user lookup |
| Security scanning, packages, webhooks, notifications, gists, projects, apps | `resources/security-webhooks.md` | Dependabot, code scanning, packages, webhooks, notifications, apps |

## Orchestration Protocol

### Phase 1: Identify Your Task

Before loading a resource, classify your GitHub API needs:

**Task Type Indicators:**
- **Setting up**: Authentication, testing credentials → Load `rest-api-basics.md`
- **Repository work**: Creating, configuring, managing repos and branches → Load `repositories.md`
- **Collaboration**: Issues, PRs, code reviews → Load `issues-pull-requests.md`
- **Automation**: Workflows, CI/CD, runners → Load `workflows-actions.md`
- **Organization**: Users, teams, permissions → Load `users-organizations-teams.md`
- **Discovery**: Finding repositories or code → Load `search-content.md`
- **Advanced**: Security features, webhooks, packages → Load `security-webhooks.md`

**Complexity Patterns:**
- **Single operation**: Load one resource file
- **Multi-step workflow**: May need 2-3 related resources (e.g., search + repository + workflows)
- **Complex integration**: Combine foundational + specialized resources

### Phase 2: Load and Execute

1. Load the appropriate resource file(s)
2. Find the specific API operation or pattern you need
3. Adapt the example to your use case
4. Execute with appropriate authentication

### Phase 3: Validate & Monitor

- Verify API responses are successful
- Check rate limit headers if making multiple calls
- Handle errors according to error handling patterns in `rest-api-basics.md`

## API Endpoints Overview

### REST API v3
- **Base URL**: `https://api.github.com`
- **Authentication**: Token, PAT, GitHub Apps
- **Rate Limit**: 5,000 requests/hour (authenticated)
- **Use for**: Straightforward CRUD operations on resources

### GraphQL API v4
- **Endpoint**: `https://api.github.com/graphql`
- **Authentication**: Bearer token
- **Rate Limit**: 5,000 points/hour (query-dependent)
- **Use for**: Complex queries combining multiple data types, mutations

## Most Common Operations

### Quick Command Reference

```bash
# Repository operations
gh repo create NAME
gh repo view owner/repo
gh repo clone owner/repo

# Issues
gh issue list
gh issue create
gh issue close NUMBER

# Pull requests
gh pr list
gh pr create
gh pr merge NUMBER

# Actions
gh workflow run WORKFLOW
gh run list
gh run view RUN_ID

# Search
gh api search/repositories -f q="QUERY"
gh api search/code -f q="QUERY"
gh api search/issues -f q="QUERY"

# Authentication
gh auth login
gh auth status
gh auth token
```

## Authentication Guide (Quick Start)

### GitHub CLI (Recommended)
```bash
gh auth login
gh api /user  # Test authentication
```

### Personal Access Token
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.github.com/user
```

→ See `resources/rest-api-basics.md` for complete auth details

## Common Patterns

### Bulk Repository Operations
```bash
# Add label to multiple issues
for issue in 1 2 3; do
  gh api repos/owner/repo/issues/$issue/labels -X POST -f labels[]=bug
  sleep 1  # Rate limiting
done
```

### Workflow Integration
```bash
# Trigger workflow with inputs
gh workflow run build.yml -f environment=production

# Monitor run status
gh api repos/owner/repo/actions/runs -f per_page=1 \
  --jq '.workflow_runs[0].conclusion'
```

### Error Handling
```bash
# Check response status
response=$(gh api repos/owner/repo -i 2>&1)
if echo "$response" | grep -q "HTTP/2 404"; then
  echo "Not found"
fi
```

→ See `resources/rest-api-basics.md` for comprehensive error handling

## Resource File Summaries

- **rest-api-basics.md** (369 lines): Authentication, rate limiting, pagination, error handling, best practices
- **repositories.md** (231 lines): Repo CRUD, branches, protection, commits, releases, Git data
- **issues-pull-requests.md** (272 lines): Issue tracking, PR management, reviews, approvals, code comments
- **users-organizations-teams.md** (162 lines): User operations, org management, teams, membership
- **workflows-actions.md** (211 lines): Workflow management, runs, artifacts, secrets, runners
- **search-content.md** (150 lines): Repository search, code search, issue/PR search, user/commit search
- **security-webhooks.md** (386 lines): Dependabot, code scanning, packages, webhooks, notifications, gists, apps, projects

## Best Practices Summary

### 1. Rate Limiting
- Use conditional requests with ETags to avoid counting against limits
- Implement exponential backoff when hitting limits
- Use GraphQL for complex multi-resource queries
- Check `rate_limit` endpoint before batch operations

### 2. Authentication
- Use fine-grained PATs with minimal scopes
- Prefer GitHub Apps for integrations
- Use `gh` CLI when available
- Never commit tokens to version control

### 3. Error Handling
- Implement retry logic with exponential backoff
- Validate input before sending requests
- Check rate limits before making requests
- Log errors with context

### 4. Performance
- Use GraphQL for complex data requirements combining multiple resources
- Implement pagination properly
- Cache responses when appropriate
- Use webhooks instead of polling

→ See `resources/rest-api-basics.md` for detailed patterns

## GraphQL vs REST Decision Tree

**Use GraphQL API v4 when:**
- Querying multiple related resources (e.g., repo + issues + PRs in one call)
- Complex filtering or sorting requirements
- Need precise field selection (bandwidth optimization)
- Working with Projects V2

**Use REST API v3 when:**
- Simple, straightforward resource operations
- Comfort with REST patterns
- Legacy integrations
- Bulk operations (GitHub CLI integration)

## Troubleshooting Quick Links

| Problem | Resource | Section |
|---------|----------|---------|
| "403 rate limited" | rest-api-basics.md | Rate Limiting |
| "401 unauthorized" | rest-api-basics.md | Authentication Methods |
| "422 validation failed" | rest-api-basics.md | Error Response Format |
| Cannot push to branch | repositories.md | Branch Protection |
| Merge conflicts in PR | issues-pull-requests.md | Merging |
| Workflow not triggering | workflows-actions.md | Workflow Management |
| Results not searchable yet | search-content.md | Search Code/Repositories |

## External Resources

- [GitHub REST API Documentation](https://docs.github.com/en/rest)
- [GitHub GraphQL API Documentation](https://docs.github.com/en/graphql)
- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [GitHub Webhooks Documentation](https://docs.github.com/en/webhooks)
- [GitHub Apps Documentation](https://docs.github.com/en/apps)

---

**Remember**: This is a modular reference organized by service area. Load only the resource files relevant to your current task. All major GitHub API operations are covered; use the quick reference table to find the right starting point.
