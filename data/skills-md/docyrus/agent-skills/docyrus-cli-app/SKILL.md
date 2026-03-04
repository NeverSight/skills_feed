---
name: docyrus-cli-app
description: Use the Docyrus CLI (`docyrus`) to interact with the Docyrus platform from the terminal. Use when the user asks to authenticate, list apps, query/manage data records (`ds`), manage dev app data source schema objects (`studio`), send API requests, switch environments/tenants/accounts, or discover OpenAPI specs via the `docyrus` command-line tool. Triggers on tasks involving docyrus CLI commands, terminal-based Docyrus operations, `docyrus ds list`, `docyrus studio`, `docyrus discover`, `docyrus auth`, `docyrus env`, or shell-based Docyrus workflows.
---

# Docyrus CLI

Guide for using the `docyrus` CLI to interact with the Docyrus platform from the terminal.

## Command Overview

| Command | Description |
|---------|-------------|
| `docyrus auth login` | Authenticate via OAuth2 device flow |
| `docyrus auth who` | Show current user |
| `docyrus auth tenants list` | List available tenants |
| `docyrus auth tenants use` | Switch active tenant |
| `docyrus env list` / `env use` | Manage environments |
| `docyrus apps list` | List tenant apps |
| `docyrus ds get` | Get data source metadata |
| `docyrus ds list` | Query records with filters, sorting, pagination |
| `docyrus ds create` | Create a record |
| `docyrus ds update` | Update a record |
| `docyrus ds delete` | Delete a record |
| `docyrus studio ...` | CRUD for dev app data sources, fields, and enums |
| `docyrus curl` | Send arbitrary API requests |
| `docyrus discover api` | Download tenant OpenAPI spec |
| `docyrus discover namespaces` | List API namespaces from OpenAPI spec |
| `docyrus discover path` | List endpoints matching a path prefix |
| `docyrus discover endpoint` | Return full endpoint object by path/method |
| `docyrus discover entity` | Return full entity schema by name |
| `docyrus discover search` | Search endpoint paths and entity names |

**See [references/cli-manifest.md](references/cli-manifest.md) for complete command reference with all flags and arguments.**

## Common Workflows

### First-Time Setup

1. Authenticate: `docyrus auth login`
2. Select tenant: `docyrus auth tenants use --tenantId <id>`
3. Verify: `docyrus auth who`

### Discover API & Entities

Download the tenant OpenAPI spec and explore available endpoints and entities:

```bash
# Download/refresh tenant OpenAPI spec
docyrus discover api --json

# List all API namespaces (e.g. /v1/users, /v1/teams)
docyrus discover namespaces --json

# List endpoints under a path prefix (with or without /v1)
docyrus discover path /v1/users --json
docyrus discover path /teams --json

# Get full endpoint details (defaults to GET; use [METHOD] prefix for others)
docyrus discover endpoint /v1/users/me --json
docyrus discover endpoint [PUT]/v1/users/me/photo --json

# Get full entity/schema definition
docyrus discover entity UserEntity --json

# Search endpoints and entities by comma-separated terms
docyrus discover search users,UserEntity --json
```

### Discover Data Sources

1. List apps: `docyrus apps list`
2. Get metadata: `docyrus ds get <appSlug> <dataSourceSlug>`

### Query Records (`ds list`)

Basic listing:

```bash
docyrus ds list crm contacts --columns "name, email, phone" --limit 20
```

With filters (JSON object):

```bash
docyrus ds list crm contacts \
  --columns "name, email" \
  --filters '{"rules":[{"field":"status","operator":"=","value":"active"}]}'
```

With relation expansion:

```bash
docyrus ds list crm contacts \
  --columns "name, ...related_account(account_name, account_phone)"
```

Date shortcut filter:

```bash
docyrus ds list crm tasks --filters '{"rules":[{"field":"created_on","operator":"this_month"}]}'
```

**See [references/list-query-examples.md](references/list-query-examples.md) for comprehensive filter, sort, pagination, and combined query examples.**

### CRUD Operations

Create:

```bash
docyrus ds create crm contacts --data '{"name":"Jane Doe","email":"jane@example.com"}'
```

Update:

```bash
docyrus ds update crm contacts <recordId> --data '{"phone":"+1234567890"}'
```

Delete:

```bash
docyrus ds delete crm contacts <recordId>
```

### Studio Schema CRUD (`studio`)

Use `studio` for developer-facing data source schema operations under `/v1/dev/apps/:app_id/data-sources` (data sources, fields, enums).

Examples:

