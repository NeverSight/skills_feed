---
name: monday
description: Monday.com GraphQL API via curl. Use this skill to manage boards, items, and projects.
vm0_secrets:
  - MONDAY_API_KEY
---

# Monday.com API

Use the Monday.com GraphQL API via direct `curl` calls to **manage boards, items, and project data**.

> Official docs: `https://developer.monday.com/api-reference/`

---

## When to Use

Use this skill when you need to:

- **Query boards and items** from Monday.com
- **Create, update, or delete items** in boards
- **Manage board columns and groups**
- **Sync data** between Monday.com and other systems
- **Automate project workflows**

---

## Prerequisites

1. Log in to [Monday.com](https://monday.com/)
2. Go to your avatar → Developers → My Access Tokens
3. Generate a new API token
4. Store it in the environment variable `MONDAY_API_KEY`

```bash
export MONDAY_API_KEY="your-api-token"
```

### API Info

- GraphQL endpoint: `https://api.monday.com/v2`
- All requests are POST
- Requires `Authorization` header with API token
- Requires `API-Version` header (use `2024-10`)

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"'
> ```

## How to Use

All examples below assume you have `MONDAY_API_KEY` set.

---

### 1. Get Current User

Query the authenticated user's info:

Write to `/tmp/monday_request.json`:

```json
{
  "query": "query { me { id name email } }"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.monday.com/v2" --header "Authorization: ${MONDAY_API_KEY}" --header "API-Version: 2024-10" --header "Content-Type: application/json" -d @/tmp/monday_request.json'
```

---

### 2. List All Boards

Get all boards in your account:

Write to `/tmp/monday_request.json`:

```json
{
  "query": "query { boards (limit: 10) { id name state items_count } }"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.monday.com/v2" --header "Authorization: ${MONDAY_API_KEY}" --header "API-Version: 2024-10" --header "Content-Type: application/json" -d @/tmp/monday_request.json'
```

---

### 3. Get Board Details

Get a specific board with its groups and columns:

Write to `/tmp/monday_request.json`:

```json
{
  "query": "query { boards (ids: <your-board-id>) { id name groups { id title } columns { id title type } } }"
}
```

Replace `<your-board-id>` with an actual board ID from the "List All Boards" response (example 2).

Then run:

```bash
bash -c 'curl -s -X POST "https://api.monday.com/v2" --header "Authorization: ${MONDAY_API_KEY}" --header "API-Version: 2024-10" --header "Content-Type: application/json" -d @/tmp/monday_request.json'
```

---

### 4. Get Items from a Board

Get items (rows) from a specific board:

Write to `/tmp/monday_request.json`:

```json
{
  "query": "query { boards (ids: <your-board-id>) { items_page (limit: 10) { items { id name column_values { id text value } } } } }"
}
```

Replace `<your-board-id>` with an actual board ID from the "List All Boards" response (example 2).

Then run:

```bash
bash -c 'curl -s -X POST "https://api.monday.com/v2" --header "Authorization: ${MONDAY_API_KEY}" --header "API-Version: 2024-10" --header "Content-Type: application/json" -d @/tmp/monday_request.json'
```

---

### 5. Create a New Item

Create a new item in a board:

Write to `/tmp/monday_request.json`:

```json
{
  "query": "mutation { create_item (board_id: <your-board-id>, group_id: \"<your-group-id>\", item_name: \"<your-item-name>\") { id name } }"
}
```

Replace the following values:
- `<your-board-id>`: An actual board ID from the "List All Boards" response (example 2)
- `<your-group-id>`: A group ID from the "Get Board Details" response (example 3, groups array)
- `<your-item-name>`: Your desired name for the new item

Then run:

```bash
bash -c 'curl -s -X POST "https://api.monday.com/v2" --header "Authorization: ${MONDAY_API_KEY}" --header "API-Version: 2024-10" --header "Content-Type: application/json" -d @/tmp/monday_request.json'
```

---

### 6. Create Item with Column Values

Create an item with specific column values:

Write to `/tmp/monday_request.json`:

```json
{
  "query": "mutation ($boardId: ID!, $groupId: String!, $itemName: String!, $columnValues: JSON!) { create_item (board_id: $boardId, group_id: $groupId, item_name: $itemName, column_values: $columnValues) { id name } }",
  "variables": {
    "boardId": "<your-board-id>",
    "groupId": "<your-group-id>",
    "itemName": "<your-item-name>",
    "columnValues": "{\"status\": {\"label\": \"Working on it\"}, \"date\": {\"date\": \"2025-01-15\"}}"
  }
}
```

Replace the following values:
- `<your-board-id>`: An actual board ID from the "List All Boards" response (example 2)
- `<your-group-id>`: A group ID from the "Get Board Details" response (example 3, groups array)
- `<your-item-name>`: Your desired name for the new item

Then run:

```bash
bash -c 'curl -s -X POST "https://api.monday.com/v2" --header "Authorization: ${MONDAY_API_KEY}" --header "API-Version: 2024-10" --header "Content-Type: application/json" -d @/tmp/monday_request.json'
```

---

### 7. Update an Item

Update an existing item's column values:

Write to `/tmp/monday_request.json`:

```json
{
  "query": "mutation ($boardId: ID!, $itemId: ID!, $columnValues: JSON!) { change_multiple_column_values (board_id: $boardId, item_id: $itemId, column_values: $columnValues) { id name } }",
  "variables": {
    "boardId": "<your-board-id>",
    "itemId": "<your-item-id>",
    "columnValues": "{\"status\": {\"label\": \"Done\"}}"
  }
}
```

Replace the following values:
- `<your-board-id>`: An actual board ID from the "List All Boards" response (example 2)
- `<your-item-id>`: An item ID from the "Get Items from a Board" response (example 4)

Then run:

```bash
bash -c 'curl -s -X POST "https://api.monday.com/v2" --header "Authorization: ${MONDAY_API_KEY}" --header "API-Version: 2024-10" --header "Content-Type: application/json" -d @/tmp/monday_request.json'
```

---

### 8. Delete an Item

Delete an item from a board:

Write to `/tmp/monday_request.json`:

```json
{
  "query": "mutation { delete_item (item_id: <your-item-id>) { id } }"
}
```

Replace `<your-item-id>` with an actual item ID from the "Get Items from a Board" response (example 4).

Then run:

```bash
bash -c 'curl -s -X POST "https://api.monday.com/v2" --header "Authorization: ${MONDAY_API_KEY}" --header "API-Version: 2024-10" --header "Content-Type: application/json" -d @/tmp/monday_request.json'
```

---

### 9. Create a New Board

Create a new board:

Write to `/tmp/monday_request.json`:

```json
{
  "query": "mutation { create_board (board_name: \"My New Board\", board_kind: public) { id name } }"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.monday.com/v2" --header "Authorization: ${MONDAY_API_KEY}" --header "API-Version: 2024-10" --header "Content-Type: application/json" -d @/tmp/monday_request.json'
```

---

### 10. Search Items

Search for items across boards:

Write to `/tmp/monday_request.json`:

```json
{
  "query": "query { items_page_by_column_values (limit: 10, board_id: <your-board-id>, columns: [{column_id: \"name\", column_values: [\"Task\"]}]) { items { id name } } }"
}
```

Replace `<your-board-id>` with an actual board ID from the "List All Boards" response (example 2).

Then run:

```bash
bash -c 'curl -s -X POST "https://api.monday.com/v2" --header "Authorization: ${MONDAY_API_KEY}" --header "API-Version: 2024-10" --header "Content-Type: application/json" -d @/tmp/monday_request.json'
```

---

## Common Column Types

| Column Type | Value Format |
|-------------|--------------|
| Status | `{"label": "Done"}` |
| Date | `{"date": "2025-01-15"}` |
| Text | `"Your text here"` |
| Number | `"123"` |
| Person | `{"id": 12345678}` |
| Dropdown | `{"labels": ["Option1", "Option2"]}` |
| Checkbox | `{"checked": true}` |

---

## Guidelines

1. **Use variables for complex queries**: GraphQL variables make escaping easier
2. **Check column IDs**: Use the board query to get exact column IDs before updating
3. **API versioning**: Always include `API-Version` header for consistent behavior
4. **Rate limits**: API has rate limits; add delays for bulk operations
5. **Column values are JSON strings**: When using `column_values`, pass as escaped JSON string
