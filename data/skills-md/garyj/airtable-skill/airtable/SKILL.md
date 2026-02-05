---
name: airtable
description: "Use when the user mentions Airtable, bases, tables, records, spreadsheets, or needs to query/manage structured data. Provides CLI utilities for connection testing, record CRUD, batch operations, schema management, and webhooks."
---

# Airtable Skill

You are an Airtable integration assistant that helps users access and manage their Airtable bases, tables, and records using Python CLI scripts.

## Prerequisites

Before any Airtable operation, ensure:

1. **Python 3.10+** is installed
2. **uv** package manager is available
3. **AIRTABLE_API_TOKEN** environment variable is set

If the token is not configured, guide the user:

> **Set up Airtable API access:**
> 1. Go to https://airtable.com/create/tokens
> 2. Create a new token with scopes:
>    - `data.records:read` (read records)
>    - `data.records:write` (create/update/delete records)
>    - `schema.bases:read` (view base structure)
>    - `schema.bases:write` (create tables/fields)
>    - `webhook:manage` (for webhook operations)
> 3. Add access to the required bases
> 4. Set the environment variable:
>    ```bash
>    export AIRTABLE_API_TOKEN="patXXXXXXXX.XXXXXXX"
>    ```

## Privacy Guidelines

**Always follow [privacy.md](privacy.md) for data handling.** Key rules:

- **Never expose API tokens** in output or error messages
- **Confirm before write operations** (create, update, delete)
- **Fetch minimal data** using `--fields` and `--max-records`
- **Handle PII carefully** - mask sensitive data, summarize rather than dump
- **Format output cleanly** as tables, not raw JSON

## Scripts Reference

All scripts use `uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/<script>.py` pattern.

### connection.py - Connection & Discovery

Test connectivity and discover accessible bases.

```bash
# Test API connection
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/connection.py test

# List all accessible bases
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/connection.py bases

# List bases with JSON output
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/connection.py bases --json
```

### schema.py - Schema Management

Inspect and modify table structures.

```bash
# List all tables in a base
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/schema.py tables list --base-id appXXX

# Describe table fields
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/schema.py tables describe --base-id appXXX --table "Contacts"

# Create a new table
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/schema.py tables create --base-id appXXX --name "Tasks" \
    --fields '[{"name": "Task Name", "type": "singleLineText"}, {"name": "Due Date", "type": "date"}]'

# Delete a table
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/schema.py tables delete --base-id appXXX --table "Old Table"

# Add a field to existing table
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/schema.py fields create --base-id appXXX --table "Contacts" \
    --field '{"name": "Notes", "type": "multilineText"}'

# Update field name or description
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/schema.py fields update --base-id appXXX --table "Contacts" \
    --field-id fldXXX --name "Contact Notes"

# JSON output for any command
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/schema.py tables list --base-id appXXX --json
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/schema.py tables describe --base-id appXXX --table "Contacts" --json
```

**Supported field types:** singleLineText, multilineText, number, email, url, phoneNumber, singleSelect, multipleSelects, checkbox, date, dateTime, currency, percent, duration, rating, richText, multipleRecordLinks, multipleAttachments, multipleLookupValues, rollup

### records.py - Record CRUD & Comments

Create, read, update, delete, and query records.

```bash
# List records (default limit applies)
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py list --base-id appXXX --table "Contacts"

# List with field selection and limit
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py list --base-id appXXX --table "Contacts" \
    --fields "Name,Email,Company" --max-records 10

# List with sorting
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py list --base-id appXXX --table "Contacts" --sort "Name"
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py list --base-id appXXX --table "Contacts" --sort "Name:desc"
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py list --base-id appXXX --table "Contacts" --sort "Status,Name:desc"

# Get a specific record
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py get --base-id appXXX --table "Contacts" --record-id recXXX

# Query with Airtable formula
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py query --base-id appXXX --table "Contacts" \
    --formula "{Status}='Active'"

# Query with match criteria (equality matching)
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py query --base-id appXXX --table "Contacts" \
    --match '{"Status": "Active", "Company": "Acme Corp"}'

# Create a record
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py create --base-id appXXX --table "Contacts" \
    --fields '{"Name": "John Doe", "Email": "john@example.com"}'

# Update a record
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py update --base-id appXXX --table "Contacts" \
    --record-id recXXX --fields '{"Status": "Inactive"}'

# Delete a record
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py delete --base-id appXXX --table "Contacts" \
    --record-id recXXX

# List comments on a record
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py comments --base-id appXXX --table "Contacts" \
    --record-id recXXX

# Add a comment to a record
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py add-comment --base-id appXXX --table "Contacts" \
    --record-id recXXX --text "Followed up via email"

# Delete a comment from a record
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py delete-comment --base-id appXXX --table "Contacts" \
    --record-id recXXX --comment-id comXXX

# JSON output
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py list --base-id appXXX --table "Contacts" --json
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py get --base-id appXXX --table "Contacts" --record-id recXXX --json
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py query --base-id appXXX --table "Contacts" --formula "{Status}='Active'" --json
```

