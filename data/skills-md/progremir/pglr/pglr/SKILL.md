---
name: pglr
description: Secure PostgreSQL CLI for AI agents. Query databases, list tables, describe schemas without handling credentials. Use when tasks involve database queries, data exploration, or schema inspection.
license: MIT
compatibility: Requires pglr CLI installed globally (npm install -g pglr). Human must configure connection first.
metadata:
  author: progremir
  version: "1.0.0"
allowed-tools: Bash(pglr:*)
---

# pglr - PostgreSQL CLI for AI Agents

You have access to `pglr`, a secure PostgreSQL CLI. Use it to query databases without needing connection credentials.

## Prerequisites

A human must first configure a connection:
```bash
pglr connect postgres://user:pass@host/database
```

If you get "No connection configured", ask the user to run the connect command.

## Commands

### Query the database
```bash
pglr query "SELECT * FROM users WHERE active = true"
```

With parameters (prevents SQL injection):
```bash
pglr query "SELECT * FROM users WHERE id = $1" --params '[123]'
```

### List all tables
```bash
pglr tables
```

### Describe a table's structure
```bash
pglr describe users
pglr describe myschema.orders
```

### Get full schema overview
```bash
pglr schema
```

## Output Format

All commands return JSON:
```json
{
  "success": true,
  "rowCount": 5,
  "rows": [{"id": 1, "name": "Alice"}, ...],
  "executionTimeMs": 12,
  "truncated": false
}
```

On error:
```json
{
  "success": false,
  "error": "Table does not exist"
}
```

## Constraints

- **Read-only by default**: INSERT, UPDATE, DELETE, DROP are blocked
- **Row limit**: Max 1000 rows returned (use LIMIT for smaller results)
- **No credentials access**: You cannot see or modify connection details

## Write Operations

If the user explicitly requests data modification:
```bash
pglr query "INSERT INTO logs (message) VALUES ($1)" --params '["test"]' --allow-writes
```

Only use `--allow-writes` when the user explicitly asks to modify data.

## Best Practices

1. **Always check table structure first**:
   ```bash
   pglr describe users
   ```

2. **Use parameters for user input**:
   ```bash
   # Good - parameterized
   pglr query "SELECT * FROM users WHERE email = $1" --params '["user@example.com"]'

   # Bad - string interpolation (SQL injection risk)
   pglr query "SELECT * FROM users WHERE email = 'user@example.com'"
   ```

3. **Limit results when exploring**:
   ```bash
   pglr query "SELECT * FROM large_table LIMIT 10"
   ```

4. **Use schema command to understand the database**:
   ```bash
   pglr schema
   ```

## Multiple Connections

If multiple databases are configured:
```bash
# List available connections
pglr connections

# Query specific connection
pglr query "SELECT 1" --connection prod
pglr tables --connection staging
```

## Example Workflow

```bash
# 1. Understand the database structure
pglr schema

# 2. Explore a specific table
pglr describe orders

# 3. Query data
pglr query "SELECT id, status, created_at FROM orders WHERE status = $1 ORDER BY created_at DESC LIMIT 20" --params '["pending"]'
```
