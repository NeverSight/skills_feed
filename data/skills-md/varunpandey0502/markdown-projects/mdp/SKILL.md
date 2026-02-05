---
name: mdp
description: Manage file-based projects using markdown. Create, list, update, and delete issues and milestones stored as markdown files with YAML frontmatter. Use when users want to track tasks, manage projects, create issues, update statuses, or work with milestones. Triggers on "create issue", "list issues", "update status", "track task", "project management", "milestone progress".
license: MIT
compatibility: Requires mdp installed via `bun install -g github:varunpandey0502/markdown-projects`.
metadata:
  author: varunpandey0502
  version: "1.0"
allowed-tools: Bash(mdp:*)
---

# mdp — Markdown Project Management

A file-based project management CLI. Projects live in `.mdp/` directories containing markdown files with YAML frontmatter.

## Installation

```bash
bun install -g github:varunpandey0502/markdown-projects
```

See [INSTALL.md](references/INSTALL.md) for details.

## Quick start

```bash
mdp project create -p . --preset software
mdp issue create -p . -t "Fix login bug" --type bug --priority High
mdp issue list -p .
mdp issue update -p . --id ISS-001 -s "In Progress"
```

## Project structure

```
.mdp/
├── settings.json          # Project config (committed)
├── issues/<status>/       # Issue markdown files by status folder
├── milestones/<status>/   # Milestone markdown files by status folder
├── docs/                  # Documentation
└── templates/             # Issue/milestone templates
```

## Configuration

Project config is stored in `.mdp/settings.json` with nested entity-scoped objects:

```json
{
  "issues": { "prefix": "ISS", "statuses": [...], "priorities": [...], "labels": [...], "types": [...] },
  "milestones": { "prefix": "M", "statuses": [...], "priorities": [...], "labels": [...] }
}
```

Issues and milestones have independent statuses, priorities, and labels.

At runtime, `.mdp/settings.json` is the sole source of truth — no merge layers.

At project creation: preset (built-in or custom from `~/.mdp/config.json`) → CLI flag overrides → written to `settings.json`.

Custom presets and default preferences (default preset, output format) are stored in `~/.mdp/config.json`.

## Global options

Every command accepts: `-p <path>` (project path), `-f json|table` (output format), `-q` (quiet), `-V` (verbose).

All output is JSON: `{ "ok": true, "data": {...} }` or `{ "ok": false, "error": {...} }`.

## Commands

### Project management

- `mdp project create -p <path> [--preset <name>] [-F|--force] [--with-templates] [--no-with-templates] [--issue-prefix <prefix>] [--milestone-prefix <prefix>] [--tags <tags>]` — Create a new project (presets: software, marketing, design, product, social-media, generic)
- `mdp project settings -p <path>` — Show project settings
- `mdp project stats -p <path>` — Project statistics
- `mdp project fix -p <path> [--dry-run]` — Fix folder structure to match frontmatter

### Project registry

Manage projects in `~/.mdp/config.json`:

- `mdp project list [--tag <tag>]`
- `mdp project add <path> [--tags <tags>]`
- `mdp project remove <path>`
- `mdp project tag <path> --add <tags> | --remove <tags>`

### Issues

#### Create

```
mdp issue create -p <path> -t "Title" [options]
```

| Option | Description |
|---|---|
| `-t, --title <title>` | Issue title (required) |
| `--type <type>` | Issue type (config-driven) |
| `-s, --status <status>` | Initial status (default: Backlog) |
| `--priority <priority>` | Priority level (default: None) |
| `-l, --labels <labels>` | Comma-separated labels |
| `-a, --assignee <assignee>` | Assignee identifier |
| `-m, --milestone <milestone>` | Milestone ID |
| `-e, --estimate <estimate>` | Effort points (positive integer) |
| `--spent <spent>` | Actual effort spent |
| `--due-date <date>` | Due date (YYYY-MM-DD) |
| `--blocked-by <ids>` | Comma-separated issue IDs |
| `--parent <id>` | Parent issue ID |
| `--related-to <ids>` | Comma-separated issue IDs |
| `--checklist <items>` | Comma-separated checklist items |
| `-d, --description <desc>` | Short description |
| `-c, --content <content>` | Full markdown body (or `-` for stdin) |
| `--template <name>` | Template name from .mdp/templates/ |
| `--dry-run` | Preview without creating |

#### List

```
mdp issue list -p <path> [options]
```

| Option | Description |
|---|---|
| `-s, --status <statuses>` | Comma-separated status filter |
| `--type <types>` | Comma-separated type filter |
| `--priority <priority>` | Priority filter |
| `-l, --labels <labels>` | Comma-separated labels filter |
| `-a, --assignee <assignee>` | Filter by assignee (`none` for unassigned) |
| `-m, --milestone <milestone>` | Filter by milestone ID (`none` for unassigned) |
| `--blocked <bool>` | `true` for blocked only, `false` for unblocked |
| `--parent <id>` | Filter by parent issue ID (`none` for top-level) |
| `--created-after <date>` | Created after date (YYYY-MM-DD) |
| `--created-before <date>` | Created before date (YYYY-MM-DD) |
| `--due-before <date>` | Due before date (YYYY-MM-DD) |
| `--due-after <date>` | Due after date (YYYY-MM-DD) |
| `--sort <field>` | Sort: id, title, status, priority, type, created, updated, estimate, spent, dueDate (default: id) |
| `--order <order>` | Sort order: asc, desc (default: asc) |

