---
name: supabase-database
description: Perform database operations (CRUD) on Supabase tables using the REST API. Use for querying, inserting, updating, and deleting data in your Supabase database.
---

# Supabase Database Operations

## Overview

This skill provides tools for working with Supabase database tables through the REST API. Supports SELECT queries with filtering, INSERT, UPDATE, DELETE operations, and calling RPC functions.

## Prerequisites

**Required environment variables:**
```bash
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_KEY="your-anon-or-service-role-key"
```

**Helper script:**
This skill uses the shared Supabase API helper. Make sure to source it:
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"
```

## Common Operations

### SELECT - Query Data

**Basic select all:**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

# Get all rows from a table
supabase_get "/rest/v1/your_table?select=*"
```

**Select specific columns:**
```bash
# Get only id and name columns
supabase_get "/rest/v1/users?select=id,name,email"
```

**Filter results:**
```bash
# Equality filter
supabase_get "/rest/v1/users?select=*&email=eq.user@example.com"

# Greater than
supabase_get "/rest/v1/products?select=*&price=gt.100"

# Less than or equal
supabase_get "/rest/v1/orders?select=*&quantity=lte.10"

# Pattern matching (LIKE)
supabase_get "/rest/v1/users?select=*&name=like.*John*"

# In list
supabase_get "/rest/v1/products?select=*&category=in.(electronics,books)"

# Is null
supabase_get "/rest/v1/users?select=*&deleted_at=is.null"
```

**Order and limit:**
```bash
# Order by column (ascending)
supabase_get "/rest/v1/posts?select=*&order=created_at.asc"

# Order by column (descending)
supabase_get "/rest/v1/posts?select=*&order=created_at.desc"

# Limit results
supabase_get "/rest/v1/posts?select=*&limit=10"

# Pagination (offset)
supabase_get "/rest/v1/posts?select=*&limit=10&offset=20"

# Range pagination
supabase_get "/rest/v1/posts?select=*" -H "Range: 0-9"
```

**Complex queries:**
```bash
# Multiple filters (AND)
supabase_get "/rest/v1/products?select=*&category=eq.electronics&price=gt.100"

# OR filter
supabase_get "/rest/v1/users?select=*&or=(status.eq.active,status.eq.pending)"

# Nested filters
supabase_get "/rest/v1/users?select=*,posts(*)&posts.published=eq.true"
```

### INSERT - Add Data

**Insert single row:**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

supabase_post "/rest/v1/users" '{
  "name": "John Doe",
  "email": "john@example.com",
  "age": 30
}'
```

**Insert multiple rows:**
```bash
supabase_post "/rest/v1/users" '[
  {
    "name": "Alice Smith",
    "email": "alice@example.com"
  },
  {
    "name": "Bob Jones",
    "email": "bob@example.com"
  }
]'
```

**Upsert (insert or update if exists):**
```bash
# Use Prefer: resolution=merge-duplicates header
curl -s -X POST \
    "${SUPABASE_URL}/rest/v1/users" \
    -H "apikey: ${SUPABASE_KEY}" \
    -H "Authorization: Bearer ${SUPABASE_KEY}" \
    -H "Content-Type: application/json" \
    -H "Prefer: resolution=merge-duplicates" \
    -d '{
      "id": 1,
      "name": "Updated Name",
      "email": "updated@example.com"
    }'
```

### UPDATE - Modify Data

**Update rows matching filter:**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

# Update specific row by id
supabase_patch "/rest/v1/users?id=eq.123" '{
  "name": "Updated Name",
  "email": "newemail@example.com"
}'

# Update multiple rows
supabase_patch "/rest/v1/products?category=eq.electronics" '{
  "discount": 10
}'
```

### DELETE - Remove Data

**Delete rows matching filter:**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

# Delete specific row by id
supabase_delete "/rest/v1/users?id=eq.123"

# Delete multiple rows
supabase_delete "/rest/v1/logs?created_at=lt.2023-01-01"
```

### RPC - Call Database Functions

**Execute stored procedures:**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

# Call function without parameters
supabase_post "/rest/v1/rpc/function_name" '{}'

# Call function with parameters
supabase_post "/rest/v1/rpc/calculate_total" '{
  "user_id": 123,
  "start_date": "2023-01-01",
  "end_date": "2023-12-31"
}'
```

## Filter Operators Reference

| Operator | Description | Example |
|----------|-------------|---------|
| `eq` | Equals | `id=eq.123` |
| `neq` | Not equals | `status=neq.deleted` |
| `gt` | Greater than | `age=gt.18` |
| `gte` | Greater than or equal | `price=gte.100` |
| `lt` | Less than | `quantity=lt.10` |
| `lte` | Less than or equal | `score=lte.50` |
| `like` | Pattern match (case-sensitive) | `name=like.*John*` |
| `ilike` | Pattern match (case-insensitive) | `email=ilike.*@gmail.com` |
| `is` | Check for exact value (null, true, false) | `deleted_at=is.null` |
| `in` | In list | `status=in.(active,pending)` |
| `not` | Negate a condition | `status=not.in.(deleted,banned)` |
| `or` | Logical OR | `or=(status.eq.active,status.eq.pending)` |
| `and` | Logical AND | `and=(age.gte.18,age.lte.65)` |

## Response Formatting

**Pretty print JSON (requires jq):**
```bash
supabase_get "/rest/v1/users?select=*" | jq '.'
```

**Extract specific field:**
```bash
# Get just the names
supabase_get "/rest/v1/users?select=name" | jq -r '.[].name'
```

**Count results:**
```bash
# Add Prefer: count=exact header for total count
curl -s -X GET \
    "${SUPABASE_URL}/rest/v1/users?select=*" \
    -H "apikey: ${SUPABASE_KEY}" \
    -H "Authorization: Bearer ${SUPABASE_KEY}" \
    -H "Prefer: count=exact" \
    -I | grep -i content-range
```

## Common Patterns

### Check if record exists
```bash
result=$(supabase_get "/rest/v1/users?select=id&email=eq.test@example.com")
if [[ "$result" == "[]" ]]; then
    echo "User does not exist"
else
    echo "User exists"
fi
```

### Create if not exists
```bash
# Check first
existing=$(supabase_get "/rest/v1/users?select=id&email=eq.test@example.com")

if [[ "$existing" == "[]" ]]; then
    # Create new user
    supabase_post "/rest/v1/users" '{
        "email": "test@example.com",
        "name": "Test User"
    }'
    echo "User created"
else
    echo "User already exists"
fi
```

### Batch operations
```bash
# Process multiple records
ids=(123 456 789)

for id in "${ids[@]}"; do
    supabase_patch "/rest/v1/users?id=eq.$id" '{
        "updated_at": "'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'"
    }'
done
```

## Error Handling

The helper script automatically handles HTTP errors and displays them. Check return codes:

```bash
if supabase_get "/rest/v1/users?select=*"; then
    echo "Query successful"
else
    echo "Query failed"
    exit 1
fi
```

## Security Notes

- Use **anon key** for client-side operations (respects Row Level Security)
- Use **service role key** for admin operations (bypasses RLS - use carefully)
- Always apply Row Level Security policies in your Supabase dashboard
- Never commit keys to version control

## API Documentation

Full Supabase REST API documentation: https://supabase.com/docs/guides/api
