---
name: sentry
description: Sentry error monitoring and issue tracking skill for retrieving issues, events, and project health data. Use when working with error tracking, exceptions, crashes, debugging production issues, or analyzing error patterns.
allowed-tools: Read Bash Edit
---

# Sentry Error Monitoring Skill

**Created by [Return Zero Inc.](https://github.com/rtzr)**

Comprehensive Sentry integration for Claude Code providing issue retrieval, event analysis, error tracking, and project health monitoring capabilities.

## Features

### 1. **Issue Management**
- List issues by project or organization
- Retrieve issue details (title, first/last seen, event count)
- Filter by status (unresolved, resolved, ignored)
- Search issues by query
- Update issue status

### 2. **Event Analysis**
- List events for specific issues
- Retrieve event details with stack traces
- Debug source map issues
- Analyze error patterns

### 3. **Project Monitoring**
- List organization projects
- Get project health statistics
- View error trends
- Monitor release health

### 4. **Tag Analysis**
- View tag distributions
- Analyze error patterns by tag
- Filter issues by tag values

## Automatic Features

- **Rate Limiting**: Respects Sentry API rate limits
- **Retry Logic**: Automatic retry on transient errors
- **Environment Detection**: Flexible environment variable pattern matching
- **Result Formatting**: Markdown tables, JSON, or summary text
- **Error Handling**: Clear, actionable error messages

## Environment Variables

This skill uses environment variables managed by `jelly-dotenv`. See `skills/jelly-dotenv/SKILL.md` for configuration details.

Required variables:
- `SENTRY_AUTH_TOKEN` - Your Sentry authentication token (org or personal)
- `SENTRY_ORG` or `SENTRY_ORGANIZATION` - Organization slug

Optional variables:
- `SENTRY_PROJECT` - Default project slug
- `SENTRY_REGION` - API region: us (default), de
- `SENTRY_TIMEOUT` - Request timeout in ms (default: 30000)

Variables can be configured in either:
- `skills/jelly-dotenv/.env` (skill-common, highest priority)
- Project root `/.env` (project-specific, fallback)

## Configuration

### Environment Variables

The skill **automatically detects** Sentry credentials using flexible pattern matching:

```bash
# ✅ Standard naming (recommended)
SENTRY_AUTH_TOKEN=sntrys_your_token_here
SENTRY_ORG=my-organization
SENTRY_PROJECT=my-project

# ✅ Alternative naming
SENTRY_ORGANIZATION=my-organization
SENTRY_TOKEN=sntrys_your_token_here

# ✅ Wildcard patterns (auto-detected)
PROD_SENTRY_TOKEN=sntrys_your_token_here
PROD_SENTRY_ORG=my-organization

# ✅ Optional settings
SENTRY_REGION=us          # us (default), de
SENTRY_TIMEOUT=30000      # Request timeout in ms
```

### Regional Endpoints

Supports US and EU (Germany) regions:

```bash
# US (default)
SENTRY_REGION=us
# Base URL: https://sentry.io/api/0/

# Germany/EU
SENTRY_REGION=de
# Base URL: https://de.sentry.io/api/0/
```

## API Endpoints Reference

### Organizations
- `GET /api/0/organizations/` - List organizations
- `GET /api/0/organizations/{org}/` - Get organization details
- `GET /api/0/organizations/{org}/projects/` - List projects

### Issues
- `GET /api/0/organizations/{org}/issues/` - List organization issues
- `GET /api/0/projects/{org}/{project}/issues/` - List project issues (deprecated)
- `GET /api/0/organizations/{org}/issues/{issue_id}/` - Get issue details
- `PUT /api/0/organizations/{org}/issues/{issue_id}/` - Update issue
- `DELETE /api/0/organizations/{org}/issues/{issue_id}/` - Delete issue

### Events
- `GET /api/0/organizations/{org}/issues/{issue_id}/events/` - List issue events
- `GET /api/0/projects/{org}/{project}/events/` - List project error events
- `GET /api/0/projects/{org}/{project}/events/{event_id}/` - Get event details

### Tags
- `GET /api/0/organizations/{org}/issues/{issue_id}/tags/` - List issue tags
- `GET /api/0/organizations/{org}/issues/{issue_id}/tags/{tag}/values/` - Get tag values

## Usage Scenarios

### Scenario 1: List Unresolved Issues

**User Request**: "Show me all unresolved Sentry issues"

**Skill Actions**:
```bash
# Load environment variables
source skills/jelly-dotenv/load-env.sh

# Build API URL
SENTRY_BASE_URL="${SENTRY_REGION:-us}"
if [ "$SENTRY_BASE_URL" = "de" ]; then
    SENTRY_BASE_URL="https://de.sentry.io"
else
    SENTRY_BASE_URL="https://sentry.io"
fi

# List unresolved issues
curl -s \
  -H "Authorization: Bearer ${SENTRY_AUTH_TOKEN}" \
  "${SENTRY_BASE_URL}/api/0/organizations/${SENTRY_ORG}/issues/?query=is:unresolved" | jq .
```

### Scenario 2: Get Issue Details

**User Request**: "Show me details for issue 123456"

**Skill Actions**:
```bash
curl -s \
  -H "Authorization: Bearer ${SENTRY_AUTH_TOKEN}" \
  "${SENTRY_BASE_URL}/api/0/organizations/${SENTRY_ORG}/issues/123456/" | jq .
```

### Scenario 3: List Recent Events for an Issue

**User Request**: "Show me the last 10 events for issue 123456"

**Skill Actions**:
```bash
curl -s \
  -H "Authorization: Bearer ${SENTRY_AUTH_TOKEN}" \
  "${SENTRY_BASE_URL}/api/0/organizations/${SENTRY_ORG}/issues/123456/events/?limit=10" | jq .
```

### Scenario 4: Search Issues by Query

**User Request**: "Find all issues containing 'NullPointerException'"

**Skill Actions**:
```bash
curl -s \
  -H "Authorization: Bearer ${SENTRY_AUTH_TOKEN}" \
  "${SENTRY_BASE_URL}/api/0/organizations/${SENTRY_ORG}/issues/?query=NullPointerException" | jq .
```

### Scenario 5: List Project Error Events

**User Request**: "Show recent errors for my-project"

**Skill Actions**:
```bash
curl -s \
  -H "Authorization: Bearer ${SENTRY_AUTH_TOKEN}" \
  "${SENTRY_BASE_URL}/api/0/projects/${SENTRY_ORG}/my-project/events/" | jq .
```

### Scenario 6: Resolve an Issue

**User Request**: "Resolve issue 123456"

**Skill Actions**:
```bash
curl -s -X PUT \
  -H "Authorization: Bearer ${SENTRY_AUTH_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"status": "resolved"}' \
  "${SENTRY_BASE_URL}/api/0/organizations/${SENTRY_ORG}/issues/123456/" | jq .
```

### Scenario 7: List Projects in Organization

**User Request**: "Show me all Sentry projects"

**Skill Actions**:
```bash
curl -s \
  -H "Authorization: Bearer ${SENTRY_AUTH_TOKEN}" \
  "${SENTRY_BASE_URL}/api/0/organizations/${SENTRY_ORG}/projects/" | jq .
```

## Security Policy

### Authentication
- **Bearer Token**: Authorization header with auth token
- **Credentials**: Loaded from environment variables only
- **Logging**: Tokens automatically redacted in logs

### Permissions
- **Org Tokens**: Recommended for CI/CD and automation
- **Personal Tokens**: Bound to user permissions
- **Scopes**: Configure minimal required scopes

### Data Access
- **Read Operations**: Primary focus (GET requests)
- **Write Operations**: Status updates allowed
- **Destructive Operations**: Issue deletion requires explicit confirmation

## Error Handling

The skill provides comprehensive error handling with actionable messages:

### Connection Errors
- Network issues
- Unreachable API
- **Action**: Check internet connection and Sentry service status

### Authentication Errors (401)
- Invalid or expired token
- **Action**: Verify SENTRY_AUTH_TOKEN is correct and not expired

### Permission Errors (403)
- Insufficient scope or access
- **Action**: Check token scopes and organization membership

### Not Found Errors (404)
- Invalid organization, project, or issue ID
- **Action**: Verify resource identifiers

### Rate Limit Errors (429)
- Too many requests
- **Action**: Wait and retry (automatic backoff)

## Output Formats

### Markdown (Default)
- Formatted tables with issue details
- Key metrics summary
- Status highlights

### JSON
- Raw API response
- Programmatic access
- Full data structure

### Summary
- Text overview
- Critical issues only
- Quick scan format

## Bash Helper Functions

For command-line usage with jelly-dotenv:

```bash
# Load environment variables from jelly-dotenv (with fallback to project root)
source skills/jelly-dotenv/load-env.sh

# Determine base URL
if [ "${SENTRY_REGION:-us}" = "de" ]; then
    SENTRY_BASE_URL="https://de.sentry.io"
else
    SENTRY_BASE_URL="https://sentry.io"
fi

# Sentry API curl helper
sentry-curl() {
    local endpoint="$1"
    shift
    curl -s \
        -H "Authorization: Bearer ${SENTRY_AUTH_TOKEN}" \
        -H "Content-Type: application/json" \
        "$@" \
        "${SENTRY_BASE_URL}/api/0${endpoint}" | jq .
}

# List unresolved issues
sentry-issues() {
    local query="${1:-is:unresolved}"
    sentry-curl "/organizations/${SENTRY_ORG}/issues/?query=${query}"
}

# Get issue details
sentry-issue() {
    local issue_id="$1"
    sentry-curl "/organizations/${SENTRY_ORG}/issues/${issue_id}/"
}

# List issue events
sentry-events() {
    local issue_id="$1"
    local limit="${2:-10}"
    sentry-curl "/organizations/${SENTRY_ORG}/issues/${issue_id}/events/?limit=${limit}"
}

# List projects
sentry-projects() {
    sentry-curl "/organizations/${SENTRY_ORG}/projects/"
}

# Resolve issue
sentry-resolve() {
    local issue_id="$1"
    sentry-curl "/organizations/${SENTRY_ORG}/issues/${issue_id}/" \
        -X PUT -d '{"status": "resolved"}'
}

# Ignore issue
sentry-ignore() {
    local issue_id="$1"
    sentry-curl "/organizations/${SENTRY_ORG}/issues/${issue_id}/" \
        -X PUT -d '{"status": "ignored"}'
}
```

### Quick Aliases

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
# Sentry quick commands
alias sentry-unresolved='sentry-issues "is:unresolved"'
alias sentry-new='sentry-issues "is:unresolved firstSeen:-24h"'
alias sentry-critical='sentry-issues "is:unresolved level:fatal"'
```

**Usage**:
```bash
# List unresolved issues
sentry-issues

# Get specific issue
sentry-issue 123456

# List events for issue
sentry-events 123456 20

# List projects
sentry-projects

# Resolve an issue
sentry-resolve 123456

# Search for specific errors
sentry-issues "TypeError is:unresolved"
```

## Query Syntax

Sentry supports a powerful search syntax:

### Status Filters
- `is:unresolved` - Unresolved issues
- `is:resolved` - Resolved issues
- `is:ignored` - Ignored issues

### Time Filters
- `firstSeen:-24h` - First seen in last 24 hours
- `lastSeen:-1w` - Last seen in past week
- `age:-30d` - Created in last 30 days

### Level Filters
- `level:error` - Error level issues
- `level:fatal` - Fatal/crash level
- `level:warning` - Warning level

### Assignment
- `is:assigned` - Assigned to someone
- `is:unassigned` - Not assigned
- `assigned:me` - Assigned to current user

### Combine Filters
```bash
# Critical unresolved issues from today
sentry-issues "is:unresolved level:fatal firstSeen:-24h"

# Unassigned errors from past week
sentry-issues "is:unresolved is:unassigned lastSeen:-1w"
```

## Integration with Claude Code

This skill activates automatically when users mention:
- "sentry"
- "error tracking"
- "issues"
- "exceptions"
- "crashes"
- "error monitoring"

The skill will:
1. Load Sentry credentials from .env
2. Execute the requested query
3. Format results as Markdown tables
4. Provide actionable error messages if something fails

## Limitations

- **API Rate Limits**: Subject to Sentry's rate limiting
- **Token Expiry**: Personal tokens don't expire, org tokens may
- **Data Retention**: Limited by Sentry plan retention period
- **Project Scope**: Single organization per configuration

## Troubleshooting

### "Configuration error: SENTRY_AUTH_TOKEN is required"
**Solution**: Add auth token to .env file:
```bash
SENTRY_AUTH_TOKEN=sntrys_your_token_here
SENTRY_ORG=my-organization
```

### "Authentication failed (401)"
**Solution**:
1. Verify token is correct
2. Check token hasn't been revoked
3. Ensure token has required scopes

### "Organization not found (404)"
**Solution**: Verify SENTRY_ORG matches your organization slug (not display name)

### "Permission denied (403)"
**Solution**:
1. Check token scopes include required permissions
2. Verify user has access to the organization/project

## Creating Auth Tokens

### Organization Auth Token (Recommended)
1. Go to Settings > Developer Settings > Internal Integrations
2. Create a new Internal Integration
3. Configure required permissions:
   - Project: Read
   - Issue & Event: Read (or Admin for updates)
   - Organization: Read
4. Copy the token

### Personal Auth Token
1. Go to Account > API > Auth Tokens
2. Click "Create New Token"
3. Select required scopes
4. Copy the token

## References

- [Sentry API Documentation](https://docs.sentry.io/api/)
- [Events & Issues API](https://docs.sentry.io/api/events/)
- [Authentication](https://docs.sentry.io/api/auth/)
- [Auth Tokens](https://docs.sentry.io/account/auth-tokens/)
- [Create Auth Token Tutorial](https://docs.sentry.io/api/guides/create-auth-token/)