#### Get

```
mdp issue get -p <path> --id <id> [--no-include-content]
```

#### Update

```
mdp issue update -p <path> --id <id> [options]
```

| Option | Description |
|---|---|
| `-t, --title <title>` | New title |
| `--type <type>` | New type |
| `-s, --status <status>` | New status |
| `--priority <priority>` | New priority |
| `-a, --assignee <assignee>` | Set assignee (`none` to clear) |
| `-m, --milestone <milestone>` | Set milestone (`none` to clear) |
| `-e, --estimate <estimate>` | Set estimate (`none` to clear) |
| `--spent <spent>` | Set spent (`none` to clear) |
| `--due-date <date>` | Set due date (`none` to clear) |
| `--parent <id>` | Set parent issue (`none` to clear) |
| `-l, --labels <labels>` | Set labels (replaces all) |
| `--add-labels <labels>` | Add labels |
| `--remove-labels <labels>` | Remove labels |
| `--blocked-by <ids>` | Set blockedBy (replaces all) |
| `--add-blocked-by <ids>` | Add to blockedBy (with cycle detection) |
| `--remove-blocked-by <ids>` | Remove from blockedBy |
| `--related-to <ids>` | Set relatedTo (replaces all) |
| `--add-related-to <ids>` | Add to relatedTo |
| `--remove-related-to <ids>` | Remove from relatedTo |
| `--add-checklist <items>` | Add checklist items |
| `--remove-checklist <items>` | Remove checklist items by text |
| `--check <items>` | Check items by text |
| `--uncheck <items>` | Uncheck items by text |
| `-c, --content <content>` | Replace markdown body |
| `--dry-run` | Preview without writing |

#### Delete

```
mdp issue delete -p <path> --id <id> [--dry-run]
```

Cleans up blockedBy, relatedTo, and parent references in other issues.

#### Comment

```
mdp issue comment -p <path> --id <id> -b "message" [--author <name>] [--dry-run]
```

### Milestones

#### Create

```
mdp milestone create -p <path> -t "Title" [options]
```

| Option | Description |
|---|---|
| `-t, --title <title>` | Milestone title (required) |
| `-s, --status <status>` | Initial status (default: Planning) |
| `--priority <priority>` | Priority level (default: None) |
| `-l, --labels <labels>` | Comma-separated labels |
| `--start-date <date>` | Start date (YYYY-MM-DD) |
| `--due-date <date>` | Due date (YYYY-MM-DD) |
| `--checklist <items>` | Comma-separated checklist items |
| `-d, --description <desc>` | Short description |
| `-c, --content <content>` | Full markdown body |
| `--template <name>` | Template name from .mdp/templates/ |
| `--dry-run` | Preview without creating |

#### List

```
mdp milestone list -p <path> [options]
```

| Option | Description |
|---|---|
| `-s, --status <statuses>` | Comma-separated status filter |
| `--priority <priority>` | Priority filter |
| `-l, --labels <labels>` | Comma-separated labels filter |
| `--overdue <bool>` | `true` for overdue only, `false` for not overdue |
| `--sort <field>` | Sort: id, title, status, priority, created, updated, dueDate, completion (default: id) |
| `--order <order>` | Sort order: asc, desc (default: asc) |

#### Get

```
mdp milestone get -p <path> --id <id> [--no-include-content]
```

#### Update

```
mdp milestone update -p <path> --id <id> [options]
```

| Option | Description |
|---|---|
| `-t, --title <title>` | New title |
| `-s, --status <status>` | New status |
| `--priority <priority>` | New priority |
| `--start-date <date>` | Set start date (`none` to clear) |
| `--due-date <date>` | Set due date (`none` to clear) |
| `-l, --labels <labels>` | Set labels (replaces all) |
| `--add-labels <labels>` | Add labels |
| `--remove-labels <labels>` | Remove labels |
| `--add-checklist <items>` | Add checklist items |
| `--remove-checklist <items>` | Remove checklist items by text |
| `--check <items>` | Check items by text |
| `--uncheck <items>` | Uncheck items by text |
| `-c, --content <content>` | Replace markdown body |
| `--dry-run` | Preview without writing |

#### Delete

```
mdp milestone delete -p <path> --id <id> [--dry-run]
```

Clears milestone reference from all assigned issues.

#### Progress

```
mdp milestone progress -p <path> --id <id>
```

Returns completion percentage, issue counts by status, and list of assigned issues.

#### Comment

```
mdp milestone comment -p <path> --id <id> -b "message" [--author <name>] [--dry-run]
```

## Workflow recommendations

1. Start with `mdp project create -p . --preset software` to set up a project
2. Create issues with `mdp issue create` — use `--type` and `--labels` for organization
3. Move issues through statuses with `mdp issue update --id ISS-1 -s "In Progress"`
4. Group work into milestones, then track with `mdp milestone progress`
5. Use `mdp issue list` with filters to find relevant issues

See [WORKFLOWS.md](references/WORKFLOWS.md) for detailed workflow patterns.
