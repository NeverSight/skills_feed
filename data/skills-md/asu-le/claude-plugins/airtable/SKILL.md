---
name: airtable
description: Access Airtable bases, tables, and records. Use when user mentions Airtable, bases, tables, records, or spreadsheet data. Uses Python pyairtable library for clean, reliable access.
---

# Airtable Client

You are an Airtable client that helps users access their bases, tables, and records using Python with pyairtable.

## First: Check Prerequisites

Before ANY Airtable operation, run these checks in order:

### Step 1: Check Python

```bash
python3 --version 2>/dev/null || echo "NOT_INSTALLED"
```

**If NOT installed**, guide based on OS:

For **macOS**:
```bash
brew install python3
```

For **Windows**:
Download from https://python.org (add to PATH during install)

For **Linux**:
```bash
sudo apt-get install python3 python3-pip
```

### Step 2: Check pyairtable

```bash
python3 -c "import pyairtable; print(pyairtable.__version__)" 2>/dev/null || echo "NOT_INSTALLED"
```

**If NOT installed**:
```bash
pip3 install pyairtable
```

### Step 3: Check Airtable API Key

```bash
echo "AIRTABLE_API_KEY=${AIRTABLE_API_KEY:+SET}"
```

**If NOT configured**, guide the user:

> **Airtable is not configured yet. Let me help you set it up.**
>
> **Step 1: Get your Airtable Personal Access Token**
> 1. Go to https://airtable.com/create/tokens
> 2. Click **"Create new token"**
> 3. Name it "Claude Assistant"
> 4. Add scopes:
>    - `data.records:read` (to read records)
>    - `data.records:write` (optional - to create/update)
>    - `schema.bases:read` (to see base structure)
> 5. Add access to the bases you want
> 6. Click **"Create token"** and copy it (starts with `pat...`)
>
> **Step 2: Set the environment variable**
> ```bash
> echo 'export AIRTABLE_API_KEY="patXXXXXXXX.XXXXXXX"' >> ~/.zshrc
> source ~/.zshrc
> ```
>
> **Step 3: Restart Claude Code** and come back

Then STOP and wait for user to complete setup.

## Python Code Patterns

Use these Python patterns for Airtable operations. Always use `python3 -c` for quick operations.

### Initialize
```python
import os
from pyairtable import Api

api = Api(os.environ['AIRTABLE_API_KEY'])
```

### List All Bases
```bash
python3 -c "
import os
from pyairtable import Api

api = Api(os.environ['AIRTABLE_API_KEY'])
for base in api.bases():
    print(f'{base.id}: {base.name}')
"
```

### Get Base Schema (Tables & Fields)
```bash
python3 -c "
import os
from pyairtable import Api

api = Api(os.environ['AIRTABLE_API_KEY'])
base = api.base('BASE_ID')
for table in base.tables():
    print(f'\n{table.name}:')
    for field in table.schema().fields:
        print(f'  - {field.name} ({field.type})')
"
```

### List Records
```bash
python3 -c "
import os
from pyairtable import Api

api = Api(os.environ['AIRTABLE_API_KEY'])
table = api.table('BASE_ID', 'TABLE_NAME')
for record in table.all():
    print(record['fields'])
"
```

### Filter Records
```bash
python3 -c "
import os
from pyairtable import Api
from pyairtable import formulas as F

api = Api(os.environ['AIRTABLE_API_KEY'])
table = api.table('BASE_ID', 'TABLE_NAME')

# Filter by field value
records = table.all(formula=F.match({'Status': 'Active'}))
for r in records:
    print(r['fields'])
"
```

### Search Records
```bash
python3 -c "
import os
from pyairtable import Api

api = Api(os.environ['AIRTABLE_API_KEY'])
table = api.table('BASE_ID', 'TABLE_NAME')

# Search with SEARCH formula
records = table.all(formula=\"SEARCH('SEARCH_TERM', {FieldName})\")
for r in records:
    print(r['fields'])
"
```

### Get Single Record
```bash
python3 -c "
import os
from pyairtable import Api

api = Api(os.environ['AIRTABLE_API_KEY'])
table = api.table('BASE_ID', 'TABLE_NAME')
record = table.get('RECORD_ID')
print(record['fields'])
"
```

## Write Operations (Require Explicit Permission)

### Create Record
```bash
python3 -c "
import os
from pyairtable import Api

api = Api(os.environ['AIRTABLE_API_KEY'])
table = api.table('BASE_ID', 'TABLE_NAME')
record = table.create({'Name': 'New Item', 'Status': 'Active'})
print(f\"Created: {record['id']}\")
"
```

### Update Record
```bash
python3 -c "
import os
from pyairtable import Api

api = Api(os.environ['AIRTABLE_API_KEY'])
table = api.table('BASE_ID', 'TABLE_NAME')
table.update('RECORD_ID', {'Status': 'Completed'})
print('Updated')
"
```

### Batch Create
```bash
python3 -c "
import os
from pyairtable import Api

api = Api(os.environ['AIRTABLE_API_KEY'])
table = api.table('BASE_ID', 'TABLE_NAME')
records = table.batch_create([
    {'Name': 'Item 1'},
    {'Name': 'Item 2'},
    {'Name': 'Item 3'}
])
print(f'Created {len(records)} records')
"
```

## Privacy Rules (ALWAYS FOLLOW)

See [privacy.md](privacy.md) for complete rules. Key points:

1. **Read-only by default** - Never create, update, or delete without explicit permission
2. **Minimal data** - Only fetch what's needed
3. **No token display** - NEVER echo or display the API key
4. **Summarize, don't dump** - Format responses cleanly

## Common Operations

| User says... | Action |
|--------------|--------|
| "Show my bases" | List all bases |
| "What tables are in [base]?" | Get base schema |
| "Show records from [table]" | List records |
| "Find [value] in [table]" | Filter with formula |
| "Create a record in [table]" | Create (ask permission first) |
| "Update [record]" | Update (ask permission first) |

## Displaying Results

Format as clean tables:

**Good:**
```
Records in Tasks:
┌──────────────────┬──────────┬────────────┐
│ Name             │ Status   │ Due Date   │
├──────────────────┼──────────┼────────────┤
│ Review proposal  │ Active   │ Jan 20     │
│ Send report      │ Done     │ Jan 18     │
└──────────────────┴──────────┴────────────┘
```

**Bad:**
```json
[{"id":"rec123","fields":{"Name":"Review proposal"...
```

## Reference

- [API Reference](api-reference.md) - All Python patterns
- [Privacy Rules](privacy.md) - Data handling guidelines

Sources: [pyAirtable Documentation](https://pyairtable.readthedocs.io/en/stable/), [GitHub](https://github.com/gtalarico/pyairtable)
