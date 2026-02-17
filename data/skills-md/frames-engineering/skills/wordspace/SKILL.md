---
name: wordspace
version: 0.0.5
description: CLI for bootstrapping and managing wordspace projects
metadata:
  category: tooling
  triggers: ["wordspace", "wordspace init", "wordspace search", "wordspace add", "add workflow", "search workflow", "browse workflows"]
  requires: { bins: ["node", "npx"] }
---

# Wordspace

Wordspace is a CLI tool that bootstraps project workspaces with workflows — reusable `.prose` programs fetched from GitHub.

## When to activate

Activate this skill when the user:

- Wants to set up a new wordspace project
- Wants to browse, search, or add workflows
- Mentions "wordspace" by name
- Asks about available workflows or how to get new ones

## Commands

### `wordspace init`

Bootstrap a new project in the current directory. Runs three steps:

1. **Workflows** — Fetches available `.prose` workflows from GitHub and presents an interactive picker. The user selects which ones to download. In CI (non-TTY), all workflows are downloaded automatically.
2. **Claude settings** — Creates `.claude/settings.local.json` with base permissions (`curl`, `python3`, `WebFetch`, `WebSearch`).
3. **Directories** — Creates the `output/` directory.

Use `--force` to re-download workflows that already exist locally.

### `wordspace search [query]`

List all available workflows from the remote repository. Optionally filter by a substring query.

```
wordspace search            # list all
wordspace search pulse      # filter by "pulse"
```

### `wordspace add <name> [...]`

Download one or more specific workflows by name. Automatically appends `.prose` if missing.

```
wordspace add x-daily-pulse
wordspace add x-daily-pulse x-weekly-report
wordspace add x-daily-pulse --force    # overwrite existing
```

## Project structure after init

```
project/
├── .claude/
│   └── settings.local.json    # Claude permissions
├── workflows/
│   └── *.prose                # downloaded workflow files
├── output/                    # working directory for outputs
└── skills/
    └── wordspace/
        └── SKILL.md           # this file
```

## Workflow picker (during init)

When running `wordspace init`, the CLI presents a numbered list of available workflows. The user can respond with:

- `all` or press Enter — download everything
- `none` or `0` — skip workflow download
- `1,3,5` — pick specific numbers
- `1-3` — pick a range
- `1,3-5,7` — mix of both

## Installation

```
npx wordspace init
```

Or install globally:

```
npm i -g wordspace
wordspace init
```