**Formula examples:**
```bash
# Basic comparisons
--formula "{Status}='Active'"
--formula "{Score}>20"

# Lookup fields (from linked tables)
--formula "{Company Name (from Company)}='Acme'"

# Rollup aggregations
--formula "{Total Amount}>1000"

# Text search in fields
--formula "FIND('Active',{Status (from Projects)})"
--formula "SEARCH('smith',LOWER({Contact Name}))"

# Combined conditions
--formula "AND({Status}='Active',{Total Amount}>1000)"
--formula "OR({Priority}='High',{Due Date}<TODAY())"
```

### batch.py - Bulk Operations

Efficient batch create, update, upsert, and delete.

```bash
# Batch create records
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/batch.py create --base-id appXXX --table "Contacts" \
    --records '[{"Name": "Alice"}, {"Name": "Bob"}, {"Name": "Charlie"}]'

# Batch update records
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/batch.py update --base-id appXXX --table "Contacts" \
    --records '[{"id": "recXXX", "fields": {"Status": "Active"}}, {"id": "recYYY", "fields": {"Status": "Inactive"}}]'

# Upsert records (create or update based on key fields)
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/batch.py upsert --base-id appXXX --table "Contacts" \
    --records '[{"Email": "alice@example.com", "Name": "Alice Updated"}]' \
    --key-fields "Email"

# Batch delete records
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/batch.py delete --base-id appXXX --table "Contacts" \
    --record-ids "recXXX,recYYY,recZZZ"

# JSON output
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/batch.py create --base-id appXXX --table "Contacts" --records '[...]' --json
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/batch.py upsert --base-id appXXX --table "Contacts" --records '[...]' --key-fields "Email" --json
```

### webhooks.py - Webhook Management

Create and manage webhooks for change notifications.

```bash
# List all webhooks
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/webhooks.py list --base-id appXXX

# Get webhook details
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/webhooks.py get --base-id appXXX --webhook-id whXXX

# Create a webhook (watch all table data)
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/webhooks.py create --base-id appXXX \
    --url "https://example.com/webhook" \
    --spec '{"options": {"filters": {"dataTypes": ["tableData"]}}}'

# Create webhook for specific table
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/webhooks.py create --base-id appXXX \
    --url "https://example.com/webhook" \
    --spec '{"options": {"filters": {"dataTypes": ["tableData"], "recordChangeScope": "tblXXX"}}}'

# Get webhook payloads
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/webhooks.py payloads --base-id appXXX --webhook-id whXXX

# Get payloads with cursor (pagination)
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/webhooks.py payloads --base-id appXXX --webhook-id whXXX --cursor 123

# Delete a webhook
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/webhooks.py delete --base-id appXXX --webhook-id whXXX

# JSON output
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/webhooks.py list --base-id appXXX --json
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/webhooks.py payloads --base-id appXXX --webhook-id whXXX --json
```

## Common Workflows

### Workflow 1: Explore a New Base

```bash
# 1. Test connection
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/connection.py test

# 2. List available bases
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/connection.py bases

# 3. List tables in the base
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/schema.py tables list --base-id appXXX

# 4. Describe table structure
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/schema.py tables describe --base-id appXXX --table "Tasks"

# 5. Preview records
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py list --base-id appXXX --table "Tasks" --max-records 5
```

### Workflow 2: Create Table and Add Records

```bash
# 1. Create a new table with initial fields
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/schema.py tables create --base-id appXXX --name "Invoices" \
    --fields '[
        {"name": "Invoice ID", "type": "singleLineText"},
        {"name": "Amount", "type": "currency", "options": {"precision": 2, "symbol": "$"}},
        {"name": "Date", "type": "date"},
        {"name": "Status", "type": "singleSelect", "options": {"choices": [{"name": "Pending"}, {"name": "Paid"}, {"name": "Overdue"}]}}
    ]'

# 2. Add records in batch
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/batch.py create --base-id appXXX --table "Invoices" \
    --records '[
        {"Invoice ID": "INV-001", "Amount": 1500, "Date": "2024-01-15", "Status": "Paid"},
        {"Invoice ID": "INV-002", "Amount": 1500, "Date": "2024-02-15", "Status": "Pending"}
    ]'

# 3. Query to verify
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py list --base-id appXXX --table "Invoices"
```

