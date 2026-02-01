---
name: posthog-analytics
description: Automate PostHog dashboard creation, sync, update, and export via API
author: SylphAI-Inc
version: 1.1.0
---

# PostHog Analytics Skill

Automate PostHog dashboard creation, sync, update, and export via API.

## Prerequisites

### Required Tools
- `curl` - HTTP client (pre-installed on macOS/Linux)
- `jq` - JSON processor: `brew install jq` or `apt install jq`
- `bash` - Shell (the script is bash)

### PostHog API Key

1. Go to [PostHog Settings → Personal API Keys](https://us.posthog.com/settings/user-api-keys)
2. Create a new key with read/write access
3. Export it:

```bash
export POSTHOG_PERSONAL_API_KEY=phx_xxx
```

**Note**: The API key determines your organization and project. The script uses `@current` project context (your default project).

### Verify Setup

```bash
# Test your API key - should return your project info
curl -s -H "Authorization: Bearer $POSTHOG_PERSONAL_API_KEY" \
  "https://us.i.posthog.com/api/projects/@current/" | jq '{id, name}'
```

Expected output:
```json
{
  "id": 209268,
  "name": "Default project"
}
```

If you get an error, check your API key is correct and has proper permissions.


## Quick Start: Blog Analytics Example

### Step 1: Write Your Config

Create `blog_dashboard.json`:

```json
{
  "name": "Blog Analytics",
  "description": "Track blog performance and reader engagement",
  "filter": {"key": "source", "value": "blog"},
  "dashboard_id": null,
  "insights": [
    {"name": "Blog Pageviews (Total)", "type": "pageviews_total"},
    {"name": "Unique Blog Readers", "type": "unique_users"},
    {"name": "Blog Traffic Trend", "type": "traffic_trend"},
    {"name": "Top Blog Posts", "type": "top_pages"}
  ]
}
```

**Note**: Set `dashboard_id: null` for new dashboards.

### Step 2: Create Dashboard

```bash
./scripts/posthog_sync.sh create blog_dashboard.json
```

**Output**:
```
Creating dashboard: Blog Analytics
Dashboard created: ID 1166599
Creating insight: Blog Pageviews (Total)
{id: 6520531, name: "Blog Pageviews (Total)"}
...
Dashboard URL: https://us.posthog.com/project/209268/dashboard/1166599
```

The script:
- Creates a new dashboard in your PostHog project
- Returns **dashboard_id** (e.g., `1166599`) and **project_id** (e.g., `209268`) in the URL
- **Automatically updates** your config file with the `dashboard_id`

### Step 3: Add New Insights (Sync)

Edit config to add new insights, then:

```bash
./scripts/posthog_sync.sh sync blog_dashboard.json
```

Only creates NEW insights. Existing ones (matched by name) are **skipped**.

### Step 4: Update Existing Insights

Changed your filter? Edit config, then:

```bash
./scripts/posthog_sync.sh update blog_dashboard.json
```

Updates ALL insights with current config settings. Use when changing filters.

### Step 5: Export Existing Dashboard

```bash
./scripts/posthog_sync.sh export 1166599 > exported_dashboard.json
```

## Config Reference

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Dashboard name |
| `description` | No | Dashboard description |
| `filter` | No* | Event property filter: `{"key": "source", "value": "blog"}` |
| `domain_filter` | No* | URL filter fallback: `"blog.sylph.ai"` |
| `dashboard_id` | No | Set to `null` for create, or existing ID for sync/update |
| `insights` | Yes | Array of insight objects |

*At least one filter recommended. `filter` takes precedence over `domain_filter`.

### Insight Types

| Type | Display | Description |
|------|---------|-------------|
| `pageviews_total` | BoldNumber | Total pageview count |
| `unique_users` | BoldNumber | Unique visitors (DAU) |
| `traffic_trend` | LineGraph | Traffic over time |
| `top_pages` | Table | Top pages breakdown |

### Optional Insight Fields

| Field | Default | Options |
|-------|---------|---------|
| `math` | `total` | `total`, `dau`, `weekly_active`, `monthly_active` |
| `display` | Auto | `BoldNumber`, `ActionsLineGraph`, `ActionsTable` |
| `date_range` | `-30d` | `-7d`, `-30d`, `-90d`, etc. |

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `POSTHOG_PERSONAL_API_KEY` | Yes | - | Your API key (determines org/project) |
| `POSTHOG_HOST` | No | us.i.posthog.com | API host (EU: eu.i.posthog.com) |
| `POSTHOG_UI_HOST` | No | us.posthog.com | UI host for dashboard URLs |

## Files

- `scripts/posthog_sync.sh` - CLI script (create/sync/update/export)
- `examples/blog_dashboard.json` - Example config

## References

- [PostHog API Docs](https://posthog.com/docs/api)
- [Personal API Keys](https://posthog.com/docs/api/overview#personal-api-keys)
