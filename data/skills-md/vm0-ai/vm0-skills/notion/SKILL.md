---
name: notion
description: Notion API for managing pages, databases, and blocks. Use this skill to create pages, query databases, search content, and build integrations with Notion workspaces.
vm0_secrets:
  - NOTION_API_KEY
---

# Notion API

Manage pages, databases, and content blocks in Notion workspaces.

## When to Use

- Create and update Notion pages
- Query and filter database entries
- Search across workspace content
- Append content blocks to pages
- Manage database schemas and properties

## Prerequisites

```bash
export NOTION_API_KEY=ntn_your-integration-token
```

### Get API Key

1. Go to https://www.notion.so/profile/integrations
2. Click "New integration"
3. Name your integration and select workspace
4. Copy the "Internal Integration Secret" (`ntn_...` or `secret_...`)
5. **Important**: Share pages/databases with the integration via "Add connections" in Notion

### Page ID Format

Notion URLs contain page IDs. Extract and normalize them:

```
URL: https://www.notion.so/My-Page-2b70e96f0134807d8450c8793839c659
Page ID: 2b70e96f0134807d8450c8793839c659 (remove hyphens if present)
```

```bash
# Normalize page ID (remove hyphens)
PAGE_ID=$(echo "2b70e96f-0134-807d-8450-c8793839c659" | tr -d '-')
```

> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"'
> ```

## Core APIs

### Read Page with Content

Replace `<your-page-id>` with your actual Notion page ID:

```bash
# Get page metadata
bash -c 'curl -s -X GET "https://api.notion.com/v1/pages/<your-page-id>" --header "Authorization: Bearer $NOTION_API_KEY" --header "Notion-Version: 2022-06-28" | jq '"'"'{title: .properties.title.title[0].plain_text, url, last_edited_time}'"'"

