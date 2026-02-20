---
name: redash
description: >
  Query Mozilla's Redash (sql.telemetry.mozilla.org) for telemetry data from BigQuery.
  Use when querying Firefox user telemetry, OS distribution, architecture breakdown, or
  running custom SQL against Mozilla's data warehouse. Triggers on "redash", "telemetry
  query", "sql.telemetry", "BigQuery query", "Firefox data", "client counts",
  "user population", "DAU", "MAU", "macOS version", "macOS distribution", "Apple Silicon",
  "aarch64", "x86_64", "architecture distribution", "Windows version", "Windows distribution",
  "how many users", "what share of users", "what percentage of Firefox users".
---

# Redash Query Tool

Query Mozilla's Redash (sql.telemetry.mozilla.org) for telemetry data. Redash is the front-end to BigQuery telemetry data.

## Knowledge References
@references/README.md
@references/fxci-schema.md

## Prerequisites

- `REDASH_API_KEY` environment variable set
- `uv` for running the script

## Quick Start

```bash
# Run custom SQL
uv run scripts/query_redash.py --sql "SELECT * FROM telemetry.main LIMIT 10"

# Fetch cached results from an existing Redash query
uv run scripts/query_redash.py --query-id 65967

# Save results to file
uv run scripts/query_redash.py --sql "SELECT 1" --output ~/moz_artifacts/data.json
```

## Usage

Either `--sql` or `--query-id` is required.

| Flag | Description |
|------|-------------|
| `--sql` | SQL query to execute against BigQuery via Redash |
| `--query-id` | Fetch cached results from an existing Redash query ID |
| `--output`, `-o` | Save results to JSON file |
| `--format`, `-f` | Output format: `json`, `csv`, `table` (default: `table`) |
| `--limit` | Limit number of rows displayed |

## Example Prompts

These natural language prompts map to queries in `references/common-queries.md`:

| Prompt | Query used |
|--------|------------|
| "What's the DAU breakdown by macOS version?" | macOS Version DAU (active_users_aggregates) |
| "Show me macOS version × architecture distribution" | macOS version × arch (baseline_clients_daily) |
| "What share of macOS users are on Apple Silicon?" | macOS version × arch, compare aarch64 vs x86_64 |
| "Pull the macOS DAU and arch breakdown for the last 28 days" | Both macOS queries |
| "What Windows versions are Firefox Desktop users on?" | Windows Version Distribution (query 65967) |
| "How many Firefox users are on Windows 11?" | Windows Version Distribution |
| "What does the macOS adoption curve look like over time?" | macOS Version DAU by os_version_major |

For questions not covered by a documented query, write SQL on the fly using the table references in `references/README.md`.

## Common Queries
@references/common-queries.md
