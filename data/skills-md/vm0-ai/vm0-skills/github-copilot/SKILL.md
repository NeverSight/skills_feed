---
name: github-copilot
description: GitHub Copilot REST API via curl. Use this skill to manage Copilot subscriptions and retrieve usage metrics.
vm0_secrets:
  - GITHUB_TOKEN
---

# GitHub Copilot API

Use the GitHub Copilot REST API via direct `curl` calls to **manage Copilot subscriptions and retrieve usage metrics** for your organization.

> Official docs: `https://docs.github.com/en/rest/copilot`

**Note:** This API is for managing Copilot subscriptions and viewing metrics, not for code generation.

---

## When to Use

Use this skill when you need to:

- **Manage Copilot seat assignments** (add/remove users and teams)
- **View Copilot billing information** for an organization
- **Retrieve usage metrics** (active users, code completions, chat usage)
- **Monitor Copilot adoption** across teams
- **Audit Copilot usage** for compliance

---

## Prerequisites

1. You need a GitHub organization with Copilot Business or Enterprise
2. Generate a Personal Access Token (PAT) or use a GitHub App
3. Required permissions: `manage_billing:copilot` or `admin:org`
4. Store your token in the environment variable `GITHUB_TOKEN`

```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
```

### Token Permissions

- `manage_billing:copilot` - For billing and seat management
- `read:org` - For reading organization data
- `admin:org` - For adding/removing users and teams

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"'
> ```

## How to Use

All examples below assume you have `GITHUB_TOKEN` set.

Base URL: `https://api.github.com`

**Required headers:**
- `Authorization: Bearer ${GITHUB_TOKEN}`
- `Accept: application/vnd.github+json`
- `X-GitHub-Api-Version: 2022-11-28`

---

### 1. Get Copilot Billing Information

Get seat breakdown and settings for an organization. Replace `your-org-name` with your organization name:

```bash
bash -c 'curl -s -X GET "https://api.github.com/orgs/your-org-name/copilot/billing" --header "Authorization: Bearer ${GITHUB_TOKEN}" --header "Accept: application/vnd.github+json" --header "X-GitHub-Api-Version: 2022-11-28"'
```

**Response:**
```json
{
  "seat_breakdown": {
  "total": 12,
  "added_this_cycle": 2,
  "pending_cancellation": 0,
  "pending_invitation": 1,
  "active_this_cycle": 12,
  "inactive_this_cycle": 0
  },
  "seat_management_setting": "assign_selected",
  "public_code_suggestions": "block"
}
```

---

### 2. List All Copilot Seat Assignments

Get all users with Copilot seats. Replace `your-org-name` with your organization name:

```bash
bash -c 'curl -s -X GET "https://api.github.com/orgs/your-org-name/copilot/billing/seats?per_page=50" --header "Authorization: Bearer ${GITHUB_TOKEN}" --header "Accept: application/vnd.github+json" --header "X-GitHub-Api-Version: 2022-11-28"' | jq '.seats[] | {login: .assignee.login, last_activity: .last_activity_at}'
```

---

### 3. Get Copilot Seat Details for a User

Get specific user's Copilot seat information. Replace `your-org-name` with your organization name and `username` with the target username:

```bash
bash -c 'curl -s -X GET "https://api.github.com/orgs/your-org-name/members/username/copilot" --header "Authorization: Bearer ${GITHUB_TOKEN}" --header "Accept: application/vnd.github+json" --header "X-GitHub-Api-Version: 2022-11-28"'
```

---

### 4. Add Users to Copilot Subscription

Assign Copilot seats to specific users. Replace `your-org-name` with your organization name:

Write to `/tmp/github_copilot_request.json`:

```json
{
  "selected_usernames": ["user1", "user2"]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.github.com/orgs/your-org-name/copilot/billing/selected_users" --header "Authorization: Bearer ${GITHUB_TOKEN}" --header "Accept: application/vnd.github+json" --header "X-GitHub-Api-Version: 2022-11-28" --header "Content-Type: application/json" -d @/tmp/github_copilot_request.json'
```

