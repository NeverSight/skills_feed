---
name: vibe-notionbot
description: Interact with Notion workspaces using official API - manage pages, databases, blocks, users, and comments
allowed-tools: Bash(vibe-notionbot:*)
---

# Vibe Notionbot

A TypeScript CLI tool that enables AI agents and humans to interact with Notion workspaces through the official Notion API. Supports pages, databases, blocks, users, comments, and search.

## Important: CLI Only

**Never call the Notion API directly.** Always use the `vibe-notionbot` CLI commands described in this skill. Do not make raw HTTP requests to the Notion API or use `@notionhq/client` directly. Direct API calls risk exposing credentials and may trigger Notion's abuse detection, getting the user's account blocked.

If a feature you need is not supported by `vibe-notionbot`, let the user know and offer to file a feature request at [devxoul/vibe-notion](https://github.com/devxoul/vibe-notion/issues) on their behalf. Before submitting, strip out any real user data — IDs, names, emails, tokens, page content, or anything else that could identify the user or their workspace. Use generic placeholders instead and keep the issue focused on describing the missing capability.

## Quick Start

```bash
# Check authentication status
vibe-notionbot auth status

# Search for a page or database
vibe-notionbot search "Project Roadmap"

# List all databases
vibe-notionbot database list

# Create a new page
vibe-notionbot page create --parent <parent_id> --title "My New Page"
```

## Authentication

### Integration Token (Official API)

Set the `NOTION_TOKEN` environment variable with your integration token from the [Notion Developer Portal](https://www.notion.so/my-integrations).

```bash
export NOTION_TOKEN=secret_xxx
vibe-notionbot auth status
```

The integration token provides access to the official Notion API (`@notionhq/client`).

## Commands

### Page Commands

```bash
# Retrieve a page
vibe-notionbot page get <page_id>

# Create a new page under a parent page or database
vibe-notionbot page create --parent <parent_id> --title "New Page Title"
vibe-notionbot page create --parent <database_id> --title "New Database Item" --database

# Create a page with markdown content
vibe-notionbot page create --parent <parent_id> --title "My Doc" --markdown '# Hello\n\nThis is **bold** text.'

# Create a page with markdown from a file
vibe-notionbot page create --parent <parent_id> --title "My Doc" --markdown-file ./content.md

# Update page properties
vibe-notionbot page update <page_id> --set "Status=In Progress" --set "Priority=High"

# Replace all content on a page with new markdown
vibe-notionbot page update <page_id> --replace-content --markdown '# New Content'
vibe-notionbot page update <page_id> --replace-content --markdown-file ./updated.md

# Archive (delete) a page
vibe-notionbot page archive <page_id>

# Retrieve a specific page property
vibe-notionbot page property <page_id> <property_id>
```

### Database Commands

```bash
# Retrieve a database schema
vibe-notionbot database get <database_id>

# Query a database with optional filters and sorts
vibe-notionbot database query <database_id> --filter '{"property": "Status", "select": {"equals": "In Progress"}}'
vibe-notionbot database query <database_id> --sort '[{"property": "Created time", "direction": "descending"}]'
vibe-notionbot database query <database_id> --page-size 10 --start-cursor <cursor>

# Create a database under a parent page
vibe-notionbot database create --parent <page_id> --title "My Database" --properties '{"Name": {"title": {}}}'

# Update a database schema or title
vibe-notionbot database update <database_id> --title "Updated Title"

# Delete a property from a database
vibe-notionbot database delete-property <database_id> --property "Status"

# List all databases accessible by the integration
vibe-notionbot database list
vibe-notionbot database list --page-size 10 --start-cursor <cursor>
```

### Block Commands

```bash
# Retrieve a block
vibe-notionbot block get <block_id>

# List direct children of a block (paginated)
vibe-notionbot block children <block_id>
vibe-notionbot block children <block_id> --page-size 50 --start-cursor <cursor>

# Append child blocks to a parent
vibe-notionbot block append <parent_id> --content '[{"type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Hello World"}}]}}]'

# Append markdown content as blocks
vibe-notionbot block append <parent_id> --markdown '# Hello\n\nThis is **bold** text.'

# Append markdown from a file
vibe-notionbot block append <parent_id> --markdown-file ./content.md

# Update a block's content
vibe-notionbot block update <block_id> --content '{"paragraph": {"rich_text": [{"type": "text", "text": {"content": "Updated content"}}]}}'

# Delete (archive) a block
vibe-notionbot block delete <block_id>
```

### User Commands

```bash
# List all users in the workspace
vibe-notionbot user list
vibe-notionbot user list --page-size 10 --start-cursor <cursor>

# Get info for a specific user
vibe-notionbot user get <user_id>

# Get info for the current bot/integration
vibe-notionbot user me
```

### Search Commands

```bash
# Search across the entire workspace
vibe-notionbot search "query text"

# Filter search by object type
vibe-notionbot search "Project" --filter page
vibe-notionbot search "Tasks" --filter database

# Sort search results
vibe-notionbot search "Meeting" --sort desc

# Paginate search results
vibe-notionbot search "Notes" --page-size 10 --start-cursor <cursor>
```

### Comment Commands

```bash
# List comments on a page
vibe-notionbot comment list --page <page_id>
vibe-notionbot comment list --page <page_id> --page-size 10 --start-cursor <cursor>

# Create a comment on a page
vibe-notionbot comment create "This is a comment" --page <page_id>

# Reply to a comment thread (discussion)
vibe-notionbot comment create "Replying to thread" --discussion <discussion_id>

# Retrieve a specific comment
vibe-notionbot comment get <comment_id>
```

## Output Format

### JSON (Default)

All commands output JSON by default for AI consumption:

```json
{
  "id": "...",
  "object": "page",
  "properties": { ... }
}
```

### Pretty (Human-Readable)

Use `--pretty` flag for formatted output:

```bash
vibe-notionbot search "Project" --pretty
```

## Error Handling

Common errors from the Notion API:
- `object_not_found`: The ID is incorrect or the integration doesn't have access.
- `unauthorized`: The `NOTION_TOKEN` is invalid.
- `rate_limited`: Too many requests.

## Troubleshooting

### `vibe-notionbot: command not found`

The `vibe-notion` package is not installed. Run it directly using a package runner. Ask the user which one to use:

```bash
npx -p vibe-notion vibe-notionbot ...
bunx -p vibe-notion vibe-notionbot ...
pnpm dlx --package vibe-notion vibe-notionbot ...
```

If you already know the user's preferred package runner, use it directly instead of asking.

## Limitations

- Supports Notion API version 2022-06-28.
- Does not support OAuth (token only).
- Does not support file uploads in v1.
- Page property updates are limited to simple key=value pairs unless using raw JSON.