```bash
# Data sources
docyrus studio list-data-sources --appSlug crm --expand fields --json
docyrus studio get-data-source --appSlug crm --dataSourceSlug contacts --json
docyrus studio create-data-source --appSlug crm --title "Contacts" --name "contacts" --slug "contacts" --json
docyrus studio update-data-source --appId <appId> --dataSourceId <dataSourceId> --data '{"title":"Contacts v2"}' --json
docyrus studio delete-data-source --appId <appId> --dataSourceSlug contacts --json
docyrus studio bulk-create-data-sources --appId <appId> --from-file ./data-sources.json --json

# Fields
docyrus studio list-fields --appSlug crm --dataSourceSlug contacts --json
docyrus studio get-field --appSlug crm --dataSourceSlug contacts --fieldSlug email --json
docyrus studio create-field --appId <appId> --dataSourceId <dataSourceId> --name "Email" --slug "email" --type "text" --json
docyrus studio update-field --appId <appId> --dataSourceId <dataSourceId> --fieldId <fieldId> --data '{"name":"Primary Email"}' --json
docyrus studio delete-field --appId <appId> --dataSourceId <dataSourceId> --fieldSlug email --json
docyrus studio create-fields-batch --appId <appId> --dataSourceId <dataSourceId> --data '[{"name":"Status","slug":"status","type":"text"}]' --json
docyrus studio update-fields-batch --appId <appId> --dataSourceId <dataSourceId> --from-file ./fields-update.json --json
docyrus studio delete-fields-batch --appId <appId> --dataSourceId <dataSourceId> --data '["field-1","field-2"]' --json

# Enums
docyrus studio list-enums --appId <appId> --dataSourceId <dataSourceId> --fieldId <fieldId> --json
docyrus studio create-enums --appId <appId> --dataSourceId <dataSourceId> --fieldId <fieldId> --data '[{"name":"Open","sortOrder":1}]' --json
docyrus studio update-enums --appId <appId> --dataSourceId <dataSourceId> --fieldId <fieldId> --from-file ./enums-update.json --json
docyrus studio delete-enums --appId <appId> --dataSourceId <dataSourceId> --fieldId <fieldId> --data '["enum-1","enum-2"]' --json
```

### Batch & File Input (`ds create` / `ds update`)

Both commands support `--from-file` with `.json` or `.csv` files.

- Object payload -> single item endpoints (`/items` or `/items/:recordId`)
- Array payload -> bulk endpoints (`/items/bulk`)
- Batch size limit: 50 items
- Batch update requires `id` in every item and must not include positional `recordId`

Examples:

```bash
# Bulk create from inline JSON array
docyrus ds create crm contacts --data '[{"name":"A"},{"name":"B"}]' --json

# Bulk update from inline JSON array (id required in each item)
docyrus ds update crm contacts --data '[{"id":"1","phone":"+111"},{"id":"2","phone":"+222"}]' --json

# Bulk create from CSV file
docyrus ds create crm contacts --from-file ./contacts-create.csv --json

# Single update from JSON file
docyrus ds update crm contacts <recordId> --from-file ./contact-update.json --json
```

### Arbitrary API Calls

```bash
docyrus curl /v1/users/me
docyrus curl /v1/dev/apps -X GET --format json
docyrus curl /v1/some/endpoint -X POST -d '{"key":"value"}'
```

## Key Rules

- Arguments use `appSlug` and `dataSourceSlug` (not IDs) — run `docyrus apps list` and `docyrus ds get` to discover slugs
- `ds create` / `ds update` accept `--data` (JSON) or `--from-file` (`.json`/`.csv`), but not both at once
- If payload is an array, CLI uses bulk endpoints with max 50 items
- For bulk update, each item must include `id` and no positional `<recordId>` should be provided
- `--filters` accepts a JSON string following the filter group structure: `{"combinator":"and","rules":[...]}`
- Filter operators include: `=`, `!=`, `>`, `>=`, `<`, `<=`, `like`, `not like`, `in`, `not in`, `empty`, `not empty`, `between`, `today`, `this_month`, `this_quarter`, `last_30_days`, `active_user`
- Filter on related fields using `rel_<relation_slug>/<field_slug>` syntax
- `--columns` uses comma-separated field slugs with support for relation expansion `()`, spread `...`, aliasing `:`, and functions `@`
- `--format` controls output: `toon` (default table), `json`, `yaml`, `md`, `jsonl`
- `--verbose` wraps response in full envelope with metadata
- Studio selectors are exclusive pairs: provide exactly one of `--appId|--appSlug`, `--dataSourceId|--dataSourceSlug`, and `--fieldId|--fieldSlug` (as required by command)
- Studio write commands accept `--data` (JSON string) or `--from-file` (JSON only), and merge with flags where flags override overlapping keys
- Studio batch commands auto-wrap root arrays to required DTO keys: `dataSources`, `fields`, `fieldIds`, `enums`, `enumIds`

## References

- **[CLI Manifest](references/cli-manifest.md)** — Complete command reference with all flags, arguments, and options.
- **[List Query Examples](references/list-query-examples.md)** — Practical `ds list` examples covering columns, filters, sorting, pagination, and combined queries.