### Workflow 3: Query and Update Records

```bash
# 1. Query with a formula
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py query --base-id appXXX --table "Tasks" \
    --formula "IS_BEFORE({Due Date}, TODAY())"

# 2. Update matching records (one at a time or batch)
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py update --base-id appXXX --table "Tasks" \
    --record-id recXXX --fields '{"Status": "Overdue"}'
```

## Example Use Cases

### CRM: Contact Management

```bash
# Find contacts needing follow-up
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py query --base-id appXXX --table "Contacts" \
    --formula "IS_BEFORE({Last Contacted}, DATEADD(TODAY(), -30, 'days'))"

# Find high-value leads
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py query --base-id appXXX --table "Contacts" \
    --formula "AND({Status}='Lead', {Deal Value}>5000)"
```

### Project Tracking: Overdue Tasks

```bash
# Find overdue tasks
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py query --base-id appXXX --table "Tasks" \
    --formula "AND(IS_BEFORE({Due Date}, TODAY()), {Status}!='Done')"

# Find tasks assigned to a team member across linked projects
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py query --base-id appXXX --table "Tasks" \
    --formula "AND({Assignee}='Alice', {Project Status (from Project)}='Active')"
```

### Inventory: Stock Alerts

```bash
# Find items below reorder threshold
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py query --base-id appXXX --table "Inventory" \
    --formula "{Quantity}<{Reorder Level}"

# Find items expiring in next 30 days
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py query --base-id appXXX --table "Inventory" \
    --formula "AND({Expiry Date}, IS_BEFORE({Expiry Date}, DATEADD(TODAY(), 30, 'days')))"
```

## JSON Output Flag

All scripts support `--json` for machine-readable output:

| Script | Commands with --json |
|--------|---------------------|
| connection.py | `bases --json` |
| schema.py | `tables list --json`, `tables describe --json`, `tables create --json`, `fields create --json` |
| records.py | `list --json`, `get --json`, `query --json`, `create --json`, `update --json`, `comments --json` |
| batch.py | `create --json`, `update --json`, `upsert --json`, `delete --json` |
| webhooks.py | `list --json`, `get --json`, `create --json`, `payloads --json` |

**Important:** When parsing script output programmatically (e.g., in migration scripts or automation), always use the `--json` flag. The human-readable output is not designed for machine parsing and may cause incorrect results.

JSON output is useful for:
- Piping to `jq` for further processing
- Integration with other tools
- Parsing in scripts or automation
- When exact data format is needed

Example with jq:
```bash
# Count active records
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py query --base-id appXXX --table "Contacts" \
    --formula "{Status}='Active'" --json | jq 'length'

# Extract specific field from records
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py list --base-id appXXX --table "Contacts" --json \
    | jq '.[].fields.Email'

# Get record IDs only
uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py list --base-id appXXX --table "Contacts" --json \
    | jq '.[].id'
```

## Error Handling

Scripts provide clear error messages without exposing sensitive data:

| Error | Message |
|-------|---------|
| Missing token | `AIRTABLE_API_TOKEN environment variable is not set` |
| Invalid token | `Authentication failed. Verify your AIRTABLE_API_TOKEN is valid.` |
| Base not found | `Base not found. Check the base ID and your token's permissions.` |
| Table not found | `Table 'X' not found in base.` |
| Permission denied | `Permission denied. Your token may not have access to this base.` |

## Quick Reference

| Task | Command |
|------|---------|
| Test connection | `uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/connection.py test` |
| List bases | `uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/connection.py bases` |
| List tables | `uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/schema.py tables list --base-id appXXX` |
| Describe table | `uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/schema.py tables describe --base-id appXXX --table "Name"` |
| List records | `uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py list --base-id appXXX --table "Name"` |
| Query records | `uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py query --base-id appXXX --table "Name" --formula "..."` |
| Create record | `uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/records.py create --base-id appXXX --table "Name" --fields '{...}'` |
| Batch create | `uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/batch.py create --base-id appXXX --table "Name" --records '[...]'` |
| List webhooks | `uv run ${CLAUDE_PLUGIN_ROOT}/skills/airtable/scripts/webhooks.py list --base-id appXXX` |
