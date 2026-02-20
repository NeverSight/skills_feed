---
name: vibe-notion
description: Interact with Notion using the unofficial private API - pages, databases, blocks, search, users, comments
allowed-tools: Bash(vibe-notion:*)
---

# Vibe Notion

A TypeScript CLI tool that enables AI agents and humans to interact with Notion workspaces through the unofficial private API. Supports full CRUD operations on pages, databases, blocks, search, and user management.

> **Note**: This skill uses Notion's internal/private API (`/api/v3/`), which is separate from the official public API. For official API access, use `vibe-notionbot`.

## Important: CLI Only

**Never call Notion's internal API directly.** Always use the `vibe-notion` CLI commands described in this skill. Do not make raw HTTP requests to `notion.so/api/v3/` or use any Notion client library. Direct API calls risk exposing credentials and may trigger Notion's abuse detection, getting the user's account blocked.

If a feature you need is not supported by `vibe-notion`, let the user know and offer to file a feature request at [devxoul/vibe-notion](https://github.com/devxoul/vibe-notion/issues) on their behalf. Before submitting, strip out any real user data — IDs, names, emails, tokens, page content, or anything else that could identify the user or their workspace. Use generic placeholders instead and keep the issue focused on describing the missing capability.

## Quick Start

```bash
# 1. Find your workspace ID
vibe-notion workspace list --pretty

# 2. Search for a page
vibe-notion search "Roadmap" --workspace-id <workspace-id> --pretty

# 3. Get page content
vibe-notion page get <page-id> --workspace-id <workspace-id> --pretty

# 4. Query a database
vibe-notion database query <collection-id> --workspace-id <workspace-id> --pretty
```

Credentials are auto-extracted from the Notion desktop app on first use. No manual setup needed.

> **Important**: `--workspace-id` is required for ALL commands that operate within a specific workspace. Use `vibe-notion workspace list` to find your workspace ID.

## Authentication

Credentials (`token_v2`) are auto-extracted from the Notion desktop app when you run any command. No API keys, OAuth, or manual extraction needed.

On macOS, your system may prompt for Keychain access on first use — this is normal and required to decrypt the cookie.

The extracted `token_v2` is stored at `~/.config/vibe-notion/credentials.json` with `0600` permissions.

## Memory

The agent maintains a `~/.config/vibe-notion/MEMORY.md` file as persistent memory across sessions. This is agent-managed — the CLI does not read or write this file. Use the `Read` and `Write` tools to manage your memory file.

### Reading Memory

At the **start of every task**, read `~/.config/vibe-notion/MEMORY.md` using the `Read` tool to load any previously discovered workspace IDs, page IDs, database IDs, and user preferences.

- If the file doesn't exist yet, that's fine — proceed without it and create it when you first have useful information to store.
- If the file can't be read (permissions, missing directory), proceed without memory — don't error out.

### Writing Memory

After discovering useful information, update `~/.config/vibe-notion/MEMORY.md` using the `Write` tool. Write triggers include:

- After discovering workspace IDs (from `workspace list`)
- After discovering useful page IDs, database IDs, collection IDs (from `search`, `page list`, `page get`, `database list`, etc.)
- After the user gives you an alias or preference ("call this the Tasks DB", "my main workspace is X")
- After discovering page/database structure (parent-child relationships, what databases live under which pages)

When writing, include the **complete file content** — the `Write` tool overwrites the entire file.

### What to Store

- Workspace IDs with names
- Page IDs with titles and parent context
- Database/collection IDs with titles and parent context
- User-given aliases ("Tasks DB", "Main workspace")
- Commonly used view IDs
- Parent-child relationships (which databases are under which pages)
- Any user preference expressed during interaction

### What NOT to Store

Never store `token_v2`, credentials, API keys, or any sensitive data. Never store full page content (just IDs and titles). Never store block-level IDs unless they're persistent references (like database blocks).

### Handling Stale Data

If a memorized ID returns an error (page not found, access denied), remove it from `MEMORY.md`. Don't blindly trust memorized data — verify when something seems off. Prefer re-searching over using a memorized ID that might be stale.

### Format / Example

Here's a concrete example of how to structure your `MEMORY.md`:

```markdown
# Vibe Notion Memory

## Workspaces

- `abc123-...` — Acme Corp (default)

## Pages (Acme Corp)

- `page-id-1` — Product Roadmap (top-level)
- `page-id-2` — Q1 Planning (under Product Roadmap)

## Databases (Acme Corp)

- `coll-id-1` — Tasks (under Product Roadmap, views: `view-1`)
- `coll-id-2` — Contacts (top-level)

## Aliases

- "roadmap" → `page-id-1` (Product Roadmap)
- "tasks" → `coll-id-1` (Tasks database)

## Notes

- User prefers --pretty output for search results
- Main workspace is "Acme Corp"
```

> Memory lets you skip repeated `search` and `workspace list` calls. When you already know an ID from a previous session, use it directly.

## Commands

### Auth Commands

```bash
vibe-notion auth status     # Check authentication status
vibe-notion auth logout     # Remove stored token_v2
vibe-notion auth extract    # Manually re-extract token_v2 (for troubleshooting)
```

### Page Commands

```bash
# List pages in a space (top-level only)
vibe-notion page list --workspace-id <workspace_id> --pretty
vibe-notion page list --workspace-id <workspace_id> --depth 2 --pretty

# Get a page and all its content blocks
vibe-notion page get <page_id> --workspace-id <workspace_id> --pretty
vibe-notion page get <page_id> --workspace-id <workspace_id> --limit 50
vibe-notion page get <page_id> --workspace-id <workspace_id> --backlinks --pretty

# Create a new page under a parent
vibe-notion page create --workspace-id <workspace_id> --parent <parent_id> --title "My Page" --pretty

# Create a page with markdown content
vibe-notion page create --workspace-id <workspace_id> --parent <parent_id> --title "My Doc" --markdown '# Hello\n\nThis is **bold** text.'

# Create a page with markdown from a file
vibe-notion page create --workspace-id <workspace_id> --parent <parent_id> --title "My Doc" --markdown-file ./content.md

# Replace all content on a page with new markdown
vibe-notion page update <page_id> --workspace-id <workspace_id> --replace-content --markdown '# New Content'
vibe-notion page update <page_id> --workspace-id <workspace_id> --replace-content --markdown-file ./updated.md

# Update page title or icon
vibe-notion page update <page_id> --workspace-id <workspace_id> --title "New Title" --pretty
vibe-notion page update <page_id> --workspace-id <workspace_id> --icon "🚀" --pretty

# Archive a page
vibe-notion page archive <page_id> --workspace-id <workspace_id> --pretty
```

### Database Commands

```bash
# Get database schema
vibe-notion database get <database_id> --workspace-id <workspace_id> --pretty

# Query a database (auto-resolves default view)
vibe-notion database query <database_id> --workspace-id <workspace_id> --pretty
vibe-notion database query <database_id> --workspace-id <workspace_id> --limit 10 --pretty
vibe-notion database query <database_id> --workspace-id <workspace_id> --view-id <view_id> --pretty
vibe-notion database query <database_id> --workspace-id <workspace_id> --search-query "keyword" --pretty
vibe-notion database query <database_id> --workspace-id <workspace_id> --timezone "America/New_York" --pretty

# List all databases in workspace
vibe-notion database list --workspace-id <workspace_id> --pretty

# Create a database
vibe-notion database create --workspace-id <workspace_id> --parent <page_id> --title "Tasks" --pretty
vibe-notion database create --workspace-id <workspace_id> --parent <page_id> --title "Tasks" --properties '{"status":{"name":"Status","type":"select"}}' --pretty

# Update database title or schema
vibe-notion database update <database_id> --workspace-id <workspace_id> --title "New Name" --pretty

# Add a row to a database
vibe-notion database add-row <database_id> --workspace-id <workspace_id> --title "Row title" --pretty
vibe-notion database add-row <database_id> --workspace-id <workspace_id> --title "Row title" --properties '{"Status":"In Progress","Due":{"start":"2025-03-01"}}' --pretty

# Update properties on an existing database row (row_id from database query)
vibe-notion database update-row <row_id> --workspace-id <workspace_id> --properties '{"Status":"Done"}' --pretty
vibe-notion database update-row <row_id> --workspace-id <workspace_id> --properties '{"Priority":"High","Tags":["backend","infra"]}' --pretty
vibe-notion database update-row <row_id> --workspace-id <workspace_id> --properties '{"Due":{"start":"2026-06-01"},"Status":"In Progress"}' --pretty
vibe-notion database update-row <row_id> --workspace-id <workspace_id> --properties '{"Related":["<target_row_id>"]}' --pretty

# Delete a property from a database (cannot delete the title property)
vibe-notion database delete-property <database_id> --workspace-id <workspace_id> --property "Status" --pretty

# Get view configuration and property visibility
vibe-notion database view-get <view_id> --workspace-id <workspace_id> --pretty

# Show or hide properties on a view (comma-separated names)
vibe-notion database view-update <view_id> --workspace-id <workspace_id> --show "ID,Due" --pretty
vibe-notion database view-update <view_id> --workspace-id <workspace_id> --hide "Assignee" --pretty
vibe-notion database view-update <view_id> --workspace-id <workspace_id> --show "Status" --hide "Due" --pretty

# Reorder columns (comma-separated names in desired order; unmentioned columns appended)
vibe-notion database view-update <view_id> --workspace-id <workspace_id> --reorder "Name,Status,Priority,Date" --pretty
vibe-notion database view-update <view_id> --workspace-id <workspace_id> --reorder "Name,Status" --show "Status" --pretty
```

### Block Commands

```bash
# Get a specific block
vibe-notion block get <block_id> --workspace-id <workspace_id> --pretty
vibe-notion block get <block_id> --workspace-id <workspace_id> --backlinks --pretty

# List child blocks
vibe-notion block children <block_id> --workspace-id <workspace_id> --pretty
vibe-notion block children <block_id> --workspace-id <workspace_id> --limit 50 --pretty
vibe-notion block children <block_id> --workspace-id <workspace_id> --start-cursor '<next_cursor_json>' --pretty

# Append child blocks
vibe-notion block append <parent_id> --workspace-id <workspace_id> --content '[{"type":"text","properties":{"title":[["Hello world"]]}}]' --pretty

# Append markdown content as blocks
vibe-notion block append <parent_id> --workspace-id <workspace_id> --markdown '# Hello\n\nThis is **bold** text.'

# Append markdown from a file
vibe-notion block append <parent_id> --workspace-id <workspace_id> --markdown-file ./content.md

# Update a block
vibe-notion block update <block_id> --workspace-id <workspace_id> --content '{"properties":{"title":[["Updated text"]]}}' --pretty

# Delete a block
vibe-notion block delete <block_id> --workspace-id <workspace_id> --pretty
```

### Block Types Reference

The internal API uses a specific block format. Here are all supported types:

#### Headings

```json
{"type": "header", "properties": {"title": [["Heading 1"]]}}
{"type": "sub_header", "properties": {"title": [["Heading 2"]]}}
{"type": "sub_sub_header", "properties": {"title": [["Heading 3"]]}}
```

#### Text

```json
{"type": "text", "properties": {"title": [["Plain text paragraph"]]}}
```

#### Lists

```json
{"type": "bulleted_list", "properties": {"title": [["Bullet item"]]}}
{"type": "numbered_list", "properties": {"title": [["Numbered item"]]}}
```

#### To-Do / Checkbox

```json
{"type": "to_do", "properties": {"title": [["Task item"]], "checked": [["Yes"]]}}
{"type": "to_do", "properties": {"title": [["Unchecked task"]], "checked": [["No"]]}}
```

#### Code Block

```json
{"type": "code", "properties": {"title": [["console.log('hello')"]], "language": [["javascript"]]}}
```

#### Quote

```json
{"type": "quote", "properties": {"title": [["Quoted text"]]}}
```

#### Divider

```json
{"type": "divider"}
```

### Rich Text Formatting

Rich text uses nested arrays with formatting codes:

| Format | Syntax | Example |
|--------|--------|---------|
| Plain | `[["text"]]` | `[["Hello"]]` |
| Bold | `["text", [["b"]]]` | `["Hello", [["b"]]]` |
| Italic | `["text", [["i"]]]` | `["Hello", [["i"]]]` |
| Strikethrough | `["text", [["s"]]]` | `["Hello", [["s"]]]` |
| Inline code | `["text", [["c"]]]` | `["Hello", [["c"]]]` |
| Link | `["text", [["a", "url"]]]` | `["Click", [["a", "https://example.com"]]]` |
| Bold + Italic | `["text", [["b"], ["i"]]]` | `["Hello", [["b"], ["i"]]]` |

Multiple segments: `[["plain "], ["bold", [["b"]]], [" more plain"]]`

### Comment Commands

```bash
# List comments on a page
vibe-notion comment list --page <page_id> --workspace-id <workspace_id> --pretty

# Create a comment on a page (starts a new discussion)
vibe-notion comment create "This is a comment" --page <page_id> --workspace-id <workspace_id> --pretty

# Reply to an existing discussion thread
vibe-notion comment create "Replying to thread" --discussion <discussion_id> --workspace-id <workspace_id> --pretty

# Get a specific comment by ID
vibe-notion comment get <comment_id> --workspace-id <workspace_id> --pretty
```

### Search Command

```bash
# Search across workspace (--workspace-id is required)
vibe-notion search "query" --workspace-id <workspace_id> --pretty
vibe-notion search "query" --workspace-id <workspace_id> --limit 10 --pretty
vibe-notion search "query" --workspace-id <workspace_id> --start-cursor <offset> --pretty
vibe-notion search "query" --workspace-id <workspace_id> --sort lastEdited --pretty
```

### User Commands

```bash
# Get current user info
vibe-notion user me --pretty

# Get a specific user
vibe-notion user get <user_id> --workspace-id <workspace_id> --pretty
```

## Output Format

### JSON (Default)

All commands output JSON by default for AI consumption:

```bash
# Search results
vibe-notion search "Roadmap" --workspace-id <workspace_id>
```
```json
{
  "results": [
    {
      "id": "305c0fcf-90b3-807a-bc1a-dc7cc18e0022",
      "title": "Getting Started",
      "score": 76.58
    }
  ],
  "has_more": true,
  "next_cursor": "20",
  "total": 100
}
```

```bash
# Database query — properties use human-readable field names from the collection schema
vibe-notion database query <database_id> --workspace-id <workspace_id>
```
```json
{
  "results": [
    {
      "id": "row-uuid",
      "properties": {
        "Name": "Acme Corp",
        "Status": "Active",
        "Type": "Enterprise"
      }
    }
  ],
  "has_more": false,
  "next_cursor": null
}
```

### Schema Hints (`$hints`)

`database get` and `database query` may include a `$hints` array when the database schema has issues. These are actionable warnings — follow the instructions in each hint to fix the problem.

```json
{
  "id": "collection-uuid",
  "name": "My Database",
  "schema": { "Name": "title", "Status": "select" },
  "$hints": [
    "Rollup 'Revenue Sum' depends on deleted relation 'Deals'. This rollup will return empty values. Fix: run `database delete-property --property \"Revenue Sum\"` to remove it."
  ]
}
```

**When `$hints` is present**: Read each hint carefully and execute the suggested fix commands. Broken properties can crash the Notion app for the user. Common issues detected:

- **Dead properties**: Soft-deleted but still in schema. Usually harmless but indicates past issues.
- **Broken rollups**: Reference deleted or missing relations. Will return empty values and may crash Notion.
- **Broken relations**: Missing target collection. May crash Notion.

If `$hints` is absent, the schema is clean — no action needed.

```bash
# Page get — returns page metadata with content blocks
vibe-notion page get <page_id> --workspace-id <workspace_id>
```
```json
{
  "id": "page-uuid",
  "title": "My Page",
  "blocks": [
    { "id": "block-1", "type": "text", "text": "Hello world" },
    { "id": "block-2", "type": "to_do", "text": "Task item" }
  ]
}
```

```bash
# With --backlinks: includes pages that link to this page/block
vibe-notion page get <page_id> --workspace-id <workspace_id> --backlinks
vibe-notion block get <block_id> --workspace-id <workspace_id> --backlinks
```
```json
{
  "id": "page-uuid",
  "title": "My Page",
  "blocks": [...],
  "backlinks": [
    { "id": "linking-page-uuid", "title": "Page That Links Here" }
  ]
}
```

```bash
# Block get — collection_view blocks include collection_id and view_ids
vibe-notion block get <block_id> --workspace-id <workspace_id>
```
```json
{
  "id": "block-uuid",
  "type": "collection_view",
  "text": "",
  "parent_id": "parent-uuid",
  "collection_id": "collection-uuid",
  "view_ids": ["view-uuid"]
}
```

### Pretty (Human-Readable)

Use `--pretty` flag for formatted output on any command:

```bash
vibe-notion search "Roadmap" --workspace-id <workspace_id> --pretty
```

## When to Use `--backlinks`

Backlinks reveal which pages/databases **link to** a given page. This is critical for efficient navigation.

**Use `--backlinks` when:**
- **Tracing relations**: A search result looks like a select option, enum value, or relation target (e.g., a plan name or category). Backlinks instantly reveal all rows/pages that reference it via relation properties — no need to hunt for the parent database.
- **Finding references**: You found a page and want to know what other pages mention or link to it.
- **Reverse lookups**: Instead of querying every database to find rows pointing to a page, use backlinks on the target page to get them directly.

**Example — finding who uses a specific plan:**
```bash
# BAD: 15 API calls — search, open empty pages, trace parents, find database, query
vibe-notion search "Enterprise Plan" ...
vibe-notion page get <plan-page-id> ...  # empty
vibe-notion block get <plan-page-id> ...  # find parent
# ... many more calls to discover the database

