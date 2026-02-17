---
name: ntion-cli
description: >
  Use the ntion CLI to interact with Notion workspaces — searching, reading,
  creating, updating, and managing pages, databases (data sources), and block
  content. Use when the user wants to: (1) search their Notion workspace,
  (2) query or list databases, (3) read, create, update, archive, or relate
  pages, (4) read, append, insert, replace, or delete block content on pages,
  (5) manage Notion authentication, or (6) perform any Notion workspace
  operation from the terminal. Trigger on mentions of "Notion", "ntion",
  page/database IDs, or requests involving workspace content management.
---

# ntion CLI

Notion CLI. Run via `npx ntion` (or `ntion` if installed globally).

## Authentication

Authentication is a one-time setup stored in `~/.config/ntion/config.json`. If a command fails with exit code 6 (auth error), prompt the user to run `ntion auth`.

```bash
ntion auth --token "secret_xxx"
# Or interactive: ntion auth
# Verify: ntion doctor
```

Token is created at https://www.notion.so/profile/integrations.

## Commands

### search

```bash
ntion search --query "meeting notes"
ntion search --query "tasks" --object page --limit 10
ntion search --query "Q1" --created-after 2026-01-01T00:00:00Z
```

Options: `--query` (required), `--scope <id>`, `--object page|data_source`, `--created-after/--created-before`, `--edited-after/--edited-before`, `--created-by <user_id>`, `--limit`, `--cursor`, `--scan-limit`, `--view compact|full`, `--pretty`.

### data-sources (databases)

```bash
ntion data-sources list --query "tasks"
ntion data-sources get --id <id> --view full
ntion data-sources schema --id <id>
ntion data-sources query --id <id> \
  --filter-json '{"property":"Status","status":{"equals":"In Progress"}}' \
  --sort-json '{"property":"Created","direction":"descending"}' \
  --limit 50
```

Use `schema` to discover property names and types before querying or creating pages. Filter/sort JSON follows the Notion API filter format.

### pages

```bash
# Read
ntion pages get --id <id>
ntion pages get --id <id> --include-content --content-format markdown

# Create
ntion pages create \
  --parent-data-source-id <ds_id> \
  --properties-json '{"Name":"New task","Status":"Not started"}'

# Bulk create (up to 100)
ntion pages create-bulk \
  --parent-data-source-id <ds_id> \
  --items-json '[{"properties":{"Name":"A"}},{"properties":{"Name":"B"}}]'

# Update
ntion pages update --id <id> --patch-json '{"Status":"Done"}'

# Archive / restore
ntion pages archive --id <id>
ntion pages unarchive --id <id>

# Relations
ntion pages relate --from-id <id> --property "Project" --to-id <target_id>
ntion pages unrelate --from-id <id> --property "Project" --to-id <target_id>
```

### blocks (page content)

```bash
# Read content as markdown
ntion blocks get --id <page_or_block_id>
ntion blocks get --id <id> --depth 2 --format compact

# Append to end
ntion blocks append --id <id> --markdown $'## Section\n\nContent here'
ntion blocks append --id <id> --markdown-file ./notes.md

# Insert at position
ntion blocks insert --parent-id <id> --markdown "Intro text" --position start
ntion blocks insert --parent-id <id> --markdown "Middle" --after-id <block_id>

# Find blocks
ntion blocks select \
  --scope-id <id> \
  --selector-json '{"where":{"type":"paragraph","text_contains":"TODO"}}'

# Replace block range
ntion blocks replace-range \
  --scope-id <id> \
  --start-selector-json '{"where":{"text_contains":"## Old Section"}}' \
  --end-selector-json '{"where":{"text_contains":"## Next Section"}}' \
  --markdown "## New Section\n\nUpdated content"

# Delete blocks
ntion blocks delete --ids <block_id>
ntion blocks delete --ids <id1> <id2> <id3>
```

## Workflow patterns

### Discover → Query → Act

1. Find the database: `ntion data-sources list --query "tasks"`
2. Get its schema: `ntion data-sources schema --id <id>`
3. Query with filters: `ntion data-sources query --id <id> --filter-json '...'`
4. Create/update pages using the discovered property names

### Read → Edit page content

1. Read current content: `ntion blocks get --id <page_id>`
2. Append new content: `ntion blocks append --id <page_id> --markdown "..."`
3. Or replace a section: use `blocks replace-range` with selectors
4. Delete specific blocks: `ntion blocks delete --ids <id1> <id2>`

## Output format

All commands return JSON envelopes:

```json
{"ok": true, "data": {...}, "meta": {"request_id": "..."}}
{"ok": false, "error": {"code": "not_found", "message": "...", "retryable": false}, "meta": {...}}
```

Exit codes: 0=success, 1=failure, 2=invalid input, 3=not found, 4=conflict, 5=retryable, 6=auth error.

## Notes

- `--view compact` (default) returns minimal data. Use `--view full` when complete details are needed.
- Mutations are idempotent with verify-first recovery on ambiguous outcomes. Re-read before retrying when the CLI reports uncertainty.
- Bulk create supports `--concurrency` (default 5) for parallel operations.
- Use `--pretty` on any command for human-readable JSON output.
