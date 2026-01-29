---
name: things3-manager
description: Manage tasks, projects, areas, headings, and tags in the Things 3 macOS app via a local CLI (list Inbox/Today/Upcoming/Anytime/Someday/Logbook, search, create/update/complete/cancel items, open items in Things). Use when Codex needs to manage Things 3 on macOS.
---

# Things 3 Manager (CLI)

## Quick start
- Ensure Things 3 is installed and opened at least once.
- In Things → Settings → General: enable “Enable Things URLs”.
- Run the CLI (auto-bootstraps `.skills-data/things3-manager/venv` and installs deps on first run):
  - `bash .codex/skills/things3-manager/scripts/things --help`
  - `bash .codex/skills/things3-manager/scripts/things inbox`
  - `bash .codex/skills/things3-manager/scripts/things search "weekly review"`
  - `bash .codex/skills/things3-manager/scripts/things add-todo --title "Book flights" --when today --tag travel --checklist "passport" --checklist "charger"`

## Operating rules (for Codex)
- Prefer read-only commands first (`inbox`, `today`, `search`, `projects`, `areas`, `tags`) to discover UUIDs and current state.
- Before any write command (`add-todo`, `add-project`, `update-todo`, `update-project`), summarize the exact changes and confirm with the user.
- If the user provides a project/area/heading by name, resolve it by listing (`projects`/`areas`/`headings`) before writing.

## Local data and env
- Store all mutable state under <project_root>/.skills-data/<skill-name>/.
- Keep config and registries in .skills-data/<skill-name>/ (for example: config.json, <feature>.json).
- Use .skills-data/<skill-name>/.env for SKILL_ROOT, SKILL_DATA_DIR, and any per-skill env keys.
- Install local tools into .skills-data/<skill-name>/bin and prepend it to PATH when needed.
- Install dependencies under .skills-data/<skill-name>/venv:
  - Python: .skills-data/<skill-name>/venv/python
  - Node: .skills-data/<skill-name>/venv/node_modules
  - Go: .skills-data/<skill-name>/venv/go (modcache, gocache)
  - PHP: .skills-data/<skill-name>/venv/php (cache, vendor)
- Write logs/cache/tmp under .skills-data/<skill-name>/logs, .skills-data/<skill-name>/cache, .skills-data/<skill-name>/tmp.
- Keep automation in <skill-root>/scripts and read SKILL_DATA_DIR (default to <project_root>/.skills-data/<skill-name>/).
- Do not write outside <skill-root> and <project_root>/.skills-data/<skill-name>/ unless the user requests it.

## Commands (CLI)
- Lists:
  - `inbox`, `today`, `upcoming`, `anytime`, `someday`, `logbook`, `trash`, `recent`
- Browsing:
  - `projects`, `areas`, `tags`, `headings`, `todos`, `tagged-items`
- Search:
  - `search`, `search-advanced`
- Writes (via Things URL scheme):
  - `add-todo`, `add-project`, `update-todo`, `update-project`
- Open in Things:
  - `show`, `search-items`

## Attribution
- CLI implementation is based on `things_server.py`, `url_scheme.py`, and `formatters.py` from `https://github.com/hald/things-mcp`.
