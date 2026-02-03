---
name: nocodb
description: Access and manage NocoDB databases via v3 REST API. Use for managing workspaces, bases, tables, fields, views, records, and more. Supports filtering, sorting, pagination, linked records, attachments, and team management.
---

# NocoDB v3 CLI

Feature-complete CLI for NocoDB v3 API.

## Setup

```bash
export NOCODB_TOKEN="your-api-token"
export NOCODB_URL="https://app.nocodb.com"  # optional, this is default
export NOCODB_VERBOSE=1                      # optional, shows resolved IDs
```

Get your API token: NocoDB → Team & Settings → API Tokens → Add New Token.

## Argument Order

Commands follow a hierarchical pattern. Arguments are always in this order:

```
WORKSPACE → BASE → TABLE → VIEW/FIELD → RECORD
```

You can use **names** (human-readable) or **IDs** (faster, from NocoDB).

**ID Prefixes:** `w`=workspace, `p`=base, `m`=table, `c`=column, `vw`=view

Examples:
- Name: `nc record:list MyBase Users`
- ID: `nc record:list pdef5678uvw mghi9012rst`

Set `NOCODB_VERBOSE=1` to see resolved IDs:
```bash
NOCODB_VERBOSE=1 nc field:list MyBase Users
# → base: MyBase → pdef5678uvw
# → table: Users → mghi9012rst
```

## Quick Reference

```bash
nc workspace:list                                   # → wabc1234xyz
nc base:list wabc1234xyz                            # → pdef5678uvw
nc table:list pdef5678uvw                           # → mghi9012rst
nc field:list pdef5678uvw mghi9012rst               # → cjkl3456opq
nc view:list pdef5678uvw mghi9012rst                # → vwmno7890abc
nc record:list pdef5678uvw mghi9012rst
nc record:get pdef5678uvw mghi9012rst 31
nc filter:list pdef5678uvw mghi9012rst vwmno7890abc
nc where:help
```

## Commands

### Workspaces

```bash
nc workspace:list                         # → wabc1234xyz
nc workspace:get wabc1234xyz
nc workspace:create '{"title":"New Workspace"}'
nc workspace:update wabc1234xyz '{"title":"Renamed"}'
nc workspace:delete wabc1234xyz
nc workspace:members wabc1234xyz
```

### Bases

```bash
nc base:list wabc1234xyz                  # → pdef5678uvw
nc base:get pdef5678uvw
nc base:create wabc1234xyz '{"title":"New Base"}'
nc base:update pdef5678uvw '{"title":"Renamed"}'
nc base:delete pdef5678uvw
```

### Tables

```bash
nc table:list pdef5678uvw                 # → mghi9012rst
nc table:get pdef5678uvw mghi9012rst
nc table:create pdef5678uvw '{"title":"NewTable"}'
nc table:update pdef5678uvw mghi9012rst '{"title":"Customers"}'
nc table:delete pdef5678uvw mghi9012rst
```

### Fields

```bash
nc field:list pdef5678uvw mghi9012rst     # → cjkl3456opq
nc field:get pdef5678uvw mghi9012rst cjkl3456opq
nc field:create pdef5678uvw mghi9012rst '{"title":"Phone","type":"PhoneNumber"}'
nc field:update pdef5678uvw mghi9012rst cjkl3456opq '{"title":"Mobile"}'
nc field:delete pdef5678uvw mghi9012rst cjkl3456opq
```

Field types: SingleLineText, LongText, Number, Decimal, Currency, Percent, Email, URL, PhoneNumber, Date, DateTime, Time, SingleSelect, MultiSelect, Checkbox, Rating, Attachment, Links, User, JSON, etc.

### Views

```bash
nc view:list pdef5678uvw mghi9012rst      # → vwmno7890abc
nc view:get pdef5678uvw mghi9012rst vwmno7890abc
nc view:create pdef5678uvw mghi9012rst '{"title":"Active Users","type":"grid"}'
nc view:update pdef5678uvw mghi9012rst vwmno7890abc '{"title":"Renamed"}'
nc view:delete pdef5678uvw mghi9012rst vwmno7890abc
```

View types: grid, gallery, kanban, calendar

### Records