**Response:**
```json
{
  "seats_created": 2
}
```

---

### 5. Remove Users from Copilot Subscription

Remove Copilot seats from specific users. Replace `your-org-name` with your organization name:

Write to `/tmp/github_copilot_request.json`:

```json
{
  "selected_usernames": ["user1", "user2"]
}
```

Then run:

```bash
bash -c 'curl -s -X DELETE "https://api.github.com/orgs/your-org-name/copilot/billing/selected_users" --header "Authorization: Bearer ${GITHUB_TOKEN}" --header "Accept: application/vnd.github+json" --header "X-GitHub-Api-Version: 2022-11-28" --header "Content-Type: application/json" -d @/tmp/github_copilot_request.json'
```

**Response:**
```json
{
  "seats_cancelled": 2
}
```

---

### 6. Add Teams to Copilot Subscription

Assign Copilot to entire teams. Replace `your-org-name` with your organization name:

Write to `/tmp/github_copilot_request.json`:

```json
{
  "selected_teams": ["engineering", "design"]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.github.com/orgs/your-org-name/copilot/billing/selected_teams" --header "Authorization: Bearer ${GITHUB_TOKEN}" --header "Accept: application/vnd.github+json" --header "X-GitHub-Api-Version: 2022-11-28" --header "Content-Type: application/json" -d @/tmp/github_copilot_request.json'
```

---

### 7. Remove Teams from Copilot Subscription

Remove Copilot from teams. Replace `your-org-name` with your organization name:

Write to `/tmp/github_copilot_request.json`:

```json
{
  "selected_teams": ["engineering"]
}
```

Then run:

```bash
bash -c 'curl -s -X DELETE "https://api.github.com/orgs/your-org-name/copilot/billing/selected_teams" --header "Authorization: Bearer ${GITHUB_TOKEN}" --header "Accept: application/vnd.github+json" --header "X-GitHub-Api-Version: 2022-11-28" --header "Content-Type: application/json" -d @/tmp/github_copilot_request.json'
```

---

### 8. Get Copilot Usage Metrics for Organization

Get usage statistics (requires 5+ active users). Replace `your-org-name` with your organization name:

```bash
bash -c 'curl -s -X GET "https://api.github.com/orgs/your-org-name/copilot/metrics?per_page=7" --header "Authorization: Bearer ${GITHUB_TOKEN}" --header "Accept: application/vnd.github+json" --header "X-GitHub-Api-Version: 2022-11-28"' | jq '.[] | {date, total_active_users, total_engaged_users}'
```

**Response:**
```json
{
  "date": "2024-06-24",
  "total_active_users": 24,
  "total_engaged_users": 20
}
```

---

### 9. Get Copilot Metrics for a Team

Get team-specific usage metrics. Replace `your-org-name` with your organization name and `team-name` with the target team:

```bash
bash -c 'curl -s -X GET "https://api.github.com/orgs/your-org-name/team/team-name/copilot/metrics" --header "Authorization: Bearer ${GITHUB_TOKEN}" --header "Accept: application/vnd.github+json" --header "X-GitHub-Api-Version: 2022-11-28"'
```

---

## Metrics Data Structure

The metrics response includes:

| Field | Description |
|-------|-------------|
| `total_active_users` | Users with Copilot activity |
| `total_engaged_users` | Users who accepted suggestions |
| `copilot_ide_code_completions` | Code completion stats by language/editor |
| `copilot_ide_chat` | IDE chat usage stats |
| `copilot_dotcom_chat` | GitHub.com chat usage |
| `copilot_dotcom_pull_requests` | PR summary usage |

---

## Guidelines

1. **Requires Copilot Business/Enterprise**: Free tier users cannot use this API
2. **Metrics need 5+ users**: Usage metrics only available with 5+ active Copilot users
3. **Data retention**: Metrics available for up to 100 days
4. **Rate limits**: Standard GitHub API rate limits apply
5. **API in preview**: Some endpoints may change