# GOOD: 2-3 API calls — search, then backlinks on the target
vibe-notion search "Enterprise Plan" ...
vibe-notion page get <plan-page-id> --backlinks --pretty
# → backlinks immediately show all people/rows linked to this plan
```

## Pagination

Commands that return lists support pagination via `has_more`, `next_cursor` fields:

- **`block children`**: Cursor-based. Pass `next_cursor` value from previous response as `--start-cursor`.
- **`search`**: Offset-based. Pass `next_cursor` value (a number) as `--start-cursor`.
- **`database query`**: Use `--limit` to control page size. `has_more` indicates more results exist, but the private API does not support cursor-based pagination — increase `--limit` to fetch more rows.

## Troubleshooting

### Authentication failures

If auto-extraction fails (e.g., Notion desktop app is not installed or not logged in), run the extract command manually for debug output:

```bash
vibe-notion auth extract --debug
```

This shows the Notion directory path and extraction steps to help diagnose the issue.

### `vibe-notion: command not found`

The `vibe-notion` package is not installed. Run it directly using a package runner. Ask the user which one to use:

```bash
npx vibe-notion ...
bunx vibe-notion ...
pnpm dlx vibe-notion ...
```

If you already know the user's preferred package runner, use it directly instead of asking.

## Limitations

- Auto-extraction supports macOS and Linux. Windows DPAPI decryption is not yet supported.
- `token_v2` uses the unofficial internal API and may break if Notion changes it.
- This is a private/unofficial API and is not supported by Notion.
