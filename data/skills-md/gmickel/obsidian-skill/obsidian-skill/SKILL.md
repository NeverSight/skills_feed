---
name: obsidian-skill
description: >-
  Controls Obsidian vaults via the official CLI (1.12+). Reads, creates, appends to,
  and searches notes. Manages daily notes, tasks, tags, properties, templates,
  bookmarks, and plugins. Analyzes knowledge graph structure including backlinks,
  orphans, and unresolved links. Triggers on Obsidian, vault, notes, daily notes,
  knowledge base, PKM, second brain, zettelkasten, backlinks, or note-taking tasks.
license: MIT
compatibility: Requires Obsidian 1.12+ with CLI enabled via Settings. macOS, Linux, or Windows.
metadata:
  author: gmickel
  version: "1.0.0"
---

# Obsidian CLI

Controls the running Obsidian app via IPC. First invocation launches Obsidian if not running.

## Prerequisites

1. Install Obsidian 1.12+
2. Enable CLI: **Settings → General → Command line interface** → follow registration prompt
3. Restart terminal (registration adds `obsidian` to PATH automatically)

Platform-specific PATH details:
- **macOS**: appends `/Applications/Obsidian.app/Contents/MacOS` to `~/.zprofile`
- **Linux**: symlink at `/usr/local/bin/obsidian` (fallback `~/.local/bin/obsidian`)
- **Windows**: requires `Obsidian.com` redirector from Discord `#insider-desktop-release`

## Syntax

```
obsidian <command> [vault=<name>] [file=<name>] [path=<path>] [flags] [--copy]
```

| Pattern | Behavior |
|---------|----------|
| `vault=<name>` | Target vault by name; defaults to cwd vault or active vault |
| `file=<name>` | Wikilink-style resolution (no path/extension needed) |
| `path=<path>` | Exact vault-relative path, e.g. `path="Folder/Note.md"` |
| `total` | Return count instead of list |
| `format=json\|text\|csv\|tsv\|md` | Output format (varies per command) |
| `--copy` | Copy any command's output to clipboard |
| `\n` / `\t` | Newline / tab in content strings |
| No file/path | Defaults to active file in Obsidian |
| Bare `obsidian` | Opens interactive TUI with autocomplete + `Ctrl+R` history |

## Quick start

These five operations cover most agent tasks. For complete command reference, see the domain-specific guides below.

### Read a note

```bash
obsidian read file="Meeting Notes"
obsidian read path="Projects/Roadmap.md"
obsidian read                              # active file
```

### Create a note

```bash
obsidian create name="New Note" content="# Title\n\nBody"
obsidian create name="From Template" template="Meeting Notes" silent
```

### Append / prepend

```bash
obsidian append file="Journal" content="- New entry"
obsidian prepend file="Ideas" content="## Latest idea"
obsidian daily:append content="- 2pm: Call with team" silent
```

### Search

```bash
obsidian search query="project deadline"
obsidian search query="API" limit=10 format=json
obsidian search query="fix" matches         # include context
```

### Tasks

```bash
obsidian tasks all todo                     # vault-wide incomplete
obsidian tasks daily                        # today's daily note
obsidian task file="Todo" line=8 toggle     # toggle completion
```

## Reference guides

Load these on demand based on the task:

| Task | Reference |
|------|-----------|
| Read, create, edit, move, delete notes; outline; word count; unique notes | [references/note-operations.md](references/note-operations.md) |
| Search, tags, properties, backlinks, orphans, unresolved links, aliases | [references/search-metadata.md](references/search-metadata.md) |
| Daily notes, tasks, templates | [references/daily-tasks-templates.md](references/daily-tasks-templates.md) |
| Vault info, files/folders, bookmarks, plugins, workspaces, themes, sync, publish, bases, dev tools | [references/vault-management.md](references/vault-management.md) |
