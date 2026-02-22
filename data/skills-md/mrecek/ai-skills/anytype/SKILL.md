---
name: anytype
description: AnyType knowledge base integration via direct REST API. USE WHEN anytype, knowledge base search, create note, create object, anytype spaces, search notes, read object, list tasks, manage tasks OR any request to interact with AnyType data.
---

# AnyType Skill

Direct integration with AnyType's local REST API. No MCP dependency — uses HTTP calls via a TypeScript CLI tool.

## Prerequisites

- AnyType desktop app running (provides REST API on localhost)
- `bun` runtime installed
- API key configured (run Auth workflow if not set up)

## Configuration

Per-machine config is resolved in order:
1. **Environment variables:** `ANYTYPE_API_KEY`, `ANYTYPE_HOST`, `ANYTYPE_PORT`
2. **Config file:** `~/.config/anytype-skill/config.json`
3. **Defaults:** host=localhost, port=31009

**Auto-space:** Commands that require a space ID will auto-detect it when you have a single space. Use `--space <id>` to override or when you have multiple spaces.

## Tool Location

All operations go through a single CLI tool at `Tools/AnyType.ts` relative to this skill's root directory. Construct the full path based on where this SKILL.md was loaded from.

```
bun <skill-root>/Tools/AnyType.ts <command> [options]
```

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| Auth | Set up API key, authenticate, auth status | `Workflows/Auth.md` |
| Search | Search objects, find notes, query AnyType | `Workflows/Search.md` |
| Read | Get object, read note, view object details | `Workflows/Read.md` |
| Tasks | List tasks, create task, mark done, manage tasks | `Workflows/Tasks.md` |

## Tool Reference

### Authentication
| Command | Description |
|---------|-------------|
| `auth challenge` | Start auth flow (4-digit code appears in AnyType) |
| `auth verify <challenge_id> <code>` | Exchange code for API key |
| `auth set-key <key>` | Manually set an API key |
| `auth status` | Check current config and connectivity |

### Querying
| Command | Description |
|---------|-------------|
| `spaces` | List all spaces |
| `search --query <text> [--types <t1,t2>] [--sort <prop>] [--direction asc\|desc] [--space <id>] [--limit N]` | Search objects |
| `get --id <id> [--space <id>]` | Get a specific object |
| `list [--space <id>] [--limit N]` | List objects in a space |
| `tasks [--done] [--all]` | List tasks (default: open/uncompleted) |

### Task Shortcuts
| Command | Description |
|---------|-------------|
| `task-add "name" [--due YYYY-MM-DD] [--body <text>]` | Quick-create a task |
| `done <task_id>` | Mark a task as complete |

### Mutating
| Command | Description |
|---------|-------------|
| `create --type <key> --name <name> [--body <md>] [--properties <json>]` | Create an object |
| `update --id <id> [--name <n>] [--body <md>] [--due DATE] [--properties <json>]` | Update an object |
| `delete --id <id>` | Archive an object |

All commands output JSON to stdout. `--space` is optional for all mutating/querying commands (auto-detected).

## Search Behavior

- Search `query` is **required** and searches object **content**, not just names
- To list all objects of a type, use a space as wildcard: `search --query " " --types <type_key>`
- The `--types` flag filters which object types are returned, not what text is searched
- Type keys (e.g., `page`, `task`, `note`) vary per space — discover them by running a broad search and inspecting the `type.key` field in results
- Objects may contain `anytype://` links in their markdown body that reference other objects by `objectId` and `spaceId` — use these with the `get` command to follow links
- Use `--sort last_modified_date --direction desc` to get most recently modified first
- Use `--space <id>` to scope search to a single space

## Property Format Reference

When using `--properties` with `create` or `update`, match the property format:

| Format | JSON Example |
|--------|-------------|
| checkbox | `{"key": "done", "checkbox": true}` |
| text | `{"key": "description", "text": "Some text"}` |
| select | `{"key": "status", "select": {"name": "In Progress"}}` |
| date | `{"key": "due_date", "date": "2026-03-01T00:00:00Z"}` |

Note: `update` also accepts `--due YYYY-MM-DD` as a shorthand for setting the due_date property.

## API Quirks

- **Unchecked checkboxes are omitted:** When `done` is `false`, the property is absent from the response (not returned as `false`). The `tasks` command handles this automatically.
- **No server-side property filtering:** The API filters by type but not property values. The `tasks` command filters client-side.
- **Delete = archive:** The DELETE endpoint archives objects; they can be restored in AnyType.

## Examples

**List open tasks:**
```
bun Tools/AnyType.ts tasks
```

**Quick-create a task with due date:**
```
bun Tools/AnyType.ts task-add "Review pull request" --due 2026-03-01
```

**Mark task done:**
```
bun Tools/AnyType.ts done <task_id>
```

**Set a due date on existing task:**
```
bun Tools/AnyType.ts update --id <task_id> --due 2026-03-15
```

**Search with sorting:**
```
bun Tools/AnyType.ts search --query "meeting" --sort last_modified_date --direction desc
```

**Read a specific object:**
```
bun Tools/AnyType.ts get --id <object_id>
```

**Create with full control:**
```
bun Tools/AnyType.ts create --type page --name "Meeting Notes" --body "## Agenda\n- Item 1"
```
