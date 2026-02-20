---
name: obsidian-cli
description: Control Obsidian from the terminal via the Obsidian CLI. Read, create, search, and manage notes, tasks, properties, and more. Includes vault structure commands (orphans, dead ends, backlinks, unresolved wikilinks), Bases, and plugin development.
metadata:
  author: nweii
  version: "1.2.0"
---

# Obsidian CLI

Run `obsidian <command>` to control Obsidian from the terminal. The app must be running for most commands; the first command will launch Obsidian if not open.

Run `obsidian help` or `obsidian help <command>` for the canonical, always-up-to-date command reference. This skill documents common patterns and non-obvious behaviors.

## Targeting vaults and files

- **Vault**: `vault=<name>` as first parameter. Default: cwd if it's a vault folder, else the active vault.
- **File**: `file=<name>` resolves like a wikilink (name only, no path or extension needed). `path=<path>` for exact path from vault root.
- **TUI**: Run `obsidian` with no args for interactive mode; omit the `obsidian` prefix inside.

## Parameters and flags

- **Parameters**: `param=value`. Quote values with spaces: `content="Hello world"`.
- **Flags**: Boolean, no value: `silent`, `overwrite`, `newtab`.
- **Multiline content**: Use `\n` for newlines, `\t` for tabs in `content=`.

## Search, links, and structure

```bash
obsidian search query="text" [path=folder] [limit=n] [format=text|json] [total] [case]
obsidian search:context query="text" [path=folder] [limit=n]  # includes surrounding context
obsidian links [file=Note] [total]
obsidian backlinks [file=Note] [counts] [total]
obsidian outline [file=Note] [format=tree|md]
obsidian orphans [total] [active]       # notes with no links to or from them
obsidian deadends [total] [active]      # notes with no outgoing links
obsidian unresolved [total] [counts] [verbose]  # broken wikilinks
obsidian tags [active] [file=Note] [total] [counts] [sort=count]
obsidian tag name=project [total] [verbose]
```

## Common patterns

### Notes and content

To peek at a note without reading its full content, use `property:read` or `properties file=Note`.

```bash
obsidian read file="Note" # Use this to read the content of a wikilink
obsidian create name="Note" content="# Title\n\nBody" [template=Name] [overwrite] [silent]
obsidian append file="Note" content="- [ ] Task"
obsidian prepend file="Note" content="# Header\n"
obsidian move file="Note" to=folder/newpath.md
obsidian rename file="Note" name="New file name"
obsidian delete file="Note"
```

### Daily notes (Daily notes plugin)

```bash
obsidian daily:read
obsidian daily [paneType=tab|split|window] [open]
obsidian daily:append content="- [ ] Buy groceries" [inline] [open]
obsidian daily:prepend content="- [ ] Morning routine" [inline]  # goes after frontmatter
obsidian daily:path  # returns expected path even if file doesn't exist yet
```

### Tasks

```bash
obsidian tasks [daily] [file=Note] [todo] [done] [status="x"] [total] [verbose]
obsidian task ref=path:line [toggle] [done] [todo] [daily]
```

### Properties and frontmatter

```bash
obsidian properties [active] [file=Note] [total] [counts] [format=yaml|json|tsv]
obsidian property:read name=status [file=Note]
obsidian property:set name=status value=done [file=Note]
obsidian property:remove name=status [file=Note]
```

### Bases (Bases plugin)

```bash
obsidian bases
obsidian base:views [file=base.base]
obsidian base:query [file=base.base] [view=name] [format=json|csv|tsv|md|paths]
obsidian base:create name="Item" content="..." [open] [newtab]
```

## Developer commands

Reload a plugin after code changes — essential for the develop/test cycle:

```bash
obsidian plugin:reload id=my-plugin
obsidian eval code="app.vault.getFiles().length"
obsidian dev:screenshot path=screenshot.png
obsidian dev:dom selector=".cm-editor" [text] [attr=class]
obsidian dev:css selector=".cm-editor" [prop=color]
obsidian dev:console [clear] [limit=10] [level=log|warn|error]
obsidian dev:errors [clear]
```

## Quick reference

| Task                       | Command                                      |
| -------------------------- | -------------------------------------------- |
| List commands              | `obsidian help`                              |
| Open daily note            | `obsidian daily`                             |
| Append to daily            | `obsidian daily:append content="- [ ] Task"` |
| Search vault               | `obsidian search query="text"`               |
| Read active/specified file | `obsidian read` or `obsidian read file=Note` |
| Create from template       | `obsidian create name="Title" template=Name` |
| List tags with counts      | `obsidian tags counts`                       |
| List tasks from daily      | `obsidian tasks daily`                       |
| Find broken wikilinks      | `obsidian unresolved counts`                 |
| Find orphan notes          | `obsidian orphans`                           |

## References

- `obsidian help` — full command list (always up to date)
- `obsidian help <command>` — help for a specific command
- [Obsidian CLI docs (Obsidian)](https://raw.githubusercontent.com/obsidianmd/obsidian-help/refs/heads/master/en/Extending%20Obsidian/Obsidian%20CLI.md)