```bash
nc record:list pdef5678uvw mghi9012rst                # page 1, 25 records
nc record:list pdef5678uvw mghi9012rst 2 50           # page 2, 50 records
nc record:list pdef5678uvw mghi9012rst 1 25 "(status,eq,active)"
nc record:list pdef5678uvw mghi9012rst 1 25 "" '[{"field":"cjkl3456opq","direction":"desc"}]'

nc record:get pdef5678uvw mghi9012rst 31
nc record:get pdef5678uvw mghi9012rst 31 "name,email"

nc record:create pdef5678uvw mghi9012rst '{"fields":{"name":"Alice"}}'
nc record:update pdef5678uvw mghi9012rst 31 '{"status":"active"}'
nc record:update-many pdef5678uvw mghi9012rst '[{"id":31,"fields":{"status":"done"}}]'

nc record:delete pdef5678uvw mghi9012rst 31
nc record:delete pdef5678uvw mghi9012rst '[31,32]'

nc record:count pdef5678uvw mghi9012rst
nc record:count pdef5678uvw mghi9012rst "(status,eq,active)"
```

### Linked Records

```bash
nc link:list pdef5678uvw mghi9012rst cjkl3456opq 31
nc link:add pdef5678uvw mghi9012rst cjkl3456opq 31 '[{"id":42}]'
nc link:remove pdef5678uvw mghi9012rst cjkl3456opq 31 '[{"id":42}]'
```

### Filters & Sorts (View-level)

```bash
nc filter:list pdef5678uvw mghi9012rst vwmno7890abc
nc filter:create pdef5678uvw mghi9012rst vwmno7890abc '{"field_id":"cjkl3456opq","operator":"eq","value":"active"}'
nc sort:list pdef5678uvw mghi9012rst vwmno7890abc
nc sort:create pdef5678uvw mghi9012rst vwmno7890abc '{"field_id":"cjkl3456opq","direction":"desc"}'
```

### Attachments

```bash
nc attachment:upload pdef5678uvw mghi9012rst 31 cjkl3456opq ./report.pdf
```

### Scripts

```bash
nc script:list pdef5678uvw
nc script:create pdef5678uvw '{"title":"My Script"}'
```

### Teams

```bash
nc team:list wabc1234xyz
nc team:create wabc1234xyz '{"title":"Engineering"}'
```

### API Tokens

```bash
nc token:list
nc token:create '{"title":"CI Token"}'
nc token:delete tkn1a2b3c4d5e6f7g
```

## Where Filter Syntax

Run `nc where:help` for full documentation.

### Basic Syntax

```
(field,operator,value)
(field,operator)                    # for null/blank/checked operators
(field,operator,sub_op)             # for date operators
(field,operator,sub_op,value)       # for date with value
```

### Common Operators

| Operator | Description | Example |
|----------|-------------|---------|
| eq | Equal | `(name,eq,John)` |
| neq | Not equal | `(status,neq,archived)` |
| like | Contains (% wildcard) | `(name,like,%john%)` |
| in | In list | `(status,in,active,pending)` |
| gt, lt, gte, lte | Numeric comparison | `(price,gt,100)` |
| blank, notblank | Null or empty | `(notes,blank)` |
| checked, notchecked | Boolean | `(is_active,checked)` |

### Date Operators

```bash
(created_at,eq,today)
(created_at,isWithin,pastWeek)
(created_at,isWithin,pastNumberOfDays,14)
(due_date,lt,today)                          # overdue
(event_date,eq,exactDate,2024-06-15)
```

### Combining Filters

**IMPORTANT:** Use `~and`, `~or`, `~not` (with tilde prefix)

```bash
(name,eq,John)~and(age,gte,18)
(status,eq,active)~or(status,eq,pending)
~not(is_deleted,checked)
(status,in,active,pending)~and(country,eq,USA)
```

### Complex Examples

```bash
# Active users created this month
"(status,eq,active)~and(created_at,isWithin,pastMonth)"

# Overdue high-priority tasks
"(due_date,lt,today)~and(priority,eq,high)~and(completed,notchecked)"

# Orders $100-$500 in pending/processing
"(amount,gte,100)~and(amount,lte,500)~and(status,in,pending,processing)"
```
