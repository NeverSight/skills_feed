---
name: bigquery
description: >
  Query Mozilla telemetry data directly from BigQuery using the bq CLI.
  Use when the user wants to run SQL against Firefox telemetry, analyze Windows version
  distribution, count DAU/MAU/WAU, query Glean metrics, or investigate user populations.
  Triggers on "bigquery", "bq", "telemetry query", "DAU", "MAU", "Windows distribution",
  "macOS distribution", "Darwin version", "Linux distribution", "kernel version",
  "client count", "user count", "Glean metrics query", "baseline_clients".
---

# BigQuery

Query Mozilla telemetry data directly using the `bq` CLI.

## Prerequisites

- `gcloud` and `bq` CLI installed (`brew install google-cloud-sdk`)
- Authenticated: `gcloud auth login` with a Mozilla account
- Billing project set: queries run against a project you have `bigquery.jobs.create` on
- (Optional but highly recommended) [mozdata-claude-plugin](https://github.com/akkomar/mozdata-claude-plugin) — provides Glean Dictionary MCP for metric/ping discovery, making it much easier to find the right tables and columns

## Authentication

```bash
# Check current account
gcloud config get-value account

# Re-authenticate if needed
gcloud auth login

# List available projects
gcloud projects list --format="table(projectId,name)"

# Set billing project (mozdata is the standard choice)
gcloud config set project mozdata
```

If queries fail with "Access Denied", the billing project likely lacks permissions. Try `--project_id=mozdata`.

## Running Queries

```bash
# Basic query
bq query --project_id=mozdata --use_legacy_sql=false --format=pretty "SELECT ..."

# Dry run (check cost before executing)
bq query --project_id=mozdata --use_legacy_sql=false --dry_run "SELECT ..."
```

Always use `--project_id=mozdata` and `--use_legacy_sql=false`.

## Table Selection

Choose the right table — this is the most important optimization:

| Query Type | Table | Why |
|------------|-------|-----|
| Windows version distribution | `telemetry.windows_10_aggregate` | Pre-aggregated, instant |
| DAU/MAU by standard dimensions | `firefox_desktop_derived.active_users_aggregates_v3` | Pre-computed, 100x faster |
| DAU with custom dimensions | `firefox_desktop.baseline_clients_daily` | One row per client per day |
| MAU/WAU/retention | `firefox_desktop.baseline_clients_last_seen` | Bit patterns, scan 1 day not 28 |
| Event analysis | `firefox_desktop.events_stream` | Pre-unnested, clustered |
| Mobile search | `search.mobile_search_clients_daily_v2` | Pre-aggregated |
| Specific Glean metric | `firefox_desktop.metrics` | Raw metrics ping |

All tables are in the `moz-fx-data-shared-prod` project. Fully qualify as `` `moz-fx-data-shared-prod.{dataset}.{table}` ``.

## Critical Rules

- **Always use aggregate tables first** — raw tables are 10-100x more expensive
- **Always include partition filter** — `submission_date` or `DATE(submission_timestamp)`
- **Use `sample_id = 0`** for development (1% sample) — remove for production
- **Say "clients" not "users"** — BigQuery tracks `client_id`, not actual humans
- **Never join across products by client_id** — each product has its own namespace
- **Use `events_stream` for events** — never raw `events_v1` (requires UNNEST)
- **Use `baseline_clients_last_seen` for MAU** — bit patterns, scan 1 day not 28

## References

- `references/tables.md` — Detailed table schemas and common query patterns
- `references/os-versions.md` — Windows, macOS, and Linux version distribution queries with build number, Darwin, and kernel version mappings

## Related Skills

- **redash** — Web UI frontend to BigQuery with visualizations and sharing
- **mozdata:query-writing** — Guided query writing with Glean Dictionary MCP
- **mozdata:probe-discovery** — Find Glean metrics and telemetry probes
