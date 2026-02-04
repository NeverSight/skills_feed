---
name: notion-sdk
description: Control Notion via Python SDK. TRIGGERS - Notion API, create page, query database, add blocks.
allowed-tools: Read, Bash, Glob, Grep, AskUserQuestion
---

# Notion SDK Skill

Control Notion programmatically using the official `notion-client` Python SDK. See [PyPI](https://pypi.org/project/notion-client/) for current version.

## When to Use This Skill

Use this skill when:

- Creating pages or databases in Notion via API
- Querying Notion databases programmatically
- Adding blocks (text, code, headings) to Notion pages
- Automating Notion workflows with Python
- Integrating external data sources with Notion

## Preflight: Token Collection

Before any Notion API operation, collect the integration token:

```
AskUserQuestion(questions=[{
    "question": "Please provide your Notion Integration Token (starts with ntn_ or secret_)",
    "header": "Notion Token",
    "options": [
        {"label": "I have a token ready", "description": "Token from notion.so/my-integrations"},
        {"label": "Need to create one", "description": "Go to notion.so/my-integrations → New integration"}
    ],
    "multiSelect": false
}])
```

After user provides token:

1. Validate format (must start with `ntn_` or `secret_`)
2. Test with `validate_token()` from `scripts/notion_wrapper.py`
3. Remind user: **Each page/database must be shared with the integration**

## Quick Start

### 1. Create a Page in Database

```python
from notion_client import Client
from scripts.create_page import (
    create_database_page,
    title_property,
    status_property,
    date_property,
)

client = Client(auth="ntn_...")
page = create_database_page(
    client,
    data_source_id="abc123...",  # Database ID
    properties={
        "Name": title_property("My New Task"),
        "Status": status_property("In Progress"),
        "Due Date": date_property("2025-12-31"),
    }
)
print(f"Created: {page['url']}")
```

### 2. Add Content Blocks

```python
from scripts.add_blocks import (
    append_blocks,
    heading,
    paragraph,
    bullet,
    code_block,
    callout,
)

blocks = [
    heading("Overview", level=2),
    paragraph("This page was created via the Notion API."),
    callout("Remember to share the page with your integration!", emoji="⚠️"),
    heading("Tasks", level=3),
    bullet("First task"),
    bullet("Second task"),
    code_block("print('Hello, Notion!')", language="python"),
]
append_blocks(client, page["id"], blocks)
```

### 3. Query Database

```python
from scripts.query_database import (
    query_data_source,
    checkbox_filter,
    status_filter,
    and_filter,
    sort_by_property,
)

# Find incomplete high-priority items
results = query_data_source(
    client,
    data_source_id="abc123...",
    filter_obj=and_filter(
        checkbox_filter("Done", False),
        status_filter("Priority", "High")
    ),
    sorts=[sort_by_property("Due Date", "ascending")]
)
for page in results:
    title = page["properties"]["Name"]["title"][0]["plain_text"]
    print(f"- {title}")
```

## Available Scripts

| Script              | Purpose                                       |
| ------------------- | --------------------------------------------- |
| `notion_wrapper.py` | Client setup, token validation, retry wrapper |
| `create_page.py`    | Create pages, property builders               |
| `add_blocks.py`     | Append blocks, block type builders            |
| `query_database.py` | Query, filter, sort, search                   |

## References

- [Property Types](./references/property-types.md) - All 24 property types with examples
- [Block Types](./references/block-types.md) - All block types with structures
- [Rich Text](./references/rich-text.md) - Formatting, links, mentions
- [Pagination](./references/pagination.md) - Handling large result sets

## Important Constraints

### Rate Limits

- **3 requests/second** average (burst tolerated briefly)
- Use `api_call_with_retry()` for automatic rate limit handling
- 429 responses include `Retry-After` header

### Authentication Model

- **Page-level sharing** required (not workspace-wide)
- User must explicitly add integration to each page/database:
  - Page → ... menu → Connections → Add connection → Select integration

### API Version (v2.6.0+)

- Uses `data_source_id` instead of `database_id` for multi-source databases
- Legacy `database_id` still works for simple databases
- Scripts handle both patterns automatically

### Operations NOT Supported

- Workspace settings modification
- User permissions management
- Template creation/management
- Billing/subscription access

## API Behavior Patterns

Insights discovered through integration testing (test citations for verification).

### Rate Limiting & Retry Logic

`api_call_with_retry()` handles transient failures automatically:

| Error Type       | Behavior          | Wait Strategy                            |
| ---------------- | ----------------- | ---------------------------------------- |
| 429 Rate Limited | Retries           | Respects Retry-After header (default 1s) |
| 500 Server Error | Retries           | Exponential backoff: 1s, 2s, 4s          |
| Auth/Validation  | Fails immediately | No retry                                 |

_Citation: `test_client.py::TestRetryLogic` (lines 146-193)_

### Read-After-Write Consistency

Newly created blocks may not be immediately queryable. Add 0.5s minimum delay:

```python
append_blocks(client, page_id, blocks)
time.sleep(0.5)  # Eventual consistency delay
children = client.blocks.children.list(page_id)
```

_Citation: `test_integration.py::TestBlockAppend::test_retrieve_appended_blocks` (line 298)_

### v2.6.0 API Migration

| Old Pattern                     | New Pattern (v2.6.0+)              |
| ------------------------------- | ---------------------------------- |
| `client.databases.query()`      | `client.data_sources.query()`      |
| `filter: {"value": "database"}` | `filter: {"value": "data_source"}` |

_Citation: `test_integration.py::TestDatabaseQuery` (line 110)_

### Archive-Only Deletion

Pages cannot be permanently deleted via API - only archived (moved to trash):

```python
client.pages.update(page_id, archived=True)  # Trash, not delete
```

_Citation: `test_integration.py` cleanup fixture (lines 72-76)_

## Edge Cases & Validation

### Property Builder Edge Cases

| Input             | Behavior                      | Valid? |
| ----------------- | ----------------------------- | ------ |
| Empty string `""` | Creates empty content         | Yes    |
| Empty array `[]`  | Clears multi-select/relations | Yes    |
| `None` for number | Clears property value         | Yes    |
| Zero `0`          | Valid number (not falsy)      | Yes    |
| Negative `-42`    | Valid number                  | Yes    |
| Unicode/emoji     | Fully preserved               | Yes    |

_Citation: `test_property_builders.py::TestPropertyBuildersEdgeCases` (lines 302-341)_

### Input Validation Responsibility

Builders are intentionally permissive - validation happens at API level:

| Property | Builder Accepts | API Validates    |
| -------- | --------------- | ---------------- |
| Date     | Any string      | ISO 8601 only    |
| URL      | Any string      | Valid URL format |
| Checkbox | Truthy values   | Boolean expected |

**Best Practice**: Validate in your application before building properties.

_Citation: `test_property_builders.py::TestPropertyBuildersInvalidInputs` (lines 347-376)_

### Token Validation

- Case-sensitive: Only lowercase `ntn_` and `secret_` valid
- Format check happens before API call (saves unnecessary requests)
- Empty/whitespace tokens rejected immediately

_Citation: `test_client.py::TestClientEdgeCases` (lines 196-224)_

## Query & Filter Patterns

### Compound Filter Composition

```python
# Empty compound (matches all)
and_filter()  # {"and": []}

# Deep nesting supported
and_filter(
    or_filter(filter_a, filter_b),
    and_filter(filter_c, filter_d)
)
```

_Citation: `test_filter_builders.py::TestFilterEdgeCases` (lines 323-360)_

### Filter Limitations

Filters don't exclude NULL properties - check in Python:

```python
if row["properties"]["Rating"]["number"] is not None:
    # Process non-null values
```

_Citation: `test_integration.py::TestDatabaseQuery::test_query_database_with_filter` (lines 120-135)_

### Pagination Invariants

| Condition          | `has_more` | `next_cursor`      |
| ------------------ | ---------- | ------------------ |
| More results exist | `True`     | Present, non-None  |
| No more results    | `False`    | May be absent/None |

Always check `has_more` before using `next_cursor`.

_Citation: `test_integration.py::TestDatabaseQuery::test_query_database_with_pagination` (lines 137-151)_

## Error Handling

```python
from notion_client import APIResponseError, APIErrorCode

try:
    result = client.pages.create(...)
except APIResponseError as e:
    if e.code == APIErrorCode.ObjectNotFound:
        print("Page/database not found or not shared with integration")
    elif e.code == APIErrorCode.Unauthorized:
        print("Token invalid or expired")
    elif e.code == APIErrorCode.RateLimited:
        print(f"Rate limited. Retry after {e.additional_data.get('retry_after')}s")
    else:
        raise
```

## Installation

```bash
uv pip install notion-client  # v2.6+ required for data_source support
```

Or use PEP 723 inline dependencies (scripts include them).

---

## Troubleshooting

| Issue                        | Cause                            | Solution                                              |
| ---------------------------- | -------------------------------- | ----------------------------------------------------- |
| Object not found             | Page not shared with integration | Share page: ... menu → Connections → Add integration  |
| Unauthorized                 | Token invalid or expired         | Generate new token at notion.so/my-integrations       |
| Rate limited (429)           | Too many requests                | Use `api_call_with_retry()` for automatic handling    |
| Empty results from query     | Filter matches nothing           | Verify filter syntax and property names               |
| Block not found after create | Eventual consistency delay       | Add 0.5s delay after write before read                |
| Invalid property type        | Wrong builder used               | Check property type in database schema                |
| Token format rejected        | Wrong prefix (case-sensitive)    | Token must start with `ntn_` or `secret_` (lowercase) |
| Data source ID not working   | Old API version                  | Upgrade notion-client to latest version               |