# Get page content blocks
bash -c 'curl -s -X GET "https://api.notion.com/v1/blocks/<your-page-id>/children?page_size=100" --header "Authorization: Bearer $NOTION_API_KEY" --header "Notion-Version: 2022-06-28" | jq '"'"'.results[] | {type, text: (.[.type].rich_text // [] | map(.plain_text) | join("")), has_children}'"'"
```

### Read Nested Blocks (Toggle, etc.)

Blocks with `has_children: true` contain nested content. Replace `<your-block-id>` with your actual block ID:

```bash
bash -c 'curl -s -X GET "https://api.notion.com/v1/blocks/<your-block-id>/children" --header "Authorization: Bearer $NOTION_API_KEY" --header "Notion-Version: 2022-06-28" | jq '"'"'.results[] | {type, text: (.[.type].rich_text // [] | map(.plain_text) | join(""))}'"'"
```

### Search Workspace

Write to `/tmp/notion_request.json`:

```json
{
  "query": "Meeting Notes",
  "page_size": 10
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.notion.com/v1/search" --header "Authorization: Bearer $NOTION_API_KEY" --header "Notion-Version: 2022-06-28" --header "Content-Type: application/json" -d @/tmp/notion_request.json | jq '"'"'.results[] | {id, object, title: .properties.title.title[0].plain_text // .title[0].plain_text}'"'"
```

Docs: https://developers.notion.com/reference/post-search

### List Database Entries

Write to `/tmp/notion_request.json`:

```json
{
  "page_size": 100
}
```

Replace `<your-database-id>` with your actual database ID and run:

```bash
bash -c 'curl -s -X POST "https://api.notion.com/v1/databases/<your-database-id>/query" --header "Authorization: Bearer $NOTION_API_KEY" --header "Notion-Version: 2022-06-28" --header "Content-Type: application/json" -d @/tmp/notion_request.json | jq '"'"'.results[] | {id, properties}'"'"
```

Docs: https://developers.notion.com/reference/post-database-query

### Query with Filter

Replace `<your-database-id>` with your actual database ID:

```bash
curl -s -X POST "https://api.notion.com/v1/databases/<your-database-id>/query" --header "Authorization: Bearer $NOTION_API_KEY" --header 'Notion-Version: 2022-06-28' --header 'Content-Type: application/json' -d @- << 'EOF'
{
  "filter": {
  "property": "Status",
  "select": {"equals": "Done"}
  },
  "sorts": [{"property": "Date", "direction": "descending"}],
  "page_size": 50
}
EOF
```

### Query with Multiple Filters

Replace `<your-database-id>` with your actual database ID:

```bash
curl -s -X POST "https://api.notion.com/v1/databases/<your-database-id>/query" --header "Authorization: Bearer $NOTION_API_KEY" --header 'Notion-Version: 2022-06-28' --header 'Content-Type: application/json' -d @- << 'EOF'
{
  "filter": {
  "and": [
  {"property": "Status", "select": {"does_not_equal": "Archived"}},
  {"property": "Due", "date": {"on_or_before": "2024-12-31"}}
  ]
  }
}
EOF
```

### Get Database Schema

Replace `<your-database-id>` with your actual database ID:

```bash
bash -c 'curl -s "https://api.notion.com/v1/databases/<your-database-id>" --header "Authorization: Bearer $NOTION_API_KEY" --header '"'"'Notion-Version: 2022-06-28'"'"' | jq '"'"'{title: .title[0].plain_text, properties: .properties | keys}'"'"
```

Docs: https://developers.notion.com/reference/retrieve-a-database

### Get Page

Replace `<your-page-id>` with your actual page ID:

```bash
bash -c 'curl -s "https://api.notion.com/v1/pages/<your-page-id>" --header "Authorization: Bearer $NOTION_API_KEY" --header '"'"'Notion-Version: 2022-06-28'"'"' | jq '"'"'{id, url, properties}'"'"
```

Docs: https://developers.notion.com/reference/retrieve-a-page

### Create Page in Database

```bash
curl -s -X POST 'https://api.notion.com/v1/pages' --header "Authorization: Bearer $NOTION_API_KEY" --header 'Notion-Version: 2022-06-28' --header 'Content-Type: application/json' -d @- << 'EOF'
{
  "parent": {"database_id": "your-database-id"},
  "properties": {
  "Name": {"title": [{"text": {"content": "New Task"}}]},
  "Status": {"select": {"name": "To Do"}},
  "Due": {"date": {"start": "2024-12-31"}}
  }
}
EOF
```

Docs: https://developers.notion.com/reference/post-page

### Create Page with Content

```bash
curl -s -X POST 'https://api.notion.com/v1/pages' --header "Authorization: Bearer $NOTION_API_KEY" --header 'Notion-Version: 2022-06-28' --header 'Content-Type: application/json' -d @- << 'EOF'
{
  "parent": {"page_id": "parent-page-id"},
  "properties": {
  "title": {"title": [{"text": {"content": "My New Page"}}]}
  },
  "children": [
  {
  "object": "block",
  "type": "heading_2",
  "heading_2": {"rich_text": [{"text": {"content": "Introduction"}}]}
  },
  {
  "object": "block",
  "type": "paragraph",
  "paragraph": {"rich_text": [{"text": {"content": "This is the content."}}]}
  }
  ]
}
EOF
```

### Update Page Properties

Replace `<your-page-id>` with your actual page ID:

```bash
curl -s -X PATCH "https://api.notion.com/v1/pages/<your-page-id>" --header "Authorization: Bearer $NOTION_API_KEY" --header 'Notion-Version: 2022-06-28' --header 'Content-Type: application/json' -d @- << 'EOF'
{
  "properties": {
  "Status": {"select": {"name": "In Progress"}}
  }
}
EOF
```

Docs: https://developers.notion.com/reference/patch-page

### Archive Page

Write to `/tmp/notion_request.json`:

```json
{
  "archived": true
}
```

Replace `<your-page-id>` with your actual page ID and run:

```bash
bash -c 'curl -s -X PATCH "https://api.notion.com/v1/pages/<your-page-id>" --header "Authorization: Bearer $NOTION_API_KEY" --header "Notion-Version: 2022-06-28" --header "Content-Type: application/json" -d @/tmp/notion_request.json'
```

### Get Block Children

Replace `<your-block-id>` with your actual block ID:

```bash
bash -c 'curl -s "https://api.notion.com/v1/blocks/<your-block-id>/children?page_size=100" --header "Authorization: Bearer $NOTION_API_KEY" --header '"'"'Notion-Version: 2022-06-28'"'"' | jq '"'"'.results[] | {type, id}'"'"
```

Docs: https://developers.notion.com/reference/get-block-children

### Append Blocks to Page

Replace `<your-page-id>` with your actual page ID:

```bash
curl -s -X PATCH "https://api.notion.com/v1/blocks/<your-page-id>/children" --header "Authorization: Bearer $NOTION_API_KEY" --header 'Notion-Version: 2022-06-28' --header 'Content-Type: application/json' -d @- << 'EOF'
{
  "children": [
  {
  "object": "block",
  "type": "paragraph",
  "paragraph": {"rich_text": [{"text": {"content": "New paragraph added."}}]}
  },
  {
  "object": "block",
  "type": "to_do",
  "to_do": {
  "rich_text": [{"text": {"content": "Task item"}}],
  "checked": false
  }
  }
  ]
}
EOF
```

Docs: https://developers.notion.com/reference/patch-block-children

### Delete Block

Replace `<your-block-id>` with your actual block ID:

```bash
curl -s -X DELETE "https://api.notion.com/v1/blocks/<your-block-id>" --header "Authorization: Bearer $NOTION_API_KEY" --header 'Notion-Version: 2022-06-28'
```

### List Users

```bash
bash -c 'curl -s '"'"'https://api.notion.com/v1/users'"'"' --header "Authorization: Bearer $NOTION_API_KEY" --header '"'"'Notion-Version: 2022-06-28'"'"' | jq '"'"'.results[] | {id, name, type}'"'"
```

Docs: https://developers.notion.com/reference/get-users

### Get Current Bot

```bash
curl -s 'https://api.notion.com/v1/users/me' --header "Authorization: Bearer $NOTION_API_KEY" --header 'Notion-Version: 2022-06-28'
```

### Create Database

```bash
curl -s -X POST 'https://api.notion.com/v1/databases' --header "Authorization: Bearer $NOTION_API_KEY" --header 'Notion-Version: 2022-06-28' --header 'Content-Type: application/json' -d @- << 'EOF'
{
  "parent": {"page_id": "parent-page-id"},
  "title": [{"text": {"content": "Task Tracker"}}],
  "properties": {
  "Name": {"title": {}},
  "Status": {"select": {"options": [
  {"name": "To Do", "color": "gray"},
  {"name": "In Progress", "color": "blue"},
  {"name": "Done", "color": "green"}
  ]}},
  "Due Date": {"date": {}},
  "Assignee": {"people": {}},
  "Priority": {"select": {"options": [
  {"name": "High", "color": "red"},
  {"name": "Medium", "color": "yellow"},
  {"name": "Low", "color": "green"}
  ]}}
  }
}
EOF
```

Docs: https://developers.notion.com/reference/create-a-database

## Property Types

### Setting Properties (Create/Update)

| Type | Format |
|------|--------|
| Title | `{"title": [{"text": {"content": "value"}}]}` |
| Rich Text | `{"rich_text": [{"text": {"content": "value"}}]}` |
| Number | `{"number": 42}` |
| Select | `{"select": {"name": "Option"}}` |
| Multi-select | `{"multi_select": [{"name": "Tag1"}, {"name": "Tag2"}]}` |
| Date | `{"date": {"start": "2024-01-01", "end": "2024-01-31"}}` |
| Checkbox | `{"checkbox": true}` |
| URL | `{"url": "https://example.com"}` |
| Email | `{"email": "user@example.com"}` |
| Phone | `{"phone_number": "+1234567890"}` |
| People | `{"people": [{"id": "user-id"}]}` |
| Relation | `{"relation": [{"id": "page-id"}]}` |

## Block Types

### Text Blocks

```json
{"type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Text"}}]}}
{"type": "heading_1", "heading_1": {"rich_text": [{"text": {"content": "H1"}}]}}
{"type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "H2"}}]}}
{"type": "heading_3", "heading_3": {"rich_text": [{"text": {"content": "H3"}}]}}
{"type": "quote", "quote": {"rich_text": [{"text": {"content": "Quote"}}]}}
{"type": "callout", "callout": {"rich_text": [{"text": {"content": "Note"}}], "icon": {"emoji": "💡"}}}
```

### List Blocks

```json
{"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "Item"}}]}}
{"type": "numbered_list_item", "numbered_list_item": {"rich_text": [{"text": {"content": "Item"}}]}}
{"type": "to_do", "to_do": {"rich_text": [{"text": {"content": "Task"}}], "checked": false}}
{"type": "toggle", "toggle": {"rich_text": [{"text": {"content": "Toggle"}}]}}
```

### Code Block

```json
{"type": "code", "code": {"rich_text": [{"text": {"content": "console.log('Hello')"}}], "language": "javascript"}}
```

### Divider

```json
{"type": "divider", "divider": {}}
```

## Filter Operators

### Text/Title/Rich Text
`equals`, `does_not_equal`, `contains`, `does_not_contain`, `starts_with`, `ends_with`, `is_empty`, `is_not_empty`

### Number
`equals`, `does_not_equal`, `greater_than`, `less_than`, `greater_than_or_equal_to`, `less_than_or_equal_to`, `is_empty`, `is_not_empty`

### Date
`equals`, `before`, `after`, `on_or_before`, `on_or_after`, `is_empty`, `is_not_empty`, `past_week`, `past_month`, `past_year`, `next_week`, `next_month`, `next_year`

### Select/Multi-select
`equals`, `does_not_equal`, `is_empty`, `is_not_empty`, `contains` (multi-select), `does_not_contain` (multi-select)

### Checkbox
`equals`, `does_not_equal`

## Rich Text Annotations

```json
{
  "text": {"content": "Styled text", "link": {"url": "https://example.com"}},
  "annotations": {
  "bold": true,
  "italic": false,
  "strikethrough": false,
  "underline": false,
  "code": false,
  "color": "red"
  }
}
```

**Colors**: `default`, `gray`, `brown`, `orange`, `yellow`, `green`, `blue`, `purple`, `pink`, `red`, `gray_background`, `brown_background`, etc.

## Pagination

All list endpoints support cursor-based pagination:

Write to `/tmp/notion_request.json`:

```json
{
  "page_size": 100
}
```

```bash
# First request
bash -c 'curl -s -X POST "https://api.notion.com/v1/databases/<your-database-id>/query" --header "Authorization: Bearer $NOTION_API_KEY" --header "Notion-Version: 2022-06-28" --header "Content-Type: application/json" -d @/tmp/notion_request.json'
# Response includes: {"next_cursor": "abc123", "has_more": true}
```

Write to `/tmp/notion_request.json`:

```json
{
  "page_size": 100,
  "start_cursor": "<your-cursor>"
}
```

```bash
# Next page
bash -c 'curl -s -X POST "https://api.notion.com/v1/databases/<your-database-id>/query" --header "Authorization: Bearer $NOTION_API_KEY" --header "Notion-Version: 2022-06-28" --header "Content-Type: application/json" -d @/tmp/notion_request.json'
```

## Rate Limits

- Average: 3 requests/second
- Burst: Higher for short periods
- 429 response = retry with exponential backoff

## API Reference

- Main Docs: https://developers.notion.com
- API Reference: https://developers.notion.com/reference
- Integration Settings: https://www.notion.so/profile/integrations
