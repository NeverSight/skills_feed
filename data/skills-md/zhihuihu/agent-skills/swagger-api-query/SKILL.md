---
name: swagger-api-query
description: Query and analyze large Swagger/OpenAPI JSON documents on-demand to extract endpoint details and schemas without loading the entire spec. Use for API discovery, searching by tag/keyword, understanding request/response structures, and tracing data models. Invoke when user asks to "find an endpoint", "search for login/upload/user APIs", or "explain a schema". Use --spec to specify document path if not in current directory, and --format json for structured output.
---

# Swagger API Query Assistant

Use `scripts/swagger_query.py` to index and query OpenAPI/Swagger JSON documents on-demand.

## Execution Principles

1. **Narrow down first**: Prioritize `list-tags`, `search`, or `tag` commands
2. **Then get details**: Only call `detail` for target endpoints
3. **Then view models**: Only call `schema` when you need field definitions
4. **Default text output**: Use `--format json` only when downstream programs need to consume the data

## Dependencies

- Python 3.6+
- OpenAPI/Swagger JSON document

## Document Path Resolution

The script looks for documents in this order:
1. Explicit `--spec <path>` parameter
2. `api-docs.json` in current directory or parent directories
3. `api-docs.json` in skill directory or parent directories

If not found, the script will show checked paths and suggest using `--spec`.

## Standard Workflow

### 1) Understand modules

```bash
python skills/swagger-api-query/scripts/swagger_query.py list-tags
```

### 2) Locate candidate endpoints

**List all endpoints:**
```bash
python skills/swagger-api-query/scripts/swagger_query.py list-all
```

**Query by tag:**
```bash
python skills/swagger-api-query/scripts/swagger_query.py tag "User Management"
```

**Search by keyword:**
```bash
python skills/swagger-api-query/scripts/swagger_query.py search "user"
```

### 3) View endpoint details

```bash
python skills/swagger-api-query/scripts/swagger_query.py detail "/inter-api/admin/users/{id}/status" put
```

If the path has only one method, you can omit the method parameter.

### 4) View Schema (optional)

```bash
python skills/swagger-api-query/scripts/swagger_query.py schema "UserDTO"
```

## Structured Output

```bash
python skills/swagger-api-query/scripts/swagger_query.py --format json search "login"
python skills/swagger-api-query/scripts/swagger_query.py --spec "D:/my/project/api-docs.json" --format json detail "/api/auth/login" post
```

## Common Tasks

### Find login endpoint
```bash
python skills/swagger-api-query/scripts/swagger_query.py search "login"
python skills/swagger-api-query/scripts/swagger_query.py detail "/api/auth/login" post
```

### List user management endpoints
```bash
python skills/swagger-api-query/scripts/swagger_query.py tag "User Management"
python skills/swagger-api-query/scripts/swagger_query.py detail "/api/users" get
```

## Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| **Global Parameters** | | |
| `--spec <path>` | Specify document path | `--spec "D:/project/api-docs.json"` |
| `--format json` | JSON structured output | `--format json search "user"` |
| **Commands** | | |
| `list-tags` | List all API categories | `python scripts/swagger_query.py list-tags` |
| `list-all` | List all endpoint indexes | `python scripts/swagger_query.py list-all` |
| `tag <tag-name>` | Query endpoints by tag | `python scripts/swagger_query.py tag "User Management"` |
| `search <keyword>` | Search by keyword | `python scripts/swagger_query.py search "user"` |
| `detail <path> [method]` | View endpoint details | `python scripts/swagger_query.py detail "/api/users" get` |
| `schema <schema-name>` | View schema definition | `python scripts/swagger_query.py schema "UserDTO"` |

## Notes

- `detail` requires explicit method (get/post/...) for paths with multiple methods
- Use quotes for paths, tags, or keywords containing spaces
- The script returns clear error messages (file not found, JSON parse failed, path or schema not found)
